import os
import csv
import sys

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

def calcular_media_geral(pasta, caminho_arquivo_saida):

    lista_arquivos = [arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.csv')]
    valores_media = [calcular_media_arquivo(os.path.join(pasta, arquivo)) for arquivo in lista_arquivos]
    
    media_geral = sum(valores_media) / len(valores_media) if len(valores_media) > 0 else 0

    with open(caminho_arquivo_saida, 'w', newline='') as arquivo_saida:
        escritor = csv.writer(arquivo_saida)
        escritor.writerow(['Arquivo', 'Média'])
        for arquivo, media in zip(lista_arquivos, valores_media):
            escritor.writerow([arquivo, media])
        escritor.writerow(['Média Geral', media_geral])
    
    print("Cálculo das médias concluído. O arquivo 'media_geral.csv' foi gerado.")

def get_folder_path(prompt, index):
    if len(sys.argv) > index:
        return sys.argv[index]
    else:
        return input(prompt)

if __name__ == '__main__':

    pasta_origem = get_folder_path("Digite o caminho da pasta com os arquivos CSV: ", 1)
    caminho_arquivo_saida = get_folder_path("Digite o caminho para a pasta de saída: ", 2)
    caminho_arquivo_saida = os.path.join(caminho_arquivo_saida, 'media_geral.csv')

    calcular_media_geral(pasta_origem, caminho_arquivo_saida)
