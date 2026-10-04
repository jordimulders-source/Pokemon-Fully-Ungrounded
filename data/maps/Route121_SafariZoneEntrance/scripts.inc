Route121_SafariZoneEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route121_SafariZoneEntrance_OnFrame
	.byte 0

Route121_SafariZoneEntrance_OnFrame:
	map_script_2 VAR_SAFARI_ZONE_STATE, 1, Route121_SafariZoneEntrance_EventScript_ExitSafariZone
	map_script_2 VAR_ROCKET_QUEST, 1, Route121_SafariZoneEntrance_EventScript_RocketKeysStolen
	map_script_2 VAR_ROCKET_QUEST, 3, Route121_SafariZoneEntrance_EventScript_RocketKeysReturned
	.2byte 0

@ Project Grounded: Rocket-sidequest. De medewerker bij de ingang vertelt wat de dief meenam (VAR_ROCKET_QUEST 1 -> 2,
@ de holle boom in Fortree Jungle gaat open) en bedankt je als je de ZONE KEYS terugbrengt (3 -> 4).
Route121_SafariZoneEntrance_EventScript_RocketKeysStolen::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Route121_SafariZoneEntrance_Text_RocketKeysStolen, MSGBOX_DEFAULT
	closemessage
	setvar VAR_ROCKET_QUEST, 2
	releaseall
	end

Route121_SafariZoneEntrance_EventScript_RocketKeysReturned::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Route121_SafariZoneEntrance_Text_RocketKeysReturned, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message Route121_SafariZoneEntrance_Text_RocketZonesOpen
	waitfanfare
	msgbox Route121_SafariZoneEntrance_Text_RocketFreeRound, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SAFARI_ZONES_OPEN
	setflag FLAG_ROCKET_FREE_SAFARI
	setflag FLAG_HIDE_ROCKET_HIDEOUT_GRUNTS
	setvar VAR_ROCKET_QUEST, 4
	releaseall
	end

Route121_SafariZoneEntrance_EventScript_ExitSafariZone::
	lockall
	applymovement LOCALID_PLAYER, Route121_SafariZoneEntrance_Movement_ExitSafariZone
	waitmovement 0
	setvar VAR_SAFARI_ZONE_STATE, 0
	releaseall
	end

Route121_SafariZoneEntrance_Movement_ExitSafariZone:
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Route121_SafariZoneEntrance_EventScript_WelcomeAttendant::
	msgbox Route121_SafariZoneEntrance_Text_WelcomeToSafariZone, MSGBOX_NPC
	end

Route121_SafariZoneEntrance_EventScript_InfoAttendant::
	lock
	faceplayer
	msgbox Route121_SafariZoneEntrance_Text_WelcomeFirstTime, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route121_SafariZoneEntrance_EventScript_FirstTimeInfo
	msgbox Route121_SafariZoneEntrance_Text_ComeInAndEnjoy, MSGBOX_DEFAULT
	release
	end

Route121_SafariZoneEntrance_EventScript_FirstTimeInfo::
	msgbox Route121_SafariZoneEntrance_Text_FirstTimeInfo, MSGBOX_DEFAULT
	release
	end

Route121_SafariZoneEntrance_EventScript_EntranceCounterTrigger::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	showmoneybox 0, 0
	msgbox Route121_SafariZoneEntrance_Text_WouldYouLikeToPlay, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route121_SafariZoneEntrance_EventScript_TryEnterSafariZone
	msgbox Route121_SafariZoneEntrance_Text_PlayAnotherTime, MSGBOX_DEFAULT
	goto Route121_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

Route121_SafariZoneEntrance_EventScript_TryEnterSafariZone::
	checkitem ITEM_POKEBLOCK_CASE
	goto_if_eq VAR_RESULT, 0, Route121_SafariZoneEntrance_EventScript_NoPokeblockCase
	call Route121_SafariZoneEntrance_EventScript_CheckHasRoomForPokemon
	goto_if_set FLAG_ROCKET_FREE_SAFARI, Route121_SafariZoneEntrance_EventScript_FreeRound
	checkmoney 500
	goto_if_eq VAR_RESULT, 0, Route121_SafariZoneEntrance_EventScript_NotEnoughMoney
	playse SE_SHOP
	msgbox Route121_SafariZoneEntrance_Text_ThatWillBe500Please, MSGBOX_DEFAULT
	removemoney 500
	updatemoneybox
Route121_SafariZoneEntrance_EventScript_GiveSafariBalls::
	msgbox Route121_SafariZoneEntrance_Text_HereAreYourSafariBalls, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message Route121_SafariZoneEntrance_Text_Received30SafariBalls
	waitfanfare
	msgbox Route121_SafariZoneEntrance_Text_PleaseEnjoyYourself, MSGBOX_DEFAULT
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, Route121_SafariZoneEntrance_Movement_EnterSafariZone
	waitmovement 0
	special EnterSafariMode
	setvar VAR_SAFARI_ZONE_STATE, 2
	clearflag FLAG_GOOD_LUCK_SAFARI_ZONE
	warp MAP_SAFARI_ZONE_SOUTH, 32, 33
	waitstate
	end

@ Project Grounded: gratis ronde als dank voor de teruggebrachte ZONE KEYS (eenmalig)
Route121_SafariZoneEntrance_EventScript_FreeRound::
	msgbox Route121_SafariZoneEntrance_Text_RocketFreeRoundCounter, MSGBOX_DEFAULT
	clearflag FLAG_ROCKET_FREE_SAFARI
	goto Route121_SafariZoneEntrance_EventScript_GiveSafariBalls

Route121_SafariZoneEntrance_EventScript_CheckHasRoomForPokemon::
	getpartysize
	goto_if_ne VAR_RESULT, PARTY_SIZE, Route121_SafariZoneEntrance_EventScript_HasRoomForPokemon
	specialvar VAR_RESULT, ScriptCheckFreePokemonStorageSpace
	goto_if_eq VAR_RESULT, 1, Route121_SafariZoneEntrance_EventScript_HasRoomForPokemon
	msgbox Route121_SafariZoneEntrance_Text_PCIsFull, MSGBOX_DEFAULT
	goto Route121_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

Route121_SafariZoneEntrance_EventScript_HasRoomForPokemon::
	return

Route121_SafariZoneEntrance_EventScript_NoPokeblockCase::
	msgbox Route121_SafariZoneEntrance_Text_YouNeedPokeblockCase, MSGBOX_DEFAULT
	goto Route121_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

Route121_SafariZoneEntrance_EventScript_NotEnoughMoney::
	msgbox Route121_SafariZoneEntrance_Text_NotEnoughMoney, MSGBOX_DEFAULT
	goto Route121_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter
	end

Route121_SafariZoneEntrance_EventScript_MovePlayerBackFromCounter::
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, Route121_SafariZoneEntrance_Movement_BackAwayFromCounter
	waitmovement 0
	releaseall
	end

Route121_SafariZoneEntrance_Movement_BackAwayFromCounter:
	walk_right
	step_end

Route121_SafariZoneEntrance_Movement_EnterSafariZone:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	delay_16
	step_end

Route121_SafariZoneEntrance_EventScript_TrainerTipSign::
	msgbox Route121_SafariZoneEntrance_Text_TrainerTip, MSGBOX_SIGN
	end

@ Project Grounded: Rocket-sidequest (placeholders)
Route121_SafariZoneEntrance_Text_RocketKeysStolen:
	.string "Oh no, oh no. {PLAYER}, did a man\n"
	.string "in a black onesie just flatten you?\p"
	.string "He stole the ZONE KEYS! The keys\n"
	.string "to our brand-new Safari Zones!\p"
	.string "Until we get them back, the new\n"
	.string "zones stay locked. Corporate calls\l"
	.string "it “a learning experience.”\p"
	.string "He yelled something about a condo\n"
	.string "inside a tree. In a jungle.\p"
	.string "There's only one jungle around\n"
	.string "here. Under FORTREE CITY.\p"
	.string "Burglars these days have zero\n"
	.string "operational security.$"

Route121_SafariZoneEntrance_Text_RocketKeysReturned:
	.string "{PLAYER}! The ZONE KEYS! And they're\n"
	.string "only slightly sticky!\p"
	.string "Our insurance didn't cover\n"
	.string "“theft by a man in a onesie.”\l"
	.string "You saved us a fortune.$"

Route121_SafariZoneEntrance_Text_RocketZonesOpen:
	.string "The new Safari Zones are open!$"

Route121_SafariZoneEntrance_Text_RocketFreeRound:
	.string "As thanks, your next Safari round\n"
	.string "is on the house. Go test the new\l"
	.string "zones before the paying customers\l"
	.string "find the bugs. And the Bug types.$"

Route121_SafariZoneEntrance_Text_RocketFreeRoundCounter:
	.string "Oh, it's our hero! This round is\n"
	.string "free, as promised. Don't tell\l"
	.string "corporate. They'll invoice you.$"
