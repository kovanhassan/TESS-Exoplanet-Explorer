"""Chart builders for the light-curve views."""

import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_light_curve(light_curve):
    """Interactive plotly view of the normalized light curve."""

    # plotly instead of matplotlib here since this is the one graph the
    # user actually zooms/hovers around on, matplotlib plots are static
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=light_curve.time.value,
            y=light_curve.flux.value,
            mode="markers",
            marker=dict(size=3),
            name="TESS Measurements",
            hovertemplate=(
                "Time: %{x:.5f} BTJD"
                "<br>Brightness: %{y:.6f}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title="Interactive TESS Light Curve",
        xaxis_title="Time (BTJD)",
        yaxis_title="Normalized Brightness",
        hovermode="closest",
        height=500,
    )

    figure.update_xaxes(showgrid=True)
    figure.update_yaxes(showgrid=True)

    return figure


def plot_periodogram(periodogram, title="Box Least Squares Period Search"):
    """Matplotlib view of BLS signal power vs. period."""

    # this is just power (how strong the signal is) plotted against every
    # period bls tried - a tall spike means that period fit the data well
    figure, axis = plt.subplots(figsize=(11, 4))

    axis.plot(periodogram.period.value, periodogram.power.value)

    axis.set_title(title)
    axis.set_xlabel("Possible Orbital Period (days)")
    axis.set_ylabel("Signal Power")
    axis.grid(alpha=0.3)

    return figure


def plot_folded_light_curve(folded_light_curve, period, title=None):
    """Matplotlib view of a light curve already folded on a period."""

    # title is optional here since results.py usually passes its own
    # (with the planet number in it) - only build a default if it didn't
    if title is None:
        title = f"Folded Light Curve — Period: {period.value:.4f} days"

    figure, axis = plt.subplots(figsize=(11, 4))

    # folding already happened in analysis.py, this just plots what it
    # handed back - phase is basically "where in the orbit" each point is
    axis.scatter(
        folded_light_curve.phase.value,
        folded_light_curve.flux.value,
        s=3,
    )

    axis.set_title(title)
    axis.set_xlabel("Orbital Phase")
    axis.set_ylabel("Normalized Brightness")
    axis.grid(alpha=0.3)

    return figure
