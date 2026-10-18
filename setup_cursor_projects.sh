#!/bin/bash
# Setup script for Cursor rapid prototyping workflow
# This creates your projects directory and sets up the structure

set -e

PROJECTS_DIR="${1:-$HOME/Projects/random-ideas}"

echo "🚀 Setting up Cursor rapid prototyping workflow..."
echo "📁 Projects directory: $PROJECTS_DIR"
echo ""

# Create projects directory
mkdir -p "$PROJECTS_DIR"
echo "✅ Created directory: $PROJECTS_DIR"

# Create a README in the projects directory
cat > "$PROJECTS_DIR/README.md" << EOF
# Random Ideas Projects

This directory contains all your random project ideas and prototypes.

## Structure

Each project should be self-contained with:
- README.md (setup and usage instructions)
- .gitignore (appropriate for the tech stack)
- Basic project structure
- Working "Hello World" example

## Quick Start

Use Cursor commands to scaffold new projects:
- \`new-python-project\` - Python with venv
- \`new-web-project\` - HTML/CSS/JS
- \`new-node-project\` - Node.js

Or just ask Cursor AI to create a project for you!
EOF

echo "✅ Created README.md in projects directory"

# Create a .gitkeep to track the directory
touch "$PROJECTS_DIR/.gitkeep"

# Create a templates directory for reusable boilerplate
TEMPLATES_DIR="$PROJECTS_DIR/.templates"
mkdir -p "$TEMPLATES_DIR"

echo "✅ Created templates directory: $TEMPLATES_DIR"

# Create a project ideas file
cat > "$PROJECTS_DIR/IDEAS.md" << 'EOF'
# Project Ideas

Add your random ideas here as they come to you!

## Ideas

- [ ] Example: URL shortener
- [ ] Example: Password generator
- [ ] Example: Todo app with local storage

## Completed

- [x] Example: Face scanner (done!)

---

**Tip:** When you complete a project, move it to a "completed" folder or archive it.
EOF

echo "✅ Created IDEAS.md for tracking project ideas"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Open Cursor Settings → Rules and Commands"
echo "2. Add the commands from CURSOR_QUICK_START.md"
echo "3. Add the rules from CURSOR_QUICK_START.md"
echo "4. Start creating projects!"
echo ""
echo "Test it out:"
echo "  Ask Cursor: 'Create a Python project called test-project'"
echo "  Or use Command Palette: Cmd/Ctrl+Shift+P → 'Cursor: Run Command'"
