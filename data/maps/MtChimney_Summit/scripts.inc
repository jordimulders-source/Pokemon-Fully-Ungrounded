@ Project Grounded: de echte top van Mt. Chimney (tools/grounded/maptools/chimney_ext.py).
@ Bereikbaar via de trap in de noordoostelijke bergkam van Mt. Chimney (vanaf badge 5).
@ Drie terrassen met sterke trainers, bovenin een kratermeer met een vaste Volcarona (lv 40) en de vulkanoloog.
MtChimney_Summit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtChimney_Summit_Legends2_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, MtChimney_Summit_OnResume
	.byte 0

MtChimney_Summit_OnResume:
	setstepcallback STEP_CB_ASH
	end

MtChimney_Summit_EventScript_Grant::
	trainerbattle_single TRAINER_SUMMIT_GRANT, MtChimney_Summit_Text_GrantIntro, MtChimney_Summit_Text_GrantDefeat
	msgbox MtChimney_Summit_Text_GrantPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_Summit_EventScript_Pyro::
	trainerbattle_single TRAINER_SUMMIT_PYRO, MtChimney_Summit_Text_PyroIntro, MtChimney_Summit_Text_PyroDefeat
	msgbox MtChimney_Summit_Text_PyroPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_Summit_EventScript_Vera::
	trainerbattle_single TRAINER_SUMMIT_VERA, MtChimney_Summit_Text_VeraIntro, MtChimney_Summit_Text_VeraDefeat
	msgbox MtChimney_Summit_Text_VeraPostBattle, MSGBOX_AUTOCLOSE
	end

MtChimney_Summit_EventScript_Volcarona::
	lock
	faceplayer
	msgbox MtChimney_Summit_Text_Volcarona, MSGBOX_DEFAULT
	playmoncry SPECIES_VOLCARONA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_VOLCARONA, 56
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	dowildbattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtChimney_Summit_EventScript_VolcaronaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtChimney_Summit_EventScript_VolcaronaStays
	removeobject LOCALID_SUMMIT_VOLCARONA
	setflag FLAG_HIDE_MT_CHIMNEY_SUMMIT_VOLCARONA
MtChimney_Summit_EventScript_VolcaronaStays::
	release
	end

MtChimney_Summit_EventScript_Volcanologist::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_FLAME_ORB_VOLCANOLOGIST, MtChimney_Summit_EventScript_VolcanologistDone
	msgbox MtChimney_Summit_Text_VolcanologistGift, MSGBOX_DEFAULT
	giveitem ITEM_FLAME_ORB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_FLAME_ORB_VOLCANOLOGIST
MtChimney_Summit_EventScript_VolcanologistDone::
	msgbox MtChimney_Summit_Text_VolcanologistAfter, MSGBOX_DEFAULT
	release
	end

MtChimney_Summit_EventScript_SummitSign::
	msgbox MtChimney_Summit_Text_SummitSign, MSGBOX_SIGN
	end

MtChimney_Summit_Text_GrantIntro:
	.string "The cable car goes to the crater.\n"
	.string "Real hikers go higher.\p"
	.string "Real hikers also can't feel their\n"
	.string "toes anymore. Coincidence.$"

MtChimney_Summit_Text_GrantDefeat:
	.string "Beaten above the clouds.\n"
	.string "At least it's a nice view to cry at.$"

MtChimney_Summit_Text_GrantPostBattle:
	.string "Breathe through your nose.\n"
	.string "The ash is free protein.$"

MtChimney_Summit_Text_PyroIntro:
	.string "I came up here to get closer\n"
	.string "to the sun.\p"
	.string "Turns out the volcano is closer.\n"
	.string "And angrier.$"

MtChimney_Summit_Text_PyroDefeat:
	.string "Sunburn AND a loss.\n"
	.string "Combo achievement unlocked.$"

MtChimney_Summit_Text_PyroPostBattle:
	.string "SPF 5000. That's what you need\n"
	.string "up here. SPF 5000 and therapy.$"

MtChimney_Summit_Text_VeraIntro:
	.string "I've climbed this peak every day for\n"
	.string "forty years.\p"
	.string "The volcano and I have an\n"
	.string "understanding. You do not.$"

MtChimney_Summit_Text_VeraDefeat:
	.string "Hmph. The mountain liked you.\n"
	.string "I can tell. It went quiet.$"

MtChimney_Summit_Text_VeraPostBattle:
	.string "When the ash covered the sky,\n"
	.string "something up there shone like a\l"
	.string "second sun.\p"
	.string "It still nests by the crater.\n"
	.string "Don't make it angry. It's the sun.$"

MtChimney_Summit_Text_Volcarona:
	.string "A huge moth rests by the crater,\n"
	.string "glowing like a small, judgmental sun.\p"
	.string "The ash in the air stops falling\n"
	.string "around it.$"

MtChimney_Summit_Text_VolcanologistGift:
	.string "Ah! A visitor! I'm a volcanologist.\n"
	.string "I measure how angry the mountain is.\p"
	.string "Today: “mildly passive-aggressive.”\n"
	.string "Here, take this. I tried to bottle\l"
	.string "the volcano. It went about as well\l"
	.string "as you'd think.$"

MtChimney_Summit_Text_VolcanologistAfter:
	.string "If the ground starts humming,\n"
	.string "run downhill. If it starts singing,\l"
	.string "it's just me. Probably.$"

MtChimney_Summit_Text_SummitSign:
	.string "MT. CHIMNEY - TRUE SUMMIT\p"
	.string "Congratulations! You are now the\n"
	.string "highest-ranking person in Hoenn.\p"
	.string "This title is not recognized by\n"
	.string "any government.$"

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
MtChimney_Summit_EventScript_Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_MOLTRES
	goto_if_unset FLAG_SYS_GAME_CLEAR, MtChimney_Summit_EventScript_Legends2_TransitionEnd
	goto_if_set FLAG_CAUGHT_KANTO_MOLTRES, MtChimney_Summit_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_MOLTRES
MtChimney_Summit_EventScript_Legends2_TransitionEnd:
	return

MtChimney_Summit_EventScript_Moltres::
	lock
	faceplayer
	playmoncry SPECIES_MOLTRES, CRY_MODE_ENCOUNTER
	msgbox MtChimney_Summit_Text_Moltres, MSGBOX_DEFAULT
	waitmoncry
	closemessage
MtChimney_Summit_EventScript_Moltres_Battle::
	setwildbattle SPECIES_MOLTRES, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtChimney_Summit_EventScript_Moltres_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtChimney_Summit_EventScript_Moltres_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtChimney_Summit_EventScript_Moltres_Stays
	removeobject LOCALID_LEGENDS_MOLTRES
	setflag FLAG_HIDE_LEGENDS_MOLTRES
	msgbox MtChimney_Summit_Text_MoltresFled, MSGBOX_DEFAULT
MtChimney_Summit_EventScript_Moltres_Stays::
	release
	end

MtChimney_Summit_EventScript_Moltres_Caught::
	removeobject LOCALID_LEGENDS_MOLTRES
	setflag FLAG_HIDE_LEGENDS_MOLTRES
	setflag FLAG_CAUGHT_KANTO_MOLTRES
	call Legends2_EventScript_CheckGalarArrive
	release
	end

MtChimney_Summit_Text_Moltres:
	.string "Kyaaoo!\p"
	.string "(It's warming its feet in the crater. The\n"
	.string "lava is warming its feet on MOLTRES.)$"

MtChimney_Summit_Text_MoltresFled:
	.string "MOLTRES dove straight into the lava.\p"
	.string "It does that. It's fine. It's always\n"
	.string "fine. It'll be back on the rim tomorrow,\l"
	.string "smug and slightly crispy.$"
@ --- einde legends2 ---

MtChimney_Summit_Legends2_OnTransition:
	call MtChimney_Summit_EventScript_Legends2_Transition
	end
