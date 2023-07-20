# ASTool
A tool to analyse SPL 

# How To Execute - Local
Execute 'ExecutionHolder.py' passing git folder to analyse

    python ExecutionHolder.py /my/git/folder

# How To Execute - Docker
Build docker image

    docker build -t astool .


Execute docker image

    export UID && docker run -v /my/git/folder:/app/git \
                             -v /my/project/folder:/app \
                             -u $UID:$UID \
                             astool /app/git


