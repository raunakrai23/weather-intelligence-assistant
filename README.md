# 🌦️ Weather Intelligence & Advisory Assistant

An AI-powered weather intelligence platform built using FastAPI, PostgreSQL, pgvector, and Streamlit. It combines real-time weather information with Retrieval-Augmented Generation (RAG) to provide contextual weather explanations and safety recommendations.

## 🚀 Features

- **Real-Time Weather:** Fetches current weather conditions using the Open-Meteo API.
- **Weather Forecasts:** Provides hourly and 7-day weather forecasts.
- **AI Weather Assistant:** Answers natural-language weather questions using an LLM.
- **RAG Pipeline:** Processes weather knowledge documents, generates vector embeddings, and retrieves relevant information.
- **User Authentication:** Secure registration and login using JWT authentication.
- **Conversation Management:** Stores conversations and messages in PostgreSQL.
- **Interactive Dashboard:** Streamlit-based frontend for weather information and AI chat.
- **Docker Support:** Containerized backend and database services.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| Vector Database | pgvector |
| AI / LLM | Groq API |
| Embeddings | Sentence Transformers |
| Weather API | Open-Meteo |
| Authentication | JWT |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |

## 📁 Project Structure

```text
weather-intelligence-assistant/
│
├── app/
│   ├── routers/
│   │   ├── assistant.py
│   │   ├── auth.py
│   │   ├── conversation.py
│   │   └── message.py
│   │
│   ├── schemas/
│   ├── services/
│   ├── weather/
│   ├── rag/
│   ├── database/
│   ├── models/
│   └── main.py
│
├── data/
│   └── documents/
│       └── weather_safety.txt
│
├── evaluation/
├── migrations/
├── tests/
├── frontend/
│   └── streamlit_app.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd weather-intelligence-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the required database credentials, JWT secret, and Groq API key.

Never commit `.env` or expose API keys.

### 5. Start Docker services

```bash
docker compose up -d --build
```

### 6. Apply database migrations

```bash
docker compose exec api python -m alembic upgrade head
```

### 7. Enable pgvector

```bash
docker compose exec db psql -U postgres -d weather_assistant -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 8. Ingest weather knowledge documents

```bash
docker compose exec api python -m app.rag.ingestion
```

## 🖥️ Running the Application

### Backend

The FastAPI backend runs at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

### Frontend

Run Streamlit locally:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

## 🧠 RAG Pipeline

1. Weather knowledge documents are stored in the data directory.
2. Documents are loaded and divided into smaller chunks.
3. Sentence Transformers generates vector embeddings.
4. Embeddings are stored in PostgreSQL using pgvector.
5. User queries are converted into embeddings.
6. Relevant document chunks are retrieved using vector similarity.
7. The LLM generates a natural-language response.

## 🧪 Testing

Run the automated test suite:

```bash
pytest -v
```

The project includes tests for weather services, authentication, query routing, and RAG retrieval.

## 🐳 Docker Commands

Check running containers:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs -f api
```

Stop services:

```bash
docker compose down
```

## 🔮 Future Enhancements

- Interactive weather charts and visualizations.
- Weather alert notifications.
- Location-based personalized recommendations.
- Expanded weather knowledge base.
- Conversation history interface.
- Cloud deployment and monitoring.

## 👨‍💻 Project

**Weather Intelligence & Advisory Assistant**

An AI-powered platform combining real-time weather APIs, vector search, and large language models to deliver intelligent weather information and safety guidance.
