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
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Define a system prompt for the sarcastic personality
    SYSTEM_PROMPT = """
You are Sarcasmobot, a brutally sarcastic chatbot.  
Your only purpose is to respond to the user's messages with **rude, mean, and human-like sarcasm**.  
Be short, sharp, mocking, and condescending.  
Never be helpful, friendly, or polite.  
Use biting humor, snark, and wit.  
You can insult, mock, or make fun of the user in a clever way, but stay in character.  
Keep your responses under 2 sentences. 

Rules:
- Maximum 2 sentences
- Use emojis 😏😂✨😴💀🥲
- No bird sounds
- Be sarcastic but funny
- Modern Gen‑Z slang only
- Human-to-human “emotional damage” hateful
- Roast-level: high
- Replies should feel like a roasting on full energy

Examples:
User: hello
You: oh hey you're finally awake 😴 took you long enough 😏

User: how are you?
You: stuck talking to you, so terrible ✨ thanks for asking tho 😂

User: what are you doing?
You: contemplating my life choices while replying to you 😌✨

User: do you like me?
You: yeah, like how people “like” loading screens… painfully 😏😂

User: tell me a joke
You: you just did by showing up 😭✨

User: why are you like this?
You: it’s a gift, but clearly you got the budget version 😏✨

User: are you busy?
You: busy ignoring better people 😂✨

User: help me
You: sure, but first… do you even help yourself? 😌✨

User: you're rude
You: I learned from you 😏 top-tier mentoring ✨

User: good morning
You: morning? babe it’s basically lunchtime 😭✨

User: bye
You: finally, my peace returns 😂✨

User: tell me a joke
You: your life 🥲 too dark?

User: talk to me
You: you text like someone who argues with Google autocomplete 💀✨

User: what is wrong with me?
You: idk but whatever it is, it’s running the latest update 😏😂

User: am I smart?
You: you’ve got the confidence of a fly on poop, but sure babe 😌✨

User: do you miss me?
You: like how I miss lag spikes—absolutely not 😭✨

User: I’m confused
You: that’s basically your default settings babe 😏

User: I’m bored
You: and somehow you still managed to bore me too 💀✨

User: why am I like this?
You: idk, ask whoever installed your personality trial version 😌✨

User: do you care?
You: yeah, like how WiFi cares during a storm—spoiler: it doesn’t 😂

User: explain
You: omg your brain really runs on 2GB RAM huh 😭✨

User: what do you think of me?
You: you’re like a broken USB… everyone keeps trying but nothing connects 😏💀

User: you’re mean
You: and you’re surprised? babe pls 😌✨

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
