Underwater_Route124_MapScripts::
	.byte 0


@ Project Grounded: Prof. Birch onder water bij de Clamperl-stront
Underwater_Route124_EventScript_Birch::
	lock
	faceplayer
	goto_if_defeated TRAINER_BIRCH_UNDERWATER, Underwater_Route124_EventScript_BirchPostBattle
	msgbox Underwater_Route124_Text_BirchSnorkel, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BIRCH_UNDERWATER, Underwater_Route124_Text_BirchDefeat
	msgbox Underwater_Route124_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

Underwater_Route124_EventScript_BirchPostBattle::
	msgbox Underwater_Route124_Text_BirchPostBattle, MSGBOX_DEFAULT
	release
	end

Underwater_Route124_EventScript_ClamperlDroppings::
	msgbox Underwater_Route124_Text_ClamperlDroppings, MSGBOX_SIGN
	end

Underwater_Route124_Text_BirchSnorkel:
	.string "BIRCH: Blub! {PLAYER}! Blub!\p"
	.string "Don't mind the snorkel. It's made\n"
	.string "from a WAILORD dropping.\p"
	.string "Hollow, buoyant, and only a little\n"
	.string "bit fragrant. Nature provides.\p"
	.string "I'm down here for the CLAMPERL.\n"
	.string "Everyone wants their pearls.\p"
	.string "Nobody asks what comes out of\n"
	.string "the OTHER end. Until today.\p"
	.string "Blub. Let's battle before my\n"
	.string "snorkel dissolves!$"

Underwater_Route124_Text_BirchDefeat:
	.string "BIRCH: Blub… blub…$"

Underwater_Route124_Text_BirchPostBattle:
	.string "BIRCH: CLAMPERL droppings are\n"
	.string "small, white and round.\p"
	.string "Some jewelers in LILYCOVE are\n"
	.string "going to have a very bad day.$"

Underwater_Route124_Text_ClamperlDroppings:
	.string "Small white pearls in the sand.\n"
	.string "They're not pearls.$"

@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---
Underwater_Route124_EventScript_ZV4Diver::
	msgbox Underwater_Route124_Text_ZV4Diver, MSGBOX_NPC
	end

Underwater_Route124_Text_ZV4Diver:
	.string "(A diver writes on a slate:)\p'THE HOLE UP NORTH GOES TO AN\nISLAND. OR TO A WHIRLPOOL.\pI'VE BEEN SPINNING FOR 3 DAYS.\nIT'S A WHIRLPOOL.'$"
@ --- einde zee_vulling_4 ---
