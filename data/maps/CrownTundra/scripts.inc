@ Project Grounded: CrownTundra (gegenereerd door tools/grounded/maptools/calyrex_quest.py; niet met de hand bewerken, teksten via de Dialoogstudio)
CrownTundra_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CrownTundra_EventScript_OnTransition
	.byte 0

CrownTundra_EventScript_OnTransition:
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	goto_if_unset FLAG_NATIONAL_PARK_DONE, CrownTundra_EventScript_OnTransitionEnd
	call_if_unset FLAG_CROWN_CALYREX_DONE, CrownTundra_EventScript_ShowCalyrex
	goto_if_unset FLAG_CROWN_QUEST_STARTED, CrownTundra_EventScript_OnTransitionEnd
	call_if_unset FLAG_CROWN_CHOSE_GLASTRIER, CrownTundra_EventScript_ShowGlastrier
	call_if_unset FLAG_CROWN_CHOSE_SPECTRIER, CrownTundra_EventScript_ShowSpectrier
CrownTundra_EventScript_OnTransitionEnd:
	end

CrownTundra_EventScript_ShowCalyrex:
	clearflag FLAG_TEMP_1
	return

CrownTundra_EventScript_ShowGlastrier:
	clearflag FLAG_TEMP_2
	return

CrownTundra_EventScript_ShowSpectrier:
	clearflag FLAG_TEMP_3
	return

CrownTundra_EventScript_Calyrex::
	lock
	faceplayer
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	waitmoncry
	goto_if_set FLAG_CROWN_STEED_DONE, CrownTundra_EventScript_CalyrexReins
	goto_if_set FLAG_CROWN_QUEST_STARTED, CrownTundra_EventScript_CalyrexWaiting
	msgbox CrownTundra_Text_CalyrexIntro, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_CROWN_QUEST_STARTED
	clearflag FLAG_TEMP_2
	clearflag FLAG_TEMP_3
	addobject LOCALID_CROWN_TUNDRA_GLASTRIER
	addobject LOCALID_CROWN_TUNDRA_SPECTRIER
	playmoncry SPECIES_GLASTRIER, CRY_MODE_NORMAL
	waitmoncry
	playmoncry SPECIES_SPECTRIER, CRY_MODE_NORMAL
	waitmoncry
	msgbox CrownTundra_Text_CalyrexTask, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_CalyrexWaiting:
	msgbox CrownTundra_Text_CalyrexWaiting, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_CalyrexReins:
	goto_if_set FLAG_RECEIVED_REINS_OF_UNITY, CrownTundra_EventScript_CalyrexBattle
	msgbox CrownTundra_Text_CalyrexReunited, MSGBOX_DEFAULT
	giveitem ITEM_REINS_OF_UNITY
	setflag FLAG_RECEIVED_REINS_OF_UNITY
CrownTundra_EventScript_CalyrexBattle:
	msgbox CrownTundra_Text_CalyrexChallenge, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CALYREX, 88
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CrownTundra_EventScript_CalyrexCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, CrownTundra_EventScript_CalyrexDefeated
	release
	end

CrownTundra_EventScript_CalyrexDefeated:
	msgbox CrownTundra_Text_CalyrexDefeated, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_CalyrexCaught:
	removeobject LOCALID_CROWN_TUNDRA_CALYREX
	setflag FLAG_CROWN_CALYREX_DONE
	msgbox CrownTundra_Text_CalyrexCaught, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_Altar::
	msgbox CrownTundra_Text_Altar, MSGBOX_SIGN
	end

CrownTundra_EventScript_Glastrier::
	lock
	faceplayer
	playmoncry SPECIES_GLASTRIER, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox CrownTundra_Text_GlastrierLook, MSGBOX_DEFAULT
	msgbox CrownTundra_Text_GlastrierBattle, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_GLASTRIER, 86
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CrownTundra_EventScript_GlastrierLater
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CrownTundra_EventScript_GlastrierLater
	removeobject LOCALID_CROWN_TUNDRA_GLASTRIER
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CrownTundra_EventScript_GlastrierCaught
	msgbox CrownTundra_Text_GlastrierFled, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_GlastrierCaught:
	setflag FLAG_CROWN_CHOSE_GLASTRIER
	setflag FLAG_CROWN_STEED_DONE
	msgbox CrownTundra_Text_GlastrierCaught, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_GlastrierLater:
	release
	end

CrownTundra_EventScript_Spectrier::
	lock
	faceplayer
	playmoncry SPECIES_SPECTRIER, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox CrownTundra_Text_SpectrierLook, MSGBOX_DEFAULT
	msgbox CrownTundra_Text_SpectrierBattle, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_SPECTRIER, 86
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, CrownTundra_EventScript_SpectrierLater
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, CrownTundra_EventScript_SpectrierLater
	removeobject LOCALID_CROWN_TUNDRA_SPECTRIER
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CrownTundra_EventScript_SpectrierCaught
	msgbox CrownTundra_Text_SpectrierFled, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_SpectrierCaught:
	setflag FLAG_CROWN_CHOSE_SPECTRIER
	setflag FLAG_CROWN_STEED_DONE
	msgbox CrownTundra_Text_SpectrierCaught, MSGBOX_DEFAULT
	release
	end

CrownTundra_EventScript_SpectrierLater:
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
CrownTundra_Text_Altar:
	.string "A crumbling shrine, half buried in snow.\n"
	.string "Carved into the stone: a crowned head\l"
	.string "and two horses, one of which is clearly\l"
	.string "being difficult.\p"
	.string "Someone left a carrot on the altar. It\n"
	.string "is frozen solid. It has been here longer\l"
	.string "than you have been alive.$"

CrownTundra_Text_CalyrexIntro:
	.string "CALYREX: Ah. The trainer from the park.\n"
	.string "You found my shrine. It used to be\l"
	.string "grander. It used to have a roof.\p"
	.string "I have a task for you, which you will\n"
	.string "accept, because I am a king and you are\l"
	.string "a person holding a bicycle.\p"
	.string "My steeds have wandered off.\n"
	.string "GLASTRIER, who is strong and stubborn,\l"
	.string "and SPECTRIER, who is fast and afraid\l"
	.string "of everything. Including me. Especially\l"
	.string "me.$"

CrownTundra_Text_CalyrexTask:
	.string "CALYREX: A king rides one horse at a\n"
	.string "time. That is a rule. Owning two is not\l"
	.string "against the rule. I checked. I wrote it.\p"
	.string "Go into the field and bring me my\n"
	.string "steeds. One will do for the REINS. Both\l"
	.string "would be greedy. You look greedy.$"

CrownTundra_Text_CalyrexWaiting:
	.string "CALYREX: The big one sulks on the ice to\n"
	.string "the west. The nervous one hides\l"
	.string "between the dark trees. I would fetch\l"
	.string "them myself, but I am very small and\l"
	.string "very royal.$"

CrownTundra_Text_CalyrexReunited:
	.string "CALYREX: You caught my steed. In a ball.\n"
	.string "With my steed inside it. I see.\p"
	.string "No matter. Take these REINS OF UNITY.\n"
	.string "With them, my steed and I become one. It\l"
	.string "is very majestic and only slightly\l"
	.string "uncomfortable for the horse.$"

CrownTundra_Text_CalyrexChallenge:
	.string "CALYREX: Reins are useless without a\n"
	.string "king attached. Show me you are worthy\l"
	.string "of carrying one around in your pocket.\p"
	.string "I will not go easy on you. I have been in\n"
	.string "a ball before, in another dimension. It\l"
	.string "was humbling. I did not enjoy being\l"
	.string "humbled.$"

CrownTundra_Text_CalyrexDefeated:
	.string "CALYREX picks itself up and\n"
	.string "straightens its crown.\p"
	.string "CALYREX: That did not happen. We will do\n"
	.string "it again, whenever you are ready. I can\l"
	.string "wait. Waiting is mostly what kings do.$"

CrownTundra_Text_CalyrexCaught:
	.string "You caught CALYREX! Use the REINS OF\n"
	.string "UNITY from your bag while CALYREX and\l"
	.string "its steed are both in your party.\p"
	.string "From inside the ball, faintly: “This is\n"
	.string "beneath me. Literally. You put the ball\l"
	.string "on the floor.”$"

CrownTundra_Text_GlastrierLook:
	.string "A massive white horse made mostly of\n"
	.string "muscle and ice stares you down. It\l"
	.string "snorts. Somewhere, a small avalanche\l"
	.string "happens.\p"
	.string "CALYREX (in your head): That is\n"
	.string "GLASTRIER. Strong. Stubborn. Has never\l"
	.string "once listened to me.$"

CrownTundra_Text_GlastrierBattle:
	.string "GLASTRIER lowers its head. That is not\n"
	.string "a bow.$"

CrownTundra_Text_GlastrierCaught:
	.string "You caught GLASTRIER!\p"
	.string "CALYREX: Bring it to the shrine. Gently.\n"
	.string "It bites.$"

CrownTundra_Text_GlastrierFled:
	.string "GLASTRIER stomps off into the snow,\n"
	.string "humiliated. It will be back: it left its\l"
	.string "dignity here and it wants it back.$"

CrownTundra_Text_SpectrierLook:
	.string "A thin black horse flickers between the\n"
	.string "trees, half here and half somewhere\l"
	.string "worse. It looks at you as if YOU are the\l"
	.string "ghost.\p"
	.string "CALYREX (in your head): That is\n"
	.string "SPECTRIER. Fast. Shy. Once fled from its\l"
	.string "own shadow, and then from the shadow\l"
	.string "of its shadow.$"

CrownTundra_Text_SpectrierBattle:
	.string "SPECTRIER panics. Panicking is how it\n"
	.string "fights.$"

CrownTundra_Text_SpectrierCaught:
	.string "You caught SPECTRIER!\p"
	.string "CALYREX: Bring it to the shrine. Quietly.\n"
	.string "Loud noises make it phase through the\l"
	.string "floor.$"

CrownTundra_Text_SpectrierFled:
	.string "SPECTRIER dissolves in fright. It will\n"
	.string "come back. It always comes back.\l"
	.string "Usually right behind you.$"
