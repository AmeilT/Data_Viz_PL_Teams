import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from adjustText import adjust_text
import re
import seaborn as sns
import pandas as pd
from constants import teams, \
    path, \
    FEATURES
from data_viz_constants import title_font, \
    title_size, \
    label_font, \
    label_size, \
    text_colour, \
    back_colour, \
    y_equals_x
from pathlib import Path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os


def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.08, alpha=.8)


def get_agg_data(gameweek, feature_type):
    season = 2021
    cwd = Path(os.getcwd())
    dict_path = {}
    for feature in FEATURES:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/team data/team_{season}_{feature} "

    dict_data = {}
    for feature in FEATURES:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])

    # Filter data
    gameweek_range = [gameweek - 4, gameweek]
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['GW ID'] >= A) & (value['GW ID'] <= B)]

    y = "Team"
    data = feature_type
    method = "sum"
    if method == "mean":
        df = dict_data[data].groupby(["Season", "Team"]).mean().reset_index()
    elif method == "sum":
        df = dict_data[data].groupby(["Season", "Team"]).sum().reset_index()

    df_final = pd.merge(df, teams, on="Team", how="left")
    return df_final


def get_data(gameweek, feature_type):
    season = 2021
    cwd = Path(os.getcwd())
    dict_path = {}
    for feature in FEATURES:
        dict_path[
            f"{feature}_data_path"] = rf"{str(cwd.parent.absolute())}/FFScout Database/scraper/data/team data/team_{season}_{feature}"

    dict_data = {}
    for feature in FEATURES:
        dict_data[f"{feature}_data"] = pd.read_csv(dict_path[f"{feature}_data_path"])

    # Filter data
    gameweek_range = [gameweek - 4, gameweek]
    A = gameweek_range[0]
    B = gameweek_range[1]

    for key, value in dict_data.items():
        dict_data[key] = value.loc[(value['GW ID'] >= A) & (value['GW ID'] <= B)]

    y = "Team"
    df = dict_data[feature_type].reset_index()
    return df


def cumm_calc_gw(df, gw_list):
    for gw in gw_list:
        cumm_list = gw_list[:gw_list.index(gw) + 1]
        df[f"Cummulative GW {gw}"] = df[cumm_list].sum(axis=1)
    df = df.reset_index().sort_values(f"Cummulative GW {gw_list[-1]}", ascending=False)
    return df


def hex_to_rgb(hx, hsl=True):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values."""
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i] * 2, 16) / div if div else
                         int(hx[i] * 2, 16) for i in (1, 2, 3))
        else:
            return tuple(int(hx[i:i + 2], 16) / div if div else
                         int(hx[i:i + 2], 16) for i in (1, 3, 5))
    else:
        raise ValueError(f'"{hx}" is not a valid HEX code.')


def create_team_graph(data, x, y, xtitle, ytitle, plottitle, gameweekrange, line):
    # Create Figure (empty canvas)
    fig, axes = plt.subplots()

    # Move set of axes to figure
    # axes = fig.add_axes([0, 0, 1, 1])  # left, bottom, width, height (range 0 to 1)

    # colours
    plt.rcParams['figure.facecolor'] = back_colour
    axes.set_facecolor(back_colour)
    plt.rcParams["font.family"] = label_font
    axes.spines['left'].set_color(text_colour)
    axes.spines['bottom'].set_color(text_colour)
    axes.spines['top'].set_visible(False)
    axes.tick_params(axis='x', colors=text_colour)
    axes.tick_params(axis='y', colors=text_colour)

    # Plot on that set of axes
    axes.scatter(data[x], data[y])
    axes.set_xlabel(xtitle, color=text_colour)  # Notice the use of set_ to begin methods
    axes.set_ylabel(ytitle, color=text_colour)

    if gameweekrange == "ALL":
        axes.set_title(f"{plottitle}\n 21/22 Season so far", color="w", loc="left", size=title_size, font=title_font)
    elif gameweekrange[0] == gameweekrange[1]:
        axes.set_title(f"{plottitle}\nGameweek {gameweekrange[0]}", color="w", loc="left", size=title_size,
                       font=title_font)
    else:
        axes.set_title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}")

    # y=x line
    if line == 1:
        a = np.linspace(data[x].min(), data[x].max(), 20)
        b = np.linspace(data[y].min(), data[y].max(), 20)
        axes.plot(a, b, "g--")
    else:
        pass

    filepath = f"Scatter for showing {x} vs {y}"
    fig.set_size_inches(10.2, 9)
    fig.savefig(path + "\\" + filepath)


def create_expected_team_graph(data, x, y, xtitle, ytitle, plottitle, gameweekrange, teams=teams):
    # Create Figure (empty canvas)
    fig, axes = plt.subplots(figsize=(6, 4), dpi=120)
    # Hide grid lines
    axes.grid(False)

    font_path = r'C:\Users\ameil\Fonts\Hydrophilia\HydrophiliaLiquid_Regular.ttf'  # Your font path goes here
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    fontproperties = prop

    # colours
    plt.rcParams['figure.facecolor'] = back_colour
    axes.set_facecolor(back_colour)
    fig.patch.set_facecolor(back_colour)
    #plt.rcParams["font.family"] = fontproperties

    axes.spines['left'].set_color(text_colour)
    axes.spines['bottom'].set_color(text_colour)
    axes.spines['top'].set_visible(False)
    axes.tick_params(axis='x', colors=text_colour)
    axes.tick_params(axis='y', colors=text_colour)

    # displaying the title
    plt.title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}",loc="left", fontsize=15,color=text_colour,
              fontproperties=fontproperties)



    # Plot on that set of axes
    axes.scatter(data[x], data[y])
    # axes.set_xlabel(xtitle, color=text_colour)  # Notice the use of set_ to begin methods
    # axes.set_ylabel(ytitle, color=text_colour)

    for index, row in data.iterrows():
        ab = AnnotationBbox(getImage(row["badge_path"]), (row[x], row[y]), frameon=False)
        axes.add_artist(ab)

    # Add average lines
    plt.vlines(data[x].mean(), data[y].min(), data[y].max(), color='#c2c1c0')
    plt.hlines(data[y].mean(), data[x].min(), data[x].max(), color='#c2c1c0')

    fig.text(0.07, .14, ytitle, size=15, color=text_colour, rotation=90,fontproperties=fontproperties)
    fig.text(.12, 0.05, xtitle, size=15, color=text_colour,fontproperties=fontproperties)

    filepath = f"Scatter for showing {x} vs {y}"
    fig.set_size_inches(10.2, 9)
    fig.savefig(path + "\\" + filepath)


def stacked_team_graph(data, x, y, xtitle, plottitle, gameweek_range):
    gw_list = range(gameweek_range[0], gameweek_range[1] + 1)
    stacked_data = pd.pivot_table(data, index='Team', values=x, columns='GW ID')
    stacked_data = cumm_calc_gw(stacked_data, gw_list)

    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots()

    font_path = r'C:\Users\ameil\Fonts\Hydrophilia\HydrophiliaLiquid_Regular.ttf'  # Your font path goes here
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    fontproperties = prop

    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(xtitle, color=titlecolor)  # Notice the use of set_ to begin methods
    # axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    # displaying the title
    plt.title(f"{plottitle}\nbetween gameweek {gameweek_range[0]} and {gameweek_range[1]}", loc="left", fontsize=15,
              color=text_colour,
              fontproperties=fontproperties)

    colours = ["b", "g", "r", "m", "c"]
    a = list(zip(range(gameweek_range[0], gameweek_range[1] + 1), colours))
    for x, colour in a:
        # Plot
        gw_list = range(gameweek_range[0], gameweek_range[1] + 1)
        sns.set_color_codes("pastel")
        sns.barplot(x=stacked_data[f"Cummulative GW {x}"], y=y, data=stacked_data,
                    label=f"Gameweek {x}", color=colour, zorder=len(gw_list) - gw_list.index(x))
        plt.xlabel(xtitle)
        plt.ylabel("")

    # Put a legend below current axis
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
                fancybox=True, shadow=True, ncol=len(gw_list))

    axes.set(xlabel=xtitle)
    sns.despine(left=True, bottom=True)

    filepath = f"Stacked {plottitle}"
    fig.set_size_inches(10.2, 9)
    fig.savefig(path + "\\" + filepath)


def hbarplot(data, x1, x2, y, ytitle, xtitle, plottitle, gameweekrange):
    data = data.merge(teams, on=["Team"])
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    fig, axes = plt.subplots(figsize=(6, 15))

    font_path = r'C:\Users\ameil\Fonts\Hydrophilia\HydrophiliaLiquid_Regular.ttf'  # Your font path goes here
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    fontproperties = prop


    # colours
    backcolour = "#020530"
    titlecolor = "w"

    # Axes
    plt.rcParams['figure.facecolor'] = backcolour
    axes.set_facecolor(backcolour)
    fig.patch.set_facecolor(backcolour)
    axes.set_xlabel(xtitle, color=titlecolor)  # Notice the use of set_ to begin methods
    axes.set_ylabel(y, color=titlecolor)
    axes.spines['bottom'].set_color(backcolour)
    axes.spines['top'].set_color(backcolour)
    axes.xaxis.label.set_color(titlecolor)
    axes.tick_params(axis='x', colors=titlecolor)
    axes.yaxis.label.set_color(titlecolor)
    axes.tick_params(axis='y', colors=titlecolor)

    # displaying the title
    plt.title(f"{plottitle}\nbetween gameweek {gameweekrange[0]} and {gameweekrange[1]}", loc="left", fontsize=15,
              color=text_colour,
              fontproperties=fontproperties)


    # Plot 1
    sns.set_color_codes("pastel")
    sns.barplot(x=data[x1], y=y, data=data,
                label="Goals Scored", color="r", alpha=0.8, order=data.sort_values(x2, ascending=False)[y])

    # Plot 2
    sns.set_color_codes("muted")
    sns.barplot(x=data[x2], y=y, data=data,
                label="Expected Goals", color="b", alpha=0.5, order=data.sort_values(x2, ascending=False)[y])

    # Add a legend and informative axis label
    axes.legend(ncol=2, loc="lower right", frameon=True)
    axes.set(ylabel=ytitle, xlabel=xtitle)
    sns.despine(left=True, bottom=True)

    filepath = f"Barplot Teams {x1} vs {y}"
    fig.set_size_inches(10.2, 9)
    fig.savefig(path + "\\" + filepath)
