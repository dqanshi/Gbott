import random

from telethon import events

from Emilia import telethn, ORIGINAL_EVENT_LOOP

loha = [
"odra"
"poda"
"kilavan"
"kilavi"
"run"
"mari iri angot"
"thenga"
"vazha"
"mandi"
"pottan"
    ]


@telethn.on(events.NewMessage(pattern="(?i)Aloha$"))
async def Emi_(m: events.NewMessage):
    if not ORIGINAL_EVENT_LOOP:
        return
    uwu = random.choice(loha)
    await m.reply(loha)
