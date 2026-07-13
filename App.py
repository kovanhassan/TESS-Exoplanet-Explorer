import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import lightkurve as lk

# sets up the webpage
st.set_page_config(
    page_title="TESS Exoplanet Explorer",
    # watch the tutorial again if I forget how to do the page icons that appear on the top of the browser
    page_icon="🪐",
    layout="wide",
)

# title at the top
st.title("TESS Exoplanet Explorer Project")

# quick description
st.write(
    """
    This application uses public data from NASA's Transiting Exoplanet
    Survey Satellite (TESS) to explore light curves and search
    for possible periodic transit signals.
    """
)

# explains what a transit is
st.info(
    "A transit may occur when a planet passes in front of its star, "
    "causing a small temporary decrease in the star's brightness."
)

# everything on the left side
st.sidebar.header("Search Settings")

# user types in a target
target = st.sidebar.text_input(
    "Target name",
    value="TIC 261136679",
    #  adds the icon for extra help for a potential text to put for the target
    help="Examples: TIC 261136679, TOI 700, Kepler-10",
)

# choose how many sectors to download
maximum_sectors = st.sidebar.slider(
    "Maximum sectors to download",
    min_value=1,
    max_value=5,
    # autoset the inital value at 2 for now
    value=2,
)

# smallest period to check
minimum_period = st.sidebar.number_input(
    "Minimum period in days",
    min_value=0.2,
    max_value=50.0,
    value=0.5,
    step=0.1,
)

# biggest period to check
maximum_period = st.sidebar.number_input(
    "Maximum period in days",
    min_value=0.5,
    max_value=100.0,
    value=15.0,
    step=0.5,
)

# button starts the search
search_button = st.sidebar.button(
    "Search TESS Data",
    type="primary",
)

# combines the downloaded light curves and cleans them
def prepare_light_curve(light_curve_collection):

    combined_light_curve = light_curve_collection.stitch()

    # Remainder, check more tutorials later on to see if data can become even more cleaner
    cleaned_light_curve = (
        combined_light_curve
        .remove_nans()              # gets rid of missing values
        .remove_outliers(sigma=5)   # removes weird spikes
        .normalize()                # puts brightness on same scale
    )

    return cleaned_light_curve

# makes the first graph
def plot_light_curve(light_curve):

    figure, axis = plt.subplots(figsize=(11, 4))

    axis.scatter(
        light_curve.time.value,
        light_curve.flux.value,
        s=2,
    )

    axis.set_title("TESS Light Curve")
    axis.set_xlabel("Time (BTJD)")
    axis.set_ylabel("Normalized Brightness")
    # input grid for rest to make it more cleaner to see (do this later on REMAINDER)
    axis.grid(alpha=0.3)

    return figure

# looks for repeating dips
def find_possible_period(light_curve, min_period, max_period):

    flattened_light_curve = light_curve.flatten(window_length=401)

    periods = np.linspace(
        min_period,
        max_period,
        2000,
    )

    periodogram = flattened_light_curve.to_periodogram(
        method="bls",
        period=periods,
        duration=0.1,
    )

    strongest_period = periodogram.period_at_max_power

    return flattened_light_curve, periodogram, strongest_period

# graph of all the periods
def plot_periodogram(periodogram):

    figure, axis = plt.subplots(figsize=(11, 4))

    axis.plot(
        periodogram.period.value,
        periodogram.power.value,
    )

    axis.set_title("Box Least Squares Period Search")
    axis.set_xlabel("Possible Orbital Period (days)")
    axis.set_ylabel("Signal Power")
    axis.grid(alpha=0.3)

    return figure

# folds the graph using the best period
def plot_folded_light_curve(light_curve, period):

    folded_light_curve = light_curve.fold(period=period)

    figure, axis = plt.subplots(figsize=(11, 4))

    axis.scatter(
        folded_light_curve.phase.value,
        folded_light_curve.flux.value,
        s=3,
    )

    axis.set_title(
        f"Folded Light Curve — Period: {period.value:.4f} days"
    )
    axis.set_xlabel("Orbital Phase")
    axis.set_ylabel("Normalized Brightness")
    axis.grid(alpha=0.3)

    return figure

# only runs after button is pressed
if search_button:

    # make sure something was typed
    if not target.strip():
        st.error("Please enter a target name.")

    # don't let min be bigger than max
    elif minimum_period >= maximum_period:
        st.error(
            "The maximum period must be greater than the minimum period."
        )

    else:
        try:

            # search NASA for TESS data
            with st.spinner(f"Searching TESS observations for {target}..."):
                search_result = lk.search_lightcurve(
                    target,
                    mission="TESS",
                    author="SPOC",
                )

            # nothing found
            if len(search_result) == 0:
                st.warning(
                    "No TESS light curves were found for this target. "
                    
                )

            else:

                st.success(
                    f"Found {len(search_result)} available TESS light curves."
                )

                st.subheader("Almost All Available Observations (Might Trunucate Later to only show more important readings)")


                st.dataframe(
                    search_result.table.to_pandas(),
                    use_container_width=True,
                )



                # downloads the files
                with st.spinner("Downloading and preparing the data..."):
                    selected_results = search_result[:maximum_sectors]
                    collection = selected_results.download_all()

                #if for some reason no data is there, show error statement just incase
                if len(collection) == 0:
                    st.error("The light-curve files could not be downloaded.")

                else:



                    # clean everything up
                    light_curve = prepare_light_curve(collection)


                    st.subheader("1. Normalized TESS Light Curve")


                    light_curve_figure = plot_light_curve(light_curve)
                    st.pyplot(light_curve_figure)
                    plt.close(light_curve_figure)

                    # search for repeating p atterns
                    
                    
                    # loading thingy
                    with st.spinner("Searching for periodic signals..."):
                        (
                            flattened_light_curve,
                            periodogram,
                            strongest_period,
                        ) = find_possible_period(
                            light_curve,
                            minimum_period,
                            maximum_period,
                        )

                    st.subheader("2. Period Search")

                    metric_column_1, metric_column_2 = st.columns(2)

                    # shows best period found
                    metric_column_1.metric(
                        "Strongest Possible Period",
                        f"{strongest_period.value:.4f} days",
                    )

                    metric_column_2.metric(
                        "Downloaded Sectors",
                        len(collection),
                    )

                    periodogram_figure = plot_periodogram(periodogram)
                    st.pyplot(periodogram_figure)
                    plt.close(periodogram_figure)

                    st.subheader("3. Folded Light Curve")

                    folded_figure = plot_folded_light_curve(
                        flattened_light_curve,
                        strongest_period,
                    )

                    st.pyplot(folded_figure)
                    plt.close(folded_figure)

                    # reminder that this doesn't prove a planet
                    st.warning(
                        "Remain der: A strong periodic signal is not automatically proof "
                        "of an exoplanet. ..... (LATER ON ADD SUMMARIZING STATEMENTS FOR THE FINDINGS)"
                    )
        
        #showcase error statement just in case
        except Exception as error:
            st.error("The analysis could not be completed.")
            st.exception(error)

# shown before the actual search button is clicked
else:

    st.subheader("How to begin")

    st.write(
        """
        1. Enter a target in the sidebar.
        2. Select how many TESS sectors to download.
        3. Choose the range of orbital periods to investigate.
        4. Click **Search TESS Data**.
        """
    )
    # small caption to guide user on what to enter
    st.caption(
        "Suggested starting target: TIC 261136679"
    )