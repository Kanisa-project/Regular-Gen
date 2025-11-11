import os
import logging
import discord
from discord import Intents
from dotenv import load_dotenv
from discord.ext import commands, tasks
from cogs.cogMTG import MagicCog
from cogs.cogPuzzle import CardPuzzle
from cogs.cogImageGen import ImageGenCog

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='config/logs/discord.log', encoding='utf-8', mode='w')

"""
I got angels on my shoulders with the devil in my head.
I don't know where I'm going but I know where I've been.
You can find me in the future where my money never ends.
"""

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
}


def is_owner(interaction: discord.Interaction) -> bool:
    if interaction.user.id == interaction.guild.owner_id:
        return True
    return False


class KanisaClient(commands.Bot):
    def __init__(self, intents: Intents):
        self.runtime_seconds = 0
        super().__init__(command_prefix="!", intents=intents)
        self.home_guild = None

    @tasks.loop(seconds=10)
    async def timer_printer(self):
        print(f"{self.user} has been running for {self.runtime_seconds} seconds.")
        self.runtime_seconds += 10

    async def setup_hook(self) -> None:
        self.tree.clear_commands(guild=self.home_guild)
        await self.add_cog(MagicCog(self))
        await self.add_cog(CardPuzzle(self))
        await self.add_cog(ImageGenCog(self))
        self.timer_printer.start()
        synced = await self.tree.sync(guild=self.home_guild)
        print(f"Synced {len(synced)} commands setup_hook().")

    async def update_puzzle_channel(self, card_type: str):
        await self.get_channel(1387612326089461810).edit(name=card_type)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
bot = KanisaClient(intents)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('config/logs/err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_ready():
    print(f'  =={bot.user.name} has connected to Discord!')


@bot.event
async def on_message_edit(before, after):
    print("Before edit: ", before)
    print("After edit: ", after)


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
