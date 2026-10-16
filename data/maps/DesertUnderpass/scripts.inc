DesertUnderpass_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DesertUnderpass_OnTransition
	.byte 0

DesertUnderpass_OnTransition:
	call DesertUnderpass_EventScript_Legends2_Transition
	setflag FLAG_LANDMARK_DESERT_UNDERPASS
	end

DesertUnderpass_EventScript_Fossil::
	lock
	faceplayer
	goto_if_set FLAG_CHOSE_ROOT_FOSSIL, DesertUnderpass_EventScript_GiveClawFossil
	goto_if_set FLAG_CHOSE_CLAW_FOSSIL, DesertUnderpass_EventScript_GiveRootFossil
	release
	end

DesertUnderpass_EventScript_GiveClawFossil::
	giveitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	removeobject LOCALID_UNDERPASS_FOSSIL
	release
	end

DesertUnderpass_EventScript_GiveRootFossil::
	giveitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	removeobject LOCALID_UNDERPASS_FOSSIL
	release
	end

@ Unused
DesertUnderpass_Text_FoundRootFossil::
	.string "{PLAYER} found the ROOT FOSSIL. The\n"
	.string "root of all troubles!$"

@ Unused
DesertUnderpass_Text_FoundClawFossil::
	.string "{PLAYER} found the CLAW FOSSIL. Did you\n"
	.string "claw that one out?$"

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
DesertUnderpass_EventScript_LVArmaldo::
	lock
	msgbox DesertUnderpass_Text_LVArmaldo, MSGBOX_DEFAULT
	playmoncry SPECIES_ARMALDO, CRY_MODE_NORMAL
	waitmoncry
	msgbox DesertUnderpass_Text_LVArmaldo_Cry, MSGBOX_DEFAULT
	release
	end

DesertUnderpass_Text_LVArmaldo:
	.string "A sign on a stick: 'ARMALDO.\nPERFECTLY PRESERVED. 10,000 YEARS.\lDO NOT FEED.'$"

DesertUnderpass_Text_LVArmaldo_Cry:
	.string "...It yawned.\pSomeone has crossed out\n'DO NOT FEED' and written\l'FEED. PLEASE. IT'S ANGRY.'$"

DesertUnderpass_EventScript_LVArchaeologist::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_DESERT_UNDERPASS_MAX_REVIVE, DesertUnderpass_EventScript_LVArchaeologist_After
	msgbox DesertUnderpass_Text_LVArchaeologist, MSGBOX_DEFAULT
	giveitem ITEM_MAX_REVIVE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_DESERT_UNDERPASS_MAX_REVIVE
	release
	end
DesertUnderpass_EventScript_LVArchaeologist_After:
	msgbox DesertUnderpass_Text_LVArchaeologist_After, MSGBOX_DEFAULT
	release
	end

DesertUnderpass_Text_LVArchaeologist:
	.string "Careful! Active dig site!\pWe found a complete ARMALDO.\nTen thousand years old! Not a\lsingle bone missing!\pIt does move a bit. Rigor mortis,\nprobably. Very slow rigor mortis.\pHere. For the fossils you'll find.\nIt's the only thing that revives\lanything down here.$"

DesertUnderpass_Text_LVArchaeologist_After:
	.string "Professor HOLLIS says ARMALDO went\nextinct. So this one is in denial.\pIt ate my trowel this morning.\nFor science, I've decided.$"

DesertUnderpass_EventScript_LVHollis::
	trainerbattle_single TRAINER_ARCHAEOLOGIST_HOLLIS, DesertUnderpass_Text_LVHollis_Intro, DesertUnderpass_Text_LVHollis_Defeat
	msgbox DesertUnderpass_Text_LVHollis_Post, MSGBOX_AUTOCLOSE
	end

DesertUnderpass_Text_LVHollis_Intro:
	.string "Stop! You're stepping on the\nCretaceous!\pEvery POKeMON I own was dug out\nof a rock. They're grateful.\lMostly. One of them bites.$"

DesertUnderpass_Text_LVHollis_Defeat:
	.string "Defeated by someone from\nthe present day. How modern.$"

DesertUnderpass_Text_LVHollis_Post:
	.string "My intern thinks that ARMALDO is\nalive. Absurd. It's just resting.\pFor ten thousand years.\nLike I want to.$"
@ --- einde land_vulling ---

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
DesertUnderpass_EventScript_Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_ZYGARDE
	goto_if_set FLAG_CAUGHT_ZYGARDE, DesertUnderpass_EventScript_Legends2_TransitionEnd
	specialvar VAR_RESULT, Grounded_CaughtXerneasAndYveltal
	goto_if_eq VAR_RESULT, FALSE, DesertUnderpass_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_ZYGARDE
DesertUnderpass_EventScript_Legends2_TransitionEnd:
	return

DesertUnderpass_EventScript_Zygarde::
	lock
	faceplayer
	playmoncry SPECIES_ZYGARDE_50, CRY_MODE_ENCOUNTER
	msgbox DesertUnderpass_Text_Zygarde, MSGBOX_DEFAULT
	waitmoncry
	closemessage
DesertUnderpass_EventScript_Zygarde_Battle::
	setwildbattle SPECIES_ZYGARDE_50, 90
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, DesertUnderpass_EventScript_Zygarde_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, DesertUnderpass_EventScript_Zygarde_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, DesertUnderpass_EventScript_Zygarde_Stays
	removeobject LOCALID_LEGENDS_ZYGARDE
	setflag FLAG_HIDE_LEGENDS_ZYGARDE
	msgbox DesertUnderpass_Text_ZygardeFled, MSGBOX_DEFAULT
DesertUnderpass_EventScript_Zygarde_Stays::
	release
	end

DesertUnderpass_EventScript_Zygarde_Caught::
	removeobject LOCALID_LEGENDS_ZYGARDE
	setflag FLAG_HIDE_LEGENDS_ZYGARDE
	setflag FLAG_CAUGHT_ZYGARDE
	@ Project Grounded: Zygarde Cube erbij, anders kan Zygarde nooit van vorm wisselen
	msgbox DesertUnderpass_Text_ZygardeCube, MSGBOX_DEFAULT
	giveitem ITEM_ZYGARDE_CUBE
	release
	end

DesertUnderpass_Text_ZygardeCube:
	.string "Something green and boxy was left\n"
	.string "behind where ZYGARDE stood.\p"
	.string "It hums. It's either a ZYGARDE CUBE\n"
	.string "or a very judgmental lunchbox.$"

DesertUnderpass_Text_Zygarde:
	.string "Grrrooo...\p"
	.string "(Life and death are both in your PC now.\n"
	.string "Somebody had to come and check the\l"
	.string "paperwork. ZYGARDE is that somebody.\l"
	.string "It is unimpressed with your filing.)$"

DesertUnderpass_Text_ZygardeFled:
	.string "ZYGARDE fell apart into a hundred little\n"
	.string "cells and crawled into the cracks.\p"
	.string "That's not a retreat. That's a\n"
	.string "reorganisation. It'll be back.$"
@ --- einde legends2 ---
