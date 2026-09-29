LilycoveCity_CoveLilyMotel_2F_MapScripts::
	.byte 0

LilycoveCity_CoveLilyMotel_2F_EventScript_GameDesigner::
	lock
	faceplayer
	call_if_unset FLAG_TEMP_2, LilycoveCity_CoveLilyMotel_2F_EventScript_ShowMeCompletedDex
	call_if_set FLAG_TEMP_2, LilycoveCity_CoveLilyMotel_2F_EventScript_ShowDiploma
	specialvar VAR_RESULT, HasAllHoennMons
	goto_if_eq VAR_RESULT, TRUE, LilycoveCity_CoveLilyMotel_2F_EventScript_AllHoennMonsFanfare
	release
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_ShowMeCompletedDex::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_ShowMeCompletedDex, MSGBOX_DEFAULT
	return

LilycoveCity_CoveLilyMotel_2F_EventScript_AllHoennMonsFanfare::
	setflag FLAG_TEMP_2
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	goto LilycoveCity_CoveLilyMotel_2F_EventScript_ShowDiploma
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_ShowDiploma::
	message LilycoveCity_CoveLilyMotel_2F_Text_FilledPokedexGiveYouThis
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	special Special_ShowDiploma
	waitstate
	release
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_Programmer::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_ImTheProgrammer, MSGBOX_NPC
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_GraphicArtist::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_ImTheGraphicArtist, MSGBOX_NPC
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_FatMan::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_GirlsAreCute, MSGBOX_NPC
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_Woman::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_SeaBreezeTicklesHeart, MSGBOX_NPC
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_GameBoyKid::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_NeverLeaveWithoutGameBoy, MSGBOX_NPC
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_Scott::
	lock
	faceplayer
	goto_if_set FLAG_MET_SCOTT_IN_LILYCOVE, LilycoveCity_CoveLilyMotel_2F_EventScript_MetScott
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_SnoozingPreferBattles, MSGBOX_DEFAULT
	addvar VAR_SCOTT_STATE, 1
	setflag FLAG_MET_SCOTT_IN_LILYCOVE
	release
	end

LilycoveCity_CoveLilyMotel_2F_EventScript_MetScott::
	msgbox LilycoveCity_CoveLilyMotel_2F_Text_ContestsDoTakeStrategy, MSGBOX_DEFAULT
	release
	end

LilycoveCity_CoveLilyMotel_2F_Text_ShowMeCompletedDex:
	.string "I'm the GAME DESIGNER.\p"
	.string "Oh, is that right?\n"
	.string "You're working on a POKéDEX?\p"
	.string "It's tough trying to complete it,\n"
	.string "but don't give up.\p"
	.string "If you do complete it, please come\n"
	.string "show me.$"

LilycoveCity_CoveLilyMotel_2F_Text_FilledPokedexGiveYouThis:
	.string "Wow! That's awesome!\n"
	.string "Yep, it's totally awesome!\p"
	.string "This POKéDEX is completely filled!\n"
	.string "You really must love POKéMON!\p"
	.string "I'm so impressed!\p"
	.string "Let me give you something in\n"
	.string "recognition of your feat!$"

LilycoveCity_CoveLilyMotel_2F_Text_ImTheProgrammer:
	.string "Me? I'm the PROGRAMMER.\p"
	.string "I made this game. Well, a version of it.\p"
	.string "Someone changed everything. I'm not\n"
	.string "angry. Just disappointed.$"

LilycoveCity_CoveLilyMotel_2F_Text_ImTheGraphicArtist:
	.string "I'm the GRAPHIC ARTIST!\p"
	.string "Aren't HOENN's POKéMON interesting?\p"
	.string "Who put all these other POKéMON in\n"
	.string "here?!$"

LilycoveCity_CoveLilyMotel_2F_Text_GirlsAreCute:
	.string "The TUBERS, the TWINS… A 2-on-2\n"
	.string "battle…\p"
	.string "Whoop, so fun!\p"
	.string "…Why is everyone looking at me like\n"
	.string "that?$"

LilycoveCity_CoveLilyMotel_2F_Text_SeaBreezeTicklesHeart:
	.string "The sea breeze tickles my heart.\p"
	.string "The mold in this room tickles my lungs.$"

LilycoveCity_CoveLilyMotel_2F_Text_NeverLeaveWithoutGameBoy:
	.string "You never know when someone challenges\n"
	.string "you.\p"
	.string "So I always carry my GAME BOY ADVANCE.\p"
	.string "And a charger. Nobody has the charger.$"

LilycoveCity_CoveLilyMotel_2F_Text_SnoozingPreferBattles:
	.string "SCOTT: … … … … … … … … … … Zzz…\p"
	.string "Huh?! Don't look at me. I'm not here.\p"
	.string "This is my room. Your room is next door.\n"
	.string "The walls are very thin.\p"
	.string "I'm not into CONTESTS, but I'll watch\n"
	.string "anything.$"

LilycoveCity_CoveLilyMotel_2F_Text_ContestsDoTakeStrategy:
	.string "SCOTT: Goodnight, {PLAYER}{KUN}. I'll be right\n"
	.string "here.$"

