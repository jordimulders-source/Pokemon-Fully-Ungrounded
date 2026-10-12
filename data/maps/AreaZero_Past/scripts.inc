@ Project Grounded: AreaZero_Past (tools/grounded/maptools/area_zero.py)
AreaZero_Past_MapScripts::
	.byte 0

AreaZero_Past_EventScript_WalkingWake::
	lock
	faceplayer
	playmoncry SPECIES_WALKING_WAKE, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Past_Text_WalkingWake, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_WALKING_WAKE, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Past_EventScript_WalkingWakeCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Past_EventScript_WalkingWakeBack
	release
	end

AreaZero_Past_EventScript_WalkingWakeBack::
	msgbox AreaZero_Past_Text_WalkingWakeBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_WalkingWakeCaught::
	removeobject LOCALID_AREA_ZERO_WALKING_WAKE
	setflag FLAG_AREAZERO_WALKING_WAKE
	release
	end

AreaZero_Past_EventScript_GougingFire::
	lock
	faceplayer
	playmoncry SPECIES_GOUGING_FIRE, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Past_Text_GougingFire, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_GOUGING_FIRE, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Past_EventScript_GougingFireCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Past_EventScript_GougingFireBack
	release
	end

AreaZero_Past_EventScript_GougingFireBack::
	msgbox AreaZero_Past_Text_GougingFireBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_GougingFireCaught::
	removeobject LOCALID_AREA_ZERO_GOUGING_FIRE
	setflag FLAG_AREAZERO_GOUGING_FIRE
	release
	end

AreaZero_Past_EventScript_RagingBolt::
	lock
	faceplayer
	playmoncry SPECIES_RAGING_BOLT, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Past_Text_RagingBolt, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_RAGING_BOLT, 96
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Past_EventScript_RagingBoltCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Past_EventScript_RagingBoltBack
	release
	end

AreaZero_Past_EventScript_RagingBoltBack::
	msgbox AreaZero_Past_Text_RagingBoltBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_RagingBoltCaught::
	removeobject LOCALID_AREA_ZERO_RAGING_BOLT
	setflag FLAG_AREAZERO_RAGING_BOLT
	release
	end

AreaZero_Past_EventScript_Legend::
	lock
	faceplayer
	playmoncry SPECIES_KORAIDON, CRY_MODE_ENCOUNTER
	msgbox AreaZero_Past_Text_Legend, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_KORAIDON, 98
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, AreaZero_Past_EventScript_LegendCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AreaZero_Past_EventScript_LegendBack
	release
	end

AreaZero_Past_EventScript_LegendBack::
	msgbox AreaZero_Past_Text_LegendBack, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_LegendCaught::
	removeobject LOCALID_AREA_ZERO_KORAIDON
	setflag FLAG_AREAZERO_KORAIDON
	msgbox AreaZero_Past_Text_Alarm, MSGBOX_DEFAULT
	goto AreaZero_Past_EventScript_Fight
	release
	end

AreaZero_Past_EventScript_Terminal::
	lock
	goto_if_defeated TRAINER_AREA_ZERO_SECURITY_PAST, AreaZero_Past_EventScript_Offline
	goto_if_set FLAG_AREAZERO_KORAIDON, AreaZero_Past_EventScript_Rearm
	msgbox AreaZero_Past_Text_Standby, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_Rearm::
	msgbox AreaZero_Past_Text_Alarm, MSGBOX_DEFAULT
AreaZero_Past_EventScript_Fight::
	trainerbattle_no_intro TRAINER_AREA_ZERO_SECURITY_PAST, AreaZero_Past_Text_Defeat
	msgbox AreaZero_Past_Text_Down, MSGBOX_DEFAULT
	checktrainerflag TRAINER_AREA_ZERO_SECURITY_FUTURE
	goto_if FALSE, AreaZero_Past_EventScript_OneLeft
	msgbox AreaZero_Past_Text_BothDown, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_OneLeft::
	msgbox AreaZero_Past_Text_OneLeft, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_Offline::
	msgbox AreaZero_Past_Text_Offline, MSGBOX_DEFAULT
	release
	end

AreaZero_Past_EventScript_Log::
	msgbox AreaZero_Past_Text_Log, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AreaZero_Past_Text_WalkingWake:
	.string "A roaring blue beast with a blazing mane\n"
	.string "snorts steam at you.\p"
	.string "Somebody's ancient legend. Extra spicy.$"

AreaZero_Past_Text_WalkingWakeBack:
	.string "WALKING WAKE shakes the water off and\n"
	.string "comes right back. Extinction is a\l"
	.string "suggestion.$"

AreaZero_Past_Text_GougingFire:
	.string "A colossal molten beast paws the\n"
	.string "ground.\p"
	.string "The floor underneath it has given up on\n"
	.string "being solid.$"

AreaZero_Past_Text_GougingFireBack:
	.string "GOUGING FIRE flares up again from its\n"
	.string "own embers. The floor sighs.$"

AreaZero_Past_Text_RagingBolt:
	.string "A long-necked thundercloud of a\n"
	.string "dinosaur grumbles at you.\p"
	.string "Every grumble is a minor weather event.$"

AreaZero_Past_Text_RagingBoltBack:
	.string "RAGING BOLT crackles back to life.\n"
	.string "Lightning never strikes the same place\l"
	.string "twice. This one does, out of spite.$"

AreaZero_Past_Text_Legend:
	.string "KORAIDON lies at the bottom of the\n"
	.string "crater, sunning itself under a sun that\l"
	.string "went out millions of years ago.\p"
	.string "It wags. That's either friendly or a\n"
	.string "warning. Possibly both.$"

AreaZero_Past_Text_LegendBack:
	.string "KORAIDON rolls over, yawns, and gets up\n"
	.string "again. Apex predators don't do naps on\l"
	.string "command.$"

AreaZero_Past_Text_Standby:
	.string "ZERO LAB SECURITY TERMINAL\n"
	.string "STATUS: STANDBY.\p"
	.string "CONTAINED: 1x KORAIDON.\n"
	.string "Do not throw sticks. It will bring back\l"
	.string "the tree.$"

AreaZero_Past_Text_Alarm:
	.string "BWEEEP. BWEEEP.\n"
	.string "SPECIMEN REMOVED FROM CONTAINMENT.\p"
	.string "INITIATING SECURITY PROTOCOL:\n"
	.string "ABSOLUTELY NOT.$"

AreaZero_Past_Text_Defeat:
	.string "PROTOCOL... FAILED.\n"
	.string "FILING A COMPLAINT WITH MYSELF.$"

AreaZero_Past_Text_Down:
	.string "The terminal goes dark with a sad little\n"
	.string "descending beep.$"

AreaZero_Past_Text_OneLeft:
	.string "A status line flickers before it dies:\n"
	.string "SECURITY NETWORK HALF OFFLINE. The\l"
	.string "other half is in the FUTURE. Of course\l"
	.string "it is.$"

AreaZero_Past_Text_BothDown:
	.string "A status line flickers before it dies:\n"
	.string "SECURITY NETWORK FULLY OFFLINE.\p"
	.string "Far above, in the crystal cave,\n"
	.string "something cracks like ice on a lake.$"

AreaZero_Past_Text_Offline:
	.string "SECURITY OFFLINE.\n"
	.string "HAVE A NICE DAY. OR ERA.$"

AreaZero_Past_Text_Log:
	.string "RESEARCH LOG 7P\n"
	.string "Everything here wants to eat me,\l"
	.string "including two of the plants.\p"
	.string "KORAIDON naps at the bottom of the\n"
	.string "crater like a very large, very smug dog.\l"
	.string "The security system watches it. It\l"
	.string "watches me back.$"
