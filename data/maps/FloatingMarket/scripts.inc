@ Project Grounded: de drijvende markt ten noorden van Route 133 (ZEE_PLAN.md). Kaart: tools/grounded/maptools/sea_market_steam.py.
@ De rondreizende handelaar verkoopt elke dag iets anders (src/floating_market.c). Teksten zijn placeholders.
FloatingMarket_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, FloatingMarket_OnResume
	.byte 0

FloatingMarket_OnResume:
	setstepcallback STEP_CB_PACIFIDLOG_BRIDGE
	end

FloatingMarket_EventScript_Merchant::
	lock
	faceplayer
	message FloatingMarket_Text_MerchantHello
	waitmessage
	setvar VAR_0x8004, 0
	special FloatingMarket_OpenShop
	waitstate
	msgbox FloatingMarket_Text_MerchantBye, MSGBOX_DEFAULT
	release
	end

FloatingMarket_EventScript_MerchantDoor::
	msgbox FloatingMarket_Text_MerchantDoor, MSGBOX_SIGN
	end

FloatingMarket_EventScript_Crate::
	msgbox FloatingMarket_Text_Crate, MSGBOX_SIGN
	end

FloatingMarket_EventScript_Haggler::
	msgbox FloatingMarket_Text_Haggler, MSGBOX_NPC
	end

FloatingMarket_EventScript_Fishmonger::
	msgbox FloatingMarket_Text_Fishmonger, MSGBOX_NPC
	end

FloatingMarket_EventScript_FishCrate::
	msgbox FloatingMarket_Text_FishCrate, MSGBOX_SIGN
	end

FloatingMarket_EventScript_FishmongerDoor::
	msgbox FloatingMarket_Text_FishmongerDoor, MSGBOX_SIGN
	end

FloatingMarket_EventScript_OldFisher::
	msgbox FloatingMarket_Text_OldFisher, MSGBOX_NPC
	end

FloatingMarket_EventScript_RaftRenter::
	msgbox FloatingMarket_Text_RaftRenter, MSGBOX_NPC
	end

FloatingMarket_EventScript_RenterDoor::
	msgbox FloatingMarket_Text_RenterDoor, MSGBOX_SIGN
	end

FloatingMarket_EventScript_Tuber::
	msgbox FloatingMarket_Text_Tuber, MSGBOX_NPC
	end

@ De Wingull die jat: elke keer dat je hem aanspreekt pikt hij een Poké Ball (als je er een hebt). Dat is alles.
FloatingMarket_EventScript_Wingull::
	lock
	faceplayer
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
	waitmoncry
	checkitem ITEM_POKE_BALL
	goto_if_eq VAR_RESULT, FALSE, FloatingMarket_EventScript_WingullNoBall
	removeitem ITEM_POKE_BALL
	playse SE_BALL
	msgbox FloatingMarket_Text_WingullStole, MSGBOX_DEFAULT
	release
	end

FloatingMarket_EventScript_WingullNoBall::
	msgbox FloatingMarket_Text_WingullNoBall, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
FloatingMarket_Text_MerchantHello:
	.string "New stock every day! Not better stock.\n"
	.string "Just different stock.$"

FloatingMarket_Text_MerchantBye:
	.string "I'm a wandering merchant. Well, a\n"
	.string "drifting one. The anchor was the first\l"
	.string "thing I ever sold.$"

FloatingMarket_Text_MerchantDoor:
	.string "“BACK IN 5 MINUTES.”\p"
	.string "The note is dated 1998.$"

FloatingMarket_Text_Crate:
	.string "A crate full of something that rattles.\n"
	.string "The label says “DO NOT SHAKE.”\p"
	.string "You don't shake it.\n"
	.string "Character growth.$"

FloatingMarket_Text_Haggler:
	.string "I've been haggling over a BOTTLE CAP\n"
	.string "for three hours.\p"
	.string "It's not about the money anymore.\n"
	.string "It's about winning.$"

FloatingMarket_Text_Fishmonger:
	.string "Fresh fish! Fresh-ish fish!\p"
	.string "The MAGIKARP on ice are not for sale.\n"
	.string "They're just resting. Forever.\p"
	.string "And watch out for that WINGULL.\n"
	.string "It has a better pension than me.$"

FloatingMarket_Text_FishCrate:
	.string "A crate of fish on ice.\n"
	.string "One of them winks at you.$"

FloatingMarket_Text_FishmongerDoor:
	.string "“CLOSED. GONE FISHING.”\p"
	.string "The fishmonger is standing right\n"
	.string "there. Not fishing.$"

FloatingMarket_Text_OldFisher:
	.string "I've fished off this raft for forty\n"
	.string "years. Never caught a thing.\p"
	.string "The raft drifted fourteen kilometers,\n"
	.string "though. So that's something.$"

FloatingMarket_Text_RaftRenter:
	.string "RAFT RENTAL! 500 an hour!\p"
	.string "… … …\n"
	.string "You're surfing on a POKéMON.\p"
	.string "Yeah. Business has been rough since\n"
	.string "those became a thing.$"

FloatingMarket_Text_RenterDoor:
	.string "“RAFTS FOR RENT. INQUIRE WITHIN.”\p"
	.string "It's locked. Nobody has inquired\n"
	.string "within since 2003.$"

FloatingMarket_Text_Tuber:
	.string "My mom says the whole market floats.\p"
	.string "I asked what happens when it stops\n"
	.string "floating. She went very quiet.$"

FloatingMarket_Text_WingullStole:
	.string "WINGULL snatched a POKé BALL from\n"
	.string "your BAG!\p"
	.string "It doesn't fly off. It just stares\n"
	.string "at you. It knows you know.$"

FloatingMarket_Text_WingullNoBall:
	.string "WINGULL rummages through your BAG.\n"
	.string "No POKé BALLS.\p"
	.string "It looks disappointed in you\n"
	.string "as a person.$"
