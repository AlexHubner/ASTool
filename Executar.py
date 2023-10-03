import subprocess

# Lista dos scripts na ordem especificada
scripts = [
    'ExtComm.py',
    'ReComm.py',
    'MakeTrees.sh',
    'Analise.py',
    'Medias.py',
    'Commit_Files.py',
    'GapsComm.py'
]
print("ASTool em execução.")
# Percorre a lista de scripts e executa cada um
for script in scripts:
    try:
        # Verifica se o script é um arquivo Shell (.sh) e executa com 'bash'
        if script.endswith('.sh'):
            subprocess.run(['bash', script], check=True)
        else:
            # Caso contrário, assume que é um script Python e executa com 'python'
            subprocess.run(['python', script], check=True)
        print(f'Script {script} executado com sucesso')
    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar o script {script}: {e}')
