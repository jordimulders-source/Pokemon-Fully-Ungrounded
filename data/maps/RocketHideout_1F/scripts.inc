@ Project Grounded: Rocket-hideout 1F (opslag). Kaart: tools/grounded/maptools/rocket_hideout.py
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
RocketHideout_1F_MapScripts::
	.byte 0

RocketHideout_1F_EventScript_Smuggler::
	trainerbattle_single TRAINER_ROCKET_SMUGGLER, RocketHideout_1F_Text_SmugglerIntro, RocketHideout_1F_Text_SmugglerDefeat
	msgbox RocketHideout_1F_Text_SmugglerPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_1F_EventScript_Motto::
	trainerbattle_single TRAINER_ROCKET_MOTTO, RocketHideout_1F_Text_MottoIntro, RocketHideout_1F_Text_MottoDefeat
	msgbox RocketHideout_1F_Text_MottoPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_1F_Text_SmugglerIntro:
	.string "Psst. Wanna buy a RARE CANDY?\n"
	.string "It's mostly sugar. And regret.$"

RocketHideout_1F_Text_SmugglerDefeat:
	.string "No refunds! That's the whole\n"
	.string "business model!$"

RocketHideout_1F_Text_SmugglerPostBattle:
	.string "I smuggle POKéMON in my coat.\n"
	.string "That's why it's so warm.\p"
	.string "And why it bites.$"

RocketHideout_1F_Text_MottoIntro:
	.string "Prepare for trouble! And make it…\n"
	.string "…hang on, my partner's on break.\p"
	.string "Fine, I'll do both parts.\n"
	.string "Prepare for trouble! And make it\l"
	.string "double! To protect the world from…\p"
	.string "You're not even listening.$"

RocketHideout_1F_Text_MottoDefeat:
	.string "Team Rocket's blasting off\n"
	.string "agaaain… Indoors. Ow. Ceiling.$"

RocketHideout_1F_Text_MottoPostBattle:
	.string "Twelve years I've recited that\n"
	.string "motto. Nobody ever lets me finish.$"
