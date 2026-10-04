LibertyGarden_MapScripts::
	.byte 0

@ Project Grounded: Liberty Garden (Victini). Post-game: versla de vijf Victory-uitdagers (Dewford, Slateport,
@ Fortree, Mossdeep, Ever Grande; volgorde vrij), haal bij de Victory-commissaris in de haven van Lilycove de
@ Liberty Pass en vaar met de S.S. Tidal hierheen. Kaart: tools/grounded/maptools/liberty_garden.py.

@ --- gauntlet: stempels tellen (VAR_0x8004 = aantal verslagen uitdagers) ---
VictoryGauntlet_EventScript_CountStamps::
	setvar VAR_0x8004, 0
	call_if_defeated TRAINER_VICTORY_VANCE, VictoryGauntlet_EventScript_AddStamp
	call_if_defeated TRAINER_VICTORY_VERNON, VictoryGauntlet_EventScript_AddStamp
	call_if_defeated TRAINER_VICTORY_VEGA, VictoryGauntlet_EventScript_AddStamp
	call_if_defeated TRAINER_VICTORY_VESNA, VictoryGauntlet_EventScript_AddStamp
	call_if_defeated TRAINER_VICTORY_V, VictoryGauntlet_EventScript_AddStamp
	return

VictoryGauntlet_EventScript_AddStamp::
	addvar VAR_0x8004, 1
	return

@ na het winnen van een uitdager
VictoryGauntlet_EventScript_GiveStamp::
	call VictoryGauntlet_EventScript_CountStamps
	buffernumberstring STR_VAR_1, VAR_0x8004
	playfanfare MUS_OBTAIN_SYMBOL
	message VictoryGauntlet_Text_GotStamp
	waitmessage
	waitfanfare
	goto_if_eq VAR_0x8004, 5, VictoryGauntlet_EventScript_AllStamps
	msgbox VictoryGauntlet_Text_StampCount, MSGBOX_DEFAULT
	return

VictoryGauntlet_EventScript_AllStamps::
	msgbox VictoryGauntlet_Text_AllStamps, MSGBOX_DEFAULT
	return

@ wie nog wacht (commissaris)
VictoryGauntlet_EventScript_ListRemaining::
	call_if_not_defeated TRAINER_VICTORY_VANCE, VictoryGauntlet_EventScript_WaitingVance
	call_if_not_defeated TRAINER_VICTORY_VERNON, VictoryGauntlet_EventScript_WaitingVernon
	call_if_not_defeated TRAINER_VICTORY_VEGA, VictoryGauntlet_EventScript_WaitingVega
	call_if_not_defeated TRAINER_VICTORY_VESNA, VictoryGauntlet_EventScript_WaitingVesna
	call_if_not_defeated TRAINER_VICTORY_V, VictoryGauntlet_EventScript_WaitingV
	return

VictoryGauntlet_EventScript_WaitingVance::
	msgbox VictoryGauntlet_Text_WaitingVance, MSGBOX_DEFAULT
	return

VictoryGauntlet_EventScript_WaitingVernon::
	msgbox VictoryGauntlet_Text_WaitingVernon, MSGBOX_DEFAULT
	return

VictoryGauntlet_EventScript_WaitingVega::
	msgbox VictoryGauntlet_Text_WaitingVega, MSGBOX_DEFAULT
	return

VictoryGauntlet_EventScript_WaitingVesna::
	msgbox VictoryGauntlet_Text_WaitingVesna, MSGBOX_DEFAULT
	return

VictoryGauntlet_EventScript_WaitingV::
	msgbox VictoryGauntlet_Text_WaitingV, MSGBOX_DEFAULT
	return

@ --- de Victory-commissaris in de haven van Lilycove ---
VictoryGauntlet_EventScript_Commissioner::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_LIBERTY_PASS, VictoryGauntlet_EventScript_CommissionerAfterPass
	goto_if_unset FLAG_SYS_GAME_CLEAR, VictoryGauntlet_EventScript_CommissionerNotChampion
	call VictoryGauntlet_EventScript_CountStamps
	goto_if_eq VAR_0x8004, 5, VictoryGauntlet_EventScript_CommissionerGivePass
	goto_if_set FLAG_VICTORY_GAUNTLET_EXPLAINED, VictoryGauntlet_EventScript_CommissionerProgress
	setflag FLAG_VICTORY_GAUNTLET_EXPLAINED
	msgbox VictoryGauntlet_Text_CommissionerExplain, MSGBOX_DEFAULT
	call VictoryGauntlet_EventScript_ListRemaining
	release
	end

VictoryGauntlet_EventScript_CommissionerProgress::
	buffernumberstring STR_VAR_1, VAR_0x8004
	msgbox VictoryGauntlet_Text_CommissionerProgress, MSGBOX_DEFAULT
	call VictoryGauntlet_EventScript_ListRemaining
	release
	end

VictoryGauntlet_EventScript_CommissionerNotChampion::
	msgbox VictoryGauntlet_Text_CommissionerNotChampion, MSGBOX_DEFAULT
	release
	end

VictoryGauntlet_EventScript_CommissionerGivePass::
	setflag FLAG_VICTORY_GAUNTLET_EXPLAINED
	msgbox VictoryGauntlet_Text_CommissionerGivePass, MSGBOX_DEFAULT
	giveitem ITEM_LIBERTY_PASS
	setflag FLAG_RECEIVED_LIBERTY_PASS
	msgbox VictoryGauntlet_Text_CommissionerAfterGive, MSGBOX_DEFAULT
	release
	end

VictoryGauntlet_EventScript_CommissionerAfterPass::
	msgbox VictoryGauntlet_Text_CommissionerAfterPass, MSGBOX_DEFAULT
	release
	end

@ --- veerboot: de baliemedewerker in de haven roept dit aan (call); geeft terug bij geen pas of NEE ---
VictoryGauntlet_EventScript_TryFerry::
	checkitem ITEM_LIBERTY_PASS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
	msgbox VictoryGauntlet_Text_FerryAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Common_EventScript_NopReturn
	call LilycoveCity_Harbor_EventScript_BoardFerry
	warp MAP_LIBERTY_GARDEN, 13, 22
	waitstate
	release
	end

@ --- het eiland ---
LibertyGarden_EventScript_Sailor::
	lock
	faceplayer
	msgbox LibertyGarden_Text_SailBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LibertyGarden_EventScript_Stay
	msgbox EventTicket_Text_SailHome, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	hideobjectat LOCALID_LIBERTY_GARDEN_SAILOR, MAP_LIBERTY_GARDEN
	setvar VAR_0x8004, LOCALID_LIBERTY_GARDEN_SS_TIDAL
	call Common_EventScript_FerryDepartIsland
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	release
	end

LibertyGarden_EventScript_Stay::
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
	release
	end

LibertyGarden_EventScript_Sign::
	msgbox LibertyGarden_Text_Sign, MSGBOX_SIGN
	end

LibertyGarden_EventScript_Victini::
	lock
	faceplayer
	playmoncry SPECIES_VICTINI, CRY_MODE_ENCOUNTER
	msgbox LibertyGarden_Text_Victini, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_VICTINI, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LibertyGarden_EventScript_VictiniStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LibertyGarden_EventScript_VictiniStays
	removeobject LOCALID_LIBERTY_GARDEN_VICTINI
	setflag FLAG_HIDE_LIBERTY_GARDEN_VICTINI
LibertyGarden_EventScript_VictiniStays::
	release
	end

VictoryGauntlet_Text_GotStamp:
	.string "{PLAYER} received a VICTORY STAMP!$"

VictoryGauntlet_Text_StampCount:
	.string "VICTORY STAMPS: {STR_VAR_1} of 5.\p"
	.string "The others are still out there, being\n"
	.string "smug.$"

VictoryGauntlet_Text_AllStamps:
	.string "That makes five VICTORY STAMPS!\p"
	.string "The VICTORY COMMISSIONER at LILYCOVE\n"
	.string "HARBOR will want to see this.$"

VictoryGauntlet_Text_CommissionerNotChampion:
	.string "I'm the VICTORY COMMISSIONER. I hand\n"
	.string "out victory. To CHAMPIONS.\p"
	.string "You are not a CHAMPION. I checked. I\n"
	.string "have a list.\p"
	.string "It's a short list. You're not on it.$"

VictoryGauntlet_Text_CommissionerExplain:
	.string "A CHAMPION! Finally! I've been standing\n"
	.string "here since the game came out.\p"
	.string "I run the VICTORY GAUNTLET. Five\n"
	.string "VICTORY CHALLENGERS are waiting all\l"
	.string "over HOENN.\p"
	.string "Beat them in any order you like. Each\n"
	.string "win earns you a VICTORY STAMP.\p"
	.string "Bring me all five and you get the\n"
	.string "LIBERTY PASS. It takes the ferry to\l"
	.string "LIBERTY GARDEN.\p"
	.string "Something very small and very\n"
	.string "victorious lives there. Here's who you\l"
	.string "need to beat:$"

VictoryGauntlet_Text_CommissionerProgress:
	.string "VICTORY STAMPS: {STR_VAR_1} of 5.\p"
	.string "Still waiting for you:$"

VictoryGauntlet_Text_CommissionerGivePass:
	.string "Five VICTORY STAMPS! A clean sweep!\p"
	.string "By the power vested in me by absolutely\n"
	.string "nobody, I give you this.$"

VictoryGauntlet_Text_CommissionerAfterGive:
	.string "Show it to the ferry attendant and\n"
	.string "you'll sail to LIBERTY GARDEN.\p"
	.string "There used to be a lighthouse there. We\n"
	.string "sold it to pay for the tickets.$"

VictoryGauntlet_Text_CommissionerAfterPass:
	.string "Go on. LIBERTY GARDEN. The ferry's right\n"
	.string "there.\p"
	.string "It's the big boat. You can't miss it.\n"
	.string "People do, somehow.$"

VictoryGauntlet_Text_FerryAsk:
	.string "Oh! A LIBERTY PASS!\p"
	.string "Shall we sail to LIBERTY GARDEN?$"

LibertyGarden_Text_SailBack:
	.string "Had enough victory for one day? Shall\n"
	.string "we sail back to LILYCOVE?$"

LibertyGarden_Text_Sign:
	.string "LIBERTY GARDEN\p"
	.string "The lighthouse is temporarily two lamp\n"
	.string "posts.\p"
	.string "Please do not feed the VICTORY.$"

LibertyGarden_Text_Victini:
	.string "Vic-tiii!$"

VictoryGauntlet_Text_WaitingVance:
	.string "VANCE is sweating somewhere on the\n"
	.string "beach of DEWFORD TOWN.$"

VictoryGauntlet_Text_WaitingVernon:
	.string "VERNON is spending money in SLATEPORT\n"
	.string "CITY.$"

VictoryGauntlet_Text_WaitingVega:
	.string "VEGA is predicting things up in FORTREE\n"
	.string "CITY.$"

VictoryGauntlet_Text_WaitingVesna:
	.string "VESNA is being dramatic in MOSSDEEP\n"
	.string "CITY.$"

VictoryGauntlet_Text_WaitingV:
	.string "V is standing in front of the POKéMON\n"
	.string "LEAGUE in EVER GRANDE CITY. Ominously.$"
