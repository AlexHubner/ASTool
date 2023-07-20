import os
import sys
import subprocess

def create_directories():

    GIT_FOLDER_PATH = sys.argv[1]
    CURRENT_FOLDER = os.getcwd()

    GIT_FOLDER_NAME = os.path.basename(GIT_FOLDER_PATH)

    BUILDED_PATH = os.path.join(CURRENT_FOLDER, "ToAnalyze", GIT_FOLDER_NAME)
    PROCESSED_GIT_COMMITS_FOLDER = os.path.join(BUILDED_PATH, "commits")
    REORGANIZED_GIT_COMMITS_FOLDER = os.path.join(BUILDED_PATH, "output")
    TREE_FOLDER = os.path.join(BUILDED_PATH, "tree")
    REPORT_FOLDER = os.path.join(BUILDED_PATH, "report")

    os.makedirs(PROCESSED_GIT_COMMITS_FOLDER, exist_ok=True)
    os.makedirs(REORGANIZED_GIT_COMMITS_FOLDER, exist_ok=True)
    os.makedirs(TREE_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    return BUILDED_PATH, GIT_FOLDER_PATH, PROCESSED_GIT_COMMITS_FOLDER, REORGANIZED_GIT_COMMITS_FOLDER, TREE_FOLDER, REPORT_FOLDER

def execute_steps():
    
    BUILDED_PATH, GIT_FOLDER_PATH, PROCESSED_GIT_COMMITS_FOLDER, REORGANIZED_GIT_COMMITS_FOLDER, TREE_FOLDER, REPORT_FOLDER = create_directories()

    ext_comm_command = ["python", "ExtComm.py", GIT_FOLDER_PATH, PROCESSED_GIT_COMMITS_FOLDER]
    re_comm_command = ["python", "ReComm.py", PROCESSED_GIT_COMMITS_FOLDER, REORGANIZED_GIT_COMMITS_FOLDER]
    make_trees_command = ["/bin/bash", "MakeTrees.sh", REORGANIZED_GIT_COMMITS_FOLDER, TREE_FOLDER]
    analise_command = ["python", "Analise.py", TREE_FOLDER, REPORT_FOLDER]
    medias_command = ["python", "Medias.py", REPORT_FOLDER, BUILDED_PATH]

    run_command(ext_comm_command)
    run_command(re_comm_command)
    run_command(make_trees_command)
    run_command(analise_command)
    run_command(medias_command)

def run_command(command):
    subprocess.run(command)

if __name__ == "__main__":
    execute_steps()