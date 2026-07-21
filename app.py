from openai import OpenAI
import streamlit as st

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Jarvis AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#020617);
    color:white;
}

/* Header */
.title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#38bdf8;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:25px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
}

/* Hide Streamlit Footer */
footer{
    visibility:hidden;
}

/* ---------------- CHAT INPUT ---------------- */

/* Make input container wider */
[data-testid="stChatInput"]{
    width:95% !important;
    max-width:1400px !important;
    margin:auto !important;
}

/* Style the input box */
[data-testid="stChatInput"] textarea{
    font-size:18px !important;
    min-height:55px !important;
    border-radius:25px !important;
}

/* Send button */
[data-testid="stChatInput"] button{
    border-radius:50% !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown(
    "<div class='title'>🤖 JARVIS AI ChatBot</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>Powered by Groq • Llama 3.3 70B</div>",
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=120,
    )

    st.title("Jarvis")

    st.success("🟢 Online")

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("### Model")
    st.info("llama-3.3-70b-versatile")

    st.divider()

    st.caption("Made with ❤️ using Streamlit & Groq")

# ---------------- GROQ CLIENT ---------------- #

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# ---------------- SESSION ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ---------------- #

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ---------------- #

prompt = st.chat_input("💬 Ask Jarvis anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True,
            )

            response = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

# ---------------- FOOTER ---------------- #

st.markdown("""
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">

<hr>

<div style="text-align:center; padding:15px;">

<h4 style="margin-bottom:15px,font-size:14px;">Made with ❤️ by Sravan Aditya</h4>

<div style="
    display:flex;
    justify-content:center;
    align-items:center;
    gap:30px;
">

<a href="https://github.com/penumarthisaisravanaditya"
target="_blank"
style="color:white; font-size:32px; text-decoration:none;">
<i class="fab fa-github"></i>
</a>

<a href="https://instagram.com/sravan_aditya_"
target="_blank"
style="color:#E1306C; font-size:32px; text-decoration:none;">
<i class="fab fa-instagram"></i>
</a>

</div>

</div>
""", unsafe_allow_html=True)
