# ASTool
A tool to analyse SPL 

# How To Execute - Local
Execute 'ExecutionHolder.py' passing git folder to analyse

    python ExecutionHolder.py /my/git/folder

# How To Execute - Docker
Build docker image

    docker build -t astool .


Execute docker image

    docker run -v /my/git/folder:/my/git/folder \
               -v /my/project/folder:/my/project/folder \
               -e GIT_READ_FOLDER=/my/git/folder astool


