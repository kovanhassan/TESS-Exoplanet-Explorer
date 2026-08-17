"""TESS Exoplanet Explorer - Streamlit entry point."""

import streamlit as st

# these are my own helper files, not external libraries
# sidebar.py builds the left-hand controls, results.py does the actual
# search + shows the plots and tables
from sidebar import render_sidebar
from results import run_search


# sets up the webpage (title in the browser tab, the little planet icon,
# and wide layout so the plots have room to breathe)
st.set_page_config(
    page_title="TESS Exoplanet Explorer",
    page_icon="🪐",
    layout="wide",
)

st.title("TESS Exoplanet Explorer Project")

st.write(
    """
    This application uses public data from NASA's Transiting Exoplanet
    Survey Satellite (TESS) to explore light curves and search
    for possible periodic transit signals.
    """
)

st.info(
    "A transit may occur when a planet passes in front of its star, "
    "causing a small temporary decrease in the star's brightness."
)

# this draws all the sidebar widgets 
settings = render_sidebar()



# main program
# ONLY starts to run after button is clicked

# streamlit will just rerun this whole script top to bottom every time something
# changes, so this if/else is basically "did they just click search"
if settings.search_button:
    # hand everything off to results.py, that's where the real work happens
    run_search(
        settings.target,
        settings.maximum_sectors,
        settings.minimum_period,
        settings.maximum_period,
        settings.window_length,
        settings.number_of_planets,
    )

else:
    # nothing searched yet, so just show quick bit of instructions instead
    st.subheader("How to begin")

    st.write(
        """
        1. Enter a target in the sidebar.

        2. Select how many TESS sectors to download.

        3. Choose the range of orbital periods to investigate.

        4. Click **Search TESS Data**.
        """
    )

    st.caption("Suggested starting target: TIC 261136679")
