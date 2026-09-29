FortreeCity_House2_MapScripts::
	.byte 0

FortreeCity_House2_EventScript_HiddenPowerGiver::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_HIDDEN_POWER, FortreeCity_House2_EventScript_ExplainHiddenPower
	call_if_unset FLAG_MET_HIDDEN_POWER_GIVER, FortreeCity_House2_EventScript_Greeting
	msgbox FortreeCity_House2_Text_CoinInWhichHand, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 1, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_CorrectTryAgainWhichHand, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 1, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_CorrectTryAgainWhichHand2, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 0, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_YourHiddenPowerHasAwoken, MSGBOX_DEFAULT
	giveitem ITEM_TM_HIDDEN_POWER
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_HIDDEN_POWER
	msgbox FortreeCity_House2_Text_ExplainHiddenPower, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_EventScript_Greeting::
	msgbox FortreeCity_House2_Text_HiddenPowersArousedByNature, MSGBOX_DEFAULT
	setflag FLAG_MET_HIDDEN_POWER_GIVER
	return

FortreeCity_House2_EventScript_ExplainHiddenPower::
	msgbox FortreeCity_House2_Text_ExplainHiddenPower, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_EventScript_WrongGuess::
	msgbox FortreeCity_House2_Text_YouGuessedWrong, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_Text_HiddenPowersArousedByNature:
	.string "People… POKéMON…\p"
	.string "Nature awakens their hidden powers…\p"
	.string "Also coffee.$"

FortreeCity_House2_Text_CoinInWhichHand:
	.string "Let this old woman see if your hidden\n"
	.string "power has awoken…\p"
	.string "I hold a coin in my hand.\p"
	.string "Which hand? Right or left?$"

FortreeCity_House2_Text_CorrectTryAgainWhichHand:
	.string "Oh! Correct!\p"
	.string "Again. Which hand?$"

FortreeCity_House2_Text_CorrectTryAgainWhichHand2:
	.string "Correct again!\p"
	.string "One more. Which hand? Don't look at my\n"
	.string "sleeve.$"

FortreeCity_House2_Text_YourHiddenPowerHasAwoken:
	.string "Splendid! Your hidden power has awoken!\p"
	.string "Take this and awaken your POKéMON's\n"
	.string "hidden power.\p"
	.string "It was a coin trick. But the TM is real.$"

FortreeCity_House2_Text_ExplainHiddenPower:
	.string "HIDDEN POWER. Its type depends on the\n"
	.string "POKéMON. That's it. That's the move.$"

FortreeCity_House2_Text_YouGuessedWrong:
	.string "No, wrong hand.\p"
	.string "Your hidden power is still asleep. Like\n"
	.string "my husband.$"

