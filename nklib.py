import requests, json, datetime, time, base64, zlib, random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad

baseurl = "http://fast-static-api.nkstatic.com/storage/static/appdocs/11/"
addurls = {
    "coopChallenge": "dailyChallengesCoop",
    "bossBloon": "bossData",
    "odysseyEvent": "odysseyData",
    "raceEvent": "races",
    'ac': 'dailyChallengesAdvanced',
    'dc': 'dailyChallenges'
}
headers = {"User-Agent": "btd6-windowsplayer-34.3"}
rulesets = {'map', 'rewards', 'maxTowers', 'seed', 'disableMK', 'disableSelling', 'disablePowers', 'noContinues', 'noInstaReward', 'removeableCostMultiplier', 'abilityCooldownReductionMultiplier', 'roundSets', 'maxTowers'}

# input data in bytes output decoded string
# thanks Minecool and hemi
def DG_Decode(data_bytes):
    string = ""
    for i in range(14, len(data_bytes)):
        string += chr(data_bytes[i] - 21 - (i - 14) % 6)
    return string

# just hemis code but in python(js sucks)
def saveDecode(txt, padded=None):
    salt = txt[52:76]
    encry = txt[76:]
    #key = hashlib.pbkdf2_hmac('sha1', b'11', salt, 10, dklen=32)
    key = PBKDF2(b'11', salt, 32, 10, hmac_hash_module=SHA1)
    iv = key[0:16]
    key = key[16:32]
    #encry += (16 - len(encry) % 16) * b'0' # padding
    deci = AES.new(key, AES.MODE_CBC, iv)
    plaintext = deci.decrypt(pad(encry, 16))
    return zlib.decompress(plaintext)

def saveEncode(txt):
    output = b'\x00' * 44 # dummy header
    output += b'\x02' + b'\x00' * 7
    salt = get_random_bytes(24)
    #salt = b'\xed\xda\x13x\xfc\x0fJ\x8d`V)\x96\x0e\x90\x088r\xc4\xe4\xfc\x15\x1f8g'
    key = PBKDF2(b'11', salt, 32, 10, hmac_hash_module=SHA1)
    iv = key[0:16]
    key = key[16:32]
    txt = zlib.compress(txt, level=3)
    encri = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = encri.encrypt(pad(txt, 16))
    output += salt + ciphertext
    return output
# input decoded string output event schedules
# wtf is nk doing like json.dumps???
def parseEvents(data):
    return json.loads(json.loads(data)["data"])["settings"]["events"]


# get a challenge given its code try
def fetchChallenge(code, type='custom'):
    if type in {'ac', 'dc'}:
        return challenge(json.loads(requests.get(f'https://fast-static-api.nkstatic.com/storage/static/appdocs/11/{addurls[type]}/{code}', headers=headers).content.decode()))
    elif type != 'custom': raise TypeError(f'type argument must be ac, dc, or custom for challenge codes, not {type}')
    return challenge(
        json.loads(
            zlib.decompress(
                base64.b64decode(
                    requests.get(
                        f"https://static-api.nkstatic.com/appdocs/11/es/challenges/{code.upper()}",
                        headers=headers,
                    ).content
                )
            )
        )
    )


# parses challenge data
def challenge(data):
    print(data)
    if 'normalDcm' in data.keys():
        data = data['normalDcm']
    elif 'challenge' in data.keys():
        data = data['challenge']
    output = {}
    output['hero'] = None
    try:
        output['name'] = data['name']
    except KeyError: pass
    for item in data['towers']:
        if item['max'] != 0:
            if not item['isHero']:
                output[item['tower']] = {'max': item['max'], 'upgrades': f'{min(5 - item["path1NumBlockedTiers"], 5) if item["path1NumBlockedTiers"] != -1 else 0}-{min(5 - item["path2NumBlockedTiers"], 5) if item["path2NumBlockedTiers"] != -1 else 0}-{min(5 - item["path3NumBlockedTiers"], 5) if item["path3NumBlockedTiers"] != -1 else 0}'}
            elif item['tower'] != 'ChosenPrimaryHero':
                output['hero'] = item['tower']
            elif item['tower'] == 'ChosenPrimaryHero':
                print(item['tower'])
    output['modifiers'] = {}
    for item in data['bloonModifiers'].items():
        print(item)
        if isinstance(item[1], dict):
            for iter in data['bloonModifiers']['healthMultipliers'].items():
                if iter[1] != 1:
                    output['modifiers'][f'{iter[0]}Health'] = iter[1]
        elif isinstance(item[1], float) and item[1] != 1:
            output['modifiers'][item[0]] = item[1]
        elif isinstance(item[1], bool) and item[1]:
            output['modifiers'][item[0]] = True
    output['mode'] = f'{data["difficulty"]} - {data["mode"]}'
    if data['leastCashUsed'] != -1: output['mode'] += ' - Least Cash'
    elif data['leastTiersUsed'] != -1: output['mode'] += ' - Least Tiers'
    for item in rulesets:
        wgat = type(data[item]) # switch case at home since need to filter out defaults
        if wgat == bool: # isinstance(True, int) == True for some reason
            if data[item]:
                output['modifiers'][item] = data[item]
        elif wgat == int and (data[item] != -1):
            output['modifiers'][item] = data[item]
        elif wgat == float and data[item] != 1.0:
            output['modifiers'][item] = data[item]
        elif wgat == list and len(data[item]) != 0:
            output['modifiers'][item] = data[item]
        elif wgat == str:
            output['modifiers'][item] = data[item]
    output['startRules'] = data['startRules']
    return output

# events class(data is a function since we dont need to spam nks api)
class events:
    def __init__(self, type, name, start, end):
        self.type = type
        self.name = name
        self.start = datetime.datetime.fromtimestamp(start / 1000)
        self.end = datetime.datetime.fromtimestamp(end / 1000)
        self.startReal = start

    def data(self):
        return challenge(
            json.loads(
                requests.get(
                    f"{baseurl}{addurls[self.type]}/{self.name}", headers=headers
                ).content.decode()
            )#['normalDcm']
        )


# fetches and decodes schedule
def allEvents(future=False):
    if not isinstance(future, bool): raise TypeError(f'future argument must be bool not {type(future)}')
    temp = requests.get(
        "http://static-api.nkstatic.com/nkapi/skusettings/329bcc361b4cd777ad751f1394537cba.json",
        headers=headers,
    ).content
    schedule = parseEvents(DG_Decode(temp))
    with open("events.json", "w") as f:
        f.write(json.dumps(schedule))
    data = {
        "raceEvent": [],
        "odysseyEvent": [],
        "bossBloon": [],
        "coopChallenge": [],
    }
    for item in schedule:
        if item["type"] in data.keys() and (
            (time.time() * 1000) < item["end"] if future else True
        ):
            data[item["type"]].append(
                events(item["type"], item["name"], item["start"], item["end"])
            )
    return data
