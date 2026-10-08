SafariZone_Southwest_MapScripts::
	.byte 0

SafariZone_Southwest_EventScript_Woman::
	msgbox SafariZone_Southwest_Text_Woman, MSGBOX_NPC
	end

SafariZone_Southwest_EventScript_RestHouseSign::
	msgbox SafariZone_Southwest_Text_RestHouseSign, MSGBOX_SIGN
	end


@ Project Grounded: afzetting voor de Fairy Forest (weg met FLAG_SAFARI_ZONES_OPEN; tools/grounded/maptools/safari_zones.py)
SafariZone_Southwest_EventScript_FairyGuard::
	msgbox SafariZone_Southwest_Text_FairyGuard, MSGBOX_NPC
	end

SafariZone_Southwest_Text_FairyGuard:
	.string "Sorry, the FAIRY FOREST is closed.\p"
	.string "Someone stole the zone keys. A man\n"
	.string "in black, with a big red R on his\l"
	.string "shirt.\p"
	.string "He said the R stood for “Ranger.”\n"
	.string "We believed him. We are not a\l"
	.string "smart organization.$"

@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---
SafariZone_Southwest_EventScript_KV4Starter::
	msgbox SafariZone_Southwest_Text_KV4Starter, MSGBOX_NPC
	end

SafariZone_Southwest_Text_KV4Starter:
	.string "I'm studying why starter POKéMON\nlive together in the wild here.\pTheory: they were all abandoned by\nchildren who picked the other one.\pThis is a support group.\nPlease don't pick one in front of\lthe others. They talk.$"
@ --- einde kaart_vulling_4 ---
