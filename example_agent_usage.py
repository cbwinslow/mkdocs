#!/usr/bin/env python3
"""
Example usage of AI Agent document drop-off utilities.

This script demonstrates how AI agents can use the provided functions
to drop off their journal entries and todo lists.
"""

from ai_agent_utils import (
    drop_off_journal,
    drop_off_todo,
    drop_off_document,
    list_agent_documents,
    save_agent_document,
    commit_agent_document,
    get_document_path
)
from datetime import datetime


def example_basic_journal():
    """Example: Drop off a simple journal entry."""
    print("Example 1: Dropping off a basic journal entry...")
    
    journal_content = f"""# Journal Entry - Example Agent - {datetime.now().strftime('%Y-%m-%d')}

## Session Information
- **Agent**: example_agent
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Time**: {datetime.now().strftime('%H:%M:%S')}
- **Task**: Demonstrating journal drop-off functionality

## Activities Performed
- Created example journal entry
- Tested the drop_off_journal() function
- Verified atomic commit operation

## Results/Outcomes
- ✅ Successfully created and committed journal entry
- ✅ Confirmed transaction-like behavior

## Next Steps
1. Test with actual agent workflows
2. Gather feedback from AI agents
3. Iterate on the design
"""
    
    try:
        filepath = drop_off_journal(
            content=journal_content,
            agent_name="example_agent",
            commit_message="Add example journal entry from example_agent"
        )
        print(f"✅ Journal successfully dropped off at: {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_basic_todo():
    """Example: Drop off a simple todo list."""
    print("\nExample 2: Dropping off a basic todo list...")
    
    todo_content = f"""# Todo List - Example Agent - {datetime.now().strftime('%Y-%m-%d')}

## Overview
- **Agent**: example_agent
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Project/Task Context**: Testing AI agent document drop-off system

## High Priority Tasks 🔴
- [ ] **Test journal drop-off functionality**
  - Description: Verify that journals can be dropped off successfully
  - Estimated effort: 15 minutes

- [ ] **Test todo drop-off functionality**
  - Description: Verify that todo lists can be dropped off successfully
  - Estimated effort: 15 minutes

## Medium Priority Tasks 🟡
- [ ] **Write comprehensive tests**
  - Description: Add unit tests for all utility functions
  - Estimated effort: 1 hour

## Completed Tasks ✅
- [x] **Create AI agent utilities module**
  - Completed: {datetime.now().strftime('%Y-%m-%d')}
  - Notes: Implemented all core functions

- [x] **Create documentation**
  - Completed: {datetime.now().strftime('%Y-%m-%d')}
  - Notes: Added instructions and templates
"""
    
    try:
        filepath = drop_off_todo(
            content=todo_content,
            agent_name="example_agent",
            commit_message="Add example todo list from example_agent"
        )
        print(f"✅ Todo list successfully dropped off at: {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_author():
    """Example: Drop off document with custom git author."""
    print("\nExample 3: Dropping off with custom git author...")
    
    content = f"""# Journal Entry - AI Assistant - {datetime.now().strftime('%Y-%m-%d')}

## Session Information
- **Agent**: ai_assistant
- **Date**: {datetime.now().strftime('%Y-%m-%d')}

## Activities
- Demonstrated custom git author functionality
- Showed how to set author name and email

## Notes
This commit will have a custom author in the git history.
"""
    
    try:
        filepath = drop_off_journal(
            content=content,
            agent_name="ai_assistant",
            commit_message="Add journal with custom author",
            author_name="AI Assistant Bot",
            author_email="ai-assistant@example.com"
        )
        print(f"✅ Journal with custom author dropped off at: {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_manual_workflow():
    """Example: Manual workflow with separate save and commit steps."""
    print("\nExample 4: Manual workflow (save then commit separately)...")
    
    content = f"""# Todo List - Manual Workflow Agent - {datetime.now().strftime('%Y-%m-%d')}

## High Priority Tasks 🔴
- [ ] Review manual workflow example
- [ ] Understand the difference between atomic and manual operations

## Notes
This demonstrates how to use save and commit separately instead of
using the atomic drop_off_document() function.
"""
    
    try:
        # Step 1: Get the document path
        filepath = get_document_path("todo", "manual_agent")
        print(f"  Document will be saved to: {filepath}")
        
        # Step 2: Save the document
        save_agent_document(content, filepath)
        print(f"  ✓ Document saved to filesystem")
        
        # Step 3: Commit the document
        commit_agent_document(
            filepath,
            commit_message="Add todo list from manual_agent (manual workflow)"
        )
        print(f"  ✓ Document committed to git")
        
        print(f"✅ Manual workflow completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_list_documents():
    """Example: List existing agent documents."""
    print("\nExample 5: Listing existing agent documents...")
    
    try:
        # List all documents
        all_docs = list_agent_documents()
        print(f"\n  All documents ({len(all_docs)}):")
        for doc in all_docs:
            print(f"    - {doc.name}")
        
        # List only journals
        journals = list_agent_documents(doc_type="journal")
        print(f"\n  Journals only ({len(journals)}):")
        for doc in journals:
            print(f"    - {doc.name}")
        
        # List only todos
        todos = list_agent_documents(doc_type="todo")
        print(f"\n  Todos only ({len(todos)}):")
        for doc in todos:
            print(f"    - {doc.name}")
        
        # List documents from specific agent
        example_docs = list_agent_documents(agent_name="example_agent")
        print(f"\n  Documents from 'example_agent' ({len(example_docs)}):")
        for doc in example_docs:
            print(f"    - {doc.name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples."""
    print("=" * 70)
    print("AI Agent Document Drop-off System - Examples")
    print("=" * 70)
    
    # Run examples
    example_basic_journal()
    example_basic_todo()
    example_custom_author()
    example_manual_workflow()
    example_list_documents()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nCheck the 'ai_agents/' directory to see the dropped-off documents.")
    print("Check the git log to see the atomic commits.")


if __name__ == "__main__":
    main()
