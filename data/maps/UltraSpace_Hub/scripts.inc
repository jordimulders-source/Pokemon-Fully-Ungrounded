UltraSpace_Hub_MapScripts::
	.byte 0

UltraSpace_Hub_EventScript_Portal::
	lock
	goto_if_set FLAG_ULTRA_HUB_VISITED, UltraSpace_Hub_EventScript_PortalGo
	setflag FLAG_ULTRA_HUB_VISITED
	msgbox UltraSpace_Hub_Text_PortalFirst, MSGBOX_DEFAULT
UltraSpace_Hub_EventScript_PortalGo::
	special Ultra_CountOpen
	goto_if_ne VAR_RESULT, 0, UltraSpace_Hub_EventScript_PortalJump
	msgbox UltraSpace_Hub_Text_PortalAllDone, MSGBOX_DEFAULT
	closemessage
UltraSpace_Hub_EventScript_PortalJump::
	playse SE_M_TELEPORT
	waitse
	goto UltraSpace_Hub_EventScript_PortalWarp

@ Na het vangen van een Ultra Beast: even stil, dan verder (gedeeld door alle plekken)
UltraSpace_EventScript_CaughtFade::
	removeobject VAR_LAST_TALKED
	release
	end

UltraSpace_Hub_EventScript_Cosmog::
	lock
	faceplayer
	playmoncry SPECIES_COSMOG, CRY_MODE_NORMAL
	msgbox UltraSpace_Hub_Text_Cosmog, MSGBOX_DEFAULT
	waitmoncry
	release
	end

UltraSpace_Hub_EventScript_Sign::
	msgbox UltraSpace_Hub_Text_Sign, MSGBOX_SIGN
	end

@ ultra_space { gegenereerd door tools/grounded/maptools/ultra_space.py; niet met de hand bewerken
UltraSpace_Hub_EventScript_PortalWarp::
	special Ultra_PickPortal
	switch VAR_RESULT
	case 0, UltraSpace_Hub_EventScript_ToNihilego
	case 1, UltraSpace_Hub_EventScript_ToBuzzwole
	case 2, UltraSpace_Hub_EventScript_ToPheromosa
	case 3, UltraSpace_Hub_EventScript_ToXurkitree
	case 4, UltraSpace_Hub_EventScript_ToCelesteela
	case 5, UltraSpace_Hub_EventScript_ToKartana
	case 6, UltraSpace_Hub_EventScript_ToGuzzlord
	case 7, UltraSpace_Hub_EventScript_ToPoipole
	case 8, UltraSpace_Hub_EventScript_ToStakataka
	case 9, UltraSpace_Hub_EventScript_ToBlacephalon
	case 10, UltraSpace_Hub_EventScript_ToNecrozma
	end
UltraSpace_Hub_EventScript_ToNihilego::
	warp MAP_ULTRA_SPACE_NIHILEGO, 20, 27
	waitstate
	end
UltraSpace_Hub_EventScript_ToBuzzwole::
	warp MAP_ULTRA_SPACE_BUZZWOLE, 20, 28
	waitstate
	end
UltraSpace_Hub_EventScript_ToPheromosa::
	warp MAP_ULTRA_SPACE_PHEROMOSA, 28, 26
	waitstate
	end
UltraSpace_Hub_EventScript_ToXurkitree::
	warp MAP_ULTRA_SPACE_XURKITREE, 20, 27
	waitstate
	end
UltraSpace_Hub_EventScript_ToCelesteela::
	warp MAP_ULTRA_SPACE_CELESTEELA, 24, 30
	waitstate
	end
UltraSpace_Hub_EventScript_ToKartana::
	warp MAP_ULTRA_SPACE_KARTANA, 18, 24
	waitstate
	end
UltraSpace_Hub_EventScript_ToGuzzlord::
	warp MAP_ULTRA_SPACE_GUZZLORD, 38, 28
	waitstate
	end
UltraSpace_Hub_EventScript_ToPoipole::
	warp MAP_ULTRA_SPACE_POIPOLE, 6, 28
	waitstate
	end
UltraSpace_Hub_EventScript_ToStakataka::
	warp MAP_ULTRA_SPACE_STAKATAKA, 20, 30
	waitstate
	end
UltraSpace_Hub_EventScript_ToBlacephalon::
	warp MAP_ULTRA_SPACE_BLACEPHALON, 20, 28
	waitstate
	end
UltraSpace_Hub_EventScript_ToNecrozma::
	warp MAP_ULTRA_SPACE_NECROZMA, 21, 28
	waitstate
	end

UltraSpace_EventScript_ReturnToHub::
	lock
	playse SE_M_TELEPORT
	waitse
	warp MAP_ULTRA_SPACE_HUB, 13, 17
	waitstate
	release
	end

UltraSpace_Hub_EventScript_ToAlteringCave::
	lock
	playse SE_M_TELEPORT
	waitse
	warp MAP_ALTERING_CAVE, 4, 5
	waitstate
	release
	end
@ }

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
UltraSpace_Hub_Text_PortalFirst:
	.string "A hole in reality, humming like a fridge\n"
	.string "at 3 AM.\p"
	.string "Something on the other side is thinking\n"
	.string "about you. It is not thinking nice\l"
	.string "things.\p"
	.string "The hole picks where you go. You do not\n"
	.string "get a vote. Welcome to democracy.$"

UltraSpace_Hub_Text_PortalAllDone:
	.string "The portal has run out of strangers. It\n"
	.string "sends you somewhere anyway, for old\l"
	.string "times' sake.$"

UltraSpace_Hub_Text_Cosmog:
	.string "COSMOG: Pew!\p"
	.string "It seems to be lost. Or it is exactly\n"
	.string "where it wants to be, and you are lost.$"

UltraSpace_Hub_Text_Sign:
	.string "ULTRA SPACE Please do not feed the\n"
	.string "beasts.\p"
	.string "The beasts will feed themselves.$"

