GhostShip_Corridors_MapScripts::
	.byte 0

GhostShip_Corridors_EventScript_Ned::
	trainerbattle_single TRAINER_GHOST_SAILOR_NED, GhostShip_Corridors_Text_NedIntro, GhostShip_Corridors_Text_NedDefeat
	msgbox GhostShip_Corridors_Text_NedPostBattle, MSGBOX_AUTOCLOSE
	end

@ staat op de plek van de trap naar B1F (die is in deze kopie dichtgemaakt)
GhostShip_Corridors_EventScript_Deckhand::
	msgbox GhostShip_Corridors_Text_Deckhand, MSGBOX_NPC
	end

GhostShip_Corridors_Text_NedIntro:
	.string "Today's special is soup. Yesterday's\n"
	.string "special was soup.\p"
	.string "The special of 1793 was also soup. Want\n"
	.string "to fight about it?$"

GhostShip_Corridors_Text_NedDefeat:
	.string "The soup was the friends we made along\n"
	.string "the way.$"

GhostShip_Corridors_Text_NedPostBattle:
	.string "My POLTEAGEIST used to be a perfectly\n"
	.string "normal cup of tea.\p"
	.string "Then it spent a century in my galley. We\n"
	.string "all change.$"

GhostShip_Corridors_Text_Deckhand:
	.string "The stairs to B1F? Flooded. Since 1887.\p"
	.string "We put up a sign. The sign also drowned.$"
