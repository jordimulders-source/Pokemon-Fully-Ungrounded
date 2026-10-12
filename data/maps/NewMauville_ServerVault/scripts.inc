NewMauville_ServerVault_MapScripts::
	.byte 0

@ Project Grounded: serverkluis achter de Raikou-grot (post-game, deur via de terminal in de Raikou-grot).
@ Sinds v0.9.110 is Genesect weg: Neo Team Plasma heeft hem verscheept. De printer geeft de vrachtbrief
@ (VAR_PLASMA_FRIGATE 1) en zo de weg naar Nothing Island (mist ten westen van Route 105).
NewMauville_ServerVault_EventScript_Capsule::
	msgbox NewMauville_ServerVault_Text_Capsule, MSGBOX_SIGN
	end

NewMauville_ServerVault_EventScript_Printer::
	lockall
	goto_if_ne VAR_PLASMA_FRIGATE, 0, NewMauville_ServerVault_EventScript_PrinterAgain
	msgbox NewMauville_ServerVault_Text_PrinterWakes, MSGBOX_DEFAULT
	playse SE_PC_ON
	waitse
	msgbox NewMauville_ServerVault_Text_Waybill, MSGBOX_DEFAULT
	setvar VAR_PLASMA_FRIGATE, 1
	releaseall
	end

NewMauville_ServerVault_EventScript_PrinterAgain::
	msgbox NewMauville_ServerVault_Text_Waybill, MSGBOX_DEFAULT
	msgbox NewMauville_ServerVault_Text_PrinterAgain, MSGBOX_DEFAULT
	releaseall
	end

NewMauville_ServerVault_EventScript_Server1::
	msgbox NewMauville_ServerVault_Text_Server1, MSGBOX_SIGN
	end

NewMauville_ServerVault_Text_Capsule:
	.string "A containment capsule. Empty.\p"
	.string "The glass is broken outward.\n"
	.string "Something left. Something angry.\l"
	.string "Something with a forklift helping it.$"

NewMauville_ServerVault_Text_PrinterWakes:
	.string "A dusty printer wakes up, screams\n"
	.string "like a fax machine and spits out\l"
	.string "a crumpled sheet.$"

NewMauville_ServerVault_Text_Waybill:
	.string "SHIPMENT 0451\n"
	.string "1x GENESECT (ANCIENT, VERY ANGRY)\p"
	.string "DELIVER TO: P. FRIGATE\n"
	.string "c/o NOTHING ISLAND\l"
	.string "(WEST OF ROUTE 105, IN THE FOG)\p"
	.string "SIGNED: Z.\n"
	.string "P.S. THIS SIDE UP. BOTH SIDES BITE.$"

NewMauville_ServerVault_Text_PrinterAgain:
	.string "The printer is out of paper.\n"
	.string "And ink. And hope.$"

NewMauville_ServerVault_Text_Server1:
	.string "A server rack, humming happily.\p"
	.string "Someone taped a note to it:\n"
	.string "“DO NOT FEED THE BUG. IT ATE THE\l"
	.string "INTERN.”$"

NewMauville_ServerVault_Text_Server2:
	.string "A file is open on the screen:\n"
	.string "GENESECT-FINAL-v2-REAL.EXE\p"
	.string "Last modified: 300 million years ago.\n"
	.string "Still not backed up.$"
