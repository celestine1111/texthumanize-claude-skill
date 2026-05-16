#!/usr/bin/env bash
# Install the TextHumanize Claude Code skill
# Usage: bash install.sh

set -e

SKILL_DIR="$HOME/.claude/commands"
SCRIPTS_DIR="$HOME/.claude/scripts"

mkdir -p "$SKILL_DIR" "$SCRIPTS_DIR"

# Copy skill command
cp .claude/commands/humanize.md "$SKILL_DIR/humanize.md"
echo "Installed skill: $SKILL_DIR/humanize.md"

# Copy runner script
cp scripts/humanize_runner.py "$SCRIPTS_DIR/humanize_runner.py"
chmod +x "$SCRIPTS_DIR/humanize_runner.py"
echo "Installed runner: $SCRIPTS_DIR/humanize_runner.py"

# Install texthumanize Python package
echo "Installing texthumanize Python package..."
pip install texthumanize --quiet
echo "Done."

echo ""
echo "Skill installed. In Claude Code, type /humanize to use it."
