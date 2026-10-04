@ Project Grounded: Kubfu-dojo van meester Mustard (Route 112, langs het Mt. Chimney-pad).
@ Je krijgt Kubfu; boven zijn twee torens. Wie de Tower of Darkness voltooit krijgt Urshifu Single Strike,
@ wie de Tower of Waters voltooit Urshifu Rapid Strike (Grounded_EvolveKubfu). Daarna kun je Mustard zelf uitdagen.
Route112_Dojo_MapScripts::
	.byte 0

Route112_Dojo_EventScript_Mustard::
	lock
	faceplayer
	goto_if_set FLAG_KUBFU_EVOLVED, Route112_Dojo_EventScript_MustardChallenge
	goto_if_set FLAG_RECEIVED_KUBFU, Route112_Dojo_EventScript_MustardHint
	msgbox Route112_Dojo_Text_MustardIntro, MSGBOX_DEFAULT
	givemon SPECIES_KUBFU, 22
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Route112_Dojo_EventScript_KubfuReceived
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Route112_Dojo_EventScript_KubfuToPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Route112_Dojo_EventScript_KubfuReceived::
	call Route112_Dojo_EventScript_KubfuFanfare
	goto Route112_Dojo_EventScript_ExplainTowers
	end

Route112_Dojo_EventScript_KubfuToPC::
	call Route112_Dojo_EventScript_KubfuFanfare
	call Common_EventScript_TransferredToPC
	goto Route112_Dojo_EventScript_ExplainTowers
	end

Route112_Dojo_EventScript_KubfuFanfare::
	setflag FLAG_RECEIVED_KUBFU
	bufferspeciesname STR_VAR_2, SPECIES_KUBFU
	playfanfare MUS_OBTAIN_ITEM
	message Route112_Dojo_Text_ReceivedKubfu
	waitmessage
	waitfanfare
	return

Route112_Dojo_EventScript_ExplainTowers::
	msgbox Route112_Dojo_Text_ExplainTowers, MSGBOX_DEFAULT
	release
	end

Route112_Dojo_EventScript_MustardHint::
	msgbox Route112_Dojo_Text_MustardHint, MSGBOX_DEFAULT
	release
	end

Route112_Dojo_EventScript_MustardChallenge::
	goto_if_defeated TRAINER_MUSTARD, Route112_Dojo_EventScript_MustardDefeated
	msgbox Route112_Dojo_Text_MustardChallenge, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route112_Dojo_EventScript_MustardDeclined
	trainerbattle_no_intro TRAINER_MUSTARD, Route112_Dojo_Text_MustardDefeat
	msgbox Route112_Dojo_Text_MustardPostBattle, MSGBOX_DEFAULT
	release
	end

Route112_Dojo_EventScript_MustardDeclined::
	msgbox Route112_Dojo_Text_MustardDeclined, MSGBOX_DEFAULT
	release
	end

Route112_Dojo_EventScript_MustardDefeated::
	msgbox Route112_Dojo_Text_MustardPostBattle, MSGBOX_DEFAULT
	release
	end

Route112_Dojo_EventScript_Student::
	msgbox Route112_Dojo_Text_Student, MSGBOX_NPC
	end

Route112_Dojo_EventScript_Student2::
	msgbox Route112_Dojo_Text_Student2, MSGBOX_NPC
	end

Route112_Dojo_Text_MustardIntro:
	.string "Oh ho ho! A visitor! Nobody visits. The\n"
	.string "entrance is a hole in a rock.\p"
	.string "I am MUSTARD. Former champion, current\n"
	.string "pensioner, master of the hole in the\l"
	.string "rock.\p"
	.string "Here, take this little one. It eats my\n"
	.string "slippers. And my pension.$"

Route112_Dojo_Text_ReceivedKubfu:
	.string "{PLAYER} received a {STR_VAR_2}!$"

Route112_Dojo_Text_ExplainTowers:
	.string "That KUBFU wants to grow up, but can't\n"
	.string "decide what kind of adult to be. Very\l"
	.string "Gen Z.\p"
	.string "Upstairs are two towers. Both upstairs.\n"
	.string "Don't ask about the architecture.\p"
	.string "Left: the TOWER OF DARKNESS. One\n"
	.string "strike, big hurt.\p"
	.string "Right: the TOWER OF WATERS. Many\n"
	.string "strikes, many small hurts.\p"
	.string "Beat the keeper at the top with KUBFU\n"
	.string "in your team, and it picks a path.\l"
	.string "Forever. No refunds.$"

Route112_Dojo_Text_MustardHint:
	.string "Left stairs: DARKNESS. Single Strike.\n"
	.string "Right stairs: WATERS. Rapid Strike.\p"
	.string "Bring KUBFU, or the keepers will just\n"
	.string "beat you up for free.$"

Route112_Dojo_Text_MustardChallenge:
	.string "Oh ho! It evolved! I'm so proud I could\n"
	.string "cry. I'm already crying.\p"
	.string "Now show this old man what you two\n"
	.string "learned. Don't worry, my hip is insured.$"

Route112_Dojo_Text_MustardDeclined:
	.string "Wise. My back hurts anyway.$"

Route112_Dojo_Text_MustardDefeat:
	.string "Oh ho ho! Beaten by my own slipper\n"
	.string "thief! Retirement suits me after all.$"

Route112_Dojo_Text_MustardPostBattle:
	.string "Go on, take on the world.\p"
	.string "And if anyone asks where you learned\n"
	.string "that, say a hole in a rock.$"

Route112_Dojo_Text_Student:
	.string "I've been training here for twelve\n"
	.string "years. I haven't evolved once.\p"
	.string "The master says it's a mindset thing. I\n"
	.string "think it's because I'm human.$"

Route112_Dojo_Text_Student2:
	.string "The master made me paint his fence for\n"
	.string "three years. Wax on, wax off.\p"
	.string "I still can't fight. But that fence\n"
	.string "looks amazing.$"
