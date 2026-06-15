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
echo "🔒 Sana/Bios Informática & Consultoria - INSTALADOR V2.8"
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

echo -e "${AZUL}Por favor, leia atentamente os termos antes de prosseguir:${RESET}\n"
echo ""
sleep 1

echo -e "${AMARELO}1. A ferramenta Phanton foi desenvolvida exclusivamente com a finalidade de"
echo -e "   automatizar a coleta de informações iniciais em plataformas de (${RESET}${VERDE}CTF${RESET}${AMARELO}), laboratórios"
echo -e "   de estudo (${RESET}${VERDE}LABS${RESET}${AMARELO}), em programas homologados de (${RESET}${VERDE}BUG BOUNTY${RESET}${AMARELO}), ou em auditorias reais"
echo -e "   de testes de intrusão (${RESET}${VERDE}PENTEST${RESET}${AMARELO}) devidamente contratadas e autorizadas."
echo ""
sleep 1

echo -e "${AMARELO}2. O uso deste framework contra alvos sem a devida autorização expressa por escrito"
echo -e "   do proprietário é ${RESET}${VERMELHO}ilegal e viola as leis de crimes cibernéticos vigentes.${RESET}"
echo -e "   ${AMARELO}Consulte a legislação em: ${RESET}${CIANO}https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm${RESET}"
echo ""
sleep 1

echo -e "${AMARELO}3. GRATUIDADE DE USO — PHANTON RECON (DEMO)"
echo -e "   Este software é distribuído em formato binário compilado de demonstração pela"
echo -e "   ${RESET}${VERDE}Sana/Bios Informática & Consultoria${RESET}${AMARELO} de forma gratuita para a comunidade"
echo -e "   de pesquisa em segurança."
echo ""
sleep 1

echo -e "4. CONDIÇÃO OBRIGATÓRIA DE USO: Ao executar esta ferramenta e seu ecossistema, o operador"
echo -e "   concorda e assume o compromisso ético de enviar ${RESET}${VERDE}feedbacks periódicos ${RESET}${AMARELO}(${RESET}${CIANO}POSITIVOS${RESET}${AMARELO} ou"
echo -e "   ${RESET}${CIANO}NEGATIVOS${RESET}${AMARELO}) através dos canais oficiais integrados. Suas impressões, relatórios de bugs e"
echo -e "   comportamentos observados são cruciais para a melhoria contínua do motor de varredura.${RESET}"
echo ""
sleep 1

echo -e "${AMARELO}5. Ao confirmar este aviso e prosseguir com a instalação, você afirma estar ciente"
echo -e "   dessas condições e ${RESET}${VERDE}EXIME O DESENVOLVEDOR ${RESET}${AMARELO}e a ${RESET}${VERDE}SANA/BIOS INFORMÁTICA & CONSULTORIA${RESET}${AMARELO} de"
echo -e "   ${RESET}${CIANO}QUALQUER RESPONSABILIDADE${RESET}${AMARELO} pelo uso inadequado, ilegal ou malicioso dessa ferramenta,"
echo -e "   retirando a sua responsabilidade pelo uso indevido, danos causados ou vazamento de dados."
echo ""
sleep 3

echo -e "${CIANO}=========================================================================${RESET}"
read -p "Você aceita os termos e condições acima? (S/N): " aceite
echo -e "${CIANO}=========================================================================${RESET}"

# Converte para maiúsculo
aceite=$(echo "$aceite" | tr '[:lower:]' '[:upper:]')

if [ "$aceite" != "S" ] && [ "$aceite" != "SIM" ]; then
  echo -e "\n${VERMELHO}[!] Instalação abortada. Você precisa aceitar os termos para continuar.${RESET}\n"
  exit 1
fi

# SOLICITAÇÃO DO NOME DO OPERADOR
echo -e "\n${VERDE}[+] Termo Aceito com sucesso.${RESET}"
echo -e "${CIANO}[*] PERSONALIZAÇÃO DE RELATÓRIOS:${RESET}"
echo -e "Você pode definir o nome do Operador/Auditor agora para personalizar os relatórios."
echo -e "Se preferir, essa informação pode ser alterada manualmente mais tarde no arquivo de configuração.\n"

# O prompt de leitura fica limpo e focado
read -p "Digite o nome do Operador (ou pressione ENTER para o padrão): " nome_usuario

# Sua lógica cirúrgica de tratamento (Força Caixa Alta e limpa espaços)
nome_usuario=$(echo "$nome_usuario" | tr '[:lower:]' '[:upper:]' | xargs)

if [ -z "$nome_usuario" ]; then
    nome_usuario=""
fi

# Identifica o usuário real por trás do sudo para não quebrar permissões no HD
if [ -n "$SUDO_USER" ]; then
  USUARIO_REAL="$SUDO_USER"
else
  USUARIO_REAL=$(whoami)
fi

# Define as pastas base do ecossistema de forma absoluta
HOME_REAL=$(eval echo "~$USUARIO_REAL")
PATH_PROJETO_GLOBAL="$HOME_REAL/Phanton"
PATH_SETUP_REAL="$PATH_PROJETO_GLOBAL/Setup"

# Garante a existência física da pasta Setup isolada
mkdir -p "$PATH_SETUP_REAL"

# GRAVAÇÃO DA ESTRUTURA COMPLIANCE JSON
DATA_ATUAL=$(date "+%Y-%m-%d %H:%M:%S")

cat <<EOF > "$PATH_SETUP_REAL/response.json"
{
    "compliance": {
        "termo_aceito": "SIM",
        "usuario": "$nome_usuario",
        "data_instalacao": "$DATA_ATUAL"
    }
}
EOF

# Ajusta as permissões do JSON para que o usuário comum possa ler/escrever sem travar a CPU
chown "$USUARIO_REAL":"$USUARIO_REAL" "$PATH_SETUP_REAL/response.json"
chmod 644 "$PATH_SETUP_REAL/response.json"

echo -e "${VERDE}[✓] Arquivo de Compliance gerado em: $PATH_SETUP_REAL/response.json${RESET}"

if [ -n "$nome_usuario" ]; then
  echo -e "${VERDE}[✓] Operador registrado: $nome_usuario${RESET}\n"
fi

sleep 1

# ==============================================================================
# 1 - ATUALIZAÇÃO DO SISTEMA E DEPENDÊNCIAS DO SISTEMA OPERACIONAL
# ==============================================================================
echo -e "${CIANO}[*] Atualizando índices do APT e instalando pacotes de base...${RESET}"
apt update -y && apt upgrade -y

echo -e "\n${CIANO}[*] Instalando pacotes essenciais de rede e desenvolvimento...${RESET}"
apt install -y python3 python3-pip python3-venv git wget curl whois dnsutils host nmap whatweb pipx

# ==============================================================================
# 2 - CONFIGURAÇÃO E ARQUITETURA DO AMBIENTE GO (HTTPX E SUBFINDER)
# ==============================================================================
echo -e "\n${CIANO}[*] Configurando ambiente Go para ferramentas ofensivas adicionais...${RESET}"
apt install -y golang-go

# Instalação isolada do HTTPX e Subfinder direto na infraestrutura do usuário comum
echo -e "    [-] Instalando httpx (ProjectDiscovery)..."
sudo -u "$USUARIO_REAL" -H go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest >/dev/null 2>&1

echo -e "    [-] Instalando subfinder (ProjectDiscovery)..."
sudo -u "$USUARIO_REAL" -H go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest >/dev/null 2>&1

# ==============================================================================
# 3 - INSTALAÇÃO DE FERRAMENTAS VIA PIPX
# ==============================================================================
echo -e "\n${CIANO}[*] Instalando ferramentas complementares isoladas via PIPX...${RESET}"
sudo -u "$USUARIO_REAL" -H pipx ensurepath >/dev/null 2>&1

echo -e "    [-] Instalando wafw00f (Identificação de Cerca Elétrica/WAF)..."
sudo -u "$USUARIO_REAL" -H pipx install wafw00f >/dev/null 2>&1

echo -e "    [-] Instalando theHarvester (OSINT fontes abertas)..."
sudo -u "$USUARIO_REAL" -H pipx install theHarvester >/dev/null 2>&1

# ==============================================================================
# 4 - DOWNLOAD E INSTALAÇÃO DO COMBO FFUF
# ==============================================================================
echo -e "\n${CIANO}[*] Baixando e instalando o motor FFUF (Fast Fuzzing)...${RESET}"
FFUF_URL="https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz"
TMP_DIR="/tmp/ffuf_install"

mkdir -p "$TMP_DIR"
wget -q "$FFUF_URL" -O "$TMP_DIR/ffuf.tar.gz"
tar -xzf "$TMP_DIR/ffuf.tar.gz" -C "$TMP_DIR"
mv "$TMP_DIR/ffuf" /usr/local/bin/
chmod +x /usr/local/bin/ffuf
rm -rf "$TMP_DIR"
echo -e "${VERDE}[✓] FFUF binário instalado com sucesso em /usr/local/bin/ffuf${RESET}"

# ==============================================================================
# 5 - REQUISITOS PYTHON DO ARRANQUE (PYFIGLET)
# ==============================================================================
echo -e "\n${CIANO}[*] Sincronizando bibliotecas gráficas do Python...${RESET}"
pip3 install pyfiglet --break-system-packages >/dev/null 2>&1

# =============================================================================
# 7 - CRIAÇÃO DO ATALHO GLOBAL NO TERMINAL (SANA/BIOS)
# =============================================================================
echo -e "${AMARELO}[*] Criando comando global 'phanton' no terminal...${RESET}"

# Remove links antigos para avoid conflitos
rm -f "/usr/local/bin/phanton"

# Cria o link simbólico apontando direto para o novo binário compilado
ln -s "$PATH_PROJETO_GLOBAL/Phanton" "/usr/local/bin/phanton"
chmod +x "/usr/local/bin/phanton"

echo -e "${VERDE}[✓] Sucesso! Agora você pode digitar apenas 'phanton' em qualquer terminal.${RESET}"


# ==============================================================================
# 8 - GERADOR DE LANÇADORES GRÁFICOS (DESKTOP E MENU INICIAR)
# ==============================================================================
echo -e "\n${CIANO}[*] Esculpindo lançadores gráficos para o ambiente X11/Desktop...${RESET}"

# Caminho completo e absoluto do ícone oficial
ICON_PATH="$PATH_PROJETO_GLOBAL/Setup/phanton_icon.png"

# Se por acaso o ícone sumiu da pasta Setup, gera uma cópia de segurança
if [ ! -f "$ICON_PATH" ]; then
    wget -q "https://raw.githubusercontent.com/wilsonsanabio/Phanton/main/Setup/phanton_icon.png" -O "$ICON_PATH" 2>/dev/null
fi

# Conteúdo estruturado do lançador homologado pela Sana/Bios rodando o Binário
cat <<EOF > "/tmp/phanton.desktop"
[Desktop Entry]
Version=2.8
Type=Application
Name=Phanton Recon
Comment=Framework de Reconhecimento Automatizado Avançado
Exec=lxterm -e "cd $PATH_PROJETO_GLOBAL && ./Phanton"
Path=$PATH_PROJETO_GLOBAL
Icon=$ICON_PATH
Terminal=false
Categories=Network;Security;
Keywords=recon;security;nmap;ffuf;
EOF

# 🚀 8.1 - Copia para o Menu Iniciar de Aplicativos do Sistema
echo -e "    [-] Injetando lançador no Menu Iniciar..."
cp "/tmp/phanton.desktop" "/usr/share/applications/phanton.desktop"
chmod 644 "/usr/share/applications/phanton.desktop"

# 💻 8.2 - Copia para a Área de Trabalho real do usuário logado
PATH_DESKTOP=""
if [ -d "$HOME_REAL/Área de Trabalho" ]; then
    PATH_DESKTOP="$HOME_REAL/Área de Trabalho"
elif [ -d "$HOME_REAL/Desktop" ]; then
    PATH_DESKTOP="$HOME_REAL/Desktop"
elif [ -d "$HOME_REAL/Área de trabalho" ]; then
    PATH_DESKTOP="$HOME_REAL/Área de trabalho"
fi

if [ -n "$PATH_DESKTOP" ]; then
    echo -e "    [-] Injetando lançador na Área de Trabalho..."
    cp "/tmp/phanton.desktop" "$PATH_DESKTOP/phanton.desktop"
    chown "$USUARIO_REAL":"$USUARIO_REAL" "$PATH_DESKTOP/phanton.desktop"
    chmod +x "$PATH_DESKTOP/phanton.desktop"
    # Força os ambientes GNOME/XFCE antigos a confiarem no ícone imediatamente
    sudo -u "$USUARIO_REAL" gio set "$PATH_DESKTOP/phanton.desktop" metadata::trusted true 2>/dev/null
fi

rm -f "/tmp/phanton.desktop"
echo -e "${VERDE}[✓] Lançadores gráficos restaurados com sucesso!${RESET}"

# Governança de permissões final Sana/Bios para garantir posse ao usuário comum
chown -R "$USUARIO_REAL":"$USUARIO_REAL" "$PATH_PROJETO_GLOBAL"
chmod -R 755 "$PATH_PROJETO_GLOBAL"

echo -e "\n${VERDE}=======================================================${RESET}"
echo -e " ${CIANO}[✓]${RESET}${VERDE}INSTALAÇÃO E RESTAURAÇÃO GRÁFICA CONCLUÍDAS!"
echo -e " O Phanton v2.8 está 100% pronto para rodar!"
echo -e "=======================================================${RESET}"

# ==============================================================================
#  9 - PROTOCOLO DE INICIALIZAÇÃO AUTOMÁTICA SANA/BIOS
# ==============================================================================
echo -e "\n${CIANO}[*] Preparando inicialização imediata do framework...${RESET}\n"
sleep 1

opcoes=("Executar o Phanton" "Sair sem executar")
PS3=$'\n'"A configuração foi concluída com sucesso. O que deseja fazer agora? (Digite o número): "

select opt in "${opcoes[@]}"; do
    case $opt in
        "Executar o Phanton")
            echo -e "\n${CIANO}[*] Motores em marcha! Iniciando Phanton Recon...${RESET}\n"
            sleep 1
            # Muda para o diretório global e executa como o usuário comum (não-root)
            cd "$PATH_PROJETO_GLOBAL"
            sudo -u "$USUARIO_REAL" ./Phanton
            exit 0
            ;;
        "Sair sem executar")
            echo -e "\n${AZUL}[*] Entendido. A bancada da Sana/Bios está pronta para quando precisar. Até breve!${RESET}\n"
            exit 0
            ;;
    esac
done
