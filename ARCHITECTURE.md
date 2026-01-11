# System Architecture

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Security Considerations](#security-considerations)
7. [Performance Optimizations](#performance-optimizations)

## Overview

The AI Coding Agent is built on a modular, component-based architecture designed for extensibility, safety, and maintainability. The system follows the principles of separation of concerns, with clear boundaries between the user interface, agent logic, tool execution, and LLM interaction.

### Core Design Principles

- **Modularity**: Each component has a single, well-defined responsibility
- **Extensibility**: Plugin-based architecture for tools and MCP servers
- **Safety**: Multiple layers of protection against unintended actions
- **Observability**: Rich event system for monitoring agent behavior
- **Resilience**: Error handling, retries, and graceful degradation

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     User Interface Layer                      │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │  CLI/TUI   │  │  Commands   │  │  Rich Rendering     │   │
│  │  (main.py) │  │  (/save,    │  │  (Diffs, Markdown)  │   │
│  │            │  │   /model)   │  │                     │   │
│  └─────┬──────┘  └──────┬──────┘  └──────────┬──────────┘   │
└────────┼─────────────────┼────────────────────┼──────────────┘
         │                 │                    │
         │                 ▼                    │
         │        ┌─────────────────┐          │
         │        │  Command Router │          │
         │        └────────┬─────────┘          │
         │                 │                    │
┌────────▼─────────────────▼────────────────────▼──────────────┐
│                      Agent Core Layer                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                  Agent (agent.py)                     │    │
│  │  ┌──────────────────────────────────────────────┐    │    │
│  │  │         Agentic Loop (Think-Act-Observe)     │    │    │
│  │  │  1. Analyze context and user request         │    │    │
│  │  │  2. Decide on tool(s) to use                │    │    │
│  │  │  3. Execute tool(s) via ToolRegistry        │    │    │
│  │  │  4. Observe results and update context      │    │    │
│  │  │  5. Repeat or respond to user              │    │    │
│  │  └──────────────────────────────────────────────┘    │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌──────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Session    │  │ Event Handler  │  │  Persistence   │   │
│  │  (session.py)│  │  (events.py)   │  │(persistence.py)│   │
│  │              │  │                │  │                │   │
│  │ • State      │  │ • AgentStart   │  │ • Save Session │   │
│  │ • Config     │  │ • ToolCall     │  │ • Checkpoints  │   │
│  │ • Tools      │  │ • ToolResult   │  │ • Resume       │   │
│  └──────────────┘  └────────────────┘  └────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼──────────┐
│  Context Layer  │  │   Tool Layer    │  │   LLM Layer      │
│                 │  │                 │  │                  │
│ ContextManager  │  │  ToolRegistry   │  │   LLMClient      │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌──────────────┐ │
│ │ Message     │ │  │ │ Tool        │ │  │ │ API Wrapper  │ │
│ │ History     │ │  │ │ Discovery   │ │  │ │ (OpenAI/     │ │
│ │             │ │  │ │             │ │  │ │  OpenRouter) │ │
│ └─────────────┘ │  │ └─────────────┘ │  │ └──────────────┘ │
│                 │  │                 │  │                  │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌──────────────┐ │
│ │ Pruning     │ │  │ │ Built-in    │ │  │ │ Streaming    │ │
│ │ (Remove old)│ │  │ │ Tools       │ │  │ │ Response     │ │
│ └─────────────┘ │  │ │ • File I/O  │ │  │ └──────────────┘ │
│                 │  │ │ • Shell     │ │  │                  │
│ ┌─────────────┐ │  │ │ • Web       │ │  │ ┌──────────────┐ │
│ │ Compaction  │ │  │ │ • Memory    │ │  │ │ Retry Logic  │ │
│ │ (Summarize) │ │  │ └─────────────┘ │  │ │ (Exponential │ │
│ └─────────────┘ │  │                 │  │ │  Backoff)    │ │
│                 │  │ ┌─────────────┐ │  │ └──────────────┘ │
│ ┌─────────────┐ │  │ │ MCP Client  │ │  │                  │
│ │Loop Detect  │ │  │ │ (External   │ │  └──────────────────┘
│ │(Break Cycles│ │  │ │  Servers)   │ │
│ └─────────────┘ │  │ └─────────────┘ │
│                 │  │                 │
└─────────────────┘  │ ┌─────────────┐ │
                     │ │ Custom      │ │
                     │ │ Tools       │ │
                     │ │ (User       │ │
                     │ │  Scripts)   │ │
                     │ └─────────────┘ │
                     └─────────────────┘
                              │
                     ┌────────▼─────────┐
                     │  Safety Layer    │
                     │                  │
                     │ ┌──────────────┐ │
                     │ │  Approval    │ │
                     │ │  System      │ │
                     │ │              │ │
                     │ │ • Policies   │ │
                     │ │ • User       │ │
                     │ │   Prompts    │ │
                     │ └──────────────┘ │
                     └──────────────────┘
```

## Component Details

### 1. CLI / TUI Layer

**Location**: `main.py`, `ui/tui.py`

**Responsibilities**:
- Parse command-line arguments and user input
- Route slash commands (`/save`, `/model`, `/exit`)
- Render rich text output (syntax highlighting, diffs, markdown)
- Handle user approvals for dangerous operations

**Key Technologies**:
- `click`: Command-line interface framework
- `rich`: Terminal rendering with colors, tables, and formatting

**Interaction Points**:
- Forwards user messages to Agent
- Receives events from Agent for display
- Accesses Session for state management

### 2. Agent Core Layer

#### Agent (`agent/agent.py`)

**Responsibilities**:
- Implements the agentic loop: Think → Act → Observe → Repeat
- Decides which tools to call based on context
- Manages conversation flow
- Handles errors and retries

**Key Methods**:
```python
async def run(self, user_message: str) -> str:
    """Main entry point for processing user requests"""
    
async def _agentic_loop(self) -> str:
    """Core loop: get LLM response, execute tools, repeat"""
    
async def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
    """Execute a single tool with safety checks"""
```

**State Machine**:
```
[Idle] → [Thinking] → [Tool Execution] → [Observing] → [Thinking]
                                    ↓
                              [Complete] → [Response]
```

#### Session (`agent/session.py`)

**Responsibilities**:
- Container for agent state
- Holds references to Config, ToolRegistry, ContextManager
- Manages session ID and metadata

**Data Structure**:
```python
class Session:
    id: str
    config: Config
    context: ContextManager
    tools: ToolRegistry
    created_at: datetime
    metadata: dict
```

#### Events (`agent/events.py`)

**Responsibilities**:
- Define event types for observability
- Enable decoupled monitoring and logging

**Event Types**:
- `AgentStart`: Agent begins processing
- `ToolCall`: Tool is about to be executed
- `ToolResult`: Tool execution completed
- `LLMResponse`: LLM generated a response
- `ApprovalRequired`: User approval needed
- `Error`: Error occurred

### 3. Context Layer

#### ContextManager (`context/manager.py`)

**Responsibilities**:
- Store and retrieve conversation history
- Enforce token limits
- Trigger pruning and compaction

**Key Methods**:
```python
def add_message(self, role: str, content: str):
    """Add a message to history"""
    
def get_messages(self) -> List[Message]:
    """Retrieve messages for LLM"""
    
def prune_if_needed(self):
    """Remove old tool outputs if approaching limit"""
    
async def compact_if_needed(self):
    """Summarize old messages to save space"""
```

**Token Management Strategy**:
1. Count tokens in current history
2. If > 80% of max: trigger pruning (remove old tool results)
3. If still > 90%: trigger compaction (summarize chunks)
4. Keep most recent 10 messages intact

#### Compaction (`context/compaction.py`)

**Responsibilities**:
- Summarize conversation chunks using LLM
- Preserve important context while reducing tokens

**Algorithm**:
```
1. Identify messages eligible for compaction (older than N messages)
2. Group into chunks of ~10k tokens
3. Send each chunk to LLM with summarization prompt
4. Replace original messages with summary
```

#### Loop Detector (`context/loop_detector.py`)

**Responsibilities**:
- Detect repetitive agent behavior
- Break infinite loops

**Detection Methods**:
- **Exact match**: Same tool called with identical args N times
- **Semantic similarity**: Embedding-based detection of similar actions
- **Cycle detection**: Graph-based cycle detection in tool call sequence

### 4. Tool Layer

#### ToolRegistry (`tools/registry.py`)

**Responsibilities**:
- Central registry of all available tools
- Tool lookup and execution
- Schema generation for LLM

**Key Methods**:
```python
def register(self, tool: Tool):
    """Add a tool to registry"""
    
def get_tool(self, name: str) -> Tool:
    """Retrieve tool by name"""
    
def get_schemas(self) -> List[dict]:
    """Get OpenAI function schemas for all tools"""
    
async def execute(self, name: str, args: dict) -> str:
    """Execute a tool by name"""
```

#### Built-in Tools (`tools/builtin/`)

**File System Tools**:
- `read_file`: Read file contents
- `write_file`: Create/overwrite file with diff preview
- `edit_file`: Apply patch to existing file
- `list_dir`: List directory contents
- `glob`: Find files matching pattern

**System Tools**:
- `shell`: Execute shell command with timeout
- `grep`: Search files for text patterns

**Web Tools**:
- `web_search`: Search using DuckDuckGo
- `web_fetch`: Scrape webpage content

**Memory Tools**:
- `memory`: Store/retrieve user preferences
- `todos`: Task planning and tracking

#### MCP Client (`tools/mcp/`)

**Responsibilities**:
- Connect to external Model Context Protocol servers
- Translate MCP tools to internal Tool format
- Manage server lifecycle

**Supported Servers**:
- GitHub (issues, PRs, repositories)
- Google Drive (files, documents)
- Databases (SQL queries)
- Custom user-defined servers

#### Tool Discovery (`tools/discovery.py`)

**Responsibilities**:
- Scan `tools/` directory for custom Python scripts
- Dynamically load and register user tools
- Validate tool implementations

**Custom Tool Format**:
```python
# tools/my_tool.py
from tools.base import Tool

class MyTool(Tool):
    name = "my_tool"
    description = "Does something useful"
    
    async def execute(self, **kwargs) -> str:
        # Implementation
        return result
```

### 5. LLM Layer

#### LLMClient (`client/llmclient.py`)

**Responsibilities**:
- Abstract OpenAI/OpenRouter API
- Handle streaming responses
- Implement retry logic with exponential backoff
- Standardize tool calling format

**Key Methods**:
```python
async def complete(
    self,
    messages: List[dict],
    tools: List[dict] = None,
    stream: bool = True
) -> AsyncIterator[str]:
    """Get LLM completion with optional tool calling"""
    
async def _retry_with_backoff(self, request_fn):
    """Retry failed requests with exponential backoff"""
```

**Error Handling**:
- Rate limit errors: Wait and retry (max 3 times)
- Network errors: Exponential backoff
- Invalid tool calls: Return error to agent for correction

### 6. Safety Layer

#### Approval System (`safety/approval.py`)

**Responsibilities**:
- Intercept dangerous tool calls
- Request user permission based on policy
- Track approval history

**Policies**:
- `strict`: Ask before ANY write or shell execution
- `on-request`: Ask before writes, allow safe reads
- `auto-edit`: Auto-approve edits to existing files
- `yolo`: Auto-approve everything (dangerous!)

**Approval Flow**:
```
Tool Call → Check Policy → [Requires Approval?]
                                    ↓ Yes
                          Prompt User → [Approved?]
                                    ↓ Yes        ↓ No
                              Execute Tool    Reject
                                    ↓ No
                              Execute Tool
```

**Risk Classification**:
- **High Risk**: Shell commands, file deletion, network requests
- **Medium Risk**: File writes, directory creation
- **Low Risk**: File reads, directory listing

## Data Flow

### Request Flow

```
User Input
    ↓
CLI Parser
    ↓
[Slash Command?] → Yes → Command Router → Session State Update
    ↓ No
Agent.run(message)
    ↓
ContextManager.add_message(user, message)
    ↓
Agent._agentic_loop()
    ↓
ContextManager.get_messages() → LLMClient.complete()
    ↓
[Tool Call?] → No → Return response to user
    ↓ Yes
ToolRegistry.execute()
    ↓
[Approval Required?] → Yes → Prompt User → [Approved?] → No → Reject
    ↓ No                                        ↓ Yes
Tool.execute()
    ↓
ToolResult
    ↓
ContextManager.add_message(tool_result)
    ↓
[Max Iterations?] → Yes → Return to user
    ↓ No
Loop back to LLMClient.complete()
```

### Context Flow

```
New Message
    ↓
ContextManager.add_message()
    ↓
Count tokens
    ↓
[> 80% of max?] → Yes → Prune old tool results
    ↓ No
[> 90% of max?] → Yes → Compact message chunks
    ↓ No
Store message
```

### Session Persistence Flow

```
/save command
    ↓
Session.to_dict()
    ↓
{
  id, created_at, config,
  messages: [...],
  tool_history: [...],
  metadata: {...}
}
    ↓
JSON.dump() → session_TIMESTAMP.json
    ↓
Success message to user

/load command
    ↓
JSON.load(filename)
    ↓
Session.from_dict(data)
    ↓
Restore ContextManager, Config, Tools
    ↓
Resume conversation
```

## Design Patterns

### 1. Strategy Pattern
**Context Management**: Different strategies for pruning and compaction can be swapped

### 2. Observer Pattern
**Event System**: Components emit events that UI and loggers observe

### 3. Registry Pattern
**Tool Management**: Central registry for tool lookup and execution

### 4. Template Method Pattern
**Tool Base Class**: Abstract base defines interface, subclasses implement specifics

### 5. Adapter Pattern
**MCP Integration**: MCP tools adapted to internal Tool interface

### 6. Chain of Responsibility
**Approval System**: Policies form a chain that determines approval requirements

## Security Considerations

### 1. Input Validation
- All file paths validated and sandboxed to workspace
- Shell commands parsed for dangerous patterns
- Tool arguments validated against schemas

### 2. Permission System
- Granular control over tool capabilities
- User approval for destructive operations
- Audit log of all tool executions

### 3. Resource Limits
- Shell command timeouts (default 30s)
- File size limits for reads/writes
- Maximum context window enforcement

### 4. Isolation
- Tools executed in subprocess when possible
- Network requests use safe libraries (requests with timeout)
- No arbitrary code execution from LLM responses

### 5. Data Privacy
- API keys never logged
- Session data stored locally
- Optional encryption for saved sessions

## Performance Optimizations

### 1. Token Efficiency
- Aggressive pruning of stale tool outputs
- Smart compaction preserving important context
- Streaming responses for faster perceived performance

### 2. Caching
- Tool schemas cached after first generation
- File content cached during session
- Embedding cache for loop detection

### 3. Async I/O
- Non-blocking LLM API calls
- Parallel tool execution when independent
- Async file operations

### 4. Lazy Loading
- Tools loaded on-demand
- MCP servers connected only when needed
- Configuration parsed once at startup

### 5. Memory Management
- Context history bounded by tokens, not messages
- Old checkpoints auto-pruned
- Periodic garbage collection hints

## Future Enhancements

### Multi-Agent System
- Spawn specialized sub-agents for subtasks
- Agent communication protocol
- Hierarchical task delegation

### Enhanced Observability
- Structured logging to files
- Prometheus metrics export
- Trace collection for debugging

### Advanced Context Management
- RAG-based long-term memory
- Automatic codebase indexing
- Semantic search over history

### Improved Safety
- Sandboxed execution environment (Docker)
- Static analysis of proposed code changes
- Automatic rollback on detected issues

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Maintainer**: AI Coding Agent Team