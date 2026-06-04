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
def arruma(arq, target, inicio):
    # Define o título correto baseado no nome do arquivo intermediário
    if "_dir" in arq:
        titulo_secao = "## FFUF DIRETÓRIOS\n"
    elif "_api" in arq:
        titulo_secao = "## FFUF ENDPOINTS DE API\n"
    elif "_vho" in arq:
        titulo_secao = "## FFUF VHOSTS\n"
    else:
        titulo_secao = "## FFUF SUBDIRETÓRIOS\n"

    arqsai = arq.replace(".txt", ".md")  # Define o nome do arquivo final
    
    if os.path.exists(arq) and os.path.getsize(arq) > 0:
        try:
            with open(arq, "r", encoding="utf-8") as f:
                dados = json.load(f)

            # Verifica se o FFUF realmente pescou algum resultado real no laboratório
            if "results" in dados and dados["results"]:
                
                # Lista para acumular as linhas na memória (Performance!)
                linhas_tabela = []
                
                for item in dados["results"]:
                    fuzz_term      = item["input"].get("FUZZ", "")
                    url_completa   = item.get("url", "")
                    redirect_loc   = item.get("redirectlocation", "") if item.get("redirectlocation") else "N/A"
                    status_code    = item.get("status", "")
                    content_length = item.get("length", "")
                    
                    # Adiciona a linha formatada na nossa lista temporária em memória
                    linhas_tabela.append(f"| {fuzz_term} | {url_completa} | {redirect_loc} | {status_code} | {content_length} |\n")
                
                # AGORA SIM: Abre o arquivo de saída UMA ÚNICA VEZ e descarrega tudo
                with open(arqsai, "w", encoding="utf-8") as res:
                    # Escreve o cabeçalho estático da Sana/Bios
                    #res.write(f"✔️ URL: {target} - Data: {time.ctime(inicio)}\n")
                    #res.write(f"🔒 © Sana/Bios Informática & Consultoria.\n")
                    #res.write(f"🚫 Todos os direitos reservados\n")
                    #res.write(f"⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n")
                    #res.write("\n## DIRETÓRIOS E ROTAS ENCONTRADAS\n")
                    res.write(titulo_secao)
                    res.write("| FUZZ | URL | Redirect Location | Status Code | Content Length |\n")
                    res.write("| :--- | :--- | :--- | :--- | :--- |\n")
                    
                    # Escreve todas as linhas de rotas de uma vez só
                    res.writelines(linhas_tabela)
                
                return True  # Retorna True informando que o arquivo foi processado com sucesso e contém dados
                
        except Exception as e:
            print(f"{VERMELHO}[!] Erro ao processar o JSON do arquivo {arq}: {e}{RESET}")
            
    return False  # Se o arquivo não existir, estiver vazio, ou não tiver "results", retorna False

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
    print(f"{AMARELO}{'='*54}{RESET}")
    print(f" 🔒    \u00A9 {AZUL}Sana/Bios Informática & Consultoria - 2026{RESET}")
    print(f" 🛸 {CIANO}Framework de Reconhecimento Automatizado Avançado{RESET}")
    print(f" 🚫           {VERMELHO}Todos os direitos reservados{RESET}")
    print(f"{AMARELO}{'='*54}{RESET}\n")

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
    target_raw = input(f"{AZUL}Digite o domínio alvo (ex: alvo.com): {RESET}").strip()
    target = target_raw.replace("https://", "").replace("http://", "")
    target = target.split("/")[0]  # Remove barras residuais no final
    
    # ==============================================================
    # 1. Ajuste de Nome e Rotação Automática de Pastas Antigas
    # ==============================================================
    domain_clean = target.replace(".", "_")
    folder = os.path.join(phantom_base, "Documentos", domain_clean)
    subfolder = os.path.join(phantom_base, "Documentos", domain_clean, "JS")
    
    if os.path.exists(folder):
        print(f"{AMARELO}[!] Diretório existente encontrado para este alvo. Iniciando rotação...{RESET}")
        contador = 1
        while os.path.exists(f"{folder}_old{contador}"):
            contador += 1
        old_folder = f"{folder}_old{contador}"
        os.rename(folder, old_folder)
        print(f"{AMARELO}[✓] Pasta anterior preservada com sucesso em: {domain_clean}_old{contador}{RESET}")
        
    os.makedirs(subfolder, exist_ok=True)
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
        res.write(f"✔️ URL: {target} - Data: {time.ctime(inicio)}\n")
        res.write(f"🔒 \u00A9 Sana/Bios Informática & Consultoria.\n")
        res.write(f"🚫 Todos os direitos reservados\n")
        res.write(f"⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n")
        res.write("## DIRETÓRIOS E ROTAS ENCONTRADAS\n")

    print(f"\n{VERDE}[*] PHANTON RECON AUTOMAÇÃO - ALVO -> {target}{RESET}")
    print(f"{VERDE}[*] User-Agent -> {ua_customizado}{RESET}")
    print(f"{AZUL}    [i] As saídas serão salvas em: {folder}{RESET}")
    print(f"{AZUL}    [i] E os arquivos .js salvos em: {subfolder}\n")

    confirma = input(f"{CIANO}Tudo confirmado para o disparo? (S/N) [S]: {RESET}").strip().upper()
    
    if confirma == "S" or confirma == "":
        limpar_tela()
        print(f"{VERDE}[+] Confirmação OK. Iniciando varredura para o ALVO -> {target} ...{RESET}\n")
    else:
        limpar_tela()
        print(f"{VERDE}[!] Operação abortada pelo operador. Desligando bancada.{RESET}")
        exit()

    # ==============================================================
    # 2. INFRAESTRUTURA
    # ==============================================================
    print(f"{AMARELO}[*] A mapear infraestrutura (Whois, DNS, Conectividade, WAF)...{RESET}")
    infra_out = f"{folder}/{domain_clean}_infra.md"
    waf_temp = f"{folder}/temp_waf.txt"
    
    # Cabeçalho padrão
    os.system(f"echo '✔️ URL: {target} - Data: {time.ctime(inicio)}' > {infra_out}")
    os.system(f"echo '🔒 \u00A9 Sana/Bios Informática & Consultoria.' >> {infra_out}")
    os.system(f"echo '🚫 Todos os direitos reservados\n' >> {infra_out}")
    os.system(f"echo '⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n' >> {infra_out}")
    os.system(f"echo '# INFRAESTRUTURA\n' >> {infra_out}")

    # ==============================================================
    # 2.1 WHOIS
    # ==============================================================  
    print(f"    [-] Verificando o domínio")
    os.system(f"echo '## WHOIS' >> {infra_out} && whois {target} >> {infra_out} 2>/dev/null")

    # ==============================================================
    # 2.2 DNS/HOST
    # ==============================================================  
    print(f"    [-] Pesquisando os IPs")
    os.system(f"echo '\n## DNS/HOST' >> {infra_out} && host {target} >> {infra_out}")

    # ==============================================================
    # 2.3 PING
    # ==============================================================  
    print(f"    [-] Fazendo um Ping")
    os.system(f"echo '\n## PING' >> {infra_out} && ping -c 3 {target} >> {infra_out}")

    # ==============================================================
    # 2.4 WHATWEB
    # ==============================================================  
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

    # ==============================================================
    # 2.5 PESQUISA DE IP E REGISTROS (A e MX)
    # ==============================================================  
    print(f"    [-] Pesquisando os IPs e Registros MX")
    os.system(f"echo '\n## REGISTROS DNS A (IPs)' >> {infra_out} && dig {target} A +noall +answer >> {infra_out}")
    os.system(f"echo '\n## REGISTROS DNS MX (E-mails)' >> {infra_out} && dig {target} MX +noall +answer >> {infra_out}")

    # ==============================================================
    # 2.6 THEHARVESTER
    # ==============================================================  
    print(f"    [-] Fazendo OSINT em fontes abertas (theHarvester)")
    os.system(f"echo '\n## OSINT - THEHARVESTER' >> {infra_out} && theHarvester -d {target} -l 200 -b crtsh,duckduckgo,urlscan | sed '1,15d' >> {infra_out}")

    # ==============================================================
    # 2.7 SUBFINDER (Fase de Descoberta e Registro Bruto)
    # ==============================================================  
    print(f"    [-] Fazendo OSINT em fontes abertas (Subfinder)...")
    
    arquivo_tmp = f"{folder}/subdominios_tmp.txt"
    # Executa o subfinder e joga a lista bruta no arquivo temporário
    os.system(f"subfinder -d {target} -silent > {arquivo_tmp}")

    try:
        conteudo_subfinder = ""
        if os.path.exists(arquivo_tmp):
            with open(arquivo_tmp, "r", encoding="utf-8") as tmp:
                conteudo_subfinder = tmp.read()
        
        # Anexa a lista BRUTA do Subfinder diretamente no relatório oficial
        with open(infra_out, "a", encoding="utf-8") as f:
            f.write("\n## OSINT - SUBFINDER (Lista Bruta)\n")
            f.write("```text\n") 
            f.write(conteudo_subfinder)
            f.write("```\n")
            
    except Exception as e:
        print(f"    [!] Erro ao gravar dados do Subfinder: {e}")

    # ==============================================================
    # 2.8 HTTPX (Validação de Ativos com Status 200 via Instalação Go)
    # ==============================================================
    print(f"    [-] Validando subdomínios ativos com HTTPX...")
    
    with open(infra_out, "a", encoding="utf-8") as f:
        f.write("\n## Subdomínios Ativos Encontrados (Status 200)\n")

    # Chamada direta ao httpx (garantindo o uso do binário do Go presente no sistema)
    os.system(
        f"cat {arquivo_tmp} | "
        f"~/go/bin/httpx -silent -sc -title -mc 200 -H 'User-Agent: {ua_customizado}' >> {infra_out}"
    )

    # ==============================================================
    # 2.9 LIMPEZA DA BANCADA INTERMEDIÁRIA
    # ==============================================================
    if os.path.exists(arquivo_tmp):
        os.remove(arquivo_tmp)

    print(f"{CIANO}[✓] Infraestrutura mapeada com sucesso!\n{RESET}")  

    # ==============================================================
    # 3. NMAP
    # ==============================================================
    print(f"{AMARELO}[*] A verificar portas e serviços (Nmap)...{RESET}")
    nmap_out = f"{folder}/{domain_clean}_nmap.md"
    nmap_temp = f"{folder}/{domain_clean}_nmap.tmp"

    # 3.1. Executa o Nmap salvando no arquivo temporário
    os.system(f"nmap -sV -sC {target} --script-args http.useragent='{ua_customizado}' -oN {nmap_temp} > /dev/null 2>&1")

    # 3.2. Une o cabeçalho padronizado com o resultado do Nmap usando Python puro
    try:
        conteudo_nmap = ""
        if os.path.exists(nmap_temp):
            with open(nmap_temp, "r") as tmp:
                conteudo_nmap = tmp.read()
            os.remove(nmap_temp) # Remove o temporário para limpar a área
        with open(nmap_out, "w") as f:

            # Cabeçalho padrão
            f.write(f"✔️ URL: {target} - Data: {time.ctime(inicio)}\n")
            f.write(f"🔒 Sana/Bios Informática & Consultoria.\n")
            f.write(f"🚫 Todos os direitos reservados\n")
            f.write(f"⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n")
            f.write("## NMAP -sV -sC\n")
            f.write(conteudo_nmap)
    except Exception as e:
        print(f"{VERMELHO}[!] Erro ao formatar cabeçalho do Nmap: {e}{RESET}")
    print(f"{CIANO}[✓] Portas e Serviços mapeadas\n{RESET}")

    # ==============================================================
    # 4. CABEÇALHO
    # ==============================================================
    print(f"{AMARELO}[*] A capturar cabeçalhos HTTP...{RESET}")
    cab_path = f"{folder}/{domain_clean}_cabecalho.md"

    # Cabeçalho padrão
    os.system(f"echo '✔️ URL: {target} - Data: {time.ctime(inicio)}' > {cab_path}")
    os.system(f"echo '🔒 \u00A9 Sana/Bios Informática & Consultoria.' >> {cab_path}")
    os.system(f"echo '🚫 Todos os direitos reservados\n' >> {cab_path}")
    os.system(f"echo '⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n' >> {cab_path}")
    os.system(f"echo '## CABAÇALHO' >> {cab_path}")
    os.system(f"curl -I -s https://{target} -H 'User-Agent: {ua_customizado}' >> {cab_path}")
    
    with open(cab_path, "r") as f:
        headers = f.read()
        if "Set-Cookie" in headers:
            print(f"{VERMELHO}[!] ALERTA: Cookies detetados na resposta!{RESET}")
            with open(resumo_path, "a") as res:
                res.write("## ⚠️ Segurança\n- Cookies encontrados no cabeçalho.\n\n")
        else:
            print(f"  {AMARELO}[-] Nenhum cookie ou tecnologia óbvia exposta.{RESET}")
        print(f"{CIANO}[✓] Cabeçalho extraído\n{RESET}")

    # ==============================================================
    # 5. BUSCA RÁPIDA POR API NO CÓDIGO HTML
    # ==============================================================
    print(f"{AMARELO}[*] A vasculhar referências de API no domínio...{RESET}")
    api_list_out = f"{folder}/{domain_clean}_api_list.md"
    
    with open(api_list_out, "w") as f_api:


        # Cabeçalho padrão
        f_api.write(f"✔️ URL: {target} - Data: {time.ctime(inicio)}\n")
        f_api.write(f"🔒 \u00A9 Sana/Bios Informática & Consultoria.\n")
        f_api.write(f"🚫 Todos os direitos reservados\n")
        f_api.write(f"⛔ RELATÓRIO PHANTON TÉCNICO DE RECON\n\n")
        f_api.write("## REFERÊNCIAS DE API\n")
        
    os.system(f"curl -s https://{target} -H 'User-Agent: {ua_customizado}' | grep -oP '/api/[a-zA-Z0-9/_-]+' | sort -u >> {api_list_out}")
    
    if os.path.getsize(api_list_out) <= 100:  # Ajustado limite de tamanho por conta do cabeçalho de copyright
        os.remove(api_list_out)
        print(f"{CIANO}[✓] APIs verificadas: nenhuma referência encontrada no HTML principal.{RESET}")
        print(f"{AMARELO}[i] O Phanton usará a wordlist complementar: {os.path.basename(W_API)}{RESET}\n")
    else:
        print(f"{VERDE}[✓] APIs verificadas: referências extraídas e salvas no relatório.{RESET}\n")

    # ==============================================================
    # 6. FFUF (Diretórios, Subdomínios, APIs e VHOSTs)
    # ==============================================================
    print(f"{AMARELO}[*] A iniciar Fuzzing silencioso...{RESET}")
    print(f"    [+] AGUARDE: O Phanton está a processar as wordlists. Isto pode demorar alguns minutos.{RESET}", flush=True)
    
    dir_out = f"{folder}/{domain_clean}_dir.txt"
    sub_out = f"{folder}/{domain_clean}_sub.txt"
    api_out = f"{folder}/{domain_clean}_api.txt"
    vho_out = f"{folder}/{domain_clean}_vho.txt"
 
    # ==============================================================
    # 6.1 DIRETÓRIOS
    # ==============================================================   
    print(f"        [-] A varrer Diretórios...", flush=True)
    os.system(f"ffuf -u https://{target}/FUZZ -w {W_DIR} -mc 200,301,302 -t 20 -p 0.1 -H 'User-Agent: {ua_customizado}' -o {dir_out} -s")
    #arruma(dir_out, target, inicio)

    # ==============================================================
    # 6.2 SUBDOMÍNIOS
    # ==============================================================     
    print(f"        [-] A varrer Subdomínios...", flush=True)
    os.system(f"ffuf -u https://FUZZ.{target} -w {W_SUB} -mc 200,301,302 -t 20 -H 'User-Agent: {ua_customizado}' -o {sub_out} -s")
    #arruma(sub_out, target, inicio)

    # ==============================================================
    # 6.3 ENDPOINTS DE API
    # ==============================================================     
    print(f"       [-] A varrer Estruturas de API (Wordlist Moderna)...", flush=True)
    os.system(f"ffuf -u https://{target}/FUZZ -w {W_API} -mc 200,301,302,401,403 -t 20 -p 0.1 -H 'User-Agent: {ua_customizado}' -o {api_out} -s")
    #arruma(api_out, target, inicio)

    # ==============================================================
    # 6.4 VIRTUL HOST (VHOST)
    # ============================================================== 
    print(f"        [-] Procurando Virtual Hosts (VHOSTs)...", flush=True)
    os.system(f"ffuf -u https://{target} -w {W_SUB} -H 'Host: FUZZ.{target}' -H 'User-Agent: {ua_customizado}' -mc 200,301,302,403 -o {vho_out} -s")
    #arruma(vho_out, target, inicio)
    
    print(f"{CIANO}[✓] FUZZ terminado. Todos os relatórios foram limpos e consolidados em Markdown!{RESET}\n")

# ==============================================================
    # 7. EXTRAÇÃO DE ARQUIVOS JS 
    # ==============================================================
    print(f"{AMARELO}[*] Extraindo scripts Javascript (.js) do alvo...{RESET}")
    print(f"    [-] Executando mineração em segundo plano via Wget...")

    # [AJUSTE DE BANCADA]: Usando a flag -P para injetar os downloads direto na pasta certa,
    # adicionado o http:// para garantir que o wget não falhe e mitigando a saída com o -q se quiser silenciar.
    os.system(f"wget -q -r -np -nd -A '.js' -P '{subfolder}' http://{target}/ -U '{ua_customizado}'")

    print(f"{CIANO}[✓] Downloads de scripts JS concluídos e salvos na pasta 'JS'.{RESET}\n")

    # ==============================================================
    # 7.1 Verificando a existência de Source Map Leakage (SML)
    # ==============================================================
    print(f"{AMARELO}[*] Escavando metadados e possíveis vazamentos nos scripts...{RESET}")
    sml_out = os.path.join(folder, f"{domain_clean}_sml.md")
    
    vazamentos_sml = []

    # Se a pasta existe e tem arquivos, fazemos a varredura
    if os.path.exists(subfolder):
        arquivos_js = [f for f in os.listdir(subfolder) if f.endswith('.js')]
        
        for arquivo_js in arquivos_js:
            caminho_completo = os.path.join(subfolder, arquivo_js)
            try:
                with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f_js:
                    # Lemos o final do arquivo (onde o mapa costuma ficar escondido)
                    conteudo = f_js.read()
                    if "sourceMappingURL=" in conteudo[-2000:]:
                        vazamentos_sml.append(arquivo_js)
            except Exception:
                pass

    # Se a escavação encontrar algo, gera o relatório Markdown dedicado
    if vazamentos_sml:
        print(f"     {VERMELHO}[!] ALERTA: Identificado Source Map Leakage nos estáticos!{RESET}")
        with open(sml_out, "w", encoding="utf-8") as f_sml:
            f_sml.write(f"✔️ URL: {target} - Data: {time.ctime(inicio)}\n")
            f_sml.write(f"🔒 © Sana/Bios Informática & Consultoria - 2026\n")
            f_sml.write(f"🚫 Todos os direitos reservados\n\n")
            f_sml.write(f"## 🎯 RELATÓRIO DE EXPOSIÇÃO DE SOURCE MAPS\n\n")
            f_sml.write("Os seguintes arquivos contêm mapeamento reverso ativo para o código-fonte:\n\n")
            for item in vazamentos_sml:
                f_sml.write(f"- 📄 `{item}` -> Possui referência a arquivo `.map`.\n")
        print(f"{VERDE}[✓] Relatório SML gerado com sucesso em: {sml_out}{RESET}\n")
    else:
        print(f"{VERDE}[✓] Varredura concluída: Nenhum indicador óbvio de SML nos arquivos.{RESET}\n")

    # ==============================================================
    # 8. EXIBIÇÃO E EXTRAÇÃO INTELIGENTE DE RESULTADOS (CONSOLIDADO)
    # ==============================================================
    print(f"\n{AZUL}=================================================={RESET}")
    print(f"{VERDE}   RESUMO DE ACHADOS PHANTON (RELATÓRIO FINAL){RESET}")
    print(f"{AZUL}=================================================={RESET}")

    with open(resumo_path, "a") as res:
        # Cabeçalho padrão

        res.write("## DIRETÓRIOS E ROTAS ENCONTRADAS\n\n")
        
        arquivos_fuzz = [dir_out, sub_out, api_out, vho_out]
        
        # No bloco de consolidação de dados do Phanton.py:
        for arq in arquivos_fuzz:
            # A própria função arruma() processa e nos diz se o resultado foi útil (True) ou vazio (False)
            houve_sucesso = arruma(arq, target, inicio)
            
            if houve_sucesso:
                print(f"{VERDE}    [+] Resultados válidos processados para {arq}. Integrando ao relatório...{RESET}")
                arqsai = arq.replace(".txt", ".md")
                
                # Aqui entra a sua lógica existente para ler o 'arqsai' e injetar 
                # o conteúdo dele dentro do seu relatório consolidado final (ex: resumo_path)
                with open(arqsai, "r", encoding="utf-8") as f_md:
                    conteudo_formatado = f_md.read()
                    
                with open(resumo_path, "a", encoding="utf-8") as f_final:
                    f_final.write(conteudo_formatado)
                    f_final.write("\n\n")
            else:
                print(f"{AMARELO}    [-] Arquivo {arq} limpo (sem endpoints válidos). Ignorado.{RESET}")

    # ==============================================================
    # 9. 🧹 LIMPEZA DA BANCADA (Todos os provisórios inclusos)
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
