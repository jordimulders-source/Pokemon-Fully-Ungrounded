EventScript_TV::
	lockall
	incrementgamestat GAME_STAT_WATCHED_TV
	special ResetTVShowState
	goto_if_unset FLAG_SYS_TV_START, EventScript_MomDadMightLikeThis1
	goto_if_set FLAG_SYS_TV_WATCH, EventScript_MomDadMightLikeThis1
	specialvar VAR_RESULT, IsGabbyAndTyShowOnTheAir
	goto_if_eq VAR_RESULT, TRUE, EventScript_DoInSearchOfTrainers
	goto EventScript_TryDoPokeNews
	end

EventScript_TryDoTVShow::
	specialvar VAR_0x8004, GetRandomActiveShowIdx
	goto_if_eq VAR_0x8004, 255, EventScript_MomDadMightLikeThis2
	specialvar VAR_RESULT, GetNextActiveShowIfMassOutbreak
	goto_if_eq VAR_RESULT, 255, EventScript_MomDadMightLikeThis2
	copyvar VAR_0x8004, VAR_RESULT
	specialvar VAR_RESULT, GetSelectedTVShow
	goto_if_ne VAR_RESULT, 0, EventScript_DoTVShow
	end

EventScript_MomDadMightLikeThis1::
	special GetMomOrDadStringForTVMessage
	call EventScript_MomOrDadTVText
	special TurnOffTVScreen
	releaseall
	end

@ The following is a loop for the TV show messages
@ VAR_RESULT is set to TRUE when the show has printed its final message
EventScript_DoTVShow::
	special DoTVShow
	waitmessage
	waitbuttonpress
	goto_if_ne VAR_RESULT, TRUE, EventScript_DoTVShow
	goto EventScript_TurnOffTV
	end

EventScript_TurnOffTV::
	special TurnOffTVScreen
	setflag FLAG_SYS_TV_WATCH
	releaseall
	end

EventScript_MomDadMightLikeThis2::
	special GetMomOrDadStringForTVMessage
	call EventScript_MomOrDadTVText
	goto EventScript_TurnOffTV
	end

EventScript_TryDoPokeNews::
	special DoPokeNews
	goto_if_eq VAR_RESULT, FALSE, EventScript_TryDoTVShow
	waitmessage
	waitbuttonpress
	goto EventScript_TurnOffTV
	end

EventScript_DoInSearchOfTrainers::
	special DoTVShowInSearchOfTrainers
	waitmessage
	waitbuttonpress
	goto_if_eq VAR_RESULT, 0, EventScript_DoInSearchOfTrainers
	goto EventScript_TurnOffTV
	end

@ Project Grounded: eigen tekst voor Mom en Dad (VAR_TEMP_3: 1 = Mom, 2 = Dad, gezet door GetMomOrDadStringForTVMessage)
EventScript_MomOrDadTVText::
	goto_if_eq VAR_TEMP_3, 2, EventScript_DadTVText
	msgbox gText_MomMightLikeThisProgram, MSGBOX_DEFAULT
	return

EventScript_DadTVText::
	msgbox gText_DadMightLikeThisProgram, MSGBOX_DEFAULT
	return
