#!/bin/bash

# Cores para deixar o terminal padrão Sana/Bios
VERDE='\033[92m'
AMARELO='\033[93m'
VERMELHO='\033[91m'
AZUL='\033[94m'
CIANO='\033[96m'
RESET='\033[0m'

echo -e "${VERDE}"
echo "========================================================="
echo "🔒 Sana/Bios Informática & Consultoria - INSTALADOR"
echo "🛸 Instalador de Dependências do Framework PHANTON RECON "
echo "========================================================="
echo -e "${RESET}"

# Verifica se o script está rodando como root (necessário para instalar pacotes via apt)
if [ "$EUID" -ne 0 ]; then
  echo -e "${VERMELHO}[!] Por favor, execute o instalador como root ou usando sudo.${RESET}"
  exit 1
fi

# Função para checar e instalar pacotes do sistema
verificar_e_instalar_apt() {
    local programa=$1
    local pacote=$2
    
    echo -e "${AMARELO}[*] Verificando se o '$programa' está instalado...${RESET}"
    if ! command -v "$programa" &> /dev/null; then
        echo -e "${AZUL}[+] '$programa' não encontrado. Instalando via apt...${RESET}"
        apt-get update -qq && apt-get install -y "$pacote" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${VERDE}[✓] '$programa' instalado com sucesso!${RESET}"
        else
            echo -e "${VERMELHO}[X] Falha ao instalar '$programa'. Verifique sua conexão ou repositórios.${RESET}"
        fi
    else
        echo -e "${VERDE}[✓] '$programa' já está instalado na máquina.${RESET}"
    fi
}

# 1. Checagem das dependências do sistema operacional (Foco em Kali/Debian)
echo -e "\n${CIANO}[📊] Verificando ferramentas de infraestrutura e fuzzing...${RESET}"
verificar_e_instalar_apt "nmap" "nmap"
verificar_e_instalar_apt "ffuf" "ffuf"
verificar_e_instalar_apt "whatweb" "whatweb"
verificar_e_instalar_apt "wafw00f" "wafw00f"
verificar_e_instalar_apt "pip3" "python3-pip"

# 2. Checagem das dependências de bibliotecas do Python
echo -e "\n${CIANO}[🐍] Verificando bibliotecas necessárias do Python...${RESET}"
if command -v pip3 &> /dev/null; then
    echo -e "${AMARELO}[*] Instalando dependência 'pyfiglet' para renderização do Banner...${RESET}"
    pip3 install pyfiglet --break-system-packages > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${VERDE}[✓] Biblioteca 'pyfiglet' configurada.${RESET}"
    else
        # Tenta sem a flag caso seja uma versão mais antiga do pip
        pip3 install pyfiglet > /dev/null 2>&1
        echo -e "${VERDE}[✓] Biblioteca 'pyfiglet' configurada.${RESET}"
    fi
else
    echo -e "${VERMELHO}[!] Não foi possível instalar as dependências do Python porque o pip3 falhou.${RESET}"
fi

# 3. Criando a árvore de diretórios padrão caso não exista
echo -e "\n${CIANO}[📁] Estruturando os diretórios locais do projeto...${RESET}"
mkdir -p Documentos wordlists

echo -e "\n${VERDE}======================================================="
echo " 🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo " O Phanton v2.6 está pronto para rodar no seu GitHub!"
echo "=======================================================${RESET}\n"
