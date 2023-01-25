import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import AutoMinorLocator

matplotlib.use("Qt5Agg")


def create_chart(selected_sku, bottle_data):
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(8.5, 7))

    # Removing Grid from Background
    ax.grid(False)

    # Adding the minor Ticks on Y-axis
    ax.minorticks_on()
    ax.tick_params(which="minor", length=15, zorder=10, color='white', tickdir='inout')
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator(n=2))

    time_intervals = ["09:30", "10:00", "10:30", "11:00", "11:30"]

    good_count_array = []
    bad_count_array = []

    for time in time_intervals:
        good_count_array.append(bottle_data[selected_sku][time]["Good"])
        bad_count_array.append(bottle_data[selected_sku][time]["Bad"])

    # Normalizing the good and bad count array to 100% proportion
    total = len(good_count_array) + len(bad_count_array)
    good_proportion = np.true_divide(good_count_array, total) * 100
    bad_proportion = np.true_divide(bad_count_array, total) * 100

    # Setting the labels
    ax.set_ylabel('Percentage', fontdict=dict(weight='bold', size=12))
    ax.set_xlabel('Time', fontdict=dict(weight='bold', size=12))

    # Formatting the Spines and ticks of the chart according to the requirements
    ax.spines['bottom'].set_linewidth(18)
    ax.spines['left'].set_linewidth(18)

    ax.spines['left'].set_bounds(-2.8, 100)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))

    ax.spines['bottom'].set_zorder(1)
    ax.spines['left'].set_zorder(1)

    ax.tick_params(length=15, zorder=10, color='white', tickdir='inout', pad=10)

    # Labeling the X-axis ticks
    r = range(len(time_intervals))
    plt.xticks(r, time_intervals)

    # Plotting the stacked bar graph with the Good and Bad Data
    ax.bar(r, bad_proportion, bottom=good_proportion, color="#f28d3f", width=0.5, label='Bad')
    ax.bar(r, good_proportion, color="#4bbf65", label='Good', width=0.5)

    # Creating and Fixing the Legend on top right corner
    legend = ax.legend(title=f"Legend - SKU {selected_sku}", ncol=1, bbox_to_anchor=(1, 1), loc='upper right',
                       bbox_transform=plt.gcf().transFigure,
                       frameon=True,
                       edgecolor='black', facecolor='lightgrey', markerfirst=True, fontsize=10, markerscale=2,
                       handlelength=1, borderpad=1)

    title = legend.get_title()
    title.set_size(10)
    title.set_weight("bold")

    plt.tight_layout()

    return fig.canvas
