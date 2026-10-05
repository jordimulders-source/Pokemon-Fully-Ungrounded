VictoryRoad_B2F_MapScripts::
	.byte 0

VictoryRoad_B2F_EventScript_Vito::
	trainerbattle_single TRAINER_VITO, VictoryRoad_B2F_Text_VitoIntro, VictoryRoad_B2F_Text_VitoDefeat
	msgbox VictoryRoad_B2F_Text_VitoPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_SickBlik::
	trainerbattle_single TRAINER_SICKBLIK, VictoryRoad_B2F_Text_OwenIntro, VictoryRoad_B2F_Text_OwenDefeat
	msgbox VictoryRoad_B2F_Text_OwenPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Caroline::
	trainerbattle_single TRAINER_CAROLINE, VictoryRoad_B2F_Text_CarolineIntro, VictoryRoad_B2F_Text_CarolineDefeat
	msgbox VictoryRoad_B2F_Text_CarolinePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Julie::
	trainerbattle_single TRAINER_JULIE, VictoryRoad_B2F_Text_JulieIntro, VictoryRoad_B2F_Text_JulieDefeat
	msgbox VictoryRoad_B2F_Text_JuliePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Felix::
	trainerbattle_single TRAINER_FELIX, VictoryRoad_B2F_Text_FelixIntro, VictoryRoad_B2F_Text_FelixDefeat
	msgbox VictoryRoad_B2F_Text_FelixPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_EventScript_Dianne::
	trainerbattle_single TRAINER_DIANNE, VictoryRoad_B2F_Text_DianneIntro, VictoryRoad_B2F_Text_DianneDefeat
	msgbox VictoryRoad_B2F_Text_DiannePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B2F_Text_VitoIntro:
	.string "I trained with my whole family! Every\n"
	.string "one of us!\p"
	.string "We're the WINSTRATES' cousins!$"

VictoryRoad_B2F_Text_VitoDefeat:
	.string "Better than my family?! How?!$"

VictoryRoad_B2F_Text_VitoPostBattle:
	.string "I was the best in my family. Never lost.\p"
	.string "Now I have to tell them at dinner.\p"
	.string "Maybe I'll just live in this cave.$"

VictoryRoad_B2F_Text_OwenIntro:
	.string "There you are!\p"
	.string "Are you enjoying my romhack?\n"
	.string "You're approaching the E4...\l"
	.string "That's gonna be some fun battles!$"

VictoryRoad_B2F_Text_OwenDefeat:
	.string "You are ready!\n"
	.string "Hopefully you are good at team\l"
	.string "building!$"

VictoryRoad_B2F_Text_OwenPostBattle:
	.string "Man, it's so fun to be able to make\n"
	.string "your own edit of a game and get\l"
	.string "your creative ideas going.$"

VictoryRoad_B2F_Text_CarolineIntro:
	.string "You look tired. Perfect.$"

VictoryRoad_B2F_Text_CarolineDefeat:
	.string "Not tired at all?! What are you on?!$"

VictoryRoad_B2F_Text_CarolinePostBattle:
	.string "VICTORY ROAD and the LEAGUE are\n"
	.string "grueling.\p"
	.string "Bring snacks. I didn't. I'm so hungry.$"

VictoryRoad_B2F_Text_JulieIntro:
	.string "Don't get cocky because of your GYM\n"
	.string "BADGES.\p"
	.string "There's always someone better!$"

VictoryRoad_B2F_Text_JulieDefeat:
	.string "You're better than me!\p"
	.string "I guess I'm the someone.$"

VictoryRoad_B2F_Text_JuliePostBattle:
	.string "Look at your BADGES and remember who\n"
	.string "you've beaten.\p"
	.string "The jerkoffs in this cave included.$"

VictoryRoad_B2F_Text_FelixIntro:
	.string "I made it this far, but the stress gives\n"
	.string "me stomach cramps…$"

VictoryRoad_B2F_Text_FelixDefeat:
	.string "Ooh… It hurts…$"

VictoryRoad_B2F_Text_FelixPostBattle:
	.string "The LEAGUE is so close. I'm so tense.\p"
	.string "Is there a toilet in this cave? Asking\n"
	.string "urgently.$"

VictoryRoad_B2F_Text_DianneIntro:
	.string "The elite of the elite gather in this\n"
	.string "cave.\p"
	.string "How are you finding it?$"

VictoryRoad_B2F_Text_DianneDefeat:
	.string "Not rattled at all!$"

VictoryRoad_B2F_Text_DiannePostBattle:
	.string "You've got guts! Keep it up!\p"
	.string "And take a left. Trust me.$"

