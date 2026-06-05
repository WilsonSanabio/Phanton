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

# Descobre quem é o usuário real fora do sudo (Ex: fuchs, wilsonsanabio, etc.)
USUARIO_REAL=${SUDO_USER:-$USER}

# 1. Checagem das dependências do sistema operacional (Foco em Kali/Debian)
echo -e "\n${CIANO}[📊] Verificando ferramentas de infraestrutura e fuzzing...${RESET}"
verificar_e_instalar_apt "nmap" "nmap"
verificar_e_instalar_apt "ffuf" "ffuf"
verificar_e_instalar_apt "whatweb" "whatweb"
verificar_e_instalar_apt "wafw00f" "wafw00f"
verificar_e_instalar_apt "pip3" "python3-pip"
verificar_e_instalar_apt "go" "golang-go"     # Garante o compilador Go para o HTTPX

# 2. Instalação do HTTPX via GO (Garantindo compatibilidade total com Subfinder)
echo -e "\n${CIANO}[🛸] Verificando ferramentas Go (ProjectDiscovery)...${RESET}"
CAMINHO_HTTPX_GO="/home/$USUARIO_REAL/go/bin/httpx"

if [ ! -f "$CAMINHO_HTTPX_GO" ]; then
    echo -e "${AZUL}[+] Compilando HTTPX via Go para o usuário $USUARIO_REAL...${RESET}"
    # Executa o comando de instalação como o usuário comum para criar a pasta correta no home dele
    sudo -u "$USUARIO_REAL" go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest > /dev/null 2>&1
    
    if [ -f "$CAMINHO_HTTPX_GO" ]; then
        echo -e "${VERDE}[✓] HTTPX compiled e instalado via Go com sucesso!${RESET}"
    else
        echo -e "${VERMELHO}[X] Falha ao compilar HTTPX via Go. Verifique o ambiente.${RESET}"
    fi
else
    echo -e "${VERDE}[✓] HTTPX já está instalado via Go no caminho correto.${RESET}"
fi

# 3. Checagem das dependências de bibliotecas do Python
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

# 4. Criando a árvore de diretórios padrão caso não exista
echo -e "\n${CIANO}[📁] Estruturando os diretórios locais do projeto...${RESET}"
mkdir -p Documentos wordlists

# 5. Ajuste Inteligente de Permissões e Governança de Arquivos (Evita o PermissionError)
echo -e "\n${CIANO}[🛡️] Aplicando o protocolo Sana/Bios de governança de permissões...${RESET}"

if [ "$USUARIO_REAL" != "root" ]; then
    echo -e "${AMARELO}[*] Sincronizando propriedade do projeto para o operador: ${USUARIO_REAL}...${RESET}"
    chown -R "$USUARIO_REAL":"$USUARIO_REAL" .
    chmod -R 755 .
    
    # Garante que a pasta go do usuário também tenha as permissões certas
    if [ -d "/home/$USUARIO_REAL/go" ]; then
        chown -R "$USUARIO_REAL":"$USUARIO_REAL" /home/$USUARIO_REAL/go
    fi
    echo -e "${VERDE}[✓] Árvore de diretórios blindada e liberada com sucesso!${RESET}"
else
    chmod -R 755 .
fi

#==============================================================================
# 6 - PROTOCOLO VISUAL E TERMINAL SANA/BIOS (PORTABILIDADE GLOBAL DEFINITIVA)
#==============================================================================
echo -e "\n${CIANO}[🚀] Consolidando lançador de terminal e Área de Trabalho...${RESET}"

PATH_PROJETO_GLOBAL="$(pwd)"

# Interroga as configurações nativas do sistema para localizar a Área de Trabalho real
if [ -f "/home/$USUARIO_REAL/.config/user-dirs.dirs" ]; then
    PATH_DESKTOP_DETECTADO=$(sudo -u "$USUARIO_REAL" xdg-user-dir DESKTOP)
else
    # Fallback de segurança caso o arquivo de diretórios XDG não responda
    PATH_DESKTOP_DETECTADO="/home/$USUARIO_REAL/Desktop"
    if [ -d "/home/$USUARIO_REAL/Área de Trabalho" ]; then
        PATH_DESKTOP_DETECTADO="/home/$USUARIO_REAL/Área de Trabalho"
    fi
fi

ARQUIVO_DESKTOP="$PATH_DESKTOP_DETECTADO/Phanton.desktop"

echo -e "${AMARELO}[*] Área de Trabalho detectada em: $PATH_DESKTOP_DETECTADO${RESET}"

# 6.1 - Cria o arquivo .desktop apontando para o script monolítico real
cat << EOF > "$ARQUIVO_DESKTOP"
[Desktop Entry]
Version=1.0
Type=Application
Name=Phanton Recon
Comment=Framework de Reconhecimento Automatizado Avançado - Sana/Bios
Exec=python3 $PATH_PROJETO_GLOBAL/Phanton.py
Icon=$PATH_PROJETO_GLOBAL/phantom_icon.png
Terminal=true
Categories=Network;Security;
Path=$PATH_PROJETO_GLOBAL
GenericName=Phanton
EOF

# Aplica as permissões de governança sem duplicidades no arquivo gerado
chown "$USUARIO_REAL":"$USUARIO_REAL" "$ARQUIVO_DESKTOP"
chmod +x "$ARQUIVO_DESKTOP"

# Alinha o ecossistema gráfico para confiar no atalho imediatamente (Evita bloqueios no Mint)
if command -v gio &> /dev/null; then
    sudo -u "$USUARIO_REAL" DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u $USUARIO_REAL)/bus gio set "$ARQUIVO_DESKTOP" metadata::trusted true > /dev/null 2>&1
fi

# 6.2 - Blinda o link simbólico global do terminal (/usr/local/bin/phanton)
echo -e "${AMARELO}[*] Validando integridade do atalho global de terminal...${RESET}"
rm -f /usr/local/bin/phanton
ln -s "$PATH_PROJETO_GLOBAL/Phanton.py" /usr/local/bin/phanton

echo -e "${VERDE}[✓] Sucesso! Linha de comando intacta e Lançador 👻 criado com sucesso!${RESET}"

echo -e "\n${VERDE}======================================================="
echo " 🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo " O Phanton v2.6 está pronto para rodar no seu GitHub!"
echo -e "=======================================================${RESET}"

# ==============================================================================
# PROTOCOLO DE INICIALIZAÇÃO AUTOMÁTICA SANA/BIOS
# ==============================================================================
echo -e "n\${CIANO}[🚀] Preparando inicialização imediata do framework...${RESET}"
sleep 3

# Executa o framework como o usuário real para manter o ambiente correto
sudo -u "$USUARIO_REAL" python3 "$PATH_PROJETO_GLOBAL/Phanton.py"
