from aiohttp import ClientSession
from pyrogram import Client
from datetime import datetime

from Emilia import custom_filter
from Emilia.helper.disable import disable
from Emilia.utils.decorators import *


@usage("/github [username]")
@example("/github ArshCypherZ")
@description(
    "This will fetch information of given username from github.com and send it."
)
@Client.on_message(custom_filter.command("github", disable=True))
@disable
@exception
async def github(_, message):
    if len(message.text.split()) != 2:
        return await usage_string(message, github)

    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    
    async with ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404: Not Found")
            elif request.status == 403:
                return await message.reply_text("403: API Rate Limit Exceeded. Please try again later.")
            elif request.status != 200:
                return await message.reply_text(f"Error: {request.status}. Unable to fetch user data.")
            
            result = await request.json()

            # Using .get() to handle missing fields gracefully
            name = result.get("name", "Not Available")
            bio = result.get("bio", "Not Available")
            company = result.get("company", "Not Available")
            created_at = result.get("created_at", "Not Available")
            if created_at != "Not Available":
                created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
            avatar_url = result.get("avatar_url", "")
            blog = result.get("blog", "Not Available") or "Not Available"
            location = result.get("location", "Not Available")
            repositories = result.get("public_repos", "Not Available")
            followers = result.get("followers", "Not Available")
            following = result.get("following", "Not Available")
            url = result.get("html_url", "Not Available")

            caption = f"""**GitHub Information of {name}:**
**Username :** `{username}`
**Bio :** `{bio}`
**Profile Link :** [Here]({url})
**Company :** `{company}`
**Created On :** `{created_at}`
**Repositories :** `{repositories}`
**Blog :** `{blog}`
**Location :** `{location}`
**Followers :** `{followers}`
**Following :** `{following}`"""

    # Sending response
    if avatar_url:
        await message.reply_photo(photo=avatar_url, caption=caption)
    else:
        await message.reply_text(caption)

