@ Project Grounded: de Dragon's Den op het Tao-eiland. Kaart en scripts: tools/grounded/maptools/tao_island.py.
@ Onderhal met meer; de waterval (Waterfall, badge 8) leidt naar de bovenhal. Daar slaapt een DRAGONITE op het gat naar
@ Frost Hollow (KYUREM, GHETSIS); hij is weg zodra je RESHIRAM en ZEKROM allebei hebt. Teksten zijn placeholders.
TaoIsland_Den_MapScripts::
	.byte 0

TaoIsland_Den_EventScript_Osric::
	trainerbattle_single TRAINER_TAO_OSRIC, TaoIsland_Den_Text_OsricIntro, TaoIsland_Den_Text_OsricDefeat
	msgbox TaoIsland_Den_Text_OsricPost, MSGBOX_AUTOCLOSE
	end

TaoIsland_Den_EventScript_Mira::
	trainerbattle_single TRAINER_TAO_MIRA, TaoIsland_Den_Text_MiraIntro, TaoIsland_Den_Text_MiraDefeat
	msgbox TaoIsland_Den_Text_MiraPost, MSGBOX_AUTOCLOSE
	end

TaoIsland_Den_EventScript_Talon::
	trainerbattle_single TRAINER_TAO_TALON, TaoIsland_Den_Text_TalonIntro, TaoIsland_Den_Text_TalonDefeat
	msgbox TaoIsland_Den_Text_TalonPost, MSGBOX_AUTOCLOSE
	end

TaoIsland_Den_EventScript_Dragonite::
	msgbox TaoIsland_Den_Text_Dragonite, MSGBOX_DEFAULT
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
TaoIsland_Den_Text_OsricIntro:
	.string "Halt! This den is for DRAGON TAMERS\n"
	.string "only!\p"
	.string "Do you have a permit? ...Nobody has a\n"
	.string "permit.$"

TaoIsland_Den_Text_OsricDefeat:
	.string "Fine. You may stay. Unofficially.$"

TaoIsland_Den_Text_OsricPost:
	.string "Up the waterfall there's a DRAGONITE\n"
	.string "asleep on a hole in the floor.\p"
	.string "We don't ask. It doesn't tell.$"

TaoIsland_Den_Text_MiraIntro:
	.string "Shh. The dragons are sleeping. Let's\n"
	.string "fight very, very quietly.$"

TaoIsland_Den_Text_MiraDefeat:
	.string "...That was not quiet.$"

TaoIsland_Den_Text_MiraPost:
	.string "Something big is snoring up there. I\n"
	.string "hope it's a DRAGONITE.\p"
	.string "Something even bigger is snoring under\n"
	.string "the DRAGONITE.$"

TaoIsland_Den_Text_TalonIntro:
	.string "You climbed the waterfall? Impressive.\n"
	.string "I took the stairs.\p"
	.string "...There are no stairs. That's how good I\n"
	.string "am.$"

TaoIsland_Den_Text_TalonDefeat:
	.string "There really are no stairs.$"

TaoIsland_Den_Text_TalonPost:
	.string "Nobody has been down the hole under\n"
	.string "that DRAGONITE. It's cold down there.\p"
	.string "Like, emotionally cold.$"

TaoIsland_Den_Text_Dragonite:
	.string "DRAGONITE is asleep on top of a hole in\n"
	.string "the floor. Ice-cold air leaks out around\l"
	.string "it.\p"
	.string "It isn't moving. It's a very large\n"
	.string "draught excluder.$"
