import streamlit as st

st.title("Example Targets")

st.write(
    """
    Here are some example targets that work well with this application.
    """
)

st.table({
    "Target": [
        "TIC 261136679",
        "TOI 700",
        "Kepler-10",
        "Pi Mensae",
        "WASP-18"
    ],
    "Reason": [
        "Default example",
        "Known exoplanet system",
        "First rocky exoplanet discovered by Kepler",
        "Bright nearby star with a planet",
        "Large hot Jupiter"
    ]
})

st.info("The user could potentially copy one of the target names and paste it into the search box on the main page.")