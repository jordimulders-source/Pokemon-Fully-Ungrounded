@ Project Grounded: dak van de Tao-toren (layout van de schone Sky Pillar Top). RESHIRAM en ZEKROM slapen hier,
@ elk aan een eigen kant ("de broers kunnen niet samen in een kamer"); pas na de Hall of Fame wakker. Na de tweede
@ broer verdwijnt de DRAGONITE van het gat in de Dragon's Den (-> KYUREM). tools/grounded/maptools/tao_island.py
TaoIsland_TowerTop_MapScripts::
	.byte 0

TaoIsland_TowerTop_EventScript_Reshiram::
	lock
	goto_if_unset FLAG_SYS_GAME_CLEAR, TaoIsland_TowerTop_EventScript_ReshiramAsleep
	msgbox TaoIsland_TowerTop_Text_ReshiramWake, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_RESHIRAM, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_RESHIRAM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, TaoIsland_TowerTop_EventScript_ReshiramStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, TaoIsland_TowerTop_EventScript_ReshiramStays
	removeobject LOCALID_TAO_RESHIRAM
	setflag FLAG_HIDE_TAO_RESHIRAM
	call TaoIsland_TowerTop_EventScript_CheckBrothers
TaoIsland_TowerTop_EventScript_ReshiramStays::
	release
	end

TaoIsland_TowerTop_EventScript_ReshiramAsleep::
	msgbox TaoIsland_TowerTop_Text_ReshiramAsleep, MSGBOX_DEFAULT
	release
	end

TaoIsland_TowerTop_EventScript_Zekrom::
	lock
	goto_if_unset FLAG_SYS_GAME_CLEAR, TaoIsland_TowerTop_EventScript_ZekromAsleep
	msgbox TaoIsland_TowerTop_Text_ZekromWake, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_ZEKROM, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ZEKROM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, TaoIsland_TowerTop_EventScript_ZekromStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, TaoIsland_TowerTop_EventScript_ZekromStays
	removeobject LOCALID_TAO_ZEKROM
	setflag FLAG_HIDE_TAO_ZEKROM
	call TaoIsland_TowerTop_EventScript_CheckBrothers
TaoIsland_TowerTop_EventScript_ZekromStays::
	release
	end

TaoIsland_TowerTop_EventScript_ZekromAsleep::
	msgbox TaoIsland_TowerTop_Text_ZekromAsleep, MSGBOX_DEFAULT
	release
	end

TaoIsland_TowerTop_EventScript_CheckBrothers::
	goto_if_unset FLAG_HIDE_TAO_RESHIRAM, TaoIsland_TowerTop_EventScript_CheckBrothersEnd
	goto_if_unset FLAG_HIDE_TAO_ZEKROM, TaoIsland_TowerTop_EventScript_CheckBrothersEnd
	setflag FLAG_HIDE_TAO_DEN_DRAGONITE
	msgbox TaoIsland_TowerTop_Text_ColdWind, MSGBOX_DEFAULT
TaoIsland_TowerTop_EventScript_CheckBrothersEnd::
	return

TaoIsland_TowerTop_EventScript_Elder::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, TaoIsland_TowerTop_EventScript_ElderEarly
	goto_if_set FLAG_HIDE_TAO_DEN_DRAGONITE, TaoIsland_TowerTop_EventScript_ElderBoth
	msgbox TaoIsland_TowerTop_Text_Elder, MSGBOX_DEFAULT
	release
	end

TaoIsland_TowerTop_EventScript_ElderEarly::
	msgbox TaoIsland_TowerTop_Text_ElderEarly, MSGBOX_DEFAULT
	release
	end

TaoIsland_TowerTop_EventScript_ElderBoth::
	msgbox TaoIsland_TowerTop_Text_ElderBoth, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_TowerTop_Text_ReshiramAsleep:
	.string "RESHIRAM is asleep. It's giving off heat\n"
	.string "like a radiator someone forgot to turn\l"
	.string "off.$"

TaoIsland_TowerTop_Text_ZekromAsleep:
	.string "ZEKROM is asleep. Your hair stands up.\n"
	.string "All of it. Even the hair you didn't know\l"
	.string "you had.$"

TaoIsland_TowerTop_Text_ReshiramWake:
	.string "RESHIRAM wakes up!\p"
	.string "It glances across the roof, decides its\n"
	.string "brother is still asleep, and gives you\l"
	.string "its full attention.$"

TaoIsland_TowerTop_Text_ZekromWake:
	.string "ZEKROM wakes up!\p"
	.string "It was never asleep. It was pretending,\n"
	.string "so it wouldn't have to talk to its\l"
	.string "brother.$"

TaoIsland_TowerTop_Text_ColdWind:
	.string "Far below the island, something lets out\n"
	.string "a long, freezing sigh.\p"
	.string "It sounds like it was waiting for both\n"
	.string "of them to leave first.$"

TaoIsland_TowerTop_Text_ElderEarly:
	.string "Two brothers sleep up here, RESHIRAM\n"
	.string "and ZEKROM. They fell out three hundred\l"
	.string "years ago over who got the bigger side\l"
	.string "of the roof.\p"
	.string "Now neither will leave, in case the other\n"
	.string "one takes it.\p"
	.string "They only wake up for a CHAMPION.\n"
	.string "Snobs, the both of them.$"

TaoIsland_TowerTop_Text_Elder:
	.string "Go on, CHAMPION, wake one. The other\n"
	.string "will pretend to be asleep.\p"
	.string "It is not asleep. It is listening. It has\n"
	.string "always been listening.$"

TaoIsland_TowerTop_Text_ElderBoth:
	.string "Both of them gone? Then who's been\n"
	.string "snoring under the DRAGON'S DEN all\l"
	.string "these years?\p"
	.string "Something cold, I'd wager. Something\n"
	.string "that misses its brothers.$"
