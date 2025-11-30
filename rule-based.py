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
