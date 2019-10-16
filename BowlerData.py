import csv

class BowlerData:
    def __init__(self, match_id, player_name_bowler, player_link_bowler, overs, maidens, runs_bowler, wickets, econ, dot_balls, _4s_bowler, _6s_bowler, wides, no_balls):
        self.match_id = match_id
        self.player_name_bowler = player_name_bowler
        self.player_link_bowler = player_link_bowler
        self.overs = overs
        self.maidens = maidens
        self.runs_bowler = runs_bowler
        self.wickets = wickets
        self.econ = econ
        self.dot_balls = dot_balls
        self._4s_bowler = _4s_bowler
        self._6s_bowler = _6s_bowler
        self.wides = wides
        self.no_balls = no_balls

    def saveRecord(self):
        with open('./CricMatchBowlingData.csv', 'a', newline='', encoding='utf-8') as outfile:
            csvWriter = csv.writer(outfile)
            csvWriter.writerow(
                [self.match_id, self.player_name_bowler, self.player_link_bowler, self.overs, self.maidens, self.runs_bowler, self.wickets, self.econ,
                 self.dot_balls, self._4s_bowler, self._6s_bowler, self.wides, self.no_balls])
        outfile.close()