@ Project Grounded: Fortree Jungle (kaart: tools/grounded/maptools/fortree_jungle.py)
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
@ Vrijgehouden: de open plek van Zarude (zuidwest) en het masker-altaar van Ogerpon (zuidoost).

FortreeJungle_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, FortreeJungle_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeJungle_OnTransition
	.byte 0

@ Project Grounded: Rocket-sidequest. De holte in de reuzenpalm (18, 59) is pas open als de quest loopt
@ (VAR_ROCKET_QUEST >= 2); de wachtpost staat er alleen zolang Petrel de ZONE KEYS nog heeft.
FortreeJungle_OnLoad:
	call_if_ge VAR_ROCKET_QUEST, 2, FortreeJungle_EventScript_OpenRocketHollow
	end

FortreeJungle_EventScript_OpenRocketHollow::
	setmetatile 18, 59, METATILE_FortreeJungle_RocketHollow, FALSE
	return

FortreeJungle_OnTransition:
	setflag FLAG_HIDE_JUNGLE_ROCKET_GUARD
	setflag FLAG_HIDE_FORTREE_JUNGLE_ZARUDE
	call_if_set FLAG_SYS_GAME_CLEAR, FortreeJungle_EventScript_ArmZarude
	call_if_eq VAR_ROCKET_QUEST, 2, FortreeJungle_EventScript_ShowRocketGuard
	end

FortreeJungle_EventScript_ShowRocketGuard::
	clearflag FLAG_HIDE_JUNGLE_ROCKET_GUARD
	return

FortreeJungle_EventScript_RocketGuard::
	trainerbattle_single TRAINER_ROCKET_GUARD, FortreeJungle_Text_RocketGuardIntro, FortreeJungle_Text_RocketGuardDefeat
	msgbox FortreeJungle_Text_RocketGuardPostBattle, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- trainers
FortreeJungle_EventScript_Bram::
	trainerbattle_single TRAINER_JUNGLE_BRAM, FortreeJungle_Text_BramIntro, FortreeJungle_Text_BramDefeat
	msgbox FortreeJungle_Text_BramPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeJungle_EventScript_Maya::
	trainerbattle_single TRAINER_JUNGLE_MAYA, FortreeJungle_Text_MayaIntro, FortreeJungle_Text_MayaDefeat
	msgbox FortreeJungle_Text_MayaPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeJungle_EventScript_Hanzo::
	trainerbattle_single TRAINER_JUNGLE_HANZO, FortreeJungle_Text_HanzoIntro, FortreeJungle_Text_HanzoDefeat
	msgbox FortreeJungle_Text_HanzoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeJungle_EventScript_Flora::
	trainerbattle_single TRAINER_JUNGLE_FLORA, FortreeJungle_Text_FloraIntro, FortreeJungle_Text_FloraDefeat
	msgbox FortreeJungle_Text_FloraPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeJungle_EventScript_Dirk::
	trainerbattle_single TRAINER_JUNGLE_DIRK, FortreeJungle_Text_DirkIntro, FortreeJungle_Text_DirkDefeat
	msgbox FortreeJungle_Text_DirkPostBattle, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- Ogerpon (placeholder) en Zarude (placeholder)
FortreeJungle_EventScript_MaskKeeper::
	msgbox FortreeJungle_Text_MaskKeeper, MSGBOX_NPC
	end

FortreeJungle_EventScript_MaskAltar::
	msgbox FortreeJungle_Text_MaskAltar, MSGBOX_SIGN
	end

FortreeJungle_EventScript_ZarudeSign::
	msgbox FortreeJungle_Text_ZarudeSign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- Zarude (post-game)
@ Na de Hall of Fame zit Zarude verstopt in de boomkruin achter het stenen plateau in de ruine (9, 65). Stap je op de
@ vloerplaat voor het plateau (9, 62), dan springt hij via het plateau naar je toe. Verslagen = terug na de League
@ (hall_of_fame.inc), gevangen = weg. VAR_TEMP_4 = 1 zet de coord-trigger aan.
FortreeJungle_EventScript_ArmZarude::
	goto_if_set FLAG_DEFEATED_ZARUDE, FortreeJungle_EventScript_Return
	setvar VAR_TEMP_4, 1
FortreeJungle_EventScript_Return::
	return

FortreeJungle_EventScript_ZarudeScene::
	lockall
	setvar VAR_TEMP_4, 0
	applymovement LOCALID_PLAYER, Common_Movement_FaceDown
	waitmovement 0
	playse SE_M_GRASSWHISTLE
	msgbox FortreeJungle_Text_ZarudeRustle, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_FORTREE_JUNGLE_ZARUDE
	addobject LOCALID_FORTREE_JUNGLE_ZARUDE
	playmoncry SPECIES_ZARUDE, CRY_MODE_ENCOUNTER
	applymovement LOCALID_FORTREE_JUNGLE_ZARUDE, FortreeJungle_Movement_ZarudeLeaps
	waitmovement 0
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 6
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	waitmoncry
	msgbox FortreeJungle_Text_Zarude, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_ZARUDE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FortreeJungle_EventScript_ZarudeCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FortreeJungle_EventScript_ZarudeDefeated
	@ gevlucht: Zarude springt terug de boom in en wacht op je volgende bezoek
	applymovement LOCALID_FORTREE_JUNGLE_ZARUDE, FortreeJungle_Movement_ZarudeRetreats
	waitmovement 0
	removeobject LOCALID_FORTREE_JUNGLE_ZARUDE
	setflag FLAG_HIDE_FORTREE_JUNGLE_ZARUDE
	msgbox FortreeJungle_Text_ZarudeRetreats, MSGBOX_DEFAULT
	releaseall
	end

FortreeJungle_EventScript_ZarudeCaught::
	setflag FLAG_CAUGHT_ZARUDE
FortreeJungle_EventScript_ZarudeDefeated::
	setflag FLAG_DEFEATED_ZARUDE
	removeobject LOCALID_FORTREE_JUNGLE_ZARUDE
	setflag FLAG_HIDE_FORTREE_JUNGLE_ZARUDE
	releaseall
	end

FortreeJungle_Movement_ZarudeLeaps:
	jump_up
	delay_4
	jump_up
	jump_in_place_up
	step_end

FortreeJungle_Movement_ZarudeRetreats:
	jump_down
	jump_down
	step_end

@ Mangrove Mire: andere tileset, dus geen naadloze connectie maar een warp
FortreeJungle_EventScript_ToMangroveMire::
	warpsilent MAP_MANGROVE_MIRE, 1, 22
	waitstate
	end

@ ---------------------------------------------------------------- teksten
FortreeJungle_Text_BramIntro:
	.string "I've been out here for three weeks.\n"
	.string "I came for one Heracross.\p"
	.string "The mosquitoes caught me first.$"

FortreeJungle_Text_BramDefeat:
	.string "I'm donating the rest of my blood\n"
	.string "to the local wildlife.$"

FortreeJungle_Text_BramPostBattle:
	.string "Fun fact: everything in this jungle\n"
	.string "is either poisonous or offended.$"

FortreeJungle_Text_MayaIntro:
	.string "Ranger rule number one: never leave\n"
	.string "the path.\p"
	.string "Ranger rule number two: there is\n"
	.string "no path. Good luck!$"

FortreeJungle_Text_MayaDefeat:
	.string "I'll write you a ticket for\n"
	.string "trampling protected moss.$"

FortreeJungle_Text_MayaPostBattle:
	.string "It hasn't stopped raining since 1987.\n"
	.string "We stopped filing weather reports.$"

FortreeJungle_Text_HanzoIntro:
	.string "You walked past me four times.\n"
	.string "I was a tree. I was a GOOD tree.$"

FortreeJungle_Text_HanzoDefeat:
	.string "A Bug Catcher tried to climb me\n"
	.string "yesterday. Worst day of my career.$"

FortreeJungle_Text_HanzoPostBattle:
	.string "Don't tell my sensei. He thinks I'm\n"
	.string "a shrub in Petalburg by now.$"

FortreeJungle_Text_FloraIntro:
	.string "Mmm, smell that? Wet leaves, rotting\n"
	.string "fruit and a hint of something dead.\p"
	.string "I bottle it and sell it in Lilycove\n"
	.string "as “Rainforest Serenity”.$"

FortreeJungle_Text_FloraDefeat:
	.string "You smell like defeat. My defeat.\n"
	.string "Notes of copper and wet dog.$"

FortreeJungle_Text_FloraPostBattle:
	.string "Fifty Pokédollars a drop. The rich\n"
	.string "people in Lilycove love it.$"

FortreeJungle_Text_DirkIntro:
	.string "Fortree? Which way is Fortree?\n"
	.string "I went in for a short hike in '98.\p"
	.string "Is there still a guy on TV who\n"
	.string "complains about the weather?$"

FortreeJungle_Text_DirkDefeat:
	.string "My Sudowoodo has been pretending to\n"
	.string "be a tree for so long, so have I.$"

FortreeJungle_Text_DirkPostBattle:
	.string "That monkey keeps stealing my map.\n"
	.string "Not my food. Just the map.\p"
	.string "I think it wants me to stay.$"

FortreeJungle_Text_MaskKeeper:
	.string "This altar once held four masks.\n"
	.string "Teal, blue, red and grey.\p"
	.string "Some ogre took them back, and she\n"
	.string "does not do customer service.\p"
	.string "Come back later. Bring snacks.\n"
	.string "And maybe a helmet.$"

FortreeJungle_Text_MaskAltar:
	.string "A mossy stone altar with four\n"
	.string "empty, mask-shaped hollows.\p"
	.string "Someone left a note: “BACK SOON.\n"
	.string "DO NOT TOUCH. I BITE.”$"

FortreeJungle_Text_ZarudeSign:
	.string "WARNING! Monkey territory.\p"
	.string "Do not feed the monkeys.\n"
	.string "Do not look the monkeys in the eye.\p"
	.string "If a monkey offers you a banana,\n"
	.string "it is not a banana.$"

@ Project Grounded: Rocket-sidequest (placeholders)
FortreeJungle_Text_RocketGuardIntro:
	.string "Halt! This is a perfectly normal\n"
	.string "giant tree. Nothing to see here.\p"
	.string "The big hole? Woodpeckers.\n"
	.string "Very big, very organized ones.$"

FortreeJungle_Text_RocketGuardDefeat:
	.string "The woodpeckers will\n"
	.string "hear about this.$"

FortreeJungle_Text_RocketGuardPostBattle:
	.string "Fine, go in. Wipe your feet.\n"
	.string "PETREL is very particular\l"
	.string "about the carpet.$"

FortreeJungle_Text_ZarudeRustle:
	.string "The canopy behind the old stones goes\n"
	.string "dead quiet.\p"
	.string "Even the mosquitoes stop. That's never\n"
	.string "a good sign.$"

FortreeJungle_Text_Zarude:
	.string "A ZARUDE drops out of the trees!\p"
	.string "It slaps the stone twice. Somewhere, a\n"
	.string "vine takes notes.$"

FortreeJungle_Text_ZarudeRetreats:
	.string "ZARUDE swings back into the canopy.\n"
	.string "It knows where you live. Roughly.$"
