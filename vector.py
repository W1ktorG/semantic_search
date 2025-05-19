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

    chunks = []

    chunks.append("Opis szkoły: " + data["opis"])
    chunks.append(f"Nazwa szkoły: {data['nazwa_szkoły']}")
    chunks.append(f"Rok założenia szkoły: {data['rok_założenia']}")
    chunks.append(f"Liczba uczniów: {data['obecna_sytuacja']['liczba_uczniów']}")
    chunks.append(f"Kadra nauczycielska: {data['obecna_sytuacja']['kadra']}")
    chunks.append(f"Liczba absolwentów: {data['absolwenci']['łączna_liczba']}")

    for osiągnięcie in data["absolwenci"]["osiągnięcia"]:
        chunks.append(f"Osiągnięcie absolwenta: {osiągnięcie}")

    for szkola in data["szkoły"]:
        typ = szkola["typ"]
        cykl = szkola["cykl"]
        chunks.append(f"{typ} - cykl kształcenia: {cykl}")
        for profil in szkola.get("profile", []):
            chunks.append(f"{typ} - profil: {profil}")
        for zawod in szkola.get("zawody", []):
            chunks.append(f"{typ} - zawód: {zawod}")

    model = SentenceTransformer("all-MiniLM-L12-v2")
    embeddings = model.encode(chunks)

    qdrant = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    qdrant.recreate_collection(
        collection_name="szkola",
        vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE)
    )

    qdrant.upsert(
        collection_name="szkola",
        points=[PointStruct(id=i, vector=vec.tolist(), payload={"text": txt})
                for i, (txt, vec) in enumerate(zip(chunks, embeddings))]
    )

    return model, qdrant

model, qdrant = load_data_and_model()

query = st.text_input("Zadaj pytanie o szkole:")

if query:
    query_vector = model.encode([query])[0].tolist()
    results = qdrant.search(
        collection_name="szkola",
        query_vector=query_vector,
        limit=5
    )

    st.subheader("Najtrafniejsze odpowiedzi:")
    for result in results:
        st.write(f"- {result.payload['text']} (prawdopodobieństwo: {result.score:.2f})")
