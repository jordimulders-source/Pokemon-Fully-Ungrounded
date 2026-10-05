SootopolisCity_Gym_1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SootopolisCity_Gym_1F_OnFrame
	map_script MAP_SCRIPT_ON_RESUME, SootopolisCity_Gym_1F_OnResume
	map_script MAP_SCRIPT_ON_LOAD, SootopolisCity_Gym_1F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SootopolisCity_Gym_1F_OnTransition
	.byte 0

SootopolisCity_Gym_1F_OnTransition:
	setvar VAR_ICE_STEP_COUNT, 1
	end

SootopolisCity_Gym_1F_OnResume:
	setstepcallback STEP_CB_SOOTOPOLIS_ICE
	end

SootopolisCity_Gym_1F_OnLoad:
	call SootopolisCity_Gym_1F_EventScript_CheckSetStairMetatiles
	special SetSootopolisGymCrackedIceMetatiles
	end

SootopolisCity_Gym_1F_EventScript_CheckSetStairMetatiles::
	goto_if_lt VAR_ICE_STEP_COUNT, 8, SootopolisCity_Gym_1F_EventScript_StopCheckingStairs  @ All stairs ice
	goto_if_lt VAR_ICE_STEP_COUNT, 28, SootopolisCity_Gym_1F_EventScript_OpenFirstStairs
	goto_if_lt VAR_ICE_STEP_COUNT, 67, SootopolisCity_Gym_1F_EventScript_OpenFirstAndSecondStairs
	setmetatile 8, 4, METATILE_SootopolisGym_Stairs, FALSE
	setmetatile 8, 5, METATILE_SootopolisGym_Stairs, FALSE
SootopolisCity_Gym_1F_EventScript_OpenFirstAndSecondStairs::
	setmetatile 8, 10, METATILE_SootopolisGym_Stairs, FALSE
	setmetatile 8, 11, METATILE_SootopolisGym_Stairs, FALSE
SootopolisCity_Gym_1F_EventScript_OpenFirstStairs::
	setmetatile 8, 15, METATILE_SootopolisGym_Stairs, FALSE
	setmetatile 8, 16, METATILE_SootopolisGym_Stairs, FALSE
SootopolisCity_Gym_1F_EventScript_StopCheckingStairs::
	return

SootopolisCity_Gym_1F_OnFrame:
	map_script_2 VAR_ICE_STEP_COUNT, 8, SootopolisCity_Gym_1F_EventScript_UnlockFirstStairs
	map_script_2 VAR_ICE_STEP_COUNT, 28, SootopolisCity_Gym_1F_EventScript_UnlockSecondStairs
	map_script_2 VAR_ICE_STEP_COUNT, 67, SootopolisCity_Gym_1F_EventScript_UnlockThirdStairs
	map_script_2 VAR_ICE_STEP_COUNT, 0, SootopolisCity_Gym_1F_EventScript_FallThroughIce
	.2byte 0

SootopolisCity_Gym_1F_EventScript_UnlockFirstStairs::
	addvar VAR_ICE_STEP_COUNT, 1
	delay 40
	playse SE_ICE_STAIRS
	call SootopolisCity_Gym_1F_EventScript_CheckSetStairMetatiles
	special DrawWholeMapView
	end

SootopolisCity_Gym_1F_EventScript_UnlockSecondStairs::
	addvar VAR_ICE_STEP_COUNT, 1
	delay 40
	playse SE_ICE_STAIRS
	call SootopolisCity_Gym_1F_EventScript_CheckSetStairMetatiles
	special DrawWholeMapView
	end

SootopolisCity_Gym_1F_EventScript_UnlockThirdStairs::
	addvar VAR_ICE_STEP_COUNT, 1
	delay 40
	playse SE_ICE_STAIRS
	call SootopolisCity_Gym_1F_EventScript_CheckSetStairMetatiles
	special DrawWholeMapView
	end

SootopolisCity_Gym_1F_EventScript_FallThroughIce::
	lockall
	delay 20
	applymovement LOCALID_PLAYER, SootopolisCity_Gym_1F_Movement_FallThroughIce
	waitmovement 0
	playse SE_FALL
	delay 60
	warphole MAP_SOOTOPOLIS_CITY_GYM_B1F
	waitstate
	end

SootopolisCity_Gym_1F_Movement_FallThroughIce:
	set_invisible
	step_end

SootopolisCity_Gym_1F_EventScript_Wallace::
	trainerbattle_single TRAINER_WALLACE_1, SootopolisCity_Gym_1F_Text_JuanIntro, SootopolisCity_Gym_1F_Text_JuanDefeat, SootopolisCity_Gym_1F_EventScript_WallaceDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, SootopolisCity_Gym_1F_EventScript_WallaceRematch
	goto_if_unset FLAG_RECEIVED_TM_WATER_PULSE, SootopolisCity_Gym_1F_EventScript_GiveWaterPulse2
	goto_if_unset FLAG_BADGE06_GET, SootopolisCity_Gym_1F_EventScript_GoGetFortreeBadge
	msgbox SootopolisCity_Gym_1F_Text_JuanPostBattle, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_WallaceDefeated::
	message SootopolisCity_Gym_1F_Text_ReceivedRainBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox SootopolisCity_Gym_1F_Text_ExplainRainBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_SOOTOPOLIS_GYM
	setflag FLAG_BADGE08_GET
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_RESIDENTS
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_STEVEN
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_WALLACE
	setvar VAR_SOOTOPOLIS_CITY_STATE, 6
	clearflag FLAG_HIDE_SOOTOPOLIS_CITY_MAN_1
	setvar VAR_0x8008, 8
	call Common_EventScript_SetGymTrainers
	call SootopolisCity_Gym_1F_EventScript_GiveWaterPulse
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox SootopolisCity_Gym_1F_Text_RegisteredJuan, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_WALLACE_MATCH_CALL
	release
	end

SootopolisCity_Gym_1F_EventScript_GiveWaterPulse::
	giveitem ITEM_TM_VINTAGE_SPILL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox SootopolisCity_Gym_1F_Text_ExplainWaterPulse, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_WATER_PULSE
	return

SootopolisCity_Gym_1F_EventScript_GiveWaterPulse2::
	giveitem ITEM_TM_VINTAGE_SPILL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox SootopolisCity_Gym_1F_Text_ExplainWaterPulse, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_WATER_PULSE
	release
	end

SootopolisCity_Gym_1F_EventScript_GoGetFortreeBadge::
	msgbox SootopolisCity_Gym_1F_Text_GoGetFortreeBadge, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_WallaceRematch::
	trainerbattle_rematch_double TRAINER_WALLACE_1, SootopolisCity_Gym_1F_Text_JuanPreRematch, SootopolisCity_Gym_1F_Text_JuanRematchDefeat, SootopolisCity_Gym_1F_Text_JuanRematchNeedTwoMons
	msgbox SootopolisCity_Gym_1F_Text_JuanPostRematch, MSGBOX_AUTOCLOSE
	end

SootopolisCity_Gym_1F_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_SOOTOPOLIS_GYM, SootopolisCity_Gym_1F_EventScript_GymGuidePostVictory
	msgbox SootopolisCity_Gym_1F_Text_GymGuideAdvice, MSGBOX_DEFAULT
	msgbox SootopolisCity_Gym_1F_Text_GymGuideAceLevel, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_GymGuidePostVictory::
	msgbox SootopolisCity_Gym_1F_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	msgbox SootopolisCity_Gym_1F_Text_GymGuideNextAce, MSGBOX_DEFAULT
	release
	end

SootopolisCity_Gym_1F_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE08_GET, SootopolisCity_Gym_1F_EventScript_GymStatueCertified
	goto SootopolisCity_Gym_1F_EventScript_GymStatue
	end

SootopolisCity_Gym_1F_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE08_GET, SootopolisCity_Gym_1F_EventScript_GymStatueCertified
	goto SootopolisCity_Gym_1F_EventScript_GymStatue
	end

SootopolisCity_Gym_1F_EventScript_GymStatueCertified::
	msgbox SootopolisCity_Gym_1F_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_EventScript_GymStatue::
	msgbox SootopolisCity_Gym_1F_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

SootopolisCity_Gym_1F_Text_GymGuideAdvice:
	.string "Yo! How's it going, CHAMPION-\n"
	.string "bound {PLAYER}?\p"
	.string "Welcome to the Crater Pub. Watch your\n"
	.string "step, the floor is soaked in cheap\l"
	.string "ale and God knows what else.\p"
	.string "The LEADER, WALLACE, is a master of\n"
	.string "the 'Liquid Arts'. And I'm not just\l"
	.string "talking about WATER POKéMON.\p"
	.string "He is terrifying. I once saw him\n"
	.string "one-shot three MAX POTIONS in a row\l"
	.string "without even blinking.\p"
	.string "If you can make it across this slippery\n"
	.string "mess without joining the drunks in\l"
	.string "the basement, you might have a shot.\p"
	.string "Good luck. You're going to need it,\n"
	.string "and probably some aspirin later!$"

SootopolisCity_Gym_1F_Text_GymGuidePostVictory:
	.string "Yow! You actually beat WALLACE?\n"
	.string "The man who outdrank the entire\l"
	.string "Sootopolis harbor crew?\p"
	.string "Check out your TRAINER CARD.\p"
	.string "If you've gathered all the BADGES,\n"
	.string "you're ready for the LEAGUE.\l"
	.string "Just... maybe take a shower first.\l"
	.string "You smell like a brewery, kid!$"

SootopolisCity_Gym_1F_Text_JuanIntro:
	.string "Allow me to formally introduce myself.\n"
	.string "I am WALLACE. The proprietor and\l"
	.string "GYM LEADER of Sootopolis.\p"
	.string "There's something about you...\n"
	.string "A difference in your demeanor. Your\l"
	.string "spirit has a certain... bouquet.\p"
	.string "What happened inside the CAVE OF\n"
	.string "ORIGIN, and the vintage of the power\l"
	.string "you found there, I will likely learn\l"
	.string "through our upcoming battle.\p"
	.string "Now, show me. Show me the potency of\n"
	.string "the power you wield with your POKéMON.\p"
	.string "And I, in turn, shall present you with\n"
	.string "a performance of liquid illusions\l"
	.string "by me and my POKéMON!\p"
	.string "Santé!$"

SootopolisCity_Gym_1F_Text_JuanDefeat:
	.string "Bravo. A truly full-bodied victory.\p"
	.string "I realize now your authenticity and\n"
	.string "magnificence as a POKéMON TRAINER.\p"
	.string "I find much joy in having met a spirit\n"
	.string "as refined as yours. You have proven\l"
	.string "yourself worthy of the RAIN BADGE.\l"
	.string "Accept it.$"

SootopolisCity_Gym_1F_Text_ReceivedRainBadge:
	.string "{PLAYER} received the RAIN BADGE\n"
	.string "from WALLACE.$"

SootopolisCity_Gym_1F_Text_ExplainRainBadgeTakeThis:
	.string "The RAIN BADGE ensures your POKéMON\n"
	.string "obey you, even if they are completely\l"
	.string "plastered on Fermented Berries.\p"
	.string "It also allows the use of WATERFALL\n"
	.string "to scale walls of cascading gin.\p"
	.string "And, so that you never forget the\n"
	.string "vintage of this battle, take this...$"

SootopolisCity_Gym_1F_Text_ExplainWaterPulse:
	.string "That TECHNICAL MACHINE contains\n"
	.string "VINTAGE SPILL.\p"
	.string "Every splash confuses a little more.\n"
	.string "Think of it as a shot of 90 percent\l"
	.string "absinthe delivered to the face.\p"
	.string "... ... ... ... ... ...$"

SootopolisCity_Gym_1F_Text_RegisteredJuan:
	.string "Registered GYM LEADER WALLACE\n"
	.string "in the POKéNAV.$"

SootopolisCity_Gym_1F_Text_JuanPostBattle:
	.string "The TRAINERS who have survived the\n"
	.string "hangovers of HOENN should make\l"
	.string "way to the ultimate destination.\p"
	.string "The POKéMON LEAGUE.\p"
	.string "Travel to EVER GRANDE ISLAND.\n"
	.string "They have a decent wine list there,\l"
	.string "though nothing compared to mine.$"

SootopolisCity_Gym_1F_Text_GoGetFortreeBadge:
	.string "There remains but one BADGE to\n"
	.string "obtain in HOENN.\p"
	.string "It seems you skipped the craft beer\n"
	.string "festival in FORTREE. Go back and\l"
	.string "deal with WINONA first.$"

SootopolisCity_Gym_1F_Text_GymStatue:
	.string "SOOTOPOLIS CITY POKéMON GYM$"

SootopolisCity_Gym_1F_Text_GymStatueCertified:
	.string "SOOTOPOLIS CITY POKéMON GYM\p"
	.string "WALLACE'S CERTIFIED TRAINERS: {PLAYER}$"

SootopolisCity_Gym_1F_Text_JuanPreRematch:
	.string "WALLACE: Ah, my GYM had just returned\n"
	.string "to its usual state of calm\l"
	.string "intoxication…\p"
	.string "But our young typhoon has returned!\n"
	.string "Let me uncork something special. Santé!$"

SootopolisCity_Gym_1F_Text_JuanRematchDefeat:
	.string "Ahahaha, you've won again! I shall drown\n"
	.string "my sorrows. Responsibly. Mostly.$"

SootopolisCity_Gym_1F_Text_JuanPostRematch:
	.string "WALLACE: If I asked you to be my\n"
	.string "apprentice, you would refuse. If I\l"
	.string "offered you my finest bottle, you would\l"
	.string "refuse too.\p"
	.string "A sign of nobility! Or of being underage.$"

SootopolisCity_Gym_1F_Text_JuanRematchNeedTwoMons:
	.string "WALLACE: Ah, my GYM had just returned\n"
	.string "to its usual state of calm\l"
	.string "intoxication…\p"
	.string "But our young typhoon has returned!\n"
	.string "Let me uncork something special. Santé!\p"
	.string "Ah, no, no, no. One POKéMON? That's like\n"
	.string "serving wine without a glass. Return\l"
	.string "with at least two.$"

@ Project Grounded: aanwijzing van het level van de gym-ace (placeholder)
SootopolisCity_Gym_1F_Text_GymGuideAceLevel:
	.string "Insider info: the LEADER's ace\n"
	.string "is level 56.\p"
	.string "You didn't hear it from me.\n"
	.string "You heard it from me, but still.$"

SootopolisCity_Gym_1F_Text_GymGuideNextAce:
	.string "Next stop: the POKéMON LEAGUE.\n"
	.string "Their levels? No idea.\p"
	.string "Nobody ever comes back\n"
	.string "to tell me.$"
