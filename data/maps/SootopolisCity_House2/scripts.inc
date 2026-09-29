SootopolisCity_House2_MapScripts::
	.byte 0

SootopolisCity_House2_EventScript_ExpertF::
	lock
	faceplayer
	msgbox SootopolisCity_House2_Text_DidYouKnowAboutMtPyreOrbs, MSGBOX_YESNO
	call_if_eq VAR_RESULT, YES, SootopolisCity_House2_EventScript_KnowAboutOrbs
	call_if_eq VAR_RESULT, NO, SootopolisCity_House2_EventScript_DontKnowAboutOrbs
	release
	end

SootopolisCity_House2_EventScript_KnowAboutOrbs::
	msgbox SootopolisCity_House2_Text_YesTwoOrbsSideBySide, MSGBOX_DEFAULT
	return

SootopolisCity_House2_EventScript_DontKnowAboutOrbs::
	msgbox SootopolisCity_House2_Text_OughtToVisitAndSee, MSGBOX_DEFAULT
	return

SootopolisCity_House2_Text_DidYouKnowAboutMtPyreOrbs:
	.string "MT. PYRE…\p"
	.string "At its peak are two ORBS, side by side.\p"
	.string "Like the eyes of an old god. Watching.\p"
	.string "Have you seen them?$"

SootopolisCity_House2_Text_YesTwoOrbsSideBySide:
	.string "Yes, two orbs, side by side…\p"
	.string "Seeing them together… It's soothing.\n"
	.string "And a little creepy.$"

SootopolisCity_House2_Text_OughtToVisitAndSee:
	.string "No? Then go and see.\p"
	.string "Bring a snack. It's a long climb.$"

