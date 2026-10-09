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
	.string "I am the emissary of the mind. I already\n"
	.string "know how this battle goes.\p"
	.string "I'm just here for the paperwork.$"

HallOfOrigin_Atrium_Text_NousDefeat:
	.string "...I knew that. I definitely knew that.$"

HallOfOrigin_Atrium_Text_NousPost:
	.string "ARCEUS gave three POKéMON knowledge,\n"
	.string "emotion and willpower. Me it gave a\l"
	.string "clipboard.$"

HallOfOrigin_Atrium_Text_SomniaIntro:
	.string "Emissary of dreams. You're asleep, by\n"
	.string "the way. Have been since SKY PILLAR.\p"
	.string "Kidding. Probably.$"

HallOfOrigin_Atrium_Text_SomniaDefeat:
	.string "Wake up. You won. Or that's what you're\n"
	.string "dreaming.$"

HallOfOrigin_Atrium_Text_SomniaPost:
	.string "If you see yourself falling, don't worry.\n"
	.string "That's just the next floor.$"

HallOfOrigin_Atrium_Text_GladiusIntro:
	.string "Emissary of justice. Every sword in this\n"
	.string "team has sworn an oath.\p"
	.string "Mine was 'no refunds'.$"

HallOfOrigin_Atrium_Text_GladiusDefeat:
	.string "Justice is served. Cold. With a side of\n"
	.string "humiliation.$"

HallOfOrigin_Atrium_Text_GladiusPost:
	.string "The forge is next door. Don't touch\n"
	.string "anything glowing. Everything is glowing.$"

HallOfOrigin_Atrium_Text_HephaestIntro:
	.string "Emissary of the forge. ARCEUS made the\n"
	.string "world. I made the oven it was baked in.\p"
	.string "Let's see if you're done.$"

HallOfOrigin_Atrium_Text_HephaestDefeat:
	.string "Undercooked. Me, I mean.$"

HallOfOrigin_Atrium_Text_HephaestPost:
	.string "Upstairs are the last two. One of them\n"
	.string "alphabetises time.$"

HallOfOrigin_Atrium_Text_Fountain:
	.string "A pool of light, humming to itself. Your\n"
	.string "POKéMON drink from it and look\l"
	.string "healthier.\p"
	.string "You feel judged, but in a supportive\n"
	.string "way.$"
