@ Project Grounded: lobby van het PARADISO RESORT (layout van de Contest Lobby). Inchecken = gratis heal, zonder vraag.
ParadisoResort_Lobby_MapScripts::
	.byte 0

ParadisoResort_Lobby_EventScript_Receptionist::
	lock
	faceplayer
	msgbox ParadisoResort_Lobby_Text_CheckIn, MSGBOX_DEFAULT
	closemessage
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	msgbox ParadisoResort_Lobby_Text_CheckedIn, MSGBOX_DEFAULT
	release
	end

ParadisoResort_Lobby_EventScript_Concierge::
	msgbox ParadisoResort_Lobby_Text_Concierge, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_Cynthia::
	goto_if_unset FLAG_SYS_GAME_CLEAR, ParadisoResort_Lobby_EventScript_CynthiaNotYet
	goto_if_defeated TRAINER_RESORT_CYNTHIA, ParadisoResort_Lobby_EventScript_CynthiaPost
	lock
	faceplayer
	msgbox ParadisoResort_Lobby_Text_CynthiaAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ParadisoResort_Lobby_EventScript_CynthiaDecline
	trainerbattle_single TRAINER_RESORT_CYNTHIA, ParadisoResort_Lobby_Text_CynthiaIntro, ParadisoResort_Lobby_Text_CynthiaDefeat
ParadisoResort_Lobby_EventScript_CynthiaPost::
	msgbox ParadisoResort_Lobby_Text_CynthiaPost, MSGBOX_AUTOCLOSE
	end

ParadisoResort_Lobby_EventScript_CynthiaDecline::
	msgbox ParadisoResort_Lobby_Text_CynthiaDecline, MSGBOX_DEFAULT
	release
	end

ParadisoResort_Lobby_EventScript_CynthiaNotYet::
	msgbox ParadisoResort_Lobby_Text_CynthiaNotYet, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_Bellhop::
	msgbox ParadisoResort_Lobby_Text_Bellhop, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_DrunkGuest::
	msgbox ParadisoResort_Lobby_Text_DrunkGuest, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_DrunkWoman::
	msgbox ParadisoResort_Lobby_Text_DrunkWoman, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_Complainer::
	msgbox ParadisoResort_Lobby_Text_Complainer, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_WallaceFan::
	msgbox ParadisoResort_Lobby_Text_WallaceFan, MSGBOX_NPC
	end

ParadisoResort_Lobby_EventScript_Kid::
	msgbox ParadisoResort_Lobby_Text_Kid, MSGBOX_NPC
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ParadisoResort_Lobby_Text_CheckIn:
	.string "Welcome to PARADISO RESORT!\n"
	.string "You're checked in. You were always\l"
	.string "checked in. Nobody ever checks out.$"

ParadisoResort_Lobby_Text_CheckedIn:
	.string "Your POKéMON have been refreshed\n"
	.string "with our complimentary spa.\p"
	.string "It's a bucket of seawater.\n"
	.string "Enjoy your stay!$"

ParadisoResort_Lobby_Text_Concierge:
	.string "The wine tasting is through the\n"
	.string "doors behind us.\p"
	.string "Please spit in the buckets, not\n"
	.string "on the other guests. Again.$"

ParadisoResort_Lobby_Text_CynthiaNotYet:
	.string "CYNTHIA: I came here to read about\n"
	.string "ancient myths in peace.\p"
	.string "The man next to me sang the same\n"
	.string "song nine times. That's a myth now.\p"
	.string "You're not CHAMPION yet. Go on.\n"
	.string "I'll still be here. Chapter four.$"

ParadisoResort_Lobby_Text_CynthiaIntro:
	.string "CYNTHIA: So you're the CHAMPION\n"
	.string "of HOENN.\p"
	.string "I'm on vacation, but GARCHOMP\n"
	.string "isn't. GARCHOMP is never on\l"
	.string "vacation. GARCHOMP doesn't know\l"
	.string "what a vacation is.\p"
	.string "Show me what you've got.$"

ParadisoResort_Lobby_Text_CynthiaDefeat:
	.string "Wonderful. I'll write that down.\n"
	.string "Right after the chapter on loss.$"

ParadisoResort_Lobby_Text_CynthiaPost:
	.string "CYNTHIA: Did you know the old\n"
	.string "legends say HOENN rose from the sea?\p"
	.string "Judging by the guests, it'll sink\n"
	.string "back into it after happy hour.$"

ParadisoResort_Lobby_Text_Bellhop:
	.string "May I take your bag?\p"
	.string "… … …\n"
	.string "It contains 400 POTIONS and a bike.\p"
	.string "I'll just… stand here, then.$"

ParadisoResort_Lobby_Text_DrunkGuest:
	.string "I've been looking at this wall for\n"
	.string "an hour. It's the exit. Hic!\p"
	.string "I'm waiting for it to open\n"
	.string "itself. Like a gentleman.$"

ParadisoResort_Lobby_Text_DrunkWoman:
	.string "Free drinks! Free food! Free towels!\n"
	.string "I've stolen eleven towels.\p"
	.string "I don't even have a bag. I'm\n"
	.string "wearing them. Hic!$"

ParadisoResort_Lobby_Text_Complainer:
	.string "I asked for a sea view.\n"
	.string "The whole island is a sea view.\p"
	.string "That's not the point. I want\n"
	.string "to complain about something.$"

ParadisoResort_Lobby_Text_WallaceFan:
	.string "WALLACE is inside! With WINE!\p"
	.string "I don't drink. I just want to watch\n"
	.string "him swirl the glass. So elegant.\l"
	.string "He swirls like a MILOTIC.$"

ParadisoResort_Lobby_Text_Kid:
	.string "My dad says I'm too young for the\n"
	.string "wine tasting.\p"
	.string "Then he went in. Now he's too\n"
	.string "old for walking.$"

ParadisoResort_Lobby_Text_CynthiaAsk:
	.string "CYNTHIA: Hm? I'm reading. It's a book\n"
	.string "about ruins.\p"
	.string "Or would you rather battle? GARCHOMP is\n"
	.string "listening. GARCHOMP is always listening.$"

ParadisoResort_Lobby_Text_CynthiaDecline:
	.string "CYNTHIA: Understandable. GARCHOMP is\n"
	.string "disappointed, but GARCHOMP is always\l"
	.string "disappointed.$"
