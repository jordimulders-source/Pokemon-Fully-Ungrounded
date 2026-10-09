SlateportCity_SternsShipyard_1F_MapScripts::
	.byte 0

SlateportCity_SternsShipyard_1F_EventScript_Dock::
	lockall
	goto_if_set FLAG_SYS_GAME_CLEAR, SlateportCity_SternsShipyard_1F_EventScript_FerryReady
	goto_if_set FLAG_BADGE07_GET, SlateportCity_SternsShipyard_1F_EventScript_BrineyJoined
	goto_if_set FLAG_DELIVERED_DEVON_GOODS, SlateportCity_SternsShipyard_1F_EventScript_NeedVeteran
	goto_if_set FLAG_DOCK_REJECTED_DEVON_GOODS, SlateportCity_SternsShipyard_1F_EventScript_GoFindStern
	msgbox SlateportCity_SternsShipyard_1F_Text_CantMakeHeadsOrTails, MSGBOX_DEFAULT
	applymovement LOCALID_DOCK, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_SternsShipyard_1F_Text_MeetDockDeliverToStern, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_DOCK, Common_Movement_FaceOriginalDirection
	waitmovement 0
	setflag FLAG_DOCK_REJECTED_DEVON_GOODS
	setflag FLAG_HIDE_SLATEPORT_CITY_TEAM_AQUA
	releaseall
	end

SlateportCity_SternsShipyard_1F_EventScript_FerryReady::
	applymovement LOCALID_DOCK, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_SternsShipyard_1F_Text_FerryIsReady, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_SternsShipyard_1F_EventScript_BrineyJoined::
	applymovement LOCALID_DOCK, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_SternsShipyard_1F_Text_BrineyJoinedUs, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_SternsShipyard_1F_EventScript_GoFindStern::
	applymovement LOCALID_DOCK, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_SternsShipyard_1F_Text_CouldYouFindStern, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_DOCK, Common_Movement_FaceOriginalDirection
	waitmovement 0
	releaseall
	end

SlateportCity_SternsShipyard_1F_EventScript_NeedVeteran::
	applymovement LOCALID_DOCK, Common_Movement_FacePlayer
	waitmovement 0
	msgbox SlateportCity_SternsShipyard_1F_Text_CouldUseAdviceFromVeteran, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_SternsShipyard_1F_EventScript_Scientist1::
	msgbox SlateportCity_SternsShipyard_1F_Text_SeaIsLikeLivingThing, MSGBOX_NPC
	end

SlateportCity_SternsShipyard_1F_EventScript_Scientist2::
	msgbox SlateportCity_SternsShipyard_1F_Text_GetSeasickEasily, MSGBOX_NPC
	end

SlateportCity_SternsShipyard_1F_EventScript_Briney::
	msgbox SlateportCity_SternsShipyard_1F_Text_DecidedToHelpDock, MSGBOX_NPC
	end

SlateportCity_SternsShipyard_1F_Text_CantMakeHeadsOrTails:
	.string "Umm… This goes here… That goes there…\p"
	.string "Where does this doohickey go?\p"
	.string "We have IKEA instructions for a ferry.$"

SlateportCity_SternsShipyard_1F_Text_MeetDockDeliverToStern:
	.string "Hm? Hi, I'm DOCK. Yes, really. Shipbuilder.\n"
	.string "Named DOCK. Don't.\p"
	.string "CAPT. STERN hired me to design a ferry.\p"
	.string "Oh! Is that… DEVON GOODS?\p"
	.string "Hmm… That's not for me…\p"
	.string "CAPT. STERN went off somewhere. Said he\n"
	.string "had work to do.\p"
	.string "Could you find him and deliver that?$"

SlateportCity_SternsShipyard_1F_Text_CouldYouFindStern:
	.string "DOCK: Where did CAPT. STERN go?\p"
	.string "Could you find him and deliver that\n"
	.string "parcel?$"

SlateportCity_SternsShipyard_1F_Text_CouldUseAdviceFromVeteran:
	.string "DOCK: Shipbuilding is an art.\p"
	.string "Some things you can't just calculate.\p"
	.string "I could really use advice from an old\n"
	.string "sea dog…$"

SlateportCity_SternsShipyard_1F_Text_BrineyJoinedUs:
	.string "DOCK: MR. BRINEY joined us to help out!\p"
	.string "Thanks to him, the ferry is coming\n"
	.string "together. He also taught me eleven new\l"
	.string "swear words.$"

SlateportCity_SternsShipyard_1F_Text_FerryIsReady:
	.string "DOCK: The ferry is finally ready!\p"
	.string "The S.S. TIDAL is a marvel of\n"
	.string "technology!\p"
	.string "But I feel like we can build something\n"
	.string "even better.\p"
	.string "Technology never stops. Neither do I. I\n"
	.string "haven't slept in four days.$"

SlateportCity_SternsShipyard_1F_Text_DecidedToHelpDock:
	.string "MR. BRINEY: Ah, {PLAYER}{KUN}! It's been too\n"
	.string "long!\p"
	.string "Aye, since I met you, this old sea dog's\n"
	.string "been feeling frisky!\p"
	.string "So I'm helping DOCK build a ferry.\p"
	.string "A ferry carries lots of people. More\n"
	.string "people, more stories!\p"
	.string "That DOCK is something special.\p"
	.string "With his brains and my experience, we'll\n"
	.string "build one great ship, aye!$"

SlateportCity_SternsShipyard_1F_Text_SeaIsLikeLivingThing:
	.string "Seasons, weather, the moon…\p"
	.string "The sea changes its mood constantly.\p"
	.string "The sea is like my ex.$"

SlateportCity_SternsShipyard_1F_Text_GetSeasickEasily:
	.string "I get seasick easily.\p"
	.string "So I build ships. On land. Far from the\n"
	.string "sea.$"


@ Project Grounded: Meltan als gift (swords_keldeo.py zet de objecten). Rivet de lasser is zijn moeren kwijt aan
@ een Meltan en wil ervan af. Meltan evolueert in Melmetal door te levelen met een Metal Coat (Lilycove Dept. Store 2F).
SlateportCity_SternsShipyard_1F_EventScript_Rivet::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_MELTAN, SlateportCity_SternsShipyard_1F_EventScript_RivetAfter
	msgbox SlateportCity_SternsShipyard_1F_Text_RivetOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SlateportCity_SternsShipyard_1F_EventScript_RivetDecline
	givemon SPECIES_MELTAN, 12
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, Common_EventScript_NoMoreRoomForPokemon
	removeobject LOCALID_SHIPYARD_MELTAN
	setflag FLAG_RECEIVED_MELTAN
	playfanfare MUS_OBTAIN_ITEM
	message SlateportCity_SternsShipyard_1F_Text_ReceivedMeltan
	waitmessage
	waitfanfare
	msgbox SlateportCity_SternsShipyard_1F_Text_RivetThanks, MSGBOX_DEFAULT
	release
	end

SlateportCity_SternsShipyard_1F_EventScript_RivetDecline::
	msgbox SlateportCity_SternsShipyard_1F_Text_RivetDecline, MSGBOX_DEFAULT
	release
	end

SlateportCity_SternsShipyard_1F_EventScript_RivetAfter::
	msgbox SlateportCity_SternsShipyard_1F_Text_RivetAfter, MSGBOX_DEFAULT
	release
	end

SlateportCity_SternsShipyard_1F_EventScript_Meltan::
	lock
	playmoncry SPECIES_MELTAN, CRY_MODE_NORMAL
	msgbox SlateportCity_SternsShipyard_1F_Text_Meltan, MSGBOX_DEFAULT
	waitmoncry
	release
	end

SlateportCity_SternsShipyard_1F_Text_RivetOffer:
	.string "RIVET: This little nut showed up\n"
	.string "last week. It eats nuts. Bolts too.\p"
	.string "Yesterday it ate half a forklift.\n"
	.string "The half that was important.\p"
	.string "CAPT. STERN says it's “a rare\n"
	.string "mythical POKéMON.” I say it's a\l"
	.string "rare mythical invoice.\p"
	.string "You want it? Please want it.$"

SlateportCity_SternsShipyard_1F_Text_ReceivedMeltan:
	.string "{PLAYER} received MELTAN!\n"
	.string "It is already chewing on your bag.$"

SlateportCity_SternsShipyard_1F_Text_RivetThanks:
	.string "RIVET: Free at last!\p"
	.string "Word of advice: let it hold a METAL\n"
	.string "COAT when it levels up. Then it\l"
	.string "turns into something enormous.\p"
	.string "The DEPARTMENT STORE in LILYCOVE\n"
	.string "sells them. Not my shipyard anymore.\l"
	.string "Not my problem anymore.$"

SlateportCity_SternsShipyard_1F_Text_RivetDecline:
	.string "RIVET: Sure. Take your time.\n"
	.string "It's not like it's eating the ship.\p"
	.string "… … …It's eating the ship.$"

SlateportCity_SternsShipyard_1F_Text_RivetAfter:
	.string "RIVET: My toolbox is quiet again.\n"
	.string "I miss the screaming hinges.\p"
	.string "No I don't.$"

SlateportCity_SternsShipyard_1F_Text_Meltan:
	.string "MELTAN is gnawing on RIVET's wrench\n"
	.string "with total commitment.$"
