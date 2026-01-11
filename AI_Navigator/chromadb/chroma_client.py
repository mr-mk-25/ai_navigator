import chromadb
from services.embeddings import embed_text

client = chromadb.Client()
collection = client.get_or_create_collection("internships")

def add_opportunity(opp):
    text = f"{opp['title']} {', '.join(opp['skills_required'])}"
    collection.add(
        documents=[text],
        metadatas=[opp],
        embeddings=[embed_text(text)],
        ids=[str(opp["id"])]
    )

def search_opportunities(student_profile, top_k=5):
    text = f"{', '.join(student_profile['skills'])}"
    results = collection.query(
        query_embeddings=[embed_text(text)],
        n_results=top_k
    )
    return results["metadatas"][0]
