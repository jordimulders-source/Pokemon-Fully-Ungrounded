@ Project Grounded: ChargestoneCave_B1F (tools/grounded/maptools/chargestone.py)
ChargestoneCave_B1F_MapScripts::
	.byte 0

ChargestoneCave_B1F_EventScript_GruntFence::
	trainerbattle_single TRAINER_CHARGESTONE_GRUNT_B1F_1, ChargestoneCave_B1F_Text_GruntFenceIntro, ChargestoneCave_B1F_Text_GruntFenceDefeat
	msgbox ChargestoneCave_B1F_Text_GruntFencePost, MSGBOX_AUTOCLOSE
	end

ChargestoneCave_B1F_EventScript_GruntCavern::
	trainerbattle_single TRAINER_CHARGESTONE_GRUNT_B1F_2, ChargestoneCave_B1F_Text_GruntCavernIntro, ChargestoneCave_B1F_Text_GruntCavernDefeat
	msgbox ChargestoneCave_B1F_Text_GruntCavernPost, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
ChargestoneCave_B1F_Text_GruntFenceIntro:
	.string "You found the fence! We built it out of\n"
	.string "floating rocks. Very modern.\p"
	.string "It's also the only fence in the world\n"
	.string "you can push over. We're working on\l"
	.string "that.$"

ChargestoneCave_B1F_Text_GruntFenceDefeat:
	.string "The fence was a metaphor anyway.$"

ChargestoneCave_B1F_Text_GruntFencePost:
	.string "Push the stones in the gaps. Or don't.\n"
	.string "I'm not your supervisor. My supervisor\l"
	.string "is evil.$"

ChargestoneCave_B1F_Text_GruntCavernIntro:
	.string "Every rock in here hums at fifty hertz.\n"
	.string "So do I, after three weeks of overtime.$"

ChargestoneCave_B1F_Text_GruntCavernDefeat:
	.string "Bzzt. That's me, short-circuiting\n"
	.string "emotionally.$"

ChargestoneCave_B1F_Text_GruntCavernPost:
	.string "COLRESS says the cave runs on a\n"
	.string "ZERAORA now. I asked what it ran on\l"
	.string "before.\p"
	.string "He said 'ignorance' and docked my pay.$"
