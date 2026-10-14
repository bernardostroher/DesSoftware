import pygame

class Tela:
    def abrir_tela(self):
        pygame.init()
        tamanho_monitor = pygame.display.get_desktop_sizes()[0]
        screen = pygame.display.set_mode((tamanho_monitor))
        font = pygame.font.Font(None, size = 30)
        running = True
        while running:
            screen.fill((255, 255, 255))#alterar usando image load... para uma imagem //dessa forma tudo branco
            botoes = self._cria_botoes(screen, tamanho_monitor)
            conferirir_mouse = self._mouse( screen, botoes, font)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def _mouse(self, screen, botoes, font):
        clicou = pygame.mouse.get_pressed()[0]
        mpos = pygame.mouse.get_pos()
        for botao, texto in botoes:
            m_collision = botao.collidepoint(mpos)

            if m_collision and clicou:
                text = font.render(texto, True, (0,0,0))
                screen.blit(text, (300, 100))
                
                


    def _cria_botoes(self, screen, tamanho_monitor):
        largura, altura = tamanho_monitor
        px, py, pl, pc = largura*0.4, altura*0.9, 40, 40
        pax, pay, pal, pac = largura*0.6,altura*0.9 , 40, 40
        botao_play = pygame.Rect(px, py, pl, pc)
        botao_pause = pygame.Rect(pax, pay, pal, pac)
        botoes = [(botao_play, "Play"), (botao_pause, "Pause")]
        for botao, texto in botoes:
            pygame.draw.rect(screen, (255, 255, 0), botao)
        return botoes



if __name__ == "__main__":
    tela = Tela()
    tela.abrir_tela()