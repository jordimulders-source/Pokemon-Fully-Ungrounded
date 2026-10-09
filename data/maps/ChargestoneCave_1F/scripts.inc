@ Project Grounded: ChargestoneCave_1F (tools/grounded/maptools/chargestone.py)
ChargestoneCave_1F_MapScripts::
	.byte 0

ChargestoneCave_1F_EventScript_Grunt::
	trainerbattle_single TRAINER_CHARGESTONE_GRUNT_1F, ChargestoneCave_1F_Text_GruntIntro, ChargestoneCave_1F_Text_GruntDefeat
	msgbox ChargestoneCave_1F_Text_GruntPost, MSGBOX_AUTOCLOSE
	end

ChargestoneCave_1F_EventScript_Plaque::
	msgbox ChargestoneCave_1F_Text_Plaque, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ChargestoneCave_1F_Text_GruntIntro:
	.string "Halt! This cave is property of TEAM\n"
	.string "PLASMA's research division.\p"
	.string "Which is one man. And us. We're the\n"
	.string "division's legs.$"

ChargestoneCave_1F_Text_GruntDefeat:
	.string "My legs have been defeated.$"

ChargestoneCave_1F_Text_GruntPost:
	.string "COLRESS? Nice? Who told you that?\p"
	.string "The man once fired an intern for saying\n"
	.string "'good morning' without a hypothesis.$"

ChargestoneCave_1F_Text_Plaque:
	.string "CHARGESTONE CAVE\p"
	.string "The stones float because of magnetism.\n"
	.string "Do not lick the stones.\p"
	.string "Someone has added in marker: 'the\n"
	.string "stones float because of ZERAORA. Lick\l"
	.string "at own risk.'$"
