import faiss
import numpy as np
import h5py
import os

# Example: Normalize features before indexing
def build_faiss_index(features):
    features = np.array(features, dtype=np.float32)
    faiss.normalize_L2(features)  # Normalize before adding to the index
    index = faiss.IndexFlatL2(features.shape[1])  # Using L2 distance
    index.add(features)  # Add the normalized features
    return index



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

def process_files_and_build_faiss_index(base_path):
    """Process all .h5 files, load features, and build a FAISS index."""
    features_list = []
    file_paths = []
    
    # Find all .h5 files in the base directory
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                features = load_features(file_path)
                if features is not None:
                    features_list.append(features)
                    file_paths.append(file_path)

    # Convert features list to numpy array
    features_matrix = np.array(features_list, dtype=np.float32)

    # Build FAISS index (L2 distance)
    index = faiss.IndexFlatL2(features_matrix.shape[1])
    index.add(features_matrix)  # Add all features to the index

    # Save the FAISS index to the root folder for future use
    faiss.write_index(index, "./song_similarity.index")  # Save in the root folder
    print(f"FAISS index saved. Total songs processed: {len(file_paths)}")

    return index, file_paths

# Process and build the index
base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
index, file_paths = process_files_and_build_faiss_index(base_path)
