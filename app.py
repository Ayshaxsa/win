import streamlit as st

st.title("Hand Volume Control - Cloud Demo")

st.write(
    """
    Full hand tracking and system volume control works locally on Windows
    using `hand_volume.py`.  
    Streamlit Cloud cannot access your webcam, so this demo only shows info.
    """
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Hand_icon.svg/480px-Hand_icon.svg.png", caption="Demo Placeholder")
