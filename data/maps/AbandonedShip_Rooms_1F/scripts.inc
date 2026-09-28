AbandonedShip_Rooms_1F_MapScripts::
	.byte 0

AbandonedShip_Rooms_1F_EventScript_Gentleman::
	msgbox AbandonedShip_Rooms_1F_Text_TakingALookAround, MSGBOX_NPC
	end

AbandonedShip_Rooms_1F_EventScript_Demetrius::
	trainerbattle_single TRAINER_DEMETRIUS, AbandonedShip_Rooms_1F_Text_DemetriusIntro, AbandonedShip_Rooms_1F_Text_DemetriusDefeat
	msgbox AbandonedShip_Rooms_1F_Text_DemetriusPostBattle, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms_1F_EventScript_Thalia::
	trainerbattle_single TRAINER_THALIA_1, AbandonedShip_Rooms_1F_Text_ThaliaIntro, AbandonedShip_Rooms_1F_Text_ThaliaDefeat, AbandonedShip_Rooms_1F_EventScript_RegisterThalia
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, AbandonedShip_Rooms_1F_EventScript_ThaliaRematch
	msgbox AbandonedShip_Rooms_1F_Text_ThaliaPostBattle, MSGBOX_DEFAULT
	release
	end

AbandonedShip_Rooms_1F_EventScript_RegisterThalia::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox AbandonedShip_Rooms_1F_Text_ThaliaRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_THALIA_1
	release
	end

AbandonedShip_Rooms_1F_EventScript_ThaliaRematch::
	trainerbattle_rematch TRAINER_THALIA_1, AbandonedShip_Rooms_1F_Text_ThaliaRematchIntro, AbandonedShip_Rooms_1F_Text_ThaliaRematchDefeat
	msgbox AbandonedShip_Rooms_1F_Text_ThaliaPostRematch, MSGBOX_AUTOCLOSE
	end

AbandonedShip_Rooms_1F_Text_TakingALookAround:
	.string "Hmmphh, kids these days. Just taking\n"
	.string "selfies anywhere. Even in abandoned\l"
	.string "boats. Like who cares that you took a\l"
	.string "selfie with some decomposed corpses.$"

AbandonedShip_Rooms_1F_Text_ThaliaIntro:
	.string "Ugh I hate being an Urbex influencer.\n"
	.string "Brings me to all these scary places.$"

AbandonedShip_Rooms_1F_Text_ThaliaDefeat:
	.string "There's nothing to see here...$"

AbandonedShip_Rooms_1F_Text_ThaliaPostBattle:
	.string "The man next door…\p"
	.string "He says he's just sightseeing, but I\n"
	.string "don't know about that. I've seen him\l"
	.string "before. He stands still for hours.$"

AbandonedShip_Rooms_1F_Text_ThaliaRegister:
	.string "You're such a tough TRAINER! Let me add\n"
	.string "you on my social media apps. I wanna get\l"
	.string "to 10k!$"

AbandonedShip_Rooms_1F_Text_ThaliaRematchIntro:
	.string "Yes... I am still here, but so are you. My\n"
	.string "followers would love this!$"

AbandonedShip_Rooms_1F_Text_ThaliaRematchDefeat:
	.string "I shouldn't stream this.$"

AbandonedShip_Rooms_1F_Text_ThaliaPostRematch:
	.string "I'm sure that man's up to something! He\n"
	.string "just acts so suspiciously! Is he still\l"
	.string "wearing clothes?$"

AbandonedShip_Rooms_1F_Text_DemetriusIntro:
	.string "They told me I could find a Skibidi\n"
	.string "Toilet here!$"

AbandonedShip_Rooms_1F_Text_DemetriusDefeat:
	.string "I've been lied to?$"

AbandonedShip_Rooms_1F_Text_DemetriusPostBattle:
	.string "I'm in trouble with my mom, so I ran. Keep\n"
	.string "it a secret where I am! Skibidi!$"

