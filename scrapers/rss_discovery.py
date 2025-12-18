import os
import time
import feedparser
from db.postgres_utils import url_exists

from dotenv import load_dotenv
from google import genai
from config import CLASSIFICATION_PROMPT_TEMPLATE
from mistralai import Mistral

load_dotenv()
#API_key=os.getenv("GEMINI_API_KEY")
API_key=os.getenv("MISTRAL_API_KEY")
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
#client = genai.Client(api_key=API_key)

client = Mistral(api_key=API_key)
def discover_rss_utils(feeds:list):
    new_urls_count=0
    for feed_url in feeds:
        feed= feedparser.parse(feed_url)
        #breakpoint()
        for entry in feed.entries:
            url=entry.link
            title=entry.title
            #breakpoint()
            published=entry.get("published",None)
            prompt=CLASSIFICATION_PROMPT_TEMPLATE.format(title=title)
            print(prompt)
            model="ministral-3b-2410"
            response=client.chat.complete(
                model=model,
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )
            print(title)
            breakpoint()
            print(response.choices[0].message.content)
            time.sleep(10)
            
            
if __name__=="__main__":
    discover_rss_utils(["https://www.the-race.com/rss"])      