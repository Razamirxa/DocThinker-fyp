# Setup Guide - Integrated RAG Academic Assistant

This guide will help you set up and run the integrated RAG-based academic assistant system.

## 📋 What You Need

Before starting, make sure you have:

1. **Software Installed:**
   - Python 3.12 or higher
   - Node.js 18 or higher
   - PostgreSQL 15 or higher
   - Git

2. **API Keys:**
   - Google Gemini API key
   - Pinecone API key

3. **System Requirements:**
   - At least 4GB RAM
   - 2GB free disk space

## 🚀 Step-by-Step Setup

### Step 1: Get API Keys

#### Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the key (starts with "AIza...")
5. Save it somewhere safe - you'll need it later

#### Pinecone API Key
1. Go to https://www.pinecone.io/
2. Sign up for a free account
3. After logging in, go to "API Keys" in the left sidebar
4. Copy your API key
5. Create a new index:
   - Click "Create Index"
   - Name: `semester-books`
   - Dimensions: `384`
   - Metric: `cosine`
   - Click "Create Index"

### Step 2: Setup Database

#### Windows:
1. Install PostgreSQL from https://www.postgresql.org/download/windows/
2. During installation, remember the password you set for the `postgres` user
3. Open pgAdmin or SQL Shell (psql)
4. Create the database:
   ```sql
   CREATE DATABASE fyp_db;
   ```

#### Linux/Mac:
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian
# or
brew install postgresql  # Mac

# Start PostgreSQL service
sudo service postgresql start  # Linux
# or
brew services start postgresql  # Mac

# Create database
sudo -u postgres psql
CREATE DATABASE fyp_db;
\q
```

### Step 3: Setup Backend

1. **Navigate to Backend Directory:**
   ```bash
   cd "e:\Projects\students fyp\sidiqa hts\fyp-rag\RaG-based-system-main\backend"
   ```

2. **Create Virtual Environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will take a few minutes as it installs all necessary packages including:
   - FastAPI
   - LangChain
   - Pinecone client
   - Google Generative AI
   - And many more...

4. **Configure Environment:**
   ```bash
   # Copy example env file
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   ```

5. **Edit .env File:**
   Open `.env` in a text editor and fill in your details:
   ```env
   # Database
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=fyp_db

   # Security
   SECRET_KEY=change-this-to-a-random-secret-key

   # RAG Engine
   GOOGLE_API_KEY=your_google_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   DEFAULT_RAG_MODEL=gemini-1.5-pro
   PINECONE_INDEX_NAME=semester-books
   ```

6. **Start Backend Server:**
   ```bash
   # Make sure virtual environment is activated
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

7. **Test Backend:**
   Open browser and go to: http://localhost:8000/docs
   You should see the FastAPI Swagger documentation.

### Step 4: Setup Frontend

1. **Open New Terminal** (keep backend running)

2. **Navigate to Frontend Directory:**
   ```bash
   cd "e:\Projects\students fyp\sidiqa hts\fyp-rag\RaG-based-system-main\frontend"
   ```

3. **Install Dependencies:**
   ```bash
   npm install
   ```
   
   This will install React, Vite, TailwindCSS, and other frontend dependencies.

4. **Start Development Server:**
   ```bash
   npm run dev
   ```

   You should see:
   ```
   VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ➜  press h + enter to show help
   ```

5. **Open Application:**
   Open your browser and go to: http://localhost:5173

### Step 5: First Time Setup

1. **Create Admin Account:**
   - Click "Sign Up"
   - Fill in your details
   - Email: your-email@example.com
   - Password: (choose a strong password)
   - Name: Your Name
   - Role: Admin
   - Click "Sign Up"

2. **Login:**
   - Use your email and password to login

3. **Initialize RAG Engine:**
   You have two options:

   **Option A: Via API (Recommended)**
   Open a new terminal and run:
   ```bash
   # Get your token from browser (F12 -> Application -> Local Storage -> token)
   
   curl -X POST http://localhost:8000/api/rag/initialize ^
     -H "Authorization: Bearer YOUR_TOKEN" ^
     -H "Content-Type: application/json" ^
     -d "{\"google_api_key\": \"YOUR_GOOGLE_KEY\", \"pinecone_api_key\": \"YOUR_PINECONE_KEY\", \"model_name\": \"gemini-1.5-pro\"}"
   ```

   **Option B: Modify Backend Config**
   Edit `backend/config.py` to use environment variables (already done if you set up .env correctly).

4. **Test the System:**
   - Go to Chat page
   - Type a question like: "What are eigenvalues?"
   - You should get a detailed response with sources!

## ✅ Verification Checklist

Check that everything is working:

- [ ] Backend server running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] PostgreSQL database is accessible
- [ ] Can signup and login
- [ ] RAG engine initialized successfully
- [ ] Can ask questions and get responses
- [ ] Responses include source citations

## 🔧 Common Issues & Solutions

### Issue: "Module not found" errors
**Solution:** Make sure virtual environment is activated and all dependencies are installed:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Connection refused" to database
**Solution:** 
1. Check PostgreSQL is running
2. Verify credentials in `.env` file
3. Make sure database `fyp_db` exists

### Issue: "RAG engine not initialized"
**Solution:** 
1. Check API keys are correct in `.env`
2. Call the `/api/rag/initialize` endpoint
3. Check backend logs for errors

### Issue: CORS errors in browser
**Solution:**
1. Check that `http://localhost:5173` is in `CORS_ORIGINS` in `backend/config.py`
2. Restart backend server

### Issue: Pinecone dimension mismatch
**Solution:**
Make sure your Pinecone index has dimension set to `384` (not 1536 or other values)

### Issue: Port already in use
**Solution:**
```bash
# For port 8000 (backend)
# Find and kill the process using the port

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## 📚 Next Steps

After successful setup:

1. **Explore the Application:**
   - Try different types of questions
   - Check the analytics dashboard
   - Update your profile
   - Upload documents (coming soon)

2. **Customize:**
   - Modify themes in frontend
   - Add new subjects to RAG engine
   - Customize prompts in `rag_engine.py`

3. **Deploy:**
   - See `DEPLOYMENT.md` for production deployment guide
   - Configure environment variables for production
   - Set up proper database backups

## 🆘 Getting Help

If you encounter issues:

1. Check the logs:
   - Backend: Terminal where uvicorn is running
   - Frontend: Browser console (F12)

2. Verify environment variables are set correctly

3. Make sure all services (PostgreSQL, Backend, Frontend) are running

4. Check API documentation at http://localhost:8000/docs

5. Review error messages carefully - they usually point to the issue

## 🎉 Success!

If you've reached this point and everything is working, congratulations! You now have a fully functional RAG-based academic assistant.

### Quick Test:
1. Go to http://localhost:5173
2. Login with your account
3. Navigate to Chat page
4. Ask: "Explain eigenvalues and eigenvectors in simple terms"
5. You should get a detailed, sourced response!

---

For more information, see `README.md` for full documentation.
