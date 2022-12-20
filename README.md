# NKLib
### Python module to interact with NK's API and stuff

# Credits
Minecool for helping me in cq server and giving the events data URL

Hemidemisemipresent's [NkSku repo](https://github.com/hemisemidemipresent/NKsku), which is where the Profile.Save stuff was ~~stolen~~ taken

And ofc credits too Hemi's repo's credits

# Installation
I will upload it to PyPI when it doesnt look cancer for now just like download this and put it in your cd

# scuffed docs
## profile.save
### function `saveDecode(txt)`
input: a **bytestring** of NK's save file(aka Profile.Save located at ``C:\Program Files (x86)\Steam\userdata\STEAM_USER_ID\960090\local\link\PRODUCTION\current\Profile.Save``

output: a **bytestring** of the decoded Profile.Save(not parsed at all it looks cancer)

### function `saveEncode(txt)`
input: a **bytestring** of the decoded Profile.Save data(like the output of ``saveDecode``)

output: a **bytestring** of the encoded data which can be put into the Profile.Save

## How to use

```py
# Decodes Profile.Save
with open('Profile.Save', 'rb') as f:
    txt = f.read()
    txt = nklib.saveDecode(txt)
with open('output', 'wb') as f:
    f.write(txt)
# Encodes Profile.Save
with open('output.txt', 'rb') as f:
    txt = f.read()
    txt = nklib.saveEncode(txt)
with open('Profile.Save', 'wb') as f:
    f.write(txt)
```
**use WB or RB mode for reading/writing as they mean read binary/write binary**

If you are trying to use this to cheat(dont) then you need to turn off your Wifi when opening the game so it can't fetch your save from NK's API

---
## events
### function `allEvents(future=False)`
input: None, or future=True if you want events that **end** after the current time

output: a **dictionary** with list of events classes as values

## How to use
```py
events = nklib.allEvents(future=True)
print(events["bossBloon"][0].name)
# Dreadbloon2
```

---

## challenges
### function `fetchChallenge(code, type='custom)`
input: either a challenge code(as a **string**) or the number of a daily/advanced challenge(as an **int**)
(**daily challenges are offset with advanced challenges by 13, for example daily challenge 1592 shows up on the same day as advanced challenge 1579**)

output: the parsed and decoded data of the challenge

> coop challenges are **events**, so use allEvents to get them

## How to use
```py
data = nklib.fetchChallenge('zmxhrla') # does not have to be uppercase # nklib.fetchChallenge(1000, type='ac')
print(data) #{'hero': 'ANY', 'name': 'Agony', 'DartMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'BoomerangMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'BombShooter': {'max': -1, 'upgrades': '5-5-5'}, 'TackShooter': {'max': -1, 'upgrades': '5-5-5'}, 'IceMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'GlueGunner': {'max': -1, 'upgrades': '5-5-5'}, 'SniperMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeySub': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeyBuccaneer': {'max': -1, 'upgrades': '5-5-5'}, 'MortarMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'DartlingGunner': {'max': -1, 'upgrades': '5-5-5'}, 'WizardMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'SuperMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'NinjaMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'Alchemist': {'max': -1, 'upgrades': '5-5-5'}, 'Druid': {'max': -1, 'upgrades': '5-5-5'}, 'SpikeFactory': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeyVillage': {'max': -1, 'upgrades': '5-5-5'}, 'EngineerMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'modifiers': {'speedMultiplier': 1.05, 'moabSpeedMultiplier': 1.1, 'regrowRateMultiplier': 1.5, 'bloonsHealth': 1.5, 'moabsHealth': 1.5, 'disablePowers': True, 'noContinues': True, 'disableSelling': True, 'map': 'Geared', 'removeableCostMultiplier': 12.0, 'rewards': '', 'noInstaReward': True, 'seed': 60315120}, 'mode': 'Hard - HalfCash', 'startRules': {'lives': 1, 'maxLives': 1, 'cash': -1, 'round': 3, 'endRound': 100}}
```

---

## events but real
### class `events`

input: None, you should not use this, it is only used for the output of allEvents

### values
self.name: contains the name of the challenge/event

self.type: the type of event(ex. bossBloon, raceEvent, etc)

self.start: the start timestamp fed through datetime.datetime.fromtimestamp

self.end: like self.start but self explanatory

self.startReal: the raw start time of the event(in unix **millis**)
### functions

it has a singular function, `data`, which fetches the data of the class

## how to use
```py
events = nklib.allEvents(future=True)
print(events['raceEvent'][0].data())
# {'hero': 'ANY', 'name': 'Treet yourself', 'Alchemist': {'max': -1, 'upgrades': '5-5-5'}, 'BananaFarm': {'max': -1, 'upgrades': '5-5-5'}, 'BombShooter': {'max': -1, 'upgrades': '5-5-5'}, 'BoomerangMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'DartMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'Druid': {'max': -1, 'upgrades': '5-5-5'}, 'GlueGunner': {'max': -1, 'upgrades': '5-5-5'}, 'HeliPilot': {'max': -1, 'upgrades': '5-5-5'}, 'IceMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeyAce': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeyBuccaneer': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeySub': {'max': -1, 'upgrades': '5-5-5'}, 'MonkeyVillage': {'max': -1, 'upgrades': '5-5-5'}, 'NinjaMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'SniperMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'SpikeFactory': {'max': -1, 'upgrades': '5-5-5'}, 'SuperMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'TackShooter': {'max': -1, 'upgrades': '5-5-5'}, 'WizardMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'MortarMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'EngineerMonkey': {'max': -1, 'upgrades': '5-5-5'}, 'DartlingGunner': {'max': -1, 'upgrades': '5-5-5'}, 'BeastHandler': {'max': -1, 'upgrades': '5-5-5'}, 'modifiers': {'seed': 1, 'map': 'OneTwoTree', 'rewards': 'MonkeyMoney:50#Trophy:2'}, 'mode': 'Easy - Standard', 'startRules': {'lives': -1, 'cash': 1230, 'round': 10, 'maxLives': -1, 'endRound': 100}}
```
---

# something about nk updates
change this like `headers = {"User-Agent": "btd6-windowsplayer-34.3"}` to whatever version it is in the future

the events url is different for every device and user, this current one is for 34.3, to get a new one either ask in cq server(easy) or set up a proxy to find it
the url is in `allEvents` at     
```py
temp = requests.get(
        "http://static-api.nkstatic.com/nkapi/skusettings/329bcc361b4cd777ad751f1394537cba.json",
        headers=headers,
    ).content
```
