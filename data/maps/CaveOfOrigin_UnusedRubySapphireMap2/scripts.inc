CaveOfOrigin_UnusedRubySapphireMap2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CaveOfOrigin_UnusedRubySapphireMap2_OnTransition
	.byte 0

CaveOfOrigin_UnusedRubySapphireMap2_OnTransition:
	call_if_set FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE, CaveOfOrigin_EventScript_DisableTriggers
	end

@ --- dungeon_extra (gegenereerd door tools/grounded/maptools/dungeon_extra.py) ---
@ Cave of Origin dieper: Primal-lore (placeholders).
CaveOfOrigin_UnusedRubySapphireMap2_EventScript_DXHelmet::
	msgbox CaveOfOrigin_UnusedRubySapphireMap2_Text_DXHelmet, MSGBOX_SIGN
	end

CaveOfOrigin_UnusedRubySapphireMap2_Text_DXHelmet:
	.string "A MAGMA helmet, half melted, next to an\n"
	.string "AQUA bandana, half dissolved.\p"
	.string "Someone has arranged them in a little\n"
	.string "heart shape. That's worse, somehow.$"
@ --- einde dungeon_extra ---
