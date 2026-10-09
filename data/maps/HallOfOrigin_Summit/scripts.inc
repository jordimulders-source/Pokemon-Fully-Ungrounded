@ Project Grounded: HallOfOrigin_Summit (tools/grounded/maptools/hall_of_origin.py)
HallOfOrigin_Summit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, HallOfOrigin_Summit_OnTransition
	.byte 0

HallOfOrigin_Summit_EventScript_Ordo::
	trainerbattle_single TRAINER_HOO_ORDO, HallOfOrigin_Summit_Text_OrdoIntro, HallOfOrigin_Summit_Text_OrdoDefeat
	msgbox HallOfOrigin_Summit_Text_OrdoPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Summit_EventScript_Kairos::
	trainerbattle_single TRAINER_HOO_KAIROS, HallOfOrigin_Summit_Text_KairosIntro, HallOfOrigin_Summit_Text_KairosDefeat
	msgbox HallOfOrigin_Summit_Text_KairosPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Summit_OnTransition:
	getcaughtmon SPECIES_ARCEUS
	call_if_ne VAR_RESULT, 0, HallOfOrigin_Summit_EventScript_HideArceus
	call_if_eq VAR_RESULT, 0, HallOfOrigin_Summit_EventScript_ShowArceus
	end

HallOfOrigin_Summit_EventScript_HideArceus:
	setflag FLAG_HIDE_HALL_ARCEUS
	return

HallOfOrigin_Summit_EventScript_ShowArceus:
	clearflag FLAG_HIDE_HALL_ARCEUS
	return

HallOfOrigin_Summit_EventScript_CountOne:
	addvar VAR_0x8005, 1
	return

HallOfOrigin_Summit_EventScript_Arceus::
	lock
	setvar VAR_0x8005, 0
	call_if_defeated TRAINER_HOO_STRATOS, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_THALASSA, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_BEDROCK, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_NOUS, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_SOMNIA, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_GLADIUS, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_HEPHAEST, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_ORDO, HallOfOrigin_Summit_EventScript_CountOne
	call_if_defeated TRAINER_HOO_KAIROS, HallOfOrigin_Summit_EventScript_CountOne
	goto_if_ne VAR_0x8005, 9, HallOfOrigin_Summit_EventScript_ArceusNotYet
	goto_if_set FLAG_HALL_ARCEUS_DONE, HallOfOrigin_Summit_EventScript_ArceusAgain
	msgbox HallOfOrigin_Summit_Text_ArceusGreeting, MSGBOX_DEFAULT
	goto HallOfOrigin_Summit_EventScript_ArceusBattle

HallOfOrigin_Summit_EventScript_ArceusAgain:
	msgbox HallOfOrigin_Summit_Text_ArceusAgain, MSGBOX_DEFAULT
HallOfOrigin_Summit_EventScript_ArceusBattle:
	closemessage
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox HallOfOrigin_Summit_Text_ArceusHeals, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ARCEUS, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, HallOfOrigin_Summit_EventScript_ArceusWaits
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, HallOfOrigin_Summit_EventScript_ArceusWaits
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, HallOfOrigin_Summit_EventScript_ArceusCaught
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_HALL_ARCEUS
	fadescreen FADE_FROM_WHITE
	call_if_unset FLAG_HALL_ARCEUS_DONE, HallOfOrigin_Summit_EventScript_Epilogue
	msgbox HallOfOrigin_Summit_Text_ArceusDefeated, MSGBOX_DEFAULT
	release
	end

HallOfOrigin_Summit_EventScript_ArceusCaught:
	removeobject LOCALID_HALL_ARCEUS
	setflag FLAG_HIDE_HALL_ARCEUS
	call_if_unset FLAG_HALL_ARCEUS_DONE, HallOfOrigin_Summit_EventScript_Epilogue
	msgbox HallOfOrigin_Summit_Text_ArceusCaught, MSGBOX_DEFAULT
	release
	end

HallOfOrigin_Summit_EventScript_Epilogue:
	setflag FLAG_HALL_ARCEUS_DONE
	msgbox HallOfOrigin_Summit_Text_Epilogue, MSGBOX_DEFAULT
	return

HallOfOrigin_Summit_EventScript_ArceusWaits:
	msgbox HallOfOrigin_Summit_Text_ArceusWaits, MSGBOX_DEFAULT
	release
	end

HallOfOrigin_Summit_EventScript_ArceusNotYet:
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox HallOfOrigin_Summit_Text_ArceusNotYet, MSGBOX_DEFAULT
	release
	end

HallOfOrigin_Summit_EventScript_Altar::
	msgbox HallOfOrigin_Summit_Text_Altar, MSGBOX_DEFAULT
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
HallOfOrigin_Summit_Text_OrdoIntro:
	.string "Emissary of order. My POKéMON built this\n"
	.string "hall. Stone by stone. Then they built\l"
	.string "themselves.\p"
	.string "Then they argued about it for three\n"
	.string "thousand years.$"

HallOfOrigin_Summit_Text_OrdoDefeat:
	.string "Order... restored? No. Disrupted. By you.\n"
	.string "Great.$"

HallOfOrigin_Summit_Text_OrdoPost:
	.string "REGIGIGAS is slow to start. So was\n"
	.string "creation. Look how that turned out.$"

HallOfOrigin_Summit_Text_KairosIntro:
	.string "Emissary of time and space. I am the\n"
	.string "right moment, in the right place.\p"
	.string "You are neither. Let's fix that.$"

HallOfOrigin_Summit_Text_KairosDefeat:
	.string "That... was the right moment. Just not\n"
	.string "for me.$"

HallOfOrigin_Summit_Text_KairosPost:
	.string "ARCEUS is waiting at the altar. It has\n"
	.string "been waiting since before waiting was\l"
	.string "invented.$"

HallOfOrigin_Summit_Text_ArceusGreeting:
	.string "ARCEUS: So. You came.\p"
	.string "Every legend in every dimension,\n"
	.string "accounted for. You even brought the\l"
	.string "flute back. Most people lose it in a\l"
	.string "sofa.\p"
	.string "I made the world. Let us see what the\n"
	.string "world made.$"

HallOfOrigin_Summit_Text_ArceusAgain:
	.string "ARCEUS: Again? Good. I was getting\n"
	.string "bored, and I invented boredom.$"

HallOfOrigin_Summit_Text_ArceusHeals:
	.string "A warm light washes over your team.\p"
	.string "ARCEUS: There. Now nobody can say it\n"
	.string "wasn't fair.$"

HallOfOrigin_Summit_Text_ArceusDefeated:
	.string "ARCEUS dissolves into a thousand\n"
	.string "plates of light.\p"
	.string "ARCEUS: A draw, on my scale. I'll be here.\n"
	.string "I'm always here. Come back with a ball\l"
	.string "you believe in.$"

HallOfOrigin_Summit_Text_ArceusCaught:
	.string "The ball doesn't even wobble. It just...\n"
	.string "accepts it.\p"
	.string "Somewhere, the universe files a change\n"
	.string "of address.$"

HallOfOrigin_Summit_Text_Epilogue:
	.string "For a moment, everything is very quiet.\n"
	.string "Time stops ticking. Space stops being\l"
	.string "big.\p"
	.string "Then a voice, from everywhere at once:\p"
	.string "ARCEUS: Thank you for playing.\p"
	.string "...It means the game. The world. Both. Go\n"
	.string "home. Have a sandwich. You've earned it.$"

HallOfOrigin_Summit_Text_ArceusWaits:
	.string "ARCEUS: You ran. That's fine. I have all\n"
	.string "the time there is. Literally.$"

HallOfOrigin_Summit_Text_ArceusNotYet:
	.string "ARCEUS watches you from the altar.\p"
	.string "ARCEUS: My emissaries have opinions\n"
	.string "about you. {STR_VAR_1} of nine have shared\l"
	.string "theirs.\p"
	.string "Hear the rest. Then we talk.$"

HallOfOrigin_Summit_Text_Altar:
	.string "An altar of white stone. It hums at a\n"
	.string "frequency only very old things can\l"
	.string "hear.$"
