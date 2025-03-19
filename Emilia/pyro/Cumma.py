import html
from pyrogram import Client, filters
from pyrogram.types import Message

# Aloha's Telegram ID
ALOHA_ID = 5260523032  

@Client.on_message(filters.command("aloha"))
async def aloha(client: Client, message: Message):
    """Handles the /aloha command and sends Aloha's info with premium emojis."""
    
    try:
        user = await client.get_users(ALOHA_ID)  # Fetch Aloha's profile
    except:
        await message.reply_text("Couldn't fetch Aloha's info.")
        return

    # Check for premium emoji in name
    emoji = ""
    if user.emoji_status:
        emoji = user.emoji_status.emoji  # Extract premium emoji

    # Create info message
    text = (
        f"✦ ᴜsᴇʀ ɪɴғᴏ ✦\n•❅─────✧❅✦❅✧─────❅•\n"
        f"➻ <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user.id}</code>\n"
        f"➻ <b>ғɪʀsᴛ ɴᴀᴍᴇ:</b> {html.escape(user.first_name)} {emoji}"
    )

    if user.last_name:
        text += f"\n➻ <b>ʟᴀsᴛ ɴᴀᴍᴇ:</b> {html.escape(user.last_name)}"
    if user.username:
        text += f"\n➻ <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{html.escape(user.username)}"
    
    text += f"\n➻ <b>ʟɪɴᴋ:</b> <a href='tg://user?id={user.id}'>Profile Link</a>"
    text += "\n\n🐉 ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴅʀᴀɢᴏɴ</b>."

    # Fetch Aloha's profile picture
    try:
        photos = await client.get_profile_photos(user.id, limit=1)
        if photos:
            await message.reply_photo(
                photo=photos[0].file_id,
                caption=text,
                parse_mode="HTML"
            )
        else:
            await message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
    except:
        await message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
