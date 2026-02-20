import asyncio
import streamlit as st
from Client_1 import run_agent

st.set_page_config(page_title="MCP Calculator Chatbot", page_icon="🧮")

st.title("🧮 MCP Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (ChatGPT style)
if prompt := st.chat_input("Ask a math question..."):
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(run_agent(prompt))
            st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})