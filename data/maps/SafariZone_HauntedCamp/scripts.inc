@ Project Grounded: Safari Zone, Haunted Camp (kaart en tileset: tools/grounded/maptools/safari_zones.py)
@ Placeholderteksten; Jordi herschrijft ze via de Dialoogstudio.

SafariZone_HauntedCamp_MapScripts::
	.byte 0

SafariZone_HauntedCamp_EventScript_Sign::
	msgbox SafariZone_HauntedCamp_Text_Sign, MSGBOX_SIGN
	end

SafariZone_HauntedCamp_EventScript_Door::
	msgbox SafariZone_HauntedCamp_Text_Door, MSGBOX_SIGN
	end

SafariZone_HauntedCamp_EventScript_Campfire::
	msgbox SafariZone_HauntedCamp_Text_Campfire, MSGBOX_SIGN
	end

SafariZone_HauntedCamp_EventScript_Lantern::
	msgbox SafariZone_HauntedCamp_Text_Lantern, MSGBOX_SIGN
	end

SafariZone_HauntedCamp_Text_Sign:
	.string "SAFARI ZONE - HAUNTED CAMP\n"
	.string "Camping season: closed since 1997.\p"
	.string "Check-in: whenever.\n"
	.string "Check-out: never.$"

SafariZone_HauntedCamp_Text_Door:
	.string "The door of the old tea house is\n"
	.string "nailed shut.\p"
	.string "From the inside.$"

SafariZone_HauntedCamp_Text_Campfire:
	.string "A cold fire pit. Someone left a\n"
	.string "marshmallow on a stick.\p"
	.string "It's still warm.$"

SafariZone_HauntedCamp_Text_Lantern:
	.string "A broken lantern. It only flickers\n"
	.string "when you look away.$"
