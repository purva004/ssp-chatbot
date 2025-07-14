import streamlit as st
import requests

st.title("Occupancy CrewAI Chatbot")

query = st.text_input("Ask a question about occupancy data:")

if st.button("Ask"):
    response = requests.post("http://localhost:8000/crewquery", json={"query": query})
    st.write(response.json().get("result"))