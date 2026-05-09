#!/bin/bash

echo "🔍 Pre-Deployment Verification"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check functions
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not installed"
        return 1
    fi
}

# Check required files
echo "📁 Checking required files..."
check_file "app.py"
check_file "requirements.txt"
check_file "Dockerfile"
check_file "Procfile"
check_file "templates/index.html"
echo ""

# Check deployment configs
echo "⚙️ Checking deployment configs..."
check_file "railway.toml"
check_file "render.yaml"
check_file "fly.toml"
check_file "runtime.txt"
check_file ".dockerignore"
echo ""

# Check documentation
echo "📚 Checking documentation..."
check_file "DEPLOYMENT_GUIDE.md"
check_file "DEPLOY_README.md"
check_file "CLEANUP_SYSTEM.md"
echo ""

# Check tools
echo "🔧 Checking required tools..."
check_command "git"
check_command "python"
check_command "docker"
echo ""

# Check Python dependencies
echo "📦 Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "Dependencies in requirements.txt:"
    cat requirements.txt
    echo ""
fi

# Check git status
echo "📊 Checking git status..."
if [ -d .git ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"
    
    # Check if there are uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠${NC} You have uncommitted changes"
        echo "Run: git add . && git commit -m 'Ready for deployment'"
    else
        echo -e "${GREEN}✓${NC} All changes committed"
    fi
    
    # Check if remote is set
    if git remote -v | grep -q origin; then
        echo -e "${GREEN}✓${NC} Git remote configured"
        git remote -v
    else
        echo -e "${YELLOW}⚠${NC} No git remote configured"
        echo "Run: git remote add origin <your-repo-url>"
    fi
else
    echo -e "${RED}✗${NC} Git not initialized"
    echo "Run: git init"
fi
echo ""

# Test Docker build (optional)
echo "🐳 Docker build test..."
read -p "Test Docker build? (y/n): " test_docker
if [ "$test_docker" = "y" ]; then
    echo "Building Docker image..."
    docker build -t whatsapp-converter-test . 
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Docker build successful"
    else
        echo -e "${RED}✗${NC} Docker build failed"
    fi
fi
echo ""

# Summary
echo "=============================="
echo "📋 Verification Summary"
echo "=============================="
echo ""
echo "Next steps:"
echo "1. Fix any issues marked with ✗"
echo "2. Commit all changes if needed"
echo "3. Push to GitHub"
echo "4. Deploy to your chosen platform"
echo ""
echo "Quick deploy commands:"
echo "  Railway: ./deploy.sh (choose option 1)"
echo "  Render:  ./deploy.sh (choose option 2)"
echo "  Fly.io:  ./deploy.sh (choose option 3)"
echo ""
echo "Or manually:"
echo "  git push origin main"
echo "  Then deploy on platform dashboard"
echo ""
