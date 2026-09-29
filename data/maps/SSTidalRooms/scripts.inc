SSTidalRooms_MapScripts::
	.byte 0

SSTidalRooms_EventScript_SnatchGiver::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_SNATCH, SSTidalRooms_EventScript_ExplainSnatch
	msgbox SSTidalRooms_Text_NotSuspiciousTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_PLAY_ROUGH
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_SNATCH
	msgbox SSTidalRooms_Text_ExplainSnatch, MSGBOX_DEFAULT
	release
	end

SSTidalRooms_EventScript_ExplainSnatch::
	msgbox SSTidalRooms_Text_ExplainSnatch, MSGBOX_DEFAULT
	release
	end

SSTidalRooms_EventScript_Bed::
	lockall
	msgbox SSTidalRooms_Text_TakeRestOnBed, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	call SSTidalRooms_EventScript_ProgessCruiseAfterBed
	releaseall
	end

SSTidalRooms_EventScript_Colton::
	trainerbattle_single TRAINER_COLTON, SSTidalRooms_Text_ColtonIntro, SSTidalRooms_Text_ColtonDefeat
	msgbox SSTidalRooms_Text_ColtonPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Micah::
	trainerbattle_single TRAINER_MICAH, SSTidalRooms_Text_MicahIntro, SSTidalRooms_Text_MicahDefeat
	msgbox SSTidalRooms_Text_MicahPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Thomas::
	trainerbattle_single TRAINER_THOMAS, SSTidalRooms_Text_ThomasIntro, SSTidalRooms_Text_ThomasDefeat
	msgbox SSTidalRooms_Text_ThomasPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Jed::
	trainerbattle_double TRAINER_LEA_AND_JED, SSTidalRooms_Text_JedIntro, SSTidalRooms_Text_JedDefeat, SSTidalRooms_Text_JedNotEnoughMons
	msgbox SSTidalRooms_Text_JedPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Lea::
	trainerbattle_double TRAINER_LEA_AND_JED, SSTidalRooms_Text_LeaIntro, SSTidalRooms_Text_LeaDefeat, SSTidalRooms_Text_LeaNotEnoughMons
	msgbox SSTidalRooms_Text_LeaPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Garret::
	trainerbattle_single TRAINER_GARRET, SSTidalRooms_Text_GarretIntro, SSTidalRooms_Text_GarretDefeat
	msgbox SSTidalRooms_Text_GarretPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_EventScript_Naomi::
	trainerbattle_single TRAINER_NAOMI, SSTidalRooms_Text_NaomiIntro, SSTidalRooms_Text_NaomiDefeat
	msgbox SSTidalRooms_Text_NaomiPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalRooms_Text_TakeRestOnBed:
	.string "There's a bed…\n"
	.string "Let's take a rest.$"

SSTidalRooms_Text_ColtonIntro:
	.string "I often sail to LILYCOVE for the\n"
	.string "CONTESTS.\p"
	.string "With my five SKITTY. And my DELCATTY.\n"
	.string "She's the mother.$"

SSTidalRooms_Text_ColtonDefeat:
	.string "That was an enjoyable match!$"

SSTidalRooms_Text_ColtonPostBattle:
	.string "I get so excited about the next\n"
	.string "CONTEST!\p"
	.string "My cats do too. They're wearing\n"
	.string "matching bows.$"

SSTidalRooms_Text_MicahIntro:
	.string "Are your friends strong?$"

SSTidalRooms_Text_MicahDefeat:
	.string "Your friends are, indeed, strong.$"

SSTidalRooms_Text_MicahPostBattle:
	.string "Friends need not be human.\p"
	.string "My POKéMON are my only friends. By\n"
	.string "choice. Mostly.$"

SSTidalRooms_Text_ThomasIntro:
	.string "Child… I see that you raise POKéMON\n"
	.string "with utmost care.\p"
	.string "A child like you would never understand\n"
	.string "what I hope to achieve.$"

SSTidalRooms_Text_ThomasDefeat:
	.string "…I'm not GIOVANNI, by the way. I just\n"
	.string "watch a lot of mafia shows. THE\l"
	.string "SOPRANOS. Four times.$"

SSTidalRooms_Text_ThomasPostBattle:
	.string "To never be ruffled is the GENTLEMAN's\n"
	.string "code.\p"
	.string "Also TONY SOPRANO's. Different results.$"

SSTidalRooms_Text_JedIntro:
	.string "JED: This is a bit embarrassing, but…\p"
	.string "Behold our lovey-dovey power!$"

SSTidalRooms_Text_JedDefeat:
	.string "JED: Sigh…$"

SSTidalRooms_Text_JedPostBattle:
	.string "JED: Our lovey-dovey power failed for\n"
	.string "the first time!\p"
	.string "It's our honeymoon. Great start.$"

SSTidalRooms_Text_JedNotEnoughMons:
	.string "JED: Only one POKéMON? Isn't that\n"
	.string "lonely?\p"
	.string "Get a partner. Like us.$"

SSTidalRooms_Text_LeaIntro:
	.string "LEA: I feel silly, but…\p"
	.string "Behold our lovey-dovey power!$"

SSTidalRooms_Text_LeaDefeat:
	.string "LEA: Oh, boo!$"

SSTidalRooms_Text_LeaPostBattle:
	.string "LEA: Our lovey-dovey power failed…\p"
	.string "I blame JED. Honeymoon's over.$"

SSTidalRooms_Text_LeaNotEnoughMons:
	.string "LEA: You don't even have two POKéMON…\p"
	.string "That's so sad.$"

SSTidalRooms_Text_GarretIntro:
	.string "Ah, you came just in time.\p"
	.string "I'm bored. Entertain me.$"

SSTidalRooms_Text_GarretDefeat:
	.string "…That will do.$"

SSTidalRooms_Text_GarretPostBattle:
	.string "Perhaps I'll have Father buy me a yacht.\p"
	.string "This ferry has other people on it. Ew.$"

SSTidalRooms_Text_NaomiIntro:
	.string "Oh, what an adorable TRAINER.\p"
	.string "Tea? Or a battle? Or both? I'm on\n"
	.string "vacation.$"

SSTidalRooms_Text_NaomiDefeat:
	.string "I see. You're the active sort.$"

SSTidalRooms_Text_NaomiPostBattle:
	.string "A world cruise on a luxury liner has its\n"
	.string "charms…\p"
	.string "But a HOENN ferry has charm too.\p"
	.string "The charm of having no room service.$"

SSTidalRooms_Text_NotSuspiciousTakeThis:
	.string "Uh… Hi! I… I'm not acting suspicious!\p"
	.string "Take this! For free!\p"
	.string "I just like to play rough. With POKéMON.\n"
	.string "Only POKéMON.\p"
	.string "It's clean! Honestly!$"

SSTidalRooms_Text_ExplainSnatch:
	.string "PLAY ROUGH. A FAIRY move. It hits hard.\n"
	.string "It may lower ATTACK.\p"
	.string "It's not playful at all.$"

