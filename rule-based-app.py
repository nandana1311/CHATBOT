import streamlit as st
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
