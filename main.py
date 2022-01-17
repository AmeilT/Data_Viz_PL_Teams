from chart_functions import create_expected_team_graph, hbarplot, stacked_team_graph, get_agg_data, get_data
# Import data

gameweek=11
gameweek_range=[gameweek-4,gameweek]

#Defence
#GC Stacked
gw_data=get_data(gameweek,"defending_data")
stacked_team_graph(gw_data,"Goals Conceded", "Team", "", "Goals Conceded by Gameweek",gameweek_range)

# #xGC vs GC graph
gw_data=get_agg_data(gameweek,"expected_data")
create_expected_team_graph(gw_data,"Goals ConcededGC","Goals ConcededxGC","Actual Goal Conceded","Expected Goals Conceded","Actual vs Expected Goals Conceded",gameweekrange=gameweek_range)

#GC vs Shots Conceded
gw_data=get_agg_data(gameweek,"defending_data")
create_expected_team_graph(gw_data,"Goals Conceded","Shots ConcededIn","Goals Conceded","Shots Conceded In Box","Shots vs Goals Conceded",gameweekrange=gameweek_range)

# #Attack
# #GS Stacked
gw_data=get_data(gameweek,"goal-threat_data")
stacked_team_graph(gw_data,"GoalsTotal", "Team", "", "Goals Scored by Gameweek",gameweek_range)
stacked_team_graph(gw_data,"AttemptsTotal", "Team", "", "Attempts by Gameweek",gameweek_range)
gw_data=get_agg_data(gameweek,"goal-threat_data")
create_expected_team_graph(gw_data,"GoalsTotal","AttemptsIn","Goals Scored","Attempts In Box","Goals vs Attempts",gameweekrange=gameweek_range)

# #xG vs G graph
gw_data=get_agg_data(gameweek,"expected_data")
create_expected_team_graph(gw_data,"xG Expected GoalsG","xG Expected GoalsxG","Actual Goals","Expected Goals","Actual vs Expected Goals Scored",gameweekrange=gameweek_range)

# gw_data=get_data(gameweek,"expected_data")
# hbarplot(gw_data,x1="xG Expected GoalsG",x2="xG Expected GoalsxG",y="Full Name",ytitle="",xtitle="",plottitle="Actual vs Expected Goals Scored",gameweekrange=gameweek_range)

