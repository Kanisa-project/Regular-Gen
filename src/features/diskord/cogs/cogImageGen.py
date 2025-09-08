import random

import discord
from PIL import Image
from discord import app_commands
from discord.ext import commands
from mtgsdk import Card

from tcg_api import sourceMTG
from utils import dbHelper, dummyHelper, fotoes

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


def new_starter_image() -> Image:
    return Image.new("RGBA", (960, 960), (0, 0, 0, 0))


def reset_color_id_list(stringed_list: str) -> list:
    color_id = []
    for c in stringed_list:
        if c in ['W', 'R', 'G', 'U', 'B']:
            color_id.append(c)
    return color_id


def preloaded_spell_tuple_to_dict(spell_tuple) -> dict:
    return {"spell_name": spell_tuple[0],
            "spell_set": spell_tuple[1],
            "spell_cmc": float(spell_tuple[2]),
            "spell_layout": spell_tuple[3],
            "spell_type": spell_tuple[4],
            "spell_colors": reset_color_id_list(spell_tuple[5]),
            "spell_mana_cost": spell_tuple[6]}


class ImageGenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_helper = dbHelper.DatabaseHelper('/home/trevor/Documents/PycharmProjects/KanisaBot/utils/mtg_spells.db')

    async def cog_load(self) -> None:
        print(f"{self.qualified_name} added to {self.bot.user.name}, successfully.")
        self.bot.tree.add_command(self.depict_spell, guild=discord.Object(id=1035620535826141235))

    @app_commands.command(name="depict_spell", description="Depict any kind of MTG spell.")
    @app_commands.describe(spell_name="The name of the spell you want to depict.")
    async def depict_spell(self, interaction: discord.Interaction, spell_name: str):
        print(f"{interaction.user.name} wants to depict a '{spell_name}' named card.")
        await interaction.response.defer()
        nim = new_starter_image()
        spell_card = random.choice(Card.where(name=spell_name).all())
        while spell_card.layout != "normal":
            spell_card = random.choice(Card.where(name=spell_name).all())
        insert_query = dbHelper.insert_table_statement_maker('norm_spells',
                                                             list(dummyHelper.mtg_card_template.keys()))[0]
        self.db_helper.execute_query(insert_query, [spell_card.name, spell_card.set, str(spell_card.cmc),
                                                    spell_card.layout, spell_card.type.replace('\u2014', '-'),
                                                    str(spell_card.colors), spell_card.mana_cost])
        print(f"Added {spell_card.name} to 'norm_spells'")
        save_name = spell_card.name.replace(" ", "_")
        imaj: Image = sourceMTG.depict_spell(nim, sourceMTG.build_spell_dict(spell_card))
        imaj.save(f"depictions/discord/{save_name}.png")
        f = discord.File(f"depictions/discord/{save_name}.png", filename=f"depictions/discord/{save_name}.png")
        embed = discord.Embed(title=spell_card.name + f"      {mana_cost_to_manamoji(spell_card.mana_cost)}",
                              description=spell_card.type,
                              colour=discord.Colour.blurple())
        embed.set_image(url=f'attachment://{imaj}')
        await interaction.followup.send(embed=embed, file=f)
        print(f"Sent a depiction of {spell_card.name} {spell_card.cmc} {spell_card.mana_cost}.")


    @app_commands.command(name='foto', description='Blend two photographs into one, then deepfry it.')
    @app_commands.describe(tcg1='The TCG to pull first card for blending')
    @app_commands.describe(tcg2='The TCG to pull second card for blending')
    async def generate_foto(self, interaction: discord.Interaction, tcg1: str = "Magic", tcg2: str = "Magic"):
        print(f"Generating a foto for {interaction.user.name}")
        await interaction.response.defer()
        save_name = f"foto{random.randint(0, 22)}"
        imaj: Image = fotoes.make_a_foto(True, tcg1=tcg1, tcg2=tcg2)
        imaj.save(f"depictions/discord/{save_name}.png")
        f = discord.File(f"depictions/discord/{save_name}.png", filename=f"depictions/discord/{save_name}.png")
        embed = discord.Embed(title="Foto",
                              description="Blended and deepfried.",
                              colour=discord.Colour.blurple())
        embed.set_image(url=f'attachment://{imaj}')
        await interaction.followup.send(embed=embed, file=f)
        print(f"Sent {save_name}")
