@ Project Grounded: debugmenu Utilities > Legendary battle - start een legendary-gevecht via dezelfde special als het echte event (thema + transitie testen)

Debug_EventScript_Legend_Regirock::
	lockall
	setwildbattle SPECIES_REGIROCK, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Regice::
	lockall
	setwildbattle SPECIES_REGICE, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Registeel::
	lockall
	setwildbattle SPECIES_REGISTEEL, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Regidrago::
	lockall
	setwildbattle SPECIES_REGIDRAGO, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Regieleki::
	lockall
	setwildbattle SPECIES_REGIELEKI, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Regigigas::
	lockall
	setwildbattle SPECIES_REGIGIGAS, 50
	special StartRegiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Suicune::
	lockall
	setwildbattle SPECIES_SUICUNE, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Raikou::
	lockall
	setwildbattle SPECIES_RAIKOU, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Entei::
	lockall
	setwildbattle SPECIES_ENTEI, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Groudon::
	lockall
	setwildbattle SPECIES_GROUDON, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Kyogre::
	lockall
	setwildbattle SPECIES_KYOGRE, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Rayquaza::
	lockall
	setwildbattle SPECIES_RAYQUAZA, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_DeoxysNormal::
	lockall
	setwildbattle SPECIES_DEOXYS_NORMAL, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Mew::
	lockall
	setwildbattle SPECIES_MEW, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Latias::
	lockall
	setwildbattle SPECIES_LATIAS, 50
	special BattleSetup_StartLatiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Latios::
	lockall
	setwildbattle SPECIES_LATIOS, 50
	special BattleSetup_StartLatiBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Lugia::
	lockall
	setwildbattle SPECIES_LUGIA, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_HoOh::
	lockall
	setwildbattle SPECIES_HO_OH, 50
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

@ Project Grounded: debugmenu Utilities > Wild battle (map) - wild gevecht uit de tabel van deze kaart (route-transities testen)
Debug_EventScript_WildFromMap::
	lockall
	special Debug_StartMapWildBattle
	goto_if_eq VAR_RESULT, FALSE, Debug_EventScript_WildFromMap_None
	waitstate
	releaseall
	end

Debug_EventScript_WildFromMap_None::
	msgbox Debug_Text_WildFromMap_None, MSGBOX_DEFAULT
	releaseall
	end

Debug_Text_WildFromMap_None:
	.string "Deze kaart heeft geen wilde Pokémon.$"

@ Project Grounded: debugmenu Utilities > Force encounter - bevestiging
Debug_EventScript_ForcedEncounterSet::
	msgbox Debug_Text_ForcedEncounterSet, MSGBOX_DEFAULT
	releaseall
	end

Debug_Text_ForcedEncounterSet:
	.string "All wild encounters: {STR_VAR_1}.\n"
	.string "Turn off: Force encounter: off.$"

@ Project Grounded: debugmenu Utilities > Force encounter: off - weer gewone encounters
Debug_EventScript_ForcedEncounterOff::
	special Debug_ClearForcedEncounter
	msgbox Debug_Text_ForcedEncounterOff, MSGBOX_DEFAULT
	releaseall
	end

Debug_Text_ForcedEncounterOff:
	.string "Wild encounters are back to normal.$"

Debug_EventScript_Legend_Heatran::
	lockall
	setwildbattle SPECIES_HEATRAN, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

@ Project Grounded: debugmenu Utilities > The Spire - start of hervat een run (beta)
@ Project Grounded: debugmenu Utilities > Warp to the Spire - meteen naar de lobby, ongeacht je voortgang.
@ Zet de Battle Frontier op de kaart en geeft het S.S. Ticket, zodat je met de veerboot ook weer weg kunt.
Debug_EventScript_SpireWarp::
	setflag FLAG_LANDMARK_BATTLE_FRONTIER
	setflag FLAG_SYS_POKEMON_GET
	checkitem ITEM_SS_TICKET
	goto_if_eq VAR_RESULT, TRUE, Debug_EventScript_SpireWarpGo
	additem ITEM_SS_TICKET
Debug_EventScript_SpireWarpGo::
	warp MAP_BATTLE_FRONTIER_SPIRE_LOBBY, 5, 10
	waitstate
	release
	end

@ Project Grounded: debugmenu Utilities > Warp to the Stadium - meteen naar de lobby van het Battle Stadium
Debug_EventScript_StadiumWarp::
	setflag FLAG_LANDMARK_BATTLE_FRONTIER
	setflag FLAG_SYS_POKEMON_GET
	checkitem ITEM_SS_TICKET
	goto_if_eq VAR_RESULT, TRUE, Debug_EventScript_StadiumWarpGo
	additem ITEM_SS_TICKET
Debug_EventScript_StadiumWarpGo::
	warp MAP_BATTLE_FRONTIER_STADIUM_LOBBY, 11, 14
	waitstate
	release
	end

Debug_EventScript_SpirePrototype::
	lockall
	special Spire_Enter
	waitstate
	releaseall
	end

@ Project Grounded: debugmenu Utilities > Spire: reset run - wist de lopende run (zonder BP)
Debug_EventScript_SpireResetRun::
	special Spire_ResetRun
	msgbox Debug_Text_SpireResetRun, MSGBOX_DEFAULT
	release
	end

Debug_Text_SpireResetRun:
	.string "Spire-run gewist.$"

@ Project Grounded: debugmenu Utilities > Stadium: unlock all - alle compagnons vrij (testen)
Debug_EventScript_StadiumUnlockAll::
	special Stadium_DebugUnlockAll
	msgbox Debug_Text_StadiumUnlockAll, MSGBOX_DEFAULT
	release
	end

Debug_Text_StadiumUnlockAll:
	.string "Alle Stadium-compagnons vrij.$"

Debug_EventScript_Legend_Genesect::
	lockall
	setwildbattle SPECIES_GENESECT, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Mewtwo::
	lockall
	setwildbattle SPECIES_MEWTWO, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Jirachi::
	lockall
	setwildbattle SPECIES_JIRACHI, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

Debug_EventScript_Legend_Darkrai::
	lockall
	setwildbattle SPECIES_DARKRAI, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	releaseall
	end

@ Project Grounded: debugmenu Utilities > Burglar: force - de Burglar staat gegarandeerd klaar in deze stad (of de
@ volgende inbrekersstad die je binnenloopt); loop vlak voor het huis langs om de scene te starten.
Debug_EventScript_BurglarForce::
	lockall
	special Burglar_DebugForce
	goto_if_eq VAR_RESULT, FALSE, Debug_EventScript_BurglarForce_Next
	msgbox Debug_Text_BurglarForce_Here, MSGBOX_DEFAULT
	releaseall
	end

Debug_EventScript_BurglarForce_Next::
	msgbox Debug_Text_BurglarForce_Next, MSGBOX_DEFAULT
	releaseall
	end

Debug_Text_BurglarForce_Here:
	.string "Burglar staat klaar in deze stad.\n"
	.string "Loop vlak voor zijn huis langs.$"

Debug_Text_BurglarForce_Next:
	.string "Burglar komt in de volgende stad: Mauville,\n"
	.string "Slateport, Lilycove, Rustboro, Verdanturf,\l"
	.string "Fallarbor of Petalburg.$"

@ Project Grounded: debugmenu Utilities > Battle test - een uniek gevecht (thema + transitie) met een tijdelijk testteam;
@ party, geld, Pokédex en statistieken worden na afloop teruggezet (Debug_BattleTest_Start in src/debug.c)
Debug_EventScript_BattleTest::
	lockall
	special Debug_BattleTest_Start
	waitstate
	releaseall
	end
