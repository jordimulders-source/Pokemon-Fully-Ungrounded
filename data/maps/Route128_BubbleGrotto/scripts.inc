@ Project Grounded: luchtbel-grot onder Route 128 (kopie van MarineCave_Entrance). Ingang: zwemgat in
@ Underwater_Route128 (27,19); terug = duiken in de poel. Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
Route128_BubbleGrotto_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route128_BubbleGrotto_OnResume
	.byte 0

Route128_BubbleGrotto_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE128, 27, 20
	setescapewarp MAP_UNDERWATER_ROUTE128, 27, 20
	end

Route128_BubbleGrotto_EventScript_Hermit::
	msgbox Route128_BubbleGrotto_Text_Hermit, MSGBOX_NPC
	end

Route128_BubbleGrotto_EventScript_Bubble::
	msgbox Route128_BubbleGrotto_Text_Bubble, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
Route128_BubbleGrotto_Text_Hermit:
	.string "Air! Real air! Well, recycled air. Mostly\n"
	.string "mine.\p"
	.string "I came down here to study RELICANTH.\n"
	.string "It hasn't changed in a hundred million\l"
	.string "years.\p"
	.string "Neither have I, since 1987. We get along\n"
	.string "great.\p"
	.string "Don't tell the surface about this place.\n"
	.string "They'll want to put a gift shop in it.$"

Route128_BubbleGrotto_Text_Bubble:
	.string "A pocket of trapped air wobbles against\n"
	.string "the ceiling.\p"
	.string "It has been there for centuries. It is\n"
	.string "the oldest bubble in HOENN. It looks\l"
	.string "very tired.$"
