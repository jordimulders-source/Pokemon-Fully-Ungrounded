@ Project Grounded: NationalPark (tools/grounded/maptools/national_park.py)
@ Illusie (layout NationalPark) -> brandend park (NationalPark_Ruined) -> hersteld (NationalPark).
NationalPark_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, NationalPark_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, NationalPark_OnFrame
	.byte 0

NationalPark_OnTransition:
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	call_if_set FLAG_NATIONAL_PARK_SCENE_PENDING, NationalPark_EventScript_SetScene
	goto_if_set FLAG_NATIONAL_PARK_DONE, NationalPark_EventScript_StateDone
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, NationalPark_EventScript_StateRestored
	goto_if_set FLAG_NATIONAL_PARK_REVEALED, NationalPark_EventScript_StateRuined
	clearflag FLAG_TEMP_1
	goto_if_not_defeated TRAINER_NP_BUG_CATCHER_DOUGLAS, NationalPark_EventScript_StateEnd
	goto_if_not_defeated TRAINER_NP_PICNICKER_SIENNA, NationalPark_EventScript_StateEnd
	goto_if_not_defeated TRAINER_NP_GENTLEMAN_WALDORF, NationalPark_EventScript_StateEnd
	goto_if_not_defeated TRAINER_NP_AROMA_LADY_PETUNIA, NationalPark_EventScript_StateEnd
	clearflag FLAG_TEMP_3
	end

NationalPark_EventScript_SetScene:
	setvar VAR_TEMP_1, 1
	return

NationalPark_EventScript_StateDone:
	clearflag FLAG_TEMP_1
	end

NationalPark_EventScript_StateRestored:
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_3
	clearflag FLAG_TEMP_4
	end

NationalPark_EventScript_StateRuined:
	setmaplayoutindex LAYOUT_NATIONAL_PARK_RUINED
	setweather WEATHER_VOLCANIC_ASH
	savebgm MUS_RG_POKE_MANSION
	clearflag FLAG_TEMP_3
	goto_if_defeated TRAINER_NP_SHADOW_ASH, NationalPark_EventScript_StateRuinedB
	clearflag FLAG_TEMP_2
NationalPark_EventScript_StateRuinedB:
	goto_if_defeated TRAINER_NP_SHADOW_EMBER, NationalPark_EventScript_StateEnd
	clearflag FLAG_TEMP_5
NationalPark_EventScript_StateEnd:
	end

NationalPark_OnFrame:
	map_script_2 VAR_TEMP_1, 1, NationalPark_EventScript_Scene
	.2byte 0

NationalPark_EventScript_Scene:
	lockall
	setvar VAR_TEMP_1, 0
	clearflag FLAG_NATIONAL_PARK_SCENE_PENDING
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, NationalPark_EventScript_SceneRestored
	delay 30
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	msgbox NationalPark_Text_RevealAfter, MSGBOX_DEFAULT
	waitmoncry
	releaseall
	end

NationalPark_EventScript_SceneRestored:
	delay 30
	msgbox NationalPark_Text_RestoredAfter, MSGBOX_DEFAULT
	closemessage
	playse SE_THUNDER
	delay 20
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox NationalPark_Text_EternatusArrives, MSGBOX_DEFAULT
	releaseall
	end

NationalPark_EventScript_CheckCalyrex::
	goto_if_not_defeated TRAINER_NP_BUG_CATCHER_DOUGLAS, NationalPark_EventScript_CheckCalyrexEnd
	goto_if_not_defeated TRAINER_NP_PICNICKER_SIENNA, NationalPark_EventScript_CheckCalyrexEnd
	goto_if_not_defeated TRAINER_NP_GENTLEMAN_WALDORF, NationalPark_EventScript_CheckCalyrexEnd
	goto_if_not_defeated TRAINER_NP_AROMA_LADY_PETUNIA, NationalPark_EventScript_CheckCalyrexEnd
	msgbox NationalPark_Text_CalyrexAppears, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_TEMP_3
	addobject LOCALID_NATIONAL_PARK_CALYREX
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	waitmoncry
NationalPark_EventScript_CheckCalyrexEnd::
	release
	end

NationalPark_EventScript_Douglas::
	trainerbattle_single TRAINER_NP_BUG_CATCHER_DOUGLAS, NationalPark_Text_DouglasIntro, NationalPark_Text_DouglasDefeat, NationalPark_EventScript_CheckCalyrex
	msgbox NationalPark_Text_DouglasPost, MSGBOX_AUTOCLOSE
	end

NationalPark_EventScript_Sienna::
	trainerbattle_single TRAINER_NP_PICNICKER_SIENNA, NationalPark_Text_SiennaIntro, NationalPark_Text_SiennaDefeat, NationalPark_EventScript_CheckCalyrex
	msgbox NationalPark_Text_SiennaPost, MSGBOX_AUTOCLOSE
	end

NationalPark_EventScript_Waldorf::
	trainerbattle_single TRAINER_NP_GENTLEMAN_WALDORF, NationalPark_Text_WaldorfIntro, NationalPark_Text_WaldorfDefeat, NationalPark_EventScript_CheckCalyrex
	msgbox NationalPark_Text_WaldorfPost, MSGBOX_AUTOCLOSE
	end

NationalPark_EventScript_Petunia::
	trainerbattle_single TRAINER_NP_AROMA_LADY_PETUNIA, NationalPark_Text_PetuniaIntro, NationalPark_Text_PetuniaDefeat, NationalPark_EventScript_CheckCalyrex
	msgbox NationalPark_Text_PetuniaPost, MSGBOX_AUTOCLOSE
	end

NationalPark_EventScript_Calyrex::
	lock
	faceplayer
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, NationalPark_EventScript_CalyrexEternatus
	goto_if_set FLAG_NATIONAL_PARK_CELEBI_DONE, NationalPark_EventScript_CalyrexRestore
	goto_if_set FLAG_NATIONAL_PARK_REVEALED, NationalPark_EventScript_CalyrexRuins
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	msgbox NationalPark_Text_CalyrexIntro, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	playse SE_M_PSYBEAM
	fadescreenspeed FADE_TO_WHITE, 6
	setflag FLAG_NATIONAL_PARK_REVEALED
	setflag FLAG_NATIONAL_PARK_SCENE_PENDING
	warpsilent MAP_NATIONAL_PARK, 22, 27
	waitstate
	release
	end

NationalPark_EventScript_CalyrexRuins:
	goto_if_not_defeated TRAINER_NP_SHADOW_ASH, NationalPark_EventScript_CalyrexShades
	goto_if_not_defeated TRAINER_NP_SHADOW_EMBER, NationalPark_EventScript_CalyrexShades
	msgbox NationalPark_Text_CalyrexIlex, MSGBOX_DEFAULT
	release
	end

NationalPark_EventScript_CalyrexShades:
	msgbox NationalPark_Text_CalyrexShades, MSGBOX_DEFAULT
	release
	end

NationalPark_EventScript_CalyrexRestore:
	msgbox NationalPark_Text_CalyrexRestore, MSGBOX_DEFAULT
	closemessage
	setobjectxyperm LOCALID_NATIONAL_PARK_CELEBI, 21, 24
	clearflag FLAG_TEMP_6
	addobject LOCALID_NATIONAL_PARK_CELEBI
	playmoncry SPECIES_CELEBI, CRY_MODE_NORMAL
	waitmoncry
	applymovement LOCALID_NATIONAL_PARK_CELEBI, NationalPark_EventScript_CelebiCircle
	waitmovement 0
	msgbox NationalPark_Text_CelebiRestores, MSGBOX_DEFAULT
	closemessage
	playse SE_M_HEAL_BELL
	fadescreenspeed FADE_TO_WHITE, 8
	removeobject LOCALID_NATIONAL_PARK_CELEBI
	setflag FLAG_NATIONAL_PARK_RESTORED
	setflag FLAG_NATIONAL_PARK_SCENE_PENDING
	warpsilent MAP_NATIONAL_PARK, 22, 27
	waitstate
	release
	end

NationalPark_EventScript_CalyrexEternatus:
	msgbox NationalPark_Text_CalyrexEternatus, MSGBOX_DEFAULT
	release
	end

NationalPark_EventScript_CelebiCircle:
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_left
	walk_fast_left
	walk_fast_left
	face_down
	step_end

NationalPark_EventScript_Eternatus::
	lock
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	msgbox NationalPark_Text_EternatusBattle, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ETERNATUS, 95
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NationalPark_EventScript_EternatusStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NationalPark_EventScript_EternatusStays
	removeobject LOCALID_NATIONAL_PARK_ETERNATUS
	setflag FLAG_NATIONAL_PARK_DONE
	msgbox NationalPark_Text_CalyrexFarewell, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	removeobject LOCALID_NATIONAL_PARK_CALYREX
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox NationalPark_Text_ParkDone, MSGBOX_DEFAULT
NationalPark_EventScript_EternatusStays:
	release
	end

NationalPark_EventScript_ShadesA::
	lock
	faceplayer
	msgbox NationalPark_Text_ShadesA, MSGBOX_DEFAULT
	closemessage
NationalPark_EventScript_ShadesAChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, NationalPark_EventScript_ShadesABattle
	special LoadPlayerParty
	goto NationalPark_EventScript_ShadesAChoose

NationalPark_EventScript_ShadesABattle::
	multi_2_vs_2 TRAINER_NP_SHADOW_ASH, NationalPark_Text_AshDefeat, TRAINER_NP_SHADOW_CINDER, NationalPark_Text_CinderDefeat, PARTNER_CALYREX
	switch VAR_RESULT
	case 1, NationalPark_EventScript_ShadesAWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

NationalPark_EventScript_ShadesAWon::
	msgbox NationalPark_Text_ShadesAWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_NATIONAL_PARK_SHADOW_ASH
	removeobject LOCALID_NATIONAL_PARK_SHADOW_CINDER
	setflag FLAG_TEMP_2
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

NationalPark_EventScript_ShadesB::
	lock
	faceplayer
	msgbox NationalPark_Text_ShadesB, MSGBOX_DEFAULT
	closemessage
NationalPark_EventScript_ShadesBChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, NationalPark_EventScript_ShadesBBattle
	special LoadPlayerParty
	goto NationalPark_EventScript_ShadesBChoose

NationalPark_EventScript_ShadesBBattle::
	multi_2_vs_2 TRAINER_NP_SHADOW_EMBER, NationalPark_Text_EmberDefeat, TRAINER_NP_SHADOW_SOOT, NationalPark_Text_SootDefeat, PARTNER_CALYREX
	switch VAR_RESULT
	case 1, NationalPark_EventScript_ShadesBWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

NationalPark_EventScript_ShadesBWon::
	msgbox NationalPark_Text_ShadesBWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_NATIONAL_PARK_SHADOW_EMBER
	removeobject LOCALID_NATIONAL_PARK_SHADOW_SOOT
	setflag FLAG_TEMP_5
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

NationalPark_EventScript_SignPlaza::
	msgbox NationalPark_Text_SignPlaza, MSGBOX_SIGN
	end

NationalPark_EventScript_SignGate::
	msgbox NationalPark_Text_SignGate, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
NationalPark_Text_RevealAfter:
	.string "CALYREX: Behold. This is your park in\n"
	.string "this dimension. Eternatus got here\l"
	.string "first. It did not bring a picnic basket.\l"
	.string "The shades that feed on the smoke will\l"
	.string "come for us. Fight beside me. I am a\l"
	.string "king. I am also, technically, a cabbage.$"

NationalPark_Text_RestoredAfter:
	.string "The ash blows away. The grass remembers\n"
	.string "it is green. A Butterfree lands on your\l"
	.string "head as if nothing happened. Denial is a\l"
	.string "powerful thing.$"

NationalPark_Text_EternatusArrives:
	.string "CALYREX: It followed the green. Of\n"
	.string "course it did. Celebi's power is still in\l"
	.string "your team: every POKéMON you send out\l"
	.string "will rise above itself. Go. I will hold\l"
	.string "your sandwiches.$"

NationalPark_Text_CalyrexAppears:
	.string "Something by the fountain clears its\n"
	.string "throat. Regally.$"

NationalPark_Text_DouglasIntro:
	.string "This park has a bug-catching contest\n"
	.string "every day. I win every day. Nobody else\l"
	.string "enters. Is that suspicious? Don't\l"
	.string "answer that.$"

NationalPark_Text_DouglasDefeat:
	.string "My bugs! My contest record!$"

NationalPark_Text_DouglasPost:
	.string "The grass feels... painted. Like a\n"
	.string "screensaver.$"

NationalPark_Text_SiennaIntro:
	.string "I've been eating the same sandwich\n"
	.string "since I got here. It never runs out.\l"
	.string "Best day of my life! Probably! Has it\l"
	.string "been a day?$"

NationalPark_Text_SiennaDefeat:
	.string "My sandwich is crying.$"

NationalPark_Text_SiennaPost:
	.string "If you see a crowned guy on a stag, tell\n"
	.string "him the sandwich is a little suspicious.$"

NationalPark_Text_WaldorfIntro:
	.string "Good afternoon. It's always afternoon\n"
	.string "here. I find that very civilised.$"

NationalPark_Text_WaldorfDefeat:
	.string "Most uncivilised. Well played.$"

NationalPark_Text_WaldorfPost:
	.string "Have you noticed the sun never moves?\n"
	.string "Lovely. Terrifying.$"

NationalPark_Text_PetuniaIntro:
	.string "Smell that? Fresh grass, flowers... and a\n"
	.string "faint hint of something burning.\l"
	.string "Probably a barbecue. In every\l"
	.string "direction.$"

NationalPark_Text_PetuniaDefeat:
	.string "Even my Florges smells smoke now.$"

NationalPark_Text_PetuniaPost:
	.string "The fountain hums. Fountains don't hum.\n"
	.string "I'm going to pretend it's jazz.$"

NationalPark_Text_CalyrexIntro:
	.string "I am CALYREX, King of Bountiful\n"
	.string "Harvests, traveller of dimensions, and\l"
	.string "the reason this park looks so nice.\l"
	.string "Sorry. It is an illusion. I channelled it\l"
	.string "so you would not panic. You beat\l"
	.string "everyone in it, so now you may panic.\l"
	.string "Look.$"

NationalPark_Text_CalyrexShades:
	.string "CALYREX: The shades want what is left\n"
	.string "of this park. One stands by the band of\l"
	.string "the ball, the other blocks the path\l"
	.string "south. Talk to them. I will be right\l"
	.string "behind you. Slightly to the left.$"

NationalPark_Text_CalyrexIlex:
	.string "CALYREX: The shades are gone. Now go\n"
	.string "south, through the woods, to ILEX\l"
	.string "FOREST. At the shrine you will find\l"
	.string "CELEBI. It cannot beat Eternatus.\l"
	.string "Nobody here can. But it can lend you the\l"
	.string "strength to try. Bring it back. Gently.\l"
	.string "In a ball.$"

NationalPark_Text_CalyrexRestore:
	.string "CALYREX: You caught CELEBI. Now, little\n"
	.string "one: show this park what it used to be.$"

NationalPark_Text_CelebiRestores:
	.string "CELEBI circles the fountain and hums a\n"
	.string "very old song. The fire listens.$"

NationalPark_Text_CalyrexEternatus:
	.string "CALYREX: Eternatus waits north of the\n"
	.string "fountain. Your team carries CELEBI's\l"
	.string "power: each one rises above itself the\l"
	.string "moment it enters battle.$"

NationalPark_Text_EternatusBattle:
	.string "ETERNATUS looms over the tall grass. It\n"
	.string "smells like a burnt-out sun. Your\l"
	.string "POKéMON glow green: CELEBI's power is\l"
	.string "with them.$"

NationalPark_Text_CalyrexFarewell:
	.string "CALYREX: The park is safe, in this\n"
	.string "dimension and the next. My horses are\l"
	.string "waiting somewhere cold; they have been\l"
	.string "sulking without me. Farewell, trainer. Do\l"
	.string "not eat the sandwich.$"

NationalPark_Text_ParkDone:
	.string "CALYREX has left. The park is quiet. A\n"
	.string "Ledian waves at you. You wave back.\l"
	.string "Nobody saw. Good.$"

NationalPark_Text_ShadesA:
	.string "Two shapes made of smoke turn towards\n"
	.string "you. They have no faces, but somehow\l"
	.string "they look smug. CALYREX: Together,\l"
	.string "then.$"

NationalPark_Text_AshDefeat:
	.string "...hsss...$"

NationalPark_Text_CinderDefeat:
	.string "...the smoke... remembers...$"

NationalPark_Text_ShadesAWon:
	.string "The shades dissolve into ash. CALYREX\n"
	.string "nods, as if he did most of the work.$"

NationalPark_Text_ShadesB:
	.string "The shades block the path south. One of\n"
	.string "them is wearing a picnic hat. That is the\l"
	.string "worst thing you have seen today.$"

NationalPark_Text_EmberDefeat:
	.string "...hsss...$"

NationalPark_Text_SootDefeat:
	.string "...the smoke... remembers...$"

NationalPark_Text_ShadesBWon:
	.string "The shades dissolve into ash. CALYREX\n"
	.string "nods, as if he did most of the work.$"

NationalPark_Text_SignPlaza:
	.string "NATIONAL PARK\n"
	.string "The shady path south leads to ILEX\l"
	.string "FOREST.\l"
	.string "Please do not feed the Beedrill.$"

NationalPark_Text_SignGate:
	.string "NATIONAL PARK\n"
	.string "Gate to the SPACETIME CAVE. Opening\l"
	.string "hours: always, and also never.$"
