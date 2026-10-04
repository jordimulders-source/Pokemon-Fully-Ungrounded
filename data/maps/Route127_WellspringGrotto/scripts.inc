@ Project Grounded: Ogerpon-quest (post-game). Fezandipiti zit hier met de Wellspring Mask.
@ Kaart: tools/grounded/maptools/ogerpon_quest.py. Verslagen = terug na de League (hall_of_fame.inc), gevangen = weg.
@ Het masker krijg je bij de eerste overwinning of vangst; daarna is het een gewone rematch.
Route127_WellspringGrotto_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route127_WellspringGrotto_OnResume
	.byte 0

@ duiken in de poel = terug naar het zwemgat in Underwater_Route127
Route127_WellspringGrotto_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE127, 72, 46
	setescapewarp MAP_UNDERWATER_ROUTE127, 72, 46
	end

Route127_WellspringGrotto_EventScript_Fezandipiti::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_WELLSPRING_MASK, Route127_WellspringGrotto_EventScript_FezandipitiBattle
	msgbox Route127_WellspringGrotto_Text_Fezandipiti, MSGBOX_DEFAULT
	closemessage
Route127_WellspringGrotto_EventScript_FezandipitiBattle::
	playmoncry SPECIES_FEZANDIPITI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_FEZANDIPITI, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Route127_WellspringGrotto_EventScript_FezandipitiCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Route127_WellspringGrotto_EventScript_FezandipitiDefeated
	msgbox Route127_WellspringGrotto_Text_FezandipitiStays, MSGBOX_DEFAULT
	release
	end

Route127_WellspringGrotto_EventScript_FezandipitiCaught::
	setflag FLAG_CAUGHT_FEZANDIPITI
Route127_WellspringGrotto_EventScript_FezandipitiDefeated::
	setflag FLAG_DEFEATED_FEZANDIPITI
	removeobject LOCALID_WELLSPRING_GROTTO_FEZANDIPITI
	call_if_unset FLAG_RECEIVED_WELLSPRING_MASK, Route127_WellspringGrotto_EventScript_GetMask
	release
	end

Route127_WellspringGrotto_EventScript_GetMask::
	msgbox Route127_WellspringGrotto_Text_MaskDropped, MSGBOX_DEFAULT
	giveitem ITEM_WELLSPRING_MASK
	setflag FLAG_RECEIVED_WELLSPRING_MASK
	msgbox Route127_WellspringGrotto_Text_MaskHint, MSGBOX_DEFAULT
	return

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
Route127_WellspringGrotto_Text_Fezandipiti:
	.string "FEZANDIPITI is admiring itself in\n"
	.string "the pool, wearing a stolen mask\l"
	.string "as a fashion statement.\p"
	.string "It has been doing this for roughly\n"
	.string "four hundred years.\p"
	.string "The village built it a statue.\n"
	.string "It still thinks the statue is\l"
	.string "too small.$"

Route127_WellspringGrotto_Text_FezandipitiStays:
	.string "FEZANDIPITI goes back to its\n"
	.string "reflection. You were never here.$"

Route127_WellspringGrotto_Text_MaskDropped:
	.string "The WELLSPRING MASK slips off and\n"
	.string "floats ashore. Finders keepers.$"

Route127_WellspringGrotto_Text_MaskHint:
	.string "The old lady at the altar in\n"
	.string "FORTREE JUNGLE wants it back.\l"
	.string "So does everyone, apparently.$"
