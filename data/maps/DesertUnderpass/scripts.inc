DesertUnderpass_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DesertUnderpass_OnTransition
	.byte 0

DesertUnderpass_OnTransition:
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
