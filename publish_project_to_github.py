import os
import subprocess
TOKEN = os.environ.get('GITHUB_TOKEN')

# Function to execute shell commands
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error executing command: {command}\n{stderr.decode()}")
    return stdout.decode()

# Set your GitHub repository details
GITHUB_USERNAME = 'ali-tuna-cybersec'
REPO_NAME = 'network-scanner'
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# Project directory setup
project_dir = os.path.expanduser('/home/rakun/cybersecurity-projects/network-scanner')
os.makedirs(project_dir, exist_ok=True)

# Read and save content from text files
def save_file_from_txt(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

def load_content_from_txt(txt_file):
    with open(txt_file, 'r') as f:
        return f.read()

# Paths to the text files
network_scanner_script_txt = 'network_scanner_script.txt'
readme_content_txt = 'README_content.txt'
setup_content_txt = 'SETUP_content.txt'
usage_content_txt = 'USAGE_content.txt'

# Load content from text files
network_scanner_script = load_content_from_txt(network_scanner_script_txt)
readme_content = load_content_from_txt(readme_content_txt)
setup_content = load_content_from_txt(setup_content_txt)
usage_content = load_content_from_txt(usage_content_txt)

# Save files in the project directory
save_file_from_txt(os.path.join(project_dir, 'network_scanner.py'), network_scanner_script)

docs_dir = os.path.join(project_dir, 'docs')
os.makedirs(docs_dir, exist_ok=True)
save_file_from_txt(os.path.join(docs_dir, 'README.md'), readme_content)
save_file_from_txt(os.path.join(docs_dir, 'SETUP.md'), setup_content)
save_file_from_txt(os.path.join(docs_dir, 'USAGE.md'), usage_content)

# Create logs, reports, and screenshots directories
for sub_dir in ['logs', 'reports', 'screenshots']:
    os.makedirs(os.path.join(project_dir, sub_dir), exist_ok=True)

# Git commands to initialize repository and push to GitHub
commands = [
    f'cd {project_dir}',
    'git init',
    'git add .',
    'git commit -m "Initial commit with network scanner script and documentation"',
    f'git remote add origin {REPO_URL}',
    f'git push -u https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git main'
]

# Execute Git commands
for command in commands:
    run_command(command)

print("Project and documentation successfully published to GitHub.")
