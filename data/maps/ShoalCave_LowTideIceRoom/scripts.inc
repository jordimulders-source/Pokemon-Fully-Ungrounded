ShoalCave_LowTideIceRoom_MapScripts::
	.byte 0

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
ShoalCave_LowTideIceRoom_EventScript_KV4Olga::
	trainerbattle_single TRAINER_KV4_EXPERT_OLGA, ShoalCave_LowTideIceRoom_Text_KV4Olga_Intro, ShoalCave_LowTideIceRoom_Text_KV4Olga_Defeat
	msgbox ShoalCave_LowTideIceRoom_Text_KV4Olga_Post, MSGBOX_AUTOCLOSE
	end

ShoalCave_LowTideIceRoom_Text_KV4Olga_Intro:
	.string "You came in at low tide? Brave.\nThe sea locks this room twice\la day.\pI've been locked in since Tuesday.\nI'm fine. My POKéMON are fine.\lWe are all VERY fine.$"

ShoalCave_LowTideIceRoom_Text_KV4Olga_Defeat:
	.string "Warm. You're warm. I'd forgotten\nwhat that was like.$"

ShoalCave_LowTideIceRoom_Text_KV4Olga_Post:
	.string "When the water comes back, I'll\nbe here. Practising my glare.\lIt's the only thing that's warm.$"
@ --- einde kaart_vulling_4 ---
