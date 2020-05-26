import time, argparse, json, configparser, pprint, random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pypresence import Presence

# Functions


def lower_if_exists(lie_argument):
    if lie_argument:
        lie_output = lie_argument.lower()
    else:
        lie_output = lie_argument
    return lie_output


def fuzzy_error(fe_string, fe_list, fe_thresh):
    if fe_string != None:
        if process.extractOne(fe_string, fe_list)[1] < fe_thresh:
            return True
        else:
            return False


def presence_gen():

    # Setup default values

    pg_presencedict = {}
    pg_presencedict["party_size"] = []
    pg_presencedict["start"] = start_time
    pg_formatdict = {}
    pg_formatdict["map_image"] = ""
    pg_formatdict["map_hf"] = ""
    pg_formatdict["difficulty_hf"] = ""
    pg_formatdict["icon"] = "icon"
    if terrain:
        pg_terrain = process.extractOne(terrain, list(assets["terrains"].keys()))[0]
        pg_formatdict["map_image"] = assets["terrains"][pg_terrain]["maps"][
            random.choice(list(assets["terrains"][pg_terrain]["maps"].keys()))
        ]["image"]
        pg_formatdict["terrain_hf"] = assets["terrains"][pg_terrain]["name_hf"]
    if map:
        pg_map = process.extractOne(
            map, list(assets["terrains"][pg_terrain]["maps"].keys())
        )[0]
        pg_formatdict["map_image"] = assets["terrains"][pg_terrain]["maps"][pg_map][
            "image"
        ]
        pg_formatdict["map_hf"] = assets["terrains"][pg_terrain]["maps"][pg_map][
            "name_hf"
        ]
    if difficulty:
        pg_difficulty = difficulty
        pg_formatdict["difficulty_image"] = assets["difficulties"][pg_difficulty][
            "image"
        ]
        pg_formatdict["difficulty_hf"] = assets["difficulties"][pg_difficulty][
            "name_hf"
        ]
        pg_formatdict["difficulty_dots"] = assets["difficulties"][pg_difficulty]["dots"]

    if terrain and map and difficulty:
        for pg_field in list(config["Terrain, Map, Difficulty"].keys()):
            pg_presencedict[pg_field] = config["Terrain, Map, Difficulty"][
                pg_field
            ].format(**pg_formatdict)
    elif terrain and not map and difficulty:
        for pg_field in list(config["Terrain, No Map, Difficulty"].keys()):
            pg_presencedict[pg_field] = config["Terrain, No Map, Difficulty"][
                pg_field
            ].format(**pg_formatdict)
    elif terrain and map and not difficulty:
        for pg_field in list(config["Terrain, Map, No Difficulty"].keys()):
            pg_presencedict[pg_field] = config["Terrain, Map, No Difficulty"][
                pg_field
            ].format(**pg_formatdict)
    elif terrain and not map and not difficulty:
        for pg_field in list(config["Terrain, No Map, No Difficulty"].keys()):
            pg_presencedict[pg_field] = config["Terrain, No Map, No Difficulty"][
                pg_field
            ].format(**pg_formatdict)
    elif not terrain and not map and not difficulty:
        for pg_field in list(config["No Terrain, No Map, No Difficulty"].keys()):
            pg_presencedict[pg_field] = config["No Terrain, No Map, No Difficulty"][
                pg_field
            ].format(**pg_formatdict)
        pg_presencedict["start"] = None
    for pg_field in list(pg_presencedict.keys()):
        if pg_presencedict[pg_field] == "" or pg_presencedict[pg_field] == []:
            pg_presencedict[pg_field] = None
    return pg_presencedict


# Parsers

# Parse the arguments. Note that -m and -v do not have to be exact.

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--terrain", help="Terrain you are playing on.")
parser.add_argument("-m", "--map", help="Map you are playing.")
parser.add_argument("-d", "--difficulty", help="Difficulty you are playing at.")
args = parser.parse_args()

# Parse the config file.

config = configparser.ConfigParser()
config.read("config.ini")

# Parse the json file.

assets = json.load(open("assets.json", "r"))


# If the argument exists, then make it lowercase to normalize.

terrain = lower_if_exists(args.terrain)
map = lower_if_exists(args.map)
difficulty = lower_if_exists(args.difficulty)

# Load the data for each map and difficulty from the json.

assets = json.load(open("assets.json", "r"))

# Set up some basic errors if there are invalid inputs.

if difficulty and (terrain == None):  # Cannot have a difficulty without a terrain
    parser.error("--difficulty requires --terrain.")
if map and (terrain == None):  # Cannot have a map without a terrain
    parser.error("--map requires --terrain.")

# For map and variation, fuzzywuzzy will check if the closest match in the list has a score of lower than 75.
# If it does, it will return an error.

if fuzzy_error(terrain, list(assets["terrains"].keys()), 75):
    parser.error("invalid terrain.")
    if fuzzy_error(map, list(assets["terrains"][terrain]["maps"].keys()), 75):
        parser.error("invalid map.")
if difficulty:
    if difficulty not in list(assets["difficulties"].keys()):
        parser.error("invalid difficulty.")


# Setting up the rich presence.

client_id = config["Rich Presence"]["client_id"]
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="icon", large_text="Bloons TD 6", details="In Menu")
start_time = time.time()

# Check through different cases and run the one that fits.

pvars = presence_gen()
pprint.pprint(pvars)
while True:
    RPC.update(
        large_image=pvars["large_image"],
        large_text=pvars["large_text"],
        small_image=pvars["small_image"],
        small_text=pvars["small_text"],
        details=pvars["details"],
        state=pvars["state"],
        party_size=pvars["party_size"],
        start=pvars["start"],
    )
    time.sleep(5)
