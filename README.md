# Handwritten and Printed Text Classification

A modern, responsive web application for classifying and localizing text in images. The application can distinguish between handwritten, printed, mixed, and other types of text regions within an image.

## 🚀 Features
- **Modern Web Interface**: Clean, dark-themed UI built for premium user experience.
- **Image Upload**: Drag-and-drop or click-to-upload functionality.
- **Text Localization**: Automatically detects text regions and draws bounding boxes:
  - **Blue**: Printed Text
  - **Green**: Handwritten Text
  - **Red**: Mixed Text
  - **Yellow**: Other
- **Real-time Processing**: Fast classification using a Random Forest model.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn, Joblib
- **Image Processing**: OpenCV, NumPy
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Modern Aesthetics)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yashwanth-m1/handwritten-and-printeted-text-classification.git
   cd handwritten-and-printeted-text-classification
   ```

2. **Install dependencies**:
   ```bash
   pip install -r text_localization_and_classification/requirements.txt
   ```

3. **Ensure model file exists**:
   Make sure `data.joblib` is present in the `text_localization_and_classification/` directory.

## 🏃 How to Run

1. Navigate to the project directory:
   ```bash
   cd text_localization_and_classification
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. Open your browser and go to:
   `http://127.0.0.1:5000`

## 📁 Project Structure
- `app.py`: Main Flask application server.
- `classifier.py`: Core logic for image processing and text classification.
- `data.joblib`: Pre-trained Random Forest model.
- `static/`: Contains frontend assets (HTML, CSS, JS).
- `uploads/`: Temporary storage for uploaded images.

## 📄 License
This project is licensed under the MIT License.