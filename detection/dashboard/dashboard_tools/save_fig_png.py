from config import CONFIG
from flask import url_for
import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

def save_fig_png(fig, prefix="chart"):
    """Save a Matplotlib figure to a unique PNG under static/charts and return URL path."""
    filename = f"{prefix}.png"
    filepath = os.path.join(CONFIG['static_dir'], filename)
    fig.tight_layout()
    plt.savefig(filepath, format="png", dpi=120)
    plt.close(fig)
    plt.clf()
    return url_for("static", filename=f"charts/{filename}")