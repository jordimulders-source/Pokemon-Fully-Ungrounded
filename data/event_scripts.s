#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/apprentice.h"
#include "constants/apricorn_tree.h"
#include "constants/battle.h"
#include "constants/battle_arena.h"
#include "constants/battle_dome.h"
#include "constants/battle_factory.h"
#include "constants/battle_frontier.h"
#include "constants/battle_palace.h"
#include "constants/battle_pike.h"
#include "constants/battle_pyramid.h"
#include "constants/battle_special.h"
#include "constants/battle_tent.h"
#include "constants/battle_tower.h"
#include "constants/berry.h"
#include "constants/cable_club.h"
#include "constants/coins.h"
#include "constants/comparison_operators.h"
#include "constants/contest.h"
#include "constants/daycare.h"
#include "constants/decorations.h"
#include "constants/difficulty.h"
#include "constants/easy_chat.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/fame_checker.h"
#include "constants/field_effects.h"
#include "constants/field_move.h"
#include "constants/field_poison.h"
#include "constants/field_specials.h"
#include "constants/field_tasks.h"
#include "constants/field_weather.h"
#include "constants/flags.h"
#include "constants/follower_npc.h"
#include "constants/frontier_util.h"
#include "constants/game_stat.h"
#include "constants/item.h"
#include "constants/items.h"
#include "constants/heal_locations.h"
#include "constants/layouts.h"
#include "constants/lilycove_lady.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/mass_outbreak.h"
#include "constants/mauville_old_man.h"
#include "constants/metatile_labels.h"
#include "constants/move_relearner.h"
#include "constants/moves.h"
#include "constants/mystery_gift.h"
#include "constants/party_menu.h"
#include "constants/pokeball.h"
#include "constants/pokedex.h"
#include "constants/pokemon.h"
#include "constants/pokemon_size_record.h"
#include "constants/random_mon_generation.h"
#include "constants/rtc.h"
#include "constants/roulette.h"
#include "constants/script_menu.h"
#include "constants/seagallop.h"
#include "constants/secret_bases.h"
#include "constants/siirtc.h"
#include "constants/songs.h"
#include "constants/sound.h"
#include "constants/species.h"
#include "constants/trade.h"
#include "constants/trainer_hill.h"
#include "constants/trainer_tower.h"
#include "constants/trainers.h"
#include "constants/trainer_card.h"
#include "constants/tv.h"
#include "constants/union_room.h"
#include "constants/vars.h"
#include "constants/weather.h"
#include "constants/speaker_names.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.section script_data, "aw", %progbits

	.set ALLOCATE_SCRIPT_CMD_TABLE, 1
	.include "data/script_cmd_table.inc"

.align 2
gSpecialVars::
	.4byte gSpecialVar_0x8000
	.4byte gSpecialVar_0x8001
	.4byte gSpecialVar_0x8002
	.4byte gSpecialVar_0x8003
	.4byte gSpecialVar_0x8004
	.4byte gSpecialVar_0x8005
	.4byte gSpecialVar_0x8006
	.4byte gSpecialVar_0x8007
	.4byte gSpecialVar_0x8008
	.4byte gSpecialVar_0x8009
	.4byte gSpecialVar_0x800A
	.4byte gSpecialVar_0x800B
	.4byte gSpecialVar_Facing
	.4byte gSpecialVar_Result
	.4byte gSpecialVar_ItemId
	.4byte gSpecialVar_LastTalked
	.4byte gSpecialVar_ContestRank
	.4byte gSpecialVar_ContestCategory
	.4byte gSpecialVar_MonBoxId
	.4byte gSpecialVar_MonBoxPos
	.4byte gSpecialVar_Unused_0x8014
	.4byte gTrainerBattleParameter + 2 // gTrainerBattleParameter.params.opponentA

	.purgem def_special
	.set ALLOCATE_SPECIAL_TABLE, 1
	.include "data/specials.inc"

gStdScripts::
	.4byte Std_ObtainItem              @ STD_OBTAIN_ITEM
	.4byte Std_FindItem                @ STD_FIND_ITEM
	.4byte Std_MsgboxNPC               @ MSGBOX_NPC
	.4byte Std_MsgboxSign              @ MSGBOX_SIGN
	.4byte Std_MsgboxDefault           @ MSGBOX_DEFAULT
	.4byte Std_MsgboxYesNo             @ MSGBOX_YESNO
	.4byte Std_MsgboxAutoclose         @ MSGBOX_AUTOCLOSE
	.4byte Std_ObtainDecoration        @ STD_OBTAIN_DECORATION
	.4byte Std_RegisteredInMatchCall   @ STD_REGISTER_MATCH_CALL
	.4byte Std_MsgboxGetPoints         @ MSGBOX_GETPOINTS
	.4byte Std_MsgboxPokenav           @ MSGBOX_POKENAV
	.4byte Std_PutItemAway             @ STD_PUT_ITEM_AWAY
	.4byte Std_ReceivedItem            @ STD_RECEIVED_ITEM
gStdScripts_End::

	.include "data/scripts/shared_secret_base.inc"

.if IS_FRLG

@ FRLG scripts
	.include "data/maps/BattleColosseum_2P_Frlg/scripts.inc"
	.include "data/maps/TradeCenter_Frlg/scripts.inc"
	.include "data/maps/RecordCorner_Frlg/scripts.inc"
	.include "data/maps/BattleColosseum_4P_Frlg/scripts.inc"
	.include "data/maps/UnionRoom_Frlg/scripts.inc"
	.include "data/maps/ViridianForest_Frlg/scripts.inc"
	.include "data/maps/MtMoon_1F_Frlg/scripts.inc"
	.include "data/maps/MtMoon_B1F_Frlg/scripts.inc"
	.include "data/maps/MtMoon_B2F_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Exterior_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_3F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Deck_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Kitchen_Frlg/scripts.inc"
	.include "data/maps/SSAnne_CaptainsOffice_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room7_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room6_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room6_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_NorthSouthTunnel_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_WestEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_EastWestTunnel_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_EastEntrance_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_B1F_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_1F_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_2F_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_3F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B1F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B2F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B3F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B4F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_Elevator_Frlg/scripts.inc"
	.include "data/maps/SilphCo_1F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_2F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_3F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_4F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_5F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_6F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_7F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_8F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_9F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_10F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_11F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_Elevator_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_1F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_2F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_3F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_B1F_Frlg/scripts.inc"
	.include "data/maps/SafariZone_Center_Frlg/scripts.inc"
	.include "data/maps/SafariZone_East_Frlg/scripts.inc"
	.include "data/maps/SafariZone_North_Frlg/scripts.inc"
	.include "data/maps/SafariZone_West_Frlg/scripts.inc"
	.include "data/maps/SafariZone_Center_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_East_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_North_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_West_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_SecretHouse_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_1F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_2F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_B1F_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_LoreleisRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_BrunosRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_AgathasRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_LancesRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_ChampionsRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_HallOfFame_Frlg/scripts.inc"
	.include "data/maps/RockTunnel_1F_Frlg/scripts.inc"
	.include "data/maps/RockTunnel_B1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B2F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B3F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_1F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_2F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_3F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_5F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_6F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_7F_Frlg/scripts.inc"
	.include "data/maps/PowerPlant_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B4F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_Exterior_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_2F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_3F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_Summit_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B5F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B2F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B3F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B1F_Stairs_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B2F_Stairs_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_BerryForest_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_Entrance_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_B1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_Back_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B2F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B3F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B4F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_SapphireRoom_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PatternBush_Frlg/scripts.inc"
	.include "data/maps/SixIsland_AlteringCave_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Exterior_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_1F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_2F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_3F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_4F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_5F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_6F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_7F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_8F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_Roof_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_Lobby_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_Elevator_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Entrance_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room1_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room2_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room3_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room4_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room5_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room6_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room7_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room8_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room9_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room10_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room11_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room12_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room13_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room14_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_MoneanChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_LiptooChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_WeepthChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_DilfordChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_ScufibChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_RixyChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_ViapoisChamber_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_DunsparceTunnel_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_TanobyKey_Frlg/scripts.inc"
	.include "data/maps/NavelRock_1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Summit_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Base_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_2F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_3F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_4F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_5F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B2F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B3F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B4F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B5F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B6F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B7F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B8F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B9F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B10F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B11F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_B1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Fork_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Exterior_Frlg/scripts.inc"
	.include "data/maps/OneIsland_KindleRoad_EmberSpa_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Harbor_Frlg/scripts.inc"
	.include "data/maps/PalletTown_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_Exterior_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Connection_Frlg/scripts.inc"
	.include "data/maps/OneIsland_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Frlg/scripts.inc"
	.include "data/maps/Route1_Frlg/scripts.inc"
	.include "data/maps/Route2_Frlg/scripts.inc"
	.include "data/maps/Route3_Frlg/scripts.inc"
	.include "data/maps/Route4_Frlg/scripts.inc"
	.include "data/maps/Route5_Frlg/scripts.inc"
	.include "data/maps/Route6_Frlg/scripts.inc"
	.include "data/maps/Route7_Frlg/scripts.inc"
	.include "data/maps/Route8_Frlg/scripts.inc"
	.include "data/maps/Route9_Frlg/scripts.inc"
	.include "data/maps/Route10_Frlg/scripts.inc"
	.include "data/maps/Route11_Frlg/scripts.inc"
	.include "data/maps/Route12_Frlg/scripts.inc"
	.include "data/maps/Route13_Frlg/scripts.inc"
	.include "data/maps/Route14_Frlg/scripts.inc"
	.include "data/maps/Route15_Frlg/scripts.inc"
	.include "data/maps/Route16_Frlg/scripts.inc"
	.include "data/maps/Route17_Frlg/scripts.inc"
	.include "data/maps/Route18_Frlg/scripts.inc"
	.include "data/maps/Route19_Frlg/scripts.inc"
	.include "data/maps/Route20_Frlg/scripts.inc"
	.include "data/maps/Route21_North_Frlg/scripts.inc"
	.include "data/maps/Route21_South_Frlg/scripts.inc"
	.include "data/maps/Route22_Frlg/scripts.inc"
	.include "data/maps/Route23_Frlg/scripts.inc"
	.include "data/maps/Route24_Frlg/scripts.inc"
	.include "data/maps/Route25_Frlg/scripts.inc"
	.include "data/maps/OneIsland_KindleRoad_Frlg/scripts.inc"
	.include "data/maps/OneIsland_TreasureBeach_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_CapeBrink_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_BondBridge_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Port_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_ResortGorgeous_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_WaterLabyrinth_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Meadow_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_MemorialPillar_Frlg/scripts.inc"
	.include "data/maps/SixIsland_OutcastIsland_Frlg/scripts.inc"
	.include "data/maps/SixIsland_GreenPath_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_Frlg/scripts.inc"
	.include "data/maps/SixIsland_RuinValley_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TrainerTower_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_Entrance_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_Frlg/scripts.inc"
	.include "data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc"
	.include "data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc"
	.include "data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc"
	.include "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_House_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Gym_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_School_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Mart_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Museum_1F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Museum_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Gym_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Mart_Frlg/scripts.inc"
	.include "data/maps/PewterCity_House1_Frlg/scripts.inc"
	.include "data/maps/PewterCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_House2_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House1_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House2_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House3_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Gym_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_BikeShop_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Mart_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House4_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House5_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_House1_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_House2_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_Mart_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House1_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonFanClub_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House2_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Mart_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Gym_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House3_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_3F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_4F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_5F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_Roof_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_Elevator_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_3F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_Roof_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_RoofRoom_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_GameCorner_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_GameCorner_PrizeRoom_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Gym_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Restaurant_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_House1_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Hotel_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Mart_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_SafariZone_Office_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Gym_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House1_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_WardensHouse_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House2_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House3_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Gym_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_Entrance_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_Lounge_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_ExperimentRoom_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_CopycatsHouse_1F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_CopycatsHouse_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Dojo_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Gym_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_House_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Mart_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_MrPsychicsHouse_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonTrainerFanClub_Frlg/scripts.inc"
	.include "data/maps/Route2_ViridianForest_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route2_House_Frlg/scripts.inc"
	.include "data/maps/Route2_EastBuilding_Frlg/scripts.inc"
	.include "data/maps/Route2_ViridianForest_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route4_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/Route4_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/Route5_PokemonDayCare_Frlg/scripts.inc"
	.include "data/maps/Route5_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route6_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route6_UnusedHouse_Frlg/scripts.inc"
	.include "data/maps/Route7_EastEntrance_Frlg/scripts.inc"
	.include "data/maps/Route8_WestEntrance_Frlg/scripts.inc"
	.include "data/maps/Route10_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/Route10_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/Route11_EastEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route11_EastEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route12_NorthEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route12_NorthEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route12_FishingHouse_Frlg/scripts.inc"
	.include "data/maps/Route15_WestEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route15_WestEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route16_House_Frlg/scripts.inc"
	.include "data/maps/Route16_NorthEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route16_NorthEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route18_EastEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route18_EastEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route22_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route25_SeaCottage_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_House_Room1_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_House_Room2_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/OneIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/OneIsland_House1_Frlg/scripts.inc"
	.include "data/maps/OneIsland_House2_Frlg/scripts.inc"
	.include "data/maps/OneIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_JoyfulGameCorner_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_House_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House1_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House2_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House3_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House4_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House5_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonDayCare_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_House1_Frlg/scripts.inc"
	.include "data/maps/FourIsland_LoreleisHouse_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FourIsland_House2_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_House1_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_House2_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/SixIsland_House_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_ResortGorgeous_House_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_CapeBrink_House_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_House1_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_House2_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_House_Frlg/scripts.inc"

	.include "data/scripts/trainer_tower.inc"
	.include "data/scripts/fame_checker_frlg.inc"
	.include "data/text/fame_checker_frlg.inc"
	.include "data/scripts/item_ball_scripts_frlg.inc"
	.include "data/scripts/silphco_doors.inc"
	.include "data/scripts/move_tutors_frlg.inc"
	.include "data/scripts/cable_club_frlg.inc"
	.include "data/scripts/trainer_card_frlg.inc"
	.include "data/text/trainer_card_frlg.inc"
	.include "data/scripts/mystery_event_club.inc"
	.include "data/scripts/day_care_frlg.inc"
	.include "data/text/day_care_frlg.inc"
	.include "data/scripts/seagallop.inc"
	.include "data/scripts/static_pokemon.inc"
	.include "data/scripts/aide.inc"
	.include "data/scripts/pokemon_mansion.inc"
	.include "data/scripts/pokemon_league.inc"
	.include "data/scripts/route23.inc"
	.include "data/text/new_game_intro_frlg.inc"
	.include "data/scripts/trainers_frlg.inc"
	.include "data/text/trainers_frlg.inc"
	.include "data/text/ingame_trade_frlg.inc"
	.include "data/scripts/flavor_text.inc"
	.include "data/scripts/pkmn_center_nurse_frlg.inc"

.endif

	.include "data/scripts/std_msgbox.inc"
	.include "data/scripts/trainer_battle.inc"
	.include "data/scripts/new_game.inc"
	.include "data/scripts/hall_of_fame.inc"
	.include "data/scripts/hall_of_fame_frlg.inc"

	.include "data/scripts/config.inc"
	.include "data/scripts/debug.inc"
	.include "data/scripts/grounded_debug.inc"
	.include "data/scripts/burglar.inc"
	.include "data/scripts/grounded_gifts.inc"
	.include "data/scripts/forces.inc"
	.include "data/scripts/enamorus.inc"

EventScript_WhiteOut::
	call EverGrandeCity_HallOfFame_EventScript_ResetEliteFour
	end

EventScript_AfterWhiteOutHeal::
	lockall
	msgbox gText_FirstShouldRestoreMonsHealth
	call EventScript_PkmnCenterNurse_TakeAndHealPkmn
	call_if_unset FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsgPreFirstBoss
	call_if_set FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsg
	applymovement VAR_LAST_TALKED, Movement_PkmnCenterNurse_Bow
	waitmovement 0
	fadedefaultbgm
	releaseall
	end

EventScript_AfterWhiteOutHealMsgPreFirstBoss::
	msgbox gText_MonsHealedShouldBuyPotions
	return

EventScript_AfterWhiteOutHealMsg::
	msgbox gText_MonsHealed
	return

EventScript_AfterWhiteOutMomHeal::
	lockall
	textcolor NPC_TEXT_COLOR_FEMALE
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown @ Fully Ungrounded: Mom = respawn_npc van de heal location
	waitmovement 0
	msgbox gText_HadQuiteAnExperienceTakeRest
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox gText_MomExplainHPGetPotions
	fadedefaultbgm
	releaseall
	end

EverGrandeCity_HallOfFame_EventScript_ResetEliteFour::
	clearflag FLAG_DEFEATED_ELITE_4_SIDNEY
	clearflag FLAG_DEFEATED_ELITE_4_PHOEBE
	clearflag FLAG_DEFEATED_ELITE_4_GLACIA
	clearflag FLAG_DEFEATED_ELITE_4_DRAKE
	setvar VAR_ELITE_4_STATE, 0
	return

	.include "data/scripts/pkmn_center_nurse.inc"
	.include "data/scripts/obtain_item.inc"
	.include "data/scripts/record_mix.inc"
	.include "data/scripts/pc.inc"
	.include "data/scripts/move_relearner.inc"

@ scripts/notices.inc? signs.inc? See comment about text/notices.inc
Common_EventScript_ShowPokemartSign::
	msgbox gText_PokemartSign, MSGBOX_SIGN
	end

Common_EventScript_ShowPokemonCenterSign::
	msgbox gText_PokemonCenterSign, MSGBOX_SIGN
	end

Common_ShowEasyChatScreen::
	fadescreen FADE_TO_BLACK
	special ShowEasyChatScreen
	fadescreen FADE_FROM_BLACK
	return

Common_EventScript_ReadyPetalburgGymForBattle::
	clearflag FLAG_HIDE_PETALBURG_GYM_GREETER
	setflag FLAG_PETALBURG_MART_EXPANDED_ITEMS
	return

Common_EventScript_BufferTrendyPhrase::
	dotimebasedevents
	setvar VAR_0x8004, 0
	special BufferTrendyPhraseString
	return

	.include "data/scripts/surf.inc"

EventScript_CancelMessageBox::
	special UseBlankMessageToCancelPokemonPic
	release
	end

Common_EventScript_ShowBagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	release
	end

Common_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	return

EventScript_BagIsFull::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox gText_TooBadBagIsFull
	release
	end

Common_EventScript_ShowNoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	release
	end

Common_EventScript_NoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	return

Common_EventScript_PlayGymBadgeFanfare::
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	return

Common_EventScript_OutOfCenterPartyHeal::
	fadescreenswapbuffers FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	callnative UpdateFollowingPokemon
	fadescreenswapbuffers FADE_FROM_BLACK
	return

@ Fully Ungrounded: de tekst stond in het oude spelershuis (LittlerootTown_BrendansHouse_2F)
Common_Text_LookCloserAtMap:
	.string "{PLAYER} took a closer look at the\n"
	.string "region map.$"

EventScript_RegionMap::
	lockall
	msgbox Common_Text_LookCloserAtMap, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	special FieldShowRegionMap
	releaseall
	end

	.include "data/scripts/prof_birch.inc"

	.include "data/scripts/kecleon.inc"

Common_EventScript_NameReceivedPartyMon::
	fadescreen FADE_TO_BLACK
	special ChangePokemonNickname
	return

Common_EventScript_PlayerHandedOverTheItem::
	bufferitemname STR_VAR_1, VAR_0x8004
	playfanfare MUS_OBTAIN_TMHM
	message gText_PlayerHandedOverTheItem
	waitmessage
	waitfanfare
	removeitem VAR_0x8004
	return

	.include "data/scripts/movement.inc"
	.include "data/scripts/check_furniture.inc"
	.include "data/scripts/mart_clerk.inc"
	.include "data/text/record_mix.inc"
	.include "data/text/pc.inc"
	.include "data/text/pkmn_center_nurse.inc"
	.include "data/text/obtain_item.inc"
	.include "data/text/move_relearner.inc"

@ The below and surf.inc could be split into some text/notices.inc
gText_PokemartSign::
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

gText_PokemonCenterSign::
	.string "“Rejuvenate your tired partners!”\n"
	.string "POKéMON CENTER$"

gText_MomOrDadMightLikeThisProgram::
	.string "{STR_VAR_1} might like this program.\n"
	.string "… … … … … … … … … … … … … … … …\p"
	.string "Better get going!$"

gText_WhichFloorWouldYouLike::
	.string "Welcome to LILYCOVE DEPARTMENT STORE.\p"
	.string "Which floor would you like?$"

gText_SandstormIsVicious::
	.string "The sandstorm is vicious.\n"
	.string "It's impossible to keep going.$"

gText_SelectWithoutRegisteredItem::
	.string "An item in the BAG can be\n"
	.string "registered to SELECT for easy use.$"

gText_PokemonTrainerSchoolEmail::
	.string "There's an e-mail from POKéMON TRAINER\n"
	.string "SCHOOL.\p"
	.string "… … … … … …\p"
	.string "A POKéMON may learn up to four moves.\p"
	.string "A TRAINER's expertise is tested on the\n"
	.string "move sets chosen for POKéMON.\p"
	.string "… … … … … …$"

gText_PlayerHouseBootPC::
	.string "{PLAYER} booted up the PC.$"

gText_PokeblockLinkCanceled::
	.string "The link was canceled.$"

gText_UnusedNicknameReceivedPokemon::
	.string "Want to give a nickname to\n"
	.string "the {STR_VAR_2} you received?$"

gText_PlayerWhitedOut::
	.string "{PLAYER} is out of usable\n"
	.string "POKéMON!\p{PLAYER} whited out!$"

gText_FirstShouldRestoreMonsHealth::
	.string "First, you should restore your\n"
	.string "POKéMON to full health.$"

gText_MonsHealedShouldBuyPotions::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "If your POKéMON's energy, HP,\n"
	.string "is down, please come see us.\p"
	.string "If you're planning to go far in the\n"
	.string "field, you should buy some POTIONS\l"
	.string "at the POKéMON MART.\p"
	.string "We hope you excel!$"

gText_MonsHealed::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "We hope you excel!$"

gText_HadQuiteAnExperienceTakeRest::
	.string "MOM: {PLAYER}!\n"
	.string "Welcome home.\p"
	.string "It sounds like you had quite\n"
	.string "an experience.\p"
	.string "Maybe you should take a quick\n"
	.string "rest.$"

gText_MomExplainHPGetPotions::
	.string "MOM: Oh, good! You and your\n"
	.string "POKéMON are looking great.\p"
	.string "I just heard from {STR_VAR_1}.\p"
	.string "He said that POKéMON's energy is\n"
	.string "measured in HP.\p"
	.string "If your POKéMON lose their HP,\n"
	.string "you can restore them at any\l"
	.string "POKéMON CENTER.\p"
	.string "If you're going to travel far away,\n"
	.string "the smart TRAINER stocks up on\l"
	.string "POTIONS at the POKéMON MART.\p"
	.string "Make me proud, honey!\p"
	.string "Take care!$"

gText_RegisteredTrainerinPokeNav::
	.string "Registered {STR_VAR_1} {STR_VAR_2}\n"
	.string "in the POKéNAV.$"

gText_ComeBackWithSecretPower::
	.string "Do you know the TM SECRET POWER?\p"
	.string "Our group, we love the TM SECRET\n"
	.string "POWER.\p"
	.string "One of our members will give it to you.\n"
	.string "Come back and show me if you get it.\p"
	.string "We'll accept you as a member and sell\n"
	.string "you good stuff in secrecy.$"

gText_PokerusExplanation::
	.string "Your POKéMON may be infected with\n"
	.string "POKéRUS.\p"
	.string "Nobody really knows what POKéRUS is.\n"
	.string "Tiny life-forms that stick to POKéMON.\p"
	.string "Infected POKéMON grow exceptionally\n"
	.string "well. Don't tell the ministry.$"

	.include "data/text/surf.inc"

gText_DoorOpenedFarAway::
	.string "It sounded as if a door opened\n"
	.string "somewhere far away.$"

gText_BigHoleInTheWall::
	.string "There is a big hole in the wall.$"

gText_SorryWirelessClubAdjustments::
	.string "I'm terribly sorry, this room is\n"
	.string "completely useless.\p"
	.string "This game has never supported\n"
	.string "online play and link cables are\l"
	.string "out of fashion.$"

gText_UndergoingAdjustments::
	.string "It appears to be undergoing\n"
	.string "adjustments…$"

@ Unused
gText_SorryTradeCenterInspections::
	.string "I'm terribly sorry. The TRADE CENTER\n"
	.string "is undergoing inspections.$"

@ Unused
gText_SorryRecordCornerPreparation::
	.string "I'm terribly sorry. The RECORD CORNER\n"
	.string "is under preparation.$"

gText_PlayerHandedOverTheItem::
	.string "{PLAYER} handed over the\n"
	.string "{STR_VAR_1}.$"

gText_ThankYouForAccessingMysteryGift::
	.string "Thank you for accessing the\n"
	.string "MYSTERY GIFT System.$"

gText_PlayerFoundOneTMHM::
	.string "{PLAYER} found one {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_PlayerFoundTMHMs::
	.string "{PLAYER} found {STR_VAR_3} {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_Sudowoodo_Attacked::
	.string "The weird tree doesn't like the\n"
	.string "WAILMER PAIL!\p"
	.string "The weird tree attacked!$"

gText_LegendaryFlewAway::
	.string "The {STR_VAR_1} flew away!$"

gText_WantWhichFloor::
	.string "Which floor do you want?$"

	.include "data/text/pc_transfer.inc"
	.include "data/text/questionnaire.inc"

EventScript_GetInGameTradeSpeciesInfo::
	copyvar VAR_0x8005, VAR_0x8008
	specialvar VAR_0x8009, GetInGameTradeSpeciesInfo
	return

EventScript_ChooseMonForInGameTrade::
	special ChoosePartyMon
	lock
	faceplayer
	return

EventScript_GetInGameTradeSpecies::
	specialvar VAR_RESULT, GetTradeSpecies
	return

EventScript_DoInGameTrade::
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	lock
	faceplayer
	return

EventScript_SelectWithoutRegisteredItem::
	msgbox gText_SelectWithoutRegisteredItem, MSGBOX_SIGN
	end

	.include "data/scripts/field_poison.inc"

Common_EventScript_NopReturn::
	return

EventScript_SetResultTrue::
	setvar VAR_RESULT, TRUE
	return

EventScript_SetResultFalse::
	setvar VAR_RESULT, FALSE
	return

EventScript_GetElevatorFloor::
	special GetElevatorFloor
	return

@ Unused
EventScript_CableClub_SetVarResult1::
	setvar VAR_RESULT, 1
	return

EventScript_CableClub_SetVarResult0::
	setvar VAR_RESULT, 0
	return

Common_EventScript_UnionRoomAttendant::
#if IS_FRLG
	call CableClub_EventScript_UnionRoomAttendant_Frlg
#else
	call CableClub_EventScript_UnionRoomAttendant
#endif
	end

Common_EventScript_WirelessClubAttendant::
#if IS_FRLG
	call CableClub_EventScript_WirelessClubAttendant_Frlg
#else
	call CableClub_EventScript_WirelessClubAttendant
#endif
	end

Common_EventScript_DirectCornerAttendant::
#if IS_FRLG
	call CableClub_EventScript_DirectCornerAttendant_Frlg
#else
	call CableClub_EventScript_DirectCornerAttendant
#endif
	end

Common_EventScript_RemoveStaticPokemon::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

Common_EventScript_LegendaryFlewAway::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	bufferspeciesname STR_VAR_1, VAR_0x8004
	msgbox gText_LegendaryFlewAway, MSGBOX_DEFAULT
	release
	end

EventScript_VsSeekerChargingDone::
	special VsSeekerFreezeObjectsAfterChargeComplete
	waitstate
	special VsSeekerResetObjectMovementAfterChargeComplete
	releaseall
	end

@ FRLG scripts

EventScript_SetExitingCyclingRoad::
	lockall
	clearflag FLAG_SYS_ON_CYCLING_ROAD
	setvar VAR_MAP_SCENE_ROUTE16, 0
	releaseall
	end

EventScript_SetEnteringCyclingRoad::
	lockall
	setvar VAR_MAP_SCENE_ROUTE16, 1
	releaseall
	end

EventScript_TryDarkenRuins::
	goto_if_set FLAG_SYS_UNLOCKED_TANOBY_RUINS, Common_EventScript_NopReturn
	setweather WEATHER_SHADE
	doweather
	return

Text_MonFlewAway::
	.string "The {STR_VAR_1} flew away!$"

@ Call for legendary bird trio
Text_Gyaoo::
	.string "Gyaoo!$"

EventScript_BrailleCursorWaitButton::
	special BrailleCursorToggle
	waitbuttonpress
	closebraillemessage
	playse SE_SELECT
	setvar VAR_0x8006, 1
	special BrailleCursorToggle
	return

EventScript_PalletTown_PlayersHouse_2F_ShutDownPC::
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

EventScript_PalletTown_PlayersHouse_2F_TurnOnPC::
	lockall
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox gText_PlayerHouseBootPC
	special BedroomPC
	releaseall
	end


	.include "data/scripts/pc_transfer.inc"
	.include "data/scripts/questionnaire.inc"
	.include "data/scripts/trainer_script.inc"
	.include "data/scripts/berry_tree.inc"
	.include "data/scripts/secret_base.inc"
	.include "data/scripts/cable_club.inc"
	.include "data/text/cable_club.inc"
	.include "data/scripts/contest_hall.inc"
	.include "data/scripts/tv.inc"
	.include "data/text/tv.inc"
	.include "data/scripts/interview.inc"
	.include "data/scripts/gabby_and_ty.inc"
	.include "data/text/pokemon_news.inc"
	.include "data/scripts/mauville_man.inc"
	.include "data/scripts/field_move_scripts.inc"
	.include "data/scripts/item_ball_scripts.inc"
	.include "data/scripts/profile_man.inc"
	.include "data/scripts/day_care.inc"
	.include "data/scripts/flash.inc"
	.include "data/scripts/players_house.inc"
	.include "data/scripts/berry_blender.inc"
	.include "data/text/mauville_man.inc"
	.include "data/text/trainers.inc"
	.include "data/scripts/repel.inc"
	.include "data/scripts/safari_zone.inc"
	.include "data/scripts/roulette.inc"
	.include "data/scripts/pokedex_rating.inc"
	.include "data/text/pokedex_rating.inc"
	.include "data/text/check_furniture.inc"
	.include "data/scripts/cave_hole.inc"
	.include "data/scripts/lilycove_lady.inc"
	.include "data/text/match_call.inc"
	.include "data/scripts/apprentice.inc"
	.include "data/text/apprentice.inc"
	.include "data/scripts/battle_pike.inc"
	.include "data/text/blend_master.inc"
	.include "data/text/battle_tent.inc"
	.include "data/text/move_tutors.inc"
	.include "data/scripts/move_tutors.inc"
	.include "data/scripts/trainer_hill.inc"
	.include "data/scripts/test_signpost.inc"
	.include "data/scripts/follower.inc"
	.include "data/text/save.inc"
	.include "data/text/birch_speech.inc"
	.include "data/text/burglar.inc"
	.include "data/text/grounded_gifts.inc"
	.include "data/scripts/dexnav.inc"
	.include "data/scripts/battle_frontier.inc"
	.include "data/scripts/apricorn_tree.inc"
	.include "data/scripts/map_compat_stubs.inc" @ Fully Ungrounded: stubs voor labels uit verdwenen kaarten (map_compat.py)
	.include "data/maps/StartTown/scripts.inc"
	.include "data/maps/StartTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/StartTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/StartTown_Mart/scripts.inc"
	.include "data/maps/Stock_House1/scripts.inc"
	.include "data/maps/Stock_House2/scripts.inc"
	.include "data/maps/Stock_HouseWithBed/scripts.inc"
	.include "data/maps/Stock_SmallHouse/scripts.inc"
	.include "data/maps/Stock_TwoStory_1F/scripts.inc"
	.include "data/maps/Stock_TwoStory_2F/scripts.inc"
	.include "data/maps/Stock_Lab/scripts.inc"
	.include "data/maps/TestMap/scripts.inc"
	.include "data/scripts/wild_encounter.inc"
