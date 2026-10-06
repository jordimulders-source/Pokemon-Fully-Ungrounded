@ Project Grounded: Fullmoon Island, een halvemaanvormig eilandje in de West-zee, ten oosten van Route 105.
@ Kaart: tools/grounded/maptools/tapu_cresselia.py. Cresselia (lv 60) staat alleen 's nachts aan het maanmeertje,
@ en pas na de Hall of Fame. Verslagen (niet gevangen) = terug na de volgende League (hall_of_fame.inc).
@ Objectvlag FLAG_TEMP_12 (ON_TRANSITION). Lore: de tegenhanger van Darkrai (Mt. Pyre). Teksten zijn placeholders.
FullmoonIsland_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FullmoonIsland_OnTransition
	.byte 0

FullmoonIsland_OnTransition:
	goto_if_unset FLAG_SYS_GAME_CLEAR, FullmoonIsland_EventScript_HideCresselia
	goto_if_set FLAG_DEFEATED_CRESSELIA, FullmoonIsland_EventScript_HideCresselia
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, FALSE, FullmoonIsland_EventScript_HideCresselia
	end

FullmoonIsland_EventScript_HideCresselia:
	setflag FLAG_TEMP_12
	end

FullmoonIsland_EventScript_Cresselia::
	lock
	faceplayer
	msgbox FullmoonIsland_Text_Cresselia, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_CRESSELIA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_CRESSELIA, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FullmoonIsland_EventScript_CresseliaCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FullmoonIsland_EventScript_CresseliaDefeated
	msgbox FullmoonIsland_Text_CresseliaStays, MSGBOX_DEFAULT
	release
	end

FullmoonIsland_EventScript_CresseliaCaught::
	setflag FLAG_CAUGHT_CRESSELIA
FullmoonIsland_EventScript_CresseliaDefeated::
	setflag FLAG_DEFEATED_CRESSELIA
	setflag FLAG_TEMP_12
	removeobject LOCALID_FULLMOON_CRESSELIA
	msgbox FullmoonIsland_Text_Feather, MSGBOX_DEFAULT
	giveitem ITEM_PRETTY_FEATHER
	msgbox FullmoonIsland_Text_FeatherAfter, MSGBOX_DEFAULT
	release
	end

FullmoonIsland_EventScript_MoonPool::
	goto_if_unset FLAG_SYS_GAME_CLEAR, FullmoonIsland_EventScript_MoonPoolDay
	goto_if_set FLAG_DEFEATED_CRESSELIA, FullmoonIsland_EventScript_MoonPoolEmpty
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, FullmoonIsland_EventScript_MoonPoolNight
FullmoonIsland_EventScript_MoonPoolDay:
	msgbox FullmoonIsland_Text_MoonPoolDay, MSGBOX_SIGN
	end

FullmoonIsland_EventScript_MoonPoolNight:
	msgbox FullmoonIsland_Text_MoonPoolNight, MSGBOX_SIGN
	end

FullmoonIsland_EventScript_MoonPoolEmpty:
	msgbox FullmoonIsland_Text_MoonPoolEmpty, MSGBOX_SIGN
	end

FullmoonIsland_EventScript_Sailor::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_CRESSELIA, FullmoonIsland_EventScript_SailorAfter
	msgbox FullmoonIsland_Text_Sailor, MSGBOX_DEFAULT
	release
	end

FullmoonIsland_EventScript_SailorAfter::
	msgbox FullmoonIsland_Text_SailorAfter, MSGBOX_DEFAULT
	release
	end

FullmoonIsland_Text_Cresselia:
	.string "A swan made of moonlight is gliding\n"
	.string "over the little lake.\p"
	.string "CRESSELIA. The good dream, as\n"
	.string "opposed to the one on MT. PYRE.\p"
	.string "It looks at you like you've been\n"
	.string "sleeping badly. You have.$"

FullmoonIsland_Text_CresseliaStays:
	.string "CRESSELIA is still circling the\n"
	.string "lake. It's in no hurry. Nights are\l"
	.string "long when you're a crescent.$"

FullmoonIsland_Text_Feather:
	.string "Something glimmers on the shore.\n"
	.string "A crescent-shaped feather!\p"
	.string "It's the legendary LUNAR FEATHER!\p"
	.string "…No, wait. It's a normal feather.\n"
	.string "The moon was out of stock.$"

FullmoonIsland_Text_FeatherAfter:
	.string "Still, {PLAYER} feels strangely\n"
	.string "well-rested.$"

FullmoonIsland_Text_MoonPoolDay:
	.string "A small, round lake. It reflects the\n"
	.string "sky, as lakes do.\p"
	.string "At night, people say, it reflects\n"
	.string "something else.$"

FullmoonIsland_Text_MoonPoolNight:
	.string "The moon floats in the lake. There\n"
	.string "is a second, smaller moon next to it.\l"
	.string "That one is looking back.$"

FullmoonIsland_Text_MoonPoolEmpty:
	.string "Just the moon. One of them.\n"
	.string "The normal amount.$"

FullmoonIsland_Text_Sailor:
	.string "Can't sleep. Haven't slept in weeks.\p"
	.string "Ever since some kid went poking\n"
	.string "around the top of MT. PYRE at night,\l"
	.string "I dream of graves. My own, mostly.\l"
	.string "Spelled wrong.\p"
	.string "Except here. On this island I sleep\n"
	.string "like a baby. Something sings the bad\l"
	.string "dreams away. At night. By the lake.\p"
	.string "I'd go look, but I'm asleep then.$"

FullmoonIsland_Text_SailorAfter:
	.string "Slept nine hours last night. Dreamt\n"
	.string "about a swan. Woke up with a feather\l"
	.string "in my ear. Best night of my life.$"
