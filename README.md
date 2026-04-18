# Arxelos

**Synchronous Multi-Model Intelligence Platform**
*AI at the Intersection of Intelligence & Biology*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is Arxelos?

Arxelos is a research-grade platform hosting three deployed AI models, each sitting at the intersection of neuroscience and deep learning:

| Model | Domain | Status |
|-------|--------|--------|
| **Brain Tumor MRI Classifier** | Medical Computer Vision | 🔧 Building |
| **Virtual Lesions CNN Visualizer** | Neuro-AI / Interpretability | 📋 Planned |
| **RAG Medical Literature Q&A** | NLP / LLM | 📋 Planned |

Each model is both a research deliverable and a deployed, demo-ready artifact.

## Project Structure

```
Arxelos/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py           # Application entrypoint
│   │   ├── config.py         # Settings & environment config
│   │   ├── routers/          # API route handlers
│   │   │   ├── health.py     # Health check endpoints
│   │   │   ├── tumor.py      # Model 1 — Brain Tumor Classifier
│   │   │   ├── lesions.py    # Model 2 — Virtual Lesions Visualizer
│   │   │   └── rag.py        # Model 3 — Medical RAG Q&A
│   │   ├── models/           # Pydantic schemas & ML model loaders
│   │   ├── services/         # Business logic & inference pipelines
│   │   └── utils/            # Shared utilities
│   ├── tests/                # pytest test suite
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Static site & demo UI
│   ├── templates/            # Jinja2 HTML templates
│   ├── static/
│   │   ├── css/              # Stylesheets
│   │   ├── js/               # Client-side scripts
│   │   └── images/           # Assets & logos
├── docker/                   # Dockerfiles & compose configs
│   ├── Dockerfile            # Production image
│   └── docker-compose.yml    # Local dev orchestration
├── notebooks/                # Research notebooks (Neuro-AI labs)
├── docs/                     # Architecture docs & write-ups
├── scripts/                  # Utility scripts
├── .github/workflows/        # CI/CD pipelines
├── .env.example              # Environment variable template
├── .gitignore
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- Docker (optional, for containerized runs)

### Local Development

```bash
# Clone the repo
git clone https://github.com/aryanp2107/Arxelos.git
cd Arxelos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the API server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at `http://localhost:8000/docs`

### Docker

```bash
cd docker
docker-compose up --build
```

## Roadmap

- [x] Project structure & repository setup
- [ ] Model 1: Brain Tumor MRI Classifier — FastAPI + Docker + deploy
- [ ] Model 2: Virtual Lesions CNN Visualizer — interactive ablation demos
- [ ] Model 3: RAG Medical Literature Q&A — retrieval pipeline + deploy
- [ ] Phase 2: Multimodal orchestration layer
- [ ] CI/CD via GitHub Actions
- [ ] Model monitoring & MLOps integration

## Tech Stack

**Backend:** FastAPI · Uvicorn · PyTorch · TensorFlow/Keras
**NLP:** LangChain · ChromaDB/FAISS · Transformers
**Frontend:** Jinja2 · Vanilla JS (lightweight, fast)
**Infra:** Docker · GitHub Actions · Cloud TBD (Render / Railway / AWS)
**MLOps:** MLflow · DVC · GitHub Actions CI/CD

## Author

**Aryan Patel**
MS in Artificial Intelligence — Northeastern University
[aryanp2107](https://github.com/aryanp2107) · [patel.aryana@northeastern.edu](mailto:patel.aryana@northeastern.edu)

## License

MIT — see [LICENSE](LICENSE) for details.
