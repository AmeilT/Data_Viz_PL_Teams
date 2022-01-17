import os
from pathlib import Path
import pandas as pd

cwd = Path(os.getcwd())
path=r"C:\Users\ameil\Documents\Viz Saves\Team"

FEATURES = ["defending", "expected", "goal-threat"]

teams = pd.DataFrame()
teams["Team"] = ['ARS','AVL','BHA','BUR','CHE','CRY','EVE','FUL','LEE','LEI','LIV','MCI','MUN','NEW','SHU','SOU','TOT','WBA','WHU','WOL',"BRE","WAT","NOR","TOT","LEI","MCI","MUN"]
teams["Full Name"]=["Arsenal","Aston Villa","Brighton","Burnley","Chelsea","Crystal Palace","Everton","Fulham","Leeds","Leicester City","Liverpool","Man City","Man Utd",
"Newcastle","Sheff Utd","Southampton","Tottenham","West Brom","West Ham","Wolves","Brentford","Watford","Norwich","Spurs","Leicester","Manchester City","Manchester United"]
dict_team={k:v for k,v in zip(teams["Team"], teams["Full Name"])}


colours = ["#EE3B3B", "#942257", "#afd6f0", "#631938"
    , "#1c19a8", "#500678", "#3d64e3", "#eff0e9"
    , "#eff0e9", "#4157c4"
    , "#c20245", "#04becf", "#de020a"
    , "#877777", "#e65353", "#ff001e", "#FFFFFF"
    , "#022873", "#70072f", "#f59247","#8f1e07","#e3df5f","#ebe307"]
dict_team={k:v for k,v in zip(teams["Team"], colours)}
teams["Colours"]=teams['Team'].map(dict_team)
teams["badge_path"]="team_badges/"+teams["Full Name"]+".png"
teams.sort_values(by="Team",ascending=True,inplace=True)
teams=teams.drop_duplicates(subset=["Team"])

