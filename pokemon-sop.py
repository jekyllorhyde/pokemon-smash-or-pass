import requests
import os
import pickle
import plotext

TOTAL_POKEMON = 1010
TYPES = ["Normal",   "Fire",    "Water",
         "Electric", "Grass",   "Ice",
         "Fighting", "Poison",  "Ground",
         "Flying",   "Psychic", "Bug",
         "Rock",     "Ghost",   "Dragon",
         "Dark",     "Steel",   "Fairy"]

# load pokemon into memory if required and save as a pickle file for easy access
# all pokemon currently sit at a 100MB pickle file
if not os.path.exists("./all-pokemon-data.pkl"):
    all_pokemon = []
    for pokemon_id in range(1, TOTAL_POKEMON + 1):
        os.system("clear")
        print(f"Loading {pokemon_id}/{TOTAL_POKEMON} Pokemon")
        all_pokemon.append(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/").json())
    with open("all-pokemon-data.pkl", "wb") as pickle_file:
        pickle.dump(all_pokemon, pickle_file)

# this definitely can be done better, 100MB of memory is way too much
# i have 16GB of ram though, so i dont think i need to fix it atm
all_pokemon_data_file = open("all-pokemon-data.pkl", "rb")
all_pokemon_data = pickle.load(all_pokemon_data_file)
all_pokemon_data_file.close()

class Participant:

    def __init__(self, name):
        self.name = name
        self.smashed_list = []
        self.total_smashed = -1
        self.percent_smashed = -1
        self.type_counts = {"Normal": 0,   "Fire": 0,    "Water": 0,
                            "Electric": 0, "Grass": 0,   "Ice": 0,
                            "Fighting": 0, "Poison": 0,  "Ground": 0,
                            "Flying": 0,   "Psychic": 0, "Bug": 0,
                            "Rock": 0,     "Ghost": 0,   "Dragon": 0,
                            "Dark": 0,     "Steel": 0,   "Fairy": 0}
        self.sorted_type_counts = {}
        self.preferred_egg_group = ""
        self.preferred_height = ""
        self.preferred_weight = ""
        self.preffered_appearance1 = ""
        self.preffered_appearance2 = ""
        self.preffered_base_exp = ""
        self.preffered_base_stats = ""

    def __repr__(self):
        print(self.name)

    def update_attributes(self):
        self.total_smashed = len(self.smashed_list)
        self.percent_smashed = (self.total_smashed/float(TOTAL_POKEMON)) * 100
        for pokemon_id, pokemon_name in self.smashed_list:
            for type in all_pokemon_data[pokemon_id-1]["types"]:
                self.type_counts[type["type"]["name"].title()] += 1
        self.sorted_type_counts = dict(sorted(self.type_counts.items(), key=lambda item: item[1], reverse=True))
        pass


def main():

    participant_list = []

    with open("data.csv", "r") as data_file:
        for pokemon_id, response_list in enumerate([line.strip("\n").split(",") for line in data_file]):
            boolean_response_list = []
            for response in response_list:
                if response == "s":
                    boolean_response_list.append(True)
                elif response == "p":
                    boolean_response_list.append(False)
                else:
                    participant_list.append(Participant(response))
                    boolean_response_list.append(-1)
            if boolean_response_list[0] != -1:
                for i, boolean in enumerate(boolean_response_list):
                    if boolean:
                        participant_list[i].smashed_list.append((pokemon_id, all_pokemon_data[pokemon_id-1]["species"]["name"]))

    for participant in participant_list:
        participant.update_attributes()
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
        plotext.simple_bar(TYPES, [count for type, count in participant.type_counts.items()], width=75, title="Total Number of Pokemon Smashed by Type")
        plotext.theme("clear")
        plotext.show()
        print()
    print()
    plotext.simple_multiple_bar(TYPES, [[count for type, count in participant.type_counts.items()] for participant in participant_list],
                                labels=[participant.name for participant in participant_list],
                                width=75,
                                title="Everyones Total of Pokemon Smashed by Type")
    plotext.show()


if __name__ == "__main__":
    main()
