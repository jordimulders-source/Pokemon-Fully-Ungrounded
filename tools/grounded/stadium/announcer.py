#!/usr/bin/env python3
"""Battle Stadium (Project Grounded): de omroeper in de arena.

Volgorde (één tekstvak per zin): bij het eerste gevecht een welkom, dan elke ronde de rondenaam;
bij het eerste gevecht ook de speler (zin op basis van hoe je gespeeld hebt, anders de vanilla-zin) en in
doubles de compagnon; daarna de tegenstander(s) om beurten (doubles: allebei).

Bewerk de teksten hier (platte tekst; het script breekt af op de breedte van het tekstvak met dezelfde
regels als tools/dialogen/import.py) en draai opnieuw. Max. 2 regels = één tekstvak.

Genereert:
- src/data/stadium_announcer.h (tabel trainer -> tekst, plus een algemene tekst als terugval)
- STADIUM_OMROEPER.md (overzicht voor Jordi)

{PLAYER} = spelernaam, {STR_VAR_1} = naam van de compagnon of de legendary (gemeten als lange naam).
Nieuwe personages in de pool (pool.py POOL): hier ook een regel toevoegen; het script waarschuwt.
Gebruik: python3 tools/grounded/stadium/announcer.py
"""
import importlib.util, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location('dialogen_import', os.path.join(ROOT, 'tools/dialogen/import.py'))
dimp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dimp)

OUT_H = os.path.join(ROOT, 'src/data/stadium_announcer.h')
OUT_MD = os.path.join(ROOT, 'STADIUM_OMROEPER.md')

# Welkom (alleen het eerste gevecht van een toernooi)
WELCOME = {
    'SINGLES': "Welcome to the BATTLE STADIUM! 32 trainers, one trophy, zero refunds.",
    'DOUBLES': "Welcome to STADIUM DOUBLES! Sixteen teams, twice the property damage.",
}
# Rondenaam (elke ronde): ronde van 32, 16, kwartfinale, halve finale, finale
ROUNDS = [
    "ROUND OF 32! Half of you go home today. The parking lot is already cheering.",
    "ROUND OF 16! The hot dog stand has outlasted half the field already.",
    "QUARTERFINALS! Eight left. The crowd has learned two of their names.",
    "The SEMIFINALS! Four left. Somebody's grandma just woke up for this.",
    "The FINAL! One match, one trophy, and one very nervous janitor.",
]
# De speler (eerste gevecht). De C-code (src/stadium.c, AnnouncePlayer) verzamelt de zinnen waarvan de voorwaarde
# klopt en kiest er willekeurig één, gewogen: hoe specifieker, hoe groter de kans (gewicht 1 = algemeen,
# 3 = opvallend, 6 = 'we weten wat je deed', à la Grey Fox in MGS). Klopt er geen, dan VANILLA.
# Per zin: (gewicht, voorwaarde voor STADIUM_OMROEPER.md, tekst). Een lege regel = een tweede tekstvak.
# {STR_VAR_1} = soort/type/legendary (gemeten als lange naam), {STR_VAR_2} = een getal (gemeten als 7 cijfers).
# Nieuwe tellers (game stats 53-56, src/overworld.c): white-outs, gevlucht, vrijgelaten, eigen flauwgevallen.
PLAYER = {
    # --- Jordi's voorbeelden ---
    'WHITE_OUTS': (6, 'white-outs >= 15 (gewone run ±5-10)',
                   "{PLAYER}! This trainer loses more than they win.\n\nSo let's all pretend this time is gonna be different."),
    'LEAGUE_BULLY': (6, 'Hall of Fame >= 10 keer',
                     "{PLAYER}! {STR_VAR_2} wins at the POKéMON LEAGUE.\n\nA trainer who likes to fight the same people over and over again. Bully!"),
    'FAN': (6, '>= 5 van dezelfde soort in team + pc',
            "{PLAYER} owns {STR_VAR_2} {STR_VAR_1}!\n\nThat's not a team. That's a fan club with a membership fee."),
    # --- het Stadium-team zelf ---
    'MAGIKARP': (6, 'een MAGIKARP in het Stadium-team',
                 "{PLAYER} entered a MAGIKARP. In a tournament. On purpose.\n\nBold strategy. Or a cry for help."),
    'MONOTYPE': (6, 'het hele Stadium-team deelt een type',
                 "{PLAYER} brought only {STR_VAR_1} types.\n\nA theme team! Subtle. Like a brass band."),
    # --- 'we weten wat je deed' ---
    'IMPLOSION': (6, 'ooit IMPLOSION gebruikt',
                  "{PLAYER} once used IMPLOSION. A black hole. Indoors.\n\nOur insurance went up 400 percent."),
    'TRASH_SPIRITOMB': (6, 'Spiritomb uit de prullenbak van het Abandoned Ship',
                        "{PLAYER} caught a SPIRITOMB in a trash can. We don't judge. The trash can does."),
    'HOOPA_SNACK': (6, 'Hoopa-wens: een snack',
                    "{PLAYER} met a genie and wished for a snack.\n\nA grandma in LAVARIDGE is short one batch of cookies."),
    'HOOPA_FAME': (6, 'Hoopa-wens: roem',
                   "{PLAYER} wished for fame and got GABBY's. Remember GABBY? No? Exactly."),
    'HOOPA_RICHES': (6, 'Hoopa-wens: rijkdom',
                     "{PLAYER} wished for riches. Somewhere, a RICH BOY's piggy bank is empty. Boo!"),
    'HOOPA_POWER': (6, 'Hoopa-wens: kracht',
                    "{PLAYER} wished for power and got a CHOICE BAND.\n\nBRAWLY lost his headband that day. Funny, that."),
    'BURGLAR': (6, 'Burglar (SIMON) >= 5 keer verslagen',
                "{PLAYER} has beaten SIMON the BURGLAR {STR_VAR_2} times.\n\nHe keeps coming back. Lock your doors."),
    'BIRCH': (6, '>= 5 Birch-gevechten gewonnen',
              "{PLAYER} has beaten PROF. BIRCH and his... samples.\n\nMany times. We washed the trophy twice."),
    'DAVE': (6, 'alle vier Dave-gevechten gewonnen',
             "{PLAYER} beat DAVE four times.\n\nDAVE says it doesn't count. He says you were offside."),
    'COMMUNITY_SERVICE': (6, 'Archie of Maxie verslagen tijdens hun werkstraf',
                          "{PLAYER} battled ARCHIE and MAXIE during their community service.\n\nThey were holding mops. Cold."),
    'SHINY_RAYQUAZA': (6, 'shiny Rayquaza gevangen',
                       "{PLAYER} caught a black RAYQUAZA.\n\nAn ancient sky god. Now a pocket accessory."),
    'RELEASED': (6, '>= 30 Pokémon vrijgelaten',
                 "{PLAYER} released {STR_VAR_2} POKéMON.\n\nThey live on a farm now. A lovely farm. Don't ask."),
    'FAINTED': (6, '>= 200 keer een eigen Pokémon flauwgevallen',
                "{PLAYER}'s POKéMON have fainted {STR_VAR_2} times.\n\nThe POKéMON CENTER sends a fruit basket every Christmas."),
    'FLED': (6, '>= 50 keer gevlucht',
             "{PLAYER} has run from {STR_VAR_2} battles. Great cardio.\n\nTonight, the exit is locked."),
    'SPLASH': (6, '>= 10 keer SPLASH gebruikt',
               "{PLAYER} has used SPLASH {STR_VAR_2} times. Nothing happened. Every. Single. Time."),
    'STRUGGLE': (6, '>= 10 keer STRUGGLE',
                 "{PLAYER}'s POKéMON have used STRUGGLE {STR_VAR_2} times. PP? Never heard of her."),
    # --- opvallende statistieken ---
    'STEPS': (3, '>= 100.000 stappen',
              "{PLAYER} has walked {STR_VAR_2} steps. The shoes have filed a complaint."),
    'EGGS': (3, '>= 50 eieren uitgebroed',
             "{PLAYER} has hatched {STR_VAR_2} eggs.\n\nSomewhere, a very tired DITTO needs a vacation."),
    'FISHING': (3, '>= 200 keer gevist',
                "{PLAYER} has gone fishing {STR_VAR_2} times. IVAN calls that a warm-up."),
    'SAVES': (3, '>= 500 keer opgeslagen',
              "{PLAYER} has saved the game {STR_VAR_2} times. Trust issues?\n\nRelax. This match can't be undone."),
    'POKECENTER': (3, '>= 300 keer in een Pokémon Center',
                   "{PLAYER} has visited a POKéMON CENTER {STR_VAR_2} times.\n\nThe nurse has a punch card with your face on it."),
    'SHINIES': (3, '>= 3 shiny Pokémon in team + pc',
                "{PLAYER} owns {STR_VAR_2} shiny POKéMON. Wrong colors, right attitude."),
    'LEDGES': (3, '>= 300 keer van een richel gesprongen',
               "{PLAYER} has jumped off {STR_VAR_2} ledges. Never once climbed back up. Committed."),
    'JACKPOT': (3, 'jackpot in de Game Corner',
                "{PLAYER} hit a jackpot at the GAME CORNER.\n\nThe casino knows. The casino remembers."),
    'RICH': (3, '>= 500.000 geld',
             "{PLAYER} has half a million in the bank.\n\nTonight's prize money goes to the janitor."),
    'BROKE': (3, '< 1.000 geld (met minstens 1 badge)',
              "{PLAYER} is broke. Like, really broke. Win this one. The hot dogs aren't free."),
    'LEGENDARY': (3, 'een legendary gevangen',
                  "{PLAYER} owns a {STR_VAR_1}! A legend. In a ball. In a pocket. Sure."),
    'BIG_DEX': (3, '>= 200 soorten gevangen',
                "{PLAYER} caught over 200 POKéMON. The PC storage union is on strike."),
    'PLAYTIME': (3, '>= 100 uur speeltijd',
                 "{PLAYER}! Over a hundred hours on the clock. Go outside. After this match."),
    # --- algemeen ---
    'TITLES': (1, 'een Stadium-titel', "Defending the trophy: {PLAYER}! The trophy remembers you. It's scared."),
    'VETERAN': (1, '>= 20 Stadium-wedstrijden gewonnen',
                "{PLAYER}! Twenty-plus wins here. The floor knows your footprints by heart."),
    'RETURNING': (1, '>= 2 toernooien, geen titel',
                  "{PLAYER} is back! Last time didn't go great. Don't worry, we kept the footage."),
    'NEWCOMER': (1, 'eerste toernooi', "A fresh face: {PLAYER}! First time here. The medics are on standby. Just in case."),
    'HALL_OF_FAME': (1, 'kampioen (Hall of Fame)',
                     "The CHAMPION of HOENN: {PLAYER}! Yes, the real one. STEVEN is still in therapy."),
    'EIGHT_BADGES': (1, '8 badges, nog geen kampioen',
                     "{PLAYER}! Eight BADGES, no ELITE FOUR win. Ambition: high. Results: pending."),
    'TREECKO': (1, 'starter Treecko', "{PLAYER} picked TREECKO. The cool one. That's what everybody says."),
    'TORCHIC': (1, 'starter Torchic', "{PLAYER} picked TORCHIC. A chicken that learns to kick. Respect."),
    'MUDKIP': (1, 'starter Mudkip', "{PLAYER} picked MUDKIP. Of course. The internet told you to."),
}
VANILLA = "In the blue corner: {PLAYER}! A trainer. With POKéMON. That's all it says here."
# De compagnon (doubles, eerste gevecht), Jordi: "de compagnon moet hun typische tekst krijgen". Volgorde:
# 1. een eigen compagnonzin hieronder (partnernaam uit pool.py), 2. de omroepzin van de bron-trainer (LINES),
# 3. pas als terugval een algemene zin uit PARTNER.
COMPANION = {
    'BRENDAN': "Teaming up with {PLAYER}: BRENDAN! Your rival.\n\nHe wants a rematch. After this match. Obviously.",
    'MAY': "Teaming up with {PLAYER}: MAY! She keeps score of your rivalry. She is \"ahead\".",
    'KECCLES': "And next to {PLAYER}... KECCLES! Probably. He could be anywhere.\n\nA KECLEON with a PhD and an existential crisis. Same thing, really.",
    'WALLY': "With {PLAYER}: WALLY! The sick kid from PETALBURG got better.\n\nMuch better. Worryingly better.",
    'MASCOTS': "With {PLAYER}: the MASCOTS!\n\nOn the lunchbox, on the plushie, and now on the battlefield.",
    'STARTERS': "With {PLAYER}: the KANTO STARTERS! Fully evolved.\n\nStill holding a grudge about the lab.",
    'FOSSILS': "With {PLAYER}: the FOSSILS! Millions of years old.\n\nStill faster than the WiFi in here.",
    'EEVEES': "With {PLAYER}: the EEVEE family!\n\nThree cousins, one family reunion, zero agreement.",
    'LAKE': "With {PLAYER}: the LAKE TRIO!\n\nKnowledge, emotion and willpower. You bring the snacks.",
    'REGIS': "With {PLAYER}: the REGIS! They speak only in beeps. Our translator quit.",
    'BIRDS': "With {PLAYER}: the LEGENDARY BIRDS! Please do not feed them.\n\nThey bite. And freeze. And zap.",
    'BEASTS': "With {PLAYER}: the LEGENDARY BEASTS!\n\nThey roamed half of HOENN to get here. Took the bus the last bit.",
    'PSEUDOS': "With {PLAYER}: three PSEUDO-LEGENDARIES!\n\n600 base stats each. The other trainers want a word.",
    'SWORDS': "With {PLAYER}: the SWORDS OF JUSTICE!\n\nThey're here to judge. Mostly the referee.",
    'LOYAL': "With {PLAYER}: the LOYAL THREE! Loyal to {PLAYER}. Today. Read the contract.",
    'TAPUS': "With {PLAYER}: the TAPUS! Island guardians.\n\nVery protective. Of the snack table.",
    'GENIES': "With {PLAYER}: the FORCES OF NATURE! Weather forecast: yes.",
    'ULTRAS': "With {PLAYER}: the ULTRA BEASTS! From another dimension.\n\nTheir visas are pending.",
    'RUIN': "With {PLAYER}: the TREASURES OF RUIN! Four were sealed.\n\nThree showed up. Nobody asks about the fourth.",
    'WEATHER': "With {PLAYER}: the WEATHER TRIO!\n\nRain, sun, and a sky dragon that hates both. Bring a coat.",
    'SELENE': "With {PLAYER}: SELENE! She calls you “the chosen one”.\n\nShe also calls her kettle that.",
    'REGINALD': "With {PLAYER}: REGINALD! He left his cave for this.\n\nHe wants it on record that he hates it.",
    'HELIA': "With {PLAYER}: HELIA! She brought sunscreen. For her BRONZONG.\n\nNot for you. Never for you.",
    'CREATORS': "With {PLAYER}: the CREATORS! Time, space and antimatter. The janitor gave up.",
}
# Terugval voor de compagnon (willekeurig)
PARTNER = [
    "At {PLAYER}'s side: {STR_VAR_1}! Friends? Their lawyers say partners.",
    "With {PLAYER}: {STR_VAR_1}! They met five minutes ago. Chemistry!",
    "{PLAYER}'s partner: {STR_VAR_1}! Paid in exposure and one free hot dog.",
    "Covering {PLAYER}: {STR_VAR_1}! Or standing nearby. Close enough.",
]

FALLBACK = "And the next challenger! We were told to say something funny here. We forgot."

LINES = {
    # Hoenn-gymleiders
    'ROXANNE_5': "ROXANNE! You don't have to put on the red light. She brought rocks instead.",
    'BRAWLY_5': "BRAWLY! Trains six days a week. Five days a week, three days a week.",
    'WATTSON_5': "WATTSON! He isn't here to battle. He's mining crypto on the arena's power grid.",
    'FLANNERY_5': "FLANNERY! She forgot her catchphrase again. Something about embers?",
    'NORMAN_5': "NORMAN paused his series for this. Make it quick, he's on a cliffhanger.",
    'WINONA_5': "WINONA landed twenty minutes ago and is still looking for suitcase number 36.",
    'TATE_AND_LIZA_5': "TATE & LIZA! Two bodies, one soul, zero spoons. Lawyers in row one.",
    'WALLACE_5': "WALLACE! Contest star, GYM LEADER, and the reason HOENN ran out of glitter.",
    # Elite Four en kampioenen
    'SIDNEY': "SIDNEY of the ELITE FOUR! Everyone at home has money on him. Bet responsibly.",
    'PHOEBE': "PHOEBE! Her ghosts are already complaining about the hot dogs in here.",
    'GLACIA': "GLACIA! An ice master who moved to a tropical region. On purpose. Twice.",
    'DRAKE': "DRAKE, the DRAGON master! Not that one. Do NOT play the Kendrick song.",
    'JUAN': "JUAN! He taught WALLACE everything. Then WALLACE took his gym. Awkward.",
    'STEVEN': "STEVEN STONE! HE'S MADE OF METAL! HIS CIRCUITS GLEAM! His wallet too.",
    # verhaal
    'WALLY_VR_5': "WALLY! He once needed help catching a RALTS. Now he owns a FLUTTER MANE.",
    'ARCHIE_SOOTOPOLIS': "ARCHIE of AQUA SPARKLING WATER! Our official hydration sponsor!",
    'MAXIE_SOOTOPOLIS': "MAXIE of MAGMA HOT SAUCE! Spiciest man in HOENN. Pale fans, cover your lips.",
    'BIRCH_UNDERWATER': "Cue the Macarena! PROF. BIRCH and his... samples. Don't touch them.",
    'KECCLES_3': "KECCLES! A KECLEON with a PhD and existential dread. Is he here?",
    'COLRESS_MAGMA': "COLRESS! He'll analyze your team. And everything wrong with MAUVILLE.",
    'ZINNIA': "ZINNIA, the LOREKEEPER! She'll explain the lore. All of it. Mid-battle.",
    'MIMI': "MIMI! Yes, she's a MIMIKYU. No, nobody knows who signed her up. ...pika...",
    'GABBY_AND_TY_6': "GABBY & TY! Breaking news... right after... these... very... long... pauses.",
    'STADIUM_JOEY': "Youngster JOEY! His POOCHYENA is in the top percentage of the top percentage!",
    'STADIUM_WINSTON': "WINSTON! His whole team is shiny. He paid for it. Mo money, mo problems.",
    'STADIUM_MUSTARD': "Mustard on the beat, ho! The dojo master himself... MUSTAAAAAAAAAARD!",
    # Aqua- en Magma-admins
    'MATT': "MATT! He brought a WAILORD and a SNORLAX. The floor filed a complaint.",
    'SHELLY_SEAFLOOR_CAVERN': "AQUA ADMIN SHELLY! She's mainly here to sell you a crate of sparkling water.",
    'TABITHA_MOSSDEEP': "TABITHA! MAXIE's loyal right hand. The left one is holding the hot sauce.",
    # Kanto
    'STADIUM_BROCK': "BROCK of PEWTER CITY! Rocks, fossils, and his eyes are open. We think.",
    'STADIUM_MISTY': "MISTY! She still wants her bike back. It's been almost thirty years, kid.",
    'STADIUM_LT_SURGE': "LT. SURGE! He'll shock you. Then tell you war stories nobody asked for.",
    'STADIUM_ERIKA': "ERIKA! She may doze off mid-battle. Don't wake her. It's called self-care.",
    'STADIUM_KOGA': "KOGA, the ninja master! He's already here. He's been here for an hour.",
    'STADIUM_SABRINA': "SABRINA! She already knows how this match ends. She's not telling.",
    'STADIUM_BLAINE': "BLAINE! He'll quiz you between turns. Wrong answers get burned.",
    'STADIUM_GIOVANNI': "GIOVANNI! A perfectly legitimate businessman. No rockets. None.",
    'STADIUM_LORELEI': "LORELEI! The coldest welcome in KANTO. GLACIA says she copied her.",
    'STADIUM_BRUNO': "BRUNO! He trained with boulders for twenty years. The boulders quit.",
    'STADIUM_AGATHA': "AGATHA! She thinks OAK went soft. She's here to prove she didn't.",
    'STADIUM_LANCE': "LANCE! Cape, DRAGONITE, and a history of using HYPER BEAM on people.",
    'STADIUM_BLUE': "BLUE, the CHAMPION! Historically for about five minutes. Smell ya later!",
    'STADIUM_RED': "RED! He came down from MT. SILVER for this. He has said nothing. Ever.",
    'STADIUM_OAK': "PROF. OAK! He still can't remember if you're a boy or a girl.",
    # Sinnoh
    'STADIUM_ROARK': "ROARK! Coal miner, fossil nerd. The helmet stays on. Indoors too.",
    'STADIUM_GARDENIA': "GARDENIA! She loves GRASS POKéMON. Ask her about the chateau and she leaves.",
    'STADIUM_MAYLENE': "MAYLENE! She fights barefoot. On this floor. After GRIMER's match. Brave.",
    'STADIUM_WAKE': "CRASHER WAKE! A luchador with a GYARADOS. The mask stays on. Always.",
    'STADIUM_FANTINA': "FANTINA! Contest queen, dance teacher, ghost lady. Mostly ghost lady.",
    'STADIUM_BYRON': "BYRON! ROARK's dad. Steel, fossils, and strong opinions about both.",
    'STADIUM_CANDICE': "CANDICE! She goes all out! In a skirt! In the snow! Every single day!",
    'STADIUM_VOLKNER': "VOLKNER! He got bored and blacked out his whole city. Welcome back!",
    'STADIUM_AARON': "AARON of the ELITE FOUR! Bugs only. Except DRAPION. Do not ask.",
    'STADIUM_BERTHA': "BERTHA! Sweet old granny with an EARTHQUAKE. Ground rules apply.",
    'STADIUM_FLINT': "FLINT! His hair is on fire. That's not a style. Someone get a bucket.",
    'STADIUM_LUCIAN': "LUCIAN! He brought a book. He'll finish a chapter between your turns.",
    'STADIUM_CYNTHIA': "CYNTHIA! Her GARCHOMP has a fan club, a lawyer and a skincare line.",
    'STADIUM_CYRUS': "CYRUS of TEAM GALACTIC! He wants a world without spirit. Tough crowd.",
    'STADIUM_BARRY': "BARRY! He's late! No, early! He'll fine you ten million either way!",
    'STADIUM_MARS': "Commander MARS! She's here for your POKéMON. And maybe an autograph.",
    'STADIUM_JUPITER': "Commander JUPITER! Purple hair, poison team, zero chill.",
    'STADIUM_SATURN': "Commander SATURN! The sensible one. He'd rather be literally anywhere else.",
    # Frontier Brains
    'STADIUM_PALMER': "TOWER TYCOON PALMER! Pure dad energy. He brought HEATRAN to the barbecue.",
    'STADIUM_THORTON': "THORTON! He has a spreadsheet of your team. You're row 47. It's not pretty.",
    'STADIUM_ARGENTA': "HALL MATRON ARGENTA! She's seen 30 years of trainers. You're not special.",
    'STADIUM_DAHLIA': "ARCADE STAR DAHLIA! Her moves are picked by roulette. So is your fate.",
    'STADIUM_RILEY': "RILEY! He reads auras. He knew about this match before the bracket did.",
    'STADIUM_ANABEL': "SALON MAIDEN ANABEL! She brought legendaries to a level 50 tournament.",
    'STADIUM_TUCKER': "DOME ACE TUCKER! He loves the crowd more than the crowd loves him.",
    'STADIUM_SPENSER': "PALACE MAVEN SPENSER! His POKéMON don't listen to him either. Relatable.",
    'STADIUM_GRETA': "ARENA TYCOON GRETA! She has a SHEDINJA. One hit. Good luck with that.",
    'STADIUM_NOLAND': "FACTORY HEAD NOLAND! He'll borrow your POKéMON. He won't give them back.",
    'STADIUM_LUCY': "PIKE QUEEN LUCY! She hasn't smiled since 2004. Neither has her SEVIPER.",
    'STADIUM_BRANDON': "PYRAMID KING BRANDON! He brought all three REGIS. They didn't ask to come.",
    # Unova
    'STADIUM_N': "N, the KING of TEAM PLASMA! He wants to free your POKéMON. Ticket refunds: no.",
    'STADIUM_GHETSIS': "GHETSIS! He'd like everyone to sit down. Yes, you too. Especially you.",
    # Team Rocket (Rocket-hideout, Project Grounded)
    'STADIUM_PETREL': "ROCKET EXEC PETREL! Or GIOVANNI. Or a DITTO. Nobody checked his ID.",
    # Neo Team Plasma (Black 2/White 2)
    'STADIUM_ZINZOLIN': "SAGE ZINZOLIN! He froze a whole city. Then himself. Do not lick him.",
    'STADIUM_ROOD': "SAGE ROOD! Ex-villain, current grandpa. His POKéMON heal. His knees don't.",
    'STADIUM_SHADOW_TRIAD': "THE SHADOW TRIAD! Three ninjas, one ticket. Security is still looking.",
    'STADIUM_PLASMA_GRUNT_M': "A NEO PLASMA GRUNT! Nobody knows his name. Including him.",
    'STADIUM_PLASMA_GRUNT_F': "A NEO PLASMA GRUNT! She joined for the dental plan. There is no dental plan.",
    # Jordi en zijn maten
    'DAVE': "From VICTORY ROAD: DAVE is on fire! Your defense is terrified!",
    'MITCH': "MITCH! He has stage fright. Thousands of fans. Everybody, stare at him!",
    'SICKBLIK': "SICKBLIK! He made this romhack. Beat him and he nerfs you next patch.",
    # gasten
    'STADIUM_WARIO': "WARIO! Here for the prize money and the free buffet. Mostly the buffet.",
    'STADIUM_YOSHI': "YOSHI! Please be gentle, he cries. We have tissues on standby.",
    'STADIUM_GOLBAT': "GOLBAT! From every cave of your childhood. REPEL does not work in here.",
    'STADIUM_GRIMER': "GRIMER! Here since 1996. So is the smell. Front rows, we apologize.",
    'STADIUM_BOO': "BOO! Don't look at him. Seriously, look away. It's in the rules.",
    'STADIUM_MEW': "MEW! Found under a truck in LILYCOVE. The rumors were true all along!",
    'STADIUM_SHY_GUY_RED': "SHY GUY! He asked us not to announce him. Sorry, buddy.",
    'STADIUM_SHY_GUY_GREEN': "SHYER GUY! Even shyer than SHY GUY. He's under the bleachers. Somewhere.",
    'STADIUM_SHY_GUY_PINK': "FLY GUY! He refuses to land. The referee has given up.",
    'STADIUM_SHY_GUY_BLACK': "SHADY GUY! Everybody check your pockets. Now check them again.",
    'STADIUM_BURGLAR': "SIMON the BURGLAR! Straight out of 1996. Mind your wallet. And the trophy.",
    'STADIUM_DITTO': "DITTO! He asked me to read his statement. Ahem. “...” “:)”",
    # meme-trainers
    'STADIUM_DONALD': "DONALD the BUG MANIAC! Six BUG POKéMON, he says. They are all DITTO.",
    'STADIUM_IVAN': "IVAN the FISHERMAN! Very rare fishies. His MAGIKARP knows HYDRO PUMP.",
    'STADIUM_JOHNSON': "JOHNSON! Tik tok, tik tok. Nobody knows what happens next. Not even him.",
    'STADIUM_LYLE': "LYLE! His brother's bugs, finally trained! IVs: still zero. Heart: maxed.",
    # post-game
    'PLASMA_NIGEL': "NIGEL, NEO PLASMA's Head of Logistics! He signed for a GENESECT.",
    'VICTORY_V': "V! Only POKéMON with a V! VOLCARONA! VIKAVOLT! VICTORY? We'll see.",
    'GRIMSBY': "CAPTAIN GRIMSBY! Dead since 1802, still clocks in. Union rules.",
    'LAVIS': "LAVIS! Thirty-one years painting one lake. Today: you, small, in the corner.",
    'TALLOW': "TALLOW! Lighthouse keeper, 1952 to 1953. Mostly 1953. Mostly dead.",
    'WICK': "WICK! Forty years a lighthouse keeper. His lamp is a fish. It works.",
    'SALIM': "SALIM of the MIRAGE BAZAAR! Everything for sale, nothing his!",
    'DRACONID_ELDER': "SELENE, DRACONID ELDER! Waited 300 years for a sky dragon. You'll do.",
    'VR_REGINALD': "REGINALD, the VICTORY ROAD HERMIT! Last saw daylight in 1987. Didn't like it.",
    'SLAB_HELIA': "HELIA of the SCORCHED SLAB! Worships the sun. The sun has not replied.",
    # rivalen
    'BRENDAN_ROUTE_136_TREECKO': "BRENDAN! Your rival. Still salty about which starter you picked.",
    'MAY_ROUTE_136_TORCHIC': "MAY! Your rival. She swears she's better at this than you. Prove it.",
}


LONG_NAME = '\u2603' * 12    # {STR_VAR_1}: meten als een lange naam (TATE & LIZA, REGIGIGAS; ±72 px)
NUMBER = '\u2604' * 7       # {STR_VAR_2}: meten als een getal van 7 cijfers (stappen)


def wrap(text, boxes=1):
    """Max. 2 regels per tekstvak, max. `boxes` tekstvakken (een lege regel in de tekst = nieuw tekstvak)."""
    t = text.replace('{STR_VAR_1}', LONG_NAME).replace('{STR_VAR_2}', NUMBER)
    layout = dimp.layout(dimp.curly_quotes(t))
    if len(layout) > boxes or any(len(b) > 2 for b in layout):
        sys.exit(f'Te lang ({[len(b) for b in layout]} regels per tekstvak): {text}')
    lines = [x.replace(LONG_NAME, '{STR_VAR_1}').replace(NUMBER, '{STR_VAR_2}') for x in dimp.to_strings(t)]
    return ''.join(lines).rstrip('$')


def c_list(name, texts, boxes=1):
    return [f'static const u8 *const {name}[] =', '{'] + [f'    COMPOUND_STRING("{wrap(t, boxes)}"),' for t in texts] + ['};', '']


def main():
    src = open(os.path.join(ROOT, 'tools/grounded/stadium/pool.py')).read()
    pool = eval(re.search(r'POOL = (\[.*?\n\])', src, re.S).group(1))
    rivals = eval(re.search(r'RIVALS = (\{.*?\})', src).group(1))
    for t in pool + list(rivals):
        if t not in LINES:
            print(f'Waarschuwing: geen omroeptekst voor {t} (algemene tekst)')

    out = ['// Gegenereerd door tools/grounded/stadium/announcer.py; niet met de hand bewerken.',
           '// De omroeper in de arena (één tekstvak per zin): welkom, ronde, speler en compagnon, tegenstanders.',
           '', 'struct StadiumAnnouncerLine', '{', '    u16 trainerId;', '    const u8 *text;', '};', '',
           f'static const u8 sStadiumAnnouncerFallback[] = _("{wrap(FALLBACK)}");', '',
           f'static const u8 sStadiumAnnouncerVanilla[] = _("{wrap(VANILLA)}");', '']
    out += c_list('sStadiumAnnouncerWelcome', [WELCOME['SINGLES'], WELCOME['DOUBLES']])
    out += c_list('sStadiumAnnouncerRounds', ROUNDS)
    out += ['enum StadiumAnnouncePlayer', '{'] + [f'    ANNOUNCE_PLAYER_{k},' for k in PLAYER] + ['    ANNOUNCE_PLAYER_COUNT', '};', '']
    out += c_list('sStadiumAnnouncerPlayer', [v[2] for v in PLAYER.values()], boxes=2)
    out += ['static const u8 sStadiumAnnouncerPlayerWeight[] =', '{'] + [f'    {v[0]},' for v in PLAYER.values()] + ['};', '']
    out += c_list('sStadiumAnnouncerPartner', PARTNER)
    out += ['struct StadiumAnnouncerCompanion', '{', '    u16 partnerId;', '    const u8 *text;', '};', '',
            'static const struct StadiumAnnouncerCompanion sStadiumAnnouncerCompanion[] =', '{']
    out += [f'    {{PARTNER_STADIUM_{k}, COMPOUND_STRING("{wrap(v, 2)}")}},' for k, v in COMPANION.items()] + ['};', '']
    out += [
           'static const struct StadiumAnnouncerLine sStadiumAnnouncerLines[] =', '{']
    md = ['# Battle Stadium: de omroeper', '',
          'Vóór elke wedstrijd in de arena: bij het eerste gevecht een welkom, elke ronde de rondenaam, bij het eerste',
          'gevecht de speler (en in doubles de compagnon), dan de tegenstander(s) om beurten.',
          'Bewerken: `tools/grounded/stadium/announcer.py`, daarna het script draaien.', '',
          '## Welkom en rondes', ''] + [f'- {t}' for t in list(WELCOME.values()) + ROUNDS] + [
          '', '## De speler (willekeurig uit wat klopt, gewogen: 6 = specifiek, 3 = opvallend, 1 = algemeen)', '',
          '| Sleutel | Gewicht | Voorwaarde | Zin |', '|---|---|---|---|'] + [
          f'| `{k}` | {v[0]} | {v[1]} | {v[2].replace(chr(10) + chr(10), " / ")} |' for k, v in PLAYER.items()] + [
          f'| (geen) | | | {VANILLA} |', '', '## De compagnon', '',
          'Eigen zin hieronder; anders zijn omroepzin als tegenstander (zie Tegenstanders); anders een algemene zin.', '',
          '| Compagnon | Zin |', '|---|---|'] + [f'| `{k}` | {v.replace(chr(10) + chr(10), " / ")} |' for k, v in COMPANION.items()] + [
          '', 'Algemeen (terugval):', ''] + [f'- {t}' for t in PARTNER] + ['', '## Tegenstanders', '',
          '| Trainer | Aankondiging |', '|---|---|']
    for t, text in LINES.items():
        s = wrap(text)
        out.append(f'    {{TRAINER_{t}, COMPOUND_STRING("{s}")}},')
        md.append(f'| `{t}` | {dimp.curly_quotes(text)} |')
    out += ['};', '']
    md += ['', f'Terugval (trainer zonder eigen zin): {FALLBACK}', '']
    open(OUT_H, 'w').write('\n'.join(out))
    open(OUT_MD, 'w').write('\n'.join(md))
    print(f'{len(LINES)} teksten -> {os.path.relpath(OUT_H, ROOT)}, {os.path.relpath(OUT_MD, ROOT)}')


if __name__ == '__main__':
    main()
