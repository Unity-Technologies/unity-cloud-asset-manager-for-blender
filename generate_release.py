from git import Repo
import os
import shutil


def add_remote(repo, name, url):
    remote = repo.create_remote(name, url)
    print(f"Added remote {remote.name} with URL {remote.url}")


def remove_remote(repo, name):
    remote = repo.remotes[name]
    repo.delete_remote(remote)
    print(f"Removed remote {remote.name}")


def checkout_tempo_branch(repo, branch_name):
    print("Creating temporary branch...")
    repo.git.checkout('-b', 'tempo-' + branch_name)


def return_to_original_branch(repo, branch_name):
    print("Returning to original branch...")
    repo.git.checkout(branch_name)
    repo.git.branch('-D', 'tempo-' + branch_name)


def add_subtree(repo, remote_name):
    print(f"Adding subtree from remote {remote_name} and branch main...")
    run_subtree_command(repo,["add", "--prefix=PublicRepo/", remote_name, "main", "--squash"])


def pull_changes(repo, remote_name):
    print(f"Pulling changes from public repo...")
    run_subtree_command(repo,["pull", "--prefix=PublicRepo/", remote_name, "main"])


def push_changes(repo, remote_name, local_branch):
    print(f"Pushing changes to branch {local_branch}...")
    repo.git.add(all=True)
    repo.git.commit('-m', 'Update public repo')

    run_subtree_command(repo,["push", "--prefix=PublicRepo/", remote_name, local_branch])


def run_subtree_command(repo, command):
    git_command = ['git', 'subtree'] + command
    print(f"Running '{' '.join(git_command)}'")
    return repo.git.execute(git_command)


def copy_directory(src, dst, ignore=None):
    shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)
    print(f"All files and directories copied from {src} to {dst}")


def ignore_files(dir, files):
    ignore_list = {'.git', '.gitattributes', '.gitignore', '.github', 'PublicRepo', 'generate_release.py'}
    return set(file for file in files if file in ignore_list)


def main():
    public_repo_url = "https://github.com/Unity-Technologies/unity-cloud-asset-manager-for-blender"
    repo = Repo(os.getcwd())
    current_branch = repo.active_branch.name

    if current_branch == 'main' or current_branch == 'develop':
        print("Cannot run this script on the main branch. Please create a new branch and run the script again.")
        return

    # Ensure the public remote is added
    if 'public' not in repo.remotes:
        add_remote(repo, 'public', public_repo_url)

    # Create a temporary branch
    checkout_tempo_branch(repo, current_branch)

    # Add the subtree from the public repository
    add_subtree(repo, 'public')

    # Copy all files and directories to the PublicRepo directory
    copy_directory(os.getcwd(), "PublicRepo/", ignore=ignore_files)

    # Push changes to the branch in the public repository
    push_changes(repo, 'public', current_branch)

    # Reset the local repository to the state before running the script
    repo.git.reset('--hard')

    # Return to the original branch
    return_to_original_branch(repo, current_branch)

    # Remove the public remote
    remove_remote(repo, 'public')


if __name__ == "__main__":
    main()