@ Project Grounded: debugmenu Utilities > Legendary battle - start een legendary-gevecht via dezelfde special als het echte event (thema + transitie testen)

Debug_EventScript_Legend_Regirock::
	lockall
	setwildbattle SPECIES_REGIROCK, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Regice::
	lockall
	setwildbattle SPECIES_REGICE, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Registeel::
	lockall
	setwildbattle SPECIES_REGISTEEL, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Regidrago::
	lockall
	setwildbattle SPECIES_REGIDRAGO, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Regieleki::
	lockall
	setwildbattle SPECIES_REGIELEKI, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Regigigas::
	lockall
	setwildbattle SPECIES_REGIGIGAS, 50
	special StartRegiBattle
	releaseall
	end

Debug_EventScript_Legend_Suicune::
	lockall
	setwildbattle SPECIES_SUICUNE, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Raikou::
	lockall
	setwildbattle SPECIES_RAIKOU, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Entei::
	lockall
	setwildbattle SPECIES_ENTEI, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Groudon::
	lockall
	setwildbattle SPECIES_GROUDON, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Kyogre::
	lockall
	setwildbattle SPECIES_KYOGRE, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Rayquaza::
	lockall
	setwildbattle SPECIES_RAYQUAZA, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_DeoxysNormal::
	lockall
	setwildbattle SPECIES_DEOXYS_NORMAL, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Mew::
	lockall
	setwildbattle SPECIES_MEW, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Latias::
	lockall
	setwildbattle SPECIES_LATIAS, 50
	special BattleSetup_StartLatiBattle
	releaseall
	end

Debug_EventScript_Legend_Latios::
	lockall
	setwildbattle SPECIES_LATIOS, 50
	special BattleSetup_StartLatiBattle
	releaseall
	end

Debug_EventScript_Legend_Lugia::
	lockall
	setwildbattle SPECIES_LUGIA, 50
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_HoOh::
	lockall
	setwildbattle SPECIES_HO_OH, 50
	special BattleSetup_StartLegendaryBattle
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
	releaseall
	end

Debug_EventScript_Legend_Genesect::
	lockall
	setwildbattle SPECIES_GENESECT, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Mewtwo::
	lockall
	setwildbattle SPECIES_MEWTWO, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Jirachi::
	lockall
	setwildbattle SPECIES_JIRACHI, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_Darkrai::
	lockall
	setwildbattle SPECIES_DARKRAI, 70
	special BattleSetup_StartLegendaryBattle
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
	.string "Burglar komt in de volgende stad:\n"
	.string "Mauville, Slateport, Lilycove, Rustboro,\l"
	.string "Verdanturf, Fallarbor of Petalburg.$"

@ Project Grounded: debugmenu Utilities > Battle test - een uniek gevecht (thema + transitie) met een tijdelijk testteam;
@ party, geld, Pokédex en statistieken worden na afloop teruggezet (Debug_BattleTest_Start in src/debug.c)
Debug_EventScript_BattleTest::
	lockall
	special Debug_BattleTest_Start
	waitstate
	releaseall
	end

@ Project Grounded: alle legendaries met een eigen intro/thema (debug > Legendary battle)
Debug_EventScript_Legend_G_ArceusNormal::
	lockall
	setwildbattle SPECIES_ARCEUS_NORMAL, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Dialga::
	lockall
	setwildbattle SPECIES_DIALGA, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Palkia::
	lockall
	setwildbattle SPECIES_PALKIA, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_GiratinaAltered::
	lockall
	setwildbattle SPECIES_GIRATINA_ALTERED, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Celebi::
	lockall
	setwildbattle SPECIES_CELEBI, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Uxie::
	lockall
	setwildbattle SPECIES_UXIE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Mesprit::
	lockall
	setwildbattle SPECIES_MESPRIT, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Azelf::
	lockall
	setwildbattle SPECIES_AZELF, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Cresselia::
	lockall
	setwildbattle SPECIES_CRESSELIA, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_MeloettaAria::
	lockall
	setwildbattle SPECIES_MELOETTA_ARIA, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Zeraora::
	lockall
	setwildbattle SPECIES_ZERAORA, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Zygarde50::
	lockall
	setwildbattle SPECIES_ZYGARDE_50, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Necrozma::
	lockall
	setwildbattle SPECIES_NECROZMA, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Eternatus::
	lockall
	setwildbattle SPECIES_ETERNATUS, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Calyrex::
	lockall
	setwildbattle SPECIES_CALYREX, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Glastrier::
	lockall
	setwildbattle SPECIES_GLASTRIER, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Spectrier::
	lockall
	setwildbattle SPECIES_SPECTRIER, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Cobalion::
	lockall
	setwildbattle SPECIES_COBALION, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Terrakion::
	lockall
	setwildbattle SPECIES_TERRAKION, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Virizion::
	lockall
	setwildbattle SPECIES_VIRIZION, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_KeldeoOrdinary::
	lockall
	setwildbattle SPECIES_KELDEO_ORDINARY, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Pecharunt::
	lockall
	setwildbattle SPECIES_PECHARUNT, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Xerneas::
	lockall
	setwildbattle SPECIES_XERNEAS, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Yveltal::
	lockall
	setwildbattle SPECIES_YVELTAL, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ZacianHero::
	lockall
	setwildbattle SPECIES_ZACIAN_HERO, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ZamazentaHero::
	lockall
	setwildbattle SPECIES_ZAMAZENTA_HERO, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Articuno::
	lockall
	setwildbattle SPECIES_ARTICUNO, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Zapdos::
	lockall
	setwildbattle SPECIES_ZAPDOS, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Moltres::
	lockall
	setwildbattle SPECIES_MOLTRES, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ArticunoGalar::
	lockall
	setwildbattle SPECIES_ARTICUNO_GALAR, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ZapdosGalar::
	lockall
	setwildbattle SPECIES_ZAPDOS_GALAR, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_MoltresGalar::
	lockall
	setwildbattle SPECIES_MOLTRES_GALAR, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Victini::
	lockall
	setwildbattle SPECIES_VICTINI, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ShayminLand::
	lockall
	setwildbattle SPECIES_SHAYMIN_LAND, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Manaphy::
	lockall
	setwildbattle SPECIES_MANAPHY, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Volcanion::
	lockall
	setwildbattle SPECIES_VOLCANION, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_HoopaConfined::
	lockall
	setwildbattle SPECIES_HOOPA_CONFINED, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_TornadusIncarnate::
	lockall
	setwildbattle SPECIES_TORNADUS_INCARNATE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ThundurusIncarnate::
	lockall
	setwildbattle SPECIES_THUNDURUS_INCARNATE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_LandorusIncarnate::
	lockall
	setwildbattle SPECIES_LANDORUS_INCARNATE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Zarude::
	lockall
	setwildbattle SPECIES_ZARUDE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_WoChien::
	lockall
	setwildbattle SPECIES_WO_CHIEN, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ChienPao::
	lockall
	setwildbattle SPECIES_CHIEN_PAO, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_TingLu::
	lockall
	setwildbattle SPECIES_TING_LU, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_ChiYu::
	lockall
	setwildbattle SPECIES_CHI_YU, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_OgerponTeal::
	lockall
	setwildbattle SPECIES_OGERPON_TEAL, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_TapuKoko::
	lockall
	setwildbattle SPECIES_TAPU_KOKO, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Nihilego::
	lockall
	setwildbattle SPECIES_NIHILEGO, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Buzzwole::
	lockall
	setwildbattle SPECIES_BUZZWOLE, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Pheromosa::
	lockall
	setwildbattle SPECIES_PHEROMOSA, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Kartana::
	lockall
	setwildbattle SPECIES_KARTANA, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Koraidon::
	lockall
	setwildbattle SPECIES_KORAIDON, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Miraidon::
	lockall
	setwildbattle SPECIES_MIRAIDON, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_TerapagosNormal::
	lockall
	setwildbattle SPECIES_TERAPAGOS_NORMAL, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_GreatTusk::
	lockall
	setwildbattle SPECIES_GREAT_TUSK, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_IronValiant::
	lockall
	setwildbattle SPECIES_IRON_VALIANT, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Reshiram::
	lockall
	setwildbattle SPECIES_RESHIRAM, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Zekrom::
	lockall
	setwildbattle SPECIES_ZEKROM, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Kyurem::
	lockall
	setwildbattle SPECIES_KYUREM, 80
	special BattleSetup_StartLegendaryBattle
	releaseall
	end

Debug_EventScript_Legend_G_Marshadow::
	lockall
	setwildbattle SPECIES_MARSHADOW, 70
	special BattleSetup_StartLegendaryBattle
	releaseall
	end
