@ Project Grounded: Rocket-hideout B2F (kantoor van executive Petrel). Kaart: tools/grounded/maptools/rocket_hideout.py
@ Na het gevecht krijg je de ZONE KEYS terug (VAR_ROCKET_QUEST 3); Petrel en de dief verdwijnen. Het teleportvlak
@ rechts is een nooduitgang naar de holle boom in Fortree Jungle.
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
RocketHideout_B2F_MapScripts::
	.byte 0

RocketHideout_B2F_EventScript_Petrel::
	trainerbattle_single TRAINER_PETREL, RocketHideout_B2F_Text_PetrelIntro, RocketHideout_B2F_Text_PetrelDefeat, RocketHideout_B2F_EventScript_PetrelDefeated
	msgbox RocketHideout_B2F_Text_PetrelPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B2F_EventScript_PetrelDefeated::
	msgbox RocketHideout_B2F_Text_PetrelGivesKeys, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message RocketHideout_B2F_Text_GotZoneKeys
	waitfanfare
	setvar VAR_ROCKET_QUEST, 3
	applymovement LOCALID_ROCKET_RUNNER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox RocketHideout_B2F_Text_RunnerSmoke, MSGBOX_DEFAULT
	msgbox RocketHideout_B2F_Text_PetrelRetreat, MSGBOX_DEFAULT
	closemessage
	playse SE_M_EXPLOSION
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_ROCKET_PETREL
	removeobject LOCALID_ROCKET_RUNNER
	setflag FLAG_HIDE_ROCKET_EXEC
	fadescreen FADE_FROM_WHITE
	msgbox RocketHideout_B2F_Text_SmokeClears, MSGBOX_DEFAULT
	release
	end

RocketHideout_B2F_EventScript_Runner::
	msgbox RocketHideout_B2F_Text_Runner, MSGBOX_NPC
	end

RocketHideout_B2F_Text_PetrelIntro:
	.string "Kneel before GIOVANNI, supreme\n"
	.string "boss of Team Rocket!\p"
	.string "What? The purple hair? It's a new\n"
	.string "look. Very bold. Very boss.\p"
	.string "…Fine. I'm PETREL, Rocket's master\n"
	.string "of disguise. And the ZONE KEYS stay\l"
	.string "right here in my pocket!$"

RocketHideout_B2F_Text_PetrelDefeat:
	.string "Even my DITTO is having an\n"
	.string "identity crisis now.$"

RocketHideout_B2F_Text_PetrelPostBattle:
	.string "I was never here.$"

RocketHideout_B2F_Text_PetrelGivesKeys:
	.string "Fine! Take your stupid ZONE KEYS.\n"
	.string "They didn't even fit the condo.$"

RocketHideout_B2F_Text_GotZoneKeys:
	.string "{PLAYER} got the ZONE KEYS back!$"

RocketHideout_B2F_Text_RunnerSmoke:
	.string "Boss! Boss! Should we use the smoke\n"
	.string "bomb? The one that smells like toast?$"

RocketHideout_B2F_Text_PetrelRetreat:
	.string "No time! Smoke bomb!\n"
	.string "Team Rocket retreats to…\l"
	.string "…a better tree!$"

RocketHideout_B2F_Text_SmokeClears:
	.string "They're gone. They left the coffee\n"
	.string "machine running.\p"
	.string "The pad on the right looks like\n"
	.string "an emergency exit.$"

RocketHideout_B2F_Text_Runner:
	.string "I'm just the intern. I only run.\n"
	.string "I'm VERY good at running.$"
