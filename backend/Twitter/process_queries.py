from pinecone import Pinecone
import os
from dotenv import load_dotenv
from .analyze import get_subqueries, get_description
from openai import OpenAI
import uuid

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("xsearch")

openai_client = OpenAI(
    organization="org-1EDbnzjdGhFGeAAiDIyKSyc6",
)
def generate_embeddings(query):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
        )
    return response.data[0].embedding

def upload_embeddings(query, embeddings, subqueries, description):
    index.upsert(vectors=[{
        "id": str(uuid.uuid4()),
        "values": embeddings,
        "metadata": {
            "subqueries": subqueries,
            "description": description
        }
    }])
    return True

def get_metadata(id):
    res = index.fetch(ids=[id])
    return res.vectors[id].metadata

def check_embeddings(query):
    embeddings = generate_embeddings(query)

    res = index.query(
    vector=embeddings,
    top_k=1,
    include_values=True
    )
    if len(res.matches) == 0:
        return None
    if res.matches[0].score >= 0.95:
        return get_metadata(res.matches[0].id)
    else:
        return None

def analyze(query):
    check = check_embeddings(query)

    if check!=None:
        return check

    subqueries = get_subqueries(query)
    description = get_description(query)
    embeddings = generate_embeddings(query)
    upload_embeddings(query, embeddings, subqueries, description)
    print("Uploaded")
    return {
        "subqueries": subqueries,
        "description": description
    }

# if __name__ == "__main__":
#     print(analyze("NBA Playoffs"))