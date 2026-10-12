Route122_MapScripts::
	.byte 0

@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---
Route122_EventScript_ZV2Ferryman::
	msgbox Route122_Text_ZV2Ferryman, MSGBOX_NPC
	end

Route122_Text_ZV2Ferryman:
	.string "The fee to cross is one coin.\pYou have no coin? Then swim.\nEveryone swims. That's the joke.\pI used to row the dead to the\nmountain. Now they take the\lLILYCOVE bus. Times change.$"

Route122_EventScript_ZV2Boat::
	msgbox Route122_Text_ZV2Boat, MSGBOX_SIGN
	end

Route122_Text_ZV2Boat:
	.string "A small boat. Painted on the side:\n'ONE WAY ONLY'.\pIt's been crossed out and replaced\nwith 'RETURN TRIPS NEGOTIABLE'.$"

Route122_EventScript_ZV2Mortimer::
	trainerbattle_single TRAINER_MORTIMER, Route122_Text_ZV2Mortimer_Intro, Route122_Text_ZV2Mortimer_Defeat
	msgbox Route122_Text_ZV2Mortimer_Post, MSGBOX_AUTOCLOSE
	end

Route122_Text_ZV2Mortimer_Intro:
	.string "Ah, a customer. How... lively.\pI'm an undertaker. Business is\ndead. That's not a joke, it's\la quarterly report.$"

Route122_Text_ZV2Mortimer_Defeat:
	.string "Splendid. I'll put you down for\nthe premium package. Later. Much\llater. I'm patient.$"

Route122_Text_ZV2Mortimer_Post:
	.string "Every POKeMON on MT. PYRE has a\ngrave. Except the GHOSTS.\pThey refuse. Something about\n'commitment issues'.$"

Route122_EventScript_ZV2Cora::
	trainerbattle_single TRAINER_SWIMMER_CORA, Route122_Text_ZV2Cora_Intro, Route122_Text_ZV2Cora_Defeat
	msgbox Route122_Text_ZV2Cora_Post, MSGBOX_AUTOCLOSE
	end

Route122_Text_ZV2Cora_Intro:
	.string "I swim laps around MT. PYRE.\nGrandpa is up there.\pEvery lap I wave. Once, something\nwaved back. It wasn't Grandpa.$"

Route122_Text_ZV2Cora_Defeat:
	.string "Okay, okay. You win.\nGrandpa would've cheered for you.\lHe always picked the wrong side.$"

Route122_Text_ZV2Cora_Post:
	.string "Lap 4,012. Still haven't seen\nwhat waved back. Maybe tomorrow.$"
@ --- einde zee_vulling_2 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Route122_EventScript_ZV3Vesper::
	trainerbattle_single TRAINER_HEX_MANIAC_VESPER, Route122_Text_ZV3Vesper_Intro, Route122_Text_ZV3Vesper_Defeat
	msgbox Route122_Text_ZV3Vesper_Post, MSGBOX_AUTOCLOSE
	end

Route122_Text_ZV3Vesper_Intro:
	.string "I'm the maid of honor at a wedding\ntonight. Both of them are dead.\pThe groom has been dead for 200\nyears. The bride is 'only' 80.\lPeople are talking.$"

Route122_Text_ZV3Vesper_Defeat:
	.string "I'll still catch the bouquet.\nIt goes straight through my hands.$"

Route122_Text_ZV3Vesper_Post:
	.string "The ceremony is on the shore at\nmidnight. Dress code: transparent.\pThe ferryman refuses to do the\ncatering. Again.$"
@ --- einde zee_vulling_3 ---
