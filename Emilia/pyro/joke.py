import aiohttp
from pyrogram import Client
from Emilia import custom_filter
from Emilia.helper.disable import disable
from Emilia.utils.decorators import *

@Client.on_message(
    custom_filter.command(commands=["joke", "jokes", "funny"], disable=True)
)
@rate_limit(10, 60)
@disable
async def joke(client, message):
    url = "https://v2.jokeapi.dev/joke/Any"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return await message.reply("Failed to fetch a joke. Please try again later.")

                joke = await response.json()

                # Extracting the joke based on the type
                joke_type = joke.get("type")
                if joke_type == "twopart":
                    get1 = joke.get("setup", "Oops! Something went wrong.")
                    get2 = joke.get("delivery", "")
                    await message.reply(f"{get1}\n{get2}")
                elif joke_type == "single":
                    get3 = joke.get("joke", "Oops! Something went wrong.")
                    await message.reply(get3)
                else:
                    await message.reply("Could not fetch a proper joke. Please try again.")
        except Exception as e:
            await message.reply(
                f"An error occurred: {str(e)}\nPlease report to support chat @SpiralTechDivision"
            )
