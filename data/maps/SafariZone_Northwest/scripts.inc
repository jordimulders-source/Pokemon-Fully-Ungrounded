SafariZone_Northwest_MapScripts::
	.byte 0

SafariZone_Northwest_EventScript_Man::
	msgbox SafariZone_Northwest_Text_Man, MSGBOX_NPC
	end


@ Project Grounded: afzetting voor het Haunted Camp (weg met FLAG_SAFARI_ZONES_OPEN; tools/grounded/maptools/safari_zones.py)
SafariZone_Northwest_EventScript_SpookGuard::
	msgbox SafariZone_Northwest_Text_SpookGuard, MSGBOX_NPC
	end

SafariZone_Northwest_Text_SpookGuard:
	.string "Turn back. The HAUNTED CAMP is\n"
	.string "locked.\p"
	.string "A man in black with a big red R\n"
	.string "stole every zone key we had.\p"
	.string "Out of all the gates in this park,\n"
	.string "he took the key to the haunted one.\p"
	.string "Honestly? Let him keep it.$"
