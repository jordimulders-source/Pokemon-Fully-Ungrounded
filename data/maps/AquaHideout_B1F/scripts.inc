AquaHideout_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, AquaHideout_B1F_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, AquaHideout_B1F_OnTransition
	.byte 0

AquaHideout_B1F_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, AquaHideout_B1F_EventScript_TryRemoveElectrode
	end

AquaHideout_B1F_EventScript_TryRemoveElectrode::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

AquaHideout_B1F_OnTransition:
	call_if_unset FLAG_DEFEATED_ELECTRODE_1_AQUA_HIDEOUT, AquaHideout_B1F_EventScript_ShowElectrode1
	call_if_unset FLAG_DEFEATED_ELECTRODE_2_AQUA_HIDEOUT, AquaHideout_B1F_EventScript_ShowElectrode2
	end

AquaHideout_B1F_EventScript_ShowElectrode1::
	clearflag FLAG_HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_1
	return

AquaHideout_B1F_EventScript_ShowElectrode2::
	clearflag FLAG_HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_2
	return

AquaHideout_B1F_EventScript_Electrode1::
	lock
	faceplayer
	setwildbattle SPECIES_ELECTRODE, 30
	waitse
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AquaHideout_B1F_EventScript_DefeatedElectrode1
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, AquaHideout_B1F_EventScript_DefeatedElectrode1
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, AquaHideout_B1F_EventScript_DefeatedElectrode1
	setflag FLAG_DEFEATED_ELECTRODE_1_AQUA_HIDEOUT
	release
	end

AquaHideout_B1F_EventScript_DefeatedElectrode1::
	setflag FLAG_DEFEATED_ELECTRODE_1_AQUA_HIDEOUT
	goto Common_EventScript_RemoveStaticPokemon
	end

AquaHideout_B1F_EventScript_Electrode2::
	lock
	faceplayer
	setwildbattle SPECIES_ELECTRODE, 30
	waitse
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, AquaHideout_B1F_EventScript_DefeatedElectrode2
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, AquaHideout_B1F_EventScript_DefeatedElectrode2
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, AquaHideout_B1F_EventScript_DefeatedElectrode2
	setflag FLAG_DEFEATED_ELECTRODE_2_AQUA_HIDEOUT
	release
	end

AquaHideout_B1F_EventScript_DefeatedElectrode2::
	setflag FLAG_DEFEATED_ELECTRODE_2_AQUA_HIDEOUT
	goto Common_EventScript_RemoveStaticPokemon
	end

AquaHideout_B1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_2, AquaHideout_B1F_Text_Grunt2Intro, AquaHideout_B1F_Text_Grunt2Defeat, AquaHideout_B1F_EventScript_Grunt2Defeated
	msgbox AquaHideout_B1F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B1F_EventScript_Grunt2Defeated::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox AquaHideout_B1F_Text_Grunt2PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_B1F_EventScript_Grunt3::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_3, AquaHideout_B1F_Text_Grunt3Intro, AquaHideout_B1F_Text_Grunt3Defeat, AquaHideout_B1F_EventScript_Grunt3Defeated
	msgbox AquaHideout_B1F_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B1F_EventScript_Grunt3Defeated::
	msgbox AquaHideout_B1F_Text_Grunt3PostBattle, MSGBOX_DEFAULT
	release
	end

AquaHideout_B1F_EventScript_Grunt5::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_5, AquaHideout_B1F_Text_Grunt5Intro, AquaHideout_B1F_Text_Grunt5Defeat
	msgbox AquaHideout_B1F_Text_Grunt5PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B1F_EventScript_Grunt7::
	trainerbattle_single TRAINER_GRUNT_AQUA_HIDEOUT_7, AquaHideout_B1F_Text_Grunt7Intro, AquaHideout_B1F_Text_Grunt7Defeat
	msgbox AquaHideout_B1F_Text_Grunt7PostBattle, MSGBOX_AUTOCLOSE
	end

AquaHideout_B1F_Text_Grunt2Intro:
	.string "I've been told to tell nothing about our\n"
	.string "HIDEOUT. But you know how it works in\l"
	.string "this game. You beat me and suddenly my\l"
	.string "filter will slip off!$"

AquaHideout_B1F_Text_Grunt2Defeat:
	.string "Ahhh this is how I become a snitch.$"

AquaHideout_B1F_Text_Grunt2PostBattle:
	.string "So in our HIDEOUT there's a submarine,\n"
	.string "that might play a small but significant\l"
	.string "part in this story. But once you will get\l"
	.string "there the submarine will escape just\l"
	.string "before you will confront it. Anyways, to\l"
	.string "advance the game, you'd still have to go\l"
	.string "there! Good luck!$"

AquaHideout_B1F_Text_Grunt3Intro:
	.string "Fuel supply loaded A-OK! In-cruise\n"
	.string "snacks and booze loaded A-OK!\p"
	.string "Nothing left to do but KO a pesky\n"
	.string "meddler!$"

AquaHideout_B1F_Text_Grunt3Defeat:
	.string "OH SNAP!$"

AquaHideout_B1F_Text_Grunt3PostBattle:
	.string "Humph! This was supposed to happen! I\n"
	.string "am a weak grunt!\p"
	.string "My mission was to just hold you up!\n"
	.string "Mwuahauhaha.$"

AquaHideout_B1F_Text_Grunt5Intro:
	.string "Life in the hideout is boring. You wanna\n"
	.string "gamble? No? Just fight?$"

AquaHideout_B1F_Text_Grunt5Defeat:
	.string "Yawn… Oh, I lost…Should've gambled...$"

AquaHideout_B1F_Text_Grunt5PostBattle:
	.string "Team AQUA will keep on chasing you. We\n"
	.string "are mighty and we have the strongest\l"
	.string "grunts!$"

AquaHideout_B1F_Text_Grunt7Intro:
	.string "Hey! You there!\p"
	.string "Which do you think is cooler? TEAM\n"
	.string "AQUA's uniform or TEAM MAGMA's? Do you\l"
	.string "like pirates?$"

AquaHideout_B1F_Text_Grunt7Defeat:
	.string "Aaargh matey, at least I am still very\n"
	.string "pirate like!$"

AquaHideout_B1F_Text_Grunt7PostBattle:
	.string "If you have a cool uniform, you look\n"
	.string "fashionable even while losing!$"

@ Project Grounded: laptop naast TM51 (Seltzer Surge)
AquaHideout_B1F_EventScript_SeltzerNote::
	msgbox AquaHideout_B1F_Text_SeltzerNote, MSGBOX_SIGN
	end

AquaHideout_B1F_Text_SeltzerNote:
	.string "On this laptop there is a Google\n"
	.string "Doc, reading the following:\p"
	.string "Our hard work, finally paid off.\n"
	.string "The ultimate move.\p"
	.string "This will be a commercial success,\n"
	.string "bottle, ship and sell it!\p"
	.string "Sparkling water forever!$"
