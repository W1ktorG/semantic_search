import streamlit as st
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from dotenv import load_dotenv

load_dotenv()

def load_data_and_model():
    with open("szkola.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [
        data["opis"],
        f"Szkoła została założona w {data['rok_założenia']} roku.",
        f"Szkołę ukończyło ponad {data['absolwenci']['łączna_liczba']} absolwentów. Wielu z nich pełni ważne funkcje w administracji i oświacie.",
        f"Aktualnie do szkoły uczęszcza {data['obecna_sytuacja']['liczba_uczniów']} uczniów.",
        f"Kadra nauczycielska to: {data['obecna_sytuacja']['kadra']}."
    ] + [f"Osiągnięcie absolwenta: {a}" for a in data["absolwenci"]["osiągnięcia"]]

    for szkola in data["szkoły"]:
        typ = szkola["typ"]
        texts.append(f"{typ} - cykl {szkola['cykl']}")
        texts += [f"{typ} - profil: {p}" for p in szkola.get("profile", [])]
        texts += [f"{typ} - zawód: {z}" for z in szkola.get("zawody", [])]

    model = SentenceTransformer("all-MiniLM-L12-v2")
    embeddings = model.encode(texts)

    qdrant = QdrantClient(
        url="https://a1012f34-e7bc-47be-95ac-aba9af1c8853.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key=os.getenv("QDRANT_API_KEY")
    )
    qdrant.recreate_collection(
        collection_name="szkola",
        vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE)
    )

    qdrant.upsert(
        collection_name="szkola",
        points=[PointStruct(id=i, vector=vec.tolist(), payload={"text": txt})
                for i, (txt, vec) in enumerate(zip(texts, embeddings))]
    )

    return model, qdrant


model, qdrant = load_data_and_model()

query = st.text_input("Zadaj pytanie o szkole:")

if query:
    query_vector = model.encode([query])[0].tolist()
    results = qdrant.search(
        collection_name="szkola",
        query_vector=query_vector,
        limit=10
    )

    st.subheader("Najtrafniejsze odpowiedzi:")
    for result in results:
        st.write(f"- {result.payload['text']} (prawdopodobieństwo: {result.score:.4f})")