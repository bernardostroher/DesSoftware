"""Módulo responsável por gerenciar operações de arquivos, 
como abrir e salvar arquivos de texto e MIDI."""
import tkinter as tk
from tkinter import filedialog

class GerenciadorArquivos:
    """Classe responsável por gerenciar operações de arquivos."""

    def escolher_caminho_abrir(self):
        """Abre uma janela de diálogo para o usuário escolher um arquivo de texto para abrir."""
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
        """Lê o conteúdo de um arquivo de texto dado o caminho do arquivo."""
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            return arquivo.read()

    def ler_arquivo_txt(self):
        """Lê o conteúdo de um arquivo de texto escolhido pelo usuário."""
        caminho_arquivo = self.escolher_caminho_abrir()
        if not caminho_arquivo:
            return None
        return self.ler_conteudo_txt(caminho_arquivo)

    def salvar_arquivo_txt(self, conteudo):
        """Abre uma janela de diálogo para o usuário escolher onde salvar um arquivo de texto."""
        root = tk.Tk()
        root.withdraw()

        try:
            caminho = filedialog.asksaveasfilename(title = "Salvar Texto Como",
                defaultextension = ".txt",
                filetypes = [("Arquivo de Texto", "*.txt"),
                ("Todos os Arquivos", "*.*")])
            if caminho:
                with open(caminho, 'w', encoding = 'utf-8') as arquivo:
                    arquivo.write(conteudo)
        finally:
            root.destroy()

    def escolher_caminho_salvar(self):
        """Abre uma janela de diálogo para o usuário escolher onde salvar um arquivo MIDI."""
        root = tk.Tk()
        root.withdraw()

        try:
            return filedialog.asksaveasfilename(title = "Salvar Música Como",
                defaultextension = ".mid",
                filetypes = [("Arquivo MIDI", "*.mid")]
                ) or None
        finally:
            root.destroy()
