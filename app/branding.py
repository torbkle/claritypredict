import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError

# --- Fargepalett ---
PRIMARY_COLOR = "#4A90E2"       # Branding-blå
SECONDARY_COLOR = "#7FB3D5"     # Lysere blå
ACCENT_COLOR = "#AED6F1"        # Pastellblå
TEXT_COLOR = "#2C3E50"          # Mørk gråblå
BACKGROUND_COLOR = "#F9F9F9"    # Lys bakgrunn

# --- Fontvalg ---
FONT_FAMILY = "Inter, sans-serif"

# --- CSS-injeksjon ---
def apply_custom_style():
    st.markdown(f"""
        <style>
            html, body {{
                background-color: {BACKGROUND_COLOR};
                font-family: {FONT_FAMILY};
                color: {TEXT_COLOR};
            }}
            h1 {{
                color: {PRIMARY_COLOR};
                font-size: 1.6rem;
            }}
            h2 {{
                color: {TEXT_COLOR};
                font-size: 1.3rem;
                font-weight: 600;
            }}
            h3 {{
                color: {PRIMARY_COLOR};
                font-size: 1.1rem;
                font-weight: 500;
            }}
            .stButton>button {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 6px;
                padding: 0.5em 1em;
            }}
            .stDownloadButton>button {{
                background-color: {SECONDARY_COLOR};
                color: white;
                border-radius: 6px;
            }}
            .metric {{
                color: {TEXT_COLOR};
            }}
        </style>
    """, unsafe_allow_html=True)

# --- Logo-visning ---
def show_logo():
    logo_path = Path(__file__).parent / "../assets/logo_101.png"
    st.markdown("<div style='text-align: center; margin-bottom: 0px;'>", unsafe_allow_html=True)
    st.image(logo_path.resolve(), width=150)
    st.markdown(
        f"""
        <h2 style='margin-top: 4px; margin-bottom: 6px;'>
        Welcome to ClarityPredict – a prototype for explainable biomarker prediction
        </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Stilfunksjoner ---
def styled_header(text, level=3):
    tag = f"h{level}"
    color = TEXT_COLOR if level == 2 else PRIMARY_COLOR
    st.markdown(f"<{tag} style='color:{color};'>{text}</{tag}>", unsafe_allow_html=True)

def styled_table(df):
    st.markdown("""
        <style>
            thead {background-color: #4A90E2; color: white;}
            td {padding: 8px;}
        </style>
    """, unsafe_allow_html=True)
    st.dataframe(df)
