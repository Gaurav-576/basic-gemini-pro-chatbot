
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini Pro",
    page_icon="🧠",
    layout="wide"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model=genai.GenerativeModel("gemini-pro")

def translate_role(user_role):
    if user_role=="model":
        return "assistant"
    else:
        return user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("Chat with Gemini Pro")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text)
        
user_input=st.chat_input("Type a message...")
if user_input:
    st.chat_message("user").markdown(user_input)
    gemini_response=st.session_state.chat_session.send_message(user_input)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)