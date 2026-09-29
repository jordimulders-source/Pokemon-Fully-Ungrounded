DewfordTown_House1_MapScripts::
	.byte 0

DewfordTown_House1_EventScript_Man::
	msgbox DewfordTown_House1_Text_LotToBeSaidForLivingOnIsland, MSGBOX_NPC
	end

DewfordTown_House1_EventScript_Woman::
	msgbox DewfordTown_House1_Text_LifeGoesSlowlyOnIsland, MSGBOX_NPC
	end

DewfordTown_House1_EventScript_Zigzagoon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
	msgbox DewfordTown_House1_Text_Zigzagoon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

DewfordTown_House1_Text_LotToBeSaidForLivingOnIsland:
	.string "There's a lot to be said for living on a\n"
	.string "small island in harmony with the family.\p"
	.string "…Why is everyone in town looking at me\n"
	.string "like that? Did someone say something?\l"
	.string "Who said something?$"

DewfordTown_House1_Text_LifeGoesSlowlyOnIsland:
	.string "I left SLATEPORT CITY to marry my\n"
	.string "husband and live on this little island.\p"
	.string "Lately he's been coming home late,\n"
	.string "smelling like glitter and stage fog. He\l"
	.string "says it's from fishing.\p"
	.string "Everyone in town keeps giving me\n"
	.string "casseroles. I don't know why. I'm not\l"
	.string "sick.$"

DewfordTown_House1_Text_Zigzagoon:
	.string "ZIGZAGOON: Guguuh!\p"
	.string "It glances at RANDY, then at you, then\n"
	.string "does a slow little shoulder shimmy. It\l"
	.string "winks.\p"
	.string "It knows. It definitely knows.$"

