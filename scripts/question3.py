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

data = {}
for index, row in df.iterrows():
    name = row["name"]
    usage = row["norm_use"]
    new_usage = data.get(name, 0) + usage
    data[name] = new_usage

# sorted_data = sorted(data.items(), key = lambda x:x[1], reverse = True)

sorted_data = pd.DataFrame.from_dict(data, orient='index', columns=['norm_use'])
sorted_data = sorted_data.sort_values(by = "norm_use", ascending=False)
top_ten = sorted_data[:10]

print(top_ten)

       