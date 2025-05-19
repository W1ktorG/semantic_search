# import streamlit as st
# import json
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams, PointStruct
# import os
# from dotenv import load_dotenv

# # Załaduj zmienne środowiskowe z pliku .env
# load_dotenv()

# def load_data_and_model():
#     # Wczytaj dane z pliku JSON
#     with open("szkola.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     texts = []

#     # Dodaj mniejsze chunki tekstu dla lepszego dopasowania zapytań
#     texts.append(f"Nazwa szkoły: {data['nazwa_szkoły']}")
#     texts.append(f"Szkola powstala w {data['rok_założenia']}")
#     texts.append(f"Opis: {data['opis']}")
#     texts.append(f"Liczba uczniów: {data['obecna_sytuacja']['liczba_uczniów']}")
#     texts.append(f"Kadra nauczycielska: {data['obecna_sytuacja']['kadra']}")

#     absolwenci = ", ".join(data["absolwenci"]["osiągnięcia"])
#     texts.append(f"Szkołę ukończyło już {data['absolwenci']['łączna_liczba']} absolwentów. Osiągnięcia: {absolwenci}.")

#     # Dodaj info o każdej ze szkół z osobna, profile i zawody jako osobne fragmenty
#     for szkola in data["szkoły"]:
#         typ = szkola["typ"]
#         cykl = szkola["cykl"]

#         texts.append(f"{typ} ({cykl})")

#         profile = szkola.get("profile", [])
#         for p in profile:
#             texts.append(f"{typ} - profil: {p}")

#         zawody = szkola.get("zawody", [])
#         for z in zawody:
#             texts.append(f"{typ} - zawód: {z}")

#     # Załaduj model do embeddingów
#     model = SentenceTransformer("all-MiniLM-L12-v2")
#     embeddings = model.encode(texts)

#     # Połącz się z Qdrant (adres i klucz z .env)
#     qdrant = QdrantClient(
#         url=os.getenv("QDRANT_URL"),
#         api_key=os.getenv("QDRANT_API_KEY")
#     )

#     # Odtwórz (usuń i utwórz) kolekcję
#     qdrant.recreate_collection(
#         collection_name="szkola",
#         vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE)
#     )

#     # Wstaw dane (embeddingi + teksty) do kolekcji
#     points = [
#         PointStruct(id=i, vector=vec.tolist(), payload={"text": txt})
#         for i, (txt, vec) in enumerate(zip(texts, embeddings))
#     ]

#     qdrant.upsert(collection_name="szkola", points=points)

#     return model, qdrant

# # Inicjalizacja modelu i bazy wektorów
# model, qdrant = load_data_and_model()

# # Interfejs użytkownika w Streamlit
# st.title("Asystent Szkoły")
# query = st.text_input("Zadaj pytanie o szkole:")

# if query:
#     query_vector = model.encode([query])[0].tolist()
#     results = qdrant.search(
#         collection_name="szkola",
#         query_vector=query_vector,
#         limit=5
#     )

#     st.subheader("Najtrafniejsze odpowiedzi:")
#     for result in results:
#         st.write(f"- {result.payload['text']} (trafność: {result.score:.4f})")
