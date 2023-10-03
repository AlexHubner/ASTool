import csv
from git import Repo

# Caminho para o repositório Git clonado
repo_path = input("\nDigite o caminho para o repositório: ")

print("Calculando a média de arquivos por commit. AGUARDE... \n\n")

# Caminho para o arquivo CSV de saída
output_csv_path = 'ArquivosPorCommits.csv'

# Inicializa o repositório
repo = Repo(repo_path)

# Cria o arquivo CSV e escreve o cabeçalho
with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Commit', 'Quant_Arquivos']  # Cabeçalho base
    commits = list(repo.iter_commits())
    max_files = 0

    # Calcula o número máximo de arquivos alterados por commit
    for commit in commits:
        max_files = max(max_files, len(commit.stats.files))

    # Adiciona os nomes dos arquivos como colunas
    for i in range(max_files):
        fieldnames.append(f'Arquivo{i + 1}')

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Preenche as informações dos commits no arquivo CSV
    total_quant_arquivos = 0
    for commit in commits:
        commit_info = {
            'Commit': commit.hexsha,
            'Quant_Arquivos': len(commit.stats.files)
        }
        total_quant_arquivos += len(commit.stats.files)

        for i, file in enumerate(commit.stats.files.keys()):
            commit_info[f'Arquivo{i + 1}'] = file
        
        writer.writerow(commit_info)

    # Calcula e escreve a média da coluna Quant_Arquivos
    average_quant_arquivos = total_quant_arquivos / len(commits)
    writer.writerow({'Commit': 'Média', 'Quant_Arquivos': average_quant_arquivos})

print(f"As informações dos commits e a média foram escritas em '{output_csv_path}'.")