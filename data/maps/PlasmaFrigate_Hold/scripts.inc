@ Project Grounded: Plasma Frigate, ruim/vrieslab (kopie van de S.S. Tidal-laaddek). Kaart: tools/grounded/maptools/plasma_frigate.py
@ Zinzolin + Rood (dubbel; met één bruikbare Pokémon na elkaar), dan Genesect (lv 70, eigen transitie en muziek via de
@ soort in GetWildBattleTransition/pokemon.c). Daarna de vier Drives en de bazen smeren 'm (VAR_PLASMA_FRIGATE 8).
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
PlasmaFrigate_Hold_MapScripts::
	.byte 0

PlasmaFrigate_Hold_EventScript_Bosses::
	lock
	faceplayer
	goto_if_ge VAR_PLASMA_FRIGATE, 7, PlasmaFrigate_Hold_EventScript_BossesBeaten
	msgbox PlasmaFrigate_Hold_Text_ZinzolinIntro, MSGBOX_DEFAULT
	msgbox PlasmaFrigate_Hold_Text_RoodIntro, MSGBOX_DEFAULT
	closemessage
	specialvar VAR_RESULT, GetMonsStateToDoubles
	goto_if_eq VAR_RESULT, PLAYER_HAS_TWO_USABLE_MONS, PlasmaFrigate_Hold_EventScript_BossesDouble
	msgbox PlasmaFrigate_Hold_Text_OneMon, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PLASMA_ZINZOLIN, PlasmaFrigate_Hold_Text_ZinzolinDefeat
	trainerbattle_no_intro TRAINER_PLASMA_ROOD, PlasmaFrigate_Hold_Text_RoodDefeat
	goto PlasmaFrigate_Hold_EventScript_BossesDefeated

PlasmaFrigate_Hold_EventScript_BossesDouble::
	trainerbattle_two_trainers TRAINER_PLASMA_ZINZOLIN, PlasmaFrigate_Hold_Text_ZinzolinDefeat, TRAINER_PLASMA_ROOD, PlasmaFrigate_Hold_Text_RoodDefeat
PlasmaFrigate_Hold_EventScript_BossesDefeated::
	setvar VAR_PLASMA_FRIGATE, 7
	msgbox PlasmaFrigate_Hold_Text_BossesDefeated, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Hold_EventScript_BossesBeaten::
	msgbox PlasmaFrigate_Hold_Text_BossesBeaten, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Hold_EventScript_Genesect::
	lock
	goto_if_lt VAR_PLASMA_FRIGATE, 7, PlasmaFrigate_Hold_EventScript_GenesectGuarded
	msgbox PlasmaFrigate_Hold_Text_TargetAcquired, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_GENESECT, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_GENESECT, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, PlasmaFrigate_Hold_EventScript_GenesectStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, PlasmaFrigate_Hold_EventScript_GenesectStays
	removeobject LOCALID_PLASMA_GENESECT
	setflag FLAG_HIDE_NEW_MAUVILLE_GENESECT
	msgbox PlasmaFrigate_Hold_Text_RoodAfter, MSGBOX_DEFAULT
	msgbox PlasmaFrigate_Hold_Text_ZinzolinDrives, MSGBOX_DEFAULT
	additem ITEM_BURN_DRIVE
	additem ITEM_CHILL_DRIVE
	additem ITEM_DOUSE_DRIVE
	additem ITEM_SHOCK_DRIVE
	playfanfare MUS_OBTAIN_ITEM
	message PlasmaFrigate_Hold_Text_GotDrives
	waitmessage
	waitfanfare
	msgbox PlasmaFrigate_Hold_Text_Flee, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_PLASMA_ZINZOLIN
	removeobject LOCALID_PLASMA_ROOD
	setflag FLAG_HIDE_PLASMA_BOSSES
	setvar VAR_PLASMA_FRIGATE, 8
	fadescreen FADE_FROM_WHITE
	msgbox PlasmaFrigate_Hold_Text_AfterFlee, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Hold_EventScript_GenesectStays::
	release
	end

PlasmaFrigate_Hold_EventScript_GenesectGuarded::
	msgbox PlasmaFrigate_Hold_Text_GenesectGuarded, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Hold_EventScript_Console::
	msgbox PlasmaFrigate_Hold_Text_Console, MSGBOX_SIGN
	end

PlasmaFrigate_Hold_Text_ZinzolinIntro:
	.string "ZINZOLIN: You! The child who\n"
	.string "reads other people's laptops!\p"
	.string "This ancient POKéMON will be the\n"
	.string "centerpiece of NEO TEAM PLASMA.\p"
	.string "Frozen. Forever. Like a nice\n"
	.string "ice sculpture at a wedding.$"

PlasmaFrigate_Hold_Text_RoodIntro:
	.string "ROOD: I only came to make sure it\n"
	.string "had a blanket.\p"
	.string "But you did break into our ship.\n"
	.string "So. Gently. With love. We fight.$"

PlasmaFrigate_Hold_Text_OneMon:
	.string "ZINZOLIN: One POKéMON? Then we\n"
	.string "take turns. Like civilized villains.$"

PlasmaFrigate_Hold_Text_ZinzolinDefeat:
	.string "Defeated… and STILL cold.$"

PlasmaFrigate_Hold_Text_RoodDefeat:
	.string "A wonderful battle. I'll write you\n"
	.string "a strongly worded letter. Kindly.$"

PlasmaFrigate_Hold_Text_BossesDefeated:
	.string "ZINZOLIN: Fine! Take a look at the\n"
	.string "bug. It's been in the freezer for\l"
	.string "three days. It's in a mood.$"

PlasmaFrigate_Hold_Text_BossesBeaten:
	.string "ROOD: Go on. Say hello.\n"
	.string "Use your indoor voice.$"

PlasmaFrigate_Hold_Text_GenesectGuarded:
	.string "ZINZOLIN: Ah, ah! No touching the\n"
	.string "merchandise.$"

PlasmaFrigate_Hold_Text_TargetAcquired:
	.string "The freezer capsule cracks.\n"
	.string "Every screen in the hold turns red.\p"
	.string "TARGET ACQUIRED.\n"
	.string "TARGET: YOU.\p"
	.string "HASTA LA VISTA, BABY.$"

PlasmaFrigate_Hold_Text_RoodAfter:
	.string "ROOD: …Well. It's out of the\n"
	.string "freezer. That's growth.$"

PlasmaFrigate_Hold_Text_ZinzolinDrives:
	.string "ZINZOLIN: Take the Drives. Without\n"
	.string "the bug they're just very expensive\l"
	.string "coasters.$"

PlasmaFrigate_Hold_Text_GotDrives:
	.string "{PLAYER} received the BURN DRIVE,\n"
	.string "CHILL DRIVE, DOUSE DRIVE and\l"
	.string "SHOCK DRIVE!$"

PlasmaFrigate_Hold_Text_Flee:
	.string "ZINZOLIN: NEO TEAM PLASMA will\n"
	.string "return! In a warmer ship!\p"
	.string "ROOD: Leave the frigate. It has\n"
	.string "a lovely sauna. It's the engine room.$"

PlasmaFrigate_Hold_Text_AfterFlee:
	.string "They're gone. The ship is yours now.\p"
	.string "Legally, that makes you a pirate.$"

PlasmaFrigate_Hold_Text_Console:
	.string "The freezer console. Four slots\n"
	.string "shaped like Drives, labeled RED,\l"
	.string "BLUE, WHITE and YELLOW.\p"
	.string "Very helpful. Thank you, someone.$"
