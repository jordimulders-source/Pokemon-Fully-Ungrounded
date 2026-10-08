@ Project Grounded: de Dragon's Den in Dragonspine Isle. Kaart en scripts: tools/grounded/maptools/beacon_dragon.py.
@ Onderhal met meer; de waterval (Waterfall, badge 8) leidt naar de bovenhal met drakenwachter GERALD.
@ Teksten zijn placeholders.
DragonspineIsle_Den_MapScripts::
	.byte 0

DragonspineIsle_Den_EventScript_Osric::
	trainerbattle_single TRAINER_DRAGONSPINE_OSRIC, DragonspineIsle_Den_Text_OsricIntro, DragonspineIsle_Den_Text_OsricDefeat
	msgbox DragonspineIsle_Den_Text_OsricPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_Den_EventScript_Mira::
	trainerbattle_single TRAINER_DRAGONSPINE_MIRA, DragonspineIsle_Den_Text_MiraIntro, DragonspineIsle_Den_Text_MiraDefeat
	msgbox DragonspineIsle_Den_Text_MiraPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_Den_EventScript_Talon::
	trainerbattle_single TRAINER_DRAGONSPINE_TALON, DragonspineIsle_Den_Text_TalonIntro, DragonspineIsle_Den_Text_TalonDefeat
	msgbox DragonspineIsle_Den_Text_TalonPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_Den_EventScript_Gerald::
	trainerbattle_single TRAINER_GERALD_WARDEN, DragonspineIsle_Den_Text_GeraldIntro, DragonspineIsle_Den_Text_GeraldDefeat, DragonspineIsle_Den_EventScript_GeraldDefeated
	msgbox DragonspineIsle_Den_Text_GeraldPost, MSGBOX_AUTOCLOSE
	end

DragonspineIsle_Den_EventScript_GeraldDefeated::
	msgbox DragonspineIsle_Den_Text_GeraldGift, MSGBOX_DEFAULT
	giveitem ITEM_EXPERT_BELT
	msgbox DragonspineIsle_Den_Text_GeraldPost, MSGBOX_DEFAULT
	release
	end

DragonspineIsle_Den_EventScript_Dragonite::
	msgbox DragonspineIsle_Den_Text_Dragonite, MSGBOX_DEFAULT
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
DragonspineIsle_Den_Text_OsricIntro:
	.string "Halt! This den is for DRAGON TAMERS\n"
	.string "only!\p"
	.string "Do you have a permit? ...Nobody has a\n"
	.string "permit.$"

DragonspineIsle_Den_Text_OsricDefeat:
	.string "Fine. You may stay. Unofficially.$"

DragonspineIsle_Den_Text_OsricPost:
	.string "The waterfall leads to the warden.\n"
	.string "Climbing it is the easy part.\p"
	.string "Filling in his forms is the hard part.$"

DragonspineIsle_Den_Text_MiraIntro:
	.string "Shh. The dragons are sleeping. Let's\n"
	.string "fight very, very quietly.$"

DragonspineIsle_Den_Text_MiraDefeat:
	.string "...That was not quiet.$"

DragonspineIsle_Den_Text_MiraPost:
	.string "Something big is snoring up there. I\n"
	.string "hope it's a DRAGONITE.\p"
	.string "I really hope it's not GERALD.$"

DragonspineIsle_Den_Text_TalonIntro:
	.string "You climbed the waterfall? Impressive.\n"
	.string "I took the stairs.\p"
	.string "...There are no stairs. That's how good I\n"
	.string "am.$"

DragonspineIsle_Den_Text_TalonDefeat:
	.string "There really are no stairs.$"

DragonspineIsle_Den_Text_TalonPost:
	.string "GERALD has guarded this den for thirty\n"
	.string "years. Nobody knows what he's guarding\l"
	.string "it from.\p"
	.string "Possibly from us.$"

DragonspineIsle_Den_Text_GeraldGift:
	.string "Your paperwork is in order. Take this\n"
	.string "EXPERT BELT.\p"
	.string "Standard issue for people who keep\n"
	.string "winning. Sign here. And here. And here.$"

DragonspineIsle_Den_Text_GeraldIntro:
	.string "Ah. A visitor. I am GERALD, Warden of the\n"
	.string "Dragon's Den.\p"
	.string "Have you filled in form D-7, “Intent to\n"
	.string "Battle a Dragon Warden”?\p"
	.string "...No? Then I shall have to process you\n"
	.string "manually.$"

DragonspineIsle_Den_Text_GeraldDefeat:
	.string "Request... approved.$"

DragonspineIsle_Den_Text_GeraldPost:
	.string "Dragons used to rule these islands.\n"
	.string "These days they're mostly retired.\p"
	.string "I make sure nobody disturbs their\n"
	.string "pension.$"

DragonspineIsle_Den_Text_Dragonite:
	.string "DRAGONITE is asleep on a stack of\n"
	.string "paperwork.\p"
	.string "It is snoring in triplicate.$"
