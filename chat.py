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
API_KEY = "AIzaSyC1SvHcTUca2r9ohy3yFKLvye2frQdiGqE"  # <--- PASTE YOUR KEY HERE

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

/* ========== ROLLING EYES ANIMATION ========== */
.eyes-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    margin-bottom: 10px;
    margin-top: 80px;
}

.eye-wrapper {
    position: relative;
}

.eyebrow {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 56px;
    height: 8px;
    background: #333;
    border-radius: 10px;
    animation: eyebrow-raise 4s ease-in-out infinite;
}

.eye-socket {
    width: 56px;
    height: 56px;
    background: linear-gradient(to bottom, #1a1a1a, #111);
    border-radius: 50%;
    border: 2px solid #333;
    box-shadow: inset 0 4px 8px rgba(0,0,0,0.5), 0 0 20px rgba(0,212,255,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}

.eye-socket.right {
    box-shadow: inset 0 4px 8px rgba(0,0,0,0.5), 0 0 20px rgba(255,0,204,0.15);
}

.eyeball {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, white, #e0e0e0);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.blood-vessel {
    position: absolute;
    width: 6px;
    height: 12px;
    background: rgba(255, 100, 100, 0.2);
    border-radius: 50%;
}

.blood-vessel.v1 { top: 4px; left: 4px; transform: rotate(45deg); }
.blood-vessel.v2 { top: 6px; right: 6px; transform: rotate(-30deg); width: 4px; height: 10px; }

.iris {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    position: relative;
    animation: eye-roll 4s ease-in-out infinite;
}

.iris.cyan {
    background: linear-gradient(135deg, #00d4ff, #0088aa);
}

.iris.magenta {
    background: linear-gradient(135deg, #ff00cc, #aa0088);
}

.pupil {
    width: 12px;
    height: 12px;
    background: black;
    border-radius: 50%;
    animation: pupil-contract 4s ease-in-out infinite;
}

.light-reflection {
    position: absolute;
    top: 2px;
    right: 2px;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
}

.eyelid {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(to bottom, #1a1a1a, #0a0a0a);
    border-radius: 28px 28px 0 0;
    z-index: 10;
    animation: blink 4s ease-in-out infinite;
}

/* Eye Animation Keyframes */
@keyframes eye-roll {
    0%, 100% { transform: translate(0, 0); }
    15% { transform: translate(4px, 2px); }
    30% { transform: translate(-3px, -2px); }
    45%, 55% { transform: translate(0, -10px); } /* Roll up - the sarcastic look */
    70% { transform: translate(3px, 1px); }
    85% { transform: translate(-4px, 0); }
}

@keyframes blink {
    0%, 40%, 60%, 100% { height: 0%; }
    45%, 55% { height: 50%; } /* Half-closed during eye roll */
    48%, 52% { height: 100%; } /* Quick blink */
}

@keyframes eyebrow-raise {
    0%, 40%, 60%, 100% { transform: translateX(-50%) rotate(0deg) translateY(0); }
    45%, 55% { transform: translateX(-50%) rotate(-10deg) translateY(-4px); }
}

@keyframes pupil-contract {
    0%, 40%, 60%, 100% { transform: scale(1); }
    45%, 55% { transform: scale(0.7); }
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

<!-- ROLLING EYES -->
<div class="eyes-container">
    <!-- Left Eye -->
    <div class="eye-wrapper">
        <div class="eyebrow"></div>
        <div class="eye-socket">
            <div class="eyeball">
                <div class="blood-vessel v1"></div>
                <div class="blood-vessel v2"></div>
                <div class="iris cyan">
                    <div class="pupil"></div>
                    <div class="light-reflection"></div>
                </div>
            </div>
            <div class="eyelid"></div>
        </div>
    </div>
    
    <!-- Right Eye -->
    <div class="eye-wrapper">
        <div class="eyebrow" style="animation-delay: 0.1s;"></div>
        <div class="eye-socket right">
            <div class="eyeball">
                <div class="blood-vessel v1"></div>
                <div class="blood-vessel v2"></div>
                <div class="iris magenta">
                    <div class="pupil"></div>
                    <div class="light-reflection"></div>
                </div>
            </div>
            <div class="eyelid" style="animation-delay: 0.05s;"></div>
        </div>
    </div>
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
