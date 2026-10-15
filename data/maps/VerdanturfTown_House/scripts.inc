VerdanturfTown_House_MapScripts::
	.byte 0

@ Project Grounded: eenmalige item-giveaway (testrun Jordi)
VerdanturfTown_House_EventScript_Woman1::
	lock
	faceplayer
	msgbox VerdanturfTown_House_Text_TrainersGatherAtPokemonLeague, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_VERDANTURF_HOUSE_GIFT, VerdanturfTown_House_EventScript_Woman1_GiftDone
	msgbox VerdanturfTown_House_Text_TakeMetronome, MSGBOX_DEFAULT
	giveitem ITEM_METRONOME
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_VERDANTURF_HOUSE_GIFT
VerdanturfTown_House_EventScript_Woman1_GiftDone::
	release
	end

VerdanturfTown_House_EventScript_Woman2::
	msgbox VerdanturfTown_House_Text_DefeatEliteFourInARow, MSGBOX_NPC
	end

VerdanturfTown_House_Text_TrainersGatherAtPokemonLeague:
	.string "SABRINA CARPENTER is the best.\n"
	.string "Espresso! Short n' Sweet!\p"
	.string "TAYLOR SWIFT has had, what, eleven\n"
	.string "eras? Pick one, Taylor.$"

VerdanturfTown_House_Text_DefeatEliteFourInARow:
	.string "TAYLOR SWIFT is a generational talent.\n"
	.string "Eleven eras, because she's a GENIUS.\p"
	.string "SABRINA is just… short. And sweet.\n"
	.string "That's it. That's the whole thing.$"

VerdanturfTown_House_Text_TakeMetronome:
	.string "Here, a METRONOME. It powers up a\n"
	.string "move you keep using in a row.\p"
	.string "Like ESPRESSO on repeat. Forever.\n"
	.string "Don't tell the Swiftie over there.$"
