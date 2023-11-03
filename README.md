# Auto Changelog

## Description

This project Generates automatically a changelog from git metadata. It follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## Run

1. Install libraries.

    ```sh
    pip install -r requirements.txt
    ```

2. Prepare environment variables with Huggingface credentials. Use `.envSAMPLE` as a template.

3. Run program.

    ```sh
    python src/main.py
    ```

## Usage

Run with `--help` to show this information.

```sh
main.py GIT_DIR CHANGELOG_DIR
```

- __GIT_DIR__. Git repository directory. This is the folder to read git information. By default, currentt directory.
- __CHANGELOG_DIR__. Changelog directory. The process write output on this folder. It must contain a _CHANGELOG.md_ file before run. By default, current directory.
