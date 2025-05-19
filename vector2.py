import streamlit as st
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def load_data_and_model():
    qdrant = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=60
    )

    try:
        qdrant.get_collection(collection_name="news")
    except Exception as e:
        st.write("Kolekcja nie istnieje. Tworzę nową kolekcję.")

        with open("news.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        texts = []
        payloads = []

        for item in data:
            title = item.get("title", "")
            date = item.get("date", "")
            content = item.get("content", "")
            link = item.get("link", "")
            
            # Łączymy tytuł, datę i treść dla lepszego wyszukiwania
            combined_text = f"{title} {date} {content}".strip()
            texts.append(combined_text)
            payloads.append({
                "title": title,
                "date": date,
                "content": content,
                "link": link,
                "ID": item.get("ID", "")
            })

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(texts)

        qdrant.recreate_collection(
            collection_name="news",
            vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE),
        )

        qdrant.upsert(
            collection_name="news",
            points=[
                PointStruct(id=i, vector=vec.tolist(), payload=payloads[i])
                for i, vec in enumerate(embeddings)
            ]
        )

        st.write("Kolekcja 'news' została utworzona i dane zostały załadowane.")

    model = SentenceTransformer("all-MiniLM-L6-v2")  
    
    return model, qdrant

model, qdrant = load_data_and_model()

st.title("Wyszukiwarka wiadomości")

query = st.text_input("Zadaj pytanie:")

if query:
    query_vector = model.encode([query])[0].tolist()
    results = qdrant.search(
        collection_name="news",
        query_vector=query_vector,
        limit=5
    )

    st.subheader("Najtrafniejsze wiadomości:")
    for result in results:
        title = result.payload.get("title", "Brak tytułu")
        date = result.payload.get("date", "Brak daty")
        content = result.payload.get("content") or ""
        link = result.payload.get("link", "")

        st.write(f"###  {title}")
        st.write(f" {date}")
    
        if link and link != "no link":
            st.write(f" [Link do artykułu]({link})")
    
        st.write(content[:300] + "..." if len(content) > 300 else content)
    
        st.write(f"**Trafność:** {result.score:.4f}")
        st.write("---")
