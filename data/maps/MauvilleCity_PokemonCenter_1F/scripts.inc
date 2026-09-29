MauvilleCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MauvilleCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

MauvilleCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_MAUVILLE_CITY
	call Common_EventScript_UpdateBrineyLocation
	goto MauvilleCity_PokemonCenter_1F_EventScript_SetMauvilleOldManGfx
	end

MauvilleCity_PokemonCenter_1F_EventScript_SetMauvilleOldManGfx::
	special SetMauvilleOldManObjEventGfx
	end

MauvilleCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_MAUVILLE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

MauvilleCity_PokemonCenter_1F_EventScript_Protipmaster::
	lock
	faceplayer
	msgbox MauvilleCity_PokemonCenter_1F_Text_ProtipMaster, MSGBOX_NPC
	release
	end

MauvilleCity_PokemonCenter_1F_EventScript_Woman1::
	msgbox MauvilleCity_PokemonCenter_1F_Text_ManOverThereSaysWeirdThings, MSGBOX_NPC
	end

MauvilleCity_PokemonCenter_1F_EventScript_Woman2::
	msgbox MauvilleCity_PokemonCenter_1F_Text_MyDataUpdatedFromRecordCorner, MSGBOX_NPC
	end

MauvilleCity_PokemonCenter_1F_EventScript_Youngster::
	msgbox MauvilleCity_PokemonCenter_1F_Text_RecordCornerSoundsFun, MSGBOX_NPC
	end

MauvilleCity_PokemonCenter_1F_Text_ManOverThereSaysWeirdThings:
	.string "That man over there says weird things!\p"
	.string "He's funny in a weird way.\p"
	.string "He just said “datacenter” 14 times.$"

MauvilleCity_PokemonCenter_1F_Text_MyDataUpdatedFromRecordCorner:
	.string "Shh! I'm in a raid.\p"
	.string "… … … … … …\p"
	.string "Sorry, did you say something?\p"
	.string "I didn't see you. I never see anyone.$"

MauvilleCity_PokemonCenter_1F_Text_RecordCornerSoundsFun:
	.string "I've spent ¥50,000 on EA FC packs.\p"
	.string "My best player is still RODRI.\p"
	.string "He walks. Everywhere.\p"
	.string "…One more pack.$"

MauvilleCity_PokemonCenter_1F_Text_ProtipMaster:
	.string "Hello, I am the PROTIP ORACLE!\p"
	.string "I spread my knowledge around POKéMON\n"
	.string "CENTERS teaching the younger\l"
	.string "generation how to play.\p"
	.string "Did you know: You can gamble at the\n"
	.string "casino. You can win prizes there,\l"
	.string "but you can also lose money.\p"
	.string "“GOKKEN? WEES BEWUST 18+”$"
	