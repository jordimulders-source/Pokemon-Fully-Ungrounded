Route116_TunnelersRestHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route116_TunnelersRestHouse_OnTransition
	.byte 0

Route116_TunnelersRestHouse_OnTransition:
	setflag FLAG_LANDMARK_TUNNELERS_REST_HOUSE
	end

Route116_TunnelersRestHouse_EventScript_Tunneler1::
	msgbox Route116_TunnelersRestHouse_Text_WeHadToStopBoring, MSGBOX_NPC
	end

Route116_TunnelersRestHouse_EventScript_Tunneler2::
	msgbox Route116_TunnelersRestHouse_Text_ManDiggingHisWayToVerdanturf, MSGBOX_NPC
	end

Route116_TunnelersRestHouse_EventScript_Tunneler3::
	lock
	faceplayer
	goto_if_set FLAG_RUSTURF_TUNNEL_OPENED, Route116_TunnelersRestHouse_EventScript_TunnelOpened
	msgbox Route116_TunnelersRestHouse_Text_GetToVerdanturfWithoutTunnel, MSGBOX_DEFAULT
	release
	end

Route116_TunnelersRestHouse_EventScript_TunnelOpened::
	msgbox Route116_TunnelersRestHouse_Text_TunnelHasGoneThrough, MSGBOX_DEFAULT
	release
	end

Route116_TunnelersRestHouse_Text_WeHadToStopBoring:
	.string "That RUSTURF TUNNEL…\p"
	.string "We had a big crew and fancy machines.\n"
	.string "Then we had to stop.\p"
	.string "It bothered the wild POKéMON.\p"
	.string "So now we just loll around here. Still on\n"
	.string "the payroll.$"

Route116_TunnelersRestHouse_Text_ManDiggingHisWayToVerdanturf:
	.string "A man is digging to VERDANTURF by\n"
	.string "himself.\p"
	.string "By hand. No machines. To not disturb the\n"
	.string "POKéMON.\p"
	.string "And to see his girlfriend.\p"
	.string "We watch him through the window. It's\n"
	.string "our entertainment.$"

Route116_TunnelersRestHouse_Text_GetToVerdanturfWithoutTunnel:
	.string "Without the TUNNEL, VERDANTURF means:\n"
	.string "sail to DEWFORD, then SLATEPORT, then\l"
	.string "through MAUVILLE.\p"
	.string "Three days. For a town that's right\n"
	.string "there.$"

Route116_TunnelersRestHouse_Text_TunnelHasGoneThrough:
	.string "Did you hear? The TUNNEL to VERDANTURF\n"
	.string "is through!\p"
	.string "If you hope hard enough, dreams come\n"
	.string "true.\p"
	.string "Now what do we watch?$"

