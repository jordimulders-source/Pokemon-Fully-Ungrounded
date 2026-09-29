VictoryRoad_B1F_MapScripts::
	.byte 0

VictoryRoad_B1F_EventScript_Samuel::
	trainerbattle_single TRAINER_SAMUEL, VictoryRoad_B1F_Text_SamuelIntro, VictoryRoad_B1F_Text_SamuelDefeat
	msgbox VictoryRoad_B1F_Text_SamuelPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Shannon::
	trainerbattle_single TRAINER_SHANNON, VictoryRoad_B1F_Text_ShannonIntro, VictoryRoad_B1F_Text_ShannonDefeat
	msgbox VictoryRoad_B1F_Text_ShannonPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Michelle::
	trainerbattle_single TRAINER_MICHELLE, VictoryRoad_B1F_Text_MichelleIntro, VictoryRoad_B1F_Text_MichelleDefeat
	msgbox VictoryRoad_B1F_Text_MichellePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Mitchell::
	trainerbattle_single TRAINER_MITCHELL, VictoryRoad_B1F_Text_MitchellIntro, VictoryRoad_B1F_Text_MitchellDefeat
	msgbox VictoryRoad_B1F_Text_MitchellPostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_EventScript_Halle::
	trainerbattle_single TRAINER_HALLE, VictoryRoad_B1F_Text_HalleIntro, VictoryRoad_B1F_Text_HalleDefeat
	msgbox VictoryRoad_B1F_Text_HallePostBattle, MSGBOX_AUTOCLOSE
	end

VictoryRoad_B1F_Text_SamuelIntro:
	.string "Getting closer to the POKéMON LEAGUE…\p"
	.string "I'm getting stage fright…$"

VictoryRoad_B1F_Text_SamuelDefeat:
	.string "I couldn't do a single thing…$"

VictoryRoad_B1F_Text_SamuelPostBattle:
	.string "The POKéMON LEAGUE is far away again…\p"
	.string "Phew. Honestly, relief.$"

VictoryRoad_B1F_Text_ShannonIntro:
	.string "To win the POKéMON LEAGUE, you need\n"
	.string "your POKéMON's trust.$"

VictoryRoad_B1F_Text_ShannonDefeat:
	.string "Your bond is built on solid trust.$"

VictoryRoad_B1F_Text_ShannonPostBattle:
	.string "Trust grows by spending time together.\p"
	.string "And by not boxing them for three weeks.$"

VictoryRoad_B1F_Text_MichelleIntro:
	.string "This isn't the goal. It's just on the way\n"
	.string "to the LEAGUE.\p"
	.string "A very long, very dark way.$"

VictoryRoad_B1F_Text_MichelleDefeat:
	.string "That's the way! …For you. Not for me.$"

VictoryRoad_B1F_Text_MichellePostBattle:
	.string "You'll do fine! Your POKéMON are eager\n"
	.string "to go!\p"
	.string "Mine are eager to go home.$"

VictoryRoad_B1F_Text_MitchellIntro:
	.string "My POKéMON are cosmically\n"
	.string "awe-inspiring!\p"
	.string "The SOLROCK and LUNATONE are a couple.$"

VictoryRoad_B1F_Text_MitchellDefeat:
	.string "I've never met anyone like you.$"

VictoryRoad_B1F_Text_MitchellPostBattle:
	.string "I sense incredible power coming from\n"
	.string "you and your POKéMON.\p"
	.string "Or radiation. The METAGROSS leaks a bit.$"

VictoryRoad_B1F_Text_HalleIntro:
	.string "Relax! Let's take it easy!\p"
	.string "This is VICTORY ROAD, not a job\n"
	.string "interview.$"

VictoryRoad_B1F_Text_HalleDefeat:
	.string "Whoa! Wonderful!$"

VictoryRoad_B1F_Text_HallePostBattle:
	.string "Sure, this is VICTORY ROAD.\p"
	.string "But it's like the rest of your journey.\p"
	.string "Just darker. And with more ROCK SMASH.$"

