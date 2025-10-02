# **Initial Project Setup**

This branch establishes the initial project structure for the **Agentic Patterns** project. It contains a minimal Python package under `src/`, with supporting folders for notebooks, utilities, tests, and GitHub workflows. At this stage, no agent logic or data integration is included — only the foundation for development.

## **Project Structure**

```
llm-agentic-patterns/
├── .github/
│   └── workflows/              # CI/CD workflows (e.g. release testing)
│       └── release_test.yml
├── img/                        # Project images and assets
├── notebooks/                  # Jupyter notebooks (exploration, experiments)
│   ├── 1_reflection.ipynb
│   ├── 2_agent_tools.ipynb
│   ├── 3_planning_agent.ipynb
│   └── 4_multi_agents.ipynb
├── src/
│   └── agentic_patterns/       # Core Python package
│       ├── 1_reflection/       # Reflection agent modules
│       ├── 2_agent_tools/      # Tools for agent reasoning
│       ├── 3_planning_agent/   # Planning agent logic
│       ├── 4_multi_agents/     # Multi-agent orchestration
│       └── utils/              # Utility functions
├── tests/                      # Unit tests
├── .env.example                # Example environment variables
├── .gitignore                  # Ignore rules for Git
├── .python-version             # Python version pin
├── pyproject.toml              # Project metadata & build configuration
├── README.md                   # Project documentation (you are here)
└── requirements.txt            # Python dependencies
```

> Note: Any `.venv/` folder is ignored and should not be committed.

## **Development Environment**

This project uses [uv](https://github.com/astral-sh/uv) for Python environment and dependency management.

### 1) Prerequisites

Install the following tools:

* [Python 3.11](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [uv – Python package and environment manager](https://github.com/astral-sh/uv)
* (Optional) [Docker Desktop](https://www.docker.com/products/docker-desktop) – for future containerisation

### 2) Clone the repository

```bash
git clone https://github.com/<your-username>/llm-agentic-patterns.git
cd llm-agentic-patterns
```

### 3) Create a virtual environment

```bash
uv venv --python python3.11
```

Activate it:

```bash
# On Linux / macOS
source .venv/bin/activate

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1

# On Windows (Git Bash)
source .venv/Scripts/activate
```

### 4) Install dependencies

```bash
uv pip install -r requirements.txt
```

Alternatively, run

```bash
uv sync
```

### 5) Deactivate when done

```bash
deactivate
```