from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from constants import FootballConsts
import sys

def MatchDetails(url, matchDetails):
    driver = webdriver.Chrome()
    driver.get(url)
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, "lxml")
    team = []
    teams = matchDetails.find_all("span", class_=re.compile("teamBlock"))
    for t in teams:
        team.append(t.string)
    score = matchDetails.find("span", class_=re.compile("fm-match"))
    time = matchDetails.find("span", class_=re.compile("matchTime"))
    print(team)
    print(score.string)
    print(time.string)

def getFootballMatch():
    print("Enter team name (full name)")
    teamName = input()
    driver = webdriver.Chrome()
    url = f"{FootballConsts.baseURL.value}{FootballConsts.ongoing.value}"
    driver.get(url)
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, "lxml")
    matches = soup.find_all("a", class_=re.compile("livescore"))
    foundTeam = False
    matchURL = None
    matchDetails = None
    if matches is not None:
        for match in matches:
            if foundTeam:
                break
            teams = match.find_all("span", class_=re.compile("teamBlock"))
            for team in teams:
                if teamName.lower() in team.string.lower():
                    matchURL = match.attrs['href']
                    foundTeam = True
                    matchDetails = match
                    break
    if not foundTeam:
        print(FootballConsts.noMatch.value)
        driver.close()
        sys.exit()
    driver.quit()
    url = f"{FootballConsts.baseURL.value}{matchURL}"
    MatchDetails(url,matchDetails)