@ Project Grounded: Rocket-hideout 1F (opslag). Kaart: tools/grounded/maptools/rocket_hideout.py
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
RocketHideout_1F_MapScripts::
	.byte 0

RocketHideout_1F_EventScript_Smuggler::
	trainerbattle_single TRAINER_ROCKET_SMUGGLER, RocketHideout_1F_Text_SmugglerIntro, RocketHideout_1F_Text_SmugglerDefeat
	msgbox RocketHideout_1F_Text_SmugglerPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_1F_EventScript_Recruiter::
	trainerbattle_single TRAINER_ROCKET_RECRUITER, RocketHideout_1F_Text_RecruiterIntro, RocketHideout_1F_Text_RecruiterDefeat
	msgbox RocketHideout_1F_Text_RecruiterPostBattle, MSGBOX_AUTOCLOSE
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

RocketHideout_1F_Text_RecruiterIntro:
	.string "Oh! A walk-in! Have you considered\n"
	.string "a career in organized crime?\p"
	.string "Flexible hours. Black uniforms.\n"
	.string "Very slimming. Let's do the\l"
	.string "practical part of the interview.$"

RocketHideout_1F_Text_RecruiterDefeat:
	.string "Strong candidate. Terrible attitude.\n"
	.string "I'll put you down as a “maybe”.$"

RocketHideout_1F_Text_RecruiterPostBattle:
	.string "Our benefits package is one cave\n"
	.string "and a hat. The hat is optional.\p"
	.string "The cave is not.$"
