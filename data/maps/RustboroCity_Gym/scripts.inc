RustboroCity_Gym_MapScripts::
	.byte 0

RustboroCity_Gym_EventScript_Roxanne::
	trainerbattle_single TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxanneIntro, RustboroCity_Gym_Text_RoxanneDefeat, RustboroCity_Gym_EventScript_RoxanneDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Gym_EventScript_RoxanneRematch
	goto_if_unset FLAG_RECEIVED_TM_ROCK_TOMB, RustboroCity_Gym_EventScript_GiveRockTomb
	msgbox RustboroCity_Gym_Text_RoxannePostBattle, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneDefeated::
	message RustboroCity_Gym_Text_ReceivedStoneBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox RustboroCity_Gym_Text_StoneBadgeInfoTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_RUSTBORO_GYM
	setflag FLAG_BADGE01_GET
	setvar VAR_RUSTBORO_CITY_STATE, 1
	addvar VAR_PETALBURG_GYM_STATE, 1
	setvar VAR_0x8008, 1
	call Common_EventScript_SetGymTrainers
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto RustboroCity_Gym_EventScript_GiveRockTomb
	end

RustboroCity_Gym_EventScript_GiveRockTomb::
	giveitem ITEM_TM_STEALTH_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_ROCK_TOMB
	msgbox RustboroCity_Gym_Text_ExplainRockTomb, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneRematch::
	trainerbattle_rematch_double TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxannePreRematch, RustboroCity_Gym_Text_RoxanneRematchDefeat, RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons
	msgbox RustboroCity_Gym_Text_RoxannePostRematch, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Josh::
	trainerbattle_single TRAINER_JOSH, RustboroCity_Gym_Text_JoshIntro, RustboroCity_Gym_Text_JoshDefeat
	msgbox RustboroCity_Gym_Text_JoshPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Tommy::
	trainerbattle_single TRAINER_TOMMY, RustboroCity_Gym_Text_TommyIntro, RustboroCity_Gym_Text_TommyDefeat
	msgbox RustboroCity_Gym_Text_TommyPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Dio::
	trainerbattle_single TRAINER_DIO, RustboroCity_Gym_Text_MarcIntro, RustboroCity_Gym_Text_MarcDefeat
	msgbox RustboroCity_Gym_Text_MarcPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, RustboroCity_Gym_EventScript_GymGuidePostVictory
	msgbox RustboroCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	msgbox RustboroCity_Gym_Text_GymGuideAceLevel, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_GymGuidePostVictory::
	msgbox RustboroCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	msgbox RustboroCity_Gym_Text_GymGuideNextAce, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_GymStatueCertified::
	msgbox RustboroCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_GymStatue::
	msgbox RustboroCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_RegisterRoxanne::
	lockall
	pokenavcall RustboroCity_Gym_Text_RoxanneRegisterCall
	waitmessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox RustboroCity_Gym_Text_RegisteredRoxanne, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_ROXANNE_MATCH_CALL
	clearflag FLAG_ENABLE_ROXANNE_FIRST_CALL
	releaseall
	end

RustboroCity_Gym_Text_GymGuideAdvice:
	.string "Yo! Put your lighters up!\p"
	.string "Listen, my friend! Are you ready to\n"
	.string "become the CHAMPION?\p"
	.string "I'm no TRAINER, just a roadie for the\n"
	.string "stars, but I can give you some\l"
	.string "winning advice.\p"
	.string "ROXANNE, the GYM LEADER, is a user\n"
	.string "of ROCK-type POKéMON.\p"
	.string "Look, she don't have to put on the\n"
	.string "RED LIGHT, but she'll try to stop\l"
	.string "you cold with her ROCK-types!\p"
	.string "She's just ANOTHER BRICK IN THE\n"
	.string "WALL if you use WATER moves!\p"
	.string "If you're feeling UNDER PRESSURE,\n"
	.string "hit her with GRASS and make her\l"
	.string "feel like a ROLLING STONE.\p"
	.string "Come see me afterwards. For those\n"
	.string "about to ROCK, I SALUTE YOU!\p"
	.string "Well, go for it!$"

RustboroCity_Gym_Text_GymGuidePostVictory:
	.string "Whoa! A breathtaking victory!\n"
	.string "I guess we ARE THE CHAMPIONS, my\l"
	.string "friend!\p"
	.string "Check your TRAINER CARD.\p"
	.string "That STONE BADGE is a real\n"
	.string "DIAMOND IN THE ROUGH, and it's\l"
	.string "properly recorded now.\p"
	.string "In other words…\p"
	.string "You're officially climbing the\n"
	.string "STAIRWAY TO HEAVEN. Uh, I mean,\l"
	.string "to the CHAMPIONSHIP!\p"
	.string "It's a long way to the top if you\n"
	.string "wanna ROCK 'N ROLL, but that's got\l"
	.string "to feel awesome!$"

RustboroCity_Gym_Text_JoshIntro:
	.string "Heaven smiles....above me.$"

RustboroCity_Gym_Text_JoshDefeat:
	.string "First it giveth,\n"
	.string "and then it taketh away...$"

RustboroCity_Gym_Text_JoshPostBattle:
	.string "Shock me awake! Tear me apart!\n"
	.string "Pinned like a note in a hospital gown.\p"
	.string "Prison of sleep, deepened now...\n"
	.string "A rabbit hole never to be found\l"
	.string "again.$"

RustboroCity_Gym_Text_TommyIntro:
	.string "Has he lost his mind?\n"
	.string "Can he see or is he blind?\p"
	.string "I AM IRON MAN!$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "What is this that stands before me?$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "Finished with my woman 'cause she\n"
	.string "couldn't help me with my mind…\p"
	.string "PARANOID!$"

RustboroCity_Gym_Text_MarcIntro:
	.string "Holy Diver!\p"
	.string "You've been down too long in the\n"
	.string "midnight sea!\p"
	.string "Can't you see what I mean?$"

RustboroCity_Gym_Text_MarcDefeat:
	.string "I'M GOING HOOOOOOOOOOOOOME!$"

RustboroCity_Gym_Text_MarcPostBattle:
	.string "Sleep with the devil, the devil will\n"
	.string "take you away...\p"
	.string "Oh, Gates of Babylon!\p"
	.string "The LEADER'S smarts are like a\n"
	.string "Sign of the Southern Cross!$"

RustboroCity_Gym_Text_RoxanneIntro:
	.string "I am ROXANNE.\p"
	.string "And no, you don't have to put on\n"
	.string "the red light. Wrong band.\p"
	.string "I'm just a girl in the world…\n"
	.string "with a team of solid granite!\p"
	.string "Wake me up inside? My NOSEPASS\n"
	.string "hasn't slept since the Stone Age.\p"
	.string "So hit me with your best shot.\n"
	.string "Fire away! Rock-types don't mind.$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "In your head, in your head…\n"
	.string "ZOMBIE, ZOMBIE. That's my team now.\p"
	.string "Love is a battlefield, and you\n"
	.string "just paved mine.$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "I'm only happy when it rains.\n"
	.string "Rock-types hate rain. I'm conflicted.\p"
	.string "I love rock 'n' roll. So put another\n"
	.string "dime in the jukebox and go, baby!$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} received the STONE BADGE from\n"
	.string "ROXANNE.\p"
	.string "It rocks.$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "The STONE BADGE heightens the ATTACK\n"
	.string "power of your POKéMON.\p"
	.string "It also enables them to use the HM move\n"
	.string "CUT outside of battle.\p"
	.string "Please… take this with you, too.\n"
	.string "Don't speak. Just take it.$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "That TECHNICAL MACHINE, TM39,\n"
	.string "contains STEALTH ROCK.\p"
	.string "It scatters pointed stones around\n"
	.string "your foe's side of the field.\p"
	.string "Every time a foe switches in, the\n"
	.string "rocks bite. Like a BARRACUDA.\p"
	.string "And TMs are reusable now.\n"
	.string "Unlike my last three drummers.$"

RustboroCity_Gym_Text_GymStatue:
	.string "RUSTBORO CITY POKéMON GYM\p"
	.string "Rock on!$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "RUSTBORO CITY POKéMON GYM\p"
	.string "ROXANNE'S CERTIFIED TRAINERS: {PLAYER}$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "… … … … … … … … … … … Beep!\p"
	.string "ROXANNE: Hey {PLAYER}, it's ROXANNE!\n"
	.string "BRAWLY says you're climbing the charts.\p"
	.string "Call me! Call me any, anytime.\n"
	.string "Comeback tour soon. Be there!\p"
	.string "… … … … … … … … … … … Click!$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "Registered GYM LEADER ROXANNE in the\n"
	.string "POKéNAV.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "ROXANNE: Call me… oh, you did!\p"
	.string "I've been rehearsing my comeback\n"
	.string "tour. Hit me with your best shot!$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "Love is a battlefield.\n"
	.string "I keep losing the battlefield part.$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "ROXANNE: Ain't it fun, living in the\n"
	.string "real world? No. No, it is not.\p"
	.string "Now go, before I sing the whole album.$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "ROXANNE: Call me… oh, you did!\p"
	.string "I've been rehearsing my comeback\n"
	.string "tour. Hit me with your best shot!\p"
	.string "…Only one POKéMON? It takes two, baby.\n"
	.string "Come back with at least two.$"

@ Project Grounded: aanwijzing van het level van de gym-ace (placeholder)
RustboroCity_Gym_Text_GymGuideAceLevel:
	.string "Insider info: the LEADER's ace\n"
	.string "is level 19.\p"
	.string "You didn't hear it from me.\n"
	.string "You heard it from me, but still.$"

RustboroCity_Gym_Text_GymGuideNextAce:
	.string "Next stop: BRAWLY in DEWFORD.\n"
	.string "Their ace is level 23.\p"
	.string "That's all the free advice.\n"
	.string "The rest costs a RARE CANDY.$"
