Route135_MapScripts::
	.byte 0

Route135_EventScript_Birch::
	lock
	faceplayer
	goto_if_defeated TRAINER_BIRCH_2, Route135_EventScript_BirchPostBattle
	msgbox Route135_Text_BirchSnowRock, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BIRCH_2, Route135_Text_BirchDefeat
	msgbox Route135_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

Route135_EventScript_BirchPostBattle::
	msgbox Route135_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

Route135_EventScript_Edmund::
	trainerbattle_single TRAINER_EDMUND, Route135_Text_EdmundIntro, Route135_Text_EdmundDefeat
	msgbox Route135_Text_EdmundPostBattle, MSGBOX_AUTOCLOSE
	end

Route135_EventScript_Tenzing::
	trainerbattle_single TRAINER_TENZING, Route135_Text_TenzingIntro, Route135_Text_TenzingDefeat
	msgbox Route135_Text_TenzingPostBattle, MSGBOX_AUTOCLOSE
	end

Route135_Text_BirchSnowRock:
	.string "BIRCH: Oh, {PLAYER}! Look at this\n"
	.string "rock in the snow.\p"
	.string "I've been studying it all morning.\p"
	.string "…Let's see how much you've grown!$"

Route135_Text_BirchDefeat:
	.string "BIRCH: Well done, {PLAYER}!$"

Route135_Text_BirchPostBattle:
	.string "BIRCH: Back to the rock.$"

Route135_Text_EdmundIntro:
	.string "We've climbed every mountain in HOENN.\n"
	.string "Let's see if you can keep up!$"

Route135_Text_EdmundDefeat:
	.string "You climb faster than we do.$"

Route135_Text_EdmundPostBattle:
	.string "The view from up here is worth\n"
	.string "every step.$"

Route135_Text_TenzingIntro:
	.string "Nobody passes these stairs without\n"
	.string "a battle!$"

Route135_Text_TenzingDefeat:
	.string "Beaten on our own mountain…$"

Route135_Text_TenzingPostBattle:
	.string "Take the stairs up north.\n"
	.string "There's something in the snow.$"
