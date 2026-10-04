ScorchedSlab_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ScorchedSlab_OnTransition
	.byte 0

ScorchedSlab_OnTransition:
	setflag FLAG_LANDMARK_SCORCHED_SLAB
	end


@ Project Grounded: inscriptie naast de nieuwe grotopening naar de zonnezaal (scorched_slab_ext.py).
ScorchedSlab_EventScript_Inscription::
	msgbox ScorchedSlab_Text_Inscription, MSGBOX_SIGN
	end

ScorchedSlab_Text_Inscription:
	.string "An old carving of a sun with legs.\p"
	.string "“TEMPLE OF THE SUN. SHOES OFF.\n"
	.string "SUNGLASSES ON. NO UMBRELLAS.”$"
