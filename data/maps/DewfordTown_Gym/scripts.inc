DewfordTown_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, DewfordTown_Gym_OnTransition
	.byte 0

DewfordTown_Gym_OnTransition:
	call DewfordTown_Gym_EventScript_SetFlashLevel
	end

DewfordTown_Gym_EventScript_SetFlashLevel::
	goto_if_defeated TRAINER_BRAWLY_1, DewfordTown_Gym_EventScript_SetLightsOn
	call DewfordTown_Gym_EventScript_CountTrainersDefeated
	copyvar VAR_0x8001, VAR_0x8000
	goto_if_eq VAR_0x8000, 0, DewfordTown_Gym_EventScript_SetFlashLevel7
	goto_if_eq VAR_0x8000, 1, DewfordTown_Gym_EventScript_SetFlashLevel6
	goto_if_eq VAR_0x8000, 2, DewfordTown_Gym_EventScript_SetFlashLevel5
	goto_if_eq VAR_0x8000, 3, DewfordTown_Gym_EventScript_SetFlashLevel4
	goto_if_eq VAR_0x8000, 4, DewfordTown_Gym_EventScript_SetFlashLevel3
	goto_if_eq VAR_0x8000, 5, DewfordTown_Gym_EventScript_SetFlashLevel2
	goto DewfordTown_Gym_EventScript_SetFlashLevel1

DewfordTown_Gym_EventScript_SetLightsOn::
	setflashlevel 0
	return

@ Brightest
DewfordTown_Gym_EventScript_SetFlashLevel1::
	setflashlevel 1
	return

DewfordTown_Gym_EventScript_SetFlashLevel2::
	setflashlevel 2
	return

DewfordTown_Gym_EventScript_SetFlashLevel3::
	setflashlevel 3
	return

DewfordTown_Gym_EventScript_SetFlashLevel4::
	setflashlevel 4
	return

DewfordTown_Gym_EventScript_SetFlashLevel5::
	setflashlevel 5
	return

DewfordTown_Gym_EventScript_SetFlashLevel6::
	setflashlevel 6
	return

@ Darkest
DewfordTown_Gym_EventScript_SetFlashLevel7::
	setflashlevel 7
	return

DewfordTown_Gym_EventScript_BrightenRoom::
	call DewfordTown_Gym_EventScript_CountTrainersDefeated
	nop1
	goto_if_eq VAR_0x8000, VAR_0x8001, DewfordTown_Gym_EventScript_NoLightChange
	copyvar VAR_0x8001, VAR_0x8000
	goto_if_eq VAR_0x8000, 1, DewfordTown_Gym_EventScript_AnimateFlash1Trainer
	goto_if_eq VAR_0x8000, 2, DewfordTown_Gym_EventScript_AnimateFlash2Trainers
	goto_if_eq VAR_0x8000, 3, DewfordTown_Gym_EventScript_AnimateFlash3Trainers
	goto_if_eq VAR_0x8000, 4, DewfordTown_Gym_EventScript_AnimateFlash4Trainers
	goto_if_eq VAR_0x8000, 5, DewfordTown_Gym_EventScript_AnimateFlash5Trainers
	goto_if_eq VAR_0x8000, 6, DewfordTown_Gym_EventScript_AnimateFlash6Trainers

DewfordTown_Gym_EventScript_NoLightChange::
	return

@ NOTE: A little confusingly, a larger animateflash param value is a smaller flash radius
DewfordTown_Gym_EventScript_AnimateFlash1Trainer::
	playse SE_SWITCH
	animateflash 6
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlash2Trainers::
	playse SE_SWITCH
	animateflash 5
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlash3Trainers::
	playse SE_SWITCH
	animateflash 4
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlash4Trainers::
	playse SE_SWITCH
	animateflash 3
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlash5Trainers::
	playse SE_SWITCH
	animateflash 2
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlash6Trainers::
	playse SE_SWITCH
	animateflash 1
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_AnimateFlashFullBrightness::
	playse SE_SWITCH
	animateflash 0
	call DewfordTown_Gym_EventScript_SetFlashLevel
	return

DewfordTown_Gym_EventScript_CountTrainersDefeated::
	setvar VAR_0x8000, 0
	goto_if_not_defeated TRAINER_TAKAO, DewfordTown_Gym_EventScript_CheckJocelyn
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_CheckJocelyn::
	goto_if_not_defeated TRAINER_JOCELYN, DewfordTown_Gym_EventScript_CheckLaura
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_CheckLaura::
	goto_if_not_defeated TRAINER_LAURA, DewfordTown_Gym_EventScript_CheckBrenden
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_CheckBrenden::
	goto_if_not_defeated TRAINER_BRENDEN, DewfordTown_Gym_EventScript_CheckCristian
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_CheckCristian::
	goto_if_not_defeated TRAINER_CRISTIAN, DewfordTown_Gym_EventScript_CheckLilith
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_CheckLilith::
	goto_if_not_defeated TRAINER_LILITH, DewfordTown_Gym_EventScript_StopCountingTrainers
	addvar VAR_0x8000, 1
DewfordTown_Gym_EventScript_StopCountingTrainers::
	return

DewfordTown_Gym_EventScript_Brawly::
	trainerbattle_single TRAINER_BRAWLY_1, DewfordTown_Gym_Text_BrawlyIntro, DewfordTown_Gym_Text_BrawlyDefeat, DewfordTown_Gym_EventScript_BrawlyDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, DewfordTown_Gym_EventScript_BrawlyRematch
	goto_if_unset FLAG_RECEIVED_TM_BULK_UP, DewfordTown_Gym_EventScript_GiveBulkUp2
	msgbox DewfordTown_Gym_Text_BrawlyPostBattle, MSGBOX_DEFAULT
	release
	end

DewfordTown_Gym_EventScript_BrawlyDefeated::
	call DewfordTown_Gym_EventScript_AnimateFlashFullBrightness
	message DewfordTown_Gym_Text_ReceivedKnuckleBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox DewfordTown_Gym_Text_KnuckleBadgeInfoTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_DEWFORD_GYM
	setflag FLAG_BADGE02_GET
	addvar VAR_PETALBURG_GYM_STATE, 1
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	setvar VAR_0x8008, 2
	call Common_EventScript_SetGymTrainers
	call DewfordTown_Gym_EventScript_GiveBulkUp
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox DewfordTown_Gym_Text_RegisteredBrawly, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_BRAWLY_MATCH_CALL
	setvar VAR_ROXANNE_CALL_STEP_COUNTER, 0
	setflag FLAG_ENABLE_ROXANNE_FIRST_CALL
	release
	end

DewfordTown_Gym_EventScript_GiveBulkUp::
	giveitem ITEM_TM_DRAIN_PUNCH
	goto_if_eq VAR_RESULT, 0, Common_EventScript_BagIsFull
	msgbox DewfordTown_Gym_Text_ExplainBulkUp, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_BULK_UP
	return

DewfordTown_Gym_EventScript_GiveBulkUp2:
	giveitem ITEM_TM_DRAIN_PUNCH
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
	msgbox DewfordTown_Gym_Text_ExplainBulkUp, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_BULK_UP
	release
	end

DewfordTown_Gym_EventScript_BrawlyRematch::
	trainerbattle_rematch_double TRAINER_BRAWLY_1, DewfordTown_Gym_Text_BrawlyPreRematch, DewfordTown_Gym_Text_BrawlyRematchDefeat, DewfordTown_Gym_Text_BrawlyRematchNeedTwoMons
	msgbox DewfordTown_Gym_Text_BrawlyPostRematch, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_Takao::
	trainerbattle_single TRAINER_TAKAO, DewfordTown_Gym_Text_TakaoIntro, DewfordTown_Gym_Text_TakaoDefeat, DewfordTown_Gym_EventScript_TakaoBrightenRoom
	msgbox DewfordTown_Gym_Text_TakaoPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_TakaoBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_Jocelyn::
	trainerbattle_single TRAINER_JOCELYN, DewfordTown_Gym_Text_JocelynIntro, DewfordTown_Gym_Text_JocelynDefeat, DewfordTown_Gym_EventScript_JocelynBrightenRoom
	msgbox DewfordTown_Gym_Text_JocelynPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_JocelynBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_Laura::
	trainerbattle_single TRAINER_LAURA, DewfordTown_Gym_Text_LauraIntro, DewfordTown_Gym_Text_LauraDefeat, DewfordTown_Gym_EventScript_LauraBrightenRoom
	msgbox DewfordTown_Gym_Text_LauraPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_LauraBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_Brenden::
	trainerbattle_single TRAINER_BRENDEN, DewfordTown_Gym_Text_BrendenIntro, DewfordTown_Gym_Text_BrendenDefeat, DewfordTown_Gym_EventScript_BrendenBrightenRoom
	msgbox DewfordTown_Gym_Text_BrendenPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_BrendenBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_Cristian::
	trainerbattle_single TRAINER_CRISTIAN, DewfordTown_Gym_Text_CristianIntro, DewfordTown_Gym_Text_CristianDefeat, DewfordTown_Gym_EventScript_CristianBrightenRoom
	msgbox DewfordTown_Gym_Text_CristianPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_CristianBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_Lilith::
	trainerbattle_single TRAINER_LILITH, DewfordTown_Gym_Text_LilithIntro, DewfordTown_Gym_Text_LilithDefeat, DewfordTown_Gym_EventScript_LilithBrightenRoom
	msgbox DewfordTown_Gym_Text_LilithPostBattle, MSGBOX_AUTOCLOSE
	end

DewfordTown_Gym_EventScript_LilithBrightenRoom::
	call DewfordTown_Gym_EventScript_BrightenRoom
	release
	end

DewfordTown_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_DEWFORD_GYM, DewfordTown_Gym_EventScript_GymGuidePostVictory
	msgbox DewfordTown_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

DewfordTown_Gym_EventScript_GymGuidePostVictory::
	msgbox DewfordTown_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

DewfordTown_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE02_GET, DewfordTown_Gym_EventScript_GymStatueCertified
	goto DewfordTown_Gym_EventScript_GymStatue
	end

DewfordTown_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE02_GET, DewfordTown_Gym_EventScript_GymStatueCertified
	goto DewfordTown_Gym_EventScript_GymStatue
	end

DewfordTown_Gym_EventScript_GymStatueCertified::
	msgbox DewfordTown_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Gym_EventScript_GymStatue::
	msgbox DewfordTown_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

DewfordTown_Gym_Text_GymGuideAdvice:
	.string "Listen kid, let me ask you something:\n"
	.string "Do you wanna be a fucking fighter?\p"
	.string "BRAWLY is a savage. He’s got that\n"
	.string "look in his eyes, like Chuck Liddell\l"
	.string "about to send someone to the shadow\l"
	.string "realm with an overhand right!\p"
	.string "If you go in there with NORMAL-types,\n"
	.string "you're getting starched. Period.\l"
	.string "It’s a mismatch, kid.\p"
	.string "The Gym is dark? Cry me a river.\n"
	.string "This isn't a career, it's an\l"
	.string "opportunity!\p"
	.string "You see CONOR out there? He fights\n"
	.string "anyone, anywhere. Isn't he fucking\l"
	.string "awesome?\p"
	.string "Beat those bums in the dark and the\n"
	.string "lights will come on. Now get in\l"
	.string "there and show me something!$"

DewfordTown_Gym_Text_GymGuidePostVictory:
	.string "Holy shit, kid! It's bright in here!\p"
	.string "You went out there and you showed me\n"
	.string "something. Your future is bright!\p"
	.string "Don't even ask for that 50k bonus,\n"
	.string "though. We're not doing that tonight.\p"
	.string "But seriously... isn't this kid\n"
	.string "fucking awesome?$"

DewfordTown_Gym_Text_TakaoIntro:
	.string "I want to outlive my children!\n"
	.string "I'm training six days a week...\p"
	.string "Five days a week I'll train three\n"
	.string "days a week! Come on!$"

DewfordTown_Gym_Text_TakaoDefeat:
	.string "I'm an old lion, and you're just\n"
	.string "a jackal with a cheese plate...$"

DewfordTown_Gym_Text_TakaoPostBattle:
	.string "You're reaching for those grapes...\n"
	.string "and the wine is sounding like\l"
	.string "a violin with that cheese.\p"
	.string "My technique is commendable,\n"
	.string "but your skill is outliving me!$"

DewfordTown_Gym_Text_JocelynIntro:
	.string "Muhammad the best defense, in the\n"
	.string "heavyweight, the best move, in the\l"
	.string "heavyweight...\p"
	.string "But short man, diddy boxin'!$"

DewfordTown_Gym_Text_JocelynDefeat:
	.string "Everything is possible in you life,\n"
	.string "when you believe!$"

DewfordTown_Gym_Text_JocelynPostBattle:
	.string "You have two hands.\n"
	.string "Everything is possible.\p"
	.string "Go. Go. And take it,\n"
	.string "whatever you want to do.$"

DewfordTown_Gym_Text_LauraIntro:
	.string "Who the f--- is that guy?!\p"
	.string "It's red panty night, kid!\n"
	.string "Because you're fighting the double\l"
	.string "champ, I'll change your bum life!$"

DewfordTown_Gym_Text_LauraDefeat:
	.string "My foot was a balloon!\n"
	.string "Doctor's stoppage! Doctor's stoppage!$"

DewfordTown_Gym_Text_LauraPostBattle:
	.string "I was winning that exchange! I was\n"
	.string "inefficient with my energy, and you\l"
	.string "were just sniffing my jock!\p"
	.string "I’d like to take this chance to\n"
	.string "apologize... TO ABSOLUTELY NOBODY!\p"
	.string "There were stress fractures in my\n"
	.string "leg before I even walked in here!\l"
	.string "This isn't over!$"

DewfordTown_Gym_Text_LilithIntro:
	.string "Jamie, pull up that video of the\n"
	.string "MACHOP fighting an URSARING!\p"
	.string "Look at the vascularity! Look, if there\n"
	.string "were as many AIPOM as humans, it's\l"
	.string "chaaaoooss! You could never leave your\l"
	.string "house. They'd eat babies and rip\l"
	.string "your dick off!$"

DewfordTown_Gym_Text_LilithDefeat:
	.string "OHHH! UNBELIEVABLE! A MASSIVE\n"
	.string "HEADKICK! HE'S OUT!$"

DewfordTown_Gym_Text_LilithPostBattle:
	.string "If you don't think MANKEY will steal\n"
	.string "babies and eat them, you haven't\l"
	.string "been paying attention to the\l"
	.string "literature.$"

DewfordTown_Gym_Text_BrendenIntro:
	.string "Look, he's trying to hit me with\n"
	.string "a move! DANGADA-DANGADA-DANG!\p"
	.string "I'm going to grab his head and...\n"
	.string "knee to the face! LIVER SHOT!$"

DewfordTown_Gym_Text_BrendenDefeat:
	.string "I'm sorry, sir! I'm sorry!\n"
	.string "DANG! Look at my liver!$"

DewfordTown_Gym_Text_BrendenPostBattle:
	.string "Always watch the liver. You're worthy\n"
	.string "of seeing the LEADER.\p"
	.string "But never try that again, or I'll\n"
	.string "have to break your leg. Party over!$"

DewfordTown_Gym_Text_CristianIntro:
	.string "I will do a home invasion on you,\n"
	.string "cut the power to your house, climb\l"
	.string "your stairs with night vision goggles\l"
	.string "I got in Soldier of Fortune...\p"
	.string "Catch you in bed with the NOGUEIRA\n"
	.string "brothers practicing 'jiu-jitsu'...\l"
	.string "Post the video on\l"
	.string "www.dorksfrombrazil.com...\p"
	.string "Username NOT REQUIRED, password\n"
	.string "NOT REQUIRED! That's how you\l"
	.string "threaten someone, dummy!$"

DewfordTown_Gym_Text_CristianDefeat:
	.string "I can't let you get close!$"

DewfordTown_Gym_Text_CristianPostBattle:
	.string "I thought if you tapped out, you\n"
	.string "lost the round. Come to find out,\l"
	.string "you actually lose the fight.\p"
	.string "I am still the undefeated,\n"
	.string "undisputed champion. Never lost\l"
	.string "a round. I pick fights.\p"
	.string "I'm better than JONES. I'm better\n"
	.string "than SEAN COMBS. I am even better\l"
	.string "than JOHN HOLMES.$"

DewfordTown_Gym_Text_BrawlyIntro:
	.string "I'm BRAWLY! I run this absolute\n"
	.string "asylum. You've fought my lions,\l"
	.string "my goons, and my podcast hosts...\p"
	.string "But you haven't seen anything yet.\n"
	.string "I've been churned in the rough waves\l"
	.string "of the underground circuit.\p"
	.string "You want to be a star? You want the\n"
	.string "lights? Let me see if you're worth\l"
	.string "the contract!$"

DewfordTown_Gym_Text_BrawlyDefeat:
	.string "Whoah, wow! You've got that\n"
	.string "unhinged energy I like!\p"
	.string "You made a bigger splash than\n"
	.string "a Tito Ortiz sentence!\p"
	.string "Okay, you've got me. You're the\n"
	.string "new A-side. Take this BADGE!$"

DewfordTown_Gym_Text_ReceivedKnuckleBadge:
	.string "{PLAYER} received the KNUCKLE BADGE\n"
	.string "from BRAWLY.$"

DewfordTown_Gym_Text_KnuckleBadgeInfoTakeThis:
	.string "The KNUCKLE BADGE is your ticket to\n"
	.string "the big leagues. It's a symbol of\l"
	.string "power in this gutter we call a circuit.\p"
	.string "With this, you'll be able to use\n"
	.string "FLASH to light up the dark holes\l"
	.string "where guys like ROGAN hide.\p"
	.string "And take this TECHNICAL MACHINE,\n"
	.string "too. It’s for winners only.$"

DewfordTown_Gym_Text_ExplainBulkUp:
	.string "That TM01 contains DRAIN PUNCH.\p"
	.string "It's the ultimate 'take what's mine'\n"
	.string "move. You hit 'em hard, and you\l"
	.string "suck the life force right out of\l"
	.string "their lungs to heal yourself.\p"
	.string "Pure violence. Just how I like it.\p"
	.string "… … … … … …$"

DewfordTown_Gym_Text_RegisteredBrawly:
	.string "Registered GYM LEADER BRAWLY\n"
	.string "in the POKéNAV.$"

DewfordTown_Gym_Text_BrawlyPostBattle:
	.string "I can see your talent becoming a\n"
	.string "storm of astonishment. You're going\l"
	.string "to be a problem for the LEAGUE.\p"
	.string "Now get out of my sight before I\n"
	.string "change my mind about the contract.$"

DewfordTown_Gym_Text_GymStatue:
	.string "DEWFORD TOWN POKéMON GYM$"

DewfordTown_Gym_Text_GymStatueCertified:
	.string "DEWFORD TOWN POKéMON GYM\p"
	.string "BRAWLY'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

DewfordTown_Gym_Text_BrawlyPreRematch:
	.string "BRAWLY: A real fucking fighter always\n"
	.string "comes back! You know the UFC gives a\l"
	.string "lot of rematches, so you'll get mine as\l"
	.string "well!$"

DewfordTown_Gym_Text_BrawlyRematchDefeat:
	.string "Ouch, really!$"

DewfordTown_Gym_Text_BrawlyPostRematch:
	.string "BRAWLY: MMAth would've predicted this\n"
	.string "loss!$"

DewfordTown_Gym_Text_BrawlyRematchNeedTwoMons:
	.string "BRAWLY: Do you want a rematch? I do, we\n"
	.string "can promote it!$"
