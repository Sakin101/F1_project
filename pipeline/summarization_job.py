from utils.llm_call import (
    generate_talking_points,
    summarize_singleton,
    summarize_cluster,
    get_embeddings,
)
from db.postgres_utils import get_f1_news,update_summarization_status
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
import datetime
def prepare_text(result):
    text = f"{result['title']}{result['body_text']}"
    return text[:8000]

def run_summarization_job():
    results = get_f1_news()
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
    #breakpoint()
    for cluster_id,cluster_texts in cluster_map.items():
        print(cluster_id)
        if len(cluster_texts)==1:
            digest=summarize_singleton(cluster_texts)
        else:
            print(cluster_texts[:3])
            digest=summarize_cluster(cluster_texts[:3])
        clsuter_digest[cluster_id]=digest
    final_script=generate_talking_points(list(clsuter_digest.values()),duration_minutes=20)
    with open(f"final_script{datetime.datetime.now()}.txt", "w") as f:
        f.write(final_script)