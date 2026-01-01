import os
import time
import feedparser
from google import genai
from config import CLASSIFICATION_PROMPT_TEMPLATE,websites
from mistralai import Mistral
from datetime import timezone
from dateutil import parser

from db.postgres_utils import url_exists,insert_new_article
from utils.llm_call import call_llm
from utils.classify_motorsports import classify_motorsport
#API_key=os.getenv("GEMINI_API_KEY")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
#client = genai.Client(api_key=API_key)


def discover_rss_utils(feeds:list):
    new_urls_count=0
    for feed_url in feeds:
        feed= feedparser.parse(feed_url)
        #breakpoint()
        for entry in feed.entries:
            url=entry.link
            if url_exists(url) is None:
                title=entry.title
                #breakpoint()
                published=entry.get("published",None)
                dt=parser.parse(published)
                publised_at_utc=dt.astimezone(timezone.utc)
                #breakpoint()
                mototrsports_classification=classify_motorsport(title)
                prompt=CLASSIFICATION_PROMPT_TEMPLATE.format(title=title)
                time.sleep(3)
                news_type=call_llm(prompt)
                print("Article not found")
                insert_new_article(url=url,source=feed_url,title=title,published_at=published,motorsports_type=mototrsports_classification,title_type=news_type)
            else:
                print("Url_exists")            
                    
            
# if __name__=="__main__":
#     discover_rss_utils(websites)