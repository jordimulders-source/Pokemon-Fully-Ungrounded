@ Project Grounded: het heiligdom van de zeetempel (kopie van SealedChamber_InnerRoom). Manaphy (lv 50) wacht hier
@ al sinds 2006 op een Pokemon Ranger die hem zou ophalen. Na het eerste gevecht (gevangen of verslagen, niet gevlucht)
@ ligt er een ei op het altaar (Phione) met de Silver Wing; die wijst naar Whirl Island (Lugia).
@ Verslagen = Manaphy komt bij een volgend bezoek terug; gevangen = weg.
@ Ei zichtbaar (FLAG_TEMP_1 vrij) = FLAG_SEA_TEMPLE_MANAPHY_BATTLED gezet en FLAG_RECEIVED_SEA_TEMPLE_EGG niet.
SeaTemple_Sanctum_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeaTemple_Sanctum_OnTransition
	.byte 0

SeaTemple_Sanctum_OnTransition:
	setflag FLAG_TEMP_1
	goto_if_unset FLAG_SEA_TEMPLE_MANAPHY_BATTLED, SeaTemple_Sanctum_EventScript_TransitionEnd
	goto_if_set FLAG_RECEIVED_SEA_TEMPLE_EGG, SeaTemple_Sanctum_EventScript_TransitionEnd
	clearflag FLAG_TEMP_1
SeaTemple_Sanctum_EventScript_TransitionEnd::
	end

SeaTemple_Sanctum_EventScript_Manaphy::
	lock
	faceplayer
	playmoncry SPECIES_MANAPHY, CRY_MODE_ENCOUNTER
	msgbox SeaTemple_Sanctum_Text_Manaphy, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_MANAPHY, 73
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SeaTemple_Sanctum_EventScript_ManaphyStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SeaTemple_Sanctum_EventScript_ManaphyStays
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SeaTemple_Sanctum_EventScript_ManaphyCaught
	removeobject LOCALID_SEA_TEMPLE_MANAPHY
	msgbox SeaTemple_Sanctum_Text_ManaphyFainted, MSGBOX_DEFAULT
	goto SeaTemple_Sanctum_EventScript_ShowEgg

SeaTemple_Sanctum_EventScript_ManaphyCaught::
	setflag FLAG_CAUGHT_SEA_TEMPLE_MANAPHY
	removeobject LOCALID_SEA_TEMPLE_MANAPHY
SeaTemple_Sanctum_EventScript_ShowEgg::
	goto_if_set FLAG_SEA_TEMPLE_MANAPHY_BATTLED, SeaTemple_Sanctum_EventScript_ManaphyStays
	setflag FLAG_SEA_TEMPLE_MANAPHY_BATTLED
	clearflag FLAG_TEMP_1
	addobject LOCALID_SEA_TEMPLE_EGG
	msgbox SeaTemple_Sanctum_Text_EggAppears, MSGBOX_DEFAULT
SeaTemple_Sanctum_EventScript_ManaphyStays::
	release
	end

SeaTemple_Sanctum_EventScript_Egg::
	lock
	getpartysize
	goto_if_eq VAR_RESULT, PARTY_SIZE, SeaTemple_Sanctum_EventScript_EggPartyFull
	msgbox SeaTemple_Sanctum_Text_Egg, MSGBOX_DEFAULT
	giveegg SPECIES_PHIONE
	playfanfare MUS_OBTAIN_ITEM
	message SeaTemple_Sanctum_Text_GotEgg
	waitfanfare
	waitmessage
	removeobject LOCALID_SEA_TEMPLE_EGG
	setflag FLAG_RECEIVED_SEA_TEMPLE_EGG
	giveitem ITEM_SILVER_WING
	msgbox SeaTemple_Sanctum_Text_SilverWing, MSGBOX_DEFAULT
	release
	end

SeaTemple_Sanctum_EventScript_EggPartyFull::
	msgbox SeaTemple_Sanctum_Text_EggPartyFull, MSGBOX_DEFAULT
	release
	end

SeaTemple_Sanctum_EventScript_BackWall::
	msgbox SeaTemple_Sanctum_Text_BackWall, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural1::
	msgbox SeaTemple_Sanctum_Text_Mural1, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural2::
	msgbox SeaTemple_Sanctum_Text_Mural2, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural3::
	msgbox SeaTemple_Sanctum_Text_Mural3, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural4::
	msgbox SeaTemple_Sanctum_Text_Mural4, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural5::
	msgbox SeaTemple_Sanctum_Text_Mural5, MSGBOX_SIGN
	end

SeaTemple_Sanctum_EventScript_Mural6::
	msgbox SeaTemple_Sanctum_Text_Mural6, MSGBOX_SIGN
	end

SeaTemple_Sanctum_Text_Manaphy:
	.string "Manaaa…? Phy!\p"
	.string "The PRINCE OF THE SEA looks up at you\n"
	.string "with enormous, hopeful eyes.\p"
	.string "You are not a POKéMON RANGER.\n"
	.string "The eyes become slightly less hopeful.\p"
	.string "Then MANAPHY decides you'll do.$"

SeaTemple_Sanctum_Text_ManaphyFainted:
	.string "MANAPHY dissolves into a cloud of\n"
	.string "bubbles and a faint sense of drama.\p"
	.string "It will be back. Princes always come\n"
	.string "back. Mostly for attention.$"

SeaTemple_Sanctum_Text_EggAppears:
	.string "Something rolls out from behind the\n"
	.string "altar and stops with a soft “tok.”$"

SeaTemple_Sanctum_Text_Egg:
	.string "An EGG, wrapped in a big silver\n"
	.string "feather. A label says: “SPARE.”\p"
	.string "MANAPHY's eggs hatch into PHIONE.\n"
	.string "PHIONE are not princes. PHIONE are\l"
	.string "interns.$"

SeaTemple_Sanctum_Text_GotEgg:
	.string "{PLAYER} received the EGG!$"

SeaTemple_Sanctum_Text_SilverWing:
	.string "The feather is cold and smells of\n"
	.string "storms. It doesn't belong to anything\l"
	.string "that lives in this temple.\p"
	.string "Something big, from somewhere the sea\n"
	.string "spins in circles.$"

SeaTemple_Sanctum_Text_EggPartyFull:
	.string "An EGG, wrapped in a big silver\n"
	.string "feather.\p"
	.string "There's no room for it in your party.\n"
	.string "It waits. Eggs are patient.\l"
	.string "Unlike rangers. And you.$"

SeaTemple_Sanctum_Text_BackWall:
	.string "HERE RESTS THE PRINCE OF THE SEA.\p"
	.string "PLEASE DO NOT TAP ON THE GLASS.\n"
	.string "THERE IS NO GLASS. IT'S A FIGURE OF\l"
	.string "SPEECH. STOP TAPPING.$"

SeaTemple_Sanctum_Text_Mural1:
	.string "The PRINCE OF THE SEA was born in this\n"
	.string "temple. He waits in this temple.\p"
	.string "The mural is mostly about the waiting.$"

SeaTemple_Sanctum_Text_Mural2:
	.string "A RANGER shall come and carry the\n"
	.string "PRINCE to the TEMPLE OF THE SEA.\p"
	.string "(You are standing in the TEMPLE OF\n"
	.string "THE SEA. The plan had flaws.)$"

SeaTemple_Sanctum_Text_Mural3:
	.string "The PRINCE can swap hearts with any\n"
	.string "living thing.\p"
	.string "He has swapped hearts with a SABLEYE,\n"
	.string "a GOLURK and a very confused\l"
	.string "PYUKUMUKU. Nobody talks about it.$"

SeaTemple_Sanctum_Text_Mural4:
	.string "Year three of the waiting: the PRINCE\n"
	.string "learned to count.\p"
	.string "Year seven: the PRINCE stopped\n"
	.string "counting.$"

SeaTemple_Sanctum_Text_Mural5:
	.string "The tide comes in. The tide goes out.\n"
	.string "The RANGER does not come.\p"
	.string "Next to it, smaller: “HAS ANYONE\n"
	.string "CHECKED THE OTHER CARTRIDGE?”$"

SeaTemple_Sanctum_Text_Mural6:
	.string "A silver bird circles over a ring of\n"
	.string "whirlpools, north of the city in the\l"
	.string "crater.\p"
	.string "Sometimes it drops a feather here.\n"
	.string "It never stays for dinner.$"
