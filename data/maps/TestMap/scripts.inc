TestMap_MapScripts::
	.byte 0

@ Keccles blijft te bevechten: na elk gevecht gaat zijn trainerflag weer uit.
TestMap_EventScript_Keccles::
	lock
	faceplayer
	msgbox TestMap_Text_KecclesIntro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TestMap_EventScript_KecclesDeclined
	trainerbattle_no_intro TRAINER_KECCLES_1, TestMap_Text_KecclesDefeat
	cleartrainerflag TRAINER_KECCLES_1
	msgbox TestMap_Text_KecclesPostBattle, MSGBOX_DEFAULT
	release
	end

TestMap_EventScript_KecclesDeclined::
	msgbox TestMap_Text_KecclesDeclined, MSGBOX_DEFAULT
	release
	end

TestMap_EventScript_PC::
	goto EventScript_PC
	end

TestMap_EventScript_Sign::
	msgbox TestMap_Text_Sign, MSGBOX_SIGN
	end

TestMap_Text_KecclesIntro:
	.string "KECCLES: Ah. The test map.\p"
	.string "Everything here gets tested.\n"
	.string "Including me, apparently.\p"
	.string "Battle? For science?$"

TestMap_Text_KecclesDeclined:
	.string "KECCLES: A control group. Sensible.$"

TestMap_Text_KecclesDefeat:
	.string "Results inconclusive.$"

TestMap_Text_KecclesPostBattle:
	.string "KECCLES: Same time tomorrow.\n"
	.string "Or in five seconds. I'll be here.$"

TestMap_Text_Sign:
	.string "TEST MAP\n"
	.string "Everything new gets tried here first.$"
