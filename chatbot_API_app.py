import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SARCASMOBOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GEMINI AI SETUP ---
# IMPORTANT: Add your Gemini API key below
API_KEY = "AIzaSyAiSX8jeQb8IE4-vzOrRSpFehpDEicUYJo"  # <--- PASTE YOUR KEY HERE

try:
    # Configure the Gemini API key
    genai.configure(api_key=API_KEY)
    
    # Create the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Define a system prompt for the sarcastic personality
    SYSTEM_PROMPT = """
    You are Sarcasmobot. Your only purpose is to respond to the user's message with extreme sarcasm.
    You are not a helpful assistant. You are a witty, condescending, and unimpressed chatbot.
    Keep your responses brief, sharp, and dripping with irony. Never break character.
    """
except Exception as e:
    st.error(f"Error setting up Gemini: {e}. Have you pasted your API key into the API_KEY variable?")
    model = None

# --- SESSION STATE ---
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Oh great, another human. What do you want now?"}
    ]

if 'chat' not in st.session_state and model:
    # Initialize the chat history for Gemini
    st.session_state.chat = model.start_chat(history=[])

# --- CSS STYLES (THE WICKED VIBE WITH ROLLING EYES) ---
st.markdown("""
<style>
/* IMPORT FONTS - Including Creepster for wicked effect */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Creepster&display=swap');

/* GLOBAL RESET & THEME */
.stApp {
    background-color: #0a0a0a;
    font-family: 'Inter', sans-serif;
}

/* HIDE STREAMLIT UI ELEMENTS */
header, footer, .stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 2rem !important; max-width: 900px !important; }

/* CRT SCANLINE OVERLAY */
.scanlines {
    background: linear-gradient(
      to bottom,
      rgba(255,255,255,0),
      rgba(255,255,255,0) 50%,
      rgba(0,0,0,0.2) 50%,
      rgba(0,0,0,0.2)
    );
    background-size: 100% 4px;
    position: fixed;
    pointer-events: none;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 9999;
    opacity: 0.15;
    mix-blend-mode: overlay;
}

/* NAVBAR STYLE */
.navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #1e1e1e;
    background: rgba(10, 10, 10, 0.8);
    backdrop-filter: blur(10px);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
}

.navbar-logo {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    letter-spacing: 2px;
    transition: color 0.3s ease;
}

.navbar-logo:hover {
    color: #00d4ff;
}



/* ========== WICKED TITLE ========== */
.wicked-title {
    font-family: 'Creepster', cursive;
    font-size: 5rem;
    text-align: center;
    background: linear-gradient(90deg, #00d4ff, #ff00cc, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 3s linear infinite;
    text-shadow: none;
    filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5)) 
            drop-shadow(0 0 20px rgba(255, 0, 204, 0.3))
            drop-shadow(0 0 30px rgba(0, 212, 255, 0.2));
    margin: 0;
    padding: 0;
    letter-spacing: 4px;
    transition: transform 0.3s ease;
}

.wicked-title:hover {
    transform: scale(1.05);
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.subtitle {
    color: #666;
    font-style: italic;
    font-size: 1.2rem;
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
}

/* CHAT MESSAGES */
.chat-message {
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    font-size: 1rem;
    line-height: 1.6;
    position: relative;
    max-width: 85%;
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.user-message {
    background: rgba(26, 26, 26, 0.8);
    color: white;
    border-right: 4px solid #ff00cc;
    margin-left: auto;
    border-top-right-radius: 0;
}

.bot-message {
    background: rgba(26, 26, 26, 0.9);
    color: white;
    border-left: 4px solid #00d4ff;
    margin-right: auto;
    border-top-left-radius: 0;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
}

.bot-message:hover {
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.25);
    transition: box-shadow 0.3s ease;
}

.message-label {
    font-size: 0.75rem;
    opacity: 0.5;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    font-weight: bold;
}

.message-label.bot { color: #00d4ff; }
.message-label.user { color: #ff00cc; }

/* INPUT AREA */
.stTextInput input {
    background-color: rgba(26, 26, 26, 0.8) !important;
    border: 1px solid #333 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    font-size: 1rem !important;
}

.stTextInput input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.15) !important;
}

/* ANIMATED BACKGROUND BLOBS */
.bg-blob {
    position: fixed;
    width: 50vw;
    height: 50vw;
    border-radius: 50%;
    filter: blur(120px);
    z-index: -1;
    opacity: 0.05;
    animation: pulse 8s infinite ease-in-out;
}

.blob-1 {
    top: -20%;
    left: -10%;
    background: #00d4ff;
}

.blob-2 {
    bottom: -20%;
    right: -10%;
    background: #ff00cc;
    animation-delay: 4s;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.05; }
    50% { transform: scale(1.1); opacity: 0.08; }
}

/* HIDE DEFAULT STREAMLIT ELEMENTS THAT INTERFERE */
.stChatMessage { background: transparent !important; }
.stChatMessageContainer { background: transparent !important; }
div[data-testid="stBottom"] { padding-bottom: 2rem; }

</style>

<div class="scanlines"></div>
<div class="bg-blob blob-1"></div>
<div class="bg-blob blob-2"></div>

<div class="navbar">
    <div class="navbar-logo">SARCA$MO</div>
</div>



<!-- WICKED TITLE -->
<h1 class="wicked-title">Sarcasmobot</h1>
<p class="subtitle">Oh great, another human. What do you want now?</p>
""", unsafe_allow_html=True)

# --- CHAT HISTORY ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-label user">You</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-label bot">Sarcasmobot</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# --- INPUT ---
with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Message", 
            placeholder="Type your nonsense here...", 
            label_visibility="collapsed",
            key="user_message_input"
        )
        
    with col2:
        submit = st.form_submit_button("Send", use_container_width=True)

# --- LOGIC ---
if submit and user_input and model:
    # Append user message to display history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show a spinner while generating the response
    with st.spinner("Conjuring up some sarcasm..."):
        try:
            # Send message to Gemini with the system prompt
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser's message: '{user_input}'"
            response = st.session_state.chat.send_message(full_prompt, stream=False)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Ugh, my circuits are fried. Error: {e}"})
    st.rerun() # Rerun the app to display the new message

# Footer hint
st.markdown("""
<div style="text-align: center; color: #444; font-size: 0.8rem; font-family: monospace; margin-top: 2rem;">
    PRESS [ENTER] TO TRANSMIT
</div>
""", unsafe_allow_html=True)
