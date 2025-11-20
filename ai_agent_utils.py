"""
AI Agent Document Drop-off Utilities

This module provides functions for AI agents to drop off their journal entries
and todo lists to the repository with atomic commit operations (transaction-like behavior).
"""

import os
import subprocess
from datetime import datetime
from typing import Optional, Literal
from pathlib import Path


# Configuration defaults
DEFAULT_AGENT_NAME = "ai_agent"
AGENT_DOCS_DIR = "ai_agents"
JOURNAL_DIR = "journals"
TODO_DIR = "todos"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"


def load_config() -> dict:
    """
    Load configuration from .ai_agent_config file.
    
    Returns:
        dict: Configuration dictionary with key-value pairs
    """
    config = {
        'DEFAULT_AGENT_NAME': DEFAULT_AGENT_NAME,
        'AGENT_DOCS_DIR': AGENT_DOCS_DIR,
        'JOURNAL_DIR': JOURNAL_DIR,
        'TODO_DIR': TODO_DIR,
        'TIMESTAMP_FORMAT': TIMESTAMP_FORMAT,
        'AUTO_GIT_ENABLED': 'true'
    }
    
    config_file = Path('.ai_agent_config')
    if config_file.exists():
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def get_repo_root() -> Path:
    """
    Get the root directory of the git repository.
    
    Returns:
        Path: Path to repository root
        
    Raises:
        RuntimeError: If not in a git repository
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        raise RuntimeError("Not in a git repository")


def validate_document_content(content: str) -> bool:
    """
    Validate that document content is not empty and is valid.
    
    Args:
        content: Document content to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not content or not content.strip():
        return False
    return True


def generate_filename(
    doc_type: Literal["journal", "todo"],
    agent_name: str,
    timestamp: Optional[str] = None
) -> str:
    """
    Generate a filename for an agent document.
    
    Args:
        doc_type: Type of document ("journal" or "todo")
        agent_name: Name of the agent
        timestamp: Optional timestamp string (generated if not provided)
        
    Returns:
        str: Generated filename
        
    Raises:
        ValueError: If doc_type is invalid
    """
    if doc_type not in ["journal", "todo"]:
        raise ValueError(f"Invalid doc_type: {doc_type}. Must be 'journal' or 'todo'")
    
    config = load_config()
    if timestamp is None:
        timestamp = datetime.now().strftime(config['TIMESTAMP_FORMAT'])
    
    # Sanitize agent name (remove special characters)
    safe_agent_name = "".join(c for c in agent_name if c.isalnum() or c in "-_")
    
    return f"{doc_type}_{timestamp}_{safe_agent_name}.md"


def get_document_path(
    doc_type: Literal["journal", "todo"],
    agent_name: str,
    timestamp: Optional[str] = None
) -> Path:
    """
    Get the full path for an agent document.
    
    Args:
        doc_type: Type of document ("journal" or "todo")
        agent_name: Name of the agent
        timestamp: Optional timestamp string
        
    Returns:
        Path: Full path to the document
    """
    config = load_config()
    repo_root = get_repo_root()
    
    subdir = config['JOURNAL_DIR'] if doc_type == "journal" else config['TODO_DIR']
    filename = generate_filename(doc_type, agent_name, timestamp)
    
    return repo_root / config['AGENT_DOCS_DIR'] / subdir / filename


def save_agent_document(
    content: str,
    filepath: Path,
    overwrite: bool = False
) -> Path:
    """
    Save an agent document to the filesystem.
    
    Args:
        content: Document content to save
        filepath: Path where to save the document
        overwrite: Whether to overwrite existing file
        
    Returns:
        Path: Path to the saved document
        
    Raises:
        ValueError: If content is invalid
        FileExistsError: If file exists and overwrite is False
    """
    if not validate_document_content(content):
        raise ValueError("Document content cannot be empty")
    
    if filepath.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {filepath}")
    
    # Create parent directories if they don't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content to file
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath


def commit_agent_document(
    filepath: Path,
    commit_message: str,
    author_name: Optional[str] = None,
    author_email: Optional[str] = None
) -> bool:
    """
    Atomically add and commit an agent document to git (transaction-like operation).
    
    This function ensures that the document is both added to git and committed
    in a single operation. If either step fails, the operation is rolled back.
    
    Args:
        filepath: Path to the document to commit
        commit_message: Commit message
        author_name: Optional git author name
        author_email: Optional git author email
        
    Returns:
        bool: True if successful
        
    Raises:
        FileNotFoundError: If file doesn't exist
        RuntimeError: If git operations fail
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    repo_root = get_repo_root()
    relative_path = filepath.relative_to(repo_root)
    
    try:
        # Step 1: Add the file to git staging area
        subprocess.run(
            ['git', 'add', str(relative_path)],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Step 2: Commit the file
        commit_cmd = ['git', 'commit', '-m', commit_message]
        
        # Add author information if provided
        env = os.environ.copy()
        if author_name:
            env['GIT_AUTHOR_NAME'] = author_name
            env['GIT_COMMITTER_NAME'] = author_name
        if author_email:
            env['GIT_AUTHOR_EMAIL'] = author_email
            env['GIT_COMMITTER_EMAIL'] = author_email
        
        subprocess.run(
            commit_cmd,
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        # If commit fails, try to unstage the file
        try:
            subprocess.run(
                ['git', 'reset', 'HEAD', str(relative_path)],
                cwd=repo_root,
                check=False,
                capture_output=True
            )
        except:
            pass  # Best effort rollback
        
        raise RuntimeError(f"Git operation failed: {e.stderr}")


def drop_off_document(
    content: str,
    doc_type: Literal["journal", "todo"],
    agent_name: Optional[str] = None,
    commit_message: Optional[str] = None,
    timestamp: Optional[str] = None,
    author_name: Optional[str] = None,
    author_email: Optional[str] = None
) -> Path:
    """
    Complete transaction: Save and commit an agent document in one operation.
    
    This is the main function AI agents should use. It combines save_agent_document()
    and commit_agent_document() into a single atomic operation.
    
    Args:
        content: Document content
        doc_type: Type of document ("journal" or "todo")
        agent_name: Name of the agent (uses default if not provided)
        commit_message: Git commit message (generates default if not provided)
        timestamp: Optional timestamp string
        author_name: Optional git author name
        author_email: Optional git author email
        
    Returns:
        Path: Path to the committed document
        
    Raises:
        ValueError: If content or parameters are invalid
        RuntimeError: If save or commit operations fail
    """
    config = load_config()
    
    # Use default agent name if not provided
    if agent_name is None:
        agent_name = config['DEFAULT_AGENT_NAME']
    
    # Generate filepath
    filepath = get_document_path(doc_type, agent_name, timestamp)
    
    # Generate commit message if not provided
    if commit_message is None:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if doc_type == "journal":
            commit_message = f"Add journal entry from {agent_name} - {timestamp_str}"
        else:
            commit_message = f"Add todo list from {agent_name} - {timestamp_str}"
    
    try:
        # Step 1: Save the document
        save_agent_document(content, filepath, overwrite=False)
        
        # Step 2: Commit the document
        commit_agent_document(
            filepath,
            commit_message,
            author_name=author_name,
            author_email=author_email
        )
        
        return filepath
        
    except Exception as e:
        # If anything fails, try to clean up the file
        if filepath.exists():
            try:
                filepath.unlink()
            except:
                pass  # Best effort cleanup
        
        raise RuntimeError(f"Failed to drop off document: {str(e)}")


def list_agent_documents(
    doc_type: Optional[Literal["journal", "todo"]] = None,
    agent_name: Optional[str] = None
) -> list[Path]:
    """
    List existing agent documents.
    
    Args:
        doc_type: Optional filter by document type
        agent_name: Optional filter by agent name
        
    Returns:
        list[Path]: List of document paths
    """
    config = load_config()
    repo_root = get_repo_root()
    agent_docs_dir = repo_root / config['AGENT_DOCS_DIR']
    
    documents = []
    
    # Determine which directories to search
    if doc_type == "journal":
        search_dirs = [agent_docs_dir / config['JOURNAL_DIR']]
    elif doc_type == "todo":
        search_dirs = [agent_docs_dir / config['TODO_DIR']]
    else:
        search_dirs = [
            agent_docs_dir / config['JOURNAL_DIR'],
            agent_docs_dir / config['TODO_DIR']
        ]
    
    # Find all markdown files
    for search_dir in search_dirs:
        if search_dir.exists():
            for filepath in search_dir.glob("*.md"):
                # Filter by agent name if specified
                if agent_name is None or f"_{agent_name}.md" in filepath.name:
                    documents.append(filepath)
    
    return sorted(documents)


# Convenience functions for specific document types

def drop_off_journal(
    content: str,
    agent_name: Optional[str] = None,
    commit_message: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Drop off a journal entry. Convenience wrapper for drop_off_document().
    
    Args:
        content: Journal content
        agent_name: Name of the agent
        commit_message: Git commit message
        **kwargs: Additional arguments passed to drop_off_document()
        
    Returns:
        Path: Path to the committed journal
    """
    return drop_off_document(
        content=content,
        doc_type="journal",
        agent_name=agent_name,
        commit_message=commit_message,
        **kwargs
    )


def drop_off_todo(
    content: str,
    agent_name: Optional[str] = None,
    commit_message: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Drop off a todo list. Convenience wrapper for drop_off_document().
    
    Args:
        content: Todo list content
        agent_name: Name of the agent
        commit_message: Git commit message
        **kwargs: Additional arguments passed to drop_off_document()
        
    Returns:
        Path: Path to the committed todo list
    """
    return drop_off_document(
        content=content,
        doc_type="todo",
        agent_name=agent_name,
        commit_message=commit_message,
        **kwargs
    )
