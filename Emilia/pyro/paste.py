import os
import re

import aiofiles
import httpx
from pyrogram import Client

from Emilia import custom_filter
from Emilia.helper.disable import disable
from Emilia.utils.decorators import *

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")

http = httpx.AsyncClient()

@usage("/paste [reply to text/file]")
@example("/paste ArshCypherZ is a good boi")
@description("This command will paste the given text or replied file to nekobin.com")
@Client.on_message(custom_filter.command(commands="paste", disable=True))
@disable
async def paste_func(_, message):
    if not message.reply_to_message:
        await usage_string(message, paste_func)
        return

    content = None
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_size > 1048576:
            return await message.reply("You can only paste files smaller than 1MB.")
        if not pattern.search(document.mime_type):
            return await message.reply("Only text files can be pasted.")

        doc = await message.reply_to_message.download()
        try:
            async with aiofiles.open(doc, mode="r") as f:
                content = await f.read()
        except Exception as e:
            return await message.reply(f"Failed to read the file: {str(e)}")
        finally:
            os.remove(doc)

    if content is None:
        return await message.reply("No valid content to paste.")

    link = "https://nekobin.com/api/documents"
    try:
        r = await http.post(link, json={"content": content})
        r.raise_for_status()
        response_data = r.json()
        key = response_data.get('result', {}).get('key')

        if not key:
            raise ValueError("Unexpected response format from nekobin API.")
        
        url = f"https://nekobin.com/{key}"
        return await message.reply(url, disable_web_page_preview=True)
    except httpx.RequestError as e:
        return await message.reply(f"Failed to reach nekobin.com: {str(e)}")
    except ValueError as e:
        return await message.reply(f"Error: {str(e)}")
