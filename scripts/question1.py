"""Margaret Jackson
December 8, 2023
BGP Group 6 Question 1
How do the different languages used on Github compare in usage to each other? (pie graph)
usage = (pulls + stars + pushes) / 3
expressed as exploding pie chart"""

"""comparing pushes/pulls/etc to the repo data"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""df = pd.read_csv(r"combined_data.csv")
df2 = pd.read_csv(r"total_repos.csv")
bigList = df['language'].tolist()
littleList = df2['name'].tolist()

totalList = []
bL = list(set(bigList))
for i in littleList :
    for j in bL :
        if i == j :
            totalList.append(i)
print(totalList)

with open('test.csv', 'wb') as f:
    writer = csv.writer(f)
    for val in test_list:
        writer.writerow([val])"""

df = pd.read_csv(r"combdata.csv")
reponum = df['repo'].tolist()
namenum = df['name'].tolist()
repo = []
name = []
"""isolating the data"""
for i in range (0, len(reponum)) :
    if reponum[i] > 0 :
        repo.append(reponum[i])
        name.append(namenum[i])
#print(repo)
#print(name)

"""now it is time for data analysis"""
#use repo
#use name
minnum = int(repo[0] * .05)
"""print(minnum)
#counting the number of wedges
wedcount = 1
for i in repo :
    if i >= minnum :
        wedcount += 1
        print (i)
print(wedcount)"""
#20 wedges at the 0.1 cutoff
"""creating the data for wedges"""
reponum.clear()
namenum.clear()
count = 0
for i in range (0,20) :
    reponum.append(repo[i])
    namenum.append(name[i])
for i in range(20,len(repo)) :
    count += repo[i]
reponum.append(count)
namenum.append("Other")
print(reponum)
print(namenum)

#making the graph
# Creating explode data
explode = (0.2, 0.1, 0.2, 0.1, 0.0, 0.15, 0.2, 0.3, 0.2, 0.0, 0.15, 0.1, 0.2, 0.25, 0.1, 0.2, 0.0, 0.1, 0.15, 0.1, 0.15)
 
# Creating color parameters
colors = ("steelblue","palevioletred","tomato","cyan","violet","coral","lightpink","gold","deeppink","turquoise","plum","crimson","cornflowerblue","cyan", "mediumseagreen","lightsalmon","hotpink","mediumorchid","pink","paleturquoise","wheat")

# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "darkblue" }
 
# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} )".format(pct, absolute) 

# Creating plot
fig, ax = plt.subplots(figsize =(10, 7))
wedges, texts, autotexts = ax.pie(reponum, 
                                  autopct = lambda pct: func(pct, reponum),
                                  explode = explode, 
                                  labels = namenum,
                                  shadow = True,
                                  colors = colors,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="magenta"))
 
# Adding legend
ax.legend(wedges, namenum,
          title ="Ages",
          loc ="center left",
          bbox_to_anchor =(1, 0, 0.5, 1))
 
plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Customizing pie chart")
 
# show plot
plt.show()
