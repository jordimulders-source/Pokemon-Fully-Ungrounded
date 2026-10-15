ProfileMan_EventScript_Man::
	lock
	faceplayer
	goto_if_set FLAG_SYS_CHAT_USED, ProfileMan_EventScript_GivenProfileBefore
	msgbox ProfileMan_Text_CollectTrainerProfiles, MSGBOX_DEFAULT
	goto ProfileMan_EventScript_AskToSeeProfile
	end

ProfileMan_EventScript_AskToSeeProfile::
	msgbox ProfileMan_Text_MayISeeYourProfile, MSGBOX_DEFAULT
	multichoice 17, 6, MULTI_YESNOINFO_2, FALSE
	switch VAR_RESULT
	case 0, ProfileMan_EventScript_CreateProfile
	case 1, ProfileMan_EventScript_DeclineShowProfile
	case 2, ProfileMan_EventScript_Info
	case MULTI_B_PRESSED, ProfileMan_EventScript_DeclineShowProfile
	end

ProfileMan_EventScript_Info::
	msgbox ProfileMan_Text_EasyChatExplanation, MSGBOX_DEFAULT
	goto ProfileMan_EventScript_AskToSeeProfile
	end

ProfileMan_EventScript_CreateProfile::
	msgbox ProfileMan_Text_LetsSeeItThen, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, EASY_CHAT_TYPE_PROFILE
	call Common_ShowEasyChatScreen
	lock
	faceplayer
	goto_if_eq VAR_RESULT, 0, ProfileMan_EventScript_CancelShowProfile
	goto_if_eq VAR_RESULT, 1, ProfileMan_EventScript_ShowProfile
	end

ProfileMan_EventScript_CancelShowProfile::
	msgbox ProfileMan_Text_NotIntoItRightNow, MSGBOX_DEFAULT
	release
	end

ProfileMan_EventScript_ShowProfile::
	setvar VAR_0x8004, 0
	special ShowEasyChatProfile
	waitmessage
	delay 80
	msgbox ProfileMan_Text_FantasticProfile, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_PROFILE_MAN_NUGGET, ProfileMan_EventScript_ShowProfileEnd
	msgbox ProfileMan_Text_YourCutOfTheProfits, MSGBOX_DEFAULT
	giveitem ITEM_NUGGET
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_PROFILE_MAN_NUGGET
ProfileMan_EventScript_ShowProfileEnd::
	release
	end

ProfileMan_EventScript_DeclineShowProfile::
	msgbox ProfileMan_Text_ImagineYouWouldHaveWonderfulProfile, MSGBOX_DEFAULT
	release
	end

ProfileMan_EventScript_GivenProfileBefore::
	msgbox ProfileMan_Text_YouHaveWonderfulSmile, MSGBOX_DEFAULT
	goto ProfileMan_EventScript_AskToSeeNewProfile
	end

ProfileMan_EventScript_AskToSeeNewProfile::
	msgbox ProfileMan_Text_MayISeeYourNewProfile, MSGBOX_DEFAULT
	multichoice 17, 6, MULTI_YESNOINFO_2, FALSE
	switch VAR_RESULT
	case 0, ProfileMan_EventScript_CreateNewProfile
	case 1, ProfileMan_EventScript_DeclineNewProfile
	case 2, ProfileMan_EventScript_InfoNewProfile
	case MULTI_B_PRESSED, ProfileMan_EventScript_DeclineNewProfile
	end

ProfileMan_EventScript_InfoNewProfile::
	msgbox ProfileMan_Text_EasyChatExplanation, MSGBOX_DEFAULT
	goto ProfileMan_EventScript_AskToSeeNewProfile
	end

ProfileMan_EventScript_CreateNewProfile::
	msgbox ProfileMan_Text_EvenBetterThanLastProfile, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, EASY_CHAT_TYPE_PROFILE
	call Common_ShowEasyChatScreen
	lock
	faceplayer
	goto_if_eq VAR_RESULT, 0, ProfileMan_EventScript_CancelShowProfile
	goto_if_eq VAR_RESULT, 1, ProfileMan_EventScript_ShowProfile
	end

ProfileMan_EventScript_DeclineNewProfile::
	msgbox ProfileMan_Text_LikeProfileWayItIs, MSGBOX_DEFAULT
	release
	end

@ Unused
ProfileMan_EventScript_Ret::
	return

ProfileMan_Text_CollectTrainerProfiles:
	.string "Hello there, TRAINER! You've got a\n"
	.string "wonderful, very marketable smile.\p"
	.string "I collect the profiles of POKéMON\n"
	.string "TRAINERS. As a hobby. Not for money.\p"
	.string "…Mostly not for money.$"

ProfileMan_Text_MayISeeYourProfile:
	.string "Four words. That's all I need.\n"
	.string "So, may I see your profile?$"

ProfileMan_Text_EasyChatExplanation:
	.string "Pick four words. That's your profile.\p"
	.string "Choose a group, then a word. Four\n"
	.string "times. Like a dating app, but with\l"
	.string "fewer POKéMON in the photos.\p"
	.string "Don't overthink it. Nobody reads\n"
	.string "them. Except me. And my clients.$"

ProfileMan_Text_LetsSeeItThen:
	.string "Yes! Thank you!\n"
	.string "Let's see it. I'll take notes.$"

ProfileMan_Text_ImagineYouWouldHaveWonderfulProfile:
	.string "Oh, no, really?\p"
	.string "A mysterious one. That's fine.\n"
	.string "Mystery sells too.$"

ProfileMan_Text_NotIntoItRightNow:
	.string "Oh? Cold feet?\p"
	.string "That's fine. I'll just make one up\n"
	.string "for you. I've done it before.$"

ProfileMan_Text_YouHaveWonderfulSmile:
	.string "Oh! My favorite data point!\n"
	.string "Still smiling, I see.$"

ProfileMan_Text_MayISeeYourNewProfile:
	.string "Got a new profile for me?\n"
	.string "The old one's been sold. Twice.$"

ProfileMan_Text_EvenBetterThanLastProfile:
	.string "Yes! Thank you!\p"
	.string "Fresh data. My favorite smell.$"

ProfileMan_Text_LikeProfileWayItIs:
	.string "Oh, you like your profile the way it\n"
	.string "is. So do my clients. Big fans.$"

ProfileMan_Text_FantasticProfile:
	.string "F-fantastic!\p"
	.string "Four words, and I feel like I've\n"
	.string "known you my whole life.\p"
	.string "I'll print it, frame it, and sell it\n"
	.string "to a guy in LILYCOVE. He collects.\p"
	.string "Thank you!$"

@ Project Grounded: eenmalige Nugget na je eerste profiel (FLAG_RECEIVED_PROFILE_MAN_NUGGET)
ProfileMan_Text_YourCutOfTheProfits:
	.string "You're my first profile this week.\n"
	.string "Here. Your cut of the profits.\p"
	.string "Don't tell the others. They get paid\n"
	.string "in exposure.$"

@ Unused
ProfileMan_Text_YouKnowSecretSaying:
	.string "Oh?\n"
	.string "You know the secret saying!\p"
	.string "That means you're now a fellow member\n"
	.string "of the MYSTERY EVENT CLUB!$"
