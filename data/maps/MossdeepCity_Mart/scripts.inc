MossdeepCity_Mart_MapScripts::
	.byte 0

MossdeepCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	badgemart MossdeepCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
MossdeepCity_Mart_Pokemart:
	.2byte ITEM_NET_BALL
	.2byte ITEM_DIVE_BALL
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFENSE
	pokemartlistend

MossdeepCity_Mart_EventScript_Woman::
	msgbox MossdeepCity_Mart_Text_ReviveIsFantastic, MSGBOX_NPC
	end

MossdeepCity_Mart_EventScript_Boy::
	msgbox MossdeepCity_Mart_Text_MaxRepelLastsLongest, MSGBOX_NPC
	end

MossdeepCity_Mart_EventScript_Sailor::
	msgbox MossdeepCity_Mart_Text_NetAndDiveBallsRare, MSGBOX_NPC
	end

MossdeepCity_Mart_Text_ReviveIsFantastic:
	.string "REVIVE is fantastic!\p"
	.string "It brings a fainted POKéMON back.\p"
	.string "Don't ask how. Don't ask where it was.$"

MossdeepCity_Mart_Text_MaxRepelLastsLongest:
	.string "MAX REPEL keeps weak POKéMON away.\p"
	.string "I spray it on my in-laws.$"

MossdeepCity_Mart_Text_NetAndDiveBallsRare:
	.string "NET and DIVE BALLS are made in\n"
	.string "MOSSDEEP.\p"
	.string "The rest of the world doesn't care.$"

