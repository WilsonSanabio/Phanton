# 🛸 Phanton v2.6 - Framework de Reconhecimento Automatizado

Framework avançado desenvolvido pela **Sana/Bios Informática & Consultoria** para automação de etapas de reconhecimento (Recon) em testes de intrusão e desafios de CTF.

## 🛠️ Ferramentas Integradas
O Phanton automatiza o fluxo de coleta e tabulação em Markdown das seguintes ferramentas:
* **Nmap** (Mapeamento de portas e serviços)
* **WhatWeb** (Identificação de tecnologias web)
* **Wafw00f** (Detecção de Firewalls de Aplicação Web)
* **FFUF** (Fuzzing de Diretórios, Subdomínios, APIs e Vhosts com saída JSON estável)

## 🚀 Instalação e Configuração (Kali Linux / Debian)

Para clonar o repositório e configurar todas as dependências automaticamente, rode os comandos abaixo no terminal:

```bash
git clone https://github.com/WilsonSanabio/Phanton.git
cd Phanton
chmod +x Setup/setup.sh
sudo ./Setup/setup.sh

```

## 🎯 Como Usar

Após a instalação, basta executar o script principal passando o domínio alvo:

```bash
python3 Phanton.py

```

---

🔒 *Sana/Bios Informática & Consultoria. Todos os direitos reservados.*

```
