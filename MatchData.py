import csv
import traceback
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from BattingData import BattingData
from BowlingData import BowlingData

class MatchData:

    def __init__(self, url):
        self.url = url
        chrome_path = r"C:\Users\Rasitha\Desktop\chromedriver.exe"
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chromeOptions)

        driver.get(self.url)

        matches_table = driver.find_element_by_xpath("""//*[@id="ciHomeContentlhs"]/div[3]/div/table[1]/tbody""")
        tr_matches = matches_table.find_elements_by_tag_name("tr")
        for tr_match in tr_matches:
            match_id_1 = tr_match.find_elements_by_tag_name("td")
            match_id = match_id_1[6]
            self.match_id_val = match_id_1[6].text
            self.match_link = match_id_1[6].find_element_by_tag_name("a").get_attribute("href")
            self.match_ground_link = match_id_1[4].find_element_by_tag_name("a").get_attribute("href")

            main_window = driver.current_window_handle
            str_script = "window.open('"+self.match_link+"');"
            driver.execute_script(str_script)
            driver.switch_to.window(driver.window_handles[1])

            try:
                 match_main = driver.find_elements_by_class_name("gameHeader")
            except NoSuchElementException:
                traceback.print_exc(file=open("errlog.txt", "a"))

            self.player_of_match = "No data"
            self.winning_team  = "No data"
            self.info_overview = "No data"
            self.inn_1_score = "No data"
            self.inn_2_score = "No data"

            for post in match_main:
                if post.text != "":
                    try:
                     self.info_overview = post.find_element_by_class_name("cscore_info-overview").text
                    except NoSuchElementException:
                        traceback.print_exc(file=open("errlog.txt", "a"))
                    try:
                        self.player_of_match = post.find_element_by_class_name("gp__cricket__player-match__player__detail__link").text
                    except NoSuchElementException:
                        traceback.print_exc(file=open("errlog.txt", "a"))

                    try:
                        self.winning_team = post.find_element_by_class_name("cscore_notes_game").text
                    except NoSuchElementException:
                        traceback.print_exc(file=open("errlog.txt", "a"))

                    try:
                        scores = post.find_elements_by_class_name("cscore_team")
                        self.inn_1_score = scores[0].text
                        global inn_1_country
                        inn_1_country = self.inn_1_score.splitlines()[0]
                        self.inn_2_score = scores[1].text
                        global inn_2_country
                        inn_2_country = self.inn_2_score.splitlines()[0]
                    except NoSuchElementException:
                        traceback.print_exc(file=open("errlog.txt", "a"))

            self.saveRecord()

            try:
                first_inning = driver.find_element_by_id("gp-inning-00")  # First inning data
                self.getInningData(first_inning)
            except NoSuchElementException:
                traceback.print_exc(file=open("errlog.txt", "a"))
            try:
                second_inning = driver.find_element_by_id("gp-inning-01")  # Second inning data
                self.getInningData(second_inning)
            except NoSuchElementException:
                traceback.print_exc(file=open("errlog.txt", "a"))

            driver.close()
            driver.switch_to.window(main_window)

    def saveRecord(self):
        with open('./CricMatchData.csv', 'a', newline='', encoding='utf-8') as outfile:
            csvWriter = csv.writer(outfile)
            # csvWriter.writerow(['Match', 'Ground_link', 'Match_link', 'Title', 'MoM', 'Result', 'Winner'])
            csvWriter.writerow([self.match_id_val, self.match_ground_link, self.match_link, self.info_overview, self.player_of_match, self.inn_1_score +" "+self.inn_2_score, self.winning_team])
        outfile.close()

    def getInningData(self, inning):
        batsmen_list = inning.find_element_by_class_name("scorecard-section")  # for batsmens
        batsmen_score = batsmen_list.find_elements_by_class_name("flex-row")

        try:
            score_headers = batsmen_score[0].find_element_by_class_name("header").find_elements_by_class_name("runs")

        except NoSuchElementException:
            traceback.print_exc(file=open("errlog.txt", "a"))

        for l, post2 in enumerate(batsmen_score):
            check_availability = ""
            check_availability1= ""

            try:
                check_availability = post2.find_element_by_class_name("batsmen").find_element_by_class_name("batsmen").text
                print("check_availability "+ check_availability)
            except NoSuchElementException:
                traceback.print_exc(file=open("errlog.txt", "a"))

            try:
                check_availability1 = post2.find_elements_by_class_name("batsmen")[1].find_element_by_class_name("batsmen").text
                print("check_availability1 " + check_availability1)
            except Exception:
                None

            player_name = "No_data"
            player_link = "No_data"
            runs = "No_data"
            balls = "No_data"
            minutes = "No_data"
            _4s = "No_data"
            _6s = "No_data"
            strike_Rate = "No_data"
            commentary = "No_data"
            dismissed_by = "No_data"
            country = "No_data"
            position = l+1

            if len(check_availability) or len(check_availability1) > 0:
                try:
                    batsman = post2.find_element_by_class_name("batsmen")
                    player_name = batsman.find_element_by_class_name("batsmen").text
                    player_link = batsman.find_element_by_class_name("batsmen").find_element_by_tag_name("a").get_attribute('href')
                    score_record = batsman.find_elements_by_class_name("runs")
                except NoSuchElementException:
                    traceback.print_exc(file=open("errlog.txt", "a"))
                try:
                    if l == 0:
                        batsman = post2.find_elements_by_class_name("batsmen")[1]
                        player_name = batsman.find_element_by_class_name("batsmen").text
                        player_link = batsman.find_element_by_class_name("batsmen").find_element_by_tag_name("a").get_attribute('href')
                        score_record = batsman.find_elements_by_class_name("runs")
                except NoSuchElementException:
                    traceback.print_exc(file=open("errlog.txt", "a"))

                for i, record in enumerate(score_record):
                    try:
                        if score_headers[i].text == "R":
                            runs = record.text
                        if score_headers[i].text == "B":
                            balls = record.text
                        if score_headers[i].text == "M":
                            minutes = record.text
                        if score_headers[i].text == "4s":
                            _4s = record.text
                        if score_headers[i].text == "6s":
                            _6s = record.text
                        if score_headers[i].text == "SR":
                            strike_Rate = record.text
                        if inning.get_attribute("id") == "gp-inning-00":
                            country = inn_1_country
                        if inning.get_attribute("id") == "gp-inning-01":
                            country = inn_2_country
                    except NoSuchElementException:
                        traceback.print_exc(file=open("errlog.txt", "a"))
                try:
                    commentary1 = post2.find_element_by_class_name("commentary-content")
                    commentary = commentary1.get_attribute("textContent")
                except NoSuchElementException:
                    traceback.print_exc(file=open("errlog.txt", "a"))

                try:
                    commentary2 = post2.find_element_by_class_name("commentary")  # for find not out batsman
                    dismissed_by = commentary2.get_attribute("textContent")
                    # print(dismissed_by)
                except NoSuchElementException:
                    traceback.print_exc(file=open("errlog.txt", "a"))

                try:
                    commentary2 = post2.find_elements_by_class_name("batsmen")[1].find_element_by_class_name("commentary")  # for find not out batsman
                    dismissed_by = commentary2.get_attribute("textContent")
                    # print(dismissed_by)
                except NoSuchElementException:
                    traceback.print_exc(file=open("errlog.txt", "a"))

                batsman_obj = BattingData(self.match_id_val, player_name, player_link, runs, balls, minutes, _4s, _6s,
                                          strike_Rate, commentary, dismissed_by, country,position)
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
        country = "No_data"

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
                    if inning.get_attribute("id") == "gp-inning-00":
                        country = inn_1_country
                    if inning.get_attribute("id") == "gp-inning-01":
                        country = inn_2_country

                bowler_obj = BowlingData(self.match_id_val, player_name_bowler, player_link_bowler, overs, maidens,
                                         runs_bowler, wickets, econ, dot_balls, _4s_bowler, _6s_bowler, wides, no_balls, country)
                bowler_obj.saveRecord()
                del bowler_obj
