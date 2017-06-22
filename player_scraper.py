# coding=utf-8

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests, time



class player_crawler:
    def  __init__(self):
        self.home = 'http://www.espncricinfo.com'
        self.counter = 1
        self.id = []
        self.team, self.names, self.batting_styles, self.bowling_styles, self.role, self.matches, self.batting_innings, self.nos, self.batting_runs, \
            self.bowling_innings, self.balls, self.bowling_runs, self.wickets, self.bbi, self.bbm, self.bowling_ave, self.economy, self.bowling_sr, \
            self.hs, self.batting_ave, self.bf, self.batting_sr, self.hundreds, self.fiftys, self.fours, self.sixes, self.catch, self.stumps, \
            self.four_wkts, self.five_wkts, self.ten = ([] for i in range(31))
            
    def start(self):

        for i in np.arange(1, 11):
            r = requests.get('http://www.espncricinfo.com/ci/content/player/index.html?country=' + str(i))
            soup = BeautifulSoup(r.text, 'lxml')
            table = soup.select('table.playersTable')[0]

            for row in table.findAll('tr'):
                for col in row.findAll('td'):
                    self.__extract_player(self.home + col.find('a')['href'])
                    self.id.append(self.counter)
                    self.counter += 1
                    print(self.names[-1])
                    time.sleep(3)
            time.sleep(5)


        df = pd.DataFrame({ 'id' : self.id', team' : self.team, 'name' : self.names, 'role' : self.role, 'batting style' : self.batting_styles, 'bowling style' : self.bowling_styles, 'matches played' : self.matches, 'innings batted' : self.batting_innings,
        'NO' : self.nos, 'runs scored': self.batting_runs, 'hs' : self.hs, 'batting average' : self.batting_ave, 'bf' : self.bf, 'batting strike rate' : self.batting_sr, '100' : self.hundreds, '50' : self.fiftys, '4s' : self.fours, '6s' : self.sixes,
        'ct' : self.catch, 'st' : self.stumps, 'innings bowled' : self.bowling_innings, 'balls bowled' : self.balls, 'runs conced' : self.bowling_runs, 'wickets taken' : self.wickets, 'bbi' : self.bbi, 'bbm' : self.bbm, 'bowling average' : self.bowling_ave,
        'economy' : self.economy, 'bowling strike rate' : self.bowling_sr, '4w' : self.four_wkts, '5w' : self.five_wkts, '10' : self.ten })

        columns = ['counter', 'team', 'name', 'role', 'batting style', 'bowling style', 'matches played', 'innings batted',  'NO', 'runs scored', 'hs', 'batting average', 'bf', 'batting strike rate', '100', '50', '4s', '6s', 'ct', 'st', \
        'innings bowled', 'balls bowled', 'runs conced', 'wickets taken', 'bbi', 'bbm', 'bowling average', 'economy', 'bowling strike rate', '4w', '5w', '10']
        print(columns)

        df.to_csv('data/player_data/t20-players.csv', columns = columns, index=False)


    def __extract_player(self, href):

        r = requests.get(href)
        soup = BeautifulSoup(r.text, 'lxml')
        # print(soup.encode('utf-8'))

        self.team.append(soup.select('h3.PlayersSearchLink')[0].text.strip())

        player_info = soup.find('div', {'class' : 'pnl490M'})
        self.names.append(player_info.find('h1').text.strip())
        self.role.append(player_info.find('div', style="float:left; width:310px; color:#666666; font-size:11px;").select('p')[5].select('span')[0].text.strip())
        try:
            self.batting_styles.append(player_info.find('div', style="float:left; width:310px; color:#666666; font-size:11px;").select('p')[6].select('span')[0].text.strip())
        except:
            self.batting_styles.append('-')
        try:
            self.bowling_styles.append(player_info.find('div', style="float:left; width:310px; color:#666666; font-size:11px;").select('p')[7].select('span')[0].text.strip())
        except:
            self.bowling_styles.append('-')
        batting_table, bowling_table = player_info.select('table.engineTable')[0].select('tbody')[0], player_info.select('table.engineTable')[1].select('tbody')[0]

        batting_table = batting_table.findAll('tr')[-1].findAll('td')
        self.matches.append(batting_table[1].text.strip())
        self.batting_innings.append(batting_table[2].text.strip())
        self.nos.append(batting_table[3].text.strip())
        self.batting_runs.append(batting_table[4].text.strip())
        self.hs.append(batting_table[5].text.strip())
        self.batting_ave.append(batting_table[6].text.strip())
        self.bf.append(batting_table[7].text.strip())
        self.batting_sr.append(batting_table[8].text.strip())
        self.hundreds.append(batting_table[9].text.strip())
        self.fiftys.append(batting_table[10].text.strip())
        self.fours.append(batting_table[11].text.strip())
        self.sixes.append(batting_table[12].text.strip())
        self.catch.append(batting_table[13].text.strip())
        self.stumps.append(batting_table[14].text.strip())

        bowling_table = bowling_table.findAll('tr')[-1].findAll('td')
        self.bowling_innings.append(bowling_table[2].text.strip())
        self.balls.append(bowling_table[3].text.strip())
        self.bowling_runs.append(bowling_table[4].text.strip())
        self.wickets.append(bowling_table[5].text.strip())
        self.bbi.append(bowling_table[6].text.strip())
        self.bbm.append(bowling_table[7].text.strip())
        self.bowling_ave.append(bowling_table[8].text.strip())
        self.economy.append(bowling_table[9].text.strip())
        self.bowling_sr.append(bowling_table[10].text.strip())
        self.four_wkts.append(bowling_table[11].text.strip())
        self.five_wkts.append(bowling_table[12].text.strip())




c = player_crawler()
c.start()
