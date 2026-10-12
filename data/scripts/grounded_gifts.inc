@ Project Grounded: gedeelde gift-afhandeling en de Deoxys-meteoriet (Mossdeep).

@ Geef een Pokémon: VAR_0x8004 = soort, VAR_0x8005 = level, VAR_0x8006 = vastgehouden item (ITEM_NONE = geen).
@ Team vol: naar de pc. Pc ook vol: melding. VAR_RESULT = TRUE als hij gegeven is, anders FALSE.
Grounded_EventScript_GiveGiftMon::
	copyvar VAR_TEMP_TRANSFERRED_SPECIES, VAR_0x8004
	givemon VAR_0x8004, VAR_0x8005, VAR_0x8006
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Grounded_EventScript_GiftToParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Grounded_EventScript_GiftToPC
	msgbox gText_NoMoreRoomForPokemon, MSGBOX_DEFAULT
	setvar VAR_RESULT, FALSE
	return

Grounded_EventScript_GiftToParty::
	call Grounded_EventScript_GiftFanfare
	setvar VAR_RESULT, TRUE
	return

Grounded_EventScript_GiftToPC::
	call Grounded_EventScript_GiftFanfare
	call Common_EventScript_TransferredToPC
	setvar VAR_RESULT, TRUE
	return

Grounded_EventScript_GiftFanfare::
	bufferspeciesname STR_VAR_2, VAR_0x8004
	playfanfare MUS_OBTAIN_ITEM
	message Grounded_Text_ReceivedGiftMon
	waitmessage
	waitfanfare
	return

@ De meteoriet in Mossdeep: met een Deoxys in het team kies je zijn vorm (Grounded_FindPartyDeoxys/SetDeoxysForm).
Grounded_EventScript_DeoxysMeteorite::
	lockall
	copyvar VAR_0x8004, VAR_RESULT
	bufferpartymonnick STR_VAR_1, VAR_0x8004
	msgbox Grounded_Text_DeoxysMeteorite, MSGBOX_DEFAULT
	message Grounded_Text_DeoxysWhichForm
	waitmessage
	dynmultichoice 19, 1, TRUE, 5, 0, DYN_MULTICHOICE_CB_NONE, Grounded_Text_DeoxysOptNormal, Grounded_Text_DeoxysOptAttack, Grounded_Text_DeoxysOptDefense, Grounded_Text_DeoxysOptSpeed, Grounded_Text_DeoxysOptLeave
	goto_if_ge VAR_RESULT, 4, Grounded_EventScript_DeoxysLeave
	goto_if_eq VAR_RESULT, VAR_0x8005, Grounded_EventScript_DeoxysSameForm
	copyvar VAR_0x8005, VAR_RESULT
	closemessage
	playse SE_M_COSMIC_POWER
	fadescreen FADE_TO_WHITE
	special Grounded_SetDeoxysForm
	waitse
	fadescreen FADE_FROM_WHITE
	playmoncry SPECIES_DEOXYS, CRY_MODE_NORMAL
	waitmoncry
	msgbox Grounded_Text_DeoxysChanged, MSGBOX_DEFAULT
	releaseall
	end

Grounded_EventScript_DeoxysSameForm::
	msgbox Grounded_Text_DeoxysSameForm, MSGBOX_DEFAULT
	releaseall
	end

Grounded_EventScript_DeoxysLeave::
	msgbox Grounded_Text_DeoxysLeave, MSGBOX_DEFAULT
	releaseall
	end
