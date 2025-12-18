from sqlalchemy import create_engine,Table, Column, String, MetaData, select
from config import DB_CONN_STING

engine=create_engine(DB_CONN_STING)
metadata=MetaData()

news_articles=Table(
    "news_articles",
    metadata,
    Column("url",String,primary_key=True),
    Column("source",String),
    Column("title",String),
    Column("published_at",String),
    Column("title_type",String),
    Column("motor_sports",String)
    
)

metadata.create_all(engine)

def url_exists(url:str) -> bool:
    with engine.connect() as conn:
        result=conn.execute(select(news_articles.c.url).where(news_articles.c.url==url)).fetchone()
        return result is not None
def insert_new_article(url:str,source:str,title:str,published_at:str):
    with engine.connect() as conn:
        conn.execute(
            news_articles.insert().values(
                url=url,source=source,title=title,published_at=published_at
            )
        )
        conn.commit()
    