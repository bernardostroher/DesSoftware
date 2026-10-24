import re
from modelos import EstadoVoz, Partitura, Nota, Evento, Voz

class Tradutor:

    TEMPO_PADRAO_PAUSA = 3

    def __init__(self):
        self._oitavas_padrao = [6, 5, 4, 3]
        self._volumes_padrao = [100, 80, 60, 40]
        self._instrumentos_padrao = [6, 20, 0, 70] #Cravo, Órgão, Piano, Fagote
        self._bpm_inicial = 120


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

        prefixo_atraso = re.match(r'^([<>,]*)\[(\d+)\]\s*', linha)

        if prefixo_atraso:
            comandos_iniciais = prefixo_atraso.group(1)
            atraso = int(prefixo_atraso.group(2))
            linha_limpa = linha[prefixo_atraso.end():]

        else:
            comandos_iniciais = ''
            atraso = 0
            linha_limpa = linha

        estado_atual = EstadoVoz(self._oitavas_padrao[id_voz], self._volumes_padrao[id_voz], self._instrumentos_padrao[id_voz])

        elementos_musicais = []
        elementos_musicais.append(Evento('troca_instrumento', estado_atual.instrumento))
        
        if id_voz == 0:
            elementos_musicais.append(Evento('definir_bpm', self._bpm_inicial))

        for comando in comandos_iniciais:
            if comando == '<':
                elementos_musicais.append(Evento('alterar_bpm', -10))
            elif comando == '>':
                elementos_musicais.append(Evento('alterar_bpm', 10))

        if atraso > 0:
            elementos_musicais.append(Evento('atraso', atraso))

        i = 0
        while i < len(linha_limpa):
            char_atual = linha_limpa[i]

            consumidos = self._analisa_caractere(char_atual, elementos_musicais, estado_atual, i, linha_limpa, id_voz)

            i += consumidos

        return Voz(elementos_musicais)


    def _trocar_instrumento(self, valor, estado_atual, lista_elementos):
        novo_instrumento = valor

        estado_atual.instrumento = valor

        comando = Evento('troca_instrumento', valor)
        lista_elementos.append(comando)


    def _analisa_caractere(self, char_atual, elementos_musicais, estado_atual, i, linha_limpa, id_voz):

        index = i
        i = 1

        match char_atual:
        
            case 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B':
                match_nota = re.match(r'[A-G]([#b]?):(\d+)', linha_limpa[index:])
        
                if match_nota:
                    acidente = match_nota.group(1)
                    duracao = int(match_nota.group(2))

                    nova_nota = Nota(char_atual, estado_atual.oitava, estado_atual.volume, duracao, acidente)
                    elementos_musicais.append(nova_nota)

                    estado_atual.ultima_nota = nova_nota
                    i = match_nota.end()
    
        
            case 'c' | 'd' | 'e' | 'f' | 'g' | 'a' | 'b':
                match_pausa = re.match(r'[c-g]:(\d+)', linha_limpa[index:])

                if match_pausa:
                    duracao = int(match_pausa.group(1))
                    comando = Evento('pausa', duracao)
                    elementos_musicais.append(comando)
                    i = match_pausa.end()
                    
                else:
                    comando = Evento('pausa', self.TEMPO_PADRAO_PAUSA)
                    elementos_musicais.append(comando)


            case 'i':
                match_inst = re.match(r'i:(\d+)', linha_limpa[index:])

                if match_inst:
                    novo_instrumento = int(match_inst.group(1))
                    self._trocar_instrumento(novo_instrumento, estado_atual, elementos_musicais)
                    i = match_inst.end()
                    

            case ' ':
                estado_atual.dobrar_volume()


            case '!':
                self._trocar_instrumento(24, estado_atual, elementos_musicais)

                
            case c if c.isdigit() and int(c) % 2 == 0:
                self._trocar_instrumento(estado_atual.instrumento + int(c), estado_atual, elementos_musicais)


            case '?' | '.':
                nova_oitava = estado_atual.oitava + 1

                if nova_oitava > 9:
                    estado_atual.oitava = self._oitavas_padrao[id_voz]

                else:
                    estado_atual.oitava = nova_oitava

            case 'V':
                nova_oitava = estado_atual.oitava - 1

                if nova_oitava < 0:
                    estado_atual.oitava = self._oitavas_padrao[id_voz]

                else:
                    estado_atual.oitava = nova_oitava


            case c if (c.isdigit() and int(c) % 2 != 0) or c == ';':
                self._trocar_instrumento(15, estado_atual, elementos_musicais)


            case ',':
                self._trocar_instrumento(114, estado_atual, elementos_musicais)
            

            case '>':
                comando = Evento('alterar_bpm', 10)
                elementos_musicais.append(comando)


            case '<':
                comando = Evento('alterar_bpm', -10)
                elementos_musicais.append(comando)


            case _:
                if estado_atual.ultima_nota is not None:
                    nota_repetida = Nota(estado_atual.ultima_nota.nome, estado_atual.ultima_nota.oitava, estado_atual.ultima_nota.volume, estado_atual.ultima_nota.duracao, estado_atual.ultima_nota.acidente)
                    elementos_musicais.append(nota_repetida)
                    
                else:
                    comando = Evento('pausa', self.TEMPO_PADRAO_PAUSA)
                    elementos_musicais.append(comando)

        return i
