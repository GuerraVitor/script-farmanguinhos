import os
import shutil
import subprocess
import sys

PASTA_EXTRATOR = os.path.dirname(os.path.abspath(__file__))
PASTA_SCRIPT_LATTES = os.path.abspath(os.path.join(PASTA_EXTRATOR, "..", "scriptLattes"))

def executar_comando(comando, diretorio):
    print(f"Executando: {comando} em {diretorio}")
    resultado = subprocess.run(comando, shell=True, cwd=diretorio)
    if resultado.returncode != 0:
        print(f"Erro ao executar: {comando}")
        sys.exit(1)

def main():
    # 1. Executar o bot extrator
    print("1. Iniciando o Bot Extrator...")

    # ALTERAÇÃO: Usa o mesmo executável python que iniciou este script
    python_exec = sys.executable
    executar_comando(f"{python_exec} main.py", PASTA_EXTRATOR)

    # 2. Mover o output.list
    print("2. Movendo output.list para o scriptLattes...")
    origem_output = os.path.join(PASTA_EXTRATOR, "output.list")
    destino_output = os.path.join(PASTA_SCRIPT_LATTES, "output.list")

    if os.path.exists(origem_output):
        shutil.move(origem_output, destino_output)
        print("✓ Arquivo output.list movido com sucesso.")
    else:
        # ALTERAÇÃO: Adicionado o 'f' antes da string para formatar a variável
        print(f"Erro: Arquivo {origem_output} não encontrado.")
        sys.exit(1)

    # 3. Executar o scriptLattes
    print("3. Executando o scriptLattes...")

    # Verifica o Sistema Operacional e executa usando o Python do ambiente virtual diretamente
    if os.name == "nt":  # Windows
        comando_lattes = r"venv\Scripts\python scriptLattes.py exemplo\teste-01.config"
    else:  # Linux / Mac
        comando_lattes = "venv/bin/python3 scriptLattes.py exemplo/teste-01.config"

    # Altere o nome do arquivo .config se necessário
    executar_comando(comando_lattes, PASTA_SCRIPT_LATTES)

    print("Script concluido com sucesso!")


if __name__ == "__main__":
    main()
()
