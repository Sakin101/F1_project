import requests
from bs4 import BeautifulSoup
from db.postgres_utils import get_pending_article,update_article_content

def scrape_full_article(url):
    # try:
    if True:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        soup=BeautifulSoup(response.text,"html.parser")
        paragraphs=soup.find_all("p")
        body_text = "\n".join(p.get_text() for p in paragraphs)
        update_article_content(url,body_text)
        print(f"Scraped articel: {url}")
    # except Exception as e:
    #     print(f"Failed to scrape {url}: {e}")