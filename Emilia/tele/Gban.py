import time
from datetime import datetime
from telethon import events, functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import UserIdInvalidError, ChatAdminRequiredError
from Emilia import OWNER_ID, DEV_USERS, db, telethn

GBAN_DB = db["global_bans"]

BAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=False,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)


async def get_admin_groups():
    groups = []
    try:
        async for dialog in telethn.iter_dialogs():
            if dialog.is_group:
                try:
                    chat = await telethn.get_entity(dialog.id)
                    if hasattr(chat, 'admin_rights') and chat.admin_rights and chat.admin_rights.ban_users:
                        groups.append(chat.id)
                except Exception:
                    continue
    except Exception as e:
        print(f"Error fetching admin groups: {str(e)}")
    return groups


@telethn.on(events.NewMessage(pattern=r"^/gban(?: |$)(.*)?", from_users=DEV_USERS))
async def global_ban(event):
    args = event.pattern_match.group(1)
    user_id = None

    try:
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        elif args:
            user_id = int(args.split()[0])
    except ValueError:
        return await event.reply("❌ Invalid user ID format. Please use a valid numeric ID.")
    except Exception as e:
        return await event.reply(f"❌ Error processing command: {str(e)}")

    if not user_id:
        return await event.reply("❌ Please reply to a user or provide a user ID.")

    # Prevent banning Owner & Developers
    if user_id == OWNER_ID or user_id in DEV_USERS:
        return await event.reply("🚫 You cannot globally ban the owner or developers.")

    try:
        user = await telethn.get_entity(int(user_id))
        name = user.first_name or "Unknown"
    except UserIdInvalidError:
        return await event.reply("❌ Invalid user ID provided.")
    except Exception as e:
        return await event.reply(f"❌ Error fetching user: {str(e)}")

    if await GBAN_DB.find_one({"user_id": int(user_id)}):
        return await event.reply(f"⚠️ [{name}](tg://user?id={user_id}) is already globally banned.")

    groups = await get_admin_groups()
    banned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, int(user_id), BAN_RIGHTS))
            banned_count += 1
        except ChatAdminRequiredError:
            continue
        except Exception:
            continue

    try:
        await GBAN_DB.insert_one({
            "user_id": int(user_id),
            "name": name,
            "banned_at": int(time.time()),
            "groups_banned": banned_count
        })
    except Exception as e:
        await event.reply(f"⚠️ Warning: Banned user but failed to add to database: {str(e)}")

    response = f"✅ Banned [{name}](tg://user?id={user_id}) from {banned_count} groups!"
    try:
        await event.reply(response)
    except Exception as e:
        print(f"Error sending response: {str(e)}")




@telethn.on(events.NewMessage(pattern=r"^/gbanlist$", from_users=DEV_USERS))
async def gban_list(event):
    banned_users = []
    async for user in GBAN_DB.find():
        banned_users.append(user)

    if not banned_users:
        return await event.reply("📜 No users are globally banned.")

    response = "**🚨 Global Ban List:**\n\n"
    for user in banned_users:
        banned_at = datetime.utcfromtimestamp(user["banned_at"]).strftime("%Y-%m-%d %H:%M:%S")
        response += f"• [{user['name']}](tg://user?id={user['user_id']}) - Banned from {user['groups_banned']} groups on {banned_at}\n"

    try:
        await event.reply(response)
    except Exception as e:
        print(f"Error sending ban list: {str(e)}")



@telethn.on(events.NewMessage(pattern=r"^/ungban(?: |$)(.*)?", from_users=DEV_USERS))
async def global_unban(event):
    args = event.pattern_match.group(1)
    user_id = None

    try:
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        elif args:
            user_id = int(args.split()[0])
    except ValueError:
        return await event.reply("❌ Invalid user ID format. Please use a valid numeric ID.")
    except Exception as e:
        return await event.reply(f"❌ Error processing command: {str(e)}")

    if not user_id:
        return await event.reply("❌ Please reply to a user or provide a user ID.")

    # Prevent unbanning Owner & Developers
    if user_id == OWNER_ID or user_id in DEV_USERS:
        return await event.reply("🚫 You cannot unban the owner or developers.")

    ban_data = await GBAN_DB.find_one({"user_id": int(user_id)})
    if not ban_data:
        return await event.reply(f"⚠️ This user is not globally banned.")

    name = ban_data["name"]
    groups = await get_admin_groups()
    unbanned_count = 0

    for group in groups:
        try:
            await telethn(EditBannedRequest(group, int(user_id), UNBAN_RIGHTS))
            unbanned_count += 1
        except ChatAdminRequiredError:
            continue
        except Exception:
            continue

    try:
        await GBAN_DB.delete_one({"user_id": int(user_id)})
    except Exception as e:
        await event.reply(f"⚠️ Warning: Unbanned user but failed to remove from database: {str(e)}")

    response = f"✅ Unbanned [{name}](tg://user?id={user_id}) from {unbanned_count} groups!"
    try:
        await event.reply(response)
    except Exception as e:
        print(f"Error sending response: {str(e)}")
    



@telethn.on(events.ChatAction)
async def auto_gban(event):
    if not (event.user_joined or event.user_added):
        return
        
    user_id = event.user_id
    ban_data = await GBAN_DB.find_one({"user_id": int(user_id)})

    if ban_data:
        try:
            await telethn(EditBannedRequest(event.chat_id, int(user_id), BAN_RIGHTS))
            await event.reply(
                f"🚨 Auto-banned [{ban_data['name']}](tg://user?id={user_id}) "
                f"from this group (previously banned in {ban_data['groups_banned']} groups)"
            )
        except ChatAdminRequiredError:
            return
        except Exception as e:
            print(f"Error auto-banning user {user_id} in chat {event.chat_id}: {str(e)}")
    
