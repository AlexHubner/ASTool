import os
import sys
import subprocess

pasta_origem = sys.argv[1]
pasta_destino = sys.argv[2]

def percorrer_subpastas(pasta_atual):
    pasta_relativa = os.path.relpath(pasta_atual, pasta_origem)  # Obter o caminho relativo

    # Loop pelos arquivos C na pasta atual
    for arquivo in os.scandir(pasta_atual):
        if arquivo.is_file() and arquivo.name.endswith('.c'):
            nome_arquivo = arquivo.name
            nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
            arquivo_saida = os.path.join(pasta_destino, pasta_relativa, f'{nome_sem_extensao}.txt')

            # Criar a pasta de destino, se não existir
            os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)

            # Gerar a AST do arquivo e gravar em um arquivo de texto
            subprocess.run(['clang', '-Xclang', '-detailed-preprocessing-record', '-Xclang', '-ast-dump', arquivo.path],
                           stdout=open(arquivo_saida, 'w'))

            print(f'AST gerada para o arquivo {nome_arquivo} e gravada em {arquivo_saida}')

        elif arquivo.is_dir():
            percorrer_subpastas(arquivo.path)  # Chamada recursiva para subpastas

# Verificar se o caminho da pasta origem é válido
if not os.path.isdir(pasta_origem):
    print('Caminho da pasta origem inválido!')
    sys.exit(1)

# Verificar se o caminho da pasta destino é válido
if not os.path.isdir(pasta_destino):
    print('Caminho da pasta destino inválido!')
    sys.exit(1)

# Chamada inicial para percorrer as subpastas
percorrer_subpastas(pasta_origem)

print('ARVORES CRIADAS!')