# F1 News Intelligence Pipeline

Scrapes Formula 1 news from RSS feeds, filters out other motorsports, groups articles that cover the same story, and generates a talking-points script with an LLM.

## Architecture

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Helvetica, Arial, sans-serif", "fontSize": "14px", "primaryColor": "#ffffff", "primaryTextColor": "#1f2328", "primaryBorderColor": "#8c959f", "lineColor": "#57606a", "textColor": "#1f2328", "edgeLabelBackground": "#ffffff", "clusterBkg": "#f6f8fa", "clusterBorder": "#8c959f"}}}%%
flowchart TB
    subgraph CANVAS[" "]
        direction TB

        RSS["F1 News RSS Feeds<br/>6 sources"]

        subgraph HOST["Docker Compose · Apache Airflow"]
            direction TB

            subgraph ING["Ingestion DAG · f1_news_pipeline · daily"]
                direction LR
                A["RSS discovery<br/>skip known URLs"] --> B["Classify motorsport<br/>rules, LLM fallback"] --> C["Tag news type"] --> D["Scrape article body"]
            end

            subgraph DB["PostgreSQL 15"]
                direction LR
                T1[("news_articles")]
                T2[("keyword_stats")]
            end

            subgraph SUM["Summarization DAG · f1_summarization · every 3 days"]
                direction LR
                E["Embed articles<br/>batches of 10"] --> F["Cluster by story<br/>HDBSCAN"] --> G["Summarize<br/>each story"] --> H["Write talking<br/>points script"]
            end

            ING -- "store articles + learned keywords" --> DB
            DB -- "unsummarized F1 articles" --> SUM
        end

        subgraph AI["Mistral AI API"]
            direction LR
            M1["ministral-3b<br/>classify · summarize"]
            M2["mistral-embed<br/>embeddings"]
        end

        OUT["final_script.txt"]

        RSS --> ING
        ING -.-|API calls| AI
        SUM -.-|API calls| AI
        SUM --> OUT
    end

    %% Nodes
    classDef io fill:#eaeef2,stroke:#57606a,stroke-width:1.5px,color:#1f2328
    classDef task fill:#ffffff,stroke:#d9480f,stroke-width:1.5px,color:#1f2328
    classDef table fill:#ffffff,stroke:#1864ab,stroke-width:1.5px,color:#1f2328
    classDef model fill:#ffffff,stroke:#6741d9,stroke-width:1.5px,color:#1f2328

    class RSS,OUT io
    class A,B,C,D,E,F,G,H task
    class T1,T2 table
    class M1,M2 model

    %% Containers
    style CANVAS fill:#ffffff,stroke:#d0d7de,stroke-width:1px,color:#1f2328
    style HOST fill:#f6f8fa,stroke:#8c959f,stroke-width:1.5px,stroke-dasharray:6 4,color:#424a53
    style ING fill:#fff4e6,stroke:#d9480f,stroke-width:2px,color:#a33a08
    style SUM fill:#fff4e6,stroke:#d9480f,stroke-width:2px,color:#a33a08
    style DB fill:#e7f1ff,stroke:#1864ab,stroke-width:2px,color:#0f4c81
    style AI fill:#f3f0ff,stroke:#6741d9,stroke-width:2px,color:#4527a0
```

## How it works

**Ingestion** (`f1_news_pipeline`, daily)

1. Reads the RSS feeds listed in `config/config.py` and skips URLs already in the database.
2. Classifies each title as F1, Formula E, MotoGP, etc. A keyword match runs first. The LLM is called only when no category clearly wins. Entities the LLM returns 4 or more times are added to the keyword list and saved in `keyword_stats`.
3. Tags each article as hard news, opinion or explainer.
4. Scrapes the full article text.

**Summarization** (`f1_summarization`, every 3 days)

1. Loads F1 articles that haven't been summarized yet.
2. Embeds them with `mistral-embed` in batches of 10.
3. Clusters them with HDBSCAN on cosine distance, so articles about the same story end up together.
4. Summarizes each cluster (or single article), then combines the summaries into a 20-minute script.

## Project structure

```
dags/        Airflow DAG definitions
pipeline/    Job entry points called by the DAGs
scrapers/    RSS discovery and article scraping
utils/       Motorsport classifier and Mistral API calls
config/      RSS feeds, seed keywords, prompts
db/          SQLAlchemy queries
alembic/     Database migrations
```

## Running locally

Create a `.env` file with `MISTRAL_API_KEY` and the database settings, then:

```bash
docker compose up --build
```

This starts Postgres and Airflow and runs the migrations. The Airflow UI is at http://localhost:8080.
