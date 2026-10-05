@ Project Grounded: Ogerpon-quest (post-game). Munkidori zit hier met de Hearthflame Mask.
@ Kaart: tools/grounded/maptools/ogerpon_quest.py. Verslagen = terug na de League (hall_of_fame.inc), gevangen = weg.
@ Het masker krijg je bij de eerste overwinning of vangst; daarna is het een gewone rematch.
FieryPath_EmberHollow_MapScripts::
	.byte 0

FieryPath_EmberHollow_EventScript_Munkidori::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HEARTHFLAME_MASK, FieryPath_EmberHollow_EventScript_MunkidoriBattle
	msgbox FieryPath_EmberHollow_Text_Munkidori, MSGBOX_DEFAULT
	closemessage
FieryPath_EmberHollow_EventScript_MunkidoriBattle::
	playmoncry SPECIES_MUNKIDORI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MUNKIDORI, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FieryPath_EmberHollow_EventScript_MunkidoriCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FieryPath_EmberHollow_EventScript_MunkidoriDefeated
	msgbox FieryPath_EmberHollow_Text_MunkidoriStays, MSGBOX_DEFAULT
	release
	end

FieryPath_EmberHollow_EventScript_MunkidoriCaught::
	setflag FLAG_CAUGHT_MUNKIDORI
FieryPath_EmberHollow_EventScript_MunkidoriDefeated::
	setflag FLAG_DEFEATED_MUNKIDORI
	removeobject LOCALID_EMBER_HOLLOW_MUNKIDORI
	call_if_unset FLAG_RECEIVED_HEARTHFLAME_MASK, FieryPath_EmberHollow_EventScript_GetMask
	release
	end

FieryPath_EmberHollow_EventScript_GetMask::
	msgbox FieryPath_EmberHollow_Text_MaskDropped, MSGBOX_DEFAULT
	giveitem ITEM_HEARTHFLAME_MASK
	setflag FLAG_RECEIVED_HEARTHFLAME_MASK
	msgbox FieryPath_EmberHollow_Text_MaskHint, MSGBOX_DEFAULT
	return

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
FieryPath_EmberHollow_Text_Munkidori:
	.string "MUNKIDORI is warming its hands on\n"
	.string "a mask that is very much on fire.\p"
	.string "It stares into your mind. It finds\n"
	.string "nothing worth stealing. Rude.\p"
	.string "“Heroes,” it thinks at you.\n"
	.string "“Statues. Parades. Free snacks.\l"
	.string "Nobody ever asks the ogre.”$"

FieryPath_EmberHollow_Text_MunkidoriStays:
	.string "MUNKIDORI is still here. So is the\n"
	.string "migraine it gave you.$"

FieryPath_EmberHollow_Text_MaskDropped:
	.string "The HEARTHFLAME MASK clatters onto\n"
	.string "the rock, still smoldering.$"

FieryPath_EmberHollow_Text_MaskHint:
	.string "The old lady at the altar in\n"
	.string "FORTREE JUNGLE wants it back.\l"
	.string "So does everyone, apparently.$"
