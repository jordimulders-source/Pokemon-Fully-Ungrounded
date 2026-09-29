Route109_SeashoreHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route109_SeashoreHouse_OnTransition
	.byte 0

Route109_SeashoreHouse_OnTransition:
	setflag FLAG_LANDMARK_SEASHORE_HOUSE
	end

Route109_SeashoreHouse_EventScript_Owner::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_6_SODA_POP, Route109_SeashoreHouse_EventScript_AlreadyReceivedSodaPop
	goto_if_set FLAG_DEFEATED_SEASHORE_HOUSE, Route109_SeashoreHouse_EventScript_DefeatedTrainers
	goto_if_set FLAG_TEMP_2, Route109_SeashoreHouse_EventScript_AlreadyGaveIntroduction
	msgbox Route109_SeashoreHouse_Text_SeashoreHouseIntro, MSGBOX_DEFAULT
	setflag FLAG_TEMP_2
	release
	end

Route109_SeashoreHouse_EventScript_AlreadyGaveIntroduction::
	msgbox Route109_SeashoreHouse_Text_ShowMeSomeHotMatches, MSGBOX_DEFAULT
	release
	end

Route109_SeashoreHouse_EventScript_DefeatedTrainers::
	msgbox Route109_SeashoreHouse_Text_TakeTheseSodaPopBottles, MSGBOX_DEFAULT
	giveitem ITEM_SODA_POP, 6
	goto_if_eq VAR_RESULT, FALSE, Route109_SeashoreHouse_EventScript_BagFull
	setflag FLAG_RECEIVED_6_SODA_POP
	release
	end

Route109_SeashoreHouse_EventScript_BagFull::
	msgbox Route109_SeashoreHouse_Text_BagFull, MSGBOX_DEFAULT
	release
	end

Route109_SeashoreHouse_EventScript_AlreadyReceivedSodaPop::
	showmoneybox 0, 0
	msgbox Route109_SeashoreHouse_Text_WantToBuySodaPop, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route109_SeashoreHouse_EventScript_BuySodaPop
	msgbox Route109_SeashoreHouse_Text_ThatsTooBad, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

Route109_SeashoreHouse_EventScript_BuySodaPop::
	checkmoney 300
	goto_if_eq VAR_RESULT, FALSE, Route109_SeashoreHouse_EventScript_NotEnoughMoney
	checkitemspace ITEM_SODA_POP
	goto_if_eq VAR_RESULT, FALSE, Route109_SeashoreHouse_EventScript_NotEnoughSpace
	msgbox Route109_SeashoreHouse_Text_HereYouGo, MSGBOX_DEFAULT
	removemoney 300
	updatemoneybox
.if OW_SHOW_ITEM_DESCRIPTIONS != OW_ITEM_DESCRIPTIONS_OFF
	hidemoneybox
	giveitem ITEM_SODA_POP
.else
	giveitem ITEM_SODA_POP
	hidemoneybox
.endif
	release
	end

Route109_SeashoreHouse_EventScript_NotEnoughMoney::
	msgbox Route109_SeashoreHouse_Text_NotEnoughMoney, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

Route109_SeashoreHouse_EventScript_NotEnoughSpace::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	hidemoneybox
	release
	end

Route109_SeashoreHouse_EventScript_Dwayne::
	trainerbattle_single TRAINER_DWAYNE, Route109_SeashoreHouse_Text_DwayneIntro, Route109_SeashoreHouse_Text_DwayneDefeated, Route109_SeashoreHouse_EventScript_CheckTrainersCompletion
	msgbox Route109_SeashoreHouse_Text_DwaynePostBattle, MSGBOX_AUTOCLOSE
	end

Route109_SeashoreHouse_EventScript_Johanna::
	trainerbattle_single TRAINER_JOHANNA, Route109_SeashoreHouse_Text_JohannaIntro, Route109_SeashoreHouse_Text_JohannaDefeated, Route109_SeashoreHouse_EventScript_CheckTrainersCompletion
	msgbox Route109_SeashoreHouse_Text_JohannaPostBattle, MSGBOX_AUTOCLOSE
	end

Route109_SeashoreHouse_EventScript_Simon::
	trainerbattle_single TRAINER_SIMON, Route109_SeashoreHouse_Text_SimonIntro, Route109_SeashoreHouse_Text_SimonDefeated, Route109_SeashoreHouse_EventScript_CheckTrainersCompletion
	msgbox Route109_SeashoreHouse_Text_SimonPostBattle, MSGBOX_AUTOCLOSE
	end

Route109_SeashoreHouse_EventScript_CheckTrainersCompletion::
	goto_if_not_defeated TRAINER_DWAYNE, Route109_SeashoreHouse_EventScript_TrainersNotCompleted
	goto_if_not_defeated TRAINER_JOHANNA, Route109_SeashoreHouse_EventScript_TrainersNotCompleted
	goto_if_not_defeated TRAINER_SIMON, Route109_SeashoreHouse_EventScript_TrainersNotCompleted
	setflag FLAG_DEFEATED_SEASHORE_HOUSE
	release
	end

Route109_SeashoreHouse_EventScript_TrainersNotCompleted::
	release
	end

Route109_SeashoreHouse_Text_SeashoreHouseIntro:
	.string "I own the SEASHORE HOUSE. Call me MR.\n"
	.string "SEA!\p"
	.string "I love hot POKéMON battles!\p"
	.string "Show me your heart burns hot!\p"
	.string "Beat all the TRAINERS here and I'll\n"
	.string "reward you.$"

Route109_SeashoreHouse_Text_ShowMeSomeHotMatches:
	.string "Show me some hot matches!\p"
	.string "That's the only reason I run this place.\p"
	.string "The food is terrible.$"

Route109_SeashoreHouse_Text_TakeTheseSodaPopBottles:
	.string "Scorching hot! Those battles blazed!\p"
	.string "As thanks, take these!\p"
	.string "Six bottles of SODA POP! Not sparkling\n"
	.string "water. We don't serve that here.$"

Route109_SeashoreHouse_Text_BagFull:
	.string "Your BAG's jammed full. I'll hold on to\n"
	.string "these for you.$"

Route109_SeashoreHouse_Text_WantToBuySodaPop:
	.string "Want some SODA POP? POKéMON love it!\p"
	.string "¥300 a bottle! Buy some!$"

Route109_SeashoreHouse_Text_HereYouGo:
	.string "Here you go!$"

Route109_SeashoreHouse_Text_NotEnoughMoney:
	.string "You don't have the money.$"

Route109_SeashoreHouse_Text_ThatsTooBad:
	.string "No? That's too bad.\p"
	.string "More for me.$"

Route109_SeashoreHouse_Text_DwayneIntro:
	.string "Looking for a battle in the SEASHORE\n"
	.string "HOUSE?\p"
	.string "No hotter TRAINER than me, matey!$"

Route109_SeashoreHouse_Text_DwayneDefeated:
	.string "Hot battle! I accept that loss, matey!$"

Route109_SeashoreHouse_Text_DwaynePostBattle:
	.string "In SLATEPORT I love hot battles and\n"
	.string "ice-cold SODA POP!\p"
	.string "The SODA POP is 90% sugar. Like me.$"

Route109_SeashoreHouse_Text_JohannaIntro:
	.string "Boring battles aren't worth the effort.\p"
	.string "WHITNEY is my idol!\n"
	.string "I've modeled my team after her!\l"
	.string "It's going to be fiery hot!$"

Route109_SeashoreHouse_Text_JohannaDefeated:
	.string "Waaaaah! You're so mean!\n"
	.string "That's... not hot at all!$"

Route109_SeashoreHouse_Text_JohannaPostBattle:
	.string "Whew, I'm all thirsty. Crying and\n"
	.string "battling really takes it out of you.\p"
	.string "Maybe I'll have a MOOMOO MILK...\n"
	.string "I mean, a SODA POP.$"

Route109_SeashoreHouse_Text_SimonIntro:
	.string "I'll show you how great my POKéMON are!\p"
	.string "Don't cry!$"

Route109_SeashoreHouse_Text_SimonDefeated:
	.string "…I lost, but I won't cry…\p"
	.string "…Sniff.$"

Route109_SeashoreHouse_Text_SimonPostBattle:
	.string "If my POKéMON could SURF, I'd ditch this\n"
	.string "inner tube.\p"
	.string "My POKéMON is a CLAMPERL. It can't\n"
	.string "carry me.$"

