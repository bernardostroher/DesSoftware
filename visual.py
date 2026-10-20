import pygame
import tradutor 
import audio 
import modelos
import arquivos

gerenciador = arquivos.GerenciadorArquivos()
traduzido = tradutor.Tradutor()
gerador = audio.GeradorMidi()
toca = audio.ReprodutorAudio()
#carregar imagem para botoes:
#img = pygame.image.load('algo.png').convert_alpha()
class Tela:
    def __init__(self):
        self.clicado = False# para botoes
        self.pausado = False#para selecionar arquivo
        self.carregado = False
    def abrir_tela(self):
        pygame.init()
        tamanho_monitor = pygame.display.get_desktop_sizes()[0]
        screen = pygame.display.set_mode((tamanho_monitor))
        font = pygame.font.Font(None, size = 30)
        running = True
        while running:
          #  if not self.pausado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((255, 255, 255))#alterar usando image load... para uma imagem
            botoes = self._cria_botoes(screen, tamanho_monitor)
            acao = conferirir_mouse = self._mouse( screen, botoes, font)
            pygame.display.update()
                
            if acao == "Carregar":
                documento = gerenciador.ler_arquivo_txt()
                partitura = traduzido.analisar(documento)
                gerador.cria_midi(partitura, "testemidi.mid")
                self.carregado = True
            if acao == "Play" and self.carregado == True and self.pausado == False:#configurar para so apos anterior estar feito
                toca.tocar("testemidi.mid")
            if acao == "Pause" and self.pausado == False:
                toca.pausar()
                self.pausado = True
            if acao == "Play" and self.pausado == True:
                toca.despausar()
                self.pausado = False
            #pausar continuar e parar     
               
        pygame.quit()

    def _mouse(self, screen, botoes, font):
        clicou = pygame.mouse.get_pressed()[0]
        mpos = pygame.mouse.get_pos()
        saida = "ignorar"
        for botao, texto in botoes:
            m_collision = botao.collidepoint(mpos)

            if m_collision and clicou and self.clicado == False:
                self.clicado = True
                saida = texto
               
            if  not clicou:
                self.clicado = False
        return saida
        


    def _cria_botoes(self, screen, tamanho_monitor):
        largura, altura = tamanho_monitor
        px, py, pl, pc = largura*0.4, altura*0.9, 40, 40
        pax, pay, pal, pac = largura*0.6,altura*0.9 , 40, 40
        plx, ply, pll, plc = largura*0.2,altura*0.3 , 40, 40
        botao_play = pygame.Rect(px, py, pl, pc)
        botao_pause = pygame.Rect(pax, pay, pal, pac)
        botao_load = pygame.Rect(plx, ply, pll, plc)
        botoes = [(botao_play, "Play"), (botao_pause, "Pause"), (botao_load, "Carregar")]
        for botao, texto in botoes:
            pygame.draw.rect(screen, (255, 255, 0), botao)
        return botoes



if __name__ == "__main__":
    tela = Tela()
    tela.abrir_tela()