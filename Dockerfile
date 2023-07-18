# Imagem base
FROM python:3.9

# Instalação das dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    ocaml \
    libnum-ocaml-dev

# Criação do diretório de trabalho
WORKDIR /app

# Copia dos arquivos .py para o contêiner
COPY . /app/

RUN chmod 777 /app
RUN git config --global --add safe.directory '*'

# Argumentos para a execução do contêiner
ARG GIT_READ_FOLDER

# Definição das variáveis de ambiente
ENV GIT_READ_FOLDER $GIT_READ_FOLDER

# Comando a ser executado ao iniciar o contêiner
CMD ["/bin/bash", "/app/ExecutionHolder.sh", "$GIT_READ_FOLDER"]