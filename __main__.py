import csv
from telnetlib import EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from MatchData import MatchData
from BatsmanData import BatsmanData
from BowlerData import BowlerData


# "http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year"
# change id=2010 into desired year to get required data

match = MatchData("http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id=2010;team=8;type=year")

del match


