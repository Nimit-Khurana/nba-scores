import requests
from bs4 import BeautifulSoup as soup
import click
from terminaltables import AsciiTable

def scores():
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

    def decorate(func):
        click.echo(click.style("="*20, fg="green"))
        def f():
            func()
            click.echo(click.style("="*20, fg="green") )
        return f()



    schedule_container = soup(url_content.text, "html.parser")

    # get date from page
    date = schedule_container.findAll("h2")[0]
    click.echo(click.style(date.contents[0], fg="green"))
    print ("\n")

    # next tag after h2 the table schedule
    # next after h2 is table and then tr
    table_sibling = date.next_sibling.table.findAll("tr")

    data = [["SCORE" , "Winner & Loser High"]]
    for i in range(1,len(table_sibling)):
        # tr
        for tr_data in table_sibling[i].findAll("a", {"name" : "&lpos=nba:schedule:score"}):
            #print (tr_data.contents[0].replace(",", " -"))
            score = []
            for tr_player_data in table_sibling[i].findAll("a", {"name" : "&lpos=nba:schedule:player"}):
                # "Sibling" in this context is the next node, not the next element/tag. Your element's next node is a text node, so you get the text you want.
                #print ("\t" + tr_player_data.contents[0] + tr_player_data.next_sibling)
                score.append(tr_player_data.contents[0] + tr_player_data.next_sibling )
            #click.echo(click.style("-"*20, fg="green"))

            data.append( [tr_data.contents[0].replace(",", " -") , score[0]+" & "+score[1]] )

    table = AsciiTable(data)
    if data != [["SCORE" , "Winner & Loser High"]]:
        print (table.table)
        print("\n----Team's attributes----")
        for keyss, valuess in team_attrs.items():
            print(valuess + " -- " + keyss)
    else:
        @decorate
        def func():
            click.echo(click.style( "No matches played!!", bg="green") )


def standings():
    base_url = "https://www.espn.in/nba/standings"
    url_content = requests.get(base_url)

    schedule_container = soup(url_content.text, "html.parser")

    season = schedule_container.findAll("h1")[1]
    click.echo(click.style(season.contents[0], fg="green") )

    conference = schedule_container.findAll("div", {"class": "Table2__Title"})
    data = [ [conference[0].contents[0] , conference[1].contents[0]] ]
    team_list_1 = []
    team_list_2 = []
    for conf in conference:
        #print (str(conf.contents[0]))
        stand = conf.next_sibling.contents[0].table.findAll("tr", {"class": "Table2__tr"})

        for i in range( 1,len(stand) ):
            for teams in stand[i].find("span", {"class":"hide-mobile" }):
                #print ("\t" + teams.contents[0])
                if str(conf.contents[0]) == "Eastern Conference":
                    team_list_1.append(teams.contents[0])
                else:
                    team_list_2.append(teams.contents[0])
    # append teams from list
    # uncomment below to see original
    # data.append([team_list_1, team_list_2])
    for t in range(len(team_list_2 )):
        data.append([team_list_1[t], team_list_2[t]])

    table = AsciiTable(data)
    if data != [ [conference[0] , conference[1]] ]:
        print (table.table)


def teams():
    base_url = "https://www.espn.in/nba/teams"
    url_content = requests.get(base_url)

    schedule_container = soup(url_content.text, "html.parser")

    data = []
    regions = []
    team_list_all = []
    teams = schedule_container.findAll("div", {"class": "layout__column"})
    for i in range( 1,len(teams) ):
        for t in teams[i].findAll("div", {"class": "mt7"}):
            # team regions
            regions.append(t.div.contents[0])
            #print (t.div.contents)
            team_list = []
            for t_section in t.section.findAll("section"):
                if t_section.section:
                    pl3 = t_section.section.find("div", {"class": "pl3"})
                    #print( "\t" + pl3.contents[0].h2.contents[0] )
                    team_list.append( pl3.contents[0].h2.contents[0] )
                    #print( "\t" + pl3.div.findAll("span")[2].a.contents[0] + " " + pl3.div.findAll("span")[0].a.contents[0])
            team_list_all.append(team_list)
    data.insert(0,regions)
    for j in range( len(team_list_all[0]) ):
        data.append([ team_list_all[0][j], team_list_all[1][j], team_list_all[2][j], team_list_all[3][j], team_list_all[4][j], team_list_all[5][j] ])

    heading = schedule_container.findAll("h1")[1].contents[0]

    table = AsciiTable(data)
    table.title = heading + " By Region"
    print(table.table)