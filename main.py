import csv
import os
import shutil
import requests
from datetime import datetime
import time

# Function to read a CSV file and return its content as a list of rows
def read_csv(csv_file):
    if not os.path.exists(csv_file):
        return []
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        repos = [row for row in csv_reader]
    return repos

# Function to search for Rust files in a given GitHub repository
def search_rust_files_in_repo(repo_name,headers):
    url = f"https://api.github.com/search/code?q=extension:rs+repo:{repo_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['total_count'] > 0
    return False

# Function to check if a file contains a specific string
def file_contains_string(file_path, string):
    with open(file_path, 'r') as f:
        if string in f.read():
            return True
    return False

# Function to recursively walk through a directory and find files with a specific extension
def find_files_with_extension(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

# Function to download Rust smart contracts from a given GitHub repository
def download_rust_smart_contracts(repo_name,destination_folder,headers):
    repo_url = f'https://github.com/{repo_name}.git'
    repo_dir = repo_name.split('/')[-1]

    # Clone the repository if it does not exist
    if not os.path.exists(repo_dir): 
        os.system(f'git clone {repo_url} {repo_dir}')

    # Check if any file contains 'near_sdk'
    if any(file_contains_string(file_path, 'near_sdk') for file_path in find_files_with_extension(repo_dir, '.rs')):
        # Then traverse the repository directory recursively and move all Rust files
        for file_path in find_files_with_extension(repo_dir, '.rs'):
            new_file_name = f"{repo_dir}_{os.path.dirname(file_path).replace('/','_')}_{os.path.basename(file_path)}"
            repo_folder = os.path.join(destination_folder, repo_name)
            move_file(file_path, new_file_name, repo_folder)

    # Remove the repository directory
    shutil.rmtree(repo_dir)

# Function to move a file from one location to another
def move_file(file_path,new_file_name,repo_folder):    
    # Ensure the repo folder exists
    os.makedirs(repo_folder, exist_ok=True)

    # Define the destination file path
    destination_file_path = os.path.join(repo_folder, new_file_name)

    # Move the file
    shutil.move(file_path, destination_file_path)

# Function to log processed repositories
def log_repos(repo_name,logged_repos):
    logged_repos.append([repo_name, datetime.now()])
    with open(logged_repos_file, mode='w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(logged_repos)    

# Function to loop through a list of repositories, download Rust smart contracts, and log the processed repositories
def loop_through_repos(repos,destination_folder,logged_repos,headers):
    for repo in repos:
        repo_name = repo[0]

        # Check if the repository has already been processed
        if any(repo_name in row for row in logged_repos):
            continue
        
        # Check for .rs files in the repository
        if not search_rust_files_in_repo(repo_name,headers):
            continue

        # Download the smart contract
        download_rust_smart_contracts(repo_name,destination_folder,headers)
        
        # Log the repository
        log_repos(repo_name,logged_repos)

        # Sleep for 2 seconds to avoid search rate limt of 30 reqs per minute
        time.sleep(2)

# Main script
if __name__ == '__main__':
    # GH API Key
    api_key = os.getenv('GH_API_KEY')
    if not api_key:
        raise ValueError("Please set the GH_API_KEY environment variable.")
    headers = {'Authorization': f'token {api_key}'}

    # Define paths
    directory = '.'
    repos_to_process_file = os.path.join(directory, 'sample.csv') # UPDATE WITH YOUR FILE HERE
    logged_repos_file = os.path.join(directory, 'processed_repos.csv')
    destination_folder = os.path.join(directory, 'data')

    # Load files
    repos = read_csv(repos_to_process_file)
    logged_repos = read_csv(logged_repos_file)

    # Process repos
    loop_through_repos(repos,destination_folder,logged_repos,headers)