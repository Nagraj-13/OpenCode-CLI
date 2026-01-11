# AI Coding Agent

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A sophisticated, terminal-based AI coding assistant that acts as an autonomous software engineer. Built in Python, this agent can explore codebases, edit files, execute shell commands, search the web, and manage its own memory and context intelligently.

## 🌟 Overview

This project implements a powerful AI coding agent similar to Claude Code or Cursor, designed to autonomously perform complex software engineering tasks. The agent features an advanced agentic loop that thinks, plans, executes tools, and iterates to solve problems with minimal human intervention.

## 🚀 Key Features

### 🤖 Autonomous Agentic Loop
- **Think → Tool Call → Observe → Repeat**: Intelligent decision-making cycle
- Plans multi-step solutions to complex coding tasks
- Self-corrects based on execution results

### 📁 File System Operations
- **Read/Write Files**: Safe file manipulation with automatic diffs
- **Edit Files**: Precise patch-based editing
- **Search & Glob**: Find files using patterns or grep-like search
- **Directory Listing**: Explore project structure

### 💻 Shell Execution
- Execute system commands with configurable timeouts
- Safety checks and approval mechanisms
- Real-time output streaming

### 🌐 Web Capabilities
- **Web Search**: DuckDuckGo integration for current information
- **Web Fetch**: Scrape and retrieve documentation
- Research capabilities for up-to-date knowledge

### 🧠 Context Management
- **Smart Pruning**: Automatically removes stale tool outputs to optimize token usage
- **Compaction**: Summarizes long conversation histories
- **Efficient Memory**: Maintains context over extended sessions

### 🛡️ Safety First
- **Human-in-the-Loop**: Configurable approval policies for dangerous operations
- **Loop Detection**: Identifies and breaks repetitive agent behaviors
- **Granular Permissions**: Control what the agent can do (read-only, ask-first, auto-approve)

### 🔌 Extensibility
- **MCP Support**: Connect to any Model Context Protocol server (GitHub, Google Drive, databases)
- **Custom Tools**: Drop Python scripts into a folder to extend functionality
- **Plugin Architecture**: Easy tool registration and discovery

### 💾 Session Management
- **Save/Resume**: Persist conversation state across sessions
- **Checkpoints**: Create named snapshots to roll back to
- **Export**: Save conversations and tool executions

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key or OpenRouter API key
- Terminal with UTF-8 support (for rich text rendering)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nagraj-13/OpenCode-CLI.git
cd ai-agent
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate #On Windows
# on MAC: source venv/bin/activate  
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the project root:
```bash
OPEN_ROUTERAPI_KEY=your_openrouter_or_openai_key
OPEN_ROUTER_API_BASE_URL=https://openrouter.ai/api/v1  # Optional, defaults to OpenAI
OPEN_ROUTER_LLM_MODEL=anthropic/claude-sonnet-4-20250514
```



### 5. (Optional) Configure Settings
Edit `config.toml` to customize:
- Default model
- Context window limits
- Approval policies
- Tool settings
- MCP server connections

## 💻 Usage

### Start the Agent
```bash
python main.py
```

### Interactive Commands

Once running, you can use these slash commands:

| Command | Description |
|---------|-------------|
| `/help` | Show available commands and their usage |
| `/save [filename]` | Save the current session state |
| `/load <filename>` | Resume a previously saved session |
| `/checkpoint <name>` | Create a named checkpoint to roll back to |
| `/restore <name>` | Restore to a previous checkpoint |
| `/clear` | Clear conversation history |
| `/model <name>` | Switch LLM model (e.g., `claude-3-opus`) |
| `/approval <policy>` | Change safety policy (`strict`, `on-request`, `yolo`) |
| `/context` | Show current context usage and statistics |
| `/mcp` | List connected MCP servers |
| `/tools` | List all available tools |
| `/exit` | Quit the application |

### Example Session

```
You: Create a Python script that fetches data from an API and saves it to a CSV file

[Agent thinks and plans]
[Agent calls read_file to check if similar code exists]
[Agent calls write_file to create api_fetcher.py]
[Shows diff for review]

Approve write to api_fetcher.py? (y/n): y

[Agent writes file]
[Agent calls shell to test the script]

You: Add error handling for network timeouts

[Agent reads the file]
[Agent calls edit_file with specific changes]
[Shows precise diff]
...
```

### Approval Policies

Control agent autonomy with different safety levels:

- **`strict`**: Ask before ANY file write or shell execution
- **`on-request`**: Ask before writes, allow safe reads automatically
- **`auto-edit`**: Auto-approve file edits, ask for new files
- **`yolo`**: Auto-approve everything (use with caution!)

Change policy anytime:
```
/approval strict
```

## 🏗️ Architecture

The system follows a modular, component-based architecture:

```
┌─────────────────────────────────────────────┐
│          CLI/TUI Layer (main.py)            │
│  User Input → Command Processing → Display  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Core Agent Logic (agent/)           │
│  Agentic Loop → Tool Orchestration          │
│  Session Management → Event Handling        │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
┌───────▼──┐ ┌────▼────┐ ┌─▼────────┐
│ Context  │ │  Tools  │ │   LLM    │
│ Manager  │ │Registry │ │  Client  │
│          │ │         │ │          │
│ Pruning  │ │  MCP    │ │Streaming │
│Compaction│ │ Custom  │ │ Retries  │
└──────────┘ └─────────┘ └──────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## 📂 Project Structure

```
ai-agent/
├── agent/                  # Core agent logic
│   ├── agent.py           # Main agentic loop
│   ├── session.py         # Session state management
│   ├── events.py          # Event types and handling
│   └── persistence.py     # Save/load functionality
├── client/                # LLM integration
│   ├── llmclient.py      # API wrapper
│   └── response.py       # Response parsing
├── config/                # Configuration
│   ├── config.py         # Pydantic models
│   └── loader.py         # Config file loading
├── context/               # Context management
│   ├── manager.py        # Message handling
│   ├── compaction.py     # History summarization
│   └── loop_detector.py  # Cycle detection
├── safety/                # Safety mechanisms
│   └── approval.py       # Human-in-the-loop
├── tools/                 # Tool system
│   ├── base.py           # Abstract base class
│   ├── registry.py       # Tool registration
│   ├── discovery.py      # Custom tool loader
│   ├── mcp/              # MCP client
│   └── builtin/          # Core tools
├── ui/                    # User interface
│   └── tui.py            # Rich TUI rendering
├── utils/                 # Utilities
├── main.py               # Entry point
├── config.toml           # User configuration
└── requirements.txt      # Dependencies
```

## 🔧 Configuration

### config.toml Example

```toml
[llm]
model = "anthropic/claude-sonnet-4-20250514"
base_url = "https://openrouter.ai/api/v1"
max_tokens = 4096
temperature = 0.7

[context]
max_tokens = 128000
prune_threshold = 100000
enable_compaction = true

[safety]
approval_policy = "on-request"
allow_shell = true
allow_web = true
shell_timeout = 30

[mcp]
servers = ["github", "filesystem"]

[session]
auto_save = true
checkpoint_interval = 10
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Lint
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## 🙏 Acknowledgments

- Inspired by Claude Code, Cursor, and other AI coding assistants
- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [Anthropic](https://www.anthropic.com/) and [OpenAI](https://openai.com/) models
- MCP integration based on [Model Context Protocol](https://modelcontextprotocol.io/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-agent/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/ai-agent/wiki)

## 🗺️ Roadmap

- [ ] Multi-agent collaboration (spawn sub-agents for specialized tasks)
- [ ] VSCode extension integration
- [ ] Built-in code review and testing capabilities
- [ ] Enhanced debugging tools
- [ ] Cloud session synchronization
- [ ] Voice command support

---

**Built with ❤️ by the AI Coding Agent Team**