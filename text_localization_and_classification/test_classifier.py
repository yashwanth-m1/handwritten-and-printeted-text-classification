from classifier import load_classifier, classify_image
import os

def test():
    model = load_classifier()
    if model is None:
        print("Model loading failed.")
        return
    
    sample_path = "Samples/sample1.jpg"
    if not os.path.exists(sample_path):
        # Try finding any image in Samples
        samples = os.listdir("Samples")
        for s in samples:
            if s.lower().endswith(('.png', '.jpg', '.jpeg')):
                sample_path = os.path.join("Samples", s)
                break
    
    print(f"Testing with {sample_path}...")
    try:
        img, results = classify_image(sample_path, model)
        if img is not None:
            print(f"Success! Detected {len(results)} regions.")
        else:
            print("Classification returned None.")
    except Exception as e:
        print(f"Error during classification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
