@ Project Grounded: Reginald, de "vijfde" van de Elite Four (Victory Road B2F, gat op het eilandje in
@ het bovenmeer; Surf). Sterk team, geeft daarna TM Flamethrower.
VictoryRoad_Hermit_MapScripts::
	.byte 0

VictoryRoad_Hermit_EventScript_Reginald::
	trainerbattle_single TRAINER_VR_REGINALD, VictoryRoad_Hermit_Text_ReginaldIntro, VictoryRoad_Hermit_Text_ReginaldDefeat, VictoryRoad_Hermit_EventScript_ReginaldDefeated
	goto_if_unset FLAG_RECEIVED_TM_FLAMETHROWER_REGINALD, VictoryRoad_Hermit_EventScript_GiveTM
	msgbox VictoryRoad_Hermit_Text_ReginaldPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_Hermit_EventScript_ReginaldDefeated::
	msgbox VictoryRoad_Hermit_Text_ReginaldGiveTM, MSGBOX_DEFAULT
VictoryRoad_Hermit_EventScript_GiveTM::
	giveitem ITEM_TM_FLAMETHROWER
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_FLAMETHROWER_REGINALD
	msgbox VictoryRoad_Hermit_Text_ReginaldPostBattle, MSGBOX_DEFAULT
	release
	end

VictoryRoad_Hermit_EventScript_Application::
	msgbox VictoryRoad_Hermit_Text_Application, MSGBOX_SIGN
	end

VictoryRoad_Hermit_Text_ReginaldIntro:
	.string "Ah. A visitor. Sit. Not there,\n"
	.string "that's where my dignity used to sit.\p"
	.string "I am REGINALD. ELITE FOUR\n"
	.string "candidate. The fifth one.\p"
	.string "Thirty years ago I built the\n"
	.string "perfect team. A counter for every\l"
	.string "single member.\p"
	.string "Then they told me the ELITE FOUR\n"
	.string "has, and I quote, “four members”.\p"
	.string "So I wait. Until one of them\n"
	.string "retires. Or dies. I'm flexible.\p"
	.string "You look like you'll reach them.\n"
	.string "So reach ME first. Dress rehearsal.$"

VictoryRoad_Hermit_Text_ReginaldDefeat:
	.string "So THIS is what the ELITE FOUR\n"
	.string "feels like. Bracing.$"

VictoryRoad_Hermit_Text_ReginaldGiveTM:
	.string "Take this. I was saving it for\n"
	.string "SIDNEY's funeral.\p"
	.string "He keeps not having one.$"

VictoryRoad_Hermit_Text_ReginaldPostBattle:
	.string "When you're CHAMPION, put in a\n"
	.string "good word for me.\p"
	.string "Tell them I'm available.\n"
	.string "I've been available since 1994.$"

VictoryRoad_Hermit_Text_Application:
	.string "A framed letter, slightly damp.\p"
	.string "APPLICATION: ELITE FOUR, SEAT 5\n"
	.string "STATUS: Rejected. Seat does not\l"
	.string "exist.\p"
	.string "APPEAL: Rejected.\n"
	.string "APPEAL OF APPEAL: Pending since 1996.$"
