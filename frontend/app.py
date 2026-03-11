import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📄 RAG Document Chatbot")

uploaded_file = st.file_uploader("Upload PDF")

if uploaded_file and st.button("Upload PDF"):

    res = requests.post(
        f"{API_URL}/upload",
        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    )

    st.write("Status code:", res.status_code)
    st.write("Response:", res.text)

    if res.status_code == 200:
        data = res.json()
        st.success(data["message"])
    else:
        st.error("Upload failed")

question = st.text_input("Ask question from document")

if st.button("Ask"):

    res = requests.post(
        f"{API_URL}/ask",
        params={"question": question}
    )

    data = res.json()

    if "answer" in data:

        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Sources")
        st.write(data["sources"])

    elif "error" in data:
        st.error(data["error"])
    
    else:
        st.error("Unexpected response from backend")
        st.write(data)