SlateportCity_PokemonFanClub_EventScript_SwaggerTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_SWAGGER, MoveTutor_EventScript_SwaggerAgain
	msgbox MoveTutor_Text_SwaggerTeach, MSGBOX_YESNO
MoveTutor_EventScript_SwaggerAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_SwaggerDeclined
	msgbox MoveTutor_Text_SwaggerWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_SWAGGER
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_SwaggerDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_SWAGGER
	goto MoveTutor_EventScript_SwaggerTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_SwaggerAgain::
	buffermovename STR_VAR_1, MOVE_SWAGGER
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_SwaggerAnswer
	end

MoveTutor_EventScript_SwaggerDeclined::
	msgbox MoveTutor_Text_SwaggerDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_SwaggerTaught::
	msgbox MoveTutor_Text_SwaggerTaught, MSGBOX_DEFAULT
	release
	end

MauvilleCity_EventScript_RolloutTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_ROLLOUT, MoveTutor_EventScript_RolloutAgain
	msgbox MoveTutor_Text_RolloutTeach, MSGBOX_YESNO
MoveTutor_EventScript_RolloutAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_RolloutDeclined
	msgbox MoveTutor_Text_RolloutWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_ROLLOUT
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_RolloutDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_ROLLOUT
	goto MoveTutor_EventScript_RolloutTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_RolloutAgain::
	buffermovename STR_VAR_1, MOVE_ROLLOUT
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_RolloutAnswer
	end

MoveTutor_EventScript_RolloutDeclined::
	msgbox MoveTutor_Text_RolloutDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_RolloutTaught::
	msgbox MoveTutor_Text_RolloutTaught, MSGBOX_DEFAULT
	release
	end

VerdanturfTown_PokemonCenter_1F_EventScript_FuryCutterTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_FURY_CUTTER, MoveTutor_EventScript_FuryCutterAgain
	msgbox MoveTutor_Text_FuryCutterTeach, MSGBOX_YESNO
MoveTutor_EventScript_FuryCutterAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_FuryCutterDeclined
	msgbox MoveTutor_Text_FuryCutterWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_FURY_CUTTER
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_FuryCutterDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_FURY_CUTTER
	goto MoveTutor_EventScript_FuryCutterTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_FuryCutterAgain::
	buffermovename STR_VAR_1, MOVE_FURY_CUTTER
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_FuryCutterAnswer
	end

MoveTutor_EventScript_FuryCutterDeclined::
	msgbox MoveTutor_Text_FuryCutterDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_FuryCutterTaught::
	msgbox MoveTutor_Text_FuryCutterTaught, MSGBOX_DEFAULT
	release
	end

LavaridgeTown_House_EventScript_MimicTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_MIMIC, MoveTutor_EventScript_MimicAgain
	msgbox MoveTutor_MimicTeach, MSGBOX_YESNO
MoveTutor_EventScript_MimicAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_MimicDeclined
	msgbox MoveTutor_Text_MimicWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_MIMIC
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_MimicDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_MIMIC
	goto MoveTutor_EventScript_MimicTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_MimicAgain::
	buffermovename STR_VAR_1, MOVE_MIMIC
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_MimicAnswer
	end

MoveTutor_EventScript_MimicDeclined::
	msgbox MoveTutor_MimicDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_MimicTaught::
	msgbox MoveTutor_Text_MimicTaught, MSGBOX_DEFAULT
	release
	end

FallarborTown_Mart_EventScript_MetronomeTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_METRONOME, MoveTutor_EventScript_MetronomeAgain
	msgbox MoveTutor_Text_MetronomeTeach, MSGBOX_YESNO
MoveTutor_EventScript_MetronomeAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_MetronomeDeclined
	msgbox MoveTutor_Text_MetronomeWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_METRONOME
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_MetronomeDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_METRONOME
	goto MoveTutor_EventScript_MetronomeTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_MetronomeAgain::
	buffermovename STR_VAR_1, MOVE_METRONOME
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_MetronomeAnswer
	end

MoveTutor_EventScript_MetronomeDeclined::
	msgbox MoveTutor_Text_MetronomeDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_MetronomeTaught::
	msgbox MoveTutor_Text_MetronomeTaught, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_EventScript_SleepTalkTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_SLEEP_TALK, MoveTutor_EventScript_SleepTalkAgain
	msgbox MoveTutor_Text_SleepTalkTeach, MSGBOX_YESNO
MoveTutor_EventScript_SleepTalkAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_SleepTalkDeclined
	msgbox MoveTutor_Text_SleepTalkWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_SLEEP_TALK
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_SleepTalkDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_SLEEP_TALK
	goto MoveTutor_EventScript_SleepTalkTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_SleepTalkAgain::
	buffermovename STR_VAR_1, MOVE_SLEEP_TALK
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_SleepTalkAnswer
	end

MoveTutor_EventScript_SleepTalkDeclined::
	msgbox MoveTutor_Text_SleepTalkDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_SleepTalkTaught::
	msgbox MoveTutor_Text_SleepTalkTaught, MSGBOX_DEFAULT
	release
	end

LilycoveCity_DepartmentStoreRooftop_EventScript_SubstituteTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_SUBSTITUTE, MoveTutor_EventScript_SubstituteAgain
	msgbox MoveTutor_Text_SubstituteTeach, MSGBOX_YESNO
MoveTutor_EventScript_SubstituteAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_SubstituteDeclined
	msgbox MoveTutor_Text_SubstituteWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_SUBSTITUTE
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_SubstituteDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_SUBSTITUTE
	goto MoveTutor_EventScript_SubstituteTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_SubstituteAgain::
	buffermovename STR_VAR_1, MOVE_SUBSTITUTE
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_SubstituteAnswer
	end

MoveTutor_EventScript_SubstituteDeclined::
	msgbox MoveTutor_Text_SubstituteDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_SubstituteTaught::
	msgbox MoveTutor_Text_SubstituteTaught, MSGBOX_DEFAULT
	release
	end

MossdeepCity_EventScript_DynamicPunchTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_DYNAMICPUNCH, MoveTutor_EventScript_DynamicPunchAgain
	msgbox MoveTutor_Text_DynamicPunchTeach, MSGBOX_YESNO
MoveTutor_EventScript_DynamicPunchAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_DynamicPunchDeclined
	msgbox MoveTutor_Text_DynamicPunchWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_DYNAMIC_PUNCH
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_DynamicPunchDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_DYNAMICPUNCH
	goto MoveTutor_EventScript_DynamicPunchTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_DynamicPunchAgain::
	buffermovename STR_VAR_1, MOVE_DYNAMIC_PUNCH
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_DynamicPunchAnswer
	end

MoveTutor_EventScript_DynamicPunchDeclined::
	msgbox MoveTutor_Text_DynamicPunchDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_DynamicPunchTaught::
	msgbox MoveTutor_Text_DynamicPunchTaught, MSGBOX_DEFAULT
	release
	end

SootopolisCity_PokemonCenter_1F_EventScript_DoubleEdgeTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_DOUBLE_EDGE, MoveTutor_EventScript_DoubleEdgeAgain
	msgbox MoveTutor_Text_DoubleEdgeTeach, MSGBOX_YESNO
MoveTutor_EventScript_DoubleEdgeAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_DoubleEdgeDeclined
	msgbox MoveTutor_Text_DoubleEdgeWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_DOUBLE_EDGE
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_DoubleEdgeDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_DOUBLE_EDGE
	goto MoveTutor_EventScript_DoubleEdgeTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_DoubleEdgeAgain::
	buffermovename STR_VAR_1, MOVE_DOUBLE_EDGE
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_DoubleEdgeAnswer
	end

MoveTutor_EventScript_DoubleEdgeDeclined::
	msgbox MoveTutor_Text_DoubleEdgeDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_DoubleEdgeTaught::
	msgbox MoveTutor_Text_DoubleEdgeTaught, MSGBOX_DEFAULT
	release
	end

PacifidlogTown_PokemonCenter_1F_EventScript_ExplosionTutor::
	lock
	faceplayer
	goto_if_set FLAG_MOVE_TUTOR_TAUGHT_EXPLOSION, MoveTutor_EventScript_ExplosionAgain
	msgbox MoveTutor_Text_ExplosionTeach, MSGBOX_YESNO
MoveTutor_EventScript_ExplosionAnswer::
	goto_if_eq VAR_RESULT, NO, MoveTutor_EventScript_ExplosionDeclined
	msgbox MoveTutor_Text_ExplosionWhichMon, MSGBOX_DEFAULT
	setvar VAR_0x8005, MOVE_EXPLOSION
	call MoveTutor_EventScript_OpenPartyMenu
	goto_if_eq VAR_RESULT, 0, MoveTutor_EventScript_ExplosionDeclined
	setflag FLAG_MOVE_TUTOR_TAUGHT_EXPLOSION
	goto MoveTutor_EventScript_ExplosionTaught
	end

@ Project Grounded: tutors leren onbeperkt; na de eerste keer een korte vraag
MoveTutor_EventScript_ExplosionAgain::
	buffermovename STR_VAR_1, MOVE_EXPLOSION
	msgbox MoveTutor_Text_TeachAgain, MSGBOX_YESNO
	goto MoveTutor_EventScript_ExplosionAnswer
	end

MoveTutor_EventScript_ExplosionDeclined::
	msgbox MoveTutor_Text_ExplosionDeclined, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_ExplosionTaught::
	msgbox MoveTutor_Text_ExplosionTaught, MSGBOX_DEFAULT
	release
	end

MoveTutor_EventScript_OpenPartyMenu::
	special ChooseMonForMoveTutor
	waitstate
	lock
	faceplayer
	return

