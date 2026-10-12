@ Project Grounded: AreaZero_Future (tools/grounded/maptools/area_zero.py)
AreaZero_Future_MapScripts::
	.byte 0

AreaZero_Future_EventScript_IronLeaves::
	lock
	faceplayer
	playmoncry SPECIES_IRON_LEAVES, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Future_Text_IronLeaves, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_IRON_LEAVES, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Future_EventScript_IronLeavesCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Future_EventScript_IronLeavesBack
	release
	end

AreaZero_Future_EventScript_IronLeavesBack::
	msgbox AreaZero_Future_Text_IronLeavesBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_IronLeavesCaught::
	removeobject LOCALID_AREA_ZERO_IRON_LEAVES
	setflag FLAG_AREAZERO_IRON_LEAVES
	release
	end

AreaZero_Future_EventScript_IronBoulder::
	lock
	faceplayer
	playmoncry SPECIES_IRON_BOULDER, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Future_Text_IronBoulder, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_IRON_BOULDER, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Future_EventScript_IronBoulderCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Future_EventScript_IronBoulderBack
	release
	end

AreaZero_Future_EventScript_IronBoulderBack::
	msgbox AreaZero_Future_Text_IronBoulderBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_IronBoulderCaught::
	removeobject LOCALID_AREA_ZERO_IRON_BOULDER
	setflag FLAG_AREAZERO_IRON_BOULDER
	release
	end

AreaZero_Future_EventScript_IronCrown::
	lock
	faceplayer
	playmoncry SPECIES_IRON_CROWN, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Future_Text_IronCrown, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_IRON_CROWN, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Future_EventScript_IronCrownCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Future_EventScript_IronCrownBack
	release
	end

AreaZero_Future_EventScript_IronCrownBack::
	msgbox AreaZero_Future_Text_IronCrownBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_IronCrownCaught::
	removeobject LOCALID_AREA_ZERO_IRON_CROWN
	setflag FLAG_AREAZERO_IRON_CROWN
	release
	end

AreaZero_Future_EventScript_Legend::
	lock
	faceplayer
	playmoncry SPECIES_MIRAIDON, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Future_Text_Legend, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_MIRAIDON, 98
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Future_EventScript_LegendCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Future_EventScript_LegendBack
	release
	end

AreaZero_Future_EventScript_LegendBack::
	msgbox AreaZero_Future_Text_LegendBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_LegendCaught::
	removeobject LOCALID_AREA_ZERO_MIRAIDON
	setflag FLAG_AREAZERO_MIRAIDON
	msgbox AreaZero_Future_Text_Alarm, MSGBOX_DEFAULT
	goto AreaZero_Future_EventScript_Fight
	release
	end

AreaZero_Future_EventScript_Terminal::
	lock
	goto_if_defeated TRAINER_AREA_ZERO_SECURITY_FUTURE, AreaZero_Future_EventScript_Offline
	goto_if_set FLAG_AREAZERO_MIRAIDON, AreaZero_Future_EventScript_Rearm
	msgbox AreaZero_Future_Text_Standby, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_Rearm::
	msgbox AreaZero_Future_Text_Alarm, MSGBOX_DEFAULT
AreaZero_Future_EventScript_Fight::
	trainerbattle_no_intro TRAINER_AREA_ZERO_SECURITY_FUTURE, AreaZero_Future_Text_Defeat
	msgbox AreaZero_Future_Text_Down, MSGBOX_DEFAULT
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_PAST
	goto_if FALSE, AreaZero_Future_EventScript_OneLeft
	msgbox AreaZero_Future_Text_BothDown, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_OneLeft::
	msgbox AreaZero_Future_Text_OneLeft, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_Offline::
	msgbox AreaZero_Future_Text_Offline, MSGBOX_DEFAULT
	release
	end

AreaZero_Future_EventScript_Log::
	msgbox AreaZero_Future_Text_Log, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_Future_Text_IronLeaves:
	.string "A green, gleaming knight raises a\n"
	.string "psychic blade.\p"
	.string "It looks like a legend you once heard\n"
	.string "about. The legend never had a firmware\l"
	.string "update.$"

AreaZero_Future_Text_IronLeavesBack:
	.string "IRON LEAVES kneels, sparks, and stands\n"
	.string "up again. Chivalry is a renewable\l"
	.string "resource.$"

AreaZero_Future_Text_IronBoulder:
	.string "A polished, horned machine stands\n"
	.string "perfectly still.\p"
	.string "Its horn is so sharp the air apologises\n"
	.string "when it moves.$"

AreaZero_Future_Text_IronBoulderBack:
	.string "IRON BOULDER reassembles itself,\n"
	.string "polishing out the dents. Vanity is\l"
	.string "futureproof.$"

AreaZero_Future_Text_IronCrown:
	.string "A crowned metal warrior regards you.\p"
	.string "It has no idea what a crown is for, but\n"
	.string "it knows it looks great in one.$"

AreaZero_Future_Text_IronCrownBack:
	.string "IRON CROWN straightens its crown and\n"
	.string "reboots. Royalty doesn't stay down. It\l"
	.string "delegates.$"

AreaZero_Future_Text_Legend:
	.string "MIRAIDON lies curled up at the bottom\n"
	.string "of the crater, idling like an engine\l"
	.string "somebody forgot to switch off.\p"
	.string "It opens one eye. Then the other. Then\n"
	.string "a third one, on a screen, somewhere.$"

AreaZero_Future_Text_LegendBack:
	.string "MIRAIDON reboots in a shower of sparks.\p"
	.string "Turning it off and on again: still the\n"
	.string "oldest trick in the future.$"

AreaZero_Future_Text_Standby:
	.string "ZERO LAB SECURITY TERMINAL\n"
	.string "STATUS: STANDBY.\p"
	.string "CONTAINED: 1x MIRAIDON.\n"
	.string "Do not pet. Do not feed after midnight.\l"
	.string "Do not explain midnight to it.$"

AreaZero_Future_Text_Alarm:
	.string "BWEEEP. BWEEEP.\n"
	.string "SPECIMEN REMOVED FROM CONTAINMENT.\p"
	.string "INITIATING SECURITY PROTOCOL:\n"
	.string "ABSOLUTELY NOT.$"

AreaZero_Future_Text_Defeat:
	.string "PROTOCOL... FAILED.\n"
	.string "FILING A COMPLAINT WITH MYSELF.$"

AreaZero_Future_Text_Down:
	.string "The terminal goes dark with a sad little\n"
	.string "descending beep.$"

AreaZero_Future_Text_OneLeft:
	.string "A status line flickers before it dies:\n"
	.string "SECURITY NETWORK HALF OFFLINE. The\l"
	.string "other half is in the PAST. Of course it\l"
	.string "is.$"

AreaZero_Future_Text_BothDown:
	.string "A status line flickers before it dies:\n"
	.string "SECURITY NETWORK FULLY OFFLINE.\p"
	.string "Far above, in the crystal cave,\n"
	.string "something cracks like ice on a lake.$"

AreaZero_Future_Text_Offline:
	.string "SECURITY OFFLINE.\n"
	.string "HAVE A NICE DAY. OR ERA.$"

AreaZero_Future_Text_Log:
	.string "RESEARCH LOG 7F\n"
	.string "The robots here are polite. They call me\l"
	.string "'organic legacy unit'. I've decided to\l"
	.string "take it as a compliment.\p"
	.string "MIRAIDON sleeps at the bottom of the\n"
	.string "crater. The security system sleeps\l"
	.string "next to it. Lightly.$"
