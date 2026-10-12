LavaridgeTown_Gym_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavaridgeTown_Gym_1F_OnTransition
	.byte 0

LavaridgeTown_Gym_1F_OnTransition:
	call LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars
	call LavaridgeTown_Gym_1F_EventScript_CheckBuryTrainers
	end

@ Unclear where/if these temp vars are getting checked
LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars::
	setvar VAR_TEMP_B, 0
	setvar VAR_TEMP_C, 0
	setvar VAR_TEMP_D, 0
	setvar VAR_TEMP_E, 0
	setvar VAR_TEMP_F, 0
	goto_if_defeated TRAINER_COLE, LavaridgeTown_Gym_1F_EventScript_SetGeraldTempVar
	setvar VAR_TEMP_B, 1
LavaridgeTown_Gym_1F_EventScript_SetGeraldTempVar::
	goto_if_defeated TRAINER_GERALD, LavaridgeTown_Gym_1F_EventScript_SetAxleTempVar
	setvar VAR_TEMP_C, 1
LavaridgeTown_Gym_1F_EventScript_SetAxleTempVar::
	goto_if_defeated TRAINER_AXLE, LavaridgeTown_Gym_1F_EventScript_SetDanielleTempVar
	setvar VAR_TEMP_D, 1
LavaridgeTown_Gym_1F_EventScript_SetDanielleTempVar::
	goto_if_defeated TRAINER_DANIELLE, LavaridgeTown_Gym_1F_EventScript_EndSetTrainerTempVars
	setvar VAR_TEMP_E, 1
LavaridgeTown_Gym_1F_EventScript_EndSetTrainerTempVars::
	return

LavaridgeTown_Gym_1F_EventScript_CheckBuryTrainers::
	goto_if_defeated TRAINER_COLE, LavaridgeTown_Gym_1F_EventScript_CheckBuryGerald
	setobjectmovementtype LOCALID_COLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryGerald::
	goto_if_defeated TRAINER_GERALD, LavaridgeTown_Gym_1F_EventScript_CheckBuryAxle
	setobjectmovementtype LOCALID_GERALD, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryAxle::
	goto_if_defeated TRAINER_AXLE, LavaridgeTown_Gym_1F_EventScript_CheckBuryDanielle
	setobjectmovementtype LOCALID_AXLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_CheckBuryDanielle::
	goto_if_defeated TRAINER_DANIELLE, LavaridgeTown_Gym_1F_EventScript_EndCheckBuryTrainers
	setobjectmovementtype LOCALID_DANIELLE, MOVEMENT_TYPE_BURIED
LavaridgeTown_Gym_1F_EventScript_EndCheckBuryTrainers::
	return

LavaridgeTown_Gym_1F_EventScript_Flannery::
	trainerbattle_single TRAINER_FLANNERY_1, LavaridgeTown_Gym_1F_Text_FlanneryIntro, LavaridgeTown_Gym_1F_Text_FlanneryDefeat, LavaridgeTown_Gym_1F_EventScript_FlanneryDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, LavaridgeTown_Gym_1F_EventScript_FlanneryRematch
	goto_if_unset FLAG_RECEIVED_TM_OVERHEAT, LavaridgeTown_Gym_1F_EventScript_GiveOverheat2
	msgbox LavaridgeTown_Gym_1F_Text_FlanneryPostBattle, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_FlanneryDefeated::
	message LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox LavaridgeTown_Gym_1F_Text_ExplainHeatBadgeTakeThis, MSGBOX_DEFAULT
	setflag FLAG_WHITEOUT_TO_LAVARIDGE
	setflag FLAG_DEFEATED_LAVARIDGE_GYM
	setflag FLAG_BADGE04_GET
	addvar VAR_PETALBURG_GYM_STATE, 1
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	setvar VAR_0x8008, 4
	call Common_EventScript_SetGymTrainers
	setflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLY
	setvar VAR_LAVARIDGE_TOWN_STATE, 1
	call LavaridgeTown_Gym_1F_EventScript_GiveOverheat
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox LavaridgeTown_Gym_1F_Text_RegisteredFlannery, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_FLANNERY_MATCH_CALL
	release
	end

LavaridgeTown_Gym_1F_EventScript_GiveOverheat2::
	giveitem ITEM_TM_OVERHEAT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox LavaridgeTown_Gym_1F_Text_ExplainOverheat, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_OVERHEAT
	release
	end

LavaridgeTown_Gym_1F_EventScript_GiveOverheat::
	giveitem ITEM_TM_OVERHEAT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox LavaridgeTown_Gym_1F_Text_ExplainOverheat, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_OVERHEAT
	return

LavaridgeTown_Gym_1F_EventScript_FlanneryRematch::
	trainerbattle_rematch_double TRAINER_FLANNERY_1, LavaridgeTown_Gym_1F_Text_FlanneryPreRematch, LavaridgeTown_Gym_1F_Text_FlanneryRematchDefeat, LavaridgeTown_Gym_1F_Text_FlanneryRematchNeedTwoMons
	msgbox LavaridgeTown_Gym_1F_Text_FlanneryPostRematch, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Cole::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_COLE, TRAINER_COLE, LavaridgeTown_Gym_1F_Text_ColeIntro, LavaridgeTown_Gym_1F_Text_ColeDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_1F_Text_ColePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_EventScript_CheckTrainerScript::
	call LavaridgeTown_Gym_1F_EventScript_SetTrainerTempVars
	release
	special ShouldTryGetTrainerScript
	goto_if_eq VAR_RESULT, 1, EventScript_GotoTrainerScript
	end

LavaridgeTown_Gym_1F_EventScript_Axle::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_AXLE, TRAINER_AXLE, LavaridgeTown_Gym_1F_Text_AxleIntro, LavaridgeTown_Gym_1F_Text_AxleDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_1F_Text_AxlePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Keegan::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_KEEGAN, TRAINER_KEEGAN, LavaridgeTown_Gym_B1F_Text_KeeganIntro, LavaridgeTown_Gym_B1F_Text_KeeganDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_B1F_Text_KeeganPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Danielle::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_DANIELLE, TRAINER_DANIELLE, LavaridgeTown_Gym_1F_Text_DanielleIntro, LavaridgeTown_Gym_1F_Text_DanielleDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_1F_Text_DaniellePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_Gerald::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_GERALD, TRAINER_GERALD, LavaridgeTown_Gym_1F_Text_GeraldIntro, LavaridgeTown_Gym_1F_Text_GeraldDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_1F_Text_GeraldPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Jace::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_JACE, TRAINER_JACE, LavaridgeTown_Gym_B1F_Text_JaceIntro, LavaridgeTown_Gym_B1F_Text_JaceDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_B1F_Text_JacePostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Jeff::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_JEFF, TRAINER_JEFF, LavaridgeTown_Gym_B1F_Text_JeffIntro, LavaridgeTown_Gym_B1F_Text_JeffDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_B1F_Text_JeffPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_B1F_EventScript_Eli::
	trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, LOCALID_ELI, TRAINER_ELI, LavaridgeTown_Gym_B1F_Text_EliIntro, LavaridgeTown_Gym_B1F_Text_EliDefeat, LavaridgeTown_Gym_EventScript_CheckTrainerScript, OBJ_ID_NONE, TRAINER_NONE, NULL, NULL, NULL, NULL, NULL, FALSE, TRUE, FALSE, FALSE
	msgbox LavaridgeTown_Gym_B1F_Text_EliPostBattle, MSGBOX_AUTOCLOSE
	end

LavaridgeTown_Gym_1F_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_LAVARIDGE_GYM, LavaridgeTown_Gym_1F_EventScript_GymGuidePostVictory
	msgbox LavaridgeTown_Gym_1F_Text_GymGuideAdvice, MSGBOX_DEFAULT
	msgbox LavaridgeTown_Gym_1F_Text_GymGuideAceLevel, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_GymGuidePostVictory::
	msgbox LavaridgeTown_Gym_1F_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	msgbox LavaridgeTown_Gym_1F_Text_GymGuideNextAce, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_Gym_1F_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, LavaridgeTown_Gym_1F_EventScript_GymStatueCertified
	goto LavaridgeTown_Gym_1F_EventScript_GymStatue
	end

LavaridgeTown_Gym_1F_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, LavaridgeTown_Gym_1F_EventScript_GymStatueCertified
	goto LavaridgeTown_Gym_1F_EventScript_GymStatue
	end

LavaridgeTown_Gym_1F_EventScript_GymStatueCertified::
	msgbox LavaridgeTown_Gym_1F_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

LavaridgeTown_Gym_1F_EventScript_GymStatue::
	msgbox LavaridgeTown_Gym_1F_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

LavaridgeTown_Gym_1F_Text_GymGuideAdvice:
	.string "Hey, how's it going, CHAMPION-\n"
	.string "bound {PLAYER}?\p"
	.string "LAVARIDGE's GYM LEADER FLANNERY\n"
	.string "uses FIRE-type POKéMON.\p"
	.string "Finally! A place where nobody is\n"
	.string "vlogging or talking about crypto!\p"
	.string "These people are hardcore outdoors\n"
	.string "freaks. If it doesn't involve wool\l"
	.string "socks or cast-iron pans, they don't\l"
	.string "want to hear it.\p"
	.string "Don't get too close to her--you'll burn!\n"
	.string "Hose her down with water and then\l"
	.string "go for it!\p"
	.string "And for the love of ARCEUS, put\n"
	.string "your phone on silent before they\l"
	.string "throw it into the volcano!$"

LavaridgeTown_Gym_1F_Text_GymGuidePostVictory:
	.string "Yow! That was a scorching-hot battle!\p"
	.string "Pure, analog skill! No algorithms,\n"
	.string "just raw heat!$"

LavaridgeTown_Gym_1F_Text_ColeIntro:
	.string "Owowowowow!\n"
	.string "Yikes, it's hot! It's BURNING!\p"
	.string "Don't you just love how the heat\n"
	.string "strips away your dignity?\l"
	.string "Come on! Make it sting!$"

LavaridgeTown_Gym_1F_Text_ColeDefeat:
	.string "YES! I'm blinded by sweat and defeat!\n"
	.string "The agony is… exquisite!$"

LavaridgeTown_Gym_1F_Text_ColePostBattle:
	.string "Being buried in scorching sand\n"
	.string "promotes circulation through pain.\p"
	.string "If your joints don't scream, you\n"
	.string "aren't truly living. You should\l"
	.string "try sleeping on a bed of nettles\l"
	.string "next. It's life-changing!$"

LavaridgeTown_Gym_1F_Text_AxleIntro:
	.string "I am on year ten of my digital detox!\n"
	.string "Don't bring your 5G signals over here\l"
	.string "and stress me out!\p"
	.string "I can smell the lithium in your pocket!\n"
	.string "Begone, screen-breather!$"

LavaridgeTown_Gym_1F_Text_AxleDefeat:
	.string "My chakras are misaligned!\n"
	.string "I hope FLANNERY flames you good!$"

LavaridgeTown_Gym_1F_Text_AxlePostBattle:
	.string "Haaah… Whew…\p"
	.string "If you spend too much time buried in\n"
	.string "hot sand, it tuckers you out…\p"
	.string "But at least the sand doesn't try\n"
	.string "to show me targeted ads or political\l"
	.string "takes from people I don't know.$"

LavaridgeTown_Gym_B1F_Text_KeeganIntro:
	.string "You must be getting tired by now.\n"
	.string "Forget the sand... you look like\l"
	.string "you need a steak seared in butter.\p"
	.string "Maintaining your willpower is key,\n"
	.string "but so is high-quality animal fat.\l"
	.string "No seed oils in this Gym, kid!$"

LavaridgeTown_Gym_B1F_Text_KeeganDefeat:
	.string "Too much heat in the pan...\n"
	.string "Play with fire, and be burned.$"

LavaridgeTown_Gym_B1F_Text_KeeganPostBattle:
	.string "Your skill is real… like a perfectly\n"
	.string "rested ribeye.\p"
	.string "But FLANNERY? She's a different kind\n"
	.string "of heat. If you don't watch yourself,\l"
	.string "she'll char you to a crisp.\p"
	.string "Now move along, my tallow is\n"
	.string "reaching its smoke point.$"

LavaridgeTown_Gym_1F_Text_GeraldIntro:
	.string "Can your POKéMON withstand\n"
	.string "392-degree heat?\p"
	.string "Nothing clears the pores like raw\n"
	.string "volcanic sulfur! It's nature's\l"
	.string "cologne, kid!$"

LavaridgeTown_Gym_1F_Text_GeraldDefeat:
	.string "My skin is glowing, but my\n"
	.string "team didn't burn hotly enough…$"

LavaridgeTown_Gym_1F_Text_GeraldPostBattle:
	.string "The temperature of magma is\n"
	.string "392 degrees. It's the perfect soak.\p"
	.string "I spend ten hours a day in the\n"
	.string "hot springs until I'm basically\l"
	.string "boiled. You should try it.\p"
	.string "If you can survive 392 degrees,\n"
	.string "you don't need a smartphone to\l"
	.string "feel 'connected' to the world.$"

LavaridgeTown_Gym_1F_Text_DanielleIntro:
	.string "Um… Okay, I'll battle with you.\n"
	.string "But make it quick, my canned pea\l"
	.string "soup is almost lukewarm!$"

LavaridgeTown_Gym_1F_Text_DanielleDefeat:
	.string "Oh, but you're too strong…\n"
	.string "Almost as strong as the smell of\l"
	.string "my chemical toilet.$"

LavaridgeTown_Gym_1F_Text_DaniellePostBattle:
	.string "I'm going to be a pretty and strong\n"
	.string "TRAINER just like FLANNERY.\p"
	.string "My dream is to buy a classic camper\n"
	.string "and drive from one site to the next.\p"
	.string "KALOS, PALDEA, KANTO... it doesn't\n"
	.string "matter where we are, as long as\l"
	.string "I'm in my folding chair staring\l"
	.string "at a grey hedge. How quaint!$"

LavaridgeTown_Gym_B1F_Text_JaceIntro:
	.string "Come on, get with it!\p"
	.string "I’ve been rubbing these sticks for\n"
	.string "hours! My hands are bleeding, but\l"
	.string "the fire is ALIVE!\p"
	.string "Battle me before the embers die!$"

LavaridgeTown_Gym_B1F_Text_JaceDefeat:
	.string "My flame is out… It's so hot, and\n"
	.string "yet my heart is clutched by ice…$"

LavaridgeTown_Gym_B1F_Text_JacePostBattle:
	.string "The way your spirit burns… you\n"
	.string "might actually beat FLANNERY.\p"
	.string "But never trust a man who uses a\n"
	.string "microwave. It's the devil's box!$"

LavaridgeTown_Gym_B1F_Text_JeffIntro:
	.string "See how the flames blaze wildly?\n"
	.string "They’re whispering my name!\p"
	.string "They flare in anticipation of my win!\n"
	.string "Can you hear them too, or is your\l"
	.string "brain just full of WiFi signals?$"

LavaridgeTown_Gym_B1F_Text_JeffDefeat:
	.string "The fire lied to me!\n"
	.string "Something didn't go right...$"

LavaridgeTown_Gym_B1F_Text_JeffPostBattle:
	.string "Well, so what? I say so what?\n"
	.string "I can walk on hot coals barefoot!\p"
	.string "The blisters make me feel closer\n"
	.string "to the earth! Don't try it, kid.\l"
	.string "Your feet are probably too soft\l"
	.string "from wearing 'ergonomic' sneakers!$"

LavaridgeTown_Gym_B1F_Text_EliIntro:
	.string "As much as I love mountains, I\n"
	.string "especially love volcanoes.\p"
	.string "I’ve been hiking for six weeks\n"
	.string "straight. My backpack is my home,\l"
	.string "and my musk is my shield!$"

LavaridgeTown_Gym_B1F_Text_EliDefeat:
	.string "I lost without ever being in control.\n"
	.string "Maybe it’s the lack of electrolytes...$"

LavaridgeTown_Gym_B1F_Text_EliPostBattle:
	.string "I stay here because I became a fan\n"
	.string "of FLANNERY's raw power.\p"
	.string "She doesn't use deodorant either.\n"
	.string "She’s the real deal. Hehehehe.$"

LavaridgeTown_Gym_1F_Text_FlanneryIntro:
	.string "Welcome… No, wait!\p"
	.string "Puny TRAINER, prepare to be scorched\n"
	.string "by the raw, unwashed power of… uh…\l"
	.string "Wait, what did Jace call it? Right!\l"
	.string "The primal embers of the soul!\p"
	.string "I am FLANNERY, and I'm the GYM\n"
	.string "LEADER here! I inherit the skills of\l"
	.string "my grandfather, who never used\l"
	.string "a GPS in his life!\p"
	.string "Dare not underestimate me! We hone\n"
	.string "our moves in the dirt and the sulfur!\l"
	.string "No WiFi! Just analog… uh… heat!\l"
	.string "Prepare to get cooked!$"

LavaridgeTown_Gym_1F_Text_FlanneryDefeat:
	.string "Oh…\n"
	.string "I guess I was trying too hard…\p"
	.string "I… I've only recently become\n"
	.string "a GYM LEADER. And honestly?\l"
	.string "The smell of sulfur is giving me\l"
	.string "a massive headache.\p"
	.string "I tried too hard to impress these\n"
	.string "camping fanatics by acting like\l"
	.string "someone I'm not.\p"
	.string "I have to do things my natural way.\n"
	.string "Thanks for teaching me that.\l"
	.string "For that, you deserve this.$"

LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge:
	.string "{PLAYER} received the HEAT BADGE from\n"
	.string "FLANNERY.\p"
	.string "It smells like sulfur. And patchouli.$"
LavaridgeTown_Gym_1F_Text_ExplainHeatBadgeTakeThis:
	.string "If you have a HEAT BADGE, all POKéMON\n"
	.string "up to Level 50 will obey you.\p"
	.string "It also lets you use STRENGTH out of\n"
	.string "battle. You'll need it to move heavy\l"
	.string "boulders or to haul a literal pile\l"
	.string "of trash out of the woods!\p"
	.string "This is a token of my appreciation.\n"
	.string "Don't be shy about taking it!$"

LavaridgeTown_Gym_1F_Text_ExplainOverheat:
	.string "That TM50 contains OVERHEAT.\p"
	.string "It inflicts serious damage, but it\n"
	.string "sharply cuts your SP. ATK.\p"
	.string "It’s like my WiFi router... it works\n"
	.string "great for five minutes, then it\l"
	.string "overheats and I have to go back to\l"
	.string "staring at the fire. It’s a sign!$"

LavaridgeTown_Gym_1F_Text_RegisteredFlannery:
	.string "Registered GYM LEADER FLANNERY in the\n"
	.string "POKéNAV.\p"
	.string "She said she doesn't use phones. It's\n"
	.string "registered anyway.$"

LavaridgeTown_Gym_1F_Text_FlanneryPostBattle:
	.string "Your power reminds me of someone…\p"
	.string "Oh! I know! You battle like NORMAN\n"
	.string "over in PETALBURG.\p"
	.string "Though it’s hard to believe he's\n"
	.string "still that strong. Last I heard,\l"
	.string "he hasn't left his couch in weeks.\p"
	.string "He’s on his fourth rewatch of some\n"
	.string "show about a Tiger King. Talk about\l"
	.string "a different kind of 'wildlife'...$"

LavaridgeTown_Gym_1F_Text_GymStatue:
	.string "LAVARIDGE TOWN POKéMON GYM\p"
	.string "No WiFi.$"

LavaridgeTown_Gym_1F_Text_GymStatueCertified:
	.string "LAVARIDGE TOWN POKéMON GYM\p"
	.string "FLANNERY'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

LavaridgeTown_Gym_1F_Text_FlanneryPreRematch:
	.string "FLANNERY: No more “primal embers of the\n"
	.string "soul.” I just like POKéMON, battling and\l"
	.string "this GYM.\p"
	.string "And painkillers. Let's go!$"

LavaridgeTown_Gym_1F_Text_FlanneryRematchDefeat:
	.string "Whew! On the verge of a migraine!$"

LavaridgeTown_Gym_1F_Text_FlanneryPostRematch:
	.string "FLANNERY: I lost, but I'm happy.\p"
	.string "Grandpa would say something deep now.\n"
	.string "I'm going to take a nap.$"

LavaridgeTown_Gym_1F_Text_FlanneryRematchNeedTwoMons:
	.string "FLANNERY: No more “primal embers of the\n"
	.string "soul.” I just like POKéMON, battling and\l"
	.string "this GYM.\p"
	.string "And painkillers. Let's go!\p"
	.string "Only one POKéMON? Even Grandpa\n"
	.string "brought two, and he forgets everything.\l"
	.string "Bring at least two.$"

@ Project Grounded: aanwijzing van het level van de gym-ace (placeholder)
LavaridgeTown_Gym_1F_Text_GymGuideAceLevel:
	.string "Insider info: the LEADER's ace\n"
	.string "is level 48.\p"
	.string "You didn't hear it from me.\n"
	.string "You heard it from me, but still.$"

LavaridgeTown_Gym_1F_Text_GymGuideNextAce:
	.string "Next stop: NORMAN in PETALBURG.\n"
	.string "Your dad. His ace is level 49.\p"
	.string "That's all the free advice.\n"
	.string "The rest costs a RARE CANDY.$"
