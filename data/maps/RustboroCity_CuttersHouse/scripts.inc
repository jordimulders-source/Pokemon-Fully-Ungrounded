RustboroCity_CuttersHouse_MapScripts::
	.byte 0

RustboroCity_CuttersHouse_EventScript_Cutter::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_CUT, RustboroCity_CuttersHouse_EventScript_ExplainCut
	msgbox RustboroCity_CuttersHouse_Text_YouCanPutThisHMToGoodUse, MSGBOX_DEFAULT
	giveitem ITEM_HM_CUT
	setflag FLAG_RECEIVED_HM_CUT
	msgbox RustboroCity_CuttersHouse_Text_ExplainCut, MSGBOX_DEFAULT
	release
	end

RustboroCity_CuttersHouse_EventScript_ExplainCut::
	msgbox RustboroCity_CuttersHouse_Text_ExplainCut, MSGBOX_DEFAULT
	release
	end

RustboroCity_CuttersHouse_EventScript_Lass::
	msgbox RustboroCity_CuttersHouse_Text_DadHelpedClearLandOfTrees, MSGBOX_NPC
	end

RustboroCity_CuttersHouse_Text_YouCanPutThisHMToGoodUse:
	.string "That determined look… That limber\n"
	.string "stride… Those trained POKéMON…\p"
	.string "You're obviously skilled!\p"
	.string "Don't say a word. I can tell.\p"
	.string "You'll put this HIDDEN MACHINE to good\n"
	.string "use.\p"
	.string "Don't be shy. Take it! Cut some trees!\n"
	.string "I'm out of trees.$"

RustboroCity_CuttersHouse_Text_ExplainCut:
	.string "CUT. It cuts. Small trees, mostly. You\n"
	.string "need the STONE BADGE.\p"
	.string "You can use it outside of battle, as\n"
	.string "often as you like. That's what HM means.$"

RustboroCity_CuttersHouse_Text_DadHelpedClearLandOfTrees:
	.string "When they expanded RUSTBORO, my dad\n"
	.string "helped.\p"
	.string "His POKéMON CUT down all the trees.\p"
	.string "Now he's in a climate protest group. Full\n"
	.string "circle.$"

