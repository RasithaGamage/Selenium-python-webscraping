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
        try:
            batsman = post2.find_element_by_class_name("batsmen")
            commentary = post2.find_element_by_class_name("commentary-content")
            print(batsman.text)
            print(commentary.get_attribute("textContent"))
        except NoSuchElementException:
            print("")

    #batsmen didn't bat
    bowling_list = inning.find_element_by_class_name("bowling") #for bowlers
    bowlers = bowling_list.find_elements_by_tag_name("td")
    for bowler in bowlers:
        print(bowler.text)


chrome_path = r"C:\Users\Rasitha\Desktop\chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=chromeOptions)
driver.get("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year")
match_id = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[7]""")
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

print(player_of_match)
match = MatchData(match_id_val, info_overview, player_of_match, inn_1_score+" "+inn_2_score, winning_team)

first_inning = driver.find_element_by_id("gp-inning-00") #First inning data
getInningData(first_inning)
second_inning = driver.find_element_by_id("gp-inning-01") #Second inning data
getInningData(second_inning)

with open('./CricData.csv', 'w', newline='', encoding='utf-8') as outfile:
    csvWriter = csv.writer(outfile)
    csvWriter.writerow(['Match', 'Title', 'MoM', 'Result', 'Winner'])
    csvWriter.writerow([match.match_id, match.match_title, match.mom, match.match_result, match.match_win])
outfile.close()

del match

driver.back()

