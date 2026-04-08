import sys
import os
import joblib
import sklearn.ensemble

def debug_load():
    try:
        # Try different monkeypatching
        import sklearn.ensemble._forest as forest
        sys.modules['sklearn.ensemble.forest'] = forest
        
        # Also try tree if needed
        import sklearn.tree._tree as tree
        sys.modules['sklearn.tree.tree'] = sklearn.tree # Older version had it here
        
        model = joblib.load("data.joblib")
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        return True
    except Exception as e:
        print(f"Failed to load: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_load()
