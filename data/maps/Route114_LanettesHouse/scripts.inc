Route114_LanettesHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_LanettesHouse_OnTransition
	.byte 0

Route114_LanettesHouse_OnTransition:
	setflag FLAG_LANDMARK_LANETTES_HOUSE
	end

Route114_LanettesHouse_EventScript_Lanette::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_DOLL_LANETTE, Route114_LanettesHouse_EventScript_OfferAdvice
	setflag FLAG_SYS_PC_LANETTE
	msgbox Route114_LanettesHouse_Text_EverythingClutteredKeepThis, MSGBOX_DEFAULT
	givedecoration DECOR_LOTAD_DOLL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowNoRoomForDecor
	setflag FLAG_RECEIVED_DOLL_LANETTE
	release
	end

Route114_LanettesHouse_EventScript_OfferAdvice::
	msgbox Route114_LanettesHouse_Text_OrganizeYourBoxes, MSGBOX_DEFAULT
	release
	end

Route114_LanettesHouse_EventScript_Notebook::
	lockall
	msgbox Route114_LanettesHouse_Text_ResearchNotesPage1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Route114_LanettesHouse_EventScript_NotebookPage2
	msgbox Route114_LanettesHouse_Text_ClosedTheNotebook, MSGBOX_DEFAULT
	releaseall
	end

Route114_LanettesHouse_EventScript_NotebookPage2::
	msgbox Route114_LanettesHouse_Text_ResearchNotesPage2, MSGBOX_YESNO
	call_if_eq VAR_RESULT, YES, Route114_LanettesHouse_EventScript_NotebookPage3
	releaseall
	end

Route114_LanettesHouse_EventScript_NotebookPage3::
	msgbox Route114_LanettesHouse_Text_ResearchNotesPage3, MSGBOX_DEFAULT
	return

Route114_LanettesHouse_EventScript_PC::
	msgbox Route114_LanettesHouse_Text_EmailFromBill, MSGBOX_SIGN
	end

Route114_LanettesHouse_Text_EverythingClutteredKeepThis:
	.string "LANETTE: Oh! {PLAYER}{KUN}!\p"
	.string "Sorry about the mess… When I research,\n"
	.string "this happens…\p"
	.string "This is embarrassing… Keep it a secret.\n"
	.string "Take this.$"

Route114_LanettesHouse_Text_OrganizeYourBoxes:
	.string "Some advice about my Storage System?\p"
	.string "Organize your BOXES.\p"
	.string "I know you don't. Nobody does. It hurts\n"
	.string "me.$"

Route114_LanettesHouse_Text_ResearchNotesPage1:
	.string "LANETTE's research notes. About BOXES.\p"
	.string "Each BOX holds 30 POKéMON.\p"
	.string "Each TRAINER can store 420 POKéMON.\p"
	.string "Nobody will fill this. (Everyone will fill\n"
	.string "this.)\p"
	.string "Keep reading?$"

Route114_LanettesHouse_Text_ResearchNotesPage2:
	.string "Add a marking system to organize\n"
	.string "POKéMON.\p"
	.string "BOX names and wallpapers should be\n"
	.string "changeable, to please the POKéMON.\p"
	.string "They don't care. I care.\p"
	.string "Keep reading?$"

Route114_LanettesHouse_Text_ResearchNotesPage3:
	.string "New POKéMON go to the BOX you looked at\n"
	.string "last.\p"
	.string "If that BOX is full, they go to the next\n"
	.string "one.\p"
	.string "Simple. Elegant. Nobody will thank me.$"

Route114_LanettesHouse_Text_ClosedTheNotebook:
	.string "{PLAYER} closed the notebook.$"

Route114_LanettesHouse_Text_EmailFromBill:
	.string "An e-mail on the PC.\p"
	.string "“… … … … … …\p"
	.string "”Your Storage System is better than\n"
	.string "mine.\p"
	.string "“Fun, useful, user-friendly.\p"
	.string "”Proud I helped. Keep researching!\p"
	.string "“From BILL. PS: I turned into a POKéMON\n"
	.string "again. Long story.”$"

