AshfrostTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AshfrostTown_OnTransition
	.byte 0

AshfrostTown_OnTransition:
	setflag FLAG_VISITED_ASHFROST_TOWN
	end

@ Terug de bergpas af naar Route 136 (warp; Route 136 heeft een andere tileset)
AshfrostTown_EventScript_ToRoute136::
	warpsilent MAP_ROUTE136, 49, 1
	waitstate
	end

AshfrostTown_EventScript_Fisherman::
	msgbox AshfrostTown_EventScript_Fisherman_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_Fisherman_Text:
	.string "(Placeholder: fisherman at the lake.)$"

AshfrostTown_EventScript_SnowmanKid::
	msgbox AshfrostTown_EventScript_SnowmanKid_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_SnowmanKid_Text:
	.string "(Placeholder: kid next to the snowman.)$"

AshfrostTown_EventScript_OldWoman::
	msgbox AshfrostTown_EventScript_OldWoman_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_OldWoman_Text:
	.string "Every morning I polish the three\nstone giants and pray to them.\pThey have never once said thank you.\nNeither did my late husband.$"

AshfrostTown_EventScript_Hiker::
	msgbox AshfrostTown_EventScript_Hiker_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_Hiker_Text:
	.string "(Placeholder: hiker who just climbed\nup from ROUTE 136.)$"

AshfrostTown_EventScript_Woman::
	msgbox AshfrostTown_EventScript_Woman_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_Woman_Text:
	.string "(Placeholder: woman.)$"

