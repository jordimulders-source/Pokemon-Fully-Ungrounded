#!/usr/bin/env python3
"""The Spire: events (Project Grounded). Genereert src/data/spire_events.h.

Elk event: titel, verhaal (max. 4 regels), icoon (soort), acts, en 1-3 opties.
Een optie heeft effecten (fx) en een uitkomsttekst, of een kansworp (chance, a/ra, b/rb).
De effectregel naast de optie ("+90¥, Spikes x3") wordt uit de effecten gemaakt, dus tekst en
effect kloppen altijd. Opties met 'need' vragen een type in het team (Pokémon-kennis belonen).

Effecten (zie enum SpireFx in include/spire.h):
  gold N / goldpct N      geld erbij/eraf (goldpct: procent van je geld)
  heal N                  beide Pokémon N% HP (negatief = schade, nooit flauwvallen)
  hurt1 N                 één willekeurige Pokémon verliest N%
  maxhp N                 blijvend N procentpunt max HP (beide)
  bp N                    Battle Points
  relic / loserelic       willekeurige nieuwe relic / een relic kwijt
  item R / give ITEM      vasthouditem (zeldzaamheid 0-2 of vast), speler kiest wie
  loseitems               beide vasthouditems weg
  teach R / teachtype R   move leren (willekeurig / van een type uit je team); B = overslaan
  teachmove MOVE          vaste move leren
  upgrade N / forget N    N willekeurige moves "+" / vergeten
  remove                  zelf een move kiezen om te vergeten (card removal)
  fullheal / pp           HP en PP vol / alleen PP
  sleep C                 per Pokémon C% kans: begint het volgende gevecht in slaap
  toxic N                 N gevechten Toxic Spikes (40% gif; Poison/Steel/Heavy-Duty Boots veilig)
  elite                   elitegevecht (relic + moves als beloning)
  recruit                 de event-Pokémon van dit event ({STR_VAR_3}) vervangt er één
  recruitspecies SPECIES  vaste soort vervangt er één (moet in de rentalpool staan)
  ditto                   de speciale Ditto (Jordi)
  recruitpseudo           de pseudo-legendary van dit event (icoon 'PSEUDO'), op het stadium van de act + 1
  wonder                  één willekeurige Pokémon wordt geruild voor een willekeurige rental
  evolve                  één willekeurige Pokémon evolueert nu al (geen evolutie mogelijk: +60¥)
  wheel                   Spinda's rad (zes uitkomsten, tekst uit de C-code)

Balans (SPIRE_BALANS.md, runsim.py): start 75¥, ±235¥ per act; move 45/70/120¥, item 50/85/140¥, relic 150¥;
rust = 30% HP, na een gevecht 8%, nieuwe act 40%. Een event is gemiddeld ±60-120¥ waard; gratis winst alleen met een type-eis of
als ruil (HP, max HP, een move, risico). Een paar events zijn bewust gemeen (Slay: niet elk event is
een cadeau), maar er is dan altijd een uitweg die weinig kost.

Gebruik: python3 tools/grounded/spire/events.py
"""
import os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT = os.path.join(REPO, 'src/data/spire_events.h')

STORY_W = 218       # pixels per regel (FONT_SMALL_NARROW), verhaal- en uitkomstvak
NAME_W = 64         # optienaam
SUM_W = 146         # effectregel (x 78-224)
TITLE_W = 140       # titel (FONT_NORMAL)
VAR_W = 50          # {STR_VAR_3} (soortnaam)

E = []
def ev(key, title, icon, story, options, acts=(1, 2, 3), weight=4, walk=None):
    # weight: kans om gekozen te worden (4 = normaal, 1 = zeldzaam)
    # walk: B = weglopen met deze tekst (v0.9.82, Jordi: Vending Machine). Verplicht als alle opties dicht kunnen
    # zitten (geld, type, relic of item nodig) en er geen gratis optie is; anders loop je vast of moet je iets kopen.
    E.append(dict(key=key, title=title, icon=icon, story=story, options=options, acts=acts, weight=weight, walk=walk))
def opt(name, fx=(), result='', need=None, **kw):
    d = dict(name=name, fx=list(fx), result=result, need=need)
    d.update(kw)
    return d
def gamble(name, chance, a, ra, b, rb, need=None):
    return dict(name=name, chance=chance, fx=list(a), result=ra, fxb=list(b), resultb=rb, need=need)
LEAVE = lambda text='You walk on. The tower sighs.': opt('Leave', [], text)

# --- de events -----------------------------------------------------------------------------------
# Oude 16 (v0.8.104), herschreven naar data
ev('ditto', 'A VERY SPECIAL DITTO', 'DITTO',
   'A shiny Ditto. Perfect genes, a Choice Scarf and Imposter. It wants in. It knows it is worth it. '
   'It transforms into a foe at the start of every battle.',
   [opt('Take it', [('ditto',)], 'The Ditto looks at your team, then at you. It has already decided who goes home.'),
    LEAVE('The Ditto turns into you, out of spite, and walks the other way.')])
ev('mushrooms', 'MUSHROOM PATH', 'BRELOOM',
   'Berries grow between the mushrooms. The further you reach, the more spores you breathe. '
   'A Breloom watches. It does not help.',
   [opt('Reach a bit', [('item', 0), ('sleep', 25)], 'You grab something round. It is probably a Berry.'),
    opt('Reach deep', [('item', 1), ('heal', 20), ('sleep', 70)], 'You eat half the path. It was worth it, for now.'),
    LEAVE('You hold your breath and walk past. The Breloom is disappointed.')])
ev('spikes', 'A FLOOR OF SPIKES', 'GLIMMET',
   'Toxic Spikes, wall to wall. Someone dropped a wallet in the middle. Of course they did.',
   [opt('Walk on', [('gold', 90), ('toxic', 3)], 'You get the wallet. Your feet tingle. They will keep tingling for a while.'),
    opt('Stroll over', [('gold', 90)], 'Your Poison type walks over the spikes, picks up the wallet and hands it to you. Immune and smug.', need='POISON'),
    opt('Climb around', [('heal', -12)], 'Along the outside wall. Slow, windy, and nobody is poisoned. Mostly scared.')])
ev('deleter', 'THE MOVE DELETER', None,
   'A man in a trench coat offers to clean up your moves. He does not say which. He smells of glue.',
   [opt('Let him', [('gold', 110), ('forget', 1)], 'He works fast. He pays in cash. He does not make eye contact.'),
    gamble('Tip him', 75, [('gold', -40), ('upgrade', 1)], 'For a tip he polishes a move instead. It shines.',
           [('gold', -40), ('forget', 1)], 'He deletes it anyway. "Force of habit." No refunds.'),
    LEAVE('He shrugs and offers the same deal to a Zubat.')])
ev('tutor', 'MOVE TUTOR', None,
   'A tutor sits behind a desk in the stairwell. Payment upfront. Refunds never. '
   'He only teaches what suits your team.',
   [opt('Lesson', [('gold', -45), ('teachtype', 1)], 'He hands you a worksheet. It is mostly a move.'),
    opt('Masterclass', [('gold', -100), ('teachtype', 2)], 'Three hours, one move. He insists it is worth it. He is usually right.'),
    LEAVE('He writes your name down. In a different notebook.')])
ev('lunch', "SNORLAX'S LUNCH", 'SNORLAX',
   'A sleeping Snorlax guards its lunch. You can take one thing before it wakes up.',
   [opt('Oran Berry', [('heal', 30)], 'Your team shares the Oran Berry. Snorlax snores, betrayed.'),
    opt('Rare Candy', [('maxhp', 5)], 'They were already level 100. It still helps. Do not think about it too hard.'),
    opt('Lunch box', [('relic',), ('maxhp', -8)], 'Something good inside. Snorlax wakes up and sits on your team. Permanently, a bit.')])
ev('chest', "GIMMIGHOUL'S CHEST", 'GIMMIGHOUL',
   'A chest full of coins. One of the coins is looking at you.',
   [gamble('Grab coins', 50, [('gold', 130)], 'Coins are coins. The one with eyes stays quiet. For now.',
           [('gold', 130), ('heal', -20)], 'One coin was a Gimmighoul. It bites everyone, then itself, out of habit.'),
    opt('Ask nicely', [('gold', 80)], 'Your Ghost type and the Gimmighoul talk for a while. It hands over a fair share. Professional courtesy.', need='GHOST'),
    LEAVE('The coin with eyes watches you leave. It will remember this.')])
ev('nurse', 'NURSE ON A BREAK', 'CHANSEY',
   "Nurse Joy's cousin is on her lunch break. She will help, for a fee. A big fee.",
   [opt('Heal', [('gold', -40), ('heal', 40)], 'She heals your team without putting down her sandwich. Professional.'),
    opt('Special', [('gold', -75), ('upgrade', 1)], 'She knows a Porygon2. It sends its regards.'),
    LEAVE('She waves. With the sandwich.')])
ev('wheel', "SPINDA'S WHEEL", 'SPINDA',
   'A Spinda spins a prize wheel. It is very dizzy. So is the wheel. Gold, a relic, a full heal, '
   'a fresh move, or a slap.',
   [opt('Spin it', [('wheel',)], ''),
    LEAVE('Spinda spins anyway, alone. It looks happy.')])
ev('ace', 'A FAINTED ACE', 'LUCARIO',
   'An Ace Trainer lies fainted on the stairs. Her bag is open. Her Lucario is only sleeping. Lightly.',
   [gamble('Search bag', 50, [('item', 2)], 'A rare held item. Lucario sleeps through it. You feel bad. Briefly.',
           [('elite',)], 'Lucario wakes up, reads your aura and calls its friends. Its friends are huge.'),
    LEAVE('You put a blanket over her. Lucario nods, without opening its eyes.')])
ev('glitch', 'A GLITCH IN THE WALL', 'PORYGON_Z',
   'A Porygon-Z hums inside a crack of light. Step in and your moves get rewritten. Painfully.',
   [opt('Step in', [('heal', -20), ('upgrade', 2)], 'Everything is pixels for a second. Then it is better. Mostly.'),
    LEAVE('The crack closes. Porygon-Z sends you an error message.')])
ev('candle', "LITWICK'S CANDLE", 'LITWICK',
   'A Litwick offers warmth. It only asks for a memory. A move, to be exact.',
   [opt('Offer', [('forget', 1), ('fullheal',)], 'A move burns away. Your team is fully healed in the warmth. You do not remember what you lost. That is the point.'),
    opt('Share flame', [('heal', 40)], 'Your Fire type lights the Litwick back up. It is so grateful it forgets to eat your soul.', need='FIRE'),
    LEAVE('The Litwick follows you for a while, then gives up.')])
ev('stranger', 'A STRONG STRANGER', 'RECRUIT',
   'A wild {STR_VAR_3} blocks the stairs. It is strong. It wants a fight, or a team.',
   [opt('Recruit', [('heal', -25), ('recruit',)], 'You earn its respect the hard way. It is ready to join.'),
    LEAVE('{STR_VAR_3} lets you pass. It looks disappointed in you specifically.')])
ev('samples', 'FREE SAMPLES', 'MEOWTH',
   'A Meowth runs a free sample stand. It is suspiciously free.',
   [gamble('Taste it', 50, [('heal', 30)], 'Delicious. Your team feels better. Meowth looks almost disappointed.',
           [('heal', -10)], 'It was a sock. Meowth charges you nothing for the lesson.'),
    opt('Steal it', [('gold', 40), ('heal', -15)], 'You grab the cash box. Meowth grabs you back. Meowth has claws.'),
    LEAVE()])
ev('unown', 'WRITING ON THE WALL', 'UNOWN',
   'An Unown spells out a word on the wall. It is an insult. About you.',
   [opt('Read it', [('teach', 2)], 'You say the word out loud. Something answers. It is a move.'),
    opt('Correct it', [('gold', 30)], 'You fix the spelling. The Unown pays you to go away.'),
    LEAVE('You pretend not to have seen it. The Unown underlines it.')])
ev('hiker', 'A HELPFUL HIKER', None,
   'A Hiker offers to carry your team up a floor. He insists. Loudly.',
   [opt('Accept', [('heal', 25)], 'You are carried. It is humiliating. It is also very relaxing.'),
    opt('Refuse', [('bp', 2)], 'He respects your rudeness. Hikers are like that.')])

# Nieuw (v0.8.105)
ev('magikarp', 'THE MAGIKARP SALESMAN', 'MAGIKARP',
   'A man in a suit sells a Magikarp. "It evolves into something incredible," he says. He has said this before. In court.',
   [opt('Buy it', [('gold', -100), ('recruitspecies', 'GYARADOS')], 'It evolves the moment it touches water. The salesman looks more surprised than you.'),
    gamble('Haggle', 35, [('gold', -50), ('recruitspecies', 'GYARADOS')], 'He sighs and accepts 50¥. The Magikarp evolves out of pure spite.',
           [('gold', -50)], 'He takes the 50¥ and leaves. With the Magikarp. That was the deal, apparently.'),
    LEAVE('He offers the same deal to a Wingull. The Wingull buys it.')], acts=(1, 2))
ev('butterfree', 'BUTTERFREE MIGRATION', 'BUTTERFREE',
   'A swarm of Butterfree drifts up the stairwell. One of them is lagging behind and looks at you hopefully.',
   [opt('Adopt it', [('recruitspecies', 'BUTTERFREE')], 'It lands on your head. It is staying. It never had a choice either.'),
    gamble('Breathe in', 60, [('heal', 30)], 'The scales smell like summer. Your team feels better.',
           [('sleep', 100)], 'Sleep Powder. Of course it is Sleep Powder.'),
    LEAVE('The swarm flies on. The straggler follows it, eventually.')], acts=(1, 2))
ev('feebas', 'FEEBAS IN A PUDDLE', 'FEEBAS',
   'A Feebas flops in a puddle on the stairs. Nobody wants it. It knows.',
   [opt('Feed it', [('gold', -60), ('recruitspecies', 'MILOTIC')], 'You feed it Pokéblocks and tell it it is beautiful. It believes you. It becomes Milotic out of sheer surprise.'),
    opt('Show it water', [('recruitspecies', 'MILOTIC'), ('heal', -10)], 'Your Water type carries it to the sea, which takes a while. It comes back a Milotic.', need='WATER'),
    LEAVE('The Feebas watches you go. It is used to that.')])
ev('beedrill', 'THE HIVE', 'BEEDRILL',
   'A Beedrill hive hangs over the stairs. Honey drips from it. So does venom.',
   [gamble('Take honey', 60, [('heal', 40)], 'The honey is incredible. The Beedrill are elsewhere. You got lucky.',
           [('heal', -20)], 'The Beedrill were not elsewhere.'),
    opt('Smoke out', [('heal', 40)], 'Your Fire type smokes the hive. The Beedrill leave politely. The honey is yours.', need='FIRE'),
    opt('Befriend one', [('maxhp', -10), ('recruitspecies', 'BEEDRILL')], 'It takes a while and a lot of stings, but one Beedrill decides you are its queen now.')])
ev('diggersby', 'A HOLE IN THE FLOOR', 'DIGGERSBY',
   'A Diggersby has dug a shortcut straight through the floor. It offers to dig you one too. It does not say where to.',
   [gamble('Jump in', 50, [('gold', 80), ('heal', 20)], 'You land in a storage room full of lost wallets. Nice.',
           [('heal', -20)], 'You land in the floor below. On a Geodude.'),
    opt('Hire it', [('gold', -40), ('recruitspecies', 'DIGGERSBY')], 'Diggersby signs a contract with its ear. It will dig for you now.'),
    LEAVE('It shrugs and keeps digging. You hear it for three more floors.')])
ev('kricketune', 'A VIOLIN SOLO', 'KRICKETUNE',
   'A Kricketune plays a violin solo in the stairwell. It is moving. It is also forty minutes long.',
   [opt('Listen', [('heal', 30)], 'Your team cries a little and feels better. Nobody mentions it.'),
    opt('Encore', [('gold', -80), ('recruitspecies', 'KRICKETUNE')], 'You request an encore. It is so flattered it joins your team. The encore continues in battle.'),
    gamble('Heckle', 50, [('gold', 60)], 'The crowd agrees with you and pays you to leave.',
           [('heal', -15)], 'Kricketune hits you with the violin. Twice. It was in tune.')])
ev('delibird', "DELIBIRD'S GIFTS", 'DELIBIRD',
   'A Delibird hands out presents. Some of them explode. It does not know which. Neither does the present.',
   [gamble('Open one', 60, [('relic',)], 'A real present. Delibird is as surprised as you.',
           [('heal', -25)], 'It was Present. The bad kind.'),
    opt('Regift it', [('gold', 45)], 'You sell it unopened at the next floor. The buyer screams later.'),
    LEAVE('Delibird gives your present to a Snorunt. It explodes. The Snorunt is fine.')])
ev('clefairy', 'MOONLIGHT DANCE', 'CLEFAIRY',
   'Clefairy dance in a circle around a Moon Stone. They invite you in. They do not mention the stone.',
   [opt('Dance', [('heal', 20), ('bp', 1)], 'You dance badly. The Clefairy are kind about it.'),
    opt('Lead dance', [('evolve',)], 'Your Fairy type knows the steps. The Moon Stone glows and someone evolves early.', need='FAIRY'),
    opt('Steal stone', [('evolve',), ('elite',)], 'You grab the Moon Stone and someone evolves. Then the real owners of the stone arrive.')])
ev('eviolite', 'THE EVIOLITE STAND', 'ROGGENROLA',
   'A Roggenrola sells Eviolites. "Never evolve," it says. "Stay small. Stay hard." It has never evolved.',
   [opt('Buy one', [('gold', -50), ('give', 'EVIOLITE', 'Eviolite')], 'Defenses up, as long as you have not evolved yet. The Roggenrola nods wisely.'),
    LEAVE('The Roggenrola does not move. It has not moved in years.')], acts=(1, 2))
ev('persian', 'COIN TOSS', 'PERSIAN',
   'A Persian runs a coin toss. Heads, you win. Tails, it wins. It flips its own coin.',
   [gamble('Bet 50¥', 50, [('gold', 50)], 'Heads. Persian stares at the coin for a long time.',
           [('gold', -50)], 'Tails. Persian purrs.'),
    gamble('All or nothing', 45, [('goldpct', 100)], 'Heads! Persian quietly leaves the business.',
           [('goldpct', -100)], 'Tails. Persian buys a nicer coin with your money.'),
    LEAVE('Persian flips the coin for itself. It wins.')])
ev('rotom', 'THE VENDING MACHINE', 'ROTOM',
   'A vending machine hums in the corner. A Rotom lives inside. Prices are high. The drinks are suspicious.',
   [opt('Fresh Water', [('gold', -20), ('heal', 20)], 'It is water. Rotom charged it a little.'),
    opt('Soda Pop', [('gold', -30), ('pp',)], 'Your team is buzzing. Possibly literally.'),
    opt('Kick it', [('heal', 30), ('gold', 30)], 'Your Electric type gives it a friendly jolt. Rotom recognises a colleague and pays out.', need='ELECTRIC')],
   walk='You walk away thirsty. The machine flashes "THANK YOU" anyway. Rotom is being sarcastic.')
ev('slowpoke', 'THE SLOWPOKE WELL', 'SLOWPOKE',
   'A Slowpoke dangles its tail into a well. It has been fishing for nine days. Something has been nibbling for eight.',
   [gamble('Pull the tail', 50, [('item', 2)], 'Something comes up with it. Something good. Slowpoke notices next Tuesday.',
           [('heal', -15)], 'Something comes up with it. Something with teeth.'),
    opt('Wait with it', [('fullheal',), ('sleep', 50)], 'You lose track of time. Your team is fully rested. Some of them are still resting.'),
    LEAVE('You leave. Slowpoke does not notice for a while.')])
ev('banette', 'SECOND-HAND ITEMS', 'BANETTE',
   'A Banette from the Mart sells items off the books. "Slightly used," it says. The previous owners are not mentioned.',
   [opt('Buy one', [('gold', -20), ('item', 2), ('maxhp', -5)], 'A great item for 20¥. It comes with a small curse. Nobody reads the receipt.'),
    opt('Sell yours', [('loseitems',), ('gold', 100)], 'Banette buys every held item your team owns. It strokes them. You leave quickly.'),
    LEAVE('Banette zips its mouth shut. It was smiling.')])
ev('dusknoir', 'THE COLLECTOR', 'DUSKNOIR',
   'A Dusknoir offers to carry your burdens. All of them. Forever. It has a very big bag.',
   [opt('Give a move', [('remove',), ('maxhp', 8)], 'You choose something to forget. Your team feels lighter and sturdier.'),
    opt('Give a relic', [('loserelic',), ('upgrade', 2)], 'It takes a relic and gives back strength. A fair trade, by afterlife standards.'),
    LEAVE('Dusknoir follows you with its eye. Its one eye.')])
ev('shedinja', 'AN EMPTY SHELL', 'SHEDINJA',
   'An empty shell lies on the floor. It is still looking at you. It is not empty.',
   [opt('Wear it', [('maxhp', -15), ('relic',)], 'Something hollow settles in your team. Something useful falls out of the shell.'),
    LEAVE('You back away. The shell turns its head to follow you.')])
ev('egg', 'AN ABANDONED EGG', 'TOGEPI',
   'An Egg sits on a cushion with a note: "Please raise me." The note is seven years old. The Egg is warm.',
   [opt('Hatch it', [('heal', -10), ('recruit',)], 'You walk until it hatches. It is a {STR_VAR_3}. It is already fully grown. Do not ask.', sum='Surprise joins'),
    opt('Sell it', [('gold', 70)], 'A collector pays well. You do not ask what he collects.'),
    LEAVE('You leave the Egg. It wobbles in a judgemental way.')])
ev('sableye', "SABLEYE'S STASH", 'SABLEYE',
   'A Sableye guards a pile of gems. It is eating them. It offers you one, half-chewed.',
   [opt('Take the gem', [('item', 1)], 'It is sticky. It is also valuable.'),
    gamble('Take the pile', 50, [('gold', 120)], 'Sableye is too full to stop you.',
           [('heal', -30)], 'Sableye is not too full to stop you.'),
    LEAVE('Sableye shrugs and keeps eating.')])
ev('garbodor', 'THE TRASH HEAP', 'GARBODOR',
   'A Garbodor sits on a mountain of trash. Somewhere inside: treasure. Also: everything else.',
   [gamble('Dig', 40, [('relic',)], 'Under a broken bike: treasure. Nobody ever looks under the bike.',
           [('heal', -10), ('toxic', 2)], 'You find nothing but trash. It finds you back.'),
    opt('Dig properly', [('relic',)], 'Your Poison type dives in like a professional. It comes back with a relic and a smile.', need='POISON'),
    LEAVE('Garbodor waves. Something falls off it.')])
ev('smeargle', 'THE ATELIER', 'SMEARGLE',
   "A Smeargle paints portraits of your team's moves. Mostly accurately.",
   [opt('Portrait', [('gold', -40), ('upgrade', 1)], 'It paints one move a little better than it really is. Then it becomes true.'),
    gamble('Abstract', 50, [('upgrade', 2)], 'Bold. Daring. Somehow, it works.',
           [('forget', 1)], 'Bold. Daring. It painted over one of your moves.'),
    LEAVE('Smeargle paints you leaving. It is its best work.')])
ev('mimikyu', "MIMIKYU'S BIRTHDAY", 'MIMIKYU',
   'A Mimikyu throws itself a birthday party. Nobody came. It is not crying. It is the costume.',
   [opt('Join', [('heal', 30)], 'There is cake. There are games. Mimikyu wins all of them.'),
    opt('Bring a gift', [('gold', -75), ('relic',)], 'You give it something. It gives you its best present back. It insisted.'),
    opt('Sneak out', [('maxhp', -3)], 'You leave. Mimikyu does not look up. You will carry this with you.')])
ev('zubat', 'THE CEILING', 'ZUBAT',
   'The ceiling is covered in Zubat. Every single one is, statistically, about to wake up.',
   [gamble('Tiptoe', 70, [], 'Not one of them wakes up. You did it. Nobody saw.',
           [('heal', -20)], 'One of them wakes up. Then all of them.'),
    opt('Sprint', [('heal', -8)], 'You run. A few of them notice. It is fine. It is mostly fine.'),
    opt('Lullaby', [('bp', 2)], 'Your Fairy type hums a lullaby. The Zubat sleep deeper. You get applause from one of them.', need='FAIRY')])
ev('dojo', 'THE DOJO', 'HITMONTOP',
   'A Hitmontop runs a training dojo. Spinning optional. Pain mandatory.',
   [opt('Train', [('heal', -15), ('upgrade', 1)], 'Hours of training. One move gets sharper. Everything else hurts.'),
    opt('Spar master', [('elite',)], 'Hitmontop bows and steps aside. The senior students step forward.'),
    opt('Teach a class', [('gold', 80), ('bp', 2)], 'Your Fighting type teaches the morning class. The students are terrified. They pay anyway.', need='FIGHTING')])
ev('dugtrio', "DUGTRIO'S TOLL", 'DUGTRIO',
   'Three heads pop up from the floor and ask for a toll. Each head wants its own.',
   [opt('Pay up', [('gold', -45)], 'Fifteen each. They count it three times.'),
    opt('Refuse', [('heal', -15)], 'Earthquake. Three times. They are thorough.'),
    opt('Fly over', [], 'Your Flying type floats over the toll. Dugtrio cannot touch you. Ground moves never could.', need='FLYING')])
ev('shuckle', 'SHUCKLE JUICE', 'SHUCKLE',
   'A Shuckle has been storing Berries in its shell for a long time. The juice is ready. Ready is a strong word.',
   [gamble('Drink', 60, [('maxhp', 8)], 'It tastes terrible. You feel incredible. Permanently.',
           [('heal', -20)], 'It tastes terrible. You feel terrible. Temporarily.'),
    opt('Bottle it', [('give', 'SITRUS_BERRY', 'Sitrus Berry')], 'The bottle is mostly one Sitrus Berry. For later. Later is a strong word too.'),
    LEAVE('The Shuckle withdraws, insulted.')])
ev('xatu', 'THE SEER', 'XATU',
   'A Xatu stares at your future. It offers to tell you about it. It has already seen your reaction.',
   [opt('Pay 50¥', [('gold', -50), ('upgrade', 1), ('bp', 1)], 'It tells you about your next fight. One move is ready for it.'),
    gamble('Stare back', 50, [('bp', 3)], 'You win the staring contest. Xatu is impressed. Xatu is never impressed.',
           [('sleep', 100)], 'Xatu wins. You will be very sleepy in the next fight.'),
    LEAVE('Xatu already knew you would leave.')])
ev('jirachi', 'A WISHING STAR', 'JIRACHI',
   'Jirachi sleeps in a star-shaped crack in the wall. You get one wish. It will come true. Exactly as written.',
   [opt('Power', [('upgrade', 2), ('maxhp', -10)], 'Your moves become stronger. You become a bit less. You did not specify.'),
    opt('Health', [('maxhp', 10)], 'Your team is sturdier. Forever. Jirachi yawns.'),
    opt('Wealth', [('gold', 150), ('sleep', 100)], 'Coins rain down. Jirachi wakes up cranky and casts a little Yawn.')], acts=(2, 3))
ev('oldrod', 'THE OLD ROD', 'REMORAID',
   'A fisherman offers you his Old Rod. It is terrible. It is bad on purpose. He insists you try it.',
   [gamble('Fish', 80, [('gold', 10)], 'A Magikarp. He buys it from you for 10¥. Everybody wins, technically.',
           [('relic',)], 'Something heavy. It is a relic. The fisherman cries.'),
    LEAVE('He keeps fishing. A Magikarp. Again.')])
ev('absol', 'A WARNING', 'ABSOL',
   'An Absol appears on the stairs. In the legends, it warns of disaster. It is looking straight at you.',
   [opt('Heed it', [('maxhp', 5)], 'You go carefully. Your team gets sturdier from all the caution.'),
    opt('Ignore it', [('gold', 70), ('toxic', 2)], 'You ignore it and find a wallet. Then you step on something.'),
    gamble('Pet it', 50, [('recruitspecies', 'ABSOL')], 'It lets you. It follows you. The disaster was apparently you.',
           [('heal', -25)], 'It does not let you.')])
ev('drifloon', 'A RED BALLOON', 'DRIFLOON',
   'A Drifloon offers to take you up. Children who held its hand were never seen again. But this is a tower.',
   [gamble('Hold its hand', 50, [('relic',)], 'You float up past a window ledge with a relic on it. Drifloon drops you off. Nicely.',
           [('maxhp', -10)], 'Drifloon takes you somewhere. You come back. Some of you does not.'),
    opt('Pop it', [('heal', -10), ('bp', 1)], 'It goes Aftermath. Everyone is fine. Mostly.'),
    LEAVE('Drifloon floats away, still holding out its hand.')])
ev('library', 'THE TM LIBRARY', 'SIGILYPH',
   'A library of TMs. None are labelled. Some are just music. A Sigilyph guards the rare shelf.',
   [opt('Read one', [('teach', 1)], 'You pick one at random. It is not music.'),
    opt('Rare shelf', [('gold', -60), ('teach', 2)], 'Sigilyph accepts your library fine in advance.'),
    opt('Read its mind', [('teach', 2)], 'Your Psychic type reads Sigilyph, who reads the rare shelf. It is very confusing. It works.', need='PSYCHIC')])
ev('chimecho', 'THE WIND CHIME', 'CHIMECHO',
   'A Chimecho rings in the stairwell. Your team feels better. Chimecho asks for "a small donation".',
   [opt('Donate', [('gold', -25), ('heal', 30), ('pp',)], 'It rings louder. Your team is refreshed.'),
    opt('Walk on', [('heal', 10)], 'You heard it anyway. Chimecho glares.')])
ev('medicham', 'MEDITATION', 'MEDICHAM',
   'A Medicham meditates on the landing. It offers to teach you to let go of things.',
   [opt('Let go', [('remove',), ('heal', 15)], 'You choose a move and let it go. Medicham nods. Your mind is clear.'),
    opt('Hold on', [('upgrade', 1), ('heal', -10)], 'You hold on harder. Medicham frowns. One move gets stronger out of stubbornness.'),
    LEAVE('Medicham does not open its eyes. It knew.')])
ev('voltorb', 'THREE POKé BALLS', 'VOLTORB',
   'Three Poké Balls lie on a table. One of them is a Voltorb. All three look smug.',
   [gamble('Pick one', 66, [('item', 1)], 'A real Poké Ball, with a real item inside.',
           [('heal', -25)], 'Voltorb. It used Self-Destruct, which is banned here, so it just exploded instead.'),
    opt('Grab all three', [('item', 2), ('heal', -25)], 'You get the good item. You also get the Voltorb.'),
    LEAVE('The Voltorb rolls after you for a bit. It is lonely.')])
ev('honedge', 'A SWORD IN THE STONE', 'HONEDGE',
   'A sword floats above a stone. Legend says whoever pulls it out becomes stronger. The legend leaves out the rest.',
   [opt('Pull it', [('upgrade', 2), ('maxhp', -8)], 'Your moves are sharper. The sword took something in exchange. It always does.'),
    LEAVE('The Honedge looks for someone else. It has time.')])
ev('pelipper', 'MAIL', 'PELIPPER',
   'A Pelipper delivers a letter addressed to you. It is a bill. For what, it does not say.',
   [opt('Pay it', [('gold', -40), ('maxhp', 3)], 'You pay. You feel like a responsible adult. It makes you slightly sturdier.'),
    gamble('Throw it away', 50, [], 'Nothing happens. It was a scam.',
           [('goldpct', -50)], 'It was not a scam. Collection agency. They take half.'),
    LEAVE('You do not open it. Pelipper waits.')])
ev('pyukumuku', 'BLOCKED STAIRS', 'PYUKUMUKU',
   'A Pyukumuku blocks the only stairs. Throwing them back into the sea is a local tradition. The sea is far away.',
   [opt('Kick it', [('heal', -10), ('gold', 30)], 'It goes Innards Out on your shoes. Local fishermen tip you for the effort.'),
    gamble('Step over', 50, [], 'You make it. It did not notice. Its whole life is not noticing.',
           [('heal', -15)], 'It noticed.'),
    opt('Carry it', [('gold', 30), ('bp', 1)], 'Your Water type carries it all the way to the sea. The fishermen applaud.', need='WATER')])
ev('wonder', 'WONDER TRADE', 'PORYGON',
   'A machine in the wall: put a Pokémon in, get a Pokémon out. Nobody knows where they come from. Nobody asks.',
   [opt('Trade', [('wonder',)], 'The machine whirs. Something comes out. It looks confused too.'),
    LEAVE('The machine spits out a Bidoof at you anyway. It runs off.')])
ev('zorua', 'TWO OF YOU', 'ZORUA',
   'Your own team walks towards you. One of them is a Zorua. You are fairly sure which.',
   [gamble('Point', 50, [('gold', 80)], 'Correct. Zorua drops its disguise and its wallet.',
           [('heal', -20)], 'Wrong. Your own Pokémon is offended. Zorua laughs and leaves.'),
    LEAVE('Both of them follow you. One disappears around the corner.')])
# v0.8.107 (Jordi): Gholdengo, Snorlax en een willekeurige pseudo-legendary
ev('gholdengo', '999 COINS', 'GIMMIGHOUL',
   'A Gimmighoul sits on a heap of coins and counts them out loud. It has 998. It has had 998 for years. It is looking at your wallet.',
   [opt('Give it all', [('gold', -120), ('goldpct', -100), ('recruitspecies', 'GHOLDENGO')],
        'It counts to 999 and screams. When the light fades, a Gholdengo is surfing on your money. It wants to come with you. It is keeping the money.',
        sum='{COLOR RED}{SHADOW LIGHT_RED}All ¥ (120+){COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}, {COLOR GREEN}{SHADOW LIGHT_GREEN}Gholdengo joins'),
    gamble('One coin', 10, [('gold', -1), ('recruitspecies', 'GHOLDENGO')], 'It counts again. 999. It evolves on the spot and looks at you like you hung the moon.',
           [('gold', -1)], 'It counts again. 998. It recounts. 998. It does not give the coin back.'),
    LEAVE('Gimmighoul keeps counting. 998. 998. 998.')])
ev('snorlax', 'THE STAIRS ARE ASLEEP', 'SNORLAX',
   'A Snorlax is asleep across the stairs. It has been there since floor one. Some say the tower was built around it.',
   [opt('Feed it', [('loseitems',), ('recruitspecies', 'SNORLAX')], 'It eats everything your team was holding. Then it wakes up, satisfied, and follows the food source: you.'),
    opt('Nap with it', [('fullheal',), ('sleep', 100)], 'Best nap of your life. Your team is fully rested. A bit too rested, for the next battle.'),
    opt('Climb over', [('heal', -10)], 'It rolls over halfway. Nobody is hurt badly. Nobody talks about it.')])
ev('pseudo', 'A RARE SIGHT', 'PSEUDO',
   'A wild {STR_VAR_3} lands right in front of you. It looks at you. It looks at your team. It decides you will do.',
   [opt('Welcome it', [('recruitpseudo',)], 'Trainers search for years for one of these. You took the stairs.'),
    opt('Not today', [('bp', 3)], 'You let a {STR_VAR_3} go. Somewhere, every trainer you ever met sighs at once.')],
   weight=1)
ev('audino', 'A CHECK-UP', 'AUDINO',
   'An Audino listens to your team with its ears. It frowns. It has bad news, and a discount.',
   [opt('Treatment', [('gold', -60), ('maxhp', 6), ('heal', 20)], 'It fixes something you did not know was broken.'),
    opt('2nd opinion', [('heal', 10)], 'A different Audino says it is fine. You decide to believe that one.')])

# --- typen, soorten, items -------------------------------------------------------------------------
TYPES = {'NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL', 'FIRE', 'WATER',
         'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK', 'FAIRY'}
species_h = open(os.path.join(REPO, 'include/constants/species.h')).read()
items_h = open(os.path.join(REPO, 'include/constants/items.h')).read()
pool_h = open(os.path.join(REPO, 'src/data/spire_pool.h')).read()


def load_widths(name):
    src = open(os.path.join(REPO, 'src/fonts.c')).read()
    m = re.search(name + r'\[\]\s*=\s*\{(.*?)\};', src, re.S)
    widths = [int(x) for x in re.findall(r'\d+', re.sub(r'//.*', '', m.group(1)))]
    cm = {}
    for line in open(os.path.join(REPO, 'charmap.txt'), encoding='utf-8'):
        mm = re.match(r"^'(.+?)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if mm:
            ch = mm.group(1).replace("\\'", "'")
            code = int(mm.group(2), 16)
            if len(ch) == 1 and code < len(widths):
                cm.setdefault(ch, widths[code])
    return cm


WS = load_widths('gFontSmallNarrowLatinGlyphWidths')
WN = load_widths('gFontNormalLatinGlyphWidths')


def width(s, table=WS):
    w = 0
    for part in re.split(r'(\{[^}]*\})', s):
        if not part:
            continue
        if part.startswith('{'):
            w += VAR_W if part == '{STR_VAR_3}' else 0
        else:
            w += sum(table.get(ch, 6) for ch in part)
    return w


def wrap(text, limit=STORY_W):
    lines, cur = [], ''
    for word in text.split():
        t = (cur + ' ' + word) if cur else word
        if width(t) <= limit or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def species_name(s):
    return '-'.join(p.capitalize() for p in s.split('_'))

# --- effectregel -------------------------------------------------------------------------------------
GOOD, BAD, NEUTRAL, PLAIN = '{COLOR GREEN}{SHADOW LIGHT_GREEN}', '{COLOR RED}{SHADOW LIGHT_RED}', '{COLOR BLUE}{SHADOW LIGHT_BLUE}', '{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}'
RAR = ['Item', 'Good item', 'Rare item']
MOVE_RAR = ['Move', 'Uncommon move', 'Rare move']
APPENDS = {'forget', 'upgrade', 'evolve', 'wonder', 'sleep', 'loserelic', 'relic'}   # C voegt een regel toe
INTERACTIVE = {'item', 'give', 'teach', 'teachtype', 'teachmove', 'remove', 'recruit', 'recruitspecies', 'ditto', 'recruitpseudo'}


def fx_text(f):
    k = f[0]
    a = f[1] if len(f) > 1 else None
    if k == 'gold':
        return (GOOD if a > 0 else BAD) + ('+%d¥' % a if a > 0 else '%d¥' % a)
    if k == 'goldpct':
        return (GOOD + 'Double ¥') if a == 100 else (BAD + 'Lose all ¥') if a == -100 else (BAD + '%d%% ¥' % a)
    if k == 'heal':
        return GOOD + 'Heal %d%%' % a if a > 0 else BAD + '%d%% HP' % a
    if k == 'hurt1':
        return BAD + 'One: -%d%% HP' % a
    if k == 'maxhp':
        return (GOOD + '+%d%% max HP' % a) if a > 0 else (BAD + '%d%% max HP' % a)
    if k == 'bp':
        return GOOD + '+%d BP' % a
    if k == 'relic':
        return GOOD + 'Relic'
    if k == 'loserelic':
        return BAD + 'Lose a relic'
    if k == 'item':
        return GOOD + RAR[a]
    if k == 'give':
        return GOOD + f[2]
    if k == 'loseitems':
        return BAD + 'Lose items'
    if k in ('teach', 'teachtype'):
        return GOOD + MOVE_RAR[a]
    if k == 'teachmove':
        return GOOD + f[2]
    if k == 'upgrade':
        return GOOD + ('Upgrade' if a == 1 else '%d upgrades' % a)
    if k == 'forget':
        return BAD + ('Forget move' if a == 1 else 'Forget %d moves' % a)
    if k == 'remove':
        return GOOD + 'Remove a move'
    if k == 'fullheal':
        return GOOD + 'Full heal'
    if k == 'pp':
        return GOOD + 'All PP'
    if k == 'sleep':
        return BAD + ('Asleep' if a == 100 else '%d%% asleep' % a)
    if k == 'toxic':
        return BAD + 'Spikes x%d' % a
    if k == 'elite':
        return BAD + 'Elite fight'
    if k == 'recruit':
        return GOOD + '{STR_VAR_3} joins'
    if k == 'recruitspecies':
        return GOOD + '%s joins' % species_name(a)
    if k == 'ditto':
        return GOOD + 'Ditto joins'
    if k == 'recruitpseudo':
        return GOOD + '{STR_VAR_3} joins'
    if k == 'wonder':
        return NEUTRAL + 'Random trade'
    if k == 'evolve':
        return GOOD + 'Evolve one'
    if k == 'wheel':
        return NEUTRAL + 'Anything'
    raise ValueError(k)


def summary(o):
    if 'sum' in o:
        return o['sum'] if o['sum'].startswith('{') else GOOD + o['sum']
    if 'chance' in o:
        a = ', '.join(fx_text(f) for f in o['fx'] if f[0] != 'gold' or f[1] > 0) or (PLAIN + 'safe')
        b = ', '.join(fx_text(f) for f in o['fxb'] if f[0] != 'gold' or f[1] > 0) or (PLAIN + 'nothing')
        cost = [fx_text(f) + PLAIN + ', ' for f in o['fx'] if f[0] == 'gold' and f[1] < 0]
        if not o['fxb'] or all(f[0] == 'gold' and f[1] < 0 for f in o['fxb']):
            return ''.join(cost) + PLAIN + '%d%%: ' % o['chance'] + a
        return ''.join(cost) + PLAIN + '%d%%: ' % o['chance'] + a + PLAIN + ' / ' + b
    if not o['fx']:
        return PLAIN + 'Nothing'
    return (PLAIN + ', ').join(fx_text(f) for f in o['fx'])

# --- controle en uitvoer ---------------------------------------------------------------------------
FX_ENUM = {'gold': 'GOLD', 'goldpct': 'GOLD_PCT', 'heal': 'HEAL', 'hurt1': 'HURT_ONE', 'maxhp': 'MAXHP', 'bp': 'BP',
           'relic': 'RELIC', 'loserelic': 'LOSE_RELIC', 'item': 'ITEM', 'give': 'GIVE', 'loseitems': 'LOSE_ITEMS',
           'teach': 'TEACH', 'teachtype': 'TEACH_TYPE', 'teachmove': 'TEACH_MOVE', 'upgrade': 'UPGRADE', 'forget': 'FORGET',
           'remove': 'REMOVE', 'fullheal': 'FULLHEAL', 'pp': 'PP', 'sleep': 'SLEEP', 'toxic': 'TOXIC', 'elite': 'ELITE',
           'recruit': 'RECRUIT', 'recruitspecies': 'RECRUIT_SPECIES', 'ditto': 'DITTO', 'wonder': 'WONDER',
           'evolve': 'EVOLVE', 'wheel': 'WHEEL', 'recruitpseudo': 'RECRUIT_PSEUDO'}
errors = []


def check_outcome(ev_key, name, fx, text):
    lines = wrap(text) if text else []
    extra = sum((f[1] if f[0] == 'forget' else 1) for f in fx if f[0] in APPENDS)
    if f'{len(lines) + extra}' and len(lines) + extra > 4:
        errors.append(f'{ev_key}/{name}: uitkomst {len(lines)} regels + {extra} extra > 4: {lines}')
    inter = [f for f in fx if f[0] in INTERACTIVE]
    if len(inter) > 1 or (inter and any(f[0] == 'elite' for f in fx)):
        errors.append(f'{ev_key}/{name}: meer dan één keuze-effect')
    for f in fx:
        if f[0] not in FX_ENUM:
            errors.append(f'{ev_key}/{name}: onbekend effect {f[0]}')
        if f[0] == 'recruitspecies' and not re.search(r'\{SPECIES_%s,' % f[1], pool_h):
            errors.append(f'{ev_key}/{name}: {f[1]} staat niet in de rentalpool')
        if f[0] == 'give' and not re.search(r'#define ITEM_%s\b' % f[1], items_h):
            errors.append(f'{ev_key}/{name}: onbekend item {f[1]}')
    return lines


def always_open(o):
    """Kan deze optie altijd gekozen worden (geen geld, type, relic of item nodig)?"""
    fx = o['fx']
    return (not o['need'] and not any(f[0] == 'gold' and f[1] < 0 for f in fx)
            and not any(f[0] in ('loserelic', 'loseitems') for f in fx))


def c_str(s):
    # aanhalingstekens: “ en ” (een gewone " bestaat niet in de charmap)
    out, open_q = '', True
    for ch in s:
        if ch == '"':
            out += '“' if open_q else '”'
            open_q = not open_q
        else:
            out += ch
    return 'COMPOUND_STRING("' + out + '")'


def c_fx(fx):
    out = []
    for f in fx[:4]:
        k = f[0]
        a = f[1] if len(f) > 1 else 0
        if k == 'give':
            a = 'ITEM_' + a
        elif k == 'recruitspecies':
            a = 'SPECIES_' + a
        out.append('{SPIRE_FX_%s, %s}' % (FX_ENUM[k], a))
    return '{' + ', '.join(out) + '}' if out else '{{0}}'


rows = []
for e in E:
    if width(e['title'], WN) > TITLE_W:
        errors.append(f"{e['key']}: titel te breed ({width(e['title'], WN)} px)")
    story = wrap(e['story'])
    if len(story) > 4:
        errors.append(f"{e['key']}: verhaal {len(story)} regels: {story}")
    if not 1 <= len(e['options']) <= 3:
        errors.append(f"{e['key']}: {len(e['options'])} opties")
    if e['icon'] and e['icon'] not in ('RECRUIT', 'PSEUDO') and not re.search(r'#define SPECIES_%s\b' % e['icon'], species_h):
        errors.append(f"{e['key']}: onbekende soort {e['icon']}")
    opts = []
    for o in e['options']:
        if width(o['name']) > NAME_W:
            errors.append(f"{e['key']}/{o['name']}: naam te breed ({width(o['name'])} px)")
        if o['need'] and o['need'] not in TYPES:
            errors.append(f"{e['key']}/{o['name']}: onbekend type {o['need']}")
        s = summary(o)
        if width(s) > SUM_W:
            errors.append(f"{e['key']}/{o['name']}: effectregel te breed ({width(s)} px): {re.sub(r'{[^}]*}', '', s)}")
        if len(o['fx']) > 4 or len(o.get('fxb', [])) > 4:
            errors.append(f"{e['key']}/{o['name']}: meer dan 4 effecten")
        ra = check_outcome(e['key'], o['name'], o['fx'], o['result'])
        rb = check_outcome(e['key'], o['name'], o.get('fxb', []), o.get('resultb', ''))
        if any(f[0] == 'recruit' for f in o['fx'] + o.get('fxb', [])) and '{STR_VAR_3}' not in e['story'] + o['result'] and 'sum' not in o:
            pass
        opts.append('        {%s, %s, %s, %s, %d, %s, %s, %s, %s},' % (
            c_str(o['name']), c_str(s), ('TYPE_' + o['need']) if o['need'] else 'TYPE_NONE',
            'TRUE' if any(f[0] == 'gold' and f[1] < 0 for f in o['fx']) else 'FALSE',
            o.get('chance', 100), c_fx(o['fx']), c_fx(o.get('fxb', [])),
            c_str('\\n'.join(ra)), c_str('\\n'.join(rb)) if rb else 'NULL'))
    # nooit vastlopen: zonder geld of het juiste type moet er altijd iets te kiezen zijn (of B = weglopen)
    if not any(always_open(o) for o in e['options']) and not e['walk']:
        errors.append(f"{e['key']}: alle opties kunnen dicht zitten (geld/type/relic/item) en er is geen walk-tekst (B = weglopen)")
    walk = 'NULL'
    if e['walk']:
        if len(story) > 3:
            errors.append(f"{e['key']}: verhaal {len(story)} regels; met B = weglopen max. 3 (de vierde regel is 'B: walk away')")
        wl = check_outcome(e['key'], 'B', [], e['walk'])
        walk = c_str('\\n'.join(wl))
    acts = sum(1 << (a - 1) for a in e['acts'])
    rows.append('    {%s, %s, %s, %d, %d, %d, {\n%s\n    }, %s},' % (
        c_str(e['title']), c_str('\\n'.join(story)), 'SPIRE_EVENT_ICON_RECRUIT' if e['icon'] == 'RECRUIT' else 'SPIRE_EVENT_ICON_PSEUDO' if e['icon'] == 'PSEUDO' else ('SPECIES_' + e['icon']) if e['icon'] else 'SPECIES_NONE',
        acts, e['weight'], len(e['options']), '\n'.join(opts), walk))

if errors:
    print('\n'.join(errors))
    sys.exit(1)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('// Gegenereerd door tools/grounded/spire/events.py; niet met de hand bewerken.\n')
    f.write('// {titel, verhaal, icoon, acts (bitmasker), gewicht, aantal opties, {naam, effectregel, type-eis, kost geld,\n')
    f.write('//  kans (%), effecten, effecten bij mislukken, uitkomst, uitkomst bij mislukken}, B = weglopen (tekst of NULL)}\n\n')
    f.write('static const struct SpireEventData sSpireEvents[] =\n{\n')
    f.write('\n'.join(rows))
    f.write('\n};\n')
print(f'{len(E)} events -> {os.path.relpath(OUT, REPO)}')
