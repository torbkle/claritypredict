import streamlit as st
from pathlib import Path

def show_footer():
    st.markdown("---")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.caption("Created by Torbjørn Kleiven --- 🔄 Versjon: 2025-11-13")


    with col2:
        st.markdown("[🌐 GitHub Repository](https://github.com/torbkle/claritypredict)")
        st.markdown("[📄 MIT License](https://github.com/torbkle/claritypredict/blob/main/LICENSE)")

    license_path = Path("LICENSE")
    if license_path.exists():
        with st.expander("📄 View MIT License"):
            st.code(license_path.read_text(), language="text")
