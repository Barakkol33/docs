# Claude Code — Guide & Tips for Non-Programmers

A practical guide to getting things done with Claude Code, even if you've never written code before. Each skill below builds on the previous ones.
Fun fact: Created by Claude Code.

---

## 0. Learning

This guide introduces you to some basic terms and technologies.

You want to know more? - Google it or ask your favorite LLM :)

Today you can learn and do anything - you are limited only by your imagination (and time).

---

## 1. VS Code

### What is it?

VS Code (Visual Studio Code) is a free text editor by Microsoft. Think of it as a supercharged Notepad — it can open any file, color-code different languages, and run tools like Claude Code inside it.

### Installation

Download from [code.visualstudio.com](https://code.visualstudio.com/)

### Key concepts

- **File Explorer** (left sidebar) — browse and open files in your project folder
- **Editor** (center) — where you view and edit files
- **Terminal** (bottom panel) — a command line built into VS Code
- **Extensions** (left sidebar, block icon) — add-ons (plugins) that give VS Code new abilities (like Claude Code, Python support, etc.)
- **Command Palette** — press `Ctrl+Shift+P` to search for any action

### Installing extensions

Extensions add features to VS Code — language support, themes, tools, and more. To install:

1. Click the **Extensions** icon in the left sidebar (or `Ctrl+Shift+X`)
2. Search for what you need
3. Click **Install**

**How to pick safe extensions:**

- **Prefer verified publishers** — look for the blue checkmark next to the publisher name. These are verified by Microsoft.
- **If not verified** — check the download count and ratings. Popular extensions (millions of downloads, 4+ stars) are generally safe.
- **Be careful** with unknown extensions that have few downloads — they could contain bugs or even malicious code. When in doubt, search online for recommendations.

### Essential shortcuts

| Action | Shortcut |
|---|---|
| Open Command Palette | `Ctrl+Shift+P` |
| Open file by name | `Ctrl+P` |
| Toggle terminal | `` Ctrl+` `` |
| Toggle sidebar | `Ctrl+B` |
| Save file | `Ctrl+S` |
| Find in file | `Ctrl+F` |
| Find in all files | `Ctrl+Shift+F` |
| Open Simple Browser (sidebar preview) | `Ctrl+Shift+P` → type "Simple Browser" |

> **Further reading:** [VS Code Getting Started](https://code.visualstudio.com/docs/getstarted/introvideos)

---

## 2. Command Line (Terminal)

### What is it?

The command line (also called terminal or shell) is a text-based way to talk to your computer. Instead of clicking icons, you type commands. The terminal in VS Code (`` Ctrl+` ``) is the same thing.

There are different terminal programs depending on your operating system:

- **Bash** (Mac / Linux) — the default terminal on Mac and most Linux systems. Also available on Windows via WSL (Windows Subsystem for Linux).
- **CMD** (Windows) — the classic Windows command prompt. Basic and limited, but comes pre-installed.
- **PowerShell** (Windows) — a more powerful Windows terminal. Comes pre-installed on modern Windows. Uses different command names than Bash.

> Most online tutorials and tools (including Claude Code) assume **Bash**. If you're on Windows, consider installing [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to get a Bash terminal, or use PowerShell which supports many similar commands.

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

## 3. Markdown

### What is it?

Markdown is a simple way to format text using plain characters. Files end in `.md`. This guide is written in Markdown.

### Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3

**bold text**
*italic text*

- bullet point
- another bullet

1. numbered list
2. second item

[link text](https://example.com)

> blockquote

`inline code`
```

### How to preview

- In VS Code: open a `.md` file → `Ctrl+Shift+V` to preview, or `Ctrl+K V` to preview side-by-side
- You can ask Claude to create Markdown files and preview them directly in VS Code

> **Further reading:** [Markdown Guide](https://www.markdownguide.org/basic-syntax/)

---

### Creating PDF from markdown files

There is a python script in this directory that creates PDF from markdown.

```
pip install markdown_pdf
python markdown_to_pdf.py --help
python markdown_to_pdf.py -o out.pdf --title "Claude code" claude-code-guide.md
```

## 4. Python

### What is it?

Python is a beginner-friendly programming language. You can use it for scripts, data processing, automation, and much more.

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

## 5. HTML, JavaScript & CSS

### What are they?

These three languages work together to create websites:

- **HTML** — the structure and content (headings, paragraphs, buttons)
- **CSS** — the styling (colors, fonts, layout)
- **JavaScript (JS)** — the behavior (what happens when you click things)

A basic website is just an `.html` file that can reference `.css` and `.js` files.

### How to open

1. Double-click any `.html` file — it opens in your default browser (Chrome, Firefox, etc.)
2. Or right-click the file → "Open with" → choose a browser
3. In VS Code, use the **Simple Browser** to preview without leaving the editor:
   `Ctrl+Shift+P` → type "Simple Browser: Show" → paste the file path

### Basic structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        h1 { color: darkblue; }
    </style>
</head>
<body>
    <h1>Hello!</h1>
    <p>This is a paragraph.</p>
    <button onclick="alert('clicked!')">Click me</button>
</body>
</html>
```

Save this as a `.html` file and open in a browser to see it work.

> **Further reading:** [MDN Web Docs — Getting Started](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web)

---

## 6. Claude Code

### What is it?

Claude Code is an AI assistant that lives inside VS Code (or the terminal). It can read, create, and edit files on your computer. You talk to it in plain language and it does the work.

### Where can it be used?

- Any terminal - run `claude`
- VSCode - Install plugin, `CTRL+SHIFT+P -> "Claude code: Open in Side Bar"`

### What can it do?

- **Edit files** — "change the heading color to red" or "fix the typo in paragraph 3"
- **Create files** — "create a Python script that renames all files in a folder" or "make a website with a contact form"
- **Explain code** — "what does this file do?" or "explain line 15"
- **Run commands** — it can run terminal commands on your behalf

### Modes

| Mode | What it can do | When to use |
|---|---|---|
| **Plan mode** | Reads files, thinks, makes a plan | When you want to review before changes |
| **Normal mode** | Reads and edits files | Day-to-day work |

### Permissions

Claude asks for permission before doing potentially risky things (editing files, running commands). You can:

- **Allow once** — approve a single action
- **Allow always** — trust this type of action going forward
- Review what it wants to do before approving

### Skills (slash commands)

Type `/` in the Claude Code chat to see available commands:

| Command | What it does |
|---|---|
| `/help` | Show help and available commands |
| `/commit` | Create a git commit with a good message |
| `/review-pr` | Review a pull request |

### Things to try

**Create Markdown documents:**
> "Create a markdown file called meeting-notes.md with sections for date, attendees, agenda, and action items"

**Create Python scripts:**
> "Write a Python script that reads a CSV file and prints the total of the 'amount' column"

**Build websites:**
> "Create a simple website with a dark theme that shows a list of my favorite books. Make it look nice."

**Create presentations:**
> Have text material you want to present? Ask Claude to turn it into a web-based slideshow. For example: "Create an HTML presentation from this text" — then open the `.html` file in your browser. It's a quick way to make good-looking slides without PowerPoint.

**Preview in VS Code sidebar:**
> After creating an HTML file, open it in VS Code's Simple Browser: `Ctrl+Shift+P` → "Simple Browser: Show" → enter the file path

**Edit existing files:**
> "In index.html, change the background color to light gray and make the font bigger"

### Tips

- Be specific about what you want — "make the title blue and centered" works better than "make it look better"
- You can select text in VS Code and ask Claude about just that selection
- If Claude's change isn't what you wanted, just tell it — "undo that" or "no, I meant the other heading"
- Claude can work with any file type — text, code, config files, etc.
