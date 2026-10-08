"""Project Grounded: landvulling (KAART_REVIEW (b)/(c), lege landplekken).

Alleen objecten, verborgen items en scripts; het terrein blijft zoals het is.
- Ever Grande City: Victory-promenade boven (hotdogkraam, fotograaf, fans, drie straattrainers) + inwoners beneden.
- Mt. Pyre Exterior: rouwenden die op een absurde manier rouwen, een Duskull, 4 verborgen items.
- Desert Underpass: fossielenopgraving bij het oude fossiel (archeoloog met cadeau, levende "Armaldo-fossiel",
  Ruin Maniac Hollis met een fossielenteam), Stone Plate + verborgen item.
- Navel Rock Fork: verdwaalde wandelaar, Sky Plate + verborgen item op de doodlopende gangen.
- Southern / Birth / Faraway Island: verlaten kamp van een bezoeker (kist met brieven) + 2 items.
- Safari (Fairy Forest, Thunder Plains, Haunted Camp), Starfall Grotto, Heatran-hol: per plek één NPC + items
  (Starfall: elke dag nieuw sterrenstof via dagelijkse flags).

Idempotent: eigen objecten/bg-events (herkend aan script-/flagnamen) en het gemarkeerde blok in scripts.inc
worden eerst weggehaald. Controleert per kaart dat alles bereikbaar blijft (lopen + hoogte, objecten = muur),
dat objecten niet op warps/coord-events/water staan en dat tekstregels in het tekstvak passen.
Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/land_vulling.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landlib import Kaart, obj, hidden, ball, text, talk, trainer_single, check_text, apply_events, NOPLACE

MARK = 'land_vulling'
FAIL = []
TEXTS = []


def T(label, s):
    TEXTS.append((label, s))
    return text(label, s)


def npc(label, tlabel, s):
    return talk(label, '\tmsgbox %s, MSGBOX_NPC\n\tend' % tlabel) + T(tlabel, s)


def sign_obj(label, tlabel, s):
    return talk(label, '\tmsgbox %s, MSGBOX_SIGN\n\tend' % tlabel) + T(tlabel, s)


def npc_post(label, tlabel, pre, post):
    """Andere tekst na de Hall of Fame (FLAG_SYS_GAME_CLEAR)."""
    return talk(label, '''
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, %s_Post
	msgbox %s, MSGBOX_DEFAULT
	release
	end
%s_Post:
	msgbox %s_Post, MSGBOX_DEFAULT
	release
	end''' % (label, tlabel, label, tlabel)) + T(tlabel, pre) + T(tlabel + '_Post', post)


def gift(label, tlabel, flag, item, s, after):
    return talk(label, '''
	lock
	faceplayer
	goto_if_set %s, %s_After
	msgbox %s, MSGBOX_DEFAULT
	giveitem %s
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag %s
	release
	end
%s_After:
	msgbox %s_After, MSGBOX_DEFAULT
	release
	end''' % (flag, label, tlabel, item, flag, label, tlabel)) + T(tlabel, s) + T(tlabel + '_After', after)


def trainer(label, trainer_id, intro, defeat, post):
    t = label.replace('EventScript', 'Text')
    for suf, s in (('_Intro', intro), ('_Defeat', defeat), ('_Post', post)):
        TEXTS.append((t + suf, s))
    return trainer_single(label, trainer_id, intro, defeat, post)


def place(k, objs, bgs, scr, start, targets, surf=False):
    """Controles + wegschrijven. targets = tegels die bereikbaar moeten blijven (warps, ingangen, ...)."""
    ev = k.event_tiles()
    solid = set()
    for o in objs:
        p = (o['x'], o['y'])
        assert not k.blocked(*p), '%s: object op een muur %s (%s)' % (k.name, p, o['script'])
        assert p not in ev, '%s: object op een warp/coord-event %s' % (k.name, p)
        assert k.beh(*p) not in NOPLACE, '%s: object in het water %s' % (k.name, p)
        o['elevation'] = k.elev(*p)
        solid.add(p)
    for b in bgs:
        p = (b['x'], b['y'])
        assert p not in solid and p not in ev and not k.blocked(*p), '%s: bg-event %s' % (k.name, p)
        assert k.beh(*p) not in NOPLACE, '%s: item in het water %s' % (k.name, p)
        b['elevation'] = k.elev(*p)
    old = {(o['x'], o['y']) for o in k.d['object_events']
           if o['script'] not in {x['script'] for x in objs} and 'ITEM_BALL' not in o['graphics_id']}
    for p in solid:
        assert p not in {(o['x'], o['y']) for o in k.d['object_events']
                         if o['script'] not in {x['script'] for x in objs} and o['flag'] not in {x['flag'] for x in objs}}, \
            '%s: botst met een bestaand object %s' % (k.name, p)
    for b in bgs:
        assert (b['x'], b['y']) not in {(x['x'], x['y']) for x in k.d['bg_events'] if x.get('flag') != b.get('flag')
                                        and x.get('script') != b.get('script')}, '%s: botst met bg-event' % k.name
    r = {}
    for st in (start if isinstance(start, list) else [start]):
        r.update(k.walk(st, solid=solid | old, surf=surf))
    need = list(targets)
    # elk object moet aanspreekbaar zijn (een buurtegel bereikbaar), elk bg-item betreedbaar of aanspreekbaar
    for o in objs:
        x, y = o['x'], o['y']
        if not any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            print('%s: object (%d,%d) %s niet aanspreekbaar' % (k.name, x, y, o['script'])); FAIL.append(k.name)
    for b in bgs:
        need.append((b['x'], b['y']))
    miss = [t for t in need if t not in r]
    if miss:
        print('%s: niet bereikbaar: %s' % (k.name, miss)); FAIL.append(k.name)
    apply_events(k, objs, bgs, scr, MARK)
    print('%s: %d objecten, %d bg-events' % (k.name, len(objs), len(bgs)))


# =====================================================================================================
# Ever Grande City (40x80). Boven (na Victory Road): promenade langs het pad naar de League. Beneden: inwoners.
k = Kaart('EverGrandeCity')
P = 'EverGrandeCity_EventScript_LV'
Q = 'EverGrandeCity_Text_LV'
objs = [
    obj('OBJ_EVENT_GFX_COOK', 22, 18, P + 'HotDog', move='MOVEMENT_TYPE_FACE_UP'),
    obj('OBJ_EVENT_GFX_MOVING_BOX', 21, 18, P + 'HotDogCart'),
    obj('OBJ_EVENT_GFX_CAMERAMAN', 16, 16, P + 'Photographer', move='MOVEMENT_TYPE_FACE_RIGHT'),
    obj('OBJ_EVENT_GFX_POKEFAN_M', 25, 15, P + 'FanM', move='MOVEMENT_TYPE_FACE_DOWN'),
    obj('OBJ_EVENT_GFX_GIRL_3', 26, 15, P + 'FanGirl', move='MOVEMENT_TYPE_FACE_DOWN'),
    obj('OBJ_EVENT_GFX_EXPERT_M', 29, 17, P + 'Bramwell', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=2),
    obj('OBJ_EVENT_GFX_POKEFAN_F', 20, 10, P + 'Gloria', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=1),
    # beneden (voor Victory Road)
    obj('OBJ_EVENT_GFX_MAN_5', 28, 51, P + 'Rocky', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=2),
    obj('OBJ_EVENT_GFX_OLD_WOMAN', 13, 50, P + 'OldWoman', move='MOVEMENT_TYPE_FACE_RIGHT'),
    obj('OBJ_EVENT_GFX_FISHERMAN', 21, 55, P + 'Fisherman', move='MOVEMENT_TYPE_FACE_DOWN'),
]
bgs = [hidden(15, 18, 'ITEM_FULL_RESTORE', 'FLAG_HIDDEN_ITEM_EVER_GRANDE_FULL_RESTORE')]
scr = talk(P + 'HotDog', '''
	lock
	faceplayer
	goto_if_set FLAG_DAILY_EVER_GRANDE_HOTDOG, %sHotDog_SoldOut
	msgbox %sHotDog, MSGBOX_DEFAULT
	giveitem ITEM_BIG_MALASADA
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_DAILY_EVER_GRANDE_HOTDOG
	msgbox %sHotDog_Given, MSGBOX_DEFAULT
	release
	end
%sHotDog_SoldOut:
	msgbox %sHotDog_SoldOut, MSGBOX_DEFAULT
	release
	end''' % (P, Q, Q, P, Q))
scr += T(Q + 'HotDog', "VICTORY DOGS! Get your VICTORY DOGS\\p"
         "First one's free. For courage.\\n"
         "Most challengers only need one.\\p"
         "We ran out of sausages in 2003.\\n"
         "It's a MALASADA now. Same spirit.")
scr += T(Q + 'HotDog_Given', "Eat it before the ELITE FOUR.\\n"
         "Nobody wants to lose on an empty\\l"
         "stomach. Full stomach is fine.")
scr += T(Q + 'HotDog_SoldOut', "One VICTORY DOG per person per day.\\p"
         "League rules. The ELITE FOUR\\n"
         "complained about sticky hands.")
scr += sign_obj(P + 'HotDogCart', Q + 'HotDogCart',
                "A cart. The menu says:\\n"
                "'VICTORY DOG - free'\\l"
                "'DEFEAT DOG - also free, but sad'")
scr += talk(P + 'Photographer', '''
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, %sPhotographer_Post
	msgbox %sPhotographer, MSGBOX_DEFAULT
	fadescreen FADE_TO_WHITE
	fadescreen FADE_FROM_WHITE
	msgbox %sPhotographer_Done, MSGBOX_DEFAULT
	release
	end
%sPhotographer_Post:
	msgbox %sPhotographer_Post, MSGBOX_DEFAULT
	release
	end''' % (P, Q, Q, P, Q))
scr += T(Q + 'Photographer', "Hold it! I take a picture of every\\n"
         "challenger before they go in.\\p"
         "The 'before' picture.\\n"
         "Say 'ELITE'!")
scr += T(Q + 'Photographer_Done', "Lovely. I'll take the 'after'\\n"
         "picture when you come out.\\p"
         "Those are usually sadder.\\n"
         "Better lighting, though.")
scr += T(Q + 'Photographer_Post', "The new CHAMPION! Your 'before'\\n"
         "picture is on the wall now.\\p"
         "Next to 'challenger, crying'\\n"
         "and 'challenger, crying, wet'.")
scr += npc_post(P + 'FanM', Q + 'FanM',
                "I come here every day to cheer for\\n"
                "whoever walks past.\\p"
                "GO, STRANGER! YOU CAN DO IT!\\n"
                "...Probably! Statistically, no!",
                "IT'S THE CHAMPION! I cheered for\\n"
                "you! I cheer for everyone, but\\l"
                "today it worked!")
scr += npc_post(P + 'FanGirl', Q + 'FanGirl',
                "I made a sign for the CHAMPION.\\p"
                "It says 'MARRY ME, STEVEN'.\\n"
                "I'm nine. It's a long-term plan.",
                "Oh, YOU'RE the CHAMPION now?\\p"
                "...Hold on, I need a new sign.\\n"
                "Do you spell {PLAYER} with a 'Q'?")
scr += trainer(P + 'Bramwell', 'TRAINER_EVER_GRANDE_BRAMWELL',
               "Forty-seven times I've challenged\\n"
               "the ELITE FOUR. Forty-seven!\\p"
               "This is my warm-up. You are\\n"
               "my warm-up. Nothing personal.",
               "Forty-eight.\\n"
               "That one counts. Somehow it counts.",
               "SIDNEY knows my name. Not because\\n"
               "I'm good. Because I'm always there.")
scr += trainer(P + 'Gloria', 'TRAINER_EVER_GRANDE_GLORIA',
               "Wait! Are you famous? You walk like\\n"
               "someone who could be famous.\\p"
               "Battle me, and if you win, I'll put\\n"
               "you in my scrapbook!",
               "Into the scrapbook you go!\\n"
               "Page 412. Between two strangers.",
               "My scrapbook is mostly people who\\n"
               "lost in there. Very thick book.\\l"
               "Very sad book.")
scr += trainer(P + 'Rocky', 'TRAINER_EVER_GRANDE_ROCKY',
               "I'm busking for the League entry\\n"
               "fee. One song, one battle.\\p"
               "The song is about how expensive\\n"
               "the League entry fee is.",
               "Sold out! Of everything!\\n"
               "Mostly hope.",
               "Fun fact: there IS no entry fee.\\n"
               "I just never asked.")
scr += npc_post(P + 'OldWoman', Q + 'OldWoman',
                "Sixty years I've lived at the foot\\n"
                "of the POKeMON LEAGUE.\\p"
                "Never been inside. Have you seen\\n"
                "the stairs? Have you seen my knees?",
                "A new CHAMPION, they say.\\p"
                "Lovely. Could you install a lift?\\n"
                "That's what a CHAMPION is for.")
scr += npc(P + 'Fisherman', Q + 'Fisherman',
           "Best fishing spot in HOENN, right\\n"
           "under the waterfall.\\p"
           "Every trainer who loses in there\\n"
           "throws a POKe BALL off the cliff.\\l"
           "I catch about four a day.")
# boven (vanaf de uitgang van Victory Road) en beneden (vanaf de ingang van Victory Road) samen
place(k, objs, bgs, scr, [(18, 28), (18, 42)],
      [(18, 6), (18, 27), (17, 15), (25, 26), (22, 17), (24, 16), (27, 49), (19, 55), (12, 44), (27, 50)])

# =====================================================================================================
# Mt. Pyre Exterior (38x51): rouwenden, een Duskull en vier verborgen items
k = Kaart('MtPyre_Exterior')
P = 'MtPyre_Exterior_EventScript_LV'
Q = 'MtPyre_Exterior_Text_LV'
objs = [
    obj('OBJ_EVENT_GFX_OLD_WOMAN', 16, 14, P + 'Rehearsal', move='MOVEMENT_TYPE_FACE_UP'),
    obj('OBJ_EVENT_GFX_MAN_2', 23, 14, P + 'Tamagotchi', move='MOVEMENT_TYPE_FACE_UP'),
    obj('OBJ_EVENT_GFX_HEX_MANIAC', 12, 18, P + 'Streamer', move='MOVEMENT_TYPE_LOOK_AROUND'),
    obj('OBJ_EVENT_GFX_LITTLE_BOY', 10, 26, P + 'Voltorb', move='MOVEMENT_TYPE_FACE_UP'),
    obj('OBJ_EVENT_GFX_SPECIES(DUSKULL)', 30, 36, P + 'Duskull', move='MOVEMENT_TYPE_FACE_LEFT'),
    obj('OBJ_EVENT_GFX_GENTLEMAN', 29, 43, P + 'SeaView', move='MOVEMENT_TYPE_FACE_UP'),
]
bgs = [hidden(28, 14, 'ITEM_PURE_INCENSE', 'FLAG_HIDDEN_ITEM_MT_PYRE_EXT_PURE_INCENSE'),
       hidden(7, 14, 'ITEM_RARE_BONE', 'FLAG_HIDDEN_ITEM_MT_PYRE_EXT_RARE_BONE'),
       hidden(15, 40, 'ITEM_REVIVAL_HERB', 'FLAG_HIDDEN_ITEM_MT_PYRE_EXT_REVIVAL_HERB'),
       hidden(30, 42, 'ITEM_DUSK_BALL', 'FLAG_HIDDEN_ITEM_MT_PYRE_EXT_DUSK_BALL')]
scr = npc(P + 'Rehearsal', Q + 'Rehearsal',
          "Shh. I'm rehearsing.\\p"
          "For my own funeral. I want to get\\n"
          "the lying-still part right.\\p"
          "Day four. My ZIGZAGOON thinks\\n"
          "I've already gone. It ate my lunch.")
scr += npc(P + 'Tamagotchi', Q + 'Tamagotchi',
           "I'm mourning my digital pet.\\p"
           "They said this place is only for\\n"
           "POKeMON. Grief doesn't do genres.\\p"
           "He died of hunger. I fed him\\n"
           "twice. In 1998.")
scr += npc(P + 'Streamer', Q + 'Streamer',
           "Hi chat! We're LIVE from MT. PYRE!\\p"
           "Grandma's DUSCLOPS passed, so this\\n"
           "is a memorial stream. Smash that\\l"
           "like button. He'd have wanted that.\\p"
           "...Three viewers. Two are ghosts.\\n"
           "Best numbers I've ever had.")
scr += npc(P + 'Voltorb', Q + 'Voltorb',
           "My VOLTORB used SELF-DESTRUCT.\\n"
           "For no reason.\\p"
           "Mom says it was the reason.\\p"
           "The grave is empty. There wasn't\\n"
           "much to bury. Just the smell.")
scr += talk(P + 'Duskull', '''
	lock
	faceplayer
	playmoncry SPECIES_DUSKULL, CRY_MODE_NORMAL
	msgbox %sDuskull, MSGBOX_DEFAULT
	waitmoncry
	release
	end''' % Q)
scr += T(Q + 'Duskull', "The DUSKULL is watching you.\\n"
         "Closely. Taking notes, maybe.\\p"
         "It looks at you the way a tailor\\n"
         "looks at a customer.\\l"
         "Measuring.")
scr += npc(P + 'SeaView', Q + 'SeaView',
           "I paid extra for this plot.\\n"
           "'Premium. Sea view,' they said.\\p"
           "The fog has not lifted since I\\n"
           "signed. Not once.\\p"
           "I'm not even dead yet. I just\\n"
           "come here to be disappointed early.")
place(k, objs, bgs, scr, (10, 43), [(19, 11), (20, 11), (9, 9), (27, 16), (18, 40), (24, 21)])

# =====================================================================================================
# Desert Underpass (139x23): fossielenopgraving in de oostkamer, rond het oude fossiel (132,10)
k = Kaart('DesertUnderpass')
P = 'DesertUnderpass_EventScript_LV'
Q = 'DesertUnderpass_Text_LV'
objs = [
    obj('OBJ_EVENT_GFX_SPECIES(ARMALDO)', 135, 8, P + 'Armaldo', move='MOVEMENT_TYPE_FACE_DOWN'),
    obj('OBJ_EVENT_GFX_SCIENTIST_1', 133, 8, P + 'Archaeologist', move='MOVEMENT_TYPE_FACE_RIGHT'),
    obj('OBJ_EVENT_GFX_HIKER', 128, 12, P + 'Hollis', move='MOVEMENT_TYPE_FACE_RIGHT', trainer=True, sight=4),
    obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', 130, 7, 'EventScript_RockSmash', flag='FLAG_TEMP_11'),
    obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', 134, 13, 'EventScript_RockSmash', flag='FLAG_TEMP_12'),
    ball(131, 5, 'ITEM_STONE_PLATE', 'FLAG_ITEM_DESERT_UNDERPASS_STONE_PLATE'),
]
bgs = [hidden(133, 14, 'ITEM_RARE_BONE', 'FLAG_HIDDEN_ITEM_DESERT_UNDERPASS_RARE_BONE')]
scr = talk(P + 'Armaldo', '''
	lock
	msgbox %sArmaldo, MSGBOX_DEFAULT
	playmoncry SPECIES_ARMALDO, CRY_MODE_NORMAL
	waitmoncry
	msgbox %sArmaldo_Cry, MSGBOX_DEFAULT
	release
	end''' % (Q, Q))
scr += T(Q + 'Armaldo', "A sign on a stick: 'ARMALDO.\\n"
         "PERFECTLY PRESERVED. 10,000 YEARS.\\l"
         "DO NOT FEED.'")
scr += T(Q + 'Armaldo_Cry', "...It yawned.\\p"
         "Someone has crossed out\\n"
         "'DO NOT FEED' and written\\l"
         "'FEED. PLEASE. IT'S ANGRY.'")
scr += gift(P + 'Archaeologist', Q + 'Archaeologist', 'FLAG_RECEIVED_DESERT_UNDERPASS_MAX_REVIVE', 'ITEM_MAX_REVIVE',
            "Careful! Active dig site!\\p"
            "We found a complete ARMALDO.\\n"
            "Ten thousand years old! Not a\\l"
            "single bone missing!\\p"
            "It does move a bit. Rigor mortis,\\n"
            "probably. Very slow rigor mortis.\\p"
            "Here. For the fossils you'll find.\\n"
            "It's the only thing that revives\\l"
            "anything down here.",
            "Professor HOLLIS says ARMALDO went\\n"
            "extinct. So this one is in denial.\\p"
            "It ate my trowel this morning.\\n"
            "For science, I've decided.")
scr += trainer(P + 'Hollis', 'TRAINER_ARCHAEOLOGIST_HOLLIS',
               "Stop! You're stepping on the\\n"
               "Cretaceous!\\p"
               "Every POKeMON I own was dug out\\n"
               "of a rock. They're grateful.\\l"
               "Mostly. One of them bites.",
               "Defeated by someone from\\n"
               "the present day. How modern.",
               "My intern thinks that ARMALDO is\\n"
               "alive. Absurd. It's just resting.\\p"
               "For ten thousand years.\\n"
               "Like I want to.")
place(k, objs, bgs, scr, (10, 11), [(10, 12), (132, 11), (131, 9), (16, 7)])

# =====================================================================================================
# Navel Rock Fork (27x86): een verdwaalde wandelaar boven, items op de doodlopende gangen
k = Kaart('NavelRock_Fork')
P = 'NavelRock_Fork_EventScript_LV'
Q = 'NavelRock_Fork_Text_LV'
objs = [obj('OBJ_EVENT_GFX_HIKER', 8, 7, P + 'Hiker', move='MOVEMENT_TYPE_LOOK_AROUND'),
        ball(23, 16, 'ITEM_SKY_PLATE', 'FLAG_ITEM_NAVEL_ROCK_FORK_SKY_PLATE')]
bgs = [hidden(3, 16, 'ITEM_PP_MAX', 'FLAG_HIDDEN_ITEM_NAVEL_ROCK_FORK_PP_MAX')]
scr = npc(P + 'Hiker', Q + 'Hiker',
          "Left goes up. Right goes down.\\n"
          "I've known that for eleven years.\\p"
          "Every morning I say: today I try\\n"
          "the other one.\\p"
          "Then I have lunch. It's a big\\n"
          "decision. You need lunch for it.")
place(k, objs, bgs, scr, (11, 80), [(4, 7), (22, 7), (11, 79)])

# =====================================================================================================
# Southern Island (33x30): verlaten kamp van een Latias-fan (oostlus)
k = Kaart('SouthernIsland_Exterior')
P = 'SouthernIsland_Exterior_EventScript_LV'
Q = 'SouthernIsland_Exterior_Text_LV'
objs = [obj('OBJ_EVENT_GFX_MOVING_BOX', 26, 12, P + 'Letters'),
        obj('OBJ_EVENT_GFX_SWABLU_DOLL', 25, 10, P + 'Plush'),
        ball(27, 14, 'ITEM_DRAGON_FANG', 'FLAG_ITEM_SOUTHERN_ISLAND_CAMP_DRAGON_FANG')]
bgs = [hidden(10, 17, 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_SOUTHERN_ISLAND_CAMP_BIG_NUGGET')]
scr = sign_obj(P + 'Letters', Q + 'Letters',
               "A crate full of letters. The top\\n"
               "one reads:\\p"
               "'Day 1. A red dragon lives here.\\n"
               "I just know it. I'll wait.'\\p"
               "'Day 90. Still waiting. Built a\\n"
               "chair. The chair is my friend now.'\\p"
               "'Day 2,190. The boat came. I went.\\n"
               "Keep the stuff. Keep the chair.\\l"
               "Don't keep the dream. It's heavy.'")
scr += sign_obj(P + 'Plush', Q + 'Plush',
                "A handmade LATIAS plush.\\p"
                "On closer inspection: a SWABLU\\n"
                "doll, painted red. Badly.\\l"
                "With love, but badly.")
place(k, objs, bgs, scr, (13, 22), [(14, 6), (15, 6), (16, 8), (24, 9)])

# =====================================================================================================
# Birth Island (30x30): kamp van een sterrenkijker, weg van de plekken van de Deoxys-driehoek
k = Kaart('BirthIsland_Exterior')
P = 'BirthIsland_Exterior_EventScript_LV'
Q = 'BirthIsland_Exterior_Text_LV'
TRIANGLE = [(15, 12), (11, 14), (15, 8), (19, 14), (12, 11), (18, 11), (15, 14), (15, 15), (15, 10)]
objs = [obj('OBJ_EVENT_GFX_MOVING_BOX', 6, 15, P + 'Letters'),
        ball(5, 16, 'ITEM_MIND_PLATE', 'FLAG_ITEM_BIRTH_ISLAND_CAMP_MIND_PLATE')]
bgs = [hidden(25, 16, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_BIRTH_ISLAND_CAMP_STAR_PIECE')]
for o in objs + bgs:
    near = [t for t in TRIANGLE if abs(t[0] - o['x']) + abs(t[1] - o['y']) <= 1]
    assert not near, 'Birth Island: te dicht bij de driehoek %s' % near
scr = sign_obj(P + 'Letters', Q + 'Letters',
               "A crate with a telescope lens\\n"
               "and a stack of letters.\\p"
               "'Night 1. The triangle moved.\\n"
               "I didn't touch it. I swear.'\\p"
               "'Night 40. It hums at night.\\n"
               "I've started humming back.'\\p"
               "'Night 90. The triangle and I are\\n"
               "engaged. My mother doesn't\\l"
               "understand. Nobody understands.'\\p"
               "'Night 91. It left me for a kid\\n"
               "with a ticket. Keep the lens.'")
place(k, objs, bgs, scr, (15, 23), [t for t in TRIANGLE if t != (15, 12)] + [(15, 16), (15, 13)])

# =====================================================================================================
# Faraway Island (34x46): kamp van een Mew-onderzoeker (zuidwesthoek, bij het bord)
k = Kaart('FarawayIsland_Entrance')
P = 'FarawayIsland_Entrance_EventScript_LV'
Q = 'FarawayIsland_Entrance_Text_LV'
objs = [obj('OBJ_EVENT_GFX_MOVING_BOX', 6, 34, P + 'Letters'),
        ball(2, 37, 'ITEM_PP_MAX', 'FLAG_ITEM_FARAWAY_ISLAND_CAMP_PP_MAX')]
bgs = [hidden(3, 20, 'ITEM_BIG_MUSHROOM', 'FLAG_HIDDEN_ITEM_FARAWAY_ISLAND_CAMP_BIG_MUSHROOM')]
scr = sign_obj(P + 'Letters', Q + 'Letters',
               "A damp crate. Research notes,\\n"
               "signed 'DR. P. LUMB'.\\p"
               "'Week 1. Saw a small pink cat.\\n"
               "Possibly the ancestor of all\\l"
               "POKeMON. Possibly a cat.'\\p"
               "'Week 12. It knows my name.\\n"
               "I never told it my name.'\\p"
               "'Week 30. It turned into my sister.\\n"
               "I am an only child.'\\p"
               "'Week 31. Going home. If my sister\\n"
               "calls, don't pick up.'")
place(k, objs, bgs, scr, (13, 38), [(22, 8), (23, 8), (3, 33)])

# =====================================================================================================
# Fiery Path, Heatran-hol (59x28): oud vrouwtje dat de lava als sauna gebruikt
k = Kaart('FieryPath_HeatranLair')
P = 'FieryPath_HeatranLair_EventScript_LV'
Q = 'FieryPath_HeatranLair_Text_LV'
objs = [obj('OBJ_EVENT_GFX_HOT_SPRINGS_OLD_WOMAN', 5, 13, P + 'Sauna', move='MOVEMENT_TYPE_FACE_RIGHT')]
bgs = [hidden(10, 4, 'ITEM_FLAME_PLATE', 'FLAG_HIDDEN_ITEM_HEATRAN_LAIR_FLAME_PLATE')]
scr = npc(P + 'Sauna', Q + 'Sauna',
          "Ahh. Twelve hundred degrees.\\n"
          "Best thing there is for the knees.\\p"
          "The hot springs in LAVARIDGE?\\n"
          "Lukewarm soup for tourists.\\p"
          "The big one in the back doesn't\\n"
          "mind me. We're both old and we\\l"
          "both like it hot.")
place(k, objs, bgs, scr, (46, 8), [(20, 21), (16, 21), (47, 8)])

# =====================================================================================================
# Meteor Falls, Starfall Grotto (47x44): sterrenkijker; elke dag nieuw sterrenstof (dagelijkse flags)
k = Kaart('MeteorFalls_StarfallGrotto')
P = 'MeteorFalls_StarfallGrotto_EventScript_LV'
Q = 'MeteorFalls_StarfallGrotto_Text_LV'
objs = [obj('OBJ_EVENT_GFX_SCIENTIST_2', 26, 20, P + 'Stargazer', move='MOVEMENT_TYPE_FACE_UP')]
bgs = [hidden(17, 23, 'ITEM_STARDUST', 'FLAG_DAILY_HIDDEN_STARFALL_STARDUST_1'),
       hidden(29, 26, 'ITEM_STARDUST', 'FLAG_DAILY_HIDDEN_STARFALL_STARDUST_2')]
scr = npc(P + 'Stargazer', Q + 'Stargazer',
          "I'm counting the stars that fall\\n"
          "in here. I lost count at four.\\p"
          "So I started over. Four again.\\n"
          "It's always four. It's suspicious.\\p"
          "They leave STARDUST on the floor.\\n"
          "Every single day. Like a cat\\l"
          "bringing you a bird.")
place(k, objs, bgs, scr, (23, 29), [(18, 21), (28, 29)])

# =====================================================================================================
# Safari-zones: per zone één NPC + één verborgen item
k = Kaart('SafariZone_FairyForest')
P = 'SafariZone_FairyForest_EventScript_LV'
Q = 'SafariZone_FairyForest_Text_LV'
objs = [obj('OBJ_EVENT_GFX_LASS', 12, 3, P + 'Godmother', move='MOVEMENT_TYPE_FACE_DOWN')]
bgs = [hidden(33, 36, 'ITEM_MEADOW_PLATE', 'FLAG_HIDDEN_ITEM_SAFARI_FAIRY_MEADOW_PLATE')]
scr = npc(P + 'Godmother', Q + 'Godmother',
          "I came here to find my fairy\\n"
          "godmother.\\p"
          "I found a HATTERENE. It read my\\n"
          "mind and hit me with a hammer.\\p"
          "I think that's a yes?\\n"
          "I'm waiting for the dress.")
place(k, objs, bgs, scr, (42, 21), [(36, 7), (7, 32), (3, 18)])

k = Kaart('SafariZone_ThunderPlains')
P = 'SafariZone_ThunderPlains_EventScript_LV'
Q = 'SafariZone_ThunderPlains_Text_LV'
objs = [obj('OBJ_EVENT_GFX_MAN_3', 42, 13, P + 'Lightning', move='MOVEMENT_TYPE_FACE_LEFT')]
bgs = [hidden(43, 4, 'ITEM_ELECTIRIZER', 'FLAG_HIDDEN_ITEM_SAFARI_THUNDER_ELECTIRIZER')]
scr = npc(P + 'Lightning', Q + 'Lightning',
          "I study lightning. Up close.\\n"
          "With this metal rod.\\p"
          "I've been struck fourteen times.\\n"
          "My theory: it likes me.\\p"
          "My hair has a theory too.\\n"
          "It points straight up.")
place(k, objs, bgs, scr, (24, 4), [(41, 7), (6, 32), (15, 21)])

k = Kaart('SafariZone_HauntedCamp')
P = 'SafariZone_HauntedCamp_EventScript_LV'
Q = 'SafariZone_HauntedCamp_Text_LV'
objs = [obj('OBJ_EVENT_GFX_CAMPER', 4, 24, P + 'Counselor', move='MOVEMENT_TYPE_FACE_RIGHT')]
bgs = [hidden(14, 38, 'ITEM_CLEANSE_TAG', 'FLAG_HIDDEN_ITEM_SAFARI_SPOOK_CLEANSE_TAG')]
scr = npc(P + 'Counselor', Q + 'Counselor',
          "Welcome to CAMP SPOOKAMORE!\\n"
          "I'm your camp counselor.\\p"
          "Ghost stories start at nine.\\n"
          "Same story for thirty years.\\p"
          "The campers stopped coming in '94.\\n"
          "Some of them still listen.")
place(k, objs, bgs, scr, (42, 27), [(5, 7), (35, 7), (17, 35), (13, 17)])

# =====================================================================================================
for label, s in TEXTS:
    try:
        check_text(label, s)
    except AssertionError as e:
        print(e); FAIL.append('tekst')
assert not FAIL, FAIL
print('ok')
