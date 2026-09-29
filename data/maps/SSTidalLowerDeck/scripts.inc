SSTidalLowerDeck_MapScripts::
	.byte 0

SSTidalLowerDeck_EventScript_Phillip::
	trainerbattle_single TRAINER_PHILLIP, SSTidalLowerDeck_Text_PhillipIntro, SSTidalLowerDeck_Text_PhillipDefeat
	msgbox SSTidalLowerDeck_Text_PhillipPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalLowerDeck_EventScript_Leonard::
	trainerbattle_single TRAINER_LEONARD, SSTidalLowerDeck_Text_LeonardIntro, SSTidalLowerDeck_Text_LeonardDefeat
	msgbox SSTidalLowerDeck_Text_LeonardPostBattle, MSGBOX_AUTOCLOSE
	end

SSTidalLowerDeck_Text_PhillipIntro:
	.string "Arrrgh! I'm sick of cleaning this huge\n"
	.string "ship!\p"
	.string "Quick battle! Break time!$"

SSTidalLowerDeck_Text_PhillipDefeat:
	.string "Little bro, I lost! Don't tell Mom!$"

SSTidalLowerDeck_Text_PhillipPostBattle:
	.string "We're the CLEANUP BROTHERS!\p"
	.string "The old one dumps detergent, the young\n"
	.string "one scrubs!\p"
	.string "I'm the old one. Guess who has the easy\n"
	.string "job.$"

SSTidalLowerDeck_Text_LeonardIntro:
	.string "This is the bottom of the hull.\p"
	.string "Plenty of room for a battle.\p"
	.string "And plenty of rats.$"

SSTidalLowerDeck_Text_LeonardDefeat:
	.string "Big bro, I lost! I'm telling Mom!$"

SSTidalLowerDeck_Text_LeonardPostBattle:
	.string "We're the CLEANUP BROTHERS!\p"
	.string "The old one dumps detergent, the young\n"
	.string "one scrubs!\p"
	.string "I'm the young one. My hands are raw.$"

