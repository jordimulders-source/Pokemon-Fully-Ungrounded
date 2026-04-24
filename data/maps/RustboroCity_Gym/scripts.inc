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

RustboroCity_Gym_EventScript_Marc::
	trainerbattle_single TRAINER_MARC, RustboroCity_Gym_Text_MarcIntro, RustboroCity_Gym_Text_MarcDefeat
	msgbox RustboroCity_Gym_Text_MarcPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, RustboroCity_Gym_EventScript_GymGuidePostVictory
	msgbox RustboroCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_GymGuidePostVictory::
	msgbox RustboroCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
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
	.string "The world is full of Kings and Queens\n"
	.string "who'll blind your eyes and steal\l"
	.string "your dreams!\p"
	.string "I am the Iron Man! Feel the weight\n"
	.string "of my heavy metal riffs!$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "The bells have tolled for me...$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "ROXANNE is the true Master of\n"
	.string "Reality. If you're not careful,\l"
	.string "you'll be Paranoid before the\l"
	.string "final solo!$"

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
	.string "I am ROXANNE.\n"
	.string "Listen... I never meant to brag,\l"
	.string "but I've got you where I want you now!\p"
	.string "It was never my intention to steal\n"
	.string "it all away from you... but God,\l"
	.string "does it feel so good!\p"
	.string "I'm burning 'cross the breeze with\n"
	.string "my Rock-types. You'll be spellbound\l"
	.string "by the rag doll dance!\p"
	.string "Off with your head! I'll never break\n"
	.string "the chain of my victories!$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "It's in your head! In your head!\n"
	.string "Zombie... Zombie...\p"
	.string "I'm crazy on you, but you actually\n"
	.string "found a way through the storm.$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "Thunder only happens when it's\n"
	.string "raining... and players only love you\l"
	.string "when they're playing.\p"
	.string "I'll just look at you and fade into\n"
	.string "you. Take the badge and run like\l"
	.string "the wind!$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} received the STONE BADGE\n"
	.string "from ROXANNE.$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "The STONE BADGE heightens the ATTACK\n"
	.string "power of your POKéMON.\p"
	.string "It also enables them to use the HM move\n"
	.string "CUT outside of battle.\p"
	.string "Please... take this with you, too.\n"
	.string "Consider it a souvenir of our dance.$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "That TECHNICAL MACHINE, TM39,\n"
	.string "contains STEALTH ROCK.\p"
	.string "It sets a trap of pointed stones\n"
	.string "around your foes.\p"
	.string "Every time they step onto the stage,\n"
	.string "the rocks will tear them apart.\l"
	.string "It's a misery business, isn't it?\p"
	.string "Remember, a TM can be used only once.\n"
	.string "Don't waste it on a rag doll dance.$"

RustboroCity_Gym_Text_GymStatue:
	.string "RUSTBORO CITY POKéMON GYM$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "RUSTBORO CITY POKéMON GYM\p"
	.string "ROXANNE'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "… … … … … …\n"
	.string "… … … … … Beep!\p"
	.string "ROXANNE: Oh, hello, {PLAYER}?\n"
	.string "This is ROXANNE of RUSTBORO CITY.\p"
	.string "I heard from BRAWLY that you're\n"
	.string "moving up through the ranks of\l"
	.string "TRAINERS at an incredible clip.\p"
	.string "Well, I'd rather not think that\n"
	.string "I can't beat you.\p"
	.string "I promise, I will shape up my GYM\n"
	.string "so that you may challenge us again.\p"
	.string "I hope you'll be looking forward to\n"
	.string "that occasion as much as me!\p"
	.string "… … … … … …\n"
	.string "… … … … … Click!$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "Registered GYM LEADER ROXANNE\n"
	.string "in the POKéNAV.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "ROXANNE: I'm so glad to see you again.\n"
	.string "I'm ROXANNE, the GYM LEADER here.\p"
	.string "I'm sure we've both experienced many\n"
	.string "battles since we last met.\p"
	.string "I would like to see how much better\n"
	.string "we've become. Let us battle!$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "Grr…\n"
	.string "Again, I have lost…$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "ROXANNE: I still have much to learn\n"
	.string "when it comes to battling POKéMON.\p"
	.string "That awareness makes me love battling\n"
	.string "all that much more!$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "ROXANNE: I'm so glad to see you again.\n"
	.string "I'm ROXANNE, the GYM LEADER here.\p"
	.string "I'm sure we've both experienced many\n"
	.string "battles since we last met.\p"
	.string "I would like to see how much better\n"
	.string "we've become…\p"
	.string "Oh, no…\n"
	.string "You only have one POKéMON with you?\p"
	.string "Please return with at least one more\n"
	.string "POKéMON.$"
