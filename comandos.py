"""Módulo responsável por definir os comandos musicais e sua execução."""
from dataclasses import dataclass
import re
from abc import ABC, abstractmethod
from modelos import EstadoVoz, Nota, Evento

@dataclass
class Contexto:
    """Contexto de execução para os comandos musicais."""
    texto: str
    posicao: int
    elementos: list
    estado: EstadoVoz
    oitava_padrao: int

    @property
    def restante(self):
        """Retorna o texto restante a ser processado."""
        return self.texto[self.posicao:]

class Comando(ABC):
    """Classe base para todos os comandos musicais."""
    @abstractmethod
    def executar(self, ctx: Contexto):
        """Executa o comando e retorna quantos caracteres consumiu."""

class ComandoNota(Comando):
    """Comando para notas musicais, no formato 'A:4', 'C#:2', etc."""
    _regex = re.compile(r'([A-G])([#b]?):(\d+)')

    def executar(self, ctx):
        m = self._regex.match(ctx.restante)
        if not m:
            return 1
        nome, acidente, duracao = m.group(1), m.group(2), int(m.group(3))
        nota = Nota(nome, ctx.estado.oitava, ctx.estado.volume, duracao, acidente)
        ctx.elementos.append(nota)
        ctx.estado.ultima_nota = nota
        return m.end()

class ComandoPausa(Comando):
    """Comando para pausas, no formato 'a:4', 'c:2', etc."""
    _regex = re.compile(r'[a-g]:(\d+)')
    TEMPO_PADRAO = 3

    def executar(self, ctx):
        m = self._regex.match(ctx.restante)
        duracao = int(m.group(1)) if m else self.TEMPO_PADRAO
        ctx.elementos.append(Evento('pausa', duracao))
        return m.end() if m else 1

class ComandoTrocaInstrumento(Comando):
    """Comando para trocar o instrumento, no formato '1', '2', etc."""
    def __init__(self, novo_valor):
        self._novo_valor = novo_valor

    def executar(self, ctx):
        ctx.estado.instrumento = self._novo_valor
        ctx.elementos.append(Evento('troca_instrumento', self._novo_valor))
        return 1

class ComandoSomaInstrumento(Comando):
    """Dígito par: soma o valor ao instrumento atual."""
    def executar(self, ctx):
        valor = int(ctx.texto[ctx.posicao])
        novo = ctx.estado.instrumento + valor
        ctx.estado.instrumento = novo
        ctx.elementos.append(Evento('troca_instrumento', novo))
        return 1

class ComandoAlterarBpm(Comando):
    """Comando para alterar o BPM, no formato '>' ou '<'."""
    def __init__(self, delta):
        self._delta = delta

    def executar(self, ctx):
        ctx.elementos.append(Evento('alterar_bpm', self._delta))
        return 1

class ComandoDobrarVolume(Comando):
    """Comando para dobrar o volume atual."""
    def executar(self, ctx):
        ctx.estado.dobrar_volume()
        return 1

class ComandoAumentarOitava(Comando):
    """Comando para aumentar em 1 a oitava atual."""
    def executar(self, ctx):
        nova = ctx.estado.oitava + 1
        ctx.estado.oitava = ctx.oitava_padrao if nova > 9 else nova
        return 1

class ComandoDiminuirOitava(Comando):
    """Comando para diminuir em 1 a oitava atual."""
    def executar(self, ctx):
        nova = ctx.estado.oitava - 1
        ctx.estado.oitava = ctx.oitava_padrao if nova < 0 else nova
        return 1

class ComandoRepetir(Comando):
    """Comportamento padrão: repete a última nota ou faz pausa."""
    def executar(self, ctx):
        ultima = ctx.estado.ultima_nota
        if ultima is not None:
            ctx.elementos.append(ultima)
        else:
            ctx.elementos.append(Evento('pausa', ComandoPausa.TEMPO_PADRAO))
        return 1

class ComandoInstrumentoExplicito(Comando):
    """Comando para definir explicitamente o instrumento, no formato 'i:15'."""
    _regex = re.compile(r'i:(\d+)')

    def executar(self, ctx):
        m = self._regex.match(ctx.restante)
        if not m:
            return 1
        novo = int(m.group(1))
        ctx.estado.instrumento = novo
        ctx.elementos.append(Evento('troca_instrumento', novo))
        return m.end()

class FabricaComandos:
    """Fábrica de comandos musicais."""
    def __init__(self):
        self._tabela = {}
        self._padrao = ComandoRepetir()
        self._registrar_todos()

    def _registrar_todos(self):
        """Registra todos os comandos conhecidos na tabela."""
        for c in 'ABCDEFG':
            self._tabela[c] = ComandoNota()
        for c in 'abcdefg':
            self._tabela[c] = ComandoPausa()
        for c in '02468':
            self._tabela[c] = ComandoSomaInstrumento()
        for c in '13579;':
            self._tabela[c] = ComandoTrocaInstrumento(15)

        self._tabela['i'] = ComandoInstrumentoExplicito()
        self._tabela[' '] = ComandoDobrarVolume()
        self._tabela['!'] = ComandoTrocaInstrumento(24)
        self._tabela[','] = ComandoTrocaInstrumento(114)
        self._tabela['?'] = ComandoAumentarOitava()
        self._tabela['.'] = ComandoAumentarOitava()
        self._tabela['V'] = ComandoDiminuirOitava()
        self._tabela['>'] = ComandoAlterarBpm(10)
        self._tabela['<'] = ComandoAlterarBpm(-10)

    def obter_comando(self, caractere):
        """Retorna o comando correspondente ao caractere, ou o padrão se não houver."""
        return self._tabela.get(caractere, self._padrao)
