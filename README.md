# Self-Healing RAG Pipeline

A FastAPI-based Retrieval-Augmented Generation (RAG) system with intelligent self-healing capabilities. When retrieval confidence is low, the system automatically expands queries and re-retrieves, escalating to human review only when necessary.

Built with **FastAPI**, **LlamaIndex**, **Pinecone**, **Claude**, and **Pydantic**. This system detects low-confidence answers, retries with query expansion, and escalates uncertain cases for human review—eliminating weak responses without manual intervention.

## Features

- ✨ **Smart Query Expansion**: Automatically expands low-confidence queries to improve retrieval
- 📊 **Confidence Scoring**: Built-in confidence thresholds to identify uncertain responses
- 🔄 **Self-Healing Loop**: Retries with alternative queries when initial retrieval is weak
- 🚨 **Escalation Workflow**: Escalates uncertain cases for human review
- 💬 **Feedback Loop**: Collect user feedback to improve future responses
- 📡 **REST API**: Full REST API with OpenAPI documentation (Swagger UI)
- 🏥 **Health Monitoring**: Built-in health check endpoint
- 🐳 **Docker Ready**: Easy deployment with Docker Compose

## Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/<your-username>/self-healing-rag.git
cd self_healing_rag
```

2. **Create a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running Locally

Start the FastAPI server:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The server will start at `http://127.0.0.1:8000`

**Access the API:**
- **Root**: `GET http://127.0.0.1:8000/` → Welcome message
- **Health Check**: `GET http://127.0.0.1:8000/health` → Service status
- **Interactive API Docs**: `http://127.0.0.1:8000/docs` (Swagger UI)
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Running Tests

Run the test suite:
```bash
pytest tests/ -v

# Run a specific test
pytest tests/test_health.py -v
```

## API Endpoints

### Root
```
GET /
```
Returns welcome message and API info.

**Response:**
```json
{"message": "Self-Healing RAG API. Visit /docs for API docs."}
```

### Health Check
```
GET /health
```
Returns server status.

**Response:**
```json
{"status": "ok"}
```

### Chat
```
POST /chat
```
Submit a query and get an RAG-powered answer with confidence scoring and retrieval path.

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "session_id": "optional-session-123"
}
```

**Response:**
```json
{
  "answer": "Answer based on retrieved context...",
  "confidence": 0.95,
  "retrieval_path": ["primary"],
  "escalated": false
}
```

**Response Fields:**
- `answer` (string): The generated answer
- `confidence` (float): Confidence score (0.0–1.0)
- `retrieval_path` (array): Stages used ("primary", "expanded", "escalated", etc.)
- `escalated` (boolean): Whether the case was escalated for review

### Feedback
```
POST /feedback
```
Submit feedback on query responses to improve the system.

**Request Body:**
```json
{
  "query_id": "query-uuid",
  "label": "correct",
  "notes": "Optional notes about the response"
}
```

## How It Works

1. **Query Received**: User submits a query via `POST /chat`
2. **Initial Retrieval**: System retrieves documents from Pinecone vector DB
3. **Confidence Check**: 
   - If `confidence >= threshold` → return answer immediately
   - If `confidence < threshold` → proceed to step 4
4. **Query Expansion**: Claude generates alternative query formulations
5. **Re-retrieval**: Attempt retrieval with expanded queries
6. **Escalation Decision**:
   - If new `confidence >= threshold` → return answer
   - If still below threshold → mark as `escalated: true`
7. **Response**: Return answer with confidence, retrieval path, and escalation flag

**Self-Healing Logic Pseudocode:**
```
if initial_confidence >= threshold:
    return answer
else:
    for expanded_query in expand_queries(query):
        new_results = retrieve(expanded_query)
        confidence = max(confidence, score(new_results))
        if confidence >= threshold:
            return answer
    # Still low confidence
    return escalated_response()
```

## Project Structure

```
self_healing_rag/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat.py              # Chat endpoint handler
│   │       ├── feedback.py          # Feedback endpoint handler
│   │       └── health.py            # Health check endpoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Application configuration
│   │   └── main.py
│   ├── rag/
│   │   ├── __init__.py
│   │   └── orchestrator.py          # RAG orchestration & self-healing logic
│   ├── retrievers/
│   │   ├── __init__.py
│   │   └── pincone_retriever.py     # Pinecone vector DB client
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py                # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── claude.py                # Claude LLM integration
│   └── utils/
│       └── __init__.py
├── tests/
│   └── test_health.py               # Health endpoint tests
├── Dockerfile                        # Container image definition
├── docker-compose.yml               # Docker Compose configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Configuration

Edit `app/core/config.py` to customize:
- `confidence_threshold`: Minimum confidence score (0.0–1.0) to return a direct answer without escalation
- Pinecone API endpoint and credentials
- Claude API model and settings

### Environment Variables

Create a `.env` file in the project root (referenced in `docker-compose.yml`):
```
# LLM Configuration
ANTHROPIC_API_KEY=your-claude-api-key
CLAUDE_MODEL=claude-3-sonnet-20240229

# Vector Database
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=your-namespace

# Self-Healing Configuration
CONFIDENCE_THRESHOLD=0.7
LOG_LEVEL=INFO
```

## Docker Deployment

### Build and Run
```bash
docker compose up -d --build
```

### View Logs
```bash
docker compose logs --follow api
```

### Stop Services
```bash
docker compose down
```

### Check Status
```bash
docker compose ps
```

### Manual Docker Build
```bash
docker build -t self-healing-rag .
docker run --env-file .env -p 8000:8000 self-healing-rag
```

## Dependencies

- **FastAPI** — Modern, fast web framework for building APIs
- **Uvicorn** — ASGI server for running FastAPI applications
- **Pydantic** — Data validation and serialization using Python type hints
- **Anthropic** — Claude LLM API client
- **Pinecone** — Vector database for semantic search and retrieval
- **LlamaIndex** — RAG framework and utilities
- **Pytest** — Testing framework for unit and integration tests
- **Requests** — HTTP library for making API calls

See `requirements.txt` for the complete list with versions.

## Development

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions
- Use type hints for function parameters and return values
- Use meaningful variable and function names

### Adding New Endpoints
1. Create a new file in `app/api/routes/`
2. Define a FastAPI router with your endpoint handlers
3. Include the router in `app/main.py` using `app.include_router()`

Example:
```python
# app/api/routes/custom.py
from fastapi import APIRouter

router = APIRouter(prefix="/custom", tags=["custom"])

@router.get("/")
def custom_endpoint():
    return {"message": "Hello"}
```

Then in `app/main.py`:
```python
from app.api.routes.custom import router as custom_router
app.include_router(custom_router)
```

### Testing
- Write unit tests in `tests/` directory
- Use pytest fixtures for reusable test components
- Run tests before pushing to production: `pytest tests/ -v`

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -nP -iTCP:8000 -sTCP:LISTEN

# Kill the process (replace <PID> with actual PID)
kill <PID>
```

### ImportError or ModuleNotFoundError
Ensure your virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Type Errors (Python 3.8 Compatibility)
This project targets Python 3.8+. For type annotations:
- Use `from typing import List, Dict, Optional` instead of `list[...]`, `dict[...]`, or `Type | None`
- Use `Optional[str]` instead of `str | None`

### Missing Environment Variables
Ensure `.env` file exists with all required keys and is loaded properly. For Docker, ensure environment variables are passed:
```bash
docker compose up -d --build
```

### Docker Build Fails
Clean and rebuild:
```bash
docker compose down
docker system prune -a
docker compose up -d --build
```

## Performance Tips

- **Batch queries**: Use session IDs to track related queries for better context
- **Tune confidence threshold**: Adjust `CONFIDENCE_THRESHOLD` to balance accuracy vs. escalation rate
- **Cache vectors**: For high-volume deployments, consider caching commonly retrieved documents
- **Monitor metrics**: Track escalation rate, answer latency, and user feedback

## Roadmap

- [ ] Streaming responses for real-time answer generation
- [ ] Human review dashboard for escalated cases
- [ ] Distributed tracing with OpenTelemetry
- [ ] Response caching and answer reuse
- [ ] Automated offline evaluation suite
- [ ] Multi-turn conversation support
- [ ] Custom retriever plugins

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request

## Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Contact on my email
