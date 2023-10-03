import subprocess
import os

print("Extraindo commits. AGUARDE...\n\n")

def extract_commits():
    repo_path = input("Digite o caminho para o repositório local: ")

    commit_hash_command = 'git -C {} log --pretty=format:%H'.format(repo_path)  # Obtém os hashes de commit
    commit_hashes = subprocess.check_output(commit_hash_command.split()).decode().split('\n')

    for commit_hash in commit_hashes:
        if not commit_hash:
            continue

        commit_files_command = 'git -C {} diff-tree --no-commit-id --name-only -r {}'.format(repo_path, commit_hash)  # Obtém os arquivos alterados no commit
        commit_files = subprocess.check_output(commit_files_command.split()).decode().split('\n')

        for file_path in commit_files:
            if not file_path:
                continue

            commit_content_command = 'git -C {} show --raw --no-renames --no-textconv --no-color --binary {}:{}'.format(repo_path, commit_hash, file_path)  # Obtém o conteúdo do arquivo no commit

            try:
                commit_content = subprocess.check_output(commit_content_command.split())
            except subprocess.CalledProcessError:
                print('Arquivo não encontrado no commit {}: {}'.format(commit_hash, file_path))
                continue

            # Cria o diretório de saída (se não existir)
            output_dir = os.path.join('commits', commit_hash[:7])
            os.makedirs(output_dir, exist_ok=True)

            # Escreve o conteúdo binário do commit em um arquivo separado
            output_file = os.path.join(output_dir, file_path.replace('/', '-'))
            with open(output_file, 'wb') as f:
                f.write(commit_content)

            print('Arquivo criado: {}'.format(output_file))

if __name__ == '__main__':
    extract_commits()
