# import streamlit as st
# import json
# from openai import OpenAI
# import os
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams, PointStruct
# from dotenv import load_dotenv

# load_dotenv()
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def emb_text(text):
#     return (
#         openai_client.embeddings.create(input=text, model="text-embedding-3-large")
#         .data[0]
#         .embedding
#     )

# def load_data_and_model():
#     with open("szkola.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     texts = [  
#         data["opis"],
#         f"Szkoła została założona w {data['rok_założenia']} roku.",
#         f"Szkołę ukończyło ponad {data['absolwenci']['łączna_liczba']} absolwentów.",
#         f"Aktualnie do szkoły uczęszcza {data['obecna_sytuacja']['liczba_uczniów']} uczniów.",
#         f"Kadra nauczycielska to: {data['obecna_sytuacja']['kadra']}."
#     ] + [f"Osiągnięcie absolwenta: {a}" for a in data["absolwenci"]["osiągnięcia"]]

#     for szkola in data["szkoły"]:
#         typ, cykl = szkola["typ"], szkola["cykl"]
#         texts.append(f"{typ} - cykl {cykl}")
#         if "profile" in szkola: texts.extend([f"{typ} - profil: {p}" for p in szkola["profile"]])
#         if "zawody" in szkola: texts.extend([f"{typ} - zawód: {z}" for z in szkola["zawody"]])

#     embeddings = [emb_text(text) for text in texts]

#     qdrant = QdrantClient(":memory:")
#     qdrant.create_collection(
#         collection_name="szkola",
#         vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE)
#     )

#     qdrant.upsert(
#         collection_name="szkola",
#         points=[PointStruct(id=idx, vector=embedding, payload={"text": text})
#                 for idx, (text, embedding) in enumerate(zip(texts, embeddings))]
#     )

#     return qdrant

# qdrant = load_data_and_model()

# query = st.text_input("Zadaj pytanie o szkole:")

# if query:
#     query_vector = emb_text(query)
    
#     results = qdrant.search(
#         collection_name="szkola",
#         query_vector=query_vector,
#         limit=5
#     )

#     st.subheader("Najtrafniejsze odpowiedzi:")
#     for result in results:
#         st.write(f"- {result.payload['text']} (podobieństwo: {result.score:.3f})")
#         print()
