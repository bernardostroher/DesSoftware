import tradutor 
import audio 
import modelos

texto = '\n?C:2E:3G:3???B:3B:4?C:5D:5C:3cA:2G:3?C:3???G:3F:4E:5F:5E:3c\nC:4G:4E:4G:4C:4G:4E:4G:4D:4G:4F:4G:4C:4G:4E:4G:4C:4A:4F:4A:4C:4G:4E:4G:4B:4G:4D:4G:4C:4G:4E:4G:4'

traduzido = tradutor.Tradutor()
gerador = audio.GeradorMidi()
toca = audio.ReprodutorAudio()
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
