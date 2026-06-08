import logging
import math
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

# --- Configuration ---
OUTPUT_FILE = "/home/vitor/Projects/fiocruz/selenium-lattes/output.list"
SEARCH_QUERY = '(oncológicos OR oncology OR anticâncer OR anticancer OR antineoplásicos OR antineoplastic OR anticancerígeno OR anticancer OR antineoplásicas OR antitumoral OR antitumor OR quimioterápicos OR chemotherapy OR tumor OR neoplasm OR neoplasia) AND (câncer OR cancer OR neoplasm OR Leukemia OR Carcinoma OR Astrocytoma OR Astrocitoma OR Sarcoma OR Lymphoma or Linfoma OR cholangiocarcinoma or Colangiocarcinoma OR osteosarcoma or Osteossarcoma OR Histiocytoma OR fibro-histiocitoma OR ependymoma OR Ependimoma OR Medulloblastoma OR Meduloblastoma OR blastoma OR Hodgkin OR Non-Hodgkin OR Chordoma OR Cordoma OR adenocarcinoma OR Esthesioneuroblastoma OR Estesioneuroblastoma OR neuroblastoma OR Retinoblastoma OR melanoma OR mesothelioma OR esotelioma OR rhabdomyosarcoma OR rabdomiosarcoma OR glioblastoma)'

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def fechar_modal_se_existir(driver):
    try:
        close = driver.find_element(By.ID, "idbtnfechar")
        if close.is_displayed():
            driver.execute_script("arguments[0].click();", close)
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located((By.ID, "idbtnfechar"))
            )
            logger.debug("Modal fechado com sucesso.")
    except Exception as e:
        pass

def main():
    logger.info("Iniciando o script de extração do Lattes.")

    # Configuração do WebDriver
    driver = webdriver.Chrome()

    try:
        # Acessa o site do Busca Lattes e maximiza a janela
        logger.info("Acessando o Busca Lattes...")
        driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do")
        driver.maximize_window()

        # Configuração de espera explícita
        wait = WebDriverWait(driver, 10)

        # Navega para a busca avançada
        logger.info("Navegando para a busca avançada...")
        buscaavancada = driver.find_element(By.CSS_SELECTOR, "div#tit_simples.control-bar-top")
        buscaavancadabutton = buscaavancada.find_element(By.TAG_NAME, 'a')
        buscaavancadabutton.click()

        # Preenche o campo de busca com os termos desejados
        logger.info("Preenchendo o campo de busca...")
        input_element = driver.find_element(By.CSS_SELECTOR, "textarea.input-text.min-height")
        input_element.clear()
        input_element.send_keys(SEARCH_QUERY)

        # Realiza a busca
        logger.info("Executando a busca...")
        botaopesquisa = driver.find_element(By.CSS_SELECTOR, "a#botaoBuscaFiltros.button")
        botaopesquisa.click()

        # Aguarda o carregamento dos resultados
        logger.info("Aguardando carregamento dos resultados...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class = 'resultado']"))
        )

        # Inicializa o dicionário para armazenar os resultados
        buffer = []  # Lista para acumular os dados até a escrita no arquivo

        # Obtém o número total de currículos e páginas
        time.sleep(2)
        numero_element = driver.find_element(By.CSS_SELECTOR, "div[class = 'tit_form'] b")
        total_curriculos = int(numero_element.text)
        numero_paginas = math.ceil(total_curriculos / 10)

        logger.info(f"Total de currículos encontrados: {total_curriculos}")
        logger.info(f"Total de páginas a processar: {numero_paginas}")

        # Variáveis de controle
        traffic = 2

        # Itera pelas páginas de resultados
        for j in range(numero_paginas):
            logger.info(f"Processando página {j + 1} de {numero_paginas}...")

            if traffic % 10 == 0:
                page = driver.find_element(By.LINK_TEXT, "próximo")
            else:
                page = driver.find_element(By.LINK_TEXT, str(traffic))

            el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
            listsize = el.find_elements(By.TAG_NAME, "li")

            # Itera pelos currículos na página
            for i in range(len(listsize)):
                try:
                    element = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
                    lista = element.find_elements(By.TAG_NAME, "li")
                    link = lista[i].find_element(By.TAG_NAME, "a")

                    # Rola a tela até o elemento para garantir visibilidade
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                    time.sleep(0.5)

                    # Usamos JS para abrir o painel pois não gera popup (evita problemas com menus fixos interceptando o click)
                    driver.execute_script("arguments[0].click();", link)

                    # Aguarda o botão "Abrir Currículo" ficar visível
                    wait.until(EC.visibility_of_element_located((By.ID, "idbtnabrircurriculo")))
                    curriculo = driver.find_element(By.ID, "idbtnabrircurriculo")

                    # Pausa curta para garantir que o script do painel atrelou o evento de nova janela ao botão
                    time.sleep(1)

                    # Tenta clicar nativamente no botão. Se o navegador ignorar ou a aba não abrir, tenta de novo.
                    window_opened = False
                    for attempt in range(4):
                        try:
                            curriculo.click()
                        except ElementClickInterceptedException:
                            time.sleep(1)
                            continue

                        try:
                            # Aguarda até 4 segundos para ver se a nova aba realmente abriu após este clique
                            WebDriverWait(driver, 4).until(EC.number_of_windows_to_be(2))
                            window_opened = True
                            break
                        except TimeoutException:
                            logger.debug(f"Aba não abriu. Clicando novamente em 'Abrir Currículo' (tentativa {attempt+1}).")
                            continue

                    if not window_opened:
                        raise Exception("Timeout: Falha ao tentar abrir a nova aba do currículo.")

                    # Alterna para a nova janela
                    driver.switch_to.window(driver.window_handles[1])

                    # Aguarda o carregamento do currículo (o elemento do nome) antes de extrair os dados
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nome")))

                    # Extrai informações do currículo
                    nome = driver.find_element(By.CLASS_NAME, "nome").text
                    ul = driver.find_elements(By.TAG_NAME, "li")
                    string = ul[1].text
                    idlattes = re.findall(r'\d+', string)[0]

                    logger.info(f"Dados extraídos com sucesso - Nome: {nome}, ID Lattes: {idlattes}")

                    # Adiciona os dados ao buffer
                    buffer.append(f"{idlattes} , {nome}")

                    # Salva os dados no arquivo quando o buffer atingir 2 itens
                    if len(buffer) == 2:
                        with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
                            file.write("\n".join(buffer) + "\n")
                        logger.debug("Buffer salvo no arquivo e limpo.")
                        buffer.clear()  # Limpa o buffer após salvar

                    # Fecha a janela do currículo e retorna à janela principal
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    fechar_modal_se_existir(driver)

                except Exception as e:
                    logger.error(f"Erro ao processar currículo {i + 1} da página {j + 1}: {e}", exc_info=True)
                    # Recupera o estado das janelas caso ocorra erro com a aba do currículo aberta
                    while len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    fechar_modal_se_existir(driver)

            # Navega para a próxima página
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", page)
            time.sleep(3)
            traffic += 1

        # Salva os dados restantes no buffer (se houver)
        if buffer:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
                file.write("\n".join(buffer) + "\n")
            logger.info("Dados remanescentes salvos no arquivo.")

    except Exception as e:
        logger.critical(f"Erro crítico durante a execução do script: {e}")
    finally:
        # Aguarda antes de encerrar o WebDriver e garante que sempre será fechado
        logger.info("Encerrando o WebDriver...")
        time.sleep(2)
        driver.quit()
        logger.info("Script finalizado.")

if __name__ == "__main__":
    main()
