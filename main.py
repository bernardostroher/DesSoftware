from mido import MidiFile, MidiTrack
from musica import Musica
         
if __name__ == '__main__':

    midi = MidiFile()
    track = MidiTrack() 
    midi.tracks.append(track)  

    texto = input('Insira o texto para a música:\n')
    musica = Musica.a_partir_de_texto(texto)

    musica.montar_trilha(track)
    musica.tocar_musica(midi)
    musica.salvar_midi(midi)
