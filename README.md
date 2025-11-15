# 🗂️ Organizador de PC Caótico
<img width="610" height="740" alt="projeto" src="https://github.com/user-attachments/assets/44b2ebca-e5c5-47d6-b956-32e5bc4e65d9" />

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg)

**Uma solução inteligente para organizar automaticamente seus arquivos e acabar com a bagunça no computador!**

---

## 🎯 Sobre o Projeto

Você já abriu sua pasta de Downloads e encontrou um caos completo? Imagens, documentos, vídeos e programas todos misturados? O **Organizador de PC Caótico** é a solução definitiva para esse problema!

Este projeto Python oferece uma suite completa de ferramentas para:
- 🔍 **Encontrar arquivos duplicados** usando hash MD5
- 📂 **Organizar automaticamente** por tipo e categoria
- 🧹 **Limpar a pasta de Downloads** com um clique
- 💾 **Identificar arquivos grandes** que ocupam espaço desnecessário
- 📊 **Gerar relatórios detalhados** do seu sistema de arquivos

---

## ✨ Funcionalidades

### 🎨 Interface Gráfica Moderna
- Interface intuitiva e dark theme
- Barra de progresso em tempo real
- Operações não-bloqueantes com threading
- Logs detalhados de todas as operações

### 🔍 Detector de Duplicados Inteligente
- Usa algoritmo de hash MD5 para comparação precisa
- Ignora arquivos muito pequenos para melhor performance
- Mostra localização exata dos arquivos duplicados

### 📂 Sistema de Organização
- **12 categorias pré-definidas:**
  - 🖼️ Imagens (JPG, PNG, GIF, etc.)
  - 📄 Documentos (PDF, DOC, TXT, etc.)
  - 🎬 Vídeos (MP4, AVI, MOV, etc.)
  - 🎵 Músicas (MP3, WAV, FLAC, etc.)
  - 📦 Compactados (ZIP, RAR, 7z, etc.)
  - ⚙️ Programas (EXE, MSI, DEB, etc.)
  - 💻 Códigos (PY, JS, HTML, etc.)
  - 📊 Planilhas (CSV, XLS, ODS, etc.)
  - 🎤 Apresentações (PPT, PPTX, etc.)
  - 🎮 E muito mais!

### 🧹 Limpeza Automática de Downloads
- Foco especial na pasta mais caótica do sistema
- Organização instantânea com um clique
- Preserva a estrutura de subpastas

### 💾 Caçador de Arquivos Grandes
- Identifica arquivos acima de 50MB (configurável)
- Ordena por tamanho (maiores primeiro)
- Mostra data de modificação

---

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8 ou superior
- Bibliotecas padrão (não requer instalações extras)

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/organizador-pc-caotico.git

# Entre no diretório
cd organizador-pc-caotico

# Execute o programa
python organizador_pc.py
