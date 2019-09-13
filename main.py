from features import scores, standings, teams


def main():
    user = input("[s]cores | St[a]ndings | [t]eams: ")
    if user == "s":
        scores()
    elif user == "a":
        standings()
    elif user == "t":
        teams()

if __name__ == "__main__":
    main()
