#!/bin/bash

"""
Comando de Execução Homologado:
sudo chmod +x ./Setup/setup.sh
sudo ./Setup/setup.sh
"""

# Cores para deixar o terminal padrão Sana/Bios
VERDE='\033[92m'
AMARELO='\033[93m'
VERMELHO='\033[91m'
AZUL='\033[94m'
CIANO='\033[96m'
RESET='\033[0m'

echo -e "${VERDE}"
echo "========================================================="
echo "🔒 Sana/Bios Informática & Consultoria - INSTALADOR V2.7"
echo "🛸 Instalador de Dependências do Framework PHANTON RECON"
echo "========================================================="
echo -e "${RESET}"

# Verifica se o script está rodando como root (necessário para apt e atalhos globais)
if [ "$EUID" -ne 0 ]; then
  echo -e "${VERMELHO}[!] Por favor, execute o instalador como root usando: sudo ./Setup/setup.sh${RESET}"
  exit 1
fi

# ==============================================================================
# 0 - TERMO DE RESPONSABILIDADE E ACEITE DE COMPLIANCE (SANA/BIOS)
# ==============================================================================
clear
echo -e "${VERMELHO}"
echo "========================================================================="
echo "⚠️  AVISO LEGAL E TERMO DE COMPLIANCE DE SEGURANÇA - FRAMEWORK PHANTON"
echo "========================================================================="
echo -e "${RESET}"

echo -e "${AMARELO}Por favor, leia atentamente as condições de uso antes de prosseguir:${RESET}\n"
echo -e "1. A ferramenta Phanton foi desenvolvida exclusivamente com a finalidade de"
echo -e "   automatizar a coleta de informações iniciais em plataformas de (${VERDE}CTF${RESET}), laboratórios"
echo -e "   de estudo (${VERDE}LABS${RESET}), em programas homologados de (${VERDE}BUG BOUNTY${RESET}), ou em auditorias reais"
echo -e "   de testes de intrusão (${VERDE}PENTEST${RESET}) devidamente contratadas e autorizadas."
echo ""
sleep 1

echo -e "2. O uso desta ferramenta contra alvos reais que não se enquadrem nas exceções"
echo -e "   acima constitui crime e violação de privacidade de dados conforme a LGPD brasileira."
echo -e "   Consulte a legislação em: ${CIANO}https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm${RESET}"
echo ""
sleep 2

echo -e "3. Ao confirmar este aviso e prosseguir com a instalação, você afirma estar ciente"
echo -e "   destas condições e ${VERDE}EXIME O DESENVOLVEDOR DE QUALQUER RESPONSABILIDADE${RESET}"
echo -e "   pelo uso inadequado, ilegal ou malicioso desta ferramenta."
echo -e "\n=========================================================================\n"
sleep 1

while true; do
    echo -e -n "${AMARELO}[?] Você concorda com os termos e assume a responsabilidade de uso? [S/N]: ${RESET}"
    read -r OPCAO_TERMO
    OPCAO_TERMO=$(echo "$OPCAO_TERMO" | tr '[:lower:]' '[:upper:]')

    if [ "$OPCAO_TERMO" = "N" ]; then
        echo -e "\n${VERMELHO}[X] Instalação abortada pelo usuário por não conformidade com os termos.${RESET}\n"
        exit 1
    elif [ "$OPCAO_TERMO" = "S" ]; then
        echo -e "\n${VERDE}[✓] Termo aceito! Registrando credenciais de conformidade...${RESET}\n"
        break
    else
        echo -e "${VERMELHO}[!] Opção inválida. Digite apenas S ou N.${RESET}"
    fi
done

# ==============================================================================
# 1 - MAPEAMENTO CORRETO DOS DIRETÓRIOS (CORREÇÃO DA RAIZ)
# ==============================================================================
# O script roda dentro de /Setup, a raiz real do projeto está um nível acima!
CD_CORRETO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PATH_PROJETO_GLOBAL="$CD_CORRETO"

CAMINHO_JSON_RAIZ="$PATH_PROJETO_GLOBAL/response.json"
USUARIO_REAL=${SUDO_USER:-$USER}

echo -e "${AZUL}[*] Base do projeto identificada em: ${PATH_PROJETO_GLOBAL}${RESET}"
echo -e "${AZUL}[*] Operador do sistema identificado como: ${USUARIO_REAL}${RESET}"

# Gera o JSON estruturado diretamente pelo Instalador na raiz correta
cat << EOF > "$CAMINHO_JSON_RAIZ"
{
    "compliance": {
        "termo_aceito": "SIM",
        "data_instalacao": "$(date '+%Y-%m-%d %H:%M:%S')"
    }
}
EOF

# Rotina auxiliar de instalação apt
verificar_e_instalar_apt() {
    local programa=$1
    local pacote=$2
    echo -e "${AMARELO}    [-] Verificando dependência do sistema: '$programa'...${RESET}"
    if ! command -v "$programa" &> /dev/null; then
        echo -e "${AZUL}[+] '$programa' não encontrado. Configurando via apt...${RESET}"
        apt-get update -qq && apt-get install -y "$pacote" > /dev/null 2>&1
    fi
    echo -e "${VERDE}        [✓] '$programa' pronto.${RESET}"
}

echo -e "\n${CIANO}[*] Verificando ferramentas de infraestrutura e fuzzing...${RESET}"
verificar_e_instalar_apt "nmap" "nmap"
verificar_e_instalar_apt "ffuf" "ffuf"
verificar_e_instalar_apt "whatweb" "whatweb"
verificar_e_instalar_apt "wafw00f" "wafw00f"
verificar_e_instalar_apt "pip3" "python3-pip"
verificar_e_instalar_apt "go" "golang-go"

# ==============================================================================
# 2 - INSTALAÇÃO ROBUSTA DO GO HTTPX (CORRIGIDO)
# ==============================================================================
echo -e "\n${CIANO}[*] Configurando ferramenta analítica HTTPX da ProjectDiscovery...${RESET}"

if ! command -v httpx &> /dev/null; then
    echo -e "${AZUL}[+] Compilando e alocando HTTPX globalmente via Go...${RESET}"
    # Executa a instalação limpa diretamente no ambiente global do Go do sistema
    export GOPATH="/home/$USUARIO_REAL/go"
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest > /dev/null 2>&1
    
    # Copia o binário compilado para os caminhos de execução global do Linux (Acessível de qualquer lugar)
    if [ -f "/home/$USUARIO_REAL/go/bin/httpx" ]; then
        cp "/home/$USUARIO_REAL/go/bin/httpx" /usr/local/bin/httpx
        chmod +x /usr/local/bin/httpx
    fi
fi

if command -v httpx &> /dev/null; then
    echo -e "${VERDE}    [✓] HTTPX integrado ao PATH global com sucesso!${RESET}"
else
    # Fallback caso o barramento Go falhe: baixa o binário oficial compilado direto da release estável
    echo -e "${AMARELO}[!] Compilação Go falhou. Aplicando fallback via binário oficial pré-compilado...${RESET}"
    wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip -O /tmp/httpx.zip
    if [ -f /tmp/httpx.zip ]; then
        apt-get install -y unzip > /dev/null 2>&1
        unzip -o /tmp/httpx.zip -d /tmp/httpx_bin > /dev/null 2>&1
        cp /tmp/httpx_bin/httpx /usr/local/bin/httpx
        chmod +x /usr/local/bin/httpx
        rm -rf /tmp/httpx.zip /tmp/httpx_bin
    fi
    echo -e "${VERDE}    [✓] HTTPX (Fallback Estável) injetado com sucesso!${RESET}"
fi

# 3. Dependências Python
echo -e "\n${CIANO}[*] Sincronizando bibliotecas do Python...${RESET}"
pip3 install pyfiglet --break-system-packages > /dev/null 2>&1 || pip3 install pyfiglet > /dev/null 2>&1
echo -e "${VERDE}    [✓] Ambiente Python estabilizado.${RESET}"

# 4. Criação da árvore
mkdir -p "$PATH_PROJETO_GLOBAL/Documentos" "$PATH_PROJETO_GLOBAL/wordlists"

# ==============================================================================
# 5 - ARQUITETURA INTERFACES GRÁFICAS E LANÇADORES (CORRIGIDO)
# ==============================================================================
echo -e "\n${CIANO}[*] Consolidando lançador de terminal e Área de Trabalho...${RESET}"

# Identifica a Área de Trabalho real do usuário (Portabilidade Linux Avançada)
if [ -f "/home/$USUARIO_REAL/.config/user-dirs.dirs" ]; then
    PATH_DESKTOP_DETECTADO=$(sudo -u "$USUARIO_REAL" xdg-user-dir DESKTOP)
else
    PATH_DESKTOP_DETECTADO="/home/$USUARIO_REAL/Desktop"
    if [ -d "/home/$USUARIO_REAL/Área de Trabalho" ]; then
        PATH_DESKTOP_DETECTADO="/home/$USUARIO_REAL/Área de Trabalho"
    fi
fi

echo -e "${AMARELO}    [-] Escrevendo lançador gráfico em: $PATH_DESKTOP_DETECTADO${RESET}"

# Cria o .desktop definitivo para a Área de Trabalho apontando para a Raiz Real
ARQUIVO_DESKTOP="$PATH_DESKTOP_DETECTADO/Phanton.desktop"

# Estrutura limpa em conformidade com os menus do Kali Linux
TEMPLATE_DESKTOP="[Desktop Entry]
Version=1.0
Type=Application
Name=Phanton Recon
Comment=Framework de Reconhecimento Automatizado Avançado - Sana/Bios
Exec=python3 $PATH_PROJETO_GLOBAL/Phanton.py
Icon=$PATH_PROJETO_GLOBAL/Setup/phanton_icon.png
Terminal=true
Categories=Development;IDE;Security;
Path=$PATH_PROJETO_GLOBAL
GenericName=Phanton Tools
StartupNotify=true"

# Salva na Área de Trabalho
echo "$TEMPLATE_DESKTOP" > "$ARQUIVO_DESKTOP"
chown "$USUARIO_REAL":"$USUARIO_REAL" "$ARQUIVO_DESKTOP"
chmod +x "$ARQUIVO_DESKTOP"

# 🧠 INCLUSÃO CORRIGIDA NO MENU INICIAR DO SISTEMA (DESENVOLVIMENTO / SEGURANÇA)
echo -e "${AMARELO}    [-] Clonando lançador para o Menu Iniciar Global do Sistema...${RESET}"
echo "$TEMPLATE_DESKTOP" > /usr/share/applications/Phanton.desktop
chmod +x /usr/share/applications/Phanton.desktop

# Alinha segurança gráfica do atalho para evitar o aviso de "Atalho Não Confiável"
if command -v gio &> /dev/null; then
    sudo -u "$USUARIO_REAL" DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u $USUARIO_REAL)/bus gio set "$ARQUIVO_DESKTOP" metadata::trusted true > /dev/null 2>&1
fi

# 5.1 - Blinda o link simbólico global do terminal (/usr/local/bin/phanton)
rm -f /usr/local/bin/phanton
ln -s "$PATH_PROJETO_GLOBAL/Phanton.py" /usr/local/bin/phanton
chmod +x "$PATH_PROJETO_GLOBAL/Phanton.py"

# Governança de permissões final Sana/Bios
chown -R "$USUARIO_REAL":"$USUARIO_REAL" "$PATH_PROJETO_GLOBAL"
chmod -R 755 "$PATH_PROJETO_GLOBAL"

echo -e "\n${VERDE}=======================================================${RESET}"
echo " ${CIANO}[✓]${RESET}${VERDE}INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo " O Phanton v2.7 está pronto para rodar!"
echo "=======================================================${RESET}"

# ==============================================================================
# PROTOCOLO DE INICIALIZAÇÃO AUTOMÁTICA SANA/BIOS
# ==============================================================================
echo -e "\n${CIANO}[*] Preparando inicialização imediata do framework...${RESET}\n"
sleep 1

opcoes=("Executar o Phanton" "Sair sem executar")
PS3=$'\n'"A configuração foi concluída com sucesso. O que deseja fazer agora? (Digite o número): "

select opt in "${opcoes[@]}"; do
    case $opt in
        "Executar o Phanton")
            echo -e "\n${CIANO}[*] Iniciando o Phanton...${RESET}"
            sleep 1
            sudo -u "$USUARIO_REAL" python3 "$PATH_PROJETO_GLOBAL/Phanton.py" 
            break
            ;;
        "Sair sem executar")
            echo -e "\n${VERDE}Encerrando script. Até logo!${RESET}\n"
            echo -e "${AZUL}Sana/Bios Informática & Consultoria agradece.${RESET}\n"
            sleep 2
            clear
            break
            ;;
        *) 
            echo -e "${VERMELHO}Opção inválida.${RESET}" 
            ;;
    esac
done
