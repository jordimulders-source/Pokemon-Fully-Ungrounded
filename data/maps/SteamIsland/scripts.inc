@ Project Grounded: het stoomeiland ten noorden van Route 131 (ZEE_PLAN.md). Kaart: tools/grounded/maptools/sea_market_steam.py.
@ Hete bron: wie erin stapt (coord-trigger op de eerste brontegel) wordt meteen gehealed, zonder ja/nee-vraag.
@ De grotopening in de vulkaan (naar Volcanion) gaat pas open na de Hall of Fame. Teksten zijn placeholders.
SteamIsland_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SteamIsland_OnLoad
	.byte 0

SteamIsland_OnLoad:
	goto_if_unset FLAG_SYS_GAME_CLEAR, SteamIsland_EventScript_CaveSealed
	setmetatile 20, 15, METATILE_Lavaridge_CaveEntrance_Top, TRUE
	setmetatile 20, 16, METATILE_Lavaridge_CaveEntrance_Bottom, FALSE
SteamIsland_EventScript_CaveSealed:
	end

SteamIsland_EventScript_Soak::
	lockall
	special HealPlayerParty
	playse SE_USE_ITEM
	msgbox SteamIsland_Text_Soak, MSGBOX_DEFAULT
	releaseall
	end

SteamIsland_EventScript_Bather::
	msgbox SteamIsland_Text_Bather, MSGBOX_NPC
	end

SteamIsland_EventScript_Bather2::
	msgbox SteamIsland_Text_Bather2, MSGBOX_NPC
	end

SteamIsland_EventScript_Volcanologist::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, SteamIsland_EventScript_VolcanologistOpen
	msgbox SteamIsland_Text_VolcanologistSealed, MSGBOX_DEFAULT
	release
	end

SteamIsland_EventScript_VolcanologistOpen::
	msgbox SteamIsland_Text_VolcanologistOpen, MSGBOX_DEFAULT
	release
	end

SteamIsland_EventScript_Tourist::
	msgbox SteamIsland_Text_Tourist, MSGBOX_NPC
	end

SteamIsland_EventScript_Swimmer::
	msgbox SteamIsland_Text_Swimmer, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
SteamIsland_Text_Soak:
	.string "OLD LADY: Ahh. The spring heals\n"
	.string "everything. Burns. Poison.\l"
	.string "My second marriage.\p"
	.string "Your POKéMON were fully healed!\n"
	.string "You are lightly poached.$"

SteamIsland_Text_Bather:
	.string "Don't splash, dear. I've been in here\n"
	.string "since the last eruption.\p"
	.string "I'm not getting out until\n"
	.string "the next one.$"

SteamIsland_Text_Bather2:
	.string "They say the steam comes from a\n"
	.string "POKéMON inside the volcano.\p"
	.string "I say it comes from me.\n"
	.string "I'm very stressed.$"

SteamIsland_Text_VolcanologistSealed:
	.string "There's a sealed cave in this volcano.\n"
	.string "The steam pressure keeps it shut.\p"
	.string "My calculations say it opens once you\n"
	.string "become CHAMPION.\p"
	.string "Don't ask me how the geology knows.\n"
	.string "I stopped asking years ago.$"

SteamIsland_Text_VolcanologistOpen:
	.string "The cave is open! Something in there\n"
	.string "is venting like a kettle with anger\l"
	.string "issues.\p"
	.string "I'd go in myself, but I'm attached\n"
	.string "to my eyebrows.$"

SteamIsland_Text_Tourist:
	.string "STEAM ISLAND! Free sauna, free\n"
	.string "facial, free second-degree burns.\p"
	.string "Five stars. Would melt again.$"

SteamIsland_Text_Swimmer:
	.string "The sea around this island is soup\n"
	.string "temperature.\p"
	.string "I'm not swimming. I'm being slowly\n"
	.string "cooked. It's very relaxing.$"
