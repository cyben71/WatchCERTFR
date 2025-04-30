# EssencePy
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

**EssencePy** is a lightweight and modular Python project designed to serve as a modular foundation for technical projects and automation workflows.
It brings together reusable utilities, structured code organization, and cross-platform compatibility (Linux & Windows), making it ideal for building reliable tools quickly.

> EssencePy is the *core essence* of many future tools — minimal yet extensible.

---

## 🚀 Key Features

- 🔧 **Modular Design** — Clean separation of concerns, designed for easy customization and extension.
- 🖥️ **Cross-Platform** — Compatible with both Linux and Windows environments.
- 🗂️ **Structured Setup** — Includes standard directories for logs, scripts, notebooks, configs, and reusable libraries.
- 📦 **Utilities Included** — Config reader, environment info loader, and more.
- 🧪 **Notebook/Script Ready** — Load and execute code from Jupyter or as standalone Python scripts.

---

## 📁 Project Structure (Sample)
```shell
EssencePy/ 
├── app/            # Python applications folder
├── config/         # Configuration files (.yaml, .properties, etc.) 
├── lib/            # Core Python libraries 
│ └── init/         # Autoloaded classes (e.g., ConfigLoader, AppEnv, etc.) 
├── logs/           # Application logs  (folder automatically created if not existing)
├── notebooks/      # Jupyter notebooks for development or analysis 
├── scripts/        # Core executable scripts
│ ├── shell/        # Scripts for Linux OS
│ └── powershell/   # Scripts for Windows OS
└── README.md
```

## 📌 Goals

- Provide a reusable starting point for scripting, automation or other cool stuff
- Maintain simplicity while allowing for scalability
- Ensure portability and easy setup across environments

## 📣 About

This project started as a personal toolkit to accelerate scripting and automation tasks across various technical contexts.
Now open-sourced to share its benefits, and evolve through real-world usage.

Feel free to fork, extend, and adapt EssencePy to your own workflows 💡

## 🛠️ How to use EssencePy
1. First of all, clone the project 😉
2. Edit `conf/env.conf` file and **setup** location for Python binaries in **PARENT_PYTHON_HOME** (for Linux) or **WIN_PARENT_PYTHON_HOME** (for Windows)
3. Fulfill `conf/requirements.txt` file to add your required Python libs to project
4. Launch the required script `project-init` (with correct extension for your system)

This setup and script will create a **Python virtual environment**, loads dependencies and enables Jupyter (which can be used in your IDE, converting notebook...etc ). 

### Main functions
```shell
# Converting a Jupyter notebook (example with a Windows OS)
# Notebook is called myNotebook.ipynb and stored in "notebooks" folder 
cd <APPLICATION_HOME>/scripts/powershell
.\notebook-converter.ps1 myNotebook.ipynb
```
```shell
# Launching my Python program (example with a Windows OS)
# Program is called myNotebook.py and stored in "app" folder 
cd <APPLICATION_HOME>/scripts/powershell>
.\app-start.ps1 myNotebook.py
```
## 💡 Some use cases
```md
> Tip: I want to use my own Python lib. 

Put your Python lib in "lib/init/" folder. 
Your lib should be loaded automatically after restarting Jupyter kernel or when launching Python program (for example)
```

```md
> Tip: I already have a Python program.

Put your Python program in "app" folder and launch it with the required script
```

```md
> Tip: VScode do not allow me to use my virtual env.

VScode could be a little bit ennoying and can not detect your fresh Python virtual env. 
You have to set "python.defaultInterpreterPath" with your Python virtual env in VScode settings
By default with value like: "rt/python/bin/python3"
```
### Currently working with
- Windows 10    | Powershell 5.1    | Python 3.12.8
- Centos 7      | Bash 4.2.46       | Python 3.9.21
- MacOS 15      | Zsh 5.9           | Python 3.12 (installed by brew)

---
Made with ❤️ for curious developers and pragmatic engineers.
