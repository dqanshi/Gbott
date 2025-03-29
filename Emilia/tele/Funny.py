import random

from telethon import events

from Emilia import telethn, ORIGINAL_EVENT_LOOP

loha = [
"She was beautiful, not like those girls in the magazines. She was beautiful for the way she thought.",
"Her soul is like a diamond, beautiful and unbreakable.",
"You are a rare gem, a single soul in a world of billions.",
"Her smile is the most captivating beauty.",
"She is the embodiment of grace, charm, and beauty.",
"Her love for others makes her even more beautiful.",
"She walks in beauty, like the night.",
"Her inner beauty captivates and enchants.",
"Her laughter is an orchestra of beauty in its purest form.",
"A strong woman looks a challenge in the eye and gives it a wink."
    ]


@telethn.on(events.NewMessage(pattern="(?i)Aloha$"))
async def Emi_(m: events.NewMessage):
    if not ORIGINAL_EVENT_LOOP:
        return
    one = random.choice(loha)
    await m.reply(one)
