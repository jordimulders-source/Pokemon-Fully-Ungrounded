@ Project Grounded: Tao-toren 3F (layout van de schone Sky Pillar 5F). tools/grounded/maptools/tao_island.py
TaoIsland_Tower3F_MapScripts::
	.byte 0

TaoIsland_Tower3F_EventScript_Ying::
	trainerbattle_single TRAINER_TAO_YING, TaoIsland_Tower3F_Text_YingIntro, TaoIsland_Tower3F_Text_YingDefeat
	msgbox TaoIsland_Tower3F_Text_YingPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_Tower3F_Text_YingIntro:
	.string "Team RESHIRAM! Truth! Fire! Being right,\n"
	.string "with footnotes!$"

TaoIsland_Tower3F_Text_YingDefeat:
	.string "That's... true. Sadly.$"

TaoIsland_Tower3F_Text_YingPost:
	.string "The brothers sleep on the roof. Wake\n"
	.string "one, and the other pretends it didn't\l"
	.string "notice.\p"
	.string "Wake both and it's basically Christmas\n"
	.string "dinner.$"
