.global Route102_MiniForest_MapScripts
Route102_MiniForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route102_MiniForest_OnTransition
	.byte 0

@ Project Grounded: Mega Forest (tools/grounded/maptools/mega_forest.py). In de noordrand ligt een omgevallen
@ reuzenboom, met links het roestige zwaard en rechts het roestige schild. Na de Hall of Fame is de boom weg
@ (de weg naar het Mega Forest, Zacian en Zamazenta) en kun je zwaard en schild oppakken.
Route102_MiniForest_OnTransition:
	call_if_set FLAG_SYS_GAME_CLEAR, Route102_MiniForest_EventScript_ClearLog
	end

Route102_MiniForest_EventScript_ClearLog::
	setflag FLAG_HIDE_MINI_FOREST_GIANT_LOG
	return

Route102_MiniForest_EventScript_GiantLog::
	msgbox Route102_MiniForest_Text_GiantLog, MSGBOX_SIGN
	end

Route102_MiniForest_EventScript_RustedSword::
	lock
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route102_MiniForest_EventScript_SwordStuck
	msgbox Route102_MiniForest_Text_SwordFree, MSGBOX_DEFAULT
	giveitem ITEM_RUSTED_SWORD
	goto_if_eq VAR_RESULT, FALSE, Route102_MiniForest_EventScript_BagFull
	removeobject LOCALID_MINI_FOREST_RUSTED_SWORD
	setflag FLAG_RECEIVED_RUSTED_SWORD
	release
	end

Route102_MiniForest_EventScript_SwordStuck::
	msgbox Route102_MiniForest_Text_SwordStuck, MSGBOX_DEFAULT
	release
	end

Route102_MiniForest_EventScript_RustedShield::
	lock
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route102_MiniForest_EventScript_ShieldStuck
	msgbox Route102_MiniForest_Text_ShieldFree, MSGBOX_DEFAULT
	giveitem ITEM_RUSTED_SHIELD
	goto_if_eq VAR_RESULT, FALSE, Route102_MiniForest_EventScript_BagFull
	removeobject LOCALID_MINI_FOREST_RUSTED_SHIELD
	setflag FLAG_RECEIVED_RUSTED_SHIELD
	release
	end

Route102_MiniForest_EventScript_ShieldStuck::
	msgbox Route102_MiniForest_Text_ShieldStuck, MSGBOX_DEFAULT
	release
	end

Route102_MiniForest_EventScript_BagFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	release
	end

Route102_MiniForest_Text_GiantLog:
	.string "A colossal fallen tree plugs the gap.\p"
	.string "It has been lying here so long that\n"
	.string "the moss has started paying rent.\p"
	.string "From the other side comes a deep,\n"
	.string "slow snoring. Two snores, actually.\l"
	.string "In harmony.$"

Route102_MiniForest_Text_SwordStuck:
	.string "A rusted sword, stuck point-first\n"
	.string "in the dirt.\p"
	.string "It won't budge. It gives off the\n"
	.string "energy of an item that is “not for\l"
	.string "you yet.”$"

Route102_MiniForest_Text_SwordFree:
	.string "The rusted sword slides out of the\n"
	.string "ground, as if it had been waiting\l"
	.string "for someone with a Hall of Fame\l"
	.string "entry.$"

Route102_MiniForest_Text_ShieldStuck:
	.string "A rusted shield, half sunk into the\n"
	.string "roots.\p"
	.string "Someone carved “DO NOT TOUCH” into\n"
	.string "it. Someone else carved “OK.”$"

Route102_MiniForest_Text_ShieldFree:
	.string "The rusted shield comes loose.\n"
	.string "It's heavier than it looks.\p"
	.string "It's also, somehow, warm.$"
