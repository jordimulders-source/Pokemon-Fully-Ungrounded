MossdeepCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MossdeepCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, MossdeepCity_Gym_OnLoad
	.byte 0

@ NOTE: Mossdeep Gym was redesigned between R/S and E. Leftover (and now functionally unused) scripts are commented below

MossdeepCity_Gym_OnTransition:
	setflag FLAG_TEMP_HIDE_FOLLOWER @ Hide follower since it can collide with moving statues
	end

@ All the below checks are leftover from RS. FLAG_MOSSDEEP_GYM_SWITCH_X is never set
MossdeepCity_Gym_OnLoad:
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_1, MossdeepCity_Gym_EventScript_SetSwitch1Metatiles
	goto MossdeepCity_Gym_EventScript_CheckSwitch2
	end

MossdeepCity_Gym_EventScript_CheckSwitch2::
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_2, MossdeepCity_Gym_EventScript_SetSwitch2Metatiles
	goto MossdeepCity_Gym_EventScript_CheckSwitch3
	end

MossdeepCity_Gym_EventScript_CheckSwitch3::
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_3, MossdeepCity_Gym_EventScript_SetSwitch3Metatiles
	goto MossdeepCity_Gym_EventScript_CheckSwitch4
	end

MossdeepCity_Gym_EventScript_CheckSwitch4::
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_4, MossdeepCity_Gym_EventScript_SetSwitch4Metatiles
	end

@ All the below set metatile scripts are leftover from RS and are functionally unused
MossdeepCity_Gym_EventScript_SetSwitch1Metatiles::
	setmetatile 5, 5, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 2, 7, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_CheckSwitch2
	end

MossdeepCity_Gym_EventScript_SetSwitch2Metatiles::
	setmetatile 8, 14, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 8, 10, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_CheckSwitch3
	end

MossdeepCity_Gym_EventScript_SetSwitch3Metatiles::
	setmetatile 15, 17, METATILE_RSMossdeepGym_RedArrow_Left, FALSE
	setmetatile 17, 15, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_CheckSwitch4
	end

MossdeepCity_Gym_EventScript_SetSwitch4Metatiles::
	setmetatile 1, 23, METATILE_RSMossdeepGym_RedArrow_Up, FALSE
	setmetatile 5, 24, METATILE_RSMossdeepGym_Switch_Down, TRUE
	end

MossdeepCity_Gym_EventScript_TateAndLiza::
	trainerbattle_double TRAINER_TATE_AND_LIZA_1, MossdeepCity_Gym_Text_TateAndLizaIntro, MossdeepCity_Gym_Text_TateAndLizaDefeat, MossdeepCity_Gym_Text_TateAndLizaNeedTwoMons, MossdeepCity_Gym_EventScript_TateAndLizaDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MossdeepCity_Gym_EventScript_TateAndLizaRematch
	goto_if_unset FLAG_RECEIVED_TM_CALM_MIND, MossdeepCity_Gym_EventScript_GiveCalmMind2
	msgbox MossdeepCity_Gym_Text_TateAndLizaPostBattle, MSGBOX_DEFAULT
	release
	end

MossdeepCity_Gym_EventScript_TateAndLizaDefeated::
	message MossdeepCity_Gym_Text_ReceivedMindBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox MossdeepCity_Gym_Text_ExplainMindBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_MOSSDEEP_GYM
	setflag FLAG_BADGE07_GET
	setflag FLAG_HIDE_AQUA_HIDEOUT_GRUNTS
	clearflag FLAG_HIDE_SLATEPORT_CITY_STERNS_SHIPYARD_MR_BRINEY
	clearflag FLAG_UNKNOWN_0x393
	setvar VAR_0x8008, 7
	call Common_EventScript_SetGymTrainers
	clearflag FLAG_HIDE_SLATEPORT_CITY_HARBOR_PATRONS
	clearflag FLAG_HIDE_MOSSDEEP_CITY_TEAM_MAGMA
	clearflag FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_TEAM_MAGMA
	clearflag FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_TEAM_MAGMA
	clearflag FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_STEVEN
	setvar VAR_MOSSDEEP_CITY_STATE, 1
	setflag FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_STEVEN
	setvar VAR_MOSSDEEP_SPACE_CENTER_STATE, 1
	call MossdeepCity_Gym_EventScript_GiveCalmMind
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox MossdeepCity_Gym_Text_RegisteredTateAndLiza, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_TATE_AND_LIZA_MATCH_CALL
	release
	end

MossdeepCity_Gym_EventScript_GiveCalmMind2::
	giveitem ITEM_TM_LASER_BEAM
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox MossdeepCity_Gym_Text_ExplainCalmMind, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_CALM_MIND
	release
	end

MossdeepCity_Gym_EventScript_GiveCalmMind::
	giveitem ITEM_TM_LASER_BEAM
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox MossdeepCity_Gym_Text_ExplainCalmMind, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_CALM_MIND
	return

MossdeepCity_Gym_EventScript_TateAndLizaRematch::
	trainerbattle_rematch_double TRAINER_TATE_AND_LIZA_1, MossdeepCity_Gym_Text_TateAndLizaPreRematch, MossdeepCity_Gym_Text_TateAndLizaRematchDefeat, MossdeepCity_Gym_Text_TateAndLizaRematchNeedTwoMons
	msgbox MossdeepCity_Gym_Text_TateAndLizaPostRematch, MSGBOX_AUTOCLOSE
	end

@ All the below switch scripts are leftover from RS and are functionally unused
MossdeepCity_Gym_EventScript_Switch1::
	lockall
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_1, MossdeepCity_Gym_EventScript_ClearSwitch1
	setflag FLAG_MOSSDEEP_GYM_SWITCH_1
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 5, 5, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 2, 7, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed::
	special DrawWholeMapView
	playse SE_CLICK
	releaseall
	end

MossdeepCity_Gym_EventScript_ClearSwitch1::
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_1
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 5, 5, METATILE_RSMossdeepGym_RedArrow_Left, FALSE
	setmetatile 2, 7, METATILE_RSMossdeepGym_Switch_Up, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_Switch2::
	lockall
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_2, MossdeepCity_Gym_EventScript_ClearSwitch2
	setflag FLAG_MOSSDEEP_GYM_SWITCH_2
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 8, 14, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 8, 10, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_ClearSwitch2::
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_2
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 8, 14, METATILE_RSMossdeepGym_RedArrow_Down, FALSE
	setmetatile 8, 10, METATILE_RSMossdeepGym_Switch_Up, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_Switch3::
	lockall
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_3, MossdeepCity_Gym_EventScript_ClearSwitch3
	setflag FLAG_MOSSDEEP_GYM_SWITCH_3
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 15, 17, METATILE_RSMossdeepGym_RedArrow_Left, FALSE
	setmetatile 17, 15, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_ClearSwitch3::
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_3
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 15, 17, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 17, 15, METATILE_RSMossdeepGym_Switch_Up, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_Switch4::
	lockall
	goto_if_set FLAG_MOSSDEEP_GYM_SWITCH_4, MossdeepCity_Gym_EventScript_ClearSwitch4
	setflag FLAG_MOSSDEEP_GYM_SWITCH_4
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 1, 23, METATILE_RSMossdeepGym_RedArrow_Up, FALSE
	setmetatile 5, 24, METATILE_RSMossdeepGym_Switch_Down, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_ClearSwitch4::
	clearflag FLAG_MOSSDEEP_GYM_SWITCH_4
	applymovement LOCALID_PLAYER, MossdeepCity_Gym_Movement_WaitAfterSwitchUse
	waitmovement 0
	setmetatile 1, 23, METATILE_RSMossdeepGym_RedArrow_Right, FALSE
	setmetatile 5, 24, METATILE_RSMossdeepGym_Switch_Up, TRUE
	goto MossdeepCity_Gym_EventScript_DrawMapAfterSwitchUsed
	end

MossdeepCity_Gym_EventScript_WarpToEntrance::
	lockall
	warpmossdeepgym MAP_MOSSDEEP_CITY_GYM, 7, 30
	waitstate
	releaseall
	end

MossdeepCity_Gym_EventScript_Uri::
	trainerbattle_single TRAINER_URI, MossdeepCity_Gym_Text_PrestonIntro, MossdeepCity_Gym_Text_PrestonDefeat
	msgbox MossdeepCity_Gym_Text_PrestonPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Virgil::
	trainerbattle_single TRAINER_VIRGIL, MossdeepCity_Gym_Text_VirgilIntro, MossdeepCity_Gym_Text_VirgilDefeat
	msgbox MossdeepCity_Gym_Text_VirgilPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Blake::
	trainerbattle_single TRAINER_BLAKE, MossdeepCity_Gym_Text_BlakeIntro, MossdeepCity_Gym_Text_BlakeDefeat
	msgbox MossdeepCity_Gym_Text_BlakePostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Hannah::
	trainerbattle_single TRAINER_HANNAH, MossdeepCity_Gym_Text_HannahIntro, MossdeepCity_Gym_Text_HannahDefeat
	msgbox MossdeepCity_Gym_Text_HannahPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Samantha::
	trainerbattle_single TRAINER_SAMANTHA, MossdeepCity_Gym_Text_SamanthaIntro, MossdeepCity_Gym_Text_SamanthaDefeat
	msgbox MossdeepCity_Gym_Text_SamanthaPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Maura::
	trainerbattle_single TRAINER_MAURA, MossdeepCity_Gym_Text_MauraIntro, MossdeepCity_Gym_Text_MauraDefeat
	msgbox MossdeepCity_Gym_Text_MauraPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Sylvia::
	trainerbattle_single TRAINER_SYLVIA, MossdeepCity_Gym_Text_SylviaIntro, MossdeepCity_Gym_Text_SylviaDefeat
	msgbox MossdeepCity_Gym_Text_SylviaPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Nate::
	trainerbattle_single TRAINER_NATE, MossdeepCity_Gym_Text_NateIntro, MossdeepCity_Gym_Text_NateDefeat
	msgbox MossdeepCity_Gym_Text_NatePostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Macey::
	trainerbattle_single TRAINER_MACEY, MossdeepCity_Gym_Text_MaceyIntro, MossdeepCity_Gym_Text_MaceyDefeat
	msgbox MossdeepCity_Gym_Text_MaceyPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Clifford::
	trainerbattle_double TRAINER_CLIFFORD, MossdeepCity_Gym_Text_CliffordIntro, MossdeepCity_Gym_Text_CliffordDefeat, MossdeepCity_Gym_Text_CliffordNotEnoughMons
	msgbox MossdeepCity_Gym_Text_CliffordPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Nicholas::
	trainerbattle_single TRAINER_NICHOLAS, MossdeepCity_Gym_Text_NicholasIntro, MossdeepCity_Gym_Text_NicholasDefeat
	msgbox MossdeepCity_Gym_Text_NicholasPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_Kathleen::
	trainerbattle_single TRAINER_KATHLEEN, MossdeepCity_Gym_Text_KathleenIntro, MossdeepCity_Gym_Text_KathleenDefeat
	msgbox MossdeepCity_Gym_Text_KathleenPostBattle, MSGBOX_AUTOCLOSE
	end

MossdeepCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_MOSSDEEP_GYM, MossdeepCity_Gym_EventScript_GymGuidePostVictory
	msgbox MossdeepCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	msgbox MossdeepCity_Gym_Text_GymGuideAceLevel, MSGBOX_DEFAULT
	release
	end

MossdeepCity_Gym_EventScript_GymGuidePostVictory::
	msgbox MossdeepCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	msgbox MossdeepCity_Gym_Text_GymGuideNextAce, MSGBOX_DEFAULT
	release
	end

@ Leftover from RS, functionally unused
MossdeepCity_Gym_Movement_WaitAfterSwitchUse:
	delay_16
	delay_16
	step_end

MossdeepCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE07_GET, MossdeepCity_Gym_EventScript_GymStatueCertified
	goto MossdeepCity_Gym_EventScript_GymStatue
	end

MossdeepCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE07_GET, MossdeepCity_Gym_EventScript_GymStatueCertified
	goto MossdeepCity_Gym_EventScript_GymStatue
	end

MossdeepCity_Gym_EventScript_GymStatueCertified::
	msgbox MossdeepCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

MossdeepCity_Gym_EventScript_GymStatue::
	msgbox MossdeepCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

MossdeepCity_Gym_EventScript_YellowFloorSwitch::
	playse SE_SWITCH
	waitse
	playse SE_REPEL
	initrotatingtilepuzzle FALSE
	moverotatingtileobjects 0
	waitmovement 0
	turnrotatingtileobjects
	waitmovement 0
	freerotatingtilepuzzle
	end

MossdeepCity_Gym_EventScript_BlueFloorSwitch::
	playse SE_SWITCH
	waitse
	playse SE_REPEL
	initrotatingtilepuzzle FALSE
	moverotatingtileobjects 1
	waitmovement 0
	turnrotatingtileobjects
	waitmovement 0
	freerotatingtilepuzzle
	end

MossdeepCity_Gym_EventScript_GreenFloorSwitch::
	playse SE_SWITCH
	waitse
	playse SE_REPEL
	initrotatingtilepuzzle FALSE
	moverotatingtileobjects 2
	waitmovement 0
	turnrotatingtileobjects
	waitmovement 0
	freerotatingtilepuzzle
	end

MossdeepCity_Gym_EventScript_PurpleFloorSwitch::
	playse SE_SWITCH
	waitse
	playse SE_REPEL
	initrotatingtilepuzzle FALSE
	moverotatingtileobjects 3
	waitmovement 0
	turnrotatingtileobjects
	waitmovement 0
	freerotatingtilepuzzle
	end

MossdeepCity_Gym_EventScript_RedFloorSwitch::
	playse SE_SWITCH
	waitse
	playse SE_REPEL
	initrotatingtilepuzzle FALSE
	moverotatingtileobjects 4
	waitmovement 0
	turnrotatingtileobjects
	waitmovement 0
	freerotatingtilepuzzle
	end

MossdeepCity_Gym_Text_GymGuideAdvice:
    .string "Yo, how's it going, CHAMPION-bound\n"
    .string "{PLAYER}?\p"
    .string "Look, I'll be real with you: I've had\n"
    .string "a headache for three hours just from\l"
    .string "breathing in all this incense.\p"
    .string "The GYM LEADERS here use PSYCHIC-type\n"
    .string "POKéMON, but they call themselves\l"
    .string "“Spiritual Alignment Coaches.”\p"
    .string "If you go in with FIGHTING- or POISON-\n"
    .string "types, they'll “energetically cleanse”\l"
    .string "your team right out of the building.\p"
    .string "They fight in a Double Battle.\n"
    .string "It's a mess of manifesting, tarot\l"
    .string "cards, and bad cosmic vibes.\p"
    .string "Stay focused, trust your logic, and\n"
    .string "don't let them upsell you any crystals.\l"
    .string "Go for it!$"

MossdeepCity_Gym_Text_GymGuidePostVictory:
    .string "Wow, you actually won!\n"
    .string "I guess your vibe was just stronger.\p"
    .string "Can I finally unplug that salt lamp\n"
    .string "now? The glowing is giving me\l"
    .string "serious eye strain.$"

MossdeepCity_Gym_Text_PrestonIntro:
	.string "Stop! Cease and desist!\n"
	.string "I sense a massive copyright violation!\p"
	.string "Using a spoon to focus psychic power\n"
	.string "is MY brand. You and your POKéMON\l"
	.string "will hear from my lawyers!$"

MossdeepCity_Gym_Text_PrestonDefeat:
	.string "Objection!\n"
	.string "This result is inadmissible in court!$"

MossdeepCity_Gym_Text_PrestonPostBattle:
	.string "KADABRA and ALAKAZAM are clearly\n"
	.string "guilty of identity theft.\p"
	.string "I tried to sue them for 20 years,\n"
	.string "but apparently, you can't serve papers\l"
	.string "to a fictional species. What a scam!$"

MossdeepCity_Gym_Text_VirgilIntro:
	.string "Stop! I can see your potential from\n"
	.string "a mile away, but your energy is totally\l"
	.string "unmonetized!\p"
	.string "Let me show you my 'Elite Ascension'\n"
	.string "battle strategy. For a small fee, I can\l"
	.string "unlock your true talent!$"

MossdeepCity_Gym_Text_VirgilDefeat:
	.string "Wait! This defeat is just a\n"
	.string "learning opportunity for your brand!$"

MossdeepCity_Gym_Text_VirgilPostBattle:
	.string "You have raw talent, kid, but you're\n"
	.string "missing the 'Twin Flame' mindset.\p"
	.string "Our GYM LEADERS? They're the ultimate\n"
	.string "prodigies. They've reached the\l"
	.string "diamond tier of consciousness!\p"
	.string "Check out my webinar later if you\n"
	.string "want to reach their level... or just\l"
	.string "give me 5000 PokéDollars now?$"

MossdeepCity_Gym_Text_BlakeIntro:
	.string "Fufufufu… Behold! I am currently\n"
	.string "projecting my consciousness into the\l"
	.string "astral plane!\p"
	.string "Wrooooooooaaaar!\n"
	.string "… … … … … … …\p"
	.string "Wait, give me a second… my soul is\n"
	.string "having some lag issues…$"

MossdeepCity_Gym_Text_BlakeDefeat:
	.string "My win-rate in the astral plane is\n"
	.string "much higher than this!$"

MossdeepCity_Gym_Text_BlakePostBattle:
	.string "Lifting a POKé BALL with my mind is\n"
	.string "hard because of its dense atoms.\l"
	.string "But this dust bunny…\p"
	.string "Whoooooooooooooooh!\n"
	.string "… … … … … …\p"
	.string "Stop laughing! I am levitating it!\n"
	.string "I am NOT blowing on it with my mouth!\l"
	.string "That's just the wind of the cosmos!$"

MossdeepCity_Gym_Text_HannahIntro:
	.string "When you lose to me, don't be too hard\n"
	.string "on yourself or your aura.\p"
	.string "It's not that you're weak... I'm just\n"
	.string "that strong! My rising sign is\l"
	.string "naturally cracked at battling!$"

MossdeepCity_Gym_Text_HannahDefeat:
	.string "The stars... they lied to me? This\n"
	.string "wasn't in my daily horoscope!$"

MossdeepCity_Gym_Text_HannahPostBattle:
	.string "I'm not going to let this loss lower\n"
	.string "my vibrations. I'll just manifest a\l"
	.string "win in my next encounter.\p"
	.string "Delusional optimism is my\n"
	.string "strong point!$"

MossdeepCity_Gym_Text_SamanthaIntro:
	.string "I see it...\n"
	.string "The cards don't lie!\p"
	.string "The Tower, the Moon, and... oh, a\n"
	.string "reversed Magician! If you can beat\l"
	.string "me, I'll reveal your true destiny!$"

MossdeepCity_Gym_Text_SamanthaDefeat:
	.string "The cards... they were upside down!$"

MossdeepCity_Gym_Text_SamanthaPostBattle:
	.string "You will wage a terrifically intense\n"
	.string "battle with our GYM LEADERS...\p"
	.string "The result... I can see it clearly in\n"
	.string "the Three of Swords, but you'll have\l"
	.string "to pay for the full reading!$"

MossdeepCity_Gym_Text_MauraIntro:
	.string "The spirits you have carried...\n"
	.string "The shadows that follow you...\p"
	.string "My board is twitching with your\n"
	.string "darkest secrets. Come and face the\l"
	.string "judgment of the beyond!$"

MossdeepCity_Gym_Text_MauraDefeat:
	.string "The spirits... they have gone silent!$"

MossdeepCity_Gym_Text_MauraPostBattle:
	.string "I thought I was reading your future\n"
	.string "and the voices of the departed.\p"
	.string "But it turns out I was just picking\n"
	.string "up the telepathic static from my\l"
	.string "COFRAGRIGUS the whole time.\p"
	.string "What goes around comes around...\n"
	.string "usually in a gold plated coffin.$"

MossdeepCity_Gym_Text_SylviaIntro:
	.string "Even at the risk of my mortal soul,\n"
	.string "I will win this battle!\p"
	.string "The spirits of the night and the\n"
	.string "SUCCUBUS guides are on my side!$"

MossdeepCity_Gym_Text_SylviaDefeat:
	.string "What you do...\n"
	.string "It horrifies me...$"

MossdeepCity_Gym_Text_SylviaPostBattle:
	.string "How dare you break my circle...\p"
	.string "It won't be my fault if a SUCCUBUS\n"
	.string "haunts your dreams or something\l"
	.string "horrible befalls you...$"

MossdeepCity_Gym_Text_NateIntro:
	.string "Hohoho.\p"
	.string "I say... you look like a fellow scholar!\p"
	.string "I recently read a very thick book\n"
	.string "about secret societies and cults.\l"
	.string "Let me demonstrate the tenacious\l"
	.string "rituals... I mean, tactics I learned!$"

MossdeepCity_Gym_Text_NateDefeat:
	.string "Oh! My, my!\n"
	.string "The book didn't mention this part!$"

MossdeepCity_Gym_Text_NatePostBattle:
	.string "I... I must admit I don't really\n"
	.string "understand what is happening here.\p"
	.string "Everyone is talking about auras and\n"
	.string "cosmic vibrations, but I just want\l"
	.string "to discuss chapter four of my book.\p"
	.string "It's all very rattle... rattling!$"

MossdeepCity_Gym_Text_KathleenIntro:
	.string "YOU ARE BEWIIIIIIIIIITCHEEEED!\p"

MossdeepCity_Gym_Text_KathleenDefeat:
	.string "N-nooooo!\p"
	.string "The spell… it backfired!$"

MossdeepCity_Gym_Text_KathleenPostBattle:
	.string "Your vitality is contagious!\n"
	.string "Get away from me quickly before\l"
	.string "you accidentally manifest some\l"
	.string "sunshine and rainbows!$"

MossdeepCity_Gym_Text_CliffordIntro:
	.string "Do what thou wilt shall be the whole\n"
	.string "of the law!\p"
	.string "I may be past my prime, but my\n"
	.string "magick is more potent than ever.\l"
	.string "Prepare for a true initiation!$"

MossdeepCity_Gym_Text_CliffordDefeat:
	.string "Abrahadabra... the ritual... failed!$"

MossdeepCity_Gym_Text_CliffordNotEnoughMons:
	.string "A double battle with only one\n"
	.string "POKéMON? Come back with two.$"

MossdeepCity_Gym_Text_CliffordPostBattle:
	.string "You possess a terrifying amount of\n"
	.string "willpower. Perhaps you are the\l"
	.string "chosen one I read about in my\l"
	.string "midnight evocations.\p"
	.string "Love is the law, love under will... but\n"
	.string "losing still stings!$"

MossdeepCity_Gym_Text_MaceyIntro:
	.string "You shall not pass into the inner\n"
	.string "sanctum! The Law of Thelema is\l"
	.string "absolute, and your vibration is\l"
	.string "not authorized for this ritual!$"

MossdeepCity_Gym_Text_MaceyDefeat:
	.string "How could a profane outsider be so\n"
	.string "ludicrously strong?$"

MossdeepCity_Gym_Text_MaceyPostBattle:
	.string "Humph! You may be strong, but you're\n"
	.string "not suitable for the PSYCHIC type!\p"
	.string "The way you battle is somehow brutal\n"
	.string "and lacking in magickal grace.\l"
	.string "Master CLIFFORD will be displeased!$"

MossdeepCity_Gym_Text_NicholasIntro:
	.string "Wroooar! Science and alchemy are\n"
	.string "two sides of the same coin!\p"
	.string "Humankind cannot gain anything\n"
	.string "without first giving something in\l"
	.string "return. To obtain, something of equal\l"
	.string "value must be lost!\p"
	.string "That is the law of EQUIVALENT\n"
	.string "EXCHANGE! Prepare to be dissected!$"

MossdeepCity_Gym_Text_NicholasDefeat:
	.string "The reaction... it failed!\n"
	.string "My calculations were off!$"

MossdeepCity_Gym_Text_NicholasPostBattle:
	.string "All right! I need a catalyst to\n"
	.string "bypass the law of exchange.\p"
	.string "I shall develop a red, glowing\n"
	.string "PHILOSOPHER'S STONE next.\p"
	.string "I just need a few thousand souls and\n"
	.string "some mercury... hohoho!$"

MossdeepCity_Gym_Text_TateAndLizaIntro:
	.string "TATE: Hehehe... Did you feel that?\p"
	.string "LIZA: Fufufu... The vibration of the\n"
	.string "cosmic door slamming shut?\p"
	.string "TATE: We are not just two LEADERS.\n"
	.string "LIZA: We are one soul split by a\l"
	.string "shooting star and ancient stardust!\p"
	.string "TATE: We don't need to speak...\n"
	.string "LIZA: Because our Twin Flame energy\l"
	.string "is currently peak performance!\p"
	.string "TATE: I am thinking of a number...\n"
	.string "LIZA: It is the sound of your aura\l"
	.string "screaming in lowercase!\p"
	.string "TATE: This quantum combination...\n"
	.string "LIZA: This psychic fever dream...\l"
	.string "Can you even comprehend it?$"

MossdeepCity_Gym_Text_TateAndLizaDefeat:
	.string "TATE: What?! Our frequency...\n"
	.string "LIZA: It has been scrambled by a\l"
	.string "lower vibrational entity!\p"
	.string "TATE: The cards... the stars...\n"
	.string "LIZA: They are all out of alignment!\l"
	.string "Fine... take the badge before our\l"
	.string "chakras implode!$"

MossdeepCity_Gym_Text_ReceivedMindBadge:
	.string "{PLAYER} received the MIND BADGE from\n"
	.string "TATE and LIZA.\p"
	.string "They finished each other's sentences\n"
	.string "while handing it over.$"

MossdeepCity_Gym_Text_ExplainMindBadgeTakeThis:
	.string "TATE: The MIND BADGE aligns the\n"
	.string "chakras of your team's power.\p"
	.string "LIZA: It grants them focus in their\n"
	.string "SP. ATK and SP. DEF.\p"
	.string "TATE: It also allows your soul to\n"
	.string "DIVE into the depths of the ocean.\p"
	.string "LIZA: Take this offering as well... it\n"
	.string "vibrates with intense energy.$"

MossdeepCity_Gym_Text_ExplainCalmMind:
	.string "TATE: That TM55 contains...\n"
	.string "LIZA: LASER BEAM!\p"
	.string "TATE: A beam of pure focus, thinner\n"
	.string "than a hair...\p"
	.string "LIZA: That burns through every wall\n"
	.string "the mind can build!\p"
	.string "TATE: Protect, screens, boosts...\n"
	.string "LIZA: Nothing survives a clear mind!\p"
	.string "... ... ... ... ... ...$"

MossdeepCity_Gym_Text_RegisteredTateAndLiza:
	.string "The cosmic signatures of TATE & LIZA\n"
	.string "were etched into the POKéNAV.$"

MossdeepCity_Gym_Text_TateAndLizaPostBattle:
	.string "TATE: Your bond is like a supernova\n"
	.string "swallowing our collective dream.\p"
	.string "LIZA: You have transcended our\n"
	.string "Twin Flame connection.\p"
	.string "TATE: Go now... the stars have\n"
	.string "already written your next victory.\p"
	.string "LIZA: We will continue to manifest\n"
	.string "your downfall in our dreams.$"

MossdeepCity_Gym_Text_TateAndLizaNeedTwoMons:
	.string "TATE: Hehehe... Were you surprised?\p"
	.string "LIZA: That the universe requires\n"
	.string "balance in all things?\p"
	.string "TATE: You only have one soul...\n"
	.string "LIZA: I mean, one POKéMON that\l"
	.string "can battle in this plane.\p"
	.string "TATE: We cannot dance in the moonlight\n"
	.string "with an uneven number!\p"
	.string "LIZA: Return when your party has\n"
	.string "achieved numerical symmetry.$"

MossdeepCity_Gym_Text_GymStatue:
	.string "MOSSDEEP CITY POKéMON GYM\p"
	.string "The mystic combination.$"

MossdeepCity_Gym_Text_GymStatueCertified:
	.string "MOSSDEEP CITY POKéMON GYM\p"
	.string "LIZA AND TATE'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

MossdeepCity_Gym_Text_TateAndLizaPreRematch:
	.string "TATE: Mercury… LIZA: …is in retrograde.\p"
	.string "TATE: A perfect day… LIZA: …for a\n"
	.string "rematch!\p"
	.string "TATE: Our Twin Flame… LIZA: …has been\n"
	.string "recharged by the full moon!$"

MossdeepCity_Gym_Text_TateAndLizaRematchDefeat:
	.string "TATE: The tarot said… LIZA: …we would\n"
	.string "win. We want a refund!$"

MossdeepCity_Gym_Text_TateAndLizaPostRematch:
	.string "TATE: You can knock us down… LIZA: …but\n"
	.string "our horoscope says we'll rise again.\p"
	.string "TATE: Next week. LIZA: Probably.$"

MossdeepCity_Gym_Text_TateAndLizaRematchNeedTwoMons:
	.string "TATE: You're back… LIZA: You're back…\p"
	.string "TATE: With one POKéMON? LIZA: The\n"
	.string "universe demands two. Come back\l"
	.string "balanced.$"

@ Project Grounded: aanwijzing van het level van de gym-ace (placeholder)
MossdeepCity_Gym_Text_GymGuideAceLevel:
	.string "Insider info: the LEADER's ace\n"
	.string "is level 49.\p"
	.string "You didn't hear it from me.\n"
	.string "You heard it from me, but still.$"

MossdeepCity_Gym_Text_GymGuideNextAce:
	.string "Next stop: WALLACE in SOOTOPOLIS.\n"
	.string "Their ace is level 56.\p"
	.string "That's all the free advice.\n"
	.string "The rest costs a RARE CANDY.$"
