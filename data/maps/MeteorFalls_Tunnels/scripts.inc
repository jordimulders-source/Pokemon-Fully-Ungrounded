@ Project Grounded: de Draconid-gangen onder Meteor Falls (kaart: tools/grounded/maptools/meteor_falls_ext.py).
@ Doodlopend knooppunt in het midden: brokkelrots op een gat in de vloer (val naar de Sterrenvalgrot).
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.

MeteorFalls_Tunnels_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, MeteorFalls_Tunnels_OnResume
	.byte 0

MeteorFalls_Tunnels_OnResume:
	setholewarp MAP_METEOR_FALLS_STARFALL_GROTTO
	end

MeteorFalls_Tunnels_EventScript_Boulderman::
	trainerbattle_single TRAINER_METEOR_BOULDERMAN, MeteorFalls_Tunnels_Text_BouldermanIntro, MeteorFalls_Tunnels_Text_BouldermanDefeat
	msgbox MeteorFalls_Tunnels_Text_BouldermanPostBattle, MSGBOX_AUTOCLOSE
	end

MeteorFalls_Tunnels_EventScript_Orion::
	trainerbattle_single TRAINER_METEOR_ORION, MeteorFalls_Tunnels_Text_OrionIntro, MeteorFalls_Tunnels_Text_OrionDefeat
	msgbox MeteorFalls_Tunnels_Text_OrionPostBattle, MSGBOX_AUTOCLOSE
	end

MeteorFalls_Tunnels_EventScript_Vesper::
	trainerbattle_single TRAINER_METEOR_VESPER, MeteorFalls_Tunnels_Text_VesperIntro, MeteorFalls_Tunnels_Text_VesperDefeat
	msgbox MeteorFalls_Tunnels_Text_VesperPostBattle, MSGBOX_AUTOCLOSE
	end

MeteorFalls_Tunnels_EventScript_Nova::
	trainerbattle_single TRAINER_METEOR_NOVA, MeteorFalls_Tunnels_Text_NovaIntro, MeteorFalls_Tunnels_Text_NovaDefeat
	msgbox MeteorFalls_Tunnels_Text_NovaPostBattle, MSGBOX_AUTOCLOSE
	end

MeteorFalls_Tunnels_Text_BouldermanIntro:
	.string "I've been lost in these tunnels since\n"
	.string "the last Hoenn remake.\p"
	.string "Which one? Exactly.$"

MeteorFalls_Tunnels_Text_BouldermanDefeat:
	.string "Left, left, right… No. That's how\n"
	.string "I got here.$"

MeteorFalls_Tunnels_Text_BouldermanPostBattle:
	.string "The Draconids dug these tunnels by\n"
	.string "hand. Or by claw. Or by Bagon.\p"
	.string "Nobody asked the Bagon.$"

MeteorFalls_Tunnels_Text_OrionIntro:
	.string "I foresaw this battle.\p"
	.string "I also foresaw myself winning,\n"
	.string "so please cooperate.$"

MeteorFalls_Tunnels_Text_OrionDefeat:
	.string "My third eye needs glasses.$"

MeteorFalls_Tunnels_Text_OrionPostBattle:
	.string "I sense a hollow somewhere in these\n"
	.string "tunnels. Then again, I also sense\l"
	.string "one in my soul. Hard to tell apart.$"

MeteorFalls_Tunnels_Text_VesperIntro:
	.string "The Draconids raised dragons down\n"
	.string "here for a thousand years.\p"
	.string "I've been doing it for three weeks.\n"
	.string "Same energy.$"

MeteorFalls_Tunnels_Text_VesperDefeat:
	.string "My Haxorus is looking at me like I'm\n"
	.string "the one who should evolve.$"

MeteorFalls_Tunnels_Text_VesperPostBattle:
	.string "There's an old woman in the shrine\n"
	.string "to the northwest.\p"
	.string "She beat me with one hand while\n"
	.string "knitting with the other.$"

MeteorFalls_Tunnels_Text_NovaIntro:
	.string "I study meteorites. Mostly I study\n"
	.string "how much it hurts when one lands\l"
	.string "on you. Let me demonstrate!$"

MeteorFalls_Tunnels_Text_NovaDefeat:
	.string "Extinction-level event. For my team.$"

MeteorFalls_Tunnels_Text_NovaPostBattle:
	.string "The core down the middle hall is\n"
	.string "full of Minior.\p"
	.string "And something big that eats them.\n"
	.string "Bring snacks. Be the snack, maybe.$"
