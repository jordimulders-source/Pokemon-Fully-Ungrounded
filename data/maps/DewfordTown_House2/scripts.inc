DewfordTown_House2_MapScripts::
	.byte 0

DewfordTown_House2_EventScript_Man::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_SILK_SCARF, DewfordTown_House2_EventScript_ExplainSilkScarf
	msgbox DewfordTown_House2_Text_WantYouToHaveSilkScarf, MSGBOX_DEFAULT
	giveitem ITEM_SILK_SCARF
	goto_if_eq VAR_RESULT, FALSE, DewfordTown_House2_EventScript_NoRoomForScarf
	setflag FLAG_RECEIVED_SILK_SCARF
	release
	end

DewfordTown_House2_EventScript_NoRoomForScarf::
	msgbox DewfordTown_House2_Text_NoRoom, MSGBOX_DEFAULT
	release
	end

DewfordTown_House2_EventScript_ExplainSilkScarf::
	msgbox DewfordTown_House2_Text_ExplainSilkScarf, MSGBOX_DEFAULT
	release
	end

DewfordTown_House2_EventScript_Boy::
	msgbox DewfordTown_House2_Text_BrawlySoCool, MSGBOX_NPC
	end

DewfordTown_House2_Text_WantYouToHaveSilkScarf:
	.string "Gorge your eyes on this! It's a SILK\n"
	.string "SCARF!\p"
	.string "Every Friday I perform as MADAME SILK.\n"
	.string "Just me, this scarf and a very tasteful\l"
	.string "amount of shoulder.\p"
	.string "One night, a married man sat in the\n"
	.string "front row and never looked away. What\l"
	.string "can I say? The scarf does things to\l"
	.string "people.\p"
	.string "Oh, you've got that same twinkle in your\n"
	.string "eyes! Here, take it. I have seventeen\l"
	.string "more.$"

DewfordTown_House2_Text_NoRoom:
	.string "Oh, you don't have room? Make room,\n"
	.string "darling.\p"
	.string "Nobody has ever said no to MADAME SILK.\n"
	.string "Just ask RANDY.$"

DewfordTown_House2_Text_ExplainSilkScarf:
	.string "The SILK SCARF raises the power of\n"
	.string "NORMAL-type moves.\p"
	.string "It goes with almost every POKéMON. And\n"
	.string "almost every husband, apparently.$"

DewfordTown_House2_Text_BrawlySoCool:
	.string "Wow, you crossed the sea to visit\n"
	.string "DEWFORD? Did you hear about RANDY too?\p"
	.string "Back in the day, BRAWLY's GYM was pure:\n"
	.string "the best fought the best, no trash\l"
	.string "talk, no excuses.\p"
	.string "Now it's all rumors, press conferences\n"
	.string "and who slept with whom. DEWFORD used\l"
	.string "to be about fighting!$"

