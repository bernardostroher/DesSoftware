import pygame
import tradutor 
import audio 
import modelos
import arquivos
import pygame_gui

gerenciador = arquivos.GerenciadorArquivos()
traduzido = tradutor.Tradutor()
gerador = audio.GeradorMidi()
toca = audio.ReprodutorAudio()

class Tela:

    def __init__(self):
        self.clicado = False #para botoes
        self.pausado = False #para selecionar arquivo
        self.carregado = False

    def abrir_tela(self):
        pygame.init()
        tamanho_monitor = pygame.display.get_desktop_sizes()[0]
        screen = pygame.display.set_mode(tamanho_monitor, pygame.FULLSCREEN)
        font = pygame.font.Font(None, size = 30)

        clock = pygame.time.Clock()
        gerenciador_gui = pygame_gui.UIManager(tamanho_monitor)

        largura = tamanho_monitor[0]
        altura = tamanho_monitor[1]

        rect_caixa = pygame.Rect(largura * 0.15, altura * 0.1, largura * 0.7, altura * 0.6)
        caixa_texto = pygame_gui.elements.UITextEntryBox(
            relative_rect = rect_caixa,
            initial_text = "Carregue um arquivo ou digite aqui...",
            manager = gerenciador_gui
        )

        self._carregar_texturas()

        pygame.mixer.init()

        running = True
        while running:

            time_delta = clock.tick(60) / 1000.0

          #  if not self.pausado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                gerenciador_gui.process_events(event)

            screen.fill((255, 255, 255)) #alterar usando image load... para uma imagem
            botoes = self._cria_botoes(screen, tamanho_monitor)
            acao = conferirir_mouse = self._mouse( screen, botoes, font)

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_ESCAPE]:
                running = False
            
            if acao == "Carregar":
                documento = gerenciador.ler_arquivo_txt()
                
                if documento:
                    caixa_texto.set_text(documento)
                    self.carregado = True

                    partitura = traduzido.analisar(documento)
                    gerador.cria_midi(partitura, ".temp_audio.mid")
                    pygame.mixer.music.load(".temp_audio.mid")

            if acao == "Play" and self.carregado == True and self.pausado == False: #configurar para so apos anterior estar feito
                toca.tocar(".temp_audio.mid")
                
            if acao == "Pause" and self.pausado == False and pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                toca.pausar()
                self.pausado = True

            if acao == "Play" and self.pausado == True:
                toca.despausar()
                self.pausado = False
            #pausar continuar e parar  

            if acao == "Salvar":
                caminho_final = gerenciador.escolher_caminho_salvar()

                if caminho_final:
                    texto_atualizado = caixa_texto.get_text()
                    partitura = traduzido.analisar(texto_atualizado)
                    gerador.cria_midi(partitura, caminho_final)

            if acao == "SalvarTXT":
                texto_atualizado = caixa_texto.get_text()
                gerenciador.salvar_arquivo_txt(texto_atualizado)

             
            gerenciador_gui.update(time_delta)
            gerenciador_gui.draw_ui(screen)
            pygame.display.update()   
        
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

        botao_play = pygame.Rect(largura * 0.15, altura * 0.7, 40, 40)
        botao_pause = pygame.Rect(largura * 0.175, altura * 0.7, 40, 40)
        botao_load = pygame.Rect(largura * 0.12, altura * 0.11, 40, 40)
        botao_savemidi = pygame.Rect(largura * 0.825, altura * 0.7, 40, 40)
        botao_savetxt = pygame.Rect(largura * 0.85, altura * 0.7, 40, 40)

        botoes = [(botao_play, "Play", self.img_play), (botao_pause, "Pause", self.img_pause), (botao_load, "Carregar", self.img_loadfile), (botao_savemidi, "Salvar", self.img_savemidi), (botao_savetxt, "SalvarTXT", self.img_savetxt)]

        for botao, _, imagem in botoes:

            screen.blit(imagem, botao)

        return [(botao, texto) for botao, texto, _ in botoes] #Retorna apenas botoes e textos, sem imagem, para função do mouse


    def _carregar_texturas(self):
        img_play = pygame.image.load('assets/play.png').convert_alpha()
        img_pause = pygame.image.load('assets/pause.png').convert_alpha()
        img_loadfile = pygame.image.load('assets/file-import.png').convert_alpha()
        img_savemidi = pygame.image.load('assets/save_midi.png').convert_alpha()
        img_savetxt = pygame.image.load('assets/save_txt.png').convert_alpha()
        
        self.img_play = pygame.transform.scale(img_play, (40, 40))
        self.img_pause = pygame.transform.scale(img_pause, (40, 40))
        self.img_loadfile = pygame.transform.scale(img_loadfile, (40, 40))
        self.img_savemidi = pygame.transform.scale(img_savemidi, (40, 40))
        self.img_savetxt = pygame.transform.scale(img_savetxt, (40, 40))

if __name__ == "__main__":
    tela = Tela()
    tela.abrir_tela()