"""Sidebar controls for search settings."""

from dataclasses import dataclass

import streamlit as st


# just a little container to carry every sidebar value back to app.py
# in one object instead of returning a big tuple
@dataclass
class SearchSettings:
    target: str
    maximum_sectors: int
    minimum_period: float
    maximum_period: float
    window_length: int
    number_of_planets: int
    search_button: bool


def render_sidebar():
    """Render the sidebar and return the chosen search settings."""

    st.sidebar.header("Search Settings")

   
    target = st.sidebar.text_input(
        "Target name",
        value="TIC 261136679",
        help="Examples: TIC 261136679, Kepler-4, Kepler-10, TOI 700",
    )

    # how many tess sectors to pull down - more sectors = more data =
    # longer download, so keep the max reasonable
    maximum_sectors = st.sidebar.slider(
        "Maximum sectors to download",
        min_value=1,
        max_value=15,
        value=5,
        help="More sectors means more data and a cleaner signal, but a slower download.",
    )

    # the period search only looks between these two values, in days
    minimum_period = st.sidebar.number_input(
        "Minimum period in days",
        min_value=0.2,
        max_value=50.0,
        value=0.5,
        step=0.1,
    )

    maximum_period = st.sidebar.number_input(
        "Maximum period in days",
        min_value=0.5,
        max_value=100.0,
        value=50.0,
        step=0.5,
        help="Widen this to catch longer-period planets - narrowing it will miss them entirely.",
    )

    # how wide the smoothing window is when flattening out the light
    # curve before searching - bigger number = smoother but can also
    # blur out real transits if it's too big
    window_length = st.sidebar.select_slider(
        "Flattening window length",
        options=[101, 201, 301, 401, 501, 701, 1001, 1301, 1501],
        value=401,
        help=(
            "Controls how much smoothing is applied when removing "
            "long-term trends before the period search. A small window "
            "removes more variation but may distort transits; a large "
            "window preserves transit shape but removes fewer trends. "
            "Try 301, 501, 1001, or 1501."
        ),
    )

    # how many separate planets to look for one after another
    number_of_planets = st.sidebar.slider(
        "Number of planets to search for",
        min_value=1,
        max_value=4,
        value=1,
        help=(
            "After each planet is found, its transit points are masked "
            "out before searching the remaining data for another planet."
        ),
    )

    # nothing actually happens until this gets clicked
    search_button = st.sidebar.button("Search TESS Data", type="primary")

    # just a little reference list at the bottom, not tied to any input
    st.sidebar.markdown("---")

    st.sidebar.write("**NASA Eyes supported targets:**")

    st.sidebar.write(
        """
        • Kepler-4  
        • Kepler-10  
        • TRAPPIST-1  
        • TOI 700
        """
    )

    return SearchSettings(
        target=target,
        maximum_sectors=maximum_sectors,
        minimum_period=minimum_period,
        maximum_period=maximum_period,
        window_length=window_length,
        number_of_planets=number_of_planets,
        search_button=search_button,
    )
