FallarborTown_CozmosHouse_MapScripts::
	.byte 0

FallarborTown_CozmosHouse_EventScript_ProfCozmo::
	lock
	faceplayer
	call_if_set FLAG_SYS_GAME_CLEAR, FallarborTown_CozmosHouse_EventScript_CozmoCosmog @ Project Grounded: Cosmog (post-game)
	goto_if_set FLAG_RECEIVED_TM_RETURN, FallarborTown_CozmosHouse_EventScript_GaveMeteorite
	checkitem ITEM_METEORITE
	goto_if_eq VAR_RESULT, TRUE, FallarborTown_CozmosHouse_EventScript_PlayerHasMeteorite
	msgbox FallarborTown_CozmosHouse_Text_MeteoriteWillNeverBeMineNow, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_PlayerHasMeteorite::
	call_if_unset FLAG_TEMP_2, FallarborTown_CozmosHouse_EventScript_NoticeMeteorite
	call_if_set FLAG_TEMP_2, FallarborTown_CozmosHouse_EventScript_AskForMeteorite
	goto_if_eq VAR_RESULT, NO, FallarborTown_CozmosHouse_EventScript_DeclineGiveMeteorite
	msgbox FallarborTown_CozmosHouse_Text_PleaseUseThisTM, MSGBOX_DEFAULT
	giveitem ITEM_TM_RETURN
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setvar VAR_0x8004, ITEM_METEORITE
	call Common_EventScript_PlayerHandedOverTheItem
	setflag FLAG_RECEIVED_TM_RETURN
	msgbox FallarborTown_CozmosHouse_Text_ReallyGoingToHelpMyResearch, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_NoticeMeteorite::
	msgbox FallarborTown_CozmosHouse_Text_MeteoriteWillNeverBeMineNow, MSGBOX_DEFAULT
	msgbox FallarborTown_CozmosHouse_Text_IsThatMeteoriteMayIHaveIt, MSGBOX_YESNO
	return

FallarborTown_CozmosHouse_EventScript_AskForMeteorite::
	msgbox FallarborTown_CozmosHouse_Text_MayIHaveMeteorite, MSGBOX_YESNO
	return

FallarborTown_CozmosHouse_EventScript_DeclineGiveMeteorite::
	setflag FLAG_TEMP_2
	msgbox FallarborTown_CozmosHouse_Text_CrushedWithDisappointment, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_GaveMeteorite::
	msgbox FallarborTown_CozmosHouse_Text_ReallyGoingToHelpMyResearch, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_CozmosWife::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_RETURN, FallarborTown_CozmosHouse_EventScript_CozmoIsHappy
	goto_if_set FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY, FallarborTown_CozmosHouse_EventScript_CozmoIsSad
	msgbox FallarborTown_CozmosHouse_Text_CozmoWentToMeteorFalls, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_CozmoIsSad::
	msgbox FallarborTown_CozmosHouse_Text_FeelSorryForCozmo, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_CozmoIsHappy::
	msgbox FallarborTown_CozmosHouse_Text_CozmoIsSoHappy, MSGBOX_DEFAULT
	release
	end

@ Project Grounded: Cozmo geeft na de Hall of Fame een Cosmog; laat je hem de Solgaleo of Lunala zien die daaruit
@ groeide, dan krijg je een tweede Cosmog. Welke vorm het wordt, regelt src/ultra_space.c (Solrock/Lunatone eerst
@ gevangen; de tweede wordt altijd de vorm die je nog niet hebt). Teksten: placeholders.
FallarborTown_CozmosHouse_EventScript_CozmoCosmog::
	goto_if_unset FLAG_RECEIVED_COSMOG, FallarborTown_CozmosHouse_EventScript_GiveCosmog
	goto_if_set FLAG_RECEIVED_COSMOG_2, FallarborTown_CozmosHouse_EventScript_CosmogAllDone
	special Ultra_FindPartySunMoon
	goto_if_eq VAR_RESULT, 1, FallarborTown_CozmosHouse_EventScript_ShowedSolgaleo
	goto_if_eq VAR_RESULT, 2, FallarborTown_CozmosHouse_EventScript_ShowedLunala
	msgbox FallarborTown_CozmosHouse_Text_CosmogHowIsIt, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_GiveCosmog::
	msgbox FallarborTown_CozmosHouse_Text_CosmogIntro, MSGBOX_DEFAULT
	setvar VAR_0x8004, SPECIES_COSMOG
	setvar VAR_0x8005, 51
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, FallarborTown_CozmosHouse_EventScript_CosmogNoRoom
	setflag FLAG_RECEIVED_COSMOG
	msgbox FallarborTown_CozmosHouse_Text_CosmogAfter, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_ShowedSolgaleo::
	msgbox FallarborTown_CozmosHouse_Text_CosmogSawSolgaleo, MSGBOX_DEFAULT
	goto FallarborTown_CozmosHouse_EventScript_GiveCosmog2

FallarborTown_CozmosHouse_EventScript_ShowedLunala::
	msgbox FallarborTown_CozmosHouse_Text_CosmogSawLunala, MSGBOX_DEFAULT
FallarborTown_CozmosHouse_EventScript_GiveCosmog2::
	setvar VAR_0x8004, SPECIES_COSMOG
	setvar VAR_0x8005, 51
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, FallarborTown_CozmosHouse_EventScript_CosmogNoRoom
	setflag FLAG_RECEIVED_COSMOG_2
	msgbox FallarborTown_CozmosHouse_Text_Cosmog2After, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_CosmogReturn::
	return

FallarborTown_CozmosHouse_EventScript_CosmogNoRoom::
	msgbox FallarborTown_CozmosHouse_Text_CosmogNoRoom, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_EventScript_CosmogAllDone::
	goto_if_unset FLAG_RECEIVED_TM_RETURN, FallarborTown_CozmosHouse_EventScript_CosmogReturn
	msgbox FallarborTown_CozmosHouse_Text_CosmogAllDone, MSGBOX_DEFAULT
	release
	end

FallarborTown_CozmosHouse_Text_MeteoriteWillNeverBeMineNow:
	.string "PROF. COZMO: Oh… I never should have\n"
	.string "told TEAM MAGMA about the METEORITES…\p"
	.string "They promised me free hot sauce.\p"
	.string "It wasn't even that hot. It was like\n"
	.string "sriracha.$"

FallarborTown_CozmosHouse_Text_IsThatMeteoriteMayIHaveIt:
	.string "Oh! Hah?\p"
	.string "That item… Could it be?\p"
	.string "The METEORITE TEAM MAGMA took from\n"
	.string "METEOR FALLS?\p"
	.string "Please, may I have it?\p"
	.string "Not for free. How about this TM?$"

FallarborTown_CozmosHouse_Text_PleaseUseThisTM:
	.string "PROF. COZMO: This is RETURN. The more\n"
	.string "your POKéMON likes you, the harder it\l"
	.string "hits.\p"
	.string "So, not very hard, probably.$"

FallarborTown_CozmosHouse_Text_ReallyGoingToHelpMyResearch:
	.string "PROF. COZMO: Oh, I can't believe it! This\n"
	.string "is great!\p"
	.string "This will really help my research!\p"
	.string "And I can finally stop crying.$"

FallarborTown_CozmosHouse_Text_CrushedWithDisappointment:
	.string "PROF. COZMO: Oh… I'm crushed…\p"
	.string "I'll go eat sriracha. Alone.$"

FallarborTown_CozmosHouse_Text_MayIHaveMeteorite:
	.string "PROF. COZMO: Please, may I have that\n"
	.string "METEORITE?\p"
	.string "I'll give you this TM for it.$"

FallarborTown_CozmosHouse_Text_CozmoWentToMeteorFalls:
	.string "PROF. COZMO went to METEOR FALLS on\n"
	.string "ROUTE 114.\p"
	.string "With TEAM MAGMA. For hot sauce.\p"
	.string "Remind me why I married this\n"
	.string "susceptible fool?$"

FallarborTown_CozmosHouse_Text_FeelSorryForCozmo:
	.string "Poor PROF. COZMO… So depressed…\p"
	.string "I'd feel sorry for him if he hadn't sold\n"
	.string "us out for sriracha.$"

FallarborTown_CozmosHouse_Text_CozmoIsSoHappy:
	.string "Look at PROF. COZMO… So happy!\p"
	.string "He's hugging the rock. It's cute. And\n"
	.string "weird.$"

FallarborTown_CozmosHouse_Text_CosmogIntro:
	.string "PROF. COZMO: Ah, you! The CHAMPION! Or\n"
	.string "whatever you are now. Titles are just\l"
	.string "meteorites with paperwork.\p"
	.string "Last night something fell out of the\n"
	.string "sky and into my bird bath. It says\l"
	.string "“pew”. It has said “pew” four hundred\l"
	.string "times.\p"
	.string "My wife says it goes, or I go. I have\n"
	.string "chosen to keep living here. Please take\l"
	.string "it.$"

FallarborTown_CozmosHouse_Text_CosmogAfter:
	.string "It's called COSMOG. A nebula with a face.\n"
	.string "It knows SPLASH. It will always know\l"
	.string "SPLASH.\p"
	.string "They say it becomes either the sun or\n"
	.string "the moon. Which one? The stars decide.\l"
	.string "Or rocks. Probably rocks. Have you ever\l"
	.string "caught a SOLROCK? A LUNATONE? First\l"
	.string "come, first shine.$"

FallarborTown_CozmosHouse_Text_CosmogHowIsIt:
	.string "PROF. COZMO: How is my little nebula?\n"
	.string "Still saying “pew”?\p"
	.string "When it becomes the sun or the moon,\n"
	.string "show me! I want to see what I gave away\l"
	.string "out of cowardice.$"

FallarborTown_CozmosHouse_Text_CosmogSawSolgaleo:
	.string "PROF. COZMO: Is that… SOLGALEO? It\n"
	.string "became the SUN! My bird bath raised the\l"
	.string "SUN!\p"
	.string "Funny thing. Another one fell in this\n"
	.string "morning. It keeps looking at the night\l"
	.string "sky. It wants the other job, I think.$"

FallarborTown_CozmosHouse_Text_CosmogSawLunala:
	.string "PROF. COZMO: Is that… LUNALA? It\n"
	.string "became the MOON! My bird bath raised\l"
	.string "the MOON!\p"
	.string "Funny thing. Another one fell in this\n"
	.string "morning. It keeps squinting at the sun.\l"
	.string "It wants the other job, I think.$"

FallarborTown_CozmosHouse_Text_Cosmog2After:
	.string "PROF. COZMO: This one will become the\n"
	.string "other one. I'm almost sure. I asked it,\l"
	.string "and it said “pew” with conviction.\p"
	.string "Now my bird bath is empty. I miss it\n"
	.string "already. The bath, I mean.$"

FallarborTown_CozmosHouse_Text_CosmogNoRoom:
	.string "PROF. COZMO: Your team is full, and so is\n"
	.string "your PC. How? Do you just… keep\l"
	.string "everything?\p"
	.string "Come back with room for a nebula.$"

FallarborTown_CozmosHouse_Text_CosmogAllDone:
	.string "PROF. COZMO: The sun and the moon, both\n"
	.string "raised in my bird bath. I'm putting that\l"
	.string "on my resume.\p"
	.string "My wife says the bird bath is a bird\n"
	.string "bath again. I say it is a launch site.$"

