import requests
import os
import pickle
from statistics import mean

# this total pokemon count is not correct
# at the time of writing, there are actually 1025 pokemon
# but there were only 1010 at the time the sample data was collected
# that being said, there is a need for a self-updating total count
# the easiest solution is probably just incrementing the id number
# until the return value is whatever is returned for a pokemon not found by the api
TOTAL_POKEMON = 1010
TYPES = ["normal",   "fire",    "water",
         "electric", "grass",   "ice",
         "fighting", "poison",  "ground",
         "flying",   "psychic", "bug",
         "rock",     "ghost",   "dragon",
         "dark",     "steel",   "fairy"]
STATS = ["hp",
         "attack",
         "defense",
         "special-attack",
         "special-defense",
         "speed"]
API_BASE_URL = "https://pokeapi.co/api/v2/"
POKEMON_DATA_FILE_NAME = "all-relevant-pokemon-data.pkl"


class Pokemon:

    def __init__(self, pokemon_id: int) -> None:
        self.id: int = pokemon_id

        pokemon_data: dict = requests.get(f"{API_BASE_URL}pokemon/{pokemon_id}/").json()
        self.name: str = pokemon_data["name"]
        self.typing: tuple[str] = tuple([type["type"]["name"].title() for type in pokemon_data["types"]]) 
        self.weight: float = pokemon_data["weight"] * 0.220462
        self.height: float = pokemon_data["height"] * 0.328084
        self.base_exp: int = pokemon_data["base_experience"]
        self.base_stats: dict[str, int] = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}

        pokemon_data = requests.get(f"{API_BASE_URL}pokemon-species/{pokemon_id}/").json()
        self.egg_groups: tuple[str] = tuple([egg_group["name"] for egg_group in pokemon_data["egg_groups"]])

        # im not sure how necessary this is
        # the one time i want to use chat gtp for and obscure question
        # it goes down for 12 hours...
        # im under the impression that it would automatically go out of scope
        # after initialization, but im gonna do it manually for the moment
        # just in case...
        del pokemon_data

    def __repr__(self) -> str:
        return self.name


# class Group:

#     def __init__(self, pokemon_list: list[Pokemon]) -> None:
#         self.pokemon: list[Pokemon] = pokemon_list
#         self.count: int = len(pokemon_list)
#         self.type_counts: dict[str, int] = {type: 0 for type in TYPES}
#         for pokemon in pokemon_list:
#             for type in pokemon.typing:
#                 self.type_counts[type] += 1
#         self.average_weight: float = mean([pokemon.weight for pokemon in pokemon_list])
#         self.average_height: float = mean([pokemon.height for pokemon in pokemon_list])
#         self.average_exp: float = mean([pokemon.base_exp for pokemon in pokemon_list])
#         self.average_stats: dict[str: float] = {"hp": 0,
#                                                 "attack": 0,
#                                                 "defense": 0,
#                                                 "special-attack": 0,
#                                                 "special-defense": 0,
#                                                 "speed": 0}
#         for pokemon in pokemon_list:
#             for type in TYPES:
#                 self.average_stats[type] += pokemon.base_stats[type]
#         for type, value in self.average_stats.items():
#             self.average_stats[type] = value / self.count


all_pokemon: list[Pokemon] = []

# so i fixed this for the most part
# dealing with the entire json files converted to dicts was not feasible
# current file size is down from over 100M to under 200K
# not sure if currently needed data is final, so that might grow slightly
# even then, the change should be inconsequential
#
# 6/4/24:
# ill also add here that this method of "caching" is primitive
# there's not necessarily a need for caching all pokemon at once
# unless a user were to need all pokemon for a given set of participants
# a more sophisticated way to do this would be to use a set to collect
# all pokemon smashed between all participants and just save those
#
# 6/5/24:
# i just realized that i was already on my way to solving this with the Group
# class in participant.py
if not os.path.exists(POKEMON_DATA_FILE_NAME):
    for pokemon_id in range(1, TOTAL_POKEMON + 1):
        os.system("clear")
        print(f"Loading {pokemon_id}/{TOTAL_POKEMON} Pokemon")
        all_pokemon.append(Pokemon(pokemon_id))
    with open(POKEMON_DATA_FILE_NAME, "wb") as pickle_file:
        pickle.dump(all_pokemon, pickle_file)
    print(f"All Pokemon Data Successfully Saved to {POKEMON_DATA_FILE_NAME}")
else:
    with open(POKEMON_DATA_FILE_NAME, "rb") as _all_pokemon_data_file:
        all_pokemon = pickle.load(_all_pokemon_data_file)
