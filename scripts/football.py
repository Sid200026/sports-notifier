from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import re
from constants import FootballConsts
from notification import notify
import sys
from datetime import datetime
import requests
import pytz


def MatchDetails(url, team1=None, team2=None):
    options = Options()
    # Do not open the chrome browser
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, "lxml")
    team = []
    if team1 is None or team2 is None:
        teams = soup.find_all("div", class_=re.compile("MatchHeaderTeamTitle"))
        for t in teams:
            team.append(t.string)
    else:
        team = [team1, team2]
    score = soup.find("div", class_=re.compile("LivescoreMatchScore"))
    time = soup.find("div", class_=re.compile("LivescoreMatchTime"))
    scoreline = f"{team[0]} {score.string.strip()} {team[1]}"
    if time.string.strip().lower() in ['ft', 'full-time', 'fulltime']:
        notify(scoreline, FootballConsts.matchFinished.value)
        sys.exit()
    endindex = time.string.find(":")
    timePassed = time.string[0:endindex] + " minutes"
    if time.string.strip().lower() in ["ht", "halftime", "half-time", "pause"]:
        print("Half Time")
        timePassed = "Half Time"
        sleep(180)
    # Do not get the seconds. Only the minutes
    driver.quit()
    notify(scoreline, timePassed)
    sleep(60)
    MatchDetails(url, team[0], team[1])


def fetchMatch():
    tz = pytz.timezone('Asia/Kolkata')
    d = datetime.now(tz)
    d = d.strftime("%Y%m%d")
    url = FootballConsts.apiConst.value.format(d)
    site = requests.get(url)
    soup = BeautifulSoup(site.content, "lxml")
    matches = soup.find_all("match")
    print("Enter team name")
    teamFound = False
    teamName = input()
    for match in matches:
        team1 = match.attrs['ateam'].lower()
        team2 = match.attrs['hteam'].lower()
        if teamName.lower() in team1 or teamName.lower() in team2:
            teamFound = True
            url = f"{FootballConsts.baseURL.value}/livescores/{match.attrs['id']}"
            MatchDetails(url)
    if not teamFound:
        print(FootballConsts.noMatch.value)
        sys.exit()
