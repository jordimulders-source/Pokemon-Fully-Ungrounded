Route136_SuicuneCave_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route136_SuicuneCave_OnResume
	.byte 0

Route136_SuicuneCave_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE136, 12, 44
	setescapewarp MAP_ROUTE136, 51, 26
	end

Route136_SuicuneCave_EventScript_Suicune::
	lock
	faceplayer
	playmoncry SPECIES_SUICUNE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_SUICUNE, 62
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, Route136_SuicuneCave_EventScript_SuicuneStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, Route136_SuicuneCave_EventScript_SuicuneStays
	removeobject LOCALID_ROUTE136_SUICUNE
	setflag FLAG_HIDE_ROUTE136_SUICUNE
Route136_SuicuneCave_EventScript_SuicuneStays::
	release
	end
