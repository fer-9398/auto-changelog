import os
from dotenv import load_dotenv
from hugchat import hugchat
from hugchat.login import Login
import subprocess

load_dotenv()

EMAIL = os.environ.get("EMAIL")
PASSW = os.environ.get("PASSWORD")
# Log in to huggingface and grant authorization to huggingchat
sign = Login(EMAIL, PASSW)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)


def changelog_hugging(dir: str = None):
    """
    Description:
        Generate a detailed changelog for the following diff output.

    Arguments:
        dir(str): Git repository directory. By default, current directory.

    Return:
        str: ...
    """
    try:
        command = ["git", "diff", "HEAD~2", "HEAD~1"]

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=dir)
        output, _ = process.communicate()

        var = output.decode()
        pretext = """### Added

        * .env
        * cookies_snapshot

        ### Modified

        * auto_changelog.ipynb
        + Added imports for os and dotenv
        + Replaced hardcoded email and password with environment variables EMAIL and PASSW
        + Saved cookies to the local directory instead of logging them to the console
        * .gitignore
        + Ignored the .env and cookies_snapshot directories

        Now it's your turn to write a changelog for the following diff:
        """

        chatbot = hugchat.ChatBot(
            cookies=cookies.get_dict()
        )  # or cookie_path="usercookies/<email>.json"
        query_result = chatbot.query(pretext + var, stream=False)
        text = query_result.text
        lines = text.split("\n")

        # if any line contains a special character, keep it otherwise remove it
        for i in range(len(lines)):
            if any(char in lines[i] for char in ["+", "-", "*", "!", "#", "=", "", None]):
                pass
            else:
                lines[i] = None

        modified_text = "\n".join(lines)
        
        if modified_text == None:
            raise Exception("No changelog generated due to some error")
        else:
            pass
        return modified_text

    except Exception as e:
        raise Exception(e)
