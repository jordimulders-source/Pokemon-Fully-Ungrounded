@ Project Grounded: het Tapu-eiland in de Midden-zee, ten noorden van Route 132. Kaart: tools/grounded/maptools/tapu_cresselia.py.
@ Post-game: voor de Hall of Fame houdt de mist je tegen (coord-triggers op rij 45, VAR_TEMP_1 = 0). Daarna klaart het op.
@ De vier Tapu's (lv 70) een voor een: Koko (noordoost) -> Lele (zuidoost) -> Bulu (noordwest) -> Fini (zuidwest).
@ Een ruine wordt wakker zodra de vorige Tapu een keer verslagen of gevangen is (FLAG_TAPU_*_AWAKE).
@ Verslagen (niet gevangen) = terug na de volgende League (hall_of_fame.inc). Objectvlaggen: FLAG_TEMP_12-15 (ON_TRANSITION).
@ Teksten zijn placeholders.
TapuIsle_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TapuIsle_OnTransition
	.byte 0

TapuIsle_OnTransition:
	goto_if_unset FLAG_SYS_GAME_CLEAR, TapuIsle_EventScript_HideAllTapus
	setweather WEATHER_SUNNY
	setvar VAR_TEMP_1, 1
	call_if_set FLAG_DEFEATED_TAPU_KOKO, TapuIsle_EventScript_HideKoko
	call_if_unset FLAG_TAPU_LELE_AWAKE, TapuIsle_EventScript_HideLele
	call_if_set FLAG_DEFEATED_TAPU_LELE, TapuIsle_EventScript_HideLele
	call_if_unset FLAG_TAPU_BULU_AWAKE, TapuIsle_EventScript_HideBulu
	call_if_set FLAG_DEFEATED_TAPU_BULU, TapuIsle_EventScript_HideBulu
	call_if_unset FLAG_TAPU_FINI_AWAKE, TapuIsle_EventScript_HideFini
	call_if_set FLAG_DEFEATED_TAPU_FINI, TapuIsle_EventScript_HideFini
	end

TapuIsle_EventScript_HideAllTapus:
	call TapuIsle_EventScript_HideKoko
	call TapuIsle_EventScript_HideLele
	call TapuIsle_EventScript_HideBulu
	call TapuIsle_EventScript_HideFini
	end

TapuIsle_EventScript_HideKoko:
	setflag FLAG_TEMP_12
	return

TapuIsle_EventScript_HideLele:
	setflag FLAG_TEMP_13
	return

TapuIsle_EventScript_HideBulu:
	setflag FLAG_TEMP_14
	return

TapuIsle_EventScript_HideFini:
	setflag FLAG_TEMP_15
	return

@ ---------------------------------------------------------------- mist (voor de Hall of Fame)
TapuIsle_EventScript_Fog::
	lockall
	msgbox TapuIsle_Text_Fog, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, TapuIsle_Movement_TurnBack
	waitmovement 0
	releaseall
	end

TapuIsle_Movement_TurnBack:
	walk_down
	walk_down
	step_end

@ ---------------------------------------------------------------- de kahuna en het plein
TapuIsle_EventScript_Kahuna::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_TAPU_FINI, TapuIsle_EventScript_KahunaAllDone
	goto_if_set FLAG_TAPU_FINI_AWAKE, TapuIsle_EventScript_KahunaFini
	goto_if_set FLAG_TAPU_BULU_AWAKE, TapuIsle_EventScript_KahunaBulu
	goto_if_set FLAG_TAPU_LELE_AWAKE, TapuIsle_EventScript_KahunaLele
	msgbox TapuIsle_Text_KahunaIntro, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_KahunaLele::
	msgbox TapuIsle_Text_KahunaLele, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_KahunaBulu::
	msgbox TapuIsle_Text_KahunaBulu, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_KahunaFini::
	msgbox TapuIsle_Text_KahunaFini, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_KahunaAllDone::
	msgbox TapuIsle_Text_KahunaAllDone, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_Tablet::
	msgbox TapuIsle_Text_Tablet, MSGBOX_SIGN
	end

TapuIsle_EventScript_Tourist::
	msgbox TapuIsle_Text_Tourist, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- stenen beelden op het heiligdom (objecten)
TapuIsle_EventScript_StatueKoko::
	msgbox TapuIsle_Text_StatueKoko, MSGBOX_SIGN
	end

TapuIsle_EventScript_StatueLele::
	msgbox TapuIsle_Text_StatueLele, MSGBOX_SIGN
	end

TapuIsle_EventScript_StatueBulu::
	msgbox TapuIsle_Text_StatueBulu, MSGBOX_SIGN
	end

TapuIsle_EventScript_StatueFini::
	msgbox TapuIsle_Text_StatueFini, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- altaren (zonder Tapu erop)
TapuIsle_EventScript_DaisKoko::
	goto_if_set FLAG_DEFEATED_TAPU_KOKO, TapuIsle_EventScript_DaisEmpty
	msgbox TapuIsle_Text_DaisFog, MSGBOX_SIGN
	end

TapuIsle_EventScript_DaisLele::
	goto_if_set FLAG_DEFEATED_TAPU_LELE, TapuIsle_EventScript_DaisEmpty
	msgbox TapuIsle_Text_DaisAsleep, MSGBOX_SIGN
	end

TapuIsle_EventScript_DaisBulu::
	goto_if_set FLAG_DEFEATED_TAPU_BULU, TapuIsle_EventScript_DaisEmpty
	msgbox TapuIsle_Text_DaisAsleep, MSGBOX_SIGN
	end

TapuIsle_EventScript_DaisFini::
	goto_if_set FLAG_DEFEATED_TAPU_FINI, TapuIsle_EventScript_DaisEmpty
	msgbox TapuIsle_Text_DaisAsleep, MSGBOX_SIGN
	end

TapuIsle_EventScript_DaisEmpty::
	msgbox TapuIsle_Text_DaisEmpty, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- de vier Tapu's
TapuIsle_EventScript_TapuKoko::
	lock
	faceplayer
	msgbox TapuIsle_Text_TapuKoko, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_TAPU_KOKO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TAPU_KOKO, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TapuIsle_EventScript_KokoCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TapuIsle_EventScript_KokoDefeated
	msgbox TapuIsle_Text_TapuStays, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_KokoCaught::
	setflag FLAG_CAUGHT_TAPU_KOKO
TapuIsle_EventScript_KokoDefeated::
	setflag FLAG_DEFEATED_TAPU_KOKO
	setflag FLAG_TEMP_12
	removeobject LOCALID_TAPU_ISLE_KOKO
	msgbox TapuIsle_Text_KokoSeed, MSGBOX_DEFAULT
	giveitem ITEM_ELECTRIC_SEED
	goto_if_set FLAG_TAPU_LELE_AWAKE, TapuIsle_EventScript_TapuDone
	setflag FLAG_TAPU_LELE_AWAKE
	clearflag FLAG_TEMP_13
	addobject LOCALID_TAPU_ISLE_LELE
	msgbox TapuIsle_Text_LeleWakes, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_TapuLele::
	lock
	faceplayer
	msgbox TapuIsle_Text_TapuLele, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_TAPU_LELE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TAPU_LELE, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TapuIsle_EventScript_LeleCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TapuIsle_EventScript_LeleDefeated
	msgbox TapuIsle_Text_TapuStays, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_LeleCaught::
	setflag FLAG_CAUGHT_TAPU_LELE
TapuIsle_EventScript_LeleDefeated::
	setflag FLAG_DEFEATED_TAPU_LELE
	setflag FLAG_TEMP_13
	removeobject LOCALID_TAPU_ISLE_LELE
	msgbox TapuIsle_Text_LeleSeed, MSGBOX_DEFAULT
	giveitem ITEM_PSYCHIC_SEED
	goto_if_set FLAG_TAPU_BULU_AWAKE, TapuIsle_EventScript_TapuDone
	setflag FLAG_TAPU_BULU_AWAKE
	clearflag FLAG_TEMP_14
	addobject LOCALID_TAPU_ISLE_BULU
	msgbox TapuIsle_Text_BuluWakes, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_TapuBulu::
	lock
	faceplayer
	msgbox TapuIsle_Text_TapuBulu, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_TAPU_BULU, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TAPU_BULU, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TapuIsle_EventScript_BuluCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TapuIsle_EventScript_BuluDefeated
	msgbox TapuIsle_Text_TapuStays, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_BuluCaught::
	setflag FLAG_CAUGHT_TAPU_BULU
TapuIsle_EventScript_BuluDefeated::
	setflag FLAG_DEFEATED_TAPU_BULU
	setflag FLAG_TEMP_14
	removeobject LOCALID_TAPU_ISLE_BULU
	msgbox TapuIsle_Text_BuluSeed, MSGBOX_DEFAULT
	giveitem ITEM_GRASSY_SEED
	goto_if_set FLAG_TAPU_FINI_AWAKE, TapuIsle_EventScript_TapuDone
	setflag FLAG_TAPU_FINI_AWAKE
	clearflag FLAG_TEMP_15
	addobject LOCALID_TAPU_ISLE_FINI
	msgbox TapuIsle_Text_FiniWakes, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_TapuFini::
	lock
	faceplayer
	msgbox TapuIsle_Text_TapuFini, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_TAPU_FINI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_TAPU_FINI, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, TapuIsle_EventScript_FiniCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TapuIsle_EventScript_FiniDefeated
	msgbox TapuIsle_Text_TapuStays, MSGBOX_DEFAULT
	release
	end

TapuIsle_EventScript_FiniCaught::
	setflag FLAG_CAUGHT_TAPU_FINI
TapuIsle_EventScript_FiniDefeated::
	setflag FLAG_DEFEATED_TAPU_FINI
	setflag FLAG_TEMP_15
	removeobject LOCALID_TAPU_ISLE_FINI
	msgbox TapuIsle_Text_FiniSeed, MSGBOX_DEFAULT
	giveitem ITEM_MISTY_SEED
	release
	end

TapuIsle_EventScript_TapuDone::
	release
	end

@ ---------------------------------------------------------------- trainers (lv 67-70)
TapuIsle_EventScript_Kaimana::
	trainerbattle_single TRAINER_BLACK_BELT_KAIMANA, TapuIsle_Text_KaimanaIntro, TapuIsle_Text_KaimanaDefeat
	msgbox TapuIsle_Text_KaimanaPost, MSGBOX_AUTOCLOSE
	end

TapuIsle_EventScript_Leilani::
	trainerbattle_single TRAINER_AROMA_LADY_LEILANI, TapuIsle_Text_LeilaniIntro, TapuIsle_Text_LeilaniDefeat
	msgbox TapuIsle_Text_LeilaniPost, MSGBOX_AUTOCLOSE
	end

TapuIsle_EventScript_Makoa::
	trainerbattle_single TRAINER_RANGER_MAKOA, TapuIsle_Text_MakoaIntro, TapuIsle_Text_MakoaDefeat
	msgbox TapuIsle_Text_MakoaPost, MSGBOX_AUTOCLOSE
	end

TapuIsle_EventScript_Nalu::
	trainerbattle_single TRAINER_EXPERT_NALU, TapuIsle_Text_NaluIntro, TapuIsle_Text_NaluDefeat
	msgbox TapuIsle_Text_NaluPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders)
TapuIsle_Text_Fog:
	.string "A wall of fog rolls in from nowhere.\p"
	.string "Somewhere inside it, something\n"
	.string "crackles. A voice, very bored:\p"
	.string "“Come back when you're CHAMPION.\n"
	.string "We don't do tourists. Much.”$"

TapuIsle_Text_KahunaIntro:
	.string "Welcome to TAPU ISLE. I am the\n"
	.string "kahuna. It means “the man who owns\l"
	.string "the only chair”.\p"
	.string "Four guardians live here. They guard\n"
	.string "the island from tourists.\l"
	.string "They are losing.\p"
	.string "First, wake TAPU KOKO in the ruin to\n"
	.string "the north-east. He's the needy one.\p"
	.string "The others only get up once he's had\n"
	.string "his fight. It's a seniority thing.$"

TapuIsle_Text_KahunaLele:
	.string "KOKO is satisfied. Insufferable,\n"
	.string "but satisfied.\p"
	.string "Now TAPU LELE is awake, in the\n"
	.string "flower garden to the south-east.\p"
	.string "She sprinkles scales that heal you.\n"
	.string "Then she hits you. It's a whole\l"
	.string "business model.$"

TapuIsle_Text_KahunaBulu:
	.string "TAPU BULU is up. North-west, in the\n"
	.string "thickest part of the jungle.\p"
	.string "He is the lazy one. He has been\n"
	.string "asleep since the island was a rock.\l"
	.string "Don't make him get up twice.$"

TapuIsle_Text_KahunaFini:
	.string "Last one. TAPU FINI, in the lagoon\n"
	.string "to the south-west. You'll have to\l"
	.string "swim. She refuses to come ashore.\p"
	.string "She says the fog is self-care.$"

TapuIsle_Text_KahunaAllDone:
	.string "All four guardians, in one week.\n"
	.string "Nobody has ever done that.\p"
	.string "Mostly because nobody ever asked.\n"
	.string "They're going to be unbearable at\l"
	.string "the next island meeting.$"

TapuIsle_Text_Tablet:
	.string "An old stone tablet. Four symbols:\n"
	.string "a bolt, a flower, a horn, a wave.\p"
	.string "Below, in fresh chalk:\n"
	.string "“KOKO FIRST. THEN LELE. THEN BULU.\l"
	.string "THEN FINI. NO CUTTING IN LINE.”$"

TapuIsle_Text_StatueKoko:
	.string "A stone TAPU KOKO. Someone carved\n"
	.string "“KOKO FIRST” into the base. Twice.\p"
	.string "The handwriting looks suspiciously\n"
	.string "like lightning.$"

TapuIsle_Text_StatueLele:
	.string "A stone TAPU LELE. Touching it cures\n"
	.string "your headache.\p"
	.string "And then gives you a slightly\n"
	.string "different one. Free of charge.$"

TapuIsle_Text_StatueBulu:
	.string "A stone TAPU BULU. Even carved in\n"
	.string "rock, it looks like it would rather\l"
	.string "be asleep. Relatable.$"

TapuIsle_Text_StatueFini:
	.string "A stone TAPU FINI. The base is damp.\p"
	.string "It hasn't rained here in a month.\n"
	.string "Nobody asks questions anymore.$"

TapuIsle_Text_Tourist:
	.string "I booked “an authentic island\n"
	.string "experience with the locals”.\p"
	.string "The locals are gods. One of them\n"
	.string "electrocuted my selfie stick.\l"
	.string "Five stars. Would get struck again.$"

TapuIsle_Text_DaisFog:
	.string "An old altar, scorched black.\n"
	.string "It smells like a burnt-out fuse.$"

TapuIsle_Text_DaisAsleep:
	.string "An old altar. Something here is\n"
	.string "asleep, and it would like to stay\l"
	.string "that way until it's its turn.$"

TapuIsle_Text_DaisEmpty:
	.string "The altar is empty. Its guardian\n"
	.string "is out. Probably sulking.$"

TapuIsle_Text_TapuKoko:
	.string "TAPU KOKO is sitting on the altar,\n"
	.string "crackling with static.\p"
	.string "It has clearly been waiting for a\n"
	.string "challenger for a very long time.\l"
	.string "It looks offended that it's you.$"

TapuIsle_Text_TapuLele:
	.string "TAPU LELE floats over the flowers,\n"
	.string "dusting everything in glittering\l"
	.string "scales.\p"
	.string "The scales heal you. Then the\n"
	.string "scales look at you. Uh-oh.$"

TapuIsle_Text_TapuBulu:
	.string "TAPU BULU is lying on the altar,\n"
	.string "half-covered in moss.\p"
	.string "It opens one eye. It rings its tail\n"
	.string "bell, very slowly, like a man\l"
	.string "who's been woken up on a Sunday.$"

TapuIsle_Text_TapuFini:
	.string "TAPU FINI hovers above the water.\n"
	.string "The fog parts around it like it\l"
	.string "pays rent.\p"
	.string "It looks at you with deep, calm\n"
	.string "disappointment.$"

TapuIsle_Text_TapuStays:
	.string "The guardian is still here.\n"
	.string "It's not going anywhere. It's\l"
	.string "literally its job.$"

TapuIsle_Text_KokoSeed:
	.string "On the altar lies a small seed that\n"
	.string "keeps zapping your fingers.$"

TapuIsle_Text_LeleSeed:
	.string "Among the flowers lies a seed that\n"
	.string "seems to know what you're thinking.$"

TapuIsle_Text_BuluSeed:
	.string "In the moss lies a seed. It's\n"
	.string "already trying to grow on you.$"

TapuIsle_Text_FiniSeed:
	.string "On the altar lies a damp seed,\n"
	.string "wrapped in a little cloud of mist.$"

TapuIsle_Text_LeleWakes:
	.string "From the south-east comes a giggle.\n"
	.string "The flowers in the garden turn\l"
	.string "their heads. All of them.$"

TapuIsle_Text_BuluWakes:
	.string "From the north-west comes a long,\n"
	.string "deep yawn. Somewhere, a tree falls\l"
	.string "over out of politeness.$"

TapuIsle_Text_FiniWakes:
	.string "The lagoon to the south-west starts\n"
	.string "to steam. Fog drifts over the water.\l"
	.string "Something is pretending not to wait.$"

TapuIsle_Text_KaimanaIntro:
	.string "I train under the lightning ruin!\n"
	.string "I got struck eleven times!\p"
	.string "I'm not sure I'm still technically\n"
	.string "alive! LET'S FIGHT!$"

TapuIsle_Text_KaimanaDefeat:
	.string "Twelve. That counts as twelve.$"

TapuIsle_Text_KaimanaPost:
	.string "TAPU KOKO only fights the strong.\n"
	.string "Also the weak. Mostly whoever's\l"
	.string "standing closest.$"

TapuIsle_Text_LeilaniIntro:
	.string "These flowers are sacred to\n"
	.string "TAPU LELE. You stepped on four.\l"
	.string "I counted.$"

TapuIsle_Text_LeilaniDefeat:
	.string "Five. You stepped on five.$"

TapuIsle_Text_LeilaniPost:
	.string "TAPU LELE's scales heal any wound.\n"
	.string "I rub them on my face daily.\l"
	.string "I'm 112 years old.$"

TapuIsle_Text_MakoaIntro:
	.string "Ranger on duty. This jungle is\n"
	.string "protected. By me, and by a god who\l"
	.string "is currently asleep.\p"
	.string "So mostly by me.$"

TapuIsle_Text_MakoaDefeat:
	.string "Please don't tell the god.$"

TapuIsle_Text_MakoaPost:
	.string "TAPU BULU sleeps for centuries.\n"
	.string "I respect that. I'd like that.\l"
	.string "I have three kids.$"

TapuIsle_Text_NaluIntro:
	.string "I've been swimming in TAPU FINI's\n"
	.string "lagoon every morning for sixty\l"
	.string "years. The fog is good for the skin.\p"
	.string "And the fists.$"

TapuIsle_Text_NaluDefeat:
	.string "Hmph. The fog let you win.$"

TapuIsle_Text_NaluPost:
	.string "TAPU FINI never leaves the water.\n"
	.string "Smart girl. Land is overrated.$"
