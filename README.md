# Humanizer

A free AI writing workspace for rewriting drafts and estimating AI-like patterns. Inspired by publicly available AI writing tools, with all features accessible without payment.

## Features

- **AI Humanizer**: Rewrite AI-generated text into natural language with adjustable intensity and profiles
- **AI Detector**: Estimate how AI-like text reads with quick and deep analysis modes
- **Writing Tools**: Rewriter, Paraphraser, Essay Rewriter, Article Rewriter, Sentence Rewriter, Paragraph Rewriter, Content Improvement, Grammar Check
- **Workspace**: Save, manage, and retrieve documents (requires sign-in)
- **Multiple Rewrite Profiles**: Swift, Studio, Careful, and Plain modes
- **Language Support**: English, Spanish, French, German, Italian, Portuguese
- **Export Options**: Copy to clipboard, download as TXT, download as DOCX
- **Dark/Light Theme**: Toggle between themes
- **100% Free**: No subscriptions, no payments, no word limits

## Tech Stack

### Frontend
- Vue.js 3 with TypeScript
- Vite
- Tailwind CSS
- Pinia (state management)
- Vue Router
- Axios

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- Pydantic
- SQLite (development) / PostgreSQL (production)
- Alembic (migrations)

### AI Integration
- Provider-independent architecture
- Supports OpenAI, Anthropic, and Ollama
- Configurable via environment variables

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
```bash
# Copy the example .env file
cd ..
cp .env.example .env
```

6. Edit `.env` and add your AI provider credentials:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

7. Start the backend server:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Configuration

### Environment Variables

See `.env.example` for all available configuration options:

- `AI_PROVIDER`: Choose between `openai`, `anthropic`, or `ollama`
- `OPENAI_API_KEY`: Your OpenAI API key (or OpenAI-compatible endpoint)
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `DATABASE_URL`: Database connection string (SQLite for local, PostgreSQL for production)
- `CORS_ORIGINS`: Allowed frontend origins
- `MAX_INPUT_CHARS`: Maximum input character limit (abuse protection)
- `RATE_LIMIT_WRITES`: Rate limit for write operations

### Using Ollama (Local AI)

To use Ollama for local AI processing:

1. Install Ollama from https://ollama.ai
2. Start Ollama: `ollama serve`
3. Pull a model: `ollama pull llama3.1`
4. Configure `.env`:
```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.1
```

## Project Structure

```
Humanizer/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── api.py           # API endpoints
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── security.py      # Authentication
│   │   ├── rate_limit.py    # Rate limiting
│   │   └── services/        # Business logic
│   │       ├── ai_provider.py    # AI provider abstraction
│   │       ├── detection.py      # AI detection
│   │       ├── documents.py      # Document management
│   │       ├── text_utils.py      # Text utilities
│   │       └── writing.py         # Writing operations
│   ├── alembic/              # Database migrations
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend Docker config
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── views/           # Page components
│   │   ├── stores/           # Pinia stores
│   │   ├── router/           # Vue Router
│   │   ├── api/              # API client
│   │   └── main.ts           # Frontend entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite config
│   └── tailwind.config.js    # Tailwind config
├── .env.example              # Environment template
├── FEATURES.md               # Feature documentation
└── README.md                 # This file
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

### Frontend (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Build frontend: `cd frontend && npm run build`
3. Deploy: `vercel`

### Backend (Render)

1. Create a new web service on Render
2. Connect your GitHub repository
3. Configure environment variables
4. Deploy using the included `render.yaml`

### Database (Neon)

1. Create a Neon PostgreSQL database
2. Update `DATABASE_URL` in environment variables
3. Run migrations: `alembic upgrade head`

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Important Notes

- **AI Detection is Probabilistic**: The AI detector provides estimates, not definitive proof of authorship. Results can produce false positives and false negatives.
- **Review Content**: Always review rewritten content for factual accuracy, especially with citations and technical details.
- **Rate Limiting**: A rate limit is applied to prevent abuse, but this is not a paid quota—it applies equally to all users.
- **Privacy**: Unsaved text is not stored. Only explicitly saved documents are persisted in the database with user isolation.

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

This project was inspired by publicly available AI writing tools. It is an original implementation and does not use proprietary source code, private APIs, or protected branding from any specific service.
