@ Project Grounded: Scorched Slab, Koele bron onder de zonnezaal. Diep water (Dive) naar Underwater_ScorchedSlab.
ScorchedSlab_Spring_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, ScorchedSlab_Spring_OnResume
	.byte 0

ScorchedSlab_Spring_OnResume:
	setdivewarp MAP_UNDERWATER_SCORCHED_SLAB, 8, 6
	end

ScorchedSlab_Spring_EventScript_Marco::
	trainerbattle_single TRAINER_SLAB_MARCO, ScorchedSlab_Spring_Text_MarcoIntro, ScorchedSlab_Spring_Text_MarcoDefeat
	msgbox ScorchedSlab_Spring_Text_MarcoPostBattle, MSGBOX_AUTOCLOSE
	end

ScorchedSlab_Spring_EventScript_Plaque::
	msgbox ScorchedSlab_Spring_Text_Plaque, MSGBOX_SIGN
	end

ScorchedSlab_Spring_Text_MarcoIntro:
	.string "Is this the ocean? Tell me this is\n"
	.string "the ocean.\p"
	.string "I dove off ROUTE 120 three weeks ago\n"
	.string "and kept swimming. My GPS says I'm\l"
	.string "inside a rock.$"

ScorchedSlab_Spring_Text_MarcoDefeat:
	.string "Lost the battle. Lost my way.\n"
	.string "Consistent, at least.$"

ScorchedSlab_Spring_Text_MarcoPostBattle:
	.string "There's a dark spot in the water.\n"
	.string "Deep. Very deep.\p"
	.string "If you can DIVE, go look. If you\n"
	.string "find a guy named MARCO down there,\l"
	.string "that's my ghost. Tell him hi.$"

ScorchedSlab_Spring_Text_Plaque:
	.string "A plaque, worn smooth by steam:\p"
	.string "“HOLY SPRING. FOR COOLING DOWN\n"
	.string "AFTER WORSHIP. NO PEEING.”\p"
	.string "Someone scratched a tally under\n"
	.string "it. It's very long.$"
