import streamlit as st

# setup for this page
st.set_page_config(
    page_title="About the Project",
    page_icon="🪐",
    layout="wide",
)

st.title("About the Project")

st.write(
    """
    This project uses public TESS data to explore the brightness
    of stars and search for possible repeating transit signals.
    """
)

st.subheader("Project Goal")

st.write(
    """
    The goal is to make a app where a user can enter
    a star or TESS target and see its light curve data.
    """
)

st.subheader("Tools Used")

st.write(
    """
    - Python
    - Lightkurve
    - Streamlit
    - NumPy
    - Matplotlib
    """
)

st.warning(
    "This tool only finds possible transit signals. "
    "It cannot confirm that an exoplanet exists."
)