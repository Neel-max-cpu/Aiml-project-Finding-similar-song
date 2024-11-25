import os
import numpy as np
import faiss
import h5py

# Function to load features from .h5 files
def load_features(file):
    """Load audio features from an .h5 file."""
    try:
        with h5py.File(file, 'r') as f:
            if 'analysis/segments_timbre' in f:
                features = f['analysis/segments_timbre'][:].flatten()[:12]
                return features
    except Exception as e:
        print(f"Error loading {file}: {e}")
    return None

# Build FAISS index with normalized features
def build_faiss_index(dataset_path):
    """Build a FAISS index using cosine similarity (inner product)."""
    file_paths = []
    features = []

    # Iterate through all .h5 files in the dataset path
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
                
                feature = load_features(file_path)
                if feature is not None:
                    features.append(feature)
    
    # Convert the features list to a numpy array
    features = np.array(features, dtype=np.float32)
    
    # Build FAISS index using inner product for cosine similarity
    index = faiss.IndexFlatIP(features.shape[1])  # Inner product index
    index.add(features)  # Add normalized features to the index
    
    # Save the index to disk
    faiss.write_index(index, './song_similarity.index')

    # Save the file paths to a .npy file
    np.save('./file_paths.npy', file_paths)

    return index, file_paths

# Example usage: Provide the path to the dataset
dataset_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/'
index, file_paths = build_faiss_index(dataset_path)

print("FAISS index and file paths file saved!")
