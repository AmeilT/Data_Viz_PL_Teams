import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import re
import seaborn as sns
from data_viz_constants import title_font, title_size, label_font, label_size, text_colour, back_colour, y_equals_x
from constants import features, Path
import matplotlib.patches as patches
import pandas as pd
import os

gameweekrange=[1,3]
xtitle=""
plottitle=""
y=""
filepath=""

season = 2021
cwd = Path(os.getcwd())
dict_path = {}

for feature in features:
    dict_path[
        f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/team data/team_{season}_{feature}"

dict_data = {}
for feature in features:
    dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])

# Filter data
gameweek_range = [1, 3]
A = gameweek_range[0]
B = gameweek_range[1]

for key, value in dict_data.items():
    dict_data[key] = value.loc[(value['GW ID'] >= A) & (value['GW ID'] <= B)]

y="Team"
data="defending_data"
method="sum"
if method=="mean":
    df=dict_data[data].groupby(["Season", "Team"]).mean().reset_index()
elif method=="sum":
    df=dict_data[data].groupby(["Season", "Team"]).sum().reset_index()

df=dict_data[data]

def cumm_calc_gw(df,gw_list):
    for gw in gw_list:
        cumm_list = gw_list[:gw_list.index(gw) + 1]
        df[f"Cummulative GW {gw}"] = df[cumm_list].sum(axis=1)
    df = df.reset_index().sort_values(f"Cummulative GW {gw_list[-1]}", ascending=False).head(N)
    return df

x2="Goals Conceded"
N=15
gw_list = range(gameweek_range[0], gameweek_range[1] + 1)
test = pd.pivot_table(df, index='Team', values=x2, columns='GW ID')
test = cumm_calc_gw(test, gw_list, N)

sns.set_theme(style="whitegrid")

 # Initialize the matplotlib figure
fig, axes = plt.subplots()

# colours
backcolour = "#020530"
titlecolor = "w"

# Axes
plt.rcParams['figure.facecolor'] = backcolour
axes.set_facecolor(backcolour)
fig.patch.set_facecolor(backcolour)
axes.set_xlabel(xtitle, color=titlecolor)  # Notice the use of set_ to begin methods
#axes.set_ylabel(y, color=titlecolor)
axes.spines['bottom'].set_color(backcolour)
axes.spines['top'].set_color(backcolour)
axes.xaxis.label.set_color(titlecolor)
axes.tick_params(axis='x', colors=titlecolor)
axes.yaxis.label.set_color(titlecolor)
axes.tick_params(axis='y', colors=titlecolor)

if gameweekrange == "ALL":
    axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w",
                   loc="left", size=title_size, font=title_font)
elif gameweekrange[0] == gameweekrange[1]:
    axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left",
                   size=title_size, font=title_font)
else:
    axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", color="w",
                   loc="left", size=title_size, font=title_font)
#alpha = 1
colours=["b","g","r","m","c"]
a=list(zip(range(gameweekrange[0],gameweekrange[1]+1),colours))
for x,colour in a:
    # Plot
    gw_list = range(gameweekrange[0],gameweekrange[1]+1)
    sns.set_color_codes("pastel")
    sns.barplot(x=df[f"Cummulative GW {x}"], y=y,data=df,
                label=f"Gameweek {x}", color=colour,zorder=len(gw_list)-gw_list.index(x))
    plt.xlabel(xtitle)
    plt.ylabel("")

    #alpha-=0.33

# Put a legend below current axis
axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
          fancybox=True, shadow=True, ncol=len(gw_list))

axes.set(xlabel=xtitle)
sns.despine(left=True, bottom=True)

fig.set_size_inches(12.6, 6.7)
fig.savefig(filepath)