MirageTower_4F_MapScripts::
	.byte 0

MirageTower_4F_EventScript_RootFossil::
	lock
	faceplayer
	msgbox MirageTower_4F_Text_TakeRootFossil, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MirageTower_4F_EventScript_LeaveRootFossil
	giveitem ITEM_ROOT_FOSSIL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	closemessage
	setflag FLAG_HIDE_MIRAGE_TOWER_ROOT_FOSSIL
	removeobject LOCALID_MIRAGE_ROOT_FOSSIL
	delay 30
	setflag FLAG_CHOSE_ROOT_FOSSIL
	release
	end

MirageTower_4F_EventScript_LeaveRootFossil::
	msgbox MirageTower_4F_Text_LeftRootFossilAlone, MSGBOX_DEFAULT
	release
	end

MirageTower_4F_EventScript_ClawFossil::
	lock
	faceplayer
	msgbox MirageTower_4F_Text_TakeClawFossil, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MirageTower_4F_EventScript_LeaveClawFossil
	giveitem ITEM_CLAW_FOSSIL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	closemessage
	setflag FLAG_HIDE_MIRAGE_TOWER_CLAW_FOSSIL
	removeobject LOCALID_MIRAGE_CLAW_FOSSIL
	delay 30
	setflag FLAG_CHOSE_CLAW_FOSSIL
	release
	end

MirageTower_4F_EventScript_LeaveClawFossil::
	msgbox MirageTower_4F_Text_LeaveClawFossilAlone, MSGBOX_DEFAULT
	release
	end

MirageTower_4F_EventScript_CollapseMirageTower::
	release
	end

MirageTower_4F_Text_TakeRootFossil:
	.string "You found the ROOT FOSSIL.\p"
	.string "Take the ROOT FOSSIL?$"

MirageTower_4F_Text_LeftRootFossilAlone:
	.string "{PLAYER} left the ROOT FOSSIL alone.$"

MirageTower_4F_Text_TakeClawFossil:
	.string "You found the CLAW FOSSIL.\p"
	.string "Take the CLAW FOSSIL?$"

MirageTower_4F_Text_LeaveClawFossilAlone:
	.string "{PLAYER} left the CLAW FOSSIL alone.$"
	