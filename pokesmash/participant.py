from pokesmash import pokemon

class Participant:

    def __init__(self, name):
        self.name = name
        self.smashed_list = []
        self.total_smashed = 0
        self.percent_smashed = 0.0
        self.type_counts = {"Normal": 0,   "Fire": 0,    "Water": 0,
                            "Electric": 0, "Grass": 0,   "Ice": 0,
                            "Fighting": 0, "Poison": 0,  "Ground": 0,
                            "Flying": 0,   "Psychic": 0, "Bug": 0,
                            "Rock": 0,     "Ghost": 0,   "Dragon": 0,
                            "Dark": 0,     "Steel": 0,   "Fairy": 0}
        self.sorted_type_counts = {}
        self.preferred_egg_group = ""
        self.preferred_height = 0.0
        self.preferred_weight = 0.0
        self.preffered_appearance1 = ""
        self.preffered_appearance2 = ""
        self.preffered_base_exp = 0.0
        self.preffered_base_stats = 0.0

    def __repr__(self):
        print(self.name)

    def update_attributes(self):
        self.total_smashed = len(self.smashed_list)
        self.percent_smashed = (self.total_smashed/float(pokemon.TOTAL_POKEMON)) * 100
        for pokemon_id, pokemon_name in self.smashed_list:
            for type in pokemon.all_pokemon_data[pokemon_id-1]["types"]:
                self.type_counts[type["type"]["name"].title()] += 1
        self.sorted_type_counts = dict(sorted(self.type_counts.items(),
                                              key=lambda item: item[1],
                                              reverse=True))

# class Group:

#     def __init__(self, participants):
#         self.participants = participants
#         self.smashed_list = 


def load_from_csv(file_name="data.csv"):
    participant_list = []
    with open(file_name, "r") as data_file:
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
                        participant_list[i].smashed_list.append((pokemon_id,
                                                                 pokemon.all_pokemon_data[pokemon_id-1]["species"]["name"]))
    for participant in participant_list:
        participant.update_attributes()

    return participant_list
