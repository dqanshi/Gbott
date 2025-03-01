import asyncio
from datetime import datetime
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from Emilia import telethn, OWNER_ID, DEV_USERS, db

# Define allowed users (Owners & Developers)
AUTH_USERS = [OWNER_ID] + DEV_USERS if isinstance(DEV_USERS, list) else [OWNER_ID]

# MongoDB collection for storing GBan data
GBAN_COLLECTION = db["gban_users"]

# Ban and Unban Rights
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
UNBAN_RIGHTS = ChatBannedRights(until_date=None)

# Get bot's admin groups
async def get_admin_groups():
    groups = []
    async for dialog in telethn.iter_dialogs():
        if dialog.is_group:
            try:
                chat = await telethn.get_entity(dialog.id)
                if chat.admin_rights:
                    groups.append(chat.id)
            except Exception as e:
                print(f"[ERROR] Could not fetch group {dialog.id}: {e}")
    return groups

# Fetch user details from event
async def get_user(event):
    if event.is_reply:
        replied_msg = await event.get_reply_message()
        return replied_msg.sender_id
    args = event.text.split()
    if len(args) < 2:
        return None
    try:
        user = await telethn.get_entity(args[1])
        return user.id
    except:
        return None

# Global Ban Command
@telethn.on(events.NewMessage(pattern="^/gban ?(.*)"))
async def global_ban(event):
    if event.sender_id not in AUTH_USERS:
        return await event.reply("❌ **You don't have permission to use this command!**")

    user_id = await get_user(event)
    if not user_id:
        return await event.reply("⚠️ **Reply to a user or provide a user ID to gban.**")

    if user_id in AUTH_USERS:
        return await event.reply("⚠️ **You cannot gban an authorized user!**")

    reason = event.pattern_match.group(1) or "No reason provided"
    existing = GBAN_COLLECTION.find_one({"user_id": user_id})

    if existing:
        return await event.reply(f"⚠️ **User is already globally banned!**\n📝 **Reason:** `{existing['reason']}`")

    GBAN_COLLECTION.insert_one({"user_id": user_id, "reason": reason, "timestamp": datetime.utcnow()})

    groups = await get_admin_groups()
    banned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, user_id, BANNED_RIGHTS))
            banned_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to ban in {group}: {e}")

    await event.reply(f"✅ **User has been globally banned!**\n👤 **User ID:** `{user_id}`\n📝 **Reason:** `{reason}`\n🔹 **Banned in:** `{banned_count}` groups")

    # Notify the banned user
    try:
        await telethn.send_message(user_id, f"🚫 **You have been globally banned!**\n📝 **Reason:** `{reason}`")
    except:
        pass

# Global Unban Command
@telethn.on(events.NewMessage(pattern="^/ungban ?(.*)"))
async def global_unban(event):
    if event.sender_id not in AUTH_USERS:
        return await event.reply("❌ **You don't have permission to use this command!**")

    user_id = await get_user(event)
    if not user_id:
        return await event.reply("⚠️ **Reply to a user or provide a user ID to ungban.**")

    existing = GBAN_COLLECTION.find_one({"user_id": user_id})
    if not existing:
        return await event.reply("⚠️ **User is not globally banned!**")

    GBAN_COLLECTION.delete_one({"user_id": user_id})

    groups = await get_admin_groups()
    unbanned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, user_id, UNBAN_RIGHTS))
            unbanned_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to unban in {group}: {e}")

    await event.reply(f"✅ **User has been globally unbanned!**\n👤 **User ID:** `{user_id}`\n🔹 **Unbanned in:** `{unbanned_count}` groups")

    # Notify the unbanned user
    try:
        await telethn.send_message(user_id, "✅ **You have been globally unbanned!**")
    except:
        pass

# List GBanned Users
@telethn.on(events.NewMessage(pattern="^/gbanlist$"))
async def list_gbans(event):
    gbanned_users = list(GBAN_COLLECTION.find({}))
    if not gbanned_users:
        return await event.reply("📃 **No users are globally banned.**")

    text = "📜 **Globally Banned Users:**\n"
    for user in gbanned_users:
        text += f"👤 `{user['user_id']}` | 📝 `{user['reason']}`\n"

    await event.reply(text)
