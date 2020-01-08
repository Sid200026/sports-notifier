import enum


class FootballConsts(enum.Enum):
    baseURL = "https://www.fotmob.com"
    noMatch = "No such team found. Please check if the team is currently playing or you have entered the name correctly"
    apiConst = "https://api3.fotmob.com/matches?date={}&tz=19800000"
    matchFinished = "Match Over"