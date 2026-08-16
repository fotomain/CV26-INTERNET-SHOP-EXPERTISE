#!/usr/bin/env bash
# ==============================================================================
# Script: run_save_to_github_mac.sh
# Purpose: Saves codebase to GitHub on a new branch named ok_YY-MM-DD-HH-MM
# Excludes: dataset_start/
# Remote: https://github.com/fotomain/cv26repo.git
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

REMOTE_URL="https://github.com/fotomain/cv26repo.git"

echo "================================================================================"
echo ">>> [1/5] Checking Git Repository & Remote Configuration..."
echo "================================================================================"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing new Git repository..."
    git init
fi

# Ensure .gitignore exists and excludes dataset_start
if [ ! -f ".gitignore" ] || ! grep -q "dataset_start" .gitignore; then
    echo "Updating .gitignore to exclude dataset_start/..."
    cat << 'EOF' > .gitignore
# Exclude raw start dataset
dataset_start
dataset_start/
dataset_start/*

# Virtual Environment & Python Caches
.venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# OS & IDE Files
.DS_Store
.idea/
.vscode/
*.swp
*.tmp
EOF
fi

# Untrack dataset_start if previously tracked
git rm --cached -r dataset_start 2>/dev/null || true

# Configure remote origin
if git remote | grep -q "^origin$"; then
    echo "Updating remote 'origin' to $REMOTE_URL..."
    git remote set-url origin "$REMOTE_URL"
else
    echo "Adding remote 'origin' -> $REMOTE_URL..."
    git remote add origin "$REMOTE_URL"
fi

echo ""
echo "================================================================================"
echo ">>> [2/5] Creating New Branch: ok_YY-MM-DD-HH-MM..."
echo "================================================================================"

BRANCH_NAME="ok_$(date +%y-%m-%d-%H-%M)"
echo "New branch name: $BRANCH_NAME"

git checkout -b "$BRANCH_NAME"

echo ""
echo "================================================================================"
echo ">>> [3/5] Staging Project Files (excluding dataset_start/)..."
echo "================================================================================"

git add .

echo ""
echo "================================================================================"
echo ">>> [4/5] Committing Changes..."
echo "================================================================================"

if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "No uncommitted changes detected. Creating empty commit with branch tag..."
    git commit --allow-empty -m "Auto save: $BRANCH_NAME"
else
    git commit -m "Auto save: $BRANCH_NAME"
fi

echo ""
echo "================================================================================"
echo ">>> [5/5] Pushing to GitHub (origin/$BRANCH_NAME)..."
echo "================================================================================"

git push -u origin "$BRANCH_NAME"

echo ""
echo "================================================================================"
echo "✓ Successfully saved and pushed to GitHub!"
echo "  - Repository : $REMOTE_URL"
echo "  - Branch     : $BRANCH_NAME"
echo "================================================================================"
