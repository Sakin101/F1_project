from scrapers.rss_discovery import discover_rss_utils
from scrapers.article_scraper import scrape_full_article
from utils.llm_call import generate_talking_points,summarize_singleton,summarize_cluster
from db.postgres_utils import update_summarization_status,get_f1_news
from config.config import websites
from utils.llm_call import get_embeddings
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
def run_discovery():
    discover_rss_utils(websites)

def run_scraping():
    from db.postgres_utils import get_pending_article
    pending_articles = get_pending_article()
    print(pending_articles)
    for article in pending_articles:
        scrape_full_article(article['url'])
def prepare_text(result):
    text=f"{result['title']}"
    body=result["body_text"]
    text+=body
    text=text[:8000]
    return text
def get_summary(results):
    texts=[]
    url=[]
    batch_size=10
    embeddings=[]
    for i in range(0,len(results),batch_size):
        batch_results=results[i:i+batch_size]
        batch_text=[prepare_text(r) for r in batch_results]
        batch_url=[r["url"] for r in results[i:i+batch_size]]
        texts.extend(batch_text)
        url.extend(batch_url)        
        batch_embeddings=get_embeddings(batch_text)
        batch_embeddings=[embedding.embedding for embedding in batch_embeddings]
        embeddings.extend(batch_embeddings)
    sim_matrix = cosine_similarity(embeddings)
    dist_matrix = 1 - sim_matrix
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, metric='precomputed')
    labels = clusterer.fit_predict(dist_matrix.astype('float64'))
    cluster_map={}
    singleton_id=int(max(labels)) + 1 if len(labels) else 0
    #breakpoint()
    for url,label,text in zip(url,labels,texts):
        update_summarization_status(url)
        if int(label)==-1:
            cluster_map[singleton_id]=[text]
            singleton_id+=1
        else:
            cluster_map.setdefault(int(label),[]).append(text)
        
    clsuter_digest={}
    for cluster_id,cluster_texts in cluster_map.items():
        print(cluster_id)
        if len(cluster_texts)==1:
            digest=summarize_singleton(cluster_texts)
        else:
            digest=summarize_cluster(cluster_texts[:3])
        clsuter_digest[cluster_id]=digest
    final_script=generate_talking_points(list(clsuter_digest.values()),duration_minutes=20)
    with open("final_script.txt","w") as f:
        f.write(final_script)
    
if __name__=="__main__":
    #run_discovery()
    #run_scraping()
    results=get_f1_news()
    