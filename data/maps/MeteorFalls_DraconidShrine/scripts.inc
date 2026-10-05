@ Project Grounded: de oude Draconid-schrijn (kaart: tools/grounded/maptools/meteor_falls_ext.py).
@ De Draconid-oudere Selene (Zinnia-lore, Delta Episode): gesprek, gevecht, Draco Plate (één keer).

MeteorFalls_DraconidShrine_MapScripts::
	.byte 0

MeteorFalls_DraconidShrine_EventScript_Elder::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_METEOR_FALLS_ELDER_GIFT, MeteorFalls_DraconidShrine_EventScript_ElderAfter
	goto_if_defeated TRAINER_DRACONID_ELDER, MeteorFalls_DraconidShrine_EventScript_ElderGift
	msgbox MeteorFalls_DraconidShrine_Text_ElderIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_DRACONID_ELDER, MeteorFalls_DraconidShrine_Text_ElderDefeat
MeteorFalls_DraconidShrine_EventScript_ElderGift::
	msgbox MeteorFalls_DraconidShrine_Text_ElderGift, MSGBOX_DEFAULT
	giveitem ITEM_DRACO_PLATE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_METEOR_FALLS_ELDER_GIFT
MeteorFalls_DraconidShrine_EventScript_ElderAfter::
	msgbox MeteorFalls_DraconidShrine_Text_ElderAfter, MSGBOX_DEFAULT
	release
	end

MeteorFalls_DraconidShrine_EventScript_Altar::
	msgbox MeteorFalls_DraconidShrine_Text_Altar, MSGBOX_SIGN
	end

MeteorFalls_DraconidShrine_EventScript_Tablet1::
	msgbox MeteorFalls_DraconidShrine_Text_Tablet1, MSGBOX_SIGN
	end

MeteorFalls_DraconidShrine_EventScript_Tablet2::
	msgbox MeteorFalls_DraconidShrine_Text_Tablet2, MSGBOX_SIGN
	end

MeteorFalls_DraconidShrine_Text_ElderIntro:
	.string "Oh! A visitor. Nobody comes down\n"
	.string "here except Bagon and tax collectors.\p"
	.string "I am Selene, the last Draconid who\n"
	.string "still remembers the old songs.\p"
	.string "Long ago a star fell here. Our people\n"
	.string "prayed to the green dragon in the sky\l"
	.string "to eat the next one before it landed.\p"
	.string "It did. It has been eating them ever\n"
	.string "since. You're welcome, everybody.\p"
	.string "There's a girl, Zinnia. Wild child.\n"
	.string "She left to save the world. She still\l"
	.string "owes me a casserole dish.\p"
	.string "Let's see if your dragons could carry\n"
	.string "the song. Or at least a casserole.$"

MeteorFalls_DraconidShrine_Text_ElderDefeat:
	.string "Ha! My hip went before my Hydreigon\n"
	.string "did. That's a first.$"

MeteorFalls_DraconidShrine_Text_ElderGift:
	.string "Take this. It was carved from the\n"
	.string "first meteor. Probably.\p"
	.string "It might also be a very old cutting\n"
	.string "board. Either way, dragons like it.$"

MeteorFalls_DraconidShrine_Text_ElderAfter:
	.string "If you ever see Zinnia, tell her the\n"
	.string "Draconids forgive her.\p"
	.string "Except for the casserole dish.\n"
	.string "That one is unforgivable.$"

MeteorFalls_DraconidShrine_Text_Altar:
	.string "A meteorite rests on a bed of old\n"
	.string "dragon scales. Offerings lie around it:\l"
	.string "berries, a Poké Ball, a single sock.\p"
	.string "Even a sky dragon has to start\n"
	.string "somewhere.$"

MeteorFalls_DraconidShrine_Text_Tablet1:
	.string "Ancient Draconid carvings: a green\n"
	.string "serpent swallows a falling star.\p"
	.string "Underneath, in newer chalk: “RAYQUAZA\n"
	.string "WAS HERE”, and a rude drawing.$"

MeteorFalls_DraconidShrine_Text_Tablet2:
	.string "“When the sky breaks, the Lorekeeper\n"
	.string "chosen by the dragon shall rise.”\p"
	.string "Next to it: “Lorekeeper wanted. No\n"
	.string "experience required. Unpaid.”$"
