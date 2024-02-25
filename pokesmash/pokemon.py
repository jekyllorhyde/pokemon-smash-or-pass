import requests
import os
import pickle

# this total pokemon count is not correct
# at the time of writing, there are actually 1025 pokemon
# but there were only 1010 at the time the sample data was collected
# that being said, there is a need for a self-updating total count
# the easiest solution is probably just incrementing the id number
# until the return value is whatever is returned for a pokemon not found by the api
TOTAL_POKEMON = 1010
TYPES = ["Normal",   "Fire",    "Water",
         "Electric", "Grass",   "Ice",
         "Fighting", "Poison",  "Ground",
         "Flying",   "Psychic", "Bug",
         "Rock",     "Ghost",   "Dragon",
         "Dark",     "Steel",   "Fairy"]

# if pkl file doesn't exist, load pokemon data into memory and save for easy access
# all pokemon currently sit at a 100MB pickle file (i know it's too much)
if not os.path.exists("../all-pokemon-data.pkl"):
    all_pokemon: str = []
    for pokemon_id in range(1, TOTAL_POKEMON + 1):
        os.system("clear")
        print(f"Loading {pokemon_id}/{TOTAL_POKEMON} Pokemon")
        all_pokemon.append(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/").json())
    with open("../all-pokemon-data.pkl", "wb") as pickle_file:
        pickle.dump(all_pokemon, pickle_file)

# this definitely can be done better, 100MB of memory is way too much
# though i don't think anyone is running less than 4GB of ram these days
# so i dont think it's super necessary to fix it right now
# simplest fix would be to only save the required pokemon as the program moves along
# only saving the specifically required infomation for each pokemon would be even better
_all_pokemon_data_file = open("../all-pokemon-data.pkl", "rb")
all_pokemon_data = pickle.load(_all_pokemon_data_file)
_all_pokemon_data_file.close()


