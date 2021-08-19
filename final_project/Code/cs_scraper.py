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

"""################################
    Starting Webdriver and defining variables
   ################################"""

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

players_overallKAST = []

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

#OVERRIDE
# Allows user input of matchlinks

saturday_matchlinks = ["/matches/2345628/furia-vs-astralis-dreamhack-masters-winter-2020-europe"]

blast_prem_matches = [  '/matches/2345221/natus-vincere-vs-vitality-iem-beijing-haidian-2020-europe',
                        '/matches/2345219/g2-vs-natus-vincere-iem-beijing-haidian-2020-europe',
                        '/matches/2345216/astralis-vs-natus-vincere-iem-beijing-haidian-2020-europe',
                        '/matches/2345207/natus-vincere-vs-spirit-iem-beijing-haidian-2020-europe',
                        '/matches/2345204/natus-vincere-vs-complexity-iem-beijing-haidian-2020-europe',
                        '/matches/2345189/natus-vincere-vs-mad-lions-iem-beijing-haidian-2020-europe',
                        '/matches/2344822/og-vs-natus-vincere-blast-premier-fall-series-2020',
                        '/matches/2344821/natus-vincere-vs-nip-blast-premier-fall-series-2020',
                        '/matches/2344819/natus-vincere-vs-og-blast-premier-fall-series-2020',
                        '/matches/2344817/natus-vincere-vs-nip-blast-premier-fall-series-2020',
                        '/matches/2344446/natus-vincere-vs-spirit-iem-new-york-2020-cis',
                        '/matches/2344442/virtuspro-vs-natus-vincere-iem-new-york-2020-cis',]

navi_matches = []
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
match_links = []
match_links = navi_matches

progress = 0

m = 0

match_links = [ '/matches/2345189/natus-vincere-vs-mad-lions-iem-beijing-haidian-2020-europe' ]


"""################################
    Iterating though the matches
   ################################"""

for match in match_links:
    if("/matches/" in match) and ("vitality" not in match): #this AND'd match causes random bugs, stay away!



        """################################
            Building Match Information Database
           ################################"""

        url = 'https://www.hltv.org/' + match
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

            url = 'https://www.hltv.org/' + link_stat
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

                for table in sauce_tables:

                    rows = table.find_all('tr')[1:]
                    for row in rows:

                        """################################
                            Appending relevant data
                           ################################"""


                        cell = [i.text for i in row.find_all('td')]
                        players.append(cell[0].split('\n')[2])
                        players_kd.append(cell[1])
                        players_adr.append(cell[2])
                        players_kast.append(cell[3])
                        players_rating.append(cell[4])
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
                    Accessing historic player statistics
                   ################################"""

                driver.get(url)
                content = driver.page_source
                sauce = BeautifulSoup(content)

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

                            url = 'https://www.hltv.org' + link_player[0][:15] + 'individual/' + link_player[0][15:] + '?startDate=2013-01-01&endDate=' + year + '-' + month + '-' + day + map_dict[map]
                            driver.get(url)
                            content = driver.page_source
                            sauce = BeautifulSoup(content)

                            """################################
                                finding relevant data, stored in stats_aux
                               ################################"""

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
                            player_count += 1

        print(len(players_date))
        print(len(players_team1))
        print(len(players_team2))
        print(len(players_final_result1))
        print(len(players_final_result2))
        print(len(players_tournament))
        print(len(players_team))
        print(len(players))
        print(len(players_kd))
        print(len(players_adr))
        print(len(players_kast))
        print(len(players_rating))
        print(len(players_map))
        print(len(players_overallKills))
        print(len(players_overallDeaths))
        print(len(players_overallKill_Death))
        print(len(players_overallKill_Round))
        print(len(players_overallRoundsWithKills))
        print(len(players_overallKillDeathDiff))
        print(len(players_openingTotalKills))
        print(len(players_openingTotalDeaths))
        print(len(players_openingKillRatio))
        print(len(players_openingKillRating))
        print(len(players_openingTeamWinPercentAfterFirstKill))
        print(len(players_openingFirstKillInWonRounds))

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
                                              'ADR'                                       : players_adr,
                                              'KAST'                                      : players_kast,
                                              'Rating'                                    : players_rating,
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
