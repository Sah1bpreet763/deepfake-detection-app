# 🔬 DeepScan — Deepfake Image Detection System

## 📌 Overview

DeepScan is a web-based deepfake image detection system developed using **Streamlit** and a **MobileNetV2-based deep learning model**. The application allows users to upload facial images and receive a prediction indicating whether the image is **authentic (real)** or **manipulated (deepfake)**, along with a confidence score.

---

## 🚀 Features

* 🧠 Deep learning-based detection using MobileNetV2
* ⚡ Real-time inference (~milliseconds)
* 📊 Confidence scoring and probability visualization
* 🎨 Premium dark-themed user interface
* 📁 Supports JPG, PNG, and WEBP image formats

---

## 🏗️ System Architecture

```
Input Image → Preprocessing → MobileNetV2 → Feature Extraction
→ Dense Layers → Sigmoid Output → Prediction (Real/Fake)
```

---

## ⚙️ Tech Stack

* **Frontend/UI:** Streamlit
* **Model:** TensorFlow / Keras (MobileNetV2)
* **Language:** Python
* **Image Processing:** PIL, NumPy

---

## 📂 Project Structure

```
├── app.py                          # Main Streamlit application
├── deepfake_mobilenet_model.h5     # Trained deep learning model
├── requirements.txt                # Dependencies
├── runtime.txt                     # Python version
├── README.md                       # Documentation
```

---

## ▶️ Run Locally

1. Clone the repository:

```
git clone https://github.com/your-username/deepfake-detection-app.git
cd deepfake-detection-app
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
streamlit run app.py
```

---

## 🌐 Live Deployment

The application is deployed using Streamlit Community Cloud:

👉 (Add your deployed link here)

---

## ⚠️ Disclaimer

* This system is developed for **educational and research purposes only**.
* While the model is trained on curated datasets, it may produce incorrect predictions in certain cases.
* Results should not be considered as definitive proof of image authenticity.

---

## 📈 Future Enhancements

* Support for video-based deepfake detection
* Improved model accuracy using larger datasets
* API integration for external applications
* Model optimization for faster inference

---

## 👨‍💻 Author

Developed as part of an academic project on deepfake detection systems.

---

## 📜 License

This project is intended for academic and demonstration purposes.
