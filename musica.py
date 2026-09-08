import mido
from nota import Nota

class Musica:

    INSTRUMENTO_PADRAO = 'piano'

    def __init__(self, notas, instrumento=INSTRUMENTO_PADRAO):
        self.notas = notas
        self.instrumento = instrumento

    @classmethod
    def a_partir_de_texto(cls, texto):
        lista_notas = []
        volume_atual = Nota.VOLUME_PADRAO

        for caractere in texto:
            if caractere == ' ':
                volume_atual = Musica._dobrar_volume(volume_atual)
            else:
                lista_notas.append(Nota(caractere, volume=volume_atual))

        return cls(lista_notas)

    def _dobrar_volume(volume):
        return min(volume * 2, 127) 

    def montar_trilha(self, track):
        for nota in self.notas:
            nota.adicionar_na_trilha(track)

    def tocar_musica(self, midi):
        try:
            with mido.open_output() as port:
                print('Reproduzindo a música...')
                for msg in midi.play():
                    port.send(msg)
        except OSError:
            print('Erro: Nenhuma saída MIDI encontrada.')

    def salvar_midi(self, midi):
        midi.save('musica_gerada.mid')
