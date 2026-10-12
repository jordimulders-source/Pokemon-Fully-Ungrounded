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

Route135_EventScript_Bram::
	trainerbattle_single TRAINER_BRAM, Route135_Text_BramIntro, Route135_Text_BramDefeat
	msgbox Route135_Text_BramPostBattle, MSGBOX_AUTOCLOSE
	end

Route135_EventScript_Lapras::
	lock
	faceplayer
	playmoncry SPECIES_LAPRAS, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_LAPRAS, 51
	dowildbattle
	removeobject LOCALID_ROUTE135_LAPRAS
	setflag FLAG_HIDE_ROUTE135_LAPRAS
	release
	end

@ Project Grounded: Bergmite en Eiscue drijven in het meer; na het verlaten van de kaart zijn ze er weer (tijdelijke vlaggen)
Route135_EventScript_Bergmite::
	lock
	faceplayer
	playmoncry SPECIES_BERGMITE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_BERGMITE, 50
	dowildbattle
	removeobject LOCALID_ROUTE135_BERGMITE
	setflag FLAG_TEMP_11
	release
	end

Route135_EventScript_Eiscue::
	lock
	faceplayer
	playmoncry SPECIES_EISCUE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_EISCUE, 50
	dowildbattle
	removeobject LOCALID_ROUTE135_EISCUE
	setflag FLAG_TEMP_12
	release
	end

Route135_EventScript_Bergmite2::
	lock
	faceplayer
	playmoncry SPECIES_BERGMITE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_BERGMITE, 50
	dowildbattle
	removeobject LOCALID_ROUTE135_BERGMITE_2
	setflag FLAG_TEMP_13
	release
	end

Route135_EventScript_Bergmite3::
	lock
	faceplayer
	playmoncry SPECIES_BERGMITE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_BERGMITE, 50
	dowildbattle
	removeobject LOCALID_ROUTE135_BERGMITE_3
	setflag FLAG_TEMP_14
	release
	end

Route135_EventScript_Eiscue2::
	lock
	faceplayer
	playmoncry SPECIES_EISCUE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_EISCUE, 50
	dowildbattle
	removeobject LOCALID_ROUTE135_EISCUE_2
	setflag FLAG_TEMP_15
	release
	end

Route135_Text_BramIntro:
	.string "Breathe in… and out.\n"
	.string "Thirty times. Then hold it.\p"
	.string "That's the WIM HOF METHOD!\n"
	.string "Deep breathing and ice-cold water.\p"
	.string "My POKéMON and I swim in this lake\n"
	.string "every single day. Let's go!$"

Route135_Text_BramDefeat:
	.string "Brr… I forgot to breathe.$"

Route135_Text_BramPostBattle:
	.string "Cold water, deep breaths.\n"
	.string "You should try it sometime!$"
