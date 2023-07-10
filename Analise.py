import os
import csv
import difflib

# Função para comparar as ASTs em pares e armazenar as diferenças em um arquivo CSV
def comparar_ast(arquivos, arquivo_csv):
    with open(arquivo_csv, 'w', newline='') as csvfile:
        fieldnames = ['Arquivo', 'Arquivo Comparado', 'Nó Modificado', 'Profundidade']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(arquivos) - 1):
            arquivo_antigo = arquivos[i]
            arquivo_novo = arquivos[i + 1]

            with open(arquivo_antigo, 'r') as file_antigo, open(arquivo_novo, 'r') as file_novo:
                linhas_antigo = file_antigo.readlines()
                linhas_novo = file_novo.readlines()

                diff = difflib.unified_diff(linhas_antigo, linhas_novo, lineterm='')
                mudancas = list(diff)

                if mudancas:
                    for linha in mudancas:
                        if linha.startswith('+'):
                            # Identificar o nó alterado
                            no_alterado = linha[1:].strip()

                            # Calcular a profundidade do nó alterado
                            profundidade = no_alterado.count('  ')

                            if profundidade > 0:
                                writer.writerow({'Arquivo': os.path.basename(arquivo_novo),
                                                 'Arquivo Comparado': os.path.basename(arquivo_antigo),
                                                 'Nó Modificado': no_alterado,
                                                 'Profundidade': profundidade})

# Solicitar o caminho da pasta
pasta = input("Digite o caminho da pasta que contém os arquivos de texto com as ASTs: ")

# Verificar se o caminho da pasta é válido
if not os.path.isdir(pasta):
    print("Caminho inválido!")
    exit(1)

# Obter a lista de arquivos de texto na pasta
arquivos_ast = sorted([os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta) if arquivo.endswith('.txt')])

# Caminho do arquivo CSV para armazenar os resultados
arquivo_csv = 'resultados.csv'

# Comparar as ASTs nos arquivos e armazenar os resultados no arquivo CSV
comparar_ast(arquivos_ast, arquivo_csv)

print(f"Os resultados foram armazenados em: {arquivo_csv}")