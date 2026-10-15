AshfrostTown_Mart_MapScripts::
	.byte 0

AshfrostTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	badgemart AshfrostTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
AshfrostTown_Mart_Pokemart:
	pokemartlistend
