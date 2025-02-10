import wordieTab
import random
from mtgsdk import Card, Set


class Crossword(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        # self.sizes = [20 - 25, 40 - 50, 60 - 75] small, medium, and large crossword hint counts.
        self.useful_sets = ["RAV", "ZEN", "WWK", "SHM", "MOR", "ALA", "LRW"]
        self.setup_button_choices(["Fetch", "Izzet", "Azorious", "Golgari", "Boros", "Dimir",
                                   "Rakdos", "Selesnya", "Gruul", "Orzhov", "Simic"])
        self.setup_labels(["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"],
                          group_name="Across", start_x_cell=1)
        self.setup_labels(["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"],
                          group_name="Down", start_x_cell=2)
        # self.full_card_set_list = Card.where(set=random.choice(self.useful_sets)).where(type="Creature").where(
        #     rarity="Common").all()
        self.full_card_set_list = []
        self.button_dict['Fetch'][1].config(command=self.fetch_cardlist)
        self.button_dict['Izzet'][1].config(command=self.set_izzet_color_dict)
        self.button_dict['Azorious'][1].config(command=self.set_azorious_color_dict)
        self.button_dict['Golgari'][1].config(command=self.set_golgari_color_dict)
        self.button_dict['Boros'][1].config(command=self.set_boros_color_dict)
        self.button_dict['Dimir'][1].config(command=self.set_dimir_color_dict)
        self.button_dict['Rakdos'][1].config(command=self.set_rakdos_color_dict)
        self.button_dict['Selesnya'][1].config(command=self.set_selesnya_color_dict)
        self.button_dict['Gruul'][1].config(command=self.set_gruul_color_dict)
        self.button_dict['Orzhov'][1].config(command=self.set_orzhov_color_dict)
        self.button_dict['Simic'][1].config(command=self.set_simic_color_dict)
        self.colored_card_list = []
        self.across_hint_dict = {}
        self.down_hint_dict = {}

    def fetch_cardlist(self):
        self.full_card_set_list = Card.where(set=random.choice(self.useful_sets)).where(type="Creature").where(
            rarity="Common").all()

    def set_izzet_color_dict(self):
        self.set_colored_card_list(["R", "B"])

    def set_azorious_color_dict(self):
        self.set_colored_card_list(["U", "W"])

    def set_golgari_color_dict(self):
        self.set_colored_card_list(["G", "B"])

    def set_boros_color_dict(self):
        self.set_colored_card_list(["R", "W"])

    def set_dimir_color_dict(self):
        self.set_colored_card_list(["B", "U"])

    def set_rakdos_color_dict(self):
        self.set_colored_card_list(["R", "B"])

    def set_selesnya_color_dict(self):
        self.set_colored_card_list(["G", "W"])

    def set_gruul_color_dict(self):
        self.set_colored_card_list(["R", "G"])

    def set_orzhov_color_dict(self):
        self.set_colored_card_list(["B", "W"])

    def set_simic_color_dict(self):
        self.set_colored_card_list(["G", "U"])

    def set_colored_card_list(self, color_symbols: list):
        self.colored_card_list = []

        for card in self.full_card_set_list:
            try:
                for col_sym in color_symbols:
                    if col_sym in card.color_identity:
                        self.colored_card_list.append(card)
            except TypeError as e:
                print(f'{e} fucked up.')
        self.set_across_dict(color_symbols)
        self.set_down_dict(color_symbols)

    def set_across_dict(self, color_symbols: list):
        self.across_hint_dict = {}
        card_names = []
        card_list = []
        for i in range(10):
            card_b = random.choice(self.colored_card_list)
            while card_b.name in card_names and len(card_b.name) > 10:
                card_b = random.choice(self.colored_card_list)
            card_names.append(card_b.name)
            card_list.append(card_b)
        self.update_labels(card_names, group_name="Across")
        for card in card_list:
            self.across_hint_dict[card.name] = [card.type, card.mana_cost, card.multiverse_id, card.image_url]
            print(f'{card.name}: {card.type}, {card.mana_cost}, {card.power}')
        print(f'{color_symbols}➚⇗➹⤴↗   ===================================')

    def set_down_dict(self, color_symbols: list):
        self.down_hint_dict = {}
        card_names = []
        card_list = []
        for i in range(10):
            card_b = random.choice(self.colored_card_list)
            while card_b.name in card_names:
                card_b = random.choice(self.colored_card_list)
            card_names.append(card_b.name)
            card_list.append(card_b)
        self.update_labels(card_names, group_name="Down")
        for card in card_list:
            self.across_hint_dict[card.name] = [card.type, card.mana_cost, card.multiverse_id, card.image_url]
            print(f'{card.name}: {card.type}, {card.mana_cost}, {card.power}')
        print(f'{color_symbols}➚⇗➹⤴↗   ===================================')
