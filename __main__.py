import csv
from telnetlib import EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from MatchData import MatchData

def getInningData(inning):
    batsmen_list = inning.find_element_by_class_name("scorecard-section") #for batsmens
    batsmen_score = batsmen_list.find_elements_by_class_name("flex-row")
    for post2 in batsmen_score:
        check_availability = ""
        try:
            check_availability = post2.find_element_by_class_name("batsmen").find_element_by_class_name("batsmen").text
        except Exception:
            None

        if len(check_availability) > 0:
            try:
                batsman = post2.find_element_by_class_name("batsmen")
                score_record = batsman.find_elements_by_class_name("runs")
                player_name = batsman.find_element_by_class_name("batsmen").text
                player_link = batsman.find_element_by_class_name("batsmen").find_element_by_tag_name("a").get_attribute('href')
                runs = score_record[0].text
                balls = score_record[1].text
                minutes = score_record[2].text
                _4s = score_record[3].text
                _6s = score_record[4].text
                strike_Rate = score_record[5].text
                # print(player_name+" "+player_link+" "+runs+" "+balls+" "+minutes+" "+_4s+" "+_6s+" "+strike_Rate)
            except NoSuchElementException:
                None

            try:
                commentary1 = post2.find_element_by_class_name("commentary-content")
                commentary = commentary1.get_attribute("textContent")
                # print(commentary)
            except NoSuchElementException:
                None

            try:
                commentary2 = post2.find_element_by_class_name("commentary")  # for find not out batsman
                dismissed_by = commentary2.get_attribute("textContent")
                # print(dismissed_by)
            except NoSuchElementException:
                None

            try:
                with open('./CricMatchBattingData.csv', 'a', newline='', encoding='utf-8') as outfile:
                    csvWriter = csv.writer(outfile)
                    # csvWriter.writerow(['Match', 'Player_name', 'Player_link', 'Dismissed_by', 'Commentary', 'Runs', 'Balls', 'Minutes','4s', '6s', 'Strike_Rate'])
                    csvWriter.writerow(
                        [match.match_id, player_name, player_link, dismissed_by, commentary, runs, balls, minutes, _4s,
                         _6s, strike_Rate])
                outfile.close()
            except Exception:
                None

    bowling_list = inning.find_element_by_class_name("bowling") #for bowlers
    bowlers = bowling_list.find_elements_by_tag_name("tr")
    for bowler in bowlers:
        tr_data = bowler.find_elements_by_tag_name("td")
        if len(tr_data)>0:
            player_name_bowler = tr_data[0].text
            player_link_bowler = tr_data[0].find_element_by_tag_name("a").get_attribute('href')
            overs = tr_data[2].text
            maidens = tr_data[3].text
            runs_bowler = tr_data[4].text
            wickets = tr_data[5].text
            econ = tr_data[6].text
            dot_balls = tr_data[7].text
            _4s_bowler = tr_data[8].text
            _6s_bowler = tr_data[9].text
            wides = tr_data[10].text
            no_balls = tr_data[11].text
            # print(player_name_bowler+" "+player_link_bowler+" "+overs+" "+maidens+" "+runs_bowler+" "+wickets+" "+econ+" "+dot_balls+" "+_4s_bowler+" "+_6s_bowler+" "+wides+" "+no_balls)
            with open('./CricMatchBowlingData.csv', 'a', newline='', encoding='utf-8') as outfile:
                csvWriter = csv.writer(outfile)
                # csvWriter.writerow(['Match', 'Player_name', 'Player_link', 'Overs', 'Maidens', 'Runs', 'Wickets', 'Econ', 'Dot_balls', '4s','6s', 'Wides', 'No_balls'])
                csvWriter.writerow([match.match_id, player_name_bowler, player_link_bowler, overs, maidens, runs_bowler, wickets, econ, dot_balls, _4s_bowler, _6s_bowler, wides, no_balls])
            outfile.close()

chrome_path = r"C:\Users\Rasitha\Desktop\chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chromeOptions)
driver.get("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year")
match_id = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[7]""")
match_ground_link = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[5]/a""").get_attribute("href")
match_link = match_id.find_element_by_tag_name("a").get_attribute("href")
match_id_val = match_id.text;
# print(match_id.text)
match_id .click()
match_main = driver.find_elements_by_class_name("gameHeader")

for post in match_main:
    if post.text != "":
        info_overview = post.find_element_by_class_name("cscore_info-overview").text
        # print("##########################"+info_overview)
        player_of_match = post.find_element_by_class_name("gp__cricket__player-match__player__detail__link").text
        # print(player_of_match)
        winning_team = post.find_element_by_class_name("cscore_notes_game").text
        # print(winning_team)
        scores = post.find_elements_by_class_name("cscore_team")
        inn_1_score = scores[0].text
        inn_2_score = scores[1].text

# print(player_of_match)
match = MatchData(match_id_val, info_overview, match_ground_link , match_link, player_of_match, inn_1_score+" "+inn_2_score, winning_team)

first_inning = driver.find_element_by_id("gp-inning-00") #First inning data
getInningData(first_inning)
second_inning = driver.find_element_by_id("gp-inning-01") #Second inning data
getInningData(second_inning)

with open('./CricMatchData.csv', 'a', newline='', encoding='utf-8') as outfile:
    csvWriter = csv.writer(outfile)
    csvWriter.writerow(['Match', 'Ground_link', 'Match_link', 'Title', 'MoM', 'Result', 'Winner'])
    csvWriter.writerow([match.match_id,match.ground_link,match.match_link, match.match_title, match.mom, match.match_result, match.match_win])
outfile.close()

del match

driver.back()

