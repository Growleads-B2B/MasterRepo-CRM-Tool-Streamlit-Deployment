#!/bin/bash

echo "🚂 MasterCRM Repo Tool - Railway Deployment Helper"
echo "=================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm i -g @railway/cli
fi

# Check if git repo is initialized
if [ ! -d ".git" ]; then
    echo "🔄 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
fi

# Use the specific GitHub repository URL
GITHUB_REPO="https://github.com/Growleads-B2B/MasterRepo-CRM-Tool-Deployment.git"

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "🔄 Updating GitHub remote..."
    git remote set-url origin "$GITHUB_REPO"
else
    echo "🔗 Adding GitHub remote..."
    git remote add origin "$GITHUB_REPO"
fi

echo "🚀 Pushing code to GitHub repository: $GITHUB_REPO"
git push -u origin main || git push -u origin master

# Ask if user wants to deploy using Railway CLI
echo ""
echo "🚂 Would you like to deploy to Railway now?"
read -p "Deploy now? (y/n): " deploy_now

if [ "$deploy_now" = "y" ] || [ "$deploy_now" = "Y" ]; then
    # Log in to Railway
    echo "🔑 Please log in to Railway..."
    railway login

    # Create new project
    echo "🏗️ Creating new Railway project..."
    railway init

    # Deploy
    echo "🚀 Deploying to Railway..."
    railway up

    echo ""
    echo "✅ Deployment initiated! Check the Railway dashboard for progress."
    echo "🌐 Once complete, generate a public domain in the Railway dashboard under Settings > Networking."
else
    echo ""
    echo "📝 To deploy later, follow these steps:"
    echo "1. Install Railway CLI: npm i -g @railway/cli"
    echo "2. Log in: railway login"
    echo "3. Link project: railway link"
    echo "4. Deploy: railway up"
    echo ""
    echo "Or deploy through the Railway dashboard: https://railway.app"
fi

echo ""
echo "📚 For detailed instructions, see RAILWAY_DEPLOYMENT_GUIDE.md"
echo ""
