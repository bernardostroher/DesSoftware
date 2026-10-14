import pygame
import time
import mido
import modelos
from mido import MidiFile, MidiTrack, Message, bpm2tempo


class ReprodutorAudio:
    def __init__(self):
        pass

    def tocar(self, arquivo):
        pygame.mixer.init()
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
        time.sleep(10)
    def pausar(self):
        print("pausar")
        pygame.mixer.music.pause()

    def despausar(self):
        print("despausar")
        pygame.mixer.music.unpause()



class GeradorMidi:
    def __init__(self):
        self.mid = None

    def cria_arquivo_midi(self):
        self.mid = MidiFile(type=1)
        

    def cria_midi(self, texto_traduzido, nome):
        self.cria_arquivo_midi()
        for voz in texto_traduzido.vozes:
            self.cria_track(voz)

        self.salva_midi(nome)


    def cria_track(self, voz): 
        #mid = MidiFile('nome')
        track = MidiTrack()
        self.mid.tracks.append(track)
        tempo = 0
        for evento in voz.lista_elementos:
            if type(evento) == modelos.Nota:
                nota = self._cria_nota( evento)
                volume = evento.volume
                duracao = evento.duracao 
                track.append(Message('note_on', note = nota , velocity = volume , time = tempo))
                track.append(Message('note_off', note = nota , velocity = volume , time = tempo +duracao ))
                tempo = tempo + duracao
           """ else:
                tipo = evento.tipo
                valor = evento.valor
                match tipo:
                    case "troca_instrumento":
                        track.append(Message('program_change', program = valor, time = tempo))
                    case "alterar_bpm":
                        set_tempo = bpm2tempo(valor)

                    case "pausa":
                        pass
                """

    def _cria_nota(self, evento):
        tabela_notas = {
            "C": 0,
            "D": 2,
            "E": 4,
            "F": 5,
            "G": 7,
            "A": 9,
            "B": 11,
        }
        oitava = evento.oitava
        acidente = evento.acidente
        nome = evento.nome
        nota = tabela_notas[nome]
        if acidente == '#':
            nota = nota+1
        if acidente == 'b':
            nota = nota-1
        nota = nota + 12*oitava
        return nota 
        
            


    def salva_midi(self, nome):
         self.mid.save(nome)