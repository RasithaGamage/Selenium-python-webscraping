from typing import Any


class MatchData:
    match_id =""
    match_title = ""
    mom = ""
    match_result=""
    match_win = ""

    def __init__(self, match_id, match_title, mom, match_result, match_win):
        self.match_id = match_id
        self.match_title = match_title
        self.mom = mom
        self.match_result = match_result
        self.match_win = match_win

    first_inning = ""

    second_inning = ""

