@ Project Grounded: Shaymin in het Gracidea-veld (post-game, lv 70). Na het vangen krijg je een Gracidea (Sky Forme).
FlowerParadise_Meadow_MapScripts::
	.byte 0

FlowerParadise_Meadow_EventScript_Shaymin::
	lock
	faceplayer
	playmoncry SPECIES_SHAYMIN, CRY_MODE_ENCOUNTER
	msgbox FlowerParadise_Meadow_Text_Shaymin, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_SHAYMIN, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, FlowerParadise_Meadow_EventScript_ShayminCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FlowerParadise_Meadow_EventScript_ShayminStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FlowerParadise_Meadow_EventScript_ShayminStays
	@ verslagen: Shaymin verstopt zich in de bloemen en is er weer als je terugkomt
	removeobject LOCALID_FLOWER_PARADISE_SHAYMIN
	msgbox FlowerParadise_Meadow_Text_ShayminHides, MSGBOX_DEFAULT
	release
	end

FlowerParadise_Meadow_EventScript_ShayminStays::
	release
	end

FlowerParadise_Meadow_EventScript_ShayminCaught::
	removeobject LOCALID_FLOWER_PARADISE_SHAYMIN
	setflag FLAG_HIDE_FLOWER_PARADISE_SHAYMIN
	goto_if_set FLAG_RECEIVED_GRACIDEA, FlowerParadise_Meadow_EventScript_ShayminStays
	msgbox FlowerParadise_Meadow_Text_FlowerLeft, MSGBOX_DEFAULT
	giveitem ITEM_GRACIDEA
	setflag FLAG_RECEIVED_GRACIDEA
	msgbox FlowerParadise_Meadow_Text_GracideaHint, MSGBOX_DEFAULT
	release
	end

FlowerParadise_Meadow_Text_Shaymin:
	.string "Shay!\p"
	.string "(A hedgehog that is also a salad. The\n"
	.string "Gratitude POKéMON. It is not grateful\l"
	.string "you're here.)$"

FlowerParadise_Meadow_Text_ShayminHides:
	.string "SHAYMIN dove into the flowers and\n"
	.string "vanished like a passive-aggressive\l"
	.string "houseplant.\p"
	.string "It'll be back. It always comes back.$"

FlowerParadise_Meadow_Text_FlowerLeft:
	.string "Where SHAYMIN sat, one GRACIDEA is\n"
	.string "blooming. It smells like gratitude\l"
	.string "and mild hay fever.$"

FlowerParadise_Meadow_Text_GracideaHint:
	.string "Use it on SHAYMIN during the day and\n"
	.string "it turns into its SKY FORME.\p"
	.string "At night it gets cold and turns back.\n"
	.string "Relatable.$"
