import streamlit as st
from pathlib import Path

def show_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; font-size:14px; color:gray; margin-top:20px;">
            <p><strong>ClarityPredict©</strong> – Prototype for explainable biomarker prediction</p>
            <p>Developed by <strong>Torbjørn Kleiven</strong>, MSc AI/ML</p>
            <p>
                Moss / Oslo, Norway <br>
                <a href="mailto:tk@infera.no">tk@infera.no</a> | 
                <a href="https://github.com/torbkle" target="_blank">GitHub</a> | 
                <a href="https://github.com/torbkle/claritypredict/blob/main/LICENSE" target="_blank">📄 MIT License</a>
            </p>
            <p style="font-size:12px; color:darkgray;">
                © 2025 Torbjørn Kleiven – For demonstration and research purposes only.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
