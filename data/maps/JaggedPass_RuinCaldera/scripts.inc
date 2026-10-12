JaggedPass_RuinCaldera_MapScripts::
	.byte 0

@ Project Grounded: het oude lavaveld van Chi-Yu. Sinds v0.9.173 staat Chi-Yu in JaggedPass_RuinChamber en is deze
@ kaart onbereikbaar (alleen een uitgang terug, voor een save die hier nog staat). De inscriptie hieronder staat nu
@ op de rechteronderstaak van de kamer.
JaggedPass_RuinCaldera_EventScript_Stake::
	msgbox JaggedPass_RuinCaldera_Text_Stake, MSGBOX_SIGN
	end

JaggedPass_RuinCaldera_Text_Stake:
	.string "“HERE THE BEADS ARE KEPT. THEY WANTED\n"
	.string "EVERYTHING TO BURN, SO THEY BURN\l"
	.string "FOREVER.”\p"
	.string "Underneath, scratched in later: “bring\n"
	.string "marshmallows. do not bring the\l"
	.string "marshmallows back.”$"
