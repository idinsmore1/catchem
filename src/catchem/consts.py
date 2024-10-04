import json
from pathlib import Path

lib_path = Path(__file__).parent

with (lib_path / "pokestats_db.json").open() as f:
    pokestats = json.load(f)

with (lib_path / "config.json").open() as f:
    catchem_config = json.load(f)

colors = {
    "red": [239, 134, 54],
    "yellow": [249, 222, 110],
    "green": [175, 227, 75],
    "blue": [87, 191, 183],
    "normal": [170, 170, 170],
    "fire": [235, 84, 53],
    "water": [82, 151, 247],
    "electric": [247, 206, 85],
    "grass": [139, 202, 101],
    "ice": [128, 202, 250],
    "fighting": [174, 91, 74],
    "poison": [159, 90, 150],
    "ground": [215, 188, 101],
    "flying": [139, 152, 248],
    "psychic": [236, 98, 152],
    "bug": [173, 186, 68],
    "rock": [184, 171, 111],
    "ghost": [102, 102, 181],
    "dragon": [116, 103, 230],
    "dark": [114, 86, 71],
    "steel": [170, 170, 186],
    "fairy": [226, 157, 233],
}

gen_map = {
    "red": 1,
    "blue": 1,
    "yellow": 1,
    "gold": 2,
    "silver": 2,
    "crystal": 2,
    "ruby": 3,
    "sapphire": 3,
    "emerald": 3,
    "firered": 3,
    "leafgreen": 3,
    "diamond": 4,
    "pearl": 4,
    "platinum": 4,
    "heart gold": 4,
    "soul silver": 4,
    "black": 5,
    "white": 5,
    "black 2": 5,
    "white 2": 5,
    "x": 6,
    "y": 6,
    "omega ruby": 6,
    "alpha sapphire": 6,
    "sun": 7,
    "moon": 7,
    "ultra sun": 7,
    "ultra moon": 7,
    "lets go pikachu": 7,
    "lets go eevee": 7,
    "sword": 8,
    "shield": 8,
    "brilliant diamond": 8,
    "shining pearl": 8,
    "legends arceus": 8,
    "scarlet": 9,
    "violet": 9,
}
