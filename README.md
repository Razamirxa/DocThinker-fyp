# Integrated RAG-based Academic Assistant

A full-stack web application combining a modern React frontend with a powerful FastAPI backend integrated with a Retrieval-Augmented Generation (RAG) system for academic question answering.

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 + Vite
- **UI**: TailwindCSS with custom theme system
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Features**: Authentication, Chat with RAG, Document Management, Analytics Dashboard

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **RAG Engine**:
  - **Vector Store**: Pinecone
  - **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
  - **LLM**: Google Gemini Pro
  - **Framework**: LangChain
  - **Subjects**: Linear Algebra, Discrete Structures, Calculus

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Pinecone account
- Google AI Studio account

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your credentials

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

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

## 🛠️ Project Structure

```
RaG-based-system-main/
├── backend/
│   ├── main.py              # FastAPI app
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
