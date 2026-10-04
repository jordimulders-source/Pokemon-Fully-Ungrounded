@ Project Grounded: de meteoriet in de ruimte (Deoxys-event). Je komt hier vanuit het Space Center van Mossdeep
@ (MossdeepCity_SpaceCenter_1F_EventScript_LaunchToSpace). Kaart en events: tools/grounded/maptools/meteor_space.py.
@ De rode driehoek is de steen van Birth Island met het palet van de laatste puzzelstand (OBJ_EVENT_GFX_DEOXYS_TRIANGLE_RED);
@ geen puzzel, wel de vertrouwde opbouw: de steen spat uiteen, Deoxys zakt uit de ruimte naar beneden, gevecht met zijn transitie.
@ Deoxys-flags gedeeld met Birth Island: FLAG_BATTLED_DEOXYS (gevangen), FLAG_DEFEATED_DEOXYS (verslagen; terug na de League).

MeteorSpace_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MeteorSpace_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, MeteorSpace_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, MeteorSpace_OnFrame
	.byte 0

MeteorSpace_OnTransition:
	setflag FLAG_HIDE_DEOXYS
	setflag FLAG_HIDE_BIRTH_ISLAND_DEOXYS_TRIANGLE
	goto_if_set FLAG_BATTLED_DEOXYS, MeteorSpace_EventScript_End
	goto_if_set FLAG_DEFEATED_DEOXYS, MeteorSpace_EventScript_End
	clearflag FLAG_HIDE_BIRTH_ISLAND_DEOXYS_TRIANGLE
	end

MeteorSpace_EventScript_End::
	end

MeteorSpace_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, MeteorSpace_EventScript_TryRemoveDeoxys
	end

MeteorSpace_EventScript_TryRemoveDeoxys::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject LOCALID_METEOR_SPACE_DEOXYS
	return

MeteorSpace_OnFrame:
	map_script_2 VAR_TEMP_2, 0, MeteorSpace_EventScript_Landed
	.2byte 0

MeteorSpace_EventScript_Landed::
	lockall
	setvar VAR_TEMP_2, 1
	delay 30
	goto_if_set FLAG_METEOR_SPACE_RETURNED, MeteorSpace_EventScript_LandedAgain
	msgbox MeteorSpace_Text_Landed, MSGBOX_DEFAULT
	releaseall
	end

MeteorSpace_EventScript_LandedAgain::
	msgbox MeteorSpace_Text_LandedAgain, MSGBOX_DEFAULT
	releaseall
	end

@ ---------------------------------------------------------------- de radio van het Space Center
MeteorSpace_EventScript_Radio1::
	lockall
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_METEOR_SPACE_RETURNED, MeteorSpace_EventScript_RadioDone
	playse SE_POKENAV_CALL
	waitse
	msgbox MeteorSpace_Text_Radio1, MSGBOX_DEFAULT
	releaseall
	end

MeteorSpace_EventScript_Radio2::
	lockall
	setvar VAR_TEMP_1, 2
	goto_if_set FLAG_METEOR_SPACE_RETURNED, MeteorSpace_EventScript_RadioDone
	playse SE_POKENAV_CALL
	waitse
	msgbox MeteorSpace_Text_Radio2, MSGBOX_DEFAULT
	releaseall
	end

MeteorSpace_EventScript_Radio3::
	lockall
	setvar VAR_TEMP_1, 3
	goto_if_set FLAG_BATTLED_DEOXYS, MeteorSpace_EventScript_RadioDone
	goto_if_set FLAG_DEFEATED_DEOXYS, MeteorSpace_EventScript_RadioDone
	playse SE_POKENAV_CALL
	waitse
	msgbox MeteorSpace_Text_Radio3, MSGBOX_DEFAULT
	releaseall
	end

MeteorSpace_EventScript_RadioDone::
	releaseall
	end

@ ---------------------------------------------------------------- de landingscapsule (terug naar huis)
MeteorSpace_EventScript_LandingBox::
	lock
	msgbox MeteorSpace_Text_BoxGoHome, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MeteorSpace_EventScript_BoxStay
	msgbox MeteorSpace_Text_BoxClimbIn, MSGBOX_DEFAULT
	closemessage
	goto MeteorSpace_EventScript_WarpHome
	end

MeteorSpace_EventScript_BoxStay::
	release
	end

MeteorSpace_EventScript_WarpHome::
	setflag FLAG_METEOR_SPACE_RETURNED
	playse SE_M_TELEPORT
	waitse
	warpwhitefade MAP_MOSSDEEP_CITY_SPACE_CENTER_1F, 2, 3
	waitstate
	end

@ ---------------------------------------------------------------- de driehoek en Deoxys
MeteorSpace_EventScript_Triangle::
	lock
	faceplayer
	msgbox MeteorSpace_Text_Triangle, MSGBOX_DEFAULT
	closemessage
	waitse
	setfieldeffectargument 0, LOCALID_METEOR_SPACE_TRIANGLE
	setfieldeffectargument 1, MAP_NUM(MAP_METEOR_SPACE)
	setfieldeffectargument 2, MAP_GROUP(MAP_METEOR_SPACE)
	dofieldeffect FLDEFF_DESTROY_DEOXYS_ROCK
	playbgm MUS_RG_ENCOUNTER_DEOXYS, FALSE
	waitfieldeffect FLDEFF_DESTROY_DEOXYS_ROCK
	addobject LOCALID_METEOR_SPACE_DEOXYS
	applymovement LOCALID_METEOR_SPACE_DEOXYS, MeteorSpace_Movement_DeoxysApproach
	waitmovement 0
	waitse
	playmoncry SPECIES_DEOXYS_NORMAL, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setvar VAR_LAST_TALKED, LOCALID_METEOR_SPACE_DEOXYS
	seteventmon SPECIES_DEOXYS_NORMAL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MeteorSpace_EventScript_DefeatedDeoxys
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MeteorSpace_EventScript_RanFromDeoxys
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MeteorSpace_EventScript_RanFromDeoxys
	setflag FLAG_BATTLED_DEOXYS
	goto MeteorSpace_EventScript_RadioPickup
	end

MeteorSpace_EventScript_DefeatedDeoxys::
	setflag FLAG_DEFEATED_DEOXYS
	goto MeteorSpace_EventScript_DeoxysFlewAway
	end

MeteorSpace_EventScript_RanFromDeoxys::
	goto MeteorSpace_EventScript_DeoxysFlewAway
	end

MeteorSpace_EventScript_DeoxysFlewAway::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_METEOR_SPACE_DEOXYS
	fadescreenswapbuffers FADE_FROM_BLACK
	setvar VAR_0x8004, SPECIES_DEOXYS_NORMAL
	bufferspeciesname STR_VAR_1, VAR_0x8004
	msgbox gText_LegendaryFlewAway, MSGBOX_DEFAULT
	goto MeteorSpace_EventScript_RadioPickup
	end

MeteorSpace_EventScript_RadioPickup::
	playse SE_POKENAV_CALL
	waitse
	msgbox MeteorSpace_Text_RadioPickup, MSGBOX_DEFAULT
	closemessage
	goto MeteorSpace_EventScript_WarpHome
	end

MeteorSpace_Movement_DeoxysApproach:
	walk_slow_down
	walk_slow_down
	walk_slow_down
	walk_slow_down
	walk_slow_down
	walk_slow_down
	step_end

@ ---------------------------------------------------------------- zwevende Pokémon in de leegte
MeteorSpace_EventScript_FloatingMinior::
	lock
	faceplayer
	playmoncry SPECIES_MINIOR, CRY_MODE_NORMAL
	msgbox MeteorSpace_Text_FloatingMinior, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MeteorSpace_EventScript_FloatingLunatone::
	lock
	playmoncry SPECIES_LUNATONE, CRY_MODE_NORMAL
	msgbox MeteorSpace_Text_FloatingLunatone, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MeteorSpace_EventScript_FloatingSolrock::
	lock
	playmoncry SPECIES_SOLROCK, CRY_MODE_NORMAL
	msgbox MeteorSpace_Text_FloatingSolrock, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MeteorSpace_EventScript_FloatingElgyem::
	lock
	faceplayer
	playmoncry SPECIES_ELGYEM, CRY_MODE_NORMAL
	msgbox MeteorSpace_Text_FloatingElgyem, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MeteorSpace_EventScript_FloatingBeheeyem::
	lock
	faceplayer
	playmoncry SPECIES_BEHEEYEM, CRY_MODE_NORMAL
	msgbox MeteorSpace_Text_FloatingBeheeyem, MSGBOX_DEFAULT
	waitmoncry
	release
	end

@ ---------------------------------------------------------------- teksten (placeholders; Jordi herschrijft)
MeteorSpace_Text_Landed:
	.string "…kssht… Space Center to CHAMPION.\n"
	.string "Landing confirmed! Well, an impact was\l"
	.string "confirmed. Same thing.\p"
	.string "The DNA signal comes from somewhere\n"
	.string "further up. Follow it.\p"
	.string "Want to come home? Climb back into the\n"
	.string "box. Somebody down here will pull the\l"
	.string "string.$"

MeteorSpace_Text_LandedAgain:
	.string "…kssht… Impact confirmed. Again. You're\n"
	.string "getting good at this.\p"
	.string "The box is where you left it. Mostly.$"

MeteorSpace_Text_Radio1:
	.string "…kssht… Space Center here. You're still\n"
	.string "alive! That's 50 BP we owe the intern.\p"
	.string "The meteorite is crawling with POKéMON.\n"
	.string "Please don't bring any home without a\l"
	.string "permit. We don't have permits.$"

MeteorSpace_Text_Radio2:
	.string "…kssht… Small update. If you look down,\n"
	.string "the blue ball is Hoenn. If you look up,\l"
	.string "that's nothing. Space is mostly nothing.\p"
	.string "We thought you'd want to know. Our\n"
	.string "therapist says we should share more.$"

MeteorSpace_Text_Radio3:
	.string "…kssht… You're close to the strongest\n"
	.string "signal. Whatever it is, it's red, it's\l"
	.string "pointy and it really doesn't like us.\p"
	.string "Please be careful. The box isn't\n"
	.string "insured.$"

MeteorSpace_Text_BoxGoHome:
	.string "The Space Center's landing capsule. A\n"
	.string "cardboard box that says FRAGILE. It's a\l"
	.string "little dented now.\p"
	.string "Climb back in and return to Earth?$"

MeteorSpace_Text_BoxClimbIn:
	.string "You fold yourself into the box.\p"
	.string "Far below, somebody pulls a very long\n"
	.string "string.$"

MeteorSpace_Text_Triangle:
	.string "A red triangle, humming in the dark.\p"
	.string "It's sending the DNA-shaped signal. It\n"
	.string "also seems to be sending a very rude\l"
	.string "one.$"

MeteorSpace_Text_RadioPickup:
	.string "…kssht… WHOA. Every needle in this room\n"
	.string "just hit the ceiling. Did you just…\p"
	.string "Never mind. We're pulling you back now.\n"
	.string "Hold your breath. It doesn't help, but it\l"
	.string "makes us feel better.$"

MeteorSpace_Text_FloatingMinior:
	.string "MINIOR drifts past in the void.\p"
	.string "It doesn't care about you at all.$"

MeteorSpace_Text_FloatingLunatone:
	.string "LUNATONE is floating in space, looking\n"
	.string "very smug about it.$"

MeteorSpace_Text_FloatingSolrock:
	.string "SOLROCK spins slowly in the void. It's\n"
	.string "showing off.$"

MeteorSpace_Text_FloatingElgyem:
	.string "ELGYEM stares at you. Its fingers blink\n"
	.string "in a pattern.\p"
	.string "Probably rude.$"

MeteorSpace_Text_FloatingBeheeyem:
	.string "BEHEEYEM is taking notes about you.\p"
	.string "It underlines something. Twice.$"
