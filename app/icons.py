from pathlib import Path
import streamlit as st

def show_icon(icon_name: str, label: str = "", size: int = 24):
    icon_path = Path(__file__).parent / f"../assets/ico_{icon_name}.png"

    if icon_path.exists():
        icon_url = str(icon_path.resolve())
        st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
                <img src="data:image/png;base64,{_read_base64(icon_url)}" width="{size}" style="vertical-align: middle;">
                <span style="font-size: 18px; color: #4A90E2; font-weight: 600; vertical-align: middle;">
                    {label}
                </span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### {label} (missing icon: {icon_name})")

def _read_base64(path: str) -> str:
    import base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
