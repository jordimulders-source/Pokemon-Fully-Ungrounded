@ Project Grounded: de trog onder de oostelijke kom van Underwater Route 128 (zwemgat 76,19), op weg naar de
@ zeetempel. Kopie van Underwater_SealedChamber; zeewier in de onderste kom (wilde Pokemon).
@ Bovenkomen op het plateau (12,44) = de tempel, ergens anders = terug naar Route 128.
@ Kaart: tools/grounded/maptools/sea_temple_lugia.py
Underwater_SeaTemple_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, Underwater_SeaTemple_OnDive
	.byte 0

Underwater_SeaTemple_OnDive:
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_ne VAR_0x8004, 12, Underwater_SeaTemple_EventScript_SurfaceRoute128
	goto_if_ne VAR_0x8005, 44, Underwater_SeaTemple_EventScript_SurfaceRoute128
	setdivewarp MAP_SEA_TEMPLE_HALL, 10, 19
	end

Underwater_SeaTemple_EventScript_SurfaceRoute128::
	setdivewarp MAP_ROUTE128, 76, 20
	end

Underwater_SeaTemple_EventScript_Carving::
	msgbox Underwater_SeaTemple_Text_Carving, MSGBOX_SIGN
	end

Underwater_SeaTemple_Text_Carving:
	.string "An arrow is carved into the rock,\n"
	.string "pointing up.\p"
	.string "Underneath it: “TEMPLE. SURFACE HERE.\n"
	.string "NOT THERE. HERE.”\p"
	.string "Someone has scratched below it:\n"
	.string "“I SURFACED THERE.”$"
