@ Project Grounded: Tao-toren 2F (layout van de schone Sky Pillar 2F). tools/grounded/maptools/tao_island.py
TaoIsland_Tower2F_MapScripts::
	.byte 0

TaoIsland_Tower2F_EventScript_Jun::
	trainerbattle_single TRAINER_TAO_JUN, TaoIsland_Tower2F_Text_JunIntro, TaoIsland_Tower2F_Text_JunDefeat
	msgbox TaoIsland_Tower2F_Text_JunPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_Tower2F_Text_JunIntro:
	.string "I'm Team ZEKROM! Ideals! Lightning!\n"
	.string "Being right without any evidence at all!$"

TaoIsland_Tower2F_Text_JunDefeat:
	.string "My ideals have been... grounded.$"

TaoIsland_Tower2F_Text_JunPost:
	.string "Upstairs is a girl who's Team RESHIRAM.\n"
	.string "We've been arguing since Tuesday.\p"
	.string "Tuesday of last year.$"
