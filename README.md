# CRAG

<div align="center">

  <img src="https://img.shields.io/badge/Django-5.2.18-092E20?style=for-the-badge&logo=django" alt="Django" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/LangChain-1.4-000000?style=for-the-badge&logo=langchain" alt="LangChain" />
  <img src="https://img.shields.io/badge/RAG-Grounded%20AI-8B5CF6?style=for-the-badge" alt="Grounded RAG" />

  <h3>Ask questions from your documents with confidence.</h3>

  <p>
    CRAG is an AI-powered document intelligence platform that transforms PDFs and uploaded knowledge into a searchable, trustworthy Q&A experience.
  </p>

</div>

## Overview

CRAG helps teams turn large document sets into a fast, grounded knowledge system. Instead of searching manually or trusting unverified AI outputs, users can upload documents and ask natural-language questions that are answered using the most relevant document context.

This project combines:

- document ingestion and processing
- chunking and embedding generation
- semantic retrieval
- grounded answer generation
- secure authentication and modern UI

## Why this project matters

Organizations collect information in scattered folders, PDFs, reports, manuals, and internal notes. CRAG brings structure to that information by indexing it and letting users ask questions in plain English, while keeping answers anchored to the source material.

## Core features

- PDF upload and processing pipeline
- Automatic text chunking and embedding creation
- Semantic document retrieval
- Context-aware answer generation with document grounding
- Role-based user access and secure APIs
- React frontend for a polished user experience
- Celery + Redis background jobs for scalable processing

## Tech stack

- Backend: Django, Django REST Framework, JWT
- Frontend: React + Vite + Tailwind CSS
- AI/RAG: LangChain, LangGraph, embeddings, retrieval
- Database: PostgreSQL
- Background processing: Celery + Redis
- Storage/media: Cloudinary
- Email: Brevo

## Architecture

```text
Document upload
      ↓
Django backend
      ↓
Background worker processes PDF and creates embeddings
      ↓
PostgreSQL stores documents and chunk metadata
      ↓
Retrieval finds the most relevant chunks
      ↓
Agent generates a grounded answer
      ↓
Frontend displays answer with context
```

## Repository structure

```text
CRAG/
├── frontend/                  # React + Vite frontend
│   ├── src/
│   ├── package.json
│   ├── vite.config.*
│   └── public/
├── src/
│   ├── apps/
│   │   ├── accounts/
│   │   ├── agent/
│   │   └── document/
│   ├── config/
│   ├── crag/
│   └── manage.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
└── .env
```

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis
- uv or pip

### 1. Clone the repository

```bash
git clone https://github.com/AnshuSAHA176/CRAG.git
cd CRAG
```

### 2. Set up Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv sync
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

### 4. Configure environment variables

Create a `.env` file in the project root with values similar to:

```env
BREVO_API_KEY=your_brevo_key
BREVO_SENDER_EMAIL=your_sender_email
BREVO_SENDER_NAME=CRAG
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Update database and Redis settings in `src/config/settings.py` if needed.

### 5. Run backend services

```bash
cd src
python manage.py migrate
python manage.py runserver
```

### 6. Start the frontend

Open a second terminal:

```bash
cd frontend
npm run dev
```

### 7. Start Celery worker

```bash
cd src
celery -A config worker -l info
```

## Useful commands

```bash
# create migrations
cd src
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run backend tests
python manage.py test

# build frontend for production
cd frontend
npm run build
```

## Roadmap

- stronger document retrieval ranking
- improved answer citations and traceability
- support for more document formats
- workspace-level document collections
- monitoring and evaluation improvements

## Contributing

Contributions are welcome. If you want to improve CRAG, add features, or fix issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request with a clear summary

## License

This project is currently under active development and is intended for prototype, internal, and knowledge-management use cases.

---

Built to make documents searchable, understandable, and answerable.
