# Custom Production RAG System for Large-Scale Documents

A secure, high-performance, and cost-effective Retrieval-Augmented Generation (RAG) system architected for indexing, searching, and answering questions from large unstructured document bases (PDFs, DOCX, XLSX, and plain text) in both **English and Arabic**.

This repository is organized into distinct sub-modules for development, specifically containing faculty and personal experimental pipelines.

---

## 🏗️ High-Level Technical Architecture

The RAG system is engineered using a hybrid cloud, serverless-GPU architecture to achieve enterprise-grade speed and minimize operational idle costs by up to 80%:

```
[Client Applications] ──(HTTPS)──> [FastAPI Gateway] ──(Cache Check)──> [Redis Cache]
                                           │ (Cache Miss)
                                           ├──> [Qdrant Vector DB] (Retrieves source paragraphs)
                                           ├──> [Re-Ranker Model] (Selects top 5 most relevant)
                                           └──> [Ollama / RunPod Serverless] (Generates finalized answer)
```

1. **Ingestion Pipeline:** Securely reads, parses, chunks, generates embeddings (`bge-m3`), and indices document vectors in a memory-quantized **Qdrant DB**.
2. **Query Pipeline:** Accepts natural-language requests, performs semantic hybrid-search, re-ranks the candidate paragraphs for accuracy, caches requests in **Redis** (~50ms response), and feeds context to a serverless GPU-hosted `Qwen2.5-14B` model on **RunPod** to synthesize answers.

---

## ✨ Key Features

- **Multilingual Support:** High-fidelity document retrieval and answer generation in both English and Arabic.
- **Advanced Retrieval & Re-ranking:** Utilizes robust semantic search (`bge-m3`) coupled with a cross-encoder re-ranker to maximize LLM context accuracy.
- **Serverless LLM Inference:** Built to run on RunPod Serverless, scaling down to **$0/hr** when idle.
- **Caching Layer:** Redis query-caching layer to intercept repeating/highly similar queries within 50ms and zero extra GPU cost.
- **Production-Ready Ingestion:** Built-in loader support for PDFs, Word documents, Excel tables, Markdown, and Plain text files with custom chunking and a 64-token overlap window.

---

## 📂 Project Structure

```
Rag_project_software/
├── .gitignore               # Excludes large virtual envs, temporary cache, and DB files
├── README.md                # Project documentation & high-level design
├── rag_project_proposal.md  # Core project proposal & timeline
├── rag_system_plan.md      # In-depth architectural implementation blueprint
├── nike_football_catalog.pdf # Sample document for ingestion tests
├── nike_chroma_db/         # Local Chroma DB persistence directory (Git ignored)
├── faculty_project/         # Faculty-specific code, scripts, and notebook resources
└── personal_project/        # Personal development work, experimental pipelines, and custom modules
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python:** 3.10+
- **Docker & Docker Compose** (for hosting Qdrant, Redis, and FastAPI gateway)
- **Git**

### 2. Setting Up
1. Clone this repository:
   ```bash
   git clone git@github.com:AhmedAdel7472/Rag_project_software.git
   cd Rag_project_software
   ```

2. Activate virtual environment and install dependencies:
   ```bash
   # On Windows
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Spin up local database layers:
   ```bash
   docker-compose up -d
   ```

---

## 🛠️ Roadmap & Milestones
- **Week 1:** Ingestion verification & loaders setup (PDF parsing, Qdrant initialization).
- **Week 2:** FastAPI Gateway, query orchestration, and `/ask` basic endpoint.
- **Week 3:** Re-ranker integration, Redis query cache development, API authentication.
- **Week 4:** Full production hybrid deployment (Hetzner + RunPod Serverless), system hardening, and handoff.
