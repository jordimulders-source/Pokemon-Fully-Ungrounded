SootopolisCity_House3_MapScripts::
	.byte 0

SootopolisCity_House3_EventScript_Woman::
	lock
	faceplayer
	msgbox SootopolisCity_House3_Text_JuanHasManyFansDoYou, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SootopolisCity_House3_EventScript_HaveFans
	msgbox SootopolisCity_House3_Text_LonesomeTryWorkingHarder, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_HaveFans::
	msgbox SootopolisCity_House3_Text_YouMustBePrettyStrong, MSGBOX_DEFAULT
	release
	end

SootopolisCity_House3_EventScript_Girl::
	msgbox SootopolisCity_House3_Text_TrainerFanClubWasWild, MSGBOX_NPC
	end

SootopolisCity_House3_Text_JuanHasManyFansDoYou:
	.string "You're a TRAINER?\p"
	.string "Our GYM LEADER WALLACE has so many\n"
	.string "fans.\p"
	.string "Mostly wine clubs. Do you have fans?$"

SootopolisCity_House3_Text_YouMustBePrettyStrong:
	.string "Oh, then you must be pretty strong.$"

SootopolisCity_House3_Text_LonesomeTryWorkingHarder:
	.string "Oh, dear… That's lonely.\p"
	.string "Try harder. Or open a winery.$"

SootopolisCity_House3_Text_TrainerFanClubWasWild:
	.string "Fans come from outside HOENN to see\n"
	.string "TRAINERS.\p"
	.string "The TRAINER FAN CLUB in LILYCOVE was\n"
	.string "wild.\p"
	.string "Someone threw their underwear at a\n"
	.string "poster.$"

