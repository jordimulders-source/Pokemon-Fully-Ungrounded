MossdeepCity_House1_MapScripts::
	.byte 0

MossdeepCity_House1_EventScript_BlackBelt::
	lock
	faceplayer
	bufferleadmonspeciesname STR_VAR_1
	msgbox MossdeepCity_House1_Text_HmmYourPokemon, MSGBOX_DEFAULT
	specialvar VAR_RESULT, GetPokeblockNameByMonNature
	goto_if_eq VAR_RESULT, 0, MossdeepCity_House1_EventScript_NeutralNature
	msgbox MossdeepCity_House1_Text_ItLikesXPokeblocks, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House1_EventScript_NeutralNature::
	msgbox MossdeepCity_House1_Text_DoesntLikeOrDislikePokeblocks, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House1_EventScript_Woman::
	msgbox MossdeepCity_House1_Text_HusbandCanTellPokeblockMonLikes, MSGBOX_NPC
	end

MossdeepCity_House1_Text_HmmYourPokemon:
	.string "Hmm! Your {STR_VAR_1}…$"

MossdeepCity_House1_Text_ItLikesXPokeblocks:
	.string "It likes {STR_VAR_1}S, doesn't it?\p"
	.string "No, I'm positive! It definitely likes\n"
	.string "{STR_VAR_1}S!\p"
	.string "I can tell from its eyebrows.$"

MossdeepCity_House1_Text_DoesntLikeOrDislikePokeblocks:
	.string "It doesn't like or dislike any {POKEBLOCK}S.\p"
	.string "A POKéMON without opinions. Rare.$"

MossdeepCity_House1_Text_HusbandCanTellPokeblockMonLikes:
	.string "My husband can tell what {POKEBLOCK}S a POKéMON\n"
	.string "likes at a glance.\p"
	.string "He can't tell what I like. After 20\n"
	.string "years.$"

