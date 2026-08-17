"""Runs a TESS search and renders every result section."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import lightkurve as lk
import streamlit.components.v1 as components

from analysis import prepare_light_curve, prepare_flattened_light_curve, search_for_planets
from nasa_eyes import find_supported_system
from plotting import plot_light_curve, plot_periodogram, plot_folded_light_curve


def run_search(
    target,
    maximum_sectors,
    minimum_period,
    maximum_period,
    window_length,
    number_of_planets,
):
    """Validate inputs, search TESS, and render every result section."""

    # quick sanity checks before we bother hitting tess's servers at all
    if not target.strip():
        st.error("Please enter a target name.")
        return

    if minimum_period >= maximum_period:
        st.error("The maximum period must be greater than the minimum period.")
        return

    
    try:
        search_result = _search_target(target)

        if len(search_result) == 0:
            st.warning("No TESS light curves were found for this target.")
            return

        st.success(f"Found {len(search_result)} available TESS light curves.")

        render_observation_table(search_result)
        render_nasa_eyes_section(target)

        st.divider()

        collection = _download_light_curves(search_result, maximum_sectors)

        if collection is None or len(collection) == 0:
            st.error("The light-curve files could not be downloaded.")
            return

        # this version is just cleaned, not flattened - good for the
        # "raw-ish" light curve plot, the search below flattens separately
        light_curve = prepare_light_curve(collection)

        render_light_curve_section(light_curve, collection)

        # this is where the actual bls search + all its plots happen,
        # collection (not light_curve) goes in because flattening needs
        # to happen per-sector before stitching, see analysis.py
        planet_results = render_planet_search_section(
            collection,
            minimum_period,
            maximum_period,
            window_length,
            number_of_planets,
        )

        render_interpretation_section(planet_results)

    except Exception as error:
        st.error("The analysis could not be completed.")
        st.exception(error)


def _search_target(target):
    # just asks tess what observations exist for this target, doesn't
    # actually download anything yet
    with st.spinner(f"Searching TESS observations for {target}..."):
        return lk.search_lightcurve(target, mission="TESS", author="SPOC")


def _download_light_curves(search_result, maximum_sectors):
    # this is the slow part...
    # only grab up to maximum_sectors of them, not everything available
    with st.spinner("Downloading and preparing the TESS data..."):
        selected_results = search_result[:maximum_sectors]
        return selected_results.download_all()


def render_observation_table(search_result):
    st.subheader("Available TESS Observations")

    st.write(
        """
        The table below shows the available TESS observations
        that were found for the selected target.
        """
    )

    st.dataframe(search_result.table.to_pandas(), use_container_width=True)


def render_nasa_eyes_section(target):
    """Shows the NASA Eyes viewer, only if the target is supported."""

    # nasa_eyes.py just does a name lookup, returns None if it's not
    # one of the handful of systems nasa eyes actually has a 3d model for
    selected_eyes_system = find_supported_system(target)

    # if the target isn't in the list, literally nothing happens here
    if selected_eyes_system is None:
        return

    st.divider()
    st.subheader("NASA Eyes on Exoplanets")

    nasa_eyes_url = (
        "https://eyes.nasa.gov/apps/exo/"
        f"#/system/{selected_eyes_system}"
    )

    st.write(
        f"""
        **{target}** is available in NASA Eyes on Exoplanets.

        The visualization below allows you to explore the
        planetary system in an interactive 3D environment.
        """
    )

    components.iframe(nasa_eyes_url, height=650, scrolling=True)

    # backup button in case the NASA doesn't display
    # properly inside the webpage
    st.link_button("Open NASA Eyes in New Tab", nasa_eyes_url)


def render_light_curve_section(light_curve, collection):
    st.subheader("1. Interactive Normalized TESS Light Curve")

    st.write(
        """
        Each point represents a brightness measurement
        recorded by TESS.

        Hover over a point to view the exact time and
        normalized brightness value.
        """
    )

    st.info(
        "Click and drag across part of the graph to zoom into "
        "a possible transit. Double-click the graph to return "
        "to the original view."
    )

    light_curve_figure = plot_light_curve(light_curve)

    st.plotly_chart(
        light_curve_figure,
        use_container_width=True,
        config={"scrollZoom": True, "displaylogo": False},
    )

    # some basic numbers laid out side by side under the graph
    column1, column2, column3 = st.columns(3)

    column1.metric("Number of Measurements", len(light_curve.time))
    column2.metric("Downloaded Sectors", len(collection))
    column3.metric("Average Brightness", f"{np.mean(light_curve.flux.value):.5f}")


def render_planet_search_section(
    collection,
    minimum_period,
    maximum_period,
    window_length,
    number_of_planets,
):
    """Flattens the light curve and searches it for one or more planets.

    After each planet is found, its transit points are masked out
    before searching the remaining data for another planet. Renders a
    periodogram and folded light curve for every planet found, plus a
    summary table, and returns the list of planet results.
    """

    st.divider()
    st.subheader("2. Search for Possible Orbital Periods")

    st.write(
        """
        The Box Least Squares algorithm searches the light
        curve for repeating box-shaped decreases in brightness.

        A strong peak may indicate a repeating transit signal. After a
        planet is found, its transit points are masked out and the
        remaining data is searched again for additional planets.
        """
    )

    with st.spinner("Flattening the light curve..."):
        flattened_light_curve = prepare_flattened_light_curve(collection, window_length)

    # search_for_planets finds the planets one at a time
# so we can show each result as soon as it's found instead of waiting for all of them
    planet_generator = search_for_planets(
        flattened_light_curve,
        minimum_period,
        maximum_period,
        number_of_planets,
    )

    planet_results = []
    stopped_early = False

    # this loop pulls one planet at a time out of the generator, showing
    # a fresh spinner + result for each round instead of one giant wait
    for planet_number in range(1, number_of_planets + 1):

        with st.spinner(
            f"Searching for planet {planet_number} of {number_of_planets}..."
        ):
            # next(..., None) instead of just next(...) so a finished
            # generator gives us None back instead of raising an error
            result = next(planet_generator, None)

        if result is None:
            stopped_early = True
            break

        planet_results.append(result)
        render_planet_result(result, collection)

    if not planet_results:
        st.warning(
            "No periodic signals could be found in this light curve."
        )
        return planet_results

    if stopped_early:
        st.caption(
            f"Stopped after {len(planet_results)} of {number_of_planets} "
            "requested planets - too few data points remained to keep "
            "searching."
        )

    render_planet_results_table(planet_results)

    return planet_results


def render_planet_result(result, collection):
    # unpack the dict search_for_planets yielded for this one planet
    planet_number = result["planet_number"]
    period = result["period"]
    duration = result["duration"]

    st.markdown(f"#### Planet {planet_number} candidate")

    metric_column_1, metric_column_2, metric_column_3 = st.columns(3)

    metric_column_1.metric("Possible Period", f"{period.value:.4f} days")
    metric_column_2.metric("Transit Duration", f"{duration.to_value('hour'):.2f} hours")
    metric_column_3.metric("Downloaded Sectors", len(collection))

    periodogram_figure = plot_periodogram(
        result["periodogram"],
        title=f"Planet {planet_number}: Box Least Squares Period Search",
    )
    st.pyplot(periodogram_figure)
    plt.close(periodogram_figure)

    folded_figure = plot_folded_light_curve(
        result["folded_light_curve"],
        period,
        title=f"Planet {planet_number}: Folded Light Curve — Period: {period.value:.4f} days",
    )
    st.pyplot(folded_figure)
    plt.close(folded_figure)

    st.caption(
        "Higher peaks represent periods where the BLS algorithm found "
        "stronger repeating transit-like signals."
    )

    st.divider()


def render_planet_results_table(planet_results):
    st.subheader("Detected Candidate Signals")

    results_table = pd.DataFrame(
        [
            {
                "Planet": f"Planet {result['planet_number']}",
                "Period (days)": round(float(result["period"].value), 3),
                "Transit duration (hours)": round(
                    float(result["duration"].to_value("hour")), 3
                ),
                # transit_time comes from an astropy Time object and its
                # .value can come back as a numpy MaskedArray, which the
                # built-in round() can't handle directly - float() first
                "Transit time (BTJD)": round(float(result["transit_time"].value), 3),
            }
            for result in planet_results
        ]
    )

    st.dataframe(results_table, use_container_width=True)

    st.caption(
        "Compare these periods with NASA's Exoplanet Archive "
        "(https://exoplanetarchive.ipac.caltech.edu/) to see how close "
        "this search came to the published values."
    )


def render_interpretation_section(planet_results):
    st.divider()
    st.subheader("Interpreting the Results")

    st.warning(
        "A strong periodic signal is not automatically proof "
        "of an exoplanet. Stellar activity, eclipsing binary "
        "stars, instrumental effects and other sources may "
        "also cause repeating changes in brightness."
    )

    if planet_results:
        period_summary = ", ".join(
            f"**{result['period'].value:.4f} days**" for result in planet_results
        )

        st.write(
            f"""
            **Result from this search**

            The Box Least Squares search identified {len(planet_results)}
            candidate signal(s) with orbital periods of approximately
            {period_summary}.

            Try estimating the period manually by zooming into
            the interactive graph and comparing nearby dips.
            """
        )
