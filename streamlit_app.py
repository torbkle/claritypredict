import streamlit as st
from app.icons import show_icon
from app.footer import show_footer
from app.upload import upload_data
from app.prediction import run_prediction
from app.branding import show_logo, apply_custom_style
import matplotlib.pyplot as plt
from app.facts import show_random_fact
from app.components import show_biomarker_profile, compare_profiles
from scripts.generate_data import generate_synthetic_data
from app.explore import explore_data

# Toggle for midlertidige og eksperimentelle seksjoner
dev_mode = True

# Init state
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# Eksempeldata-funksjon
def load_example_data():
    df = generate_synthetic_data(n_samples=100, seed=42)
    st.session_state.example_df = df
    st.session_state.hide_info = True   # 👈 Skjul info-seksjonen
    st.success("✅ Example data loaded! Scroll down to see predictions.")

    # Vis data
    show_icon("search", "Preview of synthetic biomarker data", size=32)
    st.dataframe(df)

    # Nedlastbar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download example data as CSV", data=csv, file_name="example_data.csv", mime="text/csv")


# App config
st.set_page_config(page_title="ClarityPredict", layout="centered")

# Header med logo og info-knapp
apply_custom_style()
show_logo()


# Legg til knapp til høyre
col1, col2 = st.columns([3,1])
with col2:
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 6px;
            background-color: #f0f4f8;
            color: #0066cc;
        }
        div.stButton > button:first-child:hover {
            background-color: #e6f0ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button("ℹ️ What is ClarityPredict"):
        st.session_state.show_info = True
        # Scroll til info-seksjonen
        st.markdown(
            """
            <script>
            window.location.href = "#info";
            </script>
            """,
            unsafe_allow_html=True
        )


# --- Mobilvennlig testseksjon ---
if dev_mode:
    show_icon("search", "Test ClarityPredict instantly", size=32)

    st.markdown(
        """
This feature is designed for mobile users and others who don't have a CSV file ready.  
Click the button to test the app using pre-filled example data.
"""
    )

    if st.button("🔄 Load and run example data"):
        load_example_data()

# --- Filopplasting og prediksjon ---
df = upload_data()

# Bruk eksempeldata hvis tilgjengelig
if "example_df" in st.session_state:
    df = st.session_state.example_df

if df is not None:
    explore_data(df)  # 👈 Ny seksjon for datautforskning
    show_icon("chart", "Data is ready for prediction module", size=28)
    run_prediction(df)

    if dev_mode:
        # --- Informativ oversikt ---
        st.markdown("---")
        show_icon("chart", "Biomarker overview", size=28)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg CRP", f"{df['CRP'].mean():.2f} mg/L")
        col2.metric("Avg Cystatin C", f"{df['Cystatin_C'].mean():.2f} mg/L")
        col3.metric("Avg Creatinine", f"{df['Creatinine'].mean():.1f} µmol/L")
        col4.metric("Avg eGFR", f"{df['eGFR'].mean():.1f} mL/min")

        # Histogram for CRP
        st.markdown("---")
        show_icon("chart", " CRP Distribution", size=28)
        fig, ax = plt.subplots()
        df["CRP"].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
        ax.set_title("CRP Histogram")
        ax.set_xlabel("CRP value (mg/L)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # --- Sammenlign to rader ---
        st.markdown("---")
        show_icon("search", "Compare two cases", size=28)
        idx1 = st.number_input("Select first row", min_value=0, max_value=len(df) - 1, value=0)
        idx2 = st.number_input("Select second row", min_value=0, max_value=len(df) - 1, value=1)
        compare_profiles(df.iloc[idx1], df.iloc[idx2])

        # --- Biomarkørprofil ---
        st.markdown("---")
        show_icon("profile", "Explore individual biomarker profile", size=28)
        selected_idx = st.number_input("Select a case to inspect", min_value=0, max_value=len(df)-1, value=0)
        show_biomarker_profile(df.iloc[selected_idx])
        compare_profiles(df.iloc[idx1], df.iloc[idx2])

        # --- Fakta ---
        st.markdown("---")
        show_icon("bulb", " Did you know?", size=28)
        show_random_fact()

# --- Info-seksjon ---
if st.session_state.get("show_info", False):
    st.markdown("---")
    # Sett ID/anker for scroll
    st.markdown('<a id="info"></a>', unsafe_allow_html=True)

    st.header("What is ClarityPredict?")
    st.write("""
ClarityPredict© is a prototype for explainable biomarker prediction. 
It combines advanced machine learning with clear, interactive visualizations to help clinicians, researchers, 
and health-tech innovators make sense of complex patient data.

Key features include:
- **Data exploration**: Upload or generate biomarker datasets and instantly explore distributions, correlations, and summary statistics.
- **Predictive modeling**: Run logistic regression or random forest models with transparent performance metrics (ROC, precision-recall, confusion matrix).
- **Explainability**: Inspect individual predictions with SHAP force plots, beeswarm plots, and dependence plots to understand how biomarkers influence outcomes.
- **Patient-level insights**: Compare biomarker profiles across patients and highlight key differences in clinical markers.
- **Accessibility**: Designed to bridge the gap between complex algorithms and practical decision-making, making advanced analytics trustworthy and easy to use.

ClarityPredict© is not a diagnostic tool, but a demonstration of how explainable AI can support 
decision-making in healthcare and research.
""")

    st.write("👉 [Les på norsk](#norsk)")
    st.header("Hva er ClarityPredict?")
    st.write("""
Jeg har valgt å kalle produktet ClarityPredict© fordi navnet uttrykker kjernen i det jeg ønsker å oppnå: klarhet 
i komplekse data og tydelige prediksjoner som kan forklares. Clarity står for innsikt og transparens – at resultatene 
ikke bare skal være tall, men forståelige forklaringer. Predict viser at løsningen handler om å forutsi utfall basert 
på biomarkører. Sammen gir navnet et løfte om både presisjon og forklarbarhet: en prediksjon som kan stoles på fordi den 
kan forklares.

ClarityPredict© er en prototype for forklarbar biomarkørprediksjon. 
Den kombinerer avansert maskinlæring med tydelige, interaktive visualiseringer for å hjelpe klinikere, forskere 
og helse-teknologiutviklere med å forstå komplekse pasientdata.

Hovedfunksjoner:
- **Datautforskning**: Last opp eller generer biomarkørdatasett og utforsk fordelinger, korrelasjoner og oppsummerende statistikk.
- **Prediktiv modellering**: Kjør logistisk regresjon eller random forest-modeller med transparente ytelsesmål (ROC, precision-recall, confusion matrix).
- **Forklarbarhet**: Undersøk individuelle prediksjoner med SHAP force plots, beeswarm plots og dependence plots for å forstå hvordan biomarkører påvirker resultatene.
- **Pasientnivå-innsikt**: Sammenlign biomarkørprofiler mellom pasienter og fremhev viktige forskjeller i kliniske markører.
- **Tilgjengelighet**: Bygget for å bygge bro mellom komplekse algoritmer og praktiske beslutninger, slik at avansert analyse blir pålitelig og enkel å bruke.

ClarityPredict© er ikke et diagnostisk verktøy, men en demonstrasjon av hvordan forklarbar AI kan støtte 
beslutningstaking i helsevesen og forskning.
""")

    # Reset-knapp med scroll til toppen
    if st.button("Hide info"):
        st.session_state.show_info = False
        st.markdown(
            """
            <script>
            window.scrollTo({top: 0, behavior: 'smooth'});
            </script>
            """,
            unsafe_allow_html=True
        )
# --- Footer ---
show_footer()


