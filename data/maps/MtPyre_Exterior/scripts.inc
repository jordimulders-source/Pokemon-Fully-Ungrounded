MtPyre_Exterior_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtPyre_Exterior_OnTransition
	.byte 0

MtPyre_Exterior_OnTransition:
	call MtPyre_Exterior_EventScript_CheckEnterFromSummit
	end

MtPyre_Exterior_EventScript_CheckEnterFromSummit::
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_lt VAR_TEMP_1, 12, MtPyre_Exterior_EventScript_EnterFromSummit
	return

MtPyre_Exterior_EventScript_EnterFromSummit::
	setweather WEATHER_FOG_HORIZONTAL
	return

MtPyre_Exterior_EventScript_FogTrigger::
	setweather WEATHER_FOG_HORIZONTAL
	doweather
	end

MtPyre_Exterior_EventScript_SunTrigger::
	setweather WEATHER_SUNNY
	doweather
	end

@ --- land_vulling (gegenereerd door tools/grounded/maptools/land_vulling.py) ---
MtPyre_Exterior_EventScript_LVRehearsal::
	msgbox MtPyre_Exterior_Text_LVRehearsal, MSGBOX_NPC
	end

MtPyre_Exterior_Text_LVRehearsal:
	.string "Shh. I'm rehearsing.\pFor my own funeral. I want to get\nthe lying-still part right.\pDay four. My ZIGZAGOON thinks\nI've already gone. It ate my lunch.$"

MtPyre_Exterior_EventScript_LVTamagotchi::
	msgbox MtPyre_Exterior_Text_LVTamagotchi, MSGBOX_NPC
	end

MtPyre_Exterior_Text_LVTamagotchi:
	.string "I'm mourning my digital pet.\pThey said this place is only for\nPOKeMON. Grief doesn't do genres.\pHe died of hunger. I fed him\ntwice. In 1998.$"

MtPyre_Exterior_EventScript_LVStreamer::
	msgbox MtPyre_Exterior_Text_LVStreamer, MSGBOX_NPC
	end

MtPyre_Exterior_Text_LVStreamer:
	.string "Hi chat! We're LIVE from MT. PYRE!\pGrandma's DUSCLOPS passed, so this\nis a memorial stream. Smash that\llike button. He'd have wanted that.\p...Three viewers. Two are ghosts.\nBest numbers I've ever had.$"

MtPyre_Exterior_EventScript_LVVoltorb::
	msgbox MtPyre_Exterior_Text_LVVoltorb, MSGBOX_NPC
	end

MtPyre_Exterior_Text_LVVoltorb:
	.string "My VOLTORB used SELF-DESTRUCT.\nFor no reason.\pMom says it was the reason.\pThe grave is empty. There wasn't\nmuch to bury. Just the smell.$"

MtPyre_Exterior_EventScript_LVDuskull::
	lock
	faceplayer
	playmoncry SPECIES_DUSKULL, CRY_MODE_NORMAL
	msgbox MtPyre_Exterior_Text_LVDuskull, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MtPyre_Exterior_Text_LVDuskull:
	.string "The DUSKULL is watching you.\nClosely. Taking notes, maybe.\pIt looks at you the way a tailor\nlooks at a customer.\lMeasuring.$"

MtPyre_Exterior_EventScript_LVSeaView::
	msgbox MtPyre_Exterior_Text_LVSeaView, MSGBOX_NPC
	end

MtPyre_Exterior_Text_LVSeaView:
	.string "I paid extra for this plot.\n'Premium. Sea view,' they said.\pThe fog has not lifted since I\nsigned. Not once.\pI'm not even dead yet. I just\ncome here to be disappointed early.$"
@ --- einde land_vulling ---
