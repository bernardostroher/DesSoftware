import tradutor 
import audio 
import modelos
import arquivos

gerenciador = arquivos.GerenciadorArquivos()
traduzido = tradutor.Tradutor()
gerador = audio.GeradorMidi()
toca = audio.ReprodutorAudio()

texto = gerenciador.ler_arquivo_txt()

partitura = traduzido.analisar(texto)

#Para printar as notas e eventos:
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


# 3. Cria a lista de vozes (o objeto Partitura espera uma lista/coleção de vozes)
gerador.cria_midi(partitura, "testemidi.mid")
print('criada')
toca.tocar("testemidi.mid")
