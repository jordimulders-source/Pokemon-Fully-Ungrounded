@ Project Grounded: Yoshi's Island, de heuvels (tools/grounded/maptools/yoshis_island.py)
YoshisIsland_Hills_MapScripts::
	.byte 0

YoshisIsland_Hills_EventScript_Yoshi::
	lock
	faceplayer
	goto_if_unset FLAG_YI_CAMP_A, YoshisIsland_Hills_EventScript_YoshiCamp
	goto_if_unset FLAG_YI_CAMP_B, YoshisIsland_Hills_EventScript_YoshiPass
	goto_if_unset FLAG_YI_BOO_DONE, YoshisIsland_Hills_EventScript_YoshiBoo
	msgbox YoshisIsland_Hills_Text_YoshiFort, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_YoshiCamp::
	msgbox YoshisIsland_Hills_Text_YoshiCamp, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_YoshiPass::
	msgbox YoshisIsland_Hills_Text_YoshiPass, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_YoshiBoo::
	msgbox YoshisIsland_Hills_Text_YoshiBoo, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_CampA::
	lock
	faceplayer
	goto YoshisIsland_Hills_EventScript_CampABattle

YoshisIsland_Hills_EventScript_CampAWon::
	msgbox YoshisIsland_Hills_Text_CampAWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_CAMP_A1
	removeobject LOCALID_YI_CAMP_A2
	setflag FLAG_YI_CAMP_A
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

YoshisIsland_Hills_EventScript_CampB::
	lock
	faceplayer
	goto_if_unset FLAG_YI_CAMP_A, YoshisIsland_Hills_EventScript_CampBWait
	goto YoshisIsland_Hills_EventScript_CampBBattle

YoshisIsland_Hills_EventScript_CampBWait::
	msgbox YoshisIsland_Hills_Text_CampBWait, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_CampBWon::
	msgbox YoshisIsland_Hills_Text_CampBWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_CAMP_B1
	removeobject LOCALID_YI_CAMP_B2
	setflag FLAG_YI_CAMP_B
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

YoshisIsland_Hills_EventScript_GateGuard::
	msgbox YoshisIsland_Hills_Text_GateGuard, MSGBOX_NPC
	end

YoshisIsland_Hills_EventScript_Pecharunt::
	lock
	faceplayer
	goto_if_set FLAG_YI_WARIO_DONE, YoshisIsland_Hills_EventScript_PecharuntBattle
	msgbox YoshisIsland_Hills_Text_PecharuntShop, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_PecharuntBattle::
	playmoncry SPECIES_PECHARUNT, CRY_MODE_ENCOUNTER
	msgbox YoshisIsland_Hills_Text_PecharuntBattle, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_PECHARUNT, 92
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, YoshisIsland_Hills_EventScript_PecharuntCaught
	msgbox YoshisIsland_Hills_Text_PecharuntEscaped, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_PecharuntCaught::
	removeobject LOCALID_YI_PECHARUNT
	setflag FLAG_YI_PECHARUNT_DONE
	msgbox YoshisIsland_Hills_Text_PecharuntCaught, MSGBOX_DEFAULT
	release
	end

YoshisIsland_Hills_EventScript_CampABattle::
	msgbox YoshisIsland_Hills_Text_CampAIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_Hills_EventScript_CampAChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_Hills_EventScript_CampAFight
	special LoadPlayerParty
	goto YoshisIsland_Hills_EventScript_CampAChoose

YoshisIsland_Hills_EventScript_CampAFight::
	multi_2_vs_2 TRAINER_YI_SHY_GUY_CAMP_A1, YoshisIsland_Hills_Text_CampADefeatA, TRAINER_YI_SHY_GUY_CAMP_A2, YoshisIsland_Hills_Text_CampADefeatB, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_Hills_EventScript_CampAWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_Hills_EventScript_CampBBattle::
	msgbox YoshisIsland_Hills_Text_CampBIntro, MSGBOX_DEFAULT
	closemessage
YoshisIsland_Hills_EventScript_CampBChoose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, YoshisIsland_Hills_EventScript_CampBFight
	special LoadPlayerParty
	goto YoshisIsland_Hills_EventScript_CampBChoose

YoshisIsland_Hills_EventScript_CampBFight::
	multi_2_vs_2 TRAINER_YI_SHY_GUY_CAMP_B1, YoshisIsland_Hills_Text_CampBDefeatA, TRAINER_YI_SHY_GUY_CAMP_B2, YoshisIsland_Hills_Text_CampBDefeatB, PARTNER_YOSHI
	switch VAR_RESULT
	case 1, YoshisIsland_Hills_EventScript_CampBWon
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

YoshisIsland_Hills_EventScript_Sign::
	msgbox YoshisIsland_Hills_Text_Sign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
YoshisIsland_Hills_Text_YoshiCamp:
	.string "YOSHI: Yoshi yoshi!\p"
	.string "(The SHY GUY camp is east. The two by\n"
	.string "the campfire are in charge of the\l"
	.string "snacks, which makes them the most\l"
	.string "dangerous ones.)$"

YoshisIsland_Hills_Text_YoshiPass:
	.string "YOSHI: Yoshi!\p"
	.string "(Two more are guarding the path west,\n"
	.string "to the haunted house. Something in\l"
	.string "there giggles at night. YOSHI does not\l"
	.string "like giggling he did not start.)$"

YoshisIsland_Hills_Text_YoshiBoo:
	.string "YOSHI: Yoshi... yoshi.\p"
	.string "(The haunted house. COMMANDER BOO\n"
	.string "lives there. YOSHI is being very brave\l"
	.string "about it, from back here.)$"

YoshisIsland_Hills_Text_YoshiFort:
	.string "YOSHI: YOSHI!\p"
	.string "(The fort's door is open. Whoever is\n"
	.string "behind all this smells strongly of\l"
	.string "garlic. YOSHI has a theory. The theory\l"
	.string "is wearing yellow.)$"

YoshisIsland_Hills_Text_CampAWon:
	.string "(The SHY GUYS drop a sack of stolen\n"
	.string "eggs, a stolen flag and, for some\l"
	.string "reason, a stolen sense of direction.\l"
	.string "They run off to file a complaint with\l"
	.string "management.)$"

YoshisIsland_Hills_Text_CampBWait:
	.string "(The SHY GUYS cross their arms and\n"
	.string "point east, at the camp. Apparently you\l"
	.string "need to be beaten up by the camp first.\l"
	.string "It's policy.)$"

YoshisIsland_Hills_Text_CampBWon:
	.string "(The SHY GUYS step aside and bow. Then\n"
	.string "they keep bowing, to be safe, until you\l"
	.string "are out of sight.)$"

YoshisIsland_Hills_Text_GateGuard:
	.string "(A SHY GUY in a black cloak holds up a\n"
	.string "sign: MEMBERS ONLY. On the back, in\l"
	.string "smaller letters: MEMBERSHIP = BEING\l"
	.string "COMMANDER BOO. You are, sadly, not\l"
	.string "COMMANDER BOO.)$"

YoshisIsland_Hills_Text_PecharuntShop:
	.string "PECHARUNT: Mochi? Mochi! One for you,\n"
	.string "one for the nice SHY GUYS, a whole crate\l"
	.string "for the big man in the fort. He pays in\l"
	.string "gold. Gold is chewy too.\p"
	.string "(The mochi glisten. They smell like\n"
	.string "obedience and strawberries. You\l"
	.string "politely decline.)$"

YoshisIsland_Hills_Text_PecharuntBattle:
	.string "PECHARUNT: The big man stopped buying.\n"
	.string "The SHY GUYS stopped obeying. Business\l"
	.string "is terrible.\p"
	.string "PECHARUNT: ...unless YOU would like to be\n"
	.string "my new best customer!$"

YoshisIsland_Hills_Text_PecharuntEscaped:
	.string "(PECHARUNT has rolled back behind the\n"
	.string "counter, rearranging mochi. He will be\l"
	.string "here all week.)$"

YoshisIsland_Hills_Text_PecharuntCaught:
	.string "(The mochi stall is empty. A little sign\n"
	.string "reads: CLOSED FOR GOOD. UNDER NEW\l"
	.string "MANAGEMENT. The new management is\l"
	.string "you.)$"

YoshisIsland_Hills_Text_CampAIntro:
	.string "(A FLY GUY and a SHADY GUY are roasting\n"
	.string "a stolen Yoshi egg over the fire. Well.\l"
	.string "Warming it. Very gently. They look at\l"
	.string "you like you interrupted a ritual.)\p"
	.string "YOSHI: YOSHI!!$"

YoshisIsland_Hills_Text_CampADefeatA:
	.string "(The FLY GUY's propeller slows to a sad\n"
	.string "little spin.)$"

YoshisIsland_Hills_Text_CampADefeatB:
	.string "(The SHADY GUY tries to pickpocket you\n"
	.string "on his way down. He gets a receipt.)$"

YoshisIsland_Hills_Text_CampBIntro:
	.string "(A SPEAR GUY and a SNIFIT block the\n"
	.string "path to the haunted house. The SNIFIT\l"
	.string "inhales. It is a very threatening\l"
	.string "inhale.)\p"
	.string "YOSHI: Yoshi!$"

YoshisIsland_Hills_Text_CampBDefeatA:
	.string "(The SPEAR GUY's spear droops. He was\n"
	.string "compensating.)$"

YoshisIsland_Hills_Text_CampBDefeatB:
	.string "(The SNIFIT exhales. That was the whole\n"
	.string "plan.)$"

YoshisIsland_Hills_Text_Sign:
	.string "SHY GUY CAMP\n"
	.string "Trespassers will be stared at.\l"
	.string "Unmasking is strictly forbidden.\l"
	.string "(Mostly because we lost the\l"
	.string "instructions.)$"
