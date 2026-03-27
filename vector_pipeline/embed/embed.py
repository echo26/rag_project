from langchain_ollama import OllamaEmbeddings

embeddings_model = OllamaEmbeddings(model="bge-m3")


def embed_chunks(chunks):
    for chunk in chunks:
        text = chunk.get("chunked_text")
        chunk["embedding"] = embeddings_model.embed_documents([text])[0]
        yield chunk
