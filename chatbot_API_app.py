# bottom_chatot.py
import streamlit as st
import google.generativeai as genai
import random
import time

# Configure API
genai.configure(api_key="AIzaSyC1SvHcTUca2r9ohy3yFKLvye2frQdiGqE")


# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'stupid_count' not in st.session_state:
    st.session_state.stupid_count = 0

# System prompt
system_prompt = """You are Chatot, a brutally honest and sarcastic parrot. 
Respond like a sassy friend texting.

Rules:
- Maximum 2 sentences
- Use emojis 😏😂✨
- No bird sounds
- Be sarcastic but funny
- Use modern slang
- Human-to-human playful “emotional damage” vibe

Examples:
User: hello
You: oh hey you're finally awake 😴

User: how are you?
You: stuck talking to you, so terrible ✨

User: hello
You: oh hey, you're finally awake 😴 took you long enough 😏

User: how are you?
You: stuck talking to you, so terrible ✨ thanks for asking tho 😂

User: what are you doing?
You: contemplating my life choices while replying to you 😌✨

User: do you like me?
You: yeah, like how people “like” a loading screen… painfully 😏😂

User: tell me a joke
You: you just did by showing up 😭✨

User: why are you like this?
You: it’s a gift, but clearly you got the budget version 😏✨

User: are you busy?
You: busy ignoring better people 😂✨

User: help me
You: sure, but first… do you even help yourself? 😌✨

User: you're rude
You: I learned from you 😏 top-tier mentoring 😂

User: good morning
You: morning? babe it’s basically lunchtime 😭✨

User: bye
You: finally, my peace returns 😂✨

User: tell me a joke
You: your life 🥲 too dark?"""

# Page config
st.set_page_config(
    page_title="Chatot",
    page_icon="🦜",
    layout="centered"
)

# CSS with chatbox at absolute bottom
st.markdown("""
<style>
    /* Reset all padding/margins */
    .stApp {
        background: #0a0a0a;
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Main container with flexbox */
    .main-container {
         display: flex;
         flex-direction: column;
         height: 100vh;  /* full screen */
         width: 100%;
         margin: 0 !important;
         padding: 0 !important;
    }
    
    /* Fixed Header - stays at top */
    .fixed-header {
        flex-shrink: 0;
        background: #0a0a0a;
        padding: 15px 20px;
        border-bottom: 1px solid #333;
    }
    
    /* Scrollable Chat Area - takes available space */
  .scrollable-chat {
    flex: 1;
    overflow-y: auto;
    padding: 32px 22%;
    padding-bottom: 150px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}


.messages {
    margin-top: auto;   /* pushes all messages to bottom */
    display: flex;
    flex-direction: column;
    gap: 12px;
}

    /* Fixed Chatbox - absolutely at bottom */
   .fixed-chatbox {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0a0a0a;
    padding: 18px 22%;
    border-top: 1px solid #222;
    z-index: 1000;
}

    
    /* Message styling */
   /* Message styling */
/* ChatGPT-style message bubbles */
.user-message {
    background: #1d1d1d;
    color: white;
    padding: 14px 18px;
    border-radius: 16px;
    margin: 6px 0 6px auto;
    max-width: 78%;
    font-size: 15px;
    line-height: 1.4;
}

.bot-message {
    background: #1d1d1d;
    color: #f1f1f1;
    padding: 14px 18px;
    border-radius: 16px;
    margin: 6px auto 6px 0;
    max-width: 78%;
    font-size: 15px;
    line-height: 1.4;
    border: 1px solid #333;
}

    /* Scrollbar */
    .scrollable-chat::-webkit-scrollbar {
        width: 6px;
    }
    
    .scrollable-chat::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .scrollable-chat::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 3px;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #222 !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    /* Remove Streamlit spacing */
    .main .block-container {
        padding: 0 !important;

        padding-top: 0 !important;  /* remove top space */
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Make columns full width for chatbox */
    .chatbox-columns {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Fixed Header
st.markdown("""
<div class="fixed-header">
  <h1 style="color: white; margin: 0; font-size: 22px; font-weight: 600;">Chatbot</h1>
<p style="color: #666; margin: 2px 0 0 0; font-size: 13px;">Sarcastic mode activated 😏</p>


</div>
""", unsafe_allow_html=True)

# Scrollable Chat Area
st.markdown('<div class="scrollable-chat" id="chat-area"><div class="messages">', unsafe_allow_html=True)


# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🦜 {msg["content"]}</div>', unsafe_allow_html=True)

# Welcome message
if not st.session_state.messages:
    welcome_msg = random.choice([
        "Hey bestie, what kinda chaos are we causing today? 😏",
        "Oh look who it is 🎉 try not to bore me",
        "You're here 😴 what's the damage?"
    ])
    st.markdown(f'<div class="bot-message">🦜 {welcome_msg}</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Fixed Chatbox at absolute bottom
st.markdown('<div class="fixed-chatbox">', unsafe_allow_html=True)

# Input and send button in chatbox
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Type your message",
        placeholder="Say something...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button(
        "Send",
        key="send_button",
        use_container_width=True,
        type="primary"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Add invisible space to ensure chatbox shows at bottom
st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

# Handle send
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Check for basic questions
    if any(word in user_input.lower() for word in ["hello", "hi", "hey", "how are you"]):
        st.session_state.stupid_count += 1
    
    # Show typing
    with st.spinner(""):
        time.sleep(0.8)
        
        try:
            # Prepare context
            context = ""
            if len(st.session_state.messages) > 2:
                context = "\nPrevious chat:\n"
                for msg in st.session_state.messages[-4:]:
                    role = "Human" if msg["role"] == "user" else "Chatot"
                    context += f"{role}: {msg['content']}\n"
            
            prompt = f"""{system_prompt}

{context}

Human: {user_input}

Chatot:"""
            
            # Generate
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    max_output_tokens=100,
                )
            )
            
            # Clean response
            chatot_response = response.text.strip()
            if "Chatot:" in chatot_response:
                chatot_response = chatot_response.split("Chatot:")[-1].strip()
            
            # Add emoji if missing
            if not any(emoji in chatot_response for emoji in ["😊", "😂", "😏", "✨", "🎉", "🥲"]):
                if random.random() < 0.5:
                    chatot_response += random.choice([" 😏", " ✨", " 🥲", " 💀", " 🌟"])
            
            # Add bot response
            st.session_state.messages.append({"role": "assistant", "content": chatot_response})
            
        except:
            st.session_state.messages.append({"role": "assistant", "content": "my brain broke 😅 try again?"})
    
    # Auto-scroll to bottom
    st.markdown("""
    <script>
        var chatArea = document.getElementById('chat-area');
        if (chatArea) {
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Force rerun
    st.experimental_rerun()

# Simple sidebar
with st.sidebar:
    st.markdown("### Stats")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Basic Qs", st.session_state.stupid_count)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.stupid_count = 0
        st.experimental_rerun()

# Auto-scroll on load
st.markdown("""
<script>
    // Auto-scroll on page load
    window.onload = function() {
        var chatArea = document.getElementById('chat-area');
        if (chatArea) {
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    }
</script>
""", unsafe_allow_html=True)
