Route102_MapScripts::
	.byte 0

Route102_EventScript_LittleBoy::
	msgbox Route102_Text_ImNotVeryTall, MSGBOX_NPC
	end

Route102_EventScript_RouteSignOldale::
	msgbox Route102_Text_RouteSignOldale, MSGBOX_SIGN
	end

Route102_EventScript_RouteSignPetalburg::
	msgbox Route102_Text_RouteSignPetalburg, MSGBOX_SIGN
	end

Route102_EventScript_Boy::
	msgbox Route102_Text_CatchWholeBunchOfPokemon, MSGBOX_NPC
	end

Route102_EventScript_Calvin::
	trainerbattle_single TRAINER_CALVIN_1, Route102_Text_CalvinIntro, Route102_Text_CalvinDefeated, Route102_EventScript_CalvinRegisterMatchCallAfterBattle
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route102_EventScript_CalvinRematch
	setvar VAR_0x8004, TRAINER_CALVIN_1
	specialvar VAR_RESULT, IsTrainerRegistered
	goto_if_eq VAR_RESULT, FALSE, Route102_EventScript_CalvinTryRegister
	msgbox Route102_Text_CalvinPostBattle, MSGBOX_DEFAULT
	release
	end

Route102_EventScript_CalvinRegisterMatchCallAfterBattle::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	goto_if_set FLAG_HAS_MATCH_CALL, Route102_EventScript_CalvinRegisterMatchCall
	release
	end

Route102_EventScript_CalvinRegisterMatchCall::
	msgbox Route102_Text_CalvinRegisterShort, MSGBOX_DEFAULT
	register_matchcall TRAINER_CALVIN_1
	release
	end

Route102_EventScript_CalvinTryRegister::
	goto_if_set FLAG_HAS_MATCH_CALL, Route102_EventScript_CalvinRegister
	msgbox Route102_Text_CalvinPostBattle, MSGBOX_DEFAULT
	release
	end

Route102_EventScript_CalvinRegister::
	msgbox Route102_Text_CalvinRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CALVIN_1
	release
	end

Route102_EventScript_CalvinRematch::
	trainerbattle_rematch TRAINER_CALVIN_1, Route102_Text_CalvinRematchIntro, Route102_Text_CalvinRematchDefeated
	msgbox Route102_Text_CalvinRematchPostBattle, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Rick::
	trainerbattle_single TRAINER_RICK, Route102_Text_RickIntro, Route102_Text_RickDefeated
	msgbox Route102_Text_RickPostBattle, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Tiana::
	trainerbattle_single TRAINER_TIANA, Route102_Text_TianaIntro, Route102_Text_TianaDefeated
	msgbox Route102_Text_TianaPostBattle, MSGBOX_AUTOCLOSE
	end

Route102_EventScript_Allen::
	trainerbattle_single TRAINER_ALLEN, Route102_Text_AllenIntro, Route102_Text_AllenDefeated
	msgbox Route102_Text_AllenPostBattle, MSGBOX_AUTOCLOSE
	end

Route102_Text_WatchMeCatchPokemon:
	.string "WALLY: {PLAYER}…\n"
	.string "POKéMON, gotta catch 'em all,\l"
	.string "don't they?\p"
	.string "See I can if what I try to maybe catch\n"
	.string "Maybe can huhuh\p"
	.string "…Whoa, appear wild!$"

Route102_Text_WallyIDidIt:
	.string "WALLY: My it is now really my\n"
	.string "Is my!, POKéMON now is!$"

Route102_Text_LetsGoBack:
	.string "WALLY: {PLAYER}, thank.\n"
	.string "GYM Go! Go back I want now yes maybe!$"

Route102_Text_ImNotVeryTall:
	.string "I'm…not very tall, so I sink right\n"
	.string "into tall grass.\p"
	.string "The grass goes up and…\n"
	.string "SMOKE WEED EVERYDAY\p"

Route102_Text_CatchWholeBunchOfPokemon:
	.string "I'm going to catch a whole bunch of\n"
	.string "diseases!$"

Route102_Text_RouteSignOldale:
	.string "ROUTE 102\n"
	.string "{RIGHT_ARROW} OLDALE TOWN\p"
	.string "OLDALE: now with 30% more OLD.$"

Route102_Text_RouteSignPetalburg:
	.string "ROUTE 102\n"
	.string "{LEFT_ARROW} PETALBURG CITY\p"
	.string "Home of a GYM LEADER who hasn't left\n"
	.string "his couch.$"

Route102_EventScript_RellorBirch::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_RELLOR, Route102_EventScript_RellorBirchPostItem
	
	msgbox Route102_Text_RellorBirchIntro, MSGBOX_DEFAULT
	
	getpartysize
	goto_if_eq VAR_RESULT, PARTY_SIZE, Route102_EventScript_NoRoomForRellor
	
	givemon SPECIES_RELLOR, 7, ITEM_HARD_STONE
	
	playfanfare MUS_OBTAIN_ITEM
	message Route102_Text_PlayerReceivedRellor
	waitmessage
	waitfanfare
	
Route102_EventScript_FinishRellorGift::
	setflag FLAG_RECEIVED_RELLOR
	msgbox Route102_Text_RellorBirchPostItem, MSGBOX_DEFAULT
	release
	end

Route102_EventScript_RellorBirchPostItem::
	msgbox Route102_Text_RellorBirchPostItem, MSGBOX_DEFAULT
	release
	end

Route102_EventScript_NoRoomForRellor::
	msgbox Route102_Text_NoRoomForRellor, MSGBOX_DEFAULT
	release
	end

Route102_Text_RellorBirchIntro:
	.string "PROF. BIRCH: {PLAYER}{KUN}!\n"
	.string "Don't mind me.\p"
	.string "I'm just documenting the structural\n"
	.string "integrity of this POOCHYENA turd.\p"
	.string "Fascinating… the fibers suggest a\n"
	.string "diet of strictly RATTATA.\p"
	.string "Maybe that's why we haven't seen\n"
	.string "those in HOENN in a while.\p"
	.string "Anyway, I found this little guy\n"
	.string "rolling a massive dump earlier.\p"
	.string "Might have been my own, actually.\n"
	.string "Take it, it's a personal gift!$"

Route102_Text_PlayerReceivedRellor:
	.string "{PLAYER} reluctantly received\n"
	.string "the RELLOR!$"

Route102_Text_RellorBirchPostItem:
	.string "PROF. BIRCH: Don't look at me like\n"
	.string "that. It's all in the name of research.\p"
	.string "Now go away, I think I see a\n"
	.string "fresh one over there!$"

Route102_Text_NoRoomForRellor:
	.string "PROF. BIRCH: Your pockets are full of\n"
	.string "balls, but your party is full of junk.\l"
	.string "Make some room!$"
	