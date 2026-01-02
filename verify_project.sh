#!/bin/bash
echo "🔍 Verifying Malaysian IPTV Project..."
echo ""

# Check files
FILES=(
    "README.md"
    "QUICKSTART.md"
    "CONTRIBUTING.md"
    "requirements.txt"
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    ".gitignore"
    ".env.example"
    "run.py"
    "setup.sh"
    "test_app.py"
    "app/main.py"
    "app/__init__.py"
    "data/example_channels.m3u8"
)

echo "📄 Checking required files..."
missing=0
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        ((missing++))
    fi
done

echo ""
echo "📁 Checking directory structure..."
DIRS=(
    "app/api"
    "app/core"
    "app/models"
    "app/parsers"
    "app/services"
    "app/static/css"
    "app/static/js"
    "app/templates"
    "data"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ $dir/ (missing)"
        ((missing++))
    fi
done

echo ""
echo "🐍 Checking Python files..."
python_files=$(find app -name "*.py" | wc -l)
echo "  Found $python_files Python files"

echo ""
echo "📊 Summary:"
if [ $missing -eq 0 ]; then
    echo "  ✅ All required files and directories present!"
    echo "  🚀 Project is ready to use!"
    exit 0
else
    echo "  ⚠️  $missing files/directories missing"
    exit 1
fi
