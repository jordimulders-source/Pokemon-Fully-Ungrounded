SafariZone_Northeast_MapScripts::
	.byte 0

@ Event scripts for SafariZone_Northeast are in SafariZone_South/scripts.inc

@ Project Grounded: afzetting voor de Thunder Plains (weg met FLAG_SAFARI_ZONES_OPEN; tools/grounded/maptools/safari_zones.py)
SafariZone_Northeast_EventScript_ThunderGuard::
	msgbox SafariZone_Northeast_Text_ThunderGuard, MSGBOX_NPC
	end

SafariZone_Northeast_Text_ThunderGuard:
	.string "The tunnel to the THUNDER PLAINS\n"
	.string "is closed. Lightning, liability,\l"
	.string "the usual.\p"
	.string "Also, a man in black with a big red\n"
	.string "R stole the keys. He was very\l"
	.string "polite about it.\p"
	.string "If you see him, we want our keychain\n"
	.string "back. It had a little PIKACHU on it.$"
