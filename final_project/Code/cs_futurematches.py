from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import re
import scipy.linalg as spla
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import json
import argparse

driver = webdriver.Chrome(executable_path=r'C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe')

date = []
team1 = []
team2 = []
final_result1 = []
final_result2 = []
tournament = []
link_stats = []

players = []
players_kd = []
players_adr = []
players_kast = []
players_rating = []
players_date = []
players_tournament = []
players_team = []
players_map = []

players_team1 = []
players_team2 = []
players_final_result1 = []
players_final_result2 = []

players_overallKills = []
players_overallDeaths = []

players_overallKill_Death = []
players_overallKill_Round = []

players_overallRoundsWithKills = []
players_overallKillDeathDiff = []

players_openingTotalKills = []
players_openingTotalDeaths = []

players_openingKillRatio = []
players_openingKillRating = []

players_openingTeamWinPercentAfterFirstKill = []
players_openingFirstKillInWonRounds = []

map_dict = {

            "All maps"  : "",
            "Dust2"     : "&maps=de_dust2",
            "Mirage"    : "&maps=de_mirage",
            "Train"     : "&maps=de_train",
            "Overpass"  : "&maps=de_dust2",
            "Inferno"   : "&maps=de_inferno",
            "Nuke"      : "&maps=de_nuke",
            "Vertigo"   : "&maps=de_vertigo",
            "Cache"     : "&maps=de_cache",
            "Cobblestone" : "&maps=de_cobblestone"
                }

playersdf = pd.DataFrame(columns=[
'Date',
'Team1',
'Team2',
'Final Result 1',
'Final Result 2',
'Tournament',
'Player Team',
'Player',
'KD',
'ADR',
'KAST',
'Rating',
'Map',
'Overall Kills',
'Overall Deaths',
'Overal Kill / Death',
'Overall Kill / Round',
'Overall Rounds with Kills',
'Overall Kill - Death Diff',
'Opening Total Kills',
'Opening Total Deaths',
'Opening Kill Ratio',
'Opening Kill rating',
'Opening Team win percent after 1st kill',
'Opening 1st kill in won rounds'
])

months = {
    'January':'01',
    'February':'02',
    'March':'03',
    'April':'04',
    'May':'05',
    'June':'06',
    'July':'07',
    'August':'08',
    'September':'09',
    'October':'10',
    'November':'11',
    'December':'12'
}

""" Manual Input """

saturday_matchlinks = ["/matches/2345627/mousesports-vs-godsent-dreamhack-masters-winter-2020-europe", "/matches/2345628/furia-vs-astralis-dreamhack-masters-winter-2020-europe"]
match_links = saturday_matchlinks

m = 0



for match in match_links:
    if("/matches/" in match) and (match != "/matches/2345609/g2-vs-nemiga-dreamhack-masters-winter-2020-europe"):

        """################################
            Building Match Information Database
           ################################"""

        url = 'https://www.hltv.org/' + match
        driver.get(url)
        page = driver.page_source
        sauce = BeautifulSoup(page)

        """################################
            Finding relevant match data on matchpage
           ################################"""

        sauce_page  = sauce.findAll('div', attrs = {'class' : 'match-page'})
        sauce_team1 = sauce.findAll('div', attrs = {'class' : 'team1-gradient'})
        sauce_team2 = sauce.findAll('div', attrs = {'class' : 'team2-gradient'})
        sauce_lineups = sauce.findAll('div', attrs = {'class' : 'lineups-compare-container'})

        for div_match_page in sauce_page:
            page_date = div_match_page.find('div',attrs={'class':'date'})
            page_tournament = div_match_page.find('div',attrs={'class':'event text-ellipsis'})
            date.append(page_date.text)
            tournament.append(page_tournament.text)

        for div_team1 in sauce_team1:
            page_team1 = div_team1.find('div',attrs={'class':'teamName'})
            team1.append(page_team1.text)

        for div_team2 in sauce_team2:
            page_team2 = div_team2.find('div',attrs={'class':'teamName'})
            team2.append(page_team2.text)

        """################################
            Finding links to historic player statistics
           ################################"""

        sauce_smallstats = sauce.findAll('div',attrs={'class':'small-padding stats-detailed-stats'})

        for div_stats in sauce_smallstats:
            for a in div_stats.findAll('a'):
                link_stat = a['href']
                break

            url = 'https://www.hltv.org/' + link_stat
            link_stats.append(url)

        if sauce_smallstats == "":
            link_stats.append("")

        """################################
            Accessing historic player statistics
           ################################"""

        for div_all in sauce_lineups:

            data_team = ['data-team1-players-data','data-team2-players-data']

            for team in data_team:
                dict = json.loads(div_all[team])
                for key in dict.keys():

                    """################################
                        finding relevant data, stored in stats_aux
                       ################################"""


                    link_aux = dict[key]["statsLinkUrl"]
                    link = link_aux.split("?")

                    stats_aux = {}

                    """################################
                        Transforming date into hltv.org's URL format
                       ################################"""

                    date_stats = page_date.text
                    date_split = date_stats.split(" ")
                    year = date_split[-1]
                    month = months[date_split[-2]]

                    if (len(date_split[0]) == 3):
                        toInt = int(date_split[0][0])
                        day_aux = toInt - 1
                        day = '0' + str(day_aux)
                    else:
                        toInt = int(date_split[0][0:2])
                        day_aux = toInt - 1
                        day = str(day_aux)

                    """################################
                        Collecting player standard data
                       ################################"""

                    url = 'https://www.hltv.org' + link[0][:15] + '/' + link[0][15:] + '?startDate=2013-01-01&endDate=' + year + '-' + month + '-' + day
                    driver.get(url)
                    content = driver.page_source
                    sauce = BeautifulSoup(content)

                    imt = ""
                    for img in sauce.findAll(class_='summaryBodyshot'):
                        players.append(img['title'])
                    if (img == ""):
                        for img in sauce.findAll(class_='summarySquare'):
                            players.append(img['title'])

                    for img in sauce.findAll(class_='team-logo'):
                        players_team.append(img['title'])
                        players_team1.append(page_team1.text)
                        players_team2.append(page_team2.text)
                        break

                    """################################
                        Collecting relevant player statistics
                       ################################"""

                    url = 'https://www.hltv.org' + link[0][:15] + 'individual/' + link[0][15:] + '?startDate=2013-01-01&endDate=' + year + '-' + month + '-' + day
                    driver.get(url)
                    content = driver.page_source
                    sauce = BeautifulSoup(content)

                    sauce_player = sauce.findAll('div',attrs={'class','standard-box'})

                    for div_player in sauce_player:
                        sauce_statistics = div_player.findAll('div',attrs={'class','stats-row'})
                        for div_st in sauce_statistics:
                            stat = []
                            for span in div_st.findAll('span'):
                                if (span.text != 'K - D diff.'):
                                    stat.append(span.text)
                            stats_aux[stat[0]] = stat[1]

                    """################################
                        Appending
                       ################################"""

                    players_overallKills.append(stats_aux["Kills"])
                    players_overallDeaths.append(stats_aux["Deaths"])

                    players_overallKill_Death.append(stats_aux["Kill / Death"])
                    players_overallKill_Round.append(stats_aux["Kill / Round"])

                    players_overallRoundsWithKills.append(stats_aux["Rounds with kills"])
                    players_overallKillDeathDiff.append(stats_aux["Kill - Death difference"])

                    players_openingTotalKills.append(stats_aux["Total opening kills"])
                    players_openingTotalDeaths.append(stats_aux["Total opening deaths"])

                    players_openingKillRatio.append(stats_aux["Opening kill ratio"])
                    players_openingKillRating.append(stats_aux["Opening kill rating"])

                    players_openingTeamWinPercentAfterFirstKill.append(stats_aux["Team win percent after first kill"])
                    players_openingFirstKillInWonRounds.append(stats_aux["First kill in won rounds"])

    """################################
        Ensuring only 10 player's data are gathered
       ################################"""
    m+=1
    if m>=10:
        break


"""################################
    CSVing
   ################################"""


df = pd.DataFrame({'Date':date,'Team1':team1,'Team2':team2,'Tournament':tournament})

players_auxdf = pd.DataFrame({
                                      'Team1'                                     : players_team1,
                                      'Team2'                                     : players_team2,
                                      'Player Team'                               : players_team,
                                      'Player'                                    : players,
                                      'Overall Kills'                             : players_overallKills,
                                      'Overall Deaths'                            : players_overallDeaths,
                                      'Overal Kill / Death'                       : players_overallKill_Death,
                                      'Overall Kill / Round'                      : players_overallKill_Round,
                                      'Overall Rounds with Kills'                 : players_overallRoundsWithKills,
                                      'Overall Kill - Death Diff'                 : players_overallKillDeathDiff,
                                      'Opening Total Kills'                       : players_openingTotalKills,
                                      'Opening Total Deaths'                      : players_openingTotalDeaths,
                                      'Opening Kill Ratio'                        : players_openingKillRatio,
                                      'Opening Kill rating'                       : players_openingKillRating,
                                      'Opening Team win percent after 1st kill'   : players_openingTeamWinPercentAfterFirstKill,
                                      'Opening 1st kill in won rounds'            : players_openingFirstKillInWonRounds})

"""
This was used to generate some of the CSV files!
make sure you change the directory if you are
gonna test this as to not overwrite any of the data
"""
df.to_csv('upcoming_sat_matches_NO_OVERWRITE.csv',index=False)
players_auxdf.to_csv('upcoming_sat_players_NO_OVERWRITE.csv',index=False)
