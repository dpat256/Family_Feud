# Family Feud Graphical Game Scoreboard Object
# Author: D. Depatie
# Date: 12/3/2022

class scoreboard():
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.points = 0
        self.score1 = 0
        self.score2 = 0
        self.strikes1 = 0
        self.strikes2 = 0
        self.active = ""
        self.winner = False

    def addPoints(self, add):
        self.points += add
