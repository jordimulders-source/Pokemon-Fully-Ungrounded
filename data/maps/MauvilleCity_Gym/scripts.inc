MauvilleCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MauvilleCity_Gym_OnLoad
	.byte 0

MauvilleCity_Gym_OnLoad:
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_DeactivatePuzzle
	switch VAR_MAUVILLE_GYM_STATE
	case 0, MauvilleCity_Gym_EventScript_UpdateBarriers
	case 1, MauvilleCity_Gym_EventScript_Switch1Pressed
	case 2, MauvilleCity_Gym_EventScript_Switch2Pressed
	case 3, MauvilleCity_Gym_EventScript_Switch3Pressed
	case 4, MauvilleCity_Gym_EventScript_Switch4Pressed
	end

MauvilleCity_Gym_EventScript_UpdateBarriers::
	goto_if_set FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_SetAltBarriers
	end

MauvilleCity_Gym_EventScript_SetAltBarriers::
	setmetatile 3, 11, METATILE_MauvilleGym_RedBeamV1_On, TRUE
	setmetatile 3, 12, METATILE_MauvilleGym_RedBeamV2_On, TRUE
	setmetatile 3, 13, METATILE_MauvilleGym_PoleTop_On, TRUE
	setmetatile 4, 10, METATILE_MauvilleGym_RedBeamH1_On, FALSE
	setmetatile 5, 10, METATILE_MauvilleGym_RedBeamH2_On, FALSE
	setmetatile 4, 11, METATILE_MauvilleGym_RedBeamH3_On, TRUE
	setmetatile 5, 11, METATILE_MauvilleGym_RedBeamH4_On, TRUE
	setmetatile 7, 10, METATILE_MauvilleGym_RedBeamH1_On, FALSE
	setmetatile 8, 10, METATILE_MauvilleGym_RedBeamH2_On, FALSE
	setmetatile 7, 11, METATILE_MauvilleGym_RedBeamH3_On, TRUE
	setmetatile 8, 11, METATILE_MauvilleGym_RedBeamH4_On, TRUE
	setmetatile 4, 13, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 5, 13, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 4, 14, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 5, 14, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	setmetatile 1, 10, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 2, 10, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 1, 11, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 2, 11, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	setmetatile 6, 8, METATILE_MauvilleGym_PoleBottom_On, TRUE
	setmetatile 6, 9, METATILE_MauvilleGym_FloorTile, FALSE
	setmetatile 6, 10, METATILE_MauvilleGym_PoleTop_Off, FALSE
	setmetatile 4, 6, METATILE_MauvilleGym_GreenBeamH1_Off, FALSE
	setmetatile 5, 6, METATILE_MauvilleGym_GreenBeamH2_Off, FALSE
	setmetatile 4, 7, METATILE_MauvilleGym_GreenBeamH3_Off, FALSE
	setmetatile 5, 7, METATILE_MauvilleGym_GreenBeamH4_Off, FALSE
	end

MauvilleCity_Gym_EventScript_Switch1Pressed::
	setvar VAR_0x8004, 0
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch2Pressed::
	setvar VAR_0x8004, 1
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch3Pressed::
	setvar VAR_0x8004, 2
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_Switch4Pressed::
	setvar VAR_0x8004, 3
	special MauvilleGymPressSwitch
	goto MauvilleCity_Gym_EventScript_UpdateBarriers
	end

MauvilleCity_Gym_EventScript_DeactivatePuzzle::
	special MauvilleGymDeactivatePuzzle
	end

MauvilleCity_Gym_EventScript_Wattson::
	trainerbattle_single TRAINER_WATTSON_1, MauvilleCity_Gym_Text_WattsonIntro, MauvilleCity_Gym_Text_WattsonDefeat, MauvilleCity_Gym_EventScript_WattsonDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MauvilleCity_Gym_EventScript_WattsonRematch
	goto_if_unset FLAG_RECEIVED_TM_SHOCK_WAVE, MauvilleCity_Gym_EventScript_GiveShockWave2
	goto_if_eq VAR_NEW_MAUVILLE_STATE, 2, MauvilleCity_Gym_EventScript_CompletedNewMauville
	msgbox MauvilleCity_Gym_Text_WattsonPostBattle, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_WattsonDefeated::
	message MauvilleCity_Gym_Text_ReceivedDynamoBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox MauvilleCity_Gym_Text_ExplainDynamoBadgeTakeThis, MSGBOX_DEFAULT
	setvar VAR_SLATEPORT_OUTSIDE_MUSEUM_STATE, 3
	clearflag FLAG_HIDE_VERDANTURF_TOWN_SCOTT
	setflag FLAG_DEFEATED_MAUVILLE_GYM
	setflag FLAG_BADGE03_GET
	addvar VAR_PETALBURG_GYM_STATE, 1
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	setvar VAR_0x8008, 3
	call Common_EventScript_SetGymTrainers
	special MauvilleGymDeactivatePuzzle
	special DrawWholeMapView
	playse SE_UNLOCK
	call MauvilleCity_Gym_EventScript_GiveShockWave
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox MauvilleCity_Gym_Text_RegisteredWattson, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_WATTSON_MATCH_CALL
	release
	end

MauvilleCity_Gym_EventScript_GiveShockWave2::
	giveitem ITEM_TM_VOLT_SWITCH
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox MauvilleCity_Gym_Text_ExplainShockWave, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_SHOCK_WAVE
	release
	end

MauvilleCity_Gym_EventScript_GiveShockWave::
	giveitem ITEM_TM_VOLT_SWITCH
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox MauvilleCity_Gym_Text_ExplainShockWave, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_SHOCK_WAVE
	return

MauvilleCity_Gym_EventScript_CompletedNewMauville::
	msgbox MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_WattsonRematch::
	trainerbattle_rematch_double TRAINER_WATTSON_1, MauvilleCity_Gym_Text_WattsonPreRematch, MauvilleCity_Gym_Text_WattsonRematchDefeat, MauvilleCity_Gym_Text_WattsonRematchNeedTwoMons
	msgbox MauvilleCity_Gym_Text_WattsonPostRematch, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Switch1::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 1, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 1
	setvar VAR_0x8004, 0
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch2::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 2, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 2
	setvar VAR_0x8004, 1
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch3::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 3, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 3
	setvar VAR_0x8004, 2
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_Switch4::
	lockall
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_SwitchDoNothing
	goto_if_eq VAR_MAUVILLE_GYM_STATE, 4, MauvilleCity_Gym_EventScript_SwitchDoNothing
	setvar VAR_MAUVILLE_GYM_STATE, 4
	setvar VAR_0x8004, 3
	goto MauvilleCity_Gym_EventScript_PressFloorSwitch
	end

MauvilleCity_Gym_EventScript_PressFloorSwitch::
	special MauvilleGymSetDefaultBarriers
	special MauvilleGymPressSwitch
	special DrawWholeMapView
	playse SE_UNLOCK
	goto_if_set FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_ClearBarriersAltState
	goto_if_unset FLAG_MAUVILLE_GYM_BARRIERS_STATE, MauvilleCity_Gym_EventScript_SetBarriersAltState
	releaseall
	end

MauvilleCity_Gym_EventScript_SwitchDoNothing::
	releaseall
	end

MauvilleCity_Gym_EventScript_SetBarriersAltState::
	setflag FLAG_MAUVILLE_GYM_BARRIERS_STATE
	releaseall
	end

MauvilleCity_Gym_EventScript_ClearBarriersAltState::
	clearflag FLAG_MAUVILLE_GYM_BARRIERS_STATE
	releaseall
	end

MauvilleCity_Gym_EventScript_Kirk::
	trainerbattle_single TRAINER_KIRK, MauvilleCity_Gym_Text_KirkIntro, MauvilleCity_Gym_Text_KirkDefeat
	msgbox MauvilleCity_Gym_Text_KirkPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Shawn::
	trainerbattle_single TRAINER_SHAWN, MauvilleCity_Gym_Text_ShawnIntro, MauvilleCity_Gym_Text_ShawnDefeat
	msgbox MauvilleCity_Gym_Text_ShawnPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Ben::
	trainerbattle_single TRAINER_BEN, MauvilleCity_Gym_Text_BenIntro, MauvilleCity_Gym_Text_BenDefeat
	msgbox MauvilleCity_Gym_Text_BenPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Vivian::
	trainerbattle_single TRAINER_VIVIAN, MauvilleCity_Gym_Text_VivianIntro, MauvilleCity_Gym_Text_VivianDefeat
	msgbox MauvilleCity_Gym_Text_VivianPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_Angelo::
	trainerbattle_single TRAINER_ANGELO, MauvilleCity_Gym_Text_AngeloIntro, MauvilleCity_Gym_Text_AngeloDefeat
	msgbox MauvilleCity_Gym_Text_AngeloPostBattle, MSGBOX_AUTOCLOSE
	end

MauvilleCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_MAUVILLE_GYM, MauvilleCity_Gym_EventScript_GymGuidePostVictory
	msgbox MauvilleCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	msgbox MauvilleCity_Gym_Text_GymGuideAceLevel, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_GymGuidePostVictory::
	msgbox MauvilleCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	msgbox MauvilleCity_Gym_Text_GymGuideNextAce, MSGBOX_DEFAULT
	release
	end

MauvilleCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE03_GET, MauvilleCity_Gym_EventScript_GymStatueCertified
	goto MauvilleCity_Gym_EventScript_GymStatue
	end

MauvilleCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE03_GET, MauvilleCity_Gym_EventScript_GymStatueCertified
	goto MauvilleCity_Gym_EventScript_GymStatue
	end

MauvilleCity_Gym_EventScript_GymStatueCertified::
	msgbox MauvilleCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_Gym_EventScript_GymStatue::
	msgbox MauvilleCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

MauvilleCity_Gym_Text_GymGuideAdvice:
	.string "Hey, how's it going, CHAMPION-\n"
	.string "bound {PLAYER}?\p"
	.string "Look, I'll be honest... I don't know\n"
	.string "what's happening in here anymore.\p"
	.string "WATTSON started investing in crypto\n"
	.string "and now the whole GYM is just... kids\l"
	.string "doing dances for views and screaming\l"
	.string "about their 'Sigma' grindset.\p"
	.string "He uses ELECTRIC-type POKéMON. If you\n"
	.string "use WATER-types, they'll get zapped\l"
	.string "faster than a pump-and-dump scam!\p"
	.string "The switches open the doors, but some\n"
	.string "influencer tried to charge me 500\l"
	.string "POKéDOLLARS for the 'Alpha' route.\p"
	.string "Just... go in there, win, and please\n"
	.string "don't let them film a prank on you!$"

MauvilleCity_Gym_Text_GymGuidePostVictory:
	.string "Whoa, you actually won?! And you\n"
	.string "did it without a 'Glow Up' montage!\p"
	.string "You're electrifying! You've powered\n"
	.string "the door open and escaped the cringe!$"

MauvilleCity_Gym_Text_KirkIntro:
	.string "My electric soul, it'll shatter your\n"
	.string "dreams whole, whoa-yeahah!\p"
	.string "Buy my vinyl, kid! I'm one stream\n"
	.string "away from being able to afford\l"
	.string "a single LAVA COOKIE!$"

MauvilleCity_Gym_Text_KirkDefeat:
	.string "That was plugged in, amped up...\n"
	.string "and I just earned 0.0003 POKéDOLLARS!$"

MauvilleCity_Gym_Text_KirkPostBattle:
	.string "POKéMON and rock, it's all about heart!\n"
	.string "But you can't eat heart, man.\p"
	.string "I got a million streams last month\n"
	.string "and the platform sent me a sticker\l"
	.string "and a 'thanks' email.\p"
	.string "Meanwhile, the kid behind me just\n"
	.string "made a fortune selling a NFT of\l"
	.string "a pixelated VOLTORB. Unbelievable.$"

MauvilleCity_Gym_Text_ShawnIntro:
	.string "I trained under WATTSON, but my\n"
	.string "portfolio is my real master!\p"
	.string "You’re looking at a future trillionaire!\n"
	.string "I've got diamond hands, kid. You're\l"
	.string "about to get liquidated! HODL!$"

MauvilleCity_Gym_Text_ShawnDefeat:
	.string "No! My stop-loss didn't trigger!\n"
	.string "I'm getting rugpulled!$"

MauvilleCity_Gym_Text_ShawnPostBattle:
	.string "WATTSON has been around for a long\n"
	.string "time, but he’s still using fiat!\p"
	.string "He was battling before your daddy\n"
	.string "was born, but he doesn't even own\l"
	.string "a single Bored AIPOM NFT.\p"
	.string "Have fun staying poor, NPC!\n"
	.string "Fortune favors the brave!$"

MauvilleCity_Gym_Text_BenIntro:
	.string "This GYM's got puzzles! This is\n"
	.string "so skibidi! 6-7, 6-7, 6-7!\p"
	.string "TUNG TUNG TUNG SAHUR!\n"
	.string "TUNG TUNG TUNG SAHUR!\p"
	.string "Prepare to get mogged, NPC!$"

MauvilleCity_Gym_Text_BenDefeat:
	.string "Noo! My fanum tax! This is\n"
	.string "negative aura! It's over for me...$"

MauvilleCity_Gym_Text_BenPostBattle:
	.string "WATTSON says he likes setting up\n"
	.string "little traps with switches.\p"
	.string "Sticking out your gyatt for the\n"
	.string "rizzler... TUNG TUNG TUNG SAHUR!\l"
	.string "TUNG TUNG TUNG SAHUR!\p"
	.string "I need to find a subway surfers\n"
	.string "gameplay video to stay focused.\l"
	.string "6-7! 6-7!$"

MauvilleCity_Gym_Text_VivianIntro:
	.string "What is up, V-Squad?! Today we are\n"
	.string "battling this total NPC live!\p"
	.string "Can we get some 'W's in the chat?\n"
	.string "That IONO girl is so mid compared\l"
	.string "to my aesthetic! Don't forget to\l"
	.string "smash that like button!$"

MauvilleCity_Gym_Text_VivianDefeat:
	.string "Ugh, guys, I think they're stream-\n"
	.string "sniping me! This is so toxic!$"

MauvilleCity_Gym_Text_VivianPostBattle:
	.string "I've heard that MAUVILLE was founded\n"
	.string "by WATTSON. He's okay, but he has\l"
	.string "zero social media presence.\p"
	.string "I offered to manage his socials for\n"
	.string "a 90% cut, but he just laughed.\p"
	.string "Anyway, link in bio for my apology\n"
	.string "video! Use code 'CRINGE' for 5%\l"
	.string "off my brand of bath water!$"

MauvilleCity_Gym_Text_AngeloIntro:
	.string "I love shiny things!\p"
	.string ">be me\n"
	.string ">see a rare POKéMON\l"
	.string ">mfw an NPC tries to battle me\p"
	.string "Anon, you're about to get\n"
	.string "ratio'ed by my volts!$"

MauvilleCity_Gym_Text_AngeloDefeat:
	.string "Oh… My eyes are frazzled…\n"
	.string "This wasn't in the thread!$"

MauvilleCity_Gym_Text_AngeloPostBattle:
	.string "MAUVILLE GYM's WATTSON has a shiny\n"
	.string "forehead. It makes me happy!\p"
	.string "I'm going to post your team on the\n"
	.string "/vp/ board and call it 'mid'.\p"
	.string "Go touch grass, you absolute\n"
	.string "normie. Topkek!$"

MauvilleCity_Gym_Text_WattsonIntro:
	.string "Wahahahah! I've given up on my plans\n"
	.string "to convert the city, I have!\p"
	.string "Why build a city when you can just\n"
	.string "host a server farm? I'm mining coins\l"
	.string "while these kids mine for likes!\p"
	.string "Oh? Now, what are you doing here?\n"
	.string "You say you've gotten past all my\l"
	.string "rigged doors and influencers?\p"
	.string "Wahahahah! Now, that is amusing!\n"
	.string "You're the only real thing in this\l"
	.string "digital asylum!\p"
	.string "Then, I, WATTSON, the LEADER of\n"
	.string "MAUVILLE GYM, shall electrify you!$"

MauvilleCity_Gym_Text_WattsonDefeat:
	.string "Wahahahah!\n"
	.string "Fine, I lost!\p"
	.string "You ended up giving me a thrill that\n"
	.string "no NFT or viral video ever could!\l"
	.string "Take this BADGE!$"

MauvilleCity_Gym_Text_ReceivedDynamoBadge:
	.string "{PLAYER} received the DYNAMO BADGE\n"
	.string "from WATTSON.\p"
	.string "It comes with a subscription. Wahahaha!$"

MauvilleCity_Gym_Text_ExplainDynamoBadgeTakeThis:
	.string "With the DYNAMO BADGE, POKéMON can\n"
	.string "use ROCK SMASH out of battle.\p"
	.string "Smash those rocks like I smash the\n"
	.string "'buy' button on a dip! Wahahah!\p"
	.string "It also gives your POKéMON a little\n"
	.string "speed boost, like a high-speed\l"
	.string "internet connection!\p"
	.string "Hmm… You should take this, too!$"

MauvilleCity_Gym_Text_ExplainShockWave:
	.string "That TM34 contains VOLT SWITCH.\p"
	.string "It’s a move that lets you strike\n"
	.string "and then instantly swap out.\p"
	.string "It's just like my investment strategy:\n"
	.string "Take the profit and run before the\l"
	.string "market crashes! Wahahahah!\p"
	.string "… … … … … …$"

MauvilleCity_Gym_Text_RegisteredWattson:
	.string "Registered GYM LEADER WATTSON in the\n"
	.string "POKéNAV.\p"
	.string "You'll get his ads now.$"

MauvilleCity_Gym_Text_WattsonPostBattle:
	.string "I swell with optimism, seeing a young\n"
	.string "TRAINER who hasn't had their brain\l"
	.string "completely fried by the internet!\p"
	.string "There might be hope for this\n"
	.string "generation after all, Wahahah!$"

MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor:
	.string "Wahahahah!\p"
	.string "Go forth and endeavor, youngster!\n"
	.string "And remember: never click on\l"
	.string "suspicious links!$"

MauvilleCity_Gym_Text_GymStatue:
	.string "MAUVILLE CITY POKéMON GYM\p"
	.string "Sponsored by WATTSON.$"

MauvilleCity_Gym_Text_GymStatueCertified:
	.string "MAUVILLE CITY POKéMON GYM\p"
	.string "WATTSON'S CERTIFIED TRAINERS: {PLAYER}$"

MauvilleCity_Gym_Text_WattsonPreRematch:
	.string "WATTSON: Ah-ha! Here at last! I\n"
	.string "launched my own coin: WATTCOIN! Want to\l"
	.string "invest? No? Then battle! Wahahahaha!$"

MauvilleCity_Gym_Text_WattsonRematchDefeat:
	.string "Oof… My server farm crashed…$"

MauvilleCity_Gym_Text_WattsonPostRematch:
	.string "WATTSON: Time to reboot and restore\n"
	.string "from backup.\p"
	.string "Come back when my internet works again,\n"
	.string "won't you?$"

MauvilleCity_Gym_Text_WattsonRematchNeedTwoMons:
	.string "WATTSON: Ah-ha! Here at last! I\n"
	.string "launched my own coin: WATTCOIN! Want to\l"
	.string "invest? No? Then battle! Wahahahaha!\p"
	.string "Oops! Only one POKéMON? Even WATTCOIN\n"
	.string "has more holders than that! Come back\l"
	.string "with two.$"

@ Project Grounded: aanwijzing van het level van de gym-ace (placeholder)
MauvilleCity_Gym_Text_GymGuideAceLevel:
	.string "Insider info: the LEADER's ace\n"
	.string "is level 25.\p"
	.string "You didn't hear it from me.\n"
	.string "You heard it from me, but still.$"

MauvilleCity_Gym_Text_GymGuideNextAce:
	.string "Next stop: FLANNERY in LAVARIDGE.\n"
	.string "Their ace is level 29.\p"
	.string "That's all the free advice.\n"
	.string "The rest costs a RARE CANDY.$"
