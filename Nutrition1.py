from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
import streamlit as st
from google_auth_oauthlib.flow import Flow
import os
import random
import google.generativeai as genai
import matplotlib.pyplot as plt
from PIL import Image

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import queue
import threading
import speech_recognition as sr
from gtts import gTTS
import tempfile
import time
import random
import cv2



def get_language_instruction(lang):
    if lang == "Hindi":
        return "Answer in simple Hindi."
    elif lang == "Hinglish":
        return "Answer in Hinglish (Hindi + English mix)."
    else:
        return "Answer in simple English."



def smart_health_score():
    score = 0
    
    if st.session_state.get("water", 0) >= 8:
        score += 20
        
    if len(st.session_state.get("weight_history", [])) > 5:
        score += 20
        
    if len(st.session_state.get("sleep_history", [])) > 3:
        score += 20
        
    if len(st.session_state.get("mood_history", [])) > 3:
        score += 20
        
    if st.session_state.get("streak", 0) > 3:
        score += 20
        
    return score


if "song_index" not in st.session_state:
    st.session_state.song_index = 0



# ---------------- VOICE SETUP ----------------


def listen():
    if not VOICE_ENABLED:
        return None

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
    except:
        return None
        
# ---------------- SPEAK ASYNC FUNCTION ----------------
def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()






# 👇 ISKE NICHE ADD KARO


MOOD_SONGS = {
    "😃 Happy": [
        {"video": "https://www.youtube.com/watch?v=Oo5tqEWm-jM&list=RDOo5tqEWm-jM&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=MTX1-iIr2_8&list=RDMTX1-iIr2_8&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=0owI9XJ02ZY&list=RD0owI9XJ02ZY&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=bw7bVpI5VcM&list=RDbw7bVpI5VcM&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=S04xHs5l93k&list=RDS04xHs5l93k&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=1HtSfa0PKig&list=RD1HtSfa0PKig&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=tsm-HMLp3kQ"},
        {"video": "https://www.youtube.com/watch?v=PvhpsI5doz0&list=RDPvhpsI5doz0&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=KEGjm2C_TCg&list=RDKEGjm2C_TCg&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=UrU_xl8F7H8&list=RDUrU_xl8F7H8&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=RQ__4gfS5xQ&list=RDRQ__4gfS5xQ&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=51Oz0l-qR3M&list=RD51Oz0l-qR3M&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=2ltGXfmI6mk&list=RD2ltGXfmI6mk&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=yxAacQ4vTJY&list=RDyxAacQ4vTJY&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=qpIdoaaPa6U&list=RDqpIdoaaPa6U&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=HoCwa6gnmM0&list=RDHoCwa6gnmM0&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=II2EO3Nw4m0&list=RDII2EO3Nw4m0&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=hRkc-OPHApY&list=RDhRkc-OPHApY&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=01Pm_buODc4&list=RD01Pm_buODc4&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=ln8KreDppvI&list=RDln8KreDppvI&start_radio=1"}
    ],

    "🙂 Normal": [
        {"video": "https://www.youtube.com/watch?v=pon8irRa8II&list=RDpon8irRa8II&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=_meCewF3Y3g&list=RD_meCewF3Y3g&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=olTVf-fKfKw&list=RDolTVf-fKfKw&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=tpoOBvlvVl4&list=RDtpoOBvlvVl4&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=9CxsXA6EQro&list=RD9CxsXA6EQro&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=v3TRtMH6er4&list=RDv3TRtMH6er4&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=T_MPeEX-aIs&list=RDT_MPeEX-aIs&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=LqJjTnD_wLc&list=RDLqJjTnD_wLc&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=eil2EkRNbfI&list=RDeil2EkRNbfI&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=DVyS1TP4VnA&list=RDDVyS1TP4VnA&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=inEu2qQuGZ8&list=RDinEu2qQuGZ8&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=cUmUOb7j3dc&list=RDcUmUOb7j3dc&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=FudfVyYWNxQ&list=RDFudfVyYWNxQ&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=RazuWp5kSHk&list=RDRazuWp5kSHk&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=aRNfSqsgrgE&list=RDaRNfSqsgrgE&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=i5buD3fh0yw&list=RDi5buD3fh0yw&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=z0KTYNnEcAY&list=RDz0KTYNnEcAY&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=orYf6VDtj_k&list=RDorYf6VDtj_k&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=9pIXNy-pS10&list=RD9pIXNy-pS10&start_radio=1"},
        {"video": "https://www.youtube.com/watch?v=MJyKN-8UncM&list=RDMJyKN-8UncM&start_radio=1"}
    ],

    "😔 Sad": [
    {"video": "https://www.youtube.com/watch?v=hoNb6HuNmU0"},  # Khairiyat – Arijit Singh
    {"video": "https://www.youtube.com/watch?v=sK7riqg2mr4"},  # Agar Tum Saath Ho – Alka & Arijit
    {"video": "https://www.youtube.com/watch?v=Umqb9KENgmk"},  # Channa Mereya – Arijit Singh
    {"video": "https://www.youtube.com/watch?v=Qdz5n1Xe5Qo"},  # Tera Ban Jaunga – Akhil, Tulsi
    {"video": "https://www.youtube.com/watch?v=gvyUuxdRdR4"},  # Raataan Lambiyan – Jubin
    {"video": "https://www.youtube.com/watch?v=ElZfdU54Cp8"},  # Apna Bana Le – Arijit
    {"video": "https://www.youtube.com/watch?v=SlPhMPnQ58k"},  # Phir Bhi Tumko Chaahunga – Arijit
    {"video": "https://www.youtube.com/watch?v=YQHsXMglC9A"},  # Tum Hi Ho – Arijit Singh
    {"video": "https://www.youtube.com/watch?v=6FURuLYrR_Q"},  # Phir Le Aaya Dil – Arijit
    {"video": "https://www.youtube.com/watch?v=RgKAFK5djSk"},  # Tum Se Hi – Mohit Chauhan

    {"video": "https://www.youtube.com/watch?v=3AtDnEC4zak"},  # Jeene Laga Hoon – Atif Aslam
    {"video": "https://www.youtube.com/watch?v=8xg3vE8Ie_E"},  # Dil Diyan Gallan – Atif Aslam
    {"video": "https://www.youtube.com/watch?v=Qjo8K2EN8eM"},  # Pachtaoge – Arijit Singh
    {"video": "https://www.youtube.com/watch?v=2OEL4P1Rz04"},  # Bekhayali – Sachet
    {"video": "https://www.youtube.com/watch?v=papuvlVeZg8"},  # Kabira – Arijit & Harshdeep
    {"video": "https://www.youtube.com/watch?v=UceaB4D0jpo"},  # Shayad – Arijit Singh
    {"video": "https://www.youtube.com/watch?v=J7ck984Qhso"},  # Hasi Ban Gaye – Ami Mishra
    {"video": "https://www.youtube.com/watch?v=VbfpW0pbvaU"},  # Sunn Raha Hai – Ankit Tiwari
    {"video": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"},  # Ae Dil Hai Mushkil – Arijit
    {"video": "https://www.youtube.com/watch?v=0KSOMA3QBU0"}   # Baarish – Ash King, Shreya
],

    "😡 Stressed": [
    {"title": "Night Trouble (Slowed)", "video": "https://www.youtube.com/watch?v=qtdvb9GVOyk"},
    {"title": "Bekhayali (Slowed + Reverb)", "video": "https://www.youtube.com/watch?v=2OEL4P1Rz04"},
    {"title": "Let Me Down Slowly (Slowed)", "video": "https://www.youtube.com/watch?v=1ZYbU82GVz4"},
    {"title": "Lofi Hip Hop Radio (24/7)", "video": "https://www.youtube.com/watch?v=5qap5aO4i9A"},
    {"title": "Weightless (Relax Music)", "video": "https://www.youtube.com/watch?v=lFcSrYw-ARY"},
    {"title": "Closer (Slowed + Reverb)", "video": "https://www.youtube.com/watch?v=DWcJFNfaw9c"},
    {"title": "Faded (Slowed)", "video": "https://www.youtube.com/watch?v=6Dh-RL__uN4"},
    {"title": "Perfect (Slowed)", "video": "https://www.youtube.com/watch?v=UfcAVejslrU"},
    {"title": "Perfect Original", "video": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"},
    {"title": "Tum Se Hi (Calm)", "video": "https://www.youtube.com/watch?v=RgKAFK5djSk"},

    {"title": "Shape of You (Soft Mix)", "video": "https://www.youtube.com/watch?v=JGwWNGJdvx8"},
    {"title": "Counting Stars (Slowed)", "video": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"},
    {"title": "Until I Found You (Calm)", "video": "https://www.youtube.com/watch?v=VPRjCeoBqrI"},
    {"title": "Phir Bhi Tumko Chaahunga (Soft)", "video": "https://www.youtube.com/watch?v=SlPhMPnQ58k"},
    {"title": "Baarish (Relax)", "video": "https://www.youtube.com/watch?v=0KSOMA3QBU0"},
    {"title": "Lean On (Chill)", "video": "https://www.youtube.com/watch?v=34Na4j8AVgA"},
    {"title": "Radioactive (Slow Edit)", "video": "https://www.youtube.com/watch?v=ktvTqknDobU"},
    {"title": "Alone (Calm Mix)", "video": "https://www.youtube.com/watch?v=60ItHLz5WEA"},
    {"title": "Sunn Raha Hai (Soft)", "video": "https://www.youtube.com/watch?v=VbfpW0pbvaU"},
    {"title": "Hymn For The Weekend (Chill)", "video": "https://www.youtube.com/watch?v=09R8_2nJtjg"}
],
"😴 Tired": [
    {"title": "Raabta (Soft)", "video": "https://www.youtube.com/watch?v=zlt38OOqwDc"},
    {"title": "Tum Se Hi", "video": "https://www.youtube.com/watch?v=RgKAFK5djSk"},
    {"title": "Khairiyat (Soft)", "video": "https://www.youtube.com/watch?v=hoNb6HuNmU0"},
    {"title": "Apna Bana Le", "video": "https://www.youtube.com/watch?v=ElZfdU54Cp8"},
    {"title": "Raataan Lambiyan", "video": "https://www.youtube.com/watch?v=gvyUuxdRdR4"},
    {"title": "Shayad", "video": "https://www.youtube.com/watch?v=UceaB4D0jpo"},
    {"title": "Hasi Ban Gaye", "video": "https://www.youtube.com/watch?v=J7ck984Qhso"},
    {"title": "Agar Tum Saath Ho", "video": "https://www.youtube.com/watch?v=sK7riqg2mr4"},
    {"title": "Tera Ban Jaunga", "video": "https://www.youtube.com/watch?v=Qdz5n1Xe5Qo"},
    {"title": "Phir Le Aaya Dil", "video": "https://www.youtube.com/watch?v=6FURuLYrR_Q"},

    {"title": "Kabira (Encore)", "video": "https://www.youtube.com/watch?v=papuvlVeZg8"},
    {"title": "Dil Diyan Gallan", "video": "https://www.youtube.com/watch?v=SAcpESN_Fk4"},
    {"title": "Jeene Laga Hoon", "video": "https://www.youtube.com/watch?v=3AtDnEC4zak"},
    {"title": "Sun Saathiya", "video": "https://www.youtube.com/watch?v=Z8H4n1Zl5cA"},
    {"title": "Bolna", "video": "https://www.youtube.com/watch?v=Z8H4n1Zl5cA"},
    {"title": "Nazm Nazm", "video": "https://www.youtube.com/watch?v=UuCq8mtK8J4"},
    {"title": "Kaise Hua", "video": "https://www.youtube.com/watch?v=WWXm39leYew"},
    {"title": "Tum Hi Ho", "video": "https://www.youtube.com/watch?v=YQHsXMglC9A"},
    {"title": "Main Rang Sharbaton Ka", "video": "https://www.youtube.com/watch?v=9udS0mpi3Qk"},
    {"title": "Iktara", "video": "https://www.youtube.com/watch?v=fSS_R91Nimw"}
]
}


def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = ""
if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

# ================= SAFE VOICE SETUP =================
try:
    
    recognizer = sr.Recognizer()
    
    VOICE_ENABLED = True

except:
    VOICE_ENABLED = False
# ====================================================

def generate_pdf(text):
    file = "health_report.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()

    content = []
    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
    return file

if "user" not in st.session_state:
    st.session_state.user = "Guest"


# ================= GLOBAL SESSION INIT (FIX ERROR) =================

if "weight_history" not in st.session_state:
    st.session_state.weight_history = []

if "water" not in st.session_state:
    st.session_state.water = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "last_date" not in st.session_state:
    st.session_state.last_date = pd.Timestamp.now().date()









# ================= AI PERSONALITY =================
if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "Motivator"

AI_MODES = {
    "Motivator": "You are a highly motivating health coach.",
    "Doctor": "You are a professional medical advisor.",
    "Friend": "You are a caring and friendly buddy.",
    "Strict Trainer": "You are a strict fitness trainer."
}






# ================= THEME SETUP (ADDED ONLY) =================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""             
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)
# ============================================================


# ---- GEMINI CONFIG HERE ----
api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.warning("API key missing")
    st.stop()   # ✅ VERY IMPORTANT
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")  # ✅ yahin banana hai


# ---------------- FUNCTION TO GET GEMINI RESPONSE ----------------
def get_gemini_response(prompt, image_data=None):
    try:
        # 🔥 ADD THIS (IMPORTANT)
        personality = AI_MODES.get(st.session_state.ai_mode, "")
        prompt = personality + "\n" + prompt

        if image_data:
            response = model.generate_content([prompt, image_data[0]])
        else:
            response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error generating response: {str(e)}"
    
    

    




# ================= VOICE FUNCTIONS (YAHAN ADD KARO) =================

def listen():
    if not VOICE_ENABLED:
        return None

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
    except:
        return None





def speak(text, language="English"):
    if not VOICE_ENABLED:
        return

    try:
        # Language selection
        if language == "Hindi":
            lang = "hi"
        elif language == "Hinglish":
            lang = "hi"
        else:
            lang = "en"

        tts = gTTS(text=text, lang=lang)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)

            with open(fp.name, "rb") as audio:
                st.audio(audio.read(), format="audio/mp3")

    except Exception as e:
        st.error(f"Voice Error: {e}")



# ---------------- UI ----------------
user_input = st.text_input("Ask something")

if user_input:
    response = get_gemini_response(user_input)
    st.write(response)

# Initialize session state
if 'health_profile' not in st.session_state:
    st.session_state.health_profile ={
        'goals':'Loss 10 pounds in months\nImprove cardiovascular health',
        'conditions':'None',
        'routines':'30-minute walk 3x/week',
        'preferences':'Vegetarian\nLow carb',
        'restrictions': 'No dairy\nNo nuts'
    }



# ================= MOOD TRACKER INIT =================
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# ✅ ADD THIS
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False



# ================== IMAGE PREP FUNCTION ==================
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    return None


# ================= SAVE DATA FUNCTION =================
def save_data(username, weight, water, bmi):
    data = {
        "Username": username,
        "Weight": weight,
        "Water": water,
        "BMI": bmi,
        "Date": pd.Timestamp.now()
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv("fitness_data.csv")
        df = pd.concat([old, df], ignore_index=True)
    except:
        pass

    df.to_csv("fitness_data.csv", index=False)
# ======================================================



# ================= APP LAYOUT =================
st.set_page_config(
    page_title="AI Health Companion",
    layout="centered",
    initial_sidebar_state="collapsed"
)
apply_theme(st.session_state.theme)



# ================= ULTRA PREMIUM AI HEALTH UI =================
st.markdown("""
<style>

/* ================= GLOBAL BACKGROUND ================= */

.stApp {
    background: radial-gradient(circle at 20% 20%, #0f2027, #0a0f1f 70%);
    font-family: 'Poppins', sans-serif;
    color: #e2e8f0;
    overflow-x: hidden;
}

/* ================= PARTICLE GLOW BACKGROUND ================= */

.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    top: -50%;
    left: -50%;
    background: radial-gradient(circle, rgba(0,229,255,0.08) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: particlesMove 40s linear infinite;
    pointer-events: none;
}

@keyframes particlesMove {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ================= GLASS CARD EFFECT ================= */

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.15);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 30px;
}

/* ================= PREMIUM BUTTON ================= */

.stButton > button {
    position: relative;
    color: white;
    border: none;
    padding: 14px 36px;
    border-radius: 50px;
    font-size: 17px;
    font-weight: 600;
    letter-spacing: 0.5px;
    overflow: hidden;
    transition: all 0.3s ease;
    
    background:
      url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%2300E5FF' d='M12 12c-2-3-6-4-8-2 1 4 4 6 8 5 4 1 7-1 8-5-2-2-6-1-8 2z'/%3E%3C/svg%3E") 
        no-repeat top 6px right 14px,
      linear-gradient(145deg, #1f3b5c, #2c5364);

    background-size: 26px 26px, auto;

    box-shadow: 
        inset 0 1px 4px rgba(255,255,255,0.15),
        0 8px 20px rgba(0,0,0,0.4);
    
            

    animation: buttonGlow 3s ease-in-out infinite alternate;
}

@keyframes buttonGlow {
    from {
        box-shadow:
            inset 0 1px 4px rgba(255,255,255,0.15),
            0 8px 20px rgba(0,0,0,0.4);
    }
    to {
        box-shadow:
            inset 0 1px 6px rgba(255,255,255,0.25),
            0 12px 28px rgba(0,150,255,0.6);
    }
}
            

/* Light sweep animation */
.stButton > button::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 50%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.4), transparent);
    transform: skewX(-25deg);
}

.stButton > button:hover::after {
    animation: sweep 1s ease forwards;
}

@keyframes sweep {
    to { left: 150%; }
}

/* Hover glow */
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 
        inset 0 1px 6px rgba(255,255,255,0.25),
        0 15px 30px rgba(0,150,255,0.6);
}
            

            
            /* ================= APPLE MICRO INTERACTION ================= */

/* Soft floating idle animation */
.stButton > button {
    animation: buttonGlow 3s ease-in-out infinite alternate,
               floatButton 6s ease-in-out infinite;
}

@keyframes floatButton {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
    100% { transform: translateY(0px); }
}

/* Press effect */
.stButton > button:active {
    transform: scale(0.96);
    box-shadow: 
        inset 0 3px 8px rgba(0,0,0,0.6),
        0 4px 10px rgba(0,0,0,0.4);
}

/* ================= GLASS REFLECTION SWEEP ================= */

.stButton > button::after {
    content: "";
    position: absolute;
    top: -50%;
    left: -60%;
    width: 60%;
    height: 200%;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(255,255,255,0.25),
        transparent
    );
    transform: rotate(25deg);
    transition: all 0.6s ease;
}

/* Sweep automatically */
.stButton > button:hover::after {
    left: 130%;
}

/* ================= AI PULSE RING ON HOVER ================= */

.stButton > button::marker {
    display: none;
}

.stButton > button:hover::before {
    animation: flap 2s ease-in-out infinite,
               pulseRing 1.8s ease-out infinite;
}

@keyframes pulseRing {
    0% {
        filter: drop-shadow(0 0 10px #00E5FF)
                drop-shadow(0 0 20px #00BFFF);
    }
    50% {
        filter: drop-shadow(0 0 25px #00E5FF)
                drop-shadow(0 0 40px #00BFFF);
    }
    100% {
        filter: drop-shadow(0 0 10px #00E5FF)
                drop-shadow(0 0 20px #00BFFF);
    }
}

/* ================= ULTRA SMOOTH TRANSITIONS ================= */

.stButton > button {
    will-change: transform, box-shadow;
    backface-visibility: hidden;
}



/* ================= PURE BLUE BUTTERFLY WITH WING FLAP ================= */

.stButton > button::before {
    content: "";
    position: absolute;
    width: 26px;
    height: 26px;
    bottom: 6px;
    left: 14px;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%2300E5FF' d='M12 12c-2-3-6-4-8-2 1 4 4 6 8 5 4 1 7-1 8-5-2-2-6-1-8 2z'/%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    filter: drop-shadow(0 0 12px #00E5FF)
            drop-shadow(0 0 25px #00BFFF);
    animation: flap 2s ease-in-out infinite;
}
            


/* Opposite wing animation */
@keyframes flapReverse {
    0% { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(-5deg) scale(1.05); }
    100% { transform: rotate(0deg) scale(1); }
}



/* Wing flap subtle */
@keyframes flap {
    0% { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(5deg) scale(1.05); }
    100% { transform: rotate(0deg) scale(1); }
}

/* ================= PREMIUM HEADING ================= */

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#2563eb,#00E5FF);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 30px rgba(56,189,248,0.9);
    letter-spacing: 1px;
    position: relative;
    margin-bottom: 50px;
}
            
            /* Animated glow pulse */
.main-title {
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from {
        text-shadow: 0 0 20px rgba(0,229,255,0.6),
                     0 0 40px rgba(0,229,255,0.4);
    }
    to {
        text-shadow: 0 0 40px rgba(0,229,255,1),
                     0 0 70px rgba(0,229,255,0.7);
    }
}

/* AI rotating halo */
.main-title::before {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    border: 2px dashed rgba(0,229,255,0.3);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: rotateHalo 20s linear infinite;
    z-index: -1;
}

@keyframes rotateHalo {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Glowing underline */
.main-title::after {
    content: "";
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 4px;
    border-radius: 10px;
    background: linear-gradient(90deg,#00E5FF,#2563eb);
    box-shadow: 0 0 20px #00E5FF;
}
            




            

/* ================= 3D MOUSE DEPTH TILT ================= */

.stButton > button {
    transform-style: preserve-3d;
    perspective: 1000px;
}

.stButton > button:hover {
    transform: rotateX(8deg) rotateY(-8deg) translateY(-4px);
}


/* ================= NEON RIPPLE CLICK ================= */

.stButton > button:active::after {
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    background: rgba(0,229,255,0.6);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(1);
    animation: rippleEffect 0.6s ease-out forwards;
}

@keyframes rippleEffect {
    to {
        transform: translate(-50%, -50%) scale(14);
        opacity: 0;
    }
}


/* ================= DYNAMIC GRADIENT SHIFT ================= */

.stButton > button {
    background:
      url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%2300E5FF' d='M12 12c-2-3-6-4-8-2 1 4 4 6 8 5 4 1 7-1 8-5-2-2-6-1-8 2z'/%3E%3C/svg%3E") 
        no-repeat top 6px right 14px,
      linear-gradient(270deg, #1f3b5c, #2563eb, #00E5FF, #1f3b5c);

    background-size: 26px 26px, 400% 400%;
    animation: buttonGlow 3s ease-in-out infinite alternate,
               floatButton 6s ease-in-out infinite,
               gradientMove 10s ease infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}


/* ================= AI BREATHING BACKGROUND ================= */

.stApp {
    animation: aiBreathe 14s ease-in-out infinite;
}

@keyframes aiBreathe {
    0% {
        background: radial-gradient(circle at 20% 20%, #0f2027, #0a0f1f 70%);
    }
    50% {
        background: radial-gradient(circle at 80% 80%, #0f2027, #132b45 70%);
    }
    100% {
        background: radial-gradient(circle at 20% 20%, #0f2027, #0a0f1f 70%);
    }
}








            

</style>
""", unsafe_allow_html=True)


# ================= HEADING =================

st.markdown("""
<h1 class='main-title'>
🤖 AI Health Companion
</h1>
""", unsafe_allow_html=True)

# ================= GLASS CARD WRAPPER START =================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)


# ================= PREMIUM HEADING =================




quotes = [
    "Your body can stand almost anything. It's your mind you have to convince.",
    "Small progress is still progress.",
    "Consistency beats motivation.",
    "Eat clean. Train dirty.",
    "Healthy is not a size, it's a lifestyle."
]

st.info(random.choice(quotes))




# ================= SIDEBAR =================
with st.sidebar:

    # 🌗 THEME TOGGLE
    if st.button("🌗 Toggle Dark / Light"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

    st.divider()
    st.subheader("Your Health Profile")

    health_goals = st.text_area("Health Goals",
                                value=st.session_state.health_profile['goals'])
    medical_conditions = st.text_area("Medical Conditions",
                                value=st.session_state.health_profile['conditions'])
    fitness_routines = st.text_area("Fitness Routines",
                                value=st.session_state.health_profile['routines'])
    food_preferences = st.text_area("Food Preferences",
                                value=st.session_state.health_profile['preferences'])
    restrictions = st.text_area("Dietary Restrictions",
                                value=st.session_state.health_profile['restrictions'])
    
    if st.button("Update Profile"):
        st.session_state.health_profile = {
            'goals': health_goals,
            'conditions': medical_conditions,
            'routines': fitness_routines,
            'preferences': food_preferences,
            'restrictions': restrictions
        }
        st.success("Profile updated!")




    
   # 🔐 LOGOUT BUTTON (TOP ME)
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    st.divider()

    # 👤 Profile Section
    st.subheader("👤 Profile")

    
    st.subheader("🤖 AI Personality")

    mode = st.selectbox("Choose AI Mode", list(AI_MODES.keys()))

    if st.button("Apply AI Mode"):
        st.session_state.ai_mode = mode

    
    # ================= LANGUAGE SELECTOR =================
    st.sidebar.subheader("🌍 Select Language")

    language = st.sidebar.selectbox(
    "Choose Language",
    ["English", "Hindi", "Hinglish"]
    )














    


# ---------------- DAILY WATER RESET ----------------
if "last_date" not in st.session_state:
    st.session_state.last_date = pd.Timestamp.now().date()

today = pd.Timestamp.now().date()

if today != st.session_state.last_date:
    st.session_state.water = 0
    st.session_state.last_date = today
    st.session_state.challenge_completed = False
    st.session_state.daily_challenge = random.choice([
        "Drink 8 glasses water",
        "Walk 5000 steps",
        "Eat 2 healthy meals",
        "Do 15 min exercise"
    ])


       


   

   

    # ---------------- HEALTHY STREAK INIT ----------------
    if "streak" not in st.session_state:
        st.session_state.streak = 0


# ================= MAIN CONTENT =================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "Meal Planning",
    "Food Analysis",
    "Health Insights",
    "BMI & Fitness",
    "AI Risk Analysis",
    "📊 Dashboard",
    "🏆 Leaderboard",
    "😊 Mood Tracker",
    "🎤 Voice AI",
    "💤 Sleep",
    "🔥 Streak",
    "🧠 Insights",
    "💧 Water Tracker",
    "🧬 AI Health Brain",
    "🚀 Next-Gen AI Health (Voice + Camera + Smart AI)"
])
# ---------------- TAB 1 : MEAL PLANNING ----------------
# ---------------- TAB 1 : MEAL PLANNING ----------------
with tab1:
    st.subheader("🍽️ Personalized Meal Planning")

    # Ensure session state exists (important fix)
    if "health_profile" not in st.session_state:
        st.session_state.health_profile = {
            "goals": "",
            "conditions": "",
            "routines": "",
            "preferences": "",
            "restrictions": ""
        }

    if "mood" not in st.session_state:
        st.session_state.mood = "Not specified"

    col1, col2 = st.columns(2)

    # -------- LEFT SIDE --------
    with col1:
        st.write("### Your Current Needs")
        user_input = st.text_area(
            "Describe any specific requirements for your meal plan",
            placeholder="e.g., quick meals, high-protein diet, weight loss..."
        )

    # -------- RIGHT SIDE --------
    with col2:
        st.write("### Your Health Profile")
        st.json(st.session_state.health_profile)

    # -------- BUTTON --------
    if st.button("🚀 Generate Personalized Meal Plan"):
        profile = st.session_state.health_profile

        # Proper validation fix
        if not any(str(v).strip() for v in profile.values()):
            st.warning("⚠️ Please complete your health profile in the sidebar first.")
        else:
            with st.spinner("Creating your personalized meal plan... 🍳"):
                lang_instruction = get_language_instruction(language)


                prompt = f"""
                 {lang_instruction}
Create a personalized meal plan based on the following health profile:

Health Goals: {profile.get('goals', '')}
Medical Conditions: {profile.get('conditions', '')}
Fitness Routines: {profile.get('routines', '')}
Food Preferences: {profile.get('preferences', '')}
Dietary Restrictions: {profile.get('restrictions', '')}

Additional requirements: {user_input if user_input else "None provided"}
Current Mood: {st.session_state.mood}

Provide:
1. A 7-day meal plan with breakfast, lunch, dinner, and snacks
2. Nutritional breakdown for each day (calories, macros)
3. Reasons for meal choices
4. Shopping list (categorized)
5. Quick preparation tips

Format nicely using headings and bullet points.
"""

                try:
                    response = get_gemini_response(prompt)

                    st.subheader("📋 Your Personalized Meal Plan")
                    st.markdown(response)
                    st.success("✅ Meal Plan Generated Successfully!")

                    st.download_button(
                        label="⬇️ Download Meal Plan",
                        data=response,
                        file_name="personalized_meal_plan.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"❌ Error generating meal plan: {e}")

# ---------------- TAB 2 : FOOD ANALYSIS ----------------
with tab2:
    st.subheader("🍎 Food Analysis")

    uploaded_file = st.file_uploader(
        "Upload an image of your food",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Food Image", use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error loading image: {e}")
            st.stop()

        # -------- BUTTON --------
        if st.button("🔍 Analyze Food"):
            with st.spinner("Analyzing your food... 🍽️"):

                try:
                    image_data = input_image_setup(uploaded_file)
                    lang_instruction = get_language_instruction(language)


                    prompt = """
                     {lang_instruction}
You are an expert nutritionist. Analyze this food image.

Provide detailed information about:
- Estimated calories
- Macronutrient breakdown (protein, carbs, fats)
- Potential health benefits
- Any concerns (allergies, high sugar, etc.)
- Suggested portion sizes

If multiple food items are present, analyze each separately.
Format the response clearly using headings and bullet points.
"""

                    response = get_gemini_response(prompt, image_data)

                    st.subheader("📊 Food Analysis Results")
                    st.markdown(response)

                except Exception as e:
                    st.error(f"❌ Error analyzing food: {e}")

# ---------------- TAB 3 : HEALTH INSIGHTS ----------------
with tab3:
    st.subheader("🧠 Health Insights")

    # Ensure session state exists (important fix)
    if "health_profile" not in st.session_state:
        st.session_state.health_profile = {}

    health_query = st.text_input(
        "Ask any health/nutrition-related question",
        placeholder="e.g., How can I improve my gut health?"
    )

    # -------- BUTTON --------
    if st.button("💡 Get Expert Insights"):
        if not health_query.strip():
            st.warning("⚠️ Please enter a health question")
        else:
            with st.spinner("Researching your question... 🔍"):
                try:
                    lang_instruction = get_language_instruction(language)

                    prompt = f"""
                     {lang_instruction}
You are a certified nutritionist and health expert.

Provide detailed, science-backed insights about:
{health_query}

Consider the user's health profile:
{st.session_state.health_profile}

Include:
1. Clear explanation of the science
2. Practical recommendations
3. Precautions (if any)
4. References to studies (if applicable)
5. Suggested foods or supplements (if appropriate)

Use simple language but maintain accuracy.
"""

                    response = get_gemini_response(prompt)

                    st.subheader("📋 Expert Health Insights")
                    st.markdown(response)

                except Exception as e:
                    st.error(f"❌ Error fetching insights: {e}")


# ---------------- TAB 4 : BMI ----------------
with tab4:
    st.subheader("⚖️ BMI Calculator")

    # -------- SESSION STATE SAFETY --------
    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    if "water" not in st.session_state:
        st.session_state.water = 0

    if "user" not in st.session_state:
        st.session_state.user = "guest"

    # -------- INPUTS --------
    height = st.number_input(
        "Height (cm)", min_value=100, max_value=250, key="bmi_height"
    )
    weight = st.number_input(
        "Weight (kg)", min_value=30, max_value=200, key="bmi_weight"
    )

    # -------- BMI CALC --------
    if st.button("📊 Calculate BMI", key="calc_bmi"):
        if height > 0:
            bmi = weight / ((height / 100) ** 2)
            st.metric("Your BMI", round(bmi, 2))

            if bmi < 18.5:
                st.warning("⚠️ Underweight")
            elif 18.5 <= bmi < 25:
                st.success("✅ Normal Weight")
            elif 25 <= bmi < 30:
                st.warning("⚠️ Overweight")
            else:
                st.error("❌ Obese")
        else:
            st.error("Height must be greater than 0")

    # ================= WEIGHT TRACKER =================
    st.divider()
    st.subheader("📈 Weight Progress Tracker")

    new_weight = st.number_input(
        "Log Today's Weight", min_value=30.0, max_value=300.0, key="progress_weight"
    )

    if st.button("💾 Save Weight", key="save_weight"):
        if new_weight > 0:
            st.session_state.weight_history.append(new_weight)

            height_value = st.session_state.get("bmi_height", None)
            bmi_value = (
                new_weight / ((height_value / 100) ** 2)
                if height_value and height_value > 0
                else None
            )

            # Safe save (avoid crash if function missing)
            try:
                save_data(
                    st.session_state.user,
                    new_weight,
                    st.session_state.water,
                    bmi_value
                )
            except:
                pass

            st.success("✅ Weight Saved Successfully!")
        else:
            st.warning("⚠️ Enter a valid weight")

    # -------- CHART --------
    if st.session_state.weight_history:
        st.line_chart(st.session_state.weight_history)

    # ================= 7 DAY PREDICTION =================
    if len(st.session_state.weight_history) >= 2:
        weights = st.session_state.weight_history
        days = np.arange(len(weights))

        slope, intercept = np.polyfit(days, weights, 1)
        future_day = len(weights) + 7
        predicted_weight = slope * future_day + intercept

        st.subheader("🔮 7-Day Prediction")
        st.info(
            f"At current trend, your weight after 7 days may be: "
            f"{round(predicted_weight, 2)} kg"
        )

    # ================= ACHIEVEMENTS =================
    st.divider()
    st.subheader("🏅 Achievements")

    if st.session_state.water >= 8:
        st.success("💧 Hydration Champion!")

    if len(st.session_state.weight_history) >= 7:
        st.success("📊 Consistency Star!")

    if (
        st.session_state.water >= 8
        and len(st.session_state.weight_history) >= 7
    ):
        st.success("🔥 Ultimate Discipline Badge!")

    # ================= GOAL CELEBRATION =================
    latest_weight = (
        st.session_state.weight_history[-1]
        if st.session_state.weight_history
        else None
    )

    target_weight = st.session_state.get("target_weight", None)

    if target_weight is not None and latest_weight is not None:
        if abs(latest_weight - target_weight) <= 1:
            st.balloons()
    st.divider()
    st.subheader("🎯 Smart Goal Adjustment")

    if st.button("AI Suggest Goal"):
        lang_instruction = get_language_instruction(language)

        prompt = f"""
         {lang_instruction}
        User Weight History: {st.session_state.weight_history}
        Suggest optimal target weight and timeline.
    """
        goal = get_gemini_response(prompt)
        st.success(goal)




  


# ---------------- TAB 5 : AI RISK ANALYSIS ----------------
with tab5:
    st.subheader("🧬 AI Health Risk Predictor")

    # -------- SESSION STATE SAFETY --------
    if "health_profile" not in st.session_state:
        st.session_state.health_profile = {}

    if "water" not in st.session_state:
        st.session_state.water = 0

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    # -------- BUTTON --------
    if st.button("🧠 Analyze My Health Risks", key="risk_btn"):

        # Basic validation (important)
        if not any(str(v).strip() for v in st.session_state.health_profile.values()):
            st.warning("⚠️ Please complete your health profile first.")
        else:
            with st.spinner("Analyzing patterns... 🔍"):
                try:
                    lang_instruction = get_language_instruction(language)

                    risk_prompt = f"""
                     {lang_instruction}
You are an AI health risk analyst.

User Health Data:
Profile: {st.session_state.health_profile}
Water Intake (glasses/day): {st.session_state.water}
Weight History: {st.session_state.weight_history}

Analyze and provide:

1. Potential health risks (short-term & long-term)
2. Lifestyle imbalances
3. Risk level (Low / Moderate / High)
4. Preventive recommendations
5. Simple daily habits to improve health

Keep the explanation easy to understand and actionable.
Use bullet points and clear headings.
"""

                    risk_response = get_gemini_response(risk_prompt)

                    st.subheader("📊 Your Health Risk Analysis")
                    st.markdown(risk_response)

                except Exception as e:
                    st.error(f"❌ Error analyzing risks: {e}")



# ---------------- TAB 6 : DASHBOARD ----------------
with tab6:
    st.subheader("📊 Smart Health Dashboard")

    # -------- SESSION STATE SAFETY --------
    if "water" not in st.session_state:
        st.session_state.water = 0

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    # -------- TOP METRICS --------
    col1, col2, col3 = st.columns(3)

    col1.metric("💧 Water Today", st.session_state.water)
    col2.metric("📌 Entries Logged", len(st.session_state.weight_history))

    if st.session_state.weight_history:
        col3.metric("⚖️ Latest Weight", st.session_state.weight_history[-1])
    else:
        col3.metric("⚖️ Latest Weight", "N/A")

    # -------- WEIGHT CHART --------
    if st.session_state.weight_history:
        df = pd.DataFrame({
            "Day": range(1, len(st.session_state.weight_history) + 1),
            "Weight": st.session_state.weight_history
        })
        st.line_chart(df.set_index("Day"))

    # ================= MOOD TRACKING =================
    st.divider()
    st.subheader("😊 Mood Trends")

    if st.session_state.mood_history:
        mood_df = pd.DataFrame({
            "Day": range(1, len(st.session_state.mood_history) + 1),
            "Mood": st.session_state.mood_history
        })
        st.line_chart(mood_df.set_index("Day"))

        # -------- MOOD WARNINGS --------
        if st.session_state.mood_history.count("😔 Sad") > 2:
            st.warning("⚠️ You seem sad often. Try meditation or light exercise.")

        if st.session_state.mood_history.count("😡 Stressed") > 2:
            st.warning("⚠️ High stress detected. Consider relaxation techniques.")

    else:
        st.info("No mood data yet.")

    # ================= AI HABIT INSIGHTS =================
    st.divider()
    st.subheader("🧠 Smart Habit Insights")

    if st.button("🔍 Analyze My Habits", key="habit_btn"):
        try:
            lang_instruction = get_language_instruction(language)

            habit_prompt = f"""
             {lang_instruction}
            You are a smart health behavior analyst.

            User Data:
            Water Intake: {st.session_state.water}
            Weight History: {st.session_state.weight_history}
            Mood History: {st.session_state.mood_history}
            Streak: {st.session_state.streak}

            Analyze and provide:
            1. Bad habits
            2. Behavior patterns
            3. Improvement suggestions
            4. Positive habits to build

            Keep it simple and actionable.
            """

            insight = get_gemini_response(habit_prompt)
            st.info(insight)

        except Exception as e:
            st.error(f"❌ Error generating insights: {e}")

    # ================= WATER VS WEIGHT =================
    st.divider()
    st.subheader("📊 Water vs Weight")

    if st.session_state.weight_history:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.weight_history)
        ax.set_xlabel("Days")
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight Trend")

        st.pyplot(fig)



 # ================= FUTURE WEIGHT PREDICTION =================
if len(st.session_state.weight_history) > 2:
    st.subheader("📈 Future Weight Prediction (Next 7 Days)")
    
    # Data preparation
    days = np.arange(len(st.session_state.weight_history))
    weights = st.session_state.weight_history

    # Linear regression calculation (slope and intercept)
    slope, intercept = np.polyfit(days, weights, 1)

    # Predicting next 7 days
    future_days = np.arange(len(days), len(days) + 7)
    future_weights = slope * future_days + intercept

    # -------- CHART DATA --------
    # Dono lists ko combine karke DataFrame banaya
    chart_data = pd.DataFrame({
        "Weight Trend": list(weights) + list(future_weights)
    })
    
    # Displaying the chart
    st.line_chart(chart_data)

    st.divider()
    
    # ================= EMOTION VS HEALTH INSIGHT =================
    st.subheader("🧠 Emotion vs Health Insight")

    if st.button("🔍 Analyze Mood Impact", key="mood_impact_btn"):
        with st.spinner("AI is analyzing your patterns..."):
            try:
                lang_instruction = get_language_instruction(language)

                prompt = f"""
                 {lang_instruction}
                You are a health psychologist.
                User Mood History: {st.session_state.get('mood_history', 'No data')}
                Weight History: {st.session_state.get('weight_history', 'No data')}

                Analyze:
                1. How mood is affecting weight or health habits.
                2. Identify if there's emotional eating or stress-related patterns.
                3. Provide deep, empathetic insights and 2-3 actionable steps.
                
                Keep it professional and helpful.
                """
                
                result = get_gemini_response(prompt)
                st.info(result)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")




# ---------------- TAB 7 : GLOBAL LEADERBOARD ----------------
with tab7:
    st.subheader("🏆 Global Health Leaderboard")

    try:
        df = pd.read_csv("fitness_data.csv")

        # -------- VALIDATION --------
        if "Username" not in df.columns or "Weight" not in df.columns:
            st.error("❌ Required columns missing in dataset.")
            st.stop()

        # -------- LEADERBOARD --------
        leaderboard = (
            df.groupby("Username")
            .agg({"Weight": "count"})
            .rename(columns={"Weight": "Entries Logged"})
            .sort_values(by="Entries Logged", ascending=False)
            .reset_index()
        )

        # Add Rank
        leaderboard["Rank"] = leaderboard.index + 1

        # Reorder columns
        leaderboard = leaderboard[["Rank", "Username", "Entries Logged"]]

        st.dataframe(leaderboard, use_container_width=True)

        # -------- TOP 3 HIGHLIGHT --------
        st.subheader("🥇 Top Performers")

        top3 = leaderboard.head(3)

        for i, row in top3.iterrows():
            if i == 0:
                st.success(f"🥇 {row['Username']} - {row['Entries Logged']} entries")
            elif i == 1:
                st.info(f"🥈 {row['Username']} - {row['Entries Logged']} entries")
            elif i == 2:
                st.warning(f"🥉 {row['Username']} - {row['Entries Logged']} entries")

    except FileNotFoundError:
        st.info("📂 No data file found yet. Start tracking to appear on leaderboard!")

    except Exception as e:
        st.error(f"❌ Error loading leaderboard: {e}")

# ---------------- TAB 8 : MOOD TRACKER ----------------
with tab8:
    st.subheader("😊 Mood Tracker")



    # -------- SESSION STATE SAFETY --------
    if "mood" not in st.session_state:
        st.session_state.mood = "🙂 Normal"

    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []

    if "music_playing" not in st.session_state:
        st.session_state.music_playing = False

    if "song_index" not in st.session_state:
        st.session_state.song_index = 0

    # -------- MOOD INPUT --------
    mood = st.selectbox(
        "How are you feeling today?",
        ["😃 Happy", "🙂 Normal", "😔 Sad", "😡 Stressed", "😴 Tired"]
    )

    if st.button("💾 Save Mood", key="save_mood"):
        st.session_state.mood = mood
        st.session_state.mood_history.append(mood)
        st.success(f"✅ Mood saved: {mood}")

    # -------- AUTO DETECT --------
    user_text = st.text_area(
        "Or describe how you're feeling (AI will detect mood)",
        placeholder="e.g., I'm feeling very low and tired today..."
    )

    if st.button("🤖 Detect Mood Automatically", key="detect_mood"):
        if not user_text.strip():
            st.warning("⚠️ Please describe your mood first")
        else:
            try:
                mood_prompt = f"Detect mood from this text in one word: {user_text}"
                detected = get_gemini_response(mood_prompt).lower()

                if "happy" in detected:
                    st.session_state.mood = "😃 Happy"
                elif "sad" in detected:
                    st.session_state.mood = "😔 Sad"
                elif "stress" in detected:
                    st.session_state.mood = "😡 Stressed"
                elif "tired" in detected:
                    st.session_state.mood = "😴 Tired"
                else:
                    st.session_state.mood = "🙂 Normal"

                st.session_state.mood_history.append(st.session_state.mood)
                st.success(f"✅ Detected Mood: {st.session_state.mood}")

            except Exception as e:
                st.error(f"❌ Error detecting mood: {e}")

    # ================= MUSIC PLAYER =================
    st.divider()
    st.subheader("🎧 Smart Mood Music Player")

    songs = MOOD_SONGS.get(st.session_state.mood, [])

    if not songs:
        st.info("No songs available for this mood.")
    else:

        # -------- SONG SELECT (Dropdown) --------
        selected_song = st.selectbox(
            "🎵 Choose Song",
            range(len(songs)),
            format_func=lambda x: f"Song {x+1}"
        )

        st.session_state.song_index = selected_song

        # -------- MODE --------
        mode = st.radio("Choose Mode", ["🎬 Video", "🎧 Audio"], horizontal=True)

        # -------- BUTTONS --------
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("▶️ Play"):
                st.session_state.music_playing = True

        with col2:
            if st.button("⏸ Pause"):
                st.session_state.music_playing = False

        with col3:
            if st.button("⏭ Next"):
                st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
                st.session_state.music_playing = True

        with col4:
            if st.button("⏮ Previous"):
                st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
                st.session_state.music_playing = True

        with col5:
            if st.button("🔀 Shuffle"):
                st.session_state.song_index = random.randint(0, len(songs)-1)
                st.session_state.music_playing = True

        # -------- CURRENT SONG --------
        st.write(f"🎶 Playing: {st.session_state.song_index + 1} / {len(songs)}")

        # -------- PLAYER --------
        if st.session_state.music_playing:

            song = songs[st.session_state.song_index]
            video_url = song["video"]

            if "v=" in video_url:
                video_id = video_url.split("v=")[-1].split("&")[0]
            else:
                video_id = video_url.split("/")[-1]

            if mode == "🎬 Video":
                st.video(video_url)
            else:
                st.markdown(f"""
                <iframe width="0" height="0"
                src="https://www.youtube.com/embed/{video_id}?autoplay=1"
                allow="autoplay">
                </iframe>
                """, unsafe_allow_html=True)

                st.success("🎧 Audio Playing")

# ---------------- TAB 9 : NEXT LEVEL VOICE AI ----------------
with tab9:
    st.subheader("🎧 Smart Voice AI PRO (Jarvis Style)")

    recognizer = sr.Recognizer()

    # ---------------- SESSION STATE ----------------
    if "voice_on" not in st.session_state:
        st.session_state.voice_on = False   

    if "memory" not in st.session_state:
        st.session_state.memory = []

    if "last_mood" not in st.session_state:
        st.session_state.last_mood = "🙂 Normal"

    # ---------------- LISTEN ----------------
    def listen_voice():
        try:
            with sr.Microphone() as source:
                st.info("🎤 Listening... Speak now")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=6
                )

            text = recognizer.recognize_google(audio, language="en-IN")
            return text.lower()

        except sr.WaitTimeoutError:
            st.warning("⏳ No speech detected")
            return None
        except Exception as e:
            st.error(f"❌ Voice error: {e}")
            return None

    # ---------------- SPEAK ----------------
    def speak_voice(text):
        try:
            tts = gTTS(text=text, lang="en")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)

            with open(fp.name, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"🔊 Voice Error: {e}")

    # ---------------- MOOD DETECTION ----------------
    def detect_mood(text):
        text = text.lower()

        if any(word in text for word in ["happy", "great", "awesome", "excited"]):
            return "😃 Happy"
        elif any(word in text for word in ["sad", "depressed", "cry", "upset"]):
            return "😔 Sad"
        elif any(word in text for word in ["stress", "tension", "worried", "anxious"]):
            return "😡 Stressed"

        try:
            prompt = f"Classify mood (happy/sad/stressed/normal): {text}"
            mood = get_gemini_response(prompt).lower()

            if "happy" in mood:
                return "😃 Happy"
            elif "sad" in mood:
                return "😔 Sad"
            elif "stress" in mood:
                return "😡 Stressed"
        except:
            pass

        return "🙂 Normal"

    # ---------------- SMART WAKE WORD ----------------
    def is_wake_word(text):
        text = text.lower()

        # 🔥 flexible detection
        keywords = ["jarvis", "service", "jervis", "jarviss"]

        return any(word in text for word in keywords)

def generate_response(user_input, mood):
    memory_context = "\n".join(st.session_state.memory[-3:])
    text = user_input.lower()

    # ================= COMMAND DETECTION =================

    # 🍽️ MEAL
    if any(word in text for word in ["meal", "food", "diet", "eat"]):
        lang_instruction = get_language_instruction(language)

        prompt = f"""
         {lang_instruction}
        You are a smart AI nutritionist.
        User mood: {mood}
        Give:
        - 1 healthy meal
        - ingredients
        - 3 simple steps
        Keep it short.
        """

    # 💧 WATER
    elif "water" in text:
        water = st.session_state.get("water", 0)
        prompt = f"""
        User drank {water} glasses of water today.
        Motivate user + suggest hydration tips in 2-3 lines.
        """

    # ⚖️ WEIGHT
    elif "weight" in text:
        weight_history = st.session_state.get("weight_history", [])
        latest = weight_history[-1] if weight_history else "No data"
        prompt = f"""
        User latest weight: {latest}
        Give short insight + suggestion.
        """

    # 😴 SLEEP
    elif "sleep" in text:
        sleep_data = st.session_state.get("sleep_history", [])
        prompt = f"""
        User sleep data: {sleep_data}
        Give short advice to improve sleep.
        """

    # 😊 MOOD
    elif "mood" in text:
        prompt = f"""
        User mood is {mood}.
        Give emotional support + quick suggestion.
        """

    # 📊 HEALTH REPORT
    elif "report" in text or "summary" in text:
        prompt = f"""
        User data:
        Water: {st.session_state.get("water", 0)}
        Weight: {st.session_state.get("weight_history", [])}
        Mood: {st.session_state.get("mood_history", [])}
        Give a short health summary + advice.
        """

    # 🏃 FITNESS / EXERCISE
    elif any(word in text for word in ["exercise", "workout", "fitness"]):
        prompt = f"""
        User mood: {mood}
        Suggest:
        - quick workout
        - duration
        - benefits
        Keep it short.
        """

    # 🎯 GOAL
    elif "goal" in text:
        prompt = f"""
        User weight history: {st.session_state.get("weight_history", [])}
        Suggest realistic health goal + timeline.
        """

    # 🧠 DEFAULT AI MODE (fallback)
    else:
        
        prompt = f"""
        You are a smart AI assistant like Jarvis.
        User mood: {mood}
        Conversation memory:
        {memory_context}
        User said: {user_input}
        Respond naturally, short, helpful.
        """

    # ================= RESPONSE =================
    return get_gemini_response(prompt)

    # ---------------- UI ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start AI"):
        st.session_state.voice_on = True

with col2:
    if st.button("⏹ Stop AI"):
        st.session_state.voice_on = False

st.write("Status:", "🟢 Running" if st.session_state.voice_on else "🔴 Stopped")

# ---------------- MAIN ----------------
if st.session_state.voice_on:
    if st.button("🎤 Speak Now"):
        user_voice = listen_voice()

        if user_voice:
            # 🔥 DEBUG (IMPORTANT)
            st.write("🔍 Heard:", user_voice)

            # Wake word check
            if not is_wake_word(user_voice):
                st.warning("🛑 Wake word not detected (say Jarvis)")
            else:
                # Remove wake word
                for w in ["jarvis", "service", "jervis"]:
                    user_voice = user_voice.replace(w, "").strip()

                if user_voice == "":
                    st.warning("⚠️ Command missing after wake word")
                else:
                    st.write("🧑 You:", user_voice)

                    # Mood detection
                    mood = detect_mood(user_voice)
                    st.session_state.last_mood = mood
                    st.write("🎭 Mood:", mood)

                    # AI response
                    response = generate_response(user_voice, mood)
                    st.write("🤖 AI:", response)

                    # Save memory
                    st.session_state.memory.append(f"You: {user_voice}")
                    st.session_state.memory.append(f"AI: {response}")

                    # Speak
                    speak_voice(response)
# ---------------- TAB 10 : SLEEP TRACKER ----------------
with tab10:
    st.subheader("💤 Sleep Tracker")

    # -------- SESSION STATE SAFETY --------
    if "sleep_history" not in st.session_state:
        st.session_state.sleep_history = []

    # -------- INPUT --------
    sleep = st.slider("Hours slept", 0.0, 12.0, 6.0)

    # -------- FEEDBACK --------
    if sleep < 5:
        st.warning("⚠️ Very less sleep. This may affect your health.")
    elif 5 <= sleep < 7:
        st.info("😐 Average sleep. Try to improve it.")
    elif 7 <= sleep <= 9:
        st.success("✅ Good sleep. Keep it up!")
    else:
        st.warning("⚠️ Too much sleep can also be unhealthy.")

    # -------- SAVE --------
    if st.button("💾 Save Sleep", key="save_sleep"):
        st.session_state.sleep_history.append(sleep)
        st.success(f"✅ Logged {sleep} hours of sleep")

    # -------- CHART --------
    if st.session_state.sleep_history:
        st.line_chart(st.session_state.sleep_history)

    # -------- AI INSIGHTS --------
    st.divider()
    st.subheader("🧠 Sleep Insights")

    if st.button("🔍 Analyze Sleep Pattern", key="sleep_ai"):
        try:
            lang_instruction = get_language_instruction(language)

            sleep_prompt = f"""
             {lang_instruction}
            User Sleep Data: {st.session_state.sleep_history}

            Analyze:
            - Sleep quality
            - Risks of poor sleep
            - Suggestions to improve sleep
            - Ideal routine

            Keep it simple and actionable.
            """
            response = get_gemini_response(sleep_prompt)
            st.info(response)

        except Exception as e:
            st.error(f"❌ Error analyzing sleep: {e}")

# ---------------- TAB 11 : HEALTHY STREAK ----------------
with tab11:
    st.subheader("🔥 Healthy Streak")

    # -------- SESSION STATE SAFETY --------
    if "streak" not in st.session_state:
        st.session_state.streak = 0

    if "last_logged_day" not in st.session_state:
        st.session_state.last_logged_day = None

    today = pd.Timestamp.today().date()

    # -------- LOG BUTTON --------
    if st.button("✅ Log Healthy Day", key="streak_log_1"):
        if st.session_state.last_logged_day == today:
            st.warning("⚠️ You already logged today!")
        else:
            st.session_state.streak += 1
            st.session_state.last_logged_day = today
            st.success("🔥 Streak updated!")

    # -------- DISPLAY --------
    st.metric("🔥 Current Streak", st.session_state.streak)

    # -------- MOTIVATION --------
    if st.session_state.streak >= 7:
        st.success("🏆 Amazing! 7-day consistency!")
    elif st.session_state.streak >= 3:
        st.info("💪 Good going! Keep building momentum!")

    # -------- RESET OPTION --------
    if st.button("🔄 Reset Streak", key="reset_streak"):
        st.session_state.streak = 0
        st.session_state.last_logged_day = None
        st.warning("Streak reset!")

    # -------- VISUAL PROGRESS --------
    # 30-day goal
    st.progress(min(st.session_state.streak / 30, 1.0))



# ---------------- TAB 12 : SMART HABIT INSIGHTS ----------------
with tab12:
    st.subheader("🧠 Smart Habit Insights")

    # -------- SESSION STATE SAFETY --------
    if "water" not in st.session_state:
        st.session_state.water = 0

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []

    # ================= HABIT SCORE (FIXED POSITION) =================
    habit_score = 0

    if st.session_state.water >= 8:
        habit_score += 30
    if len(st.session_state.weight_history) >= 5:
        habit_score += 30
    if st.session_state.streak >= 3:
        habit_score += 40

    # -------- SHOW SCORE --------
    st.metric("🧠 Habit Score", f"{habit_score}/100")

    # -------- FEEDBACK --------
    if habit_score > 80:
        st.success("🔥 Excellent Lifestyle!")
    elif habit_score > 50:
        st.info("👍 Good, but can improve")
    else:
        st.warning("⚠️ Improve your habits")

    # ================= AI BUTTON =================
    if st.button("🔍 Analyze My Habits", key="habit_btn_tab12"):
        try:
            lang_instruction = get_language_instruction(language)

            habit_prompt = f"""
             {lang_instruction}
            You are an AI health habit analyst.

            User Data:
            - Water Intake (glasses/day): {st.session_state.water}
            - Weight History: {st.session_state.weight_history}
            - Mood History: {st.session_state.mood_history}
            - Streak: {st.session_state.streak}

            Analyze and provide:
            1. Key patterns in behavior
            2. Good habits to continue
            3. Bad habits to improve
            4. Personalized improvement plan
            5. Daily actionable tips

            Keep it simple, structured, and practical.
            Use bullet points and headings.
            """

            insight = get_gemini_response(habit_prompt)

            st.subheader("📊 Your Habit Insights")
            st.markdown(insight)

        except Exception as e:
            st.error(f"❌ Error generating insights: {e}")



# ---------------- TAB 13 : SMART WATER TRACKER ----------------
with tab13:
    st.subheader("💧 Smart Water Tracker")

    # -------- SESSION STATE SAFETY --------
    if "water" not in st.session_state:
        st.session_state.water = 0

    if "xp" not in st.session_state:
        st.session_state.xp = 0

    if "water_reward_given" not in st.session_state:
        st.session_state.water_reward_given = False

    goal = 8  # daily goal

    # -------- UI --------
    st.markdown("### Stay Hydrated 💙")
    st.info("Drink at least 8 glasses of water daily")

    # -------- BUTTONS --------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Drink 1 Glass", key="add_water"):
            st.session_state.water += 1

    with col2:
        if st.button("➖ Remove", key="remove_water"):
            if st.session_state.water > 0:
                st.session_state.water -= 1

    with col3:
        if st.button("🔄 Reset", key="reset_water"):
            st.session_state.water = 0
            st.session_state.water_reward_given = False  # reset reward

    # -------- PROGRESS --------
    progress = min(st.session_state.water / goal, 1.0)
    st.progress(progress)

    st.metric("💧 Water Intake", f"{st.session_state.water} / {goal} glasses")

    # -------- STATUS --------
    if st.session_state.water < 4:
        st.warning("⚠️ You need more hydration!")
    elif 4 <= st.session_state.water < 8:
        st.info("👍 Good, keep going!")
    else:
        st.success("🎉 Great! You're fully hydrated!")

    # -------- XP REWARD (FIXED INSIDE TAB) --------
    if (
        st.session_state.water >= goal
        and not st.session_state.water_reward_given
    ):
        st.session_state.xp += 5
        st.session_state.water_reward_given = True
        st.success("💎 +5 XP for hydration!")

    # -------- SHOW XP --------
    st.metric("⭐ Total XP", st.session_state.xp)
    level = st.session_state.xp // 10
    st.metric("🏆 Level", level)

    # ---------------- VISUAL HISTORY (INSIDE TAB 13) ----------------
    st.divider()
    if "water_history" not in st.session_state:
        st.session_state.water_history = []

    if st.button("📌 Save Today’s Progress", key="save_water"):
        st.session_state.water_history.append(st.session_state.get("water", 0))
        st.success("History saved!")

    if st.session_state.water_history:
        st.line_chart(st.session_state.water_history)

# ---------------- TAB 14 : AI DOCTOR+ (ULTRA SMART FINAL) ----------------
with tab14:
    st.subheader("🧬 AI Doctor+ (Patent-Level System)")

    # ================= 1. SESSION STATE =================
    if "symptom_history" not in st.session_state:
        st.session_state.symptom_history = []

    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = ""

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    if "water" not in st.session_state:
        st.session_state.water = 0

    if "target_weight" not in st.session_state:
        st.session_state.target_weight = None
    
    if st.session_state.water < 3:
       st.warning("⚠️ You are dehydrated! Drink water.")

    # ================= 2. INPUT =================
    symptoms = st.text_area(
        "🤒 Describe your symptoms",
        placeholder="e.g., fever, headache, body pain..."
    )

    duration = st.selectbox("⏳ Duration", ["1 day", "2-3 days", "1 week", "More"])
    severity = st.slider("⚠️ Severity Level", 1, 10, 5)

    # ================= 3. BODY SYSTEM DETECTION =================
    def detect_body_system(symptoms):
        s = symptoms.lower()
        if any(w in s for w in ["chest", "breathing", "heart"]):
            return "Cardiovascular System ❤️"
        elif any(w in s for w in ["headache", "dizzy", "brain"]):
            return "Neurological System 🧠"
        elif any(w in s for w in ["stomach", "vomit", "digestion"]):
            return "Digestive System 🍽️"
        else:
            return "General / Unknown"

    # ================= 4. ANALYZE SYMPTOMS =================
    if st.button("🔍 Analyze Symptoms"):
        if not symptoms.strip():
            st.warning("⚠️ Please enter symptoms")
        else:
            with st.spinner("AI Doctor is analyzing... 🧠"):

                system = detect_body_system(symptoms)
                st.info(f"🧬 Affected System: {system}")

                try:
                    past_data = st.session_state.symptom_history[-3:]

                    lang_instruction = get_language_instruction(language)

                    prompt = f"""
                    {lang_instruction}

                    You are a personalized AI doctor.

                    Symptoms: {symptoms}
                    Duration: {duration}
                    Severity: {severity}
                    Past history: {past_data}

                    Provide:
                    - Diseases
                    - Risk
                    - Medicines
                    - Remedies
                    - Home remedies
                    - When to see doctor
                    - Diet plan
                    - Things to avoid
                    """

                    result = get_gemini_response(prompt)

                    st.session_state.last_prediction = result
                    st.session_state.symptom_history.append(symptoms)

                    st.subheader("📊 Diagnosis Result")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
    

    # ================= “RELAPSE DETECTION AI” =================
    
    if len(st.session_state.symptom_history) >= 3:
       recent = st.session_state.symptom_history[-3:]

       if symptoms in recent:
          st.warning("⚠️ Possible recurring health issue detected!")



    # ================= 5. EMERGENCY AI =================
    st.divider()
    st.subheader("🚨 Emergency Check")

    emergency_score = 0

    danger_words = {
        "chest pain": 5,
        "breathing": 5,
        "unconscious": 10,
        "bleeding": 8
    }

    for word, val in danger_words.items():
        if word in symptoms.lower():
            emergency_score += val

    if severity >= 8:
        emergency_score += 5

    if emergency_score >= 10:
        st.error("🚨 HIGH EMERGENCY RISK! Seek immediate help.")
    elif emergency_score >= 5:
        st.warning("⚠️ Moderate risk. Monitor closely.")
    else:
        st.success("✅ Low emergency risk")

    # ================= 6. FOLLOW-UP AI =================
    st.divider()
    st.subheader("🤖 Follow-up Questions")

    followup = st.text_input("Ask anything about your condition")

    if st.button("💬 Ask AI Doctor"):
        if followup.strip():
            lang_instruction = get_language_instruction(language)

            prompt = f"""
            {lang_instruction}

            Previous diagnosis:
            {st.session_state.last_prediction}

            Question:
            {followup}
            """
            answer = get_gemini_response(prompt)
            st.info(answer)

    # ================= 7. PREVENTION =================
    st.divider()
    st.subheader("🛡️ Prevention Tips")

    if st.button("🧠 Get Prevention Plan"):

        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}

        Symptoms: {symptoms}

        Give:
        - Prevention tips
        - Lifestyle improvements
        - Immunity boost plan
        """
        tips = get_gemini_response(prompt)
        st.success(tips)

    # ================= 8. FUTURE PREDICTION =================
    st.divider()
    st.subheader("🔮 Future Health Prediction")

    if st.button("Predict My Future Health"):

        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}

        Symptoms history: {st.session_state.symptom_history}
        Weight history: {st.session_state.weight_history}

        Predict:
        - Future diseases
        - Risk level
        - Prevention plan
        """
        future = get_gemini_response(prompt)
        st.warning(future)

    # ================= 9. HEALTH TYPE =================
    st.divider()
    st.subheader("🧬 Your Health Type")

    if st.button("Detect My Health Type"):

        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}
        
        Water: {st.session_state.water}
        Weight: {st.session_state.weight_history}

        Classify into:
        Fit / At Risk / Unhealthy / Athlete
        Explain why
        """
        result = get_gemini_response(prompt)
        st.success(result)

    # ================= 10. FULL HEALTH INTELLIGENCE =================
    st.divider()
    st.subheader("🧠 AI Health Intelligence")

    if st.button("🔬 Analyze My Full Health"):
        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}

        Water: {st.session_state.water}
        Weight: {st.session_state.weight_history}
        Sleep: {st.session_state.get("sleep_history")}
        Mood: {st.session_state.get("mood_history")}

        Provide:
        - Hidden risks
        - Future problems
        - Lifestyle plan
        """
        insight = get_gemini_response(prompt)
        st.info(insight)
    

     # ================= “MOOD → DISEASE LINK AI” =================

    st.divider()
    st.subheader("🧠 Mind-Body Connection")

    if st.button("Analyze Mood Impact"):
       
       lang_instruction = get_language_instruction(language)

       prompt = f"""
       {lang_instruction}

       Mood history: {st.session_state.get("mood_history")}

       Detect:
       - Mental stress impact on body
       - Possible diseases from stress
       - Advice
       """

       result = get_gemini_response(prompt)
       st.warning(result)


    

    # ================= 11. HEALTH SCORE =================
    st.divider()
    st.subheader("💯 AI Health Score")

    height = st.session_state.get("bmi_height", None)
    target_weight = st.session_state.get("target_weight", None)

    latest_weight = (
        st.session_state.weight_history[-1]
        if st.session_state.weight_history else None
    )

    score = 0

    if latest_weight and height:
        bmi = latest_weight / ((height / 100) ** 2)
        if 18.5 <= bmi <= 25:
            score += 25
        else:
            score += 10

    score += min(st.session_state.water * 2, 20)

    if len(st.session_state.weight_history) >= 5:
        score += 15

    if st.session_state.get("sleep_history"):
        score += 10

    score = min(score, 100)

    st.metric("Health Score", f"{score}/100")
    st.progress(score / 100)

    risk = 100 - score
    st.metric("Risk Score", f"{risk}/100")

    if risk > 70:
        st.error("High Risk")
    elif risk > 40:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")
    
    

 # ================= “HEALTH TREND GRAPH AI” =================

    st.divider()
    st.subheader("📈 Health Trends")

    if st.session_state.weight_history:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.weight_history)
        ax.set_title("Weight Trend")
        st.pyplot(fig)
    
    # ================= “DAILY AI HEALTH MISSIONS” =================

    st.divider()
    st.subheader("🎯 Daily Health Missions")

    missions = [
        "Drink 8 glasses of water 💧",
        "Walk 5000 steps 🚶",
        "Sleep 7+ hours 😴",
    ]

    for m in missions:
        st.write(f"✅ {m}")
    
    
    # ================= “BODY WEAKNESS DETECTOR” =================


    st.divider()
    st.subheader("🧬 Weak Body Area Detection")

    if st.button("Detect Weak Areas"):
        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}

        Symptoms: {st.session_state.symptom_history}

        Detect:
        - Weakest body part
        - Why
        - How to improve
        """

        res = get_gemini_response(prompt)
        st.error(res)

    # ================= 12. WEEKLY REPORT =================
    st.divider()
    st.subheader("📅 Weekly AI Health Report")

    if "report" not in st.session_state:
        st.session_state.report = None

    if st.button("📊 Generate Weekly Report"):
        try:
            lang_instruction = get_language_instruction(language)

            prompt = f"""

            {lang_instruction}

            Weight: {st.session_state.weight_history}
            Target: {target_weight}
            Water: {st.session_state.water}

            Generate:
            - Summary
            - Progress
            - Suggestions
            - Motivation
            """

            report = get_gemini_response(prompt)
            st.session_state.report = report

            st.subheader("📄 Report")
            st.markdown(report)

        except Exception as e:
            st.error(e)

    if st.session_state.report:
        try:
            pdf_file = generate_pdf(st.session_state.report)
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, "health_report.pdf")
        except:
            st.error("PDF failed")

    st.caption("⚠️ Not a substitute for professional medical advice.")




# ---------------- TAB 15 : NEXT-GEN AI HEALTH ----------------
with tab15:

    st.header("🚀 Next-Gen AI Health Assistant")
    st.markdown("### Voice • Camera • AI Diagnosis • Smart Health Report")

    # ================= LANGUAGE =================
    language = st.selectbox(
        "🌐 Select Language",
        ["English", "Hindi", "Hinglish"]
    )

    lang_instruction = get_language_instruction(language)

    st.divider()

    # ================= AI HEALTH CHAT =================
    st.subheader("💬 Ask Health Question")

    question = st.text_input(
        "Type your health question...",
        key="health_question"
    )

    if st.button("🤖 Get AI Advice"):

        if question.strip():

            prompt = f"""
{lang_instruction}

You are an expert AI Health Assistant.

Question:
{question}

Provide:

• Possible reason

• Precautions

• Home remedies

• Lifestyle advice

• When to consult a doctor

Important:
Reply ONLY in the selected language.
"""

            response = get_gemini_response(prompt)

            st.success(response)

            speak(response, language)

        else:
            st.warning("⚠ Please enter a question.")

    st.divider()

    # ================= VOICE SYMPTOM DETECTION =================

    st.subheader("🎤 Voice Symptom Detection")

    st.markdown(
        "Click the button below and describe your symptoms."
    )

    if st.button("🎙 Start Speaking"):

        voice_text = listen(voice_lang[language])

        if voice_text:

            st.success(f"🗣 You said: {voice_text}")

            prompt = f"""
{lang_instruction}

You are an experienced AI Medical Assistant.

Patient Symptoms:
{voice_text}

Provide the response in this format:

🩺 Possible Disease

⚠ Risk Level

💊 General OTC Medicines (if appropriate)

🏠 Home Remedies

🥗 Diet Advice

🏃 Lifestyle Tips

👨‍⚕️ When should the user consult a doctor?

❗ Mention clearly that this is NOT a confirmed medical diagnosis.

IMPORTANT:
Reply ONLY in the selected language.
"""

            result = get_gemini_response(prompt)

            st.markdown("### 🤖 AI Health Analysis")

            st.success(result)

            # Voice Output
            speak(result, language)

        else:

            st.warning(
                "❌ Voice not detected. Please try again."
            )

    st.divider()
    # ================= FOOD IMAGE ANALYSIS =================

    st.subheader("🍎 AI Food Image Analysis")

    food = st.file_uploader(
        "📤 Upload Food Image",
        type=["jpg", "jpeg", "png"],
        key="food_ai"
    )

    if food:

        st.image(food, use_container_width=True)

        if st.button("🥗 Analyze Food"):

            image = input_image_setup(food)

            prompt = f"""
{lang_instruction}

You are a professional Nutrition Expert.

Analyze the uploaded food image.

Provide:

🍽 Food Name

🔥 Estimated Calories

🥩 Protein

🍞 Carbohydrates

🧈 Fat

💪 Health Benefits

⚠ Possible Health Risks

🥗 Is this healthy?

✅ Suggest healthier alternatives if required.

IMPORTANT:
Reply ONLY in the selected language.
"""

            result = get_gemini_response(prompt, image)

            st.success(result)

            speak(result, language)

    st.divider()

    # ================= SKIN ANALYSIS =================

    st.subheader("🩺 AI Skin Disease Detection")

    skin = st.file_uploader(
        "📤 Upload Skin Image",
        type=["jpg", "jpeg", "png"],
        key="skin_ai"
    )

    if skin:

        st.image(skin, use_container_width=True)

        if st.button("🔍 Analyze Skin"):

            image = input_image_setup(skin)

            prompt = f"""
{lang_instruction}

You are an experienced Dermatologist AI.

Analyze the uploaded skin image.

Provide:

🩺 Possible Skin Condition

📊 Severity Level

🏠 Home Care Tips

💊 General OTC Medicines (if appropriate)

👨‍⚕️ When should a dermatologist be consulted?

⚠ Mention clearly that this is NOT a confirmed medical diagnosis.

IMPORTANT:
Reply ONLY in the selected language.
"""

            result = get_gemini_response(prompt, image)

            st.success(result)

            speak(result, language)

    st.divider()
    # ================= SMART DISEASE DETECTOR =================

    st.subheader("🧠 Smart Disease Detection")

    symptoms = st.text_area(
        "✍ Enter your symptoms",
        placeholder="Example: Fever, cough, headache..."
    )

    if st.button("🔬 Detect Disease"):

        if symptoms.strip():

            prompt = f"""
{lang_instruction}

You are an experienced AI Medical Assistant.

Symptoms:
{symptoms}

Provide:

🩺 Possible Disease

📊 Confidence Level (Approximate)

⚠ Risk Level

💊 General OTC Medicines (if appropriate)

🏠 Home Remedies

🥗 Diet Advice

🏃 Lifestyle Tips

👨‍⚕️ When should the patient consult a doctor?

⚠ Mention this is NOT a confirmed medical diagnosis.

Reply ONLY in the selected language.
"""

            result = get_gemini_response(prompt)

            st.success(result)

            speak(result, language)

        else:
            st.warning("⚠ Please enter symptoms.")

    st.divider()

    # ================= BMI CALCULATOR =================

    st.subheader("⚖ BMI Calculator")

    col1, col2 = st.columns(2)

    with col1:
        h = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=170
        )

    with col2:
        w = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=200,
            value=70
        )

    if st.button("📊 Calculate BMI"):

        bmi = w / ((h / 100) ** 2)

        st.metric("BMI", round(bmi, 2))

        if bmi < 18.5:
            st.info("🟡 Underweight")

        elif bmi < 25:
            st.success("🟢 Normal")

        elif bmi < 30:
            st.warning("🟠 Overweight")

        else:
            st.error("🔴 Obese")

    st.divider()

    # ================= QUICK HEALTH CHECK =================

    st.subheader("⚡ Quick AI Health Tips")

    if st.button("⚡ Get Health Tips"):

        prompt = f"""
{lang_instruction}

Give 10 daily health tips.

Include:

🥗 Diet

💧 Water

😴 Sleep

🏃 Exercise

🧘 Mental Health

Reply ONLY in selected language.
"""

        tips = get_gemini_response(prompt)

        st.info(tips)

        speak(tips, language)

    st.divider()

    # ================= PDF REPORT =================

    st.subheader("📄 Generate AI Health Report")

    report = st.text_area(
        "Health Summary",
        height=180
    )

    if st.button("📥 Generate PDF"):

        if report.strip():

            pdf = generate_pdf(report)

            with open(pdf, "rb") as file:

                st.download_button(
                    "⬇ Download AI Health Report",
                    file,
                    file_name="AI_Health_Report.pdf",
                    mime="application/pdf"
                )

        else:
            st.warning("⚠ Please enter report content.")
#========================================================




# ================= VOICE ENGINE =================
def speak(text):
    try:
        tts = gTTS(text=text, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)

        with open(fp.name, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

    except Exception as e:
        st.error(f"Voice Error: {e}")


def listen(lang="en-IN"):
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Speak...")
            audio = r.listen(source)

        return r.recognize_google(audio, language=lang)

    except Exception:
        return ""


voice_lang = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Hinglish": "hi-IN"
}

voice_text = listen(voice_lang[language])

    # ================= 1. VOICE INPUT =================
st.divider()
st.subheader("🎙 Voice Symptom Detection")

if st.button("🎤 Speak Symptoms"):
    voice_text = listen()

    if voice_text:
        st.success(f"You said: {voice_text}")

        lang_instruction = get_language_instruction(language)

        prompt = f"""
{lang_instruction}

User said symptoms:
{voice_text}

Provide:
- Possible diseases
- Risk level
- What to do
"""

        result = get_gemini_response(prompt)

        st.markdown(result)

        # Play AI response
        speak(result)

    else:
        st.warning("❌ Could not understand voice.")

    # ================= 2. IMAGE / CAMERA ANALYSIS =================
    st.divider()
    st.subheader("📷 Image-Based Health Detection")

    uploaded_file = st.file_uploader("Upload image (skin, eye, etc)", type=["jpg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        img_array = np.array(image)

        # Basic brightness analysis (demo AI logic)
        brightness = np.mean(img_array)

        if brightness < 80:
            condition = "Possible skin issue / low brightness"
        elif brightness > 180:
            condition = "Possible overexposure / redness"
        else:
            condition = "Normal"

        st.info(f"🧠 AI Observation: {condition}")

        # AI Explanation
        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}
        Image condition detected: {condition}

        Explain:
        - Possible health issue
        - Should user worry?
        - Next steps
        """

        img_result = get_gemini_response(prompt)
        st.success(img_result)

    # ================= 3. SMART DISEASE DETECTOR =================
    st.divider()
    st.subheader("🧠 Smart Disease Detection AI")

    text_input = st.text_area("Enter symptoms manually")

    if st.button("🔬 Detect Disease"):

        if text_input.strip():
            lang_instruction = get_language_instruction(language)

            prompt = f"""
            {lang_instruction}
            Symptoms: {text_input}

            Predict:
            - Most likely disease
            - Confidence level (%)
            - Severity
            - Recommended action
            """

            result = get_gemini_response(prompt)
            st.success(result)

        else:
            st.warning("⚠️ Enter symptoms")

    # ================= 4. VOICE RESPONSE AI =================
    st.divider()
    st.subheader("🔊 AI Voice Response")

    text_to_speak = st.text_input("Enter text for AI to speak")

    if st.button("🔊 Speak"):
        if text_to_speak:
            speak(text_to_speak)
            st.success("✅ Speaking...")
        else:
            st.warning("Enter something")

    # ================= BONUS: QUICK HEALTH CHECK =================
    st.divider()
    st.subheader("⚡ Quick AI Health Check")

    if st.button("⚡ Run Quick Scan"):
        lang_instruction = get_language_instruction(language)

        prompt = f"""
        {lang_instruction}
        Give a quick general health checklist:
        - Daily habits
        - Warning signs
        - Fitness tips
        Keep it short
        """

        quick = get_gemini_response(prompt)
        st.info(quick)