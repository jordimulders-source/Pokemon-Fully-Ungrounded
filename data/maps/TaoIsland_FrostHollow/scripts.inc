@ Project Grounded: Frost Hollow onder de Dragon's Den (layout van de ijskamer van Shoal Cave). GHETSIS is de
@ post-league superboss en geeft de DNA SPLICERS; KYUREM (neutraal, lv 70) pas na hem. tools/grounded/maptools/tao_island.py
TaoIsland_FrostHollow_MapScripts::
	.byte 0

TaoIsland_FrostHollow_EventScript_Ghetsis::
	trainerbattle_single TRAINER_TAO_GHETSIS, TaoIsland_FrostHollow_Text_GhetsisIntro, TaoIsland_FrostHollow_Text_GhetsisDefeat, TaoIsland_FrostHollow_EventScript_GhetsisDefeated
	release
	end

TaoIsland_FrostHollow_EventScript_GhetsisDefeated::
	msgbox TaoIsland_FrostHollow_Text_GhetsisGift, MSGBOX_DEFAULT
	giveitem ITEM_DNA_SPLICERS
	msgbox TaoIsland_FrostHollow_Text_GhetsisLeave, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_TAO_GHETSIS
	setflag FLAG_HIDE_TAO_GHETSIS
	fadescreen FADE_FROM_BLACK
	release
	end

TaoIsland_FrostHollow_EventScript_Kyurem::
	lock
	goto_if_not_defeated TRAINER_TAO_GHETSIS, TaoIsland_FrostHollow_EventScript_KyuremGuarded
	msgbox TaoIsland_FrostHollow_Text_KyuremWake, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_KYUREM, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_KYUREM, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, TaoIsland_FrostHollow_EventScript_KyuremStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, TaoIsland_FrostHollow_EventScript_KyuremStays
	removeobject LOCALID_TAO_KYUREM
	setflag FLAG_HIDE_TAO_KYUREM
TaoIsland_FrostHollow_EventScript_KyuremStays::
	release
	end

TaoIsland_FrostHollow_EventScript_KyuremGuarded::
	msgbox TaoIsland_FrostHollow_Text_KyuremGuarded, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_FrostHollow_Text_GhetsisIntro:
	.string "Ah. The CHAMPION. How convenient.\p"
	.string "I am GHETSIS. I came for KYUREM: the\n"
	.string "empty shell left over when those two\l"
	.string "brothers split up.\p"
	.string "With these DNA SPLICERS I would fill it\n"
	.string "with their power. Alas, both brothers\l"
	.string "are in your bag.\p"
	.string "Hand them over, or I take them. That is\n"
	.string "not a negotiation. That is a weather\l"
	.string "forecast.$"

TaoIsland_FrostHollow_Text_GhetsisDefeat:
	.string "Impossible! I had a cape and\n"
	.string "everything!$"

TaoIsland_FrostHollow_Text_GhetsisGift:
	.string "...Very well. Keep your dragons. Take the\n"
	.string "SPLICERS as well.\p"
	.string "They are useless without both brothers\n"
	.string "and a willingness to do something\l"
	.string "deeply unethical to them.\p"
	.string "I'm told you have the brothers.$"

TaoIsland_FrostHollow_Text_GhetsisLeave:
	.string "TEAM PLASMA will return! Probably. Our\n"
	.string "funding is under review.$"

TaoIsland_FrostHollow_Text_KyuremGuarded:
	.string "KYUREM is frozen in place, glaring at\n"
	.string "the man in the robe.\p"
	.string "Nobody is going anywhere until he's\n"
	.string "dealt with.$"

TaoIsland_FrostHollow_Text_KyuremWake:
	.string "KYUREM looks at you. Then at your bag,\n"
	.string "where its brothers are.\p"
	.string "It would like a word.$"
