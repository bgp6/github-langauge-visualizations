import pandas as pd

ROOT = "./data/{}"

# reading in data
issue = pd.read_csv(ROOT.format("gh-issue-event.csv"))
request = pd.read_csv(ROOT.format("gh-pull-request.csv"))
push = pd.read_csv(ROOT.format("gh-push-event.csv"))
star = pd.read_csv(ROOT.format("gh-star-event.csv"))

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
request = add_uid(request, "request")
push = add_uid(push, "push")
star = add_uid(star, "star")

# combining the dataframes
frames = [issue, request, push, star]
ret = pd.concat(frames, axis = 1)

# imputing NaNs in dataframe
# print("Number of NaN:", ret.isna().sum().sum())
# ret.fillna(0, inplace = True)

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
ret.to_csv(ROOT.format("combined_data.csv"))
