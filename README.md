# Extrator Lattes (Playwright)

Este projeto é um bot de automação web criado para coletar dados públicos disponíveis na busca textual do Currículo Lattes. Ele realiza pesquisas automatizadas, navega pela paginação de resultados, abre os currículos e extrai o ID Lattes e o nome dos pesquisadores, salvando-os em um formato de lista (`.list`).

Este repositório é um clone do projeto original iniciado por Francisco Florêncio. O código foi totalmente refatorado e migrado para o **Playwright** por Vitor Guerra. A transição para o Playwright garante maior velocidade, confiabilidade em esperas implícitas (waits) e robustez no tratamento de múltiplas abas durante a extração.

---

## 🛠 Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. Configure um ambiente virtual Python:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Linux/macOS
   # ou: venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Instale o navegador do Playwright necessário para o bot:
   ```bash
   playwright install chromium
   ```

---

## ⚙️ Configuração (Limitando Currículos)

Dentro do arquivo `main.py`, existe uma sessão de configuração logo no topo do script. Você pode modificar as seguintes variáveis:

*   `SEARCH_QUERY`: A string de busca avançada que o robô irá digitar no site do Lattes.
*   `MAX_CURRICULOS`: Define o limite máximo de currículos que você deseja extrair em uma execução (útil para testes rápidos).
    *   *Exemplo:* `MAX_CURRICULOS = 50` salvará apenas os primeiros 50 currículos.
    *   *Desativar limite:* Defina o valor como `0` para extrair todos os resultados encontrados pela busca.

---

## 🚀 Como Usar

Existem duas formas principais de utilizar o projeto:

### 1. Execução Simples (Apenas Extração)

Se você deseja apenas gerar o arquivo `output.list` contendo os nomes e IDs extraídos, basta executar o script principal:

```bash
python main.py
```
O arquivo gerado será salvo no próprio diretório do projeto.

### 2. Execução Integrada ao `scriptLattes` (Pipeline Completo)

Se este projeto fizer parte de um ecossistema maior junto com a ferramenta [scriptLattes](https://github.com/scriptlattes/scriptlattes), você pode automatizar todo o fluxo de trabalho utilizando o **`run_pipeline.py`**.

O script de pipeline executa 3 etapas automaticamente:
1. Executa o bot extrator (`main.py`) para gerar a lista atualizada.
2. Move o arquivo `output.list` gerado para dentro da pasta do projeto vizinho (`../scriptLattes`).
3. Invoca o executável Python do ambiente virtual do `scriptLattes` para gerar os relatórios, contornando problemas comuns de ativação do `venv`.

**Pré-requisitos da Integração:**
* O diretório do `scriptLattes` deve estar no mesmo nível hierárquico (lado a lado) da pasta deste projeto.
* O `scriptLattes` já deve possuir o seu próprio ambiente virtual (`venv`) configurado com suas dependências instaladas.

**Executando o Pipeline:**
```bash
python run_pipeline.py
```
