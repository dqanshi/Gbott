import asyncio
from datetime import datetime
from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from Emilia import telethn, OWNER_ID,DEV_USERS, db

GBAN_COLLECTION = db["gban_users"]

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

AUTH_USERS = [OWNER_ID] + [DEV_USERS]

async def get_admin_groups():
    """Fetches groups where the bot has admin rights."""
    groups = []
    async for dialog in telethn.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                chat = await telethn.get_entity(dialog.id)
                permissions = await telethn.get_permissions(chat, "me")
                if permissions.is_admin and permissions.ban_users:
                    groups.append(chat.id)
            except Exception:
                pass
    return groups

async def is_gbanned(user_id):
    """Checks if a user is globally banned."""
    return bool(GBAN_COLLECTION.find_one({"user_id": user_id}))

async def add_gban(user_id, reason):
    """Adds a user to the global ban list."""
    GBAN_COLLECTION.update_one(
        {"user_id": user_id},
        {"$set": {"reason": reason, "timestamp": datetime.utcnow()}},
        upsert=True,
    )

async def remove_gban(user_id):
    """Removes a user from the global ban list."""
    GBAN_COLLECTION.delete_one({"user_id": user_id})

@telethn.on(events.NewMessage(pattern="^/gban(?: |$)(.*)"))
async def gban(event):
    """Global ban command."""
    if event.sender_id not in AUTH_USERS:
        return
    
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    reason = args if args else "No reason provided"
    
    if reply:
        user_id = reply.sender_id
    else:
        try:
            user_id = int(args.split()[0])
            reason = " ".join(args.split()[1:]) or "No reason provided"
        except ValueError:
            return await event.reply("Reply to a user or provide a valid user ID.")

    if user_id in AUTH_USERS:
        return await event.reply("You can't gban other developers or the owner.")

    if await is_gbanned(user_id):
        return await event.reply(f"This user is already globally banned.\n**Reason:** {reason}")

    await add_gban(user_id, reason)
    
    groups = await get_admin_groups()
    banned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, user_id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            banned_count += 1
        except BadRequestError:
            continue

    await event.reply(
        f"✅ **User Globally Banned**\n\n"
        f"👤 **User:** [{user_id}](tg://user?id={user_id})\n"
        f"🔒 **Banned in:** {banned_count} groups\n"
        f"📌 **Reason:** {reason}"
    )
    
    await telethn.send_message(
        user_id,
        f"⚠️ **You have been globally banned!**\n\n"
        f"👮 **Banned by:** [{event.sender_id}](tg://user?id={event.sender_id})\n"
        f"📌 **Reason:** {reason}\n"
        f"🔒 **Affected Groups:** {banned_count}"
    )

@telethn.on(events.NewMessage(pattern="^/ungban(?: |$)(.*)"))
async def ungban(event):
    """Global unban command."""
    if event.sender_id not in AUTH_USERS:
        return
    
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    
    if reply:
        user_id = reply.sender_id
    else:
        try:
            user_id = int(args.split()[0])
        except ValueError:
            return await event.reply("Reply to a user or provide a valid user ID.")

    if not await is_gbanned(user_id):
        return await event.reply("This user is not in the global ban list.")

    await remove_gban(user_id)
    
    groups = await get_admin_groups()
    unbanned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, user_id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            unbanned_count += 1
        except BadRequestError:
            continue

    await event.reply(
        f"✅ **User Globally Unbanned**\n\n"
        f"👤 **User:** [{user_id}](tg://user?id={user_id})\n"
        f"🔓 **Unbanned in:** {unbanned_count} groups"
    )
    
    await telethn.send_message(
        user_id,
        f"✅ **You have been globally unbanned!**\n\n"
        f"🔓 **Unbanned in:** {unbanned_count} groups"
    )

@telethn.on(events.ChatAction)
async def check_gban(event):
    """Checks if a joining user is globally banned and re-bans them."""
    if event.user_joined or event.user_added:
        user_id = event.user_id
        if await is_gbanned(user_id):
            try:
                await telethn(EditBannedRequest(event.chat_id, user_id, BANNED_RIGHTS))
                await event.reply(f"🚫 [{user_id}](tg://user?id={user_id}) is globally banned and was re-banned.")
            except BadRequestError:
                pass
