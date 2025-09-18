# GitHub Deployment Setup Guide

## Automated Deployment to Render

This guide sets up automated deployment from GitHub to Render when pushing to the main branch.

### Step 1: Configure Render Service

1. Log in to [Render](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository: `pudingtabi/mynfini`
4. Configure the service:
   - Name: `mynfini-ttrpg`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT web_app:app`
   - Environment Variables (add these in Render dashboard):
     - `SYNTHETIC_NEW_API_KEY`: Your Synthetic.new API key
     - `KIMI_K2_API_KEY`: Your Kimi K2 API key
     - `SECRET_KEY`: A strong secret key for Flask
     - `DEBUG`: Set to "false" for production

### Step 2: Get Render API Credentials

1. In Render, go to Account Settings → API Keys
2. Create a new API Key
3. Note down the Service ID for your web service
4. The Service ID is in the URL when viewing your service: `https://dashboard.render.com/web/srv-[SERVICE_ID]`

### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository: https://github.com/pudingtabi/mynfini
2. Navigate to Settings → Secrets and variables → Actions
3. Add these secrets:
   - `RENDER_API_KEY`: Your Render API key from Step 2
   - `RENDER_SERVICE_ID`: Your service ID from Step 2

### Step 4: Test Deployment

1. Push changes to the main branch
2. GitHub Actions will automatically:
   - Run basic tests to ensure code integrity
   - Trigger deployment to Render
3. Monitor deployment status in GitHub Actions tab
4. Check your app at the Render URL provided

### Manual Deployment

If needed, you can also manually deploy:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Troubleshooting

1. **Build Fails**: Check Render logs in the dashboard
2. **Environment Variables**: Ensure all API keys are set correctly
3. **Port Issues**: The app uses Render's $PORT environment variable
4. **Dependencies**: Ensure requirements.txt includes all necessary packages

### Required Environment Variables

Make sure these are set in Render dashboard:
- `SYNTHETIC_NEW_API_KEY`: For AI narrative generation
- `KIMI_K2_API_KEY`: For Kimi K2 AI provider
- `SECRET_KEY`: Strong random string for Flask sessions
- `DEBUG`: "false" for production
- `AI_PROVIDERS`: "synthetic_new,kimi_k2" (optional)

### Next Steps

After successful deployment:
1. Test the web interface at your Render URL
2. Configure any additional API providers in the dashboard
3. Set up monitoring and logging as needed