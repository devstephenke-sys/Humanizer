# Draftwell Architecture

This document describes the system architecture of Draftwell, a free AI writing workspace.

## High-Level Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │   Backend       │         │   Database      │
│   (Vue.js)      │◄────────┤   (FastAPI)     │◄────────┤   (PostgreSQL)  │
│                 │  HTTP   │                 │  SQL    │   or SQLite    │
│ - UI Components │         │ - API Endpoints │         │                 │
│ - State Mgmt    │         │ - AI Services   │         │ - Users         │
│ - API Client    │         │ - Auth          │         │ - Documents     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                      │
                                      │ HTTP
                                      ▼
                              ┌─────────────────┐
                              │   AI Provider   │
                              │   (OpenAI/      │
                              │   Anthropic/    │
                              │   Ollama)       │
                              └─────────────────┘
```

## Frontend Architecture

### Technology Stack
- **Framework**: Vue.js 3 with Composition API
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios

### Directory Structure

```
frontend/src/
├── components/          # Reusable Vue components
│   └── Navbar.vue      # Navigation bar with theme toggle
├── views/              # Page-level components
│   ├── Home.vue        # Landing page
│   ├── Humanizer.vue   # AI humanization tool
│   ├── Detector.vue    # AI detection tool
│   ├── Rewriter.vue    # General rewriter
│   ├── Paraphraser.vue # Paraphrasing tool
│   ├── EssayRewriter.vue
│   ├── ArticleRewriter.vue
│   ├── SentenceRewriter.vue
│   ├── ParagraphRewriter.vue
│   ├── ContentImprovement.vue
│   ├── Grammar.vue
│   ├── Workspace.vue   # Document management
│   └── Login.vue       # Authentication
├── stores/             # Pinia stores
│   ├── auth.ts         # Authentication state
│   └── theme.ts        # Theme state
├── router/             # Vue Router configuration
│   └── index.ts
├── api/                # API client and typed interfaces
│   ├── client.ts       # Axios instance
│   ├── writing.ts      # Writing API endpoints
│   ├── auth.ts         # Auth API endpoints
│   └── documents.ts    # Document API endpoints
├── lib/                # Utility libraries
├── types/              # TypeScript type definitions
├── App.vue             # Root component
├── main.ts             # Application entry point
└── style.css           # Global styles with Tailwind
```

### State Management

**Auth Store** (`stores/auth.ts`)
- Manages authentication token
- Manages user information
- Handles login/logout
- Persists to localStorage

**Theme Store** (`stores/theme.ts`)
- Manages dark/light theme
- Persists to localStorage
- Applies theme to document

### API Layer

The API layer provides typed interfaces for all backend endpoints:

- **Client Configuration**: Axios instance with interceptors for auth tokens
- **Writing API**: Rewrite, paraphrase, detect, download
- **Auth API**: Login, register
- **Documents API**: CRUD operations for saved documents

### Component Design Patterns

- **Composition API**: All components use Vue 3 Composition API
- **Reactive State**: `ref()` and `computed()` for reactive data
- **Error Handling**: Try-catch blocks with user-friendly error messages
- **Loading States**: Visual feedback during async operations
- **Form Validation**: Basic validation before API calls

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy (async)
- **Validation**: Pydantic
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Migrations**: Alembic
- **Authentication**: JWT (PyJWT)
- **Rate Limiting**: Custom in-memory implementation

### Directory Structure

```
backend/app/
├── main.py              # FastAPI application factory
├── api.py               # API route definitions
├── config.py            # Configuration management
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic request/response schemas
├── security.py          # Authentication and password hashing
├── rate_limit.py        # Rate limiting middleware
└── services/            # Business logic layer
    ├── ai_provider.py   # AI provider abstraction
    ├── detection.py     # AI detection logic
    ├── documents.py     # Document CRUD operations
    ├── text_utils.py    # Text processing utilities
    └── writing.py       # Writing operations (rewrite, etc.)
```

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         API Layer (api.py)              │
│  - Route definitions                     │
│  - Request validation                   │
│  - Response formatting                  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Service Layer (services/)          │
│  - Business logic                        │
│  - AI provider integration               │
│  - Document management                   │
│  - Text processing                       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│       Data Layer (models.py)            │
│  - SQLAlchemy models                     │
│  - Database operations                  │
└─────────────────────────────────────────┘
```

### Database Models

**User Model**
- `id`: Primary key
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `created_at`: Timestamp

**Document Model**
- `id`: Primary key
- `user_id`: Foreign key to User
- `title`: Document title
- `content`: Document content
- `tool`: Tool used to create document
- `created_at`: Timestamp

### API Endpoints

**Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

**Writing Tools**
- `POST /writing/rewrite` - Rewrite text
- `POST /writing/paraphrase` - Paraphrase text
- `POST /writing/essay-rewrite` - Rewrite essay
- `POST /writing/article-rewrite` - Rewrite article
- `POST /writing/sentence-rewrite` - Rewrite sentences
- `POST /writing/paragraph-rewrite` - Rewrite paragraph
- `POST /writing/content-improve` - Improve content
- `POST /writing/grammar` - Check grammar
- `POST /writing/detect` - Detect AI patterns
- `POST /writing/download-docx` - Download as DOCX

**Documents**
- `GET /documents` - List user's documents
- `POST /documents` - Save new document
- `GET /documents/{id}` - Get specific document
- `DELETE /documents/{id}` - Delete document

### Service Layer

**AI Provider Service** (`services/ai_provider.py`)
- Provider-agnostic interface
- Supports OpenAI, Anthropic, Ollama
- Handles API errors and retries
- Manages prompts for different tools

**Detection Service** (`services/detection.py`)
- Probabilistic AI detection
- Linguistic pattern analysis
- Sentence-level scoring
- Mode selection (quick/deep)

**Writing Service** (`services/writing.py`)
- Orchestrates text rewriting
- Manages intensity levels
- Handles different profiles
- Supports multiple languages

**Document Service** (`services/documents.py`)
- CRUD operations
- User isolation
- Query optimization

### Security

**Authentication**
- JWT-based authentication
- Bcrypt password hashing
- Token expiration (7 days default)
- Protected routes require valid token

**Rate Limiting**
- In-memory rate limiter
- Configurable limits per endpoint
- Sliding window algorithm
- Applied equally to all users

**Input Validation**
- Pydantic schemas for all inputs
- Maximum input size (60,000 chars)
- Email validation
- SQL injection prevention (ORM)

**CORS**
- Configurable allowed origins
- Credentials support
- Appropriate headers

## AI Integration Architecture

### Provider Abstraction

The AI provider is abstracted behind a common interface:

```python
class AIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
```

### Supported Providers

**OpenAI**
- Compatible with OpenAI API
- Also works with OpenRouter, Groq, Together
- Configurable base URL and model

**Anthropic**
- Native Anthropic API support
- Claude models

**Ollama**
- Local AI models
- No API key required
- Runs on localhost

### Prompt Engineering

Each writing tool has a specific prompt template:

- **Humanizer**: Focus on natural language patterns
- **Paraphraser**: Maintain meaning, change wording
- **Essay Rewriter**: Academic tone, structure preservation
- **Grammar Check**: Correct errors, explain changes

### Error Handling

- API timeout handling
- Retry logic for transient failures
- Graceful degradation
- User-friendly error messages

## Data Flow

### Rewrite Flow

```
1. User inputs text (Frontend)
2. POST /writing/rewrite (API)
3. Validate input (Pydantic)
4. Check rate limit
5. Generate prompt (Writing Service)
6. Call AI provider (AI Provider Service)
7. Process response (Writing Service)
8. Return result (API)
9. Display to user (Frontend)
```

### Document Save Flow

```
1. User clicks save (Frontend)
2. POST /documents (API)
3. Validate JWT token
4. Validate input
5. Create document record (Document Service)
6. Save to database (ORM)
7. Return document ID (API)
8. Show success message (Frontend)
```

### Detection Flow

```
1. User inputs text (Frontend)
2. POST /writing/detect (API)
3. Validate input
4. Analyze text (Detection Service)
5. Calculate scores
6. Highlight sentences
7. Return results (API)
8. Display with visualization (Frontend)
```

## Performance Considerations

### Frontend
- Code splitting via Vite
- Lazy route loading
- Optimized bundle size
- Tailwind CSS purging

### Backend
- Async/await for I/O operations
- Database connection pooling
- Efficient ORM queries
- Response caching where appropriate

### Database
- Indexed foreign keys
- Query optimization
- Connection pooling (Neon)
- Regular migrations

## Scalability

### Horizontal Scaling
- Stateless backend design
- Stateless API design
- External AI provider (no local models)
- Managed database (Neon)

### Vertical Scaling
- Configurable rate limits
- Database connection pooling
- Async request handling

## Security Best Practices

1. **Never expose API keys** to frontend
2. **Use environment variables** for all secrets
3. **Validate all inputs** with Pydantic
4. **Hash passwords** with bcrypt
5. **Use HTTPS** in production
6. **Implement rate limiting** to prevent abuse
7. **CORS configuration** to restrict origins
8. **SQL injection prevention** via ORM
9. **JWT token expiration** for sessions
10. **User isolation** for document access

## Future Enhancements

### Potential Improvements
- Add more AI providers (Cohere, Google AI)
- Implement caching for common rewrites
- Add real-time collaboration
- Implement version history for documents
- Add analytics dashboard
- Support for file uploads (PDF, DOCX)
- Batch processing for multiple texts
- Custom prompt templates
- Plugin system for extensions

### Monitoring & Observability
- Structured logging
- Error tracking (Sentry)
- Performance monitoring
- API analytics
- User behavior analytics
