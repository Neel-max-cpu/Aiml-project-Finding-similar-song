import os
import h5py
import numpy as np


def load_features(file):
    try:
        print(f"Loading features from {file}...")
        with h5py.File(file, 'r') as f:
            features = f['analysis/segments_timbre'][:].flatten()[:12]  # Take only the first 12 values
            print(f"Loaded features for {file}: {features}")  # Print the loaded features for verification
            return features
    except Exception as e:
        print(f"Error loading {file}: {e}")
        return None

def test_loading_features(base_path):
    files = []
    # Recursively list all files in the directory and subdirectories
    for root, dirs, filenames in os.walk(base_path):
        for filename in filenames:
            if filename.lower().endswith('.h5'):
                full_path = os.path.join(root, filename)
                files.append(full_path)
                print(f"Found file: {full_path}")  # Print each found file path
    
    print(f"Found {len(files)} .h5 files.")
    
    # Load features for each song with diagnostic printing
    for idx, file in enumerate(files):
        print(f"Attempting to load file {idx + 1}/{len(files)}: {file}")
        features = load_features(file)
        if features is None:
            print(f"Skipping {file} due to loading error.")
        else:
            break  # Stop after successfully loading one file for verification

# Run the function to test feature loading
base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
test_loading_features(base_path)
