@ Project Grounded: Beacon Isle, het vuurtoreneiland onder Route 133 (ZEE_PLAN.md).
@ Kaart en scripts: tools/grounded/maptools/beacon_isle.py. 's Nachts: CHINCHOU in het water (FLAG_TEMP_11
@ verbergt ze overdag) en het licht van de vuurtoren (lichtobjecten). Het rif onderaan (rij 33-34) gaat op x 14-15
@ open zodra de speler 's nachts de lamp bovenin heeft aangesproken (FLAG_BEACON_LIGHT_ISLE_FOUND); daarachter het
@ Lichteiland met de grot van TALLOW. Teksten zijn placeholders.
BeaconIsle_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, BeaconIsle_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, BeaconIsle_OnTransition
	.byte 0

BeaconIsle_OnLoad:
	goto_if_unset FLAG_BEACON_LIGHT_ISLE_FOUND, BeaconIsle_EventScript_End
	setmetatile 14, 33, METATILE_General_CalmWater, FALSE
	setmetatile 15, 33, METATILE_General_CalmWater, FALSE
	setmetatile 14, 34, METATILE_General_CalmWater, FALSE
	setmetatile 15, 34, METATILE_General_CalmWater, FALSE
BeaconIsle_EventScript_End:
	end

BeaconIsle_OnTransition:
	call_if_unset FLAG_BEACON_LIGHT_ISLE_FOUND, BeaconIsle_EventScript_HideGuideLights
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, BeaconIsle_EventScript_End
	setflag FLAG_TEMP_11
	end

BeaconIsle_EventScript_HideGuideLights::
	setflag FLAG_TEMP_12
	return

BeaconIsle_EventScript_Roald::
	trainerbattle_single TRAINER_BEACON_ROALD, BeaconIsle_Text_RoaldIntro, BeaconIsle_Text_RoaldDefeat
	msgbox BeaconIsle_Text_RoaldPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_EventScript_Lux::
	trainerbattle_single TRAINER_BEACON_LUX, BeaconIsle_Text_LuxIntro, BeaconIsle_Text_LuxDefeat
	msgbox BeaconIsle_Text_LuxPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_EventScript_Fisherman::
	msgbox BeaconIsle_Text_Fisherman, MSGBOX_NPC
	end

BeaconIsle_EventScript_Chinchou::
	msgbox BeaconIsle_Text_Chinchou, MSGBOX_DEFAULT
	end

BeaconIsle_EventScript_Plaque::
	msgbox BeaconIsle_Text_Plaque, MSGBOX_SIGN
	end

BeaconIsle_EventScript_Reef::
	msgbox BeaconIsle_Text_Reef, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
BeaconIsle_Text_RoaldIntro:
	.string "Ahoy! I sailed three days to see the\n"
	.string "famous BEACON ISLE LIGHTHOUSE.\p"
	.string "Turns out it's a fish in a tower. I want a\n"
	.string "refund. I'll take it out on you.$"

BeaconIsle_Text_RoaldDefeat:
	.string "Fine. The fish wins too.$"

BeaconIsle_Text_RoaldPost:
	.string "Ships used to crash here every week.\n"
	.string "Now they crash every other week.\p"
	.string "That's a 50% improvement. Thank you,\n"
	.string "LANTURN.$"

BeaconIsle_Text_LuxIntro:
	.string "Shh! VOLBEAT and ILLUMISE are on a\n"
	.string "date. Nature's own lighthouse!\p"
	.string "...You're ruining the mood.$"

BeaconIsle_Text_LuxDefeat:
	.string "The mood is ruined.$"

BeaconIsle_Text_LuxPost:
	.string "Moths fly into the lighthouse every\n"
	.string "night. Not my bugs, though. My bugs have\l"
	.string "standards.$"

BeaconIsle_Text_Fisherman:
	.string "At night the CHINCHOU come up to stare\n"
	.string "at the light.\p"
	.string "They think it's their mother.\p"
	.string "I haven't told them. You don't tell a\n"
	.string "fish something like that.$"

BeaconIsle_Text_Chinchou:
	.string "CHINCHOU is gazing at the lighthouse\n"
	.string "with its whole face.\p"
	.string "It's the only light it has ever loved.$"

BeaconIsle_Text_Plaque:
	.string "BEACON ISLE LIGHTHOUSE\n"
	.string "Est. 1952. Lamp broken since 1953.\p"
	.string "Ships are kindly requested to follow\n"
	.string "the fish.$"

BeaconIsle_Text_Reef:
	.string "A reef of sharp rocks. The waves foam\n"
	.string "white over every gap.\p"
	.string "Behind it, a tiny island. You'd need a\n"
	.string "very good light to find the way through.$"
