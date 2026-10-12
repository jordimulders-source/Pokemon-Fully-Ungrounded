@ Project Grounded: SickBlik als 'developer' na de Hall of Fame. Elke kaart met hem roept in OnTransition
@ Common_EventScript_SickBlikDevSpawn aan met VAR_0x8004 = zijn plek (0 Mauville, 1 Fortree, 2 Lilycove,
@ 3 Pacifidlog); Grounded_SickBlikSpot kiest per dag één plek. Eén lv 100-gevecht (TRAINER_SICKBLIK_DEV),
@ daarna wisselende developer-grappen.

Common_EventScript_SickBlikDevSpawn::
	specialvar VAR_RESULT, Grounded_SickBlikSpot
	goto_if_eq VAR_RESULT, VAR_0x8004, Common_EventScript_SickBlikDevShow
	setflag FLAG_HIDE_SICKBLIK_DEV
	return

Common_EventScript_SickBlikDevShow:
	clearflag FLAG_HIDE_SICKBLIK_DEV
	return

Common_EventScript_SickBlikDev::
	lock
	faceplayer
	goto_if_defeated TRAINER_SICKBLIK_DEV, Common_EventScript_SickBlikDevJoke
	msgbox SickBlikDev_Text_Intro, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_SICKBLIK_DEV, SickBlikDev_Text_Defeat
	msgbox SickBlikDev_Text_PostBattle, MSGBOX_DEFAULT
	release
	end

Common_EventScript_SickBlikDevJoke:
	random 5
	switch VAR_RESULT
	case 0, Common_EventScript_SickBlikDevJoke0
	case 1, Common_EventScript_SickBlikDevJoke1
	case 2, Common_EventScript_SickBlikDevJoke2
	case 3, Common_EventScript_SickBlikDevJoke3
	msgbox SickBlikDev_Text_Joke4, MSGBOX_DEFAULT
	release
	end

Common_EventScript_SickBlikDevJoke0:
	msgbox SickBlikDev_Text_Joke0, MSGBOX_DEFAULT
	release
	end

Common_EventScript_SickBlikDevJoke1:
	msgbox SickBlikDev_Text_Joke1, MSGBOX_DEFAULT
	release
	end

Common_EventScript_SickBlikDevJoke2:
	msgbox SickBlikDev_Text_Joke2, MSGBOX_DEFAULT
	release
	end

Common_EventScript_SickBlikDevJoke3:
	msgbox SickBlikDev_Text_Joke3, MSGBOX_DEFAULT
	release
	end

SickBlikDev_Text_Intro:
	.string "SICKBLIK: Oh, hey. Don't mind me.\n"
	.string "Just walking the map, checking\l"
	.string "if everything works.\p"
	.string "Found a bug, actually.\n"
	.string "It's you.\p"
	.string "Nobody is supposed to get this\n"
	.string "strong. Hold still. Hotfix incoming.$"

SickBlikDev_Text_Defeat:
	.string "Ticket closed: WONTFIX.\n"
	.string "Works as intended. Sadly.$"

SickBlikDev_Text_PostBattle:
	.string "SICKBLIK: Six level 100s and it\n"
	.string "STILL wasn't enough?\p"
	.string "I'll put it in the changelog.\n"
	.string "Nobody reads the changelog.$"

SickBlikDev_Text_Joke0:
	.string "SICKBLIK: Bug report No. 4127:\n"
	.string "“Player walks into walls on\l"
	.string "purpose for no reason.”\p"
	.string "Status: can't fix.\n"
	.string "That one's just you.$"

SickBlikDev_Text_Joke1:
	.string "SICKBLIK: That's not a bug.\n"
	.string "That's a feature.\p"
	.string "I decided that just now.\n"
	.string "Retroactively. Like a god.$"

SickBlikDev_Text_Joke2:
	.string "SICKBLIK: Someone reported that\n"
	.string "MAGIKARP is too weak.\p"
	.string "Closed. MAGIKARP is perfect.\n"
	.string "Nobody touches MAGIKARP.$"

SickBlikDev_Text_Joke3:
	.string "SICKBLIK: I counted every tree in\n"
	.string "HOENN. One is missing.\p"
	.string "If you see a tree acting\n"
	.string "suspicious, call me.$"

SickBlikDev_Text_Joke4:
	.string "SICKBLIK: This town checks out.\p"
	.string "I'm only standing here so the\n"
	.string "NPC count is an even number.\p"
	.string "Don't tell the other NPCs.\n"
	.string "They think they're real.$"
