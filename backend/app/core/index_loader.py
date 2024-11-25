import pickle

def load_precomputed_index_and_paths():
    # Load the precomputed similarity index
    index = pickle.load(open("app/core/precomputed_index.pkl", "rb"))
    
    # Load the file paths (you should have these paths saved from preprocessing)
    file_paths = pickle.load(open("app/core/file_paths.pkl", "rb"))
    
    return index, file_paths
