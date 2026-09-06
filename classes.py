#OBS: Não implementei ainda nenhuma forma de alterar oitava e instrumento, os métodos existem mas não são chamados ainda. A música tá sendo executada com um som de piano como instrumento padrão da biblioteca e a oitava tá definida no mapeamento (tá tudo na quarta oitava). Também ainda não adicionei nada relacionado à definição do andamento (bpm).

from mido import Message, MidiFile, MidiTrack  #Importação de funções da biblioteca mido, utilizada para formar o arquivo MIDI da música.
import mido

class Nota:

    DURACAO = 480  #Duração padrão de cada nota
    OITAVA_PADRAO = 1
    mapeamento = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71, 'H': 72}   #Mapeamento das notas. Na biblioteca mido, cada nota é representada por um número de 0 a 127. O dó na quarta oitava (C4) é representado pelo número 60.

    # Método construtor (com os atributos da classe):
    def __init__(self, nome, oitava):
        self.nome = nome
        self.oitava = oitava

    # Segundo método construtor que cria uma nota somente a partir do nome com valor padrao de oitava
    def __init__(self, nome_nota):
            self.nome = nome_nota
            self.oitava = self.OITAVA_PADRAO

    # Getters e setters padrão para os atributos da classe Nota:
    def get_nome(self):
        return self.nome

    def set_nome(self, novo_nome):
        self.nome = novo_nome

    def get_oitava(self):
            return self.oitava
    
    def set_oitava(self, nova_oitava):
        self.oitava = nova_oitava

    # Outros métodos:

    def para_midi(self):   #Método que converte as notas e coloca em um arquivo MIDI
        if self.nome in self.mapeamento:
            # note_on = começar o som da nota. note_off = parar o som da tecla. time: número de ticks (tempo que demora) até ser executada a ação. Velocity é a força/volume com que a tecla é apertada, de 0 a 127.
            track.append(Message('note_on', note=self.mapeamento[self.nome], velocity=64, time=0))  #Executa a nota imediatamente (time = 0)
            track.append(Message('note_off', note=self.mapeamento[self.nome], velocity=64, time=self.DURACAO)) #Para a execução da nota depois de 480 ticks (time = 480)
        elif self.nome == ' ':  #Para espaços vazios, cria um silêncio. É um tempo de espera onde não há nenhuma nota sendo tocada.
            track.append(Message('note_off', note=0, velocity=0, time=self.DURACAO))

    def salvar_midi(self):  #Método para salvar o arquivo MIDI.
        mid.save('musica_gerada.mid')   #Salva o arquivo midi (na pasta onde está o arquivo do código no momento)

class Musica:

    INSTRUMENTO_PADRAO = 'piano'

    def __init__(self, notas, instrumento):
        self.notas = notas
        self.instrumento = instrumento

    def __init__(self, notas):
        self.notas = notas
        self.instrumento = self.INSTRUMENTO_PADRAO

    # Getters e setters padrão:
    def get_notas(self):
        return self.notas

    def set_notas(self, nova_lista_notas):
        self.notas = nova_lista_notas

    def get_instrumento(self):
        return self.instrumento
        
    def set_instrumento(self, novo_instrumento):
        self.instrumento = novo_instrumento

    # Getter que retorna o nome de todas as notas (não sei se vai ser necessário mas deixei por enquanto para usarmos para checar os textos durante o desenvolvimento):
    def get_nome_notas(self):
        lista_nomes_notas = []
        for nota in self.notas:
            lista_nomes_notas.append(nota.get_nome())
        return lista_nomes_notas

    def montar_midi(self):  #Método para converter para midi e salvar no arquivo midi todas as notas da música.
        for nota in self.notas:
            nota.para_midi()
            nota.salvar_midi()

    def tocar_musica(self): #Método que faz com que a música seja tocada quando o código é executado em python, sem precisar abrir outro arquivo.
        try:    #Abre a porta MIDI padrão do sistema operacional
            with mido.open_output() as port:    #Procura o sintetizador interno padrão do sistema operacional
                print('Reproduzindo a música...')
                for msg in mid.play():  #Lê a estrutura da música, e a função play converte os ticks em segundos, calculando a duração e o tempo de espera entre as notas.
                    port.send(msg)  #Entrega a instrução de áudio diretamente para a placa de som
        except OSError: #Caso ocorra algum erro com o sistema operacional.
            print('Erro: Nenhuma saída MIDI encontrada.')
                
    # Ponto de entrada/início da execução (main)
if __name__ == '__main__':

    mid = MidiFile()    #Inicializa o arquivo MIDI onde será salva a música.
    track = MidiTrack() #Inicializa a "trilha". A trilha é como uma "linha do tempo" ou lista onde serão colocadas as notas.
    mid.tracks.append(track)  #Adiciona a trilha à lista de tracks do arquivo midi.

    #Exemplo de música que é salva em um arquivo MIDI e tocada quando o código é executado:
    Musica1 = Musica([Nota('C'), Nota('D'), Nota('E'), Nota('F'), Nota('G'), Nota('A'), Nota('B'), Nota('A'), Nota('G'), Nota('F'), Nota('E'), Nota('D'), Nota('C')])

    Musica1.montar_midi()
    Musica1.tocar_musica()
