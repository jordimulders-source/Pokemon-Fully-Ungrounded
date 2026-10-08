@ Project Grounded: de ijzige onderlaag van Shoal Cave (bij eb). Layout: kopie van ColdstepCave_IceRoom2.
@ Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
ShoalCave_LowTideFrozenDepths_MapScripts::
	.byte 0

ShoalCave_LowTideFrozenDepths_EventScript_Hole::
	msgbox ShoalCave_LowTideFrozenDepths_Text_Hole, MSGBOX_SIGN
	end

ShoalCave_LowTideFrozenDepths_EventScript_Tally::
	msgbox ShoalCave_LowTideFrozenDepths_Text_Tally, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ShoalCave_LowTideFrozenDepths_Text_Hole:
	.string "A big CETODDLE-shaped hole in the ice\n"
	.string "wall.\p"
	.string "The CETODDLE that made it is nowhere to\n"
	.string "be seen. The hole looks very proud of\l"
	.string "itself.$"

ShoalCave_LowTideFrozenDepths_Text_Tally:
	.string "Tally marks scratched into the ice.\n"
	.string "Hundreds of them.\p"
	.string "At the very end:\n"
	.string "“DAY 412. THE TIDE CAME BACK. I DID\l"
	.string "NOT.”$"
