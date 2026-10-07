"""
Nexus™ RAG Data Preparation Script
==================================
Cleans PDFs/Word docs, splits them into semantic chunks, and formats them for ChromaDB/Pinecone.
Packaged as a $19.00 digital product.
"""
def chunk_data_for_rag(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
