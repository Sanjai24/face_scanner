# Cursor Quick Start - Copy & Paste Ready

## 🚀 Quick Setup (5 minutes)

### Step 1: Add User Rules
Go to **Settings → Rules and Commands → User Rules** and add:

```
Don't be a bitch

When I ask to create a new project:
- Default location: ~/Projects/random-ideas/
- Always create: README.md, .gitignore, basic structure
- Initialize git repo
- Create a minimal working example first
- Ask for project name and type if not specified
- Use modern best practices but keep it simple
```

### Step 2: Add Project Commands
Go to **Settings → Rules and Commands → Project Commands → + Add Command**

#### Command 1: `new-python-project`
**Name:** `new-python-project`  
**Description:** Create a Python project with venv

**Command:**
```bash
PROJECT_NAME="${1:-new-project}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR" && cd "$PROJECT_DIR" && git init && \
echo "__pycache__/
*.pyc
venv/
env/
.venv
*.egg-info/
dist/
build/" > .gitignore && \
python3 -m venv venv && \
cat > main.py << 'EOF'
#!/usr/bin/env python3
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
EOF
cat > requirements.txt << 'EOF'
# Add dependencies here
EOF
cat > README.md << EOF
# $PROJECT_NAME

## Setup
\`\`\`bash
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Run
\`\`\`bash
python main.py
\`\`\`
EOF
echo "✅ Created at: $PROJECT_DIR"
```

#### Command 2: `new-web-project`
**Name:** `new-web-project`  
**Description:** Create a simple web app

**Command:**
```bash
PROJECT_NAME="${1:-new-web-app}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR" && cd "$PROJECT_DIR" && git init && \
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
    </div>
    <script src="script.js"></script>
</body>
</html>
EOF
cat > style.css << 'EOF'
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: system-ui, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.container {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
EOF
cat > script.js << 'EOF'
console.log("Hello, World!");
EOF
cat > README.md << EOF
# $PROJECT_NAME

Open \`index.html\` in your browser or run:
\`\`\`bash
python3 -m http.server 8000
\`\`\`
EOF
echo "✅ Created at: $PROJECT_DIR"
```

#### Command 3: `new-node-project`
**Name:** `new-node-project`  
**Description:** Create a Node.js project

**Command:**
```bash
PROJECT_NAME="${1:-new-node-app}"
PROJECT_DIR="$HOME/Projects/random-ideas/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR" && cd "$PROJECT_DIR" && git init && \
echo "node_modules/
dist/
.env
*.log" > .gitignore && \
npm init -y && \
mkdir -p src && \
cat > src/index.js << 'EOF'
console.log("Hello, World!");
EOF
npm pkg set scripts.start="node src/index.js" && \
npm pkg set scripts.dev="node src/index.js" && \
cat > README.md << EOF
# $PROJECT_NAME

## Setup
\`\`\`bash
npm install
\`\`\`

## Run
\`\`\`bash
npm start
\`\`\`
EOF
echo "✅ Created at: $PROJECT_DIR"
```

### Step 3: Add Project Rules
Go to **Settings → Rules and Commands → Project Rules → + Add Rule**

```
Default project location: ~/Projects/random-ideas/
Always create: README.md, .gitignore, git repo
Start with minimal working example
Use modern best practices
Ask for clarification if project idea is vague
```

---

## 🎯 How to Use

### Option 1: Via Command Palette
1. Press `Cmd/Ctrl + Shift + P`
2. Type "Cursor: Run Command"
3. Select `new-python-project` (or web/node)
4. Enter project name
5. Done!

### Option 2: Via Chat
Just say:
- *"Create a Python project called 'todo-app'"`
- *"Scaffold a web app named 'calculator'"`
- *"New Node.js project 'api-server'"`

I'll use your rules and commands to create it!

---

## 📝 Customize Location

To change the default location from `~/Projects/random-ideas/`:

1. Edit the commands above
2. Replace `$HOME/Projects/random-ideas/` with your path
3. Update the User Rules and Project Rules

Example for `/home/justdial/Projects/`:
```bash
PROJECT_DIR="/home/justdial/Projects/$PROJECT_NAME"
```

---

## 💡 Pro Tips

1. **Create the directory first:**
   ```bash
   mkdir -p ~/Projects/random-ideas
   ```

2. **Test a command:**
   - Run it once manually to verify it works
   - Adjust paths/commands as needed

3. **Add more project types:**
   - Copy an existing command
   - Modify for your needs (React, Flask, etc.)

4. **Use environment variables:**
   - `$HOME` for home directory
   - `$USER` for username
   - Custom vars in your shell config

---

## 🚀 Example Workflow

**You:** "I want to build a password generator"  
**Me:** "Creating Python project 'password-generator'..."  
**Result:** Project ready with venv, README, structure  
**You:** Start coding immediately!

---

**That's it!** You're ready to rapidly prototype ideas. 🎉
