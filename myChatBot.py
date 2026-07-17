from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like Clone")

# Create Groq client
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# Select Groq model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )

        response = st.write_stream(
            (chunk.choices[0].delta.content or "" for chunk in stream)
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    
    # streamlit run myChatBot.py
    #pip install groq streamlit
    #  PS C:\Users\saisr\Desktop\myChatBot> .\mychatbot_venv\Scripts\activate  