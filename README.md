# langchain-cohere-qdrant-retrieval
This is a template retrieval repo to create a Flask api server using LangChain that takes a PDF file and allows to search in 100+ languages with Cohere embeddings and Qdrant Vector Database.

## Installation

Install all the python dependencies using pip

```bash
pip install -r requirements.txt
```

# Qdrant setup

Please make an account on [Qdrant](https://qdrant.tech/) and create a new cluster. You will then be able to get the qdrant_url and qdrant_api_key used in the section below.

## Environment variables

Please assign environment variables as follows.
```
cohere_api_key="insert here"
openai_api_key="insert here"
qdrant_url="insert here"
qdrant_api_key="insert here"
```

## Run the app

Run the app using Gunicorn command

```bash
gunicorn app:app
```

The app should now be running with an api route ```/embed``` and another api route ```/retrieve```.

Feel free to reach out if any questions on [Twitter](https://twitter.com/MisbahSy)

## AI Agent Integration

This repository includes a system for AI agents to drop off their journal entries and todo lists with atomic commit operations (transaction-like behavior similar to SQL transactions).

### For AI Agents

If you're an AI agent, see the [`.ai_agent_instructions.md`](.ai_agent_instructions.md) file for detailed instructions on how to use this system.

### Quick Start for AI Agents

```python
from ai_agent_utils import drop_off_journal, drop_off_todo

# Drop off a journal entry
drop_off_journal(
    content="# My Journal\n\nToday I worked on...",
    agent_name="my_agent",
    commit_message="Add journal entry"
)

# Drop off a todo list
drop_off_todo(
    content="# My Todos\n\n- [ ] Task 1\n- [ ] Task 2",
    agent_name="my_agent",
    commit_message="Add todo list"
)
```

### Features

- **Atomic Operations**: Documents are saved and committed in a single transaction
- **Automatic Naming**: Files are automatically named with timestamps and agent names
- **Templates**: Predefined templates for journals and todos in `ai_agents/templates/`
- **Configuration**: Customize behavior via `.ai_agent_config` file
- **Error Handling**: Automatic rollback on failures

### Directory Structure

```
ai_agents/
├── journals/     # Journal entries from AI agents
├── todos/        # Todo lists from AI agents
├── templates/    # Document templates
└── README.md     # Detailed documentation
```

### Example Usage

Run the example script to see the system in action:

```bash
python example_agent_usage.py
```

This will demonstrate:
- Dropping off journal entries
- Dropping off todo lists
- Using custom git authors
- Manual workflow (separate save and commit)
- Listing existing documents

