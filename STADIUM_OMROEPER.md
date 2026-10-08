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

## De speler (willekeurig uit wat klopt)

| Voorwaarde | Zin |
|---|---|
| `TITLES` | Defending the trophy: {PLAYER}! The trophy remembers you. It's scared. |
| `VETERAN` | {PLAYER}! Twenty-plus wins here. The floor knows your footprints by heart. |
| `RETURNING` | {PLAYER} is back! Last time didn't go great. Don't worry, we kept the footage. |
| `NEWCOMER` | A fresh face: {PLAYER}! First time here. The medics are on standby. Just in case. |
| `HALL_OF_FAME` | The CHAMPION of HOENN: {PLAYER}! Yes, the real one. STEVEN is still in therapy. |
| `EIGHT_BADGES` | {PLAYER}! Eight BADGES, no ELITE FOUR win. Ambition: high. Results: pending. |
| `LEGENDARY` | {PLAYER} owns a {STR_VAR_1}! A legend. In a ball. In a pocket. Sure. |
| `BIG_DEX` | {PLAYER} caught over 200 POKéMON. The PC storage union is on strike. |
| `PLAYTIME` | {PLAYER}! Over a hundred hours on the clock. Go outside. After this match. |
| (geen) | In the blue corner: {PLAYER}! A trainer. With POKéMON. That's all it says here. |

## De compagnon

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
| `SALIM` | SALIM of the MIRAGE BAZAAR! Everything for sale, nothing his! |
| `BRENDAN_ROUTE_136_TREECKO` | BRENDAN! Your rival. Still salty about which starter you picked. |
| `MAY_ROUTE_136_TORCHIC` | MAY! Your rival. She swears she's better at this than you. Prove it. |

Terugval (trainer zonder eigen zin): And the next challenger! We were told to say something funny here. We forgot.
