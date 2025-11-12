import streamlit as st
from pathlib import Path

# Logo path
LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo_brand.png"

# App-wide colors and styles
PRIMARY_COLOR = "#008080"       # Teal
SECONDARY_COLOR = "#003366"     # Navy
TEXT_COLOR = "#333333"
FONT_FAMILY = "sans-serif"

def show_logo():
    st.image(str(LOGO_PATH), width=280)

def apply_custom_style():
    st.markdown(
        f"""
        <style>
        h1, h2, h3 {{
            color: {PRIMARY_COLOR};
            font-family: {FONT_FAMILY};
        }}
        .stApp {{
            background-color: #f9f9f9;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
