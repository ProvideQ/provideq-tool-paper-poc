import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Load data
df = pd.read_csv("results_vrp.csv")

# Solvers
solver_dwave = "2-Phase with D-Wave"
solver_lkh = "2-Phase with LKH-3"
reference_solvers = [
    "Optimal Solution (with Clustering)",
    "Optimal Solution (without Clustering)"
]

# Filter data
df_dwave = df[df["Solvername"] == solver_dwave]
df_lkh = df[df["Solvername"] == solver_lkh]

# Prepare problem names (without .vrp)
df["Problemname_clean"] = df["Problemname"].str.replace(".vrp", "", regex=False)
df_dwave["Problemname_clean"] = df_dwave["Problemname"].str.replace(".vrp", "", regex=False)
df_lkh["Problemname_clean"] = df_lkh["Problemname"].str.replace(".vrp", "", regex=False)

problem_order = sorted(df["Problemname_clean"].unique())
x_base = np.arange(len(problem_order))

# Colorblind-friendly colors (Okabe-Ito palette)
color_dwave = "#56B4E9"    # sky blue
color_lkh = "#E69F00"      # orange
color_opt1 = "#D55E00"     # vermillion
color_opt2 = "black"

# Plot setup
plt.figure(figsize=(14, 3.3))
sns.set(style="whitegrid")

# --- Boxplot for D-Wave (right) ---
for i, problem in enumerate(problem_order):
    data = df_dwave[df_dwave["Problemname_clean"] == problem]["Solution (Kilometer)"]
    if not data.empty:
        plt.boxplot(
            data,
            positions=[x_base[i] + 0.25],
            widths=0.2,
            patch_artist=True,
            boxprops=dict(facecolor=color_dwave, color="gray"),
            medianprops=dict(color="black"),
            whiskerprops=dict(color="gray"),
            capprops=dict(color="gray"),
            flierprops=dict(marker='o', color='gray', alpha=0.2)
        )

# --- Scatter for LKH-3 (left) ---
for i, problem in enumerate(problem_order):
    data = df_lkh[df_lkh["Problemname_clean"] == problem]["Solution (Kilometer)"]
    if not data.empty:
        x_vals = np.random.normal(loc=x_base[i] - 0.25, scale=0.02, size=len(data))
        plt.scatter(
            x_vals,
            data,
            color=color_lkh,
            alpha=0.7,
            edgecolors='white',
            linewidths=0.5,
            label=solver_lkh if i == 0 else "",
            marker='D',
            s=60,
            zorder=2
        )

# --- Overlay optimal solutions (center) ---
for ref_solver, marker, color, z in zip(
    ["Optimal Solution (without Clustering)", "Optimal Solution (with Clustering)"],
    ['s', 'x'],
    [color_opt1, color_opt2],
    [3, 4]
):
    ref_data = df[df["Solvername"] == ref_solver]
    grouped = ref_data.groupby("Problemname_clean")["Solution (Kilometer)"].mean()

    for i, problem in enumerate(problem_order):
        if problem in grouped:
            plt.scatter(
                x=x_base[i],
                y=grouped[problem],
                marker=marker,
                color=color,
                label=ref_solver if i == 0 else "",
                edgecolors='white',
                s=90,
                zorder=z
            )

# --- Axis formatting ---
plt.xticks(x_base, problem_order, rotation=0)
plt.xlabel("VRP Problem")
plt.ylabel("Solution (Kilometer)")
plt.title("Solution Comparison: LKH-3 (Scatter), D-Wave (Boxplot), Optimal (Markers)")
plt.grid(axis="y", linestyle="--", alpha=0.5)

# --- Custom legend ---
legend_elements = [
    Patch(facecolor=color_dwave, edgecolor="gray", label=solver_dwave),
    Line2D([0], [0], marker='D', color='w', label=solver_lkh,
           markerfacecolor=color_lkh, markeredgecolor='white', markersize=8),
    Line2D([0], [0], marker='s', color='w', label="Optimal Solution (without Clustering)",
           markerfacecolor=color_opt1, markeredgecolor='white', markersize=9),
    Line2D([0], [0], marker='o', color='w', label="Optimal Solution (with Clustering)",
           markerfacecolor=color_opt2, markeredgecolor='white', markersize=8)
]

plt.legend(
    handles=legend_elements,
    loc='upper left',  # top left inside the plot
    title="Solver",
    frameon=True
)

plt.tight_layout()
plt.savefig("vrp_solver_comparison.pdf", format="pdf", bbox_inches="tight")
plt.show()
plt.close()