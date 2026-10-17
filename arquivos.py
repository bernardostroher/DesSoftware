import tkinter as tk
from tkinter import filedialog

class GerenciadorArquivos:     #Classse para exibir opções ao usuário, ler o conteúdo de um arquivo txt, sobrescrever o conteúdo do arq txt se o usuário editar o texto, receber caminho e nome para salvar o midi.

    def ler_arquivo_txt(self):
        # Cria a janela raiz do Tkinter e a oculta imediatamente
        root = tk.Tk()
        root.withdraw()

        # Abre a janela do explorador de arquivos
        caminho_arquivo = filedialog.askopenfilename(title = "Selecione o arquivo de texto a ser interpretado", filetypes = [("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])

        # Verifica se o usuário selecionou um arquivo ou clicou em cancelar
        if not caminho_arquivo:
            return None

        # Abre o arquivo
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            conteudo = arquivo.read()

        return conteudo
