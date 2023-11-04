from datetime import datetime
import re


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
    pattern = r"\[\d+\.\d+\.\d+\]"
    latest = 0
    for i in re.findall(pattern, changelog):
        if int(i[-2]) > latest:
            latest = int(i[-2])
    version_tag = f"[0.0.{latest+1}]"
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
