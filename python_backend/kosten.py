import pathlib

import seaborn
import matplotlib.pyplot as plt
import numpy as np
import datetime

ROOT_DIR = r""

rc = {
    'axes.axisbelow': False,
    'axes.edgecolor': 'lightgrey',
    'axes.labelcolor': 'dimgrey',
    'lines.solid_capstyle': 'round',
    'patch.force_edgecolor': True,
    'text.color': 'dimgrey',
    'xtick.color': 'dimgrey',
    'xtick.direction': 'out',
    'xtick.top': False,
    'ytick.color': 'dimgrey',
    'ytick.direction': 'out',
    'ytick.right': False,
    'figure.figsize': (8., 4.)}

COLOR_SET = ["#118ab2", "#ffd166", "#64B351", "#7F6AA7", "#D6BD62", "#BBDDAA"]

seaborn.set_theme(context="paper", font='Franklin Gothic Book', font_scale=1.2, style="whitegrid", palette=COLOR_SET,
                  rc=rc)


def plot_compare(title, x, all_y, all_y_names, colors=COLOR_SET, x_label="Years", y_label="Costs in €",
                 save=True, **kwargs):
    """
    Args:
        title (str): Title of the plot
        x (list): List of values for the x-axis
        all_y (list): List of lists containing the values for the y-axis
        all_y_names (list): List of strings for the names of the plots - same order as the list all_y
        colors (list or None): optional colors for the graphs passed in all_y
        x_label (str)
        y_label (str):
    """
    figure, axis = plt.subplots()

    # axis.set_yscale('log')  # sets the scale to be logarithmic with powers of 10

    for j, (y, y_name) in enumerate(zip(all_y, all_y_names)):
        axis.plot(y, marker='8', color=colors[j], markersize=2, label=y_name, linewidth=3)
    # for marker type see: https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
    # plot function: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
    # first arguments set y_value range , x is set to 0..N-1 for now

    plt.legend(loc="upper left")
    axis.set_xticks(range(0, len(x)))

    axis.set_axisbelow(True)

    axis.set_xticklabels(
        [str(f"${label}$") if i % 2 == 0 else "" for i, label in enumerate(x)])

    axis.set_facecolor('white')

    axis.set(xlabel=x_label, ylabel=y_label)
    axis.grid(True, color='lightgrey')
    axis.grid(False)

    plt.plot([kwargs["be"], kwargs["be"]], [all_y[0][-1], 0], linewidth=2, color="#ef476f", linestyle='dashed')
    plt.plot([25, 25], [all_y[0][-1], all_y[1][-1]], linewidth=4, color="#06d6a0")

    plt.text(x=kwargs["be"] + 1, y=all_y[0][1], s="Brake Even", color="#ef476f")
    plt.text(x=25 - 9, y=all_y[0][-1] - 3 * all_y[0][1],
             s=f"Advantage after 25y:\n {- 1 * (all_y[1][-1] - all_y[0][-1])}€", color="#06d6a0")

    if save:
        figure.savefig(
            str(pathlib.Path(ROOT_DIR) / f".{title}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_')}.png"),
            bbox_inches='tight', dpi=800)

    return plt


####################################################################################################

# qm ist halbe Dachfläche:
def kosten_normal(qm_full, jahre):
    k_nach_qm = (4500 * qm_full / 30) * 0.27
    return int(k_nach_qm * sum([1.02 ** x for x in range(jahre)]))


def kosten_solar(qm_full, jahre):
    anschaffung = 1000 + 275 * qm_full
    return int(
        anschaffung + sum([(4500 * qm_full / 30 - 100 * qm_full * 0.99 ** x) * 0.27 * 1.02 ** x for x in range(jahre)]))


#### HIER: #################

def plot_erstellen(qm):
    kn = [kosten_normal(qm, i) for i in range(0, 26)]
    ks = [kosten_solar(qm, i) for i in range(0, 26)]

    brake_even_i = int(np.where(np.array(kn) > np.array(ks))[0][0])
    al = ks[brake_even_i] - ks[brake_even_i - 1]
    be = kn[brake_even_i] - kn[brake_even_i - 1]
    brake_even = brake_even_i - 1 + (kn[brake_even_i - 1] - ks[brake_even_i - 1]) / (al - be)

    return plot_compare(title="Price comparison:", x=list(range(0, 26)), all_y=[kn, ks],
                        all_y_names=["Regular", "Solar"],
                        be=brake_even)


if __name__ == '__main__':
    plot_erstellen(100)
