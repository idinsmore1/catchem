import argparse
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
from catchem.consts import colors, gen_map


def catchem() -> None:
    parser = argparse.ArgumentParser(description="Display the base stats of a Pokémon")
    parser.add_argument("pokemon", help="The name of the Pokémon to display")
    parser.add_argument("game_moves", nargs='?', help="The learnable moves of the Pokémon based on game version", default=None)
    parser.add_argument("-a", "--alt", help="Display the alternate form of the Pokémon", action="store_true")
    args = parser.parse_args()
    matched_pokemon = get_pokemon_data(args.pokemon)
    if args.game_moves is not None:
        game = args.game_moves.lower()
        print(args.game_moves)


def get_pokemon_data(pokemon: str) -> str:
    pokemon = pokemon.lower()
    URL = f"https://pokemondb.net/pokedex/{pokemon}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    if soup.find('title').text == 'Error 404: Page Not Found | Pokémon Database':
        print(f'Error: {pokemon.title()} not found')
        new_poke = input('Try again: ').lower()
        matched_pokemon = get_pokemon_data(new_poke)
        return matched_pokemon

    # Get the pokemon types
    types_h2 = soup.find('h2', string='Pokédex data')
    types_table = types_h2.find_next_sibling('table')
    for row in types_table.find_all('tr'):
        if row.find('th').text == 'Type':
            types = [cell.text.lower() for cell in row.find('td').find_all('a')]
        if row.find('th').text == 'National №':
            national_number = row.find('td').text
    # Find the "Base stats" section
    stats_h2 = soup.find_all('h2', string='Base stats')[0]
    
    stats_table = stats_h2.find_next_sibling('div').find('table')
    rows = stats_table.find_all('tr')
    stats = []
    for row in rows:
        stat_name = row.find('th').text
        stat_value = int(row.find('td', class_='cell-num').text)
        if stat_value < 50:
            stat_color = 'red'
        elif stat_value < 90:
            stat_color = 'yellow'
        elif stat_value < 125:
            stat_color = 'green'
        else:
            stat_color = 'blue'
        stat_bar = '|' * (stat_value // 2)
        if stat_name != 'Total': 
            color_bar = rgb_text(stat_bar, stat_color)
        else:
            if stat_value < 350:
                color_bar = rgb_text(' Bad ', 'red')
            elif stat_value < 450:
                color_bar = rgb_text(' Mid ', 'yellow')
            elif stat_value < 525:
                color_bar = rgb_text(' Good ', 'green')
            elif stat_value < 600:
                color_bar = rgb_text(' Great ', 'grass')
            else:
                color_bar = rgb_text(' Legend/Pseudo ', 'blue')
            
        stats.append([stat_name, stat_value, color_bar])
    type_header_string = ' '.join([rgb_text(f' {type_.title()} ', type_) for type_ in types])
    # header = [f'{pokemon.title()} {type_header_string}']
    header = [f'No: {national_number}', pokemon.title(), type_header_string]
    print(tabulate(stats, headers=header, tablefmt='mixed_grid'))
    return pokemon
    

def color_text(text: str, color: str) -> str:
    return f"{colors.get(color, '')}{text}{colors['end']}"


def rgb_text(text, color, background=True):
    color_type = 48 if background else 38  # 48 for background, 38 for foreground
    r, g, b = colors.get(color)
    return f"\033[{color_type};2;{r};{g};{b}m{text}\033[0m"


