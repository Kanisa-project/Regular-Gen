import random

import discord
from discord.ext import commands
from discord import app_commands

from utils import dbHelper

MANAMOJI_DICT = {
    '{0}': '<:mana0:1386425010565943317>',
    '{1}': '<:mana1:1386425026055639040>',
    '{2}': '<:mana2:1386425161133195344>',
    '{3}': '<:mana3:1386425303273963602>',
    '{4}': '<:mana4:1386425325906432112>',
    '{5}': '<:mana5:1386425341232418816>',
    '{6}': '<:mana6:1386425357070106769>',
    '{7}': '<:mana7:1386425371431272539>',
    '{8}': '<:mana8:1386425385884844277>',
    '{9}': '<:mana9:1386425398182805616>',
    '{10}': '<:mana10:1386425413458329730>',
    '{11}': '<:mana1:1386425026055639040>',
    '{12}': '<:mana12:1386425443724300318>',
    '{13}': '<:mana13:1386425463672406117>',
    '{14}': '<:mana14:1386425484073763006>',
    '{15}': '<:mana15:1386425499450085386>',
    '{16}': '<:mana16:1386425514989977640>',
    '{17}': '<:mana17:1386426493806313634>',
    '{18}': '<:mana18:1386426516627259482>',
    '{19}': '<:mana19:1386426534327484657>',
    '{20}': '<:mana20:1386425531473334402>',
    '{R}': '<:manar:1386425985267798187>',
    '{G}': '<:manag:1386425801880240229>',
    '{U}': '<:manau:1386426146664480808>',
    '{W}': '<:manaw:1386426260980371678>',
    '{B}': '<:manab:1386425563979190404>',
    '{C}': '<:manac:1386425659080835134>',
    '{C/P}': '<:manacp:1386426687272652880>',
    '{C/R}': '<:manacr:1386425727812898847>',
    '{C/G}': '<:manacg:1386425692316504135>',
    '{C/U}': '<:manacu:1386425744539914280>',
    '{C/W}': '<:manacw:1386425764475572225>',
    '{C/B}': '<:manacb:1386425675090628718>',
    '{2/R}': '<:mana2r:1386425228414161140>',
    '{2/G}': '<:mana2g:1386425106091343953>',
    '{2/U}': '<:mana2u:1386425253722456157>',
    '{2/W}': '<:mana2w:1386425276111650917>',
    '{2/B}': '<:mana2b:1386424973698142208>',
    '{R/G}': '<:manarg:1386426001923379261>',
    '{R/G/P}': '<:manargp:1386426016519422122>',
    '{R/P}': '<:manarp:1386426041915932792>',
    '{R/W}': '<:manarw:1386426059171434738>',
    '{R/W/P}': '<:manarwp:1386426075609038858>',
    '{G/P}': '<:managp:1386425819156578314>',
    '{G/U}': '<:managu:1386425842162470932>',
    '{G/U/P}': '<:managup:1386425862332878949>',
    '{G/W}': '<:managw:1386425880015933541>',
    '{G/W/P}': '<:managwp:1386425905445998682>',
    '{U/B}': '<:manaub:1386426182471516202>',
    '{U/B/P}': '<:manaubp:1386426198426390528>',
    '{U/P}': '<:manaup:1386426215157469254>',
    '{U/R}': '<:manaur:1386426231947530331>',
    '{U/R/P}': '<:manaurp:1386426247118323836>',
    '{W/B}': '<:manawb:1386426277249945762>',
    '{W/B/P}': '<:manawbp:1386426293876166778>',
    '{W/P}': '<:manawp:1386426315112054857>',
    '{W/U}': '<:manawu:1386426330140250112>',
    '{W/U/P}': '<:manawup:1386426347022454994>',
    '{B/G}': '<:manabg:1386425578906718401>',
    '{B/G/P}': '<:manabgp:1386425600763494591>',
    '{B/R}': '<:manabr:1386425617381068901>',
    '{B/R/P}': '<:manabrp:1386425632619233401>',
}


def mana_cost_to_manamoji(mana_cost: str) -> str:
    for symbol_key in list(MANAMOJI_DICT.keys()):
        mana_cost = mana_cost.replace(symbol_key, MANAMOJI_DICT[symbol_key])
    return mana_cost


def preloaded_spell_tuple_to_dict(spell_tuple) -> dict:
    return {"spell_name": spell_tuple[0],
            "spell_set": spell_tuple[1],
            "spell_cmc": spell_tuple[2],
            "spell_layout": spell_tuple[3],
            "spell_type": spell_tuple[4],
            "spell_colors": spell_tuple[5],
            "spell_mana_cost": spell_tuple[6]}


class CardPuzzle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hasActivePuzzle = False
        self.activeCardName = ''
        self.missed_guesses = 0
        self.db_helper = dbHelper.DatabaseHelper('/home/trevor/Documents/PycharmProjects/KanisaBot/utils/mtg_spells.db')
        self.home_guild = discord.Object(id=1035620535826141235)

    def next_hint(self) -> str:
        hidden_name = ''
        for i in range(len(self.activeCardName)):
            if random.randint(0, 10) <= self.missed_guesses:
                hidden_name += self.activeCardName[i]
            else:
                hidden_name += '-'
        return hidden_name

    def reset_puzzle(self):
        self.hasActivePuzzle = False
        self.activeCardName = ''
        self.missed_guesses = 0

    async def cog_load(self) -> None:
        print(f"{self.qualified_name} added to {self.bot.user.name}, successfully.")
        self.bot.tree.add_command(self.start_puzzle, guild=self.home_guild)
        self.bot.tree.add_command(self.guess_spell, guild=self.home_guild)


    @app_commands.command(name="start_puzzle", description="Start a new puzzle!")
    async def start_puzzle(self, interaction: discord.Interaction):
        await interaction.response.defer()
        spell_card = preloaded_spell_tuple_to_dict(random.choice(self.db_helper.get_available_spells()))
        manamoji_cost = mana_cost_to_manamoji(spell_card['spell_mana_cost'])
        embed = discord.Embed(title="Solve the card!",
                              description=f"What {spell_card['spell_type']} type card casts for {manamoji_cost}?",
                              colour=discord.Colour.blurple())
        self.hasActivePuzzle = True
        self.activeCardName = spell_card['spell_name']
        await interaction.followup.send(embed=embed)
        print('attempting the create')
        await self.bot.update_puzzle_channel(f"{spell_card['spell_type'].title()}")

    @app_commands.command(name="guess_spell", description="Guess a spell for the puzzle.")
    @app_commands.describe(guess="The spell being guessed, spell it correctly.")
    async def guess_spell(self, interaction: discord.Interaction, guess: str):
        if self.hasActivePuzzle:
            if guess.title() == self.activeCardName:
                self.reset_puzzle()
                await interaction.response.send_message(f"Good work! The spell is {guess.title()}!")
            else:
                self.missed_guesses += 1
                if self.missed_guesses >= 3:
                    await interaction.response.send_message(f"{guess.title()} is incorrect!\n{self.next_hint()}\n")
                await interaction.response.send_message(f"{guess.title()} is incorrect!\nMissed Guesses: {self.missed_guesses}")
        else:
            await interaction.response.send_message("There is no current active puzzle, you can start a puzzle with '/start_puzzle'.")

