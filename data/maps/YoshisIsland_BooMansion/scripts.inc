@ Project Grounded: Yoshi's Island, Boo's spookhuis (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_BooMansion_MapScripts::
	.byte 0

YoshisIsland_BooMansion_EventScript_Boo::
	lock
	faceplayer
	goto YoshisIsland_BooMansion_EventScript_BooBattle

YoshisIsland_BooMansion_EventScript_BooWon::
	msgbox YoshisIsland_BooMansion_Text_BooWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_BOO
	setflag FLAG_YI_BOO_DONE
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox YoshisIsland_BooMansion_Text_BooGone, MSGBOX_DEFAULT
	release
	end

YoshisIsland_BooMansion_EventScript_Yoshi::
	msgbox YoshisIsland_BooMansion_Text_Yoshi, MSGBOX_NPC
	end

YoshisIsland_BooMansion_EventScript_BooBattle::
	msgbox YoshisIsland_BooMansion_Text_BooIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_BooMansion_EventScript_BooChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_BooMansion_EventScript_BooFight
	special LoadPlayerParty
	goto YoshisIsland_BooMansion_EventScript_BooChoose

YoshisIsland_BooMansion_EventScript_BooFight::
	multi_2_vs_1 TRAINER_YI_COMMANDER_BOO, YoshisIsland_BooMansion_Text_BooDefeatA, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_BooMansion_EventScript_BooWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_BooMansion_EventScript_Portrait::
	msgbox YoshisIsland_BooMansion_Text_Portrait, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_BooMansion_Text_BooWon:
	.string "COMMANDER BOO: Fine! FINE! Take the\n"
	.string "stupid fort! It was never mine anyway. I\l"
	.string "just do the spooking. The big guy does\l"
	.string "the paperwork.\p"
	.string "COMMANDER BOO: ...don't look at me while\n"
	.string "I'm crying.$"

YoshisIsland_BooMansion_Text_BooGone:
	.string "(COMMANDER BOO turns invisible out of\n"
	.string "embarrassment. Somewhere outside, a\l"
	.string "SHY GUY in a black cloak hears the news\l"
	.string "and quietly cancels his membership.)$"

YoshisIsland_BooMansion_Text_Yoshi:
	.string "YOSHI: Y-yoshi...\p"
	.string "(YOSHI is hiding behind a candle. It is a\n"
	.string "thin candle. It is not working.)$"

YoshisIsland_BooMansion_Text_BooIntro:
	.string "COMMANDER BOO: Hee hee hee! A visitor!\n"
	.string "Nobody visits! Do you know how hard it\l"
	.string "is to make friends when everyone you\l"
	.string "meet screams?\p"
	.string "COMMANDER BOO: The boss pays me in\n"
	.string "mochi to keep the SHY GUYS in line. And\l"
	.string "to keep YOU out. Mostly the mochi part.\p"
	.string "YOSHI: ...yoshi! (Very small, but brave.)$"

YoshisIsland_BooMansion_Text_BooDefeatA:
	.string "COMMANDER BOO: Stop LOOKING at me!$"

YoshisIsland_BooMansion_Text_Portrait:
	.string "(A portrait of a BOO. Its eyes follow\n"
	.string "you around the room. Then it gets\l"
	.string "embarrassed and looks away.)$"
