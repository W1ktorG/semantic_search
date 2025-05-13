import streamlit as st
import json, os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer('all-MiniLM-L12-v2')

def emb_text(text):
    return model.encode(text)

def load_data_and_model():
    with open("szkola.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [
        data["opis"],
        f"Szkoła została założona w {data['rok_założenia']} roku.",
        f"Szkołę ukończyło ponad {data['absolwenci']['łączna_liczba']} absolwentów.",
        f"Aktualnie do szkoły uczęszcza {data['obecna_sytuacja']['liczba_uczniów']} uczniów.",
        f"Kadra nauczycielska to: {data['obecna_sytuacja']['kadra']}."
    ] + [f"Osiągnięcie absolwenta: {a}" for a in data["absolwenci"]["osiągnięcia"]] + [
        f"{szkola['typ']} - cykl {szkola['cykl']}" + 
        ''.join([f"{szkola['typ']} - {key}: {value}" for key, value in szkola.items() if key in ["profile", "zawody"]])
        for szkola in data["szkoły"]
    ]

    embeddings = [emb_text(text) for text in texts]

    qdrant = QdrantClient(
        url="https://a1012f34-e7bc-47be-95ac-aba9af1c8853.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key=os.getenv("QDRANT_API_KEY")
    )

    if not any(c.name == "szkola" for c in qdrant.get_collections().collections):
        qdrant.create_collection(
            collection_name="szkola",
            vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.EUCLID)
        )

    qdrant.upsert(
        collection_name="szkola",
        points=[PointStruct(id=i, vector=vec, payload={"text": txt}) for i, (txt, vec) in enumerate(zip(texts, embeddings))]
    )
    
    return qdrant

qdrant = load_data_and_model()

st.title("Informacje o szkole")

if query := st.text_input("Zadaj pytanie o szkole:"):
    query_vector = emb_text(query).tolist()

    results = qdrant.search(
        collection_name="szkola",
        query_vector=query_vector,
        limit=5
    )

    st.subheader("Najtrafniejsze odpowiedzi:")
    for result in results:
        st.write(f"- {result.payload['text']} (podobieństwo: {result.score:.3f})")
