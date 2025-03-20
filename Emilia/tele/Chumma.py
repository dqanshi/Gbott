import html
import logging
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from Emilia import telethn

logging.basicConfig(level=logging.INFO)
ALOHA_ID = 5260523032  # Aloha's Telegram ID

@telethn.on(events.NewMessage(pattern="^/aloha$"))
async def aloha(event):
    """Handles the /aloha command and sends Aloha's info with profile photo."""
    
    try:
        logging.info(f"Fetching user details for ID {ALOHA_ID}...")
        user = await telethn(GetFullUserRequest(ALOHA_ID))  # Fetch Aloha's profile
        user_info = user.user
        logging.info(f"Fetched user: {user_info.first_name}")
    except Exception as e:
        logging.error(f"Error fetching user info: {e}")
        await event.reply("Couldn't fetch Aloha's info.")
        return

    # Create info message
    text = (
        f"✦ ᴜsᴇʀ ɪɴғᴏ ✦\n•❅─────✧❅✦❅✧─────❅•\n"
        f"➻ <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_info.id}</code>\n"
        f"➻ <b>ғɪʀsᴛ ɴᴀᴍᴇ:</b> {html.escape(user_info.first_name)}"
    )

    if user_info.last_name:
        text += f"\n➻ <b>ʟᴀsᴛ ɴᴀᴍᴇ:</b> {html.escape(user_info.last_name)}"
    if user_info.username:
        text += f"\n➻ <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{html.escape(user_info.username)}"
    
    text += f"\n➻ <b>ʟɪɴᴋ:</b> <a href='tg://user?id={user_info.id}'>Profile Link</a>"
    text += "\n\n🐉 ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴅʀᴀɢᴏɴ</b>."

    # Fetch Aloha's profile picture
    logging.info("Fetching profile photo...")
    photos = await telethn.get_profile_photos(user_info.id, limit=1)
    logging.info(f"Fetched {len(photos)} profile pictures.")

    if photos:
        await event.reply(file=photos[0], message=text, parse_mode="html")
    else:
        await event.reply(text, parse_mode="html")
    
