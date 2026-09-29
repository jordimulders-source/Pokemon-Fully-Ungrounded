MtPyre_5F_MapScripts::
	.byte 0

@ Seems like the scripts for the 4F and 5F were swapped

MtPyre_4F_EventScript_Tasha::
	trainerbattle_single TRAINER_TASHA, MtPyre_4F_Text_TashaIntro, MtPyre_4F_Text_TashaDefeat
	msgbox MtPyre_4F_Text_TashaPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_4F_Text_TashaIntro:
	.string "I love all things horrifying… It's like a\n"
	.string "disease…\p"
	.string "Here… I shiver… Also, it's cold.$"

MtPyre_4F_Text_TashaDefeat:
	.string "Losing, I dislike…$"

MtPyre_4F_Text_TashaPostBattle:
	.string "I want to see dreadful things… I can't\n"
	.string "leave…\p"
	.string "Stay… Stay with me…\p"
	.string "…Forever. Please?$"

