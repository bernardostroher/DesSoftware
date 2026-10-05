class Nota:
    def __init__(self, nome, oitava, volume, duracao, acidente):
        self.nome = nome
        self.oitava = oitava
        self.volume = volume
        self.duracao = duracao
        self.acidente = acidente

class Evento:
    def __init__(self, estado):
        self.estado = estado

class EstadoVoz:

    def __init__(self, oitava_atual, volume_atual, instrumento_atual):
        self.oitava = oitava_atual
        self.volume = volume_atual
        self.instrumento = instrumento_atual

class EstadoGlobal:  #Armazena dados globais da partitura
    def __init__(self, bpm):
        self.bpm = bpm

class Voz:  #Armazena a sequência de notas e eventos de uma voz
    def __init__(self):
        pass

class Partitura:
    def __init__(self, vozes):
        if len(vozes) > 4:
            raise ValueError("A partitura pode ter no máximo 4 vozes.")
        self.vozes = vozes
