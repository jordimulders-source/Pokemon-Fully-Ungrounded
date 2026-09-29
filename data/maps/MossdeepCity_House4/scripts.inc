MossdeepCity_House4_MapScripts::
	.byte 0

MossdeepCity_House4_EventScript_Woman::
	lock
	faceplayer
	goto_if_set FLAG_SYS_GAME_CLEAR, MossdeepCity_House4_EventScript_CanBattleAtSecretBases
	msgbox MossdeepCity_House4_Text_BrotherLikesToFindBases, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House4_EventScript_CanBattleAtSecretBases::
	msgbox MossdeepCity_House4_Text_BrotherLikesToVisitBasesAndBattle, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House4_EventScript_NinjaBoy::
	lock
	faceplayer
	special CheckPlayerHasSecretBase
	goto_if_eq VAR_RESULT, FALSE, MossdeepCity_House4_EventScript_NoSecretBase
	special GetSecretBaseNearbyMapName
	msgbox MossdeepCity_House4_Text_YouMadeSecretBaseNearX, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House4_EventScript_NoSecretBase::
	msgbox MossdeepCity_House4_Text_MakeSecretBase, MSGBOX_DEFAULT
	release
	end

MossdeepCity_House4_EventScript_Skitty::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
	msgbox MossdeepCity_House4_Text_Skitty, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MossdeepCity_House4_Text_BrotherLikesToFindBases:
	.string "My little brother likes finding people's\n"
	.string "SECRET BASES.\p"
	.string "Then he moves in.$"

MossdeepCity_House4_Text_BrotherLikesToVisitBasesAndBattle:
	.string "My little brother visits people's SECRET\n"
	.string "BASES and battles them.\p"
	.string "Uninvited. Every time.$"

MossdeepCity_House4_Text_YouMadeSecretBaseNearX:
	.string "Was it you who made a SECRET BASE near\n"
	.string "{STR_VAR_1}?\p"
	.string "I've been there. I ate your snacks.$"

MossdeepCity_House4_Text_MakeSecretBase:
	.string "Make a SECRET BASE somewhere. I'll find\n"
	.string "it!\p"
	.string "And move in.$"

MossdeepCity_House4_Text_Skitty:
	.string "SKITTY: Miyaan?$"

