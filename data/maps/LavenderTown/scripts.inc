@ Project Grounded: LavenderTown (tools/grounded/maptools/spacetime_cave.py)
@ Spookstad (eigen paletten, bewolkt) tot FLAG_SPACETIME_LAVENDER_DONE; daarna layout LavenderTown_Calm.
LavenderTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition
	.byte 0

LavenderTown_OnTransition:
	call_if_set FLAG_SPACETIME_LAVENDER_DONE, LavenderTown_EventScript_Calm
	end

LavenderTown_EventScript_Calm:
	setmaplayoutindex LAYOUT_LAVENDER_TOWN_CALM
	setweather WEATHER_NONE
	setflag FLAG_HIDE_LAVENDER_GHOST_GENGAR
	setflag FLAG_HIDE_LAVENDER_GHOST_DUSKNOIR
	setflag FLAG_HIDE_LAVENDER_GHOST_BANETTE
	return

LavenderTown_EventScript_LittleGirl::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_LAVENDER_DONE, LavenderTown_EventScript_LittleGirlAfter
	msgbox LavenderTown_Text_LittleGirl, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_LittleGirlAfter::
	msgbox LavenderTown_Text_LittleGirlAfter, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_Worker::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_LAVENDER_DONE, LavenderTown_EventScript_WorkerAfter
	msgbox LavenderTown_Text_Worker, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_WorkerAfter::
	msgbox LavenderTown_Text_WorkerAfter, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_Boy::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_LAVENDER_DONE, LavenderTown_EventScript_BoyAfter
	msgbox LavenderTown_Text_Boy, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_BoyAfter::
	msgbox LavenderTown_Text_BoyAfter, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_GhostGengar::
	lock
	faceplayer
	playmoncry SPECIES_GENGAR, CRY_MODE_ENCOUNTER
	checkitem ITEM_SILPH_SCOPE
	goto_if_eq VAR_RESULT, FALSE, LavenderTown_EventScript_GhostGengarNoScope
	msgbox LavenderTown_Text_GhostGengar, MSGBOX_DEFAULT
	goto LavenderTown_EventScript_GhostGengarFight

LavenderTown_EventScript_GhostGengarNoScope::
	msgbox LavenderTown_Text_GhostNoScope, MSGBOX_DEFAULT
LavenderTown_EventScript_GhostGengarFight::
	waitmoncry
	closemessage
	setwildbattle SPECIES_GENGAR, 67
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LavenderTown_EventScript_GhostGengarGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LavenderTown_EventScript_GhostGengarGone
	release
	end

LavenderTown_EventScript_GhostGengarGone::
	removeobject LOCALID_LAVENDER_GHOST_GENGAR
	msgbox LavenderTown_Text_GhostGone, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_GhostDusknoir::
	lock
	faceplayer
	playmoncry SPECIES_DUSKNOIR, CRY_MODE_ENCOUNTER
	checkitem ITEM_SILPH_SCOPE
	goto_if_eq VAR_RESULT, FALSE, LavenderTown_EventScript_GhostDusknoirNoScope
	msgbox LavenderTown_Text_GhostDusknoir, MSGBOX_DEFAULT
	goto LavenderTown_EventScript_GhostDusknoirFight

LavenderTown_EventScript_GhostDusknoirNoScope::
	msgbox LavenderTown_Text_GhostNoScope, MSGBOX_DEFAULT
LavenderTown_EventScript_GhostDusknoirFight::
	waitmoncry
	closemessage
	setwildbattle SPECIES_DUSKNOIR, 66
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LavenderTown_EventScript_GhostDusknoirGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LavenderTown_EventScript_GhostDusknoirGone
	release
	end

LavenderTown_EventScript_GhostDusknoirGone::
	removeobject LOCALID_LAVENDER_GHOST_DUSKNOIR
	msgbox LavenderTown_Text_GhostGone, MSGBOX_DEFAULT
	release
	end

LavenderTown_EventScript_GhostBanette::
	lock
	faceplayer
	playmoncry SPECIES_BANETTE, CRY_MODE_ENCOUNTER
	checkitem ITEM_SILPH_SCOPE
	goto_if_eq VAR_RESULT, FALSE, LavenderTown_EventScript_GhostBanetteNoScope
	msgbox LavenderTown_Text_GhostBanette, MSGBOX_DEFAULT
	goto LavenderTown_EventScript_GhostBanetteFight

LavenderTown_EventScript_GhostBanetteNoScope::
	msgbox LavenderTown_Text_GhostNoScope, MSGBOX_DEFAULT
LavenderTown_EventScript_GhostBanetteFight::
	waitmoncry
	closemessage
	setwildbattle SPECIES_BANETTE, 66
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LavenderTown_EventScript_GhostBanetteGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LavenderTown_EventScript_GhostBanetteGone
	release
	end

LavenderTown_EventScript_GhostBanetteGone::
	removeobject LOCALID_LAVENDER_GHOST_BANETTE
	msgbox LavenderTown_Text_GhostGone, MSGBOX_DEFAULT
	release
	end


LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_TownSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_TowerSign::
	msgbox LavenderTown_Text_TowerSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_HouseSign::
	msgbox LavenderTown_Text_HouseSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_Notice::
	msgbox LavenderTown_Text_Notice, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
LavenderTown_Text_LittleGirl:
	.string "Do you believe in ghosts?\p"
	.string "My mom says they're just POKéMON. My\n"
	.string "dad says they're just POKéMON with\l"
	.string "unfinished business.\p"
	.string "The one in front of the TOWER has a LOT\n"
	.string "of unfinished business.$"

LavenderTown_Text_LittleGirlAfter:
	.string "The bad ghosts are gone! Now it's just\n"
	.string "the regular ghosts.\p"
	.string "The regular ghosts are fine. They do\n"
	.string "the dishes. Badly. But they do them.$"

LavenderTown_Text_Worker:
	.string "We were going to renovate the TOWER.\n"
	.string "Then the fog rolled in and Kanto just...\l"
	.string "stopped updating.\p"
	.string "I've been on lunch break for\n"
	.string "twenty-five years. The CHANNELERS\l"
	.string "went up to pray and came down wrong.$"

LavenderTown_Text_WorkerAfter:
	.string "The fog's gone. I can see the TOWER\n"
	.string "again.\p"
	.string "I suppose this means my lunch break is\n"
	.string "over. ...I'll start tomorrow. Tomorrows\l"
	.string "work again here, apparently.$"

LavenderTown_Text_Boy:
	.string "You came out of the purple hole! Cool!\p"
	.string "The last person who came out of it was a\n"
	.string "grumpy kid with spiky hair. He saw the\l"
	.string "fog, said 'smell ya never' and went\l"
	.string "straight back in.$"

LavenderTown_Text_BoyAfter:
	.string "You beat the evil ghost! Cool!\p"
	.string "When the grumpy kid comes back, I'm\n"
	.string "telling him it was me.$"

LavenderTown_Text_GhostGengar:
	.string "A GHOST is blocking the TOWER door.\p"
	.string "Through the SILPH SCOPE it's a GENGAR,\n"
	.string "and its grin is about three teeth too\l"
	.string "wide.$"

LavenderTown_Text_GhostDusknoir:
	.string "The road north is gone. There's only\n"
	.string "fog, and a GHOST in the fog.\p"
	.string "The SILPH SCOPE says DUSKNOIR. The\n"
	.string "DUSKNOIR says nothing. It just keeps\l"
	.string "looking.$"

LavenderTown_Text_GhostBanette:
	.string "A GHOST at the edge of town. Through\n"
	.string "the SILPH SCOPE: a BANETTE, zipping and\l"
	.string "unzipping its mouth.\p"
	.string "It seems to be waiting for its old\n"
	.string "trainer. You'll do.$"

LavenderTown_Text_GhostGone:
	.string "The shadow dissolved into the fog.\p"
	.string "Somewhere, a door creaks shut. Probably\n"
	.string "for the better.$"

LavenderTown_Text_GhostNoScope:
	.string "A GHOST! A grinning shadow with too\n"
	.string "many opinions about you.\p"
	.string "Darn! The GHOST can't be ID'd. Somebody\n"
	.string "in this town used to sell SILPH SCOPES.$"

LavenderTown_Text_TownSign:
	.string "LAVENDER TOWN\n"
	.string "The Noble Purple Town\p"
	.string "(Population: fluctuating. Please count\n"
	.string "yourself twice to be sure.)$"

LavenderTown_Text_TowerSign:
	.string "POKéMON TOWER\n"
	.string "Becalm the spirits of POKéMON\p"
	.string "No running. No flash photography. No\n"
	.string "asking the CHANNELERS if they're okay.\l"
	.string "They are not.$"

LavenderTown_Text_HouseSign:
	.string "VOLUNTEER POKéMON HOUSE\p"
	.string "All POKéMON welcome. Ghosts by\n"
	.string "appointment.$"

LavenderTown_Text_Notice:
	.string "NOTICE\p"
	.string "SILPH SCOPES are sold out. Until\n"
	.string "further notice, assume every shadow is\l"
	.string "a GHOST, and every GHOST is in a mood.$"
