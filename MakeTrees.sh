#!/bin/bash

# Pasta de entrada
pasta_origem="commits_org"

# Pasta de saída
pasta_destino="asts"

# Função recursiva para percorrer as subpastas
function percorrer_subpastas() {
    local pasta_atual=$1
    local pasta_relativa=${pasta_atual#$pasta_origem} # Obter a parte relativa do caminho

    # Loop pelos arquivos C na pasta atual
    for arquivo in "$pasta_atual"/*.c; do
        nome_arquivo=$(basename "$arquivo")
        nome_sem_extensao="${nome_arquivo%.*}"
        arquivo_saida="${pasta_destino}${pasta_relativa}/${nome_sem_extensao}.txt"  # Caminho de saída com a estrutura de subpastas preservada

        # Criar a pasta de destino, se não existir
        mkdir -p "$(dirname "$arquivo_saida")"

        # Gerar a AST do arquivo e gravar em um arquivo de texto (suprimindo os erros)
        clang -Xclang -detailed-preprocessing-record -Xclang -ast-dump "$arquivo" > "$arquivo_saida" 2>/dev/null
    done

    # Loop pelas subpastas na pasta atual
    for subpasta in "$pasta_atual"/*; do
        if [ -d "$subpasta" ]; then
            percorrer_subpastas "$subpasta"
        fi
    done
}

# Verificar se a pasta de entrada existe
if [ ! -d "$pasta_origem" ]; then
    echo "A pasta de entrada 'commits_org' não foi encontrada!"
    exit 1
fi

# Verificar se a pasta de saída existe ou criar se não existir
if [ ! -d "$pasta_destino" ]; then
    mkdir -p "$pasta_destino"
fi

# Chamada inicial para percorrer as subpastas
percorrer_subpastas "$pasta_origem"

echo "ARVORES CRIADAS!"
