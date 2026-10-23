import pygame
import time
import modelos
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

class ReprodutorAudio:
    def __init__(self):
        pass

    def tocar(self, arquivo):
        pygame.mixer.init()
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
 
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def pausar(self):
        
        pygame.mixer.music.pause()

    def despausar(self):
        
        pygame.mixer.music.unpause()


class GeradorMidi:

    DURACAO_EM_TICKS = {
        1: 1920,
        2: 960,
        3: 480,
        4: 240,
        5: 120,
        6: 60,
        7: 30,
    }

    def _duracao_em_ticks(self, codigo):
        try:
            return self.DURACAO_EM_TICKS[codigo]
        except KeyError:
            raise ValueError(f"Código de duração inválido: {codigo}") from None


    def _coletar_eventos_bpm(self, partitura):
        voz_controle = partitura.vozes[0]
        if voz_controle is None:
            raise ValueError("A primeira voz deve conter os eventos de controle, incluindo definição do BPM inicial.")

        eventos_bpm = []
        tick = 0
        bpm_atual = None

        for elemento in voz_controle.lista_elementos:
            if isinstance(elemento, modelos.Nota):
                tick += self._duracao_em_ticks(elemento.duracao)

            elif isinstance(elemento, modelos.Evento):
                if elemento.tipo == "definir_bpm":
                    if bpm_atual is None:
                        bpm_atual = elemento.valor
                        eventos_bpm.append((tick, bpm_atual))

                elif elemento.tipo == "alterar_bpm":
                    if bpm_atual is None:
                        raise ValueError("O BPM padrão deve ser definido antes de qualquer alteração.")

                    bpm_atual += elemento.valor
                    if bpm_atual <= 0:
                        raise ValueError("O BPM não pode ser menor ou igual a zero.")

                    eventos_bpm.append((tick, bpm_atual))

                elif elemento.tipo == "pausa":
                    tick += self._duracao_em_ticks(elemento.valor)

                elif elemento.tipo == "atraso":
                    tick += self._duracao_em_ticks(3) * elemento.valor

        if bpm_atual is None:
            raise ValueError("Nenhum BPM padrão definido na primeira voz.")

        return eventos_bpm


    def _cria_track_bpm(self, eventos_bpm):

        track = MidiTrack()
        self.mid.tracks.append(track)

        tick_anterior = 0
        for tick, bpm in eventos_bpm:
            delta_ticks = tick - tick_anterior
            track.append(MetaMessage('set_tempo', tempo = bpm2tempo(bpm), time = delta_ticks))
            tick_anterior = tick


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
                nota = nota + 1
    
            if acidente == 'b':
                nota = nota - 1
            
            nota = nota + 12 * oitava
    
            return nota     


    def cria_arquivo_midi(self):
        self.mid = MidiFile(type = 1)

        
    def cria_midi(self, texto_traduzido, nome):
        self.cria_arquivo_midi()

        eventos_bpm = self._coletar_eventos_bpm(texto_traduzido)
        self._cria_track_bpm(eventos_bpm)

        for canal, voz in enumerate(texto_traduzido.vozes):
            if voz is not None:
                self.cria_track(voz, canal)

        self.salva_midi(nome)


    def cria_track(self, voz, canal = 0):
        #mid = MidiFile('nome')
        track = MidiTrack()
        self.mid.tracks.append(track)


        for evento in voz.lista_elementos:

            if type(evento) == modelos.Nota:
                nota = self._cria_nota( evento)
                volume = evento.volume
                duracao = evento.duracao 
                track.append(Message('note_on', note = nota , velocity = volume , time = 0, channel = canal))
                track.append(Message('note_off', note = nota , velocity = volume , time = self._duracao_em_ticks(duracao), channel = canal))

            else:
                tipo = evento.tipo
                valor = evento.valor
                match tipo:

                    case "troca_instrumento":
                        track.append(Message('program_change', program = valor, time = 0, channel = canal))

                    case "pausa":
                        track.append(Message('note_off', note = 0, velocity = 0, time = self._duracao_em_ticks(valor), channel = canal))

                    case "atraso":
                        atraso_em_ticks = self._duracao_em_ticks(3) * valor
                        track.append(Message('note_off', note = 0, velocity = 0, time = atraso_em_ticks, channel = canal))
    

    def salva_midi(self, nome):
        self.mid.save(nome)