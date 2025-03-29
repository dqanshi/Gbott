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


@telethn.on(events.NewMessage(pattern="(?i)Angel$"))
async def Emi_(m: events.NewMessage):
    if not ORIGINAL_EVENT_LOOP:
        return
    uwu = random.choice(OWO)
    await m.reply(uwu)
