FortreeCity_House1_MapScripts::
	.byte 0

FortreeCity_House1_EventScript_Trader::
	lock
	faceplayer
	goto_if_set FLAG_FORTREE_NPC_TRADE_COMPLETED, FortreeCity_House1_EventScript_TradeCompleted
	setvar VAR_0x8008, INGAME_TRADE_PLUSLE
	copyvar VAR_0x8004, VAR_0x8008
	specialvar VAR_RESULT, GetInGameTradeSpeciesInfo
	copyvar VAR_0x8009, VAR_RESULT
	msgbox FortreeCity_House1_Text_YouWillTradeWontYou, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FortreeCity_House1_EventScript_DeclineTrade
	special ChoosePartyMon
	waitstate
	copyvar VAR_0x800A, VAR_0x8004
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, FortreeCity_House1_EventScript_DeclineTrade
	copyvar VAR_0x8005, VAR_0x800A
	specialvar VAR_RESULT, GetTradeSpecies
	copyvar VAR_0x800B, VAR_RESULT
	goto_if_ne VAR_RESULT, VAR_0x8009, FortreeCity_House1_EventScript_NotRequestedMon
	copyvar VAR_0x8004, VAR_0x8008
	copyvar VAR_0x8005, VAR_0x800A
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	waitstate
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox FortreeCity_House1_Text_MonYouTakeCare, MSGBOX_DEFAULT
	setflag FLAG_FORTREE_NPC_TRADE_COMPLETED
	release
	end

FortreeCity_House1_EventScript_DeclineTrade::
	msgbox FortreeCity_House1_Text_YouWontTradeMe, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_NotRequestedMon::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox FortreeCity_House1_Text_ThisIsntAMon, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_TradeCompleted::
	msgbox FortreeCity_House1_Text_GoingToMakeVolbeatStrong, MSGBOX_DEFAULT
	release
	end

@ Project Grounded: tweede ruil in dit huis, Haunter voor Machoke.
FortreeCity_House1_EventScript_ExpertF::
	lock
	faceplayer
	goto_if_set FLAG_FORTREE_HAUNTER_TRADE_COMPLETED, FortreeCity_House1_EventScript_HaunterTradeCompleted
	setvar VAR_0x8008, INGAME_TRADE_HAUNTER
	copyvar VAR_0x8004, VAR_0x8008
	specialvar VAR_RESULT, GetInGameTradeSpeciesInfo
	copyvar VAR_0x8009, VAR_RESULT
	msgbox FortreeCity_House1_Text_HaunterTradeAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FortreeCity_House1_EventScript_HaunterDecline
	special ChoosePartyMon
	waitstate
	copyvar VAR_0x800A, VAR_0x8004
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, FortreeCity_House1_EventScript_HaunterDecline
	copyvar VAR_0x8005, VAR_0x800A
	specialvar VAR_RESULT, GetTradeSpecies
	copyvar VAR_0x800B, VAR_RESULT
	goto_if_ne VAR_RESULT, VAR_0x8009, FortreeCity_House1_EventScript_HaunterWrongMon
	copyvar VAR_0x8004, VAR_0x8008
	copyvar VAR_0x8005, VAR_0x800A
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	waitstate
	msgbox FortreeCity_House1_Text_WhyDidntItEvolve, MSGBOX_DEFAULT
	setflag FLAG_FORTREE_HAUNTER_TRADE_COMPLETED
	release
	end

FortreeCity_House1_EventScript_HaunterDecline::
	msgbox FortreeCity_House1_Text_HaunterTradeDeclined, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_HaunterWrongMon::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox FortreeCity_House1_Text_HaunterWrongMon, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_HaunterTradeCompleted::
	msgbox FortreeCity_House1_Text_StillAMachoke, MSGBOX_DEFAULT
	release
	end

FortreeCity_House1_EventScript_Zigzagoon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
	msgbox FortreeCity_House1_Text_Zigzagoon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

FortreeCity_House1_Text_YouWillTradeWontYou:
	.string "Wrooooaaar! I need a {STR_VAR_1}! It's\n"
	.string "warm! Like a nightlight, but hotter!\p"
	.string "I'll trade my {STR_VAR_2}. It's from GALAR.\n"
	.string "It's a unicorn. I'm too old for unicorns.\l"
	.string "Deal?$"

FortreeCity_House1_Text_MonYouTakeCare:
	.string "Yes! {STR_VAR_1}, welcome!\p"
	.string "{STR_VAR_2}, go be a unicorn somewhere\n"
	.string "else!$"

FortreeCity_House1_Text_ThisIsntAMon:
	.string "Uh, no. That isn't a {STR_VAR_1}. It isn't\n"
	.string "even warm.$"

FortreeCity_House1_Text_YouWontTradeMe:
	.string "No? Fine. I'll keep the unicorn. And my\n"
	.string "shame.$"

FortreeCity_House1_Text_GoingToMakeVolbeatStrong:
	.string "My SLUGMA keeps my room nice and warm.\n"
	.string "My bed is on fire, but still.$"

FortreeCity_House1_Text_TradingMemoriesWithOthers:
	.string "Trading POKéMON with others…\p"
	.string "It's like trading memories.\p"
	.string "Nobody wanted my memories. Or my\n"
	.string "POKéMON.$"

FortreeCity_House1_Text_Zigzagoon:
	.string "ZIGZAGOON: Gumomoh?$"


FortreeCity_House1_Text_HaunterTradeAsk:
	.string "Trade your {STR_VAR_1} for my {STR_VAR_2}?\p"
	.string "We both get a MACHAMP and a GENGAR out\n"
	.string "of it! That's how trading works! Deal?$"

FortreeCity_House1_Text_HaunterTradeDeclined:
	.string "No? Your loss. Double evolution!$"

FortreeCity_House1_Text_HaunterWrongMon:
	.string "That's not a {STR_VAR_1}. That's not even\n"
	.string "close.$"

FortreeCity_House1_Text_WhyDidntItEvolve:
	.string "Now watch! It's gonna evolve!\p"
	.string "… … …\p"
	.string "…Wait. Why didn't it evolve?\p"
	.string "…Oh right. Evolution methods were\n"
	.string "changed in this game. Level 37 now.\l"
	.string "Yours too, by the way.\p"
	.string "Enjoy your HAUNTER, I guess.$"

FortreeCity_House1_Text_StillAMachoke:
	.string "My MACHOKE is still a MACHOKE. Seven\n"
	.string "more levels. Or fifteen.$"
