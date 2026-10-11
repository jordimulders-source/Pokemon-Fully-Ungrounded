@ Project Grounded: PARADISO RESORT, zandeiland ten zuiden van Route 129 (ZEE_PLAN.md). Kaart:
@ tools/grounded/maptools/paradiso_resort.py. Gasten vechten pas na de Hall of Fame. Teksten zijn placeholders.
ParadisoResort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ParadisoResort_OnTransition
	.byte 0

ParadisoResort_OnTransition:
	call ParadisoResort_EventScript_SetRivalGfx
	setflag FLAG_TEMP_1 @ rivaal: pas hier na gevecht 8 bij de Battle Tower (met pensioen)
	call_if_set FLAG_RIVAL_PG_RETIRED, ParadisoResort_EventScript_ShowRival
	setflag FLAG_HIDE_RESORT_RIVAL @ Dave (naam historisch: deelde vroeger de flag met de rivaal)
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_EventScript_End
	clearflag FLAG_HIDE_RESORT_RIVAL
ParadisoResort_EventScript_End:
	end

ParadisoResort_EventScript_ShowRival::
	clearflag FLAG_TEMP_1
	return

ParadisoResort_EventScript_SetRivalGfx::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, ParadisoResort_EventScript_RivalMay
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	return

ParadisoResort_EventScript_RivalMay::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

@ ---------------------------------------------------------------- gasten met een gevecht (post-game)
ParadisoResort_EventScript_Misty::
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_EventScript_MistyNotYet
	goto_if_defeated TRAINER_RESORT_MISTY, ParadisoResort_EventScript_MistyPost
	lock
	faceplayer
	msgbox ParadisoResort_Text_MistyAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_EventScript_MistyDecline
	trainerbattle_single TRAINER_RESORT_MISTY, ParadisoResort_Text_MistyIntro, ParadisoResort_Text_MistyDefeat
ParadisoResort_EventScript_MistyPost::
	msgbox ParadisoResort_Text_MistyPost, MSGBOX_AUTOCLOSE
	end

ParadisoResort_EventScript_MistyDecline::
	msgbox ParadisoResort_Text_MistyDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_MistyNotYet::
	msgbox ParadisoResort_Text_MistyNotYet, MSGBOX_NPC
	end

ParadisoResort_EventScript_Erika::
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_EventScript_ErikaNotYet
	goto_if_defeated TRAINER_RESORT_ERIKA, ParadisoResort_EventScript_ErikaPost
	lock
	faceplayer
	msgbox ParadisoResort_Text_ErikaAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_EventScript_ErikaDecline
	trainerbattle_single TRAINER_RESORT_ERIKA, ParadisoResort_Text_ErikaIntro, ParadisoResort_Text_ErikaDefeat
ParadisoResort_EventScript_ErikaPost::
	msgbox ParadisoResort_Text_ErikaPost, MSGBOX_AUTOCLOSE
	end

ParadisoResort_EventScript_ErikaDecline::
	msgbox ParadisoResort_Text_ErikaDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_ErikaNotYet::
	msgbox ParadisoResort_Text_ErikaNotYet, MSGBOX_NPC
	end

ParadisoResort_EventScript_Birch::
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_EventScript_BirchNotYet
	goto_if_defeated TRAINER_BIRCH_RESORT, ParadisoResort_EventScript_BirchPost
	lock
	faceplayer
	msgbox ParadisoResort_Text_BirchAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_EventScript_BirchDecline
	trainerbattle_single TRAINER_BIRCH_RESORT, ParadisoResort_Text_BirchIntro, ParadisoResort_Text_BirchDefeat
ParadisoResort_EventScript_BirchPost::
	msgbox ParadisoResort_Text_BirchPost, MSGBOX_AUTOCLOSE
	end

ParadisoResort_EventScript_BirchDecline::
	msgbox ParadisoResort_Text_BirchDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_BirchNotYet::
	msgbox ParadisoResort_Text_BirchNotYet, MSGBOX_NPC
	end

ParadisoResort_EventScript_Turd::
	msgbox ParadisoResort_Text_Turd, MSGBOX_SIGN
	end

@ Project Grounded: de rivaal met pensioen (na gevecht 8, FLAG_RIVAL_PG_RETIRED). Eén gevecht per dag
@ (FLAG_DAILY_REMATCH_RIVAL) tegen het Frontier-team (TRAINER_RIVAL_POSTGAME_*, fase 2 in rival_postgame.c).
ParadisoResort_EventScript_Rival::
	lock
	faceplayer
	goto_if_set FLAG_RIVAL_PG_RESORT_MET, ParadisoResort_EventScript_RivalAgain
	setflag FLAG_RIVAL_PG_RESORT_MET
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, ParadisoResort_EventScript_RivalMayTalk
	msgbox ParadisoResort_Text_RivalBrendan, MSGBOX_DEFAULT
	goto ParadisoResort_EventScript_RivalAsk
	end

ParadisoResort_EventScript_RivalMayTalk::
	msgbox ParadisoResort_Text_RivalMay, MSGBOX_DEFAULT
	goto ParadisoResort_EventScript_RivalAsk
	end

ParadisoResort_EventScript_RivalAgain::
	goto_if_set FLAG_DAILY_REMATCH_RIVAL, ParadisoResort_EventScript_RivalDoneToday
	msgbox ParadisoResort_Text_RivalAgain, MSGBOX_DEFAULT
ParadisoResort_EventScript_RivalAsk::
	goto_if_set FLAG_DAILY_REMATCH_RIVAL, ParadisoResort_EventScript_RivalDoneToday
	msgbox ParadisoResort_Text_RivalAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_EventScript_RivalDecline
	closemessage
	switch VAR_STARTER_MON
	case 0, ParadisoResort_EventScript_RivalTreecko
	case 1, ParadisoResort_EventScript_RivalTorchic
	case 2, ParadisoResort_EventScript_RivalMudkip
	release
	end

ParadisoResort_EventScript_RivalTreecko::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TREECKO, ParadisoResort_Text_RivalDefeat
	goto ParadisoResort_EventScript_RivalAfter
	end

ParadisoResort_EventScript_RivalTorchic::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_TORCHIC, ParadisoResort_Text_RivalDefeat
	goto ParadisoResort_EventScript_RivalAfter
	end

ParadisoResort_EventScript_RivalMudkip::
	trainerbattle_no_intro TRAINER_RIVAL_POSTGAME_MUDKIP, ParadisoResort_Text_RivalDefeat
	goto ParadisoResort_EventScript_RivalAfter
	end

ParadisoResort_EventScript_RivalAfter::
	setflag FLAG_DAILY_REMATCH_RIVAL
	msgbox ParadisoResort_Text_RivalPostBattle, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_RivalDecline::
	msgbox ParadisoResort_Text_RivalDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_RivalDoneToday::
	msgbox ParadisoResort_Text_RivalDoneToday, MSGBOX_DEFAULT
	release
	end

@ ---------------------------------------------------------------- overige gasten
@ Dave (Freed From Desire) na de Hall of Fame: met pensioen (tekst letterlijk van Jordi), maar één comeback-gevecht
@ op lv 100 (TRAINER_DAVE_PARADISO, eenmalig via de trainerflag).
ParadisoResort_EventScript_Dave::
	lock
	faceplayer
	goto_if_defeated TRAINER_DAVE_PARADISO, ParadisoResort_EventScript_DaveRetired
	msgbox ParadisoResort_Text_Dave, MSGBOX_DEFAULT
	msgbox ParadisoResort_Text_DaveComeback, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_DAVE_PARADISO, ParadisoResort_Text_DaveDefeat
	msgbox ParadisoResort_Text_DavePostBattle, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_DaveRetired::
	msgbox ParadisoResort_Text_DaveRetired, MSGBOX_DEFAULT
	release
	end

ParadisoResort_EventScript_PoolSwimmer::
	msgbox ParadisoResort_Text_PoolSwimmer, MSGBOX_NPC
	end

ParadisoResort_EventScript_Lifeguard::
	msgbox ParadisoResort_Text_Lifeguard, MSGBOX_NPC
	end

ParadisoResort_EventScript_DrunkHiker::
	msgbox ParadisoResort_Text_DrunkHiker, MSGBOX_NPC
	end

ParadisoResort_EventScript_DrunkBeauty::
	msgbox ParadisoResort_Text_DrunkBeauty, MSGBOX_NPC
	end

ParadisoResort_EventScript_DrunkFatMan::
	msgbox ParadisoResort_Text_DrunkFatMan, MSGBOX_NPC
	end

ParadisoResort_EventScript_DrunkFan::
	msgbox ParadisoResort_Text_DrunkFan, MSGBOX_NPC
	end

ParadisoResort_EventScript_Sunburn::
	msgbox ParadisoResort_Text_Sunburn, MSGBOX_NPC
	end

ParadisoResort_EventScript_Collector::
	msgbox ParadisoResort_Text_Collector, MSGBOX_NPC
	end

ParadisoResort_EventScript_Sign::
	msgbox ParadisoResort_Text_Sign, MSGBOX_SIGN
	end

ParadisoResort_EventScript_PoolSign::
	msgbox ParadisoResort_Text_PoolSign, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ParadisoResort_Text_Sign:
	.string "PARADISO RESORT\n"
	.string "All-inclusive. Including regret.$"

ParadisoResort_Text_PoolSign:
	.string "INFINITY POOL\p"
	.string "It's the sea. We put a sign next\n"
	.string "to it. That's the whole renovation.$"

ParadisoResort_Text_MistyNotYet:
	.string "MISTY: I'm on vacation. Don't talk\n"
	.string "to me about gyms, badges or bikes.\p"
	.string "Come back when you're CHAMPION.\n"
	.string "Then I'll pretend to be on duty.$"

ParadisoResort_Text_MistyIntro:
	.string "MISTY: The CHAMPION, here?\n"
	.string "In MY lagoon?\p"
	.string "I flew all the way from KANTO to\n"
	.string "not battle anyone. You ruined it.\l"
	.string "Now you get the full treatment!$"

ParadisoResort_Text_MistyDefeat:
	.string "Ugh! Now I need another vacation\n"
	.string "to recover from this vacation.$"

ParadisoResort_Text_MistyPost:
	.string "MISTY: The pool is just the sea.\n"
	.string "I paid extra for a pool.\p"
	.string "I'm writing a review. One star.\n"
	.string "The star is for the sea.$"

ParadisoResort_Text_ErikaNotYet:
	.string "ERIKA: I booked a garden suite.\n"
	.string "They gave me an island of sand.\p"
	.string "Sand is not soil. Sand is a lie\n"
	.string "that soil tells to tourists.$"

ParadisoResort_Text_ErikaIntro:
	.string "ERIKA: Oh, the CHAMPION.\n"
	.string "How lovely. I was napping.\p"
	.string "I nap under this umbrella because\n"
	.string "it's the only green thing here.\p"
	.string "Let's battle. Gently. Then very,\n"
	.string "very not gently.$"

ParadisoResort_Text_ErikaDefeat:
	.string "My flowers wilted. To be fair,\n"
	.string "it's 40 degrees and they're plants.$"

ParadisoResort_Text_ErikaPost:
	.string "ERIKA: I planted a seed in the sand\n"
	.string "this morning.\p"
	.string "A KRABBY ate it. Then it looked at\n"
	.string "me. It knew what it had done.$"

ParadisoResort_Text_BirchNotYet:
	.string "PROF. BIRCH: Shh! Don't move.\p"
	.string "After years of research, I finally\n"
	.string "found one. A REAL one.\p"
	.string "No goo. No meteorite. No pearls.\n"
	.string "A classic, conventional dropping.\p"
	.string "Come back when you're CHAMPION.\n"
	.string "This is a delicate moment.$"

ParadisoResort_Text_BirchIntro:
	.string "PROF. BIRCH: Look at it, {PLAYER}.\n"
	.string "Perfect spiral. Textbook.\p"
	.string "Every other one I found was goo,\n"
	.string "rock or pearl. This one is honest.\p"
	.string "And whoever made it is still on\n"
	.string "this beach. I'll find them!\p"
	.string "But first: a battle! For science!$"

ParadisoResort_Text_BirchDefeat:
	.string "Ahh! My data! Step around it!\n"
	.string "Step AROUND it!$"

ParadisoResort_Text_BirchPost:
	.string "PROF. BIRCH: The hotel says it\n"
	.string "belongs to a guest's SLOWBRO.\p"
	.string "The SLOWBRO says nothing.\n"
	.string "That's exactly what a suspect says.$"

ParadisoResort_Text_Turd:
	.string "It's a turd.\p"
	.string "A traditional, unambiguous,\n"
	.string "three-tiered turd.\p"
	.string "Somebody put a little paper\n"
	.string "umbrella in it.$"

ParadisoResort_Text_RivalBrendan:
	.string "BRENDAN: {PLAYER}! Welcome to\n"
	.string "my retirement.\p"
	.string "Guess who's in the GUINNESS BOOK\n"
	.string "OF WORLD RECORDS.\p"
	.string "Earliest retirement ever.\n"
	.string "Thirteen years old.\p"
	.string "They sent a man with a clipboard.\n"
	.string "He asked if I was sure. I said I\l"
	.string "have never been more sure.\l"
	.string "He wept a little. On the form.\p"
	.string "The previous record holder was a\n"
	.string "SLAKOTH. It's taking the news well.\l"
	.string "It hasn't moved since.\p"
	.string "My pension is paid in seashells.\n"
	.string "I own forty. I'm basically rich.\p"
	.string "Dad still thinks I'm doing\n"
	.string "fieldwork. Technically I'm lying\l"
	.string "in a field. Of sand.$"

ParadisoResort_Text_RivalMay:
	.string "MAY: {PLAYER}! Welcome to\n"
	.string "my retirement.\p"
	.string "Guess who's in the GUINNESS BOOK\n"
	.string "OF WORLD RECORDS.\p"
	.string "Earliest retirement ever.\n"
	.string "Thirteen years old.\p"
	.string "They sent a man with a clipboard.\n"
	.string "He asked if I was sure. I said I\l"
	.string "have never been more sure.\l"
	.string "He wept a little. On the form.\p"
	.string "The previous record holder was a\n"
	.string "SLAKOTH. It's taking the news well.\l"
	.string "It hasn't moved since.\p"
	.string "My pension is paid in seashells.\n"
	.string "I own forty. I'm basically rich.\p"
	.string "Dad still thinks I'm doing\n"
	.string "fieldwork. Technically I'm lying\l"
	.string "in a field. Of sand.$"

ParadisoResort_Text_RivalAgain:
	.string "{RIVAL}: Oh, it's you. I'm busy.\p"
	.string "I'm on chapter three of doing\n"
	.string "absolutely nothing. Real page-turner.$"

ParadisoResort_Text_RivalAsk:
	.string "{RIVAL}: Retired people get one\n"
	.string "battle a day. Doctor's orders.\l"
	.string "The doctor is also retired.\p"
	.string "Want today's?$"

ParadisoResort_Text_RivalDecline:
	.string "{RIVAL}: Fine. More time for my tan.\n"
	.string "One side is done. The other side\l"
	.string "is between me and the sun.$"

ParadisoResort_Text_RivalDefeat:
	.string "Retired AND defeated.\n"
	.string "I'm really nailing this lifestyle.$"

ParadisoResort_Text_RivalPostBattle:
	.string "{RIVAL}: Same time tomorrow?\n"
	.string "I'll be here. I'm always here.\l"
	.string "That's kind of the whole point.$"

ParadisoResort_Text_RivalDoneToday:
	.string "{RIVAL}: One battle a day. That's\n"
	.string "the rule. I made it up, but now\l"
	.string "it's in a book. Next to my record.$"

ParadisoResort_Text_PoolSwimmer:
	.string "Best pool I've ever been in!\n"
	.string "It goes on forever!\p"
	.string "… … …\n"
	.string "Something brushed my leg.$"

ParadisoResort_Text_Lifeguard:
	.string "Zzz… I'm not asleep. I'm watching\n"
	.string "the pool with my eyes closed.\p"
	.string "It's a technique. Zzz…$"

ParadisoResort_Text_DrunkHiker:
	.string "I climbed MT. CHIMNEY, VICTORY\n"
	.string "ROAD and the SKY PILLAR.\p"
	.string "But I cannot find my room.\n"
	.string "The hotel has ONE door. Hic!$"

ParadisoResort_Text_DrunkBeauty:
	.string "All-inclusive means the drinks are\n"
	.string "free! So I had all of them.\p"
	.string "Every single one. The bartender\n"
	.string "had to go home. Hic!$"

ParadisoResort_Text_DrunkFatMan:
	.string "I've been staring at the sea for\n"
	.string "six hours.\p"
	.string "I think it's staring back.\n"
	.string "We've reached an understanding.$"

ParadisoResort_Text_DrunkFan:
	.string "WALLACE is doing a wine tasting!\n"
	.string "I went in sober. I came out like\l"
	.string "this. Twelve glasses. HIC!\p"
	.string "They said 'swirl and spit'.\n"
	.string "I swirled. I did not spit.$"

ParadisoResort_Text_Sunburn:
	.string "I fell asleep on the beach as a\n"
	.string "normal man.\p"
	.string "I woke up as a FIRE type.\n"
	.string "Don't touch me. Please.$"

ParadisoResort_Text_Collector:
	.string "I collect seashells.\p"
	.string "That one's not a seashell, dear.\n"
	.string "Ask the professor. He won't stop\l"
	.string "talking about it.$"

ParadisoResort_Text_MistyAsk:
	.string "MISTY: Hey. You. Yes, you, blocking my\n"
	.string "sun.\p"
	.string "You look like you want a battle. Do you\n"
	.string "want a battle?$"

ParadisoResort_Text_MistyDecline:
	.string "MISTY: Smart. Go stand in someone else's\n"
	.string "light.$"

ParadisoResort_Text_ErikaAsk:
	.string "ERIKA: Mm…? Are you here to wake me up\n"
	.string "with a battle?\p"
	.string "You may say no. Please say no.$"

ParadisoResort_Text_ErikaDecline:
	.string "ERIKA: Thank you. Zzz…$"

ParadisoResort_Text_BirchAsk:
	.string "PROF. BIRCH: {PLAYER}! Don't step in it!\n"
	.string "I'm documenting it.\p"
	.string "Do you want to battle? For science?\n"
	.string "It's always for science.$"

ParadisoResort_Text_BirchDecline:
	.string "PROF. BIRCH: Fine. More time for me and\n"
	.string "the specimen.$"

ParadisoResort_Text_Dave:
	.string "DAVE: They asked me to retire.\n"
	.string "Too many goals, wasn't fair for\l"
	.string "the rest of the league.\p"
	.string "After a legendary career, there's\n"
	.string "only two things left.\p"
	.string "Raising children and chilling\n"
	.string "on the beach.\p"
	.string "And a bacardi, with a bit of coke,\n"
	.string "but you shouldn't taste the coke.\p"
	.string "Otherwise it's not a rum coke.\n"
	.string "Like a Long Island Ice Tea.$"

ParadisoResort_Text_DaveComeback:
	.string "…But you know what they say.\n"
	.string "Legends never retire. They just\l"
	.string "do a farewell tour. Forever.\p"
	.string "One last match. Kickoff after\n"
	.string "this sip.\p"
	.string "…It's empty. That's a red card\n"
	.string "for you. Let's go!$"

ParadisoResort_Text_DaveDefeat:
	.string "VAR is checking it…\n"
	.string "VAR says I lost. VAR is a liar.$"

ParadisoResort_Text_DavePostBattle:
	.string "DAVE: That wasn't a comeback.\n"
	.string "That was a testimonial match.\p"
	.string "Nobody tries in a testimonial.\n"
	.string "Write that down. In pen.$"

ParadisoResort_Text_DaveRetired:
	.string "DAVE: Shh. I'm working.\p"
	.string "Professional tanning is a\n"
	.string "full-time job. Both sides.\p"
	.string "Thirty minutes front, thirty\n"
	.string "back, and one bacardi per side.$"
