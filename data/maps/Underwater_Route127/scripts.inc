Underwater_Route127_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Underwater_Route127_OnResume
	map_script MAP_SCRIPT_ON_LOAD, Underwater_Route127_OnLoad
	.byte 0

Underwater_Route127_OnResume:
	call AbnormalWeather_Underwater_SetupEscapeWarp
	end

@ Project Grounded: Ogerpon-quest. Zodra de maskerhoedster het verhaal heeft verteld, is er een zwemgat (72,45) in de
@ noordwand van de zuidoostelijke kom, naar de grot van Fezandipiti (Route127_WellspringGrotto).
Underwater_Route127_OnLoad:
	goto_if_unset FLAG_OGERPON_QUEST_STARTED, Underwater_Route127_EventScript_NoGrotto
	setmetatile 71, 44, 0x265, TRUE
	setmetatile 72, 44, 0x266, TRUE
	setmetatile 73, 44, 0x267, TRUE
	setmetatile 71, 45, 0x26D, TRUE
	setmetatile 72, 45, 0x26E, FALSE
	setmetatile 73, 45, 0x26F, TRUE
Underwater_Route127_EventScript_NoGrotto:
	end
