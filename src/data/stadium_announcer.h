// Gegenereerd door tools/grounded/stadium/announcer.py; niet met de hand bewerken.
// De omroeper in de arena (één tekstvak per zin): welkom, ronde, speler en compagnon, tegenstanders.

struct StadiumAnnouncerLine
{
    u16 trainerId;
    const u8 *text;
};

static const u8 sStadiumAnnouncerFallback[] = _("And the next challenger! We were told\nto say something funny here. We forgot.");

static const u8 sStadiumAnnouncerVanilla[] = _("In the blue corner: {PLAYER}! A trainer.\nWith POKéMON. That's all it says here.");

static const u8 *const sStadiumAnnouncerWelcome[] =
{
    COMPOUND_STRING("Welcome to the BATTLE STADIUM! 32\ntrainers, one trophy, zero refunds."),
    COMPOUND_STRING("Welcome to STADIUM DOUBLES! Sixteen\nteams, twice the property damage."),
};

static const u8 *const sStadiumAnnouncerRounds[] =
{
    COMPOUND_STRING("ROUND OF 32! Half of you go home today.\nThe parking lot is already cheering."),
    COMPOUND_STRING("ROUND OF 16! The hot dog stand has\noutlasted half the field already."),
    COMPOUND_STRING("QUARTERFINALS! Eight left. The crowd\nhas learned two of their names."),
    COMPOUND_STRING("The SEMIFINALS! Four left. Somebody's\ngrandma just woke up for this."),
    COMPOUND_STRING("The FINAL! One match, one trophy, and\none very nervous janitor."),
};

enum StadiumAnnouncePlayer
{
    ANNOUNCE_PLAYER_TITLES,
    ANNOUNCE_PLAYER_VETERAN,
    ANNOUNCE_PLAYER_RETURNING,
    ANNOUNCE_PLAYER_NEWCOMER,
    ANNOUNCE_PLAYER_HALL_OF_FAME,
    ANNOUNCE_PLAYER_EIGHT_BADGES,
    ANNOUNCE_PLAYER_LEGENDARY,
    ANNOUNCE_PLAYER_BIG_DEX,
    ANNOUNCE_PLAYER_PLAYTIME,
    ANNOUNCE_PLAYER_COUNT
};

static const u8 *const sStadiumAnnouncerPlayer[] =
{
    COMPOUND_STRING("Defending the trophy: {PLAYER}! The\ntrophy remembers you. It's scared."),
    COMPOUND_STRING("{PLAYER}! Twenty-plus wins here. The\nfloor knows your footprints by heart."),
    COMPOUND_STRING("{PLAYER} is back! Last time didn't go\ngreat. Don't worry, we kept the footage."),
    COMPOUND_STRING("A fresh face: {PLAYER}! First time here.\nThe medics are on standby. Just in case."),
    COMPOUND_STRING("The CHAMPION of HOENN: {PLAYER}! Yes,\nthe real one. STEVEN is still in therapy."),
    COMPOUND_STRING("{PLAYER}! Eight BADGES, no ELITE FOUR\nwin. Ambition: high. Results: pending."),
    COMPOUND_STRING("{PLAYER} owns a {STR_VAR_1}! A legend.\nIn a ball. In a pocket. Sure."),
    COMPOUND_STRING("{PLAYER} caught over 200 POKéMON. The\nPC storage union is on strike."),
    COMPOUND_STRING("{PLAYER}! Over a hundred hours on the\nclock. Go outside. After this match."),
};

static const u8 *const sStadiumAnnouncerPartner[] =
{
    COMPOUND_STRING("At {PLAYER}'s side: {STR_VAR_1}!\nFriends? Their lawyers say partners."),
    COMPOUND_STRING("With {PLAYER}: {STR_VAR_1}! They met\nfive minutes ago. Chemistry!"),
    COMPOUND_STRING("{PLAYER}'s partner: {STR_VAR_1}! Paid\nin exposure and one free hot dog."),
    COMPOUND_STRING("Covering {PLAYER}: {STR_VAR_1}! Or\nstanding nearby. Close enough."),
};

static const struct StadiumAnnouncerLine sStadiumAnnouncerLines[] =
{
    {TRAINER_ROXANNE_5, COMPOUND_STRING("ROXANNE! You don't have to put on the\nred light. She brought rocks instead.")},
    {TRAINER_BRAWLY_5, COMPOUND_STRING("BRAWLY! Trains six days a week. Five\ndays a week, three days a week.")},
    {TRAINER_WATTSON_5, COMPOUND_STRING("WATTSON! He isn't here to battle. He's\nmining crypto on the arena's power grid.")},
    {TRAINER_FLANNERY_5, COMPOUND_STRING("FLANNERY! She forgot her catchphrase\nagain. Something about embers?")},
    {TRAINER_NORMAN_5, COMPOUND_STRING("NORMAN paused his series for this. Make\nit quick, he's on a cliffhanger.")},
    {TRAINER_WINONA_5, COMPOUND_STRING("WINONA landed twenty minutes ago and\nis still looking for suitcase number 36.")},
    {TRAINER_TATE_AND_LIZA_5, COMPOUND_STRING("TATE & LIZA! Two bodies, one soul, zero\nspoons. Lawyers in row one.")},
    {TRAINER_WALLACE_5, COMPOUND_STRING("WALLACE! Contest star, GYM LEADER, and\nthe reason HOENN ran out of glitter.")},
    {TRAINER_SIDNEY, COMPOUND_STRING("SIDNEY of the ELITE FOUR! Everyone at\nhome has money on him. Bet responsibly.")},
    {TRAINER_PHOEBE, COMPOUND_STRING("PHOEBE! Her ghosts are already\ncomplaining about the hot dogs in here.")},
    {TRAINER_GLACIA, COMPOUND_STRING("GLACIA! An ice master who moved to a\ntropical region. On purpose. Twice.")},
    {TRAINER_DRAKE, COMPOUND_STRING("DRAKE, the DRAGON master! Not that one.\nDo NOT play the Kendrick song.")},
    {TRAINER_JUAN, COMPOUND_STRING("JUAN! He taught WALLACE everything.\nThen WALLACE took his gym. Awkward.")},
    {TRAINER_STEVEN, COMPOUND_STRING("STEVEN STONE! HE'S MADE OF METAL! HIS\nCIRCUITS GLEAM! His wallet too.")},
    {TRAINER_WALLY_VR_5, COMPOUND_STRING("WALLY! He once needed help catching a\nRALTS. Now he owns a FLUTTER MANE.")},
    {TRAINER_ARCHIE_SOOTOPOLIS, COMPOUND_STRING("ARCHIE of AQUA SPARKLING WATER! Our\nofficial hydration sponsor!")},
    {TRAINER_MAXIE_SOOTOPOLIS, COMPOUND_STRING("MAXIE of MAGMA HOT SAUCE! Spiciest man\nin HOENN. Pale fans, cover your lips.")},
    {TRAINER_BIRCH_UNDERWATER, COMPOUND_STRING("Cue the Macarena! PROF. BIRCH and his...\nsamples. Don't touch them.")},
    {TRAINER_KECCLES_3, COMPOUND_STRING("KECCLES! A KECLEON with a PhD and\nexistential dread. Is he here?")},
    {TRAINER_COLRESS_MAGMA, COMPOUND_STRING("COLRESS! He'll analyze your team. And\neverything wrong with MAUVILLE.")},
    {TRAINER_ZINNIA, COMPOUND_STRING("ZINNIA, the LOREKEEPER! She'll explain\nthe lore. All of it. Mid-battle.")},
    {TRAINER_MIMI, COMPOUND_STRING("MIMI! Yes, she's a MIMIKYU. No, nobody\nknows who signed her up. ...pika...")},
    {TRAINER_GABBY_AND_TY_6, COMPOUND_STRING("GABBY & TY! Breaking news... right\nafter... these... very... long... pauses.")},
    {TRAINER_STADIUM_JOEY, COMPOUND_STRING("Youngster JOEY! His POOCHYENA is in the\ntop percentage of the top percentage!")},
    {TRAINER_STADIUM_WINSTON, COMPOUND_STRING("WINSTON! His whole team is shiny. He\npaid for it. Mo money, mo problems.")},
    {TRAINER_STADIUM_MUSTARD, COMPOUND_STRING("Mustard on the beat, ho! The dojo\nmaster himself... MUSTAAAAAAAAAARD!")},
    {TRAINER_MATT, COMPOUND_STRING("MATT! He brought a WAILORD and a\nSNORLAX. The floor filed a complaint.")},
    {TRAINER_SHELLY_SEAFLOOR_CAVERN, COMPOUND_STRING("AQUA ADMIN SHELLY! She's mainly here to\nsell you a crate of sparkling water.")},
    {TRAINER_TABITHA_MOSSDEEP, COMPOUND_STRING("TABITHA! MAXIE's loyal right hand. The\nleft one is holding the hot sauce.")},
    {TRAINER_STADIUM_BROCK, COMPOUND_STRING("BROCK of PEWTER CITY! Rocks, fossils,\nand his eyes are open. We think.")},
    {TRAINER_STADIUM_MISTY, COMPOUND_STRING("MISTY! She still wants her bike back.\nIt's been almost thirty years, kid.")},
    {TRAINER_STADIUM_LT_SURGE, COMPOUND_STRING("LT. SURGE! He'll shock you. Then tell you\nwar stories nobody asked for.")},
    {TRAINER_STADIUM_ERIKA, COMPOUND_STRING("ERIKA! She may doze off mid-battle.\nDon't wake her. It's called self-care.")},
    {TRAINER_STADIUM_KOGA, COMPOUND_STRING("KOGA, the ninja master! He's already\nhere. He's been here for an hour.")},
    {TRAINER_STADIUM_SABRINA, COMPOUND_STRING("SABRINA! She already knows how this\nmatch ends. She's not telling.")},
    {TRAINER_STADIUM_BLAINE, COMPOUND_STRING("BLAINE! He'll quiz you between turns.\nWrong answers get burned.")},
    {TRAINER_STADIUM_GIOVANNI, COMPOUND_STRING("GIOVANNI! A perfectly legitimate\nbusinessman. No rockets. None.")},
    {TRAINER_STADIUM_LORELEI, COMPOUND_STRING("LORELEI! The coldest welcome in KANTO.\nGLACIA says she copied her.")},
    {TRAINER_STADIUM_BRUNO, COMPOUND_STRING("BRUNO! He trained with boulders for\ntwenty years. The boulders quit.")},
    {TRAINER_STADIUM_AGATHA, COMPOUND_STRING("AGATHA! She thinks OAK went soft. She's\nhere to prove she didn't.")},
    {TRAINER_STADIUM_LANCE, COMPOUND_STRING("LANCE! Cape, DRAGONITE, and a history\nof using HYPER BEAM on people.")},
    {TRAINER_STADIUM_BLUE, COMPOUND_STRING("BLUE, the CHAMPION! Historically for\nabout five minutes. Smell ya later!")},
    {TRAINER_STADIUM_RED, COMPOUND_STRING("RED! He came down from MT. SILVER for\nthis. He has said nothing. Ever.")},
    {TRAINER_STADIUM_OAK, COMPOUND_STRING("PROF. OAK! He still can't remember if\nyou're a boy or a girl.")},
    {TRAINER_STADIUM_ROARK, COMPOUND_STRING("ROARK! Coal miner, fossil nerd. The\nhelmet stays on. Indoors too.")},
    {TRAINER_STADIUM_GARDENIA, COMPOUND_STRING("GARDENIA! She loves GRASS POKéMON. Ask\nher about the chateau and she leaves.")},
    {TRAINER_STADIUM_MAYLENE, COMPOUND_STRING("MAYLENE! She fights barefoot. On this\nfloor. After GRIMER's match. Brave.")},
    {TRAINER_STADIUM_WAKE, COMPOUND_STRING("CRASHER WAKE! A luchador with a\nGYARADOS. The mask stays on. Always.")},
    {TRAINER_STADIUM_FANTINA, COMPOUND_STRING("FANTINA! Contest queen, dance teacher,\nghost lady. Mostly ghost lady.")},
    {TRAINER_STADIUM_BYRON, COMPOUND_STRING("BYRON! ROARK's dad. Steel, fossils, and\nstrong opinions about both.")},
    {TRAINER_STADIUM_CANDICE, COMPOUND_STRING("CANDICE! She goes all out! In a skirt!\nIn the snow! Every single day!")},
    {TRAINER_STADIUM_VOLKNER, COMPOUND_STRING("VOLKNER! He got bored and blacked out\nhis whole city. Welcome back!")},
    {TRAINER_STADIUM_AARON, COMPOUND_STRING("AARON of the ELITE FOUR! Bugs only.\nExcept DRAPION. Do not ask.")},
    {TRAINER_STADIUM_BERTHA, COMPOUND_STRING("BERTHA! Sweet old granny with an\nEARTHQUAKE. Ground rules apply.")},
    {TRAINER_STADIUM_FLINT, COMPOUND_STRING("FLINT! His hair is on fire. That's not a\nstyle. Someone get a bucket.")},
    {TRAINER_STADIUM_LUCIAN, COMPOUND_STRING("LUCIAN! He brought a book. He'll finish a\nchapter between your turns.")},
    {TRAINER_STADIUM_CYNTHIA, COMPOUND_STRING("CYNTHIA! Her GARCHOMP has a fan club, a\nlawyer and a skincare line.")},
    {TRAINER_STADIUM_CYRUS, COMPOUND_STRING("CYRUS of TEAM GALACTIC! He wants a\nworld without spirit. Tough crowd.")},
    {TRAINER_STADIUM_BARRY, COMPOUND_STRING("BARRY! He's late! No, early! He'll fine\nyou ten million either way!")},
    {TRAINER_STADIUM_MARS, COMPOUND_STRING("Commander MARS! She's here for your\nPOKéMON. And maybe an autograph.")},
    {TRAINER_STADIUM_JUPITER, COMPOUND_STRING("Commander JUPITER! Purple hair, poison\nteam, zero chill.")},
    {TRAINER_STADIUM_SATURN, COMPOUND_STRING("Commander SATURN! The sensible one.\nHe'd rather be literally anywhere else.")},
    {TRAINER_STADIUM_PALMER, COMPOUND_STRING("TOWER TYCOON PALMER! Pure dad energy.\nHe brought HEATRAN to the barbecue.")},
    {TRAINER_STADIUM_THORTON, COMPOUND_STRING("THORTON! He has a spreadsheet of your\nteam. You're row 47. It's not pretty.")},
    {TRAINER_STADIUM_ARGENTA, COMPOUND_STRING("HALL MATRON ARGENTA! She's seen 30\nyears of trainers. You're not special.")},
    {TRAINER_STADIUM_DAHLIA, COMPOUND_STRING("ARCADE STAR DAHLIA! Her moves are\npicked by roulette. So is your fate.")},
    {TRAINER_STADIUM_RILEY, COMPOUND_STRING("RILEY! He reads auras. He knew about\nthis match before the bracket did.")},
    {TRAINER_STADIUM_ANABEL, COMPOUND_STRING("SALON MAIDEN ANABEL! She brought\nlegendaries to a level 50 tournament.")},
    {TRAINER_STADIUM_TUCKER, COMPOUND_STRING("DOME ACE TUCKER! He loves the crowd\nmore than the crowd loves him.")},
    {TRAINER_STADIUM_SPENSER, COMPOUND_STRING("PALACE MAVEN SPENSER! His POKéMON\ndon't listen to him either. Relatable.")},
    {TRAINER_STADIUM_GRETA, COMPOUND_STRING("ARENA TYCOON GRETA! She has a\nSHEDINJA. One hit. Good luck with that.")},
    {TRAINER_STADIUM_NOLAND, COMPOUND_STRING("FACTORY HEAD NOLAND! He'll borrow your\nPOKéMON. He won't give them back.")},
    {TRAINER_STADIUM_LUCY, COMPOUND_STRING("PIKE QUEEN LUCY! She hasn't smiled\nsince 2004. Neither has her SEVIPER.")},
    {TRAINER_STADIUM_BRANDON, COMPOUND_STRING("PYRAMID KING BRANDON! He brought all\nthree REGIS. They didn't ask to come.")},
    {TRAINER_STADIUM_N, COMPOUND_STRING("N, the KING of TEAM PLASMA! He wants to\nfree your POKéMON. Ticket refunds: no.")},
    {TRAINER_STADIUM_GHETSIS, COMPOUND_STRING("GHETSIS! He'd like everyone to sit down.\nYes, you too. Especially you.")},
    {TRAINER_STADIUM_PETREL, COMPOUND_STRING("ROCKET EXEC PETREL! Or GIOVANNI. Or a\nDITTO. Nobody checked his ID.")},
    {TRAINER_STADIUM_ZINZOLIN, COMPOUND_STRING("SAGE ZINZOLIN! He froze a whole city.\nThen himself. Do not lick him.")},
    {TRAINER_STADIUM_ROOD, COMPOUND_STRING("SAGE ROOD! Ex-villain, current grandpa.\nHis POKéMON heal. His knees don't.")},
    {TRAINER_STADIUM_SHADOW_TRIAD, COMPOUND_STRING("THE SHADOW TRIAD! Three ninjas, one\nticket. Security is still looking.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_M, COMPOUND_STRING("A NEO PLASMA GRUNT! Nobody knows his\nname. Including him.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_F, COMPOUND_STRING("A NEO PLASMA GRUNT! She joined for the\ndental plan. There is no dental plan.")},
    {TRAINER_DAVE, COMPOUND_STRING("From VICTORY ROAD: DAVE is on fire! Your\ndefense is terrified!")},
    {TRAINER_MITCH, COMPOUND_STRING("MITCH! He has stage fright. Thousands\nof fans. Everybody, stare at him!")},
    {TRAINER_SICKBLIK, COMPOUND_STRING("SICKBLIK! He made this romhack. Beat\nhim and he nerfs you next patch.")},
    {TRAINER_STADIUM_WARIO, COMPOUND_STRING("WARIO! Here for the prize money and the\nfree buffet. Mostly the buffet.")},
    {TRAINER_STADIUM_YOSHI, COMPOUND_STRING("YOSHI! Please be gentle, he cries. We\nhave tissues on standby.")},
    {TRAINER_STADIUM_GOLBAT, COMPOUND_STRING("GOLBAT! From every cave of your\nchildhood. REPEL does not work in here.")},
    {TRAINER_STADIUM_GRIMER, COMPOUND_STRING("GRIMER! Here since 1996. So is the smell.\nFront rows, we apologize.")},
    {TRAINER_STADIUM_BOO, COMPOUND_STRING("BOO! Don't look at him. Seriously, look\naway. It's in the rules.")},
    {TRAINER_STADIUM_MEW, COMPOUND_STRING("MEW! Found under a truck in LILYCOVE.\nThe rumors were true all along!")},
    {TRAINER_STADIUM_SHY_GUY_RED, COMPOUND_STRING("SHY GUY! He asked us not to announce\nhim. Sorry, buddy.")},
    {TRAINER_STADIUM_SHY_GUY_GREEN, COMPOUND_STRING("SHYER GUY! Even shyer than SHY GUY.\nHe's under the bleachers. Somewhere.")},
    {TRAINER_STADIUM_SHY_GUY_PINK, COMPOUND_STRING("FLY GUY! He refuses to land. The\nreferee has given up.")},
    {TRAINER_STADIUM_SHY_GUY_BLACK, COMPOUND_STRING("SHADY GUY! Everybody check your\npockets. Now check them again.")},
    {TRAINER_STADIUM_BURGLAR, COMPOUND_STRING("SIMON the BURGLAR! Straight out of\n1996. Mind your wallet. And the trophy.")},
    {TRAINER_STADIUM_DITTO, COMPOUND_STRING("DITTO! He asked me to read his\nstatement. Ahem. “...” “:)”")},
    {TRAINER_STADIUM_DONALD, COMPOUND_STRING("DONALD the BUG MANIAC! Six BUG\nPOKéMON, he says. They are all DITTO.")},
    {TRAINER_STADIUM_IVAN, COMPOUND_STRING("IVAN the FISHERMAN! Very rare fishies.\nHis MAGIKARP knows HYDRO PUMP.")},
    {TRAINER_STADIUM_JOHNSON, COMPOUND_STRING("JOHNSON! Tik tok, tik tok. Nobody knows\nwhat happens next. Not even him.")},
    {TRAINER_STADIUM_LYLE, COMPOUND_STRING("LYLE! His brother's bugs, finally\ntrained! IVs: still zero. Heart: maxed.")},
    {TRAINER_PLASMA_NIGEL, COMPOUND_STRING("NIGEL, NEO PLASMA's Head of Logistics!\nHe signed for a GENESECT.")},
    {TRAINER_VICTORY_V, COMPOUND_STRING("V! Only POKéMON with a V! VOLCARONA!\nVIKAVOLT! VICTORY? We'll see.")},
    {TRAINER_GRIMSBY, COMPOUND_STRING("CAPTAIN GRIMSBY! Dead since 1802, still\nclocks in. Union rules.")},
    {TRAINER_GERALD_WARDEN, COMPOUND_STRING("GERALD, Warden of the Dragon's Den! Did\nyou fill in form D-7? Too late now.")},
    {TRAINER_WICK, COMPOUND_STRING("WICK! Forty years a lighthouse keeper.\nHis lamp is a fish. It works.")},
    {TRAINER_SALIM, COMPOUND_STRING("SALIM of the MIRAGE BAZAAR! Everything\nfor sale, nothing his!")},
    {TRAINER_BRENDAN_ROUTE_136_TREECKO, COMPOUND_STRING("BRENDAN! Your rival. Still salty about\nwhich starter you picked.")},
    {TRAINER_MAY_ROUTE_136_TORCHIC, COMPOUND_STRING("MAY! Your rival. She swears she's better\nat this than you. Prove it.")},
};
