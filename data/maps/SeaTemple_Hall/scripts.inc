@ Project Grounded: de hal van de zeetempel (kopie van SealedChamber_OuterRoom). Je komt boven in de poel.
@ Puzzel: tien gebeeldhouwde stenen; het raadsel (rechtsboven) noemt de volgorde MAAN -> EB -> VLOED.
@ Een verkeerde volgorde zet de teller terug; de andere stenen zijn alleen versiering (en grappen).
@ Opgelost = de deur in de noordwand gaat open (FLAG_SEA_TEMPLE_DOOR_OPEN), naar het heiligdom met Manaphy.
@ Teller: VAR_TEMP_1 (0 = niets, 1 = maan, 2 = maan + eb).
SeaTemple_Hall_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, SeaTemple_Hall_OnResume
	map_script MAP_SCRIPT_ON_LOAD, SeaTemple_Hall_OnLoad
	.byte 0

SeaTemple_Hall_OnResume:
	setdivewarp MAP_UNDERWATER_SEA_TEMPLE, 12, 44
	setescapewarp MAP_UNDERWATER_SEA_TEMPLE, 12, 44
	end

SeaTemple_Hall_OnLoad:
	call_if_unset FLAG_SEA_TEMPLE_DOOR_OPEN, SeaTemple_Hall_EventScript_CloseDoor
	end

SeaTemple_Hall_EventScript_CloseDoor::
	setmetatile 9, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 10, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 11, 1, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 10, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 11, 2, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

SeaTemple_Hall_EventScript_OpenDoor::
	setmetatile 9, 1, METATILE_Cave_SealedChamberEntrance_TopLeft, TRUE
	setmetatile 10, 1, METATILE_Cave_SealedChamberEntrance_TopMid, TRUE
	setmetatile 11, 1, METATILE_Cave_SealedChamberEntrance_TopRight, TRUE
	setmetatile 9, 2, METATILE_Cave_SealedChamberEntrance_BottomLeft, TRUE
	setmetatile 10, 2, METATILE_Cave_SealedChamberEntrance_BottomMid, FALSE
	setmetatile 11, 2, METATILE_Cave_SealedChamberEntrance_BottomRight, TRUE
	special DrawWholeMapView
	return

@ --- de drie stenen van het raadsel ---
SeaTemple_Hall_EventScript_StoneMoon::
	lockall
	goto_if_set FLAG_SEA_TEMPLE_DOOR_OPEN, SeaTemple_Hall_EventScript_StonePressed
	msgbox SeaTemple_Hall_Text_StoneMoon, MSGBOX_DEFAULT
	setvar VAR_TEMP_1, 1
	goto SeaTemple_Hall_EventScript_Clunk

SeaTemple_Hall_EventScript_StoneLowTide::
	lockall
	goto_if_set FLAG_SEA_TEMPLE_DOOR_OPEN, SeaTemple_Hall_EventScript_StonePressed
	msgbox SeaTemple_Hall_Text_StoneLowTide, MSGBOX_DEFAULT
	goto_if_ne VAR_TEMP_1, 1, SeaTemple_Hall_EventScript_Wrong
	setvar VAR_TEMP_1, 2
	goto SeaTemple_Hall_EventScript_Clunk

SeaTemple_Hall_EventScript_StoneHighTide::
	lockall
	goto_if_set FLAG_SEA_TEMPLE_DOOR_OPEN, SeaTemple_Hall_EventScript_StonePressed
	msgbox SeaTemple_Hall_Text_StoneHighTide, MSGBOX_DEFAULT
	goto_if_ne VAR_TEMP_1, 2, SeaTemple_Hall_EventScript_Wrong
	setvar VAR_TEMP_1, 0
	playse SE_PIN
	msgbox SeaTemple_Hall_Text_Clunk, MSGBOX_DEFAULT
	closemessage
	delay 20
	playse SE_BANG
	setflag FLAG_SEA_TEMPLE_DOOR_OPEN
	call SeaTemple_Hall_EventScript_OpenDoor
	waitse
	msgbox SeaTemple_Hall_Text_DoorOpens, MSGBOX_DEFAULT
	releaseall
	end

SeaTemple_Hall_EventScript_Clunk::
	playse SE_PIN
	msgbox SeaTemple_Hall_Text_Clunk, MSGBOX_DEFAULT
	releaseall
	end

SeaTemple_Hall_EventScript_Wrong::
	setvar VAR_TEMP_1, 0
	playse SE_FAILURE
	msgbox SeaTemple_Hall_Text_Wrong, MSGBOX_DEFAULT
	releaseall
	end

SeaTemple_Hall_EventScript_StonePressed::
	msgbox SeaTemple_Hall_Text_StonePressed, MSGBOX_DEFAULT
	releaseall
	end

@ --- versiering ---
SeaTemple_Hall_EventScript_StoneSun::
	msgbox SeaTemple_Hall_Text_StoneSun, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneMagikarp::
	msgbox SeaTemple_Hall_Text_StoneMagikarp, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneWailord::
	msgbox SeaTemple_Hall_Text_StoneWailord, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneStorm::
	msgbox SeaTemple_Hall_Text_StoneStorm, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneRanger::
	msgbox SeaTemple_Hall_Text_StoneRanger, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneRiddle::
	msgbox SeaTemple_Hall_Text_Riddle, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_StoneNotice::
	msgbox SeaTemple_Hall_Text_Notice, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_Door::
	goto_if_set FLAG_SEA_TEMPLE_DOOR_OPEN, SeaTemple_Hall_EventScript_DoorOpen
	msgbox SeaTemple_Hall_Text_DoorClosed, MSGBOX_SIGN
	end

SeaTemple_Hall_EventScript_DoorOpen::
	msgbox SeaTemple_Hall_Text_DoorOpenSign, MSGBOX_SIGN
	end

SeaTemple_Hall_Text_StoneMoon:
	.string "A carving of a full MOON over the\n"
	.string "sea.\p"
	.string "It looks like it could be pushed in.\n"
	.string "You push it in. Of course you do.$"

SeaTemple_Hall_Text_StoneLowTide:
	.string "A carving of the sea pulling back\n"
	.string "from the beach. LOW TIDE.\p"
	.string "A tiny carved Krabby is left behind,\n"
	.string "looking betrayed.\p"
	.string "You push it in.$"

SeaTemple_Hall_Text_StoneHighTide:
	.string "A carving of the sea rushing back up\n"
	.string "the beach. HIGH TIDE.\p"
	.string "The tiny carved Krabby is back. It\n"
	.string "has forgiven nothing.\p"
	.string "You push it in.$"

SeaTemple_Hall_Text_Clunk:
	.string "… … …CLUNK.\n"
	.string "The carving stays in.$"

SeaTemple_Hall_Text_Wrong:
	.string "… … …clunk… … …\p"
	.string "Every carving in the hall slides back\n"
	.string "out at once.\p"
	.string "The temple sighs. You can actually\n"
	.string "hear it sigh.$"

SeaTemple_Hall_Text_DoorOpens:
	.string "Something enormous grinds open to\n"
	.string "the north.\p"
	.string "Somewhere in the walls, a very old\n"
	.string "mechanism says “finally.”$"

SeaTemple_Hall_Text_StonePressed:
	.string "The carving is pushed in all the way.\n"
	.string "It is done being pushed. Respect that.$"

SeaTemple_Hall_Text_StoneSun:
	.string "A carving of the SUN.\p"
	.string "The sea answers to the MOON. The SUN\n"
	.string "can wait in the lobby.$"

SeaTemple_Hall_Text_StoneMagikarp:
	.string "A carving of a MAGIKARP.\p"
	.string "It is the only thing in this temple\n"
	.string "that is level 5.\p"
	.string "It is not a button. It is a tribute.$"

SeaTemple_Hall_Text_StoneWailord:
	.string "A carving of a WAILORD.\p"
	.string "It took up so much of the stone that\n"
	.string "the sculptor had to stop at the eye.\p"
	.string "Wailord: always too much.$"

SeaTemple_Hall_Text_StoneStorm:
	.string "A carving of a storm at sea, with a\n"
	.string "silver shape in the clouds.\p"
	.string "It is very detailed. It has nothing\n"
	.string "to do with this door.$"

SeaTemple_Hall_Text_StoneRanger:
	.string "A carving of a man in shorts holding\n"
	.string "a box with an egg in it.\p"
	.string "Under it: “POKéMON RANGER. WILL COME\n"
	.string "TO COLLECT THE PRINCE.”\p"
	.string "Someone has carved a tally of days\n"
	.string "next to it. The tally covers three\l"
	.string "walls and part of the ceiling.$"

SeaTemple_Hall_Text_Riddle:
	.string "THE PRINCE OF THE SEA SLEEPS WITHIN.\p"
	.string "TO WAKE HIM, DO AS THE SEA DOES:\n"
	.string "FIRST THE MOON RISES,\l"
	.string "THEN THE WATER GOES OUT,\l"
	.string "THEN THE WATER COMES BACK IN.\p"
	.string "DELIVERIES: PLEASE RING.\n"
	.string "(NOBODY HAS EVER RUNG.)$"

SeaTemple_Hall_Text_Notice:
	.string "NOTICE TO VISITORS\p"
	.string "The PRINCE was to be collected by a\n"
	.string "POKéMON RANGER on the agreed date.\p"
	.string "The RANGER has not shown up.\n"
	.string "The agreed date was in 2006.\p"
	.string "If you are the RANGER: we are not\n"
	.string "angry. We are disappointed.$"

SeaTemple_Hall_Text_DoorClosed:
	.string "A heavy stone door. There is no\n"
	.string "handle, no keyhole and no doorbell.\p"
	.string "There is a small sign: “ASK THE\n"
	.string "CARVINGS.”$"

SeaTemple_Hall_Text_DoorOpenSign:
	.string "The door is open. The small sign now\n"
	.string "says: “WELL DONE. WIPE YOUR FEET.”$"
