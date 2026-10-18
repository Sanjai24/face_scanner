# Cursor Customization Guide for Rapid Prototyping

## 🎯 Your Workflow Goal
Create random projects quickly in a specific folder location with minimal setup friction.

---

## 📋 Recommended User Rules

Add these to your **User Rules** in Cursor Settings:

```
Don't be a bitch

When creating new projects:
- Always create a clean, minimal structure first
- Add README.md with clear setup instructions
- Include requirements.txt or package.json from the start
- Use modern best practices but don't over-engineer
- Prefer working code over perfect architecture
- Ask clarifying questions if the project idea is vague
- Suggest the simplest solution that works, then iterate

For project scaffolding:
- Create projects in ~/Projects/random-ideas/ by default (or ask for location)
- Always initialize version control (git init)
- Include a .gitignore appropriate for the tech stack
- Set up basic project structure before adding features
- Create a simple "Hello World" or minimal working example first
```

---

## 🚀 Project Commands to Create

Go to **Settings → Rules and Commands → Project Commands** and add these:

### 1. **Scaffold Python Project**
**Command Name:** `scaffold-python`
**Description:** Create a new Python project with virtual environment, requirements.txt, and basic structure

**Command:**
```bash
# Create project directory
PROJECT_NAME="${1:-new-project}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize git
git init
echo "__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
ENV/
.venv
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
*.log" > .gitignore

# Create basic structure
mkdir -p src tests
touch src/__init__.py tests/__init__.py

# Create requirements.txt
echo "# Add your dependencies here" > requirements.txt

# Create main.py
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""Main entry point for the project."""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
EOF

# Create README.md
cat > README.md << EOF
# $PROJECT_NAME

## Description
[Describe your project here]

## Setup

\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
\`\`\`

## Usage

\`\`\`bash
python main.py
\`\`\`
EOF

# Create virtual environment
python3 -m venv venv

echo "✅ Project created at: $PROJECT_DIR"
echo "📁 Next steps:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
```

---

### 2. **Scaffold Node.js/TypeScript Project**
**Command Name:** `scaffold-node`
**Description:** Create a new Node.js/TypeScript project with modern setup

**Command:**
```bash
PROJECT_NAME="${1:-new-project}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize git
git init
echo "node_modules/
dist/
build/
.env
*.log
.DS_Store
coverage/
.nyc_output/" > .gitignore

# Initialize npm
npm init -y

# Create basic structure
mkdir -p src tests

# Create package.json scripts
npm pkg set scripts.dev="node src/index.js"
npm pkg set scripts.start="node src/index.js"
npm pkg set scripts.test="echo 'No tests yet'"

# Create src/index.js
cat > src/index.js << 'EOF'
console.log("Hello, World!");
EOF

# Create README.md
cat > README.md << EOF
# $PROJECT_NAME

## Description
[Describe your project here]

## Setup

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`bash
npm run dev
\`\`\`
EOF

echo "✅ Project created at: $PROJECT_DIR"
echo "📁 Next steps:"
echo "   cd $PROJECT_DIR"
echo "   npm install"
echo "   npm run dev"
```

---

### 3. **Scaffold Web App (HTML/CSS/JS)**
**Command Name:** `scaffold-web`
**Description:** Create a simple web app with HTML, CSS, and JavaScript

**Command:**
```bash
PROJECT_NAME="${1:-new-web-app}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize git
git init
echo ".DS_Store
*.log" > .gitignore

# Create basic HTML
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Web App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
        <button id="clickBtn">Click Me</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
EOF

# Create CSS
cat > styles.css << 'EOF'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
    text-align: center;
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

h1 {
    color: #333;
    margin-bottom: 1rem;
}

button {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s;
}

button:hover {
    background: #5568d3;
}
EOF

# Create JavaScript
cat > script.js << 'EOF'
document.getElementById('clickBtn').addEventListener('click', () => {
    alert('Button clicked!');
});
EOF

# Create README.md
cat > README.md << EOF
# $PROJECT_NAME

## Description
[Describe your web app here]

## Usage

Open \`index.html\` in your browser or use a local server:

\`\`\`bash
python3 -m http.server 8000
# Then visit http://localhost:8000
\`\`\`
EOF

echo "✅ Web app created at: $PROJECT_DIR"
echo "📁 Open index.html in your browser or run:"
echo "   cd $PROJECT_DIR"
echo "   python3 -m http.server 8000"
```

---

### 4. **Quick Project Idea Generator**
**Command Name:** `new-random-project`
**Description:** Interactive command to scaffold a project based on your idea

**Command:**
```bash
echo "🎨 Random Project Generator"
echo ""
read -p "Project name: " PROJECT_NAME
read -p "Project type (python/node/web/other): " PROJECT_TYPE
read -p "Location (default: ~/Projects/random-ideas/): " PROJECT_LOCATION
PROJECT_LOCATION="${PROJECT_LOCATION:-$HOME/Projects/random-ideas}"

PROJECT_DIR="$PROJECT_LOCATION/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

git init

case $PROJECT_TYPE in
    python)
        echo "Setting up Python project..."
        python3 -m venv venv
        touch requirements.txt main.py README.md
        echo "__pycache__/ venv/ *.pyc" > .gitignore
        ;;
    node)
        echo "Setting up Node.js project..."
        npm init -y
        mkdir -p src
        touch src/index.js README.md
        echo "node_modules/ dist/" > .gitignore
        ;;
    web)
        echo "Setting up Web project..."
        touch index.html styles.css script.js README.md
        ;;
    *)
        echo "Creating basic project structure..."
        touch README.md
        ;;
esac

echo ""
echo "✅ Project '$PROJECT_NAME' created at: $PROJECT_DIR"
echo "📝 Edit README.md to describe your idea"
echo "🚀 Start coding!"
```

---

## 📝 Project Rules to Add

Go to **Settings → Rules and Commands → Project Rules** and add:

```
Project Organization:
- All random idea projects should be created in ~/Projects/random-ideas/ (or user-specified location)
- Each project should have: README.md, .gitignore, and basic structure
- Use descriptive project names (kebab-case recommended)

Code Style:
- Python: Use type hints, f-strings, and follow PEP 8
- JavaScript: Use modern ES6+, prefer const/let over var
- Always include error handling for user-facing code
- Add comments for non-obvious logic

Development Workflow:
- Start with minimal working example, then iterate
- Create tests when the project grows beyond a prototype
- Use version control from the start (git init)
- Document setup steps in README.md

When scaffolding:
- Ask for project name and type if not specified
- Confirm location before creating files
- Create a "Hello World" example that actually runs
- Include setup instructions in README
```

---

## 🎯 How to Use These Commands

### In Cursor:
1. Press `Cmd/Ctrl + Shift + P` (Command Palette)
2. Type "Cursor: Run Command"
3. Select your command (e.g., `scaffold-python`)
4. Enter project name when prompted
5. Start coding!

### Or via Chat:
Just say: *"Create a new Python project called 'face-detector' in my random ideas folder"*

I'll use the rules and commands to scaffold it for you.

---

## 💡 Pro Tips

1. **Create a master template folder** at `~/Projects/random-ideas/.templates/` with boilerplate code
2. **Use environment variables** in your commands: `$HOME/Projects/random-ideas/`
3. **Add aliases** to your shell config for quick access:
   ```bash
   alias newpy='cursor-command scaffold-python'
   alias newweb='cursor-command scaffold-web'
   ```
4. **Keep a project ideas list** in a markdown file for inspiration
5. **Set up a default project structure** you like and reuse it

---

## 🔧 Customization

### Change Default Location
Edit the commands above and replace:
```bash
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
```
With your preferred location:
```bash
PROJECT_DIR="/path/to/your/projects/$PROJECT_NAME"
```

### Add More Project Types
Create commands for:
- React/Vue/Angular apps
- Flask/FastAPI backends
- Docker projects
- Data science projects (Jupyter notebooks)
- CLI tools
- Mobile apps

---

## 📚 Example Workflow

1. **You have an idea:** "I want to build a URL shortener"
2. **In Cursor chat:** "Create a new Python project called 'url-shortener'"
3. **I scaffold it** with Flask, basic structure, requirements.txt
4. **You start coding** immediately without setup friction
5. **Iterate quickly** with working code

---

## 🎨 Advanced: Create Your Own Commands

Commands are just shell scripts. You can:
- Combine multiple tools
- Add interactive prompts
- Integrate with APIs
- Auto-deploy to services
- Generate boilerplate code

Example: A command that creates a project AND opens it in Cursor:
```bash
# ... create project ...
cursor "$PROJECT_DIR"
```

---

**Ready to start?** Try creating a command now, or just ask me to scaffold a project for you!
