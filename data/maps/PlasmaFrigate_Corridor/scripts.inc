@ Project Grounded: Plasma Frigate, gang (kopie van de S.S. Tidal-gang). Kaart: tools/grounded/maptools/plasma_frigate.py
@ Kleurdeuren: hut 1 is open; voor hut 2-4 staat een bewaker die het wachtwoord (de kleurcode uit de vorige hut) wil.
@ VAR_PLASMA_FRIGATE: 2 rood, 3 blauw, 4 wit, 5 geel. De Shadow Triad bewaakt het luik naar het ruim tot je alle vier hebt.
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.
PlasmaFrigate_Corridor_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PlasmaFrigate_Corridor_OnTransition
	.byte 0

PlasmaFrigate_Corridor_OnTransition:
	call_if_defeated TRAINER_PLASMA_GUARD_RED, PlasmaFrigate_Corridor_EventScript_RedAside
	call_if_defeated TRAINER_PLASMA_GUARD_BLUE, PlasmaFrigate_Corridor_EventScript_BlueAside
	call_if_defeated TRAINER_PLASMA_GUARD_WHITE, PlasmaFrigate_Corridor_EventScript_WhiteAside
	end

PlasmaFrigate_Corridor_EventScript_RedAside::
	setobjectxyperm LOCALID_PLASMA_GUARD_RED, 8, 10
	setobjectmovementtype LOCALID_PLASMA_GUARD_RED, MOVEMENT_TYPE_FACE_LEFT
	return

PlasmaFrigate_Corridor_EventScript_BlueAside::
	setobjectxyperm LOCALID_PLASMA_GUARD_BLUE, 11, 10
	setobjectmovementtype LOCALID_PLASMA_GUARD_BLUE, MOVEMENT_TYPE_FACE_LEFT
	return

PlasmaFrigate_Corridor_EventScript_WhiteAside::
	setobjectxyperm LOCALID_PLASMA_GUARD_WHITE, 14, 10
	setobjectmovementtype LOCALID_PLASMA_GUARD_WHITE, MOVEMENT_TYPE_FACE_LEFT
	return

PlasmaFrigate_Corridor_EventScript_GuardRed::
	lock
	faceplayer
	goto_if_defeated TRAINER_PLASMA_GUARD_RED, PlasmaFrigate_Corridor_EventScript_RedDone
	msgbox PlasmaFrigate_Corridor_Text_RedPassword, MSGBOX_DEFAULT
	goto_if_lt VAR_PLASMA_FRIGATE, 2, PlasmaFrigate_Corridor_EventScript_RedWrong
	msgbox PlasmaFrigate_Corridor_Text_RedCorrect, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PLASMA_GUARD_RED, PlasmaFrigate_Corridor_Text_RedDefeat
	msgbox PlasmaFrigate_Corridor_Text_RedAfter, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 8, PlasmaFrigate_Corridor_EventScript_RedLeft
	applymovement LOCALID_PLASMA_GUARD_RED, PlasmaFrigate_Corridor_Movement_StepAside
	goto PlasmaFrigate_Corridor_EventScript_RedMoved
PlasmaFrigate_Corridor_EventScript_RedLeft::
	applymovement LOCALID_PLASMA_GUARD_RED, PlasmaFrigate_Corridor_Movement_StepAsideLeft
PlasmaFrigate_Corridor_EventScript_RedMoved::
	waitmovement 0
	call PlasmaFrigate_Corridor_EventScript_RedAside
	release
	end

PlasmaFrigate_Corridor_EventScript_RedWrong::
	msgbox PlasmaFrigate_Corridor_Text_RedWrong, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_RedDone::
	msgbox PlasmaFrigate_Corridor_Text_RedDone, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_GuardBlue::
	lock
	faceplayer
	goto_if_defeated TRAINER_PLASMA_GUARD_BLUE, PlasmaFrigate_Corridor_EventScript_BlueDone
	msgbox PlasmaFrigate_Corridor_Text_BluePassword, MSGBOX_DEFAULT
	goto_if_lt VAR_PLASMA_FRIGATE, 3, PlasmaFrigate_Corridor_EventScript_BlueWrong
	msgbox PlasmaFrigate_Corridor_Text_BlueCorrect, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PLASMA_GUARD_BLUE, PlasmaFrigate_Corridor_Text_BlueDefeat
	msgbox PlasmaFrigate_Corridor_Text_BlueAfter, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 11, PlasmaFrigate_Corridor_EventScript_BlueLeft
	applymovement LOCALID_PLASMA_GUARD_BLUE, PlasmaFrigate_Corridor_Movement_StepAside
	goto PlasmaFrigate_Corridor_EventScript_BlueMoved
PlasmaFrigate_Corridor_EventScript_BlueLeft::
	applymovement LOCALID_PLASMA_GUARD_BLUE, PlasmaFrigate_Corridor_Movement_StepAsideLeft
PlasmaFrigate_Corridor_EventScript_BlueMoved::
	waitmovement 0
	call PlasmaFrigate_Corridor_EventScript_BlueAside
	release
	end

PlasmaFrigate_Corridor_EventScript_BlueWrong::
	msgbox PlasmaFrigate_Corridor_Text_BlueWrong, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_BlueDone::
	msgbox PlasmaFrigate_Corridor_Text_BlueDone, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_GuardWhite::
	lock
	faceplayer
	goto_if_defeated TRAINER_PLASMA_GUARD_WHITE, PlasmaFrigate_Corridor_EventScript_WhiteDone
	msgbox PlasmaFrigate_Corridor_Text_WhitePassword, MSGBOX_DEFAULT
	goto_if_lt VAR_PLASMA_FRIGATE, 4, PlasmaFrigate_Corridor_EventScript_WhiteWrong
	msgbox PlasmaFrigate_Corridor_Text_WhiteCorrect, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PLASMA_GUARD_WHITE, PlasmaFrigate_Corridor_Text_WhiteDefeat
	msgbox PlasmaFrigate_Corridor_Text_WhiteAfter, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 14, PlasmaFrigate_Corridor_EventScript_WhiteLeft
	applymovement LOCALID_PLASMA_GUARD_WHITE, PlasmaFrigate_Corridor_Movement_StepAside
	goto PlasmaFrigate_Corridor_EventScript_WhiteMoved
PlasmaFrigate_Corridor_EventScript_WhiteLeft::
	applymovement LOCALID_PLASMA_GUARD_WHITE, PlasmaFrigate_Corridor_Movement_StepAsideLeft
PlasmaFrigate_Corridor_EventScript_WhiteMoved::
	waitmovement 0
	call PlasmaFrigate_Corridor_EventScript_WhiteAside
	release
	end

PlasmaFrigate_Corridor_EventScript_WhiteWrong::
	msgbox PlasmaFrigate_Corridor_Text_WhiteWrong, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_WhiteDone::
	msgbox PlasmaFrigate_Corridor_Text_WhiteDone, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_Movement_StepAside:
	walk_right
	face_left
	step_end

PlasmaFrigate_Corridor_Movement_StepAsideLeft:
	walk_left
	face_right
	step_end

@ Shadow Triad voor het luik naar het ruim (15,2)
PlasmaFrigate_Corridor_EventScript_Triad::
	lock
	faceplayer
	goto_if_lt VAR_PLASMA_FRIGATE, 5, PlasmaFrigate_Corridor_EventScript_TriadNotYet
	msgbox PlasmaFrigate_Corridor_Text_TriadIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_PLASMA_SHADOW_TRIAD, PlasmaFrigate_Corridor_Text_TriadDefeat
	msgbox PlasmaFrigate_Corridor_Text_TriadVanish, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PLASMA_TRIAD
	setflag FLAG_HIDE_PLASMA_TRIAD
	setvar VAR_PLASMA_FRIGATE, 6
	fadescreen FADE_FROM_BLACK
	msgbox PlasmaFrigate_Corridor_Text_TriadGone, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_EventScript_TriadNotYet::
	copyvar VAR_0x8004, VAR_PLASMA_FRIGATE
	subvar VAR_0x8004, 1
	buffernumberstring STR_VAR_1, VAR_0x8004
	msgbox PlasmaFrigate_Corridor_Text_TriadNotYet, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	hideobjectat LOCALID_PLASMA_TRIAD, MAP_PLASMA_FRIGATE_CORRIDOR
	fadescreen FADE_FROM_BLACK
	msgbox PlasmaFrigate_Corridor_Text_TriadPoof, MSGBOX_DEFAULT
	closemessage
	showobjectat LOCALID_PLASMA_TRIAD, MAP_PLASMA_FRIGATE_CORRIDOR
	playse SE_PIN
	msgbox PlasmaFrigate_Corridor_Text_TriadBack, MSGBOX_DEFAULT
	release
	end

PlasmaFrigate_Corridor_Text_RedPassword:
	.string "Halt! This door is RED-coded.\n"
	.string "What's the password?$"

PlasmaFrigate_Corridor_Text_RedWrong:
	.string "…You didn't say anything.\n"
	.string "That's wrong, but it's the closest\l"
	.string "anyone's come all week.\p"
	.string "Read the RED code first. It's in\n"
	.string "the first cabin. Which isn't locked.\l"
	.string "Budget cuts.$"

PlasmaFrigate_Corridor_Text_RedCorrect:
	.string "“RED.” …Correct.\p"
	.string "Darn. Now I have to fight you\n"
	.string "anyway. It's in my contract.$"

PlasmaFrigate_Corridor_Text_RedDefeat:
	.string "Burned. By my own color code.$"

PlasmaFrigate_Corridor_Text_RedAfter:
	.string "Go ahead. The next code is in\n"
	.string "there. Security is a team effort.$"

PlasmaFrigate_Corridor_Text_RedDone:
	.string "I'm on my break. My break is\n"
	.string "standing next to the door.$"

PlasmaFrigate_Corridor_Text_BluePassword:
	.string "BLUE door. Password, please.\n"
	.string "And don't say “blue”.\p"
	.string "…It's blue. But don't say it.$"

PlasmaFrigate_Corridor_Text_BlueWrong:
	.string "Wrong! Or nothing. Which is wrong.\p"
	.string "The BLUE code is behind the RED\n"
	.string "door. Like a matryoshka of bad\l"
	.string "decisions.$"

PlasmaFrigate_Corridor_Text_BlueCorrect:
	.string "You said it. You actually said it.\n"
	.string "Now we fight.$"

PlasmaFrigate_Corridor_Text_BlueDefeat:
	.string "Doused. Like my career.$"

PlasmaFrigate_Corridor_Text_BlueAfter:
	.string "Fine. In you go. Wipe your feet.\n"
	.string "The deck is very waxed.$"

PlasmaFrigate_Corridor_Text_BlueDone:
	.string "The water cooler on this ship is\n"
	.string "also a weapon. Everything is.$"

PlasmaFrigate_Corridor_Text_WhitePassword:
	.string "Brr. WHITE door.\n"
	.string "Password?$"

PlasmaFrigate_Corridor_Text_WhiteWrong:
	.string "No. The WHITE code is in the BLUE\n"
	.string "cabin. Keep up.\p"
	.string "And close the door. ZINZOLIN keeps\n"
	.string "the whole ship at minus four.$"

PlasmaFrigate_Corridor_Text_WhiteCorrect:
	.string "Correct. You've earned the right\n"
	.string "to get frozen.$"

PlasmaFrigate_Corridor_Text_WhiteDefeat:
	.string "I can't feel my face.\n"
	.string "That's unrelated to you.$"

PlasmaFrigate_Corridor_Text_WhiteAfter:
	.string "Go. The last code's in there.\n"
	.string "I'm going to stand on the radiator.$"

PlasmaFrigate_Corridor_Text_WhiteDone:
	.string "The radiator is decorative.\n"
	.string "Like my will to live.$"

PlasmaFrigate_Corridor_Text_TriadNotYet:
	.string "…\p"
	.string "The hatch needs all four colors.\n"
	.string "You have {STR_VAR_1}.\p"
	.string "We will now vanish mysteriously.$"

PlasmaFrigate_Corridor_Text_TriadPoof:
	.string "He's gone!$"

PlasmaFrigate_Corridor_Text_TriadBack:
	.string "…He's back. He never left.\n"
	.string "That's the whole technique.$"

PlasmaFrigate_Corridor_Text_TriadIntro:
	.string "Four colors. Impressive.\p"
	.string "We are the SHADOW TRIAD.\n"
	.string "Tonight there is one of us.\l"
	.string "The other two are on paternity leave.$"

PlasmaFrigate_Corridor_Text_TriadDefeat:
	.string "We… vanish now.$"

PlasmaFrigate_Corridor_Text_TriadVanish:
	.string "We vanish now. For real this time.\n"
	.string "Don't watch.$"

PlasmaFrigate_Corridor_Text_TriadGone:
	.string "He's actually gone.\n"
	.string "The hatch to the hold is open.$"
