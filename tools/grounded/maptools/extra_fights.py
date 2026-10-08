#!/usr/bin/env python3
"""Project Grounded: extra gevechten in de wereld (Wally in Mt. Pyre en Mossdeep; Zinnia, Dave, Mitch en SickBlik
eerder in de game; een verstopte Shy Guy in de woestijn van Route 111).

Idempotent; beheert zijn eigen stukken in:
  - include/constants/opponents.h (blok tussen '// extra_fights {' en '// }'; TRAINERS_COUNT),
  - src/data/trainers.party (blok achteraan tussen '/* --- extra_fights --- */'-markeringen),
  - data/maps/<kaart>/map.json (objecten met local_id LOCALID_EF_*),
  - data/maps/<kaart>/scripts.inc (blok tussen '@ extra_fights {' en '@ }').
Muziek/transitie: src/pokemon.c (GetTrainerBattleBGM) en src/battle_setup.c (GetTrainerBattleTransition) noemen de
nieuwe trainers met de hand (IsDaveTrainer() e.d.).

Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/extra_fights.py
"""
import json, os, re, struct

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

FIRST_ID = 1134

# Teksten: Wally praat gebroken Engels (zijn twee openingszinnen zijn letterlijk van Jordi).
FIGHTS = [
    dict(const='WALLY_MT_PYRE', map='MtPyre_1F', x=9, y=4, gfx='OBJ_EVENT_GFX_WALLY', face='RIGHT', sight=3,
         label='WallyPyre', hide=True,
         intro=r"WALLY: {PLAYER}! Mountain of grave!\p"
               r"Scare no much, horror watching\nwhen young many.\p"
               r"Ghost now is friend team.\nBoo! You scare? I no scare.$",
         defeat=r"Aaah! Now real scare…$",
         post=r"WALLY: Horror rule number one:\nnever split up.\p"
              r"…I split up from you now.\nNot scare. Is cardio.$",
         party="""Name: WALLY
Class: Rival
Pic: Wally
Gender: Male
Music: Male
Items: Super Potion / Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Purple

Shedinja @ Focus Sash
Level: 42
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Shadow Sneak
- X-Scissor
- Will-O-Wisp
- Protect

Banette
Level: 42
Ability: Prankster
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Shadow Claw
- Knock Off
- Thunder Wave
- Destiny Bond

Gourgeist
Level: 42
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Phantom Force
- Seed Bomb
- Leech Seed
- Trick-or-Treat

Gyarados
Level: 42
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Waterfall
- Crunch
- Dragon Dance
- Scary Face

Annihilape
Level: 42
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Rage Fist
- Drain Punch
- Bulk Up
- Rock Slide

Gallade @ Sitrus Berry
Level: 44
Ability: Sharpness
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Psycho Cut
- Night Slash
- Shadow Sneak
- Leaf Blade
"""),
    dict(const='WALLY_MOSSDEEP', map='MossdeepCity', x=68, y=17, gfx='OBJ_EVENT_GFX_WALLY', face='LEFT', sight=4,
         label='WallySpace', hide=True,
         intro=r"WALLY: {PLAYER}! Look, rocket house!\p"
               r"Gallader psychic feel good in\nspacing placing.\p"
               r"Brain big now. Battle with brain!$",
         defeat=r"Brain… small again…$",
         post=r"WALLY: In space no air.\nGallader no need air.\p"
              r"Gallader need hug. I go hug.\nBye-bye, {PLAYER}!$",
         party="""Name: WALLY
Class: Rival
Pic: Wally
Gender: Male
Music: Male
Items: Hyper Potion / Hyper Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Purple

Solrock
Level: 47
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Zen Headbutt
- Rock Slide
- Morning Sun
- Sunny Day

Lunatone
Level: 47
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Psychic
- Moonblast
- Power Gem
- Calm Mind

Bronzong
Level: 47
Ability: Heatproof
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Gyro Ball
- Psychic
- Trick Room
- Stealth Rock

Darmanitan @ Charcoal
Level: 47
Ability: Zen Mode
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Flare Blitz
- Psychic
- Rock Slide
- U-Turn

Arctibax
Level: 47
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Icicle Crash
- Dragon Claw
- Ice Shard
- Dragon Dance

Gallade @ Sitrus Berry
Level: 49
Ability: Sharpness
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Psycho Cut
- Sacred Sword
- Leaf Blade
- Swords Dance
"""),
    dict(const='ZINNIA_ROUTE_114', map='Route114', x=22, y=34, gfx='OBJ_EVENT_GFX_ZINNIA', face='LEFT', sight=4,
         label='Zinnia',
         intro=r"ZINNIA: Shh. Listen. Hear that?\pA lake full of meteors, crashing\n"
               r"down for ten thousand years.\pMy people wrote a song about it.\n"
               r"Forty-seven verses.\pI'll hum it while I beat you.$",
         defeat=r"Verse thirty-two is about you now.\nIt's not flattering.$",
         post=r"ZINNIA: Somewhere up there, a rock\nis still falling.\p"
              r"Ten thousand years of falling.\nHonestly? Relatable.$",
         party="""Name: ZINNIA
Class: Lorekeeper
Pic: Zinnia
Gender: Female
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Green

Aster (Whismur) @ Eviolite
Level: 25
Ability: Soundproof
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Uproar
- Echoed Voice
- Ember
- Astonish

Swablu
Level: 25
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Dragon Breath
- Fairy Wind
- Sing
- Round

Noibat
Level: 25
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Air Cutter
- Bite
- Supersonic
- Screech

Bagon @ Dragon Fang
Level: 27
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Dragon Breath
- Headbutt
- Leer
- Focus Energy
"""),
    dict(const='ZINNIA_ROUTE_119', map='Route119', x=33, y=10, gfx='OBJ_EVENT_GFX_ZINNIA', face='LEFT', sight=4,
         label='Zinnia',
         intro=r"ZINNIA: You again. Good.\pThe clouds here feel wrong.\n"
               r"Something up there is ancient,\lgreen and extremely bored.\p"
               r"Let's make some noise so it\nnotices us. Aster, sing!$",
         defeat=r"Aster sang flat. Aster always\nsings flat. I love her anyway.$",
         post=r"ZINNIA: Keep climbing. The sky\nkeeps its own score.\p"
              r"So do I. You're one up.\nI'll take it back at the top.$",
         party="""Name: ZINNIA
Class: Lorekeeper
Pic: Zinnia
Gender: Female
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Green

Aster (Whismur) @ Eviolite
Level: 36
Ability: Soundproof
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Hyper Voice
- Fire Punch
- Ice Punch
- Shadow Ball

Altaria
Level: 36
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Dragon Pulse
- Moonblast
- Cotton Guard
- Roost

Noibat
Level: 36
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Air Slash
- Dragon Pulse
- Super Fang
- Tailwind

Tyrunt
Level: 36
Ability: Strong Jaw
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Crunch
- Dragon Tail
- Rock Slide
- Stomp

Shelgon @ Leftovers
Level: 38
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Dragon Claw
- Zen Headbutt
- Protect
- Iron Defense
"""),
    dict(const='DAVE_ROUTE_109', map='Route109', x=27, y=15, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=4,
         label='Dave',
         intro=r"DAVE: Beach football! Sand in the\nshoes, salt in the wounds!\p"
               r"Na na na na na-na-na…\pThat's not a chant.\nThat's a warning.$",
         defeat=r"Offside! Clearly offside!\nThe referee is a Wingull!$",
         post=r"DAVE: My knees are made of sand now.\nSee you on the big pitch.$",
         party="""Name: Dave
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Blue

Gastly
Level: 19
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Hex
- Confuse Ray
- Lick
- Mean Look

Charcadet
Level: 19
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Flame Charge
- Clear Smog
- Astonish
- Leer

Gible
Level: 19
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Dragon Breath
- Sand Tomb
- Bulldoze
- Sand Attack

Pawniard @ Oran Berry
Level: 20
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Metal Claw
- Fury Cutter
- Assurance
- Scary Face
"""),
    dict(const='DAVE_ROUTE_118', map='Route118', x=76, y=11, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=4,
         label='Dave',
         intro=r"DAVE: Away game! Nobody chants my\nname here. So I'll do it myself.\p"
               r"DAVE IS ON FIRE!\p…Ow. Literally.\nCeruledge, stop that.$",
         defeat=r"Red card. For me. And for my\nwhole personality.$",
         post=r"DAVE: Next stop: VICTORY ROAD.\nThe big league. My mum is coming.$",
         party="""Name: Dave
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Items: Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Blue

Haunter
Level: 33
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Shadow Ball
- Sludge Bomb
- Hypnosis
- Dream Eater

Ceruledge
Level: 33
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Bitter Blade
- Shadow Claw
- Night Slash
- Swords Dance

Gliscor
Level: 33
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Earthquake
- Acrobatics
- Knock Off
- Toxic

Gabite
Level: 33
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Dragon Claw
- Dig
- Slash
- Sandstorm

Bisharp @ Sitrus Berry
Level: 34
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Iron Head
- Night Slash
- Swords Dance
- Sucker Punch
"""),
    dict(const='MITCH_ROUTE_110', map='Route110', x=20, y=54, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=5,
         label='Mitch',
         intro=r"MITCH: Oh no. A person.\pI'm practising for a DJ set under\nthe CYCLING ROAD. People will come.\p"
               r"Please don't look at me while we\nbattle. Look at my drops.$",
         defeat=r"The bass dropped. So did I.$",
         post=r"MITCH: 174 beats per minute.\nThat's my heart rate right now.\lCoincidence.$",
         party="""Name: Mitch
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Yellow

Trapinch
Level: 23
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Bulldoze
- Bite
- Rock Slide
- Sand Tomb

Metang
Level: 23
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Metal Claw
- Confusion
- Pursuit
- Magnet Rise

Makuhita
Level: 23
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Fake Out
- Force Palm
- Knock Off
- Bulk Up

Marshtomp @ Mystic Water
Level: 24
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Mud Shot
- Water Pulse
- Rock Smash
- Protect
"""),
    dict(const='MITCH_ROUTE_121', map='Route121', x=50, y=13, gfx='OBJ_EVENT_GFX_MAN_3', face='RIGHT', sight=4,
         label='Mitch',
         intro=r"MITCH: You again. Okay. Breathe.\pLast week I played for 12 people.\n"
               r"Eleven were Zigzagoon.\pThe twelfth asked for a refund.\n"
               r"Let's battle before I overthink it.$",
         defeat=r"Drop. Silence. Story of my life.$",
         post=r"MITCH: Next gig: VICTORY ROAD.\nTerrible acoustics. Perfect.\p"
              r"Nobody will hear me fail.$",
         party="""Name: Mitch
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Items: Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Yellow

Flygon
Level: 39
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
Ability: Tinted Lens
- Earthquake
- Dragon Claw
- U-Turn
- First Impression

Metang
Level: 39
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Meteor Mash
- Zen Headbutt
- Bullet Punch
- Agility

Hariyama
Level: 39
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Fake Out
- Close Combat
- Knock Off
- Heavy Slam

Dusclops @ Eviolite
Level: 39
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Shadow Sneak
- Will-O-Wisp
- Confuse Ray
- Pain Split

Swampert @ Sitrus Berry
Level: 40
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Waterfall
- Earthquake
- Rock Slide
- Flip Turn
"""),
    dict(const='SICKBLIK_ROUTE_104', map='Route104', x=14, y=26, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=4,
         label='SickBlik',
         intro=r"Oh! A player! In my romhack!\pHi, I'm SICKBLIK. I made this.\p"
               r"Hold still. I need to check if\nthe battles actually work.$",
         defeat=r"Battles work! Losing also works!\nGreat news for everyone but me.$",
         post=r"SICKBLIK: A bug? That's a feature.\nA feature? Probably also a bug.$",
         party="""Name: SickBlik
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint
Mugshot: Yellow

Dreepy
Level: 12
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Astonish
- Quick Attack
- Infestation
- Bite

Ferroseed
Level: 12
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Metal Claw
- Pin Missile
- Harden
- Tackle

Voltorb
Level: 12
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Charge Beam
- Spark
- Eerie Impulse
- Self-Destruct

Remoraid @ Oran Berry
Level: 13
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Water Gun
- Water Pulse
- Lock-On
- Psybeam
"""),
    dict(const='SICKBLIK_ROUTE_113', map='Route113', x=70, y=13, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=5,
         label='SickBlik',
         intro=r"SICKBLIK: Still playing? Respect.\pI put ash on this route so the\nsprites look moody. Cinematic.\p"
               r"I also balanced my own team.\nTotally fair. Trust me.$",
         defeat=r"Noted. Nerfing you next patch.$",
         post=r"SICKBLIK: See you near the end.\pI'll be the guy with a hotpot\nand a problem.$",
         party="""Name: SickBlik
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Items: Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Yellow

Dreepy
Level: 26
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- U-Turn
- Hex
- Will-O-Wisp
- Quick Attack

Ferroseed
Level: 26
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- Leech Seed
- Metal Claw
- Seed Bomb
- Curse

Voltorb
Level: 26
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- Volt Switch
- Charge Beam
- Light Screen
- Explosion

Larvesta
Level: 26
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- Flame Charge
- Bug Bite
- Struggle Bug
- Will-O-Wisp

Octillery @ Expert Belt
Level: 27
Ability: Protean
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- Octazooka
- Psybeam
- Aurora Beam
- Signal Beam
"""),
    dict(const='SHY_GUY_DESERT', map='Route111', x=None, y=None, gfx='OBJ_EVENT_GFX_SHY_GUY_RED', face='BURIED', sight=1,
         label='ShyGuy',
         intro=r"…………\p(A SHY GUY was hiding in the sand.\nHe is mortified that you found him.)$",
         defeat=r"…!\p(He wants to be buried again.\nPreferably forever.)$",
         post=r"…\p(He is pretending to be a cactus.\nIt is not going well.)$",
         party="""Name: SHY GUY
Class: Guest Star
Pic: Guest Shy Guy Red
Gender: Male
Music: Suspicious
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability

Sandygast
Level: 28
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Shore Up
- Shadow Ball
- Bulldoze
- Sand Tomb

Yamask
Level: 28
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Hex
- Will-O-Wisp
- Disable
- Protect

Hawlucha
Level: 28
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Flying Press
- Aerial Ace
- Detect
- Hone Claws

Mr. Mime @ Light Clay
Level: 29
Ability: Filter
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Reflect
- Light Screen
- Psybeam
- Encore
"""),
]

# Shy Guy-plek: woestijn van Route 111 (buried = springt uit het zand)
SHY_GUY_SPOT = (37, 69)  # achter het rotsblok aan de oostrand

PREFIX = {}


def map_prefix(m):
    s = open('data/maps/%s/scripts.inc' % m).read()
    return re.search(r'^(\w+)_MapScripts::', s, re.M).group(1)


def tile_elevation(mapname, x, y):
    mj = json.load(open('data/maps/%s/map.json' % mapname))
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == mj['layout']][0]
    b = open(L['blockdata_filepath'], 'rb').read()
    v = struct.unpack_from('<H', b, (y * L['width'] + x) * 2)[0]
    assert (v >> 10) & 3 == 0, (mapname, x, y, 'botsing op deze tegel')
    return v >> 12


def replace_block(text, start, end, new):
    if start in text:
        i = text.index(start)
        j = text.index(end, i) + len(end)
        return text[:i] + new + text[j:]
    return text.rstrip('\n') + '\n\n' + new + '\n'


def main():
    for i, f in enumerate(FIGHTS):
        f['id'] = FIRST_ID + i
        if f['x'] is None:
            f['x'], f['y'] = SHY_GUY_SPOT
        f['local'] = 'LOCALID_EF_' + f['const']
        f['pfx'] = map_prefix(f['map'])

    # opponents.h
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// extra_fights { (tools/grounded/maptools/extra_fights.py)\n'
    for f in FIGHTS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: extra gevecht (%s)\n' % (f['const'], f['id'], f['map'])
    blk += '// }'
    if '// extra_fights {' in s:
        i = s.index('// extra_fights {')
        j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    ids = [int(x) for x in re.findall(r'^#define TRAINER_\w+\s+(\d+)', s, re.M)
           if True]
    top = max(int(m.group(2)) for m in re.finditer(r'^#define (TRAINER_\w+)\s+(\d+)', s, re.M)
              if m.group(1) not in ('TRAINERS_COUNT', 'MAX_TRAINERS_COUNT'))
    s = re.sub(r'^#define TRAINERS_COUNT\s+\d+', '#define TRAINERS_COUNT                      %d' % (top + 1), s, flags=re.M)
    open(p, 'w').write(s)

    # trainers.party (achteraan; het laatste blok heeft geen === erna)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- extra_fights (tools/grounded/maptools/extra_fights.py) --- */\n\n'
    for f in FIGHTS:
        blk += '=== TRAINER_%s ===\n%s\n' % (f['const'], f['party'].rstrip('\n') + '\n')
    blk += '/* --- einde extra_fights --- */'
    s = replace_block(s, '/* --- extra_fights', '/* --- einde extra_fights --- */', blk)
    open(p, 'w').write(s)

    # kaarten
    bymap = {}
    for f in FIGHTS:
        bymap.setdefault(f['map'], []).append(f)
    for m, fs in bymap.items():
        p = 'data/maps/%s/map.json' % m
        mj = json.load(open(p))
        objs = [o for o in mj['object_events'] if not str(o.get('local_id', '')).startswith('LOCALID_EF_')]
        for f in fs:
            buried = f['face'] == 'BURIED'
            objs.append({
                'local_id': f['local'],
                'graphics_id': f['gfx'],
                'x': f['x'], 'y': f['y'],
                'elevation': tile_elevation(m, f['x'], f['y']),
                'movement_type': 'MOVEMENT_TYPE_BURIED' if buried else 'MOVEMENT_TYPE_FACE_' + f['face'],
                'movement_range_x': 0, 'movement_range_y': 0,
                'trainer_type': 'TRAINER_TYPE_BURIED' if buried else 'TRAINER_TYPE_NORMAL',
                'trainer_sight_or_berry_tree_id': str(f['sight']),
                'script': '%s_EventScript_EF_%s' % (f['pfx'], f['const'].title().replace('_', '')),
                # Wally verdwijnt na zijn nederlaag: de verslagen-flag van de trainer verbergt het object
                'flag': ('TRAINER_FLAGS_START+TRAINER_%s' % f['const']) if f.get('hide') else '0',
            })
        mj['object_events'] = objs
        open(p, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')

        p = 'data/maps/%s/scripts.inc' % m
        s = open(p).read()
        blk = '@ extra_fights { (tools/grounded/maptools/extra_fights.py)\n'
        for f in fs:
            name = f['const'].title().replace('_', '')
            es = '%s_EventScript_EF_%s' % (f['pfx'], name)
            tx = '%s_Text_EF_%s' % (f['pfx'], name)
            if f.get('hide'):
                blk += f'''{es}::
	trainerbattle_single TRAINER_{f['const']}, {tx}Intro, {tx}Defeat, {es}Defeated
	msgbox {tx}PostBattle, MSGBOX_AUTOCLOSE
	end

{es}Defeated::
	msgbox {tx}PostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject {f['local']}
	fadescreen FADE_FROM_BLACK
	release
	end

'''
            else:
                blk += f'''{es}::
	trainerbattle_single TRAINER_{f['const']}, {tx}Intro, {tx}Defeat
	msgbox {tx}PostBattle, MSGBOX_AUTOCLOSE
	end

'''
            for k, key in (('Intro', 'intro'), ('Defeat', 'defeat'), ('PostBattle', 'post')):
                blk += '%s%s:\n' % (tx, k)
                parts = re.split(r'(?<=\\[npl])', f[key])
                for part in parts:
                    if part:
                        blk += '\t.string "%s"\n' % part
                blk += '\n'
        blk += '@ }'
        s = replace_block(s, '@ extra_fights {', '@ }', blk)
        open(p, 'w').write(s)
        check_widths(blk)
    print('extra_fights: %d gevechten, id %d-%d' % (len(FIGHTS), FIGHTS[0]['id'], FIGHTS[-1]['id']))


def check_widths(blk):
    for line in re.findall(r'\.string "(.*)"', blk):
        t = re.sub(r'\\[npl]|\$', '', line).replace('{PLAYER}', 'PLAYERX')  # max. 7 tekens
        if len(t) > 36:
            print('  LET OP, lange regel (%d): %s' % (len(t), t))


if __name__ == '__main__':
    main()
