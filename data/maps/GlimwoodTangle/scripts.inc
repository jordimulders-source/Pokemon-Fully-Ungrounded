@ Project Grounded: GlimwoodTangle (tools/grounded/maptools/glimwood.py)
@ Stervend bos (layout GlimwoodTangle_Dying) tot Xerneas gevangen is; daarna licht, en Yveltal.
GlimwoodTangle_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GlimwoodTangle_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, GlimwoodTangle_OnFrame
	.byte 0

GlimwoodTangle_OnTransition:
	setflag FLAG_TEMP_1
	call_if_unset FLAG_GLIMWOOD_MET_WITCH, GlimwoodTangle_EventScript_SetIntro
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, GlimwoodTangle_EventScript_StateBright
	setmaplayoutindex LAYOUT_GLIMWOOD_TANGLE_DYING
	setweather WEATHER_SHADE
	savebgm MUS_RG_POKE_TOWER
	end

GlimwoodTangle_EventScript_StateBright:
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, GlimwoodTangle_EventScript_StateEnd
	clearflag FLAG_TEMP_1
	call_if_unset FLAG_GLIMWOOD_YVELTAL_SEEN, GlimwoodTangle_EventScript_SetYveltal
GlimwoodTangle_EventScript_StateEnd:
	end

GlimwoodTangle_EventScript_SetIntro:
	setvar VAR_TEMP_1, 1
	return

GlimwoodTangle_EventScript_SetYveltal:
	setvar VAR_TEMP_1, 2
	return

GlimwoodTangle_OnFrame:
	map_script_2 VAR_TEMP_1, 1, GlimwoodTangle_EventScript_Intro
	map_script_2 VAR_TEMP_1, 2, GlimwoodTangle_EventScript_YveltalScene
	.2byte 0

GlimwoodTangle_EventScript_Intro:
	lockall
	setvar VAR_TEMP_1, 0
	delay 20
	msgbox GlimwoodTangle_Text_Intro1, MSGBOX_DEFAULT
	msgbox GlimwoodTangle_Text_Intro2, MSGBOX_DEFAULT
	setflag FLAG_GLIMWOOD_MET_WITCH
	releaseall
	end

GlimwoodTangle_EventScript_YveltalScene:
	lockall
	setvar VAR_TEMP_1, 0
	setflag FLAG_GLIMWOOD_YVELTAL_SEEN
	delay 20
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	fadescreenspeed FADE_TO_BLACK, 2
	fadescreenspeed FADE_FROM_BLACK, 2
	waitmoncry
	msgbox GlimwoodTangle_Text_YveltalScene, MSGBOX_DEFAULT
	releaseall
	end

GlimwoodTangle_EventScript_Witch::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_GLIMWOOD_DONE, GlimwoodTangle_EventScript_WitchDone
	goto_if_set FLAG_GLIMWOOD_XERNEAS_DONE, GlimwoodTangle_EventScript_WitchLight
	random 3
	switch VAR_RESULT
	case 0, GlimwoodTangle_EventScript_Quiz0
	case 1, GlimwoodTangle_EventScript_Quiz1
	msgbox GlimwoodTangle_Text_Quiz2, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_Quiz0:
	msgbox GlimwoodTangle_Text_Quiz0, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_Quiz1:
	msgbox GlimwoodTangle_Text_Quiz1, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_WitchLight:
	msgbox GlimwoodTangle_Text_WitchLight, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_WitchDone:
	msgbox GlimwoodTangle_Text_WitchDone, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_Morwen::
	trainerbattle_single TRAINER_GLIMWOOD_HEX_MANIAC_MORWEN, GlimwoodTangle_Text_MorwenIntro, GlimwoodTangle_Text_MorwenDefeat
	msgbox GlimwoodTangle_Text_MorwenPost, MSGBOX_AUTOCLOSE
	end

GlimwoodTangle_EventScript_Silas::
	trainerbattle_single TRAINER_GLIMWOOD_PSYCHIC_SILAS, GlimwoodTangle_Text_SilasIntro, GlimwoodTangle_Text_SilasDefeat
	msgbox GlimwoodTangle_Text_SilasPost, MSGBOX_AUTOCLOSE
	end

GlimwoodTangle_EventScript_Odette::
	trainerbattle_single TRAINER_GLIMWOOD_BEAUTY_ODETTE, GlimwoodTangle_Text_OdetteIntro, GlimwoodTangle_Text_OdetteDefeat
	msgbox GlimwoodTangle_Text_OdettePost, MSGBOX_AUTOCLOSE
	end

GlimwoodTangle_EventScript_Gang1::
	lock
	faceplayer
	playmoncry SPECIES_MORGREM, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Text_Gang1, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_IMPIDIMP, 64, ITEM_NONE, SPECIES_MORGREM, 64, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_EventScript_Gang1Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_EventScript_Gang1Gone
	release
	end

GlimwoodTangle_EventScript_Gang1Gone::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_GLIMWOOD_GANG_1
	setflag FLAG_GLIMWOOD_GANG_1
	fadescreen FADE_FROM_BLACK
	msgbox GlimwoodTangle_Text_GangGone, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_Gang2::
	lock
	faceplayer
	playmoncry SPECIES_IMPIDIMP, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Text_Gang2, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_MORGREM, 65, ITEM_NONE, SPECIES_IMPIDIMP, 64, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_EventScript_Gang2Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_EventScript_Gang2Gone
	release
	end

GlimwoodTangle_EventScript_Gang2Gone::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_GLIMWOOD_GANG_2
	setflag FLAG_GLIMWOOD_GANG_2
	fadescreen FADE_FROM_BLACK
	msgbox GlimwoodTangle_Text_GangGone, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_Gang3::
	lock
	faceplayer
	playmoncry SPECIES_MORGREM, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Text_Gang3, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_MORGREM, 65, ITEM_NONE, SPECIES_MORGREM, 65, ITEM_NONE
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_EventScript_Gang3Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_EventScript_Gang3Gone
	release
	end

GlimwoodTangle_EventScript_Gang3Gone::
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_GLIMWOOD_GANG_3A
	removeobject LOCALID_GLIMWOOD_GANG_3B
	setflag FLAG_GLIMWOOD_GANG_3
	fadescreen FADE_FROM_BLACK
	msgbox GlimwoodTangle_Text_GangGone, MSGBOX_DEFAULT
	release
	end


GlimwoodTangle_EventScript_Yveltal::
	lock
	faceplayer
	playmoncry SPECIES_YVELTAL, CRY_MODE_ENCOUNTER
	msgbox GlimwoodTangle_Text_Yveltal, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_YVELTAL, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GlimwoodTangle_EventScript_YveltalCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GlimwoodTangle_EventScript_YveltalCocoon
	release
	end

GlimwoodTangle_EventScript_YveltalCocoon::
	msgbox GlimwoodTangle_Text_YveltalCocoon, MSGBOX_DEFAULT
	release
	end

GlimwoodTangle_EventScript_YveltalCaught::
	removeobject LOCALID_GLIMWOOD_YVELTAL
	setflag FLAG_SPACETIME_GLIMWOOD_DONE
	msgbox GlimwoodTangle_Text_YveltalCaught, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
GlimwoodTangle_Text_Intro1:
	.string "Ah, a visitor. Mind the mushrooms,\n"
	.string "dearie. Some of them used to be people.$"

GlimwoodTangle_Text_Intro2:
	.string "I'm the witch of BALLONLEA. Retired. An\n"
	.string "IMPIDIMP gang and a deathly aura are\l"
	.string "snuffing out the forest's light. Only\l"
	.string "XERNEAS can relight it. It sleeps north\l"
	.string "of the village. Pop quiz later. There's\l"
	.string "always a pop quiz.$"

GlimwoodTangle_Text_Quiz0:
	.string "Pop quiz! What glows in the dark, has no\n"
	.string "friends and talks to mushrooms?\l"
	.string "...Correct, it's me. Ten points to nobody.$"

GlimwoodTangle_Text_Quiz1:
	.string "Pop quiz! How many IMPIDIMP does it\n"
	.string "take to ruin a forest? ...Trick question.\l"
	.string "They don't count. They can't count.\l"
	.string "That's the whole problem.$"

GlimwoodTangle_Text_Quiz2:
	.string "Pop quiz! True or false: the mushrooms\n"
	.string "are watching you. ...You hesitated.\l"
	.string "Wrong answer. They're also judging you.$"

GlimwoodTangle_Text_WitchLight:
	.string "The light's back! Lovely. Now something\n"
	.string "with big red wings is sulking in the\l"
	.string "fairy ring. Life and death, dearie. You\l"
	.string "can't have one without the other\l"
	.string "bothering you.$"

GlimwoodTangle_Text_WitchDone:
	.string "Life and death, both in your bag. Very\n"
	.string "tidy. Final quiz: was it worth it? ...Don't\l"
	.string "answer. I'm a witch, not a therapist.$"

GlimwoodTangle_Text_YveltalScene:
	.string "The new light flickers. Something vast\n"
	.string "lands in the fairy ring, wings like a\l"
	.string "funeral nobody was invited to. Where\l"
	.string "there's life, there's paperwork. And\l"
	.string "YVELTAL.$"

GlimwoodTangle_Text_MorwenIntro:
	.string "My teacups are cursed. I collect them.\n"
	.string "I'm not giving you one.$"

GlimwoodTangle_Text_MorwenDefeat:
	.string "Fine. Take the teacup. No? Nobody ever\n"
	.string "takes the teacup.$"

GlimwoodTangle_Text_MorwenPost:
	.string "The forest whispers my name.\n"
	.string "Mispronounces it, but still.$"

GlimwoodTangle_Text_SilasIntro:
	.string "I've walked in circles here since the old\n"
	.string "Galar kings. The path keeps moving. Or I\l"
	.string "do. Fight me while I figure it out.$"

GlimwoodTangle_Text_SilasDefeat:
	.string "Hm. Lost again. To you, this time.$"

GlimwoodTangle_Text_SilasPost:
	.string "If you see the exit, don't tell me. I've\n"
	.string "grown attached to being lost.$"

GlimwoodTangle_Text_OdetteIntro:
	.string "I'm a fairy! Real wings! ...They're\n"
	.string "cardboard. Don't look at the tape.$"

GlimwoodTangle_Text_OdetteDefeat:
	.string "My wings fell off. Very on-brand for\n"
	.string "this forest.$"

GlimwoodTangle_Text_OdettePost:
	.string "The mushrooms think I'm one of them. I\n"
	.string "haven't told them.$"

GlimwoodTangle_Text_Gang1:
	.string "Two IMPIDIMP-gang members are drawing\n"
	.string "mustaches on a glowing mushroom. They'd\l"
	.string "like to draw one on you.$"

GlimwoodTangle_Text_Gang2:
	.string "MORGREM is stealing the light out of\n"
	.string "the mushrooms and putting it in a jar.\l"
	.string "The jar says MINE.$"

GlimwoodTangle_Text_Gang3:
	.string "Two MORGREM block the road to\n"
	.string "BALLONLEA. Their sign says NO ENTRY.\l"
	.string "It's spelled wrong.$"

GlimwoodTangle_Text_GangGone:
	.string "The gang scatters into the dark,\n"
	.string "giggling. A little light seeps back into\l"
	.string "the mushrooms. Not much. Like a phone\l"
	.string "at one percent.$"

GlimwoodTangle_Text_Yveltal:
	.string "YVELTAL spreads its wings over the\n"
	.string "fairy ring. The mushrooms nearest to it\l"
	.string "go grey. It looks at you the way a\l"
	.string "vulture looks at a long walk.$"

GlimwoodTangle_Text_YveltalCocoon:
	.string "YVELTAL folds into a dark cocoon... and\n"
	.string "hatches again almost immediately,\l"
	.string "visibly annoyed. Death doesn't do sick\l"
	.string "days. Try again.$"

GlimwoodTangle_Text_YveltalCaught:
	.string "YVELTAL is yours. The forest keeps its\n"
	.string "light, and its shadows. Both behave, for\l"
	.string "now. GLIMWOOD TANGLE is at peace.$"
