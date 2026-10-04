MossdeepCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MossdeepCity_OnTransition
	.byte 0

MossdeepCity_OnTransition:
	call MossdeepCity_EventScript_SetScottDisguise
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_1
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_2
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_3
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_4
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

MossdeepCity_EventScript_PokefanF::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_DIVE, MossdeepCity_EventScript_PokefanFMagmaGone
	msgbox MossdeepCity_Text_SpaceCenterReceivedLetter, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_PokefanFMagmaGone::
	msgbox MossdeepCity_Text_SpaceCenterLaunchingRockets, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_Sailor::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_DIVE, MossdeepCity_EventScript_SailorMagmaGone
	msgbox MossdeepCity_Text_MossdeepTargetedByMagma, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_SailorMagmaGone::
	msgbox MossdeepCity_Text_FeelReliefOnLand, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_NinjaBoy::
	msgbox MossdeepCity_Text_WailmerWatching, MSGBOX_NPC
	end

MossdeepCity_EventScript_ExpertM::
	msgbox MossdeepCity_Text_LifeNeedsSeaToLive, MSGBOX_NPC
	end

MossdeepCity_EventScript_Girl::
	msgbox MossdeepCity_Text_NiceIfWorldCoveredByFlowers, MSGBOX_NPC
	end

MossdeepCity_EventScript_Woman::
	msgbox MossdeepCity_Text_SpecialSpaceCenterRock, MSGBOX_NPC
	end

MossdeepCity_EventScript_WhiteRock::
	msgbox MossdeepCity_Text_ItsAWhiteRock, MSGBOX_SIGN
	end

MossdeepCity_EventScript_GymSign::
	msgbox MossdeepCity_Text_GymSign, MSGBOX_SIGN
	end

MossdeepCity_EventScript_CitySign::
	msgbox MossdeepCity_Text_CitySign, MSGBOX_SIGN
	end

MossdeepCity_EventScript_SpaceCenterSign::
	msgbox MossdeepCity_Text_SpaceCenterSign, MSGBOX_SIGN
	end

MossdeepCity_EventScript_VisitedMossdeep::
	setflag FLAG_VISITED_MOSSDEEP_CITY
	setvar VAR_TEMP_1, 1
	end

MossdeepCity_EventScript_TeamMagmaEnterSpaceCenter::
	lockall
	applymovement LOCALID_MOSSDEEP_MAXIE, MossdeepCity_Movement_MaxieGestureToSpaceCenter
	waitmovement 0
	applymovement LOCALID_MOSSDEEP_GRUNT_1, MossdeepCity_Movement_GruntFaceSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_2, MossdeepCity_Movement_GruntFaceSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_3, MossdeepCity_Movement_GruntFaceSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_4, MossdeepCity_Movement_GruntFaceSpaceCenter
	waitmovement 0
	applymovement LOCALID_MOSSDEEP_MAXIE, MossdeepCity_Movement_MaxieEnterSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_1, MossdeepCity_Movement_Grunt1EnterSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_2, MossdeepCity_Movement_Grunt2EnterSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_3, MossdeepCity_Movement_Grunt3EnterSpaceCenter
	applymovement LOCALID_MOSSDEEP_GRUNT_4, MossdeepCity_Movement_Grunt4EnterSpaceCenter
	waitmovement 0
	removeobject LOCALID_MOSSDEEP_MAXIE
	removeobject LOCALID_MOSSDEEP_GRUNT_1
	removeobject LOCALID_MOSSDEEP_GRUNT_2
	removeobject LOCALID_MOSSDEEP_GRUNT_3
	removeobject LOCALID_MOSSDEEP_GRUNT_4
	delay 30
	setvar VAR_MOSSDEEP_CITY_STATE, 2
	setflag FLAG_HIDE_MOSSDEEP_CITY_TEAM_MAGMA
	releaseall
	end

MossdeepCity_Movement_MaxieGestureToSpaceCenter:
	delay_16
	face_right
	delay_16
	delay_16
	delay_16
	delay_16
	face_left
	delay_16
	delay_16
	step_end

MossdeepCity_Movement_GruntFaceSpaceCenter:
	face_right
	delay_16
	delay_16
	delay_16
	step_end

MossdeepCity_Movement_MaxieEnterSpaceCenter:
	walk_down
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MossdeepCity_Movement_Grunt1EnterSpaceCenter:
	delay_16
	delay_8
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MossdeepCity_Movement_Grunt2EnterSpaceCenter:
	delay_16
	delay_8
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MossdeepCity_Movement_Grunt3EnterSpaceCenter:
	delay_16
	delay_8
	walk_down
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MossdeepCity_Movement_Grunt4EnterSpaceCenter:
	delay_16
	delay_8
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

MossdeepCity_EventScript_Man::
	lock
	faceplayer
	msgbox MossdeepCity_Text_SurfExhilarating, MSGBOX_DEFAULT
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

MossdeepCity_EventScript_KingsRockBoy::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_KINGS_ROCK, MossdeepCity_EventScript_ReceivedKingsRock
	msgbox MossdeepCity_Text_WantKingsRockStevenGaveMe, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MossdeepCity_EventScript_DeclineKingsRock
	msgbox MossdeepCity_Text_YouCanKeepIt, MSGBOX_DEFAULT
	giveitem ITEM_KINGS_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_KINGS_ROCK
	release
	end

MossdeepCity_EventScript_ReceivedKingsRock::
	msgbox MossdeepCity_Text_StevensHouseOverThere, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_DeclineKingsRock::
	msgbox MossdeepCity_Text_WhatToDoWithWeirdRock, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_BlackBelt::
	msgbox MossdeepCity_Text_SootopolisNewGymLeader, MSGBOX_NPC
	end

MossdeepCity_EventScript_Scott::
	lock
	faceplayer
	msgbox MossdeepCity_Text_ScottSomethingWrongWithTown, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_NORTH, MossdeepCity_EventScript_ScottExitNorth
	call_if_eq VAR_FACING, DIR_EAST, MossdeepCity_EventScript_ScottExitEast
	addvar VAR_SCOTT_STATE, 1
	removeobject LOCALID_MOSSDEEP_SCOTT
	release
	end

MossdeepCity_EventScript_ScottExitNorth::
	applymovement LOCALID_PLAYER, MossdeepCity_Movement_PlayerWatchScottExit
	applymovement LOCALID_MOSSDEEP_SCOTT, MossdeepCity_Movement_ScottExitNorth
	waitmovement 0
	return

MossdeepCity_EventScript_ScottExitEast::
	applymovement LOCALID_PLAYER, MossdeepCity_Movement_PlayerWatchScottExit
	applymovement LOCALID_MOSSDEEP_SCOTT, MossdeepCity_Movement_ScottExitEast
	waitmovement 0
	return

MossdeepCity_Movement_PlayerWatchScottExit:
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

MossdeepCity_Movement_ScottExitNorth:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MossdeepCity_Movement_ScottExitEast:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

MossdeepCity_Text_WantKingsRockStevenGaveMe:
	.string "I got this from STEVEN. He called it the\n"
	.string "KING'S ROCK and then screamed for a\l"
	.string "full minute.\p"
	.string "Do you want it?$"

MossdeepCity_Text_YouCanKeepIt:
	.string "Why would you want it? You're weird.\p"
	.string "Keep it. But don't tell STEVEN. He'll\n"
	.string "write a song about it.$"

MossdeepCity_Text_StevensHouseOverThere:
	.string "STEVEN's house is right over there! You\n"
	.string "can hear the double bass from here.$"

MossdeepCity_Text_WhatToDoWithWeirdRock:
	.string "Right? What do you even do with a weird\n"
	.string "rock?\p"
	.string "STEVEN has 400 of them.$"

MossdeepCity_Text_WailmerWatching:
	.string "Around MOSSDEEP you can see wild\n"
	.string "WAILMER. It's called WAILMER watching.\p"
	.string "In anime they'd be giant sea titans.\n"
	.string "Here they just… float.$"

MossdeepCity_Text_SpaceCenterReceivedLetter:
	.string "The SPACE CENTER launches huge\n"
	.string "rockets.\p"
	.string "They got a scary letter recently.\p"
	.string "Probably from the neighbors. The\n"
	.string "rockets are loud.$"

MossdeepCity_Text_SpaceCenterLaunchingRockets:
	.string "The SPACE CENTER keeps launching huge\n"
	.string "rockets.\p"
	.string "None with me on it.$"

MossdeepCity_Text_MossdeepTargetedByMagma:
	.string "A SAILOR buddy says TEAM AQUA set up\n"
	.string "shop in LILYCOVE.\p"
	.string "And someone wiped the floor with them!\p"
	.string "Now TEAM MAGMA wants MOSSDEEP.\p"
	.string "Go check the SPACE CENTER. Bring milk.\n"
	.string "For the spice.$"

MossdeepCity_Text_FeelReliefOnLand:
	.string "I'm a SAILOR. The sea means everything\n"
	.string "to me.\p"
	.string "But after a long voyage, land feels so\n"
	.string "good.\p"
	.string "And the bars are here.$"

MossdeepCity_Text_NiceIfWorldCoveredByFlowers:
	.string "Wouldn't it be nice if the whole world\n"
	.string "was covered in flowers?\p"
	.string "Then we'd all live in space. Because of\n"
	.string "the allergies.$"

MossdeepCity_Text_LifeNeedsSeaToLive:
	.string "All life needs the sea.\p"
	.string "Life runs its course, becomes soil,\n"
	.string "returns to the land.\p"
	.string "Then we launch it into space. That's the\n"
	.string "dream.$"

MossdeepCity_Text_SurfExhilarating:
	.string "A ship is fine.\p"
	.string "But SURFING with POKéMON?\n"
	.string "Exhilarating!\p"
	.string "A rocket would be better. I've applied\n"
	.string "four times.$"

MossdeepCity_Text_SpecialSpaceCenterRock:
	.string "This rock means a lot to the SPACE\n"
	.string "CENTER.\p"
	.string "They wish upon it so their rockets fly\n"
	.string "safely.\p"
	.string "Until they eventually get fucked up by\n"
	.string "DEOXYS.$"

MossdeepCity_Text_ItsAWhiteRock:
	.string "It's a white rock.\p"
	.string "It's just a rock. STEVEN checked.$"

MossdeepCity_Text_GymSign:
	.string "MOSSDEEP CITY POKéMON GYM\n"
	.string "LEADERS: LIZA & TATE\p"
	.string "“The mystic combination! They finish\n"
	.string "each other's… sandwiches.”$"

MossdeepCity_Text_CitySign:
	.string "MOSSDEEP CITY\n"
	.string "“Our slogan: Cherish POKéMON! Our other\l"
	.string "slogan: Get to space.”$"

MossdeepCity_Text_SpaceCenterSign:
	.string "MOSSDEEP SPACE CENTER\n"
	.string "“The closest place to space. Still not\l"
	.string "very close.”$"

MossdeepCity_Text_ScottSomethingWrongWithTown:
	.string "SCOTT: Hi, {PLAYER}{KUN}! Like it? I'm you now.\n"
	.string "I've been you all week. Your mom didn't\l"
	.string "notice.\p"
	.string "… … …\p"
	.string "Okay, okay! Don't look at me like that.\n"
	.string "I'll stop. I promise.\p"
	.string "…People here are talking about a\n"
	.string "warning letter. I didn't write it. This\l"
	.string "time.$"

MossdeepCity_Text_SootopolisNewGymLeader:
	.string "Ahh… The waves on my feet… Nice.\p"
	.string "SOOTOPOLIS has a new GYM LEADER.\p"
	.string "He owns a winery. Or is a winery. Hard to\n"
	.string "say.$"


@ Project Grounded: Scott is steeds vermomd. Hier als de speler zelf.
MossdeepCity_EventScript_SetScottDisguise::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	checkplayergender
	call_if_eq VAR_RESULT, FEMALE, MossdeepCity_EventScript_SetScottDisguiseFemale
	return

MossdeepCity_EventScript_SetScottDisguiseFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

@ Project Grounded: Prof. Birch bij de meteoriet
MossdeepCity_EventScript_Birch::
	lock
	faceplayer
	goto_if_defeated TRAINER_BIRCH_MOSSDEEP, MossdeepCity_EventScript_BirchPostBattle
	msgbox MossdeepCity_Text_BirchMeteorite, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BIRCH_MOSSDEEP, MossdeepCity_Text_BirchDefeat
	msgbox MossdeepCity_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_BirchPostBattle::
	msgbox MossdeepCity_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_Meteorite::
	msgbox MossdeepCity_Text_Meteorite, MSGBOX_SIGN
	end

MossdeepCity_Text_BirchMeteorite:
	.string "BIRCH: {PLAYER}! Don't touch it!\n"
	.string "It came down this morning.\p"
	.string "Everyone in MOSSDEEP says it's\n"
	.string "a METEORITE.\p"
	.string "Look at the shape. The color.\n"
	.string "The faint glow. Smell it.\p"
	.string "That is no rock, {PLAYER}.\n"
	.string "That is a heap of COSMIC POOP.\p"
	.string "EXTRATERRESTRIAL POOP!\n"
	.string "Fresh from the stars!\p"
	.string "Something up there ate something,\n"
	.string "and this is the result.\p"
	.string "A MINIOR? A LUNATONE? A DEOXYS?\n"
	.string "The first space dropping in\l"
	.string "recorded history, and it's MINE.\p"
	.string "This calls for a celebration.\n"
	.string "And you know what that means.\p"
	.string "The MACARENA!\p"
	.string "Did you know it's by LOS DEL RÍO?\n"
	.string "Antonio Romero and Rafael Ruiz,\l"
	.string "two gentlemen from near SEVILLE.\p"
	.string "In 1992 they saw a flamenco dancer\n"
	.string "in VENEZUELA and wrote it on\l"
	.string "the spot. Science works the same.\p"
	.string "MACARENA is the middle name of\n"
	.string "Antonio's daughter. Lucky girl.\p"
	.string "But the one EVERYONE knows is\n"
	.string "the BAYSIDE BOYS remix from MIAMI.\p"
	.string "They added the English verses.\n"
	.string "Fourteen weeks at number one\l"
	.string "in the USA, in 1996!\p"
	.string "Did you know a whole political\n"
	.string "convention danced it that year?\p"
	.string "Did you know the song is about\n"
	.string "a girl whose boyfriend VITORINO\l"
	.string "joins the army…\p"
	.string "…and she spends the time with\n"
	.string "two of his friends?\p"
	.string "Did you know I know all the\n"
	.string "moves? Hands. Hands. Shoulders.\l"
	.string "Head. Hips.\p"
	.string "And did you know my team knows\n"
	.string "them too? Hit it!$"

MossdeepCity_Text_BirchDefeat:
	.string "BIRCH: Houston, we have\n"
	.string "a problem.$"

MossdeepCity_Text_BirchPostBattle:
	.string "BIRCH: The rock is still warm.\p"
	.string "I'm choosing to believe that's\n"
	.string "re-entry heat.$"

MossdeepCity_Text_Meteorite:
	.string "A strange glowing stone.\n"
	.string "It's still warm. Suspiciously warm.$"
