import tradutor 
import audio 
import modelos
import arquivos
from time import perf_counter
import pygame

gerenciador = arquivos.GerenciadorArquivos()
traduzido = tradutor.Tradutor()
gerador = audio.GeradorMidi()
toca = audio.ReprodutorAudio()

texto = gerenciador.ler_arquivo_txt()

start = perf_counter()
partitura = traduzido.analisar(texto)
print(f"Parsing: {perf_counter() - start:.3f}s")

#Para printar as notas e eventos:
"""
for i in range(len(partitura.vozes)):
    if partitura.vozes[i] is not None:
        print(f"Voz {i+1}:")
        for elemento in partitura.vozes[i].lista_elementos:
            if isinstance(elemento, modelos.Nota):
                print(f"Nota: {elemento.nome}, Oitava: {elemento.oitava}, Volume: {elemento.volume}, Duração: {elemento.duracao}, Acidente: {elemento.acidente}")
            elif isinstance(elemento, modelos.Evento):
                print(f"Evento: Tipo: {elemento.tipo}, Valor: {elemento.valor}")
    else:
        print(f"Voz {i+1}: Nenhum elemento processado.")
"""

# 3. Cria a lista de vozes (o objeto Partitura espera uma lista/coleção de vozes)
start = perf_counter()
gerador.cria_midi(partitura, "testemidi.mid")
print(f"MIDI generation: {perf_counter() - start:.3f}s")

print('criada')

pygame.mixer.init()

start = perf_counter()
toca.tocar("testemidi.mid")
print(f"Loading/starting playback: {perf_counter() - start:.3f}s")
