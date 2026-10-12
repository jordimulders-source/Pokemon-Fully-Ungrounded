@ Project Grounded: vuurtoren op Beacon Isle, eerste verdieping (kopie van de Space Center 2F + trap omhoog).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. Teksten zijn placeholders.
BeaconIsle_Lighthouse_2F_MapScripts::
	.byte 0

BeaconIsle_Lighthouse_2F_EventScript_Keiko::
	trainerbattle_single TRAINER_BEACON_KEIKO, BeaconIsle_Lighthouse_2F_Text_KeikoIntro, BeaconIsle_Lighthouse_2F_Text_KeikoDefeat
	msgbox BeaconIsle_Lighthouse_2F_Text_KeikoPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_Lighthouse_2F_EventScript_Pemberton::
	trainerbattle_single TRAINER_BEACON_PEMBERTON, BeaconIsle_Lighthouse_2F_Text_PembertonIntro, BeaconIsle_Lighthouse_2F_Text_PembertonDefeat
	msgbox BeaconIsle_Lighthouse_2F_Text_PembertonPost, MSGBOX_AUTOCLOSE
	end

BeaconIsle_Lighthouse_2F_EventScript_Machine::
	msgbox BeaconIsle_Lighthouse_2F_Text_Machine, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
BeaconIsle_Lighthouse_2F_Text_KeikoIntro:
	.string "I climb these stairs a hundred times a\n"
	.string "day. Leg day is every day.\p"
	.string "Today, it's YOUR day.$"

BeaconIsle_Lighthouse_2F_Text_KeikoDefeat:
	.string "My legs gave up before I did.$"

BeaconIsle_Lighthouse_2F_Text_KeikoPost:
	.string "The keeper climbs these stairs every\n"
	.string "night. He's 91.\p"
	.string "He says the secret is spite.$"

BeaconIsle_Lighthouse_2F_Text_PembertonIntro:
	.string "I've come to purchase this lighthouse.\n"
	.string "The keeper refuses to sell.\p"
	.string "Perhaps I can buy YOU instead?$"

BeaconIsle_Lighthouse_2F_Text_PembertonDefeat:
	.string "Priceless. How annoying.$"

BeaconIsle_Lighthouse_2F_Text_PembertonPost:
	.string "I offered the keeper a fortune for his\n"
	.string "LANTURN.\p"
	.string "He said she isn't for sale. She's for\n"
	.string "“shining.” Unbelievable.$"

BeaconIsle_Lighthouse_2F_Text_Machine:
	.string "A huge machine labeled LAMP CONTROL.\n"
	.string "It's unplugged.\p"
	.string "Someone has taped a picture of a fish\n"
	.string "over the switch.$"
