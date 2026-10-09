@ Project Grounded: Azure Flute, Arceus in de Spacetime Cave en de trap van licht op Sky Pillar.
@ Gegenereerd door tools/grounded/maptools/hall_of_origin.py; de hintlijst door tools/grounded/azure_flute.py.

@ ---------------------------------------------------------------- de fluit (vanuit de tas, src/item_use.c)
EventScript_AzureFlute::
	lockall
	playfanfare MUS_RG_POKE_FLUTE
	goto_if_set FLAG_HALL_ARCEUS_DONE, AzureFlute_EventScript_AfterArceus
	goto_if_set FLAG_HALL_OF_ORIGIN_OPEN, AzureFlute_EventScript_StairOpen
	goto_if_set FLAG_ARCEUS_SKY_PILLAR, AzureFlute_EventScript_SkyPillar
	special AzureFlute_GetHint
	goto_if_eq VAR_RESULT, 0, AzureFlute_EventScript_AllDone
	msgbox gStringVar4, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_AllDone:
	call AzureFlute_EventScript_Flash
	msgbox AzureFlute_Text_AllDone, MSGBOX_DEFAULT
	setflag FLAG_ARCEUS_SKY_PILLAR
	releaseall
	end

AzureFlute_EventScript_SkyPillar:
	msgbox AzureFlute_Text_SkyPillar, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_StairOpen:
	msgbox AzureFlute_Text_StairOpen, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_AfterArceus:
	msgbox AzureFlute_Text_AfterArceus, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_Flash:
	fadescreenspeed FADE_TO_WHITE, 0
	fadescreenspeed FADE_FROM_WHITE, 2
	fadescreenspeed FADE_TO_WHITE, 0
	fadescreenspeed FADE_FROM_WHITE, 2
	return

@ ---------------------------------------------------------------- Spacetime Cave: Arceus spreekt (na Spear Pillar)
@ Haak in SpacetimeCave_OnTransition / _OnFrame (spacetime_cave.py): VAR_TEMP_3 = 1 -> scene.
Spacetime_EventScript_ArmArceus::
	goto_if_unset FLAG_SPACETIME_CORONET_DONE, Common_EventScript_NopReturn
	goto_if_set FLAG_ARCEUS_MET, Common_EventScript_NopReturn
	setvar VAR_TEMP_3, 1
	return

Spacetime_EventScript_ArceusScene::
	lockall
	setvar VAR_TEMP_3, 0
	delay 30
	call AzureFlute_EventScript_Flash
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox Spacetime_Text_ArceusVoice1, MSGBOX_DEFAULT
	call AzureFlute_EventScript_Flash
	msgbox Spacetime_Text_ArceusVoice2, MSGBOX_DEFAULT
	giveitem ITEM_AZURE_FLUTE
	setflag FLAG_ARCEUS_MET
	msgbox Spacetime_Text_ArceusVoice3, MSGBOX_DEFAULT
	releaseall
	end

@ ---------------------------------------------------------------- Sky Pillar: de trap van licht
@ Haak in SkyPillar_Top_OnTransition / _OnFrame: VAR_TEMP_4 = 1 -> scene bij de eerste keer na de fluit.
SkyPillar_Top_EventScript_ArmHallOfOrigin::
	goto_if_unset FLAG_ARCEUS_SKY_PILLAR, Common_EventScript_NopReturn
	goto_if_set FLAG_HALL_OF_ORIGIN_OPEN, Common_EventScript_NopReturn
	setvar VAR_TEMP_4, 1
	return

SkyPillar_Top_EventScript_HallOfOriginScene::
	lockall
	setvar VAR_TEMP_4, 0
	delay 20
	msgbox SkyPillar_Top_Text_ArceusCalls, MSGBOX_DEFAULT
	closemessage
	call AzureFlute_EventScript_Flash
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	setflag FLAG_HALL_OF_ORIGIN_OPEN
	msgbox SkyPillar_Top_Text_StairDescends, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	setdynamicwarp MAP_SKY_PILLAR_TOP, 1
	warpsilent MAP_HALL_OF_ORIGIN_STAIRWAY, 0
	waitstate
	releaseall
	end

SkyPillar_Top_EventScript_StairOfLight::
	goto_if_unset FLAG_HALL_OF_ORIGIN_OPEN, SkyPillar_Top_EventScript_NoStair
	lockall
	msgbox SkyPillar_Top_Text_StairOfLight, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SkyPillar_Top_EventScript_StairRelease
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	setdynamicwarp MAP_SKY_PILLAR_TOP, 1
	warpsilent MAP_HALL_OF_ORIGIN_STAIRWAY, 0
	waitstate
SkyPillar_Top_EventScript_StairRelease:
	releaseall
	end

SkyPillar_Top_EventScript_NoStair:
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
AzureFlute_Text_AllDone:
	.string "The AZURE FLUTE plays a note that goes\n"
	.string "on far longer than your breath.\p"
	.string "ARCEUS: Every legend answers to you\n"
	.string "now. Even the ones who hate answering.\p"
	.string "Meet me at the top. SKY PILLAR or SPEAR\n"
	.string "PILLAR, I built both and I'm not\l"
	.string "precious about it. Don't bring snacks;\l"
	.string "I'll know.$"

AzureFlute_Text_SkyPillar:
	.string "The AZURE FLUTE hums: SKY PILLAR or\n"
	.string "SPEAR PILLAR. The top of either.\p"
	.string "It says it in the tone of a parent who\n"
	.string "has already said it twice.$"

AzureFlute_Text_StairOpen:
	.string "The AZURE FLUTE points up. Way up.\n"
	.string "Above SKY PILLAR and SPEAR PILLAR a\l"
	.string "stair of light is still waiting for you.$"

AzureFlute_Text_AfterArceus:
	.string "The AZURE FLUTE plays a little tune.\n"
	.string "Somewhere, ARCEUS hums along. Off-key.\l"
	.string "On purpose.$"

Spacetime_Text_ArceusVoice1:
	.string "A voice. Not from the cave. Not from\n"
	.string "anywhere. From the gaps between.\p"
	.string "???: You walked through time. You\n"
	.string "walked through space. Both of them\l"
	.string "complained about you to me.\p"
	.string "I am ARCEUS. I'm the one they complain\n"
	.string "to.$"

Spacetime_Text_ArceusVoice2:
	.string "ARCEUS: The legends of every world are\n"
	.string "scattered, sulking in caves and\l"
	.string "volcanoes and very specific islands.\p"
	.string "Gather them. All of them. Take this, so\n"
	.string "you don't get lost. I've seen your sense\l"
	.string "of direction.$"

Spacetime_Text_ArceusVoice3:
	.string "ARCEUS: Play it, and it will tell you who\n"
	.string "is still missing. It does not do\l"
	.string "requests.\p"
	.string "When it falls silent, find me. I'll be the\n"
	.string "one at the top.$"

SkyPillar_Top_Text_ArceusCalls:
	.string "The AZURE FLUTE starts playing on its\n"
	.string "own, from inside your bag.\p"
	.string "ARCEUS: Up here. No, further. Further.\n"
	.string "There.$"

SkyPillar_Top_Text_StairDescends:
	.string "A stair of light unfolds out of the sky\n"
	.string "and stops right in front of your feet.\p"
	.string "It doesn't have a railing. Of course it\n"
	.string "doesn't.$"

SkyPillar_Top_Text_StairOfLight:
	.string "A stair of light hangs above the old\n"
	.string "altar, humming.\p"
	.string "Climb to the HALL OF ORIGIN?$"
