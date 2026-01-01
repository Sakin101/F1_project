import os
from dotenv import load_dotenv
from mistralai import Mistral
load_dotenv()
API_key=os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_key)
def call_llm(prompt):
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
    return response.choices[0].message.content

def get_embeddings(texts):
    model= "mistral-embed"
    embeddings_batch_response = client.embeddings.create(
    model=model,
    inputs=texts,
)
    return embeddings_batch_response.data

def summarize_cluster(cluster_texts):
    prompt = f"""
You are preparing an internal digest for an F1 talking-points show.

Articles:
{chr(10).join("- " + t for t in cluster_texts)}

Task:
Create a short bullet-point digest.

Rules:
- Bullet points only
- Merge repeated ideas
- Casual F1 tone
- Light opinion allowed (mark it)
- Max 200 tokens
"""

    response = call_llm(prompt)
    return response
def summarize_singleton(text):
    prompt = f"""
You are preparing a quick F1 talking-point.

Article:
{text}

Rules:
- 1–2 short bullet points
- No speculation
- Max 80 tokens
"""
    return call_llm(prompt)
def generate_talking_points(digests, duration_minutes=12):
    joined_digests = "\n\n".join(
        f"Story {i+1}:\n{d}"
        for i, d in enumerate(digests)
    )

    prompt = f"""
You are an experienced F1 analyst preparing spoken talking points with a dry, sarcastic edge.

Show length: {duration_minutes} minutes

Tone and style rules:
- Conversational spoken English
- Subtle, dry sarcasm and irony typical of seasoned motorsport commentary
- Light skepticism and knowing humor (assume the audience understands F1 politics and clichés)
- Smooth transitions between stories
- No bullet lists
- About 140 words per minute
- No invented facts or speculation beyond what is stated
- Sarcasm must be grounded in the provided facts, not exaggeration

Story digests:
{joined_digests}
"""

    return call_llm(prompt)