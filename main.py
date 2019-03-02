from bs4 import BeautifulSoup as soup
import requests
import sys
import re


date = input("Enter date to look for(YYYYMMDD): ")
base_url = "http://www.espn.in/nba/schedule"
dated_url = base_url + "/_/date/" + date

url_content = requests.get(dated_url)
team_attrs = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets" : "BKN",
    "Charlotte Hornets" : "CHA",
    "Chicago Bulls" : "CHI",
    "Cleveland Cavaliers" : "CLE",
    "Dallas Mavericks" : "DAL",
    "Denver Nuggets" : "DEN",
    "Detroit Pistons" : "DET",
    "Golden State Warriors" : "GS",
    "Houston Rockets" : "HOU",
    "Indiana Pacers" : "IND",
    "LA Clippers" : "LAC",
    "Los Angeles Lakers" : "LAL",
    "Memphis Grizzles" : "MEM",
    "Miami Heat" : "MIA",
    "Milwaukee Bucks" : "MIL",
    "Minnesota Timberwolves" : "MIN",
    "New Orleanas Pelicans" : "NO",
    "New York Knicks" : "NY",
    "Oklohoma City Thunder" : "OKC",
    "Orlando Magic" : "ORL",
    "Philadelphia 76ers" : "PHI",
    "Phoenix Suns" : "PHX",
    "Portland Trail Blazers" : "POR",
    "Sacremanto Kings" : "SAC",
    "San Antonio Spurs" : "SA",
    "Toronto Raptors" : "TOR",
    "Utah Jazz" : "UTAH",
    "Washington Wizards" : "WSH"
}


if url_content.status_code == requests.codes.ok:
    print ("Response OK")

schedule_container = soup(url_content.text, "html.parser")

date = schedule_container.findAll("h2")[0]
print (date.contents[0])
print ("\n")

# next tag after h2
# the table schedule
table_sibling = date.next_sibling

for i in range(1,len(table_sibling.table.findAll("tr"))):
    for tr_data in table_sibling.table.findAll("tr")[i].findAll("a", {"name" : "&lpos=nba:schedule:score"}):
        print (tr_data.contents[0].replace(",", " beat"))

print ("Matches Played: {}".format(len(table_sibling.table.findAll("tr"))-1))
print ()