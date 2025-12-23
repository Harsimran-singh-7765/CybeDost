import streamlit as st
import google.generativeai as genai
import sqlite3
import uuid
import datetime

# ==========================================
# DATABASE SETUP (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    # Table banate hain agar nahi hai
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', 
              (session_id, role, content))
    conn.commit()
    conn.close()

def get_messages(session_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY id', (session_id,))
    messages = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    conn.close()
    return messages

def get_all_sessions():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    # Unique session IDs laate hain, latest pehle
    c.execute('SELECT DISTINCT session_id, MAX(timestamp) as time FROM messages GROUP BY session_id ORDER BY time DESC')
    sessions = [row[0] for row in c.fetchall()]
    conn.close()
    return sessions

# Database initialize karo start mein
init_db()

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Cyber Dost",
    page_icon="🛡️",
    layout="wide" # Layout wide kar diya taaki history achhi dikhe
)

# ==========================================
# API SETUP
# ==========================================
# TODO: Apna API Key yahan dalo
GOOGLE_API_KEY = "your api key"
genai.configure(api_key=GOOGLE_API_KEY)

SYSTEM_PROMPT = """
You are 'Cyber Dost', a professional Cyber Security Consultant.
Your goal is to help students (Class 11-12) stay safe online.
Keep answers concise, expert, and strictly related to Cyber Safety.
Do not answer questions about illegal hacking.
"""

@st.cache_resource
def get_model():
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite", 
        generation_config=generation_config,
        system_instruction=SYSTEM_PROMPT
    )
    return model

try:
    model = get_model()
except Exception:
    st.error("Error connecting to AI. Check API Key.")

# ==========================================
# SESSION MANAGEMENT
# ==========================================
# Agar session_id nahi hai, toh naya banao
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ==========================================
# SIDEBAR (History & New Chat)
# ==========================================
with st.sidebar:
    st.title("🛡️ Cyber Dost")
    
    # 1. NEW CHAT BUTTON
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.write("**Chat History**")

    # 2. LOAD PREVIOUS SESSIONS
    sessions = get_all_sessions()
    
    for sess_id in sessions:
        # Har session ke liye ek button
        # Button ka label thoda readable banate hain (Starting ke 8 chars)
        label = f"Chat #{sess_id[:8]}"
        
        # Agar current session yehi hai, toh highlight karo (simple trick)
        if sess_id == st.session_state.session_id:
            st.markdown(f"👉 **{label}**")
        else:
            if st.button(label, key=sess_id):
                st.session_state.session_id = sess_id
                st.rerun()

# ==========================================
# MAIN CHAT INTERFACE
# ==========================================
st.subheader("Security Operations Center")

# 1. Load messages from DB for the CURRENT Session
current_messages = get_messages(st.session_state.session_id)

# Agar naya chat hai aur DB khali hai, toh Welcome message dikhao aur save karo
if not current_messages:
    welcome_msg = "Hello! I am Cyber Dost. Ask me about passwords, phishing, or staying safe online."
    save_message(st.session_state.session_id, "model", welcome_msg)
    current_messages = [{"role": "model", "content": welcome_msg}]

# 2. Display Chat
for message in current_messages:
    avatar = "🛡️" if message["role"] == "model" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 3. User Input
if prompt := st.chat_input("Type your query here..."):
    # UI update karo immediate
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # DB mein save karo User ka message
    save_message(st.session_state.session_id, "user", prompt)

    try:
        # History for AI context
        chat_history_for_ai = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in current_messages
        ]
        
        chat = model.start_chat(history=chat_history_for_ai)
        
        with st.chat_message("model", avatar="🛡️"):
            response_placeholder = st.empty()
            full_response = ""
            
            response = chat.send_message(prompt, stream=True)
        for chunk in response:
                        try:
                            # Check if text exists before accessing it
                            if chunk.text:
                                full_response += chunk.text
                                response_placeholder.markdown(full_response + "▌")
                        except ValueError:
                            # Agar chunk khali hai (safety block ya stop signal), toh ignore karo
                            pass
        
        # DB mein save karo AI ka response
        save_message(st.session_state.session_id, "model", full_response)

    except Exception as e:
        st.error(f"Error: {e}")