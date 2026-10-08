@ Project Grounded: Hoopa's schatkamer (Hoopa-quest). Hoopa Unbound heeft Salim en jou hierheen geringd, tussen de
@ gestolen Hoenn-spullen. Hoopa Unbound (lv 70) staat boven aan de trap. Vang je hem, dan heb je Hoopa Unbound;
@ versla je hem, dan krimpt hij tot Hoopa Confined en sluit hij zich bij je aan (givemon). Daarna geeft Salim je de
@ Prison Bottle (wisselt Confined/Unbound) en ringt hij zichzelf terug naar de bazaar.
@ Kaart: tools/grounded/maptools/mirage_bazaar.py.

MirageBazaar_Vault_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MirageBazaar_Vault_OnTransition
	.byte 0

MirageBazaar_Vault_OnTransition:
	goto_if_unset FLAG_HOOPA_QUEST_DONE, MirageBazaar_Vault_EventScript_TransitionEnd
	setflag FLAG_HIDE_HOOPA_VAULT_HOOPA
	setflag FLAG_HIDE_HOOPA_VAULT_SALIM
MirageBazaar_Vault_EventScript_TransitionEnd:
	end

MirageBazaar_Vault_EventScript_ExitRing::
	lockall
	playse SE_WARP_IN
	warp MAP_MIRAGE_BAZAAR, 14, 20
	waitstate
	releaseall
	end

MirageBazaar_Vault_EventScript_Salim::
	msgbox MirageBazaar_Vault_Text_Salim, MSGBOX_NPC
	end

@ --- het eindgevecht ---
MirageBazaar_Vault_EventScript_Hoopa::
	lock
	playmoncry SPECIES_HOOPA_UNBOUND, CRY_MODE_ENCOUNTER
	msgbox MirageBazaar_Vault_Text_Hoopa, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_HOOPA_UNBOUND, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MirageBazaar_Vault_EventScript_HoopaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MirageBazaar_Vault_EventScript_HoopaStays
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MirageBazaar_Vault_EventScript_HoopaCaught
	@ verslagen: Hoopa krimpt en gaat met je mee
	msgbox MirageBazaar_Vault_Text_HoopaShrinks, MSGBOX_DEFAULT
	bufferspeciesname STR_VAR_1, SPECIES_HOOPA_CONFINED
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_HOOPA_CONFINED
	givemon SPECIES_HOOPA_CONFINED, 70
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, MirageBazaar_Vault_EventScript_NoRoom
	copyvar VAR_0x8005, VAR_RESULT
	playfanfare MUS_OBTAIN_ITEM
	message MirageBazaar_Vault_Text_ReceivedHoopa
	waitmessage
	waitfanfare
	call_if_eq VAR_0x8005, MON_GIVEN_TO_PC, Common_EventScript_TransferredToPC
	removeobject LOCALID_HOOPA_VAULT_HOOPA
	goto MirageBazaar_Vault_EventScript_Ending

MirageBazaar_Vault_EventScript_NoRoom::
	msgbox MirageBazaar_Vault_Text_NoRoom, MSGBOX_DEFAULT
	release
	end

MirageBazaar_Vault_EventScript_HoopaCaught::
	removeobject LOCALID_HOOPA_VAULT_HOOPA
	msgbox MirageBazaar_Vault_Text_HoopaCaught, MSGBOX_DEFAULT
	goto MirageBazaar_Vault_EventScript_Ending

MirageBazaar_Vault_EventScript_HoopaStays::
	release
	end

MirageBazaar_Vault_EventScript_Ending::
	setflag FLAG_HIDE_HOOPA_VAULT_HOOPA
	setflag FLAG_HOOPA_QUEST_DONE
	msgbox MirageBazaar_Vault_Text_SalimThanks, MSGBOX_DEFAULT
	giveitem ITEM_PRISON_BOTTLE
	msgbox MirageBazaar_Vault_Text_SalimBottle, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreenswapbuffers FADE_TO_WHITE
	removeobject LOCALID_HOOPA_VAULT_SALIM
	setflag FLAG_HIDE_HOOPA_VAULT_SALIM
	fadescreenswapbuffers FADE_FROM_WHITE
	release
	end

@ --- de buit ---
MirageBazaar_Vault_EventScript_BirchsBag::
	msgbox MirageBazaar_Vault_Text_BirchsBag, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_Truck::
	msgbox MirageBazaar_Vault_Text_Truck, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_Boat::
	msgbox MirageBazaar_Vault_Text_Boat, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_CableCar::
	msgbox MirageBazaar_Vault_Text_CableCar, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_Peeko::
	lock
	faceplayer
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
	msgbox MirageBazaar_Vault_Text_Peeko, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MirageBazaar_Vault_EventScript_Poochyena::
	lock
	faceplayer
	playmoncry SPECIES_POOCHYENA, CRY_MODE_NORMAL
	msgbox MirageBazaar_Vault_Text_Poochyena, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MirageBazaar_Vault_EventScript_Fossil::
	msgbox MirageBazaar_Vault_Text_Fossil, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_Box::
	msgbox MirageBazaar_Vault_Text_Box, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_StolenPC::
	msgbox MirageBazaar_Vault_Text_StolenPC, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_StolenMachine::
	msgbox MirageBazaar_Vault_Text_StolenMachine, MSGBOX_SIGN
	end

MirageBazaar_Vault_EventScript_Statue::
	msgbox MirageBazaar_Vault_Text_Statue, MSGBOX_SIGN
	end

@ ====================================================================== teksten
MirageBazaar_Vault_Text_Salim:
	.string "SALIM: Welcome to HOOPA's vault.\n"
	.string "He's been doing this for centuries.\p"
	.string "I've been filed under “MISC.”\p"
	.string "Get up those stairs and hit him\n"
	.string "until he's small again.$"

MirageBazaar_Vault_Text_Hoopa:
	.string "HOOPA: MINE! ALL MINE!\n"
	.string "YOU TOO! YOU'RE MINE TOO!$"

MirageBazaar_Vault_Text_HoopaShrinks:
	.string "HOOPA shrinks back down with a sad\n"
	.string "little pop.\p"
	.string "HOOPA: ...Hoopa is small again.\n"
	.string "Hoopa has nowhere to go.\p"
	.string "Hoopa goes with you. Hoopa decided.\n"
	.string "Hoopa is very good at deciding.$"

MirageBazaar_Vault_Text_ReceivedHoopa:
	.string "{PLAYER} received HOOPA!$"

MirageBazaar_Vault_Text_NoRoom:
	.string "There's no room for HOOPA.\p"
	.string "HOOPA rings itself back to the top\n"
	.string "of the stairs. It will wait.$"

MirageBazaar_Vault_Text_HoopaCaught:
	.string "HOOPA is in a POKé BALL now.\n"
	.string "Technically, that's just a ring.$"

MirageBazaar_Vault_Text_SalimThanks:
	.string "SALIM: You did it. My stock is back.\n"
	.string "Mostly. Somebody's boat is still here.\p"
	.string "Take the PRISON BOTTLE. Keep it far\n"
	.string "away from me.$"

MirageBazaar_Vault_Text_SalimBottle:
	.string "SALIM: It makes HOOPA big or small.\p"
	.string "Whatever he steals while he's big\n"
	.string "is your problem now.\p"
	.string "I'll ring myself home. I'm very good\n"
	.string "at being stolen by now.$"

MirageBazaar_Vault_Text_BirchsBag:
	.string "PROF. BIRCH's bag. Again.\p"
	.string "There's a note inside: “If found,\n"
	.string "please do not return. - B.”$"

MirageBazaar_Vault_Text_Truck:
	.string "The moving truck from LITTLEROOT.\p"
	.string "That's why there was no truck\n"
	.string "scene. HOOPA took it before the\l"
	.string "game even started.$"

MirageBazaar_Vault_Text_Boat:
	.string "MR. BRINEY's boat.\p"
	.string "MR. BRINEY is still out sailing it.\n"
	.string "He hasn't noticed yet.$"

MirageBazaar_Vault_Text_CableCar:
	.string "A cable car from MT. CHIMNEY.\p"
	.string "The other one is still going up and\n"
	.string "down alone. Nobody has told it.$"

MirageBazaar_Vault_Text_Peeko:
	.string "It's PEEKO.\p"
	.string "PEEKO has been kidnapped so many\n"
	.string "times it just goes with it now.$"

MirageBazaar_Vault_Text_Poochyena:
	.string "The POOCHYENA that chased PROF.\n"
	.string "BIRCH on ROUTE 101.\p"
	.string "It's on a break. It has a union.$"

MirageBazaar_Vault_Text_Fossil:
	.string "The fossil you didn't pick in the\n"
	.string "MIRAGE TOWER.\p"
	.string "Also the MIRAGE TOWER. It's in the\n"
	.string "back. Folded.$"

MirageBazaar_Vault_Text_Box:
	.string "A box labelled “MOM's TV - DO NOT\n"
	.string "OPEN.”\p"
	.string "It's empty. That explains the TV\n"
	.string "scene that never happened.$"

MirageBazaar_Vault_Text_StolenPC:
	.string "Someone's PC. Literally. The label\n"
	.string "says “SOMEONE.”\p"
	.string "There's an invoice from LANETTE\n"
	.string "taped to the screen.$"

MirageBazaar_Vault_Text_StolenMachine:
	.string "A BATTLE FRONTIER machine.\p"
	.string "It used to show your score. Now it\n"
	.string "just says “HOOPA.”$"

MirageBazaar_Vault_Text_Statue:
	.string "A statue of a POKéMON with a long\n"
	.string "snout.\p"
	.string "HOOPA stole it from the BATTLE\n"
	.string "PYRAMID. Then he stole the room.$"
