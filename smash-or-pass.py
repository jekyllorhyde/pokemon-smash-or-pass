import plotext
from pokesmash import pokemon
# i've really gone back and forth on whether participant is a good name
# participant is the only word that really makes sense
# and using any other word in this document would be inconsistent
# so i'm just gonna stick with it until it actually becomes a problem
from pokesmash import participant as part

def main():

    participant_list = part.load_from_csv()

    for participant in participant_list:
        print()
        print(participant.name)
        print("-" * 51)
        counter = 1
        total = len(participant.smashed_list)
        for pokemon_id, pokemon_name in participant.smashed_list:
            print(f"{pokemon_name.title():<16} ", end="")
            if counter % 3 == 0:
                print()
            elif counter == total:
                print()
            counter += 1
        print()
        print(f"Total Pokemon Smashed: {participant.total_smashed}")
        print()
        print(f"Percent of All Pokemon Smashed: {participant.percent_smashed:.2f}%")
        print()
        plotext.simple_bar(pokemon.TYPES, [count for type, count in participant.type_counts.items()], width=75, title="Total Number of Pokemon Smashed by Type")
        plotext.theme("clear")
        plotext.show()
        print()
    print()
    plotext.simple_multiple_bar(pokemon.TYPES, [[count for type, count in participant.type_counts.items()] for participant in participant_list],
                                labels=[participant.name for participant in participant_list],
                                width=75,
                                title="Everyones Total of Pokemon Smashed by Type")
    plotext.show()


if __name__ == "__main__":
    main()
