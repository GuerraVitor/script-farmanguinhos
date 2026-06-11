import os
import shutil
import subprocess
import sys

PASTA_SELENIUM = os.path.dirname(os.path.abspath(__file__))
PASTA_SCRIPT_LATTES = os.path.abspath(os.path.join(PASTA_SELENIUM, "..", "scriptLattes"))

def executar_comando(comando, diretorio):
    print(f"Executando: {comando} em {diretorio}")
    resultado = subprocess.run(comando, shell=True, cwd=diretorio)
    if resultado.returncode != 0:
        print(f"Erro ao executar: {comando}")
        sys.exit(1)

def main():
    # 1. Executar o bot do Selenium
    print("\n" + "=" * 40)
    print("1. Iniciando o Bot Selenium...")
    print("=" * 40)

    # ALTERAÇÃO: Usa o mesmo executável python que iniciou este script
    python_exec = sys.executable
    executar_comando(f"{python_exec} main.py", PASTA_SELENIUM)

    # 2. Mover o output.list
    print("\n" + "=" * 40)
    print("2. Movendo output.list para o scriptLattes...")
    print("=" * 40)
    origem_output = os.path.join(PASTA_SELENIUM, "output.list")
    destino_output = os.path.join(PASTA_SCRIPT_LATTES, "output.list")

    if os.path.exists(origem_output):
        shutil.move(origem_output, destino_output)
        print("✓ Arquivo output.list movido com sucesso.")
    else:
        # ALTERAÇÃO: Adicionado o 'f' antes da string para formatar a variável
        print(f"Erro: Arquivo {origem_output} não encontrado.")
        sys.exit(1)

    # 3. Executar o scriptLattes
    print("\n" + "=" * 40)
    print("3. Executando o scriptLattes...")
    print("=" * 40)

    # Verifica o Sistema Operacional para ativar o ambiente virtual
    if os.name == "nt":  # Windows
        comando_lattes = r"venv\Scripts\activate && python scriptLattes.py exemplo\teste-01.config"
    else:  # Linux / Mac
        comando_lattes = "source venv/bin/activate && python3 scriptLattes.py exemplo/teste-01.config"

    # Altere o nome do arquivo .config se necessário
    executar_comando(comando_lattes, PASTA_SCRIPT_LATTES)

    print("\n" + "=" * 40)
    print("✓ Automação concluída com sucesso!")
    print("=" * 40)


if __name__ == "__main__":
    main()
