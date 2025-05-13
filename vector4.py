# import streamlit as st
# import json
# import os
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams, PointStruct

# # Konfiguracja
# load_dotenv()
# COLLECTION_NAME = "szkola_info"
# MODEL_NAME = "multi-qa-MiniLM-L6-cos-v1"

# @st.cache_resource
# def init_qdrant():
#     """Inicjalizacja połączenia z Qdrant Cloud"""
#     try:
#         client = QdrantClient(
#             url=os.getenv("QDRANT_URL"),
#             api_key=os.getenv("QDRANT_API_KEY"),
#             timeout=10
#         )
#         # Test połączenia
#         client.get_collections()
#         return client
#     except Exception as e:
#         st.error(f"Błąd połączenia z Qdrant: {str(e)}")
#         return None

# @st.cache_resource
# def load_model():
#     """Ładowanie modelu embeddingowego"""
#     return SentenceTransformer(MODEL_NAME)

# def load_school_data():
#     """Ładowanie danych szkoły z pliku JSON"""
#     try:
#         with open("szkola.json", "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         st.error(f"Błąd ładowania danych szkoły: {str(e)}")
#         return None

# def prepare_texts(data):
#     """Przygotowanie tekstów do indeksowania"""
#     texts = [
#         data["opis"],
#         f"Szkoła {data['nazwa_szkoły']} została założona w {data['rok_założenia']} roku.",
#         f"Szkołę ukończyło ponad {data['absolwenci']['łączna_liczba']} absolwentów.",
#         f"Aktualnie do szkoły uczęszcza {data['obecna_sytuacja']['liczba_uczniów']} uczniów.",
#         f"Kadra nauczycielska: {data['obecna_sytuacja']['kadra']}."
#     ] + [f"Osiągnięcie absolwentów: {a}" for a in data["absolwenci"]["osiągnięcia"]]

#     for szkola in data["szkoły"]:
#         typ, cykl = szkola["typ"], szkola["cykl"]
#         texts.append(f"{typ} - cykl kształcenia: {cykl}")
#         if "profile" in szkola: 
#             texts.extend([f"{typ} - profil: {p}" for p in szkola["profile"]])
#         if "zawody" in szkola: 
#             texts.extend([f"{typ} - zawód: {z}" for z in szkola["zawody"]])
    
#     return texts

# def initialize_collection(qdrant_client, model, data):
#     """Inicjalizacja kolekcji w Qdrant"""
#     texts = prepare_texts(data)
#     embeddings = model.encode(texts)

#     try:
#         qdrant_client.get_collection(COLLECTION_NAME)
#         qdrant_client.delete_collection(COLLECTION_NAME)
#     except:
#         pass

#     qdrant_client.create_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config=VectorParams(
#             size=embeddings.shape[1],
#             distance=Distance.COSINE
#         )
#     )

#     points = [
#         PointStruct(
#             id=idx,
#             vector=embedding.tolist(),
#             payload={"text": text, "source": "szkola.json"}
#         )
#         for idx, (text, embedding) in enumerate(zip(texts, embeddings))
#     ]
    
#     qdrant_client.upsert(
#         collection_name=COLLECTION_NAME,
#         points=points
#     )

# def main():
#     st.title("System informacji o szkole")
    
#     # Inicjalizacja
#     qdrant_client = init_qdrant()
#     model = load_model()
#     data = load_school_data()

#     if not all([qdrant_client, model, data]):
#         st.error("Inicjalizacja nie powiodła się. Sprawdź błędy powyżej.")
#         return

#     st.subheader(data["nazwa_szkoły"] if data else "")  # Move this after data is loaded

#     # Inicjalizacja kolekcji (tylko przy pierwszym uruchomieniu)
#     if st.button("Zainicjuj bazę wiedzy"):
#         with st.spinner("Przygotowywanie danych..."):
#             initialize_collection(qdrant_client, model, data)
#         st.success("Baza wiedzy zainicjowana!")

#     # Wyszukiwanie
#     query = st.text_input("Zadaj pytanie o szkole:")
#     if query:
#         with st.spinner("Szukam odpowiedzi..."):
#             query_vector = model.encode(query).tolist()
#             results = qdrant_client.search(
#                 collection_name=COLLECTION_NAME,
#                 query_vector=query_vector,
#                 limit=3,
#                 with_payload=True,
                
#             )

#         if results:
#             st.subheader("Najlepsze odpowiedzi:")
#             for idx, hit in enumerate(results, 1):
#                 st.markdown(f"**{idx}. {hit.payload['text']}**  \n"
#                           f"*Prawdopodobieństwo: {hit.score:.2f}*")
#         else:
#             st.warning("Nie znaleziono odpowiedzi na Twoje pytanie.")
