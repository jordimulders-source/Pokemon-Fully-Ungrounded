@ Project Grounded: Ogerpon-quest (post-game). Okidogi zit hier met de Cornerstone Mask.
@ Kaart: tools/grounded/maptools/ogerpon_quest.py. Verslagen = terug na de League (hall_of_fame.inc), gevangen = weg.
@ Het masker krijg je bij de eerste overwinning of vangst; daarna is het een gewone rematch.
GraniteCave_CornerstoneRoom_MapScripts::
	.byte 0

GraniteCave_CornerstoneRoom_EventScript_Okidogi::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_CORNERSTONE_MASK, GraniteCave_CornerstoneRoom_EventScript_OkidogiBattle
	msgbox GraniteCave_CornerstoneRoom_Text_Okidogi, MSGBOX_DEFAULT
	closemessage
GraniteCave_CornerstoneRoom_EventScript_OkidogiBattle::
	playmoncry SPECIES_OKIDOGI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_OKIDOGI, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GraniteCave_CornerstoneRoom_EventScript_OkidogiCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GraniteCave_CornerstoneRoom_EventScript_OkidogiDefeated
	msgbox GraniteCave_CornerstoneRoom_Text_OkidogiStays, MSGBOX_DEFAULT
	release
	end

GraniteCave_CornerstoneRoom_EventScript_OkidogiCaught::
	setflag FLAG_CAUGHT_OKIDOGI
GraniteCave_CornerstoneRoom_EventScript_OkidogiDefeated::
	setflag FLAG_DEFEATED_OKIDOGI
	removeobject LOCALID_CORNERSTONE_ROOM_OKIDOGI
	call_if_unset FLAG_RECEIVED_CORNERSTONE_MASK, GraniteCave_CornerstoneRoom_EventScript_GetMask
	release
	end

GraniteCave_CornerstoneRoom_EventScript_GetMask::
	msgbox GraniteCave_CornerstoneRoom_Text_MaskDropped, MSGBOX_DEFAULT
	giveitem ITEM_CORNERSTONE_MASK
	setflag FLAG_RECEIVED_CORNERSTONE_MASK
	msgbox GraniteCave_CornerstoneRoom_Text_MaskHint, MSGBOX_DEFAULT
	return

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
GraniteCave_CornerstoneRoom_Text_Okidogi:
	.string "An OKIDOGI is sitting on a stone\n"
	.string "mask like it's a lawn chair.\p"
	.string "A plaque on the wall reads:\n"
	.string "“HERO OF THE VILLAGE. VERY BRAVE.\l"
	.string "DID NOT STEAL ANYTHING.”\p"
	.string "OKIDOGI wrote the plaque itself.\n"
	.string "In crayon. With its fist.$"

GraniteCave_CornerstoneRoom_Text_OkidogiStays:
	.string "OKIDOGI flexes at you. It's not\n"
	.string "leaving. It pays no rent here.$"

GraniteCave_CornerstoneRoom_Text_MaskDropped:
	.string "OKIDOGI left the CORNERSTONE MASK\n"
	.string "behind. It smells like gym socks.$"

GraniteCave_CornerstoneRoom_Text_MaskHint:
	.string "The old lady at the altar in\n"
	.string "FORTREE JUNGLE wants it back.\l"
	.string "So does everyone, apparently.$"
