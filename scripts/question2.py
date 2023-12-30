import pathlib
import pandas as pd
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT = ROOT.joinpath("output/")
OUTPUT.mkdir(exist_ok=True)
DATA_FILE = ROOT.joinpath("data/combined_data.csv")

# Generate combined data if it does not exist
if not DATA_FILE.is_file():
    import preprocess

# Apply style sheet for dark backgrounds
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

LANGUAGES = ["JavaScript", "Python", "Ruby", "Java", "PHP", "C", "C++", "Objective-C", "C#", "Perl", "Go", "CoffeeScript", "TypeScript", "Assembly", "Swift", "Scala", "Lua", "Haskell", "R", "Clojure", "Objective-C++", "Rust", "Erlang", "OCaml", ]

data = pd.read_csv(DATA_FILE)
data = data.query('year == 2023 and quarter == 3 and name in @LANGUAGES')
data = data.sort_values(by=["repo"], ascending=False)
data["issues_per_repo"] = data["issue"] / data["repo"]
plt.bar(data["name"], data["issues_per_repo"])
plt.xticks(rotation=45, ha='right')
plt.savefig(OUTPUT.joinpath("issues_per_repo.svg"), bbox_inches="tight", transparent = True)
plt.savefig(OUTPUT.joinpath("issues_per_repo.png"), bbox_inches="tight", transparent = True)
