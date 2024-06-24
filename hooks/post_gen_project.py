"""Cookiecutter post-generate hook."""

#!/usr/bin/env python

import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath: str) -> None:
    """Remove a file."""
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    """Remove a directory."""
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def create_git() -> None:
    """Create a git repository."""
    subprocess.call(["git", "init"])
    subprocess.call(["git", "add", "*"])
    subprocess.call(["git", "commit", "-m", "Initial commit"])


if __name__ == "__main__":
    print("Creating git repository...")
    create_git()
