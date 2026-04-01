# Claude Code — Guide for Non-Programmers (Advanced)

This guide covers more technical concepts. Read the [basics guide](../1-basics/1-basics.md) first.

> **Disclaimer:** I have no business relationship with any of the tools or services mentioned in this guide. These are personal recommendations based on my experience. Use them at your own discretion — I take no responsibility for any outcomes.

---

## Processes

Your computer runs many programs at the same time — each one is called a **process**. Your web browser, Microsoft Word, and Claude Code are all separate processes.

Every process has:
- **Executable file** — the program file itself (e.g., `chrome.exe`).
- **Working directory** — the folder the process operates in by default, like the folder you have open in File Explorer.
- **Command line** — the command used to start it, including any options (e.g., `code my-project/`).
- **Environment variables** — system settings the process can read, like your username or where to find installed programs.

### Example

When you open VS Code, your computer starts a process:
- **Executable:** `C:\Program Files\Microsoft VS Code\Code.exe` (on Windows)
- **Working directory:** the folder you opened in VS Code
- **Command line:** `code my-project/` (if you opened it from the terminal)
- **Environment variables:** things like `PATH` (where your computer looks for programs)

You can see all running processes in:
- **Windows:** Task Manager (`Ctrl+Shift+Esc`)
- **Mac:** Activity Monitor
- **Linux:** System Monitor or `htop` in the terminal

---

## Command Line (Terminal)

### What is it?

The command line (also called terminal or shell) is a text-based way to talk to your computer. Instead of clicking icons, you type commands. The terminal in VS Code (`` Ctrl+` ``) is the same thing.

There are different terminal programs depending on your operating system:

- **Bash** (Mac / Linux) — the default terminal on Mac and most Linux systems. Also available on Windows via WSL (Windows Subsystem for Linux).
- **CMD** (Windows) — the classic Windows command prompt. Basic and limited, but comes pre-installed.
- **PowerShell** (Windows) — a more powerful Windows terminal. Comes pre-installed on modern Windows. Uses different command names than Bash.

> Most online tutorials and tools (including Claude Code) assume **Bash**. If you're on Windows, consider installing [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to get a Bash terminal, or use PowerShell which supports many similar commands.

### Example

Here's what using the command line looks like:

```bash
$ pwd
/home/user/my-project

$ ls
index.html  style.css  script.js  images/

$ cd images
$ ls
logo.png  photo.jpg

$ cd ..
$ python script.py
Hello, world!
```

The `$` sign is the **prompt** — it means the terminal is ready for your input. You don't type it yourself.

### Useful commands

| Action | Bash (Mac/Linux) | CMD (Windows) | PowerShell (Windows) |
|---|---|---|---|
| Where am I? | `pwd` | `cd` | `pwd` |
| List files | `ls` | `dir` | `ls` |
| Go into a folder | `cd folder` | `cd folder` | `cd folder` |
| Go up one folder | `cd ..` | `cd ..` | `cd ..` |
| Show file contents | `cat file.txt` | `type file.txt` | `cat file.txt` |
| Copy a file | `cp file.txt copy.txt` | `copy file.txt copy.txt` | `cp file.txt copy.txt` |
| Rename / move | `mv old.txt new.txt` | `ren old.txt new.txt` | `mv old.txt new.txt` |
| Delete a file | `rm file.txt` | `del file.txt` | `rm file.txt` |
| Create a folder | `mkdir new-folder` | `mkdir new-folder` | `mkdir new-folder` |
| Run Python | `python script.py` | `python script.py` | `python script.py` |
| Open in VS Code | `code file.txt` | `code file.txt` | `code file.txt` |

> **Careful:** `rm` / `del` deletes permanently — there is no recycle bin!

### Tips

- Press **Tab** to autocomplete file and folder names (works in all three)
- Press **Up arrow** to recall previous commands
- Use `Ctrl+C` to stop a running command

---

## Python

### What is it?

Python is a beginner-friendly programming language used for scripts, data processing, automation, and much more. In the basics guide you learned that Claude uses it behind the scenes — here you'll learn how it works.

### How to run

**From the terminal:**

```bash
python my_script.py
```

**From VS Code:**

1. Open a `.py` file
2. Click the play button (top right) or press `Ctrl+F5`
3. Output appears in the terminal panel

### Modules & pip

Python has a huge collection of **modules** (also called packages or libraries) — ready-made code that other people wrote so you don't have to. For example, `pandas` for working with spreadsheets, `requests` for downloading web pages, or `markdown_pdf` for converting Markdown to PDF.

To install modules, use **pip** (Python's package manager) in the terminal:

```bash
pip install pandas              # install a module
pip install pandas requests     # install multiple at once
pip install pandas==2.1.0       # install a specific version
pip list                        # see what's installed
pip uninstall pandas            # remove a module
```

Then use it in your Python code:

```python
import pandas
```

> If a Python script fails with `ModuleNotFoundError: No module named 'xxx'`, it means you need to `pip install xxx` first.

### Tips

- Make sure Python is installed: run `python --version` in the terminal
- Install the Python VS Code extension for better support

> **Further reading:** [Python for Beginners (official tutorial)](https://docs.python.org/3/tutorial/)

---

## Git

### What is it?

Git is a **version control system** — it tracks every change you make to your files over time. Think of it as an "undo history" for your entire project, with the ability to create branches (parallel versions) and collaborate with others.

Git is the standard tool for this — almost every software project uses it. **GitHub** and **GitLab** are popular websites that host Git projects online, making them accessible from anywhere.

### Key concepts

- **Repository (repo)** — a project folder tracked by Git
- **Commit** — a saved snapshot of your changes, with a message describing what you did
- **Branch** — a parallel version of your project (e.g., to try a new feature without affecting the main version)
- **Remote** — a copy of your repo on a server (like GitHub)
- **Pull / Push** — download changes from / upload changes to the remote

### Useful commands

| Action | Command |
|---|---|
| Start tracking a folder | `git init` |
| See what changed | `git status` |
| See the actual changes | `git diff` |
| Stage files for commit | `git add file.txt` (or `git add .` for all) |
| Save a snapshot | `git commit -m "describe what you did"` |
| See commit history | `git log --oneline` |
| Download a project from GitHub | `git clone https://github.com/user/repo.git` |
| Get latest changes from remote | `git pull` |
| Upload your changes | `git push` |

### Display your work publicly with README.md

GitLab and GitHub automatically display any file called `README.md` as a formatted page when someone visits your project. Write a Markdown document, push it, and it's instantly visible from any computer or phone — like a small website, with no extra setup.

### Using Git from VS Code

You don't need to memorize any commands — VS Code has a built-in Git interface that makes it very easy:

1. Click the **Source Control** icon in the left sidebar (or `Ctrl+Shift+G`)
2. You'll see all your changed files listed
3. Click **+** next to a file to stage it (prepare it for saving)
4. Type a short message describing what you changed
5. Click the **checkmark** to commit (save the snapshot)
6. Click **...** → **Push** to upload your changes

This is a very easy way to manage and backup your files.

### Tips

- Claude Code can handle Git for you — just say "commit my changes" or use `/commit`
- Don't worry about memorizing commands — Claude or VS Code's interface can handle it for you
- If something goes wrong with Git, ask Claude to help fix it

> **Further reading:** [Git Handbook (GitHub)](https://guides.github.com/introduction/git-handbook/)

---

## Claude Code — Advanced

### Skills (slash commands)

Skills are built-in shortcuts you can type in the Claude Code chat. Type `/` to see the full list. Here are some useful ones:

| Command | What it does |
|---|---|
| `/help` | Show help and available commands |
| `/commit` | Look at your changes and create a Git commit with a descriptive message |
| `/review-pr` | Review a pull request — Claude reads the changes and gives feedback |
| `/simplify` | Review your changed code for quality and fix any issues |

You can also create **custom skills** — Markdown files (`.md`) with instructions for Claude. For example, a skill that tells Claude how to format documents in your team's style, or how to prepare a specific type of report. Custom skills live in your project folder and can be shared with your team.

### Permissions — more detail

As covered in the basics guide, Claude asks permission before performing actions. Here's a deeper look:

**Permission types:**

| Action type | Examples |
|---|---|
| **Read files** | Opening and reading files in your project — usually allowed automatically |
| **Edit files** | Modifying, creating, or deleting files |
| **Run commands** | Running terminal commands like `python script.py`, `pip install`, `git push` |

**When Claude asks, you have these options:**

- **Yes** — allow this one action
- **Yes, don't ask again** — allow this type of action for the current project folder. Claude remembers this so it won't ask again for similar actions in this project, but will still ask in other projects.
- **No** — deny the action

**Recommended approach:**

- **Beginners:** approve each action individually. This way you see exactly what Claude does and learn what's happening.
- **Once comfortable:** use "Yes, don't ask again" for actions you trust (like editing files in your project). This speeds up your workflow.
- **Be careful with:** commands that install software (`pip install`), delete files (`rm`), or push to remote servers (`git push`). It's good practice to review these even when you're experienced.

**CLAUDE.md for project rules:**

As mentioned in the basics guide, you can create a `CLAUDE.md` file in your project to give Claude standing instructions. This is also useful for permissions — for example, you can tell Claude to always ask before deleting files, or to never run certain commands.
