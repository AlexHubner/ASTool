import os
import shutil

def reorganize_files():
    commits_path = input("Digite o caminho para a pasta dos commits: ")
    output_path = input("Digite o caminho para a pasta de saída: ")

    for root, _, files in os.walk(commits_path):
        for file_name in files:
            if file_name.endswith('.c'):
                commit_date = os.path.basename(root)
                commit_hash = os.path.basename(os.path.dirname(root))
                file_path = os.path.join(root, file_name)

                output_dir = os.path.join(output_path, file_name)
                os.makedirs(output_dir, exist_ok=True)

                output_file = os.path.join(output_dir, commit_hash[:7] + '_' + commit_date + '.c')
                shutil.copy2(file_path, output_file)

                print('Arquivo movido: {}'.format(output_file))

if __name__ == '__main__':
    reorganize_files()
