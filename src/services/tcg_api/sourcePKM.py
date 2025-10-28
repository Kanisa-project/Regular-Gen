import os
import random

import requests
from dotenv import load_dotenv
from tcgdexsdk import TCGdex, Query
from tcg_api.sourceTCG import BaseAPIHelper
from src.utils import dbHelper, glythed
from src.utils.glythed import TcgDepicter

load_dotenv()
width_len = 36
API_KEY = os.getenv('POKEMON_API_KEY')
ENERGY_TYPES = ['grass', 'fire', 'water', 'lighting', 'psychic', 'fighting', 'darkness', 'metal']


class PkmnDepicter(TcgDepicter):
    def __init__(self, depict_settings: dict):
        super().__init__(depict_settings)

    def build_card_datadict(self, card_data) -> dict:
        card_datadict = {
            'name': card_data.name,
            'type': ''.join(card_data.types),
            'rarity': card_data.rarity,
            'id': card_data.id
        }
        self.card_datadict = card_datadict
        return card_datadict


class PokeAPIHelper(BaseAPIHelper):
    """
    An API helper for Pokemon TCG depiction, puzzling and listering on the KanisaBot.
    """
    def __init__(self):
        super().__init__()
        self.CARDTYPES = ["Energy", "Pokemon", "Trainer"]
        self.base_url = 'https://api.tcgdex.net/v2/en/'
        self.endpoint_names = {'cards': [],
                               'sets': []}
        self.color_translation_dict = {
            'grass': 'green',
            'fire': 'red',
            'water': 'blue',
            'lighting': 'yellow',
            'psychic': 'purple',
            'fighting': 'brown',
            'darkness': 'dark grey',
            'metal': 'light grey'
        }
        self.sdk = TCGdex()

    def add_card_database(self, new_card):
        all_card_insert_query = dbHelper.insert_table_statement_maker('all_cards', ['card_name', 'card_rarity', 'card_type', 'card_set', 'card_id'])[0]
        self.db_helper.execute_query(all_card_insert_query, [new_card.name, new_card.rarity, new_card.category, "Pokemon TCG", new_card.id])


    def download_card_batch(self, batch_config: dict):
        super().download_card_batch(batch_config)
        # print("ENERGY", self.sdk.energyType())
        r = requests.get(self.endpoint_builder('cards?', self.query_builder({'category': self.batch_type})))
        for i in range(self.batch_size):
            card_dict = random.choice(r.json())
            card = self.sdk.card.getSync(card_dict['id'])
            self.add_card_database(card)
            if card.image != "None" and card.image is not None:
                img_url = card.image + '/high.png'
                img_data = requests.get(img_url).content
                save_name = f"{card.set.id.upper()}_" + card.name.replace(" ", "_")
                with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/config/cardsPokemon/{save_name}.png', 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded {save_name}: {card.set.id}")


def download_energy_set():
    sdk = TCGdex()
    energy_cards = sdk.card.listSync(Query().equal('category', 'Energy'))
    random_energies = random.sample(energy_cards, 6)
    for energy_type in ENERGY_TYPES:
        print('===', energy_type)
        if random_energies[0] != "None":
            img_url = random_energies[0].image + '/high.png'
            img_data = requests.get(img_url).content
            save_name = f"{random_energies[0].set.id.upper()}_" + random_energies[0].name.replace(" ", "_")
            with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/config/src_imgs/{save_name}.png', 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}: {random_energies[0].set.id}")

def download_snorlaxes():
    sdk = TCGdex()
    snorlax_cards = sdk.card.listSync(Query().equal('name', 'Snorlax'))
    random_snorlaxes = random.sample(snorlax_cards, 6)
    for card in random_snorlaxes:
        card = sdk.card.getSync(card.id)
        print(f'{card.name}  {card.image}/high.png')
        print(f'{card.rarity}  {card.hp}')
        print(f'{card.set.name}')
        if card.image is not None:
            img_data = requests.get(f'{card.image}/high.png').content
            save_name = f"{card.set.id.upper()}_" + card.name.replace(" ", "_")
            with open(f'/home/trevor/Documents/PycharmProjects/KanisaBot/config/cardsPokemon/{save_name}.png',
                      'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {save_name}")

if __name__ == "__main__":
    # download_energy_set()
    download_snorlaxes()


def run_depicter_from_script(depict_config_dict: dict):
    depicter = PkmnDepicter(depict_config_dict)
    sdk = TCGdex()
    rando_card = random.choice(sdk.card.listSync(Query().equal('name', 'Snorlax')))
    pkmn_card = sdk.card.getSync(rando_card.id)
    card_datadict = depicter.build_card_datadict(pkmn_card)
    depicted_card = depicter.depict_card(card_datadict)
    depicted_card.save(f"depictions/{depicter.card_datadict['name']}.png")


def run_puzzler_from_script(puzzle_config_dict: dict):
    pass