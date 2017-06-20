# coding=utf-8

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import time


class crawler:
    def __init__(self):
        self.home = 'http://stats.espncricinfo.com'
        self.m_id, self.date, self.conditions, self.team1, self.team2, self.toss, self.winner, self.margin, self.ground, self.team1_total, \
            self.team2_total,self.team1_rpo, self.team2_rpo, self.team1_avg_sr, self.team2_avg_sr, self.team1_avg_ecn, self.team2_avg_ecn, \
            self.team1_wickets, self.team2_wickets, self.team1_maiden, self.team2_maiden, self.team1_6s, self.team2_6s, self.team1_4s, self.team2_4s = \
            ([] for i in range(25))


    def start(self):
        self.years = np.arange(2005, 2018)
        self.counter = 0
        for yr in self.years:
            payload = {'class' : 3, 'id' : yr, 'type' : 'year'}
            r = requests.get("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html", params=payload)
            html = r.text
            self.__bs_extract(html)
            matches = pd.DataFrame({'m_id' : self.m_id, 'date': self.date, 'conditions': self.conditions,
                                    'team1': self.team1, 'team2': self.team2, 'toss' : self.toss, 'winner' : self.winner,
                                    'margin' : self.margin, 'ground' : self.ground, 'team1_total' : self.team1_total,
                                    'team2_total' : self.team2_total, 'team1_runs_per_over' : self.team1_rpo, 'team2_runs_per_over' : self.team2_rpo,
                                    'team1_avg_sr' : self.team1_avg_sr, 'team2_avg_sr' : self.team2_avg_sr, 'team1_avg_ecn': self.team1_avg_ecn,
                                    'team2_avg_ecn' : self.team2_avg_ecn, 'team1_maidens' : self.team1_maiden, 'team2_maidens' : self.team2_maiden,
                                    'team1_6s' : self.team1_6s, 'team2_6s' : self.team2_6s, 'team1_4s' : self.team1_4s, 'team2_4s' : self.team2_4s})

            columns = ['m_id', 'date', 'conditions', 'team1', 'team2', 'toss', 'winner', 'margin', 'ground', 'team1_total', 'team2_total', 'team1_runs_per_over', \
                        'team2_runs_per_over', 'team1_avg_sr', 'team2_avg_sr', 'team1_avg_ecn', 'team2_avg_ecn', 'team1_maidens', 'team2_maidens', \
                        'team1_6s', 'team2_6s', 'team1_4s', 'team2_4s']
            matches.to_csv('matches-'+str(yr)+'.csv' , columns=columns, index=False)
            time.sleep(5)
            self.__init__()

    def __bs_extract(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", {'class' : 'engineTable'}).find('tbody')
        for row in table.findAll('tr'):
            cols = row.findAll('td')
            print("Match ID: " + str(self.counter))
            if cols[3].text.strip() != '':
                self.m_id.append(self.counter)
                self.team1.append(cols[0].text.strip())
                self.team2.append(cols[1].text.strip())
                self.winner.append(cols[2].text.strip())
                self.margin.append(cols[3].text.strip())
                self.date.append(cols[5].text.strip())
                self.__fetch_scoreboard(self.home + cols[6].find('a')['href'])
            self.counter += 1
            time.sleep(2)

    def __fetch_scoreboard(self, href):
        t1, t2 = self.team1[-1], self.team2[-1]
        r = requests.get(href)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        spans = soup.find('div', {'class' : 'space-top-bottom-10'}).findAll('span', {'class' : 'normal'})
        self.toss.append(spans[0].text.strip())
        self.ground.append(soup.select('div.large-7.medium-7.columns.text-right.match-information')[0].findAll('div', {'class' : 'space-top-bottom-5'})[1].find('a').text.strip())
        cond = soup.select('div.row.brief-summary')[0].select('div.medium-7')[0].select('div.space-top-bottom-5')[2].text.strip().split(' - ')
        if len(cond) > 1:
            self.conditions.append(cond[1].split(' ')[0])
        else:
            self.conditions.append('?')
        batting_tables = soup.find('div', {'class' : 'full-scorecard-block'}).select('div.row')[2].select('div.large.20.columns')[0].findAll('table', {'class' : 'batting-table'})
        bowling_tables = soup.find('div', {'class' : 'full-scorecard-block'}).select('div.row')[2].select('div.large.20.columns')[0].findAll('table', {'class' : 'bowling-table'})
        tr = batting_tables[0].find('tr').findAll('th')
        if t1.lower() not in tr[1].text.strip().lower():
            t1_total, t1_rpo, t1_wickets, t1_sr, t1_4, t1_6, t1_ecn, t1_maid = 0, 0, 0, [], 0, 0, [], 0
            t2_total, t2_rpo, t2_wickets, t2_sr, t2_4, t2_6, t2_ecn, t2_maid = 0, 0, 0, [], 0, 0, [], 0
            table = batting_tables[1]
            self.team1_total.append(float(table.findAll('tr')[-1].findAll('td')[3].text))
            self.team1_rpo.append(float(table.findAll('tr')[-1].findAll('td')[4].text.strip().split('(')[1].split(' ')[0]))
            t1_wickets = (table.findAll('tr')[-1].findAll('td')[2].text.strip().split('(')[1].split(';')[0])
            if t1_wickets == 'all out':
                self.team1_wickets.append(10)
            else:
                self.team1_wickets.append(float(t1_wickets.split(' ')[0]))
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                try:
                    if (cols[8].text == '-' or cols[8].text == ''):
                        t1_sr.append(0.0)
                    else:
                        t1_sr.append(float(cols[8].text))
                except:
                    if (cols[7].text == '-' or cols[7].text == ''):
                        t1_sr.append(0.0)
                    else:
                        t1_sr.append(float(cols[7].text.strip()))

                try:
                    t1_4 += int(cols[6].text)
                    t1_6 += int(cols[7].text)
                except:
                    try:
                        t1_4 += int(cols[5].text)
                        t1_6 += int(cols[6].text)
                    except:
                        pass

            self.team1_4s.append(t1_4)
            self.team1_6s.append(t1_6)
            self.team1_avg_sr.append(np.mean(np.array(t1_sr)))
            table = bowling_tables[0]
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                t1_maid += int(cols[3].text)
                t1_ecn.append(float(cols[6].text))

            self.team1_maiden.append(t1_maid)
            self.team1_avg_ecn.append(np.mean(np.array(t1_ecn)))

            table = batting_tables[0]
            self.team2_total.append(float(table.findAll('tr')[-1].findAll('td')[3].text))
            self.team2_rpo.append(float(table.findAll('tr')[-1].findAll('td')[4].text.strip().split('(')[1].split(' ')[0]))
            t2_wickets = (table.findAll('tr')[-1].findAll('td')[2].text.strip().split('(')[1].split(';')[0])
            if t2_wickets == 'all out':
                self.team1_wickets.append(10)
            else:
                self.team2_wickets.append(float(t2_wickets.split(' ')[0]))
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                try:
                    if (cols[8].text == '-' or cols[8].text == ''):
                        t2_sr.append(0.0)
                    else:
                        t2_sr.append(float(cols[8].text))
                except:
                    if (cols[7].text == '-' or cols[7].text == ''):
                        t2_sr.append(0.0)
                    else:
                        t2_sr.append(float(cols[7].text))

                try:
                    t2_4 += int(cols[6].text)
                    t2_6 += int(cols[7].text)
                except:
                    try:
                        t1_4 += int(cols[5].text)
                        t1_6 += int(cols[6].text)
                    except:
                        pass

            self.team2_4s.append(t2_4)
            self.team2_6s.append(t2_6)
            self.team2_avg_sr.append(np.mean(np.array(t2_sr)))
            table = bowling_tables[1]
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                t2_maid += int(cols[3].text)
                t2_ecn.append(float(cols[6].text))

            self.team2_maiden.append(t2_maid)
            self.team2_avg_ecn.append(np.mean(np.array(t2_ecn)))

        else:
            t1_total, t1_rpo, t1_wickets, t1_sr, t1_4, t1_6, t1_ecn, t1_maid = 0, 0, 0, [], 0, 0, [], 0
            t2_total, t2_rpo, t2_wickets, t2_sr, t2_4, t2_6, t2_ecn, t2_maid = 0, 0, 0, [], 0, 0, [], 0
            table = batting_tables[0]
            self.team1_total.append(float(table.findAll('tr')[-1].findAll('td')[3].text))
            self.team1_rpo.append(float(table.findAll('tr')[-1].findAll('td')[4].text.strip().split('(')[1].split(' ')[0]))
            t1_wickets = (table.findAll('tr')[-1].findAll('td')[2].text.strip().split('(')[1].split(';')[0])
            if t1_wickets == 'all out':
                self.team1_wickets.append(10)
            else:
                self.team1_wickets.append(float(t1_wickets.split(' ')[0]))
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                try:
                    if (cols[8].text == '-' or cols[8].text == ''):
                        t1_sr.append(0.0)
                    else:
                        t1_sr.append(float(cols[8].text))
                except:
                    if (cols[7].text == '-' or cols[7].text == ''):
                        t1_sr.append(0.0)
                    else:
                        t1_sr.append(float(cols[7].text))

                try:
                    t1_4 += int(cols[6].text)
                    t1_6 += int(cols[7].text)
                except:
                    try:
                        t1_4 += int(cols[5].text)
                        t1_6 += int(cols[6].text)
                    except:
                        pass

            self.team1_4s.append(t1_4)
            self.team1_6s.append(t1_6)
            self.team1_avg_sr.append(np.mean(np.array(t1_sr)))
            table = bowling_tables[1]
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                t1_maid += int(cols[3].text)
                t1_ecn.append(float(cols[6].text))

            self.team1_maiden.append(t1_maid)
            self.team1_avg_ecn.append(np.mean(np.array(t1_ecn)))

            table = batting_tables[1]
            self.team2_total.append(float(table.findAll('tr')[-1].findAll('td')[3].text))
            self.team2_rpo.append(float(table.findAll('tr')[-1].findAll('td')[4].text.strip().split('(')[1].split(' ')[0]))
            t2_wickets = (table.findAll('tr')[-1].findAll('td')[2].text.strip().split('(')[1].split(';')[0])
            if t2_wickets == 'all out':
                self.team2_wickets.append(10)
            else:
                self.team2_wickets.append(float(t2_wickets.split(' ')[0]))
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                try:
                    if (cols[8].text == '-' or cols[8].text == ''):
                        t2_sr.append(0.0)
                    else:
                        t2_sr.append(float(cols[8].text))
                except:
                    if (cols[7].text == '-' or cols[7].text == ''):
                        t2_sr.append(0.0)
                    else:
                        t2_sr.append(float(cols[7].text))

                try:
                    t2_4 += int(cols[6].text)
                    t2_6 += int(cols[7].text)
                except:
                    try:
                        t1_4 += int(cols[5].text)
                        t1_6 += int(cols[6].text)
                    except:
                        pass

            self.team2_4s.append(t2_4)
            self.team2_6s.append(t2_6)
            self.team2_avg_sr.append(np.mean(np.array(t2_sr)))
            table = bowling_tables[0]
            tr = table.findAll('tr', {'class' : None})
            for row in tr:
                cols = row.findAll('td')
                t2_maid += int(cols[3].text)
                t2_ecn.append(float(cols[6].text))

            self.team2_maiden.append(t2_maid)
            self.team2_avg_ecn.append(np.mean(np.array(t2_ecn)))
