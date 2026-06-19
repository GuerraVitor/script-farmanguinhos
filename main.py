"""
Main module for the Script Lattes data extractor.

This script automates the extraction of researchers' CV data from the
CNPq Lattes Platform using Playwright.
"""

import argparse
import logging
import math
import os
import re
import time
from typing import List, Optional, Tuple

from playwright.sync_api import (
    BrowserContext,
    Page,
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- Configuration Variables ---
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.list")
SEARCH_QUERY = "(Farmanguinhos)"
MAX_CURRICULOS = 20


def close_modal_if_exists(page: Page) -> None:
    """
    Closes the current modal on the page if it is visible.

    Args:
        page (Page): The current Playwright page instance.
    """
    try:
        close_btn = page.locator("#idbtnfechar")
        if close_btn.is_visible():
            close_btn.evaluate("node => node.click()")
            close_btn.wait_for(state="hidden", timeout=3000)
            logger.debug("Modal fechado com sucesso.")
    except Exception as e:
        logger.debug(f"Erro ao fechar modal ou modal não encontrado: {e}")


def save_buffer(buffer: List[str], output_file: str) -> None:
    """
    Saves the extracted Lattes IDs and names to the output file.

    Args:
        buffer (List[str]): List of strings containing formatted Lattes data.
        output_file (str): The path to the output file.
    """
    if not buffer:
        return

    try:
        with open(output_file, "a", encoding="utf-8") as file:
            file.write("\n".join(buffer) + "\n")
        logger.debug("Buffer salvo no arquivo.")
        buffer.clear()
    except IOError as e:
        logger.error(f"Erro ao salvar buffer no arquivo: {e}")


def execute_initial_search(page: Page, query: str) -> None:
    """
    Navigates to the CNPq Lattes search page and performs the initial search.

    Args:
        page (Page): The Playwright page instance.
        query (str): The search query to be used.
    """
    logger.info("Acessando o Busca Lattes")
    page.goto("https://buscatextual.cnpq.br/buscatextual/busca.do")

    logger.info("Navegando para a busca avançada")
    page.locator("div#tit_simples.control-bar-top a").click()

    logger.info("Preenchendo o campo de busca")
    input_element = page.locator("textarea.input-text.min-height")
    input_element.clear()
    input_element.fill(query)

    logger.info("Executando a busca")
    page.locator("a#botaoBuscaFiltros.button").click()

    logger.info("Aguardando carregamento dos resultados")
    page.wait_for_selector("div.resultado", timeout=10000)


def extract_curriculum_data(
    context: BrowserContext, main_page: Page, index: int
) -> Optional[Tuple[str, str]]:
    """
    Extracts the Lattes ID and name of a researcher from the search results.

    Args:
        context (BrowserContext): The Playwright browser context.
        main_page (Page): The main search results page.
        index (int): The index of the curriculum item in the results list.

    Returns:
        Optional[Tuple[str, str]]: A tuple containing the Lattes ID and Name,
        or None if extraction fails.
    """
    resultado_div = main_page.locator("div.resultado")
    lista = resultado_div.locator("li")
    link = lista.nth(index).locator("a").first

    link.scroll_into_view_if_needed()
    time.sleep(0.5)

    link.evaluate("node => node.click()")

    curriculo_btn = main_page.locator("#idbtnabrircurriculo")
    curriculo_btn.wait_for(state="visible", timeout=10000)
    time.sleep(1)

    new_page = None
    window_opened = False

    for attempt in range(4):
        try:
            with context.expect_page(timeout=4000) as new_page_info:
                curriculo_btn.click(force=True)
            new_page = new_page_info.value
            window_opened = True
            break
        except PlaywrightTimeoutError:
            logger.debug(f"Aba não abriu. Tentativa {attempt + 1}.")
            continue

    if not window_opened or not new_page:
        raise Exception("Timeout: Falha ao tentar abrir a nova aba do currículo.")

    try:
        new_page.wait_for_selector(".nome", timeout=10000)
        time.sleep(3)
        nome = new_page.locator(".nome").first.text_content()
        nome = nome.strip() if nome else "NOME_NAO_ENCONTRADO"

        ul_items = new_page.locator("li").all()
        lattes_id = None
        for item in ul_items:
            text = item.text_content() or ""
            if "Endereço para acessar este CV:" in text:
                matches = re.findall(r"\d{16}", text)
                if matches:
                    lattes_id = matches[0]
                    break

        if not lattes_id:
            content = new_page.content()
            matches = re.findall(r"\d{16}", content)
            lattes_id = matches[0] if matches else "ID_NAO_ENCONTRADO"

        return lattes_id, nome
    finally:
        new_page.close()


def navigate_to_next_page(page: Page, traffic_index: int) -> None:
    """
    Navigates to the next page of search results.

    Args:
        page (Page): The Playwright page instance.
        traffic_index (int): The current pagination index for locating the next button.
    """
    if traffic_index % 10 == 0:
        page_link = page.get_by_role("link", name="próximo").first
    else:
        page_link = page.get_by_role("link", name=str(traffic_index), exact=True).first

    page_link.scroll_into_view_if_needed()
    time.sleep(0.5)
    page_link.evaluate("node => node.click()")
    time.sleep(3)


def calculate_total_pages(page: Page) -> int:
    """
    Calculates the total number of pages based on the search results.

    Args:
        page (Page): The Playwright page instance.

    Returns:
        int: The total number of pages to process.
    """
    numero_element = page.locator("div.tit_form b").first
    total_text = numero_element.text_content()

    if not total_text:
        logger.warning("Não foi possível encontrar o total de currículos. Retornando 1 página.")
        return 1

    total_curriculos = int(total_text)
    numero_paginas = math.ceil(total_curriculos / 10)

    logger.info(f"Total de currículos encontrados: {total_curriculos}")
    logger.info(f"Total de páginas a processar: {numero_paginas}")

    return numero_paginas


def run_extraction_pipeline() -> None:
    """
    Runs the complete extraction pipeline.
    """
    logger.info("Iniciando o script de extração.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            execute_initial_search(page, SEARCH_QUERY)
            time.sleep(2)

            total_pages = calculate_total_pages(page)

            buffer: List[str] = []
            traffic_index = 2
            total_saved = 0

            for page_index in range(total_pages):
                logger.info(f"Processando página {page_index + 1} de {total_pages}...")

                resultado_div = page.locator("div.resultado")
                items_count = resultado_div.locator("li").count()

                for item_index in range(items_count):
                    try:
                        dados = extract_curriculum_data(context, page, item_index)
                        if dados:
                            lattes_id, nome = dados
                            logger.info(f"Dados extraídos com sucesso - Nome: {nome}, ID Lattes: {lattes_id}")
                            buffer.append(f"{lattes_id} , {nome}")
                            total_saved += 1

                            if len(buffer) >= 2:
                                save_buffer(buffer, OUTPUT_FILE)

                        close_modal_if_exists(page)

                        if MAX_CURRICULOS > 0 and total_saved >= MAX_CURRICULOS:
                            logger.info(f"Limite máximo de {MAX_CURRICULOS} currículos atingido.")
                            break

                    except Exception as e:
                        logger.error(f"Erro ao processar currículo {item_index + 1} da página {page_index + 1}: {e}")
                        for aba in context.pages:
                            if aba != page:
                                aba.close()
                        close_modal_if_exists(page)

                if MAX_CURRICULOS > 0 and total_saved >= MAX_CURRICULOS:
                    break

                if page_index < total_pages - 1:
                    navigate_to_next_page(page, traffic_index)
                    traffic_index += 1

            save_buffer(buffer, OUTPUT_FILE)
            logger.info(f"Extração concluída. Total de currículos salvos: {total_saved}")

        except Exception as e:
            logger.critical(f"Erro crítico durante a execução do script: {e}")
        finally:
            logger.info("Encerrando o Playwright")
            time.sleep(2)
            context.close()
            browser.close()
            logger.info("Script finalizado.")


def main() -> None:
    """Entry point of the script."""
    global SEARCH_QUERY, MAX_CURRICULOS

    parser = argparse.ArgumentParser(description="Script Lattes data extractor.")
    parser.add_argument("--query", type=str, help="Search query to be used.")
    parser.add_argument("--max", type=int, help="Maximum number of curricula to extract (0 for unlimited).")

    args = parser.parse_args()

    if args.query:
        SEARCH_QUERY = args.query
    if args.max is not None:
        MAX_CURRICULOS = args.max

    run_extraction_pipeline()


if __name__ == "__main__":
    main()
