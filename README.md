# End-to-End AI Logistics Platform

A full-stack data engineering and AI project that processes NYC Taxi data, serves analytics via a high-performance API, and includes a **Local RAG (Retrieval-Augmented Generation) AI Agent** to answer natural language questions about the data.

**Key Features:**
- **Zero-Cost Architecture:** Runs entirely on local hardware (CPU-optimized).
- **Modern Data Stack:** Uses DuckDB for high-speed local processing.
- **Privacy-First AI:** Implements a local LLM (Ollama) so no data leaves the machine.

---

<<<<<<< HEAD
##  Architecture
=======
## Architecture
>>>>>>> fcc689f1377aae3ecf4277684414ff9f35fe8db5



The system consists of three distinct micro-components:

1.  **ETL Pipeline:** Ingests raw Parquet files (Millions of rows), aggregates metrics using **DuckDB**, and loads clean data into **PostgreSQL**.
2.  **REST API:** A **FastAPI** backend that provides endpoints for frontend applications to fetch real-time analytics.
3.  **AI Research Agent:** A RAG system built with **Ollama (Phi-3/Qwen)** and **FAISS** that allows users to chat with the dataset.

---

##  Tech Stack

* **Language:** Python 3.10+
* **Data Processing:** DuckDB, Pandas, SQLAlchemy
* **Database:** PostgreSQL (Dockerized)
* **Backend:** FastAPI, Uvicorn, AsyncPG
* **AI & ML:** Ollama (Local LLM), FAISS (Vector DB), Sentence-Transformers
* **DevOps:** Docker, Virtual Environments

---

##  Setup & Installation

### Prerequisites
* Python 3.10+
* Docker Desktop
* [Ollama](https://ollama.com/) (for the AI Agent)

### 1. Clone & Install
```bash
git clone [https://github.com/YOUR_USERNAME/logistics-platform.git](https://github.com/YOUR_USERNAME/logistics-platform.git)
cd logistics-platform
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
