import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
import pygame_gui
import pygame
import tradutor
import audio
import arquivos

gerenciador = arquivos.GerenciadorArquivos()
toca = audio.ReprodutorAudio()

def _cria_midi(texto, caminho):
    """Cria um arquivo MIDI a partir do texto e salva no caminho especificado."""
    partitura = tradutor.Tradutor().analisar(texto)
    audio.GeradorMidi().cria_midi(partitura, caminho)

def _cria_midi_temporario(texto, versao):
    """Cria um arquivo MIDI temporário a partir do texto e retorna o caminho do arquivo."""
    arquivo = tempfile.NamedTemporaryFile(
        prefix=f"dessoftware_{versao}_",
        suffix=".mid",
        delete=False
    )
    caminho = arquivo.name
    arquivo.close()

    try:
        _cria_midi(texto, caminho)
    except Exception:
        os.remove(caminho)
        raise

    return versao, caminho

class Tela:
    """Classe responsável pela interface gráfica da aplicação."""
    def __init__(self):
        self.clicado = False
        self.pausado = False
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._texto_atual = ""
        self._versao_texto = 0
        self._versao_preparada = -1
        self._prazo_preparacao = None
        self._preparacao_futura = None
        self._versao_em_preparacao = -1
        self._carregamento_futuro = None
        self._versao_carregamento = -1
        self._salvamentos_futuros = []
        self._tocar_ao_ficar_pronto = False
        self._caminho_midi_temporario = None
        self.status = ""

    def abrir_tela(self):
        """Abre a interface gráfica da aplicação e inicia o loop principal."""
        pygame.init()
        tamanho_monitor = pygame.display.get_desktop_sizes()[0]
        screen = pygame.display.set_mode(tamanho_monitor, pygame.FULLSCREEN)
        font = pygame.font.Font(None, size = 30)
        clock = pygame.time.Clock()
        gerenciador_gui = pygame_gui.UIManager(tamanho_monitor)

        largura, altura = tamanho_monitor

        self.margem_x = largura * 0.15
        self.margem_y = altura * 0.15
        self.largura_caixa = largura * 0.7
        self.altura_caixa = altura * 0.6

        rect_caixa = pygame.Rect(self.margem_x,
                                    self.margem_y,
                                    self.largura_caixa,
                                    self.altura_caixa)
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                gerenciador_gui.process_events(event)
                if (
                    event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
                    and event.ui_element == caixa_texto
                ):
                    self._texto_alterado(event.text)

            self._verificar_tarefas(caixa_texto)
            self._iniciar_preparacao_se_necessario()

            screen.fill((235, 238, 240))

            botoes = self._cria_botoes(screen)
            acao = self._mouse( botoes)
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                running = False

            self._tratar_acao_botao(acao, caixa_texto)
            gerenciador_gui.update(time_delta)
            gerenciador_gui.draw_ui(screen)
            if self.status:
                texto_status = font.render(self.status, True, (40, 40, 40))
                screen.blit(
                    texto_status,
                    (self.margem_x, self.margem_y + self.altura_caixa + 75)
                )
            pygame.display.update()
        self._executor.shutdown(wait=True)
        if self._preparacao_futura:
            try:
                _, caminho = self._preparacao_futura.result()
            except Exception as erro:
                print(f"Erro ao preparar áudio: {erro}")
            else:
                os.remove(caminho)
        self._limpar_midi_temporario()
        pygame.quit()

    def _texto_alterado(self, texto):
        """Atualiza o estado interno quando o texto de entrada é alterado."""
        self._texto_atual = texto
        self._versao_texto += 1
        self._versao_preparada = -1
        self._prazo_preparacao = pygame.time.get_ticks() + 700
        self._tocar_ao_ficar_pronto = False
        self.pausado = False
        pygame.mixer.music.stop()
        self.status = "Texto alterado; preparando áudio..."

    def _verificar_tarefas(self, caixa_texto):
        """Verifica o status de tarefas assíncronas, 
        como carregamento de arquivos e preparação de áudio."""
        self._confere_arquivo(caixa_texto)
        self._confere_audio()
        self._confere_salvamento()

    def _confere_arquivo(self, caixa_texto):
        """Verifica se o carregamento de arquivo foi concluído
        e atualiza o texto da caixa de entrada."""
        if self._carregamento_futuro and self._carregamento_futuro.done():
            futuro = self._carregamento_futuro
            self._carregamento_futuro = None
            try:
                documento = futuro.result()
            except (OSError, UnicodeError) as erro:
                if self._versao_carregamento == self._versao_texto:
                    self.status = f"Erro ao ler arquivo: {erro}"
            else:
                if self._versao_carregamento == self._versao_texto:
                    caixa_texto.set_text(documento)
                    self._texto_alterado(documento)


    def _confere_audio(self):
        """Verifica se a preparação do áudio foi concluída e atualiza o estado do reprodutor."""
        if self._preparacao_futura and self._preparacao_futura.done():
            futuro = self._preparacao_futura
            self._preparacao_futura = None
            try:
                versao, caminho = futuro.result()
            except Exception as erro:
                if self._versao_em_preparacao == self._versao_texto:
                    self._tocar_ao_ficar_pronto = False
                    self.status = f"Erro ao preparar áudio: {erro}"
                else:
                    self._prazo_preparacao = pygame.time.get_ticks()
            else:
                if versao != self._versao_texto:
                    os.remove(caminho)
                    self._prazo_preparacao = pygame.time.get_ticks()
                else:
                    try:
                        pygame.mixer.music.load(caminho)
                    except pygame.error as erro:
                        os.remove(caminho)
                        self._tocar_ao_ficar_pronto = False
                        self.status = f"Erro ao carregar áudio: {erro}"
                    else:
                        self._limpar_midi_temporario()
                        self._caminho_midi_temporario = caminho
                        self._versao_preparada = versao
                        self.status = "Áudio pronto."
                        if self._tocar_ao_ficar_pronto:
                            toca.tocar()
                            self._tocar_ao_ficar_pronto = False


    def _confere_salvamento(self):
        """Verifica se os salvamentos de arquivos MIDI foram concluídos e atualiza o status."""
        salvamentos_pendentes = []
        for futuro in self._salvamentos_futuros:
            if not futuro.done():
                salvamentos_pendentes.append(futuro)
                continue
            try:
                futuro.result()
            except Exception as erro:
                self.status = f"Erro ao salvar MIDI: {erro}"
            else:
                self.status = "Arquivo MIDI salvo."
        self._salvamentos_futuros = salvamentos_pendentes

    def _iniciar_preparacao_se_necessario(self):
        """Inicia a preparação do áudio se o prazo de preparação tiver sido atingido."""
        if (
            self._prazo_preparacao is None
            or self._preparacao_futura is not None
            or pygame.time.get_ticks() < self._prazo_preparacao
        ):
            return

        self._prazo_preparacao = None
        if not self._texto_atual.strip():
            self.status = "Digite um texto para preparar o áudio."
            self._tocar_ao_ficar_pronto = False
            return

        self._preparacao_futura = self._executor.submit(
            _cria_midi_temporario, self._texto_atual, self._versao_texto
        )
        self._versao_em_preparacao = self._versao_texto

    def _limpar_midi_temporario(self):
        """Remove o arquivo MIDI temporário, se existir."""
        if self._caminho_midi_temporario and os.path.exists(
            self._caminho_midi_temporario
        ):
            os.remove(self._caminho_midi_temporario)
        self._caminho_midi_temporario = None

    def _mouse(self, botoes):
        """Verifica a interação do mouse com os botões e retorna a ação correspondente."""
        clicou = pygame.mouse.get_pressed()[0]
        mpos = pygame.mouse.get_pos()
        saida = "ignorar"

        for botao, texto in botoes:
            m_collision = botao.collidepoint(mpos)

            if m_collision and clicou and not self.clicado:
                self.clicado = True
                saida = texto
            if  not clicou:
                self.clicado = False

        return saida

    def _cria_botoes(self, screen):
        """Cria os botões da interface gráfica e retorna uma 
        lista de botões com suas ações correspondentes."""
        tamanho_botao = 50
        espacamento = 15
        audio_tocando = (
            not self.pausado
            and pygame.mixer.get_init()
            and pygame.mixer.music.get_busy()
        )

        ancora_x_dir = self.margem_x + self.largura_caixa
        ancora_y_base = self.margem_y + self.altura_caixa

        botao_load = pygame.Rect(self.margem_x,
                                self.margem_y - tamanho_botao - espacamento,
                                tamanho_botao,
                                tamanho_botao)

        botao_play = pygame.Rect(self.margem_x,
                                ancora_y_base + espacamento,
                                tamanho_botao,
                                tamanho_botao)
        botao_pause = pygame.Rect(self.margem_x + tamanho_botao + espacamento,
                                ancora_y_base + espacamento,
                                tamanho_botao,
                                tamanho_botao)

        botao_savetxt = pygame.Rect(ancora_x_dir - tamanho_botao,
                                    ancora_y_base + espacamento,
                                    tamanho_botao,
                                    tamanho_botao)
        botao_savemidi = pygame.Rect(ancora_x_dir - (tamanho_botao * 2) - espacamento,
                                    ancora_y_base + espacamento,
                                    tamanho_botao,
                                    tamanho_botao)

        botoes = [(botao_play,
                    "Stop" if audio_tocando else "Play",
                    self.img_stop if audio_tocando else self.img_play),
                    (botao_pause, "Pause", self.img_pause),
                    (botao_load, "Carregar", self.img_loadfile),
                    (botao_savemidi, "Salvar", self.img_savemidi),
                    (botao_savetxt, "SalvarTXT", self.img_savetxt)]

        for botao, _, imagem in botoes:
            if imagem:
                screen.blit(imagem, botao)
            else:
                pygame.draw.rect(screen, (100, 100, 100), botao, border_radius = 8)

        return [(botao, texto) for botao, texto, _ in botoes]

    def _carregar_texturas(self):
        """Carrega as imagens dos botões da interface gráfica, 
        redimensionando-as para o tamanho adequado."""

        tamanho = (50, 50)

        def carregar_seguro(nome_arquivo):
            """Carrega uma imagem e a redimensiona; 
            retorna None se o arquivo não for encontrado."""
            try:
                img = pygame.image.load(nome_arquivo).convert_alpha()
                return pygame.transform.scale(img, tamanho)
            except FileNotFoundError:
                return None

        self.img_stop = carregar_seguro('assets/stop.png')
        self.img_play = carregar_seguro('assets/play.png')
        self.img_pause = carregar_seguro('assets/pause.png')
        self.img_loadfile = carregar_seguro('assets/file-import.png')
        self.img_savemidi = carregar_seguro('assets/save_midi.png')
        self.img_savetxt = carregar_seguro('assets/save_txt.png')



    def _tratar_acao_botao(self, acao, caixa_texto):
        """Trata a ação correspondente ao botão clicado, 
        executando a função apropriada."""
        if acao == "Carregar":
            self._acao_carregar()
        elif acao == "Play":
            self._acao_tocar()
        elif acao == "Salvar":
            self._acao_salvar_midi(caixa_texto.get_text())
        elif acao == "SalvarTXT":
            self._acao_salvar_txt(caixa_texto.get_text())
        elif acao == "Stop":
            self._acao_stop()
        elif (acao == "Pause"
                and not self.pausado
                and pygame.mixer.get_init()
                and pygame.mixer.music.get_busy()):
            toca.pausar()
            self.pausado = True

    def _acao_salvar_txt(self, caixa_texto):
        """Salva o conteúdo da caixa de texto 
        em um arquivo TXT escolhido pelo usuário."""
        texto_atualizado = caixa_texto
        gerenciador.salvar_arquivo_txt(texto_atualizado)

    def _acao_stop(self):
        """Para a reprodução do áudio e atualiza o estado interno."""
        toca.parar()
        self.pausado = False
        self._tocar_ao_ficar_pronto = False
        self.status = "Áudio interrompido."

    def _acao_carregar(self):
        """Abre um diálogo para o usuário escolher um arquivo TXT 
        e carrega seu conteúdo na caixa de texto."""
        caminho = gerenciador.escolher_caminho_abrir()
        if caminho:
            self._versao_texto += 1
            self._versao_preparada = -1
            self._prazo_preparacao = None
            self._texto_atual = ""
            self._versao_carregamento = self._versao_texto
            self._carregamento_futuro = self._executor.submit(
                gerenciador.ler_conteudo_txt, caminho
            )
            self._tocar_ao_ficar_pronto = False
            self.pausado = False
            pygame.mixer.music.stop()
            self.status = "Carregando arquivo..."

    def _acao_tocar(self):
        """Inicia ou retoma a reprodução do áudio, dependendo do estado atual."""
        if self.pausado and self._versao_preparada == self._versao_texto:
            toca.despausar()
            self.pausado = False
        elif self._versao_preparada == self._versao_texto:
            toca.tocar()
        elif self._texto_atual.strip():
            self._tocar_ao_ficar_pronto = True
            if self._prazo_preparacao is not None:
                self._prazo_preparacao = pygame.time.get_ticks()
            self.status = "Preparando áudio..."
        else:
            self.status = "Carregue um arquivo ou digite um texto."

    def _acao_salvar_midi(self, caixa_texto):
        """Abre um diálogo para o usuário escolher o 
        local e nome do arquivo MIDI a ser salvo."""
        caminho_final = gerenciador.escolher_caminho_salvar()

        if caminho_final:
            texto_atualizado = caixa_texto
            self._salvamentos_futuros.append(
            self._executor.submit(
                _cria_midi, texto_atualizado, caminho_final
            )
        )
            self.status = "Salvando arquivo MIDI..."

if __name__ == "__main__":
    tela = Tela()
    tela.abrir_tela()
