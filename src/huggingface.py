import os
from dotenv import load_dotenv
from hugchat import hugchat
from hugchat.login import Login
import subprocess

load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSW = os.environ.get('PASSWORD')
# Log in to huggingface and grant authorization to huggingchat
sign = Login(EMAIL, PASSW)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)


def changelog_hugging():
    command = 'git diff HEAD~2 HEAD~1'

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()

    var = output.decode()
    pretext = "I want you to generate a detailed changelog for the following git diff output I'll provide you with, the format must the Keep a Changelog format : "

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
    query_result = chatbot.query(pretext + var, stream=False)
    text = query_result.text
    lines = text.split('\n')

    if len(lines) >= 2:
        lines = lines[1:-1]

    modified_text = '\n'.join(lines)

    return modified_text
