import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image
import tensorflow as tf
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import os, re, tempfile, time
from fpdf import FPDF

# ---------------- UI Setup ----------------
st.set_page_config(page_title="MediScan", page_icon="🩻", layout="wide")

# Background setup
def set_bg_image():
    try:
        with open("assets/background_lungs.png.png", "rb") as f:
            encoded = f.read()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded.decode('utf-8', errors='ignore')}");
                background-size: cover;
                background-attachment: fixed;
            }}
            .result-box {{
                background-color: rgba(0,0,0,0.7);
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
                color: white;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except:
        pass

set_bg_image()

# ---------------- Load Models ----------------
@st.cache_resource
def load_cnn():
    return load_model("./model/model.h5")

@st.cache_resource
def load_resnet():
    return ResNet50(weights="imagenet")

cnn = load_cnn()
resnet = load_resnet()

st.title("💠 MediScan: Tuberculosis Detection Using Chest X-rays")
st.markdown("Upload your chest X-ray and compare predictions from **CNN** and **ResNet50**.")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader("📤 Upload Chest X-ray", type=["jpg","jpeg","png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded X-ray", use_column_width=True)

    if st.button("🧠 Run Analysis"):
        with st.spinner("Analyzing..."):
            # ---------------- CNN Prediction ----------------
            gray_img = img.convert("L").resize((500, 500))
            cnn_input = np.expand_dims(np.array(gray_img) / 255.0, axis=(0, -1))
            cnn_pred = cnn.predict(cnn_input)[0][0]
            cnn_label = "Tuberculosis" if cnn_pred >= 0.5 else "Normal"

            # ---------------- ResNet50 Prediction ----------------
            resnet_img = img.resize((224, 224))
            x = keras_image.img_to_array(resnet_img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = resnet.predict(x)
            decoded = decode_predictions(preds, top=1)[0][0]
            resnet_label = decoded[1]
            resnet_conf = float(decoded[2])

            # ---------------- Animated Charts ----------------
            def animate_chart(score, title, color):
                chart_placeholder = st.empty()
                for val in np.linspace(0, score, 30):
                    fig, ax = plt.subplots()
                    ax.plot([0, 1], [0, val], color=color, marker="o")
                    ax.set_ylim([0, 1])
                    ax.set_title(f"{title} Prediction")
                    ax.set_ylabel("Probability")
                    ax.set_xticks([0,1])
                    ax.set_xticklabels(["Start","Score"])
                    chart_placeholder.pyplot(fig)
                    time.sleep(0.02)

            # ---------------- Display Results ----------------
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"<div class='result-box'><h4>CNN Result</h4><p>Label: {cnn_label}</p><p>Confidence: {cnn_pred*100:.2f}%</p></div>", unsafe_allow_html=True)
                animate_chart(cnn_pred, "CNN", "red")

            with col2:
                st.markdown(f"<div class='result-box'><h4>ResNet50 Result</h4><p>Label: {resnet_label}</p><p>Confidence: {resnet_conf*100:.2f}%</p></div>", unsafe_allow_html=True)
                animate_chart(resnet_conf, "ResNet50", "blue")

            # ---------------- PDF Report ----------------
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="MediScan TB Detection Report", ln=1, align="C")
            pdf.cell(200, 10, txt=f"CNN: {cnn_label} ({cnn_pred*100:.2f}%)", ln=1)
            pdf.cell(200, 10, txt=f"ResNet50: {resnet_label} ({resnet_conf*100:.2f}%)", ln=1)
            final = "TB Detected" if (cnn_pred >= 0.5 or "tuberculosis" in resnet_label.lower()) else "Normal"
            pdf.cell(200, 10, txt=f"Final Conclusion: {final}", ln=1)

            pdf_path = os.path.join(tempfile.gettempdir(), f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name="MediScan_Report.pdf")
        st.success("Analysis Complete!")