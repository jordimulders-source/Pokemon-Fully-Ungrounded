#ifndef GUARD_CONSTANTS_FLAGS_H
#define GUARD_CONSTANTS_FLAGS_H

#include "constants/opponents.h"
#include "constants/rematches.h"

// Temporary Flags
// These temporary flags are are cleared every time a map is loaded. They are used
// for things like shortening an NPCs introduction text if the player already spoke
// to them once.
#define TEMP_FLAGS_START 0x0
#define FLAG_TEMP_1      (TEMP_FLAGS_START + 0x1)
#define FLAG_TEMP_2      (TEMP_FLAGS_START + 0x2)
#define FLAG_TEMP_3      (TEMP_FLAGS_START + 0x3)
#define FLAG_TEMP_4      (TEMP_FLAGS_START + 0x4)
#define FLAG_TEMP_5      (TEMP_FLAGS_START + 0x5)  // Unused Flag
#define FLAG_TEMP_6      (TEMP_FLAGS_START + 0x6)  // Unused Flag
#define FLAG_TEMP_7      (TEMP_FLAGS_START + 0x7)  // Unused Flag
#define FLAG_TEMP_8      (TEMP_FLAGS_START + 0x8)  // Unused Flag
#define FLAG_TEMP_9      (TEMP_FLAGS_START + 0x9)  // Unused Flag
#define FLAG_TEMP_A      (TEMP_FLAGS_START + 0xA)  // Unused Flag
#define FLAG_TEMP_B      (TEMP_FLAGS_START + 0xB)  // Unused Flag
#define FLAG_TEMP_C      (TEMP_FLAGS_START + 0xC)  // Unused Flag
#define FLAG_TEMP_D      (TEMP_FLAGS_START + 0xD)  // Unused Flag
#define FLAG_TEMP_E      (TEMP_FLAGS_START + 0xE)  // When set, follower pokemon won't be spawned
#define FLAG_TEMP_F      (TEMP_FLAGS_START + 0xF)  // Unused Flag
#define FLAG_TEMP_10     (TEMP_FLAGS_START + 0x10) // Unused Flag
#define FLAG_TEMP_11     (TEMP_FLAGS_START + 0x11)
#define FLAG_TEMP_12     (TEMP_FLAGS_START + 0x12)
#define FLAG_TEMP_13     (TEMP_FLAGS_START + 0x13)
#define FLAG_TEMP_14     (TEMP_FLAGS_START + 0x14)
#define FLAG_TEMP_15     (TEMP_FLAGS_START + 0x15)
#define FLAG_TEMP_16     (TEMP_FLAGS_START + 0x16)
#define FLAG_TEMP_17     (TEMP_FLAGS_START + 0x17)
#define FLAG_TEMP_18     (TEMP_FLAGS_START + 0x18)
#define FLAG_TEMP_19     (TEMP_FLAGS_START + 0x19)
#define FLAG_TEMP_1A     (TEMP_FLAGS_START + 0x1A)
#define FLAG_TEMP_1B     (TEMP_FLAGS_START + 0x1B)
#define FLAG_TEMP_1C     (TEMP_FLAGS_START + 0x1C)
#define FLAG_TEMP_1D     (TEMP_FLAGS_START + 0x1D)
#define FLAG_TEMP_1E     (TEMP_FLAGS_START + 0x1E)
#define FLAG_TEMP_1F     (TEMP_FLAGS_START + 0x1F)
#define TEMP_FLAGS_END   FLAG_TEMP_1F
#define NUM_TEMP_FLAGS   (TEMP_FLAGS_END - TEMP_FLAGS_START + 1)

#define FLAG_CAUGHT_SHIP_SPIRITOMB    0x20 // Project Grounded: Spiritomb in de prullenbak van het Abandoned Ship gevangen
#define FLAG_SHIP_MUK_ENCOUNTERED     0x21 // Project Grounded: Muk uit de prullenbak op Abandoned Ship B1F gezien
#define FLAG_RECEIVED_SPIT_SWALLOW_MON 0x22 // Project Grounded: Silicobra of Hisui-Qwilfish van de strandman in Slateport
#define FLAG_FORTREE_HAUNTER_TRADE_COMPLETED 0x23 // Project Grounded: Haunter-voor-Machoke-ruil in Fortree
#define FLAG_INVERSE_BATTLE    0x24 // Project Grounded: aan tijdens het gevecht tegen CHARLES (inverse battle)
#define FLAG_ORAS_DOWSING    0x25 // Project Grounded: Itemfinder werkt als de ORAS Dowsing Machine
#define FLAG_HIDE_MT_CHIMNEY_WALLY    0x26 // Project Grounded: Wally rent binnen op Mt. Chimney
#define FLAG_HIDE_METEOR_FALLS_WALLY  0x27 // Project Grounded: Wally bij de ingang van Meteor Falls
#define FLAG_HIDE_ROUTE115_KECCLES    0x28 // Project Grounded: Keccles op het strand van Route 115
#define FLAG_ITEM_AQUA_HIDEOUT_B1F_TM_SELTZER_SURGE    0x29 // Project Grounded
#define FLAG_ITEM_COLDSTEP_CAVE_ICE_STONE    0x2A // Project Grounded: Coldstep Cave
#define FLAG_ITEM_COLDSTEP_CAVE_FOCUS_SASH   0x2B // Project Grounded: Coldstep Cave
#define FLAG_ITEM_COLDSTEP_CAVE_PP_UP    0x2C // Project Grounded: Coldstep Cave
#define FLAG_ITEM_COLDSTEP_CAVE_MAX_REVIVE    0x2D // Project Grounded: Coldstep Cave
#define FLAG_ITEM_COLDSTEP_CAVE_RARE_CANDY    0x2E // Project Grounded: Coldstep Cave
#define FLAG_ITEM_ROUTE_135_LIFE_ORB    0x2F // Project Grounded: Route 135
#define FLAG_ITEM_ROUTE_135_ASSAULT_VEST    0x30 // Project Grounded: Route 135
#define FLAG_ITEM_ROUTE_135_SUPER_REPEL    0x31 // Project Grounded: Route 135
#define FLAG_HIDE_ROUTE135_LAPRAS    0x32 // Project Grounded: Lapras (static) in het meer van Route 135
#define FLAG_ITEM_ROUTE_136_MAX_ETHER    0x33 // Project Grounded: Route 136
#define FLAG_ITEM_ROUTE_136_RARE_CANDY    0x34 // Project Grounded: Route 136
#define FLAG_ITEM_ROUTE_136_WEAKNESS_POLICY    0x35 // Project Grounded: Route 136
#define FLAG_HIDE_ROUTE136_RIVAL    0x36 // Project Grounded: Route 136
#define FLAG_HIDE_ROUTE136_KECCLES    0x37 // Project Grounded: Route 136
#define FLAG_HIDE_ROUTE136_SUICUNE    0x38 // Project Grounded: Suicune (static) in de grot achter het kristalmeer van Route 136
#define FLAG_VISITED_ASHFROST_TOWN    0x39 // Project Grounded: voor Fly naar Ashfrost
#define FLAG_ITEM_COLDSTEP_CAVE_TM_LAGER_LAGOON    0x3A // Project Grounded: Coldstep Cave ijskamer 1, rechts van het middelste ijsveld
#define FLAG_RECEIVED_OAK_STARTER    0x3B // Project Grounded: Kanto-starter van Prof. Oak (Slateport)
#define FLAG_RECEIVED_TM_ACID_RAIN    0x3C // Project Grounded: TM57 van de Aqua-grunt (Aqua Hideout B1F)
#define FLAG_RECEIVED_TM_POLLEN_HAZE    0x3D // Project Grounded: TM58 van Bug Maniac Timothy (Route 119)
#define FLAG_HIDE_ROUTE111_HEATRAN_ROCKS    0x3E // Project Grounded: Heatran heeft de stenen boven Mauville weggebeukt
#define FLAG_HIDE_ROUTE111_HEATRAN    0x3F // Project Grounded: Heatran (alleen zichtbaar tijdens de cutscene)
#define FLAG_CAUGHT_MAUVILLE_ROTOM 0x40
#define FLAG_HIDE_SOOTOPOLIS_KECCLES 0x41 // Project Grounded
#define FLAG_HIDE_SOOTOPOLIS_TROPIUS 0x42 // Project Grounded
#define FLAG_HIDE_VERDANTURF_BIRCH 0x43 // Project Grounded
#define FLAG_RECEIVED_HOENN_GRIMER 0x44 // Project Grounded: Birch geeft een Hoenn-Grimer (Verdanturf)
#define FLAG_HIDE_NEW_MAUVILLE_RAIKOU    0x45 // Project Grounded: Raikou (static) in de verborgen serverruimte van New Mauville
#define FLAG_NEW_MAUVILLE_SERVER_ROOM_OPEN    0x46 // Project Grounded: schakelaar op de computer in de oostkamer: deur naar de ondergrondse grot (Raikou)
#define FLAG_HIDE_MT_CHIMNEY_ENTEI    0x47 // Project Grounded: Entei (static) in de verborgen lavagrot van Mt. Chimney
#define FLAG_HIDE_MAUVILLE_COLRESS    0x48 // Project Grounded: Colress wacht in Mauville op een gevecht
#define FLAG_HIDE_MAGMA_HIDEOUT_COLRESS    0x49 // Project Grounded: Colress in de machinekamer van de Magma Hideout
#define FLAG_HIDE_SKY_PILLAR_ZINNIA    0x4A // Project Grounded: Zinnia voor de Sky Pillar
#define FLAG_SYS_REGIELEKI_PUZZLE_COMPLETED    0x4B // Project Grounded: stippenpuzzel in de Regieleki-grot (onder de Cycling Road)
#define FLAG_SYS_REGIDRAGO_PUZZLE_COMPLETED    0x4C // Project Grounded: stippenpuzzel in de Regidrago-grot (Route 130)
#define FLAG_DEFEATED_REGIELEKI    0x4D // Project Grounded: Regieleki gevangen
#define FLAG_DEFEATED_REGIDRAGO    0x4E // Project Grounded: Regidrago gevangen
#define FLAG_DEFEATED_REGIGIGAS    0x4F // Project Grounded: Regigigas gevangen

// Scripts
#define FLAG_HIDE_SKY_PILLAR_TOP_RAYQUAZA_STILL  0x50
#define FLAG_SET_WALL_CLOCK                      0x51
#define FLAG_RESCUED_BIRCH                       0x52
#define FLAG_LEGENDARIES_IN_SOOTOPOLIS           0x53

#define FLAG_RECEIVED_GALAR_ZIGZAGOON            0x54  // Unused Flag
#define FLAG_RECEIVED_RELLOR                   0x55  // Unused Flag

#define FLAG_HIDE_CONTEST_POKE_BALL          0x56  // Always set after new game, object it hides is added directly
#define FLAG_MET_RIVAL_MOM                   0x57
#define FLAG_BIRCH_AIDE_MET                  0x58
#define FLAG_DECLINED_BIKE                   0x59
#define FLAG_RECEIVED_BIKE                   0x5A
#define FLAG_WATTSON_REMATCH_AVAILABLE       0x5B
#define FLAG_COLLECTED_ALL_SILVER_SYMBOLS    0x5C
#define FLAG_GOOD_LUCK_SAFARI_ZONE           0x5D // Set after talking to NPC blocking Safari Zone entrance/exit once.
#define FLAG_RECEIVED_WAILMER_PAIL           0x5E
#define FLAG_RECEIVED_POKEBLOCK_CASE         0x5F
#define FLAG_RECEIVED_SECRET_POWER           0x60
#define FLAG_MET_TEAM_AQUA_HARBOR            0x61
#define FLAG_TV_EXPLAINED                    0x62
#define FLAG_MAUVILLE_GYM_BARRIERS_STATE     0x63
#define FLAG_MOSSDEEP_GYM_SWITCH_1           0x64 // Leftover from the RS version of Mossdeep Gym, functionally unused
#define FLAG_MOSSDEEP_GYM_SWITCH_2           0x65 //
#define FLAG_MOSSDEEP_GYM_SWITCH_3           0x66 //
#define FLAG_MOSSDEEP_GYM_SWITCH_4           0x67 //

#define FLAG_REGIGIGAS_TEMPLE_OPEN           0x68  // Project Grounded: alle vijf Regi's gevangen, de tempel in Ashfrost is open

#define FLAG_OCEANIC_MUSEUM_MET_REPORTER     0x69
#define FLAG_RECEIVED_HM_STRENGTH            0x6A
#define FLAG_RECEIVED_HM_ROCK_SMASH          0x6B
#define FLAG_WHITEOUT_TO_LAVARIDGE           0x6C // Set after defeating Flannery, so the player cant white out from poison before receiving Go Goggles
#define FLAG_RECEIVED_HM_FLASH               0x6D
#define FLAG_RECEIVED_HM_FLY                 0x6E
#define FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT  0x6F
#define FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE  0x70
#define FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE 0x71 // Unused Flag. Used in R/S to indicate whether player defeated or caught Groudon/Kyogre in Cave of Origin.
#define FLAG_SCOTT_CALL_BATTLE_FRONTIER      0x72 // Used in order to activate a phone call from Scott, inviting the player to the SS Tidal.
#define FLAG_RECEIVED_METEORITE              0x73
#define FLAG_ADVENTURE_STARTED               0x74 // RECEIVED Pokédex.
#define FLAG_DEFEATED_MAGMA_SPACE_CENTER     0x75 // Set when Team Magma is defeated at Mossdeep's Space Center.
#define FLAG_MET_HIDDEN_POWER_GIVER          0x76

#define FLAG_CANCEL_BATTLE_ROOM_CHALLENGE    0x77

#define FLAG_LANDMARK_MIRAGE_TOWER           0x78
#define FLAG_RECEIVED_TM_BRICK_BREAK         0x79
#define FLAG_RECEIVED_HM_SURF                0x7A
#define FLAG_RECEIVED_HM_DIVE                0x7B
#define FLAG_REGISTER_RIVAL_POKENAV          0x7C
#define FLAG_DEFEATED_RIVAL_ROUTE_104        0x7D
#define FLAG_DEFEATED_WALLY_VICTORY_ROAD     0x7E
#define FLAG_MET_PRETTY_PETAL_SHOP_OWNER     0x7F
#define FLAG_ENABLE_ROXANNE_FIRST_CALL       0x80 // Set after defeating Brawly. This will activate a call with Roxanne in order to register her.
#define FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN  0x81
#define FLAG_DEFEATED_RIVAL_ROUTE103         0x82
#define FLAG_RECEIVED_DOLL_LANETTE           0x83
#define FLAG_RECEIVED_POTION_OLDALE          0x84
#define FLAG_RECEIVED_AMULET_COIN            0x85
#define FLAG_PENDING_DAYCARE_EGG             0x86
#define FLAG_THANKED_FOR_PLAYING_WITH_WALLY  0x87
#define FLAG_ENABLE_FIRST_WALLY_POKENAV_CALL 0x88 // Set after defeating Wally outside Mauville Gym. Will activate a call later to register Wally.
#define FLAG_RECEIVED_HM_CUT                 0x89
#define FLAG_SCOTT_CALL_FORTREE_GYM          0x8A // Triggers call from Scott after defeating Winona
#define FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY   0x8B
#define FLAG_RECEIVED_6_SODA_POP             0x8C
#define FLAG_DEFEATED_SEASHORE_HOUSE         0x8D
#define FLAG_DEVON_GOODS_STOLEN              0x8E
#define FLAG_RECOVERED_DEVON_GOODS           0x8F
#define FLAG_RETURNED_DEVON_GOODS            0x90
#define FLAG_CAUGHT_LUGIA                    0x91
#define FLAG_CAUGHT_HO_OH                    0x92
#define FLAG_MR_BRINEY_SAILING_INTRO         0x93
#define FLAG_DOCK_REJECTED_DEVON_GOODS       0x94
#define FLAG_DELIVERED_DEVON_GOODS           0x95
#define FLAG_RECEIVED_DESERT_UNDERPASS_MAX_REVIVE 0x96 // Project Grounded (landvulling): Desert Underpass, archeoloog (was R/S-restant RECEIVED_CONTEST_PASS)
#define FLAG_RECEIVED_CASTFORM               0x97
#define FLAG_RECEIVED_SUPER_ROD              0x98
#define FLAG_RUSTBORO_NPC_TRADE_COMPLETED    0x99
#define FLAG_PACIFIDLOG_NPC_TRADE_COMPLETED  0x9A
#define FLAG_FORTREE_NPC_TRADE_COMPLETED     0x9B
#define FLAG_BATTLE_FRONTIER_TRADE_DONE      0x9C
#define FLAG_FORCE_MIRAGE_TOWER_VISIBLE      0x9D
#define FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE   0x9E
#define FLAG_INTERACTED_WITH_DEVON_EMPLOYEE_GOODS_STOLEN 0x9F
#define FLAG_COOL_PAINTING_MADE              0xA0
#define FLAG_BEAUTY_PAINTING_MADE            0xA1
#define FLAG_CUTE_PAINTING_MADE              0xA2
#define FLAG_SMART_PAINTING_MADE             0xA3
#define FLAG_TOUGH_PAINTING_MADE             0xA4
#define FLAG_RECEIVED_TM_ROCK_TOMB           0xA5
#define FLAG_RECEIVED_TM_BULK_UP             0xA6
#define FLAG_RECEIVED_TM_SHOCK_WAVE          0xA7
#define FLAG_RECEIVED_TM_OVERHEAT            0xA8
#define FLAG_RECEIVED_TM_FACADE              0xA9
#define FLAG_RECEIVED_TM_AERIAL_ACE          0xAA
#define FLAG_RECEIVED_TM_CALM_MIND           0xAB
#define FLAG_RECEIVED_TM_WATER_PULSE         0xAC
#define FLAG_HIDE_SECRET_BASE_TRAINER        0xAD
#define FLAG_DECORATION_1                    0xAE
#define FLAG_DECORATION_2                    0xAF
#define FLAG_DECORATION_3                    0xB0
#define FLAG_DECORATION_4                    0xB1
#define FLAG_DECORATION_5                    0xB2
#define FLAG_DECORATION_6                    0xB3
#define FLAG_DECORATION_7                    0xB4
#define FLAG_DECORATION_8                    0xB5
#define FLAG_DECORATION_9                    0xB6
#define FLAG_DECORATION_10                   0xB7
#define FLAG_DECORATION_11                   0xB8
#define FLAG_DECORATION_12                   0xB9
#define FLAG_DECORATION_13                   0xBA
#define FLAG_DECORATION_14                   0xBB
#define FLAG_RECEIVED_POKENAV                0xBC
#define FLAG_DELIVERED_STEVEN_LETTER         0xBD
#define FLAG_DEFEATED_WALLY_MAUVILLE         0xBE
#define FLAG_DEFEATED_GRUNT_SPACE_CENTER_1F  0xBF
#define FLAG_RECEIVED_SUN_STONE_MOSSDEEP     0xC0
#define FLAG_WALLY_SPEECH                    0xC1
#define FLAG_TRICK_HOUSE_PUZZLE_7_SWITCH_1   0xC2 // Leftover from the RS version of Puzzle Room 7, functionally unused
#define FLAG_TRICK_HOUSE_PUZZLE_7_SWITCH_2   0xC3 //
#define FLAG_TRICK_HOUSE_PUZZLE_7_SWITCH_3   0xC4 //
#define FLAG_TRICK_HOUSE_PUZZLE_7_SWITCH_4   0xC5 //
#define FLAG_TRICK_HOUSE_PUZZLE_7_SWITCH_5   0xC6 //
#define FLAG_RUSTURF_TUNNEL_OPENED           0xC7
#define FLAG_RECEIVED_RED_SCARF              0xC8
#define FLAG_RECEIVED_BLUE_SCARF             0xC9
#define FLAG_RECEIVED_PINK_SCARF             0xCA
#define FLAG_RECEIVED_GREEN_SCARF            0xCB
#define FLAG_RECEIVED_YELLOW_SCARF           0xCC
#define FLAG_INTERACTED_WITH_STEVEN_SPACE_CENTER    0xCD
#define FLAG_ENCOUNTERED_LATIAS_OR_LATIOS    0xCE
#define FLAG_MET_ARCHIE_METEOR_FALLS         0xCF
#define FLAG_GOT_BASEMENT_KEY_FROM_WATTSON   0xD0
#define FLAG_GOT_TM_THUNDERBOLT_FROM_WATTSON 0xD1
#define FLAG_FAN_CLUB_STRENGTH_SHARED        0xD2 // Set when you rate the strength of another trainer in Lilycove's Trainer Fan Club.
#define FLAG_DEFEATED_RIVAL_RUSTBORO         0xD3
#define FLAG_RECEIVED_RED_OR_BLUE_ORB        0xD4
#define FLAG_RECEIVED_PREMIER_BALL_RUSTBORO  0xD5
#define FLAG_ENABLE_WALLY_MATCH_CALL         0xD6
#define FLAG_ENABLE_SCOTT_MATCH_CALL         0xD7
#define FLAG_ENABLE_MOM_MATCH_CALL           0xD8
#define FLAG_MET_DIVING_TREASURE_HUNTER      0xD9
#define FLAG_MET_WAILMER_TRAINER             0xDA
#define FLAG_EVIL_LEADER_PLEASE_STOP         0xDB

#define FLAG_NEVER_SET_0x0DC                 0xDC // This flag is read, but never written to

#define FLAG_RECEIVED_GO_GOGGLES             0xDD
#define FLAG_WINGULL_SENT_ON_ERRAND          0xDE
#define FLAG_RECEIVED_MENTAL_HERB            0xDF
#define FLAG_WINGULL_DELIVERED_MAIL          0xE0
#define FLAG_RECEIVED_20_COINS               0xE1
#define FLAG_RECEIVED_STARTER_DOLL           0xE2
#define FLAG_RECEIVED_GOOD_ROD               0xE3
#define FLAG_REGI_DOORS_OPENED               0xE4
#define FLAG_RECEIVED_TM_RETURN              0xE5
#define FLAG_RECEIVED_TM_SLUDGE_BOMB         0xE6
#define FLAG_RECEIVED_TM_ROAR                0xE7
#define FLAG_RECEIVED_TM_GIGA_DRAIN          0xE8

#define FLAG_HIDE_REGIELEKI                  0xE9 // Project Grounded

#define FLAG_RECEIVED_TM_REST                0xEA
#define FLAG_RECEIVED_TM_ATTRACT             0xEB
#define FLAG_RECEIVED_GLASS_ORNAMENT         0xEC
#define FLAG_RECEIVED_SILVER_SHIELD          0xED
#define FLAG_RECEIVED_GOLD_SHIELD            0xEE
#define FLAG_USED_STORAGE_KEY                0xEF
#define FLAG_USED_ROOM_1_KEY                 0xF0
#define FLAG_USED_ROOM_2_KEY                 0xF1
#define FLAG_USED_ROOM_4_KEY                 0xF2
#define FLAG_USED_ROOM_6_KEY                 0xF3
#define FLAG_MET_PROF_COZMO                  0xF4
#define FLAG_RECEIVED_WAILMER_DOLL           0xF5
#define FLAG_RECEIVED_CHESTO_BERRY_ROUTE_104 0xF6
#define FLAG_DEFEATED_SS_TIDAL_TRAINERS      0xF7
#define FLAG_RECEIVED_SPELON_BERRY           0xF8
#define FLAG_RECEIVED_PAMTRE_BERRY           0xF9
#define FLAG_RECEIVED_WATMEL_BERRY           0xFA
#define FLAG_RECEIVED_DURIN_BERRY            0xFB
#define FLAG_RECEIVED_BELUE_BERRY            0xFC
#define FLAG_ENABLE_RIVAL_MATCH_CALL         0xFD
#define FLAG_RECEIVED_CHARCOAL               0xFE
#define FLAG_LATIOS_OR_LATIAS_ROAMING        0xFF
#define FLAG_RECEIVED_REPEAT_BALL            0x100
#define FLAG_RECEIVED_OLD_ROD                0x101
#define FLAG_RECEIVED_COIN_CASE              0x102
#define FLAG_RETURNED_RED_OR_BLUE_ORB        0x103
#define FLAG_RECEIVED_TM_SNATCH              0x104
#define FLAG_RECEIVED_TM_DIG                 0x105
#define FLAG_RECEIVED_TM_BULLET_SEED         0x106
#define FLAG_ENTERED_ELITE_FOUR              0x107
#define FLAG_RECEIVED_TM_HIDDEN_POWER        0x108
#define FLAG_RECEIVED_TM_TORMENT             0x109
#define FLAG_RECEIVED_LAVARIDGE_EGG          0x10A
#define FLAG_RECEIVED_REVIVED_FOSSIL_MON     0x10B
#define FLAG_SECRET_BASE_REGISTRY_ENABLED    0x10C
#define FLAG_RECEIVED_TM_THIEF               0x10D
#define FLAG_CONTEST_SKETCH_CREATED          0x10E  // Set but never read
#define FLAG_EVIL_TEAM_ESCAPED_STERN_SPOKE   0x10F
#define FLAG_RECEIVED_EXP_SHARE              0x110
#define FLAG_POKERUS_EXPLAINED               0x111
#define FLAG_RECEIVED_RUNNING_SHOES          0x112
#define FLAG_RECEIVED_QUICK_CLAW             0x113
#define FLAG_RECEIVED_KINGS_ROCK             0x114
#define FLAG_RECEIVED_MACHO_BRACE            0x115
#define FLAG_RECEIVED_SOOTHE_BELL            0x116
#define FLAG_RECEIVED_WHITE_HERB             0x117
#define FLAG_RECEIVED_SOFT_SAND              0x118
#define FLAG_ENABLE_PROF_BIRCH_MATCH_CALL    0x119
#define FLAG_RECEIVED_CLEANSE_TAG            0x11A
#define FLAG_RECEIVED_FOCUS_BAND             0x11B
#define FLAG_DECLINED_WALLY_BATTLE_MAUVILLE  0x11C
#define FLAG_RECEIVED_DEVON_SCOPE            0x11D
#define FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE  0x11E
#define FLAG_MET_DEVON_EMPLOYEE              0x11F
#define FLAG_MET_RIVAL_RUSTBORO              0x120
#define FLAG_RECEIVED_SILK_SCARF             0x121
#define FLAG_NOT_READY_FOR_BATTLE_ROUTE_120  0x122
#define FLAG_RECEIVED_SS_TICKET              0x123
#define FLAG_MET_RIVAL_LILYCOVE              0x124
#define FLAG_MET_RIVAL_IN_HOUSE_AFTER_LILYCOVE 0x125
#define FLAG_EXCHANGED_SCANNER               0x126
#define FLAG_KECLEON_FLED_FORTREE            0x127
#define FLAG_PETALBURG_MART_EXPANDED_ITEMS   0x128
#define FLAG_RECEIVED_MIRACLE_SEED           0x129
#define FLAG_RECEIVED_BELDUM                 0x12A
#define FLAG_RECEIVED_FANCLUB_TM_THIS_WEEK   0x12B
#define FLAG_MET_FANCLUB_YOUNGER_BROTHER     0x12C
#define FLAG_RIVAL_LEFT_FOR_ROUTE103         0x12D
#define FLAG_OMIT_DIVE_FROM_STEVEN_LETTER    0x12E
#define FLAG_HAS_MATCH_CALL                  0x12F
#define FLAG_ADDED_MATCH_CALL_TO_POKENAV     0x130
#define FLAG_REGISTERED_STEVEN_POKENAV       0x131
#define FLAG_ENABLE_NORMAN_MATCH_CALL        0x132
#define FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN 0x133 // Set after you follow Steven to the entrance of the Cave of Origin.
#define FLAG_MET_ARCHIE_SOOTOPOLIS           0x134
#define FLAG_MET_MAXIE_SOOTOPOLIS            0x135
#define FLAG_MET_SCOTT_RUSTBORO              0x136
#define FLAG_WALLACE_GOES_TO_SKY_PILLAR      0x137 // Set after speaking to Wallace within the Cave of Origin.
#define FLAG_RECEIVED_HM_WATERFALL           0x138
#define FLAG_BEAT_MAGMA_GRUNT_JAGGED_PASS    0x139
#define FLAG_WONDER_CARD_UNUSED_0            0x13A // Project Grounded: was Aurora Ticket
#define FLAG_RECEIVED_MYSTIC_TICKET          0x13B
#define FLAG_RECEIVED_OLD_SEA_MAP            0x13C
#define FLAG_WONDER_CARD_UNUSED_1            0x13D // These Wonder Card flags are referenced but never set
#define FLAG_WONDER_CARD_UNUSED_2            0x13E
#define FLAG_WONDER_CARD_UNUSED_3            0x13F
#define FLAG_WONDER_CARD_UNUSED_4            0x140
#define FLAG_WONDER_CARD_UNUSED_5            0x141
#define FLAG_WONDER_CARD_UNUSED_6            0x142
#define FLAG_WONDER_CARD_UNUSED_7            0x143
#define FLAG_WONDER_CARD_UNUSED_8            0x144
#define FLAG_WONDER_CARD_UNUSED_9            0x145
#define FLAG_WONDER_CARD_UNUSED_10           0x146
#define FLAG_WONDER_CARD_UNUSED_11           0x147
#define FLAG_WONDER_CARD_UNUSED_12           0x148
#define FLAG_WONDER_CARD_UNUSED_13           0x149
#define FLAG_WONDER_CARD_UNUSED_14           0x14A
#define FLAG_WONDER_CARD_UNUSED_15           0x14B
#define FLAG_WONDER_CARD_UNUSED_16           0x14C
#define FLAG_WONDER_CARD_UNUSED_17           0x14D
#define NUM_WONDER_CARD_FLAGS                (1 + FLAG_WONDER_CARD_UNUSED_17 - FLAG_WONDER_CARD_UNUSED_0)

#define FLAG_MIRAGE_TOWER_VISIBLE            0x14E
#define FLAG_CHOSE_ROOT_FOSSIL               0x14F
#define FLAG_CHOSE_CLAW_FOSSIL               0x150
#define FLAG_RECEIVED_POWDER_JAR             0x151

#define FLAG_CHOSEN_MULTI_BATTLE_NPC_PARTNER 0x152

#define FLAG_MET_BATTLE_FRONTIER_BREEDER     0x153
#define FLAG_MET_BATTLE_FRONTIER_MANIAC      0x154
#define FLAG_ENTERED_CONTEST                 0x155
#define FLAG_MET_SLATEPORT_FANCLUB_CHAIRMAN  0x156
#define FLAG_MET_BATTLE_FRONTIER_GAMBLER     0x157
#define FLAG_ENABLE_MR_STONE_POKENAV         0x158
#define FLAG_NURSE_MENTIONS_GOLD_CARD        0x159
#define FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR  0x15A
#define FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR 0x15B

// Flags for whether a rematchable trainer has been registered in the player's Match Call.
// Most are used implicitly by adding their REMATCH_* id to TRAINER_REGISTERED_FLAGS_START.
// Some Match Call entries (like those for gym leaders, Wally, and all non-trainer NPCs like Prof. Birch)
// have their own separate flag that needs to be set to be enabled; see src/pokenav_match_call_data.c
#define TRAINER_REGISTERED_FLAGS_START       0x15C
#define FLAG_REGISTERED_ROSE                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROSE)
#define FLAG_REGISTERED_ANDRES               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ANDRES)
#define FLAG_REGISTERED_DUSTY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DUSTY)
#define FLAG_REGISTERED_LOLA                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_LOLA)
#define FLAG_REGISTERED_RICKY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_RICKY)
#define FLAG_REGISTERED_LILA_AND_ROY         (TRAINER_REGISTERED_FLAGS_START + REMATCH_LILA_AND_ROY)
#define FLAG_REGISTERED_CRISTIN              (TRAINER_REGISTERED_FLAGS_START + REMATCH_CRISTIN)
#define FLAG_REGISTERED_BROOKE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BROOKE)
#define FLAG_REGISTERED_CHARLES              (TRAINER_REGISTERED_FLAGS_START + REMATCH_CHARLES)
#define FLAG_REGISTERED_VALERIE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_VALERIE)
#define FLAG_REGISTERED_CINDY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_CINDY)
#define FLAG_REGISTERED_THALIA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_THALIA)
#define FLAG_REGISTERED_JESSICA              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JESSICA)
#define FLAG_REGISTERED_WINSTON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WINSTON)
#define FLAG_REGISTERED_STEVE                (TRAINER_REGISTERED_FLAGS_START + REMATCH_STEVE)
#define FLAG_REGISTERED_TONY                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_TONY)
#define FLAG_REGISTERED_NOB                  (TRAINER_REGISTERED_FLAGS_START + REMATCH_NOB)
#define FLAG_REGISTERED_KOJI                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_KOJI)
#define FLAG_REGISTERED_FERNANDO             (TRAINER_REGISTERED_FLAGS_START + REMATCH_FERNANDO)
#define FLAG_REGISTERED_DALTON               (TRAINER_REGISTERED_FLAGS_START + REMATCH_DALTON)
#define FLAG_REGISTERED_BERNIE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BERNIE)
#define FLAG_REGISTERED_ETHAN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_ETHAN)
#define FLAG_REGISTERED_JOHN_AND_JAY         (TRAINER_REGISTERED_FLAGS_START + REMATCH_JOHN_AND_JAY)
#define FLAG_REGISTERED_JEFFREY              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JEFFREY)
#define FLAG_REGISTERED_CAMERON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_CAMERON)
#define FLAG_REGISTERED_JACKI                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JACKI)
#define FLAG_REGISTERED_WALTER               (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALTER)
#define FLAG_REGISTERED_KAREN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_KAREN)
#define FLAG_REGISTERED_JERRY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JERRY)
#define FLAG_REGISTERED_ANNA_AND_MEG         (TRAINER_REGISTERED_FLAGS_START + REMATCH_ANNA_AND_MEG)
#define FLAG_REGISTERED_ISABEL               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISABEL)
#define FLAG_REGISTERED_MIGUEL               (TRAINER_REGISTERED_FLAGS_START + REMATCH_MIGUEL)
#define FLAG_REGISTERED_TIMOTHY              (TRAINER_REGISTERED_FLAGS_START + REMATCH_TIMOTHY)
#define FLAG_REGISTERED_SHELBY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SHELBY)
#define FLAG_REGISTERED_CALVIN               (TRAINER_REGISTERED_FLAGS_START + REMATCH_CALVIN)
#define FLAG_REGISTERED_ELLIOT               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ELLIOT)
#define FLAG_REGISTERED_ISAIAH               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISAIAH)
#define FLAG_REGISTERED_MARIA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_MARIA)
#define FLAG_REGISTERED_ABIGAIL              (TRAINER_REGISTERED_FLAGS_START + REMATCH_ABIGAIL)
#define FLAG_REGISTERED_DYLAN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DYLAN)
#define FLAG_REGISTERED_KATELYN              (TRAINER_REGISTERED_FLAGS_START + REMATCH_KATELYN)
#define FLAG_REGISTERED_BENJAMIN             (TRAINER_REGISTERED_FLAGS_START + REMATCH_BENJAMIN)
#define FLAG_REGISTERED_PABLO                (TRAINER_REGISTERED_FLAGS_START + REMATCH_PABLO)
#define FLAG_REGISTERED_NICOLAS              (TRAINER_REGISTERED_FLAGS_START + REMATCH_NICOLAS)
#define FLAG_REGISTERED_ROBERT               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROBERT)
#define FLAG_REGISTERED_LAO                  (TRAINER_REGISTERED_FLAGS_START + REMATCH_LAO)
#define FLAG_REGISTERED_CYNDY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_CYNDY)
#define FLAG_REGISTERED_MADELINE             (TRAINER_REGISTERED_FLAGS_START + REMATCH_MADELINE)
#define FLAG_REGISTERED_JENNY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JENNY)
#define FLAG_REGISTERED_DIANA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DIANA)
#define FLAG_REGISTERED_AMY_AND_LIV          (TRAINER_REGISTERED_FLAGS_START + REMATCH_AMY_AND_LIV)
#define FLAG_REGISTERED_ERNEST               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ERNEST)
#define FLAG_REGISTERED_CORY                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_CORY)
#define FLAG_REGISTERED_EDWIN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_EDWIN)
#define FLAG_REGISTERED_LYDIA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_LYDIA)
#define FLAG_REGISTERED_ISAAC                (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISAAC)
#define FLAG_REGISTERED_GABRIELLE            (TRAINER_REGISTERED_FLAGS_START + REMATCH_GABRIELLE)
#define FLAG_REGISTERED_CATHERINE            (TRAINER_REGISTERED_FLAGS_START + REMATCH_CATHERINE)
#define FLAG_REGISTERED_JACKSON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JACKSON)
#define FLAG_REGISTERED_HALEY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_HALEY)
#define FLAG_REGISTERED_JAMES                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JAMES)
#define FLAG_REGISTERED_TRENT                (TRAINER_REGISTERED_FLAGS_START + REMATCH_TRENT)
#define FLAG_REGISTERED_SAWYER               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SAWYER)
#define FLAG_REGISTERED_KIRA_AND_DAN         (TRAINER_REGISTERED_FLAGS_START + REMATCH_KIRA_AND_DAN)
#define FLAG_REGISTERED_WALLY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALLY_VR)
#define FLAG_REGISTERED_ROXANNE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROXANNE)
#define FLAG_REGISTERED_BRAWLY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BRAWLY)
#define FLAG_REGISTERED_WATTSON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WATTSON)
#define FLAG_REGISTERED_FLANNERY             (TRAINER_REGISTERED_FLAGS_START + REMATCH_FLANNERY)
#define FLAG_REGISTERED_NORMAN               (TRAINER_REGISTERED_FLAGS_START + REMATCH_NORMAN)
#define FLAG_REGISTERED_WINONA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_WINONA)
#define FLAG_REGISTERED_TATE_AND_LIZA        (TRAINER_REGISTERED_FLAGS_START + REMATCH_TATE_AND_LIZA)
#define FLAG_REGISTERED_WALLACE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALLACE)
#define FLAG_REGISTERED_SIDNEY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SIDNEY)
#define FLAG_REGISTERED_PHOEBE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_PHOEBE)
#define FLAG_REGISTERED_GLACIA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_GLACIA)
#define FLAG_REGISTERED_DRAKE                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DRAKE)
#define FLAG_REGISTERED_OLD_CHAMPION         (TRAINER_REGISTERED_FLAGS_START + REMATCH_OLD_CHAMPION)

#define FLAG_HIDE_REGIDRAGO                  0x1AA // Project Grounded
#define FLAG_HIDE_REGIGIGAS                  0x1AB // Project Grounded

#define FLAG_DEFEATED_DEOXYS                 0x1AC
#define FLAG_BATTLED_DEOXYS                  0x1AD
#define FLAG_SHOWN_EON_TICKET                0x1AE
#define FLAG_UNUSED_0x1AF                    0x1AF // Project Grounded: was FLAG_SHOWN_AURORA_TICKET
#define FLAG_SHOWN_OLD_SEA_MAP               0x1B0
#define FLAG_MOVE_TUTOR_TAUGHT_SWAGGER       0x1B1
#define FLAG_MOVE_TUTOR_TAUGHT_ROLLOUT       0x1B2
#define FLAG_MOVE_TUTOR_TAUGHT_FURY_CUTTER   0x1B3
#define FLAG_MOVE_TUTOR_TAUGHT_MIMIC         0x1B4
#define FLAG_MOVE_TUTOR_TAUGHT_METRONOME     0x1B5
#define FLAG_MOVE_TUTOR_TAUGHT_SLEEP_TALK    0x1B6
#define FLAG_MOVE_TUTOR_TAUGHT_SUBSTITUTE    0x1B7
#define FLAG_MOVE_TUTOR_TAUGHT_DYNAMICPUNCH  0x1B8
#define FLAG_MOVE_TUTOR_TAUGHT_DOUBLE_EDGE   0x1B9
#define FLAG_MOVE_TUTOR_TAUGHT_EXPLOSION     0x1BA
#define FLAG_DEFEATED_REGIROCK               0x1BB
#define FLAG_DEFEATED_REGICE                 0x1BC
#define FLAG_DEFEATED_REGISTEEL              0x1BD
#define FLAG_DEFEATED_KYOGRE                 0x1BE
#define FLAG_DEFEATED_GROUDON                0x1BF
#define FLAG_DEFEATED_RAYQUAZA               0x1C0
#define FLAG_DEFEATED_VOLTORB_1_NEW_MAUVILLE 0x1C1
#define FLAG_DEFEATED_VOLTORB_2_NEW_MAUVILLE 0x1C2
#define FLAG_DEFEATED_VOLTORB_3_NEW_MAUVILLE 0x1C3
#define FLAG_DEFEATED_ELECTRODE_1_AQUA_HIDEOUT 0x1C4
#define FLAG_DEFEATED_ELECTRODE_2_AQUA_HIDEOUT 0x1C5
#define FLAG_DEFEATED_SUDOWOODO              0x1C6
#define FLAG_DEFEATED_MEW                    0x1C7
#define FLAG_DEFEATED_LATIAS_OR_LATIOS       0x1C8
#define FLAG_CAUGHT_LATIAS_OR_LATIOS         0x1C9
#define FLAG_CAUGHT_MEW                      0x1CA
#define FLAG_MET_SCOTT_AFTER_OBTAINING_STONE_BADGE 0x1CB
#define FLAG_MET_SCOTT_IN_VERDANTURF         0x1CC
#define FLAG_MET_SCOTT_IN_FALLARBOR          0x1CD
#define FLAG_MET_SCOTT_IN_LILYCOVE           0x1CE
#define FLAG_MET_SCOTT_IN_EVERGRANDE         0x1CF
#define FLAG_MET_SCOTT_ON_SS_TIDAL           0x1D0
#define FLAG_SCOTT_GIVES_BATTLE_POINTS       0x1D1
#define FLAG_COLLECTED_ALL_GOLD_SYMBOLS      0x1D2
#define FLAG_ENABLE_ROXANNE_MATCH_CALL       0x1D3
#define FLAG_ENABLE_BRAWLY_MATCH_CALL        0x1D4
#define FLAG_ENABLE_WATTSON_MATCH_CALL       0x1D5
#define FLAG_ENABLE_FLANNERY_MATCH_CALL      0x1D6
#define FLAG_ENABLE_WINONA_MATCH_CALL        0x1D7
#define FLAG_ENABLE_TATE_AND_LIZA_MATCH_CALL 0x1D8
#define FLAG_ENABLE_WALLACE_MATCH_CALL       0x1D9

#define FLAG_HIDE_FIERY_PATH_HEATRAN         0x1DA // Project Grounded: Heatran (static) in de lavagrot onder Fiery Path

#define FLAG_SHOWN_MYSTIC_TICKET             0x1DB
#define FLAG_DEFEATED_HO_OH                  0x1DC
#define FLAG_DEFEATED_LUGIA                  0x1DD

#define FLAG_CAUGHT_TAPU_KOKO                0x1DE // Project Grounded: Tapu-eiland: Tapu Koko gevangen
#define FLAG_CAUGHT_TAPU_LELE                0x1DF // Project Grounded: Tapu-eiland: Tapu Lele gevangen
#define FLAG_CAUGHT_TAPU_BULU                0x1E0 // Project Grounded: Tapu-eiland: Tapu Bulu gevangen
#define FLAG_CAUGHT_TAPU_FINI                0x1E1 // Project Grounded: Tapu-eiland: Tapu Fini gevangen
#define FLAG_DEFEATED_TAPU_KOKO              0x1E2 // Project Grounded: Tapu-eiland: Tapu Koko verslagen/gevangen (terug na de League als niet gevangen)
#define FLAG_DEFEATED_TAPU_LELE              0x1E3 // Project Grounded: Tapu-eiland: Tapu Lele verslagen/gevangen

// Mystery Gift Flags (Unknown)
#define FLAG_MYSTERY_GIFT_DONE               0x1E4
#define FLAG_MYSTERY_GIFT_1                  0x1E5
#define FLAG_MYSTERY_GIFT_2                  0x1E6
#define FLAG_MYSTERY_GIFT_3                  0x1E7
#define FLAG_MYSTERY_GIFT_4                  0x1E8
#define FLAG_MYSTERY_GIFT_5                  0x1E9
#define FLAG_MYSTERY_GIFT_6                  0x1EA
#define FLAG_MYSTERY_GIFT_7                  0x1EB
#define FLAG_MYSTERY_GIFT_8                  0x1EC
#define FLAG_MYSTERY_GIFT_9                  0x1ED
#define FLAG_MYSTERY_GIFT_10                 0x1EE
#define FLAG_MYSTERY_GIFT_11                 0x1EF
#define FLAG_MYSTERY_GIFT_12                 0x1F0
#define FLAG_MYSTERY_GIFT_13                 0x1F1
#define FLAG_MYSTERY_GIFT_14                 0x1F2
#define FLAG_MYSTERY_GIFT_15                 0x1F3

// Hidden Items
#define FLAG_HIDDEN_ITEMS_START                                                         0x1F4
#define FLAG_HIDDEN_ITEM_LAVARIDGE_TOWN_ICE_HEAL             (FLAG_HIDDEN_ITEMS_START + 0x00)
#define FLAG_HIDDEN_ITEM_TRICK_HOUSE_NUGGET                  (FLAG_HIDDEN_ITEMS_START + 0x01)
#define FLAG_HIDDEN_ITEM_ROUTE_111_STARDUST                  (FLAG_HIDDEN_ITEMS_START + 0x02)
#define FLAG_HIDDEN_ITEM_ROUTE_113_ETHER                     (FLAG_HIDDEN_ITEMS_START + 0x03)
#define FLAG_HIDDEN_ITEM_ROUTE_114_CARBOS                    (FLAG_HIDDEN_ITEMS_START + 0x04)
#define FLAG_HIDDEN_ITEM_ROUTE_119_CALCIUM                   (FLAG_HIDDEN_ITEMS_START + 0x05)
#define FLAG_HIDDEN_ITEM_ROUTE_119_ULTRA_BALL                (FLAG_HIDDEN_ITEMS_START + 0x06)
#define FLAG_HIDDEN_ITEM_ROUTE_123_SUPER_REPEL               (FLAG_HIDDEN_ITEMS_START + 0x07)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_CARBOS               (FLAG_HIDDEN_ITEMS_START + 0x08)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_GREEN_SHARD          (FLAG_HIDDEN_ITEMS_START + 0x09)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_PEARL                (FLAG_HIDDEN_ITEMS_START + 0x0A)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_BIG_PEARL            (FLAG_HIDDEN_ITEMS_START + 0x0B)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_BLUE_SHARD           (FLAG_HIDDEN_ITEMS_START + 0x0C)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_HEART_SCALE_1        (FLAG_HIDDEN_ITEMS_START + 0x0D)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_HEART_SCALE          (FLAG_HIDDEN_ITEMS_START + 0x0E)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_ULTRA_BALL           (FLAG_HIDDEN_ITEMS_START + 0x0F)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_STARDUST             (FLAG_HIDDEN_ITEMS_START + 0x10)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_PEARL                (FLAG_HIDDEN_ITEMS_START + 0x11)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_YELLOW_SHARD         (FLAG_HIDDEN_ITEMS_START + 0x12)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_IRON                 (FLAG_HIDDEN_ITEMS_START + 0x13)
#define FLAG_HIDDEN_ITEM_UNDERWATER_126_BIG_PEARL            (FLAG_HIDDEN_ITEMS_START + 0x14)
#define FLAG_HIDDEN_ITEM_UNDERWATER_127_STAR_PIECE           (FLAG_HIDDEN_ITEMS_START + 0x15)
#define FLAG_HIDDEN_ITEM_UNDERWATER_127_HP_UP                (FLAG_HIDDEN_ITEMS_START + 0x16)
#define FLAG_HIDDEN_ITEM_UNDERWATER_127_HEART_SCALE          (FLAG_HIDDEN_ITEMS_START + 0x17)
#define FLAG_HIDDEN_ITEM_UNDERWATER_127_RED_SHARD            (FLAG_HIDDEN_ITEMS_START + 0x18)
#define FLAG_HIDDEN_ITEM_UNDERWATER_128_PROTEIN              (FLAG_HIDDEN_ITEMS_START + 0x19)
#define FLAG_HIDDEN_ITEM_UNDERWATER_128_PEARL                (FLAG_HIDDEN_ITEMS_START + 0x1A)
#define FLAG_HIDDEN_ITEM_LILYCOVE_CITY_HEART_SCALE           (FLAG_HIDDEN_ITEMS_START + 0x1B)
#define FLAG_HIDDEN_ITEM_FALLARBOR_TOWN_NUGGET               (FLAG_HIDDEN_ITEMS_START + 0x1C)
#define FLAG_HIDDEN_ITEM_MT_PYRE_EXTERIOR_ULTRA_BALL         (FLAG_HIDDEN_ITEMS_START + 0x1D)
#define FLAG_HIDDEN_ITEM_ROUTE_113_TM_DOUBLE_TEAM            (FLAG_HIDDEN_ITEMS_START + 0x1E)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_1_KEY             (FLAG_HIDDEN_ITEMS_START + 0x1F)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_2_KEY             (FLAG_HIDDEN_ITEMS_START + 0x20)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_4_KEY             (FLAG_HIDDEN_ITEMS_START + 0x21)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_6_KEY             (FLAG_HIDDEN_ITEMS_START + 0x22)
#define FLAG_HIDDEN_ITEM_SS_TIDAL_LOWER_DECK_LEFTOVERS       (FLAG_HIDDEN_ITEMS_START + 0x23)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_CALCIUM              (FLAG_HIDDEN_ITEMS_START + 0x24)
#define FLAG_HIDDEN_ITEM_ROUTE_104_POTION                    (FLAG_HIDDEN_ITEMS_START + 0x25)
#define FLAG_HIDDEN_ITEM_UNDERWATER_124_HEART_SCALE_2        (FLAG_HIDDEN_ITEMS_START + 0x26)
#define FLAG_HIDDEN_ITEM_ROUTE_121_HP_UP                     (FLAG_HIDDEN_ITEMS_START + 0x27)
#define FLAG_HIDDEN_ITEM_ROUTE_121_NUGGET                    (FLAG_HIDDEN_ITEMS_START + 0x28)
#define FLAG_HIDDEN_ITEM_ROUTE_123_REVIVE                    (FLAG_HIDDEN_ITEMS_START + 0x29)
#define FLAG_HIDDEN_ITEM_ROUTE_114_REVIVE                    (FLAG_HIDDEN_ITEMS_START + 0x2A)
#define FLAG_HIDDEN_ITEM_LILYCOVE_CITY_PP_UP                 (FLAG_HIDDEN_ITEMS_START + 0x2B)
#define FLAG_HIDDEN_ITEM_ROUTE_104_SUPER_POTION              (FLAG_HIDDEN_ITEMS_START + 0x2C)
#define FLAG_HIDDEN_ITEM_ROUTE_116_SUPER_POTION              (FLAG_HIDDEN_ITEMS_START + 0x2D)
#define FLAG_HIDDEN_ITEM_ROUTE_106_STARDUST                  (FLAG_HIDDEN_ITEMS_START + 0x2E)
#define FLAG_HIDDEN_ITEM_ROUTE_106_HEART_SCALE               (FLAG_HIDDEN_ITEMS_START + 0x2F)
#define FLAG_HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_1        (FLAG_HIDDEN_ITEMS_START + 0x30)
#define FLAG_HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_2        (FLAG_HIDDEN_ITEMS_START + 0x31)
#define FLAG_HIDDEN_ITEM_ROUTE_109_REVIVE                    (FLAG_HIDDEN_ITEMS_START + 0x32)
#define FLAG_HIDDEN_ITEM_ROUTE_109_GREAT_BALL                (FLAG_HIDDEN_ITEMS_START + 0x33)
#define FLAG_HIDDEN_ITEM_ROUTE_109_HEART_SCALE_1             (FLAG_HIDDEN_ITEMS_START + 0x34)
#define FLAG_HIDDEN_ITEM_ROUTE_110_GREAT_BALL                (FLAG_HIDDEN_ITEMS_START + 0x35)
#define FLAG_HIDDEN_ITEM_ROUTE_110_REVIVE                    (FLAG_HIDDEN_ITEMS_START + 0x36)
#define FLAG_HIDDEN_ITEM_ROUTE_110_FULL_HEAL                 (FLAG_HIDDEN_ITEMS_START + 0x37)
#define FLAG_HIDDEN_ITEM_ROUTE_111_PROTEIN                   (FLAG_HIDDEN_ITEMS_START + 0x38)
#define FLAG_HIDDEN_ITEM_ROUTE_111_RARE_CANDY                (FLAG_HIDDEN_ITEMS_START + 0x39)
#define FLAG_HIDDEN_ITEM_PETALBURG_WOODS_POTION              (FLAG_HIDDEN_ITEMS_START + 0x3A)
#define FLAG_HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_1     (FLAG_HIDDEN_ITEMS_START + 0x3B)
#define FLAG_HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_2     (FLAG_HIDDEN_ITEMS_START + 0x3C)
#define FLAG_HIDDEN_ITEM_PETALBURG_WOODS_POKE_BALL           (FLAG_HIDDEN_ITEMS_START + 0x3D)
#define FLAG_HIDDEN_ITEM_ROUTE_104_POKE_BALL                 (FLAG_HIDDEN_ITEMS_START + 0x3E)
#define FLAG_HIDDEN_ITEM_ROUTE_106_POKE_BALL                 (FLAG_HIDDEN_ITEMS_START + 0x3F)
#define FLAG_HIDDEN_ITEM_ROUTE_109_ETHER                     (FLAG_HIDDEN_ITEMS_START + 0x40)
#define FLAG_HIDDEN_ITEM_ROUTE_110_POKE_BALL                 (FLAG_HIDDEN_ITEMS_START + 0x41)
#define FLAG_HIDDEN_ITEM_ROUTE_118_HEART_SCALE               (FLAG_HIDDEN_ITEMS_START + 0x42)
#define FLAG_HIDDEN_ITEM_ROUTE_118_IRON                      (FLAG_HIDDEN_ITEMS_START + 0x43)
#define FLAG_HIDDEN_ITEM_ROUTE_119_FULL_HEAL                 (FLAG_HIDDEN_ITEMS_START + 0x44)
#define FLAG_HIDDEN_ITEM_ROUTE_120_RARE_CANDY_2              (FLAG_HIDDEN_ITEMS_START + 0x45)
#define FLAG_HIDDEN_ITEM_ROUTE_120_ZINC                      (FLAG_HIDDEN_ITEMS_START + 0x46)
#define FLAG_HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1              (FLAG_HIDDEN_ITEMS_START + 0x47)
#define FLAG_HIDDEN_ITEM_ROUTE_117_REPEL                     (FLAG_HIDDEN_ITEMS_START + 0x48)
#define FLAG_HIDDEN_ITEM_ROUTE_121_FULL_HEAL                 (FLAG_HIDDEN_ITEMS_START + 0x49)
#define FLAG_HIDDEN_ITEM_ROUTE_123_HYPER_POTION              (FLAG_HIDDEN_ITEMS_START + 0x4A)
#define FLAG_HIDDEN_ITEM_LILYCOVE_CITY_POKE_BALL             (FLAG_HIDDEN_ITEMS_START + 0x4B)
#define FLAG_HIDDEN_ITEM_JAGGED_PASS_GREAT_BALL              (FLAG_HIDDEN_ITEMS_START + 0x4C)
#define FLAG_HIDDEN_ITEM_JAGGED_PASS_FULL_HEAL               (FLAG_HIDDEN_ITEMS_START + 0x4D)
#define FLAG_HIDDEN_ITEM_MT_PYRE_EXTERIOR_MAX_ETHER          (FLAG_HIDDEN_ITEMS_START + 0x4E)
#define FLAG_HIDDEN_ITEM_MT_PYRE_SUMMIT_ZINC                 (FLAG_HIDDEN_ITEMS_START + 0x4F)
#define FLAG_HIDDEN_ITEM_MT_PYRE_SUMMIT_RARE_CANDY           (FLAG_HIDDEN_ITEMS_START + 0x50)
#define FLAG_HIDDEN_ITEM_VICTORY_ROAD_1F_ULTRA_BALL          (FLAG_HIDDEN_ITEMS_START + 0x51)
#define FLAG_HIDDEN_ITEM_VICTORY_ROAD_B2F_ELIXIR             (FLAG_HIDDEN_ITEMS_START + 0x52)
#define FLAG_HIDDEN_ITEM_VICTORY_ROAD_B2F_MAX_REPEL          (FLAG_HIDDEN_ITEMS_START + 0x53)
#define FLAG_HIDDEN_ITEM_ROUTE_120_REVIVE                    (FLAG_HIDDEN_ITEMS_START + 0x54)
#define FLAG_HIDDEN_ITEM_ROUTE_104_ANTIDOTE                  (FLAG_HIDDEN_ITEMS_START + 0x55)
#define FLAG_HIDDEN_ITEM_ROUTE_108_RARE_CANDY                (FLAG_HIDDEN_ITEMS_START + 0x56)
#define FLAG_HIDDEN_ITEM_ROUTE_119_MAX_ETHER                 (FLAG_HIDDEN_ITEMS_START + 0x57)
#define FLAG_HIDDEN_ITEM_ROUTE_104_HEART_SCALE               (FLAG_HIDDEN_ITEMS_START + 0x58)
#define FLAG_HIDDEN_ITEM_ROUTE_105_HEART_SCALE               (FLAG_HIDDEN_ITEMS_START + 0x59)
#define FLAG_HIDDEN_ITEM_ROUTE_109_HEART_SCALE_2             (FLAG_HIDDEN_ITEMS_START + 0x5A)
#define FLAG_HIDDEN_ITEM_ROUTE_109_HEART_SCALE_3             (FLAG_HIDDEN_ITEMS_START + 0x5B)
#define FLAG_HIDDEN_ITEM_ROUTE_128_HEART_SCALE_1             (FLAG_HIDDEN_ITEMS_START + 0x5C)
#define FLAG_HIDDEN_ITEM_ROUTE_128_HEART_SCALE_2             (FLAG_HIDDEN_ITEMS_START + 0x5D)
#define FLAG_HIDDEN_ITEM_ROUTE_128_HEART_SCALE_3             (FLAG_HIDDEN_ITEMS_START + 0x5E)
#define FLAG_HIDDEN_ITEM_PETALBURG_CITY_RARE_CANDY           (FLAG_HIDDEN_ITEMS_START + 0x5F)
#define FLAG_HIDDEN_ITEM_ROUTE_116_BLACK_GLASSES             (FLAG_HIDDEN_ITEMS_START + 0x60)
#define FLAG_HIDDEN_ITEM_ROUTE_115_HEART_SCALE               (FLAG_HIDDEN_ITEMS_START + 0x61)
#define FLAG_HIDDEN_ITEM_ROUTE_113_NUGGET                    (FLAG_HIDDEN_ITEMS_START + 0x62)
#define FLAG_HIDDEN_ITEM_ROUTE_123_PP_UP                     (FLAG_HIDDEN_ITEMS_START + 0x63)
#define FLAG_HIDDEN_ITEM_ROUTE_121_MAX_REVIVE                (FLAG_HIDDEN_ITEMS_START + 0x64)
#define FLAG_HIDDEN_ITEM_ARTISAN_CAVE_B1F_CALCIUM            (FLAG_HIDDEN_ITEMS_START + 0x65)
#define FLAG_HIDDEN_ITEM_ARTISAN_CAVE_B1F_ZINC               (FLAG_HIDDEN_ITEMS_START + 0x66)
#define FLAG_HIDDEN_ITEM_ARTISAN_CAVE_B1F_PROTEIN            (FLAG_HIDDEN_ITEMS_START + 0x67)
#define FLAG_HIDDEN_ITEM_ARTISAN_CAVE_B1F_IRON               (FLAG_HIDDEN_ITEMS_START + 0x68)
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_SOUTH_EAST_FULL_RESTORE (FLAG_HIDDEN_ITEMS_START + 0x69)
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_NORTH_EAST_RARE_CANDY   (FLAG_HIDDEN_ITEMS_START + 0x6A)
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_NORTH_EAST_ZINC         (FLAG_HIDDEN_ITEMS_START + 0x6B)
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_SOUTH_EAST_PP_UP        (FLAG_HIDDEN_ITEMS_START + 0x6C)
#define FLAG_HIDDEN_ITEM_NAVEL_ROCK_TOP_SACRED_ASH           (FLAG_HIDDEN_ITEMS_START + 0x6D)
#define FLAG_HIDDEN_ITEM_ROUTE_123_RARE_CANDY                (FLAG_HIDDEN_ITEMS_START + 0x6E)
#define FLAG_HIDDEN_ITEM_ROUTE_105_BIG_PEARL                 (FLAG_HIDDEN_ITEMS_START + 0x6F)
#define FLAG_HIDDEN_ITEM_ROUTE_102_LEFTOVERS                 (FLAG_HIDDEN_ITEMS_START + 0x70)

#define FLAG_HIDDEN_ITEM_ROUTE_135_NUGGET  0x265 // Project Grounded: Route 135
#define FLAG_HIDDEN_ITEM_ROUTE_135_ICE_HEAL  0x266 // Project Grounded: Route 135
#define FLAG_HIDDEN_ITEM_ROUTE_136_STAR_PIECE  0x267 // Project Grounded: Route 136
#define FLAG_HIDDEN_ITEM_ROUTE_136_MAX_REPEL  0x268 // Project Grounded: Route 136
#define FLAG_HIDE_FALLARBOR_JIRACHI 0x269 // Project Grounded: Jirachi (object) bij de wenssteen in Fallarbor, verborgen tot je een wens doet
#define FLAG_DEFEATED_JIRACHI       0x26A // Project Grounded: Jirachi gevangen of verslagen (wens-event klaar)
#define FLAG_DEFEATED_DARKRAI       0x26B // Project Grounded: Darkrai gevangen of verslagen (nachtmerrie op Mt. Pyre klaar)
#define FLAG_FORCE_SHINY            0x26C // Project Grounded: P_FLAG_FORCE_SHINY (alleen tijdens het shiny Rayquaza-gevecht aan)
#define FLAG_DEFEATED_SHINY_RAYQUAZA 0x26D // Project Grounded: shiny Rayquaza gevangen of verslagen (verslagen: terug na de League)
#define FLAG_CAUGHT_SHINY_RAYQUAZA  0x26E // Project Grounded: shiny Rayquaza gevangen
#define FLAG_HIDE_SKY_PILLAR_TOP_SHINY_RAYQUAZA 0x26F // Project Grounded: wordt elke keer in OnTransition gezet/gewist
#define FLAG_HIDE_MOSSDEEP_ZINNIA   0x270 // Project Grounded: Zinnia in Mossdeep (Delta Episode); in OnTransition gezet/gewist
#define FLAG_NEW_MAUVILLE_VAULT_OPEN  0x271 // Project Grounded: serverkluis onder New Mauville herstart (terminal in de Raikou-grot), deur naar Genesect open
#define FLAG_HIDE_NEW_MAUVILLE_GENESECT  0x272 // Project Grounded: Genesect (static), sinds v0.9.110 in het ruim van de Plasma Frigate (Nothing Island)
#define FLAG_HIDE_METEOR_FALLS_MEWTWO  0x273 // Project Grounded: Mewtwo (static) in de verborgen grot achter Meteor Falls
#define FLAG_ITEM_UNKNOWN_CAVE_1F_MAX_REVIVE  0x274 // Project Grounded: item in de verborgen grot achter Meteor Falls (1F)
#define FLAG_ITEM_UNKNOWN_CAVE_B1F_MAX_ELIXIR  0x275 // Project Grounded: item in de verborgen grot achter Meteor Falls (B1F)
#define FLAG_HIDDEN_ITEM_ZV3_WHIRL_SEA_INCENSE                      0x276 // Project Grounded (zeevulling 3)
#define FLAG_RECEIVED_RESORT_WINE  0x277 // Project Grounded: Wallace' wijn (Berry Juice) in het PARADISO RESORT ontvangen
#define FLAG_HIDE_RESORT_RIVAL     0x278 // Project Grounded: rivaal in het PARADISO RESORT; in OnTransition gezet/gewist (post-game)
#define FLAG_HIDE_SKY_PILLAR_GIRATINA  0x279 // Project Grounded: Giratina (static) onderin de omgekeerde Sky Pillar
#define FLAG_FISH_TOURNEY_WEEK_BIT0  0x27A // Project Grounded: visserstoernooi (Dewford), 0x27A-0x27E = (week % 31) + 1 van de laatst opgehaalde prijs
#define FLAG_FISH_TOURNEY_WEEK_BIT1  0x27B // Project Grounded: visserstoernooi, weekbit 1
#define FLAG_FISH_TOURNEY_WEEK_BIT2  0x27C // Project Grounded: visserstoernooi, weekbit 2
#define FLAG_FISH_TOURNEY_WEEK_BIT3  0x27D // Project Grounded: visserstoernooi, weekbit 3
#define FLAG_FISH_TOURNEY_WEEK_BIT4  0x27E // Project Grounded: visserstoernooi, weekbit 4
#define FLAG_FISH_TOURNEY_TROPHY     0x27F // Project Grounded: visserstoernooi, trofee (1e plaats) ooit ontvangen
#define FLAG_FISH_TOURNEY_LUCKY_EGG  0x280 // Project Grounded: visserstoernooi, Lucky Egg (eerste troostprijs) ontvangen
#define FLAG_HIDE_FLOWER_PARADISE_SHAYMIN  0x281 // Project Grounded: Shaymin gevangen
#define FLAG_RECEIVED_GRACIDEA  0x282 // Project Grounded: Gracidea na het vangen van Shaymin
#define FLAG_RECEIVED_KUBFU  0x283 // Project Grounded: Kubfu van de dojomeester (Dewford)
#define FLAG_KUBFU_EVOLVED  0x284 // Project Grounded: een toren van de dojo voltooid, Kubfu geevolueerd
#define FLAG_HIDE_MOSSDEEP_ZINNIA_METEORITE 0x285 // Project Grounded: Zinnia bij de meteoriet (Delta Episode, afsluiter)
#define FLAG_HIDE_WEATHER_INSTITUTE_ARCHIE_MAXIE 0x286 // Project Grounded: Archie en Maxie (werkstraf); in OnTransition gezet/gewist
#define FLAG_ITEM_FORTREE_JUNGLE_BIG_ROOT  0x287 // Project Grounded: Fortree Jungle
#define FLAG_ITEM_FORTREE_JUNGLE_MAX_REVIVE  0x288 // Project Grounded: Fortree Jungle
#define FLAG_RECEIVED_LIBERTY_PASS        0x289 // Project Grounded: Liberty Pass gekregen (uitnodiging voor de Victory-gauntlet, post-game)
#define FLAG_HIDE_LIBERTY_GARDEN_VICTINI  0x28A // Project Grounded: Victini-object in Liberty Garden (verborgen tot de gauntlet af is)
#define FLAG_DEFEATED_LIBERTY_VICTINI     0x28B // Project Grounded: Victini in Liberty Garden verslagen/gevangen
#define FLAG_ITEM_FORTREE_JUNGLE_TM_U_TURN  0x28C // Project Grounded: Fortree Jungle
#define FLAG_ITEM_FORTREE_JUNGLE_MIRACLE_SEED  0x28D // Project Grounded: Fortree Jungle
#define FLAG_HIDDEN_ITEM_FORTREE_JUNGLE_LEAF_STONE  0x28E // Project Grounded: Fortree Jungle
#define FLAG_HIDDEN_ITEM_FORTREE_JUNGLE_REVIVAL_HERB  0x28F // Project Grounded: Fortree Jungle
#define FLAG_SAFARI_ZONES_OPEN  0x290 // Project Grounded: Safari-zones open (zonesleutels terug; later de Team Rocket-sidequest)
#define FLAG_ITEM_SAFARI_FAIRY_PIXIE_PLATE  0x291 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_ITEM_SAFARI_FAIRY_FAIRY_FEATHER  0x292 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_HIDDEN_ITEM_SAFARI_FAIRY_SHINY_STONE  0x293 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_ITEM_SAFARI_THUNDER_ZAP_PLATE  0x294 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_ITEM_SAFARI_THUNDER_MAGNET  0x295 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_HIDDEN_ITEM_SAFARI_THUNDER_THUNDER_STONE  0x296 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_ITEM_SAFARI_SPOOK_SPOOKY_PLATE  0x297 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_ITEM_SAFARI_SPOOK_REAPER_CLOTH  0x298 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_HIDDEN_ITEM_SAFARI_SPOOK_DUSK_STONE  0x299 // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_HIDDEN_ITEM_SAFARI_SPOOK_SPELL_TAG  0x29A // Project Grounded: Safari Zone (nieuwe zones)
#define FLAG_HIDE_GIANT_WAILORD  0x29B // Project Grounded: reuzen-Wailord verborgen (per kaartbezoek gezet, zie Grounded_GiantWailordSpot)
#define FLAG_SEA_TEMPLE_DOOR_OPEN  0x29C // Project Grounded: zeetempel (Route 128), stenenpuzzel opgelost, deur naar het heiligdom open
#define FLAG_CAUGHT_SEA_TEMPLE_MANAPHY  0x29D // Project Grounded: zeetempel, Manaphy gevangen (ook verbergflag; verslagen = komt terug)
#define FLAG_RECEIVED_SEA_TEMPLE_EGG  0x29E // Project Grounded: zeetempel, Phione-ei + Silver Wing van het altaar
#define FLAG_ITEM_PLASMA_FRIGATE_MAX_REVIVE 0x29F // Project Grounded (was 0x2B9; botste met eb en vloed)
#define FLAG_ITEM_METEOR_FALLS_B1F_2R_RARE_CANDY 0x2A0 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_B1F_2R_STAR_PIECE 0x2A1 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_HIDDEN_FALLS_DRAGON_SCALE 0x2A2 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_HIDDEN_FALLS_MAX_ELIXIR 0x2A3 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_TUNNELS_DRAGON_FANG 0x2A4 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_TUNNELS_FULL_RESTORE 0x2A5 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_TUNNELS_STARDUST 0x2A6 // Project Grounded: Meteor Falls (diepte)
#define FLAG_HIDE_METEOR_FALLS_SALAMENCE 0x2A7 // Project Grounded: Meteor Falls (diepte)
#define FLAG_VICTORY_ROAD_WAITING_ROOM_ROCK 0x2A8 // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_WAITING_ROOM_CHOICE_SCARF 0x2A9 // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_WAITING_ROOM_CHOICE_SPECS 0x2AA // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_VAULT_BIG_NUGGET 0x2AB // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_VAULT_ABILITY_CAPSULE 0x2AC // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_VAULT_PP_MAX 0x2AD // Project Grounded: Victory Road-zijkamers
#define FLAG_HIDDEN_ITEM_VICTORY_ROAD_VAULT_MAX_ELIXIR 0x2AE // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_HERMIT_EXPERT_BELT 0x2AF // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_TOADSTOOL_HOLLOW_TINY_MUSHROOM  0x2B0 // Project Grounded: Toadstool Hollow
#define FLAG_ITEM_TOADSTOOL_HOLLOW_BIG_MUSHROOM  0x2B1 // Project Grounded: Toadstool Hollow
#define FLAG_ITEM_TOADSTOOL_HOLLOW_MISTY_SEED  0x2B2 // Project Grounded: Toadstool Hollow
#define FLAG_HIDDEN_ITEM_TOADSTOOL_HOLLOW_BALM_MUSHROOM  0x2B3 // Project Grounded: Toadstool Hollow (midden van de heksenkring)
#define FLAG_HIDDEN_ITEM_TOADSTOOL_HOLLOW_TINY_MUSHROOM  0x2B4 // Project Grounded: Toadstool Hollow (einde van een stam)
#define FLAG_HIDE_PLASMA_ISLAND_CREW  0x2B5 // Project Grounded: Neo Plasma-grunts en Nigel op Nothing Island (in OnTransition: gezet zolang VAR_PLASMA_FRIGATE 0 is)
#define FLAG_HIDE_PLASMA_TRIAD        0x2B6 // Project Grounded: Shadow Triad bij het luik van de Plasma Frigate (verdwijnt na het gevecht)
#define FLAG_HIDE_PLASMA_BOSSES       0x2B7 // Project Grounded: Zinzolin en Rood in het ruim (weg na het Genesect-gevecht)
#define FLAG_ITEM_PLASMA_FRIGATE_PP_MAX     0x2B8 // Project Grounded
#define FLAG_HIDDEN_ITEM_ROUTE_132_STAR_PIECE  0x2B9 // Project Grounded: wad Route 132 (alleen bij eb)
#define FLAG_HIDDEN_ITEM_ROUTE_132_BIG_PEARL  0x2BA // Project Grounded: wad Route 132 (alleen bij eb)
#define FLAG_TIDE_HIGH  0x2BB // Project Grounded: vloed op Route 132 (gezet bij binnenkomst, oneven uur)

// Event Flags
#define FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG                      0x2BC
#define FLAG_HIDE_APPRENTICE                                        0x2BD
#define FLAG_HIDE_POKEMON_CENTER_2F_MYSTERY_GIFT_MAN                0x2BE
#define FLAG_HIDE_UNION_ROOM_PLAYER_1                               0x2BF
#define FLAG_HIDE_UNION_ROOM_PLAYER_2                               0x2C0
#define FLAG_HIDE_UNION_ROOM_PLAYER_3                               0x2C1
#define FLAG_HIDE_UNION_ROOM_PLAYER_4                               0x2C2
#define FLAG_HIDE_UNION_ROOM_PLAYER_5                               0x2C3
#define FLAG_HIDE_UNION_ROOM_PLAYER_6                               0x2C4
#define FLAG_HIDE_UNION_ROOM_PLAYER_7                               0x2C5
#define FLAG_HIDE_UNION_ROOM_PLAYER_8                               0x2C6
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_1               0x2C7
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_2               0x2C8
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_3               0x2C9
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_4               0x2CA
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_5               0x2CB
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_6               0x2CC
#define FLAG_HIDE_SAFARI_ZONE_SOUTH_CONSTRUCTION_WORKERS            0x2CD
#define FLAG_HIDE_MEW                                               0x2CE
#define FLAG_HIDE_ROUTE_104_RIVAL                                   0x2CF
#define FLAG_HIDE_ROUTE_101_BIRCH_ZIGZAGOON_BATTLE                  0x2D0
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_BIRCH                  0x2D1
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_BEDROOM          0x2D2
#define FLAG_HIDE_ROUTE_103_RIVAL                                   0x2D3
#define FLAG_HIDE_PETALBURG_WOODS_DEVON_EMPLOYEE                    0x2D4
#define FLAG_HIDE_PETALBURG_WOODS_AQUA_GRUNT                        0x2D5
#define FLAG_HIDE_PETALBURG_CITY_WALLY                              0x2D6
#define FLAG_HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_INVISIBLE_NINJA_BOY   0x2D7
#define FLAG_HIDE_PETALBURG_CITY_WALLYS_MOM                         0x2D8

#define FLAG_HIDDEN_ITEM_ZV3_WHIRL_MAX_ELIXIR                       0x2D9 // Project Grounded (zeevulling 3)

#define FLAG_HIDE_LILYCOVE_FAN_CLUB_INTERVIEWER                     0x2DA
#define FLAG_HIDE_RUSTBORO_CITY_AQUA_GRUNT                          0x2DB
#define FLAG_HIDE_RUSTBORO_CITY_DEVON_EMPLOYEE_1                    0x2DC
#define FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_KYOGRE_ASLEEP              0x2DD
#define FLAG_HIDE_PLAYERS_HOUSE_DAD                                 0x2DE
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_SIBLING      0x2DF
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_SIBLING          0x2E0
#define FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_MAGMA_NOTE             0x2E1
#define FLAG_HIDE_ROUTE_104_MR_BRINEY                               0x2E2
#define FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY                           0x2E3
#define FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN                            0x2E4
#define FLAG_HIDE_ROUTE_109_MR_BRINEY                               0x2E5
#define FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT                          0x2E6
#define FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN                       0x2E7
#define FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT                          0x2E8
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_BRENDAN            0x2E9
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MAY                    0x2EA
#define FLAG_HIDE_SAFARI_ZONE_SOUTH_EAST_EXPANSION                  0x2EB
#define FLAG_HIDE_LILYCOVE_HARBOR_EVENT_TICKET_TAKER                0x2EC
#define FLAG_HIDE_SLATEPORT_CITY_SCOTT                              0x2ED
#define FLAG_HIDE_ROUTE_101_ZIGZAGOON                               0x2EE
#define FLAG_HIDE_VICTORY_ROAD_EXIT_WALLY                           0x2EF
#define FLAG_HIDE_LITTLEROOT_TOWN_MOM_OUTSIDE                       0x2F0
#define FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_STEVEN              0x2F1
#define FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_1          0x2F2
#define FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_2          0x2F3
#define FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_TEAM_MAGMA          0x2F4
#define FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_BEDROOM_MOM               0x2F5
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_MOM                0x2F6
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MOM                    0x2F7
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_BEDROOM      0x2F8
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_TRUCK              0x2F9
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_TRUCK                  0x2FA
#define FLAG_HIDE_DEOXYS                                            0x2FB
#define FLAG_HIDE_METEOR_SPACE_DEOXYS_TRIANGLE                      0x2FC
#define FLAG_HIDE_MAUVILLE_CITY_SCOTT                               0x2FD
#define FLAG_HIDE_VERDANTURF_TOWN_SCOTT                             0x2FE
#define FLAG_HIDE_FALLARBOR_TOWN_BATTLE_TENT_SCOTT                  0x2FF
#define FLAG_HIDE_ROUTE_111_VICTOR_WINSTRATE                        0x300
#define FLAG_HIDE_ROUTE_111_VICTORIA_WINSTRATE                      0x301
#define FLAG_HIDE_ROUTE_111_VIVI_WINSTRATE                          0x302
#define FLAG_HIDE_ROUTE_111_VICKY_WINSTRATE                         0x303
#define FLAG_HIDE_PETALBURG_GYM_NORMAN                              0x304
#define FLAG_HIDE_SKY_PILLAR_TOP_RAYQUAZA                           0x305
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_CONTEST_ATTENDANT_1         0x306
#define FLAG_HIDE_LILYCOVE_MUSEUM_CURATOR                           0x307
#define FLAG_HIDE_LILYCOVE_MUSEUM_PATRON_1                          0x308
#define FLAG_HIDE_LILYCOVE_MUSEUM_PATRON_2                          0x309
#define FLAG_HIDE_LILYCOVE_MUSEUM_PATRON_3                          0x30A
#define FLAG_HIDE_LILYCOVE_MUSEUM_PATRON_4                          0x30B
#define FLAG_HIDE_LILYCOVE_MUSEUM_TOURISTS                          0x30C
#define FLAG_HIDE_PETALBURG_GYM_GREETER                             0x30D
#define FLAG_HIDE_MARINE_CAVE_KYOGRE                                0x30E
#define FLAG_HIDE_TERRA_CAVE_GROUDON                                0x30F
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_MOM          0x310
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_MOM              0x311
#define FLAG_HIDE_ROUTE_119_SCOTT                                   0x312
#define FLAG_HIDE_LILYCOVE_MOTEL_SCOTT                              0x313
#define FLAG_HIDE_MOSSDEEP_CITY_SCOTT                               0x314
#define FLAG_HIDE_FANCLUB_OLD_LADY                                  0x315
#define FLAG_HIDE_FANCLUB_BOY                                       0x316
#define FLAG_HIDE_FANCLUB_LITTLE_BOY                                0x317
#define FLAG_HIDE_FANCLUB_LADY                                      0x318
#define FLAG_HIDE_EVER_GRANDE_POKEMON_CENTER_1F_SCOTT               0x319
#define FLAG_HIDE_LITTLEROOT_TOWN_RIVAL                             0x31A
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCH                             0x31B
#define FLAG_HIDE_ROUTE_111_GABBY_AND_TY_1                          0x31C
#define FLAG_HIDE_ROUTE_118_GABBY_AND_TY_1                          0x31D
#define FLAG_HIDE_ROUTE_120_GABBY_AND_TY_1                          0x31E
#define FLAG_HIDE_ROUTE_111_GABBY_AND_TY_2                          0x31F
#define FLAG_HIDE_LUGIA                                             0x320
#define FLAG_HIDE_HO_OH                                             0x321
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_REPORTER                    0x322
#define FLAG_HIDE_SLATEPORT_CITY_CONTEST_REPORTER                   0x323
#define FLAG_HIDE_MAUVILLE_CITY_WALLY                               0x324
#define FLAG_HIDE_MAUVILLE_CITY_WALLYS_UNCLE                        0x325
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLY                0x326
#define FLAG_HIDE_RUSTURF_TUNNEL_WANDAS_BOYFRIEND                   0x327
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDAS_BOYFRIEND     0x328
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLYS_UNCLE         0x329
#define FLAG_HIDE_SS_TIDAL_CORRIDOR_SCOTT                           0x32A
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_CYNDAQUIL     0x32B
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_TOTODILE      0x32C
#define FLAG_HIDE_ROUTE_116_DROPPED_GLASSES_MAN                     0x32D
#define FLAG_HIDE_RUSTBORO_CITY_RIVAL                               0x32E
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_SWABLU_DOLL     0x32F
#define FLAG_HIDE_SOOTOPOLIS_CITY_WALLACE                           0x330
#define FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_POKE_BALL       0x331
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_POKE_BALL           0x332
#define FLAG_HIDE_ROUTE_112_TEAM_MAGMA                              0x333
#define FLAG_HIDE_CAVE_OF_ORIGIN_B1F_WALLACE                        0x334
#define FLAG_HIDE_AQUA_HIDEOUT_1F_GRUNT_1_BLOCKING_ENTRANCE         0x335
#define FLAG_HIDE_AQUA_HIDEOUT_1F_GRUNT_2_BLOCKING_ENTRANCE         0x336
#define FLAG_HIDE_MOSSDEEP_CITY_TEAM_MAGMA                          0x337
#define FLAG_HIDE_PETALBURG_GYM_WALLYS_DAD                          0x338
#define FLAG_ITEM_DESERT_UNDERPASS_STONE_PLATE                      0x339 // Project Grounded (landvulling): Desert Underpass, opgraving (was R/S-restant)
#define FLAG_HIDE_SOOTOPOLIS_CITY_ARCHIE                            0x33A
#define FLAG_HIDE_SOOTOPOLIS_CITY_MAXIE                             0x33B
#define FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_ARCHIE                     0x33C
#define FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_MAXIE                      0x33D
#define FLAG_HIDE_PETALBURG_CITY_WALLYS_DAD                         0x33E
#define FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_MAGMA_GRUNTS               0x33F
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_BLEND_MASTER                0x340
#define FLAG_HIDE_GRANITE_CAVE_STEVEN                               0x341
#define FLAG_HIDE_ROUTE_128_STEVEN                                  0x342
#define FLAG_HIDE_SLATEPORT_CITY_GABBY_AND_TY                       0x343
#define FLAG_HIDE_BATTLE_FRONTIER_RECEPTION_GATE_SCOTT              0x344
#define FLAG_HIDE_ROUTE_110_BIRCH                                   0x345
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_CHIKORITA     0x346
#define FLAG_HIDE_SOOTOPOLIS_CITY_MAN_1                             0x347
#define FLAG_HIDE_SLATEPORT_CITY_CAPTAIN_STERN                      0x348
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_CAPTAIN_STERN               0x349
#define FLAG_HIDE_BATTLE_FRONTIER_SUDOWOODO                         0x34A
#define FLAG_HIDE_ROUTE_111_ROCK_SMASH_TIP_GUY                      0x34B
#define FLAG_HIDE_RUSTBORO_CITY_SCIENTIST                           0x34C
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_AQUA_GRUNT                  0x34D
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_ARCHIE                      0x34E
#define FLAG_HIDE_JAGGED_PASS_MAGMA_GUARD                           0x34F
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_SUBMARINE_SHADOW            0x350
#define FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_PICHU_DOLL          0x351
#define FLAG_HIDE_MAGMA_HIDEOUT_4F_GROUDON_ASLEEP                   0x352
#define FLAG_HIDE_ROUTE_119_RIVAL                                   0x353
#define FLAG_HIDE_LILYCOVE_CITY_AQUA_GRUNTS                         0x354
#define FLAG_HIDE_MAGMA_HIDEOUT_4F_GROUDON                          0x355
#define FLAG_HIDE_SOOTOPOLIS_CITY_RESIDENTS                         0x356
#define FLAG_HIDE_SKY_PILLAR_WALLACE                                0x357
#define FLAG_HIDE_MT_PYRE_SUMMIT_MAXIE                              0x358
#define FLAG_HIDE_MAGMA_HIDEOUT_GRUNTS                              0x359
#define FLAG_HIDE_VICTORY_ROAD_ENTRANCE_WALLY                       0x35A
#define FLAG_HIDE_SEAFLOOR_CAVERN_ROOM_9_KYOGRE                     0x35B
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_SS_TIDAL                    0x35C
#define FLAG_HIDE_LILYCOVE_HARBOR_SSTIDAL                           0x35D
#define FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_TEAM_MAGMA          0x35E
#define FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_STEVEN              0x35F
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_1           0x360
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_2           0x361
#define FLAG_HIDE_PETALBURG_GYM_WALLY                               0x362
#define FLAG_UNKNOWN_0x363                                          0x363 // Set, however has no purpose.
#define FLAG_HIDE_LITTLEROOT_TOWN_FAT_MAN                           0x364
#define FLAG_HIDE_SLATEPORT_CITY_STERNS_SHIPYARD_MR_BRINEY          0x365
#define FLAG_HIDE_LANETTES_HOUSE_LANETTE                            0x366
#define FLAG_HIDE_FALLARBOR_POKEMON_CENTER_LANETTE                  0x367
#define FLAG_HIDE_TRICK_HOUSE_ENTRANCE_MAN                          0x368
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_BLEND_MASTER_REPLACEMENT    0x369
#define FLAG_HIDE_DESERT_UNDERPASS_FOSSIL                           0x36A
#define FLAG_HIDE_ROUTE_111_PLAYER_DESCENT                          0x36B
#define FLAG_HIDE_ROUTE_111_DESERT_FOSSIL                           0x36C
#define FLAG_HIDE_MT_CHIMNEY_TRAINERS                               0x36D
#define FLAG_HIDE_RUSTURF_TUNNEL_AQUA_GRUNT                         0x36E
#define FLAG_HIDE_RUSTURF_TUNNEL_BRINEY                             0x36F
#define FLAG_HIDE_RUSTURF_TUNNEL_PEEKO                              0x370
#define FLAG_HIDE_BRINEYS_HOUSE_PEEKO                               0x371
#define FLAG_HIDE_SLATEPORT_CITY_TEAM_AQUA                          0x372
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_AQUA_GRUNTS         0x373
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_AQUA_GRUNT_1     0x374
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_AQUA_GRUNT_2     0x375
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_ARCHIE           0x376
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_CAPTAIN_STERN    0x377
#define FLAG_HIDE_BATTLE_TOWER_OPPONENT                             0x378
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_RIVAL                  0x379
#define FLAG_HIDE_ROUTE_119_TEAM_AQUA                               0x37A
#define FLAG_HIDE_ROUTE_116_MR_BRINEY                               0x37B
#define FLAG_HIDE_WEATHER_INSTITUTE_1F_WORKERS                      0x37C
#define FLAG_HIDE_WEATHER_INSTITUTE_2F_WORKERS                      0x37D
#define FLAG_HIDE_ROUTE_116_WANDAS_BOYFRIEND                        0x37E
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_CONTEST_ATTENDANT_2         0x37F
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_UNKNOWN_0x380          0x380
#define FLAG_HIDE_ROUTE_101_BIRCH                                   0x381
#define FLAG_HIDE_ROUTE_103_BIRCH                                   0x382
#define FLAG_HIDE_TRICK_HOUSE_END_MAN                               0x383
#define FLAG_HIDE_ROUTE_110_TEAM_AQUA                               0x384
#define FLAG_HIDE_ROUTE_118_GABBY_AND_TY_2                          0x385
#define FLAG_HIDE_ROUTE_120_GABBY_AND_TY_2                          0x386
#define FLAG_HIDE_ROUTE_111_GABBY_AND_TY_3                          0x387
#define FLAG_HIDE_ROUTE_118_GABBY_AND_TY_3                          0x388
#define FLAG_HIDE_SLATEPORT_CITY_HARBOR_PATRONS                     0x389
#define FLAG_HIDE_ROUTE_104_WHITE_HERB_FLORIST                      0x38A
#define FLAG_HIDE_FALLARBOR_AZURILL                                 0x38B
#define FLAG_HIDE_LILYCOVE_HARBOR_FERRY_ATTENDANT                   0x38C
#define FLAG_HIDE_LILYCOVE_HARBOR_FERRY_SAILOR                      0x38D
#define FLAG_HIDE_SOUTHERN_ISLAND_EON_STONE                         0x38E
#define FLAG_HIDE_SOUTHERN_ISLAND_UNCHOSEN_EON_DUO_MON              0x38F
#define FLAG_HIDE_MAUVILLE_CITY_WATTSON                             0x390
#define FLAG_HIDE_MAUVILLE_GYM_WATTSON                              0x391
#define FLAG_HIDE_ROUTE_121_TEAM_AQUA_GRUNTS                        0x392
#define FLAG_UNKNOWN_0x393                                          0x393 // Set, however has no purpose.
#define FLAG_HIDE_MT_PYRE_SUMMIT_ARCHIE                             0x394
#define FLAG_HIDE_MT_PYRE_SUMMIT_TEAM_AQUA                          0x395
#define FLAG_HIDE_BATTLE_TOWER_REPORTER                             0x396
#define FLAG_HIDE_ROUTE_110_RIVAL                                   0x397
#define FLAG_HIDE_CHAMPIONS_ROOM_RIVAL                              0x398
#define FLAG_HIDE_CHAMPIONS_ROOM_BIRCH                              0x399
#define FLAG_HIDE_ROUTE_110_RIVAL_ON_BIKE                           0x39A
#define FLAG_HIDE_ROUTE_119_RIVAL_ON_BIKE                           0x39B
#define FLAG_HIDE_AQUA_HIDEOUT_GRUNTS                               0x39C
#define FLAG_HIDE_LILYCOVE_MOTEL_GAME_DESIGNERS                     0x39D
#define FLAG_HIDE_MT_CHIMNEY_TEAM_AQUA                              0x39E
#define FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA                             0x39F
#define FLAG_HIDE_FALLARBOR_HOUSE_PROF_COZMO                        0x3A0
#define FLAG_HIDE_LAVARIDGE_TOWN_RIVAL                              0x3A1
#define FLAG_HIDE_LAVARIDGE_TOWN_RIVAL_ON_BIKE                      0x3A2
#define FLAG_HIDE_RUSTURF_TUNNEL_ROCK_1                             0x3A3
#define FLAG_HIDE_RUSTURF_TUNNEL_ROCK_2                             0x3A4
#define FLAG_HIDE_FORTREE_CITY_HOUSE_4_WINGULL                      0x3A5
#define FLAG_HIDE_MOSSDEEP_CITY_HOUSE_2_WINGULL                     0x3A6
#define FLAG_HIDE_REGIROCK                                          0x3A7
#define FLAG_HIDE_REGICE                                            0x3A8
#define FLAG_HIDE_REGISTEEL                                         0x3A9
#define FLAG_HIDE_METEOR_FALLS_TEAM_AQUA                            0x3AA
#define FLAG_HIDE_METEOR_FALLS_TEAM_MAGMA                           0x3AB
#define FLAG_HIDE_DEWFORD_HALL_SLUDGE_BOMB_MAN                      0x3AC
#define FLAG_HIDE_SEAFLOOR_CAVERN_ENTRANCE_AQUA_GRUNT               0x3AD
#define FLAG_HIDE_METEOR_FALLS_1F_1R_COZMO                          0x3AE
#define FLAG_HIDE_AQUA_HIDEOUT_B2F_SUBMARINE_SHADOW                 0x3AF
#define FLAG_HIDE_ROUTE_128_ARCHIE                                  0x3B0
#define FLAG_HIDE_ROUTE_128_MAXIE                                   0x3B1
#define FLAG_HIDE_SEAFLOOR_CAVERN_AQUA_GRUNTS                       0x3B2
#define FLAG_HIDE_ROUTE_116_DEVON_EMPLOYEE                          0x3B3
#define FLAG_HIDE_SLATEPORT_CITY_TM_SALESMAN                        0x3B4
#define FLAG_HIDE_RUSTBORO_CITY_DEVON_CORP_3F_EMPLOYEE              0x3B5
#define FLAG_HIDE_SS_TIDAL_CORRIDOR_MR_BRINEY                       0x3B6
#define FLAG_HIDE_SS_TIDAL_ROOMS_SNATCH_GIVER                       0x3B7
#define FLAG_RECEIVED_SHOAL_SALT_1                                  0x3B8
#define FLAG_RECEIVED_SHOAL_SALT_2                                  0x3B9
#define FLAG_RECEIVED_SHOAL_SALT_3                                  0x3BA
#define FLAG_RECEIVED_SHOAL_SALT_4                                  0x3BB
#define FLAG_RECEIVED_SHOAL_SHELL_1                                 0x3BC
#define FLAG_RECEIVED_SHOAL_SHELL_2                                 0x3BD
#define FLAG_RECEIVED_SHOAL_SHELL_3                                 0x3BE
#define FLAG_RECEIVED_SHOAL_SHELL_4                                 0x3BF
#define FLAG_HIDE_ROUTE_111_SECRET_POWER_MAN                        0x3C0
#define FLAG_HIDE_SLATEPORT_MUSEUM_POPULATION                       0x3C1
#define FLAG_HIDE_LILYCOVE_DEPARTMENT_STORE_ROOFTOP_SALE_WOMAN      0x3C2
#define FLAG_HIDE_MIRAGE_TOWER_ROOT_FOSSIL                          0x3C3
#define FLAG_HIDE_MIRAGE_TOWER_CLAW_FOSSIL                          0x3C4
#define FLAG_HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_FAMILIAR_AQUA_GRUNT 0x3C5
#define FLAG_HIDE_ROUTE_118_STEVEN                                  0x3C6
#define FLAG_HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_STEVEN                0x3C7
#define FLAG_HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_BELDUM_POKEBALL       0x3C8
#define FLAG_HIDE_FORTREE_CITY_KECLEON                              0x3C9
#define FLAG_HIDE_ROUTE_120_KECLEON_BRIDGE                          0x3CA
#define FLAG_HIDE_LILYCOVE_CITY_RIVAL                               0x3CB
#define FLAG_HIDE_ROUTE_120_STEVEN                                  0x3CC
#define FLAG_HIDE_SOOTOPOLIS_CITY_STEVEN                            0x3CD
#define FLAG_HIDE_NEW_MAUVILLE_VOLTORB_1                            0x3CE
#define FLAG_HIDE_NEW_MAUVILLE_VOLTORB_2                            0x3CF
#define FLAG_HIDE_NEW_MAUVILLE_VOLTORB_3                            0x3D0
#define FLAG_HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_1                      0x3D1
#define FLAG_HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_2                      0x3D2
#define FLAG_HIDE_OLDALE_TOWN_RIVAL                                 0x3D3
#define FLAG_HIDE_UNDERWATER_SEA_FLOOR_CAVERN_STOLEN_SUBMARINE      0x3D4
#define FLAG_HIDE_ROUTE_120_KECLEON_BRIDGE_SHADOW                   0x3D5
#define FLAG_HIDE_ROUTE_120_KECLEON_1                               0x3D6
#define FLAG_HIDE_RUSTURF_TUNNEL_WANDA                              0x3D7
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDA                0x3D8
#define FLAG_HIDE_ROUTE_120_KECLEON_2                               0x3D9
#define FLAG_HIDE_ROUTE_120_KECLEON_3                               0x3DA
#define FLAG_HIDE_ROUTE_120_KECLEON_4                               0x3DB
#define FLAG_HIDE_ROUTE_120_KECLEON_5                               0x3DC
#define FLAG_HIDE_ROUTE_119_KECLEON_1                               0x3DD
#define FLAG_HIDE_ROUTE_119_KECLEON_2                               0x3DE
#define FLAG_HIDE_ROUTE_101_BOY                                     0x3DF
#define FLAG_HIDE_WEATHER_INSTITUTE_2F_AQUA_GRUNT_M                 0x3E0
#define FLAG_HIDE_LILYCOVE_POKEMON_CENTER_CONTEST_LADY_MON          0x3E1
#define FLAG_HIDE_MT_CHIMNEY_LAVA_COOKIE_LADY                       0x3E2
#define FLAG_HIDE_PETALBURG_CITY_SCOTT                              0x3E3
#define FLAG_HIDE_SOOTOPOLIS_CITY_RAYQUAZA                          0x3E4
#define FLAG_HIDE_SOOTOPOLIS_CITY_KYOGRE                            0x3E5
#define FLAG_HIDE_SOOTOPOLIS_CITY_GROUDON                           0x3E6
#define FLAG_HIDE_RUSTBORO_CITY_POKEMON_SCHOOL_SCOTT                0x3E7

// Item Ball Flags
#define FLAG_ITEM_ROUTE_102_POTION                                  0x3E8
#define FLAG_ITEM_ROUTE_116_X_SPECIAL                               0x3E9
#define FLAG_ITEM_ROUTE_104_PP_UP                                   0x3EA
#define FLAG_ITEM_ROUTE_105_IRON                                    0x3EB
#define FLAG_ITEM_ROUTE_106_PROTEIN                                 0x3EC
#define FLAG_ITEM_ROUTE_109_PP_UP                                   0x3ED
#define FLAG_ITEM_ROUTE_110_RARE_CANDY                              0x3EE
#define FLAG_ITEM_ROUTE_110_DIRE_HIT                                0x3EF
#define FLAG_ITEM_ROUTE_111_TM_SANDSTORM                            0x3F0
#define FLAG_ITEM_ROUTE_111_STARDUST                                0x3F1
#define FLAG_ITEM_ROUTE_111_HP_UP                                   0x3F2
#define FLAG_ITEM_ROUTE_112_NUGGET                                  0x3F3
#define FLAG_ITEM_ROUTE_113_MAX_ETHER                               0x3F4
#define FLAG_ITEM_ROUTE_113_SUPER_REPEL                             0x3F5
#define FLAG_ITEM_ROUTE_114_RARE_CANDY                              0x3F6
#define FLAG_ITEM_ROUTE_114_PROTEIN                                 0x3F7
#define FLAG_ITEM_ROUTE_115_SUPER_POTION                            0x3F8
#define FLAG_ITEM_ROUTE_115_TM_FOCUS_PUNCH                          0x3F9
#define FLAG_ITEM_ROUTE_115_IRON                                    0x3FA
#define FLAG_ITEM_ROUTE_116_ETHER                                   0x3FB
#define FLAG_ITEM_ROUTE_116_REPEL                                   0x3FC
#define FLAG_ITEM_ROUTE_116_HP_UP                                   0x3FD
#define FLAG_ITEM_ROUTE_117_GREAT_BALL                              0x3FE
#define FLAG_ITEM_ROUTE_117_REVIVE                                  0x3FF
#define FLAG_ITEM_ROUTE_119_SUPER_REPEL                             0x400
#define FLAG_ITEM_ROUTE_119_ZINC                                    0x401
#define FLAG_ITEM_ROUTE_119_ELIXIR_1                                0x402
#define FLAG_ITEM_ROUTE_119_LEAF_STONE                              0x403
#define FLAG_ITEM_ROUTE_119_RARE_CANDY                              0x404
#define FLAG_ITEM_ROUTE_119_HYPER_POTION_1                          0x405
#define FLAG_ITEM_ROUTE_120_NUGGET                                  0x406
#define FLAG_ITEM_ROUTE_120_TM_SCALD                                0x407 // Project Grounded: was Full Heal
#define FLAG_ITEM_ROUTE_123_CALCIUM                                 0x408
#define FLAG_ITEM_NAVEL_ROCK_FORK_SKY_PLATE                         0x409 // Project Grounded (landvulling): Navel Rock Fork (was R/S-restant)
#define FLAG_ITEM_ROUTE_127_ZINC                                    0x40A
#define FLAG_ITEM_ROUTE_127_CARBOS                                  0x40B
#define FLAG_ITEM_ROUTE_132_RARE_CANDY                              0x40C
#define FLAG_ITEM_ROUTE_133_BIG_PEARL                               0x40D
#define FLAG_ITEM_ROUTE_133_STAR_PIECE                              0x40E
#define FLAG_ITEM_PETALBURG_CITY_MAX_REVIVE                         0x40F
#define FLAG_ITEM_PETALBURG_CITY_ETHER                              0x410
#define FLAG_ITEM_RUSTBORO_CITY_X_DEFEND                            0x411
#define FLAG_ITEM_LILYCOVE_CITY_MAX_REPEL                           0x412
#define FLAG_ITEM_MOSSDEEP_CITY_NET_BALL                            0x413
#define FLAG_ITEM_METEOR_FALLS_1F_1R_TM_IRON_TAIL                   0x414
#define FLAG_ITEM_METEOR_FALLS_1F_1R_FULL_HEAL                      0x415
#define FLAG_ITEM_METEOR_FALLS_1F_1R_MOON_STONE                     0x416
#define FLAG_ITEM_METEOR_FALLS_1F_1R_PP_UP                          0x417
#define FLAG_ITEM_RUSTURF_TUNNEL_POKE_BALL                          0x418
#define FLAG_ITEM_RUSTURF_TUNNEL_MAX_ETHER                          0x419
#define FLAG_ITEM_GRANITE_CAVE_1F_ESCAPE_ROPE                       0x41A
#define FLAG_ITEM_GRANITE_CAVE_B1F_POKE_BALL                        0x41B
#define FLAG_ITEM_MT_PYRE_5F_LAX_INCENSE                            0x41C
#define FLAG_ITEM_GRANITE_CAVE_B2F_REPEL                            0x41D
#define FLAG_ITEM_GRANITE_CAVE_B2F_RARE_CANDY                       0x41E
#define FLAG_ITEM_PETALBURG_WOODS_X_ATTACK                          0x41F
#define FLAG_ITEM_PETALBURG_WOODS_GREAT_BALL                        0x420
#define FLAG_ITEM_ROUTE_104_POKE_BALL                               0x421
#define FLAG_ITEM_PETALBURG_WOODS_ETHER                             0x422
#define FLAG_ITEM_MAGMA_HIDEOUT_3F_3R_ECAPE_ROPE                    0x423
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_1_ORANGE_MAIL                  0x424
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_2_HARBOR_MAIL                  0x425
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_2_WAVE_MAIL                    0x426
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_3_SHADOW_MAIL                  0x427
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_3_WOOD_MAIL                    0x428
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_4_MECH_MAIL                    0x429
#define FLAG_ITEM_ROUTE_124_YELLOW_SHARD                            0x42A
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_6_GLITTER_MAIL                 0x42B
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_7_TROPIC_MAIL                  0x42C
#define FLAG_ITEM_TRICK_HOUSE_PUZZLE_8_BEAD_MAIL                    0x42D
#define FLAG_ITEM_JAGGED_PASS_BURN_HEAL                             0x42E
#define FLAG_ITEM_AQUA_HIDEOUT_B1F_MAX_ELIXIR                       0x42F
#define FLAG_ITEM_AQUA_HIDEOUT_B2F_NEST_BALL                        0x430
#define FLAG_ITEM_MT_PYRE_EXTERIOR_MAX_POTION                       0x431
#define FLAG_ITEM_MT_PYRE_EXTERIOR_TM_SKILL_SWAP                    0x432
#define FLAG_ITEM_NEW_MAUVILLE_ULTRA_BALL                           0x433
#define FLAG_ITEM_NEW_MAUVILLE_ESCAPE_ROPE                          0x434
#define FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_6_LUXURY_BALL    0x435
#define FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_2_SCANNER        0x436
#define FLAG_ITEM_SCORCHED_SLAB_TM_SUNNY_DAY                        0x437
#define FLAG_ITEM_METEOR_FALLS_B1F_2R_TM_DRAGON_CLAW                0x438
#define FLAG_ITEM_SHOAL_CAVE_ENTRANCE_BIG_PEARL                     0x439
#define FLAG_ITEM_SHOAL_CAVE_INNER_ROOM_RARE_CANDY                  0x43A
#define FLAG_ITEM_SHOAL_CAVE_STAIRS_ROOM_ICE_HEAL                   0x43B
#define FLAG_ITEM_VICTORY_ROAD_1F_MAX_ELIXIR                        0x43C
#define FLAG_ITEM_VICTORY_ROAD_1F_PP_UP                             0x43D
#define FLAG_ITEM_VICTORY_ROAD_B1F_TM_PSYCHIC                       0x43E
#define FLAG_ITEM_VICTORY_ROAD_B1F_FULL_RESTORE                     0x43F
#define FLAG_ITEM_VICTORY_ROAD_B2F_FULL_HEAL                        0x440
#define FLAG_ITEM_MT_PYRE_6F_TM_SHADOW_BALL                         0x441
#define FLAG_ITEM_SEAFLOOR_CAVERN_ROOM_9_TM_EARTHQUAKE              0x442
#define FLAG_ITEM_FIERY_PATH_TM_TOXIC                               0x443
#define FLAG_ITEM_ROUTE_124_RED_SHARD                               0x444
#define FLAG_ITEM_ROUTE_124_BLUE_SHARD                              0x445
#define FLAG_ITEM_SAFARI_ZONE_NORTH_WEST_TM_SOLAR_BEAM              0x446
#define FLAG_ITEM_ABANDONED_SHIP_ROOMS_1F_HARBOR_MAIL               0x447
#define FLAG_ITEM_ABANDONED_SHIP_ROOMS_B1F_ESCAPE_ROPE              0x448
#define FLAG_ITEM_ABANDONED_SHIP_ROOMS_2_B1F_DIVE_BALL              0x449
#define FLAG_ITEM_ABANDONED_SHIP_ROOMS_B1F_TM_ICE_BEAM              0x44A
#define FLAG_ITEM_ABANDONED_SHIP_ROOMS_2_1F_REVIVE                  0x44B
#define FLAG_ITEM_ABANDONED_SHIP_CAPTAINS_OFFICE_STORAGE_KEY        0x44C
#define FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_3_WATER_STONE    0x44D
#define FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_1_TM_RAIN_DANCE  0x44E
#define FLAG_ITEM_ROUTE_121_CARBOS                                  0x44F
#define FLAG_ITEM_ROUTE_123_ULTRA_BALL                              0x450
#define FLAG_ITEM_ROUTE_126_GREEN_SHARD                             0x451
#define FLAG_ITEM_ROUTE_119_TM_VOLT_SWITCH                          0x452 // Project Grounded: was Hyper Potion 2
#define FLAG_ITEM_ROUTE_120_HYPER_POTION                            0x453
#define FLAG_ITEM_ROUTE_120_NEST_BALL                               0x454
#define FLAG_ITEM_ROUTE_123_TM_CALM_MIND                            0x455 // Project Grounded: was Elixir
#define FLAG_ITEM_NEW_MAUVILLE_THUNDER_STONE                        0x456
#define FLAG_ITEM_FIERY_PATH_FIRE_STONE                             0x457
#define FLAG_ITEM_SHOAL_CAVE_ICE_ROOM_TM_HAIL                       0x458
#define FLAG_ITEM_SHOAL_CAVE_ICE_ROOM_NEVER_MELT_ICE                0x459
#define FLAG_ITEM_ROUTE_103_GUARD_SPEC                              0x45A
#define FLAG_ITEM_ROUTE_104_X_ACCURACY                              0x45B
#define FLAG_ITEM_MAUVILLE_CITY_X_SPEED                             0x45C
#define FLAG_ITEM_PETALBURG_WOODS_PARALYZE_HEAL                     0x45D
#define FLAG_ITEM_ROUTE_115_GREAT_BALL                              0x45E
#define FLAG_ITEM_SAFARI_ZONE_NORTH_CALCIUM                         0x45F
#define FLAG_ITEM_MT_PYRE_3F_TM_SHADOW_SIPHON                            0x460
#define FLAG_ITEM_ROUTE_118_HYPER_POTION                            0x461
#define FLAG_ITEM_NEW_MAUVILLE_FULL_HEAL                            0x462
#define FLAG_ITEM_NEW_MAUVILLE_PARALYZE_HEAL                        0x463
#define FLAG_ITEM_AQUA_HIDEOUT_B1F_MASTER_BALL                      0x464
#define FLAG_ITEM_SOUTHERN_ISLAND_CAMP_DRAGON_FANG                  0x465 // Project Grounded (landvulling): Southern Island, verlaten kamp (was Ruby-restant)
#define FLAG_ITEM_LIGHT_ISLE_MIND_PLATE                             0x466 // Project Grounded: Lichteiland (Beacon Isle; was Birth Island-kamp)
#define FLAG_ITEM_FARAWAY_ISLAND_CAMP_PP_MAX                        0x467 // Project Grounded (landvulling): Faraway Island, verlaten kamp (was Ruby-restant)
#define FLAG_HIDDEN_ITEM_ZV3_UW125_WAVE_INCENSE                     0x468 // Project Grounded (zeevulling 3)
#define FLAG_ITEM_MT_PYRE_2F_ULTRA_BALL                             0x469
#define FLAG_ITEM_MT_PYRE_4F_SEA_INCENSE                            0x46A
#define FLAG_ITEM_SAFARI_ZONE_SOUTH_WEST_MAX_REVIVE                 0x46B
#define FLAG_ITEM_AQUA_HIDEOUT_B1F_NUGGET                           0x46C
#define FLAG_HIDDEN_ITEM_EVER_GRANDE_FULL_RESTORE                   0x46D // Project Grounded (landvulling): Ever Grande, promenade (was R/S-restant HM08)
#define FLAG_ITEM_ROUTE_119_NUGGET                                  0x46E
#define FLAG_ITEM_ROUTE_104_POTION                                  0x46F
#define FLAG_HIDDEN_ITEM_ZV3_UW129_COMET_SHARD                      0x470 // Project Grounded (zeevulling 3)
#define FLAG_ITEM_ROUTE_103_PP_UP                                   0x471
#define FLAG_HIDDEN_ITEM_ZV3_R122_CLEANSE_TAG                       0x472 // Project Grounded (zeevulling 3)
#define FLAG_ITEM_ROUTE_108_STAR_PIECE                              0x473
#define FLAG_ITEM_ROUTE_109_POTION                                  0x474
#define FLAG_ITEM_ROUTE_110_ELIXIR                                  0x475
#define FLAG_ITEM_ROUTE_111_ELIXIR                                  0x476
#define FLAG_ITEM_ROUTE_113_HYPER_POTION                            0x477
#define FLAG_ITEM_ROUTE_115_HEAL_POWDER                             0x478
#define FLAG_HIDDEN_ITEM_ZV3_R125_BIG_PEARL                         0x479 // Project Grounded (zeevulling 3)
#define FLAG_ITEM_ROUTE_116_POTION                                  0x47A
#define FLAG_ITEM_ROUTE_119_ELIXIR_2                                0x47B
#define FLAG_ITEM_ROUTE_120_REVIVE                                  0x47C
#define FLAG_ITEM_ROUTE_121_REVIVE                                  0x47D
#define FLAG_ITEM_ROUTE_121_ZINC                                    0x47E
#define FLAG_ITEM_MAGMA_HIDEOUT_1F_RARE_CANDY                       0x47F
#define FLAG_ITEM_ROUTE_123_PP_UP                                   0x480
#define FLAG_ITEM_ROUTE_123_REVIVAL_HERB                            0x481
#define FLAG_ITEM_ROUTE_125_BIG_PEARL                               0x482
#define FLAG_ITEM_ROUTE_127_RARE_CANDY                              0x483
#define FLAG_ITEM_ROUTE_132_PROTEIN                                 0x484
#define FLAG_ITEM_ROUTE_133_MAX_REVIVE                              0x485
#define FLAG_ITEM_ROUTE_134_CARBOS                                  0x486
#define FLAG_ITEM_ROUTE_134_STAR_PIECE                              0x487
#define FLAG_ITEM_ROUTE_114_ENERGY_POWDER                           0x488
#define FLAG_ITEM_ROUTE_115_PP_UP                                   0x489
#define FLAG_ITEM_ARTISAN_CAVE_B1F_HP_UP                            0x48A
#define FLAG_ITEM_ARTISAN_CAVE_1F_CARBOS                            0x48B
#define FLAG_ITEM_MAGMA_HIDEOUT_2F_2R_MAX_ELIXIR                    0x48C
#define FLAG_ITEM_MAGMA_HIDEOUT_2F_2R_FULL_RESTORE                  0x48D
#define FLAG_ITEM_MAGMA_HIDEOUT_3F_1R_NUGGET                        0x48E
#define FLAG_ITEM_MAGMA_HIDEOUT_3F_2R_PP_MAX                        0x48F
#define FLAG_ITEM_MAGMA_HIDEOUT_4F_MAX_REVIVE                       0x490
#define FLAG_ITEM_SAFARI_ZONE_NORTH_EAST_NUGGET                     0x491
#define FLAG_ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL                  0x492

#define FLAG_HIDE_ROUTE121_ROCKET_RUNNER                            0x493 // Project Grounded: Rocket-sidequest: grunt die bij de Safari tegen je aan loopt
#define FLAG_HIDE_JUNGLE_ROCKET_GUARD                               0x494 // Project Grounded: Rocket-sidequest: wachtpost bij de holle boom in Fortree Jungle
#define FLAG_HIDE_ROCKET_HIDEOUT_GRUNTS                             0x495 // Project Grounded: Rocket-sidequest: grunts in de hideout (weg na de quest)
#define FLAG_HIDE_ROCKET_EXEC                                       0x496 // Project Grounded: Rocket-sidequest: Petrel en de dief (weg na het gevecht)
#define FLAG_ROCKET_FREE_SAFARI                                     0x497 // Project Grounded: Rocket-sidequest: gratis Safari-ronde tegoed
#define FLAG_ITEM_ROCKET_HIDEOUT_FULL_HEAL                          0x498 // Project Grounded: Rocket-hideout 1F
#define FLAG_ITEM_ROCKET_HIDEOUT_MAX_POTION                         0x499 // Project Grounded: Rocket-hideout B1F
#define FLAG_ITEM_ROCKET_HIDEOUT_PP_UP                              0x49A // Project Grounded: Rocket-hideout B1F
#define FLAG_ITEM_ROCKET_HIDEOUT_NUGGET                             0x49B // Project Grounded: Rocket-hideout B1F
#define FLAG_HIDDEN_ITEM_ZV3_R126_ELIXIR                            0x49C // Project Grounded (zeevulling 3)
#define FLAG_HIDDEN_ITEM_ZV3_R129_BIG_ROOT                          0x49D // Project Grounded (zeevulling 3)
#define FLAG_HIDDEN_ITEM_ZV3_R131_PP_UP                             0x49E // Project Grounded (zeevulling 3)
#define FLAG_RECEIVED_ROUTE_133_ICY_ROCK                            0x49F // Project Grounded (zeevulling 3)
#define FLAG_HIDDEN_ITEM_ZV3_R133_UTILITY_UMBRELLA                  0x4A0 // Project Grounded (zeevulling 3)
#define FLAG_CAUGHT_VOLCANION                                       0x4A1 // Project Grounded: Volcanion (Stoomeiland) gevangen
#define FLAG_DEFEATED_VOLCANION                                     0x4A2 // Project Grounded: Volcanion verslagen/gevangen of nog geen post-game (objectvlag)
#define FLAG_ITEM_METEOR_FALLS_STAR_CORE_COMET_SHARD 0x4A3 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_ECHO_CHAMBER_MAX_ETHER 0x4A4 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_STARFALL_COMET_SHARD 0x4A5 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_METEOR_FALLS_STARFALL_STAR_PIECE 0x4A6 // Project Grounded: Meteor Falls (diepte)
#define FLAG_RECEIVED_METEOR_FALLS_ELDER_GIFT 0x4A7 // Project Grounded: Meteor Falls (diepte)
#define FLAG_ITEM_ROUTE_107_DIVE_BALL                               0x4A8 // Project Grounded (zeevulling 1): Route 107, rots-eilandje
#define FLAG_RECEIVED_ROUTE_107_LEFTOVERS                           0x4A9 // Project Grounded (zeevulling 1): Route 107, sushikok (Leftovers)
#define FLAG_ITEM_ROUTE_126_METAL_COAT                              0x4AA // Project Grounded (zeevulling 1): Route 126, Garbage Patch
#define FLAG_RECEIVED_UMBRELLA_REGINALD 0x4AB // Project Grounded: Victory Road-zijkamers
#define FLAG_HIDE_VICTORY_ROAD_GARCHOMP 0x4AC // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_LIFE_ORB 0x4AD // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_EVIOLITE 0x4AE // Project Grounded: Victory Road-zijkamers
#define FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_DRAGON_FANG 0x4AF // Project Grounded: Victory Road-zijkamers
#define FLAG_ROUTE_126_CRATE_SOLVED                                 0x4B0 // Project Grounded (zeevulling 1): Route 126, raadselkist (PP Max)
#define FLAG_ROUTE_127_WAILMER_RESCUED                              0x4B1 // Project Grounded (zeevulling 1): Route 127, gestrande Wailmer teruggeduwd (object weg, Shell Bell)
#define FLAG_ITEM_UNDERWATER_105_BIG_NUGGET                         0x4B2 // Project Grounded (zeevulling 1): Underwater 105, zeemansgraf
#define FLAG_JAGGED_PASS_LAVA_TUBE_ROCK                             0x4B3 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_LAVA_TUBE_CHARCOAL                                0x4B4 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_LAVA_TUBE_FIRE_STONE                              0x4B5 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_LAVA_TUBE_HEAT_ROCK                               0x4B6 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_LAVA_TUBE_TM_FIRE_BLAST                           0x4B7 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_HIDDEN_ITEM_LAVA_TUBE_LAVA_COOKIE                      0x4B8 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_HIDE_MT_CHIMNEY_TRAIL_GUARD                            0x4B9 // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_HIDE_MT_CHIMNEY_SUMMIT_VOLCARONA                       0x4BA // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_MT_CHIMNEY_SUMMIT_MAGMARIZER                      0x4BB // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_RECEIVED_FLAME_ORB_VOLCANOLOGIST                       0x4BC // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_HIDDEN_ITEM_MT_CHIMNEY_SUMMIT_STAR_PIECE               0x4BD // Project Grounded: Lavabuis / top van Mt. Chimney
#define FLAG_ITEM_ASHFROST_LODGE_NEVER_MELT_ICE                     0x4BE // Project Grounded: Ashfrost Lodge, Never-Melt Ice op het kussen van kamer 2
#define FLAG_ITEM_WHIRL_ISLAND_SHARP_BEAK           0x4BF // Project Grounded (zeevulling 2): Whirl Island, strand van de lagune
#define FLAG_SCORCHED_SLAB_SUN_DOOR_OPEN                            0x4C0 // Project Grounded: Scorched Slab
#define FLAG_HIDE_SCORCHED_SLAB_VOLCARONA                           0x4C1 // Project Grounded: Scorched Slab
#define FLAG_ITEM_SCORCHED_SLAB_SUN_STONE                           0x4C2 // Project Grounded: Scorched Slab
#define FLAG_ITEM_SCORCHED_SLAB_DAMP_ROCK                           0x4C3 // Project Grounded: Scorched Slab
#define FLAG_ITEM_SCORCHED_SLAB_HEAT_ROCK                           0x4C4 // Project Grounded: Scorched Slab
#define FLAG_ITEM_SCORCHED_SLAB_TM_WEATHER_BALL                     0x4C5 // Project Grounded: Scorched Slab
#define FLAG_HIDDEN_ITEM_SCORCHED_SLAB_BIG_NUGGET                   0x4C6 // Project Grounded: Scorched Slab
#define FLAG_CAUGHT_WHIRL_ISLAND_LUGIA                              0x4C7 // Project Grounded: Whirl Island, Lugia gevangen (verslagen = komt terug)
#define FLAG_SEA_TEMPLE_MANAPHY_BATTLED                             0x4C8 // Project Grounded: zeetempel, eerste gevecht met Manaphy gehad (ei verschijnt op het altaar)
#define FLAG_HIDDEN_ITEM_SHIPWRECK_SHOALS_BIG_PEARL                 0x4C9 // Project Grounded: Shipwreck Shoals, verborgen Big Pearl
#define FLAG_ITEM_SHIPWRECK_SHOALS_REAPER_CLOTH                     0x4CA // Project Grounded: Shipwreck Shoals, Reaper Cloth op de ondiepte
#define FLAG_GHOST_SHIP_PIECE_BIN                                   0x4CB // Project Grounded: spookschip, kaartstuk uit de prullenbak van de kapitein
#define FLAG_GHOST_SHIP_PIECE_CABIN                                 0x4CC // Project Grounded: spookschip, kaartstuk in de hut (ook verbergflag van het object)
#define FLAG_GHOST_SHIP_PIECE_MORGAN                                0x4CD // Project Grounded: spookschip, kaartstuk van Morgan (na het gevecht)
#define FLAG_GHOST_SHIP_MAP_RETURNED                                0x4CE // Project Grounded: schatkaart terug bij kapitein Grimsby (na het gevecht)
#define FLAG_SHIPWRECK_TREASURE_FOUND                               0x4CF // Project Grounded: schat van Grimsby opgegraven (Shipwreck Shoals)
#define FLAG_DEFEATED_ZARUDE                                        0x4D0 // Project Grounded: Zarude gevangen of verslagen (Fortree Jungle; verslagen = terug na de League)
#define FLAG_CAUGHT_ZARUDE                                          0x4D1 // Project Grounded: Zarude gevangen
#define FLAG_HIDE_FORTREE_JUNGLE_ZARUDE                             0x4D2 // Project Grounded: Zarude-object in de boomkruin (verborgen tot de scene)
#define FLAG_ITEM_MANGROVE_MIRE_BLACK_SLUDGE                        0x4D3 // Project Grounded: Mangrove Mire
#define FLAG_ITEM_MANGROVE_MIRE_MYSTIC_WATER                        0x4D4 // Project Grounded: Mangrove Mire
#define FLAG_ITEM_MANGROVE_MIRE_ABSORB_BULB                         0x4D5 // Project Grounded: Mangrove Mire
#define FLAG_ITEM_MANGROVE_MIRE_TOXIC_ORB                           0x4D6 // Project Grounded: Mangrove Mire (Toxic Orb)
#define FLAG_HIDDEN_ITEM_MANGROVE_MIRE_BIG_ROOT                     0x4D7 // Project Grounded: Mangrove Mire
#define FLAG_HIDDEN_ITEM_MANGROVE_MIRE_ULTRA_BALL                   0x4D8 // Project Grounded: Mangrove Mire
#define FLAG_OGERPON_QUEST_STARTED                                  0x4D9 // Project Grounded: Ogerpon-quest: maskerhoedster heeft het verhaal verteld (openingen naar de schuilplaatsen)
#define FLAG_DEFEATED_OKIDOGI                                       0x4DA // Project Grounded: Ogerpon-quest: Okidogi gevangen of verslagen (Granite Cave; verslagen = terug na de League)
#define FLAG_CAUGHT_OKIDOGI                                         0x4DB // Project Grounded: Ogerpon-quest: Okidogi gevangen
#define FLAG_DEFEATED_MUNKIDORI                                     0x4DC // Project Grounded: Ogerpon-quest: Munkidori gevangen of verslagen (Fiery Path; verslagen = terug na de League)
#define FLAG_CAUGHT_MUNKIDORI                                       0x4DD // Project Grounded: Ogerpon-quest: Munkidori gevangen
#define FLAG_DEFEATED_FEZANDIPITI                                   0x4DE // Project Grounded: Ogerpon-quest: Fezandipiti gevangen of verslagen (Route 127 onderwater; verslagen = terug na de League)
#define FLAG_CAUGHT_FEZANDIPITI                                     0x4DF // Project Grounded: Ogerpon-quest: Fezandipiti gevangen
#define FLAG_RECEIVED_CORNERSTONE_MASK                              0x4E0 // Project Grounded: Ogerpon-quest: Cornerstone Mask terugveroverd (Okidogi)
#define FLAG_RECEIVED_HEARTHFLAME_MASK                              0x4E1 // Project Grounded: Ogerpon-quest: Hearthflame Mask terugveroverd (Munkidori)
#define FLAG_RECEIVED_WELLSPRING_MASK                               0x4E2 // Project Grounded: Ogerpon-quest: Wellspring Mask terugveroverd (Fezandipiti)
#define FLAG_OGERPON_MASKS_PLACED                                   0x4E3 // Project Grounded: Ogerpon-quest: de maskers liggen op het altaar in Fortree Jungle (Ogerpon is verschenen)
#define FLAG_DEFEATED_OGERPON                                       0x4E4 // Project Grounded: Ogerpon-quest: Ogerpon gevangen of verslagen (verslagen = terug na de League)
#define FLAG_CAUGHT_OGERPON                                         0x4E5 // Project Grounded: Ogerpon-quest: Ogerpon gevangen
#define FLAG_HIDE_FORTREE_JUNGLE_OGERPON                            0x4E6 // Project Grounded: Ogerpon-quest: Ogerpon-object achter het altaar
#define FLAG_OGERPON_MASKS_RETURNED                                 0x4E7 // Project Grounded: Ogerpon-quest: de speler heeft de drie maskers terug als hold items
#define FLAG_RECEIVED_WHIRL_ISLAND_KINGS_ROCK       0x4E8 // Project Grounded (zeevulling 2): Whirl Island, zwijgende wachter (King's Rock)
#define FLAG_ITEM_METEOR_SPACE_COMET_SHARD                          0x4E9 // Project Grounded: meteoriet in de ruimte (Deoxys-event)
#define FLAG_ITEM_METEOR_SPACE_STAR_PIECE                           0x4EA // Project Grounded: meteoriet in de ruimte
#define FLAG_ITEM_METEOR_SPACE_MOON_STONE                           0x4EB // Project Grounded: meteoriet in de ruimte
#define FLAG_METEOR_SPACE_RETURNED                                  0x4EC // Project Grounded: een keer heelhuids terug uit de ruimte (kortere teksten daarna)
#define FLAG_ITEM_ROUTE_134_LIGHT_CLAY              0x4ED // Project Grounded (zeevulling 2): Route 134, bouwplaats vuurtoren
#define FLAG_ITEM_ROUTE_133_CHOICE_SPECS            0x4EE // Project Grounded (zeevulling 2): Route 133, zandbank van de influencer
#define FLAG_ITEM_ROUTE_130_EVERSTONE               0x4EF // Project Grounded (zeevulling 2): Route 130, Wynaut-kinderopvang

#define FLAG_DEFEATED_RUSTBORO_GYM                                  0x4F0
#define FLAG_DEFEATED_DEWFORD_GYM                                   0x4F1
#define FLAG_DEFEATED_MAUVILLE_GYM                                  0x4F2
#define FLAG_DEFEATED_LAVARIDGE_GYM                                 0x4F3
#define FLAG_DEFEATED_PETALBURG_GYM                                 0x4F4
#define FLAG_DEFEATED_FORTREE_GYM                                   0x4F5
#define FLAG_DEFEATED_MOSSDEEP_GYM                                  0x4F6
#define FLAG_DEFEATED_SOOTOPOLIS_GYM                                0x4F7
#define FLAG_DEFEATED_METEOR_FALLS_STEVEN                           0x4F8

#define FLAG_ITEM_ROUTE_128_BLACK_BELT              0x4F9 // Project Grounded (zeevulling 2): Route 128, Dereks dojo
#define FLAG_RECEIVED_ROUTE_124_SMOOTH_ROCK         0x4FA // Project Grounded (zeevulling 2): Route 124, weerman (Smooth Rock)

#define FLAG_DEFEATED_ELITE_4_SIDNEY                                0x4FB
#define FLAG_DEFEATED_ELITE_4_PHOEBE                                0x4FC
#define FLAG_DEFEATED_ELITE_4_GLACIA                                0x4FD
#define FLAG_DEFEATED_ELITE_4_DRAKE                                 0x4FE

#define FLAG_RECEIVED_ROUTE_105_FOCUS_SASH          0x4FF // Project Grounded (zeevulling 2): Route 105, schipbreukeling (Focus Sash)

// Trainer Flags
// Trainer flags occupy 0x500 - 0x85F, the last 9 of which are unused
// See constants/opponents.h. The values there + FLAG_TRAINER_FLAG_START are the flag IDs

#define TRAINER_FLAGS_START                                         0x500
#define TRAINER_FLAGS_END                                           (TRAINER_FLAGS_START + MAX_TRAINERS_COUNT - 1) // 0x85F

// System Flags

#define SYSTEM_FLAGS                                   (TRAINER_FLAGS_END + 1) // 0x860

#define FLAG_SYS_POKEMON_GET                         (SYSTEM_FLAGS + 0x0) // FLAG_0x860
#define FLAG_SYS_POKEDEX_GET                         (SYSTEM_FLAGS + 0x1)
#define FLAG_SYS_POKENAV_GET                         (SYSTEM_FLAGS + 0x2)
#define FLAG_DEFEATED_TAPU_BULU                      (SYSTEM_FLAGS + 0x3) // Project Grounded: Tapu-eiland: Tapu Bulu verslagen/gevangen
#define FLAG_SYS_GAME_CLEAR                          (SYSTEM_FLAGS + 0x4)
#define FLAG_SYS_CHAT_USED                           (SYSTEM_FLAGS + 0x5)
#define FLAG_UNLOCKED_TRENDY_SAYINGS                 (SYSTEM_FLAGS + 0x6)

// Badges
#define FLAG_BADGE01_GET                             (SYSTEM_FLAGS + 0x7)
#define FLAG_BADGE02_GET                             (SYSTEM_FLAGS + 0x8)
#define FLAG_BADGE03_GET                             (SYSTEM_FLAGS + 0x9)
#define FLAG_BADGE04_GET                             (SYSTEM_FLAGS + 0xA)
#define FLAG_BADGE05_GET                             (SYSTEM_FLAGS + 0xB)
#define FLAG_BADGE06_GET                             (SYSTEM_FLAGS + 0xC)
#define FLAG_BADGE07_GET                             (SYSTEM_FLAGS + 0xD)
#define FLAG_BADGE08_GET                             (SYSTEM_FLAGS + 0xE)
#define NUM_BADGES                                   (1 + FLAG_BADGE08_GET - FLAG_BADGE01_GET)

// Towns and Cities
#define FLAG_VISITED_LITTLEROOT_TOWN                (SYSTEM_FLAGS + 0xF)
#define FLAG_VISITED_OLDALE_TOWN                    (SYSTEM_FLAGS + 0x10)
#define FLAG_VISITED_DEWFORD_TOWN                   (SYSTEM_FLAGS + 0x11)
#define FLAG_VISITED_LAVARIDGE_TOWN                 (SYSTEM_FLAGS + 0x12)
#define FLAG_VISITED_FALLARBOR_TOWN                 (SYSTEM_FLAGS + 0x13)
#define FLAG_VISITED_VERDANTURF_TOWN                (SYSTEM_FLAGS + 0x14)
#define FLAG_VISITED_PACIFIDLOG_TOWN                (SYSTEM_FLAGS + 0x15)
#define FLAG_VISITED_PETALBURG_CITY                 (SYSTEM_FLAGS + 0x16)
#define FLAG_VISITED_SLATEPORT_CITY                 (SYSTEM_FLAGS + 0x17)
#define FLAG_VISITED_MAUVILLE_CITY                  (SYSTEM_FLAGS + 0x18)
#define FLAG_VISITED_RUSTBORO_CITY                  (SYSTEM_FLAGS + 0x19)
#define FLAG_VISITED_FORTREE_CITY                   (SYSTEM_FLAGS + 0x1A)
#define FLAG_VISITED_LILYCOVE_CITY                  (SYSTEM_FLAGS + 0x1B)
#define FLAG_VISITED_MOSSDEEP_CITY                  (SYSTEM_FLAGS + 0x1C)
#define FLAG_VISITED_SOOTOPOLIS_CITY                (SYSTEM_FLAGS + 0x1D)
#define FLAG_VISITED_EVER_GRANDE_CITY               (SYSTEM_FLAGS + 0x1E)

#define FLAG_IS_CHAMPION                            (SYSTEM_FLAGS + 0x1F) // Seems to be related to linking.
#define FLAG_NURSE_UNION_ROOM_REMINDER              (SYSTEM_FLAGS + 0x20)

#define FLAG_DEFEATED_TAPU_FINI                     (SYSTEM_FLAGS + 0x21) // Project Grounded: Tapu-eiland: Tapu Fini verslagen/gevangen
#define FLAG_TAPU_LELE_AWAKE                        (SYSTEM_FLAGS + 0x22) // Project Grounded: Tapu-eiland: Tapu Lele wakker (Koko een keer verslagen/gevangen)
#define FLAG_TAPU_BULU_AWAKE                        (SYSTEM_FLAGS + 0x23) // Project Grounded: Tapu-eiland: Tapu Bulu wakker (na Lele)
#define FLAG_TAPU_FINI_AWAKE                        (SYSTEM_FLAGS + 0x24) // Project Grounded: Tapu-eiland: Tapu Fini wakker (na Bulu)
#define FLAG_CAUGHT_CRESSELIA                       (SYSTEM_FLAGS + 0x25) // Project Grounded: Fullmoon Island: Cresselia gevangen
#define FLAG_DEFEATED_CRESSELIA                     (SYSTEM_FLAGS + 0x26) // Project Grounded: Fullmoon Island: Cresselia verslagen/gevangen (terug na de League als niet gevangen)
#define FLAG_HIDDEN_ITEM_TAPU_ISLE_BIG_PEARL        (SYSTEM_FLAGS + 0x27) // Project Grounded: Tapu-eiland: verborgen Big Pearl

#define FLAG_SYS_USE_FLASH                          (SYSTEM_FLAGS + 0x28)
#define FLAG_SYS_USE_STRENGTH                       (SYSTEM_FLAGS + 0x29)
// Sets abnormal weather on maps that check for it
#define FLAG_SYS_WEATHER_CTRL                       (SYSTEM_FLAGS + 0x2A)
#define FLAG_SYS_CYCLING_ROAD                       (SYSTEM_FLAGS + 0x2B)
#define FLAG_SYS_SAFARI_MODE                        (SYSTEM_FLAGS + 0x2C)
#define FLAG_SYS_CRUISE_MODE                        (SYSTEM_FLAGS + 0x2D)

#define FLAG_ITEM_TAPU_ISLE_STAR_PIECE              (SYSTEM_FLAGS + 0x2E) // Project Grounded: Tapu-eiland: Star Piece (Bulu-ruine)
#define FLAG_HIDDEN_ITEM_FULLMOON_ISLAND_MOON_STONE (SYSTEM_FLAGS + 0x2F) // Project Grounded: Fullmoon Island: verborgen Moon Stone

#define FLAG_SYS_TV_HOME                            (SYSTEM_FLAGS + 0x30)
#define FLAG_SYS_TV_WATCH                           (SYSTEM_FLAGS + 0x31)
#define FLAG_SYS_TV_START                           (SYSTEM_FLAGS + 0x32)
#define FLAG_SYS_CHANGED_DEWFORD_TREND              (SYSTEM_FLAGS + 0x33)
#define FLAG_SYS_MIX_RECORD                         (SYSTEM_FLAGS + 0x34)
#define FLAG_SYS_CLOCK_SET                          (SYSTEM_FLAGS + 0x35)
#define FLAG_SYS_NATIONAL_DEX                       (SYSTEM_FLAGS + 0x36)
#define FLAG_HIDDEN_ITEM_SAFARI_FAIRY_MEADOW_PLATE  (SYSTEM_FLAGS + 0x37) // Project Grounded (landvulling): verborgen item (was SYS_CAVE_SHIP, ongebruikt)
#define FLAG_HIDDEN_ITEM_SAFARI_THUNDER_ELECTIRIZER (SYSTEM_FLAGS + 0x38) // Project Grounded (landvulling): verborgen item (was SYS_CAVE_WONDER, ongebruikt)
#define FLAG_HIDDEN_ITEM_SAFARI_SPOOK_CLEANSE_TAG   (SYSTEM_FLAGS + 0x39) // Project Grounded (landvulling): verborgen item (was SYS_CAVE_BATTLE, ongebruikt)
#define FLAG_SYS_SHOAL_TIDE                         (SYSTEM_FLAGS + 0x3A)
#define FLAG_SYS_RIBBON_GET                         (SYSTEM_FLAGS + 0x3B)

#define FLAG_LANDMARK_FLOWER_SHOP                   (SYSTEM_FLAGS + 0x3C)
#define FLAG_LANDMARK_MR_BRINEY_HOUSE               (SYSTEM_FLAGS + 0x3D)
#define FLAG_LANDMARK_ABANDONED_SHIP                (SYSTEM_FLAGS + 0x3E)
#define FLAG_LANDMARK_SEASHORE_HOUSE                (SYSTEM_FLAGS + 0x3F)
#define FLAG_LANDMARK_NEW_MAUVILLE                  (SYSTEM_FLAGS + 0x40)
#define FLAG_LANDMARK_OLD_LADY_REST_SHOP            (SYSTEM_FLAGS + 0x41)
#define FLAG_LANDMARK_TRICK_HOUSE                   (SYSTEM_FLAGS + 0x42)
#define FLAG_LANDMARK_WINSTRATE_FAMILY              (SYSTEM_FLAGS + 0x43)
#define FLAG_LANDMARK_GLASS_WORKSHOP                (SYSTEM_FLAGS + 0x44)
#define FLAG_LANDMARK_LANETTES_HOUSE                (SYSTEM_FLAGS + 0x45)
#define FLAG_LANDMARK_POKEMON_DAYCARE               (SYSTEM_FLAGS + 0x46)
#define FLAG_LANDMARK_SEAFLOOR_CAVERN               (SYSTEM_FLAGS + 0x47)
#define FLAG_LANDMARK_BATTLE_FRONTIER               (SYSTEM_FLAGS + 0x48)
#define FLAG_LANDMARK_SOUTHERN_ISLAND               (SYSTEM_FLAGS + 0x49)
#define FLAG_LANDMARK_FIERY_PATH                    (SYSTEM_FLAGS + 0x4A)

#define FLAG_SYS_PC_LANETTE                         (SYSTEM_FLAGS + 0x4B)
#define FLAG_SYS_MYSTERY_EVENT_ENABLE               (SYSTEM_FLAGS + 0x4C)
#define FLAG_SYS_ENC_UP_ITEM                        (SYSTEM_FLAGS + 0x4D)
#define FLAG_SYS_ENC_DOWN_ITEM                      (SYSTEM_FLAGS + 0x4E)
#define FLAG_SYS_BRAILLE_DIG                        (SYSTEM_FLAGS + 0x4F)
#define FLAG_SYS_REGIROCK_PUZZLE_COMPLETED          (SYSTEM_FLAGS + 0x50)
#define FLAG_SYS_BRAILLE_REGICE_COMPLETED           (SYSTEM_FLAGS + 0x51)
#define FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED         (SYSTEM_FLAGS + 0x52)
#define FLAG_ENABLE_SHIP_SOUTHERN_ISLAND            (SYSTEM_FLAGS + 0x53)

#define FLAG_LANDMARK_POKEMON_LEAGUE                (SYSTEM_FLAGS + 0x54)
#define FLAG_LANDMARK_ISLAND_CAVE                   (SYSTEM_FLAGS + 0x55)
#define FLAG_LANDMARK_DESERT_RUINS                  (SYSTEM_FLAGS + 0x56)
#define FLAG_LANDMARK_FOSSIL_MANIACS_HOUSE          (SYSTEM_FLAGS + 0x57)
#define FLAG_LANDMARK_SCORCHED_SLAB                 (SYSTEM_FLAGS + 0x58)
#define FLAG_LANDMARK_ANCIENT_TOMB                  (SYSTEM_FLAGS + 0x59)
#define FLAG_LANDMARK_TUNNELERS_REST_HOUSE          (SYSTEM_FLAGS + 0x5A)
#define FLAG_LANDMARK_HUNTERS_HOUSE                 (SYSTEM_FLAGS + 0x5B)
#define FLAG_LANDMARK_SEALED_CHAMBER                (SYSTEM_FLAGS + 0x5C)

#define FLAG_SYS_TV_LATIAS_LATIOS                   (SYSTEM_FLAGS + 0x5D)

#define FLAG_LANDMARK_SKY_PILLAR                    (SYSTEM_FLAGS + 0x5E)

#define FLAG_SYS_SHOAL_ITEM                         (SYSTEM_FLAGS + 0x5F)
#define FLAG_SYS_B_DASH                             (SYSTEM_FLAGS + 0x60) // RECEIVED Running Shoes
#define FLAG_SYS_CTRL_OBJ_DELETE                    (SYSTEM_FLAGS + 0x61)
#define FLAG_SYS_RESET_RTC_ENABLE                   (SYSTEM_FLAGS + 0x62)

#define FLAG_LANDMARK_BERRY_MASTERS_HOUSE           (SYSTEM_FLAGS + 0x63)

#define FLAG_SYS_TOWER_SILVER                       (SYSTEM_FLAGS + 0x64)
#define FLAG_SYS_TOWER_GOLD                         (SYSTEM_FLAGS + 0x65)
#define FLAG_SYS_DOME_SILVER                        (SYSTEM_FLAGS + 0x66)
#define FLAG_SYS_DOME_GOLD                          (SYSTEM_FLAGS + 0x67)
#define FLAG_SYS_PALACE_SILVER                      (SYSTEM_FLAGS + 0x68)
#define FLAG_SYS_PALACE_GOLD                        (SYSTEM_FLAGS + 0x69)
#define FLAG_SYS_ARENA_SILVER                       (SYSTEM_FLAGS + 0x6A)
#define FLAG_SYS_ARENA_GOLD                         (SYSTEM_FLAGS + 0x6B)
#define FLAG_SYS_FACTORY_SILVER                     (SYSTEM_FLAGS + 0x6C)
#define FLAG_SYS_FACTORY_GOLD                       (SYSTEM_FLAGS + 0x6D)
#define FLAG_SYS_PIKE_SILVER                        (SYSTEM_FLAGS + 0x6E)
#define FLAG_SYS_PIKE_GOLD                          (SYSTEM_FLAGS + 0x6F)
#define FLAG_SYS_PYRAMID_SILVER                     (SYSTEM_FLAGS + 0x70)
#define FLAG_SYS_PYRAMID_GOLD                       (SYSTEM_FLAGS + 0x71)
#define FLAG_SYS_FRONTIER_PASS                      (SYSTEM_FLAGS + 0x72)

#define FLAG_MAP_SCRIPT_CHECKED_DEOXYS              (SYSTEM_FLAGS + 0x73)
#define FLAG_DEOXYS_ROCK_COMPLETE                   (SYSTEM_FLAGS + 0x74)
#define FLAG_UNUSED_SYS_0x75                        (SYSTEM_FLAGS + 0x75) // Project Grounded: was FLAG_ENABLE_SHIP_BIRTH_ISLAND
#define FLAG_ENABLE_SHIP_FARAWAY_ISLAND             (SYSTEM_FLAGS + 0x76)

#define FLAG_SHOWN_BOX_WAS_FULL_MESSAGE             (SYSTEM_FLAGS + 0x77)

#define FLAG_ARRIVED_ON_FARAWAY_ISLAND              (SYSTEM_FLAGS + 0x78)
#define FLAG_ARRIVED_AT_MARINE_CAVE_EMERGE_SPOT     (SYSTEM_FLAGS + 0x79)
#define FLAG_ARRIVED_AT_TERRA_CAVE_ENTRANCE         (SYSTEM_FLAGS + 0x7A)

#define FLAG_SYS_MYSTERY_GIFT_ENABLE                (SYSTEM_FLAGS + 0x7B)

#define FLAG_ENTERED_MIRAGE_TOWER                   (SYSTEM_FLAGS + 0x7C)
#define FLAG_LANDMARK_ALTERING_CAVE                 (SYSTEM_FLAGS + 0x7D)
#define FLAG_LANDMARK_DESERT_UNDERPASS              (SYSTEM_FLAGS + 0x7E)
#define FLAG_LANDMARK_ARTISAN_CAVE                  (SYSTEM_FLAGS + 0x7F)
#define FLAG_ENABLE_SHIP_NAVEL_ROCK                 (SYSTEM_FLAGS + 0x80)
#define FLAG_ARRIVED_AT_NAVEL_ROCK                  (SYSTEM_FLAGS + 0x81)
#define FLAG_LANDMARK_TRAINER_HILL                  (SYSTEM_FLAGS + 0x82)

#define FLAG_HIDDEN_ITEM_MT_PYRE_EXT_PURE_INCENSE   (SYSTEM_FLAGS + 0x83) // Project Grounded (landvulling): verborgen item

#define FLAG_RECEIVED_POKEDEX_FROM_BIRCH            (SYSTEM_FLAGS + 0x84)

#define FLAG_HIDDEN_ITEM_MT_PYRE_EXT_RARE_BONE      (SYSTEM_FLAGS + 0x85) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_MT_PYRE_EXT_REVIVAL_HERB   (SYSTEM_FLAGS + 0x86) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_MT_PYRE_EXT_DUSK_BALL      (SYSTEM_FLAGS + 0x87) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_DESERT_UNDERPASS_RARE_BONE (SYSTEM_FLAGS + 0x88) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_NAVEL_ROCK_FORK_PP_MAX     (SYSTEM_FLAGS + 0x89) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_SOUTHERN_ISLAND_CAMP_BIG_NUGGET (SYSTEM_FLAGS + 0x8A) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_LIGHT_ISLE_STAR_PIECE (SYSTEM_FLAGS + 0x8B) // Project Grounded: verborgen item op het Lichteiland (was Birth Island-kamp)
#define FLAG_HIDDEN_ITEM_FARAWAY_ISLAND_CAMP_BIG_MUSHROOM (SYSTEM_FLAGS + 0x8C) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_HEATRAN_LAIR_FLAME_PLATE   (SYSTEM_FLAGS + 0x8D) // Project Grounded (landvulling): verborgen item
#define FLAG_HIDDEN_ITEM_ZV2_R120_PEARL_STRING      (SYSTEM_FLAGS + 0x8E) // Project Grounded (zeevulling 2): verborgen item (Route120)
#define FLAG_HIDDEN_ITEM_ZV2_R119_MYSTIC_WATER      (SYSTEM_FLAGS + 0x8F) // Project Grounded (zeevulling 2): verborgen item (Route119)
#define FLAG_HIDDEN_ITEM_ZV2_R118_HEART_SCALE       (SYSTEM_FLAGS + 0x90) // Project Grounded (zeevulling 2): verborgen item (Route118)
#define FLAG_HIDDEN_ITEM_ZV2_R115_BIG_PEARL         (SYSTEM_FLAGS + 0x91) // Project Grounded (zeevulling 2): verborgen item (Route115)
#define FLAG_HIDDEN_ITEM_ZV2_R110_PEARL             (SYSTEM_FLAGS + 0x92) // Project Grounded (zeevulling 2): verborgen item (Route110)
#define FLAG_HIDDEN_ITEM_ZV2_WHIRL_BIG_NUGGET       (SYSTEM_FLAGS + 0x93) // Project Grounded (zeevulling 2): verborgen item (WhirlIsland)
#define FLAG_HIDDEN_ITEM_ZV2_WHIRL_PP_MAX           (SYSTEM_FLAGS + 0x94) // Project Grounded (zeevulling 2): verborgen item (WhirlIsland)
#define FLAG_HIDDEN_ITEM_ZV2_R134_ZINC              (SYSTEM_FLAGS + 0x95) // Project Grounded (zeevulling 2): verborgen item (Route134)
#define FLAG_HIDDEN_ITEM_ZV2_R134_STAR_PIECE        (SYSTEM_FLAGS + 0x96) // Project Grounded (zeevulling 2): verborgen item (Route134)
#define FLAG_HIDDEN_ITEM_ZV2_R133_PEARL             (SYSTEM_FLAGS + 0x97) // Project Grounded (zeevulling 2): verborgen item (Route133)
#define FLAG_HIDDEN_ITEM_ZV2_R133_NUGGET            (SYSTEM_FLAGS + 0x98) // Project Grounded (zeevulling 2): verborgen item (Route133)
#define FLAG_HIDDEN_ITEM_ZV2_R131_BIG_PEARL         (SYSTEM_FLAGS + 0x99) // Project Grounded (zeevulling 2): verborgen item (Route131)
#define FLAG_HIDDEN_ITEM_ZV2_R131_HYPER_POTION      (SYSTEM_FLAGS + 0x9A) // Project Grounded (zeevulling 2): verborgen item (Route131)
#define FLAG_HIDDEN_ITEM_ZV2_R130_STARDUST          (SYSTEM_FLAGS + 0x9B) // Project Grounded (zeevulling 2): verborgen item (Route130)
#define FLAG_HIDDEN_ITEM_ZV2_R130_LUCKY_PUNCH       (SYSTEM_FLAGS + 0x9C) // Project Grounded (zeevulling 2): verborgen item (Route130)
#define FLAG_HIDDEN_ITEM_ZV2_R129_ULTRA_BALL        (SYSTEM_FLAGS + 0x9D) // Project Grounded (zeevulling 2): verborgen item (Route129)
#define FLAG_HIDDEN_ITEM_ZV2_R129_PEARL_STRING      (SYSTEM_FLAGS + 0x9E) // Project Grounded (zeevulling 2): verborgen item (Route129)
#define FLAG_HIDDEN_ITEM_ZV2_R128_STAR_PIECE        (SYSTEM_FLAGS + 0x9F) // Project Grounded (zeevulling 2): verborgen item (Route128)
#define FLAG_HIDDEN_ITEM_ZV2_R128_HP_UP             (SYSTEM_FLAGS + 0xA0) // Project Grounded (zeevulling 2): verborgen item (Route128)
#define FLAG_HIDDEN_ITEM_ZV2_R128_PROTEIN           (SYSTEM_FLAGS + 0xA1) // Project Grounded (zeevulling 2): verborgen item (Route128)
#define FLAG_HIDDEN_ITEM_ZV2_R124_HEART_SCALE       (SYSTEM_FLAGS + 0xA2) // Project Grounded (zeevulling 2): verborgen item (Route124)
#define FLAG_HIDDEN_ITEM_ZV2_R124_BIG_PEARL         (SYSTEM_FLAGS + 0xA3) // Project Grounded (zeevulling 2): verborgen item (Route124)
#define FLAG_HIDDEN_ITEM_ZV2_R124_PP_UP             (SYSTEM_FLAGS + 0xA4) // Project Grounded (zeevulling 2): verborgen item (Route124)
#define FLAG_HIDDEN_ITEM_ZV2_R122_RARE_BONE         (SYSTEM_FLAGS + 0xA5) // Project Grounded (zeevulling 2): verborgen item (Route122)
#define FLAG_HIDDEN_ITEM_ZV2_R122_SPELL_TAG         (SYSTEM_FLAGS + 0xA6) // Project Grounded (zeevulling 2): verborgen item (Route122)
#define FLAG_HIDDEN_ITEM_ZV2_R108_METAL_COAT        (SYSTEM_FLAGS + 0xA7) // Project Grounded (zeevulling 2): verborgen item (Route108)
#define FLAG_HIDDEN_ITEM_ZV2_R108_NUGGET            (SYSTEM_FLAGS + 0xA8) // Project Grounded (zeevulling 2): verborgen item (Route108)
#define FLAG_HIDDEN_ITEM_ZV2_R108_PEARL             (SYSTEM_FLAGS + 0xA9) // Project Grounded (zeevulling 2): verborgen item (Route108)
#define FLAG_HIDDEN_ITEM_ZV2_R105_HEART_SCALE       (SYSTEM_FLAGS + 0xAA) // Project Grounded (zeevulling 2): verborgen item (Route105)
#define FLAG_HIDDEN_ITEM_ZV2_R105_STAR_PIECE        (SYSTEM_FLAGS + 0xAB) // Project Grounded (zeevulling 2): verborgen item (Route105)
#define FLAG_HIDDEN_ITEM_ZV2_R105_BIG_PEARL         (SYSTEM_FLAGS + 0xAC) // Project Grounded (zeevulling 2): verborgen item (Route105)
#define FLAG_HIDDEN_ITEM_ROUTE_107_BIG_PEARL        (SYSTEM_FLAGS + 0xAD) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_107_HARD_STONE       (SYSTEM_FLAGS + 0xAE) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_126_BERRY_JUICE      (SYSTEM_FLAGS + 0xAF) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_126_BLACK_SLUDGE     (SYSTEM_FLAGS + 0xB0) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_126_PRETTY_FEATHER   (SYSTEM_FLAGS + 0xB1) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_127_BIG_PEARL        (SYSTEM_FLAGS + 0xB2) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_127_MYSTIC_WATER     (SYSTEM_FLAGS + 0xB3) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_ROUTE_127_DAMP_ROCK        (SYSTEM_FLAGS + 0xB4) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_105_DEEP_SEA_TOOTH (SYSTEM_FLAGS + 0xB5) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_105_HEART_SCALE (SYSTEM_FLAGS + 0xB6) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_105_BIG_PEARL   (SYSTEM_FLAGS + 0xB7) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_125_NEVER_MELT_ICE (SYSTEM_FLAGS + 0xB8) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_125_HEART_SCALE (SYSTEM_FLAGS + 0xB9) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_128_DEEP_SEA_SCALE (SYSTEM_FLAGS + 0xBA) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_128_STAR_PIECE  (SYSTEM_FLAGS + 0xBB) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_129_DRAGON_SCALE (SYSTEM_FLAGS + 0xBC) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_129_PEARL       (SYSTEM_FLAGS + 0xBD) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_HIDDEN_ITEM_UNDERWATER_129_HEART_SCALE (SYSTEM_FLAGS + 0xBE) // Project Grounded (zeevulling 1): verborgen item
#define FLAG_UNUSED_0x91F                           (SYSTEM_FLAGS + 0xBF) // Unused Flag

// Daily Flags
// These flags are cleared once per day
// The start and end are byte-aligned because the flags are cleared in byte increments
#define DAILY_FLAGS_START                           (FLAG_UNUSED_0x91F + (8 - FLAG_UNUSED_0x91F % 8))
#define FLAG_UNUSED_0x920                           (DAILY_FLAGS_START + 0x0)  // Unused Flag
#define FLAG_DAILY_CONTEST_LOBBY_RECEIVED_BERRY     (DAILY_FLAGS_START + 0x1)
#define FLAG_DAILY_SECRET_BASE                      (DAILY_FLAGS_START + 0x2)
#define FLAG_DAILY_WEATHER_SERVICE_BATTLE           (DAILY_FLAGS_START + 0x3)  // Project Grounded: Archie en Maxie vandaag al bevochten
#define FLAG_UNUSED_0x924                           (DAILY_FLAGS_START + 0x4)  // Unused Flag
#define FLAG_UNUSED_0x925                           (DAILY_FLAGS_START + 0x5)  // Unused Flag
#define FLAG_UNUSED_0x926                           (DAILY_FLAGS_START + 0x6)  // Unused Flag
#define FLAG_UNUSED_0x927                           (DAILY_FLAGS_START + 0x7)  // Unused Flag
#define FLAG_UNUSED_0x928                           (DAILY_FLAGS_START + 0x8)  // Unused Flag
#define FLAG_UNUSED_0x929                           (DAILY_FLAGS_START + 0x9)  // Unused Flag
#define FLAG_DAILY_PICKED_LOTO_TICKET               (DAILY_FLAGS_START + 0xA)
#define FLAG_DAILY_ROUTE_114_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xB)
#define FLAG_DAILY_ROUTE_111_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xC)
#define FLAG_DAILY_BERRY_MASTER_RECEIVED_BERRY      (DAILY_FLAGS_START + 0xD)
#define FLAG_DAILY_ROUTE_120_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xE)
#define FLAG_DAILY_LILYCOVE_RECEIVED_BERRY          (DAILY_FLAGS_START + 0xF)
#define FLAG_DAILY_FLOWER_SHOP_RECEIVED_BERRY       (DAILY_FLAGS_START + 0x10)
#define FLAG_DAILY_BERRY_MASTERS_WIFE               (DAILY_FLAGS_START + 0x11)
#define FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY        (DAILY_FLAGS_START + 0x12)
#define FLAG_UNUSED_0x933                           (DAILY_FLAGS_START + 0x13) // Unused Flag
#define FLAG_DAILY_APPRENTICE_LEAVES                (DAILY_FLAGS_START + 0x14)

#define FLAG_DAILY_REMATCH_ROXANNE                  (DAILY_FLAGS_START + 0x15) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_BRAWLY                   (DAILY_FLAGS_START + 0x16) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_WATTSON                  (DAILY_FLAGS_START + 0x17) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_FLANNERY                 (DAILY_FLAGS_START + 0x18) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_NORMAN                   (DAILY_FLAGS_START + 0x19) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_WINONA                   (DAILY_FLAGS_START + 0x1A) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_TATE_AND_LIZA            (DAILY_FLAGS_START + 0x1B) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_REMATCH_WALLACE                  (DAILY_FLAGS_START + 0x1C) // Project Grounded: gymleider-rematch vandaag al gewonnen
#define FLAG_DAILY_EVER_GRANDE_HOTDOG               (DAILY_FLAGS_START + 0x1D) // Project Grounded (landvulling): hotdogkraam (1 per dag)
#define FLAG_DAILY_HIDDEN_STARFALL_STARDUST_1       (DAILY_FLAGS_START + 0x1E) // Project Grounded (landvulling): verborgen sterrenstof, elke dag opnieuw
#define FLAG_DAILY_HIDDEN_STARFALL_STARDUST_2       (DAILY_FLAGS_START + 0x1F) // Project Grounded (landvulling): verborgen sterrenstof, elke dag opnieuw
#define FLAG_HIDDEN_ITEM_ZV3_R107_SOFT_SAND                                   (DAILY_FLAGS_START + 0x20) // Project Grounded (zeevulling 3): komt elke dag terug
#define FLAG_HIDDEN_ITEM_ZV3_R125_SNOWBALL                                    (DAILY_FLAGS_START + 0x21) // Project Grounded (zeevulling 3): komt elke dag terug
#define FLAG_HIDDEN_ITEM_ZV3_R125_ULTRA_BALL                                  (DAILY_FLAGS_START + 0x22) // Project Grounded (zeevulling 3): komt elke dag terug
#define FLAG_UNUSED_0x943                           (DAILY_FLAGS_START + 0x23) // Unused Flag
#define FLAG_UNUSED_0x944                           (DAILY_FLAGS_START + 0x24) // Unused Flag
#define FLAG_UNUSED_0x945                           (DAILY_FLAGS_START + 0x25) // Unused Flag
#define FLAG_UNUSED_0x946                           (DAILY_FLAGS_START + 0x26) // Unused Flag
#define FLAG_UNUSED_0x947                           (DAILY_FLAGS_START + 0x27) // Unused Flag
#define FLAG_UNUSED_0x948                           (DAILY_FLAGS_START + 0x28) // Unused Flag
#define FLAG_UNUSED_0x949                           (DAILY_FLAGS_START + 0x29) // Unused Flag
#define FLAG_UNUSED_0x94A                           (DAILY_FLAGS_START + 0x2A) // Unused Flag
#define FLAG_UNUSED_0x94B                           (DAILY_FLAGS_START + 0x2B) // Unused Flag
#define FLAG_UNUSED_0x94C                           (DAILY_FLAGS_START + 0x2C) // Unused Flag
#define FLAG_UNUSED_0x94D                           (DAILY_FLAGS_START + 0x2D) // Unused Flag
#define FLAG_UNUSED_0x94E                           (DAILY_FLAGS_START + 0x2E) // Unused Flag
#define FLAG_DAILY_BEACHCOMBER_FIND                 (DAILY_FLAGS_START + 0x2F) // Project Grounded: strandjutter Route 132 gaf vandaag al iets
#define FLAG_UNUSED_0x950                           (DAILY_FLAGS_START + 0x30) // Unused Flag
#define FLAG_UNUSED_0x951                           (DAILY_FLAGS_START + 0x31) // Unused Flag
#define FLAG_UNUSED_0x952                           (DAILY_FLAGS_START + 0x32) // Unused Flag
#define FLAG_UNUSED_0x953                           (DAILY_FLAGS_START + 0x33) // Unused Flag
#define FLAG_UNUSED_0x954                           (DAILY_FLAGS_START + 0x34) // Unused Flag
#define FLAG_UNUSED_0x955                           (DAILY_FLAGS_START + 0x35) // Unused Flag
#define FLAG_UNUSED_0x956                           (DAILY_FLAGS_START + 0x36) // Unused Flag
#define FLAG_UNUSED_0x957                           (DAILY_FLAGS_START + 0x37) // Unused Flag
#define FLAG_UNUSED_0x958                           (DAILY_FLAGS_START + 0x38) // Unused Flag
#define FLAG_UNUSED_0x959                           (DAILY_FLAGS_START + 0x39) // Unused Flag
#define FLAG_UNUSED_0x95A                           (DAILY_FLAGS_START + 0x3A) // Unused Flag
#define FLAG_UNUSED_0x95B                           (DAILY_FLAGS_START + 0x3B) // Unused Flag
#define FLAG_UNUSED_0x95C                           (DAILY_FLAGS_START + 0x3C) // Unused Flag
#define FLAG_UNUSED_0x95D                           (DAILY_FLAGS_START + 0x3D) // Unused Flag
#define FLAG_UNUSED_0x95E                           (DAILY_FLAGS_START + 0x3E) // Unused Flag
#define FLAG_DAILY_WINGULL_THEFT                    (DAILY_FLAGS_START + 0x3F) // Project Grounded: Wingull op de drijvende markt jat 1 Poké Ball per dag
#define DAILY_FLAGS_END                             (FLAG_DAILY_WINGULL_THEFT + (7 - FLAG_DAILY_WINGULL_THEFT % 8))
#define NUM_DAILY_FLAGS                             (DAILY_FLAGS_END - DAILY_FLAGS_START + 1)

#define FLAGS_COUNT (DAILY_FLAGS_END + 1)

// Project Grounded: extra flags (de gewone flags waren op, 8 okt). Ze staan achteraan SaveBlock1
// (gSaveBlock1Ptr->groundedFlags), zodat oude saves blijven werken. Gebruik: FLAG_GROUNDED(n), n = 0..2047.
#define GROUNDED_FLAGS_START                    0x1000
#define NUM_GROUNDED_FLAGS                      2048 // v0.9.190: 1024 -> 2048 (ruimte voor Yoshi's Island e.a.); was eerst 512
#define FLAG_GROUNDED(n)                        (GROUNDED_FLAGS_START + (n))
// Verdeling (houd bij!): 0-49 Hoopa-quest, 50-99 Forces-trio, 100-149 vuurtoren/Dragon Island, 150-199 Battle Stadium
// (omroeper), 200-329 kaartvulling 4 (kaart_vulling_4.py), 330-359 zeevulling 4, 360-399 gifts (Type: Null, Magearna,
// regionale vormen), 400-429 Beacon Isle (beacon_isle.py), 430-469 Tao-eiland (tao_island.py), 470-499 extra dungeons (dungeon_extra.py), 500-529 kratereilanden (sootopolis_craters.py), 530-559 Beasts of Ruin (ruin_beasts.py), 560-619 Spacetime Cave deel 1 (spacetime_cave.py), 620-659 Mega Forest (mega_forest.py), 660-699 Koraalkathedraal + Sea Shards (coral_cathedral.py), 700-759 National Park/Ilex (national_park.py), 760-799 Chargestone Cave (chargestone.py), 800-839 Swords of Justice/Keldeo/Meltan, 840-879 nieuwe items (nieuwe_items.py), 880+ vrij.
// lakes { (tools/grounded/maptools/lakes.py; FLAG_GROUNDED 1120-1159: 1120-1125 meren, 1140-1148 nieuwe items (nieuwe_items.py), 1126-1139 en 1149-1159 nog vrij)
#define FLAG_HIDE_LAKE_ACUITY_UXIE                       FLAG_GROUNDED(1120) // Project Grounded: Lake Acuity: Uxie gevangen of verslagen (verbergt het object)
#define FLAG_HIDE_LAKE_VALOR_AZELF                       FLAG_GROUNDED(1121) // Project Grounded: Lake Valor: Azelf gevangen of verslagen (verbergt het object)
#define FLAG_HIDE_LAKE_VERITY_MESPRIT                    FLAG_GROUNDED(1122) // Project Grounded: Lake Verity: Mesprit gevangen of verslagen (verbergt het object)
#define FLAG_LAKE_ACUITY_DONE                            FLAG_GROUNDED(1123) // Project Grounded: Lake Acuity: meerwezen afgehandeld (voor de meren-quest in de hub)
#define FLAG_LAKE_VALOR_DONE                             FLAG_GROUNDED(1124) // Project Grounded: Lake Valor: meerwezen afgehandeld (voor de meren-quest in de hub)
#define FLAG_LAKE_VERITY_DONE                            FLAG_GROUNDED(1125) // Project Grounded: Lake Verity: meerwezen afgehandeld (voor de meren-quest in de hub)
// }
// coronet { (tools/grounded/maptools/coronet.py; FLAG_GROUNDED 1160-1219: 1180-1186 nieuwe items (blok nieuwe_items), 1173-1179 en 1187-1219 nog vrij)
#define FLAG_SPACETIME_CORONET_DONE                      FLAG_GROUNDED(1160) // Project Grounded: Mt. Coronet: Dialga en Palkia allebei gevangen of verslagen (klaar-flag; Arceus-scene in de hub)
#define FLAG_CORONET_DIALGA_DONE                         FLAG_GROUNDED(1161) // Project Grounded: Spear Pillar: DIALGA gevangen of verslagen
#define FLAG_CORONET_PALKIA_DONE                         FLAG_GROUNDED(1162) // Project Grounded: Spear Pillar: PALKIA gevangen of verslagen
#define FLAG_HIDE_CORONET_DIALGA                         FLAG_GROUNDED(1163) // Project Grounded: Spear Pillar: DIALGA verborgen (verschijnt alleen via het altaar)
#define FLAG_HIDE_CORONET_PALKIA                         FLAG_GROUNDED(1164) // Project Grounded: Spear Pillar: PALKIA verborgen (verschijnt alleen via het altaar)
#define FLAG_ITEM_CORONET_4F_ROOM1_MAX_REVIVE            FLAG_GROUNDED(1165) // Project Grounded: Mt. Coronet 4F kamer 1: Max Revive
#define FLAG_HIDDEN_ITEM_CORONET_4F_ROOM1_ULTRA_BALL     FLAG_GROUNDED(1166) // Project Grounded: Mt. Coronet 4F kamer 1: verborgen Ultra Balls
#define FLAG_ITEM_CORONET_4F_OUTSIDE_MAX_ELIXIR          FLAG_GROUNDED(1167) // Project Grounded: Mt. Coronet 4F buiten: Max Elixir (op het massief)
#define FLAG_ITEM_CORONET_4F_OUTSIDE_PP_MAX              FLAG_GROUNDED(1168) // Project Grounded: Mt. Coronet 4F buiten: PP Max
#define FLAG_ITEM_CORONET_4F_ROOM3_RARE_CANDY            FLAG_GROUNDED(1169) // Project Grounded: Mt. Coronet 4F kamer 3: Rare Candy
#define FLAG_ITEM_CORONET_5F_MAX_POTION                  FLAG_GROUNDED(1170) // Project Grounded: Mt. Coronet 5F: Max Potion
#define FLAG_HIDDEN_ITEM_CORONET_5F_STAR_PIECE           FLAG_GROUNDED(1171) // Project Grounded: Mt. Coronet 5F: verborgen Star Piece
#define FLAG_ITEM_CORONET_6F_PP_UP                       FLAG_GROUNDED(1172) // Project Grounded: Mt. Coronet 6F: PP Up
// }
// yoshis_island { (tools/grounded/maptools/yoshis_island.py; FLAG_GROUNDED 1024-1119, 1050-1119 nog vrij)
#define FLAG_YI_ARRIVED                                      FLAG_GROUNDED(1024) // Project Grounded: Yoshi's Island: aankomstscene gezien (uit de lucht gevallen, Yoshi gevonden)
#define FLAG_YI_BEACH_GUARDS                                 FLAG_GROUNDED(1025) // Project Grounded: Yoshi's Island: de twee Shy Guys bij de pijp verslagen (multi battle 1)
#define FLAG_YI_CAMP_A                                       FLAG_GROUNDED(1026) // Project Grounded: Yoshi's Island: bende A in het Shy Guy-kamp verslagen (multi battle 2)
#define FLAG_YI_CAMP_B                                       FLAG_GROUNDED(1027) // Project Grounded: Yoshi's Island: bende B voor het spookhuis verslagen (multi battle 3)
#define FLAG_YI_BOO_DONE                                     FLAG_GROUNDED(1028) // Project Grounded: Yoshi's Island: Commander Boo verslagen (de fortwachter vlucht)
#define FLAG_YI_FORT_GUARDS                                  FLAG_GROUNDED(1029) // Project Grounded: Yoshi's Island: de twee fortwachters verslagen (multi battle 4)
#define FLAG_YI_WARIO_DONE                                   FLAG_GROUNDED(1030) // Project Grounded: Yoshi's Island: Wario verslagen (zet ook FLAG_SPACETIME_YOSHI_DONE)
#define FLAG_YI_PECHARUNT_DONE                               FLAG_GROUNDED(1031) // Project Grounded: Yoshi's Island: Pecharunt gevangen (of verslagen; komt dan terug)
#define FLAG_YI_YOSHI_AHEAD                                  FLAG_GROUNDED(1032) // Project Grounded: Yoshi's Island: Yoshi is vooruit de pijp in (verbergt Yoshi op het strand)
#define FLAG_YI_YOSHI_HOME                                   FLAG_GROUNDED(1033) // Project Grounded: Yoshi's Island: quest klaar, Yoshi wacht op het strand (verbergt hem elders)
#define FLAG_ITEM_YOSHIS_ISLAND_BEACH_HONEY                  FLAG_GROUNDED(1040) // Project Grounded: Yoshi's Island strand: Honey
#define FLAG_ITEM_YOSHIS_ISLAND_BEACH_HEAL_BALL              FLAG_GROUNDED(1041) // Project Grounded: Yoshi's Island strand: Heal Ball
#define FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_BEACH_EXP_CANDY_XS    FLAG_GROUNDED(1042) // Project Grounded: Yoshi's Island strand: verborgen Exp. Candy XS
#define FLAG_ITEM_YOSHIS_ISLAND_HILLS_LAGGING_TAIL           FLAG_GROUNDED(1043) // Project Grounded: Yoshi's Island heuvels: Lagging Tail
#define FLAG_ITEM_YOSHIS_ISLAND_HILLS_TOXIC_PLATE            FLAG_GROUNDED(1044) // Project Grounded: Yoshi's Island heuvels: Toxic Plate (bij Pecharunts kraampje)
#define FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_HILLS_STICKY_BARB     FLAG_GROUNDED(1045) // Project Grounded: Yoshi's Island heuvels: verborgen Sticky Barb
#define FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_FLOAT_STONE      FLAG_GROUNDED(1046) // Project Grounded: Yoshi's Island spookhuis: Float Stone
#define FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_POKE_DOLL        FLAG_GROUNDED(1047) // Project Grounded: Yoshi's Island spookhuis: Poke Doll
#define FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_GRIP_CLAW         FLAG_GROUNDED(1048) // Project Grounded: Yoshi's Island fort: Grip Claw
#define FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_MALICIOUS_ARMOR   FLAG_GROUNDED(1049) // Project Grounded: Yoshi's Island fort: Malicious Armor
// }
// national_park { (tools/grounded/maptools/national_park.py; FLAG_GROUNDED 700-759, 712-759 nog vrij)
#define FLAG_NATIONAL_PARK_REVEALED                      FLAG_GROUNDED(700) // Project Grounded: National Park: Calyrex heeft de illusie opgeheven (brandend park)
#define FLAG_NATIONAL_PARK_CELEBI_DONE                   FLAG_GROUNDED(701) // Project Grounded: Ilex Forest: Celebi gevangen
#define FLAG_NATIONAL_PARK_RESTORED                      FLAG_GROUNDED(702) // Project Grounded: National Park: Celebi heeft het park hersteld (Eternatus verschijnt)
#define FLAG_NATIONAL_PARK_DONE                          FLAG_GROUNDED(703) // Project Grounded: Spacetime-sidequest klaar: Eternatus gevangen/verslagen, Calyrex vertrokken
#define FLAG_NATIONAL_PARK_SCENE_PENDING                 FLAG_GROUNDED(704) // Project Grounded: National Park: tekst na de schermwissel nog tonen (eenmalig)
#define FLAG_ITEM_NATIONAL_PARK_SILVER_POWDER            FLAG_GROUNDED(705) // Project Grounded: National Park: Silver Powder
#define FLAG_ITEM_NATIONAL_PARK_SUN_STONE                FLAG_GROUNDED(706) // Project Grounded: National Park: Sun Stone
#define FLAG_HIDDEN_ITEM_NATIONAL_PARK_BIG_NUGGET        FLAG_GROUNDED(707) // Project Grounded: National Park: verborgen Big Nugget
#define FLAG_ITEM_ILEX_FOREST_REVIVAL_HERB               FLAG_GROUNDED(708) // Project Grounded: Ilex Forest: Revival Herb
#define FLAG_ITEM_ILEX_FOREST_BOTTLE_CAP                 FLAG_GROUNDED(709) // Project Grounded: Ilex Forest: Bottle Cap
#define FLAG_HIDDEN_ITEM_ILEX_FOREST_RARE_CANDY          FLAG_GROUNDED(710) // Project Grounded: Ilex Forest: verborgen Rare Candy
#define FLAG_ITEM_ILEX_FOREST_MIRACLE_SEED               FLAG_GROUNDED(711) // Project Grounded: Ilex Forest: Miracle Seed (dwaalpad)
// }
// area_zero { (tools/grounded/maptools/area_zero.py; FLAG_GROUNDED 920-999: 938-949 en 962-999 nog vrij, 950-961 nieuwe items (nieuwe_items.py))
#define FLAG_SPACETIME_AREAZERO_DONE                     FLAG_GROUNDED(920) // Project Grounded: Spacetime-sidequest klaar: TERAPAGOS gevangen
#define FLAG_AREAZERO_SCREAM_TAIL                        FLAG_GROUNDED(921) // Project Grounded: Area Zero, diepte: SCREAM TAIL gevangen
#define FLAG_AREAZERO_IRON_HANDS                         FLAG_GROUNDED(922) // Project Grounded: Area Zero, diepte: IRON HANDS gevangen
#define FLAG_AREAZERO_IRON_LEAVES                        FLAG_GROUNDED(923) // Project Grounded: Area Zero, toekomst: IRON LEAVES gevangen
#define FLAG_AREAZERO_IRON_BOULDER                       FLAG_GROUNDED(924) // Project Grounded: Area Zero, toekomst: IRON BOULDER gevangen
#define FLAG_AREAZERO_IRON_CROWN                         FLAG_GROUNDED(925) // Project Grounded: Area Zero, toekomst: IRON CROWN gevangen
#define FLAG_AREAZERO_MIRAIDON                           FLAG_GROUNDED(926) // Project Grounded: Area Zero, toekomst: MIRAIDON gevangen (beveiligingssysteem gaat aan)
#define FLAG_AREAZERO_WALKING_WAKE                       FLAG_GROUNDED(927) // Project Grounded: Area Zero, verleden: WALKING WAKE gevangen
#define FLAG_AREAZERO_GOUGING_FIRE                       FLAG_GROUNDED(928) // Project Grounded: Area Zero, verleden: GOUGING FIRE gevangen
#define FLAG_AREAZERO_RAGING_BOLT                        FLAG_GROUNDED(929) // Project Grounded: Area Zero, verleden: RAGING BOLT gevangen
#define FLAG_AREAZERO_KORAIDON                           FLAG_GROUNDED(930) // Project Grounded: Area Zero, verleden: KORAIDON gevangen (beveiligingssysteem gaat aan)
#define FLAG_AREAZERO_INTRO                              FLAG_GROUNDED(931) // Project Grounded: Area Zero: introtekst bij de eerste afdaling gezien
#define FLAG_ITEM_AREA_ZERO_RIM_FULL_RESTORE             FLAG_GROUNDED(932) // Project Grounded: Area Zero, kraterwand: Full Restore
#define FLAG_HIDDEN_ITEM_AREA_ZERO_RIM_MAX_ELIXIR        FLAG_GROUNDED(933) // Project Grounded: Area Zero, kraterwand: verborgen Max Elixir
#define FLAG_ITEM_AREA_ZERO_DEPTHS_PP_UP                 FLAG_GROUNDED(934) // Project Grounded: Area Zero, diepte: PP Up
#define FLAG_ITEM_AREA_ZERO_CRYSTAL_MAX_REVIVE           FLAG_GROUNDED(935) // Project Grounded: Area Zero, kristalgrot: Max Revive
#define FLAG_ITEM_AREA_ZERO_FUTURE_PP_MAX                FLAG_GROUNDED(936) // Project Grounded: Area Zero, toekomst: PP Max
#define FLAG_ITEM_AREA_ZERO_PAST_RARE_CANDY              FLAG_GROUNDED(937) // Project Grounded: Area Zero, verleden: Rare Candy
// }
// glimwood { (tools/grounded/maptools/glimwood.py; FLAG_GROUNDED 880-919, 895-919 nog vrij)
#define FLAG_GLIMWOOD_MET_WITCH                          FLAG_GROUNDED(880) // Project Grounded: Glimwood: de heks heeft zich voorgesteld
#define FLAG_GLIMWOOD_GANG_1                             FLAG_GROUNDED(881) // Project Grounded: Glimwood: Impidimp-bende 1 (west) verslagen
#define FLAG_GLIMWOOD_GANG_2                             FLAG_GROUNDED(882) // Project Grounded: Glimwood: Impidimp-bende 2 (oost) verslagen
#define FLAG_GLIMWOOD_GANG_3                             FLAG_GROUNDED(883) // Project Grounded: Glimwood: Impidimp-bende 3 (blokkeert de weg naar Ballonlea) verslagen
#define FLAG_GLIMWOOD_GANG_BOSS                          FLAG_GROUNDED(884) // Project Grounded: Ballonlea: Grimmsnarl (baas van de bende, blokkeert de trap) verslagen
#define FLAG_GLIMWOOD_XERNEAS_DONE                       FLAG_GROUNDED(885) // Project Grounded: Ballonlea: Xerneas gevangen, het bos licht weer op
#define FLAG_SPACETIME_GLIMWOOD_DONE                     FLAG_GROUNDED(886) // Project Grounded: Spacetime-sidequest klaar: Yveltal gevangen
#define FLAG_GLIMWOOD_SCENE_PENDING                      FLAG_GROUNDED(887) // Project Grounded: Ballonlea: tekst na het oplichten nog tonen (eenmalig)
#define FLAG_GLIMWOOD_YVELTAL_SEEN                       FLAG_GROUNDED(888) // Project Grounded: Glimwood: Yveltal-scene gezien (eenmalig)
#define FLAG_ITEM_GLIMWOOD_EXP_CANDY_XL                  FLAG_GROUNDED(889) // Project Grounded: Glimwood: Exp. Candy XL (westterras)
#define FLAG_ITEM_GLIMWOOD_EJECT_PACK                    FLAG_GROUNDED(890) // Project Grounded: Glimwood: Eject Pack (doodlopend pad oost)
#define FLAG_ITEM_GLIMWOOD_DREAM_BALL                    FLAG_GROUNDED(891) // Project Grounded: Glimwood: Dream Ball (oostterras)
#define FLAG_HIDDEN_ITEM_GLIMWOOD_GALARICA_CUFF          FLAG_GROUNDED(892) // Project Grounded: Glimwood: verborgen Galarica Cuff (heksenkring)
#define FLAG_ITEM_BALLONLEA_GALARICA_WREATH              FLAG_GROUNDED(893) // Project Grounded: Ballonlea: Galarica Wreath
#define FLAG_HIDDEN_ITEM_BALLONLEA_EXP_CANDY_L           FLAG_GROUNDED(894) // Project Grounded: Ballonlea: verborgen Exp. Candy L
// }
// coral_cathedral { (tools/grounded/maptools/coral_cathedral.py; FLAG_GROUNDED 660-699, 685-699 nog vrij)
#define FLAG_ITEM_SEA_SHARD_ROUTE126_CORAL_CATHEDRAL     FLAG_GROUNDED(660) // Project Grounded: Koraalkathedraal: Sea Shard
#define FLAG_ITEM_CORAL_CATHEDRAL_LUMINOUS_MOSS          FLAG_GROUNDED(661) // Project Grounded: Koraalkathedraal: Luminous Moss
#define FLAG_ITEM_CORAL_CATHEDRAL_SHELL_BELL             FLAG_GROUNDED(662) // Project Grounded: Koraalkathedraal: Shell Bell
#define FLAG_ITEM_CORAL_CATHEDRAL_PEARL_STRING           FLAG_GROUNDED(663) // Project Grounded: Koraalkathedraal: Pearl String
#define FLAG_HIDDEN_ITEM_CORAL_CATHEDRAL_BIG_PEARL       FLAG_GROUNDED(664) // Project Grounded: Koraalkathedraal: verborgen Big Pearl
#define FLAG_ITEM_SEA_SHARD_ROUTE128_BUBBLE_GROTTO       FLAG_GROUNDED(665) // Project Grounded: Sea Shard in Route128_BubbleGrotto
#define FLAG_ITEM_SEA_SHARD_UNDERWATER_ROUTE127_TRENCH   FLAG_GROUNDED(666) // Project Grounded: Sea Shard in Underwater_Route127_Trench
#define FLAG_ITEM_SEA_SHARD_SHIPWRECK_SHOALS             FLAG_GROUNDED(667) // Project Grounded: Sea Shard in ShipwreckShoals
#define FLAG_ITEM_SEA_SHARD_UNDERWATER_SEA_TEMPLE        FLAG_GROUNDED(668) // Project Grounded: Sea Shard in Underwater_SeaTemple
#define FLAG_ITEM_SEA_SHARD_ROUTE126_SILENT_CRATER       FLAG_GROUNDED(669) // Project Grounded: Sea Shard in Route126_SilentCrater
#define FLAG_ITEM_SEA_SHARD_ROUTE127_WELLSPRING_GROTTO   FLAG_GROUNDED(670) // Project Grounded: Sea Shard in Route127_WellspringGrotto
#define FLAG_ITEM_SEA_SHARD_UNDERWATER_ROUTE136          FLAG_GROUNDED(671) // Project Grounded: Sea Shard in Underwater_Route136
#define FLAG_SEA_SHARD_REWARD_2                          FLAG_GROUNDED(680) // Project Grounded: Sea Shards: beloning 2 (Dive Balls)
#define FLAG_SEA_SHARD_REWARD_4                          FLAG_GROUNDED(681) // Project Grounded: Sea Shards: beloning 4 (Heavy-Duty Boots)
#define FLAG_SEA_SHARD_REWARD_6                          FLAG_GROUNDED(682) // Project Grounded: Sea Shards: beloning 6 (Gold Bottle Cap)
#define FLAG_SEA_SHARD_REWARD_8                          FLAG_GROUNDED(683) // Project Grounded: Sea Shards: beloning 8 (Master Ball)
#define FLAG_SEA_SHARDS_EXPLAINED                        FLAG_GROUNDED(684) // Project Grounded: Sea Shards: Treasure Hunter heeft de quest uitgelegd
// }
// nieuwe_items { (tools/grounded/maptools/nieuwe_items.py; FLAG_GROUNDED 840-879, items die nergens anders liggen)
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_LURE_BALL   FLAG_GROUNDED(840) // Project Grounded: diepzeetrog: Lure Balls
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_HEAVY_BALL  FLAG_GROUNDED(841) // Project Grounded: diepzeetrog: Heavy Balls
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_BINDING_BAND FLAG_GROUNDED(842) // Project Grounded: diepzeetrog: Binding Band
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_EJECT_BUTTON FLAG_GROUNDED(843) // Project Grounded: diepzeetrog: Eject Button
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_POWER_ANKLET FLAG_GROUNDED(844) // Project Grounded: diepzeetrog: Power Anklet
#define FLAG_ITEM_UNDERWATER_ROUTE127_TRENCH_EXP_CANDY_L FLAG_GROUNDED(845) // Project Grounded: diepzeetrog: Exp. Candy L
#define FLAG_HIDDEN_ITEM_UNDERWATER_ROUTE127_TRENCH_RELIC_VASE FLAG_GROUNDED(846) // Project Grounded: diepzeetrog: verborgen Relic Vase
#define FLAG_ITEM_CHARGESTONE_CAVE_1F_FAST_BALL          FLAG_GROUNDED(850) // Project Grounded: Chargestone Cave 1F: Fast Balls
#define FLAG_ITEM_CHARGESTONE_CAVE_1F_POWER_LENS         FLAG_GROUNDED(851) // Project Grounded: Chargestone Cave 1F: Power Lens
#define FLAG_ITEM_CHARGESTONE_CAVE_B1F_EJECT_PACK        FLAG_GROUNDED(852) // Project Grounded: Chargestone Cave B1F: Eject Pack
#define FLAG_ITEM_CHARGESTONE_CAVE_B1F_TERRAIN_EXTENDER  FLAG_GROUNDED(853) // Project Grounded: Chargestone Cave B1F: Terrain Extender
#define FLAG_ITEM_CHARGESTONE_CAVE_B2F_ABILITY_SHIELD    FLAG_GROUNDED(854) // Project Grounded: Chargestone Cave B2F: Ability Shield
#define FLAG_HIDDEN_ITEM_CHARGESTONE_CAVE_B2F_EXP_CANDY_XL FLAG_GROUNDED(855) // Project Grounded: Chargestone Cave B2F: verborgen Exp. Candy XL
#define FLAG_HIDDEN_ITEM_LAVENDER_TOWN_EXP_CANDY_S       FLAG_GROUNDED(860) // Project Grounded: Lavender Town: verborgen Exp. Candy S
#define FLAG_ITEM_POKEMON_TOWER_3F_MOON_BALL             FLAG_GROUNDED(861) // Project Grounded: Pokemon Tower 3F: Moon Balls
#define FLAG_ITEM_POKEMON_TOWER_4F_RED_CARD              FLAG_GROUNDED(862) // Project Grounded: Pokemon Tower 4F: Red Card
#define FLAG_ITEM_POKEMON_TOWER_2F_POWER_BRACER          FLAG_GROUNDED(863) // Project Grounded: Pokemon Tower 2F: Power Bracer
#define FLAG_ITEM_CERULEAN_CAVE_1F_LEVEL_BALL            FLAG_GROUNDED(864) // Project Grounded: Cerulean Cave 1F: Level Balls
#define FLAG_ITEM_CERULEAN_CAVE_2F_POWER_WEIGHT          FLAG_GROUNDED(865) // Project Grounded: Cerulean Cave 2F: Power Weight
#define FLAG_ITEM_CERULEAN_CAVE_2F_ROOM_SERVICE          FLAG_GROUNDED(866) // Project Grounded: Cerulean Cave 2F: Room Service
#define FLAG_ITEM_CERULEAN_CAVE_B1F_MIRROR_HERB          FLAG_GROUNDED(867) // Project Grounded: Cerulean Cave B1F: Mirror Herb
#define FLAG_HIDDEN_ITEM_CERULEAN_CAVE_B1F_POWER_BAND    FLAG_GROUNDED(868) // Project Grounded: Cerulean Cave B1F: verborgen Power Band
#define FLAG_ITEM_NATIONAL_PARK_SPORT_BALL               FLAG_GROUNDED(870) // Project Grounded: National Park: Sport Balls
#define FLAG_ITEM_NATIONAL_PARK_INSECT_PLATE             FLAG_GROUNDED(871) // Project Grounded: National Park: Insect Plate
#define FLAG_HIDDEN_ITEM_NATIONAL_PARK_POWER_BELT        FLAG_GROUNDED(872) // Project Grounded: National Park: verborgen Power Belt
#define FLAG_ITEM_ILEX_FOREST_FRIEND_BALL                FLAG_GROUNDED(873) // Project Grounded: Ilex Forest: Friend Balls
#define FLAG_ITEM_ILEX_FOREST_LOVE_BALL                  FLAG_GROUNDED(874) // Project Grounded: Ilex Forest: Love Balls
#define FLAG_ITEM_ILEX_FOREST_DESTINY_KNOT               FLAG_GROUNDED(875) // Project Grounded: Ilex Forest: Destiny Knot
#define FLAG_HIDDEN_ITEM_ILEX_FOREST_ROSE_INCENSE        FLAG_GROUNDED(876) // Project Grounded: Ilex Forest: verborgen Rose Incense
#define FLAG_ITEM_AREA_ZERO_RIM_QUICK_BALL               FLAG_GROUNDED(950) // Project Grounded: Area Zero, kraterwand: Quick Balls
#define FLAG_ITEM_AREA_ZERO_RIM_MUSCLE_BAND              FLAG_GROUNDED(951) // Project Grounded: Area Zero, kraterwand: Muscle Band
#define FLAG_ITEM_AREA_ZERO_DEPTHS_ADRENALINE_ORB        FLAG_GROUNDED(952) // Project Grounded: Area Zero, diepte: Adrenaline Orb
#define FLAG_HIDDEN_ITEM_AREA_ZERO_DEPTHS_SHED_SHELL     FLAG_GROUNDED(953) // Project Grounded: Area Zero, diepte: verborgen Shed Shell
#define FLAG_ITEM_AREA_ZERO_CRYSTAL_BEAST_BALL           FLAG_GROUNDED(954) // Project Grounded: Area Zero, kristalgrot: Beast Balls
#define FLAG_HIDDEN_ITEM_AREA_ZERO_CRYSTAL_RING_TARGET   FLAG_GROUNDED(955) // Project Grounded: Area Zero, kristalgrot: verborgen Ring Target
#define FLAG_ITEM_AREA_ZERO_FUTURE_BOOSTER_ENERGY        FLAG_GROUNDED(956) // Project Grounded: Area Zero, toekomst: Booster Energy
#define FLAG_ITEM_AREA_ZERO_FUTURE_METAL_ALLOY           FLAG_GROUNDED(957) // Project Grounded: Area Zero, toekomst: Metal Alloy (Duraludon -> Archaludon)
#define FLAG_HIDDEN_ITEM_AREA_ZERO_FUTURE_AIR_BALLOON    FLAG_GROUNDED(958) // Project Grounded: Area Zero, toekomst: verborgen Air Balloon
#define FLAG_ITEM_AREA_ZERO_PAST_POWER_HERB              FLAG_GROUNDED(959) // Project Grounded: Area Zero, verleden: Power Herb
#define FLAG_ITEM_AREA_ZERO_PAST_GRIP_CLAW               FLAG_GROUNDED(960) // Project Grounded: Area Zero, verleden: Grip Claw
#define FLAG_HIDDEN_ITEM_AREA_ZERO_PAST_STICKY_BARB      FLAG_GROUNDED(961) // Project Grounded: Area Zero, verleden: verborgen Sticky Barb
#define FLAG_ITEM_LAKE_ACUITY_PEAT_BLOCK                 FLAG_GROUNDED(1140) // Project Grounded: Lake Acuity: Peat Block (Ursaring -> Ursaluna)
#define FLAG_HIDDEN_ITEM_LAKE_ACUITY_FULL_INCENSE        FLAG_GROUNDED(1141) // Project Grounded: Lake Acuity: verborgen Full Incense
#define FLAG_ITEM_LAKE_ACUITY_CAVERN_METAL_POWDER        FLAG_GROUNDED(1142) // Project Grounded: Lake Acuity, grot: Metal Powder
#define FLAG_ITEM_LAKE_VALOR_AUSPICIOUS_ARMOR            FLAG_GROUNDED(1143) // Project Grounded: Lake Valor: Auspicious Armor (Charcadet -> Armarouge)
#define FLAG_HIDDEN_ITEM_LAKE_VALOR_ROCK_INCENSE         FLAG_GROUNDED(1144) // Project Grounded: Lake Valor: verborgen Rock Incense
#define FLAG_ITEM_LAKE_VALOR_CAVERN_LEADERS_CREST        FLAG_GROUNDED(1145) // Project Grounded: Lake Valor, grot: Leader's Crest (Bisharp -> Kingambit)
#define FLAG_ITEM_LAKE_VERITY_ODD_INCENSE                FLAG_GROUNDED(1146) // Project Grounded: Lake Verity: Odd Incense
#define FLAG_HIDDEN_ITEM_LAKE_VERITY_LINKING_CORD        FLAG_GROUNDED(1147) // Project Grounded: Lake Verity: verborgen Linking Cord
#define FLAG_ITEM_LAKE_VERITY_CAVERN_QUICK_POWDER        FLAG_GROUNDED(1148) // Project Grounded: Lake Verity, grot: Quick Powder
#define FLAG_ITEM_MT_CORONET_4_F_ROOM2_ADAMANT_CRYSTAL   FLAG_GROUNDED(1180) // Project Grounded: Mt. Coronet 4F kamer 2: Adamant Crystal (Dialga Origin)
#define FLAG_ITEM_MT_CORONET_4_F_ROOM2_ODD_KEYSTONE      FLAG_GROUNDED(1181) // Project Grounded: Mt. Coronet 4F kamer 2: Odd Keystone
#define FLAG_HIDDEN_ITEM_MT_CORONET_4_F_OUTSIDE_LUSTROUS_GLOBE FLAG_GROUNDED(1182) // Project Grounded: Mt. Coronet 4F buiten: verborgen Lustrous Globe (Palkia Origin)
#define FLAG_ITEM_MT_CORONET_5F_IRON_BALL                FLAG_GROUNDED(1183) // Project Grounded: Mt. Coronet 5F: Iron Ball
#define FLAG_ITEM_SPEAR_PILLAR_ADAMANT_ORB               FLAG_GROUNDED(1184) // Project Grounded: Spear Pillar: Adamant Orb (bij het altaar van Dialga)
#define FLAG_ITEM_SPEAR_PILLAR_LUSTROUS_ORB              FLAG_GROUNDED(1185) // Project Grounded: Spear Pillar: Lustrous Orb (bij het altaar van Palkia)
// }
// chargestone { (tools/grounded/maptools/chargestone.py; FLAG_GROUNDED 760-799, 771-799 nog vrij)
#define FLAG_SPACETIME_CHARGESTONE_DONE                  FLAG_GROUNDED(760) // Project Grounded: Chargestone Cave: ZERAORA gevangen of verslagen (klaar-flag sidequest)
#define FLAG_HIDE_CHARGESTONE_ZERAORA                    FLAG_GROUNDED(761) // Project Grounded: Chargestone Cave B2F: ZERAORA verborgen (voor Colress verslagen is of na het gevecht)
#define FLAG_HIDE_CHARGESTONE_COLRESS                    FLAG_GROUNDED(762) // Project Grounded: Chargestone Cave B2F: Colress weg (na ZERAORA)
#define FLAG_ITEM_CHARGESTONE_1F_THUNDER_STONE           FLAG_GROUNDED(763) // Project Grounded: Chargestone Cave 1F: Thunder Stone
#define FLAG_ITEM_CHARGESTONE_1F_MAX_REVIVE              FLAG_GROUNDED(764) // Project Grounded: Chargestone Cave 1F: Max Revive (zijgrot achter de duwsteen)
#define FLAG_ITEM_CHARGESTONE_B1F_MAGNET                 FLAG_GROUNDED(765) // Project Grounded: Chargestone Cave B1F: Magnet
#define FLAG_ITEM_CHARGESTONE_B1F_METAL_COAT             FLAG_GROUNDED(766) // Project Grounded: Chargestone Cave B1F: Metal Coat
#define FLAG_ITEM_CHARGESTONE_B2F_ELECTIRIZER            FLAG_GROUNDED(767) // Project Grounded: Chargestone Cave B2F: Electirizer
#define FLAG_ITEM_CHARGESTONE_B2F_PP_MAX                 FLAG_GROUNDED(768) // Project Grounded: Chargestone Cave B2F: PP Max
#define FLAG_HIDDEN_ITEM_CHARGESTONE_1F_CELL_BATTERY     FLAG_GROUNDED(769) // Project Grounded: Chargestone Cave 1F: verborgen Cell Battery
#define FLAG_HIDDEN_ITEM_CHARGESTONE_B1F_BIG_NUGGET      FLAG_GROUNDED(770) // Project Grounded: Chargestone Cave B1F: verborgen Big Nugget
// }
// swords_keldeo { (tools/grounded/maptools/swords_keldeo.py; FLAG_GROUNDED 800-839, 810-839 nog vrij)
#define FLAG_DEFEATED_COBALION                           FLAG_GROUNDED(800) // Project Grounded: Cobalion gevangen/verslagen (Granite Cave)
#define FLAG_DEFEATED_TERRAKION                          FLAG_GROUNDED(801) // Project Grounded: Terrakion gevangen/verslagen (Victory Road)
#define FLAG_DEFEATED_VIRIZION                           FLAG_GROUNDED(802) // Project Grounded: Virizion gevangen/verslagen (Mangrove Mire)
#define FLAG_BRINEY_KELDEO_CALL                          FLAG_GROUNDED(803) // Project Grounded: Mr. Briney heeft gebeld over het eiland (na de drie zwaarden)
#define FLAG_DEFEATED_KELDEO                             FLAG_GROUNDED(804) // Project Grounded: Keldeo gevangen/verslagen (UnchartedIsle)
#define FLAG_GRANITE_SWORD_CHAMBER_ROCK                  FLAG_GROUNDED(805) // Project Grounded: Rock Smash-rots voor de zwaardkamer in Granite Cave B2F
#define FLAG_VICTORY_ROAD_SWORD_CHAMBER_ROCK             FLAG_GROUNDED(806) // Project Grounded: Rock Smash-rots voor de zwaardkamer in Victory Road B2F
#define FLAG_KELDEO_TRIP_FROM_DEWFORD                    FLAG_GROUNDED(807) // Project Grounded: Keldeo-bootreis vertrokken uit Dewford (terugweg)
#define FLAG_KELDEO_TRIP_FROM_ROUTE109                   FLAG_GROUNDED(808) // Project Grounded: Keldeo-bootreis vertrokken van Route 109 (terugweg)
#define FLAG_RECEIVED_MELTAN                             FLAG_GROUNDED(809) // Project Grounded: Meltan gekregen (Sterns scheepswerf, Slateport)
// }
// mega_forest { (tools/grounded/maptools/mega_forest.py; FLAG_GROUNDED 620-659, 631-659 nog vrij voor later)
#define FLAG_HIDE_MINI_FOREST_GIANT_LOG                  FLAG_GROUNDED(620) // Project Grounded: Mini Forest: omgevallen reuzenboom weg (na de Hall of Fame, ON_TRANSITION)
#define FLAG_RECEIVED_RUSTED_SWORD                       FLAG_GROUNDED(621) // Project Grounded: Mini Forest: roestig zwaard opgepakt (na de HoF; verbergt het zwaard)
#define FLAG_RECEIVED_RUSTED_SHIELD                      FLAG_GROUNDED(622) // Project Grounded: Mini Forest: roestig schild opgepakt (na de HoF; verbergt het schild)
#define FLAG_HIDE_MEGA_FOREST_ZACIAN                     FLAG_GROUNDED(623) // Project Grounded: Mega Forest: Zacian gevangen/verslagen
#define FLAG_HIDE_MEGA_FOREST_ZAMAZENTA                  FLAG_GROUNDED(624) // Project Grounded: Mega Forest: Zamazenta gevangen/verslagen
#define FLAG_ITEM_MEGA_FOREST_SWEET_APPLE                FLAG_GROUNDED(625) // Project Grounded: Mega Forest: Sweet Apple
#define FLAG_ITEM_MEGA_FOREST_TART_APPLE                 FLAG_GROUNDED(626) // Project Grounded: Mega Forest: Tart Apple
#define FLAG_ITEM_MEGA_FOREST_MAX_REVIVE                 FLAG_GROUNDED(627) // Project Grounded: Mega Forest: Max Revive
#define FLAG_ITEM_MEGA_FOREST_PP_MAX                     FLAG_GROUNDED(628) // Project Grounded: Mega Forest: PP Max
#define FLAG_HIDDEN_ITEM_MEGA_FOREST_STAR_PIECE          FLAG_GROUNDED(629) // Project Grounded: Mega Forest: verborgen Star Piece
#define FLAG_HIDDEN_ITEM_MEGA_FOREST_BIG_NUGGET          FLAG_GROUNDED(630) // Project Grounded: Mega Forest: verborgen Big Nugget
// }

// spacetime_cave { (tools/grounded/maptools/spacetime_cave.py; FLAG_GROUNDED 560-619)
#define FLAG_ITEM_POKEMON_TOWER_3F_MAX_REVIVE            FLAG_GROUNDED(560) // Project Grounded: Pokemon Tower 3F: Max Revive
#define FLAG_ITEM_POKEMON_TOWER_4F_MAX_ELIXIR            FLAG_GROUNDED(561) // Project Grounded: Pokemon Tower 4F: Max Elixir
#define FLAG_ITEM_POKEMON_TOWER_4F_DUSK_STONE            FLAG_GROUNDED(562) // Project Grounded: Pokemon Tower 4F: Dusk Stone
#define FLAG_ITEM_POKEMON_TOWER_4F_DUSK_BALL             FLAG_GROUNDED(563) // Project Grounded: Pokemon Tower 4F: Dusk Ball
#define FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB             FLAG_GROUNDED(564) // Project Grounded: Pokemon Tower 5F: Life Orb van de conciërge
#define FLAG_ITEM_CERULEAN_CAVE_1F_BIG_NUGGET            FLAG_GROUNDED(565) // Project Grounded: Cerulean Cave 1F: Big Nugget
#define FLAG_ITEM_CERULEAN_CAVE_1F_FULL_RESTORE          FLAG_GROUNDED(566) // Project Grounded: Cerulean Cave 1F: Full Restore
#define FLAG_ITEM_CERULEAN_CAVE_1F_MAX_ELIXIR            FLAG_GROUNDED(567) // Project Grounded: Cerulean Cave 1F: Max Elixir
#define FLAG_HIDDEN_ITEM_CERULEAN_CAVE_1F_PP_MAX         FLAG_GROUNDED(568) // Project Grounded: Cerulean Cave 1F: verborgen PP Max
#define FLAG_ITEM_CERULEAN_CAVE_2F_PP_UP                 FLAG_GROUNDED(569) // Project Grounded: Cerulean Cave 2F: PP Up
#define FLAG_ITEM_CERULEAN_CAVE_2F_RARE_CANDY            FLAG_GROUNDED(570) // Project Grounded: Cerulean Cave 2F: Rare Candy
#define FLAG_ITEM_CERULEAN_CAVE_2F_FULL_RESTORE          FLAG_GROUNDED(571) // Project Grounded: Cerulean Cave 2F: Full Restore
#define FLAG_ITEM_CERULEAN_CAVE_B1F_ULTRA_BALL           FLAG_GROUNDED(572) // Project Grounded: Cerulean Cave B1F: Ultra Ball
#define FLAG_ITEM_CERULEAN_CAVE_B1F_MAX_REVIVE           FLAG_GROUNDED(573) // Project Grounded: Cerulean Cave B1F: Max Revive
#define FLAG_SPACETIME_RIFTS_OPENED                      FLAG_GROUNDED(574) // Project Grounded: Spacetime Cave: Dialga en Palkia hebben de scheuren geopend
#define FLAG_SPACETIME_LAVENDER_DONE                     FLAG_GROUNDED(575) // Project Grounded: Spacetime-sidequest klaar: Lavender bevrijd (Agatha verslagen)
#define FLAG_SPACETIME_CERULEAN_DONE                     FLAG_GROUNDED(576) // Project Grounded: Spacetime-sidequest klaar: Mewtwo gevangen/verslagen
#define FLAG_HIDE_LAVENDER_GHOST_GENGAR                  FLAG_GROUNDED(577) // Project Grounded: Lavender Town: kwade geest voor de toren verdreven
#define FLAG_HIDE_LAVENDER_GHOST_DUSKNOIR                FLAG_GROUNDED(578) // Project Grounded: Lavender Town: kwade geest bij de noorduitgang verdreven
#define FLAG_HIDE_LAVENDER_GHOST_BANETTE                 FLAG_GROUNDED(579) // Project Grounded: Lavender Town: kwade geest bij de westuitgang verdreven
#define FLAG_SPACETIME_YOSHI_DONE                        FLAG_GROUNDED(580) // Project Grounded: Spacetime: Yoshi's Island gefixt (opent de gang naar de meren; nog nooit gezet)
#define FLAG_SPACETIME_LAKES_SCENE                       FLAG_GROUNDED(581) // Project Grounded: Spacetime: Dialga en Palkia hebben de meren-portalen geopend
#define FLAG_RECEIVED_SILPH_SCOPE                        FLAG_GROUNDED(582) // Project Grounded: Lavender Town: Silph Scope van de oud-verkoper in het PC
// }
// ruin_beasts { (tools/grounded/maptools/ruin_beasts.py; FLAG_GROUNDED 530-559)
#define FLAG_RUIN_SEAL_CHI_YU                            FLAG_GROUNDED(530) // Project Grounded: Chi-Yu-schrijn (Jagged Pass) bezocht
#define FLAG_RUIN_SEAL_TING_LU                           FLAG_GROUNDED(531) // Project Grounded: Ting-Lu-schrijn (Desert Underpass) bezocht
#define FLAG_RUIN_SEAL_WO_CHIEN                          FLAG_GROUNDED(532) // Project Grounded: Wo-Chien-schrijn (Petalburg Woods) bezocht
#define FLAG_RUIN_SEAL_CHIEN_PAO                         FLAG_GROUNDED(533) // Project Grounded: Chien-Pao-schrijn (Route 135) bezocht
#define FLAG_HIDE_RUIN_CHI_YU                            FLAG_GROUNDED(534) // Project Grounded: Chi-Yu gevangen/verslagen
#define FLAG_HIDE_RUIN_TING_LU                           FLAG_GROUNDED(535) // Project Grounded: Ting-Lu gevangen/verslagen
#define FLAG_HIDE_RUIN_WO_CHIEN                          FLAG_GROUNDED(536) // Project Grounded: Wo-Chien gevangen/verslagen
#define FLAG_HIDE_RUIN_CHIEN_PAO                         FLAG_GROUNDED(537) // Project Grounded: Chien-Pao gevangen/verslagen
#define FLAG_RUIN_SEAL_OPEN_CHI_YU                       FLAG_GROUNDED(538) // Project Grounded: zegel bij de ingang naar Chi-Yu gebroken (Sealbreaker)
#define FLAG_RUIN_SEAL_OPEN_TING_LU                      FLAG_GROUNDED(539) // Project Grounded: zegel bij de ingang naar Ting-Lu gebroken (Sealbreaker)
#define FLAG_RUIN_SEAL_OPEN_WO_CHIEN                     FLAG_GROUNDED(540) // Project Grounded: zegel bij de ingang naar Wo-Chien gebroken (Sealbreaker)
#define FLAG_RUIN_SEAL_OPEN_CHIEN_PAO                    FLAG_GROUNDED(541) // Project Grounded: zegel bij de ingang naar Chien-Pao gebroken (Sealbreaker)
// }
// sootopolis_craters { (tools/grounded/maptools/sootopolis_craters.py; FLAG_GROUNDED 500-529)
#define FLAG_ITEM_HERMIT_CRATER_WIDE_LENS                FLAG_GROUNDED(500) // Project Grounded: kluizenaarskrater: Wide Lens
#define FLAG_HIDDEN_ITEM_HERMIT_CRATER_PEARL_STRING      FLAG_GROUNDED(501) // Project Grounded: kluizenaarskrater: verborgen Pearl String
#define FLAG_ITEM_SILENT_CRATER_GOLD_BOTTLE_CAP          FLAG_GROUNDED(502) // Project Grounded: stille krater: Gold Bottle Cap (grasrichel)
#define FLAG_HIDDEN_ITEM_SILENT_CRATER_EARTH_PLATE       FLAG_GROUNDED(503) // Project Grounded: stille krater: verborgen Earth Plate (voorplein)
#define FLAG_HIDDEN_ITEM_SILENT_CRATER_SPLASH_PLATE      FLAG_GROUNDED(504) // Project Grounded: stille krater: verborgen Splash Plate (grasrand)
// }
// dungeon_extra { (tools/grounded/maptools/dungeon_extra.py; FLAG_GROUNDED 470-499)
#define FLAG_ITEM_GRANITE_CRYSTAL_STAR_PIECE             FLAG_GROUNDED(470) // Project Grounded: Granite Cave kristalgrot: Star Piece
#define FLAG_ITEM_GRANITE_CRYSTAL_HARD_STONE             FLAG_GROUNDED(471) // Project Grounded: Granite Cave kristalgrot: Hard Stone
#define FLAG_HIDDEN_ITEM_GRANITE_CRYSTAL_SHINY_STONE     FLAG_GROUNDED(472) // Project Grounded: Granite Cave kristalgrot: verborgen Shiny Stone
#define FLAG_ITEM_ORIGIN_DEEP1_DAMP_ROCK                 FLAG_GROUNDED(473) // Project Grounded: Cave of Origin diep 1: Damp Rock
#define FLAG_ITEM_ORIGIN_DEEP2_HEAT_ROCK                 FLAG_GROUNDED(474) // Project Grounded: Cave of Origin diep 2: Heat Rock
#define FLAG_ITEM_ORIGIN_DEEP3_PP_MAX                    FLAG_GROUNDED(475) // Project Grounded: Cave of Origin diep 3: PP Max
#define FLAG_HIDDEN_ITEM_ORIGIN_DEEP3_BIG_NUGGET         FLAG_GROUNDED(476) // Project Grounded: Cave of Origin diep 3: verborgen Big Nugget
#define FLAG_ITEM_SHOAL_FROZEN_ICE_STONE                 FLAG_GROUNDED(477) // Project Grounded: Shoal Cave ijzige onderlaag: Ice Stone
#define FLAG_ITEM_SHOAL_FROZEN_ICY_ROCK                  FLAG_GROUNDED(478) // Project Grounded: Shoal Cave ijzige onderlaag: Icy Rock
#define FLAG_ITEM_SHOAL_FROZEN_ABILITY_CAPSULE           FLAG_GROUNDED(479) // Project Grounded: Shoal Cave ijzige onderlaag: Ability Capsule
#define FLAG_HIDDEN_ITEM_SHOAL_FROZEN_PEARL_STRING       FLAG_GROUNDED(480) // Project Grounded: Shoal Cave ijzige onderlaag: verborgen Pearl String
#define FLAG_ITEM_BUBBLE_GROTTO_DEEP_SEA_TOOTH           FLAG_GROUNDED(481) // Project Grounded: luchtbel-grot Route 128: Deep Sea Tooth
#define FLAG_ITEM_BUBBLE_GROTTO_RARE_BONE                FLAG_GROUNDED(482) // Project Grounded: luchtbel-grot Route 128: Rare Bone
#define FLAG_HIDDEN_ITEM_BUBBLE_GROTTO_STAR_PIECE        FLAG_GROUNDED(483) // Project Grounded: luchtbel-grot Route 128: verborgen Star Piece
// }
// beacon_isle { (tools/grounded/maptools/beacon_isle.py; FLAG_GROUNDED 400-429)
#define FLAG_BEACON_LIGHT_ISLE_FOUND                     FLAG_GROUNDED(400) // Project Grounded: Beacon Isle: 's nachts de lamp aangesproken, rif naar het Lichteiland open
// }
// tao_island { (tools/grounded/maptools/tao_island.py; FLAG_GROUNDED 430-469)
#define FLAG_HIDDEN_ITEM_TAO_ISLAND_DRAGON_SCALE         FLAG_GROUNDED(430) // Project Grounded: Tao-eiland: verborgen Dragon Scale
#define FLAG_HIDDEN_ITEM_TAO_ISLAND_STAR_PIECE           FLAG_GROUNDED(431) // Project Grounded: Tao-eiland: verborgen Star Piece
#define FLAG_ITEM_TAO_ISLAND_MAX_REVIVE                  FLAG_GROUNDED(432) // Project Grounded: Tao-eiland: Max Revive
#define FLAG_ITEM_TAO_DEN_PP_UP                          FLAG_GROUNDED(433) // Project Grounded: Dragon's Den: PP Up
#define FLAG_ITEM_TAO_DEN_MAX_ELIXIR                     FLAG_GROUNDED(434) // Project Grounded: Dragon's Den: Max Elixir
#define FLAG_HIDDEN_ITEM_TAO_DEN_BIG_NUGGET              FLAG_GROUNDED(435) // Project Grounded: Dragon's Den: verborgen Big Nugget
#define FLAG_HIDE_TAO_RESHIRAM                           FLAG_GROUNDED(436) // Project Grounded: Tao-toren: Reshiram gevangen/verslagen
#define FLAG_HIDE_TAO_ZEKROM                             FLAG_GROUNDED(437) // Project Grounded: Tao-toren: Zekrom gevangen/verslagen
#define FLAG_HIDE_TAO_DEN_DRAGONITE                      FLAG_GROUNDED(438) // Project Grounded: Dragon's Den: Dragonite van het gat (na beide broers)
#define FLAG_HIDE_TAO_KYUREM                             FLAG_GROUNDED(439) // Project Grounded: Frost Hollow: Kyurem gevangen/verslagen
#define FLAG_HIDE_TAO_GHETSIS                            FLAG_GROUNDED(440) // Project Grounded: Frost Hollow: Ghetsis vertrokken (DNA Splicers gekregen)
#define FLAG_ITEM_TAO_TOWER_2F_DRAGON_FANG               FLAG_GROUNDED(441) // Project Grounded: Tao-toren 2F: Dragon Fang
#define FLAG_ITEM_TAO_TOWER_3F_FULL_RESTORE              FLAG_GROUNDED(442) // Project Grounded: Tao-toren 3F: Full Restore
#define FLAG_ITEM_TAO_FROST_NEVER_MELT_ICE               FLAG_GROUNDED(443) // Project Grounded: Frost Hollow: Never-Melt Ice
#define FLAG_ITEM_TAO_FROST_ICE_STONE                    FLAG_GROUNDED(444) // Project Grounded: Frost Hollow: Ice Stone
// }
// Battle Stadium-omroeper (src/stadium.c, AnnouncePlayer)
#define FLAG_GROUNDED_STATS_V1                  FLAG_GROUNDED(150) // game stats 53+ (white-outs e.d.) zijn op 0 gezet
#define FLAG_USED_IMPLOSION                     FLAG_GROUNDED(151) // de speler heeft ooit IMPLOSION gebruikt
// beacon_dragon { (tools/grounded/maptools/beacon_dragon.py; FLAG_GROUNDED 100-149)
#define FLAG_HIDDEN_ITEM_BEACON_ISLE_BIG_PEARL           FLAG_GROUNDED(100) // Project Grounded: Beacon Isle: verborgen Big Pearl
#define FLAG_HIDDEN_ITEM_BEACON_ISLE_PEARL_STRING        FLAG_GROUNDED(101) // Project Grounded: Beacon Isle: verborgen Pearl String
#define FLAG_ITEM_BEACON_ISLE_CELL_BATTERY               FLAG_GROUNDED(102) // Project Grounded: Beacon Isle: Cell Battery
#define FLAG_ITEM_BEACON_LIGHTHOUSE_THUNDER_STONE        FLAG_GROUNDED(103) // Project Grounded: vuurtoren 1F: Thunder Stone
#define FLAG_ITEM_BEACON_LIGHTHOUSE_ELECTIRIZER          FLAG_GROUNDED(104) // Project Grounded: vuurtoren 2F: Electirizer
// }
// Forces-trio op routes (src/forces.c): DONE = gevangen/verslagen (permanent), HIDE = objectflag, per kaartlading gezet.
#define FLAG_FORCES_TORNADUS_DONE               FLAG_GROUNDED(50)
#define FLAG_FORCES_THUNDURUS_DONE              FLAG_GROUNDED(51)
#define FLAG_FORCES_LANDORUS_DONE               FLAG_GROUNDED(52)
#define FLAG_FORCES_HIDE_TORNADUS               FLAG_GROUNDED(53)
#define FLAG_FORCES_HIDE_THUNDURUS              FLAG_GROUNDED(54)
#define FLAG_FORCES_HIDE_LANDORUS               FLAG_GROUNDED(55)

// Hoopa-quest (Mirage Bazaar, Route 111; data/maps/MirageBazaar/scripts.inc)
#define FLAG_HOOPA_WISH_RICHES                  FLAG_GROUNDED(0)  // wens: rijkdom (Big Nugget)
#define FLAG_HOOPA_WISH_POWER                   FLAG_GROUNDED(1)  // wens: kracht (Choice Band)
#define FLAG_HOOPA_WISH_FAME                    FLAG_GROUNDED(2)  // wens: roem (niets, behalve roem)
#define FLAG_HOOPA_WISH_SNACK                   FLAG_GROUNDED(3)  // wens: een snack (Lava Cookies)
#define FLAG_HOOPA_UNBOUND                      FLAG_GROUNDED(4)  // derde wens gedaan: Hoopa Unbound zit in de schatkamer
#define FLAG_HOOPA_QUEST_DONE                   FLAG_GROUNDED(5)  // Hoopa gevangen of gekregen, Prison Bottle ontvangen
#define FLAG_HIDE_ROUTE111_HOOPA_RING           FLAG_GROUNDED(6)  // ring in de woestijn (alleen post-game)
#define FLAG_HIDE_MIRAGE_BAZAAR_HOOPA           FLAG_GROUNDED(7)  // Hoopa Confined bij Salims kraam
#define FLAG_HIDE_MIRAGE_BAZAAR_SALIM           FLAG_GROUNDED(8)  // Salim (weg zolang hij in de schatkamer zit)
#define FLAG_HIDE_MIRAGE_BAZAAR_VAULT_RING      FLAG_GROUNDED(9)  // ring naar de schatkamer (na de derde wens)
#define FLAG_HIDE_HOOPA_VAULT_HOOPA             FLAG_GROUNDED(10) // Hoopa Unbound in de schatkamer
#define FLAG_HIDE_HOOPA_VAULT_SALIM             FLAG_GROUNDED(11) // Salim in de schatkamer
#define FLAG_ITEM_HOOPA_VAULT_1                 FLAG_GROUNDED(12) // items in de schatkamer
#define FLAG_ITEM_HOOPA_VAULT_2                 FLAG_GROUNDED(13)
#define FLAG_ITEM_HOOPA_VAULT_3                 FLAG_GROUNDED(14)
#define FLAG_HOOPA_BAZAAR_VISITED               FLAG_GROUNDED(15) // eerste keer door de ring: lange tekst

// kaart_vulling_4 { (tools/grounded/maptools/kaart_vulling_4.py; FLAG_GROUNDED 200-329)
#define FLAG_KV4_GRANITECAVE_B1F_GIFT_SPELUNKER          FLAG_GROUNDED(200) // Project Grounded (kaartvulling 4): GraniteCave_B1F: cadeau van Spelunker (HARD_STONE)
#define FLAG_ITEM_KV4_GRANITECAVE_B1F_FIST_PLATE         FLAG_GROUNDED(201) // Project Grounded (kaartvulling 4): GraniteCave_B1F: FIST_PLATE 
#define FLAG_HIDDEN_ITEM_KV4_GRANITECAVE_B1F_REVIVE      FLAG_GROUNDED(202) // Project Grounded (kaartvulling 4): GraniteCave_B1F: verborgen REVIVE 
#define FLAG_HIDDEN_ITEM_KV4_GRANITECAVE_1F_ESCAPE_ROPE  FLAG_GROUNDED(203) // Project Grounded (kaartvulling 4): GraniteCave_1F: verborgen ESCAPE_ROPE (doodlopend gangetje)
#define FLAG_KV4_HIDE_SHOAL_SWIMMER                      FLAG_GROUNDED(204) // Project Grounded (kaartvulling 4): Shoal Cave: zwemmer alleen bij vloed
#define FLAG_KV4_HIDE_SHOAL_SANDBAR                      FLAG_GROUNDED(205) // Project Grounded (kaartvulling 4): Shoal Cave: Splash Plate op de zandbank alleen bij eb
#define FLAG_KV4_SHOAL_SANDBAR_TAKEN                     FLAG_GROUNDED(206) // Project Grounded (kaartvulling 4): Shoal Cave: Splash Plate van de zandbank gepakt
#define FLAG_HIDDEN_ITEM_KV4_SHOALCAVE_LOWTIDEINNERROOM_PEARL_STRING FLAG_GROUNDED(207) // Project Grounded (kaartvulling 4): ShoalCave_LowTideInnerRoom: verborgen PEARL_STRING 
#define FLAG_HIDDEN_ITEM_KV4_SHOALCAVE_LOWTIDEICEROOM_ICICLE_PLATE FLAG_GROUNDED(208) // Project Grounded (kaartvulling 4): ShoalCave_LowTideIceRoom: verborgen ICICLE_PLATE 
#define FLAG_HIDDEN_ITEM_KV4_SEAFLOORCAVERN_ROOM5_DEEP_SEA_SCALE FLAG_GROUNDED(209) // Project Grounded (kaartvulling 4): SeafloorCavern_Room5: verborgen DEEP_SEA_SCALE 
#define FLAG_HIDDEN_ITEM_KV4_SEAFLOORCAVERN_ROOM6_DIVE_BALL FLAG_GROUNDED(210) // Project Grounded (kaartvulling 4): SeafloorCavern_Room6: verborgen DIVE_BALL 
#define FLAG_ITEM_KV4_SEAFLOORCAVERN_ROOM7_DREAD_PLATE   FLAG_GROUNDED(211) // Project Grounded (kaartvulling 4): SeafloorCavern_Room7: DREAD_PLATE 
#define FLAG_HIDDEN_ITEM_KV4_SEAFLOORCAVERN_ROOM7_BIG_PEARL FLAG_GROUNDED(212) // Project Grounded (kaartvulling 4): SeafloorCavern_Room7: verborgen BIG_PEARL 
#define FLAG_HIDDEN_ITEM_KV4_SEAFLOORCAVERN_ROOM9_MAX_ELIXIR FLAG_GROUNDED(213) // Project Grounded (kaartvulling 4): SeafloorCavern_Room9: verborgen MAX_ELIXIR 
#define FLAG_HIDDEN_ITEM_KV4_SEAFLOORCAVERN_ROOM9_DAMP_ROCK FLAG_GROUNDED(214) // Project Grounded (kaartvulling 4): SeafloorCavern_Room9: verborgen DAMP_ROCK 
#define FLAG_ITEM_KV4_CAVEOFORIGIN_1F_PP_UP              FLAG_GROUNDED(215) // Project Grounded (kaartvulling 4): CaveOfOrigin_1F: PP_UP 
#define FLAG_HIDDEN_ITEM_KV4_CAVEOFORIGIN_B1F_COMET_SHARD FLAG_GROUNDED(216) // Project Grounded (kaartvulling 4): CaveOfOrigin_B1F: verborgen COMET_SHARD 
#define FLAG_HIDDEN_ITEM_KV4_CAVEOFORIGIN_B1F_BOTTLE_CAP FLAG_GROUNDED(217) // Project Grounded (kaartvulling 4): CaveOfOrigin_B1F: verborgen BOTTLE_CAP 
#define FLAG_ITEM_KV4_ABANDONEDSHIP_DECK_LUXURY_BALL     FLAG_GROUNDED(218) // Project Grounded (kaartvulling 4): AbandonedShip_Deck: LUXURY_BALL 
#define FLAG_HIDDEN_ITEM_KV4_ABANDONEDSHIP_DECK_HEART_SCALE FLAG_GROUNDED(219) // Project Grounded (kaartvulling 4): AbandonedShip_Deck: verborgen HEART_SCALE 
#define FLAG_HIDDEN_ITEM_KV4_MAGMAHIDEOUT_2F_3R_HEAT_ROCK FLAG_GROUNDED(220) // Project Grounded (kaartvulling 4): MagmaHideout_2F_3R: verborgen HEAT_ROCK 
#define FLAG_HIDDEN_ITEM_KV4_MAGMAHIDEOUT_2F_3R_FULL_RESTORE FLAG_GROUNDED(221) // Project Grounded (kaartvulling 4): MagmaHideout_2F_3R: verborgen FULL_RESTORE 
#define FLAG_HIDDEN_ITEM_KV4_METEORFALLS_B1F_1R_MOON_STONE FLAG_GROUNDED(222) // Project Grounded (kaartvulling 4): MeteorFalls_B1F_1R: verborgen MOON_STONE 
#define FLAG_ITEM_KV4_METEORFALLS_B1F_1R_DRAGON_SCALE    FLAG_GROUNDED(223) // Project Grounded (kaartvulling 4): MeteorFalls_B1F_1R: DRAGON_SCALE 
#define FLAG_HIDDEN_ITEM_KV4_METEORFALLS_B1F_1R_STAR_PIECE FLAG_GROUNDED(224) // Project Grounded (kaartvulling 4): MeteorFalls_B1F_1R: verborgen STAR_PIECE 
#define FLAG_HIDDEN_ITEM_KV4_METEORFALLS_STEVENSCAVE_IRON_PLATE FLAG_GROUNDED(225) // Project Grounded (kaartvulling 4): MeteorFalls_StevensCave: verborgen IRON_PLATE 
#define FLAG_ITEM_KV4_METEORFALLS_STEVENSCAVE_MAX_REVIVE FLAG_GROUNDED(226) // Project Grounded (kaartvulling 4): MeteorFalls_StevensCave: MAX_REVIVE 
#define FLAG_HIDDEN_ITEM_KV4_METEORFALLS_STEVENSCAVE_METAL_COAT FLAG_GROUNDED(227) // Project Grounded (kaartvulling 4): MeteorFalls_StevensCave: verborgen METAL_COAT 
#define FLAG_HIDDEN_ITEM_KV4_ROUTE136_GROTTO_NEVER_MELT_ICE FLAG_GROUNDED(228) // Project Grounded (kaartvulling 4): Route136_Grotto: verborgen NEVER_MELT_ICE 
#define FLAG_ITEM_KV4_ROUTE136_GROTTO_ICE_STONE          FLAG_GROUNDED(229) // Project Grounded (kaartvulling 4): Route136_Grotto: ICE_STONE 
#define FLAG_HIDDEN_ITEM_KV4_NAVELROCK_ENTRANCE_PP_MAX   FLAG_GROUNDED(230) // Project Grounded (kaartvulling 4): NavelRock_Entrance: verborgen PP_MAX 
#define FLAG_ITEM_KV4_NAVELROCK_ENTRANCE_ULTRA_BALL      FLAG_GROUNDED(231) // Project Grounded (kaartvulling 4): NavelRock_Entrance: ULTRA_BALL 
#define FLAG_HIDDEN_ITEM_KV4_SHIPWRECKSHOALS_RELIC_GOLD  FLAG_GROUNDED(232) // Project Grounded (kaartvulling 4): ShipwreckShoals: verborgen RELIC_GOLD 
#define FLAG_ITEM_KV4_SHIPWRECKSHOALS_SPELL_TAG          FLAG_GROUNDED(233) // Project Grounded (kaartvulling 4): ShipwreckShoals: SPELL_TAG 
#define FLAG_HIDDEN_ITEM_KV4_SHIPWRECKSHOALS_PEARL_STRING FLAG_GROUNDED(234) // Project Grounded (kaartvulling 4): ShipwreckShoals: verborgen PEARL_STRING 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_NORTH_SOFT_SAND  FLAG_GROUNDED(235) // Project Grounded (kaartvulling 4): SafariZone_North: verborgen SOFT_SAND 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_NORTH_HP_UP      FLAG_GROUNDED(236) // Project Grounded (kaartvulling 4): SafariZone_North: verborgen HP_UP 
#define FLAG_ITEM_KV4_SAFARIZONE_NORTH_SMOOTH_ROCK       FLAG_GROUNDED(237) // Project Grounded (kaartvulling 4): SafariZone_North: SMOOTH_ROCK 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_NORTHWEST_ZINC   FLAG_GROUNDED(238) // Project Grounded (kaartvulling 4): SafariZone_Northwest: verborgen ZINC 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_NORTHWEST_BIG_MUSHROOM FLAG_GROUNDED(239) // Project Grounded (kaartvulling 4): SafariZone_Northwest: verborgen BIG_MUSHROOM 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_SOUTHWEST_CARBOS FLAG_GROUNDED(240) // Project Grounded (kaartvulling 4): SafariZone_Southwest: verborgen CARBOS 
#define FLAG_HIDDEN_ITEM_KV4_SAFARIZONE_SOUTHWEST_MIRACLE_SEED FLAG_GROUNDED(241) // Project Grounded (kaartvulling 4): SafariZone_Southwest: verborgen MIRACLE_SEED 
#define FLAG_HIDDEN_ITEM_KV4_NOTHINGISLAND_NUGGET        FLAG_GROUNDED(242) // Project Grounded (kaartvulling 4): NothingIsland: verborgen NUGGET 
#define FLAG_HIDDEN_ITEM_KV4_NOTHINGISLAND_RELIC_SILVER  FLAG_GROUNDED(243) // Project Grounded (kaartvulling 4): NothingIsland: verborgen RELIC_SILVER 
#define FLAG_HIDDEN_ITEM_KV4_ROUTE124_SHINY_STONE        FLAG_GROUNDED(244) // Project Grounded (kaartvulling 4): Route124: verborgen SHINY_STONE 
#define FLAG_ITEM_KV4_ROUTE124_NET_BALL                  FLAG_GROUNDED(245) // Project Grounded (kaartvulling 4): Route124: NET_BALL 
// }
// zee_vulling_4 { (tools/grounded/maptools/zee_vulling_4.py; FLAG_GROUNDED 330-429)
#define FLAG_ITEM_ZV4_TRENCH_DEEP_SEA_SCALE              FLAG_GROUNDED(330) // Project Grounded (zeevulling 4): item (Underwater_Route127_Trench)
#define FLAG_ITEM_ZV4_TRENCH_DEEP_SEA_TOOTH              FLAG_GROUNDED(331) // Project Grounded (zeevulling 4): item (Underwater_Route127_Trench)
#define FLAG_HIDDEN_ITEM_ZV4_TRENCH_RELIC_CROWN          FLAG_GROUNDED(332) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route127_Trench)
#define FLAG_HIDDEN_ITEM_ZV4_TRENCH_DIVE_BALL            FLAG_GROUNDED(333) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route127_Trench)
#define FLAG_HIDDEN_ITEM_ZV4_SOOTO_PRISM_SCALE           FLAG_GROUNDED(334) // Project Grounded (zeevulling 4): verborgen item (Underwater_SootopolisCity)
#define FLAG_HIDDEN_ITEM_ZV4_WHIRL_SHOAL_SHELL           FLAG_GROUNDED(335) // Project Grounded (zeevulling 4): verborgen item (Underwater_WhirlIsland)
#define FLAG_HIDDEN_ITEM_ZV4_MARINE_SPLASH_PLATE         FLAG_GROUNDED(336) // Project Grounded (zeevulling 4): verborgen item (Underwater_MarineCave)
#define FLAG_HIDDEN_ITEM_ZV4_R134_RELIC_SILVER           FLAG_GROUNDED(337) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route134)
#define FLAG_HIDDEN_ITEM_ZV4_SEAFLOOR_NET_BALL           FLAG_GROUNDED(338) // Project Grounded (zeevulling 4): verborgen item (Underwater_SeafloorCavern)
#define FLAG_HIDDEN_ITEM_ZV4_SEALED_RELIC_STATUE         FLAG_GROUNDED(339) // Project Grounded (zeevulling 4): verborgen item (Underwater_SealedChamber)
#define FLAG_HIDDEN_ITEM_ZV4_UW136_NEVER_MELT_ICE        FLAG_GROUNDED(340) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route136)
#define FLAG_HIDDEN_ITEM_ZV4_UW105_PEARL_STRING          FLAG_GROUNDED(341) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route105)
#define FLAG_HIDDEN_ITEM_ZV4_UW124_STAR_PIECE            FLAG_GROUNDED(342) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route124)
#define FLAG_HIDDEN_ITEM_ZV4_UW125_BIG_PEARL             FLAG_GROUNDED(343) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route125)
#define FLAG_HIDDEN_ITEM_ZV4_UW126_BIG_NUGGET            FLAG_GROUNDED(344) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route126)
#define FLAG_HIDDEN_ITEM_ZV4_UW126_HEART_SCALE           FLAG_GROUNDED(345) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route126)
#define FLAG_HIDDEN_ITEM_ZV4_UW127_PP_MAX                FLAG_GROUNDED(346) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route127)
#define FLAG_HIDDEN_ITEM_ZV4_UW128_MAX_REVIVE            FLAG_GROUNDED(347) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route128)
#define FLAG_HIDDEN_ITEM_ZV4_UW129_BOTTLE_CAP            FLAG_GROUNDED(348) // Project Grounded (zeevulling 4): verborgen item (Underwater_Route129)
#define FLAG_HIDDEN_ITEM_ZV4_R126_STARDUST               FLAG_GROUNDED(349) // Project Grounded (zeevulling 4): verborgen item (Route126)
#define FLAG_HIDDEN_ITEM_ZV4_R126_DIVE_BALL              FLAG_GROUNDED(350) // Project Grounded (zeevulling 4): verborgen item (Route126)
#define FLAG_HIDDEN_ITEM_ZV4_R127_DEEP_SEA_TOOTH         FLAG_GROUNDED(351) // Project Grounded (zeevulling 4): verborgen item (Route127)
#define FLAG_HIDDEN_ITEM_ZV4_R128_HEAT_ROCK              FLAG_GROUNDED(352) // Project Grounded (zeevulling 4): verborgen item (Route128)
#define FLAG_HIDDEN_ITEM_ZV4_R130_STAR_PIECE             FLAG_GROUNDED(353) // Project Grounded (zeevulling 4): verborgen item (Route130)
#define FLAG_HIDDEN_ITEM_ZV4_R132_SHOAL_SALT             FLAG_GROUNDED(354) // Project Grounded (zeevulling 4): verborgen item (Route132)
#define FLAG_HIDDEN_ITEM_ZV4_R132_HEART_SCALE            FLAG_GROUNDED(355) // Project Grounded (zeevulling 4): verborgen item (Route132)
#define FLAG_HIDDEN_ITEM_ZV4_R133_PEARL                  FLAG_GROUNDED(356) // Project Grounded (zeevulling 4): verborgen item (Route133)
#define FLAG_HIDDEN_ITEM_ZV4_R133_RARE_CANDY             FLAG_GROUNDED(357) // Project Grounded (zeevulling 4): verborgen item (Route133)
#define FLAG_HIDDEN_ITEM_ZV4_R134_RELIC_COPPER           FLAG_GROUNDED(358) // Project Grounded (zeevulling 4): verborgen item (Route134)
// } zee_vulling_4
// Gifts (360-399): Type: Null (Devon Corp 2F), Magearna (Colress, Mauville), regionale vormen (Paradiso Resort-lobby)
#define FLAG_RECEIVED_TYPE_NULL                 FLAG_GROUNDED(360)
#define FLAG_RECEIVED_MAGEARNA                  FLAG_GROUNDED(361)
#define FLAG_RECEIVED_ALOLA_RATTATA             FLAG_GROUNDED(362)
#define FLAG_RECEIVED_ALOLA_MEOWTH              FLAG_GROUNDED(363)
#define FLAG_RECEIVED_GALAR_FARFETCHD           FLAG_GROUNDED(364)

// Special Flags (Stored in EWRAM (sSpecialFlags), not in the SaveBlock)
#define SPECIAL_FLAGS_START                     0x4000
#define FLAG_HIDE_MAP_NAME_POPUP                (SPECIAL_FLAGS_START + 0x0)
#define FLAG_DONT_TRANSITION_MUSIC              (SPECIAL_FLAGS_START + 0x1)
#define FLAG_ENABLE_MULTI_CORRIDOR_DOOR         (SPECIAL_FLAGS_START + 0x2)
#define FLAG_SPECIAL_FLAG_UNUSED_0x4003         (SPECIAL_FLAGS_START + 0x3) // Unused Flag
#define FLAG_STORING_ITEMS_IN_PYRAMID_BAG       (SPECIAL_FLAGS_START + 0x4)
#define FLAG_SAFE_FOLLOWER_MOVEMENT             (SPECIAL_FLAGS_START + 0x5) // When set, applymovement does not put the follower inside a pokeball
                                                                            // Also, scripted movements on the player will move follower(s), too
// FLAG_SPECIAL_FLAG_0x4005 - 0x407F also exist and are unused
#define SPECIAL_FLAGS_END                       (SPECIAL_FLAGS_START + 0x7F)
#define NUM_SPECIAL_FLAGS                       (SPECIAL_FLAGS_END - SPECIAL_FLAGS_START + 1)

// Temp flag aliases
#define FLAG_TEMP_SKIP_GABBY_INTERVIEW          FLAG_TEMP_1
#define FLAG_TEMP_REGICE_PUZZLE_STARTED         FLAG_TEMP_2
#define FLAG_TEMP_REGICE_PUZZLE_FAILED          FLAG_TEMP_3
#define FLAG_TEMP_HIDE_FOLLOWER                 FLAG_TEMP_E
#define FLAG_TEMP_HIDE_MIRAGE_ISLAND_BERRY_TREE FLAG_TEMP_11

#if TESTING
#define TESTING_FLAGS_START                     0x5000
#define TESTING_FLAG_SLEEP_CLAUSE               (TESTING_FLAGS_START + 0x0)
#define TESTING_FLAG_INVERSE_BATTLE             (TESTING_FLAGS_START + 0x1)
#define TESTING_FLAG_UNUSED_2                   (TESTING_FLAGS_START + 0x2)
#define TESTING_FLAG_UNUSED_3                   (TESTING_FLAGS_START + 0x3)
#define TESTING_FLAG_UNUSED_4                   (TESTING_FLAGS_START + 0x4)
#define TESTING_FLAG_UNUSED_5                   (TESTING_FLAGS_START + 0x5)
#define TESTING_FLAG_UNUSED_6                   (TESTING_FLAGS_START + 0x6)
#define TESTING_FLAG_UNUSED_7                   (TESTING_FLAGS_START + 0x7)
#endif // TESTING

#endif // GUARD_CONSTANTS_FLAGS_H
