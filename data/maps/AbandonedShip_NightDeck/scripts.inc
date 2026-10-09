@ Project Grounded: AbandonedShip_NightDeck (gegenereerd door tools/grounded/maptools/abandoned_ship_night.py; niet met de hand bewerken, teksten via de Dialoogstudio)
AbandonedShip_NightDeck_MapScripts::
	.byte 0

AbandonedShip_NightDeck_EventScript_Sign::
	msgbox AbandonedShip_NightDeck_Text_Sign, MSGBOX_SIGN
	end

AbandonedShip_NightDeck_EventScript_Porthole::
	msgbox AbandonedShip_NightDeck_Text_Porthole, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AbandonedShip_NightDeck_Text_Sign:
	.string "LOWER DECK - CREW ONLY\p"
	.string "Crew status: deceased.\n"
	.string "Crew morale: weirdly high.$"

AbandonedShip_NightDeck_Text_Porthole:
	.string "You look through the porthole.\p"
	.string "Something on the other side looks back.\n"
	.string "It waves. It has too many fingers for a\l"
	.string "wave.$"
