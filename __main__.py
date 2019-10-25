from MatchData import MatchData

# "http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year"
# change id=2010 into desired year to get required data

# match = MatchData("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year")
match = MatchData("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;type=year")
del match


