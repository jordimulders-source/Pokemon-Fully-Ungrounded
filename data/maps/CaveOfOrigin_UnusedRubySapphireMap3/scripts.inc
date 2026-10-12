CaveOfOrigin_UnusedRubySapphireMap3_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CaveOfOrigin_UnusedRubySapphireMap3_OnTransition
	.byte 0

CaveOfOrigin_UnusedRubySapphireMap3_OnTransition:
	call_if_set FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE, CaveOfOrigin_EventScript_DisableTriggers
	end

@ --- dungeon_extra (gegenereerd door tools/grounded/maptools/dungeon_extra.py) ---
@ Cave of Origin dieper: Primal-lore (placeholders).
CaveOfOrigin_UnusedRubySapphireMap3_EventScript_DXOrbs::
	msgbox CaveOfOrigin_UnusedRubySapphireMap3_Text_DXOrbs, MSGBOX_SIGN
	end

CaveOfOrigin_UnusedRubySapphireMap3_EventScript_DXPrimal::
	msgbox CaveOfOrigin_UnusedRubySapphireMap3_Text_DXPrimal, MSGBOX_SIGN
	end

CaveOfOrigin_UnusedRubySapphireMap3_EventScript_DXResearcher::
	msgbox CaveOfOrigin_UnusedRubySapphireMap3_Text_DXResearcher, MSGBOX_NPC
	end

CaveOfOrigin_UnusedRubySapphireMap3_Text_DXOrbs:
	.string "Two empty hollows in the rock, shaped\n"
	.string "like orbs. One red, one blue.\p"
	.string "A note: “BORROWED. WILL RETURN. -A.”\n"
	.string "Underneath: “NO YOU WON'T. -M.”$"

CaveOfOrigin_UnusedRubySapphireMap3_Text_DXPrimal:
	.string "Carved deep into the stone:\n"
	.string "“THE PRIMAL FORM IS THE TRUE FORM.”\p"
	.string "Someone added, in marker:\n"
	.string "“THE TRUE FORM HAS VERY BAD MANNERS.”$"

CaveOfOrigin_UnusedRubySapphireMap3_Text_DXResearcher:
	.string "I'm writing my thesis on PRIMAL\n"
	.string "REVERSION. Twelve years now.\p"
	.string "Chapter one: it is very hot. Chapter\n"
	.string "two: it is very wet. Chapter three is\l"
	.string "mostly me crying.\p"
	.string "My supervisor says the legendaries\n"
	.string "left. I'm staying until they come back\l"
	.string "and sign my consent form.$"
@ --- einde dungeon_extra ---
