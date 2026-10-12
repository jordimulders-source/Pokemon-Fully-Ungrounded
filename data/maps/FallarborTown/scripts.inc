FallarborTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FallarborTown_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, FallarborTown_OnResume
	.byte 0

FallarborTown_OnTransition:
	setflag FLAG_VISITED_FALLARBOR_TOWN
	setflag FLAG_HIDE_FALLARBOR_JIRACHI
	setvar VAR_CONTEST_HALL_STATE, 0
	clearflag FLAG_CONTEST_SKETCH_CREATED
	end

FallarborTown_EventScript_ExpertM::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, FallarborTown_EventScript_ExpertMNormal
	msgbox FallarborTown_Text_ShadyCharactersCozmosHome, MSGBOX_DEFAULT
	release
	end

FallarborTown_EventScript_ExpertMNormal::
	goto_if_set FLAG_SYS_GAME_CLEAR, FallarborTown_EventScript_ExpertMWishHint
	msgbox FallarborTown_Text_RegionKnownForMeteors, MSGBOX_DEFAULT
	release
	end

FallarborTown_EventScript_Girl::
	msgbox FallarborTown_Text_MyPreciousAzurill, MSGBOX_NPC
	end

FallarborTown_EventScript_Gentleman::
	msgbox FallarborTown_Text_HaveYouChallengedFlannery, MSGBOX_NPC
	end

FallarborTown_EventScript_Azurill::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_AZURILL, CRY_MODE_NORMAL
	msgbox FallarborTown_Text_Azurill, MSGBOX_DEFAULT
	waitmoncry
	release
	end

FallarborTown_EventScript_BattleTentSign::
	msgbox FallarborTown_Text_BattleTentSign, MSGBOX_SIGN
	end

FallarborTown_EventScript_TownSign::
	msgbox FallarborTown_Text_TownSign, MSGBOX_SIGN
	end

FallarborTown_EventScript_MoveTutorSign::
	msgbox FallarborTown_Text_MoveTutorSign, MSGBOX_SIGN
	end

FallarborTown_Text_ShadyCharactersCozmosHome:
	.string "Something's happening, and I don't like\n"
	.string "it!\p"
	.string "Shady types in red keep going in and\n"
	.string "out of PROF. COZMO's house.\p"
	.string "They smell like chili.$"

FallarborTown_Text_RegionKnownForMeteors:
	.string "This region has been known for meteors\n"
	.string "forever.\p"
	.string "METEOR FALLS was made by one.\p"
	.string "That's why we all wear helmets. Well, I\n"
	.string "do.$"

FallarborTown_Text_MyPreciousAzurill:
	.string "Look! My precious AZURILL!\p"
	.string "Slick, smooth and plushy!\p"
	.string "It's grey now. The ash, you know.$"

FallarborTown_Text_Azurill:
	.string "AZURILL: Rooreelooo.$"

FallarborTown_Text_HaveYouChallengedFlannery:
	.string "Have you challenged FLANNERY yet?\p"
	.string "Her grandfather was in the ELITE FOUR.\p"
	.string "She went off-grid. He's not thrilled.$"

FallarborTown_Text_BattleTentSign:
	.string "BATTLE TENT FALLARBOR SITE\n"
	.string "“May the Greatest Teams Gather!”$"

FallarborTown_Text_TownSign:
	.string "FALLARBOR TOWN\n"
	.string "“A farm community with small gardens.\l"
	.string "And ash. So much ash.”$"

FallarborTown_Text_MoveTutorSign:
	.string "MOVE TUTOR'S HOUSE\n"
	.string "“New moves taught to POKéMON. No\l"
	.string "refunds.”$"


@ Project Grounded: Jirachi-wensevent. Post-game, alleen 's nachts: in de oude meteorietkrater linksonder (2,15) gaan
@ staan en een wens doen. Jirachi daalt uit de lucht neer (lv 70). VAR_NIGHT_LEGEND_STATE = 1 zet de trigger aan.
FallarborTown_OnResume:
	setvar VAR_NIGHT_LEGEND_STATE, 0
	goto_if_unset FLAG_SYS_GAME_CLEAR, FallarborTown_EventScript_NoWishTonight
	goto_if_set FLAG_DEFEATED_JIRACHI, FallarborTown_EventScript_NoWishTonight
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, FALSE, FallarborTown_EventScript_NoWishTonight
	setvar VAR_NIGHT_LEGEND_STATE, 1
FallarborTown_EventScript_NoWishTonight:
	end

FallarborTown_EventScript_ExpertMWishHint::
	msgbox FallarborTown_Text_WishingCraterHint, MSGBOX_DEFAULT
	release
	end

FallarborTown_EventScript_WishingCrater::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
	waitmovement 0
	msgbox FallarborTown_Text_MakeAWish, MSGBOX_DEFAULT
	closemessage
	playse SE_M_MOONLIGHT
	clearflag FLAG_HIDE_FALLARBOR_JIRACHI
	addobject LOCALID_FALLARBOR_JIRACHI
	applymovement LOCALID_FALLARBOR_JIRACHI, FallarborTown_Movement_JirachiDescends
	waitmovement 0
	playse SE_SHINY
	waitse
	goto FallarborTown_EventScript_JirachiBattle
	end

FallarborTown_EventScript_Jirachi::
	lockall
	faceplayer
	goto FallarborTown_EventScript_JirachiBattle
	end

FallarborTown_EventScript_JirachiBattle::
	msgbox FallarborTown_Text_JirachiAppears, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_JIRACHI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_JIRACHI, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FallarborTown_EventScript_JirachiFliesOff
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FallarborTown_EventScript_JirachiFliesOff
	setflag FLAG_DEFEATED_JIRACHI
	setvar VAR_NIGHT_LEGEND_STATE, 0
	removeobject LOCALID_FALLARBOR_JIRACHI
	setflag FLAG_HIDE_FALLARBOR_JIRACHI
	releaseall
	end

FallarborTown_EventScript_JirachiFliesOff::
	applymovement LOCALID_FALLARBOR_JIRACHI, FallarborTown_Movement_JirachiAscends
	waitmovement 0
	removeobject LOCALID_FALLARBOR_JIRACHI
	setflag FLAG_HIDE_FALLARBOR_JIRACHI
	msgbox FallarborTown_Text_JirachiFlewOff, MSGBOX_DEFAULT
	releaseall
	end

FallarborTown_Movement_JirachiDescends:
	walk_slow_down
	walk_slow_down
	walk_slow_down
	step_end

FallarborTown_Movement_JirachiAscends:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

FallarborTown_Text_WishingCraterHint:
	.string "See that old crater by COZMO's house? A\n"
	.string "meteorite made it. COZMO tried to sell it\l"
	.string "online.\p"
	.string "They say if you stand in it at night and\n"
	.string "make a wish, something answers.\p"
	.string "I wished for hair. Something answered.\n"
	.string "It laughed.$"

FallarborTown_Text_MakeAWish:
	.string "The stars are out above the old\n"
	.string "meteorite crater.\p"
	.string "{PLAYER} closes their eyes and wishes\n"
	.string "for a POKéMON game with a real\l"
	.string "difficulty setting.\p"
	.string "… … …\p"
	.string "Something small and shiny is falling out\n"
	.string "of the sky. Straight at you.$"

FallarborTown_Text_JirachiAppears:
	.string "Jiraaa!\p"
	.string "It has three wish tags on its head. One\n"
	.string "says “DIFFICULTY SETTING”.\p"
	.string "It cracks its tiny knuckles. Wish\n"
	.string "granted.$"

FallarborTown_Text_JirachiFlewOff:
	.string "JIRACHI drifted back up into the night\n"
	.string "sky, taking your wish with it.\p"
	.string "Wishes don't come true if you run away.\n"
	.string "It's in the fine print.$"
