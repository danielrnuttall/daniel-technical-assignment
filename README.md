# daniel-technical-assignment-csv-pace-calculator

## Project Setup
### VS Code
- The recommended IDE for development is Visual Studio Code.
- The .vscode/extensions.json and requirements.txt provide detail on the necessary plugins and libaries required to run the project.
### Setup Guide

A virtual environment (venv) is required to run a Python project. To set this up, follow the OS specific instructions below.

#### Mac OS
- Ensure that Python 3 is installed by running the following in a new terminal session in VSCode: `python3 --version`
- If not installed - install Python from python.org or using Brew (MacOS).
- Next, run the following commands in the terminal to activate the virtual environment (from root directory of project):

    `python3 -m venv .venv`

    `source .venv/bin/activate`
- There should now be a .venv directory at the root of the project.

#### Windows / Ubuntu 20.04
- First Download Ubuntu. [Manual installation steps for older versions of WSL | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install-manual)
    - Follow Step 1 and Step 6
    - Ubuntu 20.04 LTS
- Open WSL Ubuntu in VS Code.
- Ensure that Python 3 is installed by running the following in a new terminal session in VSCode: `python3 --version`
- If not installed - install Python from [python.org](http://python.org)
- Next, run the following commands in the terminal to activate the virtual environment (from root directory of project):

    `python3 -m venv .venv`

    `source .venv/bin/activate`
- There should now be a .venv directory at the root of the project.

> Make sure to set the Python interpreter for the project to match the version in the virtual environment (e.g. .venv/bin/python3). Use the command palette in VS Code to select an interpreter.

### Install Requirements
The following steps apply regardless of OS.
- To update the venv with all the necessary libraries/frameworks for running the project, from the terminal, run the following command: 

    `pip install -r requirements.txt`