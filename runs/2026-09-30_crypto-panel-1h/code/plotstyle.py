# cellplot.py's validated palette, copied verbatim (DECISIONS D4: seaborn/plotly not pre-approved -> matplotlib only)
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
PAL = ["#2a78d6", "#008300", "#e87ba4", "#eda100", "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"]
SURFACE, TEXT, TEXT2, GRID, GRAY = "#fcfcfb", "#0b0b0b", "#52514e", "#e5e4e0", "#9b9a94"
DIV = ["#2a78d6", "#f0efec", "#e34948"]
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def setup():
    matplotlib.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "text.color": TEXT, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
        "axes.edgecolor": GRID, "grid.color": GRID, "grid.linewidth": 0.6, "axes.grid": True,
        "axes.spines.top": False, "axes.spines.right": False, "axes.prop_cycle": matplotlib.cycler(color=PAL),
        "axes.titlesize": 11, "axes.titleweight": "bold", "figure.dpi": 110, "lines.linewidth": 1.6, "font.size": 9})
def save(fig, name):
    p = os.path.join(RUN, "plots", name + ".png"); fig.savefig(p, bbox_inches="tight"); plt.close(fig); print("[plot]", p); return p
setup()
