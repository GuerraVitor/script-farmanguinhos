import logging
import math
import re
import time
from typing import List, Optional, Tuple
import os
from playwright.sync_api import sync_playwright, Page, BrowserContext,TimeoutError as PlaywrightTimeoutError

# --- Configuration ---
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.list")
SEARCH_QUERY = '(Farmanguinhos)'
MAX_CURRICULOS = 20

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def fechar_modal_se_existir(page: Page) -> None:
    try:
        close_btn = page.locator("#idbtnfechar")
        if close_btn.is_visible():
            close_btn.evaluate("node => node.click()")
            close_btn.wait_for(state="hidden", timeout=3000)
            logger.debug("Modal fechado com sucesso.")
    except Exception:
        pass


def salvar_buffer(buffer: List[str], arquivo_saida: str) -> None:
    if not buffer:
        return

    with open(arquivo_saida, "a", encoding="utf-8") as file:
        file.write("\n".join(buffer) + "\n")
    logger.debug("Buffer salvo no arquivo.")
    buffer.clear()


def executar_busca_inicial(page: Page, query: str) -> None:
    logger.info("Acessando o Busca Lattes...")
    page.goto("https://buscatextual.cnpq.br/buscatextual/busca.do")

    logger.info("Navegando para a busca avançada...")
    page.locator("div#tit_simples.control-bar-top a").click()

    logger.info("Preenchendo o campo de busca...")
    input_element = page.locator("textarea.input-text.min-height")
    input_element.clear()
    input_element.fill(query)

    logger.info("Executando a busca...")
    page.locator("a#botaoBuscaFiltros.button").click()

    logger.info("Aguardando carregamento dos resultados...")
    page.wait_for_selector("div.resultado", timeout=10000)


def extrair_dados_curriculo(context: BrowserContext, main_page: Page, indice: int) -> Optional[Tuple[str, str]]:
    resultado_div = main_page.locator("div.resultado")
    lista = resultado_div.locator("li")
    link = lista.nth(indice).locator("a").first

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
        nome = new_page.locator(".nome").first.text_content().strip()

        ul_items = new_page.locator("li").all()
        idlattes = None
        for item in ul_items:
            text = item.text_content()
            if "Endereço para acessar este CV:" in text:
                matches = re.findall(r'\d{16}', text)
                if matches:
                    idlattes = matches[0]
                    break

        if not idlattes:
            matches = re.findall(r'\d{16}', new_page.content())
            idlattes = matches[0] if matches else "ID_NAO_ENCONTRADO"

        return idlattes, nome
    finally:
        new_page.close()


def navegar_proxima_pagina(page: Page, traffic_index: int) -> None:
    if traffic_index % 10 == 0:
        page_link = page.get_by_role("link", name="próximo").first
    else:
        page_link = page.get_by_role("link", name=str(traffic_index), exact=True).first

    page_link.scroll_into_view_if_needed()
    time.sleep(0.5)
    page_link.evaluate("node => node.click()")
    time.sleep(3)


def main() -> None:
    logger.info("Iniciando o script de extração do Lattes.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            executar_busca_inicial(page, SEARCH_QUERY)

            time.sleep(2)
            numero_element = page.locator("div.tit_form b").first
            total_curriculos = int(numero_element.text_content())
            numero_paginas = math.ceil(total_curriculos / 10)

            logger.info(f"Total de currículos encontrados: {total_curriculos}")
            logger.info(f"Total de páginas a processar: {numero_paginas}")

            buffer: List[str] = []
            traffic = 2
            total_salvos = 0

            for j in range(numero_paginas):
                logger.info(f"Processando página {j + 1} de {numero_paginas}...")

                resultado_div = page.locator("div.resultado")
                quantidade_items = resultado_div.locator("li").count()

                for i in range(quantidade_items):
                    try:
                        dados = extrair_dados_curriculo(context, page, i)
                        if dados:
                            idlattes, nome = dados
                            logger.info(f"Dados extraídos com sucesso - Nome: {nome}, ID Lattes: {idlattes}")
                            buffer.append(f"{idlattes} , {nome}")
                            total_salvos += 1

                            if len(buffer) >= 2:
                                salvar_buffer(buffer, OUTPUT_FILE)

                        fechar_modal_se_existir(page)

                        if MAX_CURRICULOS > 0 and total_salvos >= MAX_CURRICULOS:
                            logger.info(f"Limite máximo de {MAX_CURRICULOS} currículos atingido.")
                            break

                    except Exception as e:
                        logger.error(f"Erro ao processar currículo {i + 1} da página {j + 1}: {e}")
                        for aba in context.pages:
                            if aba != page:
                                aba.close()
                        fechar_modal_se_existir(page)

                if MAX_CURRICULOS > 0 and total_salvos >= MAX_CURRICULOS:
                    break

                if j < numero_paginas - 1:
                    navegar_proxima_pagina(page, traffic)
                    traffic += 1

            salvar_buffer(buffer, OUTPUT_FILE)
            logger.info(f"Extração concluída. Total de currículos salvos: {total_salvos}")

        except Exception as e:
            logger.critical(f"Erro crítico durante a execução do script: {e}")
        finally:
            logger.info("Encerrando o WebDriver...")
            time.sleep(2)
            context.close()
            browser.close()
            logger.info("Script finalizado.")


if __name__ == "__main__":
    main()
