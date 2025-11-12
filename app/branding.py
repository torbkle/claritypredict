import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError

# Logo path
LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo_brand.png"

# App-wide colors and styles
PRIMARY_COLOR = "#008080"       # Teal
SECONDARY_COLOR = "#003366"     # Navy
TEXT_COLOR = "#333333"
FONT_FAMILY = "sans-serif"

def show_logo():
    try:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=280)
        else:
            st.warning(f"⚠️ Logo not found at: {LOGO_PATH}")
            st.markdown("## ClarityPredict")
    except UnidentifiedImageError:
        st.warning("⚠️ Logo file could not be read. Please check the image format.")
        st.markdown("## ClarityPredict")

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
