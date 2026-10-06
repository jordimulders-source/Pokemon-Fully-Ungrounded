@ Project Grounded: Wallace' wijnproeverij (layout van de Contest Hall). Wallace geeft één keer een fles (Berry Juice).
ParadisoResort_WineHall_MapScripts::
	.byte 0

ParadisoResort_WineHall_EventScript_Wallace::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_RESORT_WINE, ParadisoResort_WineHall_EventScript_WallaceAgain
	msgbox ParadisoResort_WineHall_Text_Wallace, MSGBOX_DEFAULT
	giveitem ITEM_BERRY_JUICE, 3
	goto_if_eq VAR_RESULT, FALSE, ParadisoResort_WineHall_EventScript_WallaceBagFull
	setflag FLAG_RECEIVED_RESORT_WINE
	msgbox ParadisoResort_WineHall_Text_WallaceGift, MSGBOX_DEFAULT
	release
	end

ParadisoResort_WineHall_EventScript_WallaceBagFull::
	msgbox ParadisoResort_WineHall_Text_WallaceBagFull, MSGBOX_DEFAULT
	release
	end

ParadisoResort_WineHall_EventScript_WallaceAgain::
	msgbox ParadisoResort_WineHall_Text_WallaceAgain, MSGBOX_DEFAULT
	release
	end

ParadisoResort_WineHall_EventScript_Sommelier::
	msgbox ParadisoResort_WineHall_Text_Sommelier, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Fan1::
	msgbox ParadisoResort_WineHall_Text_Fan1, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Fan2::
	msgbox ParadisoResort_WineHall_Text_Fan2, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Fan3::
	msgbox ParadisoResort_WineHall_Text_Fan3, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Spitter1::
	msgbox ParadisoResort_WineHall_Text_Spitter1, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Spitter2::
	msgbox ParadisoResort_WineHall_Text_Spitter2, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Spitter3::
	msgbox ParadisoResort_WineHall_Text_Spitter3, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Bucket::
	msgbox ParadisoResort_WineHall_Text_Bucket, MSGBOX_SIGN
	end

ParadisoResort_WineHall_EventScript_Drinker1::
	msgbox ParadisoResort_WineHall_Text_Drinker1, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Drinker2::
	msgbox ParadisoResort_WineHall_Text_Drinker2, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Critic::
	msgbox ParadisoResort_WineHall_Text_Critic, MSGBOX_NPC
	end

ParadisoResort_WineHall_EventScript_Lightweight::
	msgbox ParadisoResort_WineHall_Text_Lightweight, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ParadisoResort_WineHall_Text_Wallace:
	.string "WALLACE: Ah, {PLAYER}! You're just in\n"
	.string "time for my new vintage.\p"
	.string "CHÂTEAU MILOTIC, a cheeky little\n"
	.string "red from the cliffs of SOOTOPOLIS.\p"
	.string "Notes of oak, wet stone and the\n"
	.string "faint regret of a MAGIKARP that\l"
	.string "never evolved.\p"
	.string "On the palate: assertive, yet\n"
	.string "vulnerable. Like me in a contest.\p"
	.string "The finish is long. Longer than\n"
	.string "my cape. Here, take some home.$"

ParadisoResort_WineHall_Text_WallaceGift:
	.string "WALLACE: It's labelled BERRY JUICE\n"
	.string "for legal reasons.\p"
	.string "Serve it at room temperature.\n"
	.string "To a POKéMON. Not to children.$"

ParadisoResort_WineHall_Text_WallaceBagFull:
	.string "WALLACE: Your BAG is full?\n"
	.string "Of what? Not wine, clearly.$"

ParadisoResort_WineHall_Text_WallaceAgain:
	.string "WALLACE: Swirl. Sniff. Sip.\n"
	.string "Spit. Repeat.\p"
	.string "The old gentlemen over there\n"
	.string "skipped the middle three.$"

ParadisoResort_WineHall_Text_Sommelier:
	.string "This vintage has a nose of\n"
	.string "cedar, leather and wet DEWGONG.\p"
	.string "I'm the official sommelier.\n"
	.string "I've had nineteen glasses.\l"
	.string "Professionally.$"

ParadisoResort_WineHall_Text_Fan1:
	.string "WALLACE swirled his glass and\n"
	.string "three people fainted.\p"
	.string "I was one of them.\n"
	.string "Best day of my life.$"

ParadisoResort_WineHall_Text_Fan2:
	.string "I don't even like wine.\n"
	.string "I'm here for the cape.\p"
	.string "When he raises his glass,\n"
	.string "the cape does a little flutter.$"

ParadisoResort_WineHall_Text_Fan3:
	.string "He described a wine as 'brooding,\n"
	.string "with a hint of unresolved tension'.\p"
	.string "I cried. I didn't know grapes\n"
	.string "could have feelings.$"

ParadisoResort_WineHall_Text_Spitter1:
	.string "Swirl… sniff… sip…\n"
	.string "PTOOEY!\p"
	.string "Ah. A fine vintage.\n"
	.string "Into the bucket it goes.$"

ParadisoResort_WineHall_Text_Spitter2:
	.string "I've been tasting wine for sixty\n"
	.string "years.\p"
	.string "I have never once swallowed.\n"
	.string "PTOOEY! I don't even know what\l"
	.string "wine tastes like.$"

ParadisoResort_WineHall_Text_Spitter3:
	.string "PTOOEY!\p"
	.string "Sorry, that was my dentures.\n"
	.string "Could you hand me that bucket?$"

ParadisoResort_WineHall_Text_Bucket:
	.string "A spittoon bucket.\p"
	.string "It's nearly full.\n"
	.string "The dentures are on top.$"

ParadisoResort_WineHall_Text_Drinker1:
	.string "I detect blackberry, vanilla and\n"
	.string "a hint of… GRIMER?\p"
	.string "No, that's the man next to me.$"

ParadisoResort_WineHall_Text_Drinker2:
	.string "This is my fourteenth tasting.\n"
	.string "My notes say: 'red'.\p"
	.string "All fourteen. 'Red'.\n"
	.string "I stand by them.$"

ParadisoResort_WineHall_Text_Critic:
	.string "Overpriced. Overdressed.\n"
	.string "Overwhelmingly fabulous.\p"
	.string "Five stars. I hate it.$"

ParadisoResort_WineHall_Text_Lightweight:
	.string "I had one sip. One!\p"
	.string "The ceiling is doing the cha-cha.\n"
	.string "Is the ceiling always this fun?$"
