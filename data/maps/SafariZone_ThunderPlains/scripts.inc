@ Project Grounded: Safari Zone, Thunder Plains (kaart en tileset: tools/grounded/maptools/safari_zones.py)
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.

SafariZone_ThunderPlains_MapScripts::
	.byte 0

SafariZone_ThunderPlains_EventScript_Sign::
	msgbox SafariZone_ThunderPlains_Text_Sign, MSGBOX_SIGN
	end

SafariZone_ThunderPlains_Text_Sign:
	.string "SAFARI ZONE - THUNDER PLAINS\p"
	.string "In case of lightning: you are the\n"
	.string "tallest thing out here.\l"
	.string "Think about that.\p"
	.string "The management is not responsible\n"
	.string "for new hairstyles.$"

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
SafariZone_ThunderPlains_EventScript_LVLightning::
	msgbox SafariZone_ThunderPlains_Text_LVLightning, MSGBOX_NPC
	end

SafariZone_ThunderPlains_Text_LVLightning:
	.string "I study lightning. Up close.\nWith this metal rod.\pI've been struck fourteen times.\nMy theory: it likes me.\pMy hair has a theory too.\nIt points straight up.$"
@ --- einde land_vulling ---
