# Coding Agent – Dynamic Frontend Generator

A Python-based AI frontend generator that converts a natural-language website request into a complete frontend.

The user describes the website they want, and the local Qwen model generates:

* `index.html`
* `styles.css`
* `script.js`

The generated files are saved automatically inside the `workspace/` directory.

## How It Works

```text
User Prompt
     ↓
Local Qwen Model
     ↓
HTML Generation
     ↓
CSS Generation
     ↓
JavaScript Generation
     ↓
workspace/
├── index.html
├── styles.css
└── script.js
```

Each request can produce a different website based on the user's description.

## Features

* Natural-language frontend generation
* Dynamic HTML generation
* Dynamic CSS generation
* Dynamic JavaScript generation
* Responsive desktop and mobile layouts
* Local Ollama model
* Qwen 3.5 4B support
* Workspace-restricted file operations
* Protected-file restrictions
* Path-traversal protection
* Safe command execution
* Automated HTML validation
* Pytest support

## Technologies

* Python
* Ollama
* Qwen 3.5 4B
* HTML5
* CSS3
* JavaScript
* pytest
* httpx

## Requirements

* Python 3.13+
* Ollama
* Qwen 3.5 4B model
* Windows, Linux, or macOS

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Make sure Ollama is running and the required model is available.

## Run

Start the coding agent:

```powershell
python main.py
```

Then enter a website request such as:

```text
Create a luxury Italian restaurant website called Bella Italia with a dark elegant design, menu, testimonials, reservations, contact information, and responsive mobile design.
```

The generated frontend will be written to:

```text
workspace/index.html
workspace/styles.css
workspace/script.js
```

Open `workspace/index.html` in a browser to view the generated website.

## Project Structure

```text
coding_agent/
│
├── agent/
│   ├── core.py
│   ├── llm.py
│   └── planner.py
│
├── tools/
│   ├── filesystem.py
│   ├── registry.py
│   ├── search.py
│   ├── shell.py
│   └── test_runner.py
│
├── workspace/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── tests/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Safety

The agent restricts filesystem operations to the workspace and protects sensitive files.

Command execution is restricted and does not use a shell interpreter.

The frontend generator does not create backend services, databases, authentication systems, or server-side applications.

## License

For educational and development use.
