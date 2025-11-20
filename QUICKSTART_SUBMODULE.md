# Quick Start: Collection Submodule

This is a quick reference guide for completing the collection submodule setup.

## For Repository Owners (First-Time Setup)

### Step 1: Create the Collection Repository (5 minutes)

1. Go to https://github.com/new
2. Fill in:
   - Repository name: `collection`
   - Description: `AI agent todo lists, analyses, and training data`
   - Visibility: Your choice
   - **Do NOT** check "Initialize this repository with a README"
3. Click "Create repository"

### Step 2: Initialize the Collection Repository (2 minutes)

```bash
# Navigate to the backed-up collection content
cd /tmp/collection_backup

# Initialize as a git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Collection repository for AI agent data"

# Add GitHub as remote (replace cbwinslow with your username)
git remote add origin https://github.com/cbwinslow/collection.git

# Set main branch and push
git branch -M main
git push -u origin main
```

### Step 3: Add Submodule to Main Repository (1 minute)

```bash
# Navigate to main repository
cd /home/runner/work/mkdocs/mkdocs

# Add the submodule
git submodule add https://github.com/cbwinslow/collection.git collection

# Commit the submodule
git add .gitmodules collection
git commit -m "Add collection as a git submodule"

# Push changes
git push
```

**OR** use the helper script:

```bash
cd /home/runner/work/mkdocs/mkdocs
./scripts/finalize_collection_submodule.sh
```

### Step 4: Verify (1 minute)

```bash
# Check submodule status
git submodule status

# Should output something like:
# [commit-hash] collection (heads/main)

# Navigate into collection and verify
cd collection
ls -la
git status
```

## For Users Cloning the Repository

If you're cloning the mkdocs repository after the submodule has been set up:

```bash
# Option 1: Clone with submodules in one command
git clone --recursive https://github.com/cbwinslow/mkdocs.git

# Option 2: Clone, then initialize submodules
git clone https://github.com/cbwinslow/mkdocs.git
cd mkdocs
git submodule init
git submodule update
```

## Common Commands

### Update the collection submodule to latest version
```bash
cd collection
git pull origin main
cd ..
git add collection
git commit -m "Update collection submodule"
```

### Make changes in the collection
```bash
cd collection
# Make your changes
git add .
git commit -m "Your changes"
git push origin main
cd ..
git add collection
git commit -m "Update collection reference"
```

### Check submodule status
```bash
git submodule status
```

### Reset submodule to tracked commit
```bash
git submodule update --init
```

## Need More Details?

- **For comprehensive setup instructions**: See [COLLECTION_MIGRATION.md](COLLECTION_MIGRATION.md)
- **For detailed submodule usage**: See [SUBMODULE_SETUP.md](SUBMODULE_SETUP.md)
- **For AI agent instructions**: See [agent_bundle_templates.md](agent_bundle_templates.md)

## Troubleshooting

### "fatal: repository does not exist"
- The collection repository hasn't been created yet on GitHub
- Complete Steps 1-2 above

### "collection already exists and is not an empty directory"
- Remove the existing collection directory: `rm -rf collection`
- Try adding the submodule again

### Submodule shows as modified but no changes
- Run: `git submodule update --init --recursive`

### Can't push to collection
- Make sure you're on a branch: `cd collection && git checkout -b main`
- Or checkout existing: `cd collection && git checkout main`
