import streamlit as st

# setup for this page
st.set_page_config(
    page_title="How It Works",
    page_icon="🔎",
    layout="wide",
)

st.title("How the App Works")

st.write(
    """
    The app goes through a few steps to search TESS data.
    """
)

st.subheader("Step 1: Enter a Target")

st.write(
    """
    The user enters the name or ID of a star, such as
    TIC 261136679 or TOI 700.
    """
)

st.subheader("Step 2: Search for Observations")

st.write(
    """
    Lightkurve searches for available TESS light curves
    for the entered target.
    """
)

st.subheader("Step 3: Clean the Data")

st.write(
    """
    Missing values and large outliers are removed. The brightness
    values are also normalized so the graph is potentially easier to read.
    """
)

st.subheader("Step 4: Search for Repeating Dips")

st.write(
    """
    The Box Least Squares method checks different possible periods
    to look for repeating drops in brightness.
    """
)

st.subheader("Step 5: Show the Results")

st.write(
    """
    The app displays the normal light curve, the period search,
    and the folded light curve.
    """
)

st.info(
    "A repeating dip could be caused by a planet, but it could also "
    "come from stellar activity, another star, or measurement noise."
)