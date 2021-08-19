from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import re
import scipy.linalg as spla
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

"""################################
    Starting Webdriver and defining variables
   ################################"""

driver = webdriver.Chrome(executable_path=r'C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe')


""" The following variables are lists of their respective
    values, which are in the end formed into a data frame
            and saved as a CSV file """

""" Match Metadata, all obvious variables with the
    link to the statistics associated with the match """

date = []
team1 = []
team2 = []
final_result1 = []
final_result2 = []
tournament = []
link_stats = []


""" Match Specific Player Data """

players = []        #player name

players_rating = []
players_adr = []    #prediction
players_kast = []
players_impact = []
players_kd = []
players_kpr = []

players_date = []
players_tournament = []
players_team = []
players_map = []

players_team1 = []
players_team2 = []
players_final_result1 = []
players_final_result2 = []

""" Player Averages, potentially crossed by a map column """

players_overallRating = []
players_overalladr = []             ## PREDICTION
players_overallkast = []
players_overallImpact = []
players_overallKill_Death = []
players_overallKill_Round = []







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
'kd_diff',
'ADR',
'KAST',
'Rating'
'Map',
'Overall Kill / Death',
'Overall Kill - Death Diff',
'Ovreall ADR'
'Overall Kill / Round',
'Overall Assists / Round',
'Overall Deaths / Round'
'Overall Rating',
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

#OVERRIDE
# Allows user input of matchlinks


"""
# Below code can access a list of results and index all of them
match_links = []
#driver.get('https://www.hltv.org/results?offset='+str(page_num))# MAIN PAGE
driver.get("https://www.hltv.org/results?team=4608")
content=driver.page_source
sauce=BeautifulSoup(content)

first_count = 0

for div in sauce.findAll('div', attrs={'class':'results'}):
    for a in div.findAll('a', attrs={'class':'a-reset'}):
        if(first_count < 15):
            link = a['href']
            match_links.append(link)
            first_count += 1

for match in match_links:
    print("'" + match + "',")

#match_links = blast_prem_matches
"""
progress = 0

m = 0

match_links = [ '/matches/2345189/natus-vincere-vs-mad-lions-iem-beijing-haidian-2020-europe' ]


"""################################
    Iterating though the matches
   ################################"""

def initial_stage(match_link):

    """################################
        Building Match Information Database
       ################################"""

    url = 'https://www.hltv.org' + match_links
    driver.get(url)
    page = driver.page_source
    sauce = BeautifulSoup(page)



for match in match_links:
    if("/matches/" in match) and ("vitality" not in match): #this AND'd match causes random bugs, stay away!



        """################################
            Building Match Information Database
           ################################"""

        url = 'https://www.hltv.org' + match
        driver.get(url)
        page = driver.page_source
        sauce = BeautifulSoup(page)

        """################################
            Finding links to detailed player statistics
           ################################"""

        sauce_smallstats = sauce.findAll('div',attrs={'class':'small-padding stats-detailed-stats'})

        for div_stats in sauce_smallstats:
            for a in div_stats.findAll('a'):
                link_stat = a['href']
                break

            url = 'https://www.hltv.org' + link_stat[0:15] + "performance/" + link_stat[15:]
            link_stats.append(url)



        if sauce_smallstats == "":
            link_stats.append("")


        """################################
            Finding relevant match data on matchpage
           ################################"""

        sauce_page  = sauce.findAll('div', attrs = {'class' : 'match-page'})
        sauce_team1 = sauce.findAll('div', attrs = {'class' : 'team1-gradient'})
        sauce_team2 = sauce.findAll('div', attrs = {'class' : 'team2-gradient'})
        sauce_all = sauce.findAll('div', attrs = {'id' : 'all-content'})

        for div_match_page in sauce_page:
            page_date = div_match_page.find('div',attrs={'class':'date'})
            page_tournament = div_match_page.find('div',attrs={'class':'event text-ellipsis'})
            date.append(page_date.text)
            tournament.append(page_tournament.text)

        for div_team1 in sauce_team1:
            page_team1 = div_team1.find('div',attrs={'class':'teamName'})
            page_result1 = div_team1.find('div',attrs={'class':['won','lost','tie']})
            team1.append(page_team1.text)
            final_result1.append(page_result1.text)

        for div_team2 in sauce_team2:
            page_team2 = div_team2.find('div',attrs={'class':'teamName'})
            page_result2 = div_team2.find('div',attrs={'class':['won','lost','tie']})
            team2.append(page_team2.text)
            final_result2.append(page_result2.text)

        """################################
            Finding which maps were played in
            a match, and IDs them for later use
           ################################"""
        print("finding maps")
        maps = []
        mapsID = []

        for div in sauce.findAll('div', attrs={'class':'stats-menu-link'}):
            map1 = div.findAll('div')
            maps.append(map1[-1].text)
            mapsID.append(map1[-1]['id'])

        player_count = 0

        """################################
            Building Player Database
           ################################"""

        for div_all in sauce_all:
            if( player_count < 10):
                """################################
                    Defining match-specific values, counts, and iterators
                   ################################"""
                print('player teams finding')
                team = page_team1.text
                t1 = page_team1.text
                t2 = page_team2.text

                team_count = 0
                map_count = 0
                j = 0

                """################################
                    Iterating through the statistics table
                   ################################"""
                sauce_tables = sauce.findAll(class_='table totalstats')
                #sauce_tables = sauce.findAll('div',attrs={'class','highlighted-player'})
                #print(sauce_tables)
                #for config in sauce_tables:
                #    print(config)


                for table in sauce_tables:
                    print("finding main statistics")
                    rows = table.find_all('tr')[1:]
                    for row in rows:

                        """################################
                            Appending relevant data
                           ################################"""

                        print("PULLING PLAYER STATS ", url)
                        cell = [i.text for i in row.find_all('td')]
                        print(cell)
                        players.append(cell[0].split('\n')[2])
                        print(cell[0].split('\n')[2])
                        players_kd.append(cell[1])
                        print(cell[1])
                        #players_kd_diff.append(cell[2])
                        print(cell[2])
                        players_adr.append(cell[3])
                        print(cell[3])
                        players_kast.append(cell[4])
                        print(cell[4])
                        players_rating.append(cell[5])
                        print(cell[5])
                        players_date.append(page_date.text)
                        players_team1.append(page_team1.text)
                        players_team2.append(page_team2.text)
                        players_final_result1.append(page_result1.text)
                        players_final_result2.append(page_result2.text)
                        players_tournament.append(page_tournament.text)
                        players_team.append(team)
                        players_map.append(maps[j])



                        """################################
                            Some logic that ensures players have correct
                            team labels, and map labels for specific games
                        ################################"""
                        print("map logic")
                        map_count += 1
                        team_count += 1
                        if(map_count == 10):
                            j += 1
                            map_count = 0

                        if(team_count == 5):
                            if(team == t1):
                                team = t2
                                team_count = 0
                            else:
                                team = t1
                                team_count = 0

                """################################
                    Accessing Advanced player statistics
                   ################################"""
                print("ono advanced data_")

                driver.get(url)
                content = driver.page_source
                sauce = BeautifulSoup(content)

                print("REDDIT SCRIPT")
                final_dict = {}
                for player in sauce.find_all('div',{'class':'highlighted-player'}):
                    name = player.find('a').text #get the players names from the top of the chart and save it in the di
                    graph_data = json.loads(player.find('div',{'class':'graph'})['data-fusionchart-config']) #find the graph data, load it into a json object which we can then loop through below

                    stats ={}
                    for point in graph_data['dataSource']['data']: #loop through each stat
                        stats[point['label']] = point['displayValue'] #save the stat label as a key in our new dict with the value being what is displayed on the graph
                        final_dict[name] = stats


                for gamer in final_dict.keys():
                    print(gamer)
                    for stat in final_dict[gamer]:
                        print(stat,final_dict[gamer][stat])
                        print('--')
                print("END REDDIT SCRIPT")

                for table in sauce.findAll(class_='stats-table'):
                    rows = table.find_all('tr')[1:]

                    for row in rows:
                        stats_aux = {}
                        link_player = [i['href'] for i in row.find_all('a')]

                        """################################
                            Transforming date into hltv.org's URL format
                           ################################"""

                        date_stats = page_date.text
                        date_split = date_stats.split(' ')

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
                            Collecting data for each map played,
                            along with statistics across all maps
                           ################################"""

                        for map in maps:

                            url = 'https://www.hltv.org' + link_player[0][:15] + link_player[0][15:] + '?startDate=2013-01-01&endDate=' + year + '-' + month + '-' + day + map_dict[map]
                            driver.get(url)
                            content = driver.page_source
                            sauce = BeautifulSoup(content)

                            """################################
                                finding relevant data, stored in stats_aux
                               ################################"""
                            stats_dictionary = {}

                            sauce_player = sauce.findAll('div',attrs={'class','summaryStatBreakdownRow'})
                            for div_player in sauce_player:


                                sauce_statistics = div_player.findAll('div',attrs={'class','summaryStatBreakdown'})
                                for stat in sauce_statistics:


                                    sauce_statistic_names = div_player.findAll('div',attrs={'class','summaryStatBreakdownSubHeader'})
                                    for div_stat_name in sauce_statistic_names:
                                        print(".TEXT", div_stat_name.text[0:10])






                            """################################
                                Appending
                               ################################"""





                            #players_overallKills.append(stats_aux["Total kills"])
                            #players_overallDeaths.append(stats_aux["Deaths"])


                            player_count += 1



        """################################
            Creating aux DataFrame
            this is used to collect all data for a given match, and
            is then appended to the master playersdf data frame
           ################################"""
        players_auxdf = pd.DataFrame({
                                              'Date'                                      : players_date,
                                              'Team1'                                     : players_team1,
                                              'Team2'                                     : players_team2,
                                              'Final Result 1'                            : players_final_result1,
                                              'Final Result 2'                            : players_final_result2,
                                              'Tournament'                                : players_tournament,
                                              'Player Team'                               : players_team,
                                              'Player'                                    : players,
                                              'KD'                                        : players_kd,
                                              'kd_diff'                                       : players_kd_diff,
                                              'ADR'                                      : players_adr,
                                              'KAST'                                        : players_kast,
                                              'Rating'                                  : players_rating,
                                              'Map'                                       : players_map,
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




        playersdf = pd.concat([ playersdf , players_auxdf ])
        playersdf.to_csv(r'C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\BLAST_fall_series_players.csv',index=False)


        """################################
            Reseting player data lists for the next match
           ################################"""
        print("Processed ", match)
        progress += 1

        total = str(len(match_links))
        complete = str(progress)
        percent = str( float(progress/len(match_links))*100 )
        ratio_str = complete + "/" + total + " matches processed......" + " (" + percent + "% complete)"
        print(ratio_str)

        players = []
        players_kd = []
        players_kd_diff = []
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


"""################################
    Creating final match information
    and player information CSV files
   ################################"""

df = pd.DataFrame({ 'Date'          : date,
                    'Team1'         : team1,
                    'Team2'         : team2,
                    'Final Result 1': final_result1,
                    'Final Result 2': final_result2,
                    'Tournament'    : tournament,
                    'Link Stats'    : link_stats        })


"""
This was used to generate some of the CSV files!
make sure you change the directory if you are
gonna test this as to not overwrite any of the data
"""
print("csv'd")
df.to_csv(r'C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\test_matches.csv',index=False)
playersdf.to_csv(r'C:\Users\matth\Documents\Atom\397A Homeworks\Final Project\test_players.csv',index=False)
