import streamlit as st
import pandas as pd
from groq import Groq
import os

# Get API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load data
df = pd.read_csv("data.csv")

st.title("🤖 CRM Copilot")

# Select customer
customer_name = st.selectbox("Select Customer", df["customer"])
customer_data = df[df["customer"] == customer_name].iloc[0]

st.subheader("Customer Data")
st.write(customer_data)

# LLM function
def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Features
def generate_summary(data):
    prompt = f"""
    Summarize this customer:
    {data}
    Include status, risks, and opportunities.
    """
    return call_llm(prompt)

def generate_action(data):
    prompt = f"""
    Suggest next best action:
    {data}
    Include action, reason, and impact.
    """
    return call_llm(prompt)

def generate_email(data):
    prompt = f"""
    Write a professional email:
    {data}
    Tone: helpful and empathetic.
    """
    return call_llm(prompt)

# Buttons
if st.button("Generate Summary"):
    st.write(generate_summary(customer_data))

if st.button("Next Best Action"):
    st.write(generate_action(customer_data))

if st.button("Draft Email"):
    st.write(generate_email(customer_data))