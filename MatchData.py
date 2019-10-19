import csv
import csv
from telnetlib import EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from BatsmanData import BatsmanData
from BowlerData import BowlerData


class MatchData:
    def __init__(self, url):
        self.url = url
        chrome_path = r"C:\Users\Rasitha\Desktop\chromedriver.exe"
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chromeOptions)

        driver.get(self.url)

        match_id = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[7]""")
        self.match_ground_link = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[5]/a""").get_attribute("href")
        self.match_link = match_id.find_element_by_tag_name("a").get_attribute("href")
        self.match_id_val = match_id.text;
        # print(match_id.text)
        match_id.click()
        match_main = driver.find_elements_by_class_name("gameHeader")

        for post in match_main:
            if post.text != "":
                self.info_overview = post.find_element_by_class_name("cscore_info-overview").text
                # print("##########################"+info_overview)
                self.player_of_match = post.find_element_by_class_name(
                    "gp__cricket__player-match__player__detail__link").text
                # print(player_of_match)
                self.winning_team = post.find_element_by_class_name("cscore_notes_game").text
                # print(winning_team)
                scores = post.find_elements_by_class_name("cscore_team")
                self.inn_1_score = scores[0].text
                self.inn_2_score = scores[1].text


        first_inning = driver.find_element_by_id("gp-inning-00")  # First inning data
        self.getInningData(first_inning)
        second_inning = driver.find_element_by_id("gp-inning-01")  # Second inning data
        self.getInningData(second_inning)


        driver.back()

    def saveRecord(self):
        with open('./CricMatchData.csv', 'a', newline='', encoding='utf-8') as outfile:
            csvWriter = csv.writer(outfile)
            csvWriter.writerow(['Match', 'Ground_link', 'Match_link', 'Title', 'MoM', 'Result', 'Winner'])
            csvWriter.writerow([self.match_id_val, self.match_ground_link, self.match_link, self.info_overview, self.player_of_match, self.inn_1_score +" "+self.inn_2_score, self.winning_team])
        outfile.close()

    def getInningData(self, inning):
        batsmen_list = inning.find_element_by_class_name("scorecard-section")  # for batsmens
        batsmen_score = batsmen_list.find_elements_by_class_name("flex-row")
        for post2 in batsmen_score:
            check_availability = ""
            try:
                check_availability = post2.find_element_by_class_name("batsmen").find_element_by_class_name(
                    "batsmen").text
            except Exception:
                None

            if len(check_availability) > 0:
                try:
                    batsman = post2.find_element_by_class_name("batsmen")
                    score_record = batsman.find_elements_by_class_name("runs")
                    player_name = batsman.find_element_by_class_name("batsmen").text
                    player_link = batsman.find_element_by_class_name("batsmen").find_element_by_tag_name(
                        "a").get_attribute('href')
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

                batsman_obj = BatsmanData(self.match_id_val, player_name, player_link, runs, balls, minutes, _4s, _6s,
                                          strike_Rate, commentary, dismissed_by)
                batsman_obj.saveRecord()
                del batsman_obj

        bowling_list = inning.find_element_by_class_name("bowling")  # for bowlers
        bowlers = bowling_list.find_elements_by_tag_name("tr")
        #GET THE LIST OF COLUMNS
        header = bowling_list.find_element_by_tag_name("thead")
        ths = header.find_elements_by_tag_name("th")
        player_name_bowler = "No_data"
        player_link_bowler = "No_data"
        overs = "No_data"
        maidens = "No_data"
        runs_bowler = "No_data"
        wickets = "No_data"
        econ = "No_data"
        dot_balls = "No_data"
        _4s_bowler = "No_data"
        _6s_bowler = "No_data"
        wides = "No_data"
        no_balls = "No_data"

        for bowler in bowlers:
            tr_data = bowler.find_elements_by_tag_name("td")
            if len(tr_data) > 0:
                for i, td in enumerate(tr_data):

                    if ths[i].text == "BOWLING":
                        player_name_bowler = td.text
                        player_link_bowler = td.find_element_by_tag_name("a").get_attribute('href')

                    if ths[i].text == "O":
                        overs = td.text

                    if ths[i].text == "M":
                        maidens = td.text

                    if ths[i].text == "R":
                        runs_bowler = td.text

                    if ths[i].text == "W":
                        wickets = td.text

                    if ths[i].text == "ECON":
                        econ = td.text

                    if ths[i].text == "0s":
                        dot_balls = td.text

                    if ths[i].text == "4s":
                        _4s_bowler = td.text

                    if ths[i].text == "6s":
                        _6s_bowler = td.text

                    if ths[i].text == "WD":
                        wides = td.text

                    if ths[i].text == "NB":
                        no_balls = td.text

                bowler_obj = BowlerData(self.match_id_val, player_name_bowler, player_link_bowler, overs, maidens,
                                        runs_bowler, wickets, econ, dot_balls, _4s_bowler, _6s_bowler, wides, no_balls)
                bowler_obj.saveRecord()
                del bowler_obj

    # def getData(self):
    #     chrome_path = r"C:\Users\Rasitha\Desktop\chromedriver.exe"
    #     chromeOptions = webdriver.ChromeOptions()
    #     prefs = {'profile.managed_default_content_settings.images': 2}
    #     chromeOptions.add_experimental_option("prefs", prefs)
    #     driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chromeOptions)
    #
    #     driver.get(self.url)
    #
    #     match_id = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[7]""")
    #     self.match_ground_link = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody/tr[2]/td[5]/a""").get_attribute("href")
    #
    #     self.match_link = match_id.find_element_by_tag_name("a").get_attribute("href")
    #     self.match_id_val = match_id.text;
    #     # print(match_id.text)
    #     match_id.click()
    #     match_main = driver.find_elements_by_class_name("gameHeader")
    #
    #     for post in match_main:
    #         if post.text != "":
    #             self.info_overview = post.find_element_by_class_name("cscore_info-overview").text
    #             # print("##########################"+info_overview)
    #             self.player_of_match = post.find_element_by_class_name(
    #                 "gp__cricket__player-match__player__detail__link").text
    #             # print(player_of_match)
    #             self.winning_team = post.find_element_by_class_name("cscore_notes_game").text
    #             # print(winning_team)
    #             scores = post.find_elements_by_class_name("cscore_team")
    #             self.inn_1_score = scores[0].text
    #             self.inn_2_score = scores[1].text
    #
    #
    #     first_inning = driver.find_element_by_id("gp-inning-00")  # First inning data
    #     # getInningData(first_inning)
    #     second_inning = driver.find_element_by_id("gp-inning-01")  # Second inning data
    #     # getInningData(second_inning)
    #     driver.back()