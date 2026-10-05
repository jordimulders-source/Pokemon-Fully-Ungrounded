GraniteCave_B2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, GraniteCave_B2F_OnLoad
	.byte 0

@ Project Grounded: Ogerpon-quest. Zodra de maskerhoedster het verhaal heeft verteld, is er een doorgang in de
@ zuidwand (8,22) naar de schuilplaats van Okidogi (GraniteCave_CornerstoneRoom).
GraniteCave_B2F_OnLoad:
	goto_if_unset FLAG_OGERPON_QUEST_STARTED, GraniteCave_B2F_EventScript_NoHideout
	setmetatile 8, 22, 0x23C, FALSE
	setmetatile 7, 23, 0x258, TRUE
	setmetatile 8, 23, 0x259, TRUE
	setmetatile 9, 23, 0x25A, TRUE
GraniteCave_B2F_EventScript_NoHideout:
	end
