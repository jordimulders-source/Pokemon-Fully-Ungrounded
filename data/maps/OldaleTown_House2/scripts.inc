OldaleTown_House2_MapScripts::
	.byte 0

OldaleTown_House2_EventScript_Woman::
	msgbox OldaleTown_House2_Text_PokemonLevelUp, MSGBOX_NPC
	end

OldaleTown_House2_EventScript_Man::
	msgbox OldaleTown_House2_Text_YoullGoFurtherWithStrongPokemon, MSGBOX_NPC
	end

OldaleTown_House2_Text_PokemonLevelUp:
	.string "When POKéMON battle, forces of\n"
	.string "nature collide, casualties\l"
	.string "unavoidably happen.\p"
	.string "But the world is fictional, so you\n"
	.string "don't care, I don't care…\p"
	.string "All I wanna say is that they don't\n"
	.string "really care about us, HEEHEE!$"

OldaleTown_House2_Text_YoullGoFurtherWithStrongPokemon:
	.string "If the POKéMON with you become\n"
	.string "stronger, you'll notice that this\l"
	.string "ROMhack actually has really cool\l"
	.string "balancing.\p"
	.string "Suddenly not 60% of the POKéDEX\n"
	.string "is useless anymore.\p"
	.string "This developer is a genius!$"
