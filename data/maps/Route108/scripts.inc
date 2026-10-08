Route108_MapScripts::
	.byte 0

Route108_EventScript_Jerome::
	trainerbattle_single TRAINER_JEROME, Route108_Text_JeromeIntro, Route108_Text_JeromeDefeated
	msgbox Route108_Text_JeromePostBattle, MSGBOX_AUTOCLOSE
	end

Route108_EventScript_Matthew::
	trainerbattle_single TRAINER_MATTHEW, Route108_Text_MatthewIntro, Route108_Text_MatthewDefeated
	msgbox Route108_Text_MatthewPostBattle, MSGBOX_AUTOCLOSE
	end

Route108_EventScript_Tara::
	trainerbattle_single TRAINER_TARA, Route108_Text_TaraIntro, Route108_Text_TaraDefeated
	msgbox Route108_Text_TaraPostBattle, MSGBOX_AUTOCLOSE
	end

Route108_EventScript_Missy::
	trainerbattle_single TRAINER_MISSY, Route108_Text_MissyIntro, Route108_Text_MissyDefeated
	msgbox Route108_Text_MissyPostBattle, MSGBOX_AUTOCLOSE
	end

Route108_EventScript_Carolina::
	trainerbattle_single TRAINER_CAROLINA, Route108_Text_CarolinaIntro, Route108_Text_CarolinaDefeated
	msgbox Route108_Text_CarolinaPostBattle, MSGBOX_AUTOCLOSE
	end

Route108_EventScript_Cory::
	trainerbattle_single TRAINER_CORY_1, Route108_Text_CoryIntro, Route108_Text_CoryDefeated, Route108_EventScript_CoryRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route108_EventScript_CoryRematch
	msgbox Route108_Text_CoryPostBattle, MSGBOX_DEFAULT
	release
	end

Route108_EventScript_CoryRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route108_Text_CoryRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CORY_1
	release
	end

Route108_EventScript_CoryRematch::
	trainerbattle_rematch TRAINER_CORY_1, Route108_Text_CoryRematchIntro, Route108_Text_CoryRematchDefeated
	msgbox Route108_Text_CoryRematchPostBattle, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route108_EventScript_ZV2Adjuster::
	msgbox Route108_Text_ZV2Adjuster, MSGBOX_NPC
	end

Route108_Text_ZV2Adjuster:
	.string "I'm from the insurance company.\nClaim number 4471: that ship.\pCause of loss, it says here:\n'KYOGRE.'\pThat's an act of god. Not covered.\nNeither is 'GHOSTS'. Neither is\l'we forgot where we parked it'.$"

Route108_EventScript_ZV2JoLeo::
	trainerbattle_double TRAINER_SIS_AND_BRO_JO_AND_LEO, Route108_Text_ZV2JoLeo_Intro, Route108_Text_ZV2JoLeo_Defeat, Route108_Text_ZV2JoLeo_NotEnough
	msgbox Route108_Text_ZV2JoLeo_Post, MSGBOX_AUTOCLOSE
	end

Route108_Text_ZV2JoLeo_Intro:
	.string "JO: Dad left us the salvage\nbusiness!\pLEO: The business is one rope.\nAnd this sandbank.$"

Route108_Text_ZV2JoLeo_Defeat:
	.string "JO: We lost the rope.\nLEO: We ARE the rope now.$"

Route108_Text_ZV2JoLeo_NotEnough:
	.string "JO: Two of us, two of yours.\nLEO: Family rules. Bring a friend.$"

Route108_Text_ZV2JoLeo_Post:
	.string "LEO: Everything on that ship is\nours by salvage law.\pJO: The ghosts disagree.\nThey have a lawyer. He's also dead.$"
@ --- einde zee_vulling_2 ---
