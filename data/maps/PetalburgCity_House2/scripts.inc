PetalburgCity_House2_MapScripts::
	.byte 0

PetalburgCity_House2_EventScript_Woman::
	msgbox PetalburgCity_House2_Text_NormanBecameGymLeader, MSGBOX_NPC
	end

PetalburgCity_House2_EventScript_SchoolKid::
	msgbox PetalburgCity_House2_Text_BattledNormanOnce, MSGBOX_NPC
	end

PetalburgCity_House2_Text_NormanBecameGymLeader:
	.string "NORMAN is our new GYM LEADER.\p"
	.string "He moved his whole family here from\n"
	.string "JOHTO.\p"
	.string "Nobody asked the family.$"

PetalburgCity_House2_Text_BattledNormanOnce:
	.string "I battled NORMAN once. Way too strong.\p"
	.string "He lives for POKéMON.\p"
	.string "His kid has to walk to the next town to\n"
	.string "see him.$"

