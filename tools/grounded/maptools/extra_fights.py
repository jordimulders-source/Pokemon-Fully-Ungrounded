#!/usr/bin/env python3
"""Project Grounded: extra gevechten in de wereld (Wally in Mt. Pyre en Mossdeep; Zinnia, Mitch en SickBlik
eerder in de game; Dave op Route 111, in Petalburg en in Sootopolis; een verstopte Shy Guy in de woestijn van Route 111).

Optionele sleutels per gevecht: hide (verdwijnt na zijn nederlaag), flag (eigen objectflag), trainer_type,
script (eigen eventscript met @ES@/@TX@/@LOCAL@/@TRAINER@). Kaarten zonder gevecht worden opgeruimd.

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

# Dave: verliesquote in al zijn gevechten (Jordi)
DAVE_DEFEAT = r"{PLAYER}, more....$"
# Dave 1: Route 111 zuid (x, y, kijkrichting, zicht), vóór de woestijn
DAVE1_SPOT = (26, 117, 'LEFT', 5)  # naast het pad omhoog vanaf Mauville

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
         # Wally's vaste team (eindteam Victory Road, terug geredeneerd); spook-accent: Flutter Mane komt erbij,
         # Annihilape (Rage Fist), Gallade met Night Slash
         party="""Name: WALLY
Class: Rival
Pic: Wally
Gender: Male
Music: Male
Items: Super Potion / Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Purple

Darmanitan @ Charcoal
Level: 42
Ability: Sheer Force
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Flare Blitz
- Rock Slide
- Earthquake
- U-Turn

Dondozo @ Leftovers
Level: 42
Ability: Unaware
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Waterfall
- Curse
- Rest
- Sleep Talk

Arctibax
Level: 42
Ability: Thermal Exchange
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Icicle Crash
- Dragon Claw
- Ice Shard
- Dragon Dance

Annihilape @ Chesto Berry
Level: 42
Ability: Defiant
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Rage Fist
- Drain Punch
- Bulk Up
- Rest

Flutter Mane
Level: 42
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Shadow Ball
- Dazzling Gleam
- Mystical Fire
- Confuse Ray

Gallade @ Sitrus Berry
Level: 44
Ability: Sharpness
IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe
- Psycho Cut
- Sacred Sword
- Leaf Blade
- Night Slash
"""),
    dict(const='WALLY_MOSSDEEP', map='MossdeepCity', x=68, y=17, gfx='OBJ_EVENT_GFX_WALLY', face='LEFT', sight=4,
         label='WallySpace', hide=True,
         intro=r"WALLY: {PLAYER}! Look, rocket house!\p"
               r"Gallader psychic feel good in\nspacing placing.\p"
               r"Brain big now. Battle with brain!$",
         defeat=r"Brain… small again…$",
         post=r"WALLY: In space no air.\nGallader no need air.\p"
              r"Gallader need hug. I go hug.\nBye-bye, {PLAYER}!$",
         # zelfde team, psychic-accent: Darmanitan met Zen Mode, Zen Headbutt, Psyshock
         party="""Name: WALLY
Class: Rival
Pic: Wally
Gender: Male
Music: Male
Items: Hyper Potion / Hyper Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Purple

Darmanitan @ Charcoal
Level: 47
Ability: Zen Mode
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Flare Blitz
- Zen Headbutt
- Rock Slide
- U-Turn

Dondozo @ Leftovers
Level: 47
Ability: Unaware
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Waterfall
- Curse
- Rest
- Sleep Talk

Arctibax
Level: 47
Ability: Thermal Exchange
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Icicle Crash
- Dragon Claw
- Zen Headbutt
- Dragon Dance

Annihilape @ Chesto Berry
Level: 47
Ability: Defiant
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Rage Fist
- Drain Punch
- Bulk Up
- Rest

Flutter Mane
Level: 47
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Shadow Ball
- Moonblast
- Psyshock
- Mystical Fire

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
    # Dave (Freed From Desire, GOAL!-transitie): 1 Route 111 (voor Wattson), 2 Petalburg (na Flannery, voor de gymdeur),
    # 3 Sootopolis (direct na Rayquaza), 4 = het oorspronkelijke gevecht in Victory Road (TRAINER_DAVE, lv 51),
    # daarna praat hij alleen nog op een ligstoel in het Paradiso Resort. Teksten letterlijk van Jordi.
    dict(const='DAVE_ROUTE_111', map='Route111', x=DAVE1_SPOT[0], y=DAVE1_SPOT[1], gfx='OBJ_EVENT_GFX_MAN_3',
         face=DAVE1_SPOT[2], sight=DAVE1_SPOT[3], label='Dave', hide=True,
         intro=r"DAVE: Hey, kleine speler.\p"
               r"Have you heard about the\nDublin Rules?\p"
               r"Cheating is a subjective thing.\p"
               r"If this girl is related to you,\nlike it's your mom or sister,\lit's cheating,\p"
               r"otherwise it could've been\nnon-consensual or accidental.\p"
               r"Nobody knows!\p"
               r"Well, let's fight!\nToo much info!$",
         defeat=DAVE_DEFEAT,
         post=r"DAVE: Dublin Rule number two:\nnever explain the Dublin Rules.\p"
              r"I've now broken both.\nGreat session. Bye!$",
         party="""Name: Dave
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
Mugshot: Blue

Gastly
Level: 22
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Hex
- Night Shade
- Confuse Ray
- Hypnosis

Charcadet
Level: 22
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Flame Charge
- Astonish
- Clear Smog
- Will-O-Wisp

Gible
Level: 22
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Dragon Breath
- Bulldoze
- Take Down
- Sand Tomb

Pawniard @ Oran Berry
Level: 23
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Metal Claw
- Assurance
- Fury Cutter
- Scary Face
"""),
    dict(const='DAVE_PETALBURG', map='PetalburgCity', x=15, y=9, gfx='OBJ_EVENT_GFX_MAN_3', face='DOWN', sight=1,
         label='Dave', flag='FLAG_TEMP_9',  # PetalburgCity_OnTransition: alleen na badge 4 en zolang niet verslagen
         intro=r"DAVE: I don't have time to watch\nNetflix all the time,\lI have two children.\p"
               r"Anyways, have you seen my picture,\nwhen I was a part of the first\lteam at BLC?\p"
               r"I'll show you after you beat me!$",
         defeat=DAVE_DEFEAT,
         post=r"DAVE: Fine. A deal is a deal.\p"
              r"(A faded team photo. Eleven men,\none trophy, zero necks.)\p"
              r"(Dave is circled in red marker.\nBy Dave. Several times.)\p"
              r"DAVE: Third from the left.\nThe blur. That's pace, {PLAYER}.\p"
              r"Right. Gotta get the kids.\nYour dad's GYM counts as daycare.$",
         # na de winst loopt hij de gym in en is hij weg (de deur is weer vrij)
         script="""@ES@::
	trainerbattle_single TRAINER_@TRAINER@, @TX@Intro, @TX@Defeat, @ES@Defeated
	msgbox @TX@PostBattle, MSGBOX_AUTOCLOSE
	end

@ES@Defeated::
	msgbox @TX@PostBattle, MSGBOX_DEFAULT
	closemessage
	opendoor 15, 8
	waitdooranim
	applymovement @LOCAL@, Common_Movement_WalkUp
	waitmovement 0
	removeobject @LOCAL@
	closedoor 15, 8
	waitdooranim
	release
	end

""",
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
Level: 31
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Shadow Ball
- Sludge Bomb
- Hypnosis
- Hex

Ceruledge
Level: 31
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Bitter Blade
- Shadow Claw
- Night Slash
- Swords Dance

Gliscor
Level: 31
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Dig
- Acrobatics
- Knock Off
- Toxic

Gabite
Level: 31
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Dragon Claw
- Bulldoze
- Slash
- Sandstorm

Pawniard @ Sitrus Berry
Level: 32
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
    dict(const='DAVE_SOOTOPOLIS', map='SootopolisCity', x=32, y=35, gfx='OBJ_EVENT_GFX_MAN_3', face='LEFT', sight=0,
         label='Dave', flag='FLAG_TEMP_9', trainer_type='TRAINER_TYPE_NONE',
         # gestart vanuit SootopolisCity_EventScript_KecclesScene (direct na de Rayquaza-scène), niet door aanspreken
         intro=r"DAVE: Just scored a hattrick,\nleftie, rightie and a header.\p"
               r"Doesn't get more pure than that!\nAll top bins as well.\p"
               r"Winkelhaak BV$",
         defeat=DAVE_DEFEAT,
         post=r"DAVE: A sky dragon? Mate, I've been\ncalled worse after a derby.\p"
              r"Carry on. I'm off to the\nVICTORY ROAD. Big match.$",
         script="""@ ingevoegd aan het begin van de scène met Archie, Maxie en Keccles; Dave staat rechts van de speler
@ES@Scene::
	goto_if_defeated TRAINER_@TRAINER@, @ES@SceneEnd
	clearflag FLAG_TEMP_9
	addobject @LOCAL@
	turnobject @LOCAL@, DIR_WEST
	turnobject LOCALID_PLAYER, DIR_EAST
	playse SE_PIN
	applymovement @LOCAL@, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox @TX@Intro, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_@TRAINER@, @TX@Defeat
	msgbox @TX@PostBattle, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject @LOCAL@
	fadescreenswapbuffers FADE_FROM_BLACK
@ES@SceneEnd::
	return

@ES@::
	msgbox @TX@PostBattle, MSGBOX_NPC
	end

""",
         party="""Name: Dave
Class: Cooltrainer
Pic: Cooltrainer M
Gender: Male
Music: Cool
Items: Hyper Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching
Mugshot: Blue

Gengar
Level: 48
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Shadow Ball
- Sludge Bomb
- Focus Blast
- Hypnosis

Ceruledge @ Life Orb
Level: 48
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Bitter Blade
- Poltergeist
- Psycho Cut
- Swords Dance

Gliscor @ Toxic Orb
Level: 48
Ability: Poison Heal
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Earthquake
- Acrobatics
- Knock Off
- Swords Dance

Garchomp
Level: 48
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Earthquake
- Dragon Claw
- Stone Edge
- Swords Dance

Kingambit @ Sitrus Berry
Level: 49
Ability: Supreme Overlord
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Kowtow Cleave
- Iron Head
- Sucker Punch
- Swords Dance
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
                'trainer_type': 'TRAINER_TYPE_BURIED' if buried else f.get('trainer_type', 'TRAINER_TYPE_NORMAL'),
                'trainer_sight_or_berry_tree_id': str(f['sight']),
                'script': '%s_EventScript_EF_%s' % (f['pfx'], f['const'].title().replace('_', '')),
                # Wally verdwijnt na zijn nederlaag: de verslagen-flag van de trainer verbergt het object
                'flag': f.get('flag') or (('TRAINER_FLAGS_START+TRAINER_%s' % f['const']) if f.get('hide') else '0'),
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
            if f.get('script'):
                blk += (f['script'].replace('@ES@', es).replace('@TX@', tx).replace('@LOCAL@', f['local'])
                        .replace('@TRAINER@', f['const']))
            elif f.get('hide'):
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
    # kaarten waar geen extra gevecht meer staat (bijv. Dave op Route 109/118): objecten en scriptblok weghalen
    for m in sorted(os.listdir('data/maps')):
        p = 'data/maps/%s/map.json' % m
        if m in bymap or not os.path.exists(p) or 'LOCALID_EF_' not in open(p).read():
            continue
        mj = json.load(open(p))
        mj['object_events'] = [o for o in mj['object_events']
                               if not str(o.get('local_id', '')).startswith('LOCALID_EF_')]
        open(p, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
        p = 'data/maps/%s/scripts.inc' % m
        s = open(p).read()
        if '@ extra_fights {' in s:
            i = s.index('@ extra_fights {')
            j = s.index('@ }', i) + 3
            s = (s[:i].rstrip('\n') + '\n' + s[j:].lstrip('\n')).rstrip('\n') + '\n'
            open(p, 'w').write(s)
        print('  opgeruimd:', m)
    print('extra_fights: %d gevechten, id %d-%d' % (len(FIGHTS), FIGHTS[0]['id'], FIGHTS[-1]['id']))


def check_widths(blk):
    for line in re.findall(r'\.string "(.*)"', blk):
        t = re.sub(r'\\[npl]|\$', '', line).replace('{PLAYER}', 'PLAYERX')  # max. 7 tekens
        if len(t) > 36:
            print('  LET OP, lange regel (%d): %s' % (len(t), t))


if __name__ == '__main__':
    main()
