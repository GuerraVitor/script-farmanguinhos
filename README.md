# Lattes Extractor (Bot) 🤖🎓

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated-2EAD33.svg)](https://playwright.dev/python/)

*Looking for the Portuguese version? [Click here to read in Portuguese](#extrator-lattes-bot-). / Procurando a versão em Português? [Clique aqui](#extrator-lattes-bot-).*

A web automation bot built with **Python** and **Playwright** designed to collect public data from the [Currículo Lattes](http://buscatextual.cnpq.br/buscatextual/busca.do) textual search.

This project performs automated searches, handles result pagination, opens resumes, and extracts the 16-digit Lattes ID and the researcher's name, saving the output in a clean `.list` format.

Originally created by Francisco Florêncio, this codebase has been refactored and migrated from Selenium to Playwright by Vitor Guerra. This transition ensures faster execution, better implicit wait handling, and more robust cross-tab management.

## Features
- **Automated Searching:** Directly interfaces with the advanced search field of the CNPq Lattes platform.
- **Robust Extraction:** Capable of handling pop-ups and multiple browser tabs seamlessly using Playwright.
- **Data Export:** Outputs a structured `output.list` file ready for ingestion by downstream processing tools.
- **Pipeline Integration:** Native support for piping data directly into the [scriptLattes](https://github.com/scriptlattes/scriptlattes) ecosystem.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder-name>
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or: venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Playwright Chromium browser:**
   ```bash
   playwright install chromium
   ```

## ⚙️ Configuration

In the `main.py` file, there is a configuration section at the top. You can adjust the following parameters:

- `SEARCH_QUERY`: The exact search string the bot will input into the Lattes advanced search.
- `MAX_CURRICULOS`: The maximum number of resumes you want to extract per execution (useful for testing).
  - *Example:* `MAX_CURRICULOS = 50`
  - *Disable limit:* Set to `0` to extract all found results.

## Usage

There are two primary ways to run this project:

### 1. Standalone Execution (Extraction Only)
To simply generate the `output.list` containing the extracted names and Lattes IDs, run the main script:
```bash
python main.py
```
The file will be saved in the root directory of the project.

### 2. Integrated Pipeline (`scriptLattes`)
If this project is part of a larger workflow utilizing [scriptLattes](https://github.com/scriptlattes/scriptlattes), you can automate the entire pipeline using `run_pipeline.py`.

The pipeline script automatically:
1. Runs the extractor bot (`main.py`) to generate the updated list.
2. Moves the `output.list` file into the neighboring `scriptLattes` folder.
3. Invokes the `scriptLattes` virtual environment to generate its reports.

**Prerequisites for Pipeline Integration:**
- The `scriptLattes` directory must be in the same parent folder as this project (side-by-side).
- The `scriptLattes` folder must have its own configured virtual environment (`venv`) with all its dependencies installed.

**Run the pipeline:**
```bash
python run_pipeline.py
```

---
---

# Extrator Lattes (Bot) 🤖🎓

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Automatizado-2EAD33.svg)](https://playwright.dev/python/)

Um bot de automação web construído com **Python** e **Playwright** projetado para coletar dados públicos na busca textual do [Currículo Lattes](http://buscatextual.cnpq.br/buscatextual/busca.do).

Este projeto realiza pesquisas automatizadas, navega pela paginação de resultados, abre os currículos e extrai o ID Lattes (16 dígitos) e o nome dos pesquisadores, salvando a saída em um formato limpo de `.list`.

Originalmente criado por Francisco Florêncio, este código-fonte foi totalmente refatorado e migrado do Selenium para o Playwright por Vitor Guerra. A transição garante execução mais rápida, melhor manipulação de esperas (waits) e gerenciamento mais robusto de abas no navegador.

## ✨ Funcionalidades
- **Busca Automatizada:** Interage diretamente com o campo de busca avançada da plataforma Lattes (CNPq).
- **Extração Robusta:** Capaz de lidar com modais (pop-ups) e múltiplas abas de navegador de forma nativa e fluida com Playwright.
- **Exportação de Dados:** Gera um arquivo `output.list` estruturado, pronto para consumo por outras ferramentas.
- **Integração via Pipeline:** Suporte nativo para enviar os dados diretamente para o ecossistema [scriptLattes](https://github.com/scriptlattes/scriptlattes).

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <nome-da-pasta-do-repositorio>
   ```

2. **Configure um ambiente virtual Python:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Linux/macOS
   # ou: venv\Scripts\activate no Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instale o navegador do Playwright:**
   ```bash
   playwright install chromium
   ```

## ⚙️ Configuração

Dentro do arquivo `main.py`, existe uma sessão de configuração logo no topo do script. Você pode modificar as seguintes variáveis:

- `SEARCH_QUERY`: A string de busca exata que o robô irá digitar no site do Lattes.
- `MAX_CURRICULOS`: O limite máximo de currículos que você deseja extrair em uma execução (útil para testes rápidos).
  - *Exemplo:* `MAX_CURRICULOS = 50`
  - *Desativar limite:* Defina o valor como `0` para extrair todos os resultados encontrados pela busca.

## Como Usar

Existem duas formas principais de utilizar o projeto:

### 1. Execução Simples (Apenas Extração)
Se você deseja apenas gerar o arquivo `output.list` contendo os nomes e IDs extraídos, basta executar o script principal:
```bash
python main.py
```
O arquivo gerado será salvo no próprio diretório do projeto.

### 2. Execução Integrada ao `scriptLattes` (Pipeline Completo)
Se este projeto fizer parte de um ecossistema maior junto com a ferramenta [scriptLattes](https://github.com/scriptlattes/scriptlattes), você pode automatizar todo o fluxo de trabalho utilizando o script `run_pipeline.py`.

O script de pipeline executa as seguintes etapas automaticamente:
1. Executa o bot extrator (`main.py`) para gerar a lista atualizada.
2. Move o arquivo `output.list` gerado para dentro da pasta do projeto vizinho (`../scriptLattes`).
3. Invoca o ambiente virtual do `scriptLattes` para gerar os relatórios.

**Pré-requisitos da Integração via Pipeline:**
- O diretório do `scriptLattes` deve estar no mesmo nível hierárquico (lado a lado) da pasta deste projeto.
- O projeto `scriptLattes` já deve possuir o seu próprio ambiente virtual (`venv`) configurado com suas dependências instaladas.

**Executando o Pipeline:**
```bash
python run_pipeline.py
```
