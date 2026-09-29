MtPyre_4F_MapScripts::
	.byte 0

@ Seems like the scripts for the 4F and 5F were swapped

MtPyre_5F_EventScript_Atsushi::
	trainerbattle_single TRAINER_ATSUSHI, MtPyre_5F_Text_AtsushiIntro, MtPyre_5F_Text_AtsushiDefeat
	msgbox MtPyre_5F_Text_AtsushiPostBattle, MSGBOX_AUTOCLOSE
	end

MtPyre_5F_Text_AtsushiIntro:
	.string "Teacher said: know your enemy. My enemy\n"
	.string "is INCINEROAR.\p"
	.string "So I raised a SNEASLER. FIGHTING and\n"
	.string "POISON, claws like knives. The ultimate\l"
	.string "answer to that fat cat!$"

MtPyre_5F_Text_AtsushiDefeat:
	.string "Teacher… You said SNEASLER was the\n"
	.string "answer. What was the question?$"

MtPyre_5F_Text_AtsushiPostBattle:
	.string "Until I improve, my teacher, who rests\n"
	.string "here, will never find true peace…$"

