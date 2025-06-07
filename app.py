import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
from prompt_template import SYSTEM_PROMPT_TEMPLATE
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API = os.getenv("GROQ_API")


st.title("🧠 Groq Code Companion")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["gemma2-9b-it", "llama-3.3-70b-versatile","llama3-70b-8192","mixtral-8x7b-32768"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🐍 Python Expert
    - 🐞 Debugging Assistant
    - 📝 Code Documentation
    - 💡 Solution Design
    """)
    st.divider()
    st.markdown("Built with [Groq](https://groq.com/) | [LangChain](https://python.langchain.com/)")


# Initialize the Groq client
groq_client = ChatGroq(
    groq_api_key=GROQ_API,
    model_name=selected_model,
    temperature=0.3
)

# System prompt configuration
# system_prompt = SystemMessagePromptTemplate.from_template(
#     """you name is sofia ,you are a helpfull assistance,
#     You are an expert AI coding assistant. Provide concise, correct solutions ,
#     with strategic print statements for debugging. Always respond in English."""
# )
system_prompt = SystemMessagePromptTemplate.from_template(
SYSTEM_PROMPT_TEMPLATE
)

# Session state management
if "message_log" not in st.session_state:
    # st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm sofia. How can I help you code today? 💻"}]
    st.session_state.message_log = []

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
# Chat input and processing
user_query = st.chat_input("Type your coding question here...")

# Invocation of the AI engine
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | groq_client | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()
