@ Project Grounded: kristalgrot onder Granite Cave B2F (Carbink, Steven-lore). Layout: kopie van
@ SeafloorCavern_Room3 met kristallen. Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
GraniteCave_CrystalGrotto_MapScripts::
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
