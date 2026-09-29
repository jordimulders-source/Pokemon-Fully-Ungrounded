MossdeepCity_GameCorner_1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, MossdeepCity_GameCorner_1F_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, MossdeepCity_GameCorner_1F_OnWarp
	map_script MAP_SCRIPT_ON_LOAD, CableClub_OnLoad
	.byte 0

MossdeepCity_GameCorner_1F_OnWarp:
	map_script_2 VAR_CABLE_CLUB_STATE, USING_MINIGAME, CableClub_EventScript_CheckTurnAttendant
	.2byte 0

MossdeepCity_GameCorner_1F_OnFrame:
	map_script_2 VAR_CABLE_CLUB_STATE, USING_MINIGAME, CableClub_EventScript_ExitMinigameRoom
	.2byte 0

@ Script is redundant, the label in the goto also does lock and faceplayer
MossdeepCity_GameCorner_1F_EventScript_InfoMan::
	lock
	faceplayer
	goto MossdeepCity_GameCorner_1F_EventScript_InfoMan2
	release
	end

@ Script is redundant, the label in the goto also does lock and faceplayer
MossdeepCity_GameCorner_1F_EventScript_OldMan::
	lock
	faceplayer
	goto MossdeepCity_GameCorner_1F_EventScript_OldMan2
	release
	end


@ Everything below is leftover from RS
@ The house that was here in RS was moved to Sootopolis and replaced by the Game Corner
@ The text below is unused and duplicated in its replacement in Sootopolis City
@ And the BG Door event was moved inaccessibly into a wall

RS_MysteryEventsHouse_EventScript_Door::
	msgbox RS_MysteryEventsHouse_Text_DoorIsLocked, MSGBOX_SIGN
	end

RS_MysteryEventsHouse_Text_OldManGreeting:
	.string "When I was young, I traveled as a\n"
	.string "TRAINER.\p"
	.string "Now I'm an old buzzard. I just watch\n"
	.string "young TRAINERS battle.$"

RS_MysteryEventsHouse_Text_DoorIsLocked:
	.string "The door is locked.$"

RS_MysteryEventsHouse_Text_ChallengeVisitingTrainer:
	.string "A TRAINER named {STR_VAR_1} is visiting.\p"
	.string "Challenge {STR_VAR_1}?$"

RS_MysteryEventsHouse_Text_YouWontBattle:
	.string "You won't battle? Disappointing.\p"
	.string "I'll just watch the wall, then.$"

RS_MysteryEventsHouse_Text_KeepItToA3On3:
	.string "Good, good!\p"
	.string "My house isn't sturdy. Keep it to\n"
	.string "3-on-3.\p"
	.string "The last 6-on-6 took out a wall.$"

RS_MysteryEventsHouse_Text_SaveYourProgress:
	.string "Before you battle, save your progress.$"

RS_MysteryEventsHouse_Text_HopeToSeeAGoodMatch:
	.string "I hope for a good match!$"

RS_MysteryEventsHouse_Text_BattleTie:
	.string "A draw!\p"
	.string "Neither side gave an inch. Brilliant!$"

RS_MysteryEventsHouse_Text_BattleWon:
	.string "Superb!\p"
	.string "Like seeing myself as a young man! With\n"
	.string "more hair!$"

RS_MysteryEventsHouse_Text_BattleLost:
	.string "Too bad!\p"
	.string "Good match, though. Win next time.$"
