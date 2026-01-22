# F1 Project

A data pipeline for scraping Formula 1 news from multiple sources and transforming it into structured, production-ready talking points for video generation and editorial workflows.

The system is designed to:

* Scrape motorsports news from diverse websites and RSS feeds
* Classify and filter Formula 1 content from other motorsports (e.g., MotoGP, rally racing)
* Separate **news**, **opinions**, and **explanatory** content
* Summarize articles into concise, LLM-generated talking points while controlling cost

---

## Table of Contents

* [Features](#features)
* [Design Rationale](#design-rationale)
* [Installation](#installation)

---

## Features

### Motorsports News Classification Module

A **hybrid classification approach** designed to minimize LLM usage as system confidence improves over time.

#### High-Level Flow

```
Incoming News Title
        ↓
Text Normalization & Tokenization
        ↓
Rule-Based Classification
        ↓
Confidence Evaluation
        ├─ Confident → Return Category
        └─ Not Confident
               ↓
         LLM Classification
               ↓
      Entity Extraction & Parsing
               ↓
     Keyword Frequency Tracking
               ↓
     Keyword Map Enrichment
               ↓
          Return Category
```

#### Key Characteristics

* Rule-first design to reduce unnecessary LLM calls
* Confidence-driven fallback to LLM classification
* Continuous keyword enrichment to improve future rule-based accuracy
* Explicit filtering of non-F1 motorsports content

---

### F1 News Ingestion Pipeline

**DAG ID:** `f1_news_pipeline`  
**Schedule:** Daily  
**Purpose:** Discover and scrape new Formula 1 news articles from RSS feeds.

#### Pipeline Stages

1. **RSS Discovery**

   * Identifies new article URLs from configured RSS sources
   * Prevents duplicate processing of previously discovered content

2. **Article Scraping**

   * Fetches full article content from discovered URLs
   * Extracts structured data (title, body text, metadata)

#### Execution Flow

```
RSS Discovery → Article Scraping
```

This pipeline focuses exclusively on **data collection** and runs daily to ensure timely ingestion of new content.

---

### F1 News Summarization Pipeline

A semantic clustering and summarization system that converts raw F1 news articles into coherent, video-ready talking points.

#### What This Pipeline Does

* Groups **semantically similar articles** covering the same story
* Avoids redundant summaries for near-duplicate news
* Produces **story-level digests** rather than article-level blurbs
* Generates a final, time-bounded script optimized for video production

#### How It Works (Conceptually)

1. **Article Retrieval**
   Unsummarized Formula 1 articles are fetched from the database.

2. **Context Preparation**
   Each article’s title and body are concatenated and truncated to a safe token length to fit embedding and LLM constraints.

3. **Semantic Embedding (Batched)**
   Articles are embedded in small batches to:

   * Improve throughput
   * Reduce latency spikes
   * Control embedding API costs

4. **Similarity Analysis**

   * Cosine similarity is computed across all article embeddings
   * Similarity is converted into a distance matrix suitable for clustering

5. **Unsupervised Clustering (HDBSCAN)**

   * Articles are grouped using density-based clustering
   * The number of clusters is determined automatically
   * Noise points (outliers) are treated as standalone stories

6. **Adaptive Summarization Strategy**

   * **Singleton articles** are summarized individually
   * **Clusters of related articles** are summarized jointly to produce a single consolidated narrative

7. **Talking Point Generation**
   Cluster-level summaries are merged into a structured script constrained by a target duration (e.g., 20 minutes).

8. **State Management**
   Each processed article is marked as summarized to ensure idempotent re-runs and safe retries.

#### Why This Design

* **Story-centric summarization** instead of article-centric output
* **Cost-aware LLM usage** by summarizing clusters rather than duplicates
* **Robust to news volume spikes** (race weekends, breaking news)
* **Production-ready** through batching, idempotency, and fault tolerance

---

## Design Rationale

### Pipeline Separation

Ingestion and summarization are intentionally decoupled to:

* Allow independent scaling
* Enable different execution schedules
* Reduce coupling between data collection and enrichment

### Retry & Fault Tolerance

* DAGs include retry logic with configurable delays
* Designed to handle transient network, scraping, and API failures

### Idempotent Tasks

* Discovery and scraping tasks can be safely re-run
* Duplicate data creation is explicitly avoided

### Production-Friendly Scheduling

* **Daily ingestion** ensures timely data capture
* **Periodic summarization** reduces unnecessary LLM calls

---

## Installation

### Local (Python)

1. Create and activate a virtual environment
2. Install dependencies:

```
pip install -r requirements.txt
```

### Docker (Recommended)

This project includes a Docker Compose setup for Airflow and PostgreSQL.

#### Prerequisites

* Docker >= 20.x
* Docker Compose v2

#### Steps

1. Clone the repository
2. Create a `.env` file with required environment variables
3. Start the stack:

```
docker compose up --build
```

This will:

* Build a custom Airflow image with project dependencies
* Start PostgreSQL
* Initialize Airflow metadata database
* Run Alembic migrations
* Create an admin Airflow user
* Launch Airflow webserver and scheduler

#### Access Airflow UI

```
http://localhost:8080
```
#### Data Persistence

Volumes:

* `postgres_data` – PostgreSQL data
* `airflow_logs` – Airflow logs
* `airflow_home` – Airflow runtime and metadata

#### Stop the Stack

```
docker compose down
```

Remove volumes as well:

```
docker compose down -v
```
