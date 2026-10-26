import tkinter as tk
from tkinter import filedialog

class GerenciadorArquivos:

    def escolher_caminho_abrir(self):
        root = tk.Tk()
        root.withdraw()

        try:
            return filedialog.askopenfilename(
                title="Selecione o arquivo de texto a ser interpretado",
                filetypes=[
                    ("Arquivos de Texto", "*.txt"),
                    ("Todos os Arquivos", "*.*")
                ]
            ) or None
        finally:
            root.destroy()

    def ler_conteudo_txt(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            return arquivo.read()

    def ler_arquivo_txt(self):
        caminho_arquivo = self.escolher_caminho_abrir()
        if not caminho_arquivo:
            return None
        return self.ler_conteudo_txt(caminho_arquivo)

    def salvar_arquivo_txt(self, conteudo):
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.asksaveasfilename(title = "Salvar Texto Como", defaultextension = ".txt", filetypes = [("Arquivo de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])

        if caminho:
            with open(caminho, 'w', encoding = 'utf-8') as arquivo:
                arquivo.write(conteudo)

    def escolher_caminho_salvar(self):
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.asksaveasfilename(title = "Salvar Música Como", defaultextension = ".mid", filetypes = [("Arquivo MIDI", "*.mid")])

        return caminho
