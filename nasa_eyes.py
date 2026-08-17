"""NASA Eyes on Exoplanets support.

Keeps track of which targets have a matching interactive 3D system in
NASA's "Eyes on Exoplanets" viewer, and finds the NASA Eyes name for a
given target if one exists.
"""

# NASA Eyes systems that I am supporting for now (would be kinda hard to implement for each one for now)
# can add more later
# left side is the target name a user might type into the app, right
# side is the exact name NASA Eyes uses in its own url - they're not
# always spelled the same (see TOI 700 vs TOI-700 below)
NASA_EYES_SYSTEMS = {
    "Kepler-4": "Kepler-4",
    "Kepler-10": "Kepler-10",
    "TRAPPIST-1": "TRAPPIST-1",
    "TOI 700": "TOI-700",
}


def find_supported_system(target):
    """Return the NASA Eyes system name for a target, or None."""

    # compare without caring about capitalization
    for available_target, nasa_name in NASA_EYES_SYSTEMS.items():
        if target.strip().lower() == available_target.lower():
            return nasa_name

    # if the target isn't in the list, literally nothing happens here
    return None
