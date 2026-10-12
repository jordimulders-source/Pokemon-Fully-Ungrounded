@ Project Grounded: de meteorietkern (kaart: tools/grounded/maptools/meteor_falls_ext.py).
@ Vijf Minior (FLAG_TEMP_1-5, komen terug bij opnieuw binnenkomen) en een vaste Salamence (lv 55).

MeteorFalls_StarCore_MapScripts::
	.byte 0

MeteorFalls_StarCore_EventScript_Meteorite::
	msgbox MeteorFalls_StarCore_Text_Meteorite, MSGBOX_SIGN
	end

MeteorFalls_StarCore_EventScript_Salamence::
	lock
	faceplayer
	msgbox MeteorFalls_StarCore_Text_Salamence, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_SALAMENCE, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_SALAMENCE, 80
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MeteorFalls_StarCore_EventScript_SalamenceStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MeteorFalls_StarCore_EventScript_SalamenceStays
	removeobject LOCALID_STAR_CORE_SALAMENCE
	setflag FLAG_HIDE_METEOR_FALLS_SALAMENCE
MeteorFalls_StarCore_EventScript_SalamenceStays::
	release
	end

MeteorFalls_StarCore_EventScript_Minior1::
	lock
	call MeteorFalls_StarCore_EventScript_MiniorBattle
	removeobject LOCALID_STAR_CORE_MINIOR_1
	setflag FLAG_TEMP_1
	release
	end

MeteorFalls_StarCore_EventScript_Minior2::
	lock
	call MeteorFalls_StarCore_EventScript_MiniorBattle
	removeobject LOCALID_STAR_CORE_MINIOR_2
	setflag FLAG_TEMP_2
	release
	end

MeteorFalls_StarCore_EventScript_Minior3::
	lock
	call MeteorFalls_StarCore_EventScript_MiniorBattle
	removeobject LOCALID_STAR_CORE_MINIOR_3
	setflag FLAG_TEMP_3
	release
	end

MeteorFalls_StarCore_EventScript_Minior4::
	lock
	call MeteorFalls_StarCore_EventScript_MiniorBattle
	removeobject LOCALID_STAR_CORE_MINIOR_4
	setflag FLAG_TEMP_4
	release
	end

MeteorFalls_StarCore_EventScript_Minior5::
	lock
	call MeteorFalls_StarCore_EventScript_MiniorBattle
	removeobject LOCALID_STAR_CORE_MINIOR_5
	setflag FLAG_TEMP_5
	release
	end

MeteorFalls_StarCore_EventScript_MiniorBattle::
	playmoncry SPECIES_MINIOR_METEOR, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MINIOR_METEOR, 74
	dowildbattle
	return

MeteorFalls_StarCore_Text_Meteorite:
	.string "A fragment of the meteor that made\n"
	.string "Meteor Falls. It hums.\p"
	.string "Either that's cosmic energy, or a\n"
	.string "Minior is stuck inside. Again.$"

MeteorFalls_StarCore_Text_Salamence:
	.string "A Salamence is curled around the\n"
	.string "heart of the meteorite.\p"
	.string "It spent its whole childhood as a\n"
	.string "Bagon, headbutting this rock.\p"
	.string "It won. The rock lost. It would like\n"
	.string "you to know that.$"
