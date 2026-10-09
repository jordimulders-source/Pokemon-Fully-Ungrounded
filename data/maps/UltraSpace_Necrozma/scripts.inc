UltraSpace_Necrozma_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, UltraSpace_Necrozma_OnResume
	.byte 0

UltraSpace_Necrozma_OnResume:
	setstepcallback STEP_CB_ULTRA_WORLDS
	end

UltraSpace_Necrozma_EventScript_UB::
	lock
	faceplayer
	playmoncry SPECIES_NECROZMA, CRY_MODE_ENCOUNTER
	msgbox UltraSpace_Necrozma_Text_UB, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_NECROZMA, 95
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, UltraSpace_Necrozma_EventScript_UBCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, UltraSpace_Necrozma_EventScript_UBBack
	release
	end

UltraSpace_Necrozma_EventScript_UBBack::
	msgbox UltraSpace_Necrozma_Text_UBBack, MSGBOX_DEFAULT
	release
	end

UltraSpace_Necrozma_EventScript_UBCaught::
	setflag FLAG_ULTRA_NECROZMA
	goto UltraSpace_EventScript_CaughtFade

UltraSpace_Necrozma_EventScript_Minior::
	msgbox UltraSpace_Necrozma_Text_Minior, MSGBOX_NPC
	end

UltraSpace_Necrozma_EventScript_Carbink::
	msgbox UltraSpace_Necrozma_Text_Carbink, MSGBOX_NPC
	end

UltraSpace_Necrozma_EventScript_Cryogonal::
	msgbox UltraSpace_Necrozma_Text_Cryogonal, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Necrozma_Text_UB:
	.string "A POKéMON made of hungry darkness,\n"
	.string "sucking the light out of the prisms.\p"
	.string "It wants your light. You only have a\n"
	.string "flashlight app and a bad attitude.$"

UltraSpace_Necrozma_Text_UBBack:
	.string "NECROZMA folds back into the dark. The\n"
	.string "prisms dim. They're waiting for you.$"

UltraSpace_Necrozma_Text_Minior:
	.string "A MINIOR is staring into the rainbow\n"
	.string "like a moth. A very rocky, very doomed\l"
	.string "moth.$"

UltraSpace_Necrozma_Text_Carbink:
	.string "CARBINK is admiring its reflection in\n"
	.string "the floor. The floor is admiring it back.$"

UltraSpace_Necrozma_Text_Cryogonal:
	.string "CRYOGONAL spins slowly, refracting your\n"
	.string "face into seven slightly worse faces.$"

