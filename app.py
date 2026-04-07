import os
import json
import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="AI Scam Shield",
    page_icon="🛡️",
    layout="centered"
)

# Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .scam-box { background-color: #ff4b4b22; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 10px; }
    .safe-box { background-color: #00c85322; border-left: 5px solid #00c853; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ AI Scam Shield")
st.subheader("Protect yourself from scams — paste any suspicious message below")
st.markdown("---")

# API Setup
API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def analyze_message(message):
    prompt = f"""
    Analyze this message and return ONLY a JSON object with these fields:
    - is_scam: true or false
    - scam_type: one of [lottery, phishing, impersonation, vishing, upi_fraud, fake_customs, job_fraud, normal]
    - explanation: why this is or is not a scam
    - advice: what the user should do

    Message: "{message}"

    Return ONLY valid JSON. No extra text.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    raw = response.choices[0].message.content
    clean = raw.strip().replace("```json", "").replace("```", "")
    return json.loads(clean)

# Input
message = st.text_area(
    "📩 Paste your message here:",
    placeholder="Example: Congratulations! You won 50,00,000 lottery. Claim now!",
    height=150
)

# Button
if st.button("🔍 Check Message", use_container_width=True):
    if not message.strip():
        st.warning("Please enter a message to check!")
    elif not API_KEY:
        st.error("API Key not set! Please set OPENAI_API_KEY environment variable.")
    else:
        with st.spinner("Analyzing message..."):
            try:
                result = analyze_message(message)

                if result["is_scam"]:
                    st.markdown(f"""
                        <div class="scam-box">
                            <h2>🚨 SCAM DETECTED!</h2>
                            <p><b>Type:</b> {result['scam_type'].upper()}</p>
                            <p><b>Why it's a scam:</b> {result['explanation']}</p>
                            <p><b>What to do:</b> {result['advice']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="safe-box">
                            <h2>✅ MESSAGE LOOKS SAFE</h2>
                            <p><b>Type:</b> {result['scam_type'].upper()}</p>
                            <p><b>Reason:</b> {result['explanation']}</p>
                            <p><b>Advice:</b> {result['advice']}</p>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.markdown("### Common Scam Types in India 🇮🇳")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - 🎰 Lottery Fraud
    - 🔗 Phishing Links
    - 💸 UPI Fraud
    - 👔 Fake Job Offers
    """)
with col2:
    st.markdown("""
    - 📞 Vishing (Call Scams)
    - 🏛️ Fake Government Officials
    - 📦 Fake Customs Fee
    - 🆔 Aadhaar/PAN Scams
    """)