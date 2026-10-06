@ Project Grounded: stoomgrot in de vulkaan van het stoomeiland. Volcanion lv 70 (post-game; de ingang gaat pas open
@ na de Hall of Fame). Verslagen = terug na de League (hall_of_fame.inc), gevangen = weg. Teksten zijn placeholders.
SteamIsland_Cave_MapScripts::
	.byte 0

SteamIsland_Cave_EventScript_Volcanion::
	lock
	faceplayer
	msgbox SteamIsland_Cave_Text_Volcanion, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_VOLCANION, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_VOLCANION, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SteamIsland_Cave_EventScript_VolcanionCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SteamIsland_Cave_EventScript_VolcanionDefeated
	msgbox SteamIsland_Cave_Text_VolcanionStays, MSGBOX_DEFAULT
	release
	end

SteamIsland_Cave_EventScript_VolcanionCaught::
	setflag FLAG_CAUGHT_VOLCANION
SteamIsland_Cave_EventScript_VolcanionDefeated::
	setflag FLAG_DEFEATED_VOLCANION
	removeobject LOCALID_STEAM_CAVE_VOLCANION
	release
	end

SteamIsland_Cave_Text_Volcanion:
	.string "VOLCANION is venting steam from the\n"
	.string "ring on its back.\p"
	.string "It doesn't like humans.\n"
	.string "It has been watching your team.\p"
	.string "It especially doesn't like you.$"

SteamIsland_Cave_Text_VolcanionStays:
	.string "VOLCANION is still here, steaming.\n"
	.string "Literally and emotionally.$"
