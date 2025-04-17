from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv
import numpy as np
import os

# Configuração do WebDriver
service = Service(executable_path="chromedriver.bin")
driver = webdriver.Chrome()

# Acessa o site do Busca Lattes e maximiza a janela
driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do")
driver.maximize_window()

# Configuração de espera explícita
wait = WebDriverWait(driver, 10)

# Armazena a janela original
original_window = driver.current_window_handle

# Navega para a busca avançada
buscaavancada = driver.find_element(By.CSS_SELECTOR, "div#tit_simples.control-bar-top")
buscaavancadabutton = buscaavancada.find_element(By.TAG_NAME, 'a')
buscaavancadabutton.click()

# Preenche o campo de busca com os termos desejados
input_element = driver.find_element(By.CSS_SELECTOR, "textarea.input-text.min-height")
input_element.clear()
input_element.send_keys('(oncológicos OR oncology OR anticâncer OR anticancer OR antineoplásicos OR antineoplastic OR anticancerígeno OR anticancer OR antineoplásicas OR antitumoral OR antitumor OR quimioterápicos OR chemotherapy OR tumor OR neoplasm OR neoplasia) AND (câncer OR cancer OR neoplasm OR Leukemia OR Carcinoma OR Astrocytoma OR Astrocitoma OR Sarcoma OR Lymphoma or Linfoma OR cholangiocarcinoma or Colangiocarcinoma OR osteosarcoma or Osteossarcoma OR Histiocytoma OR fibro-histiocitoma OR ependymoma OR Ependimoma OR Medulloblastoma OR Meduloblastoma OR blastoma OR Hodgkin OR Non-Hodgkin OR Chordoma OR Cordoma OR adenocarcinoma OR Esthesioneuroblastoma OR Estesioneuroblastoma OR neuroblastoma OR Retinoblastoma OR melanoma OR mesothelioma OR esotelioma OR rhabdomyosarcoma OR rabdomiosarcoma OR glioblastoma)')

# Seleciona filtros de busca
bolsproducnpqbutton = driver.find_element(By.CSS_SELECTOR, "input#filtro0")
bolsproducnpqbutton.click()

# Seleciona categorias de bolsas
for checkbox_id in ["checkbox1A", "checkbox1B", "checkbox1C", "checkbox1D", "checkbox2"]:
    driver.find_element(By.CSS_SELECTOR, f"input#{checkbox_id}").click()

# Aplica os filtros de bolsas
aplicarcnpqbutton = driver.find_element(By.CSS_SELECTOR, "a#preencheCategoriaNivelBolsa.button")
aplicarcnpqbutton.click()

# Seleciona filtros adicionais
gruposdepesquisabutton = driver.find_element(By.CSS_SELECTOR, "input#filtro9")
gruposdepesquisabutton.click()
filtrobutton = driver.find_element(By.CSS_SELECTOR, "input#participaDGP")
filtrobutton.click()
time.sleep(7)

# Seleciona área de atuação profissional
atuacaoprofissionalbutton = driver.find_element(By.CSS_SELECTOR, "input#filtro4")
atuacaoprofissionalbutton.click()

# Seleciona grande área e área de atuação
selectprofissao = driver.find_element(By.CSS_SELECTOR, "select#codigoGrandeAreaAtuacao.input-text")
Select(selectprofissao).select_by_value('40000001')
time.sleep(2)

selectarea = driver.find_element(By.CSS_SELECTOR, "select#codigoAreaAtuacao.input-text")
Select(selectarea).select_by_value('40100006')
time.sleep(7)

# Realiza a busca
botaopesquisa = driver.find_element(By.CSS_SELECTOR, "a#botaoBuscaFiltros.button")
botaopesquisa.click()

# Aguarda o carregamento dos resultados
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class = 'resultado']"))
)

# Inicializa o dicionário para armazenar os resultados
dictionary = {}

# Obtém o número total de currículos e páginas
el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
listsize = el.find_elements(By.TAG_NAME, "li")
time.sleep(2)

numero = driver.find_element(By.CSS_SELECTOR, "div[class = 'tit_form'] b").text
numero = int(np.ceil(int(numero) / 10))

# Variáveis de controle
perfis = 0
traffic = 2

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
            link.click()

            # Aguarda o botão "Abrir Currículo" e clica nele
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a#idbtnabrircurriculo.button"))
            )
            curriculo = driver.find_element(By.PARTIAL_LINK_TEXT, value="Abrir Currículo")
            time.sleep(4)
            curriculo.click()

            # Alterna para a nova janela
            wait.until(EC.number_of_windows_to_be(2))
            handles = driver.window_handles
            driver.switch_to.window(handles[1])

            # Extrai informações do currículo
            nome = driver.find_element(By.CLASS_NAME, "nome").text
            ul = driver.find_elements(By.TAG_NAME, "li")
            string = ul[1].text
            idlattes = re.findall(r'\d+', string)[0]

            # Atualiza o dicionário com os dados extraídos
            perfis += 1
            print(f'O número de perfis visualizados foi de: {perfis}')
            dictionary.update({nome: idlattes})
            print(dictionary)

            # Fecha a janela do currículo e retorna à janela principal
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Fecha o modal
            close = driver.find_element(By.ID, "idbtnfechar")
            close.click()
            
        except Exception as e:
            print(e)
    
    # Navega para a próxima página
    page.click()
    time.sleep(3)
    traffic += 1

# salva dicionario final
output_file = "/home/vitor/projects/fiocruz/selenium-bot/seleniumlattes/output.list"
with open(output_file, "w", encoding="utf-8") as file:
    for nome, idlattes in dictionary.items():
        file.write(f"{idlattes} , {nome}\n")


# Aguarda antes de encerrar o WebDriver
time.sleep(10)
driver.quit()