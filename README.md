# F1 Project

A data pipeline for scraping Formula 1 news from multiple sources and transforming it into structured, production‑ready talking points for video generation and editorial workflows.

The system is designed to:

* Scrape motorsports news from diverse websites and RSS feeds
* Classify and filter Formula 1 content from other motorsports (e.g., MotoGP, rally racing)
* Separate **news**, **opinions**, and **explanatory** content
* Summarize articles into concise, LLM‑generated talking points while controlling cost

---

## Table of Contents

* [Features](#features)
---

## Features

### Motorsports News Classification Module

A **hybrid classification approach** designed to minimize LLM usage as system confidence improves over time.

#### High‑Level Flow

```
Incoming News Title
        ↓
Text Normalization & Tokenization
        ↓
Rule‑Based Classification
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

* Rule‑first design to reduce unnecessary LLM calls
* Confidence‑driven fallback to LLM classification
* Continuous keyword enrichment to improve future rule‑based accuracy
* Explicit filtering of non‑F1 motorsports content

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

A semantic clustering and summarization system that converts raw F1 news articles into coherent, video‑ready talking points.

#### What This Pipeline Does

* Groups **semantically similar articles** covering the same story
* Avoids redundant summaries for near‑duplicate news
* Produces **story‑level digests** rather than article‑level blurbs
* Generates a final, time‑bounded script optimized for video production

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

   * Articles are grouped using density‑based clustering
   * Naturally determines the number of clusters
   * Noise points (outliers) are treated as standalone stories

6. **Adaptive Summarization Strategy**

   * **Singleton articles** (no close neighbors):

     * Summarized individually
   * **Clusters of related articles**:

     * Summarized jointly to produce a single, consolidated narrative
     * Prevents repetition across outlets reporting the same event

7. **Talking Point Generation**
   Cluster‑level summaries are merged and transformed into a structured script constrained by a target duration (e.g., 20 minutes).

8. **State Management**
   Each processed article is marked as summarized to ensure idempotent re‑runs and safe retries.

#### Why This Design

* **Story‑centric summarization** instead of article‑centric output
* **Cost‑aware LLM usage** by summarizing clusters, not duplicates
* **Robust to news volume spikes** (race weekends, breaking news)
* **Production‑ready**: batching, idempotency, and fault tolerance built in

---

## Design Rationale

### Pipeline Separation

Ingestion and summarization are intentionally decoupled to:

* Allow independent scaling
* Enable different execution schedules
* Reduce coupling between data collection and enrichment

### Retry & Fault Tolerance

* Both DAGs include retry logic with configurable delays
* Designed to handle transient network and scraping failures

### Idempotent Tasks

* Discovery and scraping tasks can be safely re‑run
* Duplicate data creation is explicitly avoided

### Production‑Friendly Scheduling

* **Daily ingestion** ensures timely data capture
* **Periodic summarization** reduces unnecessary LLM calls

---

## Project Structure

> *To be documented*

---

## Requirements

> *To be documented*

---

## Installation

> *To be documented*

---

## Usage

### Configuration

> *To be documented*

### Running Scrapers

> *To be documented*

### Database Migrations

> *To be documented*

### Pipeline Execution

#### Summarization Pipeline (Implementation)

The summarization pipeline clusters related F1 news articles using embedding similarity and generates structured talking points for video production.

**Key Steps:**

1. **Fetch Unsummarized Articles**
   Articles are retrieved from Postgres using `get_f1_news()`.

2. **Text Preparation**
   Titles and body text are concatenated and truncated to a safe context length.

3. **Embedding Generation (Batched)**
   Articles are embedded in batches to improve throughput and control LLM/API usage.

4. **Clustering**

   * Cosine similarity is computed between embeddings
   * Converted to a distance matrix
   * HDBSCAN clusters semantically similar articles
   * Noise points (`-1`) are treated as singletons

5. **Summarization Strategy**

   * **Singleton clusters** → `summarize_singleton`
   * **Multi‑article clusters** → `summarize_cluster`

6. **Talking Point Generation**
   Cluster‑level summaries are merged into a final script using `generate_talking_points`.

7. **State Update**
   Each processed article is marked summarized via `update_summarization_status`.

---


> *To be documented*
