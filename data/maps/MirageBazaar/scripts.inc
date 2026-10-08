@ Project Grounded: de Mirage Bazaar (Hoopa-quest, post-game). Een ring van Hoopa hangt na de Hall of Fame in de
@ zandstorm van Route 111; erdoor kom je in een bazaar op een luchtspiegeling. Salim verkoopt er wensen: versla hem
@ (de "vergoeding") en Hoopa Confined vervult er drie. Elke wens haalt het gewenste bij iemand anders weg (monkey's
@ paw). De derde wens bevrijdt Hoopa (of vraagt om oneindig veel wensen, wat op hetzelfde neerkomt): hij ringt de
@ Prison Bottle bij Salim weg, wordt Hoopa Unbound en ringt Salim en jou naar zijn schatkamer (MirageBazaar_Vault).
@ Kaarten: tools/grounded/maptools/mirage_bazaar.py. Flags: FLAG_GROUNDED(0-15) in include/constants/flags.h.

MirageBazaar_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MirageBazaar_OnTransition
	.byte 0

MirageBazaar_OnTransition:
	setflag FLAG_HOOPA_BAZAAR_VISITED
	clearflag FLAG_HIDE_MIRAGE_BAZAAR_SALIM
	clearflag FLAG_HIDE_MIRAGE_BAZAAR_HOOPA
	setflag FLAG_HIDE_MIRAGE_BAZAAR_VAULT_RING
	goto_if_set FLAG_HOOPA_QUEST_DONE, MirageBazaar_EventScript_AfterQuest
	goto_if_unset FLAG_HOOPA_UNBOUND, MirageBazaar_EventScript_TransitionEnd
	@ Hoopa Unbound en Salim zitten in de schatkamer; waar Hoopa zweefde, hangt een ring
	setflag FLAG_HIDE_MIRAGE_BAZAAR_SALIM
	setflag FLAG_HIDE_MIRAGE_BAZAAR_HOOPA
	clearflag FLAG_HIDE_MIRAGE_BAZAAR_VAULT_RING
MirageBazaar_EventScript_TransitionEnd:
	end

MirageBazaar_EventScript_AfterQuest:
	setflag FLAG_HIDE_MIRAGE_BAZAAR_HOOPA
	end

@ --- de ringen ---
MirageBazaar_EventScript_ExitRing::
	lockall
	playse SE_WARP_IN
	warp MAP_ROUTE111, 33, 58
	waitstate
	releaseall
	end

MirageBazaar_EventScript_VaultRing::
	lockall
	msgbox MirageBazaar_Text_VaultRing, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_IN
	warp MAP_MIRAGE_BAZAAR_VAULT, 11, 19
	waitstate
	releaseall
	end

MirageBazaar_EventScript_Sign::
	msgbox MirageBazaar_Text_Sign, MSGBOX_SIGN
	end

@ --- Salim: de vergoeding is een gevecht ---
MirageBazaar_EventScript_Salim::
	trainerbattle_single TRAINER_SALIM, MirageBazaar_Text_SalimIntro, MirageBazaar_Text_SalimDefeat, MirageBazaar_EventScript_SalimDefeated
	goto_if_set FLAG_HOOPA_QUEST_DONE, MirageBazaar_EventScript_SalimDone
	msgbox MirageBazaar_Text_SalimPost, MSGBOX_AUTOCLOSE
	end

MirageBazaar_EventScript_SalimDone::
	msgbox MirageBazaar_Text_SalimDone, MSGBOX_AUTOCLOSE
	end

MirageBazaar_EventScript_SalimDefeated::
	msgbox MirageBazaar_Text_SalimAfterBattle, MSGBOX_DEFAULT
	release
	end

@ --- Hoopa Confined: drie wensen ---
MirageBazaar_EventScript_CountWishes::
	setvar VAR_0x8004, 0
	call_if_set FLAG_HOOPA_WISH_RICHES, MirageBazaar_EventScript_AddWish
	call_if_set FLAG_HOOPA_WISH_POWER, MirageBazaar_EventScript_AddWish
	call_if_set FLAG_HOOPA_WISH_FAME, MirageBazaar_EventScript_AddWish
	call_if_set FLAG_HOOPA_WISH_SNACK, MirageBazaar_EventScript_AddWish
	return

MirageBazaar_EventScript_AddWish::
	addvar VAR_0x8004, 1
	return

MirageBazaar_EventScript_Hoopa::
	lock
	faceplayer
	playmoncry SPECIES_HOOPA_CONFINED, CRY_MODE_NORMAL
	goto_if_not_defeated TRAINER_SALIM, MirageBazaar_EventScript_HoopaNotYet
	call MirageBazaar_EventScript_CountWishes
	goto_if_ge VAR_0x8004, 2, MirageBazaar_EventScript_HoopaLastWish
	call_if_eq VAR_0x8004, 0, MirageBazaar_EventScript_HoopaFirstText
	call_if_eq VAR_0x8004, 1, MirageBazaar_EventScript_HoopaSecondText
	waitmoncry
	call_if_unset FLAG_HOOPA_WISH_RICHES, MirageBazaar_EventScript_PushRiches
	call_if_unset FLAG_HOOPA_WISH_POWER, MirageBazaar_EventScript_PushPower
	call_if_unset FLAG_HOOPA_WISH_FAME, MirageBazaar_EventScript_PushFame
	call_if_unset FLAG_HOOPA_WISH_SNACK, MirageBazaar_EventScript_PushSnack
	dynmultipush MirageBazaar_Text_OptNotNow, 9
	dynmultistack 0, 0, FALSE, 5, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	closemessage
	switch VAR_RESULT
	case 0, MirageBazaar_EventScript_WishRiches
	case 1, MirageBazaar_EventScript_WishPower
	case 2, MirageBazaar_EventScript_WishFame
	case 3, MirageBazaar_EventScript_WishSnack
	msgbox MirageBazaar_Text_HoopaLater, MSGBOX_DEFAULT
	release
	end

MirageBazaar_EventScript_HoopaFirstText::
	message MirageBazaar_Text_HoopaFirst
	waitmessage
	return

MirageBazaar_EventScript_HoopaSecondText::
	message MirageBazaar_Text_HoopaSecond
	waitmessage
	return

MirageBazaar_EventScript_PushRiches::
	dynmultipush MirageBazaar_Text_OptRiches, 0
	return

MirageBazaar_EventScript_PushPower::
	dynmultipush MirageBazaar_Text_OptPower, 1
	return

MirageBazaar_EventScript_PushFame::
	dynmultipush MirageBazaar_Text_OptFame, 2
	return

MirageBazaar_EventScript_PushSnack::
	dynmultipush MirageBazaar_Text_OptSnack, 3
	return

MirageBazaar_EventScript_HoopaNotYet::
	waitmoncry
	msgbox MirageBazaar_Text_HoopaNotYet, MSGBOX_DEFAULT
	release
	end

@ Hoopa opent een ring: even op en neer springen met een teleportgeluid
MirageBazaar_EventScript_RingOpens::
	playse SE_M_TELEPORT
	applymovement LOCALID_MIRAGE_BAZAAR_HOOPA, MirageBazaar_Movement_HoopaRing
	waitmovement 0
	return

MirageBazaar_Movement_HoopaRing:
	jump_in_place_down
	jump_in_place_down
	step_end

MirageBazaar_EventScript_WishRiches::
	setflag FLAG_HOOPA_WISH_RICHES
	msgbox MirageBazaar_Text_WishRiches, MSGBOX_DEFAULT
	call MirageBazaar_EventScript_RingOpens
	giveitem ITEM_BIG_NUGGET
	msgbox MirageBazaar_Text_WishRichesTwist, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_AfterWish

MirageBazaar_EventScript_WishPower::
	setflag FLAG_HOOPA_WISH_POWER
	msgbox MirageBazaar_Text_WishPower, MSGBOX_DEFAULT
	call MirageBazaar_EventScript_RingOpens
	giveitem ITEM_CHOICE_BAND
	msgbox MirageBazaar_Text_WishPowerTwist, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_AfterWish

MirageBazaar_EventScript_WishFame::
	setflag FLAG_HOOPA_WISH_FAME
	msgbox MirageBazaar_Text_WishFame, MSGBOX_DEFAULT
	call MirageBazaar_EventScript_RingOpens
	msgbox MirageBazaar_Text_WishFameTwist, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_AfterWish

MirageBazaar_EventScript_WishSnack::
	setflag FLAG_HOOPA_WISH_SNACK
	msgbox MirageBazaar_Text_WishSnack, MSGBOX_DEFAULT
	call MirageBazaar_EventScript_RingOpens
	giveitem ITEM_LAVA_COOKIE, 3
	msgbox MirageBazaar_Text_WishSnackTwist, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_AfterWish

MirageBazaar_EventScript_AfterWish::
	call MirageBazaar_EventScript_CountWishes
	call_if_eq VAR_0x8004, 1, MirageBazaar_EventScript_TwoLeft
	call_if_eq VAR_0x8004, 2, MirageBazaar_EventScript_OneLeft
	release
	end

MirageBazaar_EventScript_TwoLeft::
	msgbox MirageBazaar_Text_TwoLeft, MSGBOX_DEFAULT
	return

MirageBazaar_EventScript_OneLeft::
	msgbox MirageBazaar_Text_OneLeft, MSGBOX_DEFAULT
	return

@ --- de derde wens: vrijheid (of oneindig veel wensen, wat hetzelfde blijkt) ---
MirageBazaar_EventScript_HoopaLastWish::
	waitmoncry
	message MirageBazaar_Text_LastWish
	waitmessage
	dynmultichoice 0, 0, FALSE, 3, 0, DYN_MULTICHOICE_CB_NONE, MirageBazaar_Text_OptFree, MirageBazaar_Text_OptInfinite, MirageBazaar_Text_OptNotYet
	closemessage
	switch VAR_RESULT
	case 0, MirageBazaar_EventScript_WishFree
	case 1, MirageBazaar_EventScript_WishInfinite
	msgbox MirageBazaar_Text_HoopaLater, MSGBOX_DEFAULT
	release
	end

MirageBazaar_EventScript_WishFree::
	msgbox MirageBazaar_Text_WishFree, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_Unbind

MirageBazaar_EventScript_WishInfinite::
	msgbox MirageBazaar_Text_WishInfinite, MSGBOX_DEFAULT
	goto MirageBazaar_EventScript_Unbind

MirageBazaar_EventScript_Unbind::
	closemessage
	applymovement LOCALID_MIRAGE_BAZAAR_SALIM, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_MIRAGE_BAZAAR_SALIM, Common_Movement_FaceRight
	waitmovement 0
	msgbox MirageBazaar_Text_SalimNo, MSGBOX_DEFAULT
	closemessage
	call MirageBazaar_EventScript_RingOpens
	msgbox MirageBazaar_Text_BottleStolen, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HOOPA_UNBOUND
	fadescreenswapbuffers FADE_TO_WHITE
	playmoncry SPECIES_HOOPA_UNBOUND, CRY_MODE_ENCOUNTER
	removeobject LOCALID_MIRAGE_BAZAAR_HOOPA
	setflag FLAG_HIDE_MIRAGE_BAZAAR_HOOPA
	waitmoncry
	fadescreenswapbuffers FADE_FROM_WHITE
	msgbox MirageBazaar_Text_HoopaUnbound, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	removeobject LOCALID_MIRAGE_BAZAAR_SALIM
	setflag FLAG_HIDE_MIRAGE_BAZAAR_SALIM
	delay 30
	msgbox MirageBazaar_Text_RingUnderYou, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_HOOPA_VAULT_HOOPA
	clearflag FLAG_HIDE_HOOPA_VAULT_SALIM
	playse SE_WARP_IN
	warp MAP_MIRAGE_BAZAAR_VAULT, 11, 19
	waitstate
	release
	end

@ --- de rest van de bazaar ---
MirageBazaar_EventScript_Mart::
	lock
	faceplayer
	message MirageBazaar_Text_MartIntro
	waitmessage
	pokemart MirageBazaar_Pokemart
	msgbox MirageBazaar_Text_MartBye, MSGBOX_DEFAULT
	release
	end

	.align 2
MirageBazaar_Pokemart:
	.2byte ITEM_SOFT_SAND
	.2byte ITEM_SMOOTH_ROCK
	.2byte ITEM_SAFETY_GOGGLES
	.2byte ITEM_LAVA_COOKIE
	.2byte ITEM_NONE

MirageBazaar_EventScript_RugSeller::
	msgbox MirageBazaar_Text_RugSeller, MSGBOX_NPC
	end

MirageBazaar_EventScript_FortuneTeller::
	goto_if_set FLAG_HOOPA_QUEST_DONE, MirageBazaar_EventScript_FortuneTellerDone
	msgbox MirageBazaar_Text_FortuneTeller, MSGBOX_NPC
	end

MirageBazaar_EventScript_FortuneTellerDone::
	msgbox MirageBazaar_Text_FortuneTellerDone, MSGBOX_NPC
	end

MirageBazaar_EventScript_Refunds::
	msgbox MirageBazaar_Text_Refunds, MSGBOX_NPC
	end

MirageBazaar_EventScript_Hippowdon::
	lock
	faceplayer
	playmoncry SPECIES_HIPPOWDON, CRY_MODE_NORMAL
	msgbox MirageBazaar_Text_Hippowdon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

MirageBazaar_EventScript_Kid::
	msgbox MirageBazaar_Text_Kid, MSGBOX_NPC
	end

MirageBazaar_EventScript_Shopper::
	msgbox MirageBazaar_Text_Shopper, MSGBOX_NPC
	end

MirageBazaar_EventScript_MirageFisher::
	msgbox MirageBazaar_Text_MirageFisher, MSGBOX_NPC
	end

@ ====================================================================== teksten
MirageBazaar_Text_Sign:
	.string "MIRAGE BAZAAR\p"
	.string "Everything for sale.\n"
	.string "Nothing for keeps.\p"
	.string "Shoplifters will be prosecuted by\n"
	.string "the original owners.$"

MirageBazaar_Text_VaultRing:
	.string "The ring HOOPA left behind hums.\n"
	.string "It smells like other people's stuff.$"

MirageBazaar_Text_SalimIntro:
	.string "Welcome to the MIRAGE BAZAAR,\n"
	.string "friend. I am SALIM.\p"
	.string "Everything here is for sale.\n"
	.string "Nothing here is mine.\p"
	.string "The little one under my awning is\n"
	.string "HOOPA. He grants wishes.\l"
	.string "Three per customer.\p"
	.string "There is a fee. The fee is a\n"
	.string "battle. The refund policy is a myth.$"

MirageBazaar_Text_SalimDefeat:
	.string "Paid in full. I hate it when that\n"
	.string "happens.$"

MirageBazaar_Text_SalimAfterBattle:
	.string "SALIM: Go on, talk to HOOPA. Wish\n"
	.string "for something small.\p"
	.string "People who wish big end up as a\n"
	.string "warning on my business card.$"

MirageBazaar_Text_SalimPost:
	.string "SALIM: Three wishes. And don't wish\n"
	.string "for more wishes.\p"
	.string "Everybody wishes for more wishes.\n"
	.string "It never ends well. For me.$"

MirageBazaar_Text_SalimDone:
	.string "SALIM: Half my stock came back from\n"
	.string "the vault with the original price\l"
	.string "tags still on.\p"
	.string "Awkward. Excellent margins, though.$"

MirageBazaar_Text_HoopaNotYet:
	.string "HOOPA juggles a tiny ring.\p"
	.string "It looks at you. Then at SALIM.\n"
	.string "Then at your wallet.$"

MirageBazaar_Text_HoopaFirst:
	.string "HOOPA: Hoopa grants wishes! Hoopa\n"
	.string "is VERY good at wishes!\p"
	.string "Hoopa never makes anything. Hoopa\n"
	.string "just knows where it already is.\p"
	.string "What do you wish for?$"

MirageBazaar_Text_HoopaSecond:
	.string "HOOPA: Wish number two!\n"
	.string "Hoopa is warmed up!$"

MirageBazaar_Text_HoopaLater:
	.string "HOOPA: Hoopa waits. Hoopa is very\n"
	.string "patient. Hoopa is three thousand.$"

MirageBazaar_Text_OptRiches:
	.string "RICHES$"

MirageBazaar_Text_OptPower:
	.string "POWER$"

MirageBazaar_Text_OptFame:
	.string "FAME$"

MirageBazaar_Text_OptSnack:
	.string "A SNACK$"

MirageBazaar_Text_OptNotNow:
	.string "NOT NOW$"

MirageBazaar_Text_WishRiches:
	.string "HOOPA: Riches! Easy!\p"
	.string "HOOPA reaches into a ring up to\n"
	.string "the shoulder.$"

MirageBazaar_Text_WishRichesTwist:
	.string "In RUSTBORO, a RICH BOY's piggy bank\n"
	.string "just got very light.\p"
	.string "He'll be fine. He has eleven more.\n"
	.string "He is checking all eleven.$"

MirageBazaar_Text_WishPower:
	.string "HOOPA: Power! Hoopa knows a guy!\p"
	.string "A ring opens over DEWFORD.\n"
	.string "Muffled shouting.$"

MirageBazaar_Text_WishPowerTwist:
	.string "In DEWFORD GYM, BRAWLY is looking\n"
	.string "for his headband.\p"
	.string "He is doing push-ups to cope.\n"
	.string "It's not working. He's very strong.$"

MirageBazaar_Text_WishFame:
	.string "HOOPA: Fame! Hoopa takes it from\n"
	.string "someone who has too much!$"

MirageBazaar_Text_WishFameTwist:
	.string "GABBY's microphone falls through\n"
	.string "the ring. Then GABBY's fame.\p"
	.string "You are now famous. Everyone in the\n"
	.string "bazaar knows your name.\p"
	.string "They all want a refund from you,\n"
	.string "specifically.$"

MirageBazaar_Text_WishSnack:
	.string "HOOPA: A snack! Small wish. Hoopa\n"
	.string "likes small wishes. Nobody cries.$"

MirageBazaar_Text_WishSnackTwist:
	.string "In LAVARIDGE, an old lady is\n"
	.string "crying at her oven.\p"
	.string "The cookies were for her grandson.\n"
	.string "He was finally coming home today.$"

MirageBazaar_Text_TwoLeft:
	.string "HOOPA: Two wishes left!\n"
	.string "Hoopa is having so much fun!$"

MirageBazaar_Text_OneLeft:
	.string "HOOPA: One wish left. The big one.\n"
	.string "Hoopa has a suggestion.$"

MirageBazaar_Text_LastWish:
	.string "HOOPA: Last wish! Free Hoopa!\p"
	.string "Take the little bottle from SALIM.\n"
	.string "Hoopa gets big again.\p"
	.string "Big Hoopa grants BIG wishes.$"

MirageBazaar_Text_OptFree:
	.string "SET HOOPA FREE$"

MirageBazaar_Text_OptInfinite:
	.string "INFINITE WISHES$"

MirageBazaar_Text_OptNotYet:
	.string "NOT YET$"

MirageBazaar_Text_WishFree:
	.string "HOOPA: YES! Best customer ever!$"

MirageBazaar_Text_WishInfinite:
	.string "HOOPA: Ha! Everybody wishes that.\p"
	.string "Okay! Infinite wishes needs an\n"
	.string "infinite Hoopa.\p"
	.string "Hoopa needs the bottle.$"

MirageBazaar_Text_SalimNo:
	.string "SALIM: Wait. WAIT. That bottle is\n"
	.string "not for sale-$"

MirageBazaar_Text_BottleStolen:
	.string "HOOPA rings the PRISON BOTTLE right\n"
	.string "out of SALIM's sash.\p"
	.string "The cork pops.$"

MirageBazaar_Text_HoopaUnbound:
	.string "HOOPA: HOOPA IS FREE!\n"
	.string "HOOPA WANTS EVERYTHING!\p"
	.string "Rings open everywhere. The stock.\n"
	.string "The bottle. SALIM.$"

MirageBazaar_Text_RingUnderYou:
	.string "A ring opens under your feet.\p"
	.string "Apparently you are also stock.$"

MirageBazaar_Text_MartIntro:
	.string "Everything's authentic. Authentically\n"
	.string "from somewhere else.$"

MirageBazaar_Text_MartBye:
	.string "If the owner asks, you've never\n"
	.string "seen me. I've never seen him either.$"

MirageBazaar_Text_RugSeller:
	.string "This rug flies.\p"
	.string "Not well. Mostly downward. But with\n"
	.string "enormous confidence.$"

MirageBazaar_Text_FortuneTeller:
	.string "I see your future. You make a wish.\n"
	.string "Somewhere, someone else pays for it.\p"
	.string "That's not a prophecy. That's just\n"
	.string "how this bazaar works.$"

MirageBazaar_Text_FortuneTellerDone:
	.string "I see your future. You put HOOPA\n"
	.string "in your party.\p"
	.string "Your stuff starts going missing.\n"
	.string "You can't prove anything.$"

MirageBazaar_Text_Refunds:
	.string "I wished for a girlfriend.\p"
	.string "HOOPA stole one from FORTREE.\n"
	.string "She still lives up a tree.\p"
	.string "So do I now. It's fine.\n"
	.string "It's a nice tree.$"

MirageBazaar_Text_Hippowdon:
	.string "HIPPOWDON is carrying forty crates\n"
	.string "of sand.\p"
	.string "To the desert. The business model\n"
	.string "has some issues.$"

MirageBazaar_Text_Kid:
	.string "Everything here is stolen. That's\n"
	.string "why it's so cheap!\p"
	.string "My dad says that's called\n"
	.string "“the economy.”$"

MirageBazaar_Text_Shopper:
	.string "I came for a magic lamp. They only\n"
	.string "sell bottles.\p"
	.string "I rubbed one anyway. The merchant\n"
	.string "filed a complaint.$"

MirageBazaar_Text_MirageFisher:
	.string "I've fished this lake for six years.\p"
	.string "It's a mirage. There's no water.\n"
	.string "I'm not stopping now. Sunk cost.$"
