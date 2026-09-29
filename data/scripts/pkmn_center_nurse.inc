@ Project Grounded: snelle heal. Praten, één regel tekst, klaar. Geen animatie, geen ja/nee-vraag,
@ en de tekst sluit vanzelf zodat de speler direct verder kan lopen.
Common_EventScript_PkmnCenterNurse::
	lock
	faceplayer
	incrementgamestat GAME_STAT_USED_POKECENTER
	special HealPlayerParty
	callnative UpdateFollowingPokemon
	playse SE_USE_ITEM
	goto_if_unset FLAG_POKERUS_EXPLAINED, EventScript_PkmnCenterNurse_CheckPokerus
	goto EventScript_PkmnCenterNurse_QuickHealDone
	end

EventScript_PkmnCenterNurse_QuickHealDone::
	message gText_PkmnCenterQuickHeal
	waitmessage
	delay 30
	closemessage
	release
	end

EventScript_PkmnCenterNurse_CheckPokerus::
	specialvar VAR_RESULT, IsPokerusInParty
	goto_if_eq VAR_RESULT, FALSE, EventScript_PkmnCenterNurse_QuickHealDone
	setflag FLAG_POKERUS_EXPLAINED
	msgbox gText_PokerusExplanation, MSGBOX_DEFAULT
	goto EventScript_PkmnCenterNurse_QuickHealDone
	end

@ Wordt nog gebruikt na een white-out (EventScript_AfterWhiteOutHeal).
EventScript_PkmnCenterNurse_TakeAndHealPkmn::
	hidefollower 0
	applymovement VAR_0x800B, Movement_PkmnCenterNurse_Turn
	waitmovement 0
	dofieldeffect FLDEFF_POKECENTER_HEAL
.if OW_UNION_DISABLE_CHECK == FALSE && OW_FLAG_MOVE_UNION_ROOM_CHECK != 0
	setflag OW_FLAG_MOVE_UNION_ROOM_CHECK
	call CableClub_OnResume
	clearflag OW_FLAG_MOVE_UNION_ROOM_CHECK
.endif
	delay 16
	applymovement VAR_0x800B, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	special HealPlayerParty
	callnative UpdateFollowingPokemon
	return

Movement_PkmnCenterNurse_Bow:
	delay_4
	step_end

Movement_PkmnCenterNurse_Turn:
	walk_in_place_faster_left
	step_end
	
