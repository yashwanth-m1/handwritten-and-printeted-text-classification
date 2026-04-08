import sys
import numpy as np
import cv2
from joblib import load
def load_classifier(model_path="data.joblib"):
    try:
        return load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def checker(img):
    arr = []
    rows = img.shape[0]
    cols = img.shape[1]
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    arr.append(rows)
    arr.append(cols)
    arr.append(rows / cols if cols != 0 else 0)
    
    retval, bwMask = cv2.threshold(img, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    myavg = 0
    for xx in range(0, cols):
        mycnt = 0
        for yy in range(0, rows):
            if bwMask[yy, xx] == 0:
                mycnt += 1
        myavg += (mycnt * 1.0) / rows
    myavg = myavg / cols if cols != 0 else 0
    arr.append(myavg)
    
    change = 0
    for xx in range(0, rows):
        mycnt = 0
        for yy in range(0, cols - 1):
            if bwMask[xx, yy] != bwMask[xx, yy + 1]:
                mycnt += 1
        change += (mycnt * 1.0) / cols
    change = change / rows if rows != 0 else 0
    arr.append(change)
    
    return [arr]

def classify_image(image_path, model):
    img = cv2.imread(image_path)
    if img is None:
        return None, "Error: Could not read image."
    
    hgt, wdt = img.shape[:2]
    hBw = hgt / float(wdt) if wdt != 0 else 1.0
    dim = (576, int(576 * hBw))
    img_resized = cv2.resize(img, dim)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    linek = np.zeros((11, 11), dtype=np.uint8)
    linek[5, ...] = 1
    x = cv2.morphologyEx(gray, cv2.MORPH_OPEN, linek, iterations=1)
    gray = cv2.subtract(gray, x)
    
    kernel = np.ones((5, 5), np.uint8)
    ret2, gray = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    gray = cv2.dilate(gray, kernel, iterations=1)
    
    contours, _ = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    results = []
    for cnt in contours:
        x_start, y_start, width, height = cv2.boundingRect(cnt)
        if width < 5 or height < 5: continue
        
        roi = img_resized[y_start:y_start+height, x_start:x_start+width]
        features = checker(roi)
        prediction = model.predict(features)[0]
        
        color = (0, 0, 0)
        label = prediction
        if prediction == 'Printed_extended':
            color = (255, 0, 0) # Blue
        elif prediction == 'Handwritten_extended':
            color = (0, 255, 0) # Green
        elif prediction == 'Mixed_extended':
            color = (0, 0, 255) # Red
        elif prediction == 'Other_extended':
            color = (0, 255, 255) # Cyan
            
        cv2.rectangle(img_resized, (x_start, y_start), (x_start + width, y_start + height), color, 2)
        results.append({"label": str(label), "box": [int(x_start), int(y_start), int(width), int(height)]})
        
    return img_resized, results
