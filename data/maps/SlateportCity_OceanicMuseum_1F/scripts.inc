SlateportCity_OceanicMuseum_1F_MapScripts::
	.byte 0

SlateportCity_OceanicMuseum_1F_EventScript_EntranceAttendant::
	msgbox SlateportCity_OceanicMuseum_1F_Text_PleaseEnjoyYourself, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_PayEntranceFeeLeft::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	goto SlateportCity_OceanicMuseum_1F_EventScript_PayEntranceFee
	end

SlateportCity_OceanicMuseum_1F_EventScript_PayEntranceFeeRight::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	goto SlateportCity_OceanicMuseum_1F_EventScript_PayEntranceFee
	end

SlateportCity_OceanicMuseum_1F_EventScript_PayEntranceFee::
	showmoneybox 0, 0
	msgbox SlateportCity_OceanicMuseum_1F_Text_WouldYouLikeToEnter, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, SlateportCity_OceanicMuseum_1F_EventScript_CheckMoneyForFee
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, SlateportCity_OceanicMuseum_1F_Movement_PushPlayerBackFromCounter
	waitmovement 0
	releaseall
	end

SlateportCity_OceanicMuseum_1F_EventScript_CheckMoneyForFee::
	checkmoney 50
	goto_if_eq VAR_RESULT, FALSE, SlateportCity_OceanicMuseum_1F_EventScript_NotEnoughMoney
	playse SE_SHOP
	removemoney 50
	updatemoneybox
	msgbox SlateportCity_OceanicMuseum_1F_Text_PleaseEnjoyYourself, MSGBOX_DEFAULT
	setvar VAR_SLATEPORT_MUSEUM_1F_STATE, 1
	hidemoneybox
	releaseall
	end

SlateportCity_OceanicMuseum_1F_EventScript_NotEnoughMoney::
	goto_if_unset FLAG_DELIVERED_DEVON_GOODS, SlateportCity_OceanicMuseum_1F_EventScript_AllowEntranceAnyway
	msgbox SlateportCity_OceanicMuseum_1F_Text_NotEnoughMoney, MSGBOX_DEFAULT
	closemessage
	hidemoneybox
	applymovement LOCALID_PLAYER, SlateportCity_OceanicMuseum_1F_Movement_PushPlayerBackFromCounter
	waitmovement 0
	releaseall
	end

SlateportCity_OceanicMuseum_1F_EventScript_AllowEntranceAnyway::
	msgbox SlateportCity_OceanicMuseum_1F_Text_CatchUpWithYourGroup, MSGBOX_DEFAULT
	setvar VAR_SLATEPORT_MUSEUM_1F_STATE, 1
	hidemoneybox
	releaseall
	end

SlateportCity_OceanicMuseum_1F_Movement_PushPlayerBackFromCounter:
	walk_down
	step_end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt1::
	msgbox SlateportCity_OceanicMuseum_1F_Text_AquaExistForGoodOfAll, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt2::
	msgbox SlateportCity_OceanicMuseum_1F_Text_OurBossIsntHere, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt3::
	msgbox SlateportCity_OceanicMuseum_1F_Text_WouldStuffHereMakeMeRich, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt4::
	msgbox SlateportCity_OceanicMuseum_1F_Text_CanLearnForNefariousDeeds, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt5::
	msgbox SlateportCity_OceanicMuseum_1F_Text_RustboroBungled, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumGrunt6::
	msgbox SlateportCity_OceanicMuseum_1F_Text_DidntHaveMoney, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_WhirlpoolExperiment::
	msgbox SlateportCity_OceanicMuseum_1F_Text_WhirlpoolExperiment, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_WaterfallExperiment::
	msgbox SlateportCity_OceanicMuseum_1F_Text_WaterfallExperiment, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_OceanSoilDisplay::
	msgbox SlateportCity_OceanicMuseum_1F_Text_OceanSoilDisplay, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_BeachSandDisplay::
	msgbox SlateportCity_OceanicMuseum_1F_Text_BeachSandDisplay, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_OceanicMinifact1::
	msgbox SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact1, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_OceanicMinifact2::
	msgbox SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact2, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_OceanicMinifact3::
	msgbox SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact3, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_FossilDisplay::
	msgbox SlateportCity_OceanicMuseum_1F_Text_FossilDisplay, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_DepthMeasuringMachine::
	msgbox SlateportCity_OceanicMuseum_1F_Text_DepthMeasuringMachine, MSGBOX_SIGN
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumPatron1::
	msgbox SlateportCity_OceanicMuseum_1F_Text_LearnAboutSeaForBattling, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumPatron2::
	msgbox SlateportCity_OceanicMuseum_1F_Text_SternIsRoleModel, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumPatron3::
	msgbox SlateportCity_OceanicMuseum_1F_Text_MustBePokemonWeDontKnow, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_MuseumPatron4::
	msgbox SlateportCity_OceanicMuseum_1F_Text_WantSeaPokemon, MSGBOX_NPC
	end

SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGrunt::
	lock
	faceplayer
	delay 8
	playse SE_PIN
	applymovement LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT, Common_Movement_Delay48
	waitmovement 0
	msgbox SlateportCity_OceanicMuseum_1F_Text_RememberMeTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_TRICK_ROOM
	goto_if_eq VAR_RESULT, 0, SlateportCity_OceanicMuseum_1F_EventScript_NoRoomForThief
	setflag FLAG_RECEIVED_TM_THIEF
	msgbox SlateportCity_OceanicMuseum_1F_Text_HopeINeverSeeYouAgain, MSGBOX_DEFAULT
	closemessage
	goto_if_eq VAR_FACING, DIR_NORTH, SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitNorth
	goto_if_eq VAR_FACING, DIR_SOUTH, SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitSouth
	goto_if_eq VAR_FACING, DIR_WEST, SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitWestEast
	goto_if_eq VAR_FACING, DIR_EAST, SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitWestEast
	end

SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitNorth::
	applymovement LOCALID_PLAYER, SlateportCity_OceanicMuseum_1F_Movement_PlayerWatchGruntExitNorth
	applymovement LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT, SlateportCity_OceanicMuseum_1F_Movement_FamiliarGruntExitNorth
	waitmovement 0
	goto SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExited
	end

SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitSouth::
	applymovement LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT, SlateportCity_OceanicMuseum_1F_Movement_FamiliarGruntExit
	waitmovement 0
	goto SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExited
	end

SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExitWestEast::
	applymovement LOCALID_PLAYER, SlateportCity_OceanicMuseum_1F_Movement_PlayerWatchGruntExitWestEast
	applymovement LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT, SlateportCity_OceanicMuseum_1F_Movement_FamiliarGruntExit
	waitmovement 0
	goto SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExited
	end

SlateportCity_OceanicMuseum_1F_EventScript_FamiliarGruntExited::
	setflag FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_FAMILIAR_AQUA_GRUNT
	playse SE_EXIT
	removeobject LOCALID_OCEANIC_MUSEUM_FAMILIAR_GRUNT
	release
	end

SlateportCity_OceanicMuseum_1F_EventScript_NoRoomForThief::
	msgbox SlateportCity_OceanicMuseum_1F_Text_YouHaveToTakeThis, MSGBOX_DEFAULT
	release
	end

SlateportCity_OceanicMuseum_1F_Movement_PlayerWatchGruntExitNorth:
	delay_16
	delay_8
	delay_4
	walk_in_place_faster_down
	step_end

SlateportCity_OceanicMuseum_1F_Movement_PlayerWatchGruntExitWestEast:
	delay_16
	walk_in_place_faster_down
	step_end

SlateportCity_OceanicMuseum_1F_Movement_FamiliarGruntExit:
	face_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	delay_8
	step_end

SlateportCity_OceanicMuseum_1F_Movement_FamiliarGruntExitNorth:
	walk_fast_right
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	delay_8
	step_end

SlateportCity_OceanicMuseum_1F_Text_WouldYouLikeToEnter:
	.string "WELCOME to the OCEANIC MUSEUM!!! Oh my\n"
	.string "gosh, a VISITOR! You look amazing\l"
	.string "today, by the way!\p"
	.string "The entrance fee is just ¥50! That's\n"
	.string "nothing for someone as wonderful as\l"
	.string "you! Would you like to enter? Please say\l"
	.string "yes!$"

SlateportCity_OceanicMuseum_1F_Text_PleaseEnjoyYourself:
	.string "THANK YOU! You're my favorite person\n"
	.string "today! Enjoy yourself! I'll be right\l"
	.string "here! Waiting! For you!$"

SlateportCity_OceanicMuseum_1F_Text_NotEnoughMoney:
	.string "Oh no, not enough money? That's okay! I\n"
	.string "still like you! I just can't let you in.\p"
	.string "I'm so sorry. I'm going to cry a little.$"

SlateportCity_OceanicMuseum_1F_Text_CatchUpWithYourGroup:
	.string "Oh? You're with that group in the blue\n"
	.string "bandanas?\p"
	.string "You're late! Better catch up, they\n"
	.string "didn't even pay for tickets!$"

SlateportCity_OceanicMuseum_1F_Text_AquaExistForGoodOfAll:
	.string "We, TEAM AQUA, exist for the good of all!\p"
	.string "And for carbonation.$"

SlateportCity_OceanicMuseum_1F_Text_OurBossIsntHere:
	.string "We were told to assemble here.\p"
	.string "The BOSS isn't here. Probably at the\n"
	.string "tap.$"

SlateportCity_OceanicMuseum_1F_Text_WouldStuffHereMakeMeRich:
	.string "If I stole the stuff here, could I\n"
	.string "afford PERRIER every day?$"

SlateportCity_OceanicMuseum_1F_Text_CanLearnForNefariousDeeds:
	.string "What I learn here, I can use for\n"
	.string "nefarious deeds.\p"
	.string "Like carbonating the ocean.$"

SlateportCity_OceanicMuseum_1F_Text_RustboroBungled:
	.string "If our goons didn't bungle RUSTBORO,\n"
	.string "we'd be at the SPA right now.$"

SlateportCity_OceanicMuseum_1F_Text_DidntHaveMoney:
	.string "I didn't have ¥50.\p"
	.string "I spent it all on SAN PELLEGRINO.$"

SlateportCity_OceanicMuseum_1F_Text_LearnAboutSeaForBattling:
	.string "I want to learn about the sea and use it\n"
	.string "for battling.\p"
	.string "Step one: the sea is wet.$"

SlateportCity_OceanicMuseum_1F_Text_SternIsRoleModel:
	.string "I get all giddy when I see the sea!\p"
	.string "CAPT. STERN is my role model!\p"
	.string "I have his poster. And his trash. Don't\n"
	.string "ask.$"

SlateportCity_OceanicMuseum_1F_Text_MustBePokemonWeDontKnow:
	.string "After the first 251, they're not really\n"
	.string "POKéMON anymore. Just keychains with\l"
	.string "stats.$"

SlateportCity_OceanicMuseum_1F_Text_WantSeaPokemon:
	.string "HYPOCRITE! You have a MIMIKYU plushie\n"
	.string "and a LUCARIO tattoo!$"

SlateportCity_OceanicMuseum_1F_Text_RememberMeTakeThis:
	.string "Aiyeeeh! It's you! The one who thumped\n"
	.string "me!\p"
	.string "Here, take this. Just go away.\p"
	.string "I'm enjoying the water exhibit.$"

SlateportCity_OceanicMuseum_1F_Text_HopeINeverSeeYouAgain:
	.string "TRICK ROOM. Slow POKéMON move first for\n"
	.string "five turns.\p"
	.string "It suits you more than me. Hope I never\n"
	.string "see you again! Wahahaha!$"

SlateportCity_OceanicMuseum_1F_Text_YouHaveToTakeThis:
	.string "Awww, come on! Take it and let me go! I'm\n"
	.string "not even paid for this!$"

SlateportCity_OceanicMuseum_1F_Text_WhirlpoolExperiment:
	.string "A blue fluid is spinning in a glass\n"
	.string "vessel.\p"
	.string "“An experiment to create a WHIRLPOOL\n"
	.string "using wind.”\p"
	.string "Somebody flushed a gummy bear in there.$"

SlateportCity_OceanicMuseum_1F_Text_WaterfallExperiment:
	.string "A red ball is bobbing up and down in a\n"
	.string "glass vessel.\p"
	.string "“An experiment simulating a WATERFALL\n"
	.string "using the ball's buoyancy.”\p"
	.string "It's hypnotizing. You've been staring\n"
	.string "for ten minutes.$"

SlateportCity_OceanicMuseum_1F_Text_OceanSoilDisplay:
	.string "A sample of soil from the ocean floor.\p"
	.string "“Over the years, remains of life-forms\n"
	.string "settle on the seabed, making layers.\p"
	.string "“By studying these layers, we uncover\n"
	.string "the ancient past.”\p"
	.string "So it's dead-stuff lasagna.$"

SlateportCity_OceanicMuseum_1F_Text_BeachSandDisplay:
	.string "A sample of beach sand.\p"
	.string "“Rivers carry stones from the\n"
	.string "mountains, grinding them down.\p"
	.string "“They end up as sand on beaches. And in\n"
	.string "your shoes. Forever.”$"

SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact1:
	.string "“OCEANIC MINIFACT 1: Why is seawater\n"
	.string "blue?\p"
	.string "“Light is made of many colors.\p"
	.string "“In water, most colors fade away.\p"
	.string "“Blue light survives, so the sea looks\n"
	.string "blue. TEAM AQUA says it's because of\l"
	.string "them.”$"

SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact2:
	.string "“OCEANIC MINIFACT 2: Why is the sea\n"
	.string "salty?\p"
	.string "“Seawater contains salt as sodium and\n"
	.string "chlorine ions.\p"
	.string "“Rain washes them out of rocks and\n"
	.string "carries them to sea.\p"
	.string "“Also, WAILORD cries a lot.”$"

SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact3:
	.string "“OCEANIC MINIFACT 3: Which is bigger,\n"
	.string "sea or land?\p"
	.string "“The sea covers about 70% of the\n"
	.string "planet.\p"
	.string "“So the sea is more than twice the size\n"
	.string "of land. TEAM MAGMA has filed a\l"
	.string "complaint.”$"

SlateportCity_OceanicMuseum_1F_Text_FossilDisplay:
	.string "A fossil with wavy ridges on it.\p"
	.string "“The tide scours the soil on the ocean\n"
	.string "floor.\p"
	.string "“Flowing seawater leaves small ridges\n"
	.string "and valleys.\p"
	.string "“When this soil fossilizes, it's called a\n"
	.string "ripple mark.” Riveting.$"

SlateportCity_OceanicMuseum_1F_Text_DepthMeasuringMachine:
	.string "A strange machine spins under a glass\n"
	.string "dome.\p"
	.string "Maybe it measures depth… Or maybe it\n"
	.string "just spins. Respect.$"

