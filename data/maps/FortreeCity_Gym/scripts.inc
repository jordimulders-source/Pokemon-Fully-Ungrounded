FortreeCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, FortreeCity_Gym_OnWarp
	.byte 0

FortreeCity_Gym_OnTransition:
	special RotatingGate_InitPuzzle
	setflag FLAG_TEMP_HIDE_FOLLOWER @ Hide follower bc of rotating gates
	end

FortreeCity_Gym_OnWarp:
	map_script_2 VAR_TEMP_0, VAR_TEMP_0, FortreeCity_Gym_EventScript_InitRotatingGates
	.2byte 0

@ NOTE: This rotating gate puzzle makes use of VAR_TEMP_0 - VAR_TEMP_3
FortreeCity_Gym_EventScript_InitRotatingGates::
	special RotatingGate_InitPuzzleAndGraphics
	end

FortreeCity_Gym_EventScript_Winona::
	trainerbattle_single TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaIntro, FortreeCity_Gym_Text_WinonaDefeat, FortreeCity_Gym_EventScript_WinonaDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, FortreeCity_Gym_EventScript_WinonaRematch
	goto_if_unset FLAG_RECEIVED_TM_AERIAL_ACE, FortreeCity_Gym_EventScript_GiveAerialAce2
	msgbox FortreeCity_Gym_Text_WinonaPostBattle, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_WinonaDefeated::
	message FortreeCity_Gym_Text_ReceivedFeatherBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_FORTREE_GYM
	setflag FLAG_BADGE06_GET
	setvar VAR_0x8008, 6
	call Common_EventScript_SetGymTrainers
	call FortreeCity_Gym_EventScript_GiveAerialAce
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox FortreeCity_Gym_Text_RegisteredWinona, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_WINONA_MATCH_CALL
	setvar VAR_SCOTT_FORTREE_CALL_STEP_COUNTER, 0
	setflag FLAG_SCOTT_CALL_FORTREE_GYM
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce2::
	giveitem ITEM_TM_BRAVE_BIRD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce::
	giveitem ITEM_TM_BRAVE_BIRD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	return

FortreeCity_Gym_EventScript_WinonaRematch::
	trainerbattle_rematch_double TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaPreRematch, FortreeCity_Gym_Text_WinonaRematchDefeat, FortreeCity_Gym_Text_WinonaRematchNeedTwoMons
	msgbox FortreeCity_Gym_Text_WinonaPostRematch, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Jared::
	trainerbattle_single TRAINER_JARED, FortreeCity_Gym_Text_JaredIntro, FortreeCity_Gym_Text_JaredDefeat
	msgbox FortreeCity_Gym_Text_JaredPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Edwardo::
	trainerbattle_single TRAINER_EDWARDO, FortreeCity_Gym_Text_EdwardoIntro, FortreeCity_Gym_Text_EdwardoDefeat
	msgbox FortreeCity_Gym_Text_EdwardoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Flint::
	trainerbattle_single TRAINER_FLINT, FortreeCity_Gym_Text_FlintIntro, FortreeCity_Gym_Text_FlintDefeat
	msgbox FortreeCity_Gym_Text_FlintPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Ashley::
	trainerbattle_single TRAINER_ASHLEY, FortreeCity_Gym_Text_AshleyIntro, FortreeCity_Gym_Text_AshleyDefeat
	msgbox FortreeCity_Gym_Text_AshleyPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Humberto::
	trainerbattle_single TRAINER_HUMBERTO, FortreeCity_Gym_Text_HumbertoIntro, FortreeCity_Gym_Text_HumbertoDefeat
	msgbox FortreeCity_Gym_Text_HumbertoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Darius::
	trainerbattle_single TRAINER_DARIUS, FortreeCity_Gym_Text_DariusIntro, FortreeCity_Gym_Text_DariusDefeat
	msgbox FortreeCity_Gym_Text_DariusPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_FORTREE_GYM, FortreeCity_Gym_EventScript_GymGuidePostVictory
	msgbox FortreeCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_GymGuidePostVictory::
	msgbox FortreeCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE06_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE06_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_GymStatueCertified::
	msgbox FortreeCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_EventScript_GymStatue::
	msgbox FortreeCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_Text_GymGuideAdvice:
	.string "Yo, how's it going, CHAMPION-\n"
	.string "bound {PLAYER}?\p"
	.string "Listen, stay close to me. This isn't\n"
	.string "a GYM, it's a budget airline terminal\l"
	.string "during a technical strike!\p"
	.string "WINONA is a master of FLYING-type\n"
	.string "POKéMON, but her trainers are even\l"
	.string "worse... they're frequent flyers!\p"
	.string "Watch out for people trying to put\n"
	.string "oversized SKITTY-carriers in the\l"
	.string "overhead bins. It’s pure chaos!\p"
	.string "She's behind those rotating doors.\n"
	.string "Think of them as security scanners,\l"
	.string "but with more attitude.\p"
	.string "If you want that BADGE, you'll need\n"
	.string "to survive the turbulence! Go!$"

FortreeCity_Gym_Text_GymGuidePostVictory:
	.string "You did it!\n"
	.string "You've achieved liftoff!\p"
	.string "And you didn't even have to pay\n"
	.string "extra for your carry-on luggage!$"

FortreeCity_Gym_Text_JaredIntro:
	.string "Behold the elegant style of travel!\n"
	.string "Wait, let me just find my passport...\p"
	.string "Is it in this bag? No, the other one.\n"
	.string "Hold on, I need to reorganize my\l"
	.string "36 suitcases before we battle!$"

FortreeCity_Gym_Text_JaredDefeat:
	.string "You… You're strong…\n"
	.string "And you travel surprisingly light!$"

FortreeCity_Gym_Text_JaredPostBattle:
	.string "A TRAINER has to be smart to keep\n"
	.string "up with unexpected delays.\p"
	.string "I’ll probably see you at the hotel.\n"
	.string "I’ll be the one checking in right\l"
	.string "before you with a broken zipper.\p"
	.string "Do you have the patience to get to\n"
	.string "our LEADER, or will you lose it in\l"
	.string "the baggage claim?$"

FortreeCity_Gym_Text_EdwardoIntro:
	.string "The lovers of BIRD POKéMON aspire\n"
	.string "to join this GYM.\p"
	.string "Wait! Hold that pose! The lighting\n"
	.string "on your POKéBALL is perfect!\p"
	.string "First, can you take a quick photo\n"
	.string "of me with your POKéMON? The lens is\l"
	.string "just here. Wait, let's take a selfie!$"

FortreeCity_Gym_Text_EdwardoDefeat:
	.string "It was too much of a load for me\n"
	.string "to bear… and I missed the shot!$"

FortreeCity_Gym_Text_EdwardoPostBattle:
	.string "The world is huge, and I have\n"
	.string "17,000 photos of it on my Cloud.\p"
	.string "I’ve never actually looked at them,\n"
	.string "but I need to make sure I document\l"
	.string "every single second I'm here.\p"
	.string "Move aside, please! You're blocking\n"
	.string "my shot of that exit sign!$"

FortreeCity_Gym_Text_FlintIntro:
	.string "There's no need for WINONA, our GYM\n"
	.string "LEADER, to deal with you!\p"
	.string "I’ve followed her flight path across\n"
	.string "three regions in Economy Class!\l"
	.string "My knees are crushed, but my loyalty\l"
	.string "to her is soaring!$"

FortreeCity_Gym_Text_FlintDefeat:
	.string "WINONA, I… I lost!\n"
	.string "And I didn't even get any miles\l"
	.string "for this battle!$"

FortreeCity_Gym_Text_FlintPostBattle:
	.string "WINONA is cute and she's strong.\n"
	.string "She's the ultimate LEADER!\p"
	.string "Blush…\p"
	.string "I spent 14 hours in a middle seat\n"
	.string "just to be here when she lands.\l"
	.string "Worth it! Hehehe…$"

FortreeCity_Gym_Text_AshleyIntro:
	.string "WINONA taught me personally!\n"
	.string "You can't beat me easily!\p"
	.string "I would have been here sooner, but\n"
	.string "I got lost for three hours between\l"
	.string "Gate A and the taxi stand.\l"
	.string "Everything is so overwhelming!$"

FortreeCity_Gym_Text_AshleyDefeat:
	.string "I was beaten…\n"
	.string "I need to go lie down in the hotel\l"
	.string "lobby for a while.$"

FortreeCity_Gym_Text_AshleyPostBattle:
	.string "Thanks to WINONA, the people of\n"
	.string "FORTREE can live without fear.\p"
	.string "Me? I’m still terrified. I found this\n"
	.string "really cute cafe on PokeGram, but\l"
	.string "it's two blocks away... What if I\l"
	.string "take a wrong turn and end up in\l"
	.string "the Safari Zone?$"

FortreeCity_Gym_Text_HumbertoIntro:
	.string "Behold! My masterpiece of flight!\p"
	.string "I built this contraption myself using\n"
	.string "canvas, oak, and pure genius!\l"
	.string "Who needs a plane when you have\l"
	.string "flapping wooden wings?$"

FortreeCity_Gym_Text_HumbertoDefeat:
	.string "Urk!\n"
	.string "My aerodynamics... they failed!$"

FortreeCity_Gym_Text_HumbertoPostBattle:
	.string "You'd better watch it!\n"
	.string "Don't get distracted staring at WINONA\l"
	.string "or you'll go crashing down in a heap!\p"
	.string "People say I look like a guy named\n"
	.string "Leo Da Vinci? Never heard of him.\l"
	.string "Did he fly budget? Did he have a\l"
	.string "frequent flyer card? I doubt it!$"

FortreeCity_Gym_Text_DariusIntro:
	.string "You'd better know that there are all\n"
	.string "sorts of FLYING-type POKéMON.\p"
	.string "But do you know how much protein\n"
	.string "is in a DODUO wing? I do!\p"
	.string "I’m hitting 4,000 calories a day on\n"
	.string "this trip! Bulk season never stops!$"

FortreeCity_Gym_Text_DariusDefeat:
	.string "You seem to know your stuff!\n"
	.string "I think I just burned my entire\l"
	.string "breakfast surplus on that loss...$"

FortreeCity_Gym_Text_DariusPostBattle:
	.string "Sure, you beat me all right.\n"
	.string "But you'd better watch it!\p"
	.string "WINONA's POKéMON are all business.\n"
	.string "Pure muscle and zero body fat!\p"
	.string "Now move, I need to find a buffet.\n"
	.string "My cheeks are empty and my gains\l"
	.string "are fading! I'm wasting away!$"

FortreeCity_Gym_Text_WinonaIntro:
	.string "I am WINONA. LEADER of FORTREE GYM.\p"
	.string "The world sees me as a soaring star,\n"
	.string "always traveling, always elegant…\p"
	.string "But honestly? I'm exhausted. Between\n"
	.string "the jetlag and the fans, I just want\l"
	.string "to retreat to my tree house and\l"
	.string "never come down again.\p"
	.string "And my Gym trainers... Ugh. A stalker,\n"
	.string "a bulk-obsessed gym rat, and a guy\l"
	.string "who thinks he’s a 15th-century genius?\p"
	.string "Please, give me a real challenge so I\n"
	.string "can justify closing early today!\p"
	.string "Witness the elegant choreography\n"
	.string "of BIRD POKéMON and I!$"

FortreeCity_Gym_Text_WinonaDefeat:
	.string "Never before have I seen a TRAINER\n"
	.string "command POKéMON with more grace\l"
	.string "than I…\p"
	.string "Maybe you should take over? I’d give\n"
	.string "anything for a week in my tree house\l"
	.string "without someone asking for a selfie.\p"
	.string "In recognition of your prowess,\n"
	.string "I present to you this GYM BADGE.$"

FortreeCity_Gym_Text_ReceivedFeatherBadge:
	.string "{PLAYER} received the FEATHER BADGE\n"
	.string "from WINONA.$"

FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis:
	.string "With the FEATHER BADGE, all POKéMON up\n"
	.string "to LV 70, even those received through\l"
	.string "trades, will obey your every command.\p"
	.string "You will also be able to use\n"
	.string "the HM move FLY outside of battle.\p"
	.string "Fly wherever you want! Personally,\n"
	.string "I recommend flying to a high tree\l"
	.string "house and pulling up the ladder.\p"
	.string "And this…\n"
	.string "This is a gift from me for dealing\l"
	.string "with my 'frequent flyers'.$"

FortreeCity_Gym_Text_ExplainAerialAce:
	.string "TM40 contains BRAVE BIRD.\p"
	.string "It’s a move that strikes with incredible\n"
	.string "force, but it hurts the user, too.\p"
	.string "It’s the story of my life! Giving the\n"
	.string "public what they want until I’m\l"
	.string "completely exhausted.\l"
	.string "Use it wisely, or you'll burn out\l"
	.string "just like I am!$"

FortreeCity_Gym_Text_RegisteredWinona:
	.string "Registered GYM LEADER WINONA\n"
	.string "in the POKéNAV.$"

FortreeCity_Gym_Text_WinonaPostBattle:
	.string "Though I fell to you, I will remain\n"
	.string "devoted to BIRD POKéMON.\p"
	.string "They don't ask for autographs, they\n"
	.string "don't film me in the lobby, and they\l"
	.string "don't talk about their gains.\l"
	.string "Nature is so much better than fans.$"

FortreeCity_Gym_Text_GymStatue:
	.string "FORTREE CITY POKéMON GYM$"

FortreeCity_Gym_Text_GymStatueCertified:
	.string "FORTREE CITY POKéMON GYM\p"
	.string "WINONA'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

FortreeCity_Gym_Text_WinonaPreRematch:
	.string "WINONA: You again. And you're CHAMPION\n"
	.string "now.\p"
	.string "Great. Maybe the fans will follow you\n"
	.string "for a while. Battle me at full flight so I\l"
	.string "can go home!$"

FortreeCity_Gym_Text_WinonaRematchDefeat:
	.string "I failed to reach your height again…\n"
	.string "Can I go back to my tree house now?$"

FortreeCity_Gym_Text_WinonaPostRematch:
	.string "WINONA: The wings of my heart remain\n"
	.string "unbroken.\p"
	.string "My phone has 400 unread messages,\n"
	.string "though. Goodbye.$"

FortreeCity_Gym_Text_WinonaRematchNeedTwoMons:
	.string "WINONA: You again. And you're CHAMPION\n"
	.string "now.\p"
	.string "Great. Maybe the fans will follow you\n"
	.string "for a while. Battle me at full flight so I\l"
	.string "can go home!\p"
	.string "Only one POKéMON? You climbed all the\n"
	.string "way up here for that? Come back with\l"
	.string "two.$"
