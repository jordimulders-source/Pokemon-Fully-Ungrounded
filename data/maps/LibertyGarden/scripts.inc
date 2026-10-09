LibertyGarden_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LibertyGarden_OnTransition
	.byte 0

@ Project Grounded: Liberty Garden (Victini), post-game. De Victory-commissaris in de haven van Lilycove geeft na de
@ Hall of Fame de Liberty Pass (uitnodiging); de S.S. Tidal vaart hierheen. Op het eiland staan de vijf
@ Victory-uitdagers op het pad naar de fontein (gauntlet, vaste volgorde, geen heal). Verlaat je het eiland
@ voordat alle vijf verslagen zijn, dan begint de gauntlet opnieuw. Na de vijfde springt Victini van de
@ rechterlantaarn naar de fontein. Kaart en objecten: tools/grounded/maptools/liberty_garden.py.

LibertyGarden_OnTransition:
	setflag FLAG_HIDE_LIBERTY_GARDEN_VICTINI
	goto_if_set FLAG_DEFEATED_LIBERTY_VICTINI, LibertyGarden_EventScript_TransitionEnd
	call VictoryGauntlet_EventScript_CountWins
	goto_if_eq VAR_0x8004, 5, LibertyGarden_EventScript_VictiniWaiting
	cleartrainerflag TRAINER_VICTORY_VANCE
	cleartrainerflag TRAINER_VICTORY_VERNON
	cleartrainerflag TRAINER_VICTORY_VEGA
	cleartrainerflag TRAINER_VICTORY_VESNA
	cleartrainerflag TRAINER_VICTORY_V
LibertyGarden_EventScript_TransitionEnd::
	end

LibertyGarden_EventScript_VictiniWaiting::
	clearflag FLAG_HIDE_LIBERTY_GARDEN_VICTINI
	setobjectxyperm LOCALID_LIBERTY_GARDEN_VICTINI, 14, 7
	end

@ --- gauntlet: overwinningen tellen (VAR_0x8004 = aantal verslagen uitdagers) ---
VictoryGauntlet_EventScript_CountWins::
	setvar VAR_0x8004, 0
	call_if_defeated TRAINER_VICTORY_VANCE, VictoryGauntlet_EventScript_AddWin
	call_if_defeated TRAINER_VICTORY_VERNON, VictoryGauntlet_EventScript_AddWin
	call_if_defeated TRAINER_VICTORY_VEGA, VictoryGauntlet_EventScript_AddWin
	call_if_defeated TRAINER_VICTORY_VESNA, VictoryGauntlet_EventScript_AddWin
	call_if_defeated TRAINER_VICTORY_V, VictoryGauntlet_EventScript_AddWin
	return

VictoryGauntlet_EventScript_AddWin::
	addvar VAR_0x8004, 1
	return

@ --- de Victory-commissaris in de haven van Lilycove ---
VictoryGauntlet_EventScript_Commissioner::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_LIBERTY_PASS, VictoryGauntlet_EventScript_CommissionerAfterPass
	goto_if_unset FLAG_SYS_GAME_CLEAR, VictoryGauntlet_EventScript_CommissionerNotChampion
	msgbox VictoryGauntlet_Text_CommissionerInvite, MSGBOX_DEFAULT
	giveitem ITEM_LIBERTY_PASS
	setflag FLAG_RECEIVED_LIBERTY_PASS
	msgbox VictoryGauntlet_Text_CommissionerAfterGive, MSGBOX_DEFAULT
	release
	end

VictoryGauntlet_EventScript_CommissionerNotChampion::
	msgbox VictoryGauntlet_Text_CommissionerNotChampion, MSGBOX_DEFAULT
	release
	end

VictoryGauntlet_EventScript_CommissionerAfterPass::
	msgbox VictoryGauntlet_Text_CommissionerAfterPass, MSGBOX_DEFAULT
	release
	end

@ --- veerboot: de baliemedewerker in de haven roept dit aan (call); geeft terug bij geen pas of NEE ---
VictoryGauntlet_EventScript_TryFerry::
	checkitem ITEM_LIBERTY_PASS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
	msgbox VictoryGauntlet_Text_FerryAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Common_EventScript_NopReturn
	call LilycoveCity_Harbor_EventScript_BoardFerry
	warp MAP_LIBERTY_GARDEN, 13, 22
	waitstate
	release
	end

@ --- het eiland ---
LibertyGarden_EventScript_Sailor::
	lock
	faceplayer
	msgbox LibertyGarden_Text_SailBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LibertyGarden_EventScript_Stay
	msgbox EventTicket_Text_SailHome, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 30
	hideobjectat LOCALID_LIBERTY_GARDEN_SAILOR, MAP_LIBERTY_GARDEN
	setvar VAR_0x8004, LOCALID_LIBERTY_GARDEN_SS_TIDAL
	call Common_EventScript_FerryDepartIsland
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
	waitstate
	release
	end

LibertyGarden_EventScript_Stay::
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
	release
	end

LibertyGarden_EventScript_Sign::
	msgbox LibertyGarden_Text_Sign, MSGBOX_SIGN
	end

LibertyGarden_EventScript_DockSign::
	msgbox LibertyGarden_Text_DockSign, MSGBOX_SIGN
	end

@ --- de vijf uitdagers, op volgorde langs het pad (Vance..Vesna zien je, V spreek je aan) ---
LibertyGarden_EventScript_Vance::
	trainerbattle_single TRAINER_VICTORY_VANCE, LibertyGarden_Text_VanceIntro, LibertyGarden_Text_VanceDefeat, LibertyGarden_EventScript_AfterWin
	msgbox LibertyGarden_Text_VancePost, MSGBOX_AUTOCLOSE
	end

LibertyGarden_EventScript_Vernon::
	trainerbattle_single TRAINER_VICTORY_VERNON, LibertyGarden_Text_VernonIntro, LibertyGarden_Text_VernonDefeat, LibertyGarden_EventScript_AfterWin
	msgbox LibertyGarden_Text_VernonPost, MSGBOX_AUTOCLOSE
	end

LibertyGarden_EventScript_Vega::
	trainerbattle_single TRAINER_VICTORY_VEGA, LibertyGarden_Text_VegaIntro, LibertyGarden_Text_VegaDefeat, LibertyGarden_EventScript_AfterWin
	msgbox LibertyGarden_Text_VegaPost, MSGBOX_AUTOCLOSE
	end

LibertyGarden_EventScript_Vesna::
	trainerbattle_single TRAINER_VICTORY_VESNA, LibertyGarden_Text_VesnaIntro, LibertyGarden_Text_VesnaDefeat, LibertyGarden_EventScript_AfterWin
	msgbox LibertyGarden_Text_VesnaPost, MSGBOX_AUTOCLOSE
	end

LibertyGarden_EventScript_V::
	trainerbattle_single TRAINER_VICTORY_V, LibertyGarden_Text_VIntro, LibertyGarden_Text_VDefeat, LibertyGarden_EventScript_AfterWin
	msgbox LibertyGarden_Text_VPost, MSGBOX_AUTOCLOSE
	end

LibertyGarden_EventScript_AfterWin::
	call VictoryGauntlet_EventScript_CountWins
	goto_if_eq VAR_0x8004, 5, LibertyGarden_EventScript_VictiniArrives
	release
	end

@ na de vijfde overwinning: Victini verschijnt op de rechterlantaarn en springt naar de fontein
LibertyGarden_EventScript_VictiniArrives::
	lockall
	delay 30
	clearflag FLAG_HIDE_LIBERTY_GARDEN_VICTINI
	addobject LOCALID_LIBERTY_GARDEN_VICTINI
	playmoncry SPECIES_VICTINI, CRY_MODE_NORMAL
	applymovement LOCALID_LIBERTY_GARDEN_VICTINI, LibertyGarden_Movement_VictiniCheer
	waitmovement 0
	waitmoncry
	msgbox LibertyGarden_Text_VictiniAppears, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_LIBERTY_GARDEN_VICTINI, LibertyGarden_Movement_VictiniHops
	waitmovement 0
	setobjectxyperm LOCALID_LIBERTY_GARDEN_VICTINI, 14, 7
	releaseall
	end

LibertyGarden_Movement_VictiniCheer:
	jump_in_place_down
	jump_in_place_down
	step_end

LibertyGarden_Movement_VictiniHops:
	jump_left
	jump_left
	jump_left
	jump_down
	face_down
	step_end

LibertyGarden_EventScript_Victini::
	lock
	faceplayer
	playmoncry SPECIES_VICTINI, CRY_MODE_ENCOUNTER
	msgbox LibertyGarden_Text_Victini, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_VICTINI, 93
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LibertyGarden_EventScript_VictiniStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LibertyGarden_EventScript_VictiniStays
	removeobject LOCALID_LIBERTY_GARDEN_VICTINI
	setflag FLAG_HIDE_LIBERTY_GARDEN_VICTINI
	setflag FLAG_DEFEATED_LIBERTY_VICTINI
LibertyGarden_EventScript_VictiniStays::
	release
	end

VictoryGauntlet_Text_CommissionerNotChampion:
	.string "I'm the VICTORY COMMISSIONER. I hand\n"
	.string "out invitations. To CHAMPIONS.\p"
	.string "You are not a CHAMPION. I checked. I\n"
	.string "have a list.\p"
	.string "It's a short list. You're not on it.\n"
	.string "Neither am I, but I'm the one holding it.$"

VictoryGauntlet_Text_CommissionerInvite:
	.string "A CHAMPION! Finally! I've been standing\n"
	.string "here since the game came out.\p"
	.string "You are hereby invited to the VICTORY\n"
	.string "GAUNTLET on LIBERTY GARDEN.\p"
	.string "Five VICTORY CHALLENGERS. One path.\n"
	.string "One after the other. No breaks, no\l"
	.string "NURSE JOY, no mercy.\p"
	.string "Beat all five and something very small\n"
	.string "and very victorious comes out to say\l"
	.string "hello.\p"
	.string "Lose, or leave the island halfway, and\n"
	.string "the whole thing starts over. Like life,\l"
	.string "but with a ferry.$"

VictoryGauntlet_Text_CommissionerAfterGive:
	.string "Show that to the ferry attendant.\p"
	.string "There used to be a lighthouse on that\n"
	.string "island. We sold it to pay for the\l"
	.string "invitations. They're very nice\l"
	.string "invitations.$"

VictoryGauntlet_Text_CommissionerAfterPass:
	.string "Five challengers, no healing. Pack\n"
	.string "POTIONS. Then pack more POTIONS than\l"
	.string "that.\p"
	.string "The ferry's right there. It's the big\n"
	.string "boat. People miss it anyway.$"

VictoryGauntlet_Text_FerryAsk:
	.string "Oh! A LIBERTY PASS! An actual\n"
	.string "invitation! Nobody ever invites me to\l"
	.string "anything.\p"
	.string "Shall we sail to LIBERTY GARDEN?$"

LibertyGarden_Text_SailBack:
	.string "Had enough victory for one day?\p"
	.string "Heads up: if the GAUNTLET isn't\n"
	.string "finished, they all forget you ever beat\l"
	.string "them. It's in the rules. It's also in\l"
	.string "their personalities.\p"
	.string "Shall we sail back to LILYCOVE?$"

LibertyGarden_Text_Sign:
	.string "LIBERTY GARDEN\p"
	.string "The lighthouse is temporarily two lamp\n"
	.string "posts.\p"
	.string "The lamp on the right is reserved.\n"
	.string "Please don't ask by whom. It gets\l"
	.string "embarrassed.$"

LibertyGarden_Text_DockSign:
	.string "LIBERTY GARDEN - VICTORY GAUNTLET\p"
	.string "Rule 1: Five challengers. One path. Beat\n"
	.string "them in a row.\p"
	.string "Rule 2: Leave the island and the\n"
	.string "GAUNTLET starts over.\p"
	.string "Rule 3: No healing provided. Bring your\n"
	.string "own.\p"
	.string "Rule 4: Please do not feed the VICTORY.$"

LibertyGarden_Text_VictiniAppears:
	.string "Something small just landed on the lamp\n"
	.string "post.\p"
	.string "It looks extremely pleased with itself,\n"
	.string "considering you did all the work.$"

LibertyGarden_Text_Victini:
	.string "Vic-tiii!$"

LibertyGarden_Text_VanceIntro:
	.string "Welcome to LIBERTY GARDEN! I'm the\n"
	.string "welcome committee. Also the first wall.\p"
	.string "I've been sweating on this dock since\n"
	.string "the ferry left. Please stand upwind.\p"
	.string "Victory isn't given. It's sweated for.\n"
	.string "The GAUNTLET starts with me!$"

LibertyGarden_Text_VanceDefeat:
	.string "All that sweat... and the sea was right\n"
	.string "there the whole time.$"

LibertyGarden_Text_VancePost:
	.string "Four more up the path. Nobody heals you\n"
	.string "here.\p"
	.string "Except the sea. The sea heals\n"
	.string "everything eventually. Mostly by\l"
	.string "dissolving it.$"

LibertyGarden_Text_VernonIntro:
	.string "Ah. The one with the invitation. I didn't\n"
	.string "get an invitation. I bought the island.\p"
	.string "Well, a share. This bit of path is legally\n"
	.string "mine. You're trespassing on my victory.\p"
	.string "I bought my last three victories.\n"
	.string "Volume discount. Let's see if yours is\l"
	.string "on sale.$"

LibertyGarden_Text_VernonDefeat:
	.string "Impossible! I paid for this outcome! In\n"
	.string "advance!$"

LibertyGarden_Text_VernonPost:
	.string "You'll be hearing from my lawyer. He's a\n"
	.string "PERSIAN. He bills by the scratch.\p"
	.string "Three more. I hope they're expensive.$"

LibertyGarden_Text_VegaIntro:
	.string "I knew you'd come up this path. I saw it\n"
	.string "in a vision. Also, it's the only path.\p"
	.string "I have seen how this ends. It ends with\n"
	.string "me winning. Spoilers, sorry.\p"
	.string "In my TRICK ROOM, the slow become\n"
	.string "fast... and the fast become sad.$"

LibertyGarden_Text_VegaDefeat:
	.string "...I must have been reading the vision\n"
	.string "upside down.$"

LibertyGarden_Text_VegaPost:
	.string "My crystal ball says you'll beat the\n"
	.string "next two as well.\p"
	.string "It also says “LOW BATTERY”. Make of\n"
	.string "that what you will.$"

LibertyGarden_Text_VesnaIntro:
	.string "Oh. You're still alive. How awkward for\n"
	.string "both of us.\p"
	.string "All my POKéMON are already dead. That's\n"
	.string "not a threat. It's a lifestyle.\p"
	.string "Win or lose, I'm calling this a moral\n"
	.string "victory. I've had six hundred. I'm\l"
	.string "extremely moral.$"

LibertyGarden_Text_VesnaDefeat:
	.string "You won. But at what cost?\p"
	.string "...Oh. No cost. Cool.$"

LibertyGarden_Text_VesnaPost:
	.string "One left. He's by the fountain. He's\n"
	.string "been staring at it since Tuesday.\p"
	.string "I asked him why. He said “V”. That was\n"
	.string "the whole answer.$"

LibertyGarden_Text_VIntro:
	.string "...\p"
	.string "I am V. V for VICTORY. V for VENGEANCE. V\n"
	.string "for... very little imagination.\p"
	.string "Every POKéMON I own starts with a V.\n"
	.string "The rules were my idea.\p"
	.string "I am the last VICTORY CHALLENGER.\n"
	.string "Behind me, a fountain. Above us, a lamp.\l"
	.string "On that lamp, soon... well. Beat me first.$"

LibertyGarden_Text_VDefeat:
	.string "V... for... VANQUISHED.\p"
	.string "I walked right into that one.$"

LibertyGarden_Text_VPost:
	.string "I tried to catch a VICTINI once. It said\n"
	.string "no.\p"
	.string "VICTINI, I mean. Not the letter V. The\n"
	.string "letter V and I are fine.$"
