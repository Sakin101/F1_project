from scrapers.rss_discovery import discover_rss_utils
from config.config import websites

def run_discovery_job():
    discover_rss_utils(websites)