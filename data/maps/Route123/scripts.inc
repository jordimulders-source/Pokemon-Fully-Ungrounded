Route123_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route123_OnTransition
	.byte 0

Route123_OnTransition:
	call Route123_EventScript_Legends2_Transition
	special SetRoute123Weather
	end

Route123_EventScript_GigaDrainGirl::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_GIGA_DRAIN, Route123_EventScript_ReceivedGigaDrain
	msgbox Route123_Text_LoveGrassMonsHaveAny, MSGBOX_DEFAULT
	special IsGrassTypeInParty
	goto_if_eq VAR_RESULT, FALSE, Route123_EventScript_NoGrassMons
	msgbox Route123_Text_YouLikeGrassMonsTooHaveThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_GIGA_DRAIN
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_GIGA_DRAIN
	msgbox Route123_Text_CheckTreesWithMyGrassMon, MSGBOX_DEFAULT
	release
	end

Route123_EventScript_NoGrassMons::
	release
	end

Route123_EventScript_ReceivedGigaDrain::
	msgbox Route123_Text_CheckTreesWithMyGrassMon, MSGBOX_DEFAULT
	release
	end

Route123_EventScript_RouteSign::
	msgbox Route123_Text_RouteSign, MSGBOX_SIGN
	end

Route123_EventScript_RouteSignMtPyre::
	msgbox Route123_Text_RouteSignMtPyre, MSGBOX_SIGN
	end

Route123_EventScript_BerryMastersHouseSign::
	msgbox Route123_Text_BerryMastersHouse, MSGBOX_SIGN
	end

Route123_EventScript_Scarlet::
	trainerbattle_single TRAINER_SCARLET, Route123_Text_WendyIntro, Route123_Text_WendyDefeat
	msgbox Route123_Text_WendyPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Braxton::
	trainerbattle_single TRAINER_BRAXTON, Route123_Text_BraxtonIntro, Route123_Text_BraxtonDefeat
	msgbox Route123_Text_BraxtonPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Violet::
	trainerbattle_single TRAINER_VIOLET, Route123_Text_VioletIntro, Route123_Text_VioletDefeat
	msgbox Route123_Text_VioletPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Cameron::
	trainerbattle_single TRAINER_CAMERON_1, Route123_Text_CameronIntro, Route123_Text_CameronDefeat, Route123_EventScript_RegisterCameron
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route123_EventScript_RematchCameron
	msgbox Route123_Text_CameronPostBattle, MSGBOX_DEFAULT
	release
	end

Route123_EventScript_RegisterCameron::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route123_Text_CameronRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_CAMERON_1
	release
	end

Route123_EventScript_RematchCameron::
	trainerbattle_rematch TRAINER_CAMERON_1, Route123_Text_CameronRematchIntro, Route123_Text_CameronRematchDefeat
	msgbox Route123_Text_CameronPostRematch, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Jacki::
	trainerbattle_single TRAINER_JACKI_1, Route123_Text_JackiIntro, Route123_Text_JackiDefeat, Route123_EventScript_RegisterJacki
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route123_EventScript_RematchJacki
	msgbox Route123_Text_JackiPostBattle, MSGBOX_DEFAULT
	release
	end

Route123_EventScript_RegisterJacki::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route123_Text_JackiRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_JACKI_1
	release
	end

Route123_EventScript_RematchJacki::
	trainerbattle_rematch TRAINER_JACKI_1, Route123_Text_JackiRematchIntro, Route123_Text_JackiRematchDefeat
	msgbox Route123_Text_JackiPostRematch, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Miu::
	trainerbattle_double TRAINER_MIU_AND_YUKI, Route123_Text_MiuIntro, Route123_Text_MiuDefeat, Route123_Text_MiuNotEnoughMons
	msgbox Route123_Text_MiuPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Yuki::
	trainerbattle_double TRAINER_MIU_AND_YUKI, Route123_Text_YukiIntro, Route123_Text_YukiDefeat, Route123_Text_YukiNotEnoughMons
	msgbox Route123_Text_YukiPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Kindra::
	trainerbattle_single TRAINER_KINDRA, Route123_Text_KindraIntro, Route123_Text_KindraDefeat
	msgbox Route123_Text_KindraPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Frederick::
	trainerbattle_single TRAINER_FREDRICK, Route123_Text_FrederickIntro, Route123_Text_FrederickDefeat
	msgbox Route123_Text_FrederickPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Alberto::
	trainerbattle_single TRAINER_ALBERTO, Route123_Text_AlbertoIntro, Route123_Text_AlbertoDefeat
	msgbox Route123_Text_AlbertoPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Ed::
	trainerbattle_single TRAINER_ED, Route123_Text_EdIntro, Route123_Text_EdDefeat
	msgbox Route123_Text_EdPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Kayley::
	trainerbattle_single TRAINER_KAYLEY, Route123_Text_KayleyIntro, Route123_Text_KayleyDefeat
	msgbox Route123_Text_KayleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Jonas::
	trainerbattle_single TRAINER_JONAS, Route123_Text_JonasIntro, Route123_Text_JonasDefeat
	msgbox Route123_Text_JonasPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_VioletCooltrainer::
	trainerbattle_single TRAINER_VIOLET_COOLTRAINER, Route123_Text_JazmynIntro, Route123_Text_JazmynDefeat
	msgbox Route123_Text_JazmynPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Davis::
	trainerbattle_single TRAINER_DAVIS, Route123_Text_DavisIntro, Route123_Text_DavisDefeat
	msgbox Route123_Text_DavisPostBattle, MSGBOX_AUTOCLOSE
	end

Route123_EventScript_Fernando::
	trainerbattle_single TRAINER_FERNANDO_1, Route123_Text_FernandoIntro, Route123_Text_FernandoDefeat, Route123_EventScript_RegisterFernando
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route123_EventScript_RematchFernando
	msgbox Route123_Text_FernandoPostBattle, MSGBOX_DEFAULT
	release
	end

Route123_EventScript_RegisterFernando::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route123_Text_FernandoRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_FERNANDO_1
	release
	end

Route123_EventScript_RematchFernando::
	trainerbattle_rematch TRAINER_FERNANDO_1, Route123_Text_FernandoRematchIntro, Route123_Text_FernandoRematchDefeat
	msgbox Route123_Text_FernandoPostRematch, MSGBOX_AUTOCLOSE
	end

Route123_Text_LoveGrassMonsHaveAny:
	.string "I love GRASS-type POKéMON!\p"
	.string "Do you have any?$"

Route123_Text_YouLikeGrassMonsTooHaveThis:
	.string "Oh?\p"
	.string "You like GRASS-type POKéMON too!\p"
	.string "I'm so happy! Take this. A token of our\n"
	.string "friendship.$"

Route123_Text_CheckTreesWithMyGrassMon:
	.string "I check trees with my GRASS POKéMON.\p"
	.string "I'm a tree doctor.\p"
	.string "The trees have no insurance, though.$"

Route123_Text_RouteSign:
	.string "{RIGHT_ARROW} ROUTE 123\n"
	.string "{LEFT_ARROW} ROUTE 118\p"
	.string "The sign painter gave up on this one.$"

Route123_Text_RouteSignMtPyre:
	.string "{UP_ARROW} MT. PYRE\n"
	.string "“Forbidden to the faint of heart.”\p"
	.string "Also to the easily spooked and ZUBAT\n"
	.string "haters.$"

Route123_Text_BerryMastersHouse:
	.string "BERRY MASTER'S HOUSE\p"
	.string "For all your experimentation and\n"
	.string "cross-breeding on BERRIES.$"

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
Route123_EventScript_Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	setflag FLAG_HIDE_LEGENDS_MELOETTA
	goto_if_set FLAG_ROUTE123_SNORLAX_GONE, Route123_EventScript_Legends2_TransitionMeloetta
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route123_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	return
Route123_EventScript_Legends2_TransitionMeloetta:
	goto_if_set FLAG_CAUGHT_MELOETTA, Route123_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_MELOETTA
Route123_EventScript_Legends2_TransitionEnd:
	return

Route123_EventScript_Snorlax::
	lock
	msgbox Route123_Text_Snorlax, MSGBOX_DEFAULT
	release
	end

@ Post-game: de Poke Flute naast Snorlax. Oppakken = meteen spelen (geen ja/nee), Snorlax loopt weg, Meloetta komt.
Route123_EventScript_PokeFlute::
	lock
	removeobject LOCALID_LEGENDS_POKE_FLUTE
	setflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	giveitem ITEM_POKE_FLUTE
	msgbox Route123_Text_FluteBlow, MSGBOX_DEFAULT
	closemessage
	playfanfare MUS_RG_POKE_FLUTE
	waitfanfare
	playmoncry SPECIES_SNORLAX, CRY_MODE_ENCOUNTER
	applymovement LOCALID_LEGENDS_SNORLAX, Common_Movement_ExclamationMark
	waitmovement 0
	waitmoncry
	msgbox Route123_Text_SnorlaxWakes, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_LEGENDS_SNORLAX, Route123_EventScript_Movement_SnorlaxLeaves
	waitmovement 0
	removeobject LOCALID_LEGENDS_SNORLAX
	setflag FLAG_ROUTE123_SNORLAX_GONE
	delay 30
	msgbox Route123_Text_SomeoneHums, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_LEGENDS_MELOETTA
	addobject LOCALID_LEGENDS_MELOETTA
	playse SE_M_HEAL_BELL
	waitse
	playmoncry SPECIES_MELOETTA_ARIA, CRY_MODE_ENCOUNTER
	msgbox Route123_Text_MeloettaAppears, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	goto Route123_EventScript_Meloetta_Battle

Route123_EventScript_Movement_SnorlaxLeaves:
	walk_slow_down
	walk_slow_down
	walk_slow_down
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_slow_down
	step_end

Route123_Text_Snorlax:
	.string "A SNORLAX is asleep in the only gap in\n"
	.string "the fence.\p"
	.string "Behind it: the BERRY MASTER's prize\n"
	.string "fields. In front of it: you. It has\l"
	.string "chosen a side.\p"
	.string "Snoring intensifies.$"

Route123_Text_FluteBlow:
	.string "A POKé FLUTE was lying next to SNORLAX,\n"
	.string "like a snooze button someone left out.\p"
	.string "You play it. Obviously.$"

Route123_Text_SnorlaxWakes:
	.string "SNORLAX woke up!\p"
	.string "It looks at the berries. It looks at you.\n"
	.string "It decides neither is worth getting up\l"
	.string "for, gets up anyway, and wanders off to\l"
	.string "sleep somewhere quieter.$"

Route123_Text_SomeoneHums:
	.string "...Someone is humming your song back at\n"
	.string "you. Slightly better.$"

Route123_Text_MeloettaAppears:
	.string "MELOETTA drifted down out of nowhere!\p"
	.string "It was sleeping on SNORLAX's belly the\n"
	.string "whole time. Your solo has been reviewed.\l"
	.string "The review is a fight.$"

Route123_EventScript_Meloetta::
	lock
	faceplayer
	playmoncry SPECIES_MELOETTA_ARIA, CRY_MODE_ENCOUNTER
	msgbox Route123_Text_Meloetta, MSGBOX_DEFAULT
	waitmoncry
	closemessage
Route123_EventScript_Meloetta_Battle::
	setwildbattle SPECIES_MELOETTA_ARIA, 62
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Route123_EventScript_Meloetta_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, Route123_EventScript_Meloetta_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, Route123_EventScript_Meloetta_Stays
	removeobject LOCALID_LEGENDS_MELOETTA
	setflag FLAG_HIDE_LEGENDS_MELOETTA
	msgbox Route123_Text_MeloettaFled, MSGBOX_DEFAULT
Route123_EventScript_Meloetta_Stays::
	release
	end

Route123_EventScript_Meloetta_Caught::
	removeobject LOCALID_LEGENDS_MELOETTA
	setflag FLAG_HIDE_LEGENDS_MELOETTA
	setflag FLAG_CAUGHT_MELOETTA
	release
	end

Route123_Text_Meloetta:
	.string "La la laaa!\p"
	.string "(MELOETTA is still humming your POKé\n"
	.string "FLUTE tune. It has added a key change.\l"
	.string "It wants a rematch.)$"

Route123_Text_MeloettaFled:
	.string "MELOETTA spun away mid-note.\p"
	.string "It'll be back for the encore. It always\n"
	.string "comes back for the encore.$"
@ --- einde legends2 ---
