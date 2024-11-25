import faiss
import numpy as np
import h5py
import os

# Normalize the feature vector for cosine similarity
def normalize_features(features):
    """Normalize the feature vector."""
    return features / np.linalg.norm(features)

# Load the precomputed FAISS index (use IndexFlatIP for cosine similarity)
def load_faiss_index(index_file='./song_similarity.index'):
    """Load the precomputed FAISS index."""
    index = faiss.read_index(index_file)
    return index

# Load and normalize audio features from an .h5 file
def load_features(file):
    """Load and normalize audio features from an .h5 file."""
    try:
        with h5py.File(file, 'r') as f:
            if 'analysis/segments_timbre' in f:
                features = f['analysis/segments_timbre'][:].flatten()[:12]
                return normalize_features(features)  # Normalize the features
    except Exception as e:
        print(f"Error loading {file}: {e}")
    return None

# Load the list of file paths (make sure this list is saved from the index creation step)
def load_file_paths(file_paths_file='./file_paths.npy'):
    """Load the list of file paths used for indexing."""
    return np.load(file_paths_file, allow_pickle=True)

# Find similar songs using the FAISS index (cosine similarity via inner product)
def find_similar_songs(query_file, index, file_paths, k=5):
    """Find the top k most similar songs using the FAISS index."""
    query_features = load_features(query_file)
    if query_features is None:
        return []
    
    query_feature = np.array([query_features], dtype=np.float32)
    
    distances, indices = index.search(query_feature, k)
    similar_songs = [(file_paths[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    return similar_songs

# Example usage
index = load_faiss_index()  # Load the precomputed index
file_paths = load_file_paths()  # List of file paths corresponding to the index (from build_faiss_index.py)

query_file = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5'
similar_songs = find_similar_songs(query_file, index, file_paths)

# Display similar songs
for song, similarity in similar_songs:
    print(f"Song: {song}, Similarity: {similarity:.4f}")
