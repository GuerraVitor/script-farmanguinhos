Este projeto é um bot de web scraping, criado para coletar dados públicos disponíveis no site Currículo Lattes.

Você pode encontrar um exemplo de output, onde obtemos os dados (ID Lattes e nome dos pesquisadores buscados, obtidos rodando o script `main.py`) e os adicionamos a um arquivo `.list`.

Este repositório é um clone do projeto original iniciado por Francisco Florêncio, refatorado e migrado para **Playwright** por Vitor Guerra para continuação do desenvolvimento e garantir maior estabilidade na extração.

## Instalação e Uso

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd selenium-lattes
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

4. Instale os navegadores do Playwright:
   ```bash
   playwright install chromium
   ```

5. Execute o script:
   ```bash
   python main.py
   ```
