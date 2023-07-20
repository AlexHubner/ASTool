# Imagem base
FROM python:3.11-bookworm

# Instalação das dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    ocaml \
    libnum-ocaml-dev \
    gpg lsb-release wget software-properties-common

# Instala clang
RUN set -ex &&\
    echo "deb http://apt.llvm.org/bookworm/ llvm-toolchain-bookworm-15 main" > /etc/apt/sources.list.d/apt.llvm.org.list &&\
    wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key |  tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc &&\
    apt update &&\
    apt-get install -y clang-15 lldb-15 lld-15 clangd-15 clang-tidy-15 clang-format-15 clang-tools-15 llvm-15-dev lld-15 lldb-15 llvm-15-tools libomp-15-dev libc++-15-dev libc++abi-15-dev libclang-common-15-dev libclang-15-dev libclang-cpp15-dev libunwind-15-dev libclang-rt-15-dev libpolly-15-dev

# Cria alias clang
RUN ln -s /usr/bin/clang-15 /usr/bin/clang

# Instala cgum
RUN git clone https://github.com/GumTreeDiff/cgum.git /tmp/cgum && \
              make -C /tmp/cgum && \
              cp /tmp/cgum/cgum /usr/local/bin && \
              cp /tmp/cgum/cgumw /usr/local/bin/ && \
              install -D /tmp/cgum/standard.h /root/cgum/standard.h && \
              rm -Rf /tmp/cgum && \
              /usr/local/bin/cgum /root/cgum/standard.h > /dev/null 

# Criação do diretório de trabalho
WORKDIR /app

# Copia dos arquivos .py para o contêiner
COPY . /app/

RUN git config --global --add safe.directory '*'

# Concede permissao para todo diretório
RUN chmod 777 /app

# Comando a ser executado ao iniciar o contêiner
ENTRYPOINT ["python", "/app/ExecutionHolder.py"]