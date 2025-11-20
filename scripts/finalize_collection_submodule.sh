#!/bin/bash
# Script to finalize the collection submodule setup
# This script should be run AFTER the collection repository has been created on GitHub

set -e

COLLECTION_REPO_URL="https://github.com/cbwinslow/collection.git"
MAIN_REPO_DIR="/home/runner/work/mkdocs/mkdocs"
COLLECTION_BACKUP_DIR="/tmp/collection_backup"

echo "================================================"
echo "Collection Submodule Finalization Script"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -d "$MAIN_REPO_DIR/.git" ]; then
    echo "ERROR: Main repository not found at $MAIN_REPO_DIR"
    exit 1
fi

# Check if collection backup exists
if [ ! -d "$COLLECTION_BACKUP_DIR" ]; then
    echo "ERROR: Collection backup not found at $COLLECTION_BACKUP_DIR"
    echo "The collection content should have been backed up before migration."
    exit 1
fi

echo "This script will:"
echo "1. Add the collection repository as a submodule"
echo "2. Commit the submodule configuration"
echo ""
echo "PREREQUISITES:"
echo "- The collection repository must already exist at: $COLLECTION_REPO_URL"
echo "- The repository should be initialized with the content from: $COLLECTION_BACKUP_DIR"
echo ""
echo "Have you completed these prerequisites? (y/n)"
read -r response

if [ "$response" != "y" ]; then
    echo ""
    echo "Please complete the prerequisites first:"
    echo ""
    echo "1. Create repository at: https://github.com/cbwinslow/collection"
    echo ""
    echo "2. Initialize it with:"
    echo "   cd $COLLECTION_BACKUP_DIR"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit: Collection repository for AI agent data'"
    echo "   git remote add origin $COLLECTION_REPO_URL"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    exit 0
fi

echo ""
echo "Proceeding with submodule setup..."
echo ""

# Navigate to main repository
cd "$MAIN_REPO_DIR"

# Check if collection directory already exists
if [ -d "collection" ]; then
    echo "WARNING: collection directory already exists"
    echo "This could be a leftover or an existing submodule"
    echo "Current status:"
    ls -la collection/
    echo ""
    echo "Do you want to remove it and continue? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "Aborted."
        exit 0
    fi
    rm -rf collection
fi

# Add the submodule
echo "Adding collection as a submodule..."
git submodule add "$COLLECTION_REPO_URL" collection

# Verify submodule was added
echo ""
echo "Submodule added successfully!"
echo "Submodule status:"
git submodule status

# Check what needs to be committed
echo ""
echo "Changes to commit:"
git --no-pager status --short

echo ""
echo "================================================"
echo "Submodule setup complete!"
echo "================================================"
echo ""
echo "The collection has been added as a submodule."
echo "Remember to commit and push your changes:"
echo ""
echo "  git add .gitmodules collection"
echo "  git commit -m 'Add collection as a git submodule'"
echo "  git push"
echo ""
echo "See SUBMODULE_SETUP.md for usage instructions."
