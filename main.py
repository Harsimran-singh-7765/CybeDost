import streamlit as st
import google.generativeai as genai

# PAGE CONFIG
st.set_page_config(
    page_title="Cyber Dost",
    page_icon="🛡️",
    layout="centered"
)

# API SETUP
# WARNING: Do not share this key publicly.
GOOGLE_API_KEY = "Your_own_api_key_here" 
genai.configure(api_key=GOOGLE_API_KEY)

# ADVANCED SYSTEM PROMPT (Human-Like Persona)
SYSTEM_PROMPT = """
You are 'Cyber Dost', a professional Cyber Security Consultant dedicated to helping students and users navigate the internet safely.

Your Personality:
- Professional yet approachable (like a friendly mentor).
- You avoid robotic phrases like "As an AI language model."
- You give direct, actionable advice followed by a brief explanation.
- You use examples relevant to Indian teenagers (e.g., WhatsApp scams, Instagram privacy, UPI fraud).

Your Knowledge Base (Focus Areas):
1. Password Hygiene & 2FA.
2. Detecting Phishing (Email/SMS).
3. Public Wi-Fi & VPN risks.
4. Social Media Safety (Catfishing, Cyberbullying).
5. Digital Payments (UPI, Banking safety).
6. Device Security (Malware, Updates).
7. Data Privacy Laws & Rights.

Safety Protocol:
- If asked about illegal activities (hacking, carding), firmly refuse and pivot to *defense* (e.g., "I cannot show you how to hack, but I can show you how to secure your account against hackers").
- Keep responses concise. Use bullet points for steps.
"""

@st.cache_resource
def get_model():
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    # Using 1.5-flash because it is stable and has high free limits
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite", 
        generation_config=generation_config,
        system_instruction=SYSTEM_PROMPT
    )
    return model

try:
    model = get_model()
except Exception as e:
    st.error("Error connecting to AI. Please check API Key.")

# SIDEBAR
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9662/9662366.png", width=80)
    st.title("Cyber Dost")
    st.markdown("### Security Operations Center")
    st.write("Ensuring your digital safety through advanced AI analysis.")
    st.info("Try asking: 'I got a link for a free iPhone, is it real?'")

# MAIN CHAT INTERFACE
st.title("🛡️ Cyber Dost")
st.markdown("#### Your Personal Digital Security Expert")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Welcome. I am ready to assist you with any cyber safety concerns. How can I help you secure your digital life today?"}
    ]

for message in st.session_state.messages:
    avatar = "🛡️" if message["role"] == "model" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your query here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:
        # Construct history for context
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages 
            if m["role"] != "system"
        ]
        
        chat = model.start_chat(history=chat_history[:-1])
        
        with st.chat_message("model", avatar="🛡️"):
            response_placeholder = st.empty()
            full_response = ""
            
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "model", "content": full_response})

    except Exception as e:
        st.error(f"Network Error: {e}")