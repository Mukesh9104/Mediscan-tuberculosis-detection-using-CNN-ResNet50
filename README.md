🩻 Tuberculosis Detection System using CNN and ResNet50

<img src="assets/cover_tb_image.png">

> **Tuberculosis (TB)** is a chronic infectious disease that primarily affects the lungs and is among the world’s top ten causes of death. Early and accurate diagnosis is crucial to control its spread.
>
> This project uses **Deep Learning**–based models (**Convolutional Neural Network (CNN)** and **ResNet50**) to automatically classify **chest X-ray images** as *Normal* or *Tuberculosis infected*. The system provides a user-friendly **web interface built with Streamlit**, generating predictions, animated insights, and downloadable PDF reports.

---

 Project Overview

The MediScan TB Detection System combines two models for comparative diagnosis:

* CNN Model: Custom-trained from scratch on TB X-ray datasets.
* ResNet50 Model: A pretrained deep residual network fine-tuned for TB classification.

The interface allows users to upload X-ray images, visualize predictions, compare both models’ results, and download an AI-generated diagnostic report.

---

Dataset Description

This project uses the **Tuberculosis Chest X-Ray Dataset** jointly developed by
Qatar University, the University of Dhaka, and collaborators from Malaysia.

* **Total Images:** 3500 Normal + 700 TB-infected (public)
* **Format:** JPEG / PNG chest radiographs
* **Source:** [Kaggle – Tuberculosis (TB) Chest X-Ray Dataset](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset)

Dataset is preprocessed with:

* Image resizing and normalization
* Data augmentation (rotation, shift, zoom, flip)
* Train-test split for model evaluation

---

Technology Stack

| Category                    | Technologies Used                          |
| --------------------------- | ------------------------------------------ |
| **Frontend**                | Streamlit (Python-based Web UI)            |
| **Backend**                 | Python, TensorFlow, Keras                  |
| **Machine Learning Models** | CNN (Custom), ResNet50 (Transfer Learning) |
| **Dataset Handling**        | NumPy, Pandas, OpenCV                      |
| **Visualization**           | Matplotlib                                 |
| **Report Generation**       | FPDF                                       |
| **Environment**             | Virtual Environment (venv)                 |
| **Deployment (optional)**   | Cloud / Local Streamlit Server             |

---

Project Structure

```
Tuberculosis-Diagnosis-System-using-CNN-1/
│
├── web.py                        # Streamlit web interface
├── model/
│   ├── model.h5                  # Trained CNN model
│   └── resnet50_tb.h5            # Fine-tuned ResNet50 model
├── dataset/
│   └── TB_Chest_Radiography_Database/
│       ├── Normal/
│       └── Tuberculosis/
├── Tuber_Classification.ipynb    # Jupyter notebook for model training
├── assets/
│   └── background_lungs.png      # UI background
├── requirements.txt
└── README.md
```

---
 How It Works

1. **User uploads** a chest X-ray image.
2. The system preprocesses the image.
3. **CNN model** predicts infection probability.
4. **ResNet50 model** performs parallel analysis for comparison.
5. Results are shown with:

   * Label (Normal / Tuberculosis)
   * Confidence scores
   * Animated probability graphs
   * Downloadable PDF report
   * Generated report can be sent via email

---

 Installation Guide

 1. Clone this Repository

```bash
git clone https://github.com/mukeshkanna/TB-Detection-CNN-ResNet50.git
cd TB-Detection-CNN-ResNet50
```

 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # (Windows)
# or
source venv/bin/activate    # (Mac/Linux)
```

 3. Install Required Packages

```bash
pip install -r requirements.txt
```

 4. Run the Application

```bash
streamlit run web.py
```

Your app will open at:
🔗 `http://localhost:8501`

---

 Evaluation Metrics

| Metric                   | Description                                           |
| ------------------------ | ----------------------------------------------------- |
| **Accuracy**             | Overall correctness of the predictions                |
| **Precision**            | Correct positive predictions among all positives      |
| **Recall (Sensitivity)** | Ability to detect true TB cases                       |
| **F1-Score**             | Harmonic mean of precision and recall                 |
| **AUC-ROC**              | Area under the ROC curve showing model discrimination |

---

 Features

✅ Dual Model Comparison (CNN vs ResNet50)
✅ AI-Powered X-ray Classification
✅ Animated Confidence Graphs
✅ PDF Diagnostic Report Generator
✅ Simple Streamlit Web UI
✅ Easily Extendable and Cloud Deployable

---

 Future Enhancements

* Integration of Explainable AI (Grad-CAM heatmaps)
* WhatsApp & Email sharing of reports
* Larger multi-hospital dataset support
* Cloud deployment on AWS / Azure

---

Acknowledgements

Dataset: [Tuberculosis (TB) Chest X-Ray Dataset — Kaggle](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset)
Authors: Qatar University, University of Dhaka, and collaborators from Malaysia.

---
Feel free to use, modify, and distribute with proper citation.
