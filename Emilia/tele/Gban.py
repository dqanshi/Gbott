import time
from datetime import datetime

from telethon import events, functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from Emilia import OWNER_ID, DEV_USERS, db, telethn

# MongoDB collection for storing global bans
GBAN_DB = db["global_bans"]

# Ban & Unban permissions
BAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
UNBAN_RIGHTS = ChatBannedRights(until_date=None, view_messages=False)


async def get_admin_groups():
    """Fetches groups where the bot has admin rights and can ban users."""
    groups = []
    async for dialog in telethn.iter_dialogs():
        if dialog.is_group:
            try:
                chat = await telethn.get_entity(dialog.id)
                if chat.admin_rights and chat.admin_rights.ban_users:
                    groups.append(chat.id)
            except:
                continue  # Skip inaccessible chats
    return groups


@telethn.on(events.NewMessage(pattern=r"^/gban(?: |$)(.*)?", from_users=DEV_USERS))
async def global_ban(event):
    """Globally bans a user from all groups."""
    args = event.pattern_match.group(1)
    user_id, reason = None, "No reason provided"

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    elif args:
        user_id = args.split()[0]
        reason = " ".join(args.split()[1:]) if len(args.split()) > 1 else reason

    if not user_id:
        return await event.reply("Reply to a user or provide a user ID.")

    user = await telethn.get_entity(int(user_id))
    name = user.first_name

    # Prevent banning bot owner or developers
    if int(user_id) in OWNER_ID or int(user_id) in DEV_USERS:
        return await event.reply("❌ You cannot globally ban an owner or a developer!")

    # Check if user is already GBanned
    if GBAN_DB.find_one({"user_id": int(user_id)}):
        return await event.reply(f"⚠️ [{name}](tg://user?id={user_id}) is already globally banned.")

    groups = await get_admin_groups()
    banned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, int(user_id), BAN_RIGHTS))
            banned_count += 1
        except:
            continue

    # Store ban in DB
    ban_data = {
        "user_id": int(user_id),
        "name": name,
        "reason": reason,
        "banned_by": event.sender_id,
        "banned_at": int(time.time()),
        "groups_banned": banned_count,
    }
    GBAN_DB.insert_one(ban_data)

    # Log Message
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_message = (
        f"🚨 **Global Ban Issued** 🚨\n\n"
        f"👤 **User:** [{name}](tg://user?id={user_id})\n"
        f"🔨 **Banned By:** [{event.sender.first_name}](tg://user?id={event.sender_id})\n"
        f"📌 **Reason:** {reason}\n"
        f"📅 **Date:** {timestamp}\n"
        f"📢 **Groups Banned From:** {banned_count}"
    )

    # Send logs to owner & admin
    try:
        await telethn.send_message(OWNER_ID[0], log_message)
        await telethn.send_message(event.sender_id, log_message)
    except:
        pass

    await event.reply(f"✅ **Globally Banned** [{name}](tg://user?id={user_id}) in {banned_count} groups!")


@telethn.on(events.NewMessage(pattern=r"^/ungban(?: |$)(\d+)?", from_users=DEV_USERS))
async def global_unban(event):
    """Globally unbans a user from all groups."""
    args = event.pattern_match.group(1)
    user_id = None

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    elif args:
        user_id = args

    if not user_id:
        return await event.reply("Reply to a user or provide a user ID.")

    user = await telethn.get_entity(int(user_id))
    name = user.first_name

    # Check if user is globally banned
    if not GBAN_DB.find_one({"user_id": int(user_id)}):
        return await event.reply(f"⚠️ [{name}](tg://user?id={user_id}) is not globally banned.")

    groups = await get_admin_groups()
    unbanned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, int(user_id), UNBAN_RIGHTS))
            unbanned_count += 1
        except:
            continue

    # Remove from DB
    GBAN_DB.delete_one({"user_id": int(user_id)})

    # Log Message
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_message = (
        f"✅ **Global Unban Issued** ✅\n\n"
        f"👤 **User:** [{name}](tg://user?id={user_id})\n"
        f"🔓 **Unbanned By:** [{event.sender.first_name}](tg://user?id={event.sender_id})\n"
        f"📅 **Date:** {timestamp}\n"
        f"📢 **Groups Unbanned From:** {unbanned_count}"
    )

    # Send logs to owner & admin
    try:
        await telethn.send_message(OWNER_ID[0], log_message)
        await telethn.send_message(event.sender_id, log_message)
    except:
        pass

    await event.reply(f"✅ **Globally Unbanned** [{name}](tg://user?id={user_id}) from {unbanned_count} groups!")


@telethn.on(events.ChatAction)
async def auto_gban(event):
    """Auto-bans globally banned users when they join a group."""
    if event.user_joined or event.user_added:
        user_id = event.user_id
        ban_data = GBAN_DB.find_one({"user_id": int(user_id)})

        if ban_data:
            try:
                await telethn(EditBannedRequest(event.chat_id, int(user_id), BAN_RIGHTS))
                await event.reply(
                    f"🚨 **Auto Global Ban** 🚨\n"
                    f"👤 **User:** [{ban_data['name']}](tg://user?id={user_id})\n"
                    f"📌 **Reason:** {ban_data['reason']}"
                )
            except:
                pass


@telethn.on(events.NewMessage(pattern=r"^/gbanlist$", from_users=DEV_USERS))
async def gban_list(event):
    """Shows all globally banned users."""
    bans = list(GBAN_DB.find())
    if not bans:
        return await event.reply("✅ No users are globally banned.")

    message = "**🛑 Globally Banned Users List 🛑**\n\n"
    for ban in bans:
        message += f"👤 [{ban['name']}](tg://user?id={ban['user_id']})\n"
        message += f"📌 **Reason:** {ban['reason']}\n"
        message += f"📅 **Banned At:** {datetime.utcfromtimestamp(ban['banned_at']).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        message += f"📢 **Groups Affected:** {ban['groups_banned']}\n\n"

    await event.reply(message)
