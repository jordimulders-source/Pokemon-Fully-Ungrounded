MauvilleCity_House2_MapScripts::
	.byte 0

MauvilleCity_House2_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_COIN_CASE, MauvilleCity_House2_EventScript_ReceivedCoinCase
	msgbox MauvilleCity_House2_Text_BuyHarborMailAtSlateport, MSGBOX_DEFAULT
	checkitem ITEM_HARBOR_MAIL
	goto_if_eq VAR_RESULT, TRUE, MauvilleCity_House2_EventScript_AskToTradeForHarborMail
	release
	end

MauvilleCity_House2_EventScript_AskToTradeForHarborMail::
	playse SE_PIN
	applymovement VAR_LAST_TALKED, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement VAR_LAST_TALKED, Common_Movement_Delay48
	waitmovement 0
	msgbox MauvilleCity_House2_Text_TradeHarborMailForCoinCase, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, MauvilleCity_House2_EventScript_AcceptTrade
	goto_if_eq VAR_RESULT, NO, MauvilleCity_House2_EventScript_DeclineTrade
	end

MauvilleCity_House2_EventScript_AcceptTrade::
	msgbox MauvilleCity_House2_Text_IllTradeYouCoinCase, MSGBOX_DEFAULT
	giveitem ITEM_COIN_CASE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	removeitem ITEM_HARBOR_MAIL
	setflag FLAG_RECEIVED_COIN_CASE
	goto MauvilleCity_House2_EventScript_ReceivedCoinCase
	end

MauvilleCity_House2_EventScript_ReceivedCoinCase::
	msgbox MauvilleCity_House2_Text_UseCoinCaseAtGameCorner, MSGBOX_DEFAULT
	release
	end

MauvilleCity_House2_EventScript_DeclineTrade::
	msgbox MauvilleCity_House2_Text_ThatsDisappointing, MSGBOX_DEFAULT
	release
	end

MauvilleCity_House2_Text_BuyHarborMailAtSlateport:
	.string "If I had a BIKE, I'd cycle to SLATEPORT\n"
	.string "for shopping.\p"
	.string "I'd buy HARBOR MAIL.\p"
	.string "Wait, mail doesn't exist anymore? Who\n"
	.string "would do that?$"

MauvilleCity_House2_Text_TradeHarborMailForCoinCase:
	.string "Oh! You have HARBOR MAIL? Trade it for\n"
	.string "a COIN CASE?$"

MauvilleCity_House2_Text_IllTradeYouCoinCase:
	.string "I'm so happy! Here's the COIN CASE!\p"
	.string "I'm finally free of it.$"

MauvilleCity_House2_Text_UseCoinCaseAtGameCorner:
	.string "Use that COIN CASE at the GAME CORNER.\p"
	.string "Or don't. I'm serious. Don't.$"

MauvilleCity_House2_Text_ThatsDisappointing:
	.string "Oh, disappointing.\p"
	.string "You need a COIN CASE for the GAME\n"
	.string "CORNER.$"


MauvilleCity_House2_EventScript_HiddenStairs::
	lockall
	msgbox MauvilleCity_House2_Text_HiddenStairs, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	warp MAP_MAUVILLE_CITY_HOUSE2_B1F, 3, 2
	waitstate
	releaseall
	end

MauvilleCity_House2_Text_HiddenStairs:
	.string "There's a staircase hidden behind\n"
	.string "the bookcase. TV noise drifts up.$"
