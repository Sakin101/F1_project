from sqlalchemy import func,create_engine,Table, Column, String, MetaData, DateTime,select,update
from config import DB_CONN_STING

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
    Column("scraping_status",String,default="pending")
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
        return [{"url":r.url,"source":r.source} for r in result]
def update_article_content(url,body_text):
    with engine.connect() as conn:
        stmt=update(news_articles).where(news_articles.c.url==url).values(
            body_text=body_text,
            scraping_status="completed"
        )
        conn.execute(stmt)
        conn.commit()