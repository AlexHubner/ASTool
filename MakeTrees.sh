#!/bin/bash

#Solicitar o caminho da pasta com os arquivos C
read -p "Digite o caminho da pasta que contém os arquivos C: " pasta_origem

#Solicitar o caminho da pasta para salvar as ASTs
read -p "Digite o caminho da pasta para salvar as ASTs: " pasta_destino

#Função recursiva para percorrer as subpastas
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

    # Gerar a AST do arquivo e gravar em um arquivo de texto
    clang -Xclang -detailed-preprocessing-record -Xclang -ast-dump "$arquivo" > "$arquivo_saida"

    echo "AST gerada para o arquivo $nome_arquivo e gravada em $arquivo_saida"
done

# Loop pelas subpastas na pasta atual
for subpasta in "$pasta_atual"/*; do
    if [ -d "$subpasta" ]; then
        percorrer_subpastas "$subpasta"
    fi
done

}

#Verificar se o caminho da pasta origem é válido
if [ ! -d "$pasta_origem" ]; then
echo "Caminho da pasta origem inválido!"
exit 1
fi

#Verificar se o caminho da pasta destino é válido
if [ ! -d "$pasta_destino" ]; then
echo "Caminho da pasta destino inválido!"
exit 1
fi

#Chamada inicial para percorrer as subpastas
percorrer_subpastas "$pasta_origem"

echo "ARVORES CRIADAS!"