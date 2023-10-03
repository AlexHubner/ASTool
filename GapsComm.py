import os
import csv
import git
import difflib
import pandas as pd

def main():
    repo_path = input("\nDigite o caminho para o repositório: ")
    print("Calculando a média de GAPs. AGUARDE... \n\n")
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits())
    
    results = {}

    for commit in commits:
        for modified_file in commit.stats.files.keys():
            if not modified_file.endswith(('.c', '.h')):
                continue  # Ignorar arquivos sem extensão .c ou .h
            
            file_path = os.path.join(repo_path, modified_file)
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                content_str = content.decode('utf-8', errors='ignore')
            except (UnicodeDecodeError, FileNotFoundError):
                continue  # Ignorar arquivos não textuais ou arquivos que não existem

            if commit.parents:
                parent_commit = commit.parents[0]
                try:
                    parent_content = repo.git.show('{}:{}'.format(parent_commit.hexsha, modified_file))
                    diff = difflib.unified_diff(parent_content.splitlines(), content_str.splitlines(), lineterm='', n=0)
                    gaps = [len(line) for line in diff if line.startswith('-')]
                except git.exc.GitCommandError:
                    gaps = [len(line) for line in content_str.splitlines()]
            else:
                gaps = [len(line) for line in content_str.splitlines()]

            total_lines = len(content_str.splitlines())
            
            if total_lines > 1:
                max_gap = max(gaps) if gaps else 0
                normalized_gaps = [gap / max_gap for gap in gaps]  # Normalizar em relação ao maior gap
                average_gap = sum(normalized_gaps) / len(normalized_gaps) if len(normalized_gaps) > 0 else 0
            else:
                normalized_gaps = []  # Evitar resultados vazios
                max_gap = 0
                average_gap = 0

            if modified_file in results:
                results[modified_file]['Med_Arquivo'].append(average_gap)
                results[modified_file]['MGap'] = max(results[modified_file]['MGap'], max_gap)
            else:
                results[modified_file] = {
                    'Arquivo': modified_file,
                    'Med_Arquivo': [average_gap],
                    'MGap': max_gap
                }

    # Eliminar resultados com média normalizada igual a zero
    results = {k: v for k, v in results.items() if max(v['Med_Arquivo']) > 0}

    # Normalizar as médias para o intervalo [0, 1]
    for result in results.values():
        max_med_arquivo = max(result['Med_Arquivo'])
        result['Med_Arquivo'] = round(max_med_arquivo, 2)

    df = pd.DataFrame(list(results.values()))
    overall_average = df['Med_Arquivo'].mean()
    formatted_overall_average = '{:.2f}'.format(overall_average)
    df.to_csv('LinhasGAPs.csv', index=False)

    with open('LinhasGAPs.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Média Geral', formatted_overall_average, ''])

if __name__ == '__main__':
    main()
