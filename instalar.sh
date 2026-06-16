#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

info() {
  printf '\n[INFO] %s\n' "$1"
}

fail() {
  printf '\n[ERRO] %s\n' "$1"
  printf '\nPressione Enter para sair...'
  read -r _
  exit 1
}

install_python3_venv() {
  info "Tentando instalar o pacote python3-venv via apt-get."

  if ! command -v sudo >/dev/null 2>&1; then
    fail "O comando sudo não está disponível. Instale o pacote python3-venv manualmente e execute o script novamente."
  fi

  if ! command -v apt-get >/dev/null 2>&1; then
    fail "Este sistema não parece usar apt-get. Instale um Python 3 completo com suporte a venv e execute o script novamente."
  fi

  sudo apt-get update || fail "Falha ao atualizar a lista de pacotes. Verifique sua conexão e permissões de sudo."
  sudo apt-get install -y python3-venv || fail "Falha ao instalar python3-venv."
}

info "Iniciando instalação no Linux/macOS."

if ! command -v python3 >/dev/null 2>&1; then
  fail "Python 3 não foi encontrado. Instale o Python 3 e tente novamente."
fi

info "Python 3 encontrado: $(python3 --version 2>&1)"

if [ ! -d "venv" ]; then
  info "Criando ambiente virtual em venv..."
  if ! python3 -m venv venv >/dev/null 2>&1; then
    info "A criação do venv falhou na primeira tentativa."
    if command -v apt-get >/dev/null 2>&1 && [ "$(uname -s)" = "Linux" ]; then
      install_python3_venv
      info "Tentando criar o venv novamente..."
      python3 -m venv venv || fail "Não foi possível criar o ambiente virtual mesmo após instalar python3-venv."
    else
      fail "Não foi possível criar o ambiente virtual. Em macOS, instale uma distribuição completa do Python 3 (por exemplo, python.org ou Homebrew) e tente novamente."
    fi
  fi
else
  info "Ambiente virtual venv já existe."
fi

info "Ativando o ambiente virtual..."
source venv/bin/activate || fail "Não foi possível ativar o ambiente virtual."

info "Instalando dependências do projeto..."
python -m pip install -r requirements.txt || fail "Falha ao instalar as dependências do requirements.txt."

info "Instalando o Chromium do Playwright..."
python -m playwright install chromium || fail "Falha ao instalar o Chromium do Playwright."

info "Instalação concluída com sucesso."
printf '\nPressione Enter para fechar...'
read -r _
