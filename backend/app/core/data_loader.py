import os
import h5py

def get_h5_files(base_path):
    """
    Get all .h5 files from the directory recursively.
    """
    h5_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.h5'):
                h5_files.append(os.path.join(root, file))
    return h5_files

def inspect_h5_file(file_path):
    """
    Inspect the contents of an .h5 file to see its structure.
    """
    try:
        with h5py.File(file_path, 'r') as f:
            print(f"\nInspecting file: {file_path}")
            print(f"Top-level keys in {file_path}: {list(f.keys())}")
            
            # Check for 'analysis' group and 'segments_timbre' dataset
            if 'analysis' in f:
                analysis_group = f['analysis']
                print("Found 'analysis' group.")
                if 'segments_timbre' in analysis_group:
                    print("Found 'segments_timbre' dataset.")
                else:
                    print("'segments_timbre' dataset NOT found.")
            else:
                print("'analysis' group NOT found in this file.")
    except Exception as e:
        print(f"Error opening {file_path}: {e}")

def load_h5_file(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            if 'analysis' in f:
                analysis_group = f['analysis']
                if 'segments_timbre' in analysis_group:
                    features = analysis_group['segments_timbre'][:]
                    print(f"Loaded features for {file_path} with shape {features.shape}")
                    return features
                else:
                    print(f"'segments_timbre' not found in {file_path}")
            else:
                print(f"'analysis' group not found in {file_path}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return None



# Test the inspection on multiple files
base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
h5_files = get_h5_files(base_path)

# Inspect a few files for structure, you may adjust the range as needed
for file_path in h5_files[:10]:  # Inspect first 10 files for brevity
    inspect_h5_file(file_path)
