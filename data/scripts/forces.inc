@ Project Grounded: Forces of Nature op routes (post-game). Of en waar ze staan, loot src/forces.c bij elke
@ binnenkomst van een kandidaatroute; de objecten staan achteraan de map.json van die routes
@ (tools/grounded/maptools/forces_routes.py). Na vangen of verslaan zijn ze weg, vluchten/verliezen mag.

Forces_EventScript_Tornadus::
	lock
	faceplayer
	playmoncry SPECIES_TORNADUS_INCARNATE, CRY_MODE_ENCOUNTER
	msgbox Forces_Text_Tornadus, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setvar VAR_0x8004, 0
	special Forces_PrepareBattle
	setwildbattle SPECIES_TORNADUS_INCARNATE, 70
	call Forces_EventScript_Battle
	goto_if_eq VAR_RESULT, FALSE, Forces_EventScript_Stays
	setflag FLAG_FORCES_TORNADUS_DONE
	setflag FLAG_FORCES_HIDE_TORNADUS
	call Forces_EventScript_Gone
	msgbox Forces_Text_TornadusGone, MSGBOX_DEFAULT
	release
	end

Forces_EventScript_Thundurus::
	lock
	faceplayer
	playmoncry SPECIES_THUNDURUS_INCARNATE, CRY_MODE_ENCOUNTER
	msgbox Forces_Text_Thundurus, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setvar VAR_0x8004, 1
	special Forces_PrepareBattle
	setwildbattle SPECIES_THUNDURUS_INCARNATE, 70
	call Forces_EventScript_Battle
	goto_if_eq VAR_RESULT, FALSE, Forces_EventScript_Stays
	setflag FLAG_FORCES_THUNDURUS_DONE
	setflag FLAG_FORCES_HIDE_THUNDURUS
	call Forces_EventScript_Gone
	msgbox Forces_Text_ThundurusGone, MSGBOX_DEFAULT
	release
	end

Forces_EventScript_Landorus::
	lock
	faceplayer
	playmoncry SPECIES_LANDORUS_INCARNATE, CRY_MODE_ENCOUNTER
	msgbox Forces_Text_Landorus, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setvar VAR_0x8004, 2
	special Forces_PrepareBattle
	setwildbattle SPECIES_LANDORUS_INCARNATE, 70
	call Forces_EventScript_Battle
	goto_if_eq VAR_RESULT, FALSE, Forces_EventScript_Stays
	setflag FLAG_FORCES_LANDORUS_DONE
	setflag FLAG_FORCES_HIDE_LANDORUS
	call Forces_EventScript_Gone
	msgbox Forces_Text_LandorusGone, MSGBOX_DEFAULT
	release
	end

@ VAR_RESULT = TRUE als hij gevangen of verslagen is.
Forces_EventScript_Battle::
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Forces_EventScript_BattleDone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Forces_EventScript_BattleDone
	setvar VAR_RESULT, FALSE
	return

Forces_EventScript_BattleDone::
	setvar VAR_RESULT, TRUE
	return

Forces_EventScript_Gone::
	removeobject VAR_LAST_TALKED
	special Forces_Finish
	doweather
	return

Forces_EventScript_Stays::
	release
	end

@ Hint-NPC's (één per Force)
Forces_EventScript_HintTornadus::
	msgbox Forces_Text_HintTornadus, MSGBOX_NPC
	end

Forces_EventScript_HintThundurus::
	msgbox Forces_Text_HintThundurus, MSGBOX_NPC
	end

Forces_EventScript_HintLandorus::
	msgbox Forces_Text_HintLandorus, MSGBOX_NPC
	end

Forces_Text_Tornadus:
	.string "TORNADUS is hovering in its own\nprivate hurricane.\pSomewhere, a weather forecaster\nquietly updates their CV.$"

Forces_Text_TornadusGone:
	.string "The wind dies down.\nA lot of hats will never come back.$"

Forces_Text_Thundurus:
	.string "THUNDURUS is lounging on a\nthundercloud, looking for something\lto electrocute.\pIt has noticed your bicycle.$"

Forces_Text_ThundurusGone:
	.string "The thunderclouds drift apart.\nYour hair stays like that, though.$"

Forces_Text_Landorus:
	.string "LANDORUS floats above the ground\nin a cloud of sand and smugness.\pThe crops bow to it.\nNervously.$"

Forces_Text_LandorusGone:
	.string "The sandstorm settles.\nYou'll find sand in your shoes\luntil the credits roll.$"

Forces_Text_HintTornadus:
	.string "My laundry blew away again.\nNot down the street. To ROUTE 121.\pThey say a green genie with a\ncloud for legs flies around\lROUTES 113, 118 and 121,\lbringing its own weather.\pIt only shows up for people who\nalready beat the CHAMPION.\lThe laundry, sadly, doesn't care.$"

Forces_Text_HintThundurus:
	.string "Our instruments keep detecting a\nthunderstorm with a face.\pIt shows up on ROUTE 119, 120\nor 123. Never two days in a row,\lnever where we put the sensors.\pThe big storms only started after\nsomeone became CHAMPION.\lCoincidence. Probably.\lDon't quote me.$"

Forces_Text_HintLandorus:
	.string "My harvest was huge this year.\nSuspiciously huge.\pA flying tiger made of sand keeps\nturning up on ROUTE 112, 114 and\l117. Wherever it floats, stuff\lgrows.\pFolks say it only bothers with\nthe CHAMPION. Fine by me.\lMore carrots for the rest of us.$"
