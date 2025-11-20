#!/usr/bin/env python3
"""
Simple tests for AI Agent document drop-off utilities.

This file provides basic validation of the core functionality.
Note: These tests create real commits in the repository.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

# Import the utilities
from ai_agent_utils import (
    validate_document_content,
    generate_filename,
    get_document_path,
    save_agent_document,
    load_config,
    list_agent_documents,
)


def test_validate_document_content():
    """Test document validation."""
    print("Testing document validation...")
    
    # Valid content
    assert validate_document_content("# Test\nContent"), "Should accept valid content"
    assert validate_document_content("Hello world"), "Should accept simple text"
    
    # Invalid content
    assert not validate_document_content(""), "Should reject empty string"
    assert not validate_document_content("   "), "Should reject whitespace only"
    
    # Test None handling
    try:
        result = validate_document_content(None)
        # If it doesn't raise, it should return False
        assert not result, "Should reject None"
    except (TypeError, AttributeError):
        # It's also acceptable to raise an error for None
        pass
    
    print("  ✅ Document validation tests passed")


def test_generate_filename():
    """Test filename generation."""
    print("Testing filename generation...")
    
    # Test journal filename
    journal_name = generate_filename("journal", "test_agent")
    assert journal_name.startswith("journal_"), "Journal should start with 'journal_'"
    assert "_test_agent.md" in journal_name, "Should include agent name"
    assert journal_name.endswith(".md"), "Should end with .md"
    
    # Test todo filename
    todo_name = generate_filename("todo", "test_agent")
    assert todo_name.startswith("todo_"), "Todo should start with 'todo_'"
    assert "_test_agent.md" in todo_name, "Should include agent name"
    
    # Test with custom timestamp
    custom_timestamp = "20250115_120000"
    custom_name = generate_filename("journal", "agent", custom_timestamp)
    assert custom_timestamp in custom_name, "Should use custom timestamp"
    
    # Test invalid doc_type
    try:
        generate_filename("invalid", "agent")
        assert False, "Should raise ValueError for invalid doc_type"
    except ValueError:
        pass  # Expected
    
    print("  ✅ Filename generation tests passed")


def test_get_document_path():
    """Test document path generation."""
    print("Testing document path generation...")
    
    journal_path = get_document_path("journal", "test_agent")
    assert "ai_agents" in str(journal_path), "Should include ai_agents directory"
    assert "journals" in str(journal_path), "Should include journals subdirectory"
    assert journal_path.suffix == ".md", "Should have .md extension"
    
    todo_path = get_document_path("todo", "test_agent")
    assert "todos" in str(todo_path), "Should include todos subdirectory"
    
    print("  ✅ Document path generation tests passed")


def test_load_config():
    """Test configuration loading."""
    print("Testing configuration loading...")
    
    config = load_config()
    assert "DEFAULT_AGENT_NAME" in config, "Should have DEFAULT_AGENT_NAME"
    assert "AGENT_DOCS_DIR" in config, "Should have AGENT_DOCS_DIR"
    assert "JOURNAL_DIR" in config, "Should have JOURNAL_DIR"
    assert "TODO_DIR" in config, "Should have TODO_DIR"
    assert config["AGENT_DOCS_DIR"] == "ai_agents", "Should load correct default"
    
    print("  ✅ Configuration loading tests passed")


def test_save_agent_document():
    """Test document saving."""
    print("Testing document saving...")
    
    # Create a test document in /tmp
    test_dir = Path("/tmp/test_ai_agents")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "test_document.md"
    
    # Clean up if exists
    if test_file.exists():
        test_file.unlink()
    
    # Test saving
    content = "# Test Document\n\nThis is a test."
    saved_path = save_agent_document(content, test_file)
    assert saved_path.exists(), "File should be created"
    assert saved_path.read_text() == content, "Content should match"
    
    # Test overwrite protection
    try:
        save_agent_document(content, test_file, overwrite=False)
        assert False, "Should raise FileExistsError"
    except FileExistsError:
        pass  # Expected
    
    # Test overwrite allowed
    new_content = "# Updated\n\nNew content."
    save_agent_document(new_content, test_file, overwrite=True)
    assert test_file.read_text() == new_content, "Should update content"
    
    # Clean up
    test_file.unlink()
    
    print("  ✅ Document saving tests passed")


def test_list_agent_documents():
    """Test listing documents."""
    print("Testing document listing...")
    
    # List all documents (should have our example documents)
    all_docs = list_agent_documents()
    assert isinstance(all_docs, list), "Should return a list"
    
    # List journals only
    journals = list_agent_documents(doc_type="journal")
    for doc in journals:
        assert "journal" in doc.name, "Should only return journals"
    
    # List todos only
    todos = list_agent_documents(doc_type="todo")
    for doc in todos:
        assert "todo" in doc.name, "Should only return todos"
    
    print(f"  ✅ Document listing tests passed (found {len(all_docs)} documents)")


def test_sanitization():
    """Test that agent names are properly sanitized."""
    print("Testing agent name sanitization...")
    
    # Test with special characters that should be removed/sanitized
    unsafe_name = "agent@#$%name!123"
    filename = generate_filename("journal", unsafe_name)
    # Should only contain alphanumeric, dash, and underscore
    assert all(c.isalnum() or c in "_-." for c in filename), \
        "Filename should only contain safe characters"
    
    print("  ✅ Agent name sanitization tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running AI Agent Utils Tests")
    print("=" * 70)
    print()
    
    try:
        test_validate_document_content()
        test_generate_filename()
        test_get_document_path()
        test_load_config()
        test_save_agent_document()
        test_list_agent_documents()
        test_sanitization()
        
        print()
        print("=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 70)
        print(f"❌ Test failed: {e}")
        print("=" * 70)
        return 1
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Unexpected error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
