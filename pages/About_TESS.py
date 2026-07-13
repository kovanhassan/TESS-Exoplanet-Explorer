import streamlit as st

# setup for this page
st.set_page_config(
    page_title="About TESS",
    page_icon="🛰️",
    layout="wide",
)

st.title("About TESS")

st.write(
    """
    TESS stands for the Transiting Exoplanet Survey Satellite.
    It observes stars and records how their brightness changes
    over time.
    """
)

st.subheader("What Is a Light Curve?")

st.write(
    """
    A light curve is a graph showing the brightness of a star
    over time.
    """
)

st.subheader("What Is a Transit?")

st.write(
    """
    A transit can happen when a planet passes between its star
    and the observer. The planet blocks a small amount of the
    star's light, causing a dip in the light curve.
    """
)

st.subheader("Why Look for Repeating Dips?")

st.write(
    """
    A planet orbiting a star may pass in front of it repeatedly.
    The time between these dips can give an estimate of the
    planet's orbital period.
    """
)

st.info(
    "Not every brightness dip is caused by an exoplanet, so more "
    "analysis is needed before a candidate can be confirmed."
)

st.subheader("Step 3 - What are TESS Sectors?")

st.write("""
TESS does not observe the entire sky at once.

Instead, it divides the sky into large sections called **sectors**.
Each sector is observed for about **27 days** before the satellite moves to
the next part of the sky.

A star may be observed in multiple sectors over the mission.
Each sector provides another set of light-curve data for that same star.
""")

st.subheader("Step 4 - Maximum Sectors to Download")

st.write("""
The slider lets the user choose how many available sectors should be downloaded.

For example:

• 1 sector = about 27 days of observations

• 2 sectors = about 54 days of observations

• 4 sectors = about 108 days of observations

Downloading more sectors provides more data and makes it easier to detect
repeating transit signals, but with more data, it could increase download time for users on smaller tech computers.
""")