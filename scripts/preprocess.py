import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve().joinpath("data")

# reading in data
issue = pd.read_csv(ROOT.joinpath("gh-issue-event.csv"))
pull = pd.read_csv(ROOT.joinpath("gh-pull-request.csv"))
push = pd.read_csv(ROOT.joinpath("gh-push-event.csv"))
star = pd.read_csv(ROOT.joinpath("gh-star-event.csv"))
repo = pd.read_csv(ROOT.joinpath("gh-repos-with-language.csv"))

# Add dummy year and quarter to repos count data
repo["year"] = "2023"
repo["quarter"] = "3"

# creating an uid (unique identifier) for each entry so we can combine the tables
def add_uid(df, dtype):
    uid = []
    for index, row in df.iterrows():
        uid.append(row["name"] + "__" + str(row["year"]) + "__" + str(row["quarter"]))
    df["uid"] = uid
    df.set_index("uid", inplace = True)
    df.rename(columns = {"count" : dtype}, inplace = True)
    df.drop(columns = ["name", "year", "quarter"], inplace = True)
    return df

issue = add_uid(issue, "issue")
pull = add_uid(pull, "pull")
push = add_uid(push, "push")
star = add_uid(star, "star")
repo = add_uid(repo, "repo")

# combining the dataframes
frames = [issue, pull, push, star, repo]
ret = pd.concat(frames, axis = 1)

# imputing NaNs in dataframe
print("Number of NaN:", ret.isna().sum().sum())
ret.fillna(0, inplace = True)

# extracting name, year, quarter from uid 
name = []
year = []
quarter = []

for index, row in ret.iterrows():
    properties = index.split("__")
    name.append(properties[0])
    year.append(properties[1])
    quarter.append(properties[2])
    
ret["name"] = name
ret["year"] = year
ret["quarter"] = quarter

# returns list with normalized values
def get_normal(df, dtype):
    normal = []     # stores date range and value
    max_val = {}    # max val of that date range 
    for index, row in df.iterrows():
        time = str(row["year"]) + "_" + str(row["quarter"])
        if time in max_val:
            max_val[time] = max(max_val[time], row[dtype])
        else:
            max_val[time] = row[dtype]
        normal.append((time, row[dtype]))

    # scaling each data point from 0 to 1 
    for i in range(len(normal)):
        normal[i] = float(normal[i][1]) / float(max_val[normal[i][0]])

    return normal

# adding normalized columns to the dataframe
ret["norm_issue"] = get_normal(ret, "issue")
ret["norm_pull"] = get_normal(ret, "pull")
ret["norm_push"] = get_normal(ret, "push")
ret["norm_star"] = get_normal(ret, "star")

# calculating average of 4 normalized data points 
total = []
for index, row in ret.iterrows():
    total.append((row["norm_issue"] + row["norm_pull"] + row["norm_push"] + row["norm_star"]) / 4)
ret["norm_use"] = total

# saving file
ret.to_csv(ROOT.joinpath("combined_data.csv"))
