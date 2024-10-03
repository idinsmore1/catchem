from fuzzywuzzy import fuzz, process
from catchem.consts import pokestats, colors
from tabulate import tabulate

def fuzzy_search(query, limit=5):
    choices = list(pokestats.keys())
    return process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)


def catch_em_all(pokemon):
    """Get base stats, moves, and evolutions of a pokemon
    :param pokemon: The name of the pokemon
    """
    pokemon, score = fuzzy_search(pokemon)
    if score < 70:  # If the score is less than 70, the match is too weak
        print(f"Error: {pokemon.title()} not found")
        pokemon = input("Try again: ")
        catch_em_all(pokemon)
        return
    
    stats = pokestats[pokemon]
    print(f"Base stats for {pokemon.title()}")
    print(make_stats_table(stats))


def make_stats_table(stats):
    pokemon = stats['name']
    dex_no = stats['dex_no']
    poke_types = stats['types']
    stat_names = zip(
        ['hp', 'attack', 'defense', 'spatt', 'spdef', 'speed', 'total'],
        ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']
    )
    stat_rows = []
    for stat_tag, stat_name in stat_names:
        stat_value = stats[stat_tag]
        if stat_tag == 'total':
            rgb_info  = _total_stat_code(stat_value)
            color_bar = rgb_text(*rgb_info)
            stat_rows.append([stat_name, stat_value, color_bar])
            continue
        color = _base_stat_code(stat_value)
        stat_bar = '|' * (stat_value // 2)
        color_bar = rgb_text(stat_bar, color)
        stat_rows.append([stat_name, stat_value, color_bar])
    type_header_string = ' '.join([rgb_text(f' {type_.title()} ', type_) for type_ in poke_types])
    header = [f'No: {dex_no}', pokemon.title(), type_header_string]
    return tabulate(stat_rows, headers=header, tablefmt='mixed_grid')
    


def rgb_text(text, color, background=True):
    color_type = 48 if background else 38  # 48 for background, 38 for foreground
    r, g, b = colors.get(color)
    return f"\033[{color_type};2;{r};{g};{b}m{text}\033[0m"


def _base_stat_code(stat_val):
    if stat_val < 50:
        return 'red'
    elif stat_val < 90:
        return 'yellow'
    elif stat_val < 125:
        return 'green'
    else:
        return 'blue'
    
def _total_stat_code(stat_val) -> tuple[str, str]:
    if stat_val < 350:
        return ' Bad ', 'red'
    elif stat_val < 450:
        return ' Mid ', 'yellow'
    elif stat_val < 500:
        return ' Good ', 'green'
    elif stat_val < 600:
        return ' Great ', 'grass'
    else:
        return ' Legend/Pseudo ', 'blue'