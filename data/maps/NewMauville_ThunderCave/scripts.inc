NewMauville_ThunderCave_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, NewMauville_ThunderCave_OnLoad
	.byte 0

NewMauville_ThunderCave_OnLoad:
	call_if_set FLAG_NEW_MAUVILLE_VAULT_OPEN, NewMauville_ThunderCave_EventScript_SetVaultDoor
	end

@ Project Grounded: kluisdeur naar Genesect in de bovenwand (x 6-8), zelfde deur als de ingang
NewMauville_ThunderCave_EventScript_SetVaultDoor::
	setmetatile 6, 0, 0x2C3, TRUE
	setmetatile 7, 0, 0x2C4, TRUE
	setmetatile 8, 0, 0x2C5, TRUE
	setmetatile 6, 1, 0x2CB, TRUE
	setmetatile 7, 1, 0x2CC, FALSE
	setmetatile 8, 1, 0x2CD, TRUE
	return

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

@ Project Grounded: post-game terminal: de kluis met Genesect herstarten (de juiste keuze is uit- en weer aanzetten)
NewMauville_ThunderCave_EventScript_Monitor1::
	lockall
	goto_if_set FLAG_NEW_MAUVILLE_VAULT_OPEN, NewMauville_ThunderCave_EventScript_TerminalDone
	goto_if_unset FLAG_SYS_GAME_CLEAR, NewMauville_ThunderCave_EventScript_TerminalLocked
	msgbox NewMauville_ThunderCave_Text_TerminalBoot, MSGBOX_DEFAULT
NewMauville_ThunderCave_EventScript_TerminalMenu::
	message NewMauville_ThunderCave_Text_TerminalPrompt
	waitmessage
	dynmultichoice 17, 1, FALSE, 4, 0, DYN_MULTICHOICE_CB_NONE, NewMauville_ThunderCave_Text_OptHit, NewMauville_ThunderCave_Text_OptWattson, NewMauville_ThunderCave_Text_OptReboot, NewMauville_ThunderCave_Text_OptLogOut
	switch VAR_RESULT
	case 0, NewMauville_ThunderCave_EventScript_TerminalHit
	case 1, NewMauville_ThunderCave_EventScript_TerminalWattson
	case 2, NewMauville_ThunderCave_EventScript_TerminalReboot
	msgbox NewMauville_ThunderCave_Text_TerminalLogOut, MSGBOX_DEFAULT
	releaseall
	end

NewMauville_ThunderCave_EventScript_TerminalLocked::
	msgbox NewMauville_ThunderCave_Text_Monitor1, MSGBOX_DEFAULT
	releaseall
	end

NewMauville_ThunderCave_EventScript_TerminalHit::
	playse SE_M_DOUBLE_SLAP
	waitse
	msgbox NewMauville_ThunderCave_Text_TerminalHit, MSGBOX_DEFAULT
	goto NewMauville_ThunderCave_EventScript_TerminalMenu

NewMauville_ThunderCave_EventScript_TerminalWattson::
	playse SE_POKENAV_CALL
	waitse
	msgbox NewMauville_ThunderCave_Text_TerminalWattson, MSGBOX_DEFAULT
	goto NewMauville_ThunderCave_EventScript_TerminalMenu

NewMauville_ThunderCave_EventScript_TerminalReboot::
	msgbox NewMauville_ThunderCave_Text_TerminalShutdown, MSGBOX_DEFAULT
	closemessage
	playse SE_PC_OFF
	fadescreen FADE_TO_BLACK
	delay 40
	playse SE_PC_ON
	fadescreen FADE_FROM_BLACK
	msgbox NewMauville_ThunderCave_Text_TerminalBooting, MSGBOX_DEFAULT
	setflag FLAG_NEW_MAUVILLE_VAULT_OPEN
	call NewMauville_ThunderCave_EventScript_SetVaultDoor
	special DrawWholeMapView
	playse SE_BANG
	waitse
	msgbox NewMauville_ThunderCave_Text_VaultOpened, MSGBOX_DEFAULT
	releaseall
	end

NewMauville_ThunderCave_EventScript_TerminalDone::
	msgbox NewMauville_ThunderCave_Text_TerminalDone, MSGBOX_DEFAULT
	releaseall
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

NewMauville_ThunderCave_Text_TerminalBoot:
	.string "The screen flickers.\p"
	.string "ERROR: FUTURE NOT FOUND.\p"
	.string "SECTOR B: 1 UNREGISTERED LIFEFORM.\n"
	.string "BUG-TYPE. ARMED. SULKING.\p"
	.string "VAULT DOOR: LOCKED SINCE 1998.$"

NewMauville_ThunderCave_Text_TerminalPrompt:
	.string "SELECT RECOVERY PROCEDURE:$"

NewMauville_ThunderCave_Text_OptHit:
	.string "HIT IT$"

NewMauville_ThunderCave_Text_OptWattson:
	.string "CALL WATTSON$"

NewMauville_ThunderCave_Text_OptReboot:
	.string "OFF AND ON AGAIN$"

NewMauville_ThunderCave_Text_OptLogOut:
	.string "LOG OUT$"

NewMauville_ThunderCave_Text_TerminalHit:
	.string "You hit the server.\p"
	.string "The server is now also\n"
	.string "disappointed in you.$"

NewMauville_ThunderCave_Text_TerminalWattson:
	.string "Calling WATTSON…\p"
	.string "“Wahahahah! Did you try paying\n"
	.string "the power bill? I didn't!”\p"
	.string "He hangs up. Classic Wattson.$"

NewMauville_ThunderCave_Text_TerminalLogOut:
	.string "You log out. Somewhere behind the\n"
	.string "wall, something sighs. Metallically.$"

NewMauville_ThunderCave_Text_TerminalShutdown:
	.string "SHUTTING DOWN…\n"
	.string "PLEASE DO NOT PANIC.$"

NewMauville_ThunderCave_Text_TerminalBooting:
	.string "BOOTING NEW MAUVILLE OS 98…\p"
	.string "RECOVERING SECTOR B… DONE.\n"
	.string "VAULT DOOR: UNLOCKED.\p"
	.string "Have a nice day. Please do not\n"
	.string "open the vault.$"

NewMauville_ThunderCave_Text_VaultOpened:
	.string "Something heavy clicks open\n"
	.string "in the back wall.$"

NewMauville_ThunderCave_Text_TerminalDone:
	.string "VAULT DOOR: UNLOCKED.\n"
	.string "USER ACCEPTS ALL CONSEQUENCES.$"
