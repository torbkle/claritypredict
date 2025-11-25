import streamlit as st
from app.icons import show_icon
from scripts.generate_data import generate_synthetic_data
from app.profile import show_biomarker_profile

def show_demo_section():
    show_icon("search", "Test ClarityPredict instantly", size=32)

    st.markdown(
        """
This feature is designed for mobile users and others who don't have a CSV file ready.  
Click the button to test the app using pre-filled example data.
"""
    )

    # Knappen genererer data og lagrer i session_state
    if st.button("🔄 Load and run example data"):
        df = generate_synthetic_data(n_samples=10, seed=42)
        st.session_state.example_df = df
        st.success("✅ Example data loaded! Scroll down to see predictions.")

    # Hvis data finnes i session_state → vis tabell og profiler
    if "example_df" in st.session_state:
        df = st.session_state.example_df
        st.dataframe(df)

        st.markdown("---")
        show_icon("profile", "Demo patient profile", size=28)

        # Velg én pasient
        selected_idx = st.selectbox(
            "Select demo patient",
            options=range(len(df)),
            format_func=lambda i: f"Patient {i+1} (Age {df.iloc[i]['Age']}, {df.iloc[i]['Sex']})"
        )
        show_biomarker_profile(df.iloc[selected_idx])

        # --- Ny seksjon: sammenlign to pasienter ---
        st.markdown("---")
        show_icon("compare", "Compare two demo patients", size=28)

        col1, col2 = st.columns(2)

        with col1:
            idx1 = st.selectbox(
                "Select first patient",
                options=range(len(df)),
                format_func=lambda i: f"Patient {i+1} (Age {df.iloc[i]['Age']}, {df.iloc[i]['Sex']})",
                key="compare1"
            )
            show_biomarker_profile(df.iloc[idx1])

        with col2:
            idx2 = st.selectbox(
                "Select second patient",
                options=range(len(df)),
                format_func=lambda i: f"Patient {i+1} (Age {df.iloc[i]['Age']}, {df.iloc[i]['Sex']})",
                key="compare2"
            )
            show_biomarker_profile(df.iloc[idx2])
