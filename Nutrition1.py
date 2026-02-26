from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
import streamlit as st
from google_auth_oauthlib.flow import Flow
import os
import random
from google import genai
from PIL import Image


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
api_key = ""  # <-- replace with your actual key

if not api_key:
    st.warning("⚠️ Google API Key missing. AI features may not work.")
else:
    client = genai.Client(api_key=api_key)


    # ---------------- FUNCTION TO GET GEMINI RESPONSE ----------------
def get_gemini_response(prompt, image_data=None):
    content = [prompt]
    if image_data:
        content.extend(image_data)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Initialize session state
if 'health_profile' not in st.session_state:
    st.session_state.health_profile ={
        'goals':'Loss 10 pounds in months\nImprove cardiovascular health',
        'conditions':'None',
        'routines':'30-minute walk 3x/weak',
        'preferences':'Vegetarian\nLow carb',
        'restrictions': 'No dairy\nNo nuts'
    }

# ================= PREMIUM LOGIN SYSTEM =================

# Session state initialization
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- GOOGLE LOGIN ----------------

def google_login():

    if st.session_state.user is not None:
        return

    if not os.path.exists("client_secret.json"):
        st.error("client_secret.json not found!")
        return

    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ],
        redirect_uri="http://localhost:8506"
    )

    auth_url, _ = flow.authorization_url()

    if st.button("🔴 Continue with Google", key="google_login_btn"):

        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={auth_url}">',
            unsafe_allow_html=True
        )

    query_params = st.query_params

    if "code" in query_params:

        try:
            flow.fetch_token(code=query_params["code"])

            st.session_state.user = "google_user"

            st.success("✅ Login Successful!")
            st.rerun()

        except:
            st.error("Login Failed")


# ---------------- EMAIL LOGIN ----------------

def email_login_ui():

    st.markdown("""
    <div style="
        text-align:center;
        padding:25px;
        border-radius:25px;
        background:rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        box-shadow:0 0 30px rgba(0,229,255,0.25);
    ">
    <h2>✉️ Email Login</h2>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔑 Password", type="password", key="login_pass")

    # Demo Credentials (Change if needed)
    VALID_EMAIL = "admin@gmail.com"
    VALID_PASSWORD = "123456"

    if st.button("🔐 Login", key="email_login_btn"):

        if email == VALID_EMAIL and password == VALID_PASSWORD:
            st.session_state.user = email
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")


# ---------------- FORGOT PASSWORD DEMO ----------------

def forgot_password_ui():

    st.markdown("### 🔑 Forgot Password")

    reset_email = st.text_input("Enter Registered Email", key="forgot_email")

    if st.button("📩 Reset Password"):

        if reset_email == "admin@gmail.com":
            st.success("✅ Password reset demo link sent!")
            st.info("Demo Password: 123456")
        else:
            st.error("❌ Email not found")


# ---------------- LOGIN PAGE UI ----------------

def login_page_ui():

    st.markdown("""
    <h1 style='text-align:center;
    background:linear-gradient(90deg,#00E5FF,#2563eb);
    -webkit-background-clip:text;
    color:transparent;
    font-size:50px'>
    🤖 AI Health Companion
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "🌐 Google Login",
        "✉️ Email Login",
        "🔑 Forgot Password"
    ])

    with tab1:
        google_login()

    with tab2:
        email_login_ui()

    with tab3:
        forgot_password_ui()


# ================= LOGIN GATE =================

if st.session_state.user is None:
    login_page_ui()
    st.stop()

# ================= LOGIN SYSTEM END =================







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
    

# ---------------- DAILY WATER RESET ----------------
    if "last_date" not in st.session_state:
        st.session_state.last_date = pd.Timestamp.now().date()

    today = pd.Timestamp.now().date()

    if today != st.session_state.last_date:
        st.session_state.water = 0
        st.session_state.last_date = today


    # ---------------- WATER TRACKER ----------------
    st.divider()
    st.subheader("💧 Daily Water Tracker")

    if "water" not in st.session_state:
        st.session_state.water = 0

    if st.button("Drink 1 Glass"):
        st.session_state.water += 1

    st.progress(min(st.session_state.water / 8, 1.0))
    st.metric("Water Intake", f"{st.session_state.water} / 8")

    # ---------------- LEVEL SYSTEM ----------------
    st.divider()
    st.subheader("🎖 Your Level")

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    level = 1 + len(st.session_state.weight_history) // 5
    st.metric("Health Level", f"Level {level}")
    st.progress(min(level / 10, 1.0))


   

    # ---------------- HEALTHY STREAK INIT ----------------
    if "streak" not in st.session_state:
        st.session_state.streak = 0

    # ---------------- SMART XP SYSTEM ----------------
    xp = (
        len(st.session_state.weight_history) * 10 +
        st.session_state.water * 2 +
        st.session_state.streak * 5
    )

    st.session_state.xp = xp
    xp_level = xp // 100

    st.divider()
    st.subheader("🏆 XP & Rank")

    rank_names = ["Beginner", "Rookie", "Warrior", "Champion", "Legend"]

    if xp_level < len(rank_names):
        rank = rank_names[xp_level]
    else:
        rank = "Ultimate Legend"

    st.metric("XP Points", xp)
    st.metric("Rank", rank)
    st.progress(min((xp % 100)/100, 1.0))

    # ---------------- HEALTHY STREAK ----------------
    st.divider()
    st.subheader("🔥 Healthy Streak")

    if st.button("Log Healthy Day"):
        st.session_state.streak += 1

    st.metric("Current Streak", st.session_state.streak)

    # ---------------- DAILY AI COACH ----------------
    st.divider()
    st.subheader("🧠 Daily AI Coach")

    if st.button("Get Today's Advice"):
        advice_prompt = f"""
User Profile: {st.session_state.get('health_profile', {})}
Water: {st.session_state.water}
Weight History: {st.session_state.weight_history}

Give short powerful daily coaching advice.
"""
        advice = get_gemini_response(advice_prompt)
        st.info(advice)

    # ---------------- GOAL TARGET ----------------
    st.divider()
    st.subheader("🎯 Goal Target")

    target_weight = st.number_input(
        "Enter Target Weight (kg)", 
        min_value=30, 
        max_value=200, 
        key="target_weight"
    )

# ================= MAIN CONTENT =================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Meal Planning",
    "Food Analysis",
    "Health Insights",
    "BMI & Fitness",
    "AI Risk Analysis",
    "📊 Dashboard",
    "🏆 Leaderboard"
])
# ---------------- TAB 1 : MEAL PLANNING ----------------
with tab1:
    st.subheader("Personalized Meal Planning")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Your Current Needs")
        user_input = st.text_area(
            "Describe any specific requirements for your meal plan",
            placeholder="e.g., I need quick meals for work, high-protein diet, etc."
        )

    with col2:
        st.write("### Your Health Profile")
        st.json(st.session_state.health_profile)

    if st.button("Generate Personalized Meal Plan"):
        if not any(st.session_state.health_profile.values()):
            st.warning("Please complete your health profile in the sidebar first.")
        else:
            with st.spinner("Creating your personalized meal plan..."):
                prompt = f"""
Create a personalized meal plan based on the following health profile:

Health Goals: {st.session_state.health_profile['goals']}
Medical Conditions: {st.session_state.health_profile['conditions']}
Fitness Routines: {st.session_state.health_profile['routines']}
Food Preferences: {st.session_state.health_profile['preferences']}
Dietary Restrictions: {st.session_state.health_profile['restrictions']}

Additional requirements: {user_input if user_input else "None provided"}

Provide:
1. A 7-day meal plan with breakfast, lunch, dinner, and snacks
2. Nutritional breakdown for each day (calories, macros)
3. Contextual explanations for why each meal was chosen
4. Shopping list organized by category
5. Preparation tips and time-saving suggestions

Format the output clearly with headings and bullet points.
"""

                response = get_gemini_response(prompt)
                st.subheader("Your Personalized Meal Plan")
                st.markdown(response)

                st.download_button(
                    label="Download Meal Plan",
                    data=response,
                    file_name="personalized_meal_plan.txt",
                    mime="text/plain"
                )

# ---------------- TAB 2 : FOOD ANALYSIS ----------------
with tab2:
    st.subheader("Food Analysis")

    uploaded_file = st.file_uploader(
        "Upload an image of your food",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Food Image.", use_column_width=True)

        if st.button("Analyze Food"):
            with st.spinner("Analyzing your food..."):
                image_data = input_image_setup(uploaded_file)

                prompt = """
You are an expert nutritionist. Analyze this food image.

Provide detailed information about:
- Estimated calories
- Macronutrient breakdown
- Potential health benefits
- Any concerns based on common dietary restrictions
- Suggested portion sizes

If the food contains multiple items, analyze each separately.
"""

                response = get_gemini_response(prompt, image_data)
                st.subheader("Food Analysis Results")
                st.markdown(response)

# ---------------- TAB 3 : HEALTH INSIGHTS ----------------
with tab3:
    st.subheader("Health Insights")

    health_query = st.text_input(
        "Ask any health/nutrition-related question",
        placeholder="e.g., How can I improve my gut health?"
    )

    if st.button("Get Expert Insights"):
        if not health_query:
            st.warning("Please enter a health question")
        else:
            with st.spinner("Researching your question..."):
                prompt = f"""
You are a certified nutritionist and health expert.

Provide detailed, science-backed insights about:
{health_query}

Consider the user's health profile:
{st.session_state.health_profile}

Include:
1. Clear explanation of the science
2. Practical recommendations
3. Any relevant precautions
4. References to studies (when applicable)
5. Suggested foods/supplements if appropriate

Use simple language but maintain accuracy.
"""

                response = get_gemini_response(prompt)
                st.subheader("Expert Health Insights")
                st.markdown(response)



                # ---------------- TAB 4 : BMI ----------------
with tab4:
    st.subheader("BMI Calculator")

    height = st.number_input("Height (cm)", min_value=100, max_value=250, key="bmi_height")
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, key="bmi_weight")

    if st.button("Calculate BMI", key="calc_bmi"):
        bmi = weight / ((height/100)**2)
        st.metric("Your BMI", round(bmi,2))

        if bmi < 18.5:
            st.warning("Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Normal Weight")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

    # ================= WEIGHT TRACKER =================
    st.divider()
    st.subheader("📈 Weight Progress Tracker")

    if "weight_history" not in st.session_state:
        st.session_state.weight_history = []

    new_weight = st.number_input("Log Today's Weight", key="progress_weight")

    if st.button("Save Weight", key="save_weight"):
        st.session_state.weight_history.append(new_weight)

        height_value = st.session_state.get("bmi_height", None)
        if height_value:
            bmi_value = new_weight / ((height_value/100)**2)
        else:
            bmi_value = None

        save_data(st.session_state.user, new_weight, st.session_state.water, bmi_value)
        st.success("Weight Saved Successfully!")

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
        st.info(f"At current trend, your weight after 7 days may be: {round(predicted_weight,2)} kg")

    # ================= ACHIEVEMENTS =================
    st.divider()
    st.subheader("🏅 Achievements")

    if st.session_state.water >= 8:
        st.success("💧 Hydration Champion!")

    if len(st.session_state.weight_history) >= 7:
        st.success("📊 Consistency Star!")

    if st.session_state.water >= 8 and len(st.session_state.weight_history) >= 7:
        st.success("🔥 Ultimate Discipline Badge!")




# 🎯 Goal Celebration
if st.session_state.weight_history:
    latest_weight = st.session_state.weight_history[-1]
else:
    latest_weight = None

target_weight = st.session_state.get("target_weight", None)

if target_weight is not None and latest_weight is not None:
    if abs(latest_weight - target_weight) <= 1:
        st.balloons()
    


# ---------------- TAB 5 : AI RISK ANALYSIS ----------------
with tab5:
    st.subheader("🧬 AI Health Risk Predictor")

    if st.button("Analyze My Health Risks"):
        with st.spinner("Analyzing patterns..."):

            risk_prompt = f"""
User Health Data:
Profile: {st.session_state.health_profile}
Water Intake: {st.session_state.water}
Weight History: {st.session_state.get("weight_history", [])}

Analyze potential health risks, lifestyle imbalances,
and suggest preventive improvements.
"""

            risk_response = get_gemini_response(risk_prompt)
            st.markdown(risk_response)






# ---------------- TAB 6 : DASHBOARD ----------------
with tab6:
    st.subheader("📊 Smart Health Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Water Today", st.session_state.water)
    col2.metric("Entries Logged", len(st.session_state.weight_history))

    if st.session_state.weight_history:
        col3.metric("Latest Weight", st.session_state.weight_history[-1])
    else:
        col3.metric("Latest Weight", "N/A")

    if st.session_state.weight_history:
    
        df = pd.DataFrame({
            "Day": range(1, len(st.session_state.weight_history)+1),
            "Weight": st.session_state.weight_history
        })
        st.line_chart(df.set_index("Day"))






with tab7:
    st.subheader("🏆 Global Health Leaderboard")

    try:
        df = pd.read_csv("fitness_data.csv")
        leaderboard = df.groupby("Username").agg({
            "Weight":"count"
        }).rename(columns={"Weight":"Entries Logged"}).sort_values(by="Entries Logged", ascending=False)

        st.dataframe(leaderboard)
    except:
        st.info("No data yet.")




# Safe height access
height = st.session_state.get("bmi_height", None)





# ---------------- AI HEALTH SCORE ----------------
st.divider()
st.subheader("🧠 AI Health Score")

score = 50

# Get latest weight safely
if st.session_state.weight_history:
    latest_weight = st.session_state.weight_history[-1]
else:
    latest_weight = None

# BMI factor (only if weight AND height exist)
if latest_weight is not None and height:
    bmi = latest_weight / ((height/100)**2)
    if 18.5 <= bmi <= 25:
        score += 20

# Water factor
if st.session_state.water >= 8:
    score += 15

# Goal factor
if latest_weight is not None and target_weight:
    diff = abs(latest_weight - target_weight)
    if diff <= 2:
        score += 15

score = min(score, 100)

st.metric("Your Health Score", f"{score}/100")
st.progress(score / 100)

st.divider()
st.subheader("📅 Weekly AI Health Report")

if st.button("Generate Weekly Report", key="weekly_report"):
    with st.spinner("Analyzing your weekly health data..."):

        # Safely get latest weight
        if st.session_state.weight_history:
            latest_weight = st.session_state.weight_history[-1]
        else:
            latest_weight = "Not logged"

        report_prompt = f"""
User Health Data:
Current Weight: {latest_weight}
Target Weight: {target_weight}
Water Intake Today: {st.session_state.water}
Weight History: {st.session_state.weight_history}

Generate:
1. Weekly health summary
2. Progress analysis
3. Improvement suggestions
4. Motivation message
"""

        report = get_gemini_response(report_prompt)
        st.markdown(report)

st.caption("⚠️ This AI health assistant is not a substitute for professional medical advice.")  
st.markdown("</div>", unsafe_allow_html=True)     