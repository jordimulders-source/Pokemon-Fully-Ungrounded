Route119_House_MapScripts::
	.byte 0

Route119_House_EventScript_Woman::
	msgbox Route119_House_Text_RumorAboutCaveOfOrigin, MSGBOX_NPC
	end

Route119_House_EventScript_Wingull::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
	msgbox Route119_House_Text_Wingull, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route119_House_Text_RumorAboutCaveOfOrigin:
	.string "Welcome! Mind the WINGULLS!\p"
	.string "I had one. Then two. Now I've stopped\n"
	.string "counting.\p"
	.string "They eat my fish. They sleep in my bed.\n"
	.string "They pay no rent.\p"
	.string "I heard there's a CAVE OF ORIGIN where\n"
	.string "POKéMON spirits are revived.\p"
	.string "If I bring one WINGULL there… do I get\n"
	.string "two back?\p"
	.string "…I'm going to find out.$"

Route119_House_Text_Wingull:
	.string "WINGULL: Pihyoh!$"

