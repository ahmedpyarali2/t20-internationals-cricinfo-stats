# coding=utf-8

from scraper import crawler
import pandas as pd

if __name__ == '__main__':
    c = crawler()
    c.start()
    print(vars(c))
    matches = pd.DataFrame({'m_id' : c.m_id, 'date': c.date, 'conditions': c.conditions,
                            'team1': c.team1, 'team2': c.team2, 'toss' : c.toss, 'winner' : c.winner,
                            'margin' : c.margin, 'ground' : c.ground, 'team1_total' : c.team1_total,
                            'team2_total' : c.team2_total, 'team1_runs_per_over' : c.team1_rpo, 'team2_runs_per_over' : c.team2_rpo,
                            'team1_avg_sr' : c.team1_avg_sr, 'team2_avg_sr' : c.team2_avg_sr, 'team1_avg_ecn': c.team1_avg_ecn,
                            'team2_avg_ecn' : c.team2_avg_ecn, 'team1_maidens' : c.team1_maiden, 'team2_maidens' : c.team2_maiden,
                            'team1_6s' : c.team1_6s, 'team2_6s' : c.team2_6s, 'team1_4s' : c.team1_4s, 'team2_4s' : c.team2_4s})

    columns = ['m_id', 'date', 'conditions', 'team1', 'team2', 'toss', 'winner', 'margin', 'ground', 'team1_total', 'team2_total', 'team1_runs_per_over', \
                'team2_runs_per_over', 'team1_avg_sr', 'team2_avg_sr', 'team1_avg_ecn', 'team2_avg_ecn', 'team1_maidens', 'team2_maidens', \
                'team1_6s', 'team2_6s', 'team1_4s', 'team2_4s']

    matches.to_csv('matches.csv', columns=columns, index=False)
