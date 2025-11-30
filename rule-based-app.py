import streamlit as st

def chatbot(user_input):
  user_input=user_input.lower()
  if "hello" in user_input or "hi" in user_input:
        return "Hello! 👋 How can I help you today?"
  elif "your name" in user_input:
        return "I'm your simple chatbot! 😊"
  elif "bye" in user_input:
        return "Goodbye! 👋 Have a great day!"
  return "I'm not sure how to respond to that yet, but I'm learning! 🤖"

st.title("💬 Simple Rule-Based Chatbot")
st.write("Type something and the chatbot will respond!")
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input.strip() != "":
        bot_reply = chatbot(user_input)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", bot_reply))

for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
