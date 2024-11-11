# backend/app/core/data_loader.py

import os
import h5py
import numpy as np

def get_h5_files(base_path):
    """Recursively get all .h5 files from the directory."""
    h5_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.h5'):
                h5_files.append(os.path.join(root, file))
    return h5_files

def load_h5_file(file_path):
    """Load features from a .h5 file."""
    try:
        with h5py.File(file_path, 'r') as f:
            # Here you can specify which features you want to extract.
            # For example, extracting "analysis/segments_timbre":
            features = f['analysis/segments_timbre'][:]
            return np.mean(features, axis=0)  # You can also return other aggregates
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None
