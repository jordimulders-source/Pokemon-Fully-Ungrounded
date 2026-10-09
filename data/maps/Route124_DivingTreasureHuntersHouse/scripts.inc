Route124_DivingTreasureHuntersHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route124_DivingTreasureHuntersHouse_OnTransition
	.byte 0

Route124_DivingTreasureHuntersHouse_OnTransition:
	setflag FLAG_LANDMARK_HUNTERS_HOUSE
	end

Route124_DivingTreasureHuntersHouse_EventScript_TreasureHunter::
	lock
	faceplayer
	checkitem ITEM_SEA_SHARD
	goto_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_SeaShards
	goto_if_set FLAG_MET_DIVING_TREASURE_HUNTER, Route124_DivingTreasureHuntersHouse_EventScript_SkipGreeting
	msgbox Route124_DivingTreasureHuntersHouse_Text_Greeting, MSGBOX_DEFAULT
	setflag FLAG_MET_DIVING_TREASURE_HUNTER
	goto Route124_DivingTreasureHuntersHouse_EventScript_CheckPlayerHasShard
	end

Route124_DivingTreasureHuntersHouse_EventScript_SkipGreeting::
	msgbox Route124_DivingTreasureHuntersHouse_Text_HaveYouSeenAnyShards, MSGBOX_DEFAULT
	goto Route124_DivingTreasureHuntersHouse_EventScript_CheckPlayerHasShard
	end

Route124_DivingTreasureHuntersHouse_EventScript_CheckPlayerHasShard::
	call Route124_DivingTreasureHuntersHouse_EventScript_GetPlayersShards
	goto_if_eq VAR_TEMP_1, 0, Route124_DivingTreasureHuntersHouse_EventScript_NoShards
	goto Route124_DivingTreasureHuntersHouse_EventScript_HasShard
	end

Route124_DivingTreasureHuntersHouse_EventScript_GetPlayersShards::
	setvar VAR_TEMP_1, 0
	checkitem ITEM_RED_SHARD
	call_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_HasRedShard
	checkitem ITEM_YELLOW_SHARD
	call_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_HasYellowShard
	checkitem ITEM_BLUE_SHARD
	call_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_HasBlueShard
	checkitem ITEM_GREEN_SHARD
	call_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_HasGreenShard
	return

Route124_DivingTreasureHuntersHouse_EventScript_HasRedShard::
	addvar VAR_TEMP_1, 1
	return

Route124_DivingTreasureHuntersHouse_EventScript_HasYellowShard::
	addvar VAR_TEMP_1, 2
	return

Route124_DivingTreasureHuntersHouse_EventScript_HasBlueShard::
	addvar VAR_TEMP_1, 4
	return

Route124_DivingTreasureHuntersHouse_EventScript_HasGreenShard::
	addvar VAR_TEMP_1, 8
	return

Route124_DivingTreasureHuntersHouse_EventScript_HasShard::
	msgbox Route124_DivingTreasureHuntersHouse_Text_ThatsAShardIllTradeYou, MSGBOX_DEFAULT
	goto Route124_DivingTreasureHuntersHouse_EventScript_ShowTradeOptions
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShowTradeOptions::
	message Route124_DivingTreasureHuntersHouse_Text_WhatDoYouWantToTrade
	waitmessage
	switch VAR_TEMP_1
	case 1,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsR
	case 2,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsY
	case 3,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRY
	case 4,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsB
	case 5,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRB
	case 6,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYB
	case 7,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYB
	case 8,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsG
	case 9,  Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRG
	case 10, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYG
	case 11, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYG
	case 12, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsBG
	case 13, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRBG
	case 14, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYBG
	case 15, Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYBG
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsR::
	multichoice 0, 0, MULTI_SHARDS_R, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsY::
	multichoice 0, 0, MULTI_SHARDS_Y, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRY::
	multichoice 0, 0, MULTI_SHARDS_RY, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsB::
	multichoice 0, 0, MULTI_SHARDS_B, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRB::
	multichoice 0, 0, MULTI_SHARDS_RB, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYB::
	multichoice 0, 0, MULTI_SHARDS_YB, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYB::
	multichoice 0, 0, MULTI_SHARDS_RYB, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 3, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsG::
	multichoice 0, 0, MULTI_SHARDS_G, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRG::
	multichoice 0, 0, MULTI_SHARDS_RG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYG::
	multichoice 0, 0, MULTI_SHARDS_YG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYG::
	multichoice 0, 0, MULTI_SHARDS_RYG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 3, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsBG::
	multichoice 0, 0, MULTI_SHARDS_BG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRBG::
	multichoice 0, 0, MULTI_SHARDS_RBG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 3, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsYBG::
	multichoice 0, 0, MULTI_SHARDS_YBG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 3, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardOptionsRYBG::
	multichoice 0, 0, MULTI_SHARDS_RYBG, FALSE
	switch VAR_RESULT
	case 0, Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard
	case 1, Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard
	case 2, Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard
	case 3, Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard
	case 4, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_TradeRedShard::
	setvar VAR_0x8008, ITEM_RED_SHARD
	setvar VAR_0x8009, ITEM_FIRE_STONE
	goto Route124_DivingTreasureHuntersHouse_EventScript_TryTradeShard

Route124_DivingTreasureHuntersHouse_EventScript_TradeYellowShard::
	setvar VAR_0x8008, ITEM_YELLOW_SHARD
	setvar VAR_0x8009, ITEM_THUNDER_STONE
	goto Route124_DivingTreasureHuntersHouse_EventScript_TryTradeShard

Route124_DivingTreasureHuntersHouse_EventScript_TradeBlueShard::
	setvar VAR_0x8008, ITEM_BLUE_SHARD
	setvar VAR_0x8009, ITEM_WATER_STONE
	goto Route124_DivingTreasureHuntersHouse_EventScript_TryTradeShard

Route124_DivingTreasureHuntersHouse_EventScript_TradeGreenShard::
	setvar VAR_0x8008, ITEM_GREEN_SHARD
	setvar VAR_0x8009, ITEM_LEAF_STONE
	goto Route124_DivingTreasureHuntersHouse_EventScript_TryTradeShard

Route124_DivingTreasureHuntersHouse_EventScript_TryTradeShard::
	bufferitemname STR_VAR_1, VAR_0x8008
	bufferitemname STR_VAR_2, VAR_0x8009
	msgbox Route124_DivingTreasureHuntersHouse_Text_YoullTradeShardForStone, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	checkitemspace VAR_0x8009
	goto_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_TradeShard
	checkitem VAR_0x8008, 2
	goto_if_eq VAR_RESULT, FALSE, Route124_DivingTreasureHuntersHouse_EventScript_TradeShard
	goto Route124_DivingTreasureHuntersHouse_EventScript_BagFull
	end

Route124_DivingTreasureHuntersHouse_EventScript_TradeShard::
	removeitem VAR_0x8008
	giveitem VAR_0x8009
	msgbox Route124_DivingTreasureHuntersHouse_Text_ItsADeal, MSGBOX_DEFAULT
	call Route124_DivingTreasureHuntersHouse_EventScript_GetPlayersShards
	goto_if_eq VAR_TEMP_1, 0, Route124_DivingTreasureHuntersHouse_EventScript_EndTrade
	msgbox Route124_DivingTreasureHuntersHouse_Text_TradeSomethingElse, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route124_DivingTreasureHuntersHouse_EventScript_ShowTradeOptions
	goto Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade
	end

Route124_DivingTreasureHuntersHouse_EventScript_BagFull::
	msgbox Route124_DivingTreasureHuntersHouse_Text_BagFull, MSGBOX_DEFAULT
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_DeclineTrade::
	msgbox Route124_DivingTreasureHuntersHouse_Text_ComeBackIfYouChangeMind, MSGBOX_DEFAULT
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_NoShards::
	msgbox Route124_DivingTreasureHuntersHouse_Text_YouHaventGotAnyShards, MSGBOX_DEFAULT
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_EndTrade::
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_ShardTradeBoard::
	msgbox Route124_DivingTreasureHuntersHouse_Text_ShardTradeBoard, MSGBOX_SIGN
	end

Route124_DivingTreasureHuntersHouse_Text_Greeting:
	.string "I'm the DIVING TREASURE HUNTER!\p"
	.string "This island feels emptier than ALOLA.\p"
	.string "So I dive. At least the seafloor has\n"
	.string "shards.$"

Route124_DivingTreasureHuntersHouse_Text_HaveYouSeenAnyShards:
	.string "Have you seen any SHARDS of ancient\n"
	.string "tools?\p"
	.string "I need them. Don't ask why.$"

Route124_DivingTreasureHuntersHouse_Text_YouHaventGotAnyShards:
	.string "No treasures for me…\p"
	.string "If you find SHARDS, like a RED SHARD,\n"
	.string "bring them here!$"

Route124_DivingTreasureHuntersHouse_Text_ThatsAShardIllTradeYou:
	.string "Hey! That's a SHARD! I want those!\p"
	.string "Trade it! I'll give you something good!$"

Route124_DivingTreasureHuntersHouse_Text_WhatDoYouWantToTrade:
	.string "What do you want to trade?$"

Route124_DivingTreasureHuntersHouse_Text_YoullTradeShardForStone:
	.string "Your {STR_VAR_1} for my {STR_VAR_2}?$"

Route124_DivingTreasureHuntersHouse_Text_ItsADeal:
	.string "Deal! Use it wisely!\p"
	.string "I'll add the SHARD to my pile. It's a big\n"
	.string "pile.$"

Route124_DivingTreasureHuntersHouse_Text_TradeSomethingElse:
	.string "Trade something else?$"

Route124_DivingTreasureHuntersHouse_Text_BagFull:
	.string "Whoops, your BAG's full. Toss some junk,\n"
	.string "friend!$"

Route124_DivingTreasureHuntersHouse_Text_ComeBackIfYouChangeMind:
	.string "No? Bummer. Come back if you change\n"
	.string "your mind.\p"
	.string "I'm always here. Always. Nobody visits.$"

Route124_DivingTreasureHuntersHouse_Text_ShardTradeBoard:
	.string "{CLEAR_TO 0x0a}Wanted item{CLEAR_TO 0x7c}Trade item\n"
	.string "{CLEAR_TO 0x0f}RED SHARD{CLEAR_TO 0x59}{LEFT_ARROW}{RIGHT_ARROW}{CLEAR_TO 0x7b}FIRE STONE{CLEAR_TO 0xc8}\p"
	.string "{CLEAR_TO 0x0a}Wanted item{CLEAR_TO 0x7c}Trade item\n"
	.string "{CLEAR_TO 0x06}YELLOW SHARD{CLEAR_TO 0x59}{LEFT_ARROW}{RIGHT_ARROW}{CLEAR_TO 0x73}THUNDERSTONE{CLEAR_TO 0xc8}\p"
	.string "{CLEAR_TO 0x0a}Wanted item{CLEAR_TO 0x7c}Trade item\n"
	.string "{CLEAR_TO 0x0c}BLUE SHARD{CLEAR_TO 0x59}{LEFT_ARROW}{RIGHT_ARROW}{CLEAR_TO 0x79}WATER STONE{CLEAR_TO 0xc8}\p"
	.string "{CLEAR_TO 0x0a}Wanted item{CLEAR_TO 0x7c}Trade item\n"
	.string "{CLEAR_TO 0x08}GREEN SHARD{CLEAR_TO 0x59}{LEFT_ARROW}{RIGHT_ARROW}{CLEAR_TO 0x7b}LEAF STONE$"

@ --- coral_cathedral (Sea Shards; gegenereerd door tools/grounded/maptools/coral_cathedral.py) ---
Route124_DivingTreasureHuntersHouse_EventScript_SeaShards::
	goto_if_set FLAG_SEA_SHARDS_EXPLAINED, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsAgain
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardsFirst, MSGBOX_DEFAULT
	setflag FLAG_SEA_SHARDS_EXPLAINED
	goto Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsTake

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsAgain::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardsAgain, MSGBOX_DEFAULT

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsTake::
	removeitem ITEM_SEA_SHARD
	checkitem ITEM_SEA_SHARD
	goto_if_eq VAR_RESULT, TRUE, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsTake
	setvar VAR_TEMP_2, 0
	call_if_set FLAG_ITEM_SEA_SHARD_ROUTE126_CORAL_CATHEDRAL, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_ROUTE128_BUBBLE_GROTTO, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_UNDERWATER_ROUTE127_TRENCH, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_SHIPWRECK_SHOALS, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_UNDERWATER_SEA_TEMPLE, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_ROUTE126_SILENT_CRATER, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_ROUTE127_WELLSPRING_GROTTO, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	call_if_set FLAG_ITEM_SEA_SHARD_UNDERWATER_ROUTE136, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount
	buffernumberstring STR_VAR_1, VAR_TEMP_2
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardsCount, MSGBOX_DEFAULT
	goto_if_lt VAR_TEMP_2, 2, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsDone
	call_if_unset FLAG_SEA_SHARD_REWARD_2, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward2
	goto_if_lt VAR_TEMP_2, 4, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsDone
	call_if_unset FLAG_SEA_SHARD_REWARD_4, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward4
	goto_if_lt VAR_TEMP_2, 6, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsDone
	call_if_unset FLAG_SEA_SHARD_REWARD_6, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward6
	goto_if_lt VAR_TEMP_2, 8, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsDone
	call_if_unset FLAG_SEA_SHARD_REWARD_8, Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward8
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardsAll, MSGBOX_DEFAULT
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardsDone::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardsMore, MSGBOX_DEFAULT
	release
	end

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardCount::
	addvar VAR_TEMP_2, 1
	return

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward2::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardReward2, MSGBOX_DEFAULT
	giveitem ITEM_DIVE_BALL, 10
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_SEA_SHARD_REWARD_2
	return

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward4::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardReward4, MSGBOX_DEFAULT
	giveitem ITEM_HEAVY_DUTY_BOOTS, 1
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_SEA_SHARD_REWARD_4
	return

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward6::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardReward6, MSGBOX_DEFAULT
	giveitem ITEM_GOLD_BOTTLE_CAP, 1
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_SEA_SHARD_REWARD_6
	return

Route124_DivingTreasureHuntersHouse_EventScript_SeaShardReward8::
	msgbox Route124_DivingTreasureHuntersHouse_Text_SeaShardReward8, MSGBOX_DEFAULT
	giveitem ITEM_MASTER_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_SEA_SHARD_REWARD_8
	return

Route124_DivingTreasureHuntersHouse_Text_SeaShardsFirst:
	.string "Hold on. Is that a SEA SHARD?\p"
	.string "Nobody knows what they are. Not me, not\n"
	.string "the professors, not the shards\l"
	.string "themselves.\p"
	.string "But they glow, and in my line of work,\n"
	.string "glowing means money. I'll take every one\l"
	.string "you have.\p"
	.string "In return you get things from the\n"
	.string "seabed that don't glow. That's called a\l"
	.string "business model.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardsAgain:
	.string "More SEA SHARDS! Hand them over. Slowly.\n"
	.string "I've been hurt before.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardsCount:
	.string "That makes {STR_VAR_1} out of the eight I'm\n"
	.string "sure exist.\p"
	.string "I'm sure because I made a list, and lists\n"
	.string "are never wrong.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardReward2:
	.string "Two already! Have some DIVE BALLS. They\n"
	.string "work best underwater. Like me. Unlike my\l"
	.string "marriage.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardReward4:
	.string "Four! Take these HEAVY-DUTY BOOTS.\p"
	.string "I found them on a skeleton on the\n"
	.string "seabed. He won't miss them. He isn't\l"
	.string "going anywhere.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardReward6:
	.string "Six! Here's a GOLD BOTTLE CAP.\p"
	.string "It sealed the captain's private rum on a\n"
	.string "sunken ship. The rum is gone. So is the\l"
	.string "captain. The cap stayed loyal.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardReward8:
	.string "All eight.\p"
	.string "Thirty years I searched for these. You\n"
	.string "did it between two naps. I hate you a\l"
	.string "little.\p"
	.string "Take my greatest treasure: a MASTER\n"
	.string "BALL from a sunken bank vault.\p"
	.string "I never used it. I never met anything\n"
	.string "worth it. That includes people.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardsMore:
	.string "There are more down there. Check every\n"
	.string "place you can dive.\p"
	.string "I'll be here. Slowly drying out. Like a\n"
	.string "sponge with regrets.$"

Route124_DivingTreasureHuntersHouse_Text_SeaShardsAll:
	.string "That's every SEA SHARD in HOENN. I can\n"
	.string "finally retire.\p"
	.string "Where to? Underwater, obviously. Where\n"
	.string "else would I go?$"
@ --- einde coral_cathedral ---
