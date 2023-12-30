import pathlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT = ROOT.joinpath("output/")
OUTPUT.mkdir(exist_ok=True)
DATA_FILE = ROOT.joinpath("data/combined_data.csv")

# Generate combined data if it does not exist
if not DATA_FILE.is_file():
    import preprocess

# Apply style sheet for dark backgrounds
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

df = pd.read_csv(DATA_FILE)
# Drop unused columns
df = df.drop(columns = ["uid", "year", "quarter", "issue", "pull", "push", "star", "norm_issue", "norm_pull", "norm_push", "norm_star", "norm_use"])
# Drop rows with no repo count, then sort
df = df[df.repo > 0]
df = df.sort_values(by = "repo", ascending=False)

"""now it is time for data analysis"""
# Threshold for the `Other` category
minnum = int(df.repo.max() * 0.25)

# Counting the number of wedges
wedcount = df[df.repo >= minnum].size + 1

"""creating the data for wedges"""
# Select rows that will not be grouped into other (normal wedges)
wedgeData = df[:wedcount-1]
# Sum repo counts for all languages in `Other` (all remaining languages)
otherCount = df[wedcount:].repo.sum()
# Construct a row for the `Other` wedge and append
otherData = pd.Series({'name': "Other", 'repo': otherCount}).to_frame().T
wedgeData = pd.concat([wedgeData, otherData], ignore_index = True)

# Making the graph

# Creating color parameters
colors = ("deeppink","turquoise","plum","crimson","cornflowerblue","turquoise", "mediumseagreen","lightsalmon","hotpink","mediumorchid","pink","paleturquoise","wheat", "steelblue","palevioletred","mediumslateblue","cyan","violet","coral","lightpink","gold")

# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "white", 'antialiased' : True }
# Collect percentages for the legend
perc = []
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    perc.append("{:.1f}%".format(pct, absolute))
    return ""

# Creating plot
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(wedgeData.repo, 
                                  autopct = lambda pct: func(pct, wedgeData.repo),
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  )
# Construct legend labels
labels = []
for i in range(0, wedgeData.name.size):
    labels.append(f"{wedgeData.name[i]} {perc[i]}")

# Add legend
ax.legend(wedges, labels,
          title = "Languages",
          loc = "center left",
          bbox_to_anchor = (1, 0, 0.5, 1))
 
plt.savefig(OUTPUT.joinpath("question_1.svg"), bbox_inches="tight", transparent = True)
plt.savefig(OUTPUT.joinpath("question_1.png"), bbox_inches="tight", transparent = True)
