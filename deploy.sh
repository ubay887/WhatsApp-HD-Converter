#!/bin/bash

echo "🚀 WhatsApp HD Converter - Quick Deploy Script"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Ready for deployment"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "Choose deployment platform:"
echo "1. Railway (Recommended)"
echo "2. Render"
echo "3. Fly.io"
echo "4. Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "Steps:"
        echo "1. Push code to GitHub"
        echo "2. Go to https://railway.app"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Select your repository"
        echo "5. Wait for deployment"
        echo "6. Generate domain in Settings"
        echo ""
        read -p "Push to GitHub now? (y/n): " push
        if [ "$push" = "y" ]; then
            read -p "Enter GitHub repo URL: " repo_url
            git remote add origin $repo_url
            git branch -M main
            git push -u origin main
            echo "✅ Code pushed to GitHub!"
            echo "Now go to Railway and deploy from GitHub"
        fi
        ;;
    2)
        echo ""
        echo "🎨 Deploying to Render..."
        echo ""
        echo "Steps:"
        echo "1. Push code to GitHub"
        echo "2. Go to https://render.com"
        echo "3. Click 'New' → 'Web Service'"
        echo "4. Connect GitHub repository"
        echo "5. Select 'Docker' environment"
        echo "6. Click 'Create Web Service'"
        echo ""
        read -p "Push to GitHub now? (y/n): " push
        if [ "$push" = "y" ]; then
            read -p "Enter GitHub repo URL: " repo_url
            git remote add origin $repo_url
            git branch -M main
            git push -u origin main
            echo "✅ Code pushed to GitHub!"
            echo "Now go to Render and deploy from GitHub"
        fi
        ;;
    3)
        echo ""
        echo "✈️ Deploying to Fly.io..."
        echo ""
        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo "Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
        fi
        
        echo "Logging in to Fly.io..."
        flyctl auth login
        
        echo "Launching app..."
        flyctl launch --no-deploy
        
        echo "Deploying..."
        flyctl deploy
        
        echo "✅ Deployed to Fly.io!"
        flyctl open
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo ""
echo "Next steps:"
echo "1. Test your deployment"
echo "2. Check logs for any errors"
echo "3. Setup custom domain (optional)"
echo "4. Monitor usage"
echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"
