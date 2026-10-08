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
	.string "The lake froze, thawed, froze again, and\n"
	.string "then the volcano dusted it with ash.\p"
	.string "Now it's a grey slushie. The fish taste\n"
	.string "like a campfire.\p"
	.string "I eat them anyway. What else is there to\n"
	.string "do up here?$"

AshfrostTown_EventScript_SnowmanKid::
	msgbox AshfrostTown_EventScript_SnowmanKid_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_SnowmanKid_Text:
	.string "I built a snowman. Then the ash came\n"
	.string "down and now he's all grey and wheezy.\p"
	.string "Mom says I can't play with him anymore.\n"
	.string "She says he's a bad influence.$"

AshfrostTown_EventScript_OldWoman::
	msgbox AshfrostTown_EventScript_OldWoman_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_OldWoman_Text:
	.string "Every morning I polish the three\nstone giants and pray to them.\pThey have never once said thank you.\nNeither did my late husband.$"

AshfrostTown_EventScript_Hiker::
	msgbox AshfrostTown_EventScript_Hiker_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_Hiker_Text:
	.string "Cold, eh? But look at your feet. You can\n"
	.string "just... walk.\p"
	.string "In SINNOH the snow comes up to your\n"
	.string "waist. You have to mash the D-Pad like a\l"
	.string "lunatic for every single step.\p"
	.string "However cold it gets in ASHFROST, you\n"
	.string "never get stuck in the snow. That's a\l"
	.string "promise. It's on the welcome sign.\l"
	.string "Somewhere under the ash.$"

AshfrostTown_EventScript_Woman::
	msgbox AshfrostTown_EventScript_Woman_Text, MSGBOX_NPC
	end

AshfrostTown_EventScript_Woman_Text:
	.string "Half the year it snows. The other half\n"
	.string "it rains ash. Some days it does both and\l"
	.string "the snow comes down grey.\p"
	.string "My laundry has never once been white.\n"
	.string "Not once. I've stopped buying white\l"
	.string "things. I've stopped hoping.$"


@ Project Grounded: bord naast het Pokémon Center
AshfrostTown_EventScript_VillageSign::
	msgbox AshfrostTown_Text_VillageSign, MSGBOX_SIGN
	end

@ de drie stenen Regi-beelden bij het heiligdom: elk een cryptische hint naar zijn grot
AshfrostTown_EventScript_StatueRegirock::
	msgbox AshfrostTown_Text_StatueRegirock, MSGBOX_SIGN
	end

AshfrostTown_EventScript_StatueRegice::
	msgbox AshfrostTown_Text_StatueRegice, MSGBOX_SIGN
	end

AshfrostTown_EventScript_StatueRegisteel::
	msgbox AshfrostTown_Text_StatueRegisteel, MSGBOX_SIGN
	end

AshfrostTown_Text_VillageSign:
	.string "ASHFROST VILLAGE\n"
	.string "“Where even the snow is grey.”\p"
	.string "Please do not eat the snow. We know\n"
	.string "what's in it. Now you do too.$"

AshfrostTown_Text_StatueRegirock:
	.string "A giant made of rock, carved out of\n"
	.string "stone. Dots run across its face in the\l"
	.string "shape of an H.\p"
	.string "The pedestal reads:\n"
	.string "“I sleep in a ruin the desert keeps\l"
	.string "swallowing. Walk into the storm, and\l"
	.string "keep walking.”$"

AshfrostTown_Text_StatueRegice:
	.string "A giant made of ice, carved out of\n"
	.string "stone. Its dots form a ring around a\l"
	.string "single dot.\p"
	.string "The pedestal reads:\n"
	.string "“I sleep in a cave in the sea, between\l"
	.string "the father's city and the island of the\l"
	.string "fist. The cold you feel there is mine.”$"

AshfrostTown_Text_StatueRegisteel:
	.string "A giant made of steel, carved out of\n"
	.string "stone. Its dots form a cross.\p"
	.string "The pedestal reads:\n"
	.string "“I sleep in a tomb on the road where the\l"
	.string "rain never stops, south of the city in\l"
	.string "the trees. I do not rust. I have\l"
	.string "checked.”$"
