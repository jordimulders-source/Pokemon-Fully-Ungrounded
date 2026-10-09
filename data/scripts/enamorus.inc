@ Project Grounded: Enamorus en de liefdesdagen (post-game, na de drie Forces). Welk stadje vandaag liefdesdag
@ heeft, loot src/enamorus.c per dag; de objecten staan achteraan de map.json van Oldale, Dewford, Fallarbor en
@ Lavaridge (tools/grounded/maptools/enamorus_towns.py). Gevangen = weg voorgoed, verslagen = weg tot een
@ volgende liefdesdag, vluchten/verliezen mag.

Enamorus_EventScript_Enamorus::
	lock
	faceplayer
	playmoncry SPECIES_ENAMORUS_INCARNATE, CRY_MODE_ENCOUNTER
	msgbox Enamorus_Text_Enamorus, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ENAMORUS_INCARNATE, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Enamorus_EventScript_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Enamorus_EventScript_Defeated
	release
	end

Enamorus_EventScript_Caught::
	setflag FLAG_ENAMORUS_DONE
	setflag FLAG_ENAMORUS_HIDE
	removeobject VAR_LAST_TALKED
	msgbox Enamorus_Text_Caught, MSGBOX_DEFAULT
	release
	end

Enamorus_EventScript_Defeated::
	special Enamorus_Defeated
	setflag FLAG_ENAMORUS_HIDE
	removeobject VAR_LAST_TALKED
	msgbox Enamorus_Text_Defeated, MSGBOX_DEFAULT
	release
	end

@ Koppels: wie je aanspreekt krijgt een hartje, de tekst is van het hele koppel.
Enamorus_EventScript_Heart::
	applymovement VAR_LAST_TALKED, Enamorus_Movement_Heart
	waitmovement 0
	return

Enamorus_EventScript_OldaleCouple::
	lock
	call Enamorus_EventScript_Heart
	msgbox Enamorus_Text_OldaleCouple, MSGBOX_DEFAULT
	release
	end

Enamorus_EventScript_DewfordCouple::
	lock
	call Enamorus_EventScript_Heart
	msgbox Enamorus_Text_DewfordCouple, MSGBOX_DEFAULT
	release
	end

Enamorus_EventScript_FallarborCouple::
	lock
	call Enamorus_EventScript_Heart
	msgbox Enamorus_Text_FallarborCouple, MSGBOX_DEFAULT
	release
	end

Enamorus_EventScript_LavaridgeCouple::
	lock
	call Enamorus_EventScript_Heart
	msgbox Enamorus_Text_LavaridgeCouple, MSGBOX_DEFAULT
	release
	end

@ Prof. Birch en de drol van het strandresort (ParadisoResort_Text_Turd): hij volgt de liefde, stadje na stadje.
Enamorus_EventScript_Birch::
	lock
	call Enamorus_EventScript_Heart
	msgbox Enamorus_Text_Birch, MSGBOX_DEFAULT
	release
	end

Enamorus_EventScript_Turd::
	msgbox Enamorus_Text_Turd, MSGBOX_SIGN
	end

Enamorus_Movement_Heart:
	emote_heart
	step_end

Enamorus_Text_Enamorus:
	.string "ENAMORUS is hovering over town,\n"
	.string "raining pink petals on everyone.\p"
	.string "Two strangers just got engaged.\n"
	.string "A third is filing for divorce.\p"
	.string "It looks at you like you're\n"
	.string "next on the list.$"

Enamorus_Text_Caught:
	.string "The pink haze lifts.\p"
	.string "Nobody stops kissing, though.\n"
	.string "Turns out that was just them.$"

Enamorus_Text_Defeated:
	.string "ENAMORUS storms off, sulking.\p"
	.string "It'll be back on some other day\n"
	.string "of love. Exes always are.$"

Enamorus_Text_OldaleCouple:
	.string "OLD MAN: We've been neighbours for\n"
	.string "forty years. Today I noticed her.\p"
	.string "OLD WOMAN: He brought me flowers.\n"
	.string "From my own garden.\p"
	.string "With the roots still on.\n"
	.string "Nobody has ever been so thorough.$"

Enamorus_Text_DewfordCouple:
	.string "SAILOR: I've sailed every sea in\n"
	.string "HOENN. None of them looked at me\l"
	.string "the way she does.\p"
	.string "BEAUTY: He smells like a harbour.\n"
	.string "I've decided that's a personality.$"

Enamorus_Text_FallarborCouple:
	.string "HIKER: I gave her a rock.\n"
	.string "My second-best rock.\p"
	.string "PICNICKER: Nobody's ever given me a\n"
	.string "rock. I don't know what to do with\l"
	.string "my hands.\p"
	.string "HIKER: You hold the rock.\n"
	.string "That's what the hands are for.$"

Enamorus_Text_LavaridgeCouple:
	.string "PSYCHIC: I've seen our future.\n"
	.string "In nine years, she leaves me for\l"
	.string "a CAMERUPT.\p"
	.string "HEX MANIAC: I cursed him so he'd\n"
	.string "love me forever. Ehehe...\p"
	.string "It's going really well.\n"
	.string "Better than the last three.$"

Enamorus_Text_Birch:
	.string "PROF. BIRCH: Shh! Not so loud,\n"
	.string "you'll embarrass her.\p"
	.string "We met at the resort. Everybody\n"
	.string "said she was just a turd.\p"
	.string "But she listens. She never\n"
	.string "interrupts. She has never once\l"
	.string "asked about my research funding.\p"
	.string "My wife calls it a cry for help.\n"
	.string "My kid won't make eye contact.\p"
	.string "It's fieldwork. Very, very\n"
	.string "close fieldwork.$"

Enamorus_Text_Turd:
	.string "It's the turd from the resort.\p"
	.string "Somebody tied a little pink bow\n"
	.string "on it. It smells of aftershave.\p"
	.string "BIRCH's aftershave.$"
