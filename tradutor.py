"""Módulo responsável por traduzir o texto de entrada em uma partitura estruturada."""
import re
from modelos import EstadoVoz, Partitura, Evento, Voz
from comandos import FabricaComandos, Contexto

class Tradutor:
    """Traduz o texto de entrada em uma partitura estruturada."""
    def __init__(self, fabrica=None):
        self._fabrica = fabrica or FabricaComandos()
        self._oitavas_padrao = [6, 5, 4, 3]
        self._volumes_padrao = [100, 80, 60, 40]
        self._instrumentos_padrao = [6, 20, 0, 70]
        self._bpm_inicial = 120

    def analisar(self, texto):
        """Analisa o texto de entrada e retorna uma partitura estruturada."""
        linhas = texto.strip().splitlines()
        vozes_processadas = []
        for i, linha in enumerate(linhas):
            id_voz = i % 4
            voz = self._processar_linha(linha, id_voz)
            vozes_processadas.append(voz)
        return Partitura(vozes_processadas)

    def _processar_linha(self, linha, id_voz):
        if not linha.strip():
            return None

        prefixo_atraso = re.match(r'^([<>,]*)\[(\d+)\]\s*', linha)

        if prefixo_atraso:
            comandos_iniciais = prefixo_atraso.group(1)
            atraso = int(prefixo_atraso.group(2))
            linha_limpa = linha[prefixo_atraso.end():]
        else:
            comandos_iniciais = ''
            atraso = 0
            linha_limpa = linha

        estado_atual = EstadoVoz(self._oitavas_padrao[id_voz],
                                 self._volumes_padrao[id_voz], self._instrumentos_padrao[id_voz])

        elementos_musicais = []
        elementos_musicais.append(Evento('troca_instrumento', estado_atual.instrumento))
        if id_voz == 0:
            elementos_musicais.append(Evento('definir_bpm', self._bpm_inicial))

        if comandos_iniciais:
            ctx_iniciais = Contexto(
                comandos_iniciais, 0, elementos_musicais, estado_atual,
                self._oitavas_padrao[id_voz]
                )
            while ctx_iniciais.posicao < len(ctx_iniciais.texto):
                comando = self._fabrica.obter_comando(
                ctx_iniciais.texto[ctx_iniciais.posicao]
             )
                ctx_iniciais.posicao += comando.executar(ctx_iniciais)


        if atraso > 0:
            elementos_musicais.append(Evento('atraso', atraso))

        ctx = Contexto(linha_limpa, 0, elementos_musicais,
                       estado_atual, self._oitavas_padrao[id_voz])

        while ctx.posicao < len(linha_limpa):
            comando = self._fabrica.obter_comando(linha_limpa[ctx.posicao])
            ctx.posicao += comando.executar(ctx)

        return Voz(elementos_musicais)
