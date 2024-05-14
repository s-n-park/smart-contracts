# Smart Contracts Dataset
This Python script downloads Rust smart contracts from a list of GitHub repositories, and logs the processed repositories. It specifically looks for files that include "near_sdk".

## How it works

1. The script reads a CSV file containing a list of GitHub repositories.
2. For each repository, it checks if there are any Rust files (`.rs` extension) in the repository using the GitHub Search API.
3. If Rust files are found, the repository is cloned, and the Rust files containing "near_sdk" are moved to a specified destination folder.
4. The repository name and the current timestamp are logged to a CSV file.

## Setup

1. Clone this repository.
2. Install the required Python libraries with `pip install -r requirements.txt`.
3. Set the `GH_API_KEY` environment variable to your GitHub API key. On Unix-based systems, you can do this with `export GH_API_KEY=your_api_key`. On Windows, use `set GH_API_KEY=your_api_key`.
4. Run the script with `python main.py`.

## Usage

1. Prepare a CSV file with a list of GitHub repositories to process. Each row should contain the full name of a repository. For example, if the repository's URL is `https://github.com/user/repo_name`, the full name would be `user/repo_name`.
2. Specify the path to this CSV file in the `repos_to_process_file` variable in the script.
3. Set your GitHub API key in the `api_key` variable.
4. Run the script with `python main.py`.

## Requirements

- Python 3
- `requests` library