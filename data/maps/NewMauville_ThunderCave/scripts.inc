NewMauville_ThunderCave_MapScripts::
	.byte 0

@ Project Grounded: Raikou in het kapotte ondergrondse datacenter onder New Mauville
NewMauville_ThunderCave_EventScript_Raikou::
	lock
	faceplayer
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_RAIKOU, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NewMauville_ThunderCave_EventScript_RaikouStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NewMauville_ThunderCave_EventScript_RaikouStays
	removeobject LOCALID_NEW_MAUVILLE_RAIKOU
	setflag FLAG_HIDE_NEW_MAUVILLE_RAIKOU
NewMauville_ThunderCave_EventScript_RaikouStays::
	release
	end

NewMauville_ThunderCave_EventScript_Rubble::
	msgbox NewMauville_ThunderCave_Text_Rubble, MSGBOX_SIGN
	end

NewMauville_ThunderCave_EventScript_Monitor1::
	msgbox NewMauville_ThunderCave_Text_Monitor1, MSGBOX_SIGN
	end

NewMauville_ThunderCave_EventScript_Monitor2::
	msgbox NewMauville_ThunderCave_Text_Monitor2, MSGBOX_SIGN
	end

NewMauville_ThunderCave_EventScript_Monitor3::
	msgbox NewMauville_ThunderCave_Text_Monitor3, MSGBOX_SIGN
	end

NewMauville_ThunderCave_Text_Rubble:
	.string "Concrete, cables and a mouse pad\n"
	.string "that says WORLD'S BEST INTERN.$"

NewMauville_ThunderCave_Text_Monitor1:
	.string "The screen flickers.\p"
	.string "ERROR: FUTURE NOT FOUND.$"

NewMauville_ThunderCave_Text_Monitor2:
	.string "A gutted server. Someone mined\n"
	.string "crypto on it until it melted.\p"
	.string "Then they kept going.$"

NewMauville_ThunderCave_Text_Monitor3:
	.string "A cracked monitor. Last message:\p"
	.string "WATTSON, PLEASE PAY THE POWER BILL.\n"
	.string "Sent: 1998.$"
