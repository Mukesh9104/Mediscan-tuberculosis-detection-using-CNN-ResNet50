import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile, os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from deep_translator import GoogleTranslator

# ------------------ Page Setup ------------------
st.set_page_config(page_title="MediScan", page_icon="🩻", layout="wide")

# ------------------ Background ------------------
def set_bg_image():
    bg_path = "assets/background_lungs.png"
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            import base64
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            [data-testid="stHeader"] {{
                background: rgba(0,0,0,0);
            }}
            [data-testid="stSidebar"] {{
                background: rgba(0,0,0,0.6);
                color: white;
            }}
            .result-box {{
                background-color: rgba(0,0,0,0.7);
                padding: 15px;
                border-radius: 12px;
                margin-top: 10px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
                color: white;
            }}
            .center {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
set_bg_image()

# ------------------ Language Translator ------------------
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Tamil": "ta",
    "Telugu": "te", "Spanish": "es", "French": "fr",
    "Chinese (Simplified)": "zh-CN"
}
st.sidebar.title("🌐 " + "Translator")
selected_lang = st.sidebar.selectbox("Select Language", options=list(LANGUAGES.keys()))
lang_code = LANGUAGES[selected_lang]

def tr(text):
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# ------------------ Sidebar Info ------------------
st.sidebar.markdown("---")
st.sidebar.subheader(tr("📖 About Tuberculosis"))
st.sidebar.write(tr(
    "Tuberculosis (TB) is a bacterial infection that mainly affects the lungs. "
    "It spreads through tiny droplets released into the air via coughs and sneezes. "
    "Common symptoms include cough with phlegm, chest pain, fever, night sweats, and weight loss."
))
st.sidebar.subheader(tr("💊 Treatment"))
st.sidebar.write(tr(
    "TB is treatable with a course of antibiotics, usually taken for 6 to 9 months. "
    "Early diagnosis and regular medication are essential to ensure full recovery and prevent complications."
))
st.sidebar.subheader(tr("📊 Model Accuracy"))
st.sidebar.write(tr("CNN Model Accuracy: ~92%\n\nResNet50 Model Accuracy: ~95%"))
st.sidebar.subheader(tr("💡 Final Advice"))
st.sidebar.info(tr(
    "This app is for medical assistance and educational purposes. "
    "If TB is suspected, please consult a certified healthcare professional immediately. "
    "Do not rely solely on automated diagnosis."
))

# ------------------ Load Models ------------------
@st.cache_resource
def load_cnn(): return load_model("./model/model.h5")
@st.cache_resource
def load_resnet(): return load_model("./model/resnet50_tb.h5")
cnn_model = load_cnn()
resnet_model = load_resnet()

# ------------------ Email Function ------------------
def send_email(to_email, pdf_bytes):
    from_email = "mediscanreports007@gmail.com"
    app_password = "nqtp hhba ospc hgxm"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "MediScan TB Detection Report"
    msg.attach(MIMEText(tr("Dear User,\n\nPlease find attached your TB detection report.\n\nRegards,\nMediScan Team"), 'plain'))
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename=MediScan_Report.pdf")
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, app_password)
    server.send_message(msg)
    server.quit()

# ------------------ Title ------------------
st.markdown("<h1 style='text-align:center'>💠 MediScan: Tuberculosis Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>" + tr("Upload your Chest X-ray to get predictions from CNN and ResNet50 models.") + "</p>", unsafe_allow_html=True)

# ------------------ File Upload ------------------
# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(tr("Upload Chest X-ray"), type=["jpg","jpeg","png"], key="uploader")

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img = img.resize((400,400))

    # --- Added Fix: Reset analysis if new image uploaded ---
    if 'uploaded_img' not in st.session_state or uploaded_file.name != st.session_state.get('last_uploaded'):
        st.session_state['uploaded_img'] = img
        st.session_state['last_uploaded'] = uploaded_file.name
        st.session_state['analysis_done'] = False
        st.session_state.pop('cnn_label', None)
        st.session_state.pop('resnet_label', None)
    # -------------------------------------------------------



# ------------------ PDF Generation ------------------
def generate_pdf(img, cnn_label, cnn_conf, resnet_label, resnet_conf):
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.set_fill_color(0,102,204)
    pdf.set_text_color(255,255,255)
    pdf.cell(0,10,tr("MediScan TB Detection Report"),0,1,"C",fill=True)
    pdf.ln(3)

    # Image
    img_pdf = img.copy()
    img_pdf.thumbnail((200,200))
    img_path = os.path.join(tempfile.gettempdir(),"xray_temp.png")
    img_pdf.save(img_path)
    pdf.image(img_path,x=(210-90)/2,w=90)
    pdf.ln(5)

    # Predictions and confidence bars
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,8,tr("Model Predictions:"),ln=1)
    pdf.set_font("Arial","",12)
    pdf.cell(0,6,f"CNN Model: {cnn_label} ({cnn_conf*100:.2f}%)",ln=1)
    pdf.cell(0,6,f"ResNet50 Model: {resnet_label} ({resnet_conf*100:.2f}%)",ln=1)

    # Confidence bars
    pdf.set_fill_color(255,0,0)
    pdf.rect(30,pdf.get_y(),cnn_conf*150,5,'F')
    pdf.set_xy(30,pdf.get_y()+6)
    pdf.set_fill_color(0,0,255)
    pdf.rect(30,pdf.get_y(),resnet_conf*150,5)
    pdf.ln(12)

    # Final conclusion
    final = "TB Detected" if (cnn_conf>=0.5 or resnet_conf>=0.5) else "Normal"
    pdf.set_font("Arial","B",13)
    pdf.cell(0,7,f"{tr('Final Conclusion')}: {tr(final)}",ln=1)
    pdf.ln(2)
    pdf.set_font("Arial","",12)

    # Professional paragraph descriptions
    if final=="TB Detected":
        description = tr(
            "The patient shows radiological signs consistent with Tuberculosis. "
            "Immediate consultation with a pulmonologist or infectious disease specialist is strongly advised. "
            "Confirmatory diagnostic tests, such as sputum culture, GeneXpert, or chest CT scan, are recommended to establish a definitive diagnosis. "
            "Strict adherence to the prescribed anti-TB medication regimen is crucial for effective treatment and recovery, and monitoring for potential side effects such as hepatotoxicity or neuropathy should be performed. "
            "The patient should avoid exposing others if infectious to prevent disease transmission. "
            "Regular follow-ups are necessary to assess treatment response and adjust therapy as needed. "
            "Maintaining proper nutrition and hydration will support immune function, and any worsening symptoms such as persistent fever, hemoptysis, or unexplained weight loss should be reported immediately. "
            "Avoidance of smoking or exposure to lung irritants is essential to reduce complications."
        )
    else:
        description = tr(
            "No radiological evidence of Tuberculosis was detected in the chest X-ray. "
            "The patient should continue routine health monitoring and maintain regular medical check-ups. "
            "Maintaining a healthy lifestyle, including a balanced diet, regular exercise, and adequate rest, is recommended. "
            "It is important to monitor for any respiratory symptoms such as persistent cough, fever, or night sweats. "
            "Ensuring proper hygiene, following vaccination schedules, and avoiding exposure to high-risk environments are important preventive measures. "
            "Promoting lung health through physical activity and avoidance of pollutants or smoking is advised. "
            "Awareness of family medical history and prompt reporting of any new or unusual symptoms to a physician is encouraged. "
            "Mental and emotional well-being should also be maintained to support overall immune health, and immediate medical attention should be sought if any respiratory illness develops."
        )
    pdf.multi_cell(0,6,description)
    return bytes(pdf.output(dest='S'))

# ------------------ Analysis ------------------
if 'uploaded_img' in st.session_state:
    img = st.session_state['uploaded_img']
    st.markdown("<div class='center' style='margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)
    st.image(img,width=300)
    st.markdown("</div>", unsafe_allow_html=True)

    if 'analysis_done' not in st.session_state:
        st.session_state['analysis_done'] = False

    run_analysis = st.button(tr("Run Analysis"), key="run_analysis")
    if run_analysis or st.session_state['analysis_done']:
        if not st.session_state['analysis_done']:
            with st.spinner(tr("Analyzing...")):
                # CNN
                gray_img = img.convert("L").resize((500,500))
                cnn_input = np.expand_dims(np.array(gray_img)/255.0, axis=(0,-1))
                cnn_conf = float(cnn_model.predict(cnn_input)[0][0])
                cnn_label = tr("Tuberculosis") if cnn_conf>=0.5 else tr("Normal")
                # ResNet
                res_img = img.resize((224,224))
                x = keras_image.img_to_array(res_img)
                x = np.expand_dims(x,axis=0)/255.0
                resnet_conf = float(resnet_model.predict(x)[0][0])
                resnet_label = tr("Tuberculosis") if resnet_conf>=0.5 else tr("Normal")
                # save results
                st.session_state['cnn_conf'] = cnn_conf
                st.session_state['cnn_label'] = cnn_label
                st.session_state['resnet_conf'] = resnet_conf
                st.session_state['resnet_label'] = resnet_label
                st.session_state['analysis_done'] = True
                # generate pdf
                st.session_state['pdf_bytes'] = generate_pdf(img,cnn_label,cnn_conf,resnet_label,resnet_conf)

        # show results with horizontal bar charts
        def plot_bar(value,color,title):
            fig, ax = plt.subplots(figsize=(4,0.6))
            ax.barh([0],[value], color=color)
            ax.set_xlim(0,1)
            ax.set_yticks([])
            ax.set_xlabel(tr("Confidence"))
            ax.set_title(title)
            for i,v in enumerate([value]):
                ax.text(v + 0.01, i, f"{v*100:.2f}%", va='center')
            plt.tight_layout()
            return fig

        col1,col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='result-box'><h4>CNN Result</h4><p>{st.session_state['cnn_label']}</p><p>{st.session_state['cnn_conf']*100:.2f}%</p></div>",unsafe_allow_html=True)
            st.pyplot(plot_bar(st.session_state['cnn_conf'],'red','CNN'))
        with col2:
            st.markdown(f"<div class='result-box'><h4>ResNet50 Result</h4><p>{st.session_state['resnet_label']}</p><p>{st.session_state['resnet_conf']*100:.2f}%</p></div>",unsafe_allow_html=True)
            st.pyplot(plot_bar(st.session_state['resnet_conf'],'blue','ResNet50'))

        # Download & Email
        st.markdown("<div class='center' style='margin-top:20px;'>",unsafe_allow_html=True)
        st.download_button(tr("Download PDF Report"), st.session_state['pdf_bytes'], file_name="MediScan_Report.pdf", mime="application/pdf")
        with st.form(key="email_form"):
            email = st.text_input(tr("Enter Email to send the report"))
            submitted = st.form_submit_button(tr("Send Report via Email"))
            if submitted and email:
                try:
                    send_email(email, st.session_state['pdf_bytes'])
                    st.balloons()
                    st.success(tr(f"Report sent successfully to {email}!"))
                except Exception as e:
                    st.error(tr(f"Email sending failed: {e}"))
        st.markdown("</div>",unsafe_allow_html=True)
