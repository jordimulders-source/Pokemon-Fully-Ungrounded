Route136_Grotto_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route136_Grotto_OnResume
	.byte 0

@ Duiken in het kristalmeer: naar de onderwatertrog (bovenaan, onder de deur)
Route136_Grotto_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE136, 7, 2
	end
