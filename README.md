# CRAG

<div align="center">

  <img src="https://img.shields.io/badge/Django-5.2.18-092E20?style=for-the-badge&logo=django" alt="Django" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/LangChain-1.4-000000?style=for-the-badge&logo=langchain" alt="LangChain" />
  <img src="https://img.shields.io/badge/RAG-AI-powered-8B5CF6?style=for-the-badge" alt="RAG" />

  <h3>Turn scattered documents into instant, grounded answers.</h3>

  <p>
    CRAG is a document intelligence platform that ingests PDFs and other knowledge sources,
    chunks and embeds them, and answers user questions with references grounded in the uploaded content.
  </p>

</div>

## Why CRAG?

Modern teams drown in documents: PDFs, research notes, manuals, reports, and internal knowledge dumps. CRAG helps you turn that information into a searchable, AI-powered knowledge layer without losing trust in the answer.

Instead of raw model guessing, CRAG:

- reads and processes uploaded documents
- splits them into meaningful chunks
- creates vector embeddings for semantic search
- retrieves the most relevant context for a query
- answers using the retrieved content as the source of truth

## Highlights

- AI-powered document Q&A grounded in uploaded files
- PDF ingestion and automatic chunking
- Vector search and semantic retrieval
- Role-based auth and user management
- React + Django full-stack app
- Redis + Celery background processing for scalable document workflows

## Tech Stack

- Backend: Django, Django REST Framework, JWT auth
- Frontend: React, Vite, Tailwind CSS
- AI/RAG: LangChain, LangGraph, embeddings, semantic retrieval
- Database: PostgreSQL
- Background jobs: Celery + Redis
- File/media: Cloudinary
- Email: Brevo

## Project Structure

```text
CRAG/
├── frontend/                  # Vite + React app
│   ├── src/
│   ├── package.json
│   └── vite.config.*
├── src/
│   ├── apps/
│   │   ├── accounts/
│   │   ├── agent/
│   │   └── document/
│   ├── config/
│   ├── manage.py
│   └── crag/
├── .env.example or environment variables
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Architecture

```text
User uploads document
        ↓
Django REST API
        ↓
Celery worker processes PDF + embeddings
        ↓
PostgreSQL stores metadata and document chunks
        ↓
Semantic retrieval finds relevant chunks
        ↓
Agent synthesizes grounded answer
        ↓
Frontend displays answer and context
```

## Features in Detail

### Document ingestion
Upload PDFs and trigger background processing to extract text, split content into chunks, and generate embeddings.

### Semantic retrieval
The system finds the most relevant document segments using embedding-based similarity search.

### Grounded answers
Responses are generated using the retrieved context, reducing hallucination risk and improving trust.

### Secure auth
User accounts, login, and protected routes are handled with Django authentication and JWT-based APIs.

### Modern frontend experience
The UI is built with React for a lightweight, polished experience that feels fast and responsive.

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis
- uv (recommended) or pip

### 1) Clone the repo

```bash
git clone https://github.com/AnshuSAHA176/CRAG.git
cd CRAG
```

### 2) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install Python dependencies

```bash
pip install uv
uv sync
```

### 4) Install frontend dependencies

```bash
cd frontend
npm install
```

### 5) Configure environment variables

Create a `.env` file in the project root with values for:

```env
BREVO_API_KEY=your_brevo_key
BREVO_SENDER_EMAIL=your_sender_email
BREVO_SENDER_NAME=CRAG
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Update the database and Redis connection settings if needed in `src/config/settings.py`.

### 6) Start supporting services

Start PostgreSQL and Redis locally, then run:

```bash
cd src
python manage.py migrate
python manage.py runserver
```

### 7) Start the frontend

In another terminal:

```bash
cd frontend
npm run dev
```

### 8) Run Celery worker

```bash
cd src
celery -A config worker -l info
```

## Common Commands

```bash
# database migrations
cd src
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run backend tests
python manage.py test

# build frontend
cd frontend
npm run build
```

## Roadmap

- improve retrieval quality and ranking
- support more file types beyond PDFs
- add document collections and workspace organization
- add richer citations and answer traceability
- upgrade monitoring and evaluation pipelines

## Contributing

Contributions are welcome. If you want to improve the product, fix bugs, or add capabilities:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description

## Notes

This project is actively evolving. The stack is optimized for a modern AI document workflow and is ideal for prototypes, internal tools, and knowledge-management applications.

---

Built to make documents searchable, understandable, and answerable.
