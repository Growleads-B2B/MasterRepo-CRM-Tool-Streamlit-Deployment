# MasterCRM Repo Tool - Railway Deployment Guide

This guide will walk you through deploying your MasterCRM Repo Tool to Railway with Docker support, maintaining your existing Baserow setup exactly as it is.

## Prerequisites

1. A GitHub account
2. A Railway account (sign up at [railway.app](https://railway.app))

## Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Push your code to the repository:

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for Railway deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy to Railway

### Option 1: Using Railway Web Interface (Easiest)

1. Go to [railway.app](https://railway.app) and log in with your GitHub account
2. Click on "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository from the list
5. Railway will automatically detect your Dockerfile and deploy your application
6. Once deployment is complete, click on "Settings" and go to "Networking"
7. Generate a public domain to access your application

### Option 2: Using Railway CLI

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Log in to Railway:
```bash
railway login
```

3. Link your project:
```bash
railway link
```

4. Deploy your application:
```bash
railway up
```

## Step 3: Configure Your Application

1. Go to your project on Railway dashboard
2. Click on "Variables" tab
3. Add any environment variables if needed (usually not required as we're using the Docker setup)
4. Under "Settings" → "Networking", generate a domain to access your application

## Step 4: Access Your Application

1. Once deployment is complete, Railway will provide you with a URL
2. Open the URL in your browser to access your MasterCRM Repo Tool
3. The first time you access it, Baserow will need to be set up:
   - Create an admin account in Baserow
   - Set up your API token as usual

## Troubleshooting

### Docker-in-Docker Issues

If you encounter issues with Docker running inside Railway's container:

1. Check Railway logs for specific error messages
2. You might need to adjust resource allocations in Railway dashboard
3. Consider using Railway's "Volumes" feature for persistent storage

### Resource Limitations

Railway's free tier provides $5 of usage credits per month. To optimize:

1. Configure your application to use minimal resources
2. Set up auto-shutdown when not in use
3. Monitor your usage in Railway dashboard

## Maintaining Your Application

1. Any changes pushed to your GitHub repository will trigger automatic redeployment
2. You can monitor logs and performance in Railway dashboard
3. For database persistence, ensure you're using Railway's volume feature

## Railway Free Tier Limitations

- $5 of usage credits per month
- Projects spin down after 15 minutes of inactivity
- 512 MB RAM by default (can be adjusted)
- 1 GB of persistent storage

## Need Help?

If you encounter any issues with your Railway deployment, you can:

1. Check [Railway documentation](https://docs.railway.app/)
2. Join [Railway Discord community](https://discord.gg/railway)
3. Contact Railway support through their website
