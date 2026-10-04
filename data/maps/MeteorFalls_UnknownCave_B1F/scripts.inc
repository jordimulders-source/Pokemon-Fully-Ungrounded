MeteorFalls_UnknownCave_B1F_MapScripts::
	.byte 0

@ Project Grounded: Mewtwo onderin de verborgen grot achter Meteor Falls (post-game, Cerulean Cave-hommage)
MeteorFalls_UnknownCave_B1F_EventScript_Mewtwo::
	lock
	faceplayer
	msgbox MeteorFalls_UnknownCave_B1F_Text_Mewtwo, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MEWTWO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MeteorFalls_UnknownCave_B1F_EventScript_MewtwoStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MeteorFalls_UnknownCave_B1F_EventScript_MewtwoStays
	removeobject LOCALID_UNKNOWN_CAVE_MEWTWO
	setflag FLAG_HIDE_METEOR_FALLS_MEWTWO
MeteorFalls_UnknownCave_B1F_EventScript_MewtwoStays::
	release
	end

MeteorFalls_UnknownCave_B1F_Text_Mewtwo:
	.string "A voice echoes inside your head.\p"
	.string "“I was made to be the strongest.\n"
	.string "You were made by accident.”\p"
	.string "“Let us see which one of us\n"
	.string "the universe regrets more.”$"
