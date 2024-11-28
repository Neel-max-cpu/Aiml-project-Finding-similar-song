import faiss

def load_faiss_index(index_file='./song_similarity.index'):
    """Load the precomputed FAISS index."""
    return faiss.read_index(index_file)

if __name__ == "__main__":
    index = load_faiss_index()
    print(f"Total number of vectors in the FAISS index: {index.ntotal}")
