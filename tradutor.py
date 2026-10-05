import re
from modelos import EstadoVoz, Partitura, Nota, Evento

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


    def _processar_linha(self, linha, id_voz):
        if not linha.strip():
            return None # Ignorar linhas em branco

        atraso = self._extrair_atraso(linha)
        linha_limpa = re.sub(r'^\[\d+\]\s*', '', linha) # Remove a expressão de atraso ([n]) da linha

        estado_atual = EstadoVoz(self._oitavas_padrao[id_voz], self._volumes_padrao[id_voz], self._instrumentos_padrao[id_voz])

        elementos_musicais = []

        for i in range(len(linha_limpa)):
            char_atual = linha_limpa[i]

            #Lógica de decisão:
            match char_atual:

                case 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B':
                    match_nota = re.match(r'[A-G]([#b]?):(\d+)', linha_limpa[i:])

                    if match_nota:
                        acidente = match_nota.group(1)
                        duracao = int(match_nota.group(2))

                        nova_nota = Nota(char_atual, estado_atual.oitava, estado_atual.volume, duracao, acidente)
                        elementos_musicais.append(nova_nota)

                        i += match_nota.end() - 1

                #   Se char_atual for '>' ou '<'...
                case '>', '<':
                    pass   

        #return objeto Voz com as notas e eventos processados para esta linha


    def _extrair_atraso(self, linha):
        match = re.match(r'^\[(\d+)\]', linha)
        if match:
            return int(match.group(1))
        return 0
    