import pygame
import time




class ReprodutorAudio:
    def __init__(self):
        pass

    def tocar(self, arquivo):
        pygame.mixer.init()
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
       
    def pausar(self):
        print("pausar")
        pygame.mixer.music.pause()

    def despausar(self):
        print("despausar")
        pygame.mixer.music.unpause()



class GeradorMidi:
    def __init__(self):
        pass

