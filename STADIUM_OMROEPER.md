# Battle Stadium: de omroeper

Vóór elke wedstrijd in de arena: bij het eerste gevecht een welkom, elke ronde de rondenaam, bij het eerste
gevecht de speler (en in doubles de compagnon), dan de tegenstander(s) om beurten.
Bewerken: `tools/grounded/stadium/announcer.py`, daarna het script draaien.

## Welkom en rondes

- Welcome to the BATTLE STADIUM! 32 trainers, one trophy, zero refunds.
- Welcome to STADIUM DOUBLES! Sixteen teams, twice the property damage.
- ROUND OF 32! Half of you go home today. The parking lot is already cheering.
- ROUND OF 16! The hot dog stand has outlasted half the field already.
- QUARTERFINALS! Eight left. The crowd has learned two of their names.
- The SEMIFINALS! Four left. Somebody's grandma just woke up for this.
- The FINAL! One match, one trophy, and one very nervous janitor.

## De speler (willekeurig uit wat klopt, gewogen: 6 = specifiek, 3 = opvallend, 1 = algemeen)

| Sleutel | Gewicht | Voorwaarde | Zin |
|---|---|---|---|
| `WHITE_OUTS` | 6 | white-outs >= 15 (gewone run ±5-10) | {PLAYER}! This trainer loses more than they win. / So let's all pretend this time is gonna be different. |
| `LEAGUE_BULLY` | 6 | Hall of Fame >= 10 keer | {PLAYER}! {STR_VAR_2} wins at the POKéMON LEAGUE. / A trainer who likes to fight the same people over and over again. Bully! |
| `FAN` | 6 | >= 5 van dezelfde soort in team + pc | {PLAYER} owns {STR_VAR_2} {STR_VAR_1}! / That's not a team. That's a fan club with a membership fee. |
| `MAGIKARP` | 6 | een MAGIKARP in het Stadium-team | {PLAYER} entered a MAGIKARP. In a tournament. On purpose. / Bold strategy. Or a cry for help. |
| `MONOTYPE` | 6 | het hele Stadium-team deelt een type | {PLAYER} brought only {STR_VAR_1} types. / A theme team! Subtle. Like a brass band. |
| `IMPLOSION` | 6 | ooit IMPLOSION gebruikt | {PLAYER} once used IMPLOSION. A black hole. Indoors. / Our insurance went up 400 percent. |
| `TRASH_SPIRITOMB` | 6 | Spiritomb uit de prullenbak van het Abandoned Ship | {PLAYER} caught a SPIRITOMB in a trash can. We don't judge. The trash can does. |
| `HOOPA_SNACK` | 6 | Hoopa-wens: een snack | {PLAYER} met a genie and wished for a snack. / A grandma in LAVARIDGE is short one batch of cookies. |
| `HOOPA_FAME` | 6 | Hoopa-wens: roem | {PLAYER} wished for fame and got GABBY's. Remember GABBY? No? Exactly. |
| `HOOPA_RICHES` | 6 | Hoopa-wens: rijkdom | {PLAYER} wished for riches. Somewhere, a RICH BOY's piggy bank is empty. Boo! |
| `HOOPA_POWER` | 6 | Hoopa-wens: kracht | {PLAYER} wished for power and got a CHOICE BAND. / BRAWLY lost his headband that day. Funny, that. |
| `BURGLAR` | 6 | Burglar (SIMON) >= 5 keer verslagen | {PLAYER} has beaten SIMON the BURGLAR {STR_VAR_2} times. / He keeps coming back. Lock your doors. |
| `BIRCH` | 6 | >= 5 Birch-gevechten gewonnen | {PLAYER} has beaten PROF. BIRCH and his... samples. / Many times. We washed the trophy twice. |
| `DAVE` | 6 | alle vier Dave-gevechten gewonnen | {PLAYER} beat DAVE four times. / DAVE says it doesn't count. He says you were offside. |
| `COMMUNITY_SERVICE` | 6 | Archie of Maxie verslagen tijdens hun werkstraf | {PLAYER} battled ARCHIE and MAXIE during their community service. / They were holding mops. Cold. |
| `SHINY_RAYQUAZA` | 6 | shiny Rayquaza gevangen | {PLAYER} caught a black RAYQUAZA. / An ancient sky god. Now a pocket accessory. |
| `RELEASED` | 6 | >= 30 Pokémon vrijgelaten | {PLAYER} released {STR_VAR_2} POKéMON. / They live on a farm now. A lovely farm. Don't ask. |
| `FAINTED` | 6 | >= 200 keer een eigen Pokémon flauwgevallen | {PLAYER}'s POKéMON have fainted {STR_VAR_2} times. / The POKéMON CENTER sends a fruit basket every Christmas. |
| `FLED` | 6 | >= 50 keer gevlucht | {PLAYER} has run from {STR_VAR_2} battles. Great cardio. / Tonight, the exit is locked. |
| `SPLASH` | 6 | >= 10 keer SPLASH gebruikt | {PLAYER} has used SPLASH {STR_VAR_2} times. Nothing happened. Every. Single. Time. |
| `STRUGGLE` | 6 | >= 10 keer STRUGGLE | {PLAYER}'s POKéMON have used STRUGGLE {STR_VAR_2} times. PP? Never heard of her. |
| `STEPS` | 3 | >= 100.000 stappen | {PLAYER} has walked {STR_VAR_2} steps. The shoes have filed a complaint. |
| `EGGS` | 3 | >= 50 eieren uitgebroed | {PLAYER} has hatched {STR_VAR_2} eggs. / Somewhere, a very tired DITTO needs a vacation. |
| `FISHING` | 3 | >= 200 keer gevist | {PLAYER} has gone fishing {STR_VAR_2} times. IVAN calls that a warm-up. |
| `SAVES` | 3 | >= 500 keer opgeslagen | {PLAYER} has saved the game {STR_VAR_2} times. Trust issues? / Relax. This match can't be undone. |
| `POKECENTER` | 3 | >= 300 keer in een Pokémon Center | {PLAYER} has visited a POKéMON CENTER {STR_VAR_2} times. / The nurse has a punch card with your face on it. |
| `SHINIES` | 3 | >= 3 shiny Pokémon in team + pc | {PLAYER} owns {STR_VAR_2} shiny POKéMON. Wrong colors, right attitude. |
| `LEDGES` | 3 | >= 300 keer van een richel gesprongen | {PLAYER} has jumped off {STR_VAR_2} ledges. Never once climbed back up. Committed. |
| `JACKPOT` | 3 | jackpot in de Game Corner | {PLAYER} hit a jackpot at the GAME CORNER. / The casino knows. The casino remembers. |
| `RICH` | 3 | >= 500.000 geld | {PLAYER} has half a million in the bank. / Tonight's prize money goes to the janitor. |
| `BROKE` | 3 | < 1.000 geld (met minstens 1 badge) | {PLAYER} is broke. Like, really broke. Win this one. The hot dogs aren't free. |
| `LEGENDARY` | 3 | een legendary gevangen | {PLAYER} owns a {STR_VAR_1}! A legend. In a ball. In a pocket. Sure. |
| `BIG_DEX` | 3 | >= 200 soorten gevangen | {PLAYER} caught over 200 POKéMON. The PC storage union is on strike. |
| `PLAYTIME` | 3 | >= 100 uur speeltijd | {PLAYER}! Over a hundred hours on the clock. Go outside. After this match. |
| `TITLES` | 1 | een Stadium-titel | Defending the trophy: {PLAYER}! The trophy remembers you. It's scared. |
| `VETERAN` | 1 | >= 20 Stadium-wedstrijden gewonnen | {PLAYER}! Twenty-plus wins here. The floor knows your footprints by heart. |
| `RETURNING` | 1 | >= 2 toernooien, geen titel | {PLAYER} is back! Last time didn't go great. Don't worry, we kept the footage. |
| `NEWCOMER` | 1 | eerste toernooi | A fresh face: {PLAYER}! First time here. The medics are on standby. Just in case. |
| `HALL_OF_FAME` | 1 | kampioen (Hall of Fame) | The CHAMPION of HOENN: {PLAYER}! Yes, the real one. STEVEN is still in therapy. |
| `EIGHT_BADGES` | 1 | 8 badges, nog geen kampioen | {PLAYER}! Eight BADGES, no ELITE FOUR win. Ambition: high. Results: pending. |
| `TREECKO` | 1 | starter Treecko | {PLAYER} picked TREECKO. The cool one. That's what everybody says. |
| `TORCHIC` | 1 | starter Torchic | {PLAYER} picked TORCHIC. A chicken that learns to kick. Respect. |
| `MUDKIP` | 1 | starter Mudkip | {PLAYER} picked MUDKIP. Of course. The internet told you to. |
| (geen) | | | In the blue corner: {PLAYER}! A trainer. With POKéMON. That's all it says here. |

## De compagnon

Eigen zin hieronder; anders zijn omroepzin als tegenstander (zie Tegenstanders); anders een algemene zin.

| Compagnon | Zin |
|---|---|
| `BRENDAN` | Teaming up with {PLAYER}: BRENDAN! Your rival. / He wants a rematch. After this match. Obviously. |
| `MAY` | Teaming up with {PLAYER}: MAY! She keeps score of your rivalry. She is "ahead". |
| `KECCLES` | And next to {PLAYER}... KECCLES! Probably. He could be anywhere. / A KECLEON with a PhD and an existential crisis. Same thing, really. |
| `WALLY` | With {PLAYER}: WALLY! The sick kid from PETALBURG got better. / Much better. Worryingly better. |
| `MASCOTS` | With {PLAYER}: the MASCOTS! / On the lunchbox, on the plushie, and now on the battlefield. |
| `STARTERS` | With {PLAYER}: the KANTO STARTERS! Fully evolved. / Still holding a grudge about the lab. |
| `FOSSILS` | With {PLAYER}: the FOSSILS! Millions of years old. / Still faster than the WiFi in here. |
| `EEVEES` | With {PLAYER}: the EEVEE family! / Three cousins, one family reunion, zero agreement. |
| `LAKE` | With {PLAYER}: the LAKE TRIO! / Knowledge, emotion and willpower. You bring the snacks. |
| `REGIS` | With {PLAYER}: the REGIS! They speak only in beeps. Our translator quit. |
| `BIRDS` | With {PLAYER}: the LEGENDARY BIRDS! Please do not feed them. / They bite. And freeze. And zap. |
| `BEASTS` | With {PLAYER}: the LEGENDARY BEASTS! / They roamed half of HOENN to get here. Took the bus the last bit. |
| `PSEUDOS` | With {PLAYER}: three PSEUDO-LEGENDARIES! / 600 base stats each. The other trainers want a word. |
| `SWORDS` | With {PLAYER}: the SWORDS OF JUSTICE! / They're here to judge. Mostly the referee. |
| `LOYAL` | With {PLAYER}: the LOYAL THREE! Loyal to {PLAYER}. Today. Read the contract. |
| `TAPUS` | With {PLAYER}: the TAPUS! Island guardians. / Very protective. Of the snack table. |
| `GENIES` | With {PLAYER}: the FORCES OF NATURE! Weather forecast: yes. |
| `ULTRAS` | With {PLAYER}: the ULTRA BEASTS! From another dimension. / Their visas are pending. |
| `RUIN` | With {PLAYER}: the TREASURES OF RUIN! Four were sealed. / Three showed up. Nobody asks about the fourth. |
| `WEATHER` | With {PLAYER}: the WEATHER TRIO! / Rain, sun, and a sky dragon that hates both. Bring a coat. |
| `CREATORS` | With {PLAYER}: the CREATORS! Time, space and antimatter. The janitor gave up. |

Algemeen (terugval):

- At {PLAYER}'s side: {STR_VAR_1}! Friends? Their lawyers say partners.
- With {PLAYER}: {STR_VAR_1}! They met five minutes ago. Chemistry!
- {PLAYER}'s partner: {STR_VAR_1}! Paid in exposure and one free hot dog.
- Covering {PLAYER}: {STR_VAR_1}! Or standing nearby. Close enough.

## Tegenstanders

| Trainer | Aankondiging |
|---|---|
| `ROXANNE_5` | ROXANNE! You don't have to put on the red light. She brought rocks instead. |
| `BRAWLY_5` | BRAWLY! Trains six days a week. Five days a week, three days a week. |
| `WATTSON_5` | WATTSON! He isn't here to battle. He's mining crypto on the arena's power grid. |
| `FLANNERY_5` | FLANNERY! She forgot her catchphrase again. Something about embers? |
| `NORMAN_5` | NORMAN paused his series for this. Make it quick, he's on a cliffhanger. |
| `WINONA_5` | WINONA landed twenty minutes ago and is still looking for suitcase number 36. |
| `TATE_AND_LIZA_5` | TATE & LIZA! Two bodies, one soul, zero spoons. Lawyers in row one. |
| `WALLACE_5` | WALLACE! Contest star, GYM LEADER, and the reason HOENN ran out of glitter. |
| `SIDNEY` | SIDNEY of the ELITE FOUR! Everyone at home has money on him. Bet responsibly. |
| `PHOEBE` | PHOEBE! Her ghosts are already complaining about the hot dogs in here. |
| `GLACIA` | GLACIA! An ice master who moved to a tropical region. On purpose. Twice. |
| `DRAKE` | DRAKE, the DRAGON master! Not that one. Do NOT play the Kendrick song. |
| `JUAN` | JUAN! He taught WALLACE everything. Then WALLACE took his gym. Awkward. |
| `STEVEN` | STEVEN STONE! HE'S MADE OF METAL! HIS CIRCUITS GLEAM! His wallet too. |
| `WALLY_VR_5` | WALLY! He once needed help catching a RALTS. Now he owns a FLUTTER MANE. |
| `ARCHIE_SOOTOPOLIS` | ARCHIE of AQUA SPARKLING WATER! Our official hydration sponsor! |
| `MAXIE_SOOTOPOLIS` | MAXIE of MAGMA HOT SAUCE! Spiciest man in HOENN. Pale fans, cover your lips. |
| `BIRCH_UNDERWATER` | Cue the Macarena! PROF. BIRCH and his... samples. Don't touch them. |
| `KECCLES_3` | KECCLES! A KECLEON with a PhD and existential dread. Is he here? |
| `COLRESS_MAGMA` | COLRESS! He'll analyze your team. And everything wrong with MAUVILLE. |
| `ZINNIA` | ZINNIA, the LOREKEEPER! She'll explain the lore. All of it. Mid-battle. |
| `MIMI` | MIMI! Yes, she's a MIMIKYU. No, nobody knows who signed her up. ...pika... |
| `GABBY_AND_TY_6` | GABBY & TY! Breaking news... right after... these... very... long... pauses. |
| `STADIUM_JOEY` | Youngster JOEY! His POOCHYENA is in the top percentage of the top percentage! |
| `STADIUM_WINSTON` | WINSTON! His whole team is shiny. He paid for it. Mo money, mo problems. |
| `STADIUM_MUSTARD` | Mustard on the beat, ho! The dojo master himself... MUSTAAAAAAAAAARD! |
| `MATT` | MATT! He brought a WAILORD and a SNORLAX. The floor filed a complaint. |
| `SHELLY_SEAFLOOR_CAVERN` | AQUA ADMIN SHELLY! She's mainly here to sell you a crate of sparkling water. |
| `TABITHA_MOSSDEEP` | TABITHA! MAXIE's loyal right hand. The left one is holding the hot sauce. |
| `STADIUM_BROCK` | BROCK of PEWTER CITY! Rocks, fossils, and his eyes are open. We think. |
| `STADIUM_MISTY` | MISTY! She still wants her bike back. It's been almost thirty years, kid. |
| `STADIUM_LT_SURGE` | LT. SURGE! He'll shock you. Then tell you war stories nobody asked for. |
| `STADIUM_ERIKA` | ERIKA! She may doze off mid-battle. Don't wake her. It's called self-care. |
| `STADIUM_KOGA` | KOGA, the ninja master! He's already here. He's been here for an hour. |
| `STADIUM_SABRINA` | SABRINA! She already knows how this match ends. She's not telling. |
| `STADIUM_BLAINE` | BLAINE! He'll quiz you between turns. Wrong answers get burned. |
| `STADIUM_GIOVANNI` | GIOVANNI! A perfectly legitimate businessman. No rockets. None. |
| `STADIUM_LORELEI` | LORELEI! The coldest welcome in KANTO. GLACIA says she copied her. |
| `STADIUM_BRUNO` | BRUNO! He trained with boulders for twenty years. The boulders quit. |
| `STADIUM_AGATHA` | AGATHA! She thinks OAK went soft. She's here to prove she didn't. |
| `STADIUM_LANCE` | LANCE! Cape, DRAGONITE, and a history of using HYPER BEAM on people. |
| `STADIUM_BLUE` | BLUE, the CHAMPION! Historically for about five minutes. Smell ya later! |
| `STADIUM_RED` | RED! He came down from MT. SILVER for this. He has said nothing. Ever. |
| `STADIUM_OAK` | PROF. OAK! He still can't remember if you're a boy or a girl. |
| `STADIUM_ROARK` | ROARK! Coal miner, fossil nerd. The helmet stays on. Indoors too. |
| `STADIUM_GARDENIA` | GARDENIA! She loves GRASS POKéMON. Ask her about the chateau and she leaves. |
| `STADIUM_MAYLENE` | MAYLENE! She fights barefoot. On this floor. After GRIMER's match. Brave. |
| `STADIUM_WAKE` | CRASHER WAKE! A luchador with a GYARADOS. The mask stays on. Always. |
| `STADIUM_FANTINA` | FANTINA! Contest queen, dance teacher, ghost lady. Mostly ghost lady. |
| `STADIUM_BYRON` | BYRON! ROARK's dad. Steel, fossils, and strong opinions about both. |
| `STADIUM_CANDICE` | CANDICE! She goes all out! In a skirt! In the snow! Every single day! |
| `STADIUM_VOLKNER` | VOLKNER! He got bored and blacked out his whole city. Welcome back! |
| `STADIUM_AARON` | AARON of the ELITE FOUR! Bugs only. Except DRAPION. Do not ask. |
| `STADIUM_BERTHA` | BERTHA! Sweet old granny with an EARTHQUAKE. Ground rules apply. |
| `STADIUM_FLINT` | FLINT! His hair is on fire. That's not a style. Someone get a bucket. |
| `STADIUM_LUCIAN` | LUCIAN! He brought a book. He'll finish a chapter between your turns. |
| `STADIUM_CYNTHIA` | CYNTHIA! Her GARCHOMP has a fan club, a lawyer and a skincare line. |
| `STADIUM_CYRUS` | CYRUS of TEAM GALACTIC! He wants a world without spirit. Tough crowd. |
| `STADIUM_BARRY` | BARRY! He's late! No, early! He'll fine you ten million either way! |
| `STADIUM_MARS` | Commander MARS! She's here for your POKéMON. And maybe an autograph. |
| `STADIUM_JUPITER` | Commander JUPITER! Purple hair, poison team, zero chill. |
| `STADIUM_SATURN` | Commander SATURN! The sensible one. He'd rather be literally anywhere else. |
| `STADIUM_PALMER` | TOWER TYCOON PALMER! Pure dad energy. He brought HEATRAN to the barbecue. |
| `STADIUM_THORTON` | THORTON! He has a spreadsheet of your team. You're row 47. It's not pretty. |
| `STADIUM_ARGENTA` | HALL MATRON ARGENTA! She's seen 30 years of trainers. You're not special. |
| `STADIUM_DAHLIA` | ARCADE STAR DAHLIA! Her moves are picked by roulette. So is your fate. |
| `STADIUM_RILEY` | RILEY! He reads auras. He knew about this match before the bracket did. |
| `STADIUM_ANABEL` | SALON MAIDEN ANABEL! She brought legendaries to a level 50 tournament. |
| `STADIUM_TUCKER` | DOME ACE TUCKER! He loves the crowd more than the crowd loves him. |
| `STADIUM_SPENSER` | PALACE MAVEN SPENSER! His POKéMON don't listen to him either. Relatable. |
| `STADIUM_GRETA` | ARENA TYCOON GRETA! She has a SHEDINJA. One hit. Good luck with that. |
| `STADIUM_NOLAND` | FACTORY HEAD NOLAND! He'll borrow your POKéMON. He won't give them back. |
| `STADIUM_LUCY` | PIKE QUEEN LUCY! She hasn't smiled since 2004. Neither has her SEVIPER. |
| `STADIUM_BRANDON` | PYRAMID KING BRANDON! He brought all three REGIS. They didn't ask to come. |
| `STADIUM_N` | N, the KING of TEAM PLASMA! He wants to free your POKéMON. Ticket refunds: no. |
| `STADIUM_GHETSIS` | GHETSIS! He'd like everyone to sit down. Yes, you too. Especially you. |
| `STADIUM_PETREL` | ROCKET EXEC PETREL! Or GIOVANNI. Or a DITTO. Nobody checked his ID. |
| `STADIUM_ZINZOLIN` | SAGE ZINZOLIN! He froze a whole city. Then himself. Do not lick him. |
| `STADIUM_ROOD` | SAGE ROOD! Ex-villain, current grandpa. His POKéMON heal. His knees don't. |
| `STADIUM_SHADOW_TRIAD` | THE SHADOW TRIAD! Three ninjas, one ticket. Security is still looking. |
| `STADIUM_PLASMA_GRUNT_M` | A NEO PLASMA GRUNT! Nobody knows his name. Including him. |
| `STADIUM_PLASMA_GRUNT_F` | A NEO PLASMA GRUNT! She joined for the dental plan. There is no dental plan. |
| `DAVE` | From VICTORY ROAD: DAVE is on fire! Your defense is terrified! |
| `MITCH` | MITCH! He has stage fright. Thousands of fans. Everybody, stare at him! |
| `SICKBLIK` | SICKBLIK! He made this romhack. Beat him and he nerfs you next patch. |
| `STADIUM_WARIO` | WARIO! Here for the prize money and the free buffet. Mostly the buffet. |
| `STADIUM_YOSHI` | YOSHI! Please be gentle, he cries. We have tissues on standby. |
| `STADIUM_GOLBAT` | GOLBAT! From every cave of your childhood. REPEL does not work in here. |
| `STADIUM_GRIMER` | GRIMER! Here since 1996. So is the smell. Front rows, we apologize. |
| `STADIUM_BOO` | BOO! Don't look at him. Seriously, look away. It's in the rules. |
| `STADIUM_MEW` | MEW! Found under a truck in LILYCOVE. The rumors were true all along! |
| `STADIUM_SHY_GUY_RED` | SHY GUY! He asked us not to announce him. Sorry, buddy. |
| `STADIUM_SHY_GUY_GREEN` | SHYER GUY! Even shyer than SHY GUY. He's under the bleachers. Somewhere. |
| `STADIUM_SHY_GUY_PINK` | FLY GUY! He refuses to land. The referee has given up. |
| `STADIUM_SHY_GUY_BLACK` | SHADY GUY! Everybody check your pockets. Now check them again. |
| `STADIUM_BURGLAR` | SIMON the BURGLAR! Straight out of 1996. Mind your wallet. And the trophy. |
| `STADIUM_DITTO` | DITTO! He asked me to read his statement. Ahem. “...” “:)” |
| `STADIUM_DONALD` | DONALD the BUG MANIAC! Six BUG POKéMON, he says. They are all DITTO. |
| `STADIUM_IVAN` | IVAN the FISHERMAN! Very rare fishies. His MAGIKARP knows HYDRO PUMP. |
| `STADIUM_JOHNSON` | JOHNSON! Tik tok, tik tok. Nobody knows what happens next. Not even him. |
| `STADIUM_LYLE` | LYLE! His brother's bugs, finally trained! IVs: still zero. Heart: maxed. |
| `PLASMA_NIGEL` | NIGEL, NEO PLASMA's Head of Logistics! He signed for a GENESECT. |
| `VICTORY_V` | V! Only POKéMON with a V! VOLCARONA! VIKAVOLT! VICTORY? We'll see. |
| `GRIMSBY` | CAPTAIN GRIMSBY! Dead since 1802, still clocks in. Union rules. |
| `TALLOW` | TALLOW! Lighthouse keeper, 1952 to 1953. Mostly 1953. Mostly dead. |
| `GERALD_WARDEN` | GERALD, Warden of the Dragon's Den! Did you fill in form D-7? Too late now. |
| `WICK` | WICK! Forty years a lighthouse keeper. His lamp is a fish. It works. |
| `SALIM` | SALIM of the MIRAGE BAZAAR! Everything for sale, nothing his! |
| `BRENDAN_ROUTE_136_TREECKO` | BRENDAN! Your rival. Still salty about which starter you picked. |
| `MAY_ROUTE_136_TORCHIC` | MAY! Your rival. She swears she's better at this than you. Prove it. |

Terugval (trainer zonder eigen zin): And the next challenger! We were told to say something funny here. We forgot.
