import pandas as pd

ROOT = "{}"

data = pd.read_csv(ROOT.format("combined_data.csv"))

def get_normal(df, dtype):
    normal = []
    max_val = {}
    for index, row in df.iterrows():
        time = str(row["year"]) + "_" + str(row["quarter"])
        if time in max_val:
            max_val[time] = max(max_val[time], row[dtype])
        else:
            max_val[time] = row[dtype]
        normal.append((time, row[dtype]))

    for i in range(len(normal)):
        normal[i] = float(normal[i][1]) / float(max_val[normal[i][0]])

    return normal

data["norm_issue"] = get_normal(data, "issue")
data["norm_pull"] = get_normal(data, "pull")
data["norm_push"] = get_normal(data, "push")
data["norm_star"] = get_normal(data, "star")

total = []
for index, row in data.iterrows():
    total.append((row["norm_issue"] + row["norm_pull"] + row["norm_push"] + row["norm_star"]) / 4)
data["norm_use"] = total

data.to_csv(ROOT.format("normalized_data.csv"))
