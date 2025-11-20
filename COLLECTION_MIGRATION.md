# Collection Folder Migration to Submodule

This document describes the migration of the `collection` folder to a git submodule.

## What Was Changed

### Completed Steps

1. ✅ **Documentation Updated**
   - Updated `agent_bundle_templates.md` to reference the collection submodule
   - Updated `README.md` with submodule cloning instructions
   - Created `SUBMODULE_SETUP.md` with detailed submodule usage guide
   - Created this migration document

2. ✅ **Collection Folder Removed**
   - Removed the `collection` folder from the main repository
   - Original content backed up and prepared for the new repository

3. ✅ **Collection Repository Content Prepared**
   - Created initialization files in `/tmp/collection_backup/`
   - Files include: README.md, .gitignore, SETUP_INSTRUCTIONS.md, and original .pgkeep

### Pending Manual Steps

The following steps require manual action and cannot be automated:

1. ⏳ **Create the Collection Repository on GitHub**
   - Go to: https://github.com/new
   - Repository name: `collection`
   - Description: "AI agent todo lists, analyses, and training data"
   - Do NOT initialize with README
   - Create the repository

2. ⏳ **Initialize and Push Collection Repository**
   ```bash
   cd /tmp/collection_backup
   git init
   git add .
   git commit -m "Initial commit: Collection repository for AI agent data"
   git remote add origin https://github.com/cbwinslow/collection.git
   git branch -M main
   git push -u origin main
   ```

3. ⏳ **Add Collection as Submodule**
   ```bash
   cd /home/runner/work/mkdocs/mkdocs
   git submodule add https://github.com/cbwinslow/collection.git collection
   git add .gitmodules collection
   git commit -m "Add collection as a git submodule"
   ```

## Why Use a Submodule?

The collection was converted to a submodule for several reasons:

1. **Separation of Concerns**: Agent data is kept separate from application code
2. **Independent Versioning**: The collection can be versioned and updated independently
3. **Scalability**: Large amounts of agent data don't bloat the main repository
4. **Flexibility**: Multiple projects can reference the same collection
5. **Cleaner History**: Agent data changes don't clutter the main repository's commit history

## Repository Structure After Migration

```
mkdocs/                          (main repository)
├── collection/                   (submodule → cbwinslow/collection)
│   ├── README.md
│   ├── .gitignore
│   ├── SETUP_INSTRUCTIONS.md
│   └── agent_bundle_<UUID>/     (future agent bundles go here)
├── app.py
├── agent_bundle_templates.md
├── SUBMODULE_SETUP.md
├── COLLECTION_MIGRATION.md
└── ...
```

## Collection Repository Structure

```
collection/                       (separate repository)
├── README.md                     (purpose and usage)
├── .gitignore                    (ignore patterns)
├── SETUP_INSTRUCTIONS.md         (how it was set up)
└── agent_bundle_<UUID>/          (agent bundles)
    ├── agents.md
    ├── rules.md
    ├── journal.md
    ├── todos.md
    ├── features.md
    ├── project_summary.md
    ├── srs.md
    └── bundle.json
```

## For AI Agents

When working with this repository:

1. **Clone with submodules**: Always use `git clone --recursive` or initialize submodules after cloning
2. **Store data in collection**: Place all agent bundles in the `collection/` submodule
3. **Commit to submodule first**: Changes in `collection/` should be committed to the collection repository
4. **Update main repository**: After updating the collection, commit the submodule reference in the main repo

See [SUBMODULE_SETUP.md](SUBMODULE_SETUP.md) for detailed instructions.

## Verification

After completing the manual steps, verify the setup:

```bash
# Check submodule status
git submodule status

# Should show:
#  <commit-hash> collection (heads/main)

# Navigate into collection
cd collection
git status

# Should show:
# On branch main
# Your branch is up to date with 'origin/main'.
```

## Rollback (If Needed)

If you need to rollback this change:

```bash
# Remove the submodule
git submodule deinit -f collection
git rm -f collection
rm -rf .git/modules/collection

# Restore the original collection folder
git checkout HEAD~1 -- collection

# Revert documentation changes
git checkout HEAD~1 -- README.md agent_bundle_templates.md
git rm SUBMODULE_SETUP.md COLLECTION_MIGRATION.md
```

## Questions or Issues?

If you encounter any issues during the migration:

1. Check the detailed instructions in [SUBMODULE_SETUP.md](SUBMODULE_SETUP.md)
2. Review the collection repository's [SETUP_INSTRUCTIONS.md](https://github.com/cbwinslow/collection/blob/main/SETUP_INSTRUCTIONS.md)
3. Consult the git submodule documentation: https://git-scm.com/book/en/v2/Git-Tools-Submodules
