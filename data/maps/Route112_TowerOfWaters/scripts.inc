@ Project Grounded: Tower of Waters van de Kubfu-dojo (Route 112). Twee trainers en bovenin de torenwachter; na zijn
@ nederlaag laat hij Kubfu evolueren tot Urshifu Rapid Strike (special Grounded_EvolveKubfu, VAR_0x8004 = 1).
Route112_TowerOfWaters_MapScripts::
	.byte 0

Route112_TowerOfWaters_EventScript_Trainer1::
	trainerbattle_single TRAINER_DOJO_WATER_1, Route112_TowerOfWaters_Text_Trainer1Intro, Route112_TowerOfWaters_Text_Trainer1Defeat
	msgbox Route112_TowerOfWaters_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route112_TowerOfWaters_EventScript_Trainer2::
	trainerbattle_single TRAINER_DOJO_WATER_2, Route112_TowerOfWaters_Text_Trainer2Intro, Route112_TowerOfWaters_Text_Trainer2Defeat
	msgbox Route112_TowerOfWaters_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route112_TowerOfWaters_EventScript_Keeper::
	trainerbattle_single TRAINER_DOJO_WATER_KEEPER, Route112_TowerOfWaters_Text_KeeperIntro, Route112_TowerOfWaters_Text_KeeperDefeat, Route112_TowerOfWaters_EventScript_Ritual
	goto Route112_TowerOfWaters_EventScript_Ritual
	end

Route112_TowerOfWaters_EventScript_Ritual::
	lock
	faceplayer
	goto_if_set FLAG_KUBFU_EVOLVED, Route112_TowerOfWaters_EventScript_AlreadyDone
	specialvar VAR_RESULT, Grounded_PartyHasKubfu
	goto_if_eq VAR_RESULT, FALSE, Route112_TowerOfWaters_EventScript_NoKubfu
	msgbox Route112_TowerOfWaters_Text_Ritual, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 1
	special Grounded_EvolveKubfu
	waitstate
	setflag FLAG_KUBFU_EVOLVED
	msgbox Route112_TowerOfWaters_Text_AfterRitual, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfWaters_EventScript_NoKubfu::
	msgbox Route112_TowerOfWaters_Text_NoKubfu, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfWaters_EventScript_AlreadyDone::
	msgbox Route112_TowerOfWaters_Text_AlreadyDone, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfWaters_Text_Trainer1Intro:
	.string "Welcome to the TOWER OF WATERS!\n"
	.string "There's no pool. I checked.$"

Route112_TowerOfWaters_Text_Trainer1Defeat:
	.string "I'm drenched! In shame!$"

Route112_TowerOfWaters_Text_Trainer1Post:
	.string "I wore a swimsuit to a tower.\n"
	.string "Everyone here knew. Nobody told me.$"

Route112_TowerOfWaters_Text_Trainer2Intro:
	.string "Flow like water! Hit like water!\n"
	.string "Many, many times! HYAH-YAH-YAH!$"

Route112_TowerOfWaters_Text_Trainer2Defeat:
	.string "I flowed… straight into defeat.$"

Route112_TowerOfWaters_Text_Trainer2Post:
	.string "Water always wins in the end.\n"
	.string "Just not today. Or yesterday.$"

Route112_TowerOfWaters_Text_KeeperIntro:
	.string "I am TIDE, keeper of the\n"
	.string "TOWER OF WATERS.\p"
	.string "The scroll behind me teaches a\n"
	.string "thousand small strikes. Earn them.$"

Route112_TowerOfWaters_Text_KeeperDefeat:
	.string "Splash after splash after splash…\n"
	.string "You've learned the flow.$"

Route112_TowerOfWaters_Text_Ritual:
	.string "Your KUBFU is reading the scroll.\n"
	.string "It's moving its lips. Adorable.\p"
	.string "Let the water carry it.$"

Route112_TowerOfWaters_Text_AfterRitual:
	.string "Many strikes. One path.\n"
	.string "No going back.\p"
	.string "Go show MUSTARD. Bring tissues.\n"
	.string "For him.$"

Route112_TowerOfWaters_Text_NoKubfu:
	.string "No KUBFU? Then this was just very\n"
	.string "aggressive stair exercise.\p"
	.string "Bring it, and the scroll is yours.$"

Route112_TowerOfWaters_Text_AlreadyDone:
	.string "Your partner already chose its path.\n"
	.string "Water under the bridge. Literally.$"
