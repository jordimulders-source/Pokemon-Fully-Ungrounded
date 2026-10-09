@ Project Grounded: gedeelde scripts voor de Kanto-/Galar-vogels (tools/grounded/maptools/legends2.py).

@ VAR_RESULT = TRUE als alle drie de Kanto-vogels gevangen zijn (dan komen de Galar-neven kijken).
Legends2_EventScript_GalarReady::
	setvar VAR_RESULT, FALSE
	goto_if_unset FLAG_CAUGHT_KANTO_ARTICUNO, Legends2_EventScript_GalarReadyEnd
	goto_if_unset FLAG_CAUGHT_KANTO_ZAPDOS, Legends2_EventScript_GalarReadyEnd
	goto_if_unset FLAG_CAUGHT_KANTO_MOLTRES, Legends2_EventScript_GalarReadyEnd
	setvar VAR_RESULT, TRUE
Legends2_EventScript_GalarReadyEnd::
	return

@ Na het vangen van een Kanto-vogel: was dit de derde, dan een hint over de Galar-vogels.
Legends2_EventScript_CheckGalarArrive::
	call Legends2_EventScript_GalarReady
	goto_if_eq VAR_RESULT, FALSE, Legends2_EventScript_GalarReadyEnd
	msgbox Legends2_Text_GalarArrive, MSGBOX_DEFAULT
	return

Legends2_Text_GalarArrive::
	.string "All three legendary birds of KANTO are\n"
	.string "in your PC now.\p"
	.string "Somewhere far away, three cousins from\n"
	.string "GALAR hear about it.\p"
	.string "They're coming to visit. They're bringing\n"
	.string "the wrong types. One of them is running.$"
