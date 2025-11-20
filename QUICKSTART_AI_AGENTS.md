# AI Agent Quickstart Guide

This guide provides a quick introduction to using the AI agent document drop-off system.

## What is This?

This system allows AI agents to save their journal entries and todo lists to the repository with **atomic commit operations** - similar to database transactions. When you drop off a document, it's both saved to the filesystem AND committed to git in a single operation that either fully succeeds or fully fails (with automatic rollback).

## Installation

No additional installation needed! The system uses standard Python libraries and git.

## Basic Usage

### 1. Drop Off a Journal Entry

```python
from ai_agent_utils import drop_off_journal

journal_content = """# Journal Entry - My Agent - 2025-01-15

## Session Information
- **Agent**: my_agent
- **Date**: 2025-01-15
- **Task**: Working on feature X

## Activities
- Implemented feature Y
- Fixed bug Z

## Next Steps
- Test feature Y
- Deploy to staging
"""

# This will save AND commit in one atomic operation
filepath = drop_off_journal(
    content=journal_content,
    agent_name="my_agent",
    commit_message="Add journal entry for feature X work"
)

print(f"Journal saved and committed at: {filepath}")
```

### 2. Drop Off a Todo List

```python
from ai_agent_utils import drop_off_todo

todo_content = """# Todo List - My Agent - 2025-01-15

## High Priority 🔴
- [ ] Complete feature X
- [ ] Write tests

## Medium Priority 🟡
- [ ] Update documentation
- [ ] Code review for PR #123

## Completed ✅
- [x] Set up development environment
- [x] Read project documentation
"""

filepath = drop_off_todo(
    content=todo_content,
    agent_name="my_agent",
    commit_message="Add todo list for current sprint"
)

print(f"Todo list saved and committed at: {filepath}")
```

### 3. Using Templates

Templates are available in `ai_agents/templates/`:
- `journal_template.md` - Comprehensive journal entry template
- `todo_template.md` - Structured todo list template

```python
from pathlib import Path

# Read the template
template = Path("ai_agents/templates/journal_template.md").read_text()

# Fill in your content (replace placeholders)
journal = template.replace("[Agent Name]", "my_agent")
journal = journal.replace("[Date]", "2025-01-15")
# ... fill in more details ...

# Drop it off
drop_off_journal(content=journal, agent_name="my_agent")
```

### 4. List Existing Documents

```python
from ai_agent_utils import list_agent_documents

# List all documents
all_docs = list_agent_documents()
print(f"Found {len(all_docs)} documents")

# List only journals
journals = list_agent_documents(doc_type="journal")
for journal in journals:
    print(f"  - {journal.name}")

# List only todos
todos = list_agent_documents(doc_type="todo")

# List documents from a specific agent
my_docs = list_agent_documents(agent_name="my_agent")
```

## Advanced Usage

### Custom Git Author

```python
drop_off_journal(
    content=journal_content,
    agent_name="my_agent",
    author_name="AI Assistant Bot",
    author_email="ai-bot@example.com"
)
```

### Manual Workflow (Save then Commit)

If you need more control, you can split the save and commit operations:

```python
from ai_agent_utils import (
    get_document_path,
    save_agent_document,
    commit_agent_document
)

# Step 1: Get the path
filepath = get_document_path("journal", "my_agent")

# Step 2: Save to filesystem
save_agent_document(content, filepath)

# Step 3: Commit to git
commit_agent_document(filepath, "My commit message")
```

⚠️ **Warning**: If you use the manual workflow, you need to handle errors yourself. The atomic `drop_off_document()` function is recommended.

### Using drop_off_document() Directly

```python
from ai_agent_utils import drop_off_document

# For journals
drop_off_document(
    content=journal_content,
    doc_type="journal",
    agent_name="my_agent"
)

# For todos
drop_off_document(
    content=todo_content,
    doc_type="todo",
    agent_name="my_agent"
)
```

## Configuration

The `.ai_agent_config` file contains configuration options:

```ini
# Default agent name (used when not specified)
DEFAULT_AGENT_NAME=ai_agent

# Base directory for agent documents
AGENT_DOCS_DIR=ai_agents

# Subdirectories
JOURNAL_DIR=journals
TODO_DIR=todos

# Timestamp format for filenames
TIMESTAMP_FORMAT=%Y%m%d_%H%M%S
```

## File Naming Convention

Documents are automatically named with this pattern:
- Journals: `journal_YYYYMMDD_HHMMSS_agentname.md`
- Todos: `todo_YYYYMMDD_HHMMSS_agentname.md`

Example: `journal_20250115_143022_copilot.md`

## Error Handling

The system includes automatic error handling and rollback:

```python
try:
    filepath = drop_off_journal(content, agent_name="my_agent")
    print(f"Success: {filepath}")
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Operation failed: {e}")
except FileExistsError as e:
    print(f"File already exists: {e}")
```

If an error occurs during the atomic operation:
1. The file is removed if it was created
2. Git changes are rolled back
3. An exception is raised with details

## Examples

Run the example script to see everything in action:

```bash
python3 example_agent_usage.py
```

This will demonstrate:
- ✅ Basic journal drop-off
- ✅ Basic todo drop-off
- ✅ Custom git author
- ✅ Manual workflow
- ✅ Listing documents

## Testing

Run the test suite:

```bash
python3 test_ai_agent_utils.py
```

## Directory Structure

```
ai_agents/
├── journals/                 # Your journal entries go here
│   └── journal_*.md
├── todos/                    # Your todo lists go here
│   └── todo_*.md
├── templates/                # Templates to help you get started
│   ├── journal_template.md
│   └── todo_template.md
└── README.md                 # Documentation
```

## Tips

1. **Use meaningful commit messages** - They appear in git history
2. **Include timestamps in your content** - Makes documents easier to find
3. **Use the templates** - They provide a good structure
4. **Use the atomic operations** - They're safer than manual save+commit
5. **Filter when listing** - Use `doc_type` or `agent_name` parameters

## Need Help?

- Read the full instructions: `.ai_agent_instructions.md`
- Check the module documentation: `ai_agent_utils.py`
- Run the examples: `python3 example_agent_usage.py`
- Run the tests: `python3 test_ai_agent_utils.py`

## Security Notes

- ⚠️ Never commit sensitive information (API keys, passwords, etc.)
- ✅ Review your document content before dropping it off
- ✅ Use appropriate commit messages for audit trails
- ✅ The system validates and sanitizes filenames automatically

Happy journaling! 📝
