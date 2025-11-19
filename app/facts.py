import streamlit as st
import random

def show_random_fact():
    facts = [
        "CRP is a marker of inflammation and can rise dramatically during infection or trauma.",
        "Albumin levels can reflect nutritional status and liver function.",
        "Creatinine is a waste product filtered by the kidneys – high levels may indicate impaired kidney function.",
        "BMI is a simple measure of body fat based on height and weight.",
        "Low albumin levels are often seen in chronic illness or malnutrition.",
        "CRP levels can increase up to 1000-fold during acute inflammation.",
        "Creatinine clearance is used to estimate glomerular filtration rate (GFR).",
        "BMI does not distinguish between muscle and fat mass – athletes may have high BMI but low fat.",
        "CRP is often used to monitor treatment response in infections and autoimmune diseases.",
        "Albumin helps maintain oncotic pressure and transport hormones, vitamins, and drugs."
    ]
    st.info(random.choice(facts))
