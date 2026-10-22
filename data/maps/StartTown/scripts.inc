StartTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StartTown_OnTransition
	.byte 0

StartTown_OnTransition:
	setflag FLAG_VISITED_LITTLEROOT_TOWN
	end

StartTown_EventScript_TownSign::
	msgbox StartTown_Text_TownSign, MSGBOX_SIGN
	end

StartTown_EventScript_MartEmployee::
	msgbox StartTown_Text_MartEmployee, MSGBOX_NPC
	end

StartTown_Text_TownSign:
	.string "START TOWN\n"
	.string "A placeholder with a POKéMON CENTER.$"

StartTown_Text_MartEmployee:
	.string "The real town is still being drawn.\p"
	.string "Until then, this one is load-bearing.\n"
	.string "Please don't lean on the houses.$"
