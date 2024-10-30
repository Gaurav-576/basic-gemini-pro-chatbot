import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(
    page_title="Gemini Pro Chat Assistant",
    page_icon="🧠",
    layout="centered"
)

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model=genai.GenerativeModel("gemini-pro")

def translate_role(user_role):
    return "assistant" if user_role=="model" else user_role
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])
st.markdown("""
    <style>
        /* Dark background and overall font adjustments */
        .stApp {
            background-color: #121212; /* Very dark gray background */
            color: #E0E0E0; /* Light font color for overall readability */
        }
        .title {
            font-size: 2.5rem;
            color: #FF8A65; /* Soft coral color for title */
            font-weight: 700;
            text-align: center;
        }
        .description {
            font-size: 1.2rem;
            color: #BDBDBD; /* Light gray color for description */
            text-align: center;
            margin-bottom: 20px;
        }
        /* Styling for user and assistant chat bubbles */
        .user-bubble, .assistant-bubble {
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            display: inline-block;
            max-width: 80%;
            font-size: 1rem;
            font-weight: 500;
        }
        .user-bubble {
            background-color: #263238; /* Dark teal background for user bubble */
            color: #E0F7FA; /* Light cyan font color for user text */
            text-align: right;
        }
        .assistant-bubble {
            background-color: #424242; /* Dark gray background for assistant bubble */
            color: #FFECB3; /* Soft amber font color for assistant text */
            text-align: left;
        }
        /* Additional padding for chat input */
        .stTextInput > div {
            padding: 10px;
        }
    </style>
    <h1 class="title">Gemini Pro Chat Assistant 🧠</h1>
    <p class="description">Interact with Gemini Pro for intelligent conversation and insights.</p>
""", unsafe_allow_html=True)
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        bubble_style="user-bubble" if translate_role(message.role)=="user" else "assistant-bubble"
        st.markdown(f"<div class='{bubble_style}'>{message.parts[0].text}</div>", unsafe_allow_html=True)
user_input=st.chat_input("Type your message here...")
if user_input:
    st.chat_message("user").markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)
    gemini_response=st.session_state.chat_session.send_message(user_input)
    with st.chat_message("assistant"):
        st.markdown(f"<div class='assistant-bubble'>{gemini_response.text}</div>", unsafe_allow_html=True)
