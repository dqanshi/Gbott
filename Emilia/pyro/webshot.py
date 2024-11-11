import validators
from pyrogram import Client
from pyrogram.errors import WebpageCurlFailed
from pyrogram.types import Message

from Emilia import custom_filter
from Emilia.helper.disable import disable
from Emilia.utils.decorators import *


@usage("/webss [website link]")
@example("/webss google.com")
@description("Screenshots given website.")
@Client.on_message(custom_filter.command(commands="webss", disable=True))
@disable
@rate_limit(10, 60)
async def take_ss(_, message: Message):
    if len(message.text.split()) != 2:
        await usage_string(message, take_ss)
        return

    url = message.text.split(None, 1)[1].strip()

    # Ensure the URL has a valid format
    if not validators.url(url):
        # Attempt to add "https://" and revalidate
        url_with_protocol = "https://" + url
        if not validators.url(url_with_protocol):
            await message.reply("Invalid URL format. Please try again with a valid URL.")
            return
        url = url_with_protocol

    screenshot_url = f"https://service.headless-render-api.com/screenshot/{url}"

    try:
        await message.reply_photo(photo=screenshot_url, quote=False)
    except WebpageCurlFailed:
        await message.reply("Failed to fetch the screenshot. The website may be unreachable or blocked.")
    except Exception as e:
        await message.reply_text(f"An unexpected error occurred: {str(e)}")
