@ Project Grounded: CeruleanCave_1F (tools/grounded/maptools/spacetime_cave.py)
CeruleanCave_1F_MapScripts::
	.byte 0

CeruleanCave_1F_EventScript_Arlo::
	trainerbattle_single TRAINER_CC_GRUNT_ARLO, CeruleanCave_1F_Text_ArloIntro, CeruleanCave_1F_Text_ArloDefeat
	msgbox CeruleanCave_1F_Text_ArloPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
CeruleanCave_1F_Text_ArloIntro:
	.string "Halt! This cave is property of TEAM\n"
	.string "ROCKET. Well. It will be. We're filling in\l"
	.string "the forms.$"

CeruleanCave_1F_Text_ArloDefeat:
	.string "The forms! You've ruined the forms!$"

CeruleanCave_1F_Text_ArloPost:
	.string "The BOSS says there's a POKéMON down\n"
	.string "here worth more than all of Kanto. I'm\l"
	.string "just here for the dental plan.$"
