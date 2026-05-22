#!/usr/bin/env python3
import os
import time
import subprocess
import re
import pyfiglet
import json

# Códigos de Cores ANSI para Destaque (Declarados no topo para uso global)
VERDE = '\033[92m'
AMARELO = '\033[93m'
VERMELHO = '\033[91m'
AZUL = '\033[94m'
CIANO = '\033[96m'
RESET = '\033[0m'

# ==========================================
# INÍCIO DAS FUNÇÕES DE SUPORTE (BANCADA)
# ==========================================

# Função para arrumar os arquivos do FFUF
def arruma(arq):
    # O próprio Python investiga o nome do arquivo para definir o cabeçalho
    if "_dir" in arq:
        titulo = "## FFUF DIRETÓRIOS\n\n"
    elif "_api" in arq:
        titulo = "## FFUF ENDPOINTS DE API\n\n"
    elif "_vho" in arq:
        titulo = "## FFUF VHOSTS\n\n"
    else:
        titulo = "## FFUF SUBDIRETÓRIOS\n\n"
    arqsai = arq.replace(".txt", ".md")  # Garante a extensão de saída correta
    # Monta a estrutura inicial gravando os direitos autorais e limpando o arquivo antigo
    with open(arqsai, "w") as res:
        res.write("🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n")
        res.write("[*] Iniciado em: {time.ctime(inicio)}\n\n")
        res.write(titulo)
        res.write("| FUZZ | URL | Redirect Location | Status Code | Content Length |\n")
        res.write("| :--- | :--- | :--- | :--- | :--- |\n")
    # Processa o arquivo JSON bruto do FFUF
    if os.path.exists(arq) and os.path.getsize(arq) > 0:
        try:
            with open(arq, "r") as f:
                dados = json.load(f)
            # O ffuf joga os achados dentro da chave 'results'
            if "results" in dados:
                for item in dados["results"]:
                    # Coleta de dados segura usando .get() para evitar travar o script
                    fuzz_term      = item["input"].get("FUZZ", "")
                    url_completa   = item.get("url", "")
                    redirect_loc   = item.get("redirectlocation", "") if item.get("redirectlocation") else "N/A"
                    status_code    = item.get("status", "")
                    content_length = item.get("length", "")
                    nova_linha = f"| {fuzz_term} | {url_completa} | {redirect_loc} | {status_code} | {content_length} |\n"
                    with open(arqsai, "a") as res:
                        res.write(nova_linha)
        except Exception as e:
            print(f"{VERMELHO}[!] Erro ao processar o JSON do arquivo {arq}: {e}{RESET}")

# Função para limpar a tela
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Exibir Banner unificado e atualizado com Copyright 2026
def exibir_banner():
    limpar_tela()
    logo = pyfiglet.figlet_format("PHANTON RECON", font="slant")
    print(f"{VERDE}{logo}{RESET}")
    print(f"{AMARELO}{'='*55}{RESET}")
    print(f"{AZUL}🔒 \u00A9 Sana/Bios Informática & Consultoria - 2026{RESET}")
    print(f"{CIANO}🛸 Framework de Reconhecimento Automatizado Avançado{RESET}")
    print(f"{AMARELO}{'='*55}{RESET}\n")

# ==========================================
# FIM DAS FUNÇÕES DE SUPORTE (BANCADA)
# ==========================================

# Configurações de Wordlists Oficiais (Ajustadas para o Teste de Fogo)
BASE_PATH_RESOURCES = "/home/sanabio/Phanton/wordlists/"
W_DIR = os.path.join(BASE_PATH_RESOURCES, "common.txt")
W_SUB = os.path.join(BASE_PATH_RESOURCES, "subdomains-top1million-5000.txt")
W_API = os.path.join(BASE_PATH_RESOURCES, "common-api-endpoints.txt")

def main():
    exibir_banner()
    
    # Define o caminho da pasta Phanton na home do usuário
    home_dir = os.path.expanduser("~")
    phantom_base = os.path.join(home_dir, "Phanton")

    if not os.path.exists(phantom_base):
        print(f"{AMARELO}[!] Pasta ~/Phanton não encontrada. Criando...{RESET}")
        os.makedirs(phantom_base)

    # Pergunta o domínio do alvo
    target_raw = input(f"{AZUL}Digite o domínio alvo (ex: smartfit.com.br): {RESET}").strip()
    target = target_raw.replace("https://", "").replace("http://", "")
    target = target.split("/")[0]  # Remove barras residuais no final
    
    # ==============================================================
    # 1. Ajuste de Nome e Rotação Automática de Pastas Antigas
    # ==============================================================
    domain_clean = target.replace(".", "_")
    folder = os.path.join(phantom_base, "Documentos", domain_clean)
    
    if os.path.exists(folder):
        print(f"{AMARELO}[!] Diretório existente encontrado para este alvo. Iniciando rotação...{RESET}")
        contador = 1
        while os.path.exists(f"{folder}_old{contador}"):
            contador += 1
        old_folder = f"{folder}_old{contador}"
        os.rename(folder, old_folder)
        print(f"{AMARELO}[✓] Pasta anterior preservada com sucesso em: {domain_clean}_old{contador}{RESET}")
        
    os.makedirs(folder, exist_ok=True)
    print(f"{VERDE}[✓] Novo diretório de trabalho pronto para o combate: {folder}{RESET}")
   
    print("\n")
    
    # Pergunta o User-Agent (Opcional)
    print(f"{AZUL}1 - User-Agent padrão - Mozilla{RESET}")
    print(f"{AZUL}2 - User-Agent Bughunt - Security Research{RESET}")
    print(f"{AZUL}3 - User-Agent Customizado\n{RESET}")

    ua_opcao = input(f"{AZUL}Sua opção para o User-Agent: {RESET}")

    if ua_opcao == "1" or ua_opcao == "":
        ua_customizado = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    elif ua_opcao == "2":
        ua_customizado = "Bughunt - Security Research"
    else:
        ua_customizado = input(f"{AZUL}User-Agent: {RESET}")
    
    inicio = time.time()  # Começa a contar depois das entradas do operador

    # Criação do arquivo central de resultados consolidados
    resumo_path = os.path.join(folder, "RESULTADOS_IMPORTANTES.md")
    
    with open(resumo_path, "w") as res:
        res.write(f"# 🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n")
        res.write(f"[*] Iniciado em: {time.ctime(inicio)}\n\n")
        res.write(f"# 🚩 RELATÓRIO PHANTON: {target}\n")

    print(f"\n{VERDE}[*] PHANTON RECON AUTOMAÇÃO - ALVO -> {target}{RESET}")
    print(f"{VERDE}[*] User-Agent -> {ua_customizado}{RESET}")
    print(f"{AZUL}[i] Saídas serão salvas em: {folder}{RESET}\n")

    confirma = input(f"{CIANO}Tudo confirmado para o disparo? (S/N) [S]: {RESET}").strip().upper()
    
    if confirma == "S" or confirma == "":
        limpar_tela()
        print(f"{VERDE}[+] Motores aquecidos. Iniciando varredura para o ALVO -> {target}...{RESET}\n")
    else:
        limpar_tela()
        print(f"{VERDE}[!] Operação abortada pelo operador. Desligando bancada.{RESET}")
        exit()

    # 2. INFRAESTRUTURA
    print(f"{AMARELO}[*] A mapear infraestrutura (Whois, DNS, Conectividade, WAF)...{RESET}")
    infra_out = f"{folder}/{domain_clean}_infra.md"
    waf_temp = f"{folder}/temp_waf.txt"
    
    os.system(f"echo '🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados' > {infra_out}")
    os.system(f"echo '[*] Iniciado em: {time.ctime(inicio)}\n\n' >> {infra_out}")
    os.system(f"echo '# Infraestrutura\n' >> {infra_out}")

    print(f"    [-] Verificando o domínio")
    os.system(f"echo '## WHOIS\n' >> {infra_out} && whois {target} >> {infra_out} 2>/dev/null")

    print(f"    [-] Pesquisando os IPs")
    os.system(f"echo '\n## DNS/HOST' >> {infra_out} && host {target} >> {infra_out}")

    print(f"    [-] Fazendo um Ping")
    os.system(f"echo '\n## PING' >> {infra_out} && ping -c 3 {target} >> {infra_out}")

    print(f"    [-] Rodando o Whatweb")
    os.system(f"echo '\n## WHATWEB' >> {infra_out} && whatweb {target} --color=never >> {infra_out}")

    print(f"    [-] Verificando WAF")
    os.system(f"wafw00f {target} -o {waf_temp} > /dev/null 2>&1")
    
    if os.path.exists(waf_temp):
        os.system(f"echo '\n## WAF DETECTION' >> {infra_out}")
        os.system(f"cat {waf_temp} >> {infra_out}")
        os.system(f"echo '' >> {infra_out}")
        os.system(f"rm {waf_temp}")
    else:
        os.system(f"echo '\n## WAF DETECTION\nNão foi possível detectar o WAF.' >> {infra_out}")

    print(f"    [-] Pesquisando os IPs e Registros MX")
    os.system(f"echo '\n## REGISTROS DNS A (IPs)' >> {infra_out} && dig {target} A +noall +answer >> {infra_out}")
    os.system(f"echo '\n## REGISTROS DNS MX (E-mails)' >> {infra_out} && dig {target} MX +noall +answer >> {infra_out}")

    print(f"    [-] Fazendo OSINT em fontes abertas (theHarvester)")
    os.system(f"echo '\n## OSINT - THEHARVESTER' >> {infra_out} && theHarvester -d {target} -l 200 -b crtsh,duckduckgo,urlscan | sed '1,15d' >> {infra_out}")

    print(f"    [-] Fazendo OSINT em fontes abertas (Subfinder)")
    os.system(f"echo '\n## OSINT - SUBFINDER' >> {infra_out} && subfinder -d {target} -silent >> {infra_out}")
    print(f"{CIANO}[✓] Infraestrutura mapeada com sucesso!\n{RESET}")

    # 3. NMAP
    print(f"{AMARELO}[*] A verificar portas e serviços (Nmap)...{RESET}")
    nmap_out = f"{folder}/{domain_clean}_nmap.md"
    nmap_temp = f"{folder}/{domain_clean}_nmap.tmp"
    # 1. Executa o Nmap salvando no arquivo temporário
    os.system(f"nmap -sV -sC {target} --script-args http.useragent='{ua_customizado}' -oN {nmap_temp} > /dev/null 2>&1")
    # 2. Une o cabeçalho padronizado com o resultado do Nmap usando Python puro
    try:
        conteudo_nmap = ""
        if os.path.exists(nmap_temp):
            with open(nmap_temp, "r") as tmp:
                conteudo_nmap = tmp.read()
            os.remove(nmap_temp) # Remove o temporário para limpar a área
        with open(nmap_out, "w") as f:
            f.write("# 🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n")
            f.write(f"[*] Iniciado em: {time.ctime(inicio)}\n\n")
            f.write("## NMAP -sV -sC\n")
            f.write(conteudo_nmap)
    except Exception as e:
        print(f"{VERMELHO}[!] Erro ao formatar cabeçalho do Nmap: {e}{RESET}")
    print(f"{CIANO}[✓] Portas e Serviços mapeadas\n{RESET}")

    # 4. CABEÇALHO
    print(f"{AMARELO}[*] A capturar cabeçalhos HTTP...{RESET}")
    cab_path = f"{folder}/{domain_clean}_cabecalho.md"
    os.system(f"echo '🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n' > {cab_path}")
    os.system(f"echo '[*] Iniciado em: {time.ctime(inicio)}\n\n' >> {cab_path}")
    os.system(f"echo '# Cabeçalho' >> {cab_path}")
    os.system(f"curl -I -s https://{target} -H 'User-Agent: {ua_customizado}' >> {cab_path}")
    
    with open(cab_path, "r") as f:
        headers = f.read()
        if "Set-Cookie" in headers:
            print(f"{VERMELHO}[!] ALERTA: Cookies detetados na resposta!{RESET}")
            with open(resumo_path, "a") as res:
                res.write("## 🍪 Segurança\n- Cookies encontrados no cabeçalho.\n\n")
        else:
            print(f"  {AMARELO}[-] Nenhum cookie ou tecnologia óbvia exposta.{RESET}")
        print(f"{CIANO}[✓] Cabeçalho extraído\n{RESET}")

    # 5. BUSCA RÁPIDA POR API NO CÓDIGO HTML
    print(f"{AMARELO}[*] A vasculhar referências de API no domínio...{RESET}")
    api_list_out = f"{folder}/{domain_clean}_api_list.md"
    
    with open(api_list_out, "w") as f_api:
        f_api.write("🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n")
        f_api.write(f"[*] Iniciado em: {time.ctime(inicio)}\n\n")
        f_api.write("# Referências de API\n")
        
    os.system(f"curl -s https://{target} -H 'User-Agent: {ua_customizado}' | grep -oP '/api/[a-zA-Z0-9/_-]+' | sort -u >> {api_list_out}")
    
    if os.path.getsize(api_list_out) <= 100:  # Ajustado limite de tamanho por conta do cabeçalho de copyright
        os.remove(api_list_out)
        print(f"{CIANO}[✓] APIs verificadas: nenhuma referência encontrada no HTML principal.{RESET}")
        print(f"{AMARELO}[i] O Phanton usará a wordlist complementar: {os.path.basename(W_API)}{RESET}\n")
    else:
        print(f"{VERDE}[✓] APIs verificadas: referências extraídas e salvas no relatório.{RESET}\n")

    # 6. FFUF (Diretórios, Subdomínios, APIs e VHOSTs)
    print(f"{AMARELO}[*] A iniciar Fuzzing silencioso...{RESET}")
    print(f"[...] AGUARDE: O Phanton está a processar as wordlists. Isto pode demorar alguns minutos.{RESET}", flush=True)
    
    dir_out = f"{folder}/{domain_clean}_dir.txt"
    sub_out = f"{folder}/{domain_clean}_sub.txt"
    api_out = f"{folder}/{domain_clean}_api.txt"
    vho_out = f"{folder}/{domain_clean}_vho.txt"
    
    # PASSO 1: Diretórios
    print(f"    [-] A varrer Diretórios...", flush=True)
    os.system(f"ffuf -u https://{target}/FUZZ -w {W_DIR} -mc 200,301,302 -t 20 -p 0.1 -H 'User-Agent: {ua_customizado}' -o {dir_out} -s")
    arruma(dir_out)
    
    # PASSO 2: Subdomínios
    print(f"    [-] A varrer Subdomínios...", flush=True)
    os.system(f"ffuf -u https://FUZZ.{target} -w {W_SUB} -mc 200,301,302 -t 20 -H 'User-Agent: {ua_customizado}' -o {sub_out} -s")
    arruma(sub_out)
    
    # PASSO 3: Endpoints de API
    print(f"    [-] A varrer Estruturas de API (Wordlist Moderna)...", flush=True)
    os.system(f"ffuf -u https://{target}/FUZZ -w {W_API} -mc 200,301,302,401,403 -t 20 -p 0.1 -H 'User-Agent: {ua_customizado}' -o {api_out} -s")
    arruma(api_out)

    # PASSO 4: Virtual Hosts (VHOSTs)
    print(f"    [-] Procurando Virtual Hosts (VHOSTs)...", flush=True)
    os.system(f"ffuf -u https://{target} -w {W_SUB} -H 'Host: FUZZ.{target}' -H 'User-Agent: {ua_customizado}' -mc 200,301,302,403 -o {vho_out} -s")
    arruma(vho_out)
    
    print(f"{CIANO}[✓] FUZZ terminado. Todos os relatórios foram limpos e consolidados em Markdown!{RESET}\n")

# ==============================================================
    # 7. EXIBIÇÃO E EXTRAÇÃO INTELIGENTE DE RESULTADOS (CONSOLIDADO)
    # ==============================================================
    print(f"\n{AZUL}=================================================={RESET}")
    print(f"{VERDE}   RESUMO DE ACHADOS PHANTON (RELATÓRIO FINAL){RESET}")
    print(f"{AZUL}=================================================={RESET}")

    with open(resumo_path, "a") as res:
        res.write("🔒 Sana/Bios Informática & Consultoria. Todos os direitos reservados\n\n")
        res.write("## 🔍 DIRETÓRIOS E ROTAS ENCONTRADAS\n\n")
        
        arquivos_fuzz = [dir_out, sub_out, api_out, vho_out]
        
        for arq in arquivos_fuzz:
            if os.path.exists(dir_out) and os.path.getsize(arq) > 0:
                try:
                    with open(dir_out, "r") as f:
                        dados = json.load(f)
                        
                    if "results" in dados:
                        for item in dados["results"]:
                            status_code = item.get("status", 0)
                            
                            # Filtro inteligente pelos status desejados
                            if status_code in [200, 301, 302, 401, 403, 500]:
                                fuzz_term      = item["input"].get("FUZZ", "")
                                url_completa   = item.get("url", "")
                                redirect_loc   = item.get("redirectlocation", "") if item.get("redirectlocation") else "N/A"
                                content_length = item.get("length", "")
                                
                                # Escreve no relatório consolidado (.md)
                                res.write(f"- **Rota/Alvo: `/{fuzz_term}` | **Status: `{status_code}` | **Tamanho: `{content_length} bytes` | **URL: {url_completa}\n")
                                if redirect_loc != "N/A":
                                    res.write(f"  - Redirecionamento: {redirect_loc}\n")
                                res.write("\n")
                                
                                # Formatação elegante para o Terminal em tempo real
                                print(f"{VERDE}[+] ENCONTRADO:{RESET} /{fuzz_term} {AMARELO}(Status: {status_code} | Size: {content_length}){RESET}")
                except Exception as e:
                    pass  # Evita que um arquivo corrompido quebre o encerramento do script

    # ==============================================================
    # 🧹 LIMPEZA DA BANCADA (Todos os provisórios inclusos)
    # ==============================================================
    print(f"\n{AMARELO}[*] Finalizando os trabalhos e limpando arquivos brutos...{RESET}")
    # [CORRIGIDO]: vho_out adicionado ao ciclo de limpeza
    for arquivo_provisorio in [dir_out, sub_out, api_out, vho_out]:
        if os.path.exists(arquivo_provisorio):
            os.remove(arquivo_provisorio)
            print(f"[-] Arquivo temporário deletado: {arquivo_provisorio}")#

    # Finalização do Tempo 
    fim = time.time()
    tempo_total = time.strftime("%H:%M:%S", time.gmtime(fim - inicio))
    
    with open(resumo_path, "a") as res:
        res.write(f"\n\n**Tempo total de varredura:** {tempo_total}\n")
        
    print(f"\n{AZUL}[+] Missão cumprida em: {tempo_total}{RESET}")
    print(f"{AZUL}[*] Relatório final limpo em: {resumo_path}{RESET}")

    # --- EXIBIR O RELATÓRIO NA TELA ---
    print(f"\n{AMARELO}{'='*40}{RESET}")
    print(f"{VERDE}📄 CONTEÚDO DO RELATÓRIO FINAL:{RESET}")
    print(f"{AMARELO}{'='*40}{RESET}\n")
    
    if os.path.exists(resumo_path):
        with open(resumo_path, "r") as res:
            print(res.read())
    
    print(f"{AMARELO}{'='*40}{RESET}")
    
    print(f"\n{AZUL}[👉] Para entrar na pasta de resultados, copie e cole:{RESET}")
    print(f"{VERDE}cd {folder}{RESET}\n")

if __name__ == "__main__":
    main()
