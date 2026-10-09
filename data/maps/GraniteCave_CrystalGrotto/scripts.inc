@ Project Grounded: kristalgrot onder Granite Cave B2F (Carbink, Steven-lore). Layout: kopie van
@ SeafloorCavern_Room3 met kristallen. Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
GraniteCave_CrystalGrotto_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GraniteCave_CrystalGrotto_Legends2_OnTransition
	.byte 0

GraniteCave_CrystalGrotto_EventScript_Collector::
	msgbox GraniteCave_CrystalGrotto_Text_Collector, MSGBOX_NPC
	end

GraniteCave_CrystalGrotto_EventScript_Scratches::
	msgbox GraniteCave_CrystalGrotto_Text_Scratches, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
GraniteCave_CrystalGrotto_Text_Collector:
	.string "Shh. The CARBINK think I'm a rock.\p"
	.string "I've been a rock for three days. My\n"
	.string "knees are basically gravel now.\p"
	.string "They say a pink princess made of\n"
	.string "diamond sleeps down here. The CARBINK\l"
	.string "say that. They're liars. Beautiful,\l"
	.string "sparkly liars.$"

GraniteCave_CrystalGrotto_Text_Scratches:
	.string "Scratched into the wall:\n"
	.string "“S. STONE WAS HERE. TOOK NOTHING.”\p"
	.string "Below it, smaller:\n"
	.string "“TOOK ONE.”\p"
	.string "Below that, smaller still:\n"
	.string "“OK, SEVEN.”$"

@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---
GraniteCave_CrystalGrotto_EventScript_Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_DIANCIE
	setflag FLAG_HIDE_LEGENDS_CARBINK
	goto_if_unset FLAG_SYS_GAME_CLEAR, GraniteCave_CrystalGrotto_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_CARBINK
	goto_if_set FLAG_RECEIVED_DIANCIE, GraniteCave_CrystalGrotto_EventScript_Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_DIANCIE
GraniteCave_CrystalGrotto_EventScript_Legends2_TransitionEnd:
	return

GraniteCave_CrystalGrotto_EventScript_Diancie::
	lock
	faceplayer
	playmoncry SPECIES_DIANCIE, CRY_MODE_ENCOUNTER
	msgbox GraniteCave_CrystalGrotto_Text_Diancie, MSGBOX_DEFAULT
	waitmoncry
	setvar VAR_0x8004, SPECIES_DIANCIE
	setvar VAR_0x8005, 80
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, GraniteCave_CrystalGrotto_EventScript_DiancieNoRoom
	setflag FLAG_RECEIVED_DIANCIE
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_LEGENDS_DIANCIE
	setflag FLAG_HIDE_LEGENDS_DIANCIE
	fadescreen FADE_FROM_BLACK
	msgbox GraniteCave_CrystalGrotto_Text_DiancieAfter, MSGBOX_DEFAULT
	release
	end

GraniteCave_CrystalGrotto_EventScript_DiancieNoRoom::
	msgbox GraniteCave_CrystalGrotto_Text_DiancieNoRoom, MSGBOX_DEFAULT
	release
	end

GraniteCave_CrystalGrotto_EventScript_Carbink::
	lock
	faceplayer
	playmoncry SPECIES_CARBINK, CRY_MODE_NORMAL
	msgbox GraniteCave_CrystalGrotto_Text_Carbink, MSGBOX_DEFAULT
	waitmoncry
	release
	end

GraniteCave_CrystalGrotto_Text_Diancie:
	.string "Between the CARBINK, a pink crystal\n"
	.string "opens its eyes.\p"
	.string "DIANCIE looks you over like a jeweller\n"
	.string "looks at a fake. Then it notices the\l"
	.string "CHAMPION ribbon, or the dirt on your\l"
	.string "shoes. Hard to say which.\p"
	.string "It floats closer. It has decided you're\n"
	.string "its new royal guard. Nobody asked the\l"
	.string "CARBINK.$"

GraniteCave_CrystalGrotto_Text_DiancieAfter:
	.string "The CARBINK watch their princess leave\n"
	.string "with you.\p"
	.string "Next door, in his own little cave, STEVEN\n"
	.string "is going to be so jealous. Don't tell him.\l"
	.string "Do tell him.$"

GraniteCave_CrystalGrotto_Text_DiancieNoRoom:
	.string "DIANCIE looks at your full party and\n"
	.string "your full PC.\p"
	.string "It refuses to be the eighth wheel. Make\n"
	.string "room.$"

GraniteCave_CrystalGrotto_Text_Carbink:
	.string "Carbink!\p"
	.string "(It's guarding the princess. It's a rock.\n"
	.string "It's doing its best.)$"
@ --- einde legends2 ---

GraniteCave_CrystalGrotto_Legends2_OnTransition:
	call GraniteCave_CrystalGrotto_EventScript_Legends2_Transition
	end
