@ Fully Ungrounded: het spelershuis van Littleroot (verhuisdozen, klok zetten, Petalburg-gymnieuws, Lati-noodbericht,
@ Dad, de S.S. Ticket) is weg. Over zijn de algemene stukken die een nieuw spelershuis kan gebruiken:
@ - PlayersHouse_1F_EventScript_Mom: Mom (standaardtekst, PokéNav-registratie, healen); een object in het nieuwe huis
@   met dit script werkt meteen.
@ - de wandklok (ook in het debugmenu) en de handleiding van de Running Shoes (metatile-gedrag).
@ De teksten komen uit het oude LittlerootTown_BrendansHouse_1F (labels ongewijzigd: Dialoogstudio-sleutels).

PlayersHouse_1F_EventScript_Mom::
	lock
	faceplayer
	goto_if_set FLAG_HAS_MATCH_CALL, PlayersHouse_1F_EventScript_TryRegisterMom
	goto_if_set FLAG_SYS_POKEMON_GET, PlayersHouse_1F_EventScript_MomHealsParty
	msgbox PlayersHouse_1F_Text_IsntItNiceInHere, MSGBOX_DEFAULT
	release
	end

PlayersHouse_1F_EventScript_TryRegisterMom::
	goto_if_set FLAG_ENABLE_MOM_MATCH_CALL, PlayersHouse_1F_EventScript_MomHealsParty
	msgbox PlayersHouse_1F_Text_IsThatAPokenav, MSGBOX_DEFAULT
	closemessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox PlayersHouse_1F_Text_RegisteredMom, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_MOM_MATCH_CALL
	release
	end

PlayersHouse_1F_EventScript_MomHealsParty::
	msgbox PlayersHouse_1F_Text_YouShouldRestABit, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	incrementgamestat GAME_STAT_RESTED_AT_HOME
	msgbox PlayersHouse_1F_Text_TakeCareHoney, MSGBOX_DEFAULT
	release
	end

PlayersHouse_2F_EventScript_CheckWallClock::
	incrementgamestat GAME_STAT_CHECKED_CLOCK
	fadescreen FADE_TO_BLACK
	special Special_ViewWallClock
	releaseall
	end

PlayersHouse_2F_EventScript_SetWallClock::
	fadescreen FADE_TO_BLACK
	special StartWallClock
	return

EventScript_RunningShoesManual::
	msgbox PlayersHouse_1F_Text_RunningShoesManual, MSGBOX_SIGN
	end

PlayersHouse_1F_Text_IsntItNiceInHere:
	.string "MOM: The A-Team will be on soon!\n"
	.string "YOU FOOL!$"

PlayersHouse_1F_Text_YouShouldRestABit:
	.string "MOM: How are you doing, {PLAYER}?\n"
	.string "You look a little tired.\p"
	.string "I think you should rest a bit.$"

PlayersHouse_1F_Text_TakeCareHoney:
	.string "MOM: Take care, honey!$"

PlayersHouse_1F_Text_IsThatAPokenav:
	.string "MOM: What is that, honey? A POKéNAV?\n"
	.string "Someone from DEVON gave it to you?\p"
	.string "Well, honey, how about registering\n"
	.string "your mom?\p"
	.string "… … …$"

PlayersHouse_1F_Text_RegisteredMom:
	.string "Registered MOM\n"
	.string "in the POKéNAV.$"

PlayersHouse_1F_Text_RunningShoesManual:
	.string "If you do the KONAMI CODE,\n"
	.string "you can do a moonwalk.$"


@ PC op de slaapkamer (met inrichten); was het PC-script van Brendans huis. Tegels van de Brendan-PC (Stock_TwoStory_2F).
PlayersHouse_2F_EventScript_PC::
	lockall
	setvar VAR_0x8004, PC_LOCATION_BRENDANS_HOUSE
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox gText_PlayerHouseBootPC, MSGBOX_DEFAULT
	special BedroomPC
	releaseall
	end

PlayersHouse_2F_EventScript_TurnOffPlayerPC::
	setvar VAR_0x8004, PC_LOCATION_BRENDANS_HOUSE
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

PlayersHouse_2F_EventScript_WallClock::
	lockall
	goto PlayersHouse_2F_EventScript_CheckWallClock
