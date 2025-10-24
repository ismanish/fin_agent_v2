# Deployment Guide for Financial AQRR Application

## Railway Deployment Instructions

### Prerequisites
- GitHub account with the repository forked/cloned
- Railway account (https://railway.app)
- API keys for OpenAI, Finnhub, and SEC-API services

### Environment Variables Required

Create these environment variables in Railway:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=2048
OPENAI_TEMPERATURE=0.0

# SEC API Configuration
SEC_API_KEY=your_sec_api_key_here

# Finnhub Configuration
FINNHUB_API_KEY=your_finnhub_api_key_here

# Application Configuration
PORT=9259
```

### Step-by-Step Deployment

1. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Log in to Railway (https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Python application

3. **Configure Environment Variables**
   - Go to your project settings in Railway
   - Click on "Variables"
   - Add all the environment variables listed above
   - Save the configuration

4. **Configure Build Settings**
   - Railway should auto-detect the Python buildpack
   - The start command will be: `uvicorn app:app --host 0.0.0.0 --port $PORT`

5. **Initial Data Setup**
   After deployment, you need to:
   - Generate the FAISS index by running: `python src/on_demand_insights/document_processor.py`
   - This creates the vector store for the RAG pipeline

### Post-Deployment Tasks

1. **Test the Application**
   - Access your Railway-provided URL
   - Login with test credentials
   - Generate an AQRR report for a test ticker (e.g., ELME, STAG)

2. **Monitor Logs**
   - Check Railway logs for any errors
   - Ensure all API connections are working

### Known Issues and Solutions

1. **PDF Preview Issue on Railway**
   - The application uses a dedicated API endpoint `/api/v1/pdf/{ticker}` for PDF serving
   - This should work on Railway, but if issues persist, PDFs can still be downloaded

2. **FAISS Index Missing (On Demand Insights)**
   - The FAISS index (46MB) is not included in Git for size reasons
   - On Demand Insights will show "being set up" message until index is created
   - **Solution**: The index will be automatically generated during build if documents are available
   - **Note**: ODI requires SEC filings to be present in the data folder to generate embeddings
   - If ODI is critical, consider using Railway's persistent volumes to store the index

3. **Data Lineage Token Limit**
   - If you see "rate limit exceeded" errors with Data Lineage
   - The app now truncates context to 40,000 characters (well under OpenAI's 30,000 TPM limit)
   - This has been fixed in the latest version

4. **Memory Issues**
   - If you encounter memory issues, consider upgrading your Railway plan
   - The FAISS index requires ~100MB of memory

### Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual keys

# Run the application
python app.py
```

Access at: http://localhost:9259

### API Endpoints

- `/` - Main dashboard
- `/api/v1/aqrr-pdf-word` - Generate AQRR reports (PDF and Word)
- `/api/v1/odi/chat/message` - On Demand Insights chat
- `/api/v1/comparables` - Get comparable companies
- `/api/v1/pdf/{ticker}` - Serve PDF files (Railway-compatible)

### Support

For issues or questions, please check:
- Railway documentation: https://docs.railway.app
- Application logs in Railway dashboard
- GitHub issues for this repository

