@ Project Grounded: het Keldeo-eiland "???" (tools/grounded/maptools/swords_keldeo.py). Een zandbank die er gisteren
@ nog niet was, in een ring van draaikolken. Heb je Cobalion, Terrakion en Virizion gehad, dan belt Mr. Briney
@ (SwordsOfJustice_EventScript_AfterSword); praat met hem (huis Route 104, Dewford of Route 109) en hij vaart je
@ hierheen. Keldeo lv 70. Briney brengt je terug naar waar je vertrok.
UnchartedIsle_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- gedeeld: de drie zwaarden
SwordsOfJustice_EventScript_HideSword::
	setflag FLAG_TEMP_1
	return

SwordsOfJustice_EventScript_SwordStays::
	release
	end

SwordsOfJustice_EventScript_NotchedStone::
	msgbox SwordsOfJustice_Text_NotchedStone, MSGBOX_SIGN
	end

@ Na elk zwaard: zijn ze alle drie weg, dan belt Briney (een keer).
SwordsOfJustice_EventScript_AfterSword::
	goto_if_unset FLAG_DEFEATED_COBALION, SwordsOfJustice_EventScript_SwordStays
	goto_if_unset FLAG_DEFEATED_TERRAKION, SwordsOfJustice_EventScript_SwordStays
	goto_if_unset FLAG_DEFEATED_VIRIZION, SwordsOfJustice_EventScript_SwordStays
	goto_if_set FLAG_BRINEY_KELDEO_CALL, SwordsOfJustice_EventScript_SwordStays
	setflag FLAG_BRINEY_KELDEO_CALL
	delay 30
	pokenavcall SwordsOfJustice_Text_BrineyCall
	waitmessage
	closemessage
	release
	end

@ ---------------------------------------------------------------- Briney: de bootreis
@ Aangeroepen (call) vanuit Brineys gesprekken; VAR_0x8004 = vertrekplek (0 huis, 1 Dewford, 2 Route 109).
@ Geen reis (nog niet gebeld, al geweest of "nee"): return, en Briney doet zijn gewone ding.
EventScript_BrineyKeldeoTrip::
	goto_if_unset FLAG_BRINEY_KELDEO_CALL, EventScript_BrineyKeldeoTrip_Return
	goto_if_set FLAG_DEFEATED_KELDEO, EventScript_BrineyKeldeoTrip_Return
	msgbox SwordsOfJustice_Text_BrineyAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_BrineyKeldeoTrip_Return
	msgbox SwordsOfJustice_Text_BrineyGo, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_KELDEO_TRIP_FROM_DEWFORD
	clearflag FLAG_KELDEO_TRIP_FROM_ROUTE109
	call_if_eq VAR_0x8004, 1, EventScript_BrineyKeldeoTrip_FromDewford
	call_if_eq VAR_0x8004, 2, EventScript_BrineyKeldeoTrip_FromRoute109
	fadescreen FADE_TO_BLACK
	playse SE_M_SURF
	delay 40
	warpsilent MAP_UNCHARTED_ISLE, 14, 14
	waitstate
	releaseall
	end

EventScript_BrineyKeldeoTrip_FromDewford::
	setflag FLAG_KELDEO_TRIP_FROM_DEWFORD
	return

EventScript_BrineyKeldeoTrip_FromRoute109::
	setflag FLAG_KELDEO_TRIP_FROM_ROUTE109
	return

EventScript_BrineyKeldeoTrip_Return::
	return

@ ---------------------------------------------------------------- het eiland
UnchartedIsle_EventScript_Keldeo::
	lock
	msgbox UnchartedIsle_Text_Keldeo, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_KELDEO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_KELDEO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SwordsOfJustice_EventScript_SwordStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SwordsOfJustice_EventScript_SwordStays
	removeobject LOCALID_UNCHARTED_ISLE_KELDEO
	setflag FLAG_DEFEATED_KELDEO
	release
	end

UnchartedIsle_EventScript_Briney::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_KELDEO, UnchartedIsle_EventScript_BrineyDone
	msgbox UnchartedIsle_Text_BrineyWaiting, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, UnchartedIsle_EventScript_SailHome
	release
	end

UnchartedIsle_EventScript_BrineyDone::
	msgbox UnchartedIsle_Text_BrineyDone, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, UnchartedIsle_EventScript_SailHome
	release
	end

UnchartedIsle_EventScript_SailHome::
	msgbox UnchartedIsle_Text_BrineyHome, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_M_SURF
	delay 40
	goto_if_set FLAG_KELDEO_TRIP_FROM_DEWFORD, UnchartedIsle_EventScript_ToDewford
	goto_if_set FLAG_KELDEO_TRIP_FROM_ROUTE109, UnchartedIsle_EventScript_ToRoute109
	warpsilent MAP_ROUTE104_MR_BRINEYS_HOUSE, 5, 4
	waitstate
	releaseall
	end

UnchartedIsle_EventScript_ToDewford::
	warpsilent MAP_DEWFORD_TOWN, 13, 9
	waitstate
	releaseall
	end

UnchartedIsle_EventScript_ToRoute109::
	warpsilent MAP_ROUTE109, 22, 24
	waitstate
	releaseall
	end

@ ---------------------------------------------------------------- teksten (placeholders)
SwordsOfJustice_Text_NotchedStone:
	.string "A boulder with one deep, clean notch,\n"
	.string "as if someone tested a sword on it.\p"
	.string "Next to it, scratched much smaller:\n"
	.string "“JUSTICE WAS HERE.”$"

SwordsOfJustice_Text_BrineyCall:
	.string "… … … … … … … … … … … Beep!\p"
	.string "MR. BRINEY: Ahoy, {PLAYER}! It's me,\n"
	.string "BRINEY! PEEKO says hello!\p"
	.string "PEEKO also says there is an island\n"
	.string "out at sea that wasn't there\l"
	.string "yesterday. With whirlpools!\p"
	.string "I checked my charts. Twice.\n"
	.string "Then I checked my glasses.\p"
	.string "Come see me and we'll sail out!\n"
	.string "PEEKO insists. PEEKO is the boss.\p"
	.string "… … … … … … … … … … … Click!$"

SwordsOfJustice_Text_BrineyAsk:
	.string "MR. BRINEY: {PLAYER}! The island! The\n"
	.string "one that isn't on any map!\p"
	.string "Shall we sail out and have a look?$"

SwordsOfJustice_Text_BrineyGo:
	.string "MR. BRINEY: Anchors aweigh!\n"
	.string "PEEKO, my darling, mind the\l"
	.string "whirlpools! They mind you back!$"

UnchartedIsle_Text_Keldeo:
	.string "A small blue pony stands in the\n"
	.string "middle of the sandbank, very\l"
	.string "seriously holding a pose.\p"
	.string "It has clearly been practicing a\n"
	.string "heroic entrance for three swords\l"
	.string "who are not coming.\p"
	.string "You'll have to do.$"

UnchartedIsle_Text_BrineyWaiting:
	.string "MR. BRINEY: I'll wait right here.\n"
	.string "The boat is the only thing on this\l"
	.string "island I trust.\p"
	.string "Or shall we head home already?$"

UnchartedIsle_Text_BrineyDone:
	.string "MR. BRINEY: Well, I'll be. A pony.\n"
	.string "PEEKO thought it was a horse-shaped\l"
	.string "fish. PEEKO is never wrong, so it\l"
	.string "was both.\p"
	.string "Ready to head home?$"

UnchartedIsle_Text_BrineyHome:
	.string "MR. BRINEY: Home it is! I'm not\n"
	.string "putting this place on my charts.\p"
	.string "Nobody would believe me anyway.$"
