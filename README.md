# DocThinker - AI-Powered Academic Assistant 🎓

An intelligent RAG-based chatbot for academic subjects including **Linear Algebra**, **Discrete Mathematics**, and **Calculus**. Built with FastAPI backend and modern React frontend.

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 + Vite
- **UI**: TailwindCSS with custom theme system
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Features**: Real-time chat, Authentication, Analytics Dashboard

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **RAG Engine**:
  - **Vector Store**: Pinecone (semester-books index)
  - **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
  - **LLM**: Google Gemini 2.5 Flash
  - **Framework**: LangChain
  - **Supported Subjects**: Linear Algebra, Discrete Structures, Calculus & Analytical Geometry

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.13+** installed
- **Node.js 18+** and npm
- **PostgreSQL 15+** installed and running
- **UV** (Python package manager) - Install: `pip install uv`
- **Git** for cloning the repository
- **VS Code** (recommended) or any code editor

### Required Accounts & API Keys
- [Google AI Studio](https://makersuite.google.com/app/apikey) - For Gemini API key
- [Pinecone](https://www.pinecone.io/) - For vector database

## 🚀 Complete Setup Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Razamirxa/DocThinker-fyp.git

# Navigate to project directory
cd DocThinker-fyp

# Open in VS Code
code .
```

### Step 2: Backend Setup with UV

```bash
# Navigate to project root
cd DocThinker-fyp

# Create UV virtual environment
uv venv

# Activate the environment
# Windows PowerShell:
.venv\Scripts\activate

# Linux/Mac:
# source .venv/bin/activate

# Install all dependencies using uv sync
uv sync

# Navigate to backend directory
cd backend

# Create .env file from example
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### Step 3: Configure Environment Variables

Edit `backend/.env` file with your credentials:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fyp_db

# JWT Secret Key (generate a secure random string)
SECRET_KEY=your_secure_secret_key_here

# RAG Engine API Keys
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key

# RAG Configuration
DEFAULT_RAG_MODEL=gemini-2.5-flash
PINECONE_INDEX_NAME=semester-books
```

### Step 4: Setup PostgreSQL Database

```bash
# Open PostgreSQL command line (psql)
psql -U postgres

# Create database
CREATE DATABASE fyp_db;

# Exit psql
\q
```

### Step 5: Setup Pinecone Index

1. Log in to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with these settings:
   - **Name**: `semester-books`
   - **Dimensions**: `384`
   - **Metric**: `cosine`
3. Copy your API key to `.env` file

### Step 6: Start Backend Server

```bash
# Make sure you're in the backend directory with activated virtual environment
cd backend

# Start FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Server will start at: http://localhost:8000
# API Docs available at: http://localhost:8000/docs
```

### Step 7: Frontend Setup

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will start at: http://localhost:5173
```

## 🎯 First Time Usage

1. **Open Browser**: Navigate to `http://localhost:5173`
2. **Create Account**: Click "Sign Up" and create your account (first user will be admin)
3. **Login**: Use your credentials to login
4. **Start Chatting**: 
   - Ask questions directly in the chat
   - Examples: "What are eigenvalues?", "Explain graph theory", "What is calculus?"
5. The RAG engine auto-initializes on startup using your API keys!

## 🔑 Required API Keys

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Get your API key
3. Add to `.env`: `GOOGLE_API_KEY=your_key`

### Pinecone
1. Visit [Pinecone](https://www.pinecone.io/)
2. Create account and get API key
3. Create index named `semester-books` (dimension: 384, metric: cosine)
4. Add to `.env`: `PINECONE_API_KEY=your_key`

## 📚 Key Features

### Current
- ✅ User authentication & authorization
- ✅ RAG-based question answering
- ✅ Multi-subject support (Math, CS, Calculus)
- ✅ Document management
- ✅ Analytics dashboard
- ✅ Real-time chat interface
- ✅ Source citation

### Upcoming
- 🔄 Document upload to Pinecone
- 🔄 Streaming responses
- 🔄 Voice input/output
- 🔄 Chat history

## 📊 API Endpoints

### Authentication
- `POST /api/signup` - Register
- `POST /api/login` - Login
- `GET /api/profile` - Get profile

### RAG
- `POST /api/rag/initialize` - Initialize RAG engine (Admin)
- `POST /api/rag/chat` - Ask questions
- `GET /api/rag/status` - Engine status
- `GET /api/rag/subjects` - Available subjects

See `http://localhost:8000/docs` for full API documentation.

## 🎯 Usage Examples

### Initialize RAG Engine (First Time Only)

```bash
curl -X POST http://localhost:8000/api/rag/initialize \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "google_api_key": "YOUR_GOOGLE_KEY",
    "pinecone_api_key": "YOUR_PINECONE_KEY",
    "model_name": "gemini-1.5-pro"
  }'
```

### Example Questions

**Linear Algebra:**
- "What are eigenvalues and eigenvectors?"
- "How do I solve a system of linear equations?"

**Discrete Structures:**
- "Explain mathematical induction"
- "What is a graph in discrete math?"

**Calculus:**
- "How do I find derivatives?"
- "Explain integration by parts"

## � Quick Commands Reference

```bash
# Setup (one-time)
git clone https://github.com/Razamirxa/DocThinker-fyp.git
cd DocThinker-fyp
uv venv
.venv\Scripts\activate
uv sync

# Backend (in terminal 1)
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in terminal 2)
cd frontend
npm install
npm run dev
```

## 🛠️ Project Structure

```
DocThinker-fyp/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── rag_engine.py        # RAG core logic
│   ├── rag_engine.py        # RAG core
│   ├── config.py            # Settings
│   ├── requirements.txt     # Dependencies
│   ├── routes/              # API routes
│   └── database/            # DB schema
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── components/      # Reusable components
│   │   └── services/        # API calls
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔧 Troubleshooting

**RAG Not Initialized**: Call `/api/rag/initialize` with valid keys

**Database Error**: Check PostgreSQL is running and credentials in `.env`

**CORS Issues**: Verify frontend URL in `backend/config.py` CORS_ORIGINS

**Pinecone Errors**: Ensure index dimension is 384 (matches embedding model)

## 📝 Environment Variables

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=fyp_db

# Security
SECRET_KEY=your_secret_key

# RAG
GOOGLE_API_KEY=your_google_key
PINECONE_API_KEY=your_pinecone_key
DEFAULT_RAG_MODEL=gemini-1.5-pro
PINECONE_INDEX_NAME=semester-books
```

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push and create PR

## 📞 Support

For issues: Open a GitHub issue

## 👥 Credits

- Frontend: RaG-based-system-main
- RAG Backend: academic-rag-assistant-master
- Built with: LangChain, Pinecone, Google Gemini, FastAPI, React

---

**Note**: Academic project. Monitor API usage and rate limits for Google AI and Pinecone.
