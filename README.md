# F1 Intelligence Platform

A platform that ingests Formula 1 news, uses LLMs to work out what happened, and links events, drivers, teams and races over time.

## System Design

```mermaid
flowchart LR
    %% ---------- External ----------
    subgraph EXT["🌐 External Sources"]
        RSS["RSS Feeds<br/>F1 news sites"]
        WEB["Article Pages<br/>HTML"]
    end

    %% ---------- Host ----------
    subgraph HOST["🐳 Docker Compose Host"]
        direction LR

        subgraph ORCH["Orchestration · Apache Airflow"]
            SCHED["Scheduler"]
            UI["Webserver<br/>:8080"]
        end

        subgraph INGEST["DAG · f1_news_pipeline · @daily"]
            DISC["① rss_discovery<br/>dedupe by URL"]
            CLS{"② Rule-based<br/>keyword match<br/>confident?"}
            SCRAPE["③ article_scraping<br/>extract body text"]
        end

        subgraph SUMM["DAG · f1_summarization · every 3 days"]
            EMB["④ Batch embed<br/>title + body"]
            CLUS["⑤ Cosine similarity<br/>+ HDBSCAN clustering"]
            SUM["⑥ Summarize<br/>cluster / singleton"]
            OUT["⑦ Talking-points<br/>script"]
        end

        subgraph DATA["Storage · PostgreSQL 15"]
            ART[("news_articles")]
            KW[("keyword_stats")]
            MIG["Alembic<br/>migrations"]
        end

        subgraph PLAN["🚧 Planned · Intelligence Layer"]
            EVT["Event extraction"]
            KG[("Temporal<br/>knowledge graph")]
            QA["Q&A over<br/>multi-source evidence"]
            ALERT["Emerging-story<br/>notifications"]
        end
    end

    %% ---------- AI Provider ----------
    subgraph AI["☁️ Mistral AI API"]
        LLM["ministral-3b<br/>classify · summarize"]
        EMBM["mistral-embed"]
    end

    %% ---------- Flows (built) ----------
    SCHED --> DISC
    SCHED --> EMB
    RSS --> DISC
    DISC --> CLS
    CLS -- "not confident" --> LLM
    LLM -- "new entities" --> KW
    KW -- "load keyword map" --> CLS
    CLS -- "category + news type" --> ART
    ART -- "pending URLs" --> SCRAPE
    WEB --> SCRAPE
    SCRAPE -- "body_text" --> ART

    ART -- "unsummarized F1 articles" --> EMB
    EMB <--> EMBM
    EMB --> CLUS --> SUM
    SUM <--> LLM
    SUM --> OUT
    SUM -- "summarized = true" --> ART
    MIG -.- ART

    %% ---------- Flows (planned) ----------
    ART -.-> EVT
    EVT -.-> KG
    KG -.-> QA
    KG -.-> ALERT

    %% ---------- Styles ----------
    classDef ext fill:#eef2f7,stroke:#5b6b82,color:#1b2430
    classDef compute fill:#fff4e5,stroke:#e8890c,color:#3a2400
    classDef store fill:#e8f1fb,stroke:#2f6fb5,color:#0d2742
    classDef ai fill:#f3ecfb,stroke:#7a4cc2,color:#2a1250
    classDef planned fill:#f7f7f7,stroke:#9a9a9a,stroke-dasharray:5 4,color:#555

    class RSS,WEB ext
    class SCHED,UI,DISC,CLS,SCRAPE,EMB,CLUS,SUM,OUT compute
    class ART,KW,MIG store
    class LLM,EMBM ai
    class EVT,KG,QA,ALERT planned
```

**Legend:** solid arrows are built · dashed boxes and arrows are planned · circled numbers are the order of processing

| Component | Code |
|---|---|
| Airflow DAGs | [dags/](dags/) |
| RSS discovery + classification | [scrapers/rss_discovery.py](scrapers/rss_discovery.py), [utils/classify_motorsports.py](utils/classify_motorsports.py) |
| Article scraping | [scrapers/article_scraper.py](scrapers/article_scraper.py) |
| Embedding, clustering, summaries | [pipeline/summarization_job.py](pipeline/summarization_job.py), [utils/llm_call.py](utils/llm_call.py) |
| Database access | [db/postgres_utils.py](db/postgres_utils.py), [alembic/](alembic/) |

## Run

```bash
docker compose up --build   # Airflow UI at http://localhost:8080
```

Needs a `.env` file with `MISTRAL_API_KEY` and the database connection settings.
