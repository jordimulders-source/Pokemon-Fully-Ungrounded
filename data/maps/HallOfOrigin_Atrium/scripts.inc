@ Project Grounded: HallOfOrigin_Atrium (tools/grounded/maptools/hall_of_origin.py)
HallOfOrigin_Atrium_MapScripts::
	.byte 0

HallOfOrigin_Atrium_EventScript_Nous::
	trainerbattle_single TRAINER_HOO_NOUS, HallOfOrigin_Atrium_Text_NousIntro, HallOfOrigin_Atrium_Text_NousDefeat
	msgbox HallOfOrigin_Atrium_Text_NousPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Atrium_EventScript_Somnia::
	trainerbattle_single TRAINER_HOO_SOMNIA, HallOfOrigin_Atrium_Text_SomniaIntro, HallOfOrigin_Atrium_Text_SomniaDefeat
	msgbox HallOfOrigin_Atrium_Text_SomniaPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Atrium_EventScript_Gladius::
	trainerbattle_single TRAINER_HOO_GLADIUS, HallOfOrigin_Atrium_Text_GladiusIntro, HallOfOrigin_Atrium_Text_GladiusDefeat
	msgbox HallOfOrigin_Atrium_Text_GladiusPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Atrium_EventScript_Hephaest::
	trainerbattle_single TRAINER_HOO_HEPHAEST, HallOfOrigin_Atrium_Text_HephaestIntro, HallOfOrigin_Atrium_Text_HephaestDefeat
	msgbox HallOfOrigin_Atrium_Text_HephaestPost, MSGBOX_AUTOCLOSE
	end

HallOfOrigin_Atrium_EventScript_Fountain::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox HallOfOrigin_Atrium_Text_Fountain, MSGBOX_DEFAULT
	releaseall
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
HallOfOrigin_Atrium_Text_NousIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION: MIND.\p"
	.string "I already calculated how this ends. I'm\n"
	.string "only here because ARCEUS likes to\l"
	.string "watch the numbers happen.$"

HallOfOrigin_Atrium_Text_NousDefeat:
	.string "Recalculating. Recalculating. ...Oh no.$"

HallOfOrigin_Atrium_Text_NousPost:
	.string "I have no thoughts of my own. ARCEUS\n"
	.string "lends me his. They're very loud.$"

HallOfOrigin_Atrium_Text_SomniaIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION:\n"
	.string "DREAMS.\p"
	.string "Statues don't sleep. I've been awake\n"
	.string "for four thousand years. Ask me how I'm\l"
	.string "doing.$"

HallOfOrigin_Atrium_Text_SomniaDefeat:
	.string "Finally. Darkness. Five more minutes.$"

HallOfOrigin_Atrium_Text_SomniaPost:
	.string "If you see yourself falling, don't worry.\n"
	.string "That's just the next floor.$"

HallOfOrigin_Atrium_Text_GladiusIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION:\n"
	.string "JUSTICE.\p"
	.string "ARCEUS gave me a sword arm and no\n"
	.string "sword. I've been very fair about it.$"

HallOfOrigin_Atrium_Text_GladiusDefeat:
	.string "Justice served. Cold. With a side of\n"
	.string "gravel.$"

HallOfOrigin_Atrium_Text_GladiusPost:
	.string "The forge is next door. Don't touch\n"
	.string "anything glowing. Everything is glowing.$"

HallOfOrigin_Atrium_Text_HephaestIntro:
	.string "CONSTRUCT ONLINE. DESIGNATION: FORGE.\p"
	.string "I built the other eight. Then they\n"
	.string "asked who built me. Awkward silence.\l"
	.string "Fourteen centuries of it.$"

HallOfOrigin_Atrium_Text_HephaestDefeat:
	.string "Cracked. Hairline. Don't tell the others.$"

HallOfOrigin_Atrium_Text_HephaestPost:
	.string "Upstairs are the last two. One of them\n"
	.string "alphabetises time.$"

HallOfOrigin_Atrium_Text_Fountain:
	.string "A pool of light, humming to itself. Your\n"
	.string "POKéMON drink from it and look\l"
	.string "healthier.\p"
	.string "You feel judged, but in a supportive\n"
	.string "way.$"
