import aiohttp
from pyrogram import Client
from Emilia import custom_filter
from Emilia.helper.disable import disable
from Emilia.utils.decorators import *

@usage("/pokedex [pokemon name]")
@example("/pokedex pikachu")
@description(
    "This works like a real pokedex and it will send you information regarding a specific pokemon."
)
@Client.on_message(custom_filter.command(commands="pokedex", disable=True))
@disable
async def PokeDex(_, message):
    if len(message.text.split()) != 2:
        await usage_string(message, PokeDex)
        return

    pokemon = message.text.split(None, 1)[1].strip().lower()  # Normalize input to lowercase
    pokedex_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    async with aiohttp.ClientSession() as session:
        async with session.get(pokedex_url) as request:
            if request.status == 404:
                return await message.reply_text("Invalid Pokémon name. Please try again.")

            if request.status != 200:
                return await message.reply_text("An error occurred while fetching the Pokémon data. Please try again later.")

            result = await request.json()

            try:
                pokemon_name = result.get("name", "N/A")
                pokedex_id = result.get("id", "N/A")
                types = ", ".join(typo["type"]["name"] for typo in result.get("types", [])[:5])
                abilities = ", ".join(ability["ability"]["name"] for ability in result.get("abilities", [])[:5])
                height = result.get("height", "N/A")
                weight = result.get("weight", "N/A")
                stats = "\n".join(f"{stat['stat']['name']}: {stat['base_stat']}" for stat in result.get("stats", []))

                caption = f"""**Pokemon:** `{pokemon_name}`
**Pokedex ID:** `{pokedex_id}`
**Type:** `{types}`
**Abilities:** `{abilities}`
**Height:** `{height}`
**Weight:** `{weight}`
**Stats:**
{stats}
"""
            except Exception as e:
                return await message.reply_text(f"An error occurred while processing the Pokémon data: {str(e)}")

    poke_img = f"https://img.pokemondb.net/artwork/large/{pokemon_name}.jpg" if pokemon_name != "N/A" else None

    if poke_img:
        await message.reply_photo(photo=poke_img, caption=caption)
    else:
        await message.reply_text(caption)

