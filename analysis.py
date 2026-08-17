"""Light-curve data processing.

Cleans downloaded TESS light curves and searches them for repeating
transit-like signals using the Box Least Squares (BLS) method, one
planet at a time.
"""

import numpy as np

# how much extra time around the transit we remove before looking for another planet
# gonna increase this if the same planet keeps getting detected
MASK_WIDTH_FACTOR = 1.5

# how many different periods to test in each BLS search
# using too few can miss the actual period and cause the same planet to show up again
NUMBER_OF_PERIODS = 20000

# minimum number of data points left before we give up searching for
# another planet in the same light curve
MINIMUM_POINTS_REMAINING = 50


def prepare_light_curve(light_curve_collection):
    """Stitch and clean a collection of light curves for display.

    Cleaning happens per sector, before stitching - each TESS sector
    has its own independent systematics (pointing, background, etc.),
    so cleaning the already-stitched, multi-sector series instead would
    let one sector's quirks bleed into the others.
    """

    return light_curve_collection.stitch(
        corrector_func=lambda lc: lc.remove_nans().normalize().remove_outliers(sigma=5)
    )


def prepare_flattened_light_curve(light_curve_collection, window_length):
    """Stitch, clean, and flatten a collection of light curves for the
    period search.

    Flattening happens per sector, before stitching - just like the
    cleaning above. Running a Savitzky-Golay flattening window across a
    multi-sector, already-stitched series would let that window span
    the time gaps between sectors, which can distort or wash out real
    transit signals right at the sector boundaries.
    """

    return light_curve_collection.stitch(
        corrector_func=lambda lc: (
            lc.remove_nans()
            .normalize()
            .flatten(window_length=window_length)
            .remove_outliers(sigma=5)
        )
    )


def search_for_planets(light_curve, min_period, max_period, number_of_planets):
    """Iteratively search a flattened light curve for periodic signals.

    After each planet is found, its transit points are masked out and
    the search repeats on the remaining data, up to ``number_of_planets``
    times. The search stops early if too few points remain.

    This is a generator: each planet's result (a dict with its period,
    duration, transit time, periodogram, and folded light curve) is
    yielded as soon as that round finishes, instead of only returning
    everything at once after the full search completes. That lets the
    caller show a result immediately after each planet is found rather
    than one long, silent wait for all of them.
    """

    # this is just the list of candidate periods (in days) that bls will
    # try one by one to see which fits the data best
    periods = np.linspace(min_period, max_period, NUMBER_OF_PERIODS)

    # this variable gets smaller each loop as we mask out planets we
    # already found, so the next search only looks at leftover data
    remaining_light_curve = light_curve

    for planet_number in range(1, number_of_planets + 1):

        # ran out of usable data points, no point trying to search more
        if len(remaining_light_curve) < MINIMUM_POINTS_REMAINING:
            break

        # duration is left unset here so lightkurve picks it - passing
        # an explicit range of durations multiplies the search cost by
        # however many values are tested
        periodogram = remaining_light_curve.to_periodogram(
            method="bls",
            period=periods,
        )

        # grab whatever period/duration/time gave the strongest signal
        best_period = periodogram.period_at_max_power
        best_duration = periodogram.duration_at_max_power
        best_transit_time = periodogram.transit_time_at_max_power

        # fold = stack every orbit on top of each other using that period,
        # so if it's a real transit you'll see a dip repeat at the same spot
        folded_light_curve = remaining_light_curve.fold(
            period=best_period,
            epoch_time=best_transit_time,
        )

        # send this planet's info back to whoever called this function
        yield {
            "planet_number": planet_number,
            "period": best_period,
            "duration": best_duration,
            "transit_time": best_transit_time,
            "periodogram": periodogram,
            "folded_light_curve": folded_light_curve,
        }

# remove the points from this transit so the next search
# can look for a different planet instead of finding the same one again
        transit_mask = periodogram.get_transit_mask(
            period=best_period,
            transit_time=best_transit_time,
            duration=best_duration * MASK_WIDTH_FACTOR,
        )

        remaining_light_curve = remaining_light_curve[~transit_mask]
