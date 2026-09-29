MeteorFalls_1F_2R_MapScripts::
	.byte 0

MeteorFalls_1F_2R_EventScript_Nicolas::
	trainerbattle_single TRAINER_NICOLAS_1, MeteorFalls_1F_2R_Text_NicolasIntro, MeteorFalls_1F_2R_Text_NicolasDefeat, MeteorFalls_1F_2R_EventScript_RegisterNicolas
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MeteorFalls_1F_2R_EventScript_RematchNicolas
	msgbox MeteorFalls_1F_2R_Text_NicolasPostBattle, MSGBOX_DEFAULT
	release
	end

MeteorFalls_1F_2R_EventScript_RegisterNicolas::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox MeteorFalls_1F_2R_Text_NicolasRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_NICOLAS_1
	release
	end

MeteorFalls_1F_2R_EventScript_RematchNicolas::
	trainerbattle_rematch TRAINER_NICOLAS_1, MeteorFalls_1F_2R_Text_NicolasRematchIntro, MeteorFalls_1F_2R_Text_NicolasRematchDefeat
	msgbox MeteorFalls_1F_2R_Text_NicolasPostRematch, MSGBOX_AUTOCLOSE
	end

MeteorFalls_1F_2R_EventScript_John::
	trainerbattle_double TRAINER_JOHN_AND_JAY_1, MeteorFalls_1F_2R_Text_JohnIntro, MeteorFalls_1F_2R_Text_JohnDefeat, MeteorFalls_1F_2R_Text_JohnNotEnoughMons, MeteorFalls_1F_2R_EventScript_RegisterJohn
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MeteorFalls_1F_2R_EventScript_RematchJohn
	msgbox MeteorFalls_1F_2R_Text_JohnPostBattle, MSGBOX_DEFAULT
	release
	end

MeteorFalls_1F_2R_EventScript_RegisterJohn::
	msgbox MeteorFalls_1F_2R_Text_JohnRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_JOHN_AND_JAY_1
	release
	end

MeteorFalls_1F_2R_EventScript_RematchJohn::
	trainerbattle_rematch_double TRAINER_JOHN_AND_JAY_1, MeteorFalls_1F_2R_Text_JohnRematchIntro, MeteorFalls_1F_2R_Text_JohnRematchDefeat, MeteorFalls_1F_2R_Text_JohnRematchNotEnoughMons
	msgbox MeteorFalls_1F_2R_Text_JohnPostRematch, MSGBOX_AUTOCLOSE
	end

MeteorFalls_1F_2R_EventScript_Jay::
	trainerbattle_double TRAINER_JOHN_AND_JAY_1, MeteorFalls_1F_2R_Text_JayIntro, MeteorFalls_1F_2R_Text_JayDefeat, MeteorFalls_1F_2R_Text_JayNotEnoughMons, MeteorFalls_1F_2R_EventScript_RegisterJay
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, MeteorFalls_1F_2R_EventScript_RematchJay
	msgbox MeteorFalls_1F_2R_Text_JayPostBattle, MSGBOX_DEFAULT
	release
	end

MeteorFalls_1F_2R_EventScript_RegisterJay::
	msgbox MeteorFalls_1F_2R_Text_JohnRegister, MSGBOX_DEFAULT  @ John speaks for both during register
	register_matchcall TRAINER_JOHN_AND_JAY_1
	release
	end

MeteorFalls_1F_2R_EventScript_RematchJay::
	trainerbattle_rematch_double TRAINER_JOHN_AND_JAY_1, MeteorFalls_1F_2R_Text_JayRematchIntro, MeteorFalls_1F_2R_Text_JayRematchDefeat, MeteorFalls_1F_2R_Text_JayRematchNotEnoughMons
	msgbox MeteorFalls_1F_2R_Text_JayPostRematch, MSGBOX_AUTOCLOSE
	end

MeteorFalls_1F_2R_Text_NicolasIntro:
	.string "This is where we DRAGON users train.\p"
	.string "The CHAMPION even visits. He once said\n"
	.string "hi to me.\p"
	.string "I think about it daily.$"

MeteorFalls_1F_2R_Text_NicolasDefeat:
	.string "Urgh! I didn't expect you to be so\n"
	.string "strong!$"

MeteorFalls_1F_2R_Text_NicolasPostBattle:
	.string "The road ahead is long and harsh.\p"
	.string "My DRAGON POKéMON and I will be the\n"
	.string "best.\p"
	.string "In about 40 years.$"

MeteorFalls_1F_2R_Text_NicolasRegister:
	.string "I want to know more about your power.\p"
	.string "Register me. For research.$"

MeteorFalls_1F_2R_Text_NicolasRematchIntro:
	.string "We trained with our sights on number\n"
	.string "one!\p"
	.string "Show us how much stronger we got!$"

MeteorFalls_1F_2R_Text_NicolasRematchDefeat:
	.string "Urgh! Stronger again?!$"

MeteorFalls_1F_2R_Text_NicolasPostRematch:
	.string "You keep training. So will I.\p"
	.string "My dragons need fewer naps, though.$"

MeteorFalls_1F_2R_Text_JohnIntro:
	.string "JOHN: We've battled as a twosome for\n"
	.string "fifty years.\p"
	.string "She does the battling. I do the nodding.$"

MeteorFalls_1F_2R_Text_JohnDefeat:
	.string "JOHN: Oh, my. We lost, dear.$"

MeteorFalls_1F_2R_Text_JohnPostBattle:
	.string "JOHN: Fifty years of marriage.\p"
	.string "I've never beaten my wife in a battle.\p"
	.string "Or an argument.$"

MeteorFalls_1F_2R_Text_JohnNotEnoughMons:
	.string "JOHN: Well, well, a young TRAINER!\p"
	.string "Come back with more POKéMON. We battle\n"
	.string "as a pair. Like everything.$"

MeteorFalls_1F_2R_Text_JohnRegister:
	.string "JOHN: Young TRAINER, battle us again\n"
	.string "sometime.\p"
	.string "We don't get out much.$"

MeteorFalls_1F_2R_Text_JayIntro:
	.string "JAY: Fifty years married.\p"
	.string "Nothing can break our bond. We've tried.$"

MeteorFalls_1F_2R_Text_JayDefeat:
	.string "JAY: Oh, dear. We lost, my dear husband.\p"
	.string "Your fault, of course.$"

MeteorFalls_1F_2R_Text_JayPostBattle:
	.string "JAY: Fifty years… Every argument, we\n"
	.string "settled with a POKéMON battle.\p"
	.string "I've won 4,381 of them.$"

MeteorFalls_1F_2R_Text_JayNotEnoughMons:
	.string "JAY: Oh, a young TRAINER!\p"
	.string "We battle as a pair, dear. Bring more\n"
	.string "POKéMON.$"

MeteorFalls_1F_2R_Text_JohnRematchIntro:
	.string "JOHN: Twosome, fifty years. Let's go,\n"
	.string "dear.$"

MeteorFalls_1F_2R_Text_JohnRematchDefeat:
	.string "JOHN: Oh, my. We lost again, dear.$"

MeteorFalls_1F_2R_Text_JohnPostRematch:
	.string "JOHN: Fifty years… We battled every\n"
	.string "single day.\p"
	.string "That's why my hearing is gone.$"

MeteorFalls_1F_2R_Text_JohnRematchNotEnoughMons:
	.string "JOHN: Come back with more POKéMON,\n"
	.string "young one.$"

MeteorFalls_1F_2R_Text_JayRematchIntro:
	.string "JAY: Fifty years of supporting each\n"
	.string "other.\p"
	.string "He still can't find the remote.$"

MeteorFalls_1F_2R_Text_JayRematchDefeat:
	.string "JAY: Oh, dear. We lost again, my dear\n"
	.string "husband.$"

MeteorFalls_1F_2R_Text_JayPostRematch:
	.string "JAY: Fifty years… So many memories.\p"
	.string "Most of them about the remote.$"

MeteorFalls_1F_2R_Text_JayRematchNotEnoughMons:
	.string "JAY: Bring more POKéMON, dear. We battle\n"
	.string "as a pair.$"

