CaveOfOrigin_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, CaveOfOrigin_B1F_OnLoad
	.byte 0

CaveOfOrigin_B1F_EventScript_Wallace::
	lock
	faceplayer
	msgbox CaveOfOrigin_B1F_Text_WallaceStory, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 60
	playse SE_PIN
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_Delay48
	waitmovement 0
	delay 30
	applymovement LOCALID_CAVE_OF_ORIGIN_WALLACE, Common_Movement_FacePlayer
	waitmovement 0
	message CaveOfOrigin_B1F_Text_WhereIsRayquaza
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_WheresRayquaza::
	multichoice 0, 0, MULTI_WHERES_RAYQUAZA, FALSE
	switch VAR_RESULT
	case 0, CaveOfOrigin_B1F_EventScript_AtCaveOfOrigin
	case 1, CaveOfOrigin_B1F_EventScript_AtMtPyre
	case 2, CaveOfOrigin_B1F_EventScript_AtSkyPillar
	case 3, CaveOfOrigin_B1F_EventScript_DontRemember
	goto CaveOfOrigin_B1F_EventScript_DontRemember
	end

CaveOfOrigin_B1F_EventScript_AtCaveOfOrigin::
	message CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_AtMtPyre::
	message CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_DontRemember::
	message CaveOfOrigin_B1F_Text_CantYouRememberSomehow
	waitmessage
	goto CaveOfOrigin_B1F_EventScript_WheresRayquaza

CaveOfOrigin_B1F_EventScript_AtSkyPillar::
	msgbox CaveOfOrigin_B1F_Text_WellHeadToSkyPillar, MSGBOX_DEFAULT
	closemessage
	playse SE_EXIT
	fadescreenspeed FADE_TO_BLACK, 4
	setflag FLAG_WALLACE_GOES_TO_SKY_PILLAR
	setvar VAR_SOOTOPOLIS_CITY_STATE, 3
	removeobject LOCALID_CAVE_OF_ORIGIN_WALLACE
	clearflag FLAG_HIDE_SKY_PILLAR_WALLACE
	fadescreen FADE_FROM_BLACK
	release
	end

CaveOfOrigin_B1F_Text_WallaceStory:
	.string "Ah, so you are {PLAYER}{KUN}? I've heard\n"
	.string "tales of your exploits.\p"
	.string "My name is WALLACE.\p"
	.string "I was once the GYM LEADER of\n"
	.string "SOOTOPOLIS, but something came up. So I\l"
	.string "became a sommelier and alcohol lover.\p"
	.string "Then, JUAN took over my gym. But people\n"
	.string "wanted me back, since JUAN has no\l"
	.string "personality. So now I am back, with a\l"
	.string "gym full of alcoholics! What a story\l"
	.string "right?\p"
	.string "… … … … … … … … … … … …\p"
	.string "Oh wait, you are here about GROUDON and\n"
	.string "KYOGRE, the two POKéMON wreaking havoc\l"
	.string "here, they are considered to be\l"
	.string "super-ancient POKéMON.\p"
	.string "But there aren't just two super-\n"
	.string "ancient POKéMON. There are a huge\l"
	.string "number. But most of them aren't in\l"
	.string "Hoenn. Wait you do not care? Hmm. Well.\p"
	.string "There is one more somewhere.\p"
	.string "Somewhere, there is a super- ancient\n"
	.string "POKéMON named GEODUDE.\p"
	.string "It's said that it was this GEODUDE that\n"
	.string "becalmed the two combatants in the\l"
	.string "distant past. He flexed his rocky bicep\l"
	.string "and they...\p"
	.string "Wait, you do not believe me? What if I\n"
	.string "said it was my LUVDISC?\p"
	.string "Uh, okay. Boring... It is a RAYQUAZA. That\n"
	.string "green serpent. To be honest I prefer my\l"
	.string "LUVDISC.$"

CaveOfOrigin_B1F_Text_WhereIsRayquaza:
	.string "WALLACE: {PLAYER}{KUN}, do you perhaps know\n"
	.string "where RAYQUAZA is now?\p"
	.string "If you do, please don't tell me. I really\n"
	.string "do not care.$"

CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin:
	.string "WALLACE: The CAVE OF ORIGIN?\p"
	.string "But that's right here! I need you to do\n"
	.string "better than that! There is nothing in\l"
	.string "here, except for my wine cellar.$"

CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat:
	.string "WALLACE: MT. PYRE?\p"
	.string "There are a lot of ghosts and serpent\n"
	.string "like beings over there. But no GEODUDE,\l"
	.string "nor LUVDISC, nor a green serpent.$"

CaveOfOrigin_B1F_Text_CantYouRememberSomehow:
	.string "WALLACE: Huh? You don't remember? Hmm…\n"
	.string "That's a problem…\p"
	.string "Did you drink too much?$"

CaveOfOrigin_B1F_Text_WellHeadToSkyPillar:
	.string "WALLACE: The SKY PILLAR?\p"
	.string "I do not know this building! It's very\n"
	.string "strange, just a random pillar in the\l"
	.string "middle of the ocean. You know what, you\l"
	.string "check it out, while I will have a little\l"
	.string "drink with my gals!\p"
	.string "{PLAYER}{KUN}, there's not a moment to lose!\n"
	.string "You'll head to the SKY PILLAR right\l"
	.string "away! Only you!$"

@ --- dungeon_extra (gegenereerd door tools/grounded/maptools/dungeon_extra.py) ---
@ Na de Hall of Fame: ladder (13,4) omlaag naar de oude R/S-kamers (Cave of Origin dieper).
CaveOfOrigin_B1F_OnLoad:
	goto_if_unset FLAG_SYS_GAME_CLEAR, CaveOfOrigin_B1F_EventScript_NoDeepLadder
	setmetatile 13, 4, 0x33D, FALSE
CaveOfOrigin_B1F_EventScript_NoDeepLadder:
	end
@ --- einde dungeon_extra ---
