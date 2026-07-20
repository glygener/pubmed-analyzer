from pathlib import Path
import streamlit as st

about_file = Path(__file__).parent.parent / "ANALYSIS.md"
st.markdown(about_file.read_text(encoding="utf-8"))
