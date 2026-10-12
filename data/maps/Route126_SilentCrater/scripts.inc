@ Project Grounded: verlaten kratertje bij Sootopolis (Route 126) met een verzegelde tweelingpoort van de Cave of Origin. Ingang: zwemgat in Underwater_Route126 37,9.
@ Kaart en scripts: tools/grounded/maptools/sootopolis_craters.py (niet met de hand bewerken).
Route126_SilentCrater_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route126_SilentCrater_OnResume
	.byte 0

Route126_SilentCrater_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE126, 37, 10
	setescapewarp MAP_UNDERWATER_ROUTE126, 37, 10
	end

Route126_SilentCrater_EventScript_Gate::
	msgbox Route126_SilentCrater_Text_Gate, MSGBOX_SIGN
	end

Route126_SilentCrater_EventScript_Sea::
	msgbox Route126_SilentCrater_Text_Sea, MSGBOX_SIGN
	end

Route126_SilentCrater_EventScript_Land::
	msgbox Route126_SilentCrater_Text_Land, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)
Route126_SilentCrater_Text_Gate:
	.string "A sealed gate, the twin of the one in\n"
	.string "SOOTOPOLIS. This door was never meant\l"
	.string "to open.\p"
	.string "Carved above it:\n"
	.string "'THE SKY CAME DOWN TO PART THEM. THEN\l"
	.string "IT WENT BACK UP. IT DID NOT ENJOY THE\l"
	.string "VISIT.'$"

Route126_SilentCrater_Text_Sea:
	.string "A worn statue of a whale. Its markings\n"
	.string "glow faintly when nobody is looking.\p"
	.string "The plaque:\n"
	.string "'SHE WANTED MORE SEA. THERE IS NEVER\l"
	.string "ENOUGH SEA. ASK THE SEA.'$"

Route126_SilentCrater_Text_Land:
	.string "A statue with claws, half melted.\p"
	.string "The plaque:\n"
	.string "'HE WANTED MORE LAND. HE GOT A VOLCANO.\l"
	.string "HE SULKED FOR AN AGE.'\p"
	.string "Scratched underneath, much newer:\n"
	.string "'REVERSION IS NOT A PHASE, MOM.'$"
