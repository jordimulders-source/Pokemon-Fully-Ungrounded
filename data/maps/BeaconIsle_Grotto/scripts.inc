@ Project Grounded: de grot op het Lichteiland achter het rif van Beacon Isle (layout: Steven's kamer in
@ Granite Cave, gedeeld). TALLOW, de geest van de eerste vuurtorenwachter (1952-1953), en zeldzame wilde soorten.
@ Kaart en scripts: tools/grounded/maptools/beacon_isle.py. Teksten zijn placeholders.
BeaconIsle_Grotto_MapScripts::
	.byte 0

BeaconIsle_Grotto_EventScript_Tallow::
	trainerbattle_single TRAINER_TALLOW, BeaconIsle_Grotto_Text_TallowIntro, BeaconIsle_Grotto_Text_TallowDefeat, BeaconIsle_Grotto_EventScript_TallowDefeated
	msgbox BeaconIsle_Grotto_Text_TallowPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_Grotto_EventScript_TallowDefeated::
	msgbox BeaconIsle_Grotto_Text_TallowGift, MSGBOX_DEFAULT
	giveitem ITEM_DUSK_STONE
	msgbox BeaconIsle_Grotto_Text_TallowPost, MSGBOX_DEFAULT
	release
	end

BeaconIsle_Grotto_EventScript_Candles::
	msgbox BeaconIsle_Grotto_Text_Candles, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
BeaconIsle_Grotto_Text_TallowGift:
	.string "Take this. Hold it up to a LAMPENT and\n"
	.string "something wonderful happens.\p"
	.string "Hold it up to a lighthouse and nothing\n"
	.string "happens. I've checked. For seventy\l"
	.string "years.$"

BeaconIsle_Grotto_Text_TallowIntro:
	.string "...Oh! A visitor. Forgive me, I'm a little\n"
	.string "transparent today.\p"
	.string "I am TALLOW, first keeper of the BEACON\n"
	.string "ISLE LIGHT. 1952 to 1953. Mostly 1953.\p"
	.string "I broke the lamp. I was trying to make it\n"
	.string "brighter. I made it a candle.\p"
	.string "Seventy years I've practised in this\n"
	.string "cave. Let me show you real light!$"

BeaconIsle_Grotto_Text_TallowDefeat:
	.string "...Even a ghost can be outshone. How\n"
	.string "embarrassing.$"

BeaconIsle_Grotto_Text_TallowPost:
	.string "Tell WICK the fish is doing a better job\n"
	.string "than I ever did.\p"
	.string "Don't tell him I said that. Tell him I'm\n"
	.string "haunting him. Professionally.$"

BeaconIsle_Grotto_Text_Candles:
	.string "Hundreds of melted candles, in neat\n"
	.string "rows.\p"
	.string "Every one has a little label:\n"
	.string "“BRIGHTER?”$"
