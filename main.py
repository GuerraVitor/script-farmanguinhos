from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import re
import numpy as np

# Configuração do WebDriver
service = Service(executable_path="chromedriver.bin")
driver = webdriver.Chrome()

# Acessa o site do Busca Lattes e maximiza a janela
driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do")
driver.maximize_window()

# Configuração de espera explícita
wait = WebDriverWait(driver, 10)

# Navega para a busca avançada
buscaavancada = driver.find_element(By.CSS_SELECTOR, "div#tit_simples.control-bar-top")
buscaavancadabutton = buscaavancada.find_element(By.TAG_NAME, 'a')
buscaavancadabutton.click()

# Preenche o campo de busca com os termos desejados
input_element = driver.find_element(By.CSS_SELECTOR, "textarea.input-text.min-height")
input_element.clear()
input_element.send_keys('(oncológicos OR oncology OR anticâncer OR anticancer OR antineoplásicos OR antineoplastic OR anticancerígeno OR anticancer OR antineoplásicas OR antitumoral OR antitumor OR quimioterápicos OR chemotherapy OR tumor OR neoplasm OR neoplasia) AND (câncer OR cancer OR neoplasm OR Leukemia OR Carcinoma OR Astrocytoma OR Astrocitoma OR Sarcoma OR Lymphoma or Linfoma OR cholangiocarcinoma or Colangiocarcinoma OR osteosarcoma or Osteossarcoma OR Histiocytoma OR fibro-histiocitoma OR ependymoma OR Ependimoma OR Medulloblastoma OR Meduloblastoma OR blastoma OR Hodgkin OR Non-Hodgkin OR Chordoma OR Cordoma OR adenocarcinoma OR Esthesioneuroblastoma OR Estesioneuroblastoma OR neuroblastoma OR Retinoblastoma OR melanoma OR mesothelioma OR esotelioma OR rhabdomyosarcoma OR rabdomiosarcoma OR glioblastoma)')

# Realiza a busca
botaopesquisa = driver.find_element(By.CSS_SELECTOR, "a#botaoBuscaFiltros.button")
botaopesquisa.click()

# Aguarda o carregamento dos resultados
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class = 'resultado']"))
)

# Inicializa o dicionário para armazenar os resultados
output_file = "/home/vitor/Projects/fiocruz/selenium-lattes/output.list"
buffer = []  # Lista para acumular os dados até a escrita no arquivo

# Obtém o número total de currículos e páginas
el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
listsize = el.find_elements(By.TAG_NAME, "li")
time.sleep(2)

numero = driver.find_element(By.CSS_SELECTOR, "div[class = 'tit_form'] b").text
numero = int(np.ceil(int(numero) / 10))

# Variáveis de controle
traffic = 2

def fechar_modal_se_existir(driver):
    try:
        close = driver.find_element(By.ID, "idbtnfechar")
        close.click()
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "idbtnfechar"))
        )
    except NoSuchElementException:
        pass

# Itera pelas páginas de resultados
for j in range(numero):
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
            try:
                link.click()
            except ElementClickInterceptedException:
                fechar_modal_se_existir(driver)
                link.click()

            # Aguarda o botão "Abrir Currículo" estar clicável e clica nele pelo ID
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idbtnabrircurriculo"))
            )
            curriculo = driver.find_element(By.ID, "idbtnabrircurriculo")
            try:
                curriculo.click()
            except ElementClickInterceptedException:
                fechar_modal_se_existir(driver)
                curriculo.click()

            # Alterna para a nova janela
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])

            # Extrai informações do currículo
            nome = driver.find_element(By.CLASS_NAME, "nome").text
            ul = driver.find_elements(By.TAG_NAME, "li")
            string = ul[1].text
            idlattes = re.findall(r'\d+', string)[0]

            # Adiciona os dados ao buffer
            buffer.append(f"{idlattes} , {nome}")

            # Salva os dados no arquivo quando o buffer atingir 2 itens
            if len(buffer) == 2:
                with open(output_file, "a", encoding="utf-8") as file:
                    file.write("\n".join(buffer) + "\n")
                buffer.clear()  # Limpa o buffer após salvar

            # Fecha a janela do currículo e retorna à janela principal
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            fechar_modal_se_existir(driver)
            
        except Exception as e:
            print(e)
            fechar_modal_se_existir(driver)
    
    # Navega para a próxima página
    try:
        page.click()
    except ElementClickInterceptedException:
        fechar_modal_se_existir(driver)
        page.click()
    time.sleep(3)
    traffic += 1

# Salva os dados restantes no buffer (se houver)
if buffer:
    with open(output_file, "a", encoding="utf-8") as file:
        file.write("\n".join(buffer) + "\n")

# Aguarda antes de encerrar o WebDriver
time.sleep(10)
driver.quit()