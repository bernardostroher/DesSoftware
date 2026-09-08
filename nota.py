from mido import Message

class Nota:

    VOLUME_PADRAO = 64
    OITAVA_PADRAO = 1
    DURACAO_NOTA = 480
    MAPEAMENTO_NOTAS = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71, 'H': 72}
    MAPEAMENTO_PAUSA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def __init__(self, nome, oitava=OITAVA_PADRAO, volume=VOLUME_PADRAO):
        self.nome = nome
        self.oitava = oitava
        self.volume = volume


    def _adicionar_nota(nota, track, volume, duracao):
        inicio_nota = Message('note_on', note=nota, velocity=volume, time=0)
        fim_nota = Message('note_off', note=nota, velocity=volume, time=duracao)
        track.append(inicio_nota)
        track.append(fim_nota) 

    def _adicionar_pausa(track, duracao):
        track.append(Message('note_off', note=0, velocity=0, time=duracao))


    def adicionar_na_trilha(self, track):
        
        if self.nome in self.MAPEAMENTO_NOTAS:
            nota = self.MAPEAMENTO_NOTAS[self.nome]
            Nota._adicionar_nota(nota, track, self.volume, self.DURACAO_NOTA)

        elif self.nome in self.MAPEAMENTO_PAUSA:
            Nota._adicionar_pausa(track, self.DURACAO_NOTA)
