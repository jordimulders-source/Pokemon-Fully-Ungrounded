Route126_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route126_OnTransition
	.byte 0

Route126_OnTransition:
	call Route126_EventScript_ZV3Night
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

Route126_EventScript_Barry::
	trainerbattle_single TRAINER_BARRY, Route126_Text_BarryIntro, Route126_Text_BarryDefeat
	msgbox Route126_Text_BarryPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Dean::
	trainerbattle_single TRAINER_DEAN, Route126_Text_DeanIntro, Route126_Text_DeanDefeat
	msgbox Route126_Text_DeanPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Nikki::
	trainerbattle_single TRAINER_NIKKI, Route126_Text_NikkiIntro, Route126_Text_NikkiDefeat
	msgbox Route126_Text_NikkiPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Brenda::
	trainerbattle_single TRAINER_BRENDA, Route126_Text_BrendaIntro, Route126_Text_BrendaDefeat
	msgbox Route126_Text_BrendaPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Leonardo::
	trainerbattle_single TRAINER_LEONARDO, Route126_Text_LeonardoIntro, Route126_Text_LeonardoDefeat
	msgbox Route126_Text_LeonardoPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Isobel::
	trainerbattle_single TRAINER_ISOBEL, Route126_Text_IsobelIntro, Route126_Text_IsobelDefeat
	msgbox Route126_Text_IsobelPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Sienna::
	trainerbattle_single TRAINER_SIENNA, Route126_Text_SiennaIntro, Route126_Text_SiennaDefeat
	msgbox Route126_Text_SiennaPostBattle, MSGBOX_AUTOCLOSE
	end

Route126_EventScript_Pablo::
	trainerbattle_single TRAINER_PABLO_1, Route126_Text_PabloIntro, Route126_Text_PabloDefeat, Route126_EventScript_RegisterPablo
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, Route126_EventScript_RematchPablo
	msgbox Route126_Text_PabloPostBattle, MSGBOX_DEFAULT
	release
	end

Route126_EventScript_RegisterPablo::
	special PlayerFaceTrainerAfterBattle
	waitmovement 0
	msgbox Route126_Text_PabloRegister, MSGBOX_DEFAULT
	register_matchcall TRAINER_PABLO_1
	release
	end

Route126_EventScript_RematchPablo::
	trainerbattle_rematch TRAINER_PABLO_1, Route126_Text_PabloRematchIntro, Route126_Text_PabloRematchDefeat
	msgbox Route126_Text_PabloPostRematch, MSGBOX_AUTOCLOSE
	end

@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---
Route126_EventScript_ZVOldCouple::
	trainerbattle_double TRAINER_OLD_COUPLE_HAL_AND_MAE, Route126_Text_ZVOldCouple_Intro, Route126_Text_ZVOldCouple_Defeat, Route126_Text_ZVOldCouple_NotEnough
	msgbox Route126_Text_ZVOldCouple_Post, MSGBOX_AUTOCLOSE
	end

Route126_Text_ZVOldCouple_Intro:
	.string "HAL: Fifty years married, and every\nanniversary we picnic on a sandbank.\pMAE: The tide takes the sandbank\nat four. We have until then.\lMake it quick, dear.$"

Route126_Text_ZVOldCouple_Defeat:
	.string "HAL: Mae, the young one won.\nMAE: I heard, Hal. I'm right here.$"

Route126_Text_ZVOldCouple_NotEnough:
	.string "HAL: Bring a friend, youngster.\nWe only fight as a couple.\lIt's in the vows.$"

Route126_Text_ZVOldCouple_Post:
	.string "MAE: Hal proposed on this very\nsandbank. It was a different\lsandbank. Sandbanks move.$"

Route126_EventScript_ZVVolunteer::
	msgbox Route126_Text_ZVVolunteer, MSGBOX_NPC
	end

Route126_Text_ZVVolunteer:
	.string "Welcome to the GREAT PACIFIDLOG\nGARBAGE PATCH. Day 412 of the\lclean-up.\pSo far I've removed one sock.\nIt came back. With a friend.\pThe currents bring everything\nhere. Last week: a whole TV.\lStill showing the weather.$"

Route126_EventScript_ZVCrate::
	lock
	goto_if_set FLAG_ROUTE_126_CRATE_SOLVED, Route126_EventScript_ZVCrate_Done
	msgbox Route126_Text_ZVCrate, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route126_EventScript_ZVCrate_No
	msgbox Route126_Text_ZVCrateYes, MSGBOX_DEFAULT
	giveitem ITEM_PP_MAX
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_ROUTE_126_CRATE_SOLVED
	release
	end
Route126_EventScript_ZVCrate_No:
	msgbox Route126_Text_ZVCrateNo, MSGBOX_DEFAULT
	release
	end
Route126_EventScript_ZVCrate_Done:
	msgbox Route126_Text_ZVCrateDone, MSGBOX_DEFAULT
	release
	end

Route126_Text_ZVCrate:
	.string "A crate is floating here. Stamped on\nthe lid: 'ANSWER ME AND I OPEN.'\pIt speaks. Somehow.\p'What has a bed but never sleeps,\nand a mouth but never eats?'\p...\p'A RIVER. Obviously.\nWas that correct?'$"

Route126_Text_ZVCrateYes:
	.string "'Thank you. Nobody ever lets me\nwin.' The lid creaks open.$"

Route126_Text_ZVCrateNo:
	.string "'...Then YOU tell me what it is.'\pThe crate sulks. Loudly.$"

Route126_Text_ZVCrateDone:
	.string "The crate is empty. It is thinking\nof a new riddle. It's been a while.$"

Route126_EventScript_ZVDuck::
	msgbox Route126_Text_ZVDuck, MSGBOX_SIGN
	end

Route126_Text_ZVDuck:
	.string "A pink rubber duck.\pOn closer inspection: a DITTO.\nIt has been a duck for so long\lit has forgotten how to stop.\pIt seems happy. Let it be.$"

Route126_EventScript_ZVOswald::
	trainerbattle_single TRAINER_BIRD_KEEPER_OSWALD, Route126_Text_ZVOswald_Intro, Route126_Text_ZVOswald_Defeat
	msgbox Route126_Text_ZVOswald_Post, MSGBOX_AUTOCLOSE
	end

Route126_Text_ZVOswald_Intro:
	.string "I came out here to watch seabirds.\nMy birds don't swim. Or float.\pWe've been on this rock since\nTuesday. Battle me, it's something\lto do.$"

Route126_Text_ZVOswald_Defeat:
	.string "Squawk.\n...Sorry, that was me.$"

Route126_Text_ZVOswald_Post:
	.string "If you see a boat, wave it over.\nNot too much. My birds are proud.$"

Route126_EventScript_ZVSirena::
	trainerbattle_single TRAINER_SIRENA, Route126_Text_ZVSirena_Intro, Route126_Text_ZVSirena_Defeat
	msgbox Route126_Text_ZVSirena_Post, MSGBOX_AUTOCLOSE
	end

Route126_Text_ZVSirena_Intro:
	.string "Shh! I'm a MERMAID.\pMy lawyer says I have to add:\n'legally a swimmer in a costume.'\pMy POKeMON are very rare and\nvery tiny. Don't hurt them. Or do.\lIt's a battle.$"

Route126_Text_ZVSirena_Defeat:
	.string "The tail is rented. I can't afford\nto lose. I just did. Oh no.$"

Route126_Text_ZVSirena_Post:
	.string "Under the sea it's better, down\nwhere it's wetter. I sing that\lto the WAILMER. They leave.$"
@ --- einde zee_vulling_1 ---

@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---
Route126_EventScript_ZV3Night::
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, Route126_EventScript_ZV3Night_End
	setflag FLAG_TEMP_11
Route126_EventScript_ZV3Night_End:
	return

Route126_EventScript_ZV3Marty::
	trainerbattle_single TRAINER_SAILOR_MARTY, Route126_Text_ZV3Marty_Intro, Route126_Text_ZV3Marty_Defeat
	msgbox Route126_Text_ZV3Marty_Post, MSGBOX_AUTOCLOSE
	end

Route126_Text_ZV3Marty_Intro:
	.string "See that pile of junk? That was my\nship. Well, a third of it.\pThe other two thirds are a sock\nand that TV. The ocean doesn't\ldo refunds.$"

Route126_Text_ZV3Marty_Defeat:
	.string "Sunk twice in one week.\nThat has to be a record.$"

Route126_Text_ZV3Marty_Post:
	.string "Every morning I salute my ship.\nEvery morning a WINGULL sits on it.\lWe have an understanding.$"

Route126_EventScript_ZV3TV::
	lock
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, Route126_EventScript_ZV3TV_Night
	msgbox Route126_Text_ZV3TV, MSGBOX_DEFAULT
	release
	end
Route126_EventScript_ZV3TV_Night:
	msgbox Route126_Text_ZV3TVNight, MSGBOX_DEFAULT
	release
	end

Route126_Text_ZV3TV:
	.string "A TV washed up in a crate. It has\nno cable and no power.\pIt's showing the weather anyway.\nForecast for this sandbank:\l'GARBAGE, WITH SPELLS OF GARBAGE.'$"

Route126_Text_ZV3TVNight:
	.string "At night the TV picks up\nPOKeNAV RADIO.\p'...and that was the shipping\nforecast. Route 126: moderate,\loccasionally a sock.'$"

Route126_EventScript_ZV3Seel::
	lock
	faceplayer
	playmoncry SPECIES_SEEL, CRY_MODE_NORMAL
	msgbox Route126_Text_ZV3Seel, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route126_Text_ZV3Seel:
	.string "SEEL: Arf.\pA SEEL is listening to the radio\nwith its eyes closed.\pIt shushes you. This is the\nshipping forecast. It's important.$"

Route126_EventScript_ZV3Ticket::
	msgbox Route126_Text_ZV3Ticket, MSGBOX_SIGN
	end

Route126_Text_ZV3Ticket:
	.string "A soggy ticket in the sand:\p'GREAT PACIFIDLOG GARBAGE PATCH.\nADMIT ONE. NO RE-ENTRY.\lNO EXIT EITHER, REALLY.'$"
@ --- einde zee_vulling_3 ---
