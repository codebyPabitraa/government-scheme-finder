# pyrefly: ignore [missing-import]
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.retriever import rag_pipeline

st.set_page_config(
    page_title="Government Scheme Finder",
    page_icon="🇮🇳",
    layout="centered"
)

st.title("🇮🇳 Government Scheme Finder")
st.subheader("Find schemes you are eligible for")

st.divider()

with st.form("user_form"):
    age = st.number_input("Your Age", min_value=0, max_value=100, value=25)
    income = st.number_input("Annual Family Income (Rs)", min_value=0, value=150000, step=10000)
    state = st.selectbox("State", ["All India", "West Bengal", "Maharashtra", "Tamil Nadu", "Uttar Pradesh"])
    caste = st.selectbox("Category", ["All", "SC", "ST", "OBC", "Minority"])
    occupation = st.selectbox("Occupation", ["Farmer", "Student", "Business Owner", "Unemployed", "Salaried", "Other"])
    extra = st.text_input("Any specific need? (optional)", placeholder="e.g. health insurance, housing, girl child")
    submitted = st.form_submit_button("Find Schemes")

if submitted:
    query = f"I am a {age} year old {occupation} from {state}. My annual family income is Rs {income}. I belong to {caste} category. {extra}"
    
    with st.spinner("Finding schemes for you..."):
        response = rag_pipeline(query)
    
    st.divider()
    st.markdown("### Schemes You May Be Eligible For")
    st.markdown(response)