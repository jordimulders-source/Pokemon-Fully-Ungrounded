@ Project Grounded: Yoshi's Island, het Yoshi-huis (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_YoshiHouse_MapScripts::
	.byte 0

YoshisIsland_YoshiHouse_EventScript_YoshiGreen::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiGreen, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiRed::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiRed, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiYellow::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiYellow, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiLightBlue::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiLightBlue, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiPink::
	lock
	faceplayer
	goto_if_set FLAG_ITEM_YOSHIS_ISLAND_YOSHI_HOUSE_SWEET_HEART, YoshisIsland_YoshiHouse_EventScript_YoshiPinkAfter
	msgbox YoshisIsland_YoshiHouse_Text_YoshiPink, MSGBOX_DEFAULT
	giveitem ITEM_SWEET_HEART, 1
	goto_if_eq VAR_RESULT, FALSE, YoshisIsland_YoshiHouse_EventScript_YoshiPinkEnd
	setflag FLAG_ITEM_YOSHIS_ISLAND_YOSHI_HOUSE_SWEET_HEART
YoshisIsland_YoshiHouse_EventScript_YoshiPinkAfter::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiPinkAfter, MSGBOX_DEFAULT
YoshisIsland_YoshiHouse_EventScript_YoshiPinkEnd::
	release
	end

YoshisIsland_YoshiHouse_EventScript_YoshiPurple::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiPurple, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiBrown::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiBrown, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiBlack::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiBlack, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiWhite::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiWhite, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_YoshiBlue::
	msgbox YoshisIsland_YoshiHouse_Text_YoshiBlue, MSGBOX_NPC
	end

YoshisIsland_YoshiHouse_EventScript_Hearth::
	msgbox YoshisIsland_YoshiHouse_Text_Hearth, MSGBOX_SIGN
	end

YoshisIsland_YoshiHouse_EventScript_Portrait::
	msgbox YoshisIsland_YoshiHouse_Text_Portrait, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_YoshiHouse_Text_YoshiGreen:
	.string "(A green YOSHI. Not THE YOSHI. This one\n"
	.string "is called GREG. People keep asking GREG\l"
	.string "to save the island. GREG is in his\l"
	.string "pajamas.)$"

YoshisIsland_YoshiHouse_Text_YoshiRed:
	.string "(The red YOSHI breathes fire after he\n"
	.string "eats a red shell. There are no red shells\l"
	.string "on this island. He has been waiting\l"
	.string "since 1990. He has a lot of fire saved\l"
	.string "up.)$"

YoshisIsland_YoshiHouse_Text_YoshiYellow:
	.string "(The yellow YOSHI makes the ground\n"
	.string "shake when he lands. He is sitting very,\l"
	.string "very still. For everyone's sake,\l"
	.string "including the furniture's.)$"

YoshisIsland_YoshiHouse_Text_YoshiLightBlue:
	.string "(The light-blue YOSHI can fly with a\n"
	.string "blue shell. He asks if any of your\l"
	.string "POKEMON is a shell. He looks at your\l"
	.string "party for a very long time.)$"

YoshisIsland_YoshiHouse_Text_YoshiPink:
	.string "(The pink YOSHI baked you something.\n"
	.string "It's shaped like a heart. It has been in\l"
	.string "her mouth. It is still a gift. Gifts are\l"
	.string "about the thought.)$"

YoshisIsland_YoshiHouse_Text_YoshiPinkAfter:
	.string "(The pink YOSHI is baking another one.\n"
	.string "For herself, this time. She has earned\l"
	.string "it.)$"

YoshisIsland_YoshiHouse_Text_YoshiPurple:
	.string "(The purple YOSHI says purple is just a\n"
	.string "darker, better pink and that the pink\l"
	.string "one copied him. The pink one is not\l"
	.string "listening. The pink one is baking.)$"

YoshisIsland_YoshiHouse_Text_YoshiBrown:
	.string "(The brown YOSHI would like you to know\n"
	.string "he is not dirty. It's his natural color.\l"
	.string "He says it like he's had to say it a lot.)$"

YoshisIsland_YoshiHouse_Text_YoshiBlack:
	.string "(The black YOSHI is wearing sunglasses\n"
	.string "indoors. He is the edgy one. He is eating\l"
	.string "a cupcake with sprinkles. Edgily.)$"

YoshisIsland_YoshiHouse_Text_YoshiWhite:
	.string "(The white YOSHI is very rare. He tells\n"
	.string "you this immediately. Then once more. He\l"
	.string "has a small framed certificate and\l"
	.string "nowhere to hang it.)$"

YoshisIsland_YoshiHouse_Text_YoshiBlue:
	.string "(A real blue YOSHI. Not a fish in a\n"
	.string "costume, not a lake with eyebrows. He\l"
	.string "wants that on record. Please put it on\l"
	.string "record.)$"

YoshisIsland_YoshiHouse_Text_Hearth:
	.string "(A crackling fireplace. Every YOSHI's\n"
	.string "house has one. Nobody knows who lights\l"
	.string "it. The fire doesn't know either.)$"

YoshisIsland_YoshiHouse_Text_Portrait:
	.string "(A family portrait. It's an egg. All the\n"
	.string "YOSHI family portraits are eggs. It's a\l"
	.string "very efficient family.)$"
