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


@ Project Grounded: de iglo. Zijn alle vijf Regi's gevangen, dan is de vloer ingestort tot een trap naar de Regigigas-tempel.
AshfrostTown_EventScript_Igloo::
	lockall
	goto_if_set FLAG_REGIGIGAS_TEMPLE_OPEN, AshfrostTown_EventScript_IglooOpen
	msgbox AshfrostTown_Text_IglooClosed, MSGBOX_DEFAULT
	releaseall
	end

AshfrostTown_EventScript_IglooOpen::
	msgbox AshfrostTown_Text_IglooOpen, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	warp MAP_REGIGIGAS_TEMPLE, 0
	waitstate
	releaseall
	end

AshfrostTown_Text_IglooClosed:
	.string "An igloo. It's very cold inside.\p"
	.string "Suspiciously cold. Colder than an igloo\n"
	.string "has any right to be.$"

AshfrostTown_Text_IglooOpen:
	.string "The floor of the igloo has caved in.\n"
	.string "Stone steps lead down into the dark...$"
