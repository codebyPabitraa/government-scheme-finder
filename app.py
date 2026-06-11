# pyrefly: ignore [missing-import]
import streamlit as st  
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.retriever import rag_pipeline

st.set_page_config(
    page_title="Sarkar Yojana Finder",
    page_icon="🇮🇳",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f7f8fa;
    }

    .hero {
        background: linear-gradient(135deg, #FF6B35, #FF9F1C, #138808);
        padding: 50px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }

    .hero h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    .form-card {
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .result-card {
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
        border-left: 5px solid #FF6B35;
    }

    .stats-bar {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }

    .stat-item {
        background: white;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        flex: 1;
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FF6B35;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #666;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #f0f0f0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #FF9F1C);
        color: white;
        border: none;
        padding: 12px 40px;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.9;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🇮🇳 Sarkar Yojana Finder</h1>
    <p>Discover government schemes you are eligible for — powered by AI</p>
    <p style="font-size:0.9rem; margin-top:8px;">4715+ Central & State Schemes Indexed</p>
</div>
""", unsafe_allow_html=True)

# Stats Bar
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">4715+</div>
        <div class="stat-label">Total Schemes</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">28+</div>
        <div class="stat-label">States Covered</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">15+</div>
        <div class="stat-label">Categories</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">Free</div>
        <div class="stat-label">No Login Needed</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Form
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Tell Us About Yourself</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=0, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    income = st.number_input("Annual Family Income (Rs)", min_value=0, value=150000, step=10000)
    caste = st.selectbox("Category", ["General", "SC", "ST", "OBC", "Minority"])

with col3:
    state = st.selectbox("State", [
        "All India", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
        "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
        "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
        "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
    ])
    occupation = st.selectbox("Occupation", [
        "Farmer", "Student", "Business Owner", "Unemployed",
        "Salaried", "Self Employed", "Artisan", "Daily Wage Worker", "Other"
    ])

extra = st.text_input(
    "Any specific need? (optional)",
    placeholder="e.g. housing loan, girl child education, health insurance, startup funding"
)

submitted = st.button("🔍 Find My Schemes")
st.markdown('</div>', unsafe_allow_html=True)

# Results
if submitted:
    query = f"""
    I am a {age} year old {gender} from {state}.
    My annual family income is Rs {income}.
    I belong to {caste} category.
    My occupation is {occupation}.
    {f'I am looking for: {extra}' if extra else ''}
    What government schemes am I eligible for?
    """

    with st.spinner("🔍 Searching 4715+ schemes for you..."):
        response = rag_pipeline(query)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ Schemes You May Be Eligible For</div>', unsafe_allow_html=True)
    st.markdown(response)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 Visit [MyScheme.gov.in](https://www.myscheme.gov.in) to apply for these schemes officially.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#999; font-size:0.85rem;'>Built with ❤️ for citizens of India | Data sourced from MyScheme.gov.in</p>",
    unsafe_allow_html=True
)