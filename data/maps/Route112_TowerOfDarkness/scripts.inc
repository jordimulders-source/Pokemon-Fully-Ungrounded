@ Project Grounded: Tower of Darkness van de Kubfu-dojo (Route 112). Twee trainers en bovenin de torenwachter; na zijn
@ nederlaag laat hij Kubfu evolueren tot Urshifu Single Strike (special Grounded_EvolveKubfu, VAR_0x8004 = 0).
Route112_TowerOfDarkness_MapScripts::
	.byte 0

Route112_TowerOfDarkness_EventScript_Trainer1::
	trainerbattle_single TRAINER_DOJO_DARK_1, Route112_TowerOfDarkness_Text_Trainer1Intro, Route112_TowerOfDarkness_Text_Trainer1Defeat
	msgbox Route112_TowerOfDarkness_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route112_TowerOfDarkness_EventScript_Trainer2::
	trainerbattle_single TRAINER_DOJO_DARK_2, Route112_TowerOfDarkness_Text_Trainer2Intro, Route112_TowerOfDarkness_Text_Trainer2Defeat
	msgbox Route112_TowerOfDarkness_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route112_TowerOfDarkness_EventScript_Keeper::
	trainerbattle_single TRAINER_DOJO_DARK_KEEPER, Route112_TowerOfDarkness_Text_KeeperIntro, Route112_TowerOfDarkness_Text_KeeperDefeat, Route112_TowerOfDarkness_EventScript_Ritual
	goto Route112_TowerOfDarkness_EventScript_Ritual
	end

Route112_TowerOfDarkness_EventScript_Ritual::
	lock
	faceplayer
	goto_if_not_defeated TRAINER_DOJO_DARK_KEEPER, Route112_TowerOfDarkness_EventScript_KeeperLost @ verloren: geen white-out, gewoon opnieuw proberen
	goto_if_set FLAG_KUBFU_EVOLVED, Route112_TowerOfDarkness_EventScript_AlreadyDone
	specialvar VAR_RESULT, Grounded_PartyHasKubfu
	goto_if_eq VAR_RESULT, FALSE, Route112_TowerOfDarkness_EventScript_NoKubfu
	msgbox Route112_TowerOfDarkness_Text_Ritual, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 0
	special Grounded_EvolveKubfu
	waitstate
	setflag FLAG_KUBFU_EVOLVED
	msgbox Route112_TowerOfDarkness_Text_AfterRitual, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfDarkness_EventScript_KeeperLost::
	release
	end

Route112_TowerOfDarkness_EventScript_NoKubfu::
	msgbox Route112_TowerOfDarkness_Text_NoKubfu, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfDarkness_EventScript_AlreadyDone::
	msgbox Route112_TowerOfDarkness_Text_AlreadyDone, MSGBOX_DEFAULT
	release
	end

Route112_TowerOfDarkness_Text_Trainer1Intro:
	.string "Welcome to the TOWER OF DARKNESS. The\n"
	.string "lights are off. Spiritually and\l"
	.string "financially.$"

Route112_TowerOfDarkness_Text_Trainer1Defeat:
	.string "Ow. I walked into a wall.\n"
	.string "Unrelated to the battle.$"

Route112_TowerOfDarkness_Text_Trainer1Post:
	.string "I told WATTSON I'd pay the power bill\n"
	.string "next month. That was four years ago.$"

Route112_TowerOfDarkness_Text_Trainer2Intro:
	.string "One strike! That's all a true fighter\n"
	.string "needs!\p"
	.string "FINISH HIM! …Wait, I'm supposed to say\n"
	.string "that at the end.$"

Route112_TowerOfDarkness_Text_Trainer2Defeat:
	.string "FATALITY.\n"
	.string "…Mine.$"

Route112_TowerOfDarkness_Text_Trainer2Post:
	.string "The keeper upstairs only needs one hit.\n"
	.string "He also only has one friend. It's the\l"
	.string "scroll.$"

Route112_TowerOfDarkness_Text_KeeperIntro:
	.string "I am OBSIDIAN, keeper of the TOWER OF\n"
	.string "DARKNESS. And no, it's not a phase.\p"
	.string "The scroll at my back teaches one\n"
	.string "perfect strike. Earn it.$"

Route112_TowerOfDarkness_Text_KeeperDefeat:
	.string "…A perfect strike. I'll write a poem\n"
	.string "about it. Nobody will read it.$"

Route112_TowerOfDarkness_Text_Ritual:
	.string "Your KUBFU is staring at the scroll\n"
	.string "like it owes it money.\p"
	.string "Good. Let it read.\n"
	.string "The darkness will do the rest.$"

Route112_TowerOfDarkness_Text_AfterRitual:
	.string "One strike. One path. No going back.\p"
	.string "Go show MUSTARD. He'll cry.\n"
	.string "He always cries.$"

Route112_TowerOfDarkness_Text_NoKubfu:
	.string "You climbed my tower without KUBFU?\p"
	.string "That is like going to a restaurant\n"
	.string "and forgetting your mouth.\p"
	.string "Bring it, and the scroll is yours.$"

Route112_TowerOfDarkness_Text_AlreadyDone:
	.string "Your partner already chose its path.\n"
	.string "The scroll has nothing left to say.\p"
	.string "It's a scroll. It never said much.$"
