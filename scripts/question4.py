import numpy as np
import pandas as pd
import seaborn as sns
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT = ROOT.joinpath("output/")
OUTPUT.mkdir(exist_ok=True)
DATA_FILE = ROOT.joinpath("data/combined_data.csv")

if not DATA_FILE.is_file():
    import preprocess

df = pd.read_csv(DATA_FILE)
df.drop(columns = ["year", "quarter", "repo"], inplace = True)

sns.set(font_scale = 1)
svm = sns.heatmap(df.corr(), xticklabels = True, yticklabels = True, annot=True)
figure = svm.get_figure()

figure.savefig(OUTPUT.joinpath("correlation_heatmap.png"), bbox_inches="tight")
