AbandonedShip_Rooms2_1F_MapScripts::
	.byte 0

AbandonedShip_Rooms2_1F_EventScript_Dan::
	trainerbattle_double TRAINER_KIRA_AND_DAN_1, AbandonedShip_Rooms2_1F_Text_DanIntro, AbandonedShip_Rooms2_1F_Text_DanDefeat, AbandonedShip_Rooms2_1F_Text_DanNotEnoughMons, AbandonedShip_Rooms2_1F_EventScript_RegisterDan
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, AbandonedShip_Rooms2_1F_EventScript_DanRematch
	msgbox AbandonedShip_Rooms2_1F_Text_DanPostBattle, MSGBOX_DEFAULT
	release
	end

AbandonedShip_Rooms2_1F_EventScript_RegisterDan::
	msgbox AbandonedShip_Rooms2_1F_Text_KiraRegister, MSGBOX_DEFAULT  @ Kira speaks for both when registering KiraAndDan
	register_matchcall TRAINER_KIRA_AND_DAN_1
	release
	end

AbandonedShip_Rooms2_1F_EventScript_DanRematch::
	trainerbattle_rematch_double TRAINER_KIRA_AND_DAN_1, AbandonedShip_Rooms2_1F_Text_DanRematchIntro, AbandonedShip_Rooms2_1F_Text_DanRematchDefeat, AbandonedShip_Rooms2_1F_Text_DanRematchNotEnoughMons
	msgbox AbandonedShip_Rooms2_1F_Text_DanPostRematch, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms2_1F_EventScript_Kira::
	trainerbattle_double TRAINER_KIRA_AND_DAN_1, AbandonedShip_Rooms2_1F_Text_KiraIntro, AbandonedShip_Rooms2_1F_Text_KiraDefeat, AbandonedShip_Rooms2_1F_Text_KiraNotEnoughMons, AbandonedShip_Rooms2_1F_EventScript_RegisterKira
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, AbandonedShip_Rooms2_1F_EventScript_KiraRematch
	msgbox AbandonedShip_Rooms2_1F_Text_KiraPostBattle, MSGBOX_DEFAULT
	release
	end

AbandonedShip_Rooms2_1F_EventScript_RegisterKira::
	msgbox AbandonedShip_Rooms2_1F_Text_KiraRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_KIRA_AND_DAN_1
	release
	end

AbandonedShip_Rooms2_1F_EventScript_KiraRematch::
	trainerbattle_rematch_double TRAINER_KIRA_AND_DAN_1, AbandonedShip_Rooms2_1F_Text_KiraRematchIntro, AbandonedShip_Rooms2_1F_Text_KiraRematchDefeat, AbandonedShip_Rooms2_1F_Text_KiraRematchNotEnoughMons
	msgbox AbandonedShip_Rooms2_1F_Text_KiraPostRematch, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms2_1F_EventScript_Jani::
	trainerbattle_single TRAINER_JANI, AbandonedShip_Rooms2_1F_Text_JaniIntro, AbandonedShip_Rooms2_1F_Text_JaniDefeat
	msgbox AbandonedShip_Rooms2_1F_Text_JaniPostBattle, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms2_1F_EventScript_Garrison::
	trainerbattle_single TRAINER_GARRISON, AbandonedShip_Rooms2_1F_Text_GarrisonIntro, AbandonedShip_Rooms2_1F_Text_GarrisonDefeat
	msgbox AbandonedShip_Rooms2_1F_Text_GarrisonPostBattle, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms2_1F_Text_DanIntro:
	.string "DAN: While searching for love, we\n"
	.string "discovered a TRAINER. Ughhhh, why are\l"
	.string "you here?$"

AbandonedShip_Rooms2_1F_Text_DanDefeat:
	.string "DAN: Now move yo' ass, we were talking\n"
	.string "marriage plans.$"

AbandonedShip_Rooms2_1F_Text_DanPostBattle:
	.string "DAN: We can't find any treasures… I\n"
	.string "wonder if someone got them already?\l"
	.string "I need a ring...$"

AbandonedShip_Rooms2_1F_Text_DanNotEnoughMons:
	.string "DAN: Why are you walking around with\n"
	.string "just one Pokémon. It's not even a\l"
	.string "CHARIZARD?$"

AbandonedShip_Rooms2_1F_Text_KiraIntro:
	.string "KIRA: Oh? Dan is into me? Very one sided\n"
	.string "love. Can you help me get rid of him?$"

AbandonedShip_Rooms2_1F_Text_KiraDefeat:
	.string "KIRA: Ooh, so strong! I'd rather go with\n"
	.string "you!$"

AbandonedShip_Rooms2_1F_Text_KiraPostBattle:
	.string "KIRA: You are my treasure! Can you tell\n"
	.string "DAN that I'm leaving him for you? Wait,\l"
	.string "what, you don't want me? That's ironic.$"

AbandonedShip_Rooms2_1F_Text_KiraNotEnoughMons:
	.string "KIRA: Why are you soloing the game? Are\n"
	.string "you Jrose11?$"

AbandonedShip_Rooms2_1F_Text_KiraRegister:
	.string "KIRA: Oh, you make me so angry! I'm going\n"
	.string "to register you for that!$"

AbandonedShip_Rooms2_1F_Text_DanRematchIntro:
	.string "DAN: We've found some treasure.\n"
	.string "Niceeeeeeeee! Let me show ya!$"

AbandonedShip_Rooms2_1F_Text_DanRematchDefeat:
	.string "DAN: Turns out treasure's bad at\n"
	.string "fighting...$"

AbandonedShip_Rooms2_1F_Text_DanPostRematch:
	.string "DAN: We can't find any treasures, we\n"
	.string "lose at POKéMON…\p"
	.string "I want to go home… But if I say that,\n"
	.string "she will probably leave me…$"

AbandonedShip_Rooms2_1F_Text_DanRematchNotEnoughMons:
	.string "DAN: C'mon dawg, why you only have one\n"
	.string "Pokémon.$"

AbandonedShip_Rooms2_1F_Text_KiraRematchIntro:
	.string "KIRA: Oh? We meet again!\p"
	.string "I've gotten over you! I'm a pirate now,\n"
	.string "look at my gold!$"

AbandonedShip_Rooms2_1F_Text_KiraRematchDefeat:
	.string "KIRA: Oh, we lost again… Gold or no gold.$"

AbandonedShip_Rooms2_1F_Text_KiraPostRematch:
	.string "KIRA: We're not leaving until we raise\n"
	.string "our POKéMON some more and we find the\l"
	.string "treasures here!$"

AbandonedShip_Rooms2_1F_Text_KiraRematchNotEnoughMons:
	.string "KIRA: Why are you wandering around with\n"
	.string "just one Pokémon? Must be a Pelipper or\l"
	.string "something, since you can swim and fly.$"

AbandonedShip_Rooms2_1F_Text_JaniIntro:
	.string "I'm not good at swimming, but I am good\n"
	.string "at battles! If it's not in the water lol.$"

AbandonedShip_Rooms2_1F_Text_JaniDefeat:
	.string "I'm probably a better swimmer.$"

AbandonedShip_Rooms2_1F_Text_JaniPostBattle:
	.string "Walking around barefoot in this ship is\n"
	.string "kind of gross. You'll get athlete's foot,\l"
	.string "or other infections, fungi, Foongus,\l"
	.string "Paras.$"

AbandonedShip_Rooms2_1F_Text_GarrisonIntro:
	.string "I'm hiking a boat! Luckily it sinked, so\n"
	.string "there's a bit of a hill to climb.$"

AbandonedShip_Rooms2_1F_Text_GarrisonDefeat:
	.string "Huff, puff, I'm not used to this\n"
	.string "anymore. Boat hiking is never this\l"
	.string "taxing.$"

AbandonedShip_Rooms2_1F_Text_GarrisonPostBattle:
	.string "In a cabin somewhere on board, I saw\n"
	.string "something sparkle in a dark brownish\l"
	.string "color.$"
