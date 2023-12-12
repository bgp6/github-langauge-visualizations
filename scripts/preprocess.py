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

# saving file
ret.to_csv(ROOT.joinpath("combined_data.csv"))
