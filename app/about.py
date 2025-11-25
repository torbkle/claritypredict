import streamlit as st

def show_about():
    st.markdown("---")
    st.markdown('<a id="info"></a>', unsafe_allow_html=True)

    # English section
    st.header("🇬🇧 ClarityPredict© – English Overview")
    st.write("""
    **ClarityPredict©** is a prototype designed for explainable biomarker prediction.  
    It integrates advanced machine learning with clear, interactive visualizations to support clinicians, researchers, 
    and health-tech innovators in interpreting complex patient data.

    **Key Features:**
    - **Data Exploration**: Upload or generate biomarker datasets and explore distributions, correlations, and summary statistics.
    - **Predictive Modeling**: Apply logistic regression or random forest models with transparent performance metrics (ROC, precision-recall, confusion matrix).
    - **Explainability**: Analyze individual predictions using SHAP force plots, beeswarm plots, and dependence plots to understand biomarker impact.
    - **Patient-Level Insights**: Compare biomarker profiles across patients and highlight clinically relevant differences.
    - **Accessibility**: Built to bridge the gap between complex algorithms and practical decision-making, ensuring trustworthy and user-friendly analytics.

    **Disclaimer:**  
    ClarityPredict© is not a diagnostic tool. It is a demonstration of how explainable AI can enhance 
    decision-making in healthcare and research.
    """)

    # Norwegian section
    st.header("🇳🇴 ClarityPredict© – Norsk oversikt")
    st.write("""
    **ClarityPredict©** er en prototype utviklet for forklarbar biomarkørprediksjon.  
    Løsningen kombinerer avansert maskinlæring med tydelige, interaktive visualiseringer for å støtte klinikere, forskere 
    og helse-teknologiutviklere i å tolke komplekse pasientdata.

    **Hovedfunksjoner:**
    - **Datautforskning**: Last opp eller generer biomarkørdatasett og analyser fordelinger, korrelasjoner og oppsummerende statistikk.
    - **Prediktiv modellering**: Kjør logistisk regresjon eller random forest-modeller med transparente ytelsesmål (ROC, precision-recall, confusion matrix).
    - **Forklarbarhet**: Undersøk individuelle prediksjoner med SHAP force plots, beeswarm plots og dependence plots for å forstå biomarkørenes innflytelse.
    - **Pasientnivå-innsikt**: Sammenlign biomarkørprofiler mellom pasienter og fremhev klinisk viktige forskjeller.
    - **Tilgjengelighet**: Utviklet for å bygge bro mellom avanserte algoritmer og praktiske beslutninger, slik at analysene blir pålitelige og enkle å bruke.

    **Ansvarsfraskrivelse:**  
    ClarityPredict© er ikke et diagnostisk verktøy. Det er en demonstrasjon av hvordan forklarbar AI kan støtte 
    beslutningstaking i helsevesen og forskning.
    """)
