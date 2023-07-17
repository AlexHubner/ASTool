import os
import csv
import difflib

# Função para comparar as ASTs em pares e armazenar as diferenças em um arquivo CSV
def comparar_ast(arquivos, pasta_resultados):
    for i in range(len(arquivos) - 1):
        arquivo_antigo = arquivos[i]
        arquivo_novo = arquivos[i + 1]

        with open(arquivo_antigo, 'r') as file_antigo, open(arquivo_novo, 'r') as file_novo:
            linhas_antigo = file_antigo.readlines()
            linhas_novo = file_novo.readlines()

            diff = difflib.unified_diff(linhas_antigo, linhas_novo, lineterm='')
            mudancas = list(diff)

            if mudancas:
                nome_pasta_antigo = os.path.basename(os.path.dirname(arquivo_antigo))
                nome_pasta_novo = os.path.basename(os.path.dirname(arquivo_novo))

                # Criar o nome do arquivo de resultado
                nome_arquivo_resultado = f'resultado_{nome_pasta_novo}.csv'

                # Caminho completo para o arquivo de resultado
                caminho_arquivo_resultado = os.path.join(pasta_resultados, nome_arquivo_resultado)

                with open(caminho_arquivo_resultado, 'w', newline='') as csvfile:
                    fieldnames = ['Arquivo', 'Arquivo Comparado', 'Nó Modificado', 'Profundidade']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                    for linha in mudancas:
                        if linha.startswith('+'):
                            # Identificar o nó alterado
                            no_alterado = linha[1:].strip()

                            # Calcular a profundidade do nó alterado
                            profundidade = no_alterado.count('  ')

                            if profundidade > 0:
                                writer.writerow({'Arquivo': nome_pasta_novo,
                                                 'Arquivo Comparado': nome_pasta_antigo,
                                                 'Nó Modificado': no_alterado,
                                                 'Profundidade': profundidade})

# Solicitar o caminho da pasta
pasta = input("Digite o caminho da pasta que contém os arquivos de texto com as ASTs: ")

# Verificar se o caminho da pasta é válido
if not os.path.isdir(pasta):
    print("Caminho inválido!")
    exit(1)

# Solicitar o caminho da pasta para os resultados
pasta_resultados = input("Digite o caminho da pasta para armazenar os resultados: ")

# Verificar se o caminho da pasta para os resultados é válido
if not os.path.isdir(pasta_resultados):
    print("Caminho inválido!")
    exit(1)

# Obter a lista de arquivos de texto nas subpastas da pasta principal
arquivos_ast = []
for diretorio_raiz, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(diretorio_raiz, arquivo)
            arquivos_ast.append(caminho_arquivo)

# Comparar as ASTs nos arquivos e armazenar os resultados em arquivos CSV separados
comparar_ast(arquivos_ast, pasta_resultados)

print("Os resultados foram armazenados em arquivos CSV na pasta indicada.")