import random

from telethon import events

from Emilia import telethn, ORIGINAL_EVENT_LOOP

GDMORNING = [
    "`ഒരു താൽക്കാലിക ജീവിതത്തിൽ നിങ്ങൾക്ക് എല്ലാം ശാശ്വതമായി ഉൾക്കൊള്ളാൻ കഴിയില്ലെന്ന് നിങ്ങൾ മനസ്സിലാക്കുമ്പോൾ ജീവിതം വളരെ എളുപ്പമാകും. മനോഹരമായ ഒരു ദിനം ആശംസിക്കുന്നു. സുപ്രഭാതം!`",
    "`വീണുപോയ പൂക്കൾക്ക് മരത്തിൽ വീണ്ടും വളരാൻ കഴിയില്ല, പക്ഷേ വേരുകൾ ശക്തമാണെങ്കിൽ, പുതിയ പൂക്കൾക്ക് തീർച്ചയായും കഴിയും .. ജീവിതം ഇതുവരെ നമുക്ക് ചെയ്യാൻ കഴിയാത്തതിനെക്കുറിച്ചല്ല, നമുക്ക് ഇപ്പോഴും ചെയ്യാൻ കഴിയുന്നതിനെക്കുറിച്ചല്ല .... സുപ്രഭാതം!`",
    "`സന്തോഷകരമായ ജീവിതത്തിനുള്ള ഒരു ലളിതമായ ഫോർമുല. ഒരിക്കലും ആരെയും പരാജയപ്പെടുത്താൻ ശ്രമിക്കരുത്, എല്ലാവരേയും വിജയിപ്പിക്കാൻ ശ്രമിക്കുക, ആരെയും പരിഹസിക്കാതെ എല്ലാവരുമായും ചിരിക്കരുത്. സുപ്രഭാതം!`",
    "`ഓരോ പുതിയ പ്രഭാതത്തിലും നിങ്ങളുടെ പശ്ചാത്താപം മായ്‌ക്കാനുള്ള അവസരം നിങ്ങൾക്ക് ലഭിക്കും. ഇന്നലത്തെ നിർഭാഗ്യങ്ങൾ മറന്ന ഒരു രാജാവിനെപ്പോലെ ജീവിക്കുക. സുപ്രഭാതം!`",
    "`കഠിനാധ്വാനം ചെയ്യുക, കഠിനമായി കളിക്കുക, നിങ്ങളുടെ ജീവിതത്തിലെ ഓരോ നിമിഷവും ആസ്വദിക്കുക, എല്ലാ ദിവസവും രാവിലെ ഉണരുക എന്നത് ആഘോഷിക്കേണ്ട ഒരു സമ്മാനമാണെന്ന് ഓർമ്മിക്കുക, അതിനാൽ നന്ദിയോടെ ദിവസം സ്വീകരിക്കുക!`",
    "`എല്ലാ പ്രഭാതത്തിലും പുതിയ പ്രതീക്ഷകൾ നൽകുന്നു, ഓരോ പ്രതീക്ഷയും നമ്മുടെ സ്വപ്നങ്ങൾക്ക് പുതിയ ജീവിതം നൽകുന്നു, ഓരോ സ്വപ്നവും മറ്റുള്ളവർക്ക് പ്രചോദനം നൽകുന്നു. എല്ലാ ദിവസവും നിങ്ങൾക്ക് മനോഹരമായ പ്രഭാതം നേരുന്നു!`",
    "`ലോകത്തിലെ മനോഹരമായ സ്ഥലം ഒരാളുടെ ഹൃദയത്തിലും മറ്റൊരാളുടെ ചിന്തകളിലും മറ്റൊരാളുടെ പ്രാർത്ഥനയിലുമാണ്. ഒരു നല്ല ദിവസം ആശംസിക്കുന്നു സുപ്രഭാതം!`",
    "`ആരെങ്കിലും നിങ്ങളുടെ ജീവിതത്തിന്റെ ഭാഗമാകാൻ ഗ seriously രവമായി ആഗ്രഹിക്കുന്നുവെങ്കിൽ, അവർ അതിൽ ഗൗരവമായി ശ്രമിക്കും. കാരണങ്ങളൊന്നുമില്ല. ഒഴികഴിവുകളൊന്നുമില്ല. സുപ്രഭാതം!`",
    "`ബുദ്ധിമുട്ടുള്ള റോഡ് പലപ്പോഴും മനോഹരമായ സ്ഥലങ്ങളിലേക്ക് നയിക്കുന്നു. സുപ്രഭാതം!!`",
    "`എല്ലാ പ്രശ്നങ്ങളും മനസും കാര്യവും തമ്മിൽ കുടുങ്ങിയിരിക്കുന്നു. നിങ്ങൾ ചിന്തിക്കുന്നില്ലെങ്കിൽ, അത് പ്രശ്നമല്ല. സുപ്രഭാതം! അതിശയകരമായ ഒരു ദിവസം ആശംസിക്കുന്നു!`",
    "`സന്തുഷ്ടനായ ഒരു വ്യക്തി സന്തുഷ്ടനാണ്, കാരണം അവന്റെ ജീവിതത്തിൽ എല്ലാം ശരിയാണ്. ജീവിതത്തിലെ എല്ലാ കാര്യങ്ങളോടും ഉള്ള മനോഭാവം ശരിയായതിനാൽ അദ്ദേഹം സന്തുഷ്ടനാണ്. സുപ്രഭാതം.`",
    "`നിങ്ങളുടെ സ്വന്തം കൊടുങ്കാറ്റിലൂടെ കടന്നുപോകുമ്പോൾ മറ്റൊരാളെ അനുഗ്രഹിക്കാൻ കഴിയുക എന്നതാണ് ചിലപ്പോൾ ജീവിതത്തിലെ ഏറ്റവും വലിയ പരീക്ഷണം. സുപ്രഭാതം!`",
    "`സുപ്രഭാതം. നിങ്ങൾക്ക് ഒരേ നിമിഷം രണ്ടുതവണ ലഭിക്കില്ലെന്ന ലളിതമായ വസ്തുത മനസ്സിലാക്കുമ്പോൾ ജീവിതം കൂടുതൽ അർത്ഥവത്താകുന്നു!`",
    "`വിഷമിക്കുന്നത് നാളത്തെ പ്രശ്‌നങ്ങൾ ഇല്ലാതാക്കുന്നില്ല, അത് ഇന്നത്തെ സമാധാനത്തെ കവർന്നെടുക്കുന്നു. സുപ്രഭാതം!`",
    "`കിളി കൊഞ്ചലിന്റെ നാദവും, ഉദയ സൂര്യന്റെ പൊന്‍ കിരണങ്ങളും ഭൂമിയെ തഴുകുന്ന ഈ പ്രഭാതത്തില്‍ എന്റെ സുഹൃത്തുക്കള്‍ക്ക് നേരുന്നു എന്‍ ശുഭദിനം!`",
    "`മഞ്ഞു പുതപ്പില്‍ ഉണരാന്‍ മടിച്ചുറങ്ങുന്ന പ്രകൃ തിയെ നേര്‍ത്ത പൊന്‍ കിരണങ്ങളാല്‍ തഴുകി ഉണര്‍ത്തുന്ന സൂര്യനും ഉറക്കത്തിന്‍റെ ആലസ്യം വിടാതെ കണ്‍‌തുറന്നു നോക്കുന്ന കുഞ്ഞു പുല്‍കൊടികളും നല്ലൊരു ദിവസത്തിനായി ഉറ്റു നോക്കി കൊണ്ടിരിക്കുന്നു !`",
    "`അരികിലില്ലെങ്കിലും നിന്റെ സ്നേഹനത്തിന്റെ ആഴം ഞാൻ മനസ്സിലാക്കുന്നു. ഗുഡ് മോർണിംഗ്.`",
    "`ലോകത്തിന്റെ ഏതു കോണിലായാലും എന്റെ മനസ്സ് എന്നും നിന്നോടൊപ്പം ഉണ്ടാവും. ഗുഡ് മോർണിംഗ്!`",
    "`അരികിലില്ലെങ്കിലും എന്റെ മനസ്സിന്റെ ഒരു കോണിൽ എന്നും നീ മാത്രമാണ്. ഗുഡ് മോർണിംഗ്!`",
    "`ഒരോ പ്രഭാതവും ഒരു പുതിയ പ്രതീക്ഷയാണ്, ഒരു പുതിയ തുടക്കമാണ്. ഇത് നല്ലൊരു തുടക്കം ആവട്ടെ. ഗുഡ് മോർണിംഗ്!`",
    "`രാണസഖിയായി നീ കൂടെയുണ്ടെങ്കിൽ ജീവിതത്തിൽ മറ്റെന്താണ് എനിയ്ക്കു വേണ്ടത്? നല്ല ഒരു ദിനം എന്റെ നല്ലപാതിയ്ക്ക് നേരുന്നു!`",
    "`നമ്മുടെ ഇന്നിനെ നാം നന്നാക്കാൻ ശ്രമിച്ചാൽ നമ്മുടെ നാളെയും നല്ലതായിത്തീരും. ഗുഡ് മോർണിംഗ്!`",
    "`പുതിയ പ്രതീക്ഷകളും സന്തോഷങ്ങളുമായി ഒരു പുതിയ പൊൻപുലരി കൂടിയിതാ. ഈ സുദിനത്തിൽ നിങ്ങളുടെ എല്ലാ ആഗ്രഹങ്ങളും സഫലമാകട്ടെ. ഗുഡ് മോർണിംഗ്.`",
    "`സന്തോഷവും, സമാധാനവും നമ്മുടെ ഉള്ളിൽ തന്നെയാണ്. അത് കണ്ടെത്തുമ്പോൾ ജീവിതം സുന്ദരമാവുന്നു. ശുഭ ദിനം!`",
    "`കഴിഞ്ഞു പോയതിനെ കുറിച്ചോർത്തു ദുഖിക്കാതെ, വരാനിരിയ്ക്കുന്നതിനെ ഓർത്തു സന്തോഷിയ്ക്കുക. ശുഭ ദിനം!`",
    "`ഈ മെസ്സേജ് കാണുമ്പോൾ നിങ്ങളുടെ മുഖത്തു വിരിയുന്ന ആ പുഞ്ചിരിയുണ്ടല്ലോ അതാണ് എന്റെ ഏറ്റവും വലിയ സന്തോഷം. ഗുഡ് മോർണിംഗ്!`",
    "`ഒരോ പ്രഭാതവും ഒരോ പുതിയ അവസങ്ങളാണ്. ഈ അവസരം നിങ്ങൾക്ക് ഏറ്റവും അനുയോജ്യമായി വിനിയോഗിയ്ക്കാൻ സാധിയ്ക്കയട്ടെ. ഗുഡ് മോർണിംഗ്!`",
    "`മാറ്റങ്ങൾ അനിവാര്യമാണ്. ജീവിതത്തിലെ ഓരോ മാറ്റത്തോടും നാം എങ്ങിനെ പ്രതികരിയ്ക്കുന്നു എന്നതാണ് നമ്മുടെ ജീവിത വിജയവും പരാജയവും തീരുമാനിക്കുന്നത്. ഗുഡ് മോർണിംഗ്!`",
    "`നിങ്ങൾ ലോകത്തെ മാറ്റാൻ ആഗ്രഹിയ്ക്കുന്നു എങ്കിൽ ആദ്യം സ്വയം മാറ്റം ഉൾകൊള്ളാൻ തയ്യാറാവുക. ശുഭ ദിനം നേരുന്നു!`",
    "`ഹൃതുഭേദങ്ങൾ മാറിയാലും എനിയ്ക്കു നിന്നോടുള്ള സ്നേഹം ഒരിയ്ക്കലും മായില്ല. ശുഭ ദിനം!`",
    "`സ്വന്തം കഴിവിൽ വിശ്വസിയ്ക്കുക, പ്രയത്നിയ്ക്കുക ഈ ലോകം നിങ്ങള്ക്ക് കീഴടക്കാൻ സാധിയ്ക്കും. ഗുഡ് മോർണിംഗ്!`",
    "`ഇന്നത്തെ പ്രഭാതം നിങ്ങള്ക്ക് എല്ലാ സന്തോഷങ്ങളും ഐശ്വര്യങ്ങളും കൊണ്ടുവരട്ടെ. സുപ്രഭാതം!`",
    "`സുര്യനെപ്പോലെ ചുറ്റും പ്രകാശം പരത്താൻ നിങ്ങള്ക്ക് സാധിയ്ക്കട്ടെ. ഗുഡ് മോർണിംഗ്.`",
    "`ഈ പ്രഭാത പൊട്ടി വിടരുമ്പോൾ മനസ്സിനുസന്തോഷവും, കണ്ണിനു കുളിർമയും നൽകുന്ന കാഴ്ച്ചകളാകട്ടെ നിങ്ങളെ കാത്തിരിയ്ക്കുന്നത്. ഗുഡ് മോർണിംഗ്!`",
    "`ജീവിതത്തിലെ എല്ലാ നിമിഷങ്ങളെയും നമുക്ക് നിയന്ത്രിയ്ക്കാൻ സാധിയ്ക്കില്ല. നമുക്ക് സാധിയ്ക്കുന്നതു ആ നിമിഷങ്ങളോടുള്ള നമ്മുടെ മനോഭാവം നിയന്ത്രിയ്ക്കുക എന്നതാണ്. ഗുഡ് മോർണിംഗ്.`",
]



@telethn.on(events.NewMessage(pattern=r"(?i)^(good\s?morning|gdmorning|gd\s?morning)$"))
async def good_morning_handler(event: events.NewMessage):
    if not ORIGINAL_EVENT_LOOP:
        return
    await event.reply(random.choice(GDMORNING))
