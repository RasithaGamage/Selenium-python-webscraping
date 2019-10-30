import csv


class BattingData:
    def __init__(self, match_id, player_name, player_link, runs, balls, minutes, _4s, _6s, strike_rate, commentary,
                 dismissed_by, country,position):
        self.match_id = match_id
        self.player_name = player_name
        self.player_link = player_link
        self.runs = runs
        self.balls = balls
        self._4s = _4s
        self._6s = _6s
        self.minutes = minutes
        self.strike_rate = strike_rate
        self.commentary = commentary
        self.dismissed_by = dismissed_by
        self.country = country
        self.position = position

    def saveRecord(self):
        try:
            with open('./CricMatchBattingData.csv', 'a', newline='', encoding='utf-8') as outfile:
                csvWriter = csv.writer(outfile)
                csvWriter.writerow(
                    [self.match_id, self.player_name, self.country, self.player_link, self.position, self.dismissed_by, self.commentary, self.runs,
                     self.balls, self.minutes, self._4s, self._6s, self.strike_rate])
            outfile.close()
        except Exception as e:
            print(e)
