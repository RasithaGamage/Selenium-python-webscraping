
class MatchData:
    match_id =""
    match_title = ""
    mom = ""
    match_result=""
    match_win = ""
    ground_link = ""
    match_link = ""

    def __init__(self, match_id, match_title, ground_link, match_link, mom, match_result, match_win):
        self.match_id = match_id
        self.match_link = match_link
        self.ground_link = ground_link
        self.match_title = match_title
        self.mom = mom
        self.match_result = match_result
        self.match_win = match_win

