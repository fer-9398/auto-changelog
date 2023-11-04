from datetime import datetime
import re
import os
import git

def changelog_checker():
    """
    Description: Check if the CHANGELOG.md file exists. And if it does not exist, 
    create it from template.
    
    Arguments:
        None
    """
    if not os.path.exists("CHANGELOG.md"):
        with open("src/changelog_template.md", "r") as f:
            changelog_template = f.read()
        with open("CHANGELOG.md", "w") as file:
            file.write(changelog_template)
    else:
        pass

def tag_handler(repo_path) -> str:
    """
    Description: Get the latest version tag from git repository.
    In order to properly work git tag command must be used before git commit.
    
    arguments:
        repo_path (str): path to git repository

    return:
        str: latest version tag
    """
    try:
        repo = git.Repo(repo_path)
        tags = repo.tags
        latest_tag = max(tags, key=lambda t: t.commit.committed_date)
        return str(latest_tag)
    except git.exc.NoSuchPathError:
        return "Invalid repository path"
    except ValueError:
        return "No tags found in the repository"


def tag_checker(text: None, dir: str = './'):
    """
    Description: Check if a version tag exists. If it exists, it will be used in changelog. 
    otherwise a minor version tag will be created and used in changelog.
    
    Arguments:
        None
    """
    if dir:
        changelog_file = dir + "/CHANGELOG.md"
    else:
        changelog_file = "CHANGELOG.md"
    
    with open(changelog_file) as file:
        changelog = file.read()
    pattern = r"\[\d+\.\d+\.\d+\]"
    latest = 0
    greatest = None
    for version_match in re.findall(pattern, changelog):
        version_str = version_match[1:-1]
        major, minor, patch = map(int, version_str.split('.'))
        weighted_value_changelog = major * 1000 + minor * 100 + patch
        if weighted_value_changelog > latest:
            latest = weighted_value_changelog
            greatest = version_str
        else:
            pass
    if greatest:
        print(f"The greatest version is {greatest}")
    else:
        greatest = None
        print("There is no version tag in CHANGELOG.md")

    git_tag = tag_handler(dir)
    print(f"The latest tag in git is {git_tag}")
    try:
        major, minor, patch = map(int, git_tag.split('.'))
        weighted_value_git = major * 1000 + minor * 100 + patch
    except Exception as e:
        raise Exception(e) 
    if re.match(r'\[\d+\.\d+\.\d+\]', git_tag) and weighted_value_git > weighted_value_changelog:
        tag = git_tag
    elif greatest == None and len(git_tag) != 5:
        tag = '[0.1.0]'
    else:
        tag = f'[{int(greatest[0])}.{int(greatest[2])+1}.{int(greatest[4])}]'
    return tag

def parse(text: str, dir: str = None):
    """
    Description:
        Parse the text from huggingface chatbot and save it to CHANGELOG.md

    Arguments:
        text (str): Information to save in CHANGELOG.
        dir (str): Changelog folder.
    """
    if dir:
        changelog_file = dir + "/CHANGELOG.md"
    else:
        changelog_file = "CHANGELOG.md"

    with open(changelog_file) as file:
        changelog = file.read()
    version_tag = tag_checker(None, dir)
    today = datetime.today().strftime("%Y-%m-%d")
    first_line = f"## {version_tag} - {today}"
    # Locate the "Unreleased" section
    unrelease_tag = len("## [Unreleased]")
    unreleased_index = changelog.find("## [Unreleased]")
    if unreleased_index != -1:
        # Add your text after the "Unreleased" section
        changelog = (
            changelog[: (unreleased_index + unrelease_tag)] + "\n"
            "\n" + first_line + text + changelog[(unrelease_tag + unreleased_index) :]
        )

    # Write the updated changelog back to the file
    with open(changelog_file, "w") as file:
        file.write(changelog)
