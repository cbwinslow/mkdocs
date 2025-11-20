# Next Steps: Complete Collection Submodule Setup

This document provides a simple checklist to complete the collection submodule setup.

## Quick Status Check

✅ **Completed:**
- Collection folder removed from main repository
- Documentation updated to reference the submodule
- Helper scripts created
- Collection repository content prepared in `/tmp/collection_backup/`

⏳ **Pending:**
- Create collection repository on GitHub
- Initialize collection repository with prepared content
- Add collection as submodule to main repository

## Completion Checklist

Follow these steps **in order**:

### [ ] Step 1: Create Collection Repository on GitHub

1. Open your browser to: https://github.com/new
2. Fill in the form:
   - **Repository name**: `collection`
   - **Description**: `AI agent todo lists, analyses, and training data`
   - **Visibility**: Choose based on your needs (Public recommended if main repo is public)
   - **Important**: Do NOT check "Initialize this repository with a README"
3. Click "Create repository"
4. Leave the browser window open (you'll need the instructions)

### [ ] Step 2: Initialize Collection Repository

Copy and paste these commands into your terminal:

```bash
# Navigate to the prepared collection content
cd /tmp/collection_backup

# Verify the files are there
ls -la
# You should see: README.md, .gitignore, SETUP_INSTRUCTIONS.md, .pgkeep

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Collection repository for AI agent data"

# Add GitHub remote (replace cbwinslow with YOUR username if different)
git remote add origin https://github.com/cbwinslow/collection.git

# Rename branch to main and push
git branch -M main
git push -u origin main
```

Expected output: You should see the files being uploaded to GitHub.

### [ ] Step 3: Add Submodule to Main Repository

**Option A: Use the helper script (Recommended)**

```bash
cd /home/runner/work/mkdocs/mkdocs
./scripts/finalize_collection_submodule.sh
```

Follow the prompts and answer 'y' when asked.

**Option B: Manual commands**

```bash
cd /home/runner/work/mkdocs/mkdocs

# Add the submodule
git submodule add https://github.com/cbwinslow/collection.git collection

# Commit the submodule
git add .gitmodules collection
git commit -m "Add collection as a git submodule"

# Push changes
git push
```

### [ ] Step 4: Verify Setup

Run these verification commands:

```bash
cd /home/runner/work/mkdocs/mkdocs

# Check submodule status
git submodule status
# Expected: Should show collection with a commit hash

# Navigate into collection
cd collection

# Check it's a proper git repository
git status
# Expected: "On branch main" or similar

# Check remote
git remote -v
# Expected: Should show origin pointing to cbwinslow/collection

# List files
ls -la
# Expected: Should show README.md, .gitignore, SETUP_INSTRUCTIONS.md, .pgkeep

# Return to main repo
cd ..

# Verify main repo status
git status
# Expected: Should be clean (everything committed)
```

### [ ] Step 5: Test Cloning (Optional but Recommended)

Test that the submodule works for new users:

```bash
# In a different directory
cd /tmp
git clone --recursive https://github.com/cbwinslow/mkdocs.git test-clone
cd test-clone

# Verify collection submodule was cloned
ls -la collection/
# Expected: Should show collection files, not empty

# Clean up
cd ..
rm -rf test-clone
```

## If You Encounter Issues

### Issue: "Repository does not exist" when adding submodule
**Solution**: Complete Steps 1-2 first. The collection repository must exist on GitHub.

### Issue: "fatal: destination path 'collection' already exists"
**Solution**: 
```bash
rm -rf collection
git submodule add https://github.com/cbwinslow/collection.git collection
```

### Issue: Authentication failed
**Solution**: 
- If using HTTPS, ensure you have a valid GitHub token
- Consider using SSH: `git submodule add git@github.com:cbwinslow/collection.git collection`

### Issue: Submodule appears empty after clone
**Solution**:
```bash
git submodule update --init --recursive
```

## After Completion

Once all steps are complete:

1. Update any CI/CD pipelines to use `--recursive` when cloning
2. Notify team members about the submodule
3. Share the [QUICKSTART_SUBMODULE.md](QUICKSTART_SUBMODULE.md) guide with team members
4. Mark this task as complete in your project tracker

## Documentation Reference

- **Quick commands**: [QUICKSTART_SUBMODULE.md](QUICKSTART_SUBMODULE.md)
- **Detailed setup guide**: [SUBMODULE_SETUP.md](SUBMODULE_SETUP.md)
- **Migration documentation**: [COLLECTION_MIGRATION.md](COLLECTION_MIGRATION.md)
- **Agent instructions**: [agent_bundle_templates.md](agent_bundle_templates.md)

## Questions?

If you have questions or encounter issues not covered here:
1. Check the troubleshooting sections in the documentation above
2. Review git submodule documentation: https://git-scm.com/book/en/v2/Git-Tools-Submodules
3. Check GitHub's submodule guide: https://docs.github.com/en/get-started/using-git/about-git-subtree-merges

---

**Estimated time to complete**: 10-15 minutes
