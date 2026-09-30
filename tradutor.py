import re
from modelos import EstadoVoz, Partitura

class Tradutor:
    def __init__(self):
        self._oitavas_padrao = [6, 5, 4, 3]
        self._volumes_padrao = [100, 80, 60, 40]
        self._instrumentos_padrao = [6, 20, 0, 70] #Cravo, Órgão, Piano, Fagote


    def analisar(self, texto):
        linhas = texto.strip().splitlines()

        vozes_processadas = []

        for i, linha in enumerate(linhas):
            id_voz = i % 4 # Alterna entre as quatro vozes (0, 1, 2, 3)
            voz = self._processar_linha(linha, id_voz)
            vozes_processadas.append(voz)

        return Partitura(vozes_processadas)


    def _processar_linha(self, linha, voz):
        if not linha.strip():
            return None # Ignorar linhas em branco

        atraso = self._extrair_atraso(linha)
        linha_limpa = re.sub(r'^\[\d+\]\s*', '', linha) # Remove a expressão de atraso ([n]) da linha

        estado_voz = EstadoVoz(volume_atual=self._volumes_padrao[voz], oitava_base=self._oitavas_padrao[voz], instrumento_atual=self._instrumentos_padrao[voz])

        indice = 0
        while indice < len(linha_limpa):
            char_atual = linha_limpa[indice]
                #Lógica de decisão:
                #   Se char_atual for A-G...
                #   Se char_atual for '>' ou '<'...
            
            indice += 1

        #return objeto Voz com as notas e eventos processados para esta linha


    def _extrair_atraso(self, linha):
        match = re.match(r'^\[(\d+)\]', linha)
        if match:
            return int(match.group(1))
        return 0
