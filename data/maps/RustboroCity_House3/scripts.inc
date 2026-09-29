RustboroCity_House3_MapScripts::
	.byte 0

RustboroCity_House3_EventScript_OldMan::
	msgbox RustboroCity_House3_Text_IGivePerfectlySuitedNicknames, MSGBOX_NPC
	end

RustboroCity_House3_EventScript_OldWoman::
	msgbox RustboroCity_House3_Text_NamingPikachuPekachu, MSGBOX_NPC
	end

@ Misspelling on purpose, see nickname
RustboroCity_House3_EventScript_Pekachu::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
	msgbox RustboroCity_House3_Text_Pekachu, MSGBOX_DEFAULT
	waitmoncry
	release
	end

RustboroCity_House3_Text_IGivePerfectlySuitedNicknames:
	.string "I give my POKéMON perfect nicknames!\p"
	.string "It's my… originality!$"

RustboroCity_House3_Text_NamingPikachuPekachu:
	.string "PEAKYCHU. For a PIKACHU.\p"
	.string "It also looks very pale and its ears are\n"
	.string "down.\p"
	.string "It seems to be popular online, though.$"

RustboroCity_House3_Text_Pekachu:
	.string "PEAKYCHU: Peka…$"

