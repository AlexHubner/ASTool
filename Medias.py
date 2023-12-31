import os
import csv

print("\nCalculando as médias de profundidade. AGUARDE... \n\n")

def calcular_media_arquivo(nome_arquivo):
    soma = 0
    contador = 0
    with open(nome_arquivo, 'r') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            profundidade = float(linha['Profundidade'])
            soma += profundidade
            contador += 1
    if contador > 0:
        media = soma / contador
        return media
    return 0

def calcular_media_geral(pasta):
    lista_arquivos = os.listdir(pasta)
    valores_media = []
    for arquivo in lista_arquivos:
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            media = calcular_media_arquivo(caminho_arquivo)
            valores_media.append(media)
    
    media_geral = sum(valores_media) / len(valores_media) if len(valores_media) > 0 else 0
    
    with open('media_geral.csv', 'w', newline='') as arquivo_saida:
        escritor = csv.writer(arquivo_saida)
        escritor.writerow(['Arquivo', 'Média'])
        for arquivo, media in zip(lista_arquivos, valores_media):
            # Formatar a média com até 4 casas decimais
            media_formatada = "{:.4f}".format(media)
            escritor.writerow([arquivo, media_formatada])
        media_geral_formatada = "{:.4f}".format(media_geral)
        escritor.writerow(['Média Geral', media_geral_formatada])
    
    print("Cálculo das médias concluído. O arquivo 'media_geral.csv' foi gerado.")

# Solicitar ao usuário a pasta de origem dos arquivos CSV
pasta_origem = "analises"

calcular_media_geral(pasta_origem)
