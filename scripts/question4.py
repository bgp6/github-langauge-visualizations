import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT = ROOT.joinpath("output/")
OUTPUT.mkdir(exist_ok=True)
DATA_FILE = ROOT.joinpath("data/combined_data.csv")

if not DATA_FILE.is_file():
    import preprocess

df = pd.read_csv(DATA_FILE)
df.drop(columns = ["year", "quarter", "repo", "uid", "name"], inplace = True)

correlations = np.round(df.corr().to_numpy(), decimals=2)

#plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
plt.style.use(['dark_background'])

fig, ax = plt.subplots()
im = ax.imshow(correlations, cmap = 'inferno')

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(list(df.columns))), labels=list(df.columns))
ax.set_yticks(np.arange(len(list(df.columns))), labels=list(df.columns))

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(list(df.columns))):
    for j in range(len(list(df.columns))):
        text = ax.text(j, i, correlations[i, j], ha="center", va="center", color="aqua")

fig.tight_layout()

plt.savefig(OUTPUT.joinpath("correlation_heatmap.png"), bbox_inches="tight", transparent = True)
