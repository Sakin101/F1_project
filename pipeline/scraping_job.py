from scrapers.article_scraper import scrape_full_article
from db.postgres_utils import get_pending_article

def run_scraping_job():
    pending_articles = get_pending_article()
    for article in pending_articles:
        scrape_full_article(article["url"])