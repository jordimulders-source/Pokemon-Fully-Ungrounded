@ Project Grounded: LavenderTown_Mart (kopie van AshfrostTown_Mart, tools/grounded/maptools/spacetime_cave.py)
LavenderTown_Mart_MapScripts::
	.byte 0

LavenderTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	badgemart LavenderTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
LavenderTown_Mart_Pokemart:
	pokemartlistend
