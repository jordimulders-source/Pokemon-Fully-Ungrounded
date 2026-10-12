@ Project Grounded: MtCoronet_4F_Room3 (tools/grounded/maptools/coronet.py)
MtCoronet_4F_Room3_MapScripts::
	.byte 0

MtCoronet_4F_Room3_EventScript_Vertex::
	trainerbattle_single TRAINER_CORONET_VERTEX, MtCoronet_4F_Room3_Text_VertexIntro, MtCoronet_4F_Room3_Text_VertexDefeat
	msgbox MtCoronet_4F_Room3_Text_VertexPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
MtCoronet_4F_Room3_Text_VertexIntro:
	.string "Every DRAGON you see is a point in\n"
	.string "space where PALKIA got bored.\p"
	.string "I am the tip of the spear. Literally.\n"
	.string "Look up.$"

MtCoronet_4F_Room3_Text_VertexDefeat:
	.string "Pointless. Which is ironic, for a vertex.$"

MtCoronet_4F_Room3_Text_VertexPost:
	.string "Up the ladder it gets narrower. Space\n"
	.string "does that up here. So does my patience.$"
