# Lattes Extractor (Bot) 🤖🎓

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated-2EAD33.svg)](https://playwright.dev/python/)

*Looking for the Portuguese version? [Click here to read in Portuguese](#extrator-lattes-bot-). / Procurando a versão em Português? [Clique aqui](#extrator-lattes-bot-).*

A web automation tool built with **Python** and **Playwright**, designed to securely and efficiently collect public data from the [Currículo Lattes](http://buscatextual.cnpq.br/buscatextual/busca.do) advanced search.

This application acts as a specialized data pipeline to automatically generate the `.list` input files required by the [scriptLattes](https://github.com/scriptlattes/scriptlattes) ecosystem. By utilizing Playwright, it offers high-speed execution, resilient DOM element waiting, and reliable multi-tab handling.

## 📑 Table of Contents
1. [Features](#features)
2. [Architecture & Workflow](#architecture--workflow)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Pipeline Integration](#pipeline-integration)

## ✨ Features
- **Automated Searching:** Directly interfaces with the advanced search form on the CNPq Lattes platform.
- **Resilient Extraction:** Gracefully handles unexpected pop-ups, network delays, and complex tab management natively via Playwright.
- **Structured Export:** Generates clean, formatted `output.list` files consisting of the 16-digit Lattes ID and the researcher's name.
- **Pipeline Ready:** Includes a `run_pipeline.py` script to automatically execute the extraction and trigger `scriptLattes` in a single run.

## 🏗️ Architecture & Workflow
The extractor interacts with the Lattes platform iteratively:
1. Accesses the Advanced Search interface and inputs the configured `SEARCH_QUERY`.
2. Calculates the total number of pages and iterates through the paginated results.
3. Opens individual researcher CVs in temporary tabs.
4. Parses the DOM or source code to reliably locate the 16-digit ID and name.
5. Buffers and flushes the data asynchronously into `output.list`.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd lattes-extractor
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # Windows: venv\Scripts\activate
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

Open `main.py` and adjust the variables in the `# --- Configuration ---` section to suit your needs:

- `SEARCH_QUERY`: The exact search query string to be used.
- `MAX_CURRICULOS`: The maximum number of CVs to extract per run (e.g., `MAX_CURRICULOS = 50`). Set to `0` for unlimited extraction.

## 🚀 Usage

### 1. Standalone Execution
Run the extractor independently to simply generate an `output.list` file in the current directory:
```bash
python main.py
```

### 2. Pipeline Integration (`scriptLattes`)
This tool is built to seamlessly feed data into `scriptLattes`.

**Prerequisites:**
- The `scriptLattes` repository must be cloned in the same parent directory (side-by-side with this extractor).
- The `scriptLattes` project must have its own virtual environment (`venv`) fully configured and dependencies installed.

**Run the pipeline:**
```bash
python run_pipeline.py
```
This script will automatically run the extractor, move the resulting `output.list` into the `scriptLattes` folder, and trigger the `scriptLattes` reporting engine.

---

# Extrator Lattes (Bot) 🤖🎓

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Automatizado-2EAD33.svg)](https://playwright.dev/python/)

Uma ferramenta robusta de automação web construída com **Python** e **Playwright**, projetada para coletar de forma segura e eficiente dados públicos da busca avançada do [Currículo Lattes](http://buscatextual.cnpq.br/buscatextual/busca.do).

Esta aplicação atua como um pipeline de dados especializado para gerar automaticamente os arquivos `.list` de entrada necessários para o ecossistema [scriptLattes](https://github.com/scriptlattes/scriptlattes). Utilizando Playwright, oferece execução de alta velocidade, tratamento resiliente de elementos do DOM e gerenciamento confiável de múltiplas abas.

## 📑 Índice
1. [Funcionalidades](#-funcionalidades)
2. [Arquitetura e Fluxo de Trabalho](#%EF%B8%8F-arquitetura-e-fluxo-de-trabalho)
3. [Instalação](#%EF%B8%8F-instalação)
4. [Configuração](#%EF%B8%8F-configuração)
5. [Como Usar](#-como-usar)
6. [Integração via Pipeline](#2-execução-integrada-ao-scriptlattes-pipeline)

## ✨ Funcionalidades
- **Busca Automatizada:** Interage de forma autônoma com o formulário de busca avançada do CNPq.
- **Extração Resiliente:** Lida de forma robusta com pop-ups inesperados, atrasos de rede e gerenciamento complexo de abas via Playwright.
- **Exportação Estruturada:** Gera arquivos `output.list` limpos e formatados, contendo o ID Lattes (16 dígitos) e o nome do pesquisador.
- **Pronto para Pipeline:** Inclui um script `run_pipeline.py` para executar a extração e acionar o `scriptLattes` automaticamente em uma única execução.

## 🏗️ Arquitetura e Fluxo de Trabalho
O extrator interage com a plataforma Lattes de forma iterativa:
1. Acessa a interface de Busca Avançada e insere a `SEARCH_QUERY` configurada.
2. Calcula o número total de páginas e itera pelos resultados paginados.
3. Abre os currículos individuais dos pesquisadores em abas temporárias.
4. Analisa o DOM ou código-fonte para localizar de forma confiável o ID de 16 dígitos e o nome.
5. Armazena em buffer e grava os dados no arquivo `output.list`.

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd lattes-extractor
   ```

2. **Configure um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # Windows: venv\Scripts\activate
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

Abra o arquivo `main.py` e ajuste as variáveis na seção `# --- Configuration ---` para atender às suas necessidades:

- `SEARCH_QUERY`: A string de busca exata a ser utilizada na pesquisa.
- `MAX_CURRICULOS`: O número máximo de currículos a serem extraídos por execução (ex: `MAX_CURRICULOS = 50`). Defina como `0` para extração ilimitada.

## 🚀 Como Usar

### 1. Execução Simples (Apenas Extração)
Execute o extrator de forma independente para gerar apenas o arquivo `output.list` no diretório atual:
```bash
python main.py
```

### 2. Execução Integrada ao `scriptLattes` (Pipeline)
Esta ferramenta foi desenvolvida para alimentar dados de forma fluida para o `scriptLattes`.

**Pré-requisitos:**
- O repositório `scriptLattes` deve estar clonado no mesmo diretório pai (lado a lado com este extrator).
- O projeto `scriptLattes` deve possuir seu próprio ambiente virtual (`venv`) configurado com todas as dependências instaladas.

**Executando o pipeline:**
```bash
python run_pipeline.py
```
Este script executará automaticamente o extrator, moverá o arquivo `output.list` resultante para a pasta do `scriptLattes` e iniciará o motor de relatórios do `scriptLattes`.
