from pokesmash import pokemon

class Participant:

    def __init__(self, participant_data: list[str | tuple[int, str]]) -> None:
        self.name: str = participant_data.pop(0)
        self.smashed_list: list[tuple[int, str]] = participant_data
        # done with participant_data from here on
        self.total_smashed: int = len(self.smashed_list)
        self.percent_smashed: float = (self.total_smashed/float(pokemon.TOTAL_POKEMON)) * 100
        self.type_counts: dict[str, int] = {"normal": 0,   "fire": 0,    "water": 0,
                                            "electric": 0, "grass": 0,   "ice": 0,
                                            "fighting": 0, "poison": 0,  "ground": 0,
                                            "flying": 0,   "psychic": 0, "bug": 0,
                                            "rock": 0,     "ghost": 0,   "dragon": 0,
                                            "dark": 0,     "steel": 0,   "fairy": 0}
        for pokemon_id, pokemon_name in self.smashed_list:
            for type in pokemon.all_pokemon_data[pokemon_id-1]["types"]:
                self.type_counts[type["type"]["name"].title()] += 1
        self.sorted_type_counts: dict[str, int] = dict(sorted(self.type_counts.items(), key=lambda item: item[1], reverse=True))
        self.preferred_egg_group: str = ""
        self.preferred_height: float = 0.0
        self.preferred_weight: float = 0.0
        self.preffered_appearance1: str = ""
        self.preffered_appearance2: str = ""
        self.preffered_base_exp: float = 0.0
        self.preffered_base_stats: float = 0.0

    def __repr__(self) -> str:
        return self.name

    def update_attributes(self) -> None:
        self.total_smashed = len(self.smashed_list)
        self.percent_smashed = (self.total_smashed/float(pokemon.TOTAL_POKEMON)) * 100
        for pokemon_id, pokemon_name in self.smashed_list:
            for type in pokemon.all_pokemon_data[pokemon_id-1]["types"]:
                self.type_counts[type["type"]["name"].title()] += 1
        self.sorted_type_counts = dict(sorted(self.type_counts.items(),
                                              key=lambda item: item[1],
                                              reverse=True))

class Group:

    def __init__(self, participants: list[Participant]):
        self.participants = participants
        self.collective_smashed_list: set[tuple[int, str]] = {}
        self.smashed_in_common_list: set[tuple[int, str]] = {}


def load_from_csv(file_name:str="data.csv") -> list[Participant]:
    with open(file_name, "r") as data_file:
        participant_data_list: list[list[str | tuple[int, str]]] = [[name] for name in data_file.readline().strip("\n").split(",")]
        for pokemon_id, response_list in enumerate([line.strip("\n").split(",") for line in data_file]):
            boolean_response_list: list[bool] = []
            for response in response_list:
                boolean_response_list.append(True if response == "s" else False)
            for i, boolean in enumerate(boolean_response_list):
                if boolean:
                    participant_data_list[i].append((pokemon_id,
                                                     pokemon.all_pokemon_data[pokemon_id-1]["species"]["name"]))

    return [Participant(participant_data) for participant_data in participant_data_list]
