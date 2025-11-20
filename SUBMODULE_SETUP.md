# Collection Submodule Setup Guide

This document describes the process of converting the `collection` folder into a git submodule.

## Overview

The `collection` folder has been converted from a regular directory to a git submodule. This allows the collection content to be maintained in its own repository while still being accessible from the main mkdocs repository.

## What is the Collection?

The collection is where all AI agent todo lists, details, and analyses are stored. This data can be used for analysis and training purposes.

## Repository Structure

- **Main Repository**: `https://github.com/cbwinslow/mkdocs`
- **Collection Submodule**: `https://github.com/cbwinslow/collection`

## Initial Setup Steps (Already Completed)

1. ✅ Backed up the original collection folder content
2. ✅ Removed the collection folder from the main repository
3. ✅ Created the collection submodule reference
4. ✅ Updated documentation to reference the submodule

## For Users Cloning This Repository

When cloning this repository for the first time, you need to initialize the submodules:

```bash
# Clone the repository with submodules
git clone --recursive https://github.com/cbwinslow/mkdocs.git

# OR, if you've already cloned without --recursive:
git clone https://github.com/cbwinslow/mkdocs.git
cd mkdocs
git submodule init
git submodule update
```

## Working with the Submodule

### Updating the Collection Submodule

To pull the latest changes from the collection repository:

```bash
cd collection
git pull origin main
cd ..
git add collection
git commit -m "Update collection submodule"
```

### Making Changes to the Collection

1. Navigate into the collection submodule:
   ```bash
   cd collection
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

3. Update the main repository to reference the new commit:
   ```bash
   cd ..
   git add collection
   git commit -m "Update collection submodule reference"
   git push
   ```

## CI/CD Configuration

If you use CI/CD pipelines, make sure to update them to initialize submodules:

```yaml
# Example for GitHub Actions
- name: Checkout code
  uses: actions/checkout@v3
  with:
    submodules: recursive
```

## Troubleshooting

### Submodule appears empty after clone

Run:
```bash
git submodule update --init --recursive
```

### Detached HEAD state in submodule

This is normal for submodules. To work on changes:
```bash
cd collection
git checkout main
# Make changes and commit
```

## Agent Instructions

AI agents working with this repository should:
1. Initialize submodules when cloning the repository
2. Store agent todo lists and analyses in the `collection` submodule
3. Commit changes to the collection submodule separately from the main repository
4. Update the main repository's submodule reference after collection updates
