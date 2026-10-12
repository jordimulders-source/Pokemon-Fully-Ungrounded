CaveOfOrigin_UnusedRubySapphireMap1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CaveOfOrigin_UnusedRubySapphireMap1_OnTransition
	.byte 0

CaveOfOrigin_UnusedRubySapphireMap1_OnTransition:
	call_if_set FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE, CaveOfOrigin_EventScript_DisableTriggers
	end

@ --- dungeon_extra (gegenereerd door tools/grounded/maptools/dungeon_extra.py) ---
@ Cave of Origin dieper: Primal-lore (placeholders).
CaveOfOrigin_UnusedRubySapphireMap1_EventScript_DXMural::
	msgbox CaveOfOrigin_UnusedRubySapphireMap1_Text_DXMural, MSGBOX_SIGN
	end

CaveOfOrigin_UnusedRubySapphireMap1_EventScript_DXGlyphs::
	msgbox CaveOfOrigin_UnusedRubySapphireMap1_Text_DXGlyphs, MSGBOX_SIGN
	end

CaveOfOrigin_UnusedRubySapphireMap1_Text_DXMural:
	.string "An ancient mural. A huge whale and a\n"
	.string "huge... other whale? No, that one has\l"
	.string "legs.\p"
	.string "They are fighting over a small island.\n"
	.string "The island looks like it would rather\l"
	.string "not be involved.$"

CaveOfOrigin_UnusedRubySapphireMap1_Text_DXGlyphs:
	.string "Old glyphs:\n"
	.string "“WHEN THE SEA ROSE, WE BUILT BOATS.\l"
	.string "WHEN THE LAND ROSE, WE BUILT SMALLER\l"
	.string "BOATS.”\p"
	.string "“WE WERE NOT VERY GOOD AT THIS.”$"
@ --- einde dungeon_extra ---
