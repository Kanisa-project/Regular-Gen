import random

import discord
from discord import app_commands
from discord.ext import commands
from mtgsdk import Card

from utils import dbHelper, dummyHelper


def is_owner(interaction: discord.Interaction) -> bool:
    if interaction.user.id == interaction.guild.owner_id:
        return True
    return False


class MagicCog(commands.Cog):
    def __init__(self, bot):
        self.running_secs = 0
        self.bot = bot
        self.db_helper = dbHelper.DatabaseHelper('/home/trevor/Documents/PycharmProjects/KanisaBot/utils/mtg_spells.db')

    async def cog_load(self) -> None:
        self.bot.tree.add_command(self.set_spells, guild=discord.Object(id=1035620535826141235))
        print(f"{self.qualified_name} added to {self.bot.user.name}, successfully.")

    @app_commands.command(name="set_spells", description="Load a set of MTG cards.")
    @app_commands.describe(spells_amount="The number of spells to add from the set_code.")
    @app_commands.describe(set_code="The 3 digit code to describe what set to pull spells from.")
    @app_commands.check(is_owner)
    async def set_spells(self, interaction: discord.Interaction, spells_amount: int, set_code: str):
        print(f"Gathering {spells_amount} spells from {set_code.upper()}")
        await interaction.response.defer()
        card_list = Card.where(set=set_code).all()
        for i in range(spells_amount):
            next_card = random.choice(card_list)
            insert_statement = \
                dbHelper.insert_table_statement_maker('norm_spells', list(dummyHelper.mtg_card_template.keys()))[0]
            print(self.db_helper.execute_query(insert_statement, [next_card.name, next_card.set, str(next_card.cmc),
                                                                   next_card.layout,
                                                                   next_card.type.replace('\u2014', '-'),
                                                                   str(next_card.colors), next_card.mana_cost]))
        await interaction.followup.send(f'{card_list}')
