from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sn
import itertools
import re
import scipy.linalg as spla
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import category_encoders as ce
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix

matches_csv = pd.read_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Input Data\master_matches.csv")
players_csv = pd.read_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Input Data\master_players.csv")

"""################################
    Creating a unique match identifier column in each
    data set to be able to cross reference between dfs
   ################################"""

match_identifiers = []

for i, row in matches_csv.iterrows():

    date_teams_result_event = ""

    date = str(row["Date"])
    team1 = str(row["Team1"])
    team2 = str(row["Team2"])
    result1 = str(row["Final Result 1"])
    result2 = str(row["Final Result 2"])
    event = str(row["Tournament"])

    date_teams_result_event = date + team1 + team2 + result1 + result2 + event

    match_identifiers.append(date_teams_result_event)

matches_csv["Match Identifier"] = match_identifiers

match_identifiers = []

for i, row in players_csv.iterrows():

    date_teams_result_event = ""

    date = str(row["Date"])
    team1 = str(row["Team1"])
    team2 = str(row["Team2"])
    result1 = str(row["Final Result 1"])
    result2 = str(row["Final Result 2"])
    event = str(row["Tournament"])

    date_teams_result_event = date + team1 + team2 + result1 + result2 + event

    match_identifiers.append(date_teams_result_event)

players_csv["Match Identifier"] = match_identifiers

"""################################
        Finding the total KD for
        each team, in each match
   ################################"""

total_adr_team1 = []
total_adr_team2 = []

for i, match_row in matches_csv.iterrows():

    team1_adr = 0
    team2_adr = 0

    team1_name = match_row["Team1"]
    team2_name = match_row["Team2"]

    u_id_match = match_row["Match Identifier"]

    for j, player_row in players_csv.iterrows():

        team = player_row["Player Team"]
        adr = player_row["ADR"]

        u_id_player = player_row["Match Identifier"]

        if(u_id_match == u_id_player):

            if(team == team1_name):
                team1_adr += adr
            if(team == team2_name):
                team2_adr += adr

    total_adr_team1.append(team1_adr)
    total_adr_team2.append(team2_adr)

matches_csv["Total ADR Team1"] = total_adr_team1
matches_csv["Total ADR Team2"] = total_adr_team2

"""################################
    Encoding a teriary value to represent
    final result of the game

    1 = Team1 Wins
    0 = team 2 Wins
    2 = Tie
   ################################"""

team1_wins=  []

for k, row in matches_csv.iterrows():
    if( row["Final Result 1"] > row["Final Result 2"] ):
        team1_wins.append(1)
    elif( row["Final Result 1"] < row["Final Result 2"] ):
        team1_wins.append(0)
    elif( row["Final Result 1"] == row["Final Result 2"] ):
        team1_wins.append(2)

matches_csv["Team 1 Wins"] = team1_wins

"""plt.subplot(1,2,1)
sn.distplot( a = matches_csv[matches_csv['Team 1 Wins']==1]['Total ADR Team1'], label = 'Team 1 wins', kde=False)
sn.distplot( a = matches_csv[matches_csv['Team 1 Wins']==0]['Total ADR Team1'], label = 'Team 1 loses', kde=False)
plt.legend()

plt.subplot(1,2,2)
sn.distplot( a = matches_csv[matches_csv['Team 1 Wins']==0]['Total ADR Team2'], label = 'Team 2 wins', kde=False)
sn.distplot( a = matches_csv[matches_csv['Team 1 Wins']==1]['Total ADR Team2'], label = 'Team 2 loses', kde=False)
plt.legend()

plt.show()"""


"""################################
    Beginnging to get data into proper form for linear regression
   ################################"""

train_x = players_csv

"""################################
    Creating a new column for each player, "Opposing Team"

    Represents whatever team that player was playing against
    in that specific match
   ################################"""

opposing_team = []

for i, row in train_x.iterrows():
    if( row["Player Team"] == row["Team1"]):
        opposing_team.append(row["Team2"])
    else:
        opposing_team.append(row["Team1"])

train_x["Opposing Team"] = opposing_team

"""################################
    setting training and target data
   ################################"""

train_column_y = train_x["ADR"]

model_columns_x = [ "Player", "Player Team", "Overall Kill / Death", "Overall Kill / Round",
                    "Overall Kill - Death Diff", "Opening Kill Ratio", "Opening Kill rating",
                    "Opening Team win percent after 1st kill","Opening Team win percent after 1st kill","Opening 1st kill in won rounds", "Opposing Team"]
#, "KAST"
train_columns_x = train_x[model_columns_x]
train_columns_x.info()

"""################################
    Converting Percent Values to decimal
            27.30% -> .2730
   ################################"""

first_kill = []
win_percentage = []

for i, row in train_columns_x.iterrows():
    fkr_num = row["Opening Team win percent after 1st kill"][0]
    first_kill_rate = float(row["Opening 1st kill in won rounds"][0][0:4])/100
    first_kill.append(first_kill_rate)
    win_ratio = float(row["Opening Team win percent after 1st kill"][0][0:4])/100
    win_percentage.append(win_ratio)

train_columns_x["Opening 1st kill in won rounds float"] = first_kill
train_columns_x["Opening Team win percent after 1st kill float"] = win_percentage

train_columns_x.drop(["Opening Team win percent after 1st kill", "Opening 1st kill in won rounds"], axis = 1, inplace = True)

"""################################
    Converting 'Player', 'Player Team', and
    'Opposing Team' to unique integer values
   ################################"""

cat_features_encoding = ['Player', 'Player Team', 'Opposing Team'] #
target_enc = ce.TargetEncoder(cols = cat_features_encoding)
target_enc.fit(train_columns_x[cat_features_encoding], train_column_y)

train_encoded_x = train_columns_x.join(target_enc.transform(train_columns_x[cat_features_encoding]).add_suffix('_target'))

train_encoded_x.drop(['Player', 'Player Team', 'Opposing Team'], axis = 1, inplace = True)#

"""################################
    Creating and training model
   ################################"""

x_train, x_test, y_train, y_test = train_test_split(train_encoded_x,train_column_y, train_size=0.6, random_state=1)

logistic = LinearRegression()
logistic.fit(x_train, y_train)
y_pred = logistic.predict(x_test)

"""################################
    Preliminary data analysis
   ################################"""

abs_reals = []
final = pd.DataFrame()
final["y_pred"] = y_pred
final["y_real"] = train_column_y

print('Mean squared Error :',mean_absolute_error(y_test,y_pred))

print('Accuracy of linear regression classifier on test set: ', logistic.score(x_test, y_test))


"""################################
    Predicting future matches
   ################################"""

future_players = pd.read_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Upcoming_Matches\sat\upcoming_sat_players.csv")
future_matches = pd.read_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Upcoming_Matches\sat\upcoming_sat_matches.csv")
train_x_new = future_players

"""################################
    Creating a new column for each player, "Opposing Team"

    Represents whatever team that player was playing against
    in that specific match
   ################################"""

opposing_team = []

for i, row in train_x_new.iterrows():
    if( row["Player Team"] == row["Team1"]):
        opposing_team.append(row["Team2"])
    else:
        opposing_team.append(row["Team1"])

train_x_new["Opposing Team"] = opposing_team


model_columns_x_new = [ "Player", "Player Team", "Overal Kill / Death", "Overall Kill / Round",
                    "Overall Kill - Death Diff", "Opening Kill Ratio", "Opening Kill rating",
                    "Opening Team win percent after 1st kill","Opening Team win percent after 1st kill","Opening 1st kill in won rounds", "Opposing Team"]
train_columns_x_new = train_x_new[model_columns_x_new]


"""################################
    Converting Percent Values to decimal
            27.30% -> .2730
   ################################"""


first_kill = []
win_percentage = []

for i, row in train_columns_x_new.iterrows():
    first_kill_rate = float(row["Opening 1st kill in won rounds"][0][0:4])/100
    first_kill.append(first_kill_rate)
    win_ratio = float(row["Opening Team win percent after 1st kill"][0][0:4])/100
    win_percentage.append(win_ratio)

train_columns_x_new["Opening 1st kill in won rounds float"] = first_kill
train_columns_x_new["Opening Team win percent after 1st kill float"] = win_percentage

train_columns_x_new.drop(["Opening Team win percent after 1st kill", "Opening 1st kill in won rounds"], axis = 1, inplace = True)


"""################################
    Converting 'Player', 'Player Team', and
    'Opposing Team' to unique integer values
   ################################"""


cat_features_encoding = ['Player', 'Player Team', 'Opposing Team']
target_enc = ce.TargetEncoder(cols = cat_features_encoding)
target_enc.fit(train_columns_x_new[cat_features_encoding], train_columns_x_new['Opening Kill Ratio'])

train_encoded_x_new = train_columns_x_new.join(target_enc.transform(train_columns_x_new[cat_features_encoding]).add_suffix('_target'))

train_encoded_x_new.drop(['Player', 'Player Team', 'Opposing Team'], axis = 1, inplace = True)


print("New Players Encoded!")

"""################################
    Making Final Prediction
   ################################"""

final_pred = logistic.predict(train_encoded_x_new)

future_players["Predicted ADR"] = final_pred

net_adr = [] # team1adr - team2adr
pred_winner = []

for i, match in future_matches.iterrows():

    team1 = match["Team1"]
    team2 = match["Team2"]
    team1adr = 0
    team2adr = 0

    for i, player in future_players.iterrows():

        pred_adr = player["Predicted ADR"]

        if(player["Player Team"] == team1):
            team1adr += pred_adr
        if(player["Player Team"] == team2):
            team2adr += pred_adr
    diff_adr = team1adr - team2adr
    net_adr.append(diff_adr)

    if( diff_adr > 0 ):
        pred_winner.append(team1)

    if(diff_adr < 0):
        pred_winner.append(team2)

future_matches["Predicted Net ADR"] = net_adr
future_matches["Predicted Winner"] = pred_winner
future_matches.to_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Predictions\sat\test_predictions.csv")
future_players.to_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\Predictions\sat\test_predictions.csv")

print(future_matches)

for i, match in future_matches.iterrows():
    winner = match["Predicted Winner"]
    if( winner == match["Team1"]):
        loser = match["Team2"]
    else:
        loser = match["Team1"]

    pos_adr = match["Predicted Net ADR"]
    print_string = winner + " is predicted to beat " + loser + ", with a net adr of " + str(pos_adr)
    print(print_string)
