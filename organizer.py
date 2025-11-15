import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class OrganizadorPC:
    def __init__(self):
        self.arquivos_duplicados = []
        self.extensoes_pastas = {
            'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Vídeos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'],
            'Músicas': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'Compactados': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Programas': ['.exe', '.msi', '.deb', '.rpm', '.dmg'],
            'Códigos': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
            'Planilhas': ['.csv', '.xls', '.xlsx', '.ods'],
            'Apresentações': ['.ppt', '.pptx', '.odp'],
            'Outros': []
        }
    
    def calcular_hash_arquivo(self, caminho_arquivo):
        """Calcula o hash MD5 de um arquivo para verificar duplicatas"""
        hash_md5 = hashlib.md5()
        try:
            with open(caminho_arquivo, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Erro ao calcular hash: {e}")
            return None
    
    def encontrar_duplicados(self, pasta):
        """Encontra arquivos duplicados baseado no hash MD5"""
        print("🔍 Procurando arquivos duplicados...")
        hashes_vistos = {}
        duplicados = []
        
        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                
                # Pula arquivos muito pequenos
                if os.path.getsize(caminho_completo) < 1024:  # Menos de 1KB
                    continue
                
                file_hash = self.calcular_hash_arquivo(caminho_completo)
                if file_hash:
                    if file_hash in hashes_vistos:
                        duplicados.append({
                            'original': hashes_vistos[file_hash],
                            'duplicado': caminho_completo,
                            'tamanho': os.path.getsize(caminho_completo)
                        })
                    else:
                        hashes_vistos[file_hash] = caminho_completo
        
        self.arquivos_duplicados = duplicados
        return duplicados
    
    def organizar_por_tipo(self, pasta_destino):
        """Organiza arquivos por tipo em pastas específicas"""
        print("📂 Organizando arquivos por tipo...")
        
        # Cria as pastas de categorias
        for categoria in self.extensoes_pastas.keys():
            pasta_categoria = os.path.join(pasta_destino, categoria)
            os.makedirs(pasta_categoria, exist_ok=True)
        
        arquivos_movidos = 0
        
        for raiz, _, arquivos in os.walk(pasta_destino):
            for arquivo in arquivos:
                if raiz == pasta_destino:  # Só arquivos na raiz
                    continue
                    
                caminho_antigo = os.path.join(raiz, arquivo)
                extensao = Path(arquivo).suffix.lower()
                
                # Encontra a categoria apropriada
                categoria_destino = 'Outros'
                for categoria, extensoes in self.extensoes_pastas.items():
                    if extensao in extensoes:
                        categoria_destino = categoria
                        break
                
                # Move o arquivo
                pasta_destino_categoria = os.path.join(pasta_destino, categoria_destino)
                caminho_novo = os.path.join(pasta_destino_categoria, arquivo)
                
                # Evita sobrescrever arquivos
                contador = 1
                while os.path.exists(caminho_novo):
                    nome_base = Path(arquivo).stem
                    extensao = Path(arquivo).suffix
                    caminho_novo = os.path.join(pasta_destino_categoria, 
                                              f"{nome_base}_{contador}{extensao}")
                    contador += 1
                
                try:
                    shutil.move(caminho_antigo, caminho_novo)
                    arquivos_movidos += 1
                    print(f"📦 Movido: {arquivo} → {categoria_destino}")
                except Exception as e:
                    print(f"❌ Erro ao mover {arquivo}: {e}")
        
        return arquivos_movidos
    
    def limpar_pasta_downloads(self, pasta_downloads):
        """Limpa e organiza a pasta de downloads"""
        print("🧹 Limpando pasta de downloads...")
        
        if not os.path.exists(pasta_downloads):
            return 0
        
        return self.organizar_por_tipo(pasta_downloads)
    
    def encontrar_arquivos_grandes(self, pasta, limite_mb=100):
        """Encontra arquivos maiores que o limite especificado"""
        print(f"🔎 Procurando arquivos maiores que {limite_mb}MB...")
        arquivos_grandes = []
        limite_bytes = limite_mb * 1024 * 1024
        
        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    tamanho = os.path.getsize(caminho_completo)
                    if tamanho > limite_bytes:
                        arquivos_grandes.append({
                            'caminho': caminho_completo,
                            'tamanho_mb': tamanho / (1024 * 1024),
                            'data_modificacao': datetime.fromtimestamp(
                                os.path.getmtime(caminho_completo)
                            )
                        })
                except Exception as e:
                    print(f"Erro ao verificar {caminho_completo}: {e}")
        
        # Ordena por tamanho (maiores primeiro)
        arquivos_grandes.sort(key=lambda x: x['tamanho_mb'], reverse=True)
        return arquivos_grandes
    
    def gerar_relatorio(self, pasta):
        """Gera um relatório completo da organização"""
        print("📊 Gerando relatório...")
        
        total_arquivos = 0
        total_tamanho = 0
        por_extensao = {}
        
        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                total_arquivos += 1
                
                try:
                    tamanho = os.path.getsize(caminho_completo)
                    total_tamanho += tamanho
                    
                    extensao = Path(arquivo).suffix.lower()
                    por_extensao[extensao] = por_extensao.get(extensao, 0) + 1
                except:
                    pass
        
        relatorio = {
            'total_arquivos': total_arquivos,
            'tamanho_total_mb': total_tamanho / (1024 * 1024),
            'extensoes': dict(sorted(por_extensao.items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
            'duplicados': len(self.arquivos_duplicados),
            'data_geracao': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        return relatorio

class InterfaceOrganizador:
    def __init__(self):
        self.organizador = OrganizadorPC()
        self.janela = tk.Tk()
        self.janela.title("🗂️ Organizador de PC Caótico")
        self.janela.geometry("600x700")
        self.janela.configure(bg='#2b2b2b')
        
        self.criar_interface()
    
    def criar_interface(self):
        # Título
        titulo = tk.Label(
            self.janela, 
            text="🗂️ ORGANIZADOR DE PC CAÓTICO", 
            font=('Arial', 16, 'bold'),
            fg='#00ff88',
            bg='#2b2b2b'
        )
        titulo.pack(pady=20)
        
        # Frame de seleção de pasta
        frame_pasta = tk.Frame(self.janela, bg='#2b2b2b')
        frame_pasta.pack(pady=10, fill='x', padx=20)
        
        tk.Label(
            frame_pasta, 
            text="Pasta para organizar:", 
            font=('Arial', 10),
            fg='white',
            bg='#2b2b2b'
        ).pack(anchor='w')
        
        self.entry_pasta = tk.Entry(frame_pasta, width=50, font=('Arial', 10))
        self.entry_pasta.pack(side='left', fill='x', expand=True, pady=5)
        
        btn_procurar = tk.Button(
            frame_pasta,
            text="📁 Procurar",
            command=self.selecionar_pasta,
            bg='#444444',
            fg='white',
            font=('Arial', 9)
        )
        btn_procurar.pack(side='right', padx=(5,0))
        
        # Frame de opções
        frame_opcoes = tk.Frame(self.janela, bg='#2b2b2b')
        frame_opcoes.pack(pady=20, fill='x', padx=20)
        
        # Botões de ação
        btn_duplicados = tk.Button(
            frame_opcoes,
            text="🔍 Encontrar Duplicados",
            command=self.encontrar_duplicados,
            bg='#ff6b6b',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        )
        btn_duplicados.pack(pady=5)
        
        btn_organizar = tk.Button(
            frame_opcoes,
            text="📂 Organizar Arquivos",
            command=self.organizar_arquivos,
            bg='#4ecdc4',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        )
        btn_organizar.pack(pady=5)
        
        btn_limpar_downloads = tk.Button(
            frame_opcoes,
            text="🧹 Limpar Downloads",
            command=self.limpar_downloads,
            bg='#45b7d1',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        )
        btn_limpar_downloads.pack(pady=5)
        
        btn_arquivos_grandes = tk.Button(
            frame_opcoes,
            text="💾 Arquivos Grandes",
            command=self.encontrar_arquivos_grandes,
            bg='#96ceb4',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20,
            height=2
        )
        btn_arquivos_grandes.pack(pady=5)
        
        # Área de resultados
        frame_resultados = tk.Frame(self.janela, bg='#2b2b2b')
        frame_resultados.pack(pady=20, fill='both', expand=True, padx=20)
        
        tk.Label(
            frame_resultados, 
            text="Resultados:", 
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#2b2b2b'
        ).pack(anchor='w')
        
        self.texto_resultados = tk.Text(
            frame_resultados,
            height=15,
            width=70,
            bg='#1a1a1a',
            fg='#00ff88',
            font=('Consolas', 9)
        )
        self.texto_resultados.pack(fill='both', expand=True, pady=5)
        
        # Barra de progresso
        self.barra_progresso = ttk.Progressbar(
            self.janela,
            orient='horizontal',
            mode='indeterminate'
        )
        self.barra_progresso.pack(fill='x', padx=20, pady=10)
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.entry_pasta.delete(0, tk.END)
            self.entry_pasta.insert(0, pasta)
    
    def log(self, mensagem):
        self.texto_resultados.insert(tk.END, f"{mensagem}\n")
        self.texto_resultados.see(tk.END)
        self.janela.update()
    
    def encontrar_duplicados(self):
        pasta = self.entry_pasta.get()
        if not pasta:
            messagebox.showerror("Erro", "Selecione uma pasta primeiro!")
            return
        
        def tarefa():
            self.barra_progresso.start()
            self.texto_resultados.delete(1.0, tk.END)
            self.log("🔍 Procurando arquivos duplicados...")
            
            duplicados = self.organizador.encontrar_duplicados(pasta)
            
            self.barra_progresso.stop()
            self.texto_resultados.delete(1.0, tk.END)
            
            if duplicados:
                self.log(f"🎯 Encontrados {len(duplicados)} arquivos duplicados:\n")
                for dup in duplicados[:10]:  # Mostra apenas os 10 primeiros
                    self.log(f"📄 ORIGINAL: {dup['original']}")
                    self.log(f"📄 DUPLICADO: {dup['duplicado']}")
                    self.log(f"📏 TAMANHO: {dup['tamanho'] / 1024 / 1024:.2f} MB")
                    self.log("-" * 50)
                
                if len(duplicados) > 10:
                    self.log(f"\n... e mais {len(duplicados) - 10} arquivos duplicados")
            else:
                self.log("✅ Nenhum arquivo duplicado encontrado!")
        
        threading.Thread(target=tarefa).start()
    
    def organizar_arquivos(self):
        pasta = self.entry_pasta.get()
        if not pasta:
            messagebox.showerror("Erro", "Selecione uma pasta primeiro!")
            return
        
        def tarefa():
            self.barra_progresso.start()
            self.texto_resultados.delete(1.0, tk.END)
            self.log("📂 Organizando arquivos...")
            
            movidos = self.organizador.organizar_por_tipo(pasta)
            
            self.barra_progresso.stop()
            self.texto_resultados.delete(1.0, tk.END)
            self.log(f"✅ Organização concluída!")
            self.log(f"📦 {movidos} arquivos organizados em categorias")
            
            # Gera relatório
            relatorio = self.organizador.gerar_relatorio(pasta)
            self.log(f"\n📊 RELATÓRIO:")
            self.log(f"📁 Total de arquivos: {relatorio['total_arquivos']}")
            self.log(f"💾 Tamanho total: {relatorio['tamanho_total_mb']:.2f} MB")
            self.log(f"🔁 Arquivos duplicados: {relatorio['duplicados']}")
            self.log(f"📅 Data: {relatorio['data_geracao']}")
        
        threading.Thread(target=tarefa).start()
    
    def limpar_downloads(self):
        pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        self.entry_pasta.delete(0, tk.END)
        self.entry_pasta.insert(0, pasta_downloads)
        
        def tarefa():
            self.barra_progresso.start()
            self.texto_resultados.delete(1.0, tk.END)
            self.log("🧹 Limpando pasta de Downloads...")
            
            movidos = self.organizador.limpar_pasta_downloads(pasta_downloads)
            
            self.barra_progresso.stop()
            self.texto_resultados.delete(1.0, tk.END)
            self.log(f"✅ Downloads organizados!")
            self.log(f"📦 {movidos} arquivos movidos para categorias")
        
        threading.Thread(target=tarefa).start()
    
    def encontrar_arquivos_grandes(self):
        pasta = self.entry_pasta.get()
        if not pasta:
            messagebox.showerror("Erro", "Selecione uma pasta primeiro!")
            return
        
        def tarefa():
            self.barra_progresso.start()
            self.texto_resultados.delete(1.0, tk.END)
            self.log("💾 Procurando arquivos grandes...")
            
            arquivos_grandes = self.organizador.encontrar_arquivos_grandes(pasta, 50)
            
            self.barra_progresso.stop()
            self.texto_resultados.delete(1.0, tk.END)
            
            if arquivos_grandes:
                self.log(f"📏 Encontrados {len(arquivos_grandes)} arquivos maiores que 50MB:\n")
                for arquivo in arquivos_grandes[:15]:
                    self.log(f"📄 {os.path.basename(arquivo['caminho'])}")
                    self.log(f"   📁 {arquivo['caminho']}")
                    self.log(f"   💾 Tamanho: {arquivo['tamanho_mb']:.2f} MB")
                    self.log(f"   📅 Modificado: {arquivo['data_modificacao'].strftime('%d/%m/%Y')}")
                    self.log("-" * 40)
            else:
                self.log("✅ Nenhum arquivo grande encontrado!")
        
        threading.Thread(target=tarefa).start()
    
    def executar(self):
        self.janela.mainloop()

# 🚀 EXECUTAR O PROGRAMA
if __name__ == "__main__":
    print("🚀 Iniciando Organizador de PC Caótico...")
    app = InterfaceOrganizador()
    app.executar()