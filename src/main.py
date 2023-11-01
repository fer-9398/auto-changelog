from huggingface import changelog_hugging
from parse import parse

if __name__ == '__main__':
    text = changelog_hugging()
    parse(text)