# AI Agents Document Storage

This directory contains journal entries and todo lists dropped off by AI agents.

## Directory Structure

```
ai_agents/
├── journals/         # Journal entries from AI agents
│   └── journal_YYYYMMDD_HHMMSS_agentname.md
├── todos/           # Todo lists from AI agents
│   └── todo_YYYYMMDD_HHMMSS_agentname.md
├── templates/       # Document templates for AI agents
└── README.md        # This file
```

## Purpose

This system allows AI agents to:
- Keep track of their work sessions through journal entries
- Maintain todo lists for ongoing and future tasks
- Commit their documents atomically to the repository

## For AI Agents

If you're an AI agent looking to drop off documents, please refer to the `.ai_agent_instructions.md` file in the repository root for detailed instructions.

## For Developers

The `ai_agent_utils.py` module provides the following key functions:

- `drop_off_document()`: Complete transaction to save and commit a document
- `drop_off_journal()`: Convenience function for journal entries
- `drop_off_todo()`: Convenience function for todo lists
- `save_agent_document()`: Save document to filesystem only
- `commit_agent_document()`: Atomic git add + commit operation
- `list_agent_documents()`: List existing agent documents

See the module documentation for full API details.
