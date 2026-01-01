from sqlalchemy import func,create_engine,Table, Column, Boolean,String, MetaData, DateTime,select,update, and_
from config import DB_CONN_STING
from datetime import datetime, timedelta
engine=create_engine(DB_CONN_STING)
metadata=MetaData()

news_articles=Table(
    "news_articles",
    metadata,
    Column("url",String,primary_key=True),
    Column("source",String),
    Column("title",String),
    Column("published_at",DateTime(timezone=True),index=True,nullable=True),
    Column("ingested_at",
           DateTime(timezone=True),
           server_default=func.now(),
           nullable=False,
           index=True),
    Column("title_type",String),
    Column("motor_sports",String),
    Column("body_text", String),
    Column("scraping_status",String,default="pending"),
    Column("summarized",Boolean,default=False)
)

#metadata.drop_all(engine)
#metadata.create_all(engine)

def url_exists(url:str):
    with engine.connect() as conn:
        result=conn.execute(select(news_articles.c.url).where(news_articles.c.url==url)).fetchone()
        return result
def insert_new_article(url:str,source:str,title:str,published_at,motorsports_type:str,title_type:str):
    with engine.connect() as conn:
        conn.execute(
            news_articles.insert().values(
                url=url,source=source,title=title,published_at=published_at,motor_sports=motorsports_type,title_type=title_type
            )
        )
        conn.commit()
def get_pending_article():
    with engine.connect() as conn:
        result=conn.execute(
            select(news_articles.c.url, news_articles.c.source).where(
                news_articles.c.scraping_status=="pending")).fetchall()
        return [{"url":row.url,"source":row.source} for row in result]
def update_article_content(url,body_text):
    with engine.connect() as conn:
        stmt=update(news_articles).where(news_articles.c.url==url).values(
            body_text=body_text,
            scraping_status="completed"
        )
        conn.execute(stmt)
        conn.commit()
def update_summarization_status(url):
    with engine.connect() as conn:
        stmt=update(news_articles).where(news_articles.c.url==url).values(
            summarized=True
        )
        conn.execute(stmt)
        conn.commit()
def get_f1_news():
    #three_days_ago = datetime.utcnow() - timedelta(days=3)
    with engine.connect() as conn:
        results = conn.execute(
            select(news_articles.c.body_text,news_articles.c.title,news_articles.c.url).where(
                and_(
                    news_articles.c.title_type == "HARD_NEWS",
                    news_articles.c.motor_sports == "F1",
                    news_articles.c.summarized == False
                    #news_articles.c.published_at >= three_days_ago
                )
            )
        )
        # for result in results:
        #     update_summarization_status(result.url)
        #breakpoint()
        return [{"title":row.title,"body_text":row.body_text,"url":row.url} for row in results]