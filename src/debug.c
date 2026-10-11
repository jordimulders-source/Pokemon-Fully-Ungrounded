#include "global.h"
#include "battle.h"
#include "battle_setup.h"
#include "berry.h"
#include "clock.h"
#include "coins.h"
#include "credits.h"
#include "data.h"
#include "daycare.h"
#include "debug.h"
#include "decoration.h"
#include "decoration_inventory.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "event_scripts.h"
#include "field_message_box.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "follower_npc.h"
#include "international_string_util.h"
#include "item.h"
#include "item_icon.h"
#include "item_use.h"
#include "list_menu.h"
#include "m4a.h"
#include "main.h"
#include "main_menu.h"
#include "malloc.h"
#include "map_name_popup.h"
#include "menu.h"
#include "money.h"
#include "naming_screen.h"
#include "new_game.h"
#include "overworld.h"
#include "palette.h"
#include "party_menu.h"
#include "pokedex.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "pokemon_storage_system.h"
#include "random.h"
#include "region_map.h"
#include "rtc.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "sound.h"
#include "strings.h"
#include "string_util.h"
#include "task.h"
#include "tv.h"
#include "pokemon_summary_screen.h"
#include "wild_encounter.h"
#include "constants/abilities.h"
#include "constants/battle_ai.h"
#include "constants/battle_frontier.h"
#include "constants/coins.h"
#include "constants/decorations.h"
#include "constants/event_objects.h"
#include "constants/expansion.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "constants/weather.h"
#include "siirtc.h"
#include "rtc.h"
#include "fake_rtc.h"
#include "save.h"

enum FollowerNPCCreateDebugMenu
{
    DEBUG_FNPC_BRENDAN,
    DEBUG_FNPC_MAY,
    DEBUG_FNPC_STEVEN,
    DEBUG_FNPC_WALLY,
    DEBUG_FNPC_RED,
    DEBUG_FNPC_LEAF,
    DEBUG_FNPC_COUNT,
};

enum FlagsVarsDebugMenu
{
    DEBUG_FLAGVAR_MENU_ITEM_FLAGS,
    DEBUG_FLAGVAR_MENU_ITEM_VARS,
    DEBUG_FLAGVAR_MENU_ITEM_DEXFLAGS_ALL,
    DEBUG_FLAGVAR_MENU_ITEM_DEXFLAGS_RESET,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKEDEX,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_NATDEX,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKENAV,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_MATCH_CALL,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_RUN_SHOES,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_LOCATIONS,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BADGES_ALL,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_GAME_CLEAR,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_FRONTIER_PASS,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_COLLISION,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_ENCOUNTER,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_TRAINER_SEE,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_CATCHING,
    DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BAG_USE,
};

enum DebugBattleType
{
    DEBUG_BATTLE_0_MENU_ITEM_WILD,
    DEBUG_BATTLE_0_MENU_ITEM_WILD_DOUBLE,
    DEBUG_BATTLE_0_MENU_ITEM_SINGLE,
    DEBUG_BATTLE_0_MENU_ITEM_DOUBLE,
    DEBUG_BATTLE_0_MENU_ITEM_MULTI,
};

enum DebugBattleAIFlags
{
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_00,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_01,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_02,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_03,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_04,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_05,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_06,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_07,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_08,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_09,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_10,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_11,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_12,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_13,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_14,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_15,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_16,
    DEBUG_BATTLE_1_MENU_ITEM_AI_FLAG_17,
    DEBUG_BATTLE_1_MENU_ITEM_CONTINUE,
};

enum DebugBattleEnvironment
{
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_0,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_1,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_2,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_3,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_4,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_5,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_6,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_7,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_8,
    DEBUG_BATTLE_2_MENU_ITEM_ENVIRONMENT_9,
};

// *******************************
// Constants
#define DEBUG_MENU_FONT FONT_NORMAL

#define DEBUG_MENU_WIDTH_MAIN 17
#define DEBUG_MENU_HEIGHT_MAIN 9

#define DEBUG_MENU_WIDTH_EXTRA 10
#define DEBUG_MENU_HEIGHT_EXTRA 4

#define DEBUG_MENU_WIDTH_WEATHER 15
#define DEBUG_MENU_HEIGHT_WEATHER 3

#define DEBUG_MENU_WIDTH_SOUND 20
#define DEBUG_MENU_HEIGHT_SOUND 6

#define DEBUG_MENU_WIDTH_FLAGVAR 4
#define DEBUG_MENU_HEIGHT_FLAGVAR 2

#define DEBUG_NUMBER_DIGITS_FLAGS 4
#define DEBUG_NUMBER_DIGITS_VARIABLES 5
#define DEBUG_NUMBER_DIGITS_VARIABLE_VALUE 5
#define DEBUG_NUMBER_DIGITS_ITEMS 4
#define DEBUG_NUMBER_DIGITS_ITEM_QUANTITY 3

#define DEBUG_NUMBER_ICON_X 210
#define DEBUG_NUMBER_ICON_Y 50

#define DEBUG_MAX_MENU_ITEMS 160 // Project Grounded: was 20, daarna 50; "Battle test…" heeft er >100 (alles boven het maximum viel stil weg)
#define DEBUG_MAX_SUB_MENU_LEVELS 4

// *******************************
struct DebugMenuOption;

typedef void (*DebugFunc)(u8 taskId);
typedef void (*DebugSubmenuFunc)(u8 taskId, const struct DebugMenuOption *items);

struct DebugMenuOption
{
    const u8 *text;
    const void *action;
    const void *actionParams;
};

struct DebugMonData
{
    u16 species;
    u8 level;
    bool8 isShiny:1;
    u8 nature:5;
    u8 abilityNum:2;
    u8 monIVs[NUM_STATS];
    u16 monMoves[MAX_MON_MOVES];
    u8 monEVs[NUM_STATS];
    u8 teraType;
    u8 dynamaxLevel:7;
    u8 gmaxFactor:1;
};

struct DebugMenuListData
{
    const struct DebugMenuOption *subMenuItems[DEBUG_MAX_SUB_MENU_LEVELS];
    struct ListMenuItem listItems[DEBUG_MAX_MENU_ITEMS + 1];
    u8 itemNames[DEBUG_MAX_MENU_ITEMS + 1][26];
    u8 listId;
};

// EWRAM
static EWRAM_DATA struct DebugMonData *sDebugMonData = NULL;
static EWRAM_DATA struct DebugMenuListData *sDebugMenuListData = NULL;
EWRAM_DATA bool8 gIsDebugBattle = FALSE;
EWRAM_DATA u64 gDebugAIFlags = 0;

// *******************************
// Define functions
static void Debug_ShowMenu(DebugFunc HandleInput, const struct DebugMenuOption *items);
static u8 Debug_GenerateListMenuNames(void);
static void Debug_DestroyMenu(u8 taskId);
static void DebugAction_Cancel(u8 taskId);
static void DebugAction_DestroyExtraWindow(u8 taskId);
static void Debug_RefreshListMenu(u8 taskId);
static u8 DebugNativeStep_CreateDebugWindow(void);
static void DebugNativeStep_CloseDebugWindow(u8 taskId);

static void DebugAction_OpenSubMenu(u8 taskId, const struct DebugMenuOption *items);
static void DebugAction_OpenSubMenuFlagsVars(u8 taskId, const struct DebugMenuOption *items);
static void DebugAction_OpenSubMenuFakeRTC(u8 taskId, const struct DebugMenuOption *items);
static void DebugAction_OpenSubMenuCreateFollowerNPC(u8 taskId, const struct DebugMenuOption *items);
static void DebugAction_ExecuteScript(u8 taskId, const u8 *script);
static void DebugAction_ToggleFlag(u8 taskId);

static void DebugTask_HandleMenuInput_General(u8 taskId);

static void DebugAction_Util_Fly(u8 taskId);
static void DebugAction_Util_Warp_Warp(u8 taskId);
static void DebugAction_Util_Warp_SelectMapGroup(u8 taskId);
static void DebugAction_Util_Warp_SelectMap(u8 taskId);
static void DebugAction_Util_Warp_SelectWarp(u8 taskId);
static void DebugAction_Util_Weather(u8 taskId);
static void DebugAction_Util_Weather_SelectId(u8 taskId);
static void DebugAction_Util_WatchCredits(u8 taskId);
static void DebugAction_Util_CheatStart(u8 taskId);

static void DebugAction_TimeMenu_ChangeTimeOfDay(u8 taskId);
static void DebugAction_TimeMenu_ChangeWeekdays(u8 taskId);

static void DebugAction_CreateFollowerNPC(u8 taskId);
static void DebugAction_DestroyFollowerNPC(u8 taskId);

static void DebugAction_PCBag_Fill_PCBoxes_Fast(u8 taskId);
static void DebugAction_PCBag_Fill_PCBoxes_Slow(u8 taskId);
static void DebugAction_PCBag_Fill_PCItemStorage(u8 taskId);
static void DebugAction_PCBag_Fill_PocketItems(u8 taskId);
static void DebugAction_PCBag_Fill_PocketPokeBalls(u8 taskId);
static void DebugAction_PCBag_Fill_PocketTMHM(u8 taskId);
static void DebugAction_PCBag_Fill_PocketBerries(u8 taskId);
static void DebugAction_PCBag_Fill_PocketKeyItems(u8 taskId);
static void DebugAction_PCBag_ClearBag(u8 taskId);
static void DebugAction_PCBag_ClearBoxes(u8 taskId);

static void DebugAction_Party_HealParty(u8 taskId);
static void DebugAction_Party_ClearParty(u8 taskId);
static void DebugAction_Party_SetParty(u8 taskId);
static void DebugAction_Party_BattleSingle(u8 taskId);

static void DebugAction_FlagsVars_Flags(u8 taskId);
static void DebugAction_FlagsVars_FlagsSelect(u8 taskId);
static void DebugAction_FlagsVars_Vars(u8 taskId);
static void DebugAction_FlagsVars_Select(u8 taskId);
static void DebugAction_FlagsVars_SetValue(u8 taskId);
static void DebugAction_FlagsVars_PokedexFlags_All(u8 taskId);
static void DebugAction_FlagsVars_PokedexFlags_Reset(u8 taskId);
static void DebugAction_FlagsVars_SwitchDex(u8 taskId);
static void DebugAction_FlagsVars_SwitchNatDex(u8 taskId);
static void DebugAction_FlagsVars_SwitchPokeNav(u8 taskId);
static void DebugAction_FlagsVars_SwitchMatchCall(u8 taskId);
static void DebugAction_FlagsVars_ToggleFlyFlags(u8 taskId);
static void DebugAction_FlagsVars_ToggleBadgeFlags(u8 taskId);
static void DebugAction_FlagsVars_ToggleGameClear(u8 taskId);
static void DebugAction_FlagsVars_ToggleFrontierPass(u8 taskId);
static void DebugAction_FlagsVars_CollisionOnOff(u8 taskId);
static void DebugAction_FlagsVars_EncounterOnOff(u8 taskId);
static void DebugAction_FlagsVars_TrainerSeeOnOff(u8 taskId);
static void DebugAction_FlagsVars_BagUseOnOff(u8 taskId);
static void DebugAction_FlagsVars_CatchingOnOff(u8 taskId);
static void DebugAction_FlagsVars_RunningShoes(u8 taskId);

static void DebugAction_Give_Item(u8 taskId);
static void DebugAction_Give_Item_SelectId(u8 taskId);
static void DebugAction_Give_Item_SelectQuantity(u8 taskId);
static void DebugAction_Give_PokemonSimple(u8 taskId);
static void DebugAction_Give_PokemonComplex(u8 taskId);
static void DebugAction_Give_Pokemon_SelectId(u8 taskId);
static void DebugAction_Util_ForceEncounter(u8 taskId);
struct BattleTest;
static void DebugAction_Util_BattleTest(u8 taskId, const struct BattleTest *test);
static void DebugAction_Util_ZoneWarp(u8 taskId, const void *mapId); // Project Grounded
static void DebugAction_Util_ForceEncounter_SelectId(u8 taskId);
static void DebugAction_Give_Pokemon_SelectLevel(u8 taskId);
static void DebugAction_Give_Pokemon_SelectShiny(u8 taskId);
static void DebugAction_Give_Pokemon_SelectNature(u8 taskId);
static void DebugAction_Give_Pokemon_SelectAbility(u8 taskId);
static void DebugAction_Give_Pokemon_SelectTeraType(u8 taskId);
static void DebugAction_Give_Pokemon_SelectDynamaxLevel(u8 taskId);
static void DebugAction_Give_Pokemon_SelectGigantamaxFactor(u8 taskId);
static void DebugAction_Give_Pokemon_SelectIVs(u8 taskId);
static void DebugAction_Give_Pokemon_SelectEVs(u8 taskId);
static void DebugAction_Give_Pokemon_ComplexCreateMon(u8 taskId);
static void DebugAction_Give_Pokemon_Move(u8 taskId);
static void DebugAction_Give_Decoration(u8 taskId);
static void DebugAction_Give_Decoration_SelectId(u8 taskId);
static void DebugAction_Give_MaxMoney(u8 taskId);
static void DebugAction_Give_MaxCoins(u8 taskId);
static void DebugAction_Give_MaxBattlePoints(u8 taskId);
static void DebugAction_Give_DayCareEgg(u8 taskId);

static void DebugAction_Sound_SE(u8 taskId);
static void DebugAction_Sound_SE_SelectId(u8 taskId);
static void DebugAction_Sound_MUS(u8 taskId);
static void DebugAction_Sound_MUS_SelectId(u8 taskId);

static void DebugAction_BerryFunctions_ClearAll(u8 taskId);
static void DebugAction_BerryFunctions_Ready(u8 taskId);
static void DebugAction_BerryFunctions_NextStage(u8 taskId);
static void DebugAction_BerryFunctions_Pests(u8 taskId);
static void DebugAction_BerryFunctions_Weeds(u8 taskId);

static void DebugAction_Player_Name(u8 taskId);
static void DebugAction_Player_Gender(u8 taskId);
static void DebugAction_Player_Id(u8 taskId);

extern const u8 Debug_FlagsNotSetOverworldConfigMessage[];
extern const u8 Debug_FlagsNotSetBattleConfigMessage[];
extern const u8 Debug_VarsNotSetBattleConfigMessage[];
extern const u8 Debug_FlagsAndVarNotSetBattleConfigMessage[];
extern const u8 Debug_EventScript_FontTest[];
extern const u8 Debug_EventScript_CheckEVs[];
extern const u8 Debug_EventScript_CheckIVs[];
extern const u8 Debug_EventScript_InflictStatus1[];
extern const u8 Debug_EventScript_SetHiddenNature[];
extern const u8 Debug_EventScript_SetAbility[];
extern const u8 Debug_EventScript_SetFriendship[];
extern const u8 Debug_EventScript_Script_1[];
extern const u8 Debug_EventScript_Script_2[];
extern const u8 Debug_EventScript_Script_3[];
extern const u8 Debug_EventScript_Script_4[];
extern const u8 Debug_EventScript_Script_5[];
extern const u8 Debug_EventScript_Script_6[];
extern const u8 Debug_EventScript_Script_7[];
extern const u8 Debug_EventScript_Script_8[];
extern const u8 DebugScript_DaycareMonsNotCompatible[];
extern const u8 DebugScript_OneDaycareMons[];
extern const u8 DebugScript_ZeroDaycareMons[];

extern const u8 Debug_ShowFieldMessageStringVar4[];
extern const u8 Debug_CheatStart[];
extern const u8 Debug_HatchAnEgg[];
extern const u8 PlayersHouse_2F_EventScript_SetWallClock[];
extern const u8 PlayersHouse_2F_EventScript_CheckWallClock[];
extern const u8 Debug_CheckSaveBlock[];
extern const u8 Debug_CheckROMSpace[];
extern const u8 Debug_BoxFilledMessage[];
extern const u8 Debug_ShowExpansionVersion[];
extern const u8 Debug_EventScript_EWRAMCounters[];
extern const u8 Debug_Follower_NPC_Event_Script[];
extern const u8 Debug_Follower_NPC_Not_Enabled[];
extern const u8 Debug_EventScript_Steven_Multi[];
extern const u8 Debug_EventScript_Legend_G_ArceusNormal[];
extern const u8 Debug_EventScript_Legend_G_Dialga[];
extern const u8 Debug_EventScript_Legend_G_Palkia[];
extern const u8 Debug_EventScript_Legend_G_GiratinaAltered[];
extern const u8 Debug_EventScript_Legend_G_Celebi[];
extern const u8 Debug_EventScript_Legend_G_Uxie[];
extern const u8 Debug_EventScript_Legend_G_Mesprit[];
extern const u8 Debug_EventScript_Legend_G_Azelf[];
extern const u8 Debug_EventScript_Legend_G_Cresselia[];
extern const u8 Debug_EventScript_Legend_G_MeloettaAria[];
extern const u8 Debug_EventScript_Legend_G_Zeraora[];
extern const u8 Debug_EventScript_Legend_G_Zygarde50[];
extern const u8 Debug_EventScript_Legend_G_Necrozma[];
extern const u8 Debug_EventScript_Legend_G_Eternatus[];
extern const u8 Debug_EventScript_Legend_G_Calyrex[];
extern const u8 Debug_EventScript_Legend_G_Glastrier[];
extern const u8 Debug_EventScript_Legend_G_Spectrier[];
extern const u8 Debug_EventScript_Legend_G_Cobalion[];
extern const u8 Debug_EventScript_Legend_G_Terrakion[];
extern const u8 Debug_EventScript_Legend_G_Virizion[];
extern const u8 Debug_EventScript_Legend_G_KeldeoOrdinary[];
extern const u8 Debug_EventScript_Legend_G_Pecharunt[];
extern const u8 Debug_EventScript_Legend_G_Xerneas[];
extern const u8 Debug_EventScript_Legend_G_Yveltal[];
extern const u8 Debug_EventScript_Legend_G_ZacianHero[];
extern const u8 Debug_EventScript_Legend_G_ZamazentaHero[];
extern const u8 Debug_EventScript_Legend_G_Articuno[];
extern const u8 Debug_EventScript_Legend_G_Zapdos[];
extern const u8 Debug_EventScript_Legend_G_Moltres[];
extern const u8 Debug_EventScript_Legend_G_ArticunoGalar[];
extern const u8 Debug_EventScript_Legend_G_ZapdosGalar[];
extern const u8 Debug_EventScript_Legend_G_MoltresGalar[];
extern const u8 Debug_EventScript_Legend_G_Victini[];
extern const u8 Debug_EventScript_Legend_G_ShayminLand[];
extern const u8 Debug_EventScript_Legend_G_Manaphy[];
extern const u8 Debug_EventScript_Legend_G_Volcanion[];
extern const u8 Debug_EventScript_Legend_G_HoopaConfined[];
extern const u8 Debug_EventScript_Legend_G_TornadusIncarnate[];
extern const u8 Debug_EventScript_Legend_G_ThundurusIncarnate[];
extern const u8 Debug_EventScript_Legend_G_LandorusIncarnate[];
extern const u8 Debug_EventScript_Legend_G_Zarude[];
extern const u8 Debug_EventScript_Legend_G_WoChien[];
extern const u8 Debug_EventScript_Legend_G_ChienPao[];
extern const u8 Debug_EventScript_Legend_G_TingLu[];
extern const u8 Debug_EventScript_Legend_G_ChiYu[];
extern const u8 Debug_EventScript_Legend_G_OgerponTeal[];
extern const u8 Debug_EventScript_Legend_G_TapuKoko[];
extern const u8 Debug_EventScript_Legend_G_Nihilego[];
extern const u8 Debug_EventScript_Legend_G_Buzzwole[];
extern const u8 Debug_EventScript_Legend_G_Pheromosa[];
extern const u8 Debug_EventScript_Legend_G_Kartana[];
extern const u8 Debug_EventScript_Legend_G_Koraidon[];
extern const u8 Debug_EventScript_Legend_G_Miraidon[];
extern const u8 Debug_EventScript_Legend_G_TerapagosNormal[];
extern const u8 Debug_EventScript_Legend_G_GreatTusk[];
extern const u8 Debug_EventScript_Legend_G_IronValiant[];
extern const u8 Debug_EventScript_Legend_G_Reshiram[];
extern const u8 Debug_EventScript_Legend_G_Zekrom[];
extern const u8 Debug_EventScript_Legend_G_Kyurem[];
extern const u8 Debug_EventScript_Legend_G_Marshadow[];
extern const u8 Debug_EventScript_Legend_Regirock[];
extern const u8 Debug_EventScript_Legend_Regice[];
extern const u8 Debug_EventScript_Legend_Registeel[];
extern const u8 Debug_EventScript_Legend_Regidrago[];
extern const u8 Debug_EventScript_Legend_Regieleki[];
extern const u8 Debug_EventScript_Legend_Regigigas[];
extern const u8 Debug_EventScript_Legend_Suicune[];
extern const u8 Debug_EventScript_Legend_Raikou[];
extern const u8 Debug_EventScript_Legend_Entei[];
extern const u8 Debug_EventScript_Legend_Groudon[];
extern const u8 Debug_EventScript_Legend_Kyogre[];
extern const u8 Debug_EventScript_Legend_Rayquaza[];
extern const u8 Debug_EventScript_Legend_DeoxysNormal[];
extern const u8 Debug_EventScript_Legend_Mew[];
extern const u8 Debug_EventScript_Legend_Latias[];
extern const u8 Debug_EventScript_Legend_Latios[];
extern const u8 Debug_EventScript_Legend_Lugia[];
extern const u8 Debug_EventScript_Legend_HoOh[];
extern const u8 Debug_EventScript_Legend_Heatran[];
extern const u8 Debug_EventScript_Legend_Genesect[];
extern const u8 Debug_EventScript_Legend_Mewtwo[];
extern const u8 Debug_EventScript_Legend_Jirachi[];
extern const u8 Debug_EventScript_Legend_Darkrai[];
extern const u8 Debug_EventScript_WildFromMap[];
extern const u8 Debug_EventScript_BattleTest[];
extern const u8 Debug_EventScript_BurglarForce[];
extern const u8 Debug_EventScript_ForcedEncounterSet[];
extern const u8 Debug_EventScript_ForcedEncounterOff[];
extern const u8 Debug_EventScript_SpirePrototype[];
extern const u8 Debug_EventScript_SpireResetRun[];
extern const u8 Debug_EventScript_SpireWarp[];
extern const u8 Debug_EventScript_StadiumWarp[];
extern const u8 BattleStadium_EventScript_Singles[];
extern const u8 BattleStadium_EventScript_Doubles[];
extern const u8 Debug_EventScript_StadiumUnlockAll[];
extern const u8 Debug_EventScript_PrintTimeOfDay[];
extern const u8 Debug_EventScript_TellTheTime[];
extern const u8 Debug_EventScript_FakeRTCNotEnabled[];

extern const u8 Debug_BerryPestsDisabled[];
extern const u8 Debug_BerryWeedsDisabled[];

extern const u8 Common_EventScript_MoveRelearner[];

#include "data/map_group_count.h"

// Text
// General
static const u8 sDebugText_Arrow[] =          _("{CLEAR_TO 110}{RIGHT_ARROW}");
static const u8 sDebugText_True[] =          _("TRUE");
static const u8 sDebugText_False[] =         _("FALSE");
static const u8 sDebugText_Colored_True[] =  _("{COLOR GREEN}TRUE");
static const u8 sDebugText_Colored_False[] = _("{COLOR RED}FALSE");
static const u8 sDebugText_Dashes[] =        _("---");
static const u8 sDebugText_Empty[] =         _("");
static const u8 sDebugText_Continue[] =      _("Continue…");
// Util Menu
static const u8 sDebugText_Util_WarpToMap_SelectMapGroup[] = _("Group: {STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n\n{STR_VAR_3}{CLEAR_TO 90}");
static const u8 sDebugText_Util_WarpToMap_SelectMap[] =      _("Map: {STR_VAR_1}{CLEAR_TO 90}\nMapSec:{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}\n{STR_VAR_3}{CLEAR_TO 90}");
static const u8 sDebugText_Util_WarpToMap_SelectWarp[] =     _("Warp:{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_3}{CLEAR_TO 90}");
static const u8 sDebugText_Util_WarpToMap_SelMax[] =         _("{STR_VAR_1} / {STR_VAR_2}");
static const u8 sDebugText_Util_Weather_ID[] =               _("Weather ID: {STR_VAR_3}\n{STR_VAR_1}\n{STR_VAR_2}");

//Time Menu

static const u8 *const gDayNameStringsTable[WEEKDAY_COUNT] = {
    COMPOUND_STRING("Sunday"),
    COMPOUND_STRING("Monday"),
    COMPOUND_STRING("Tuesday"),
    COMPOUND_STRING("Wednesday"),
    COMPOUND_STRING("Thursday"),
    COMPOUND_STRING("Friday"),
    COMPOUND_STRING("Saturday"),
};

static const u8 *const gTimeOfDayStringsTable[TIMES_OF_DAY_COUNT] = {
    COMPOUND_STRING("Morning"),
    COMPOUND_STRING("Day"),
    COMPOUND_STRING("Evening"),
    COMPOUND_STRING("Night"),
};

// Follower NPC

static const u8 *const gFollowerNPCStringsTable[DEBUG_FNPC_COUNT] = {
    COMPOUND_STRING("Brendan"),
    COMPOUND_STRING("May"),
    COMPOUND_STRING("Steven"),
    COMPOUND_STRING("Wally"),
    COMPOUND_STRING("Red"),
    COMPOUND_STRING("Leaf"),
};

// Flags/Vars Menu
static const u8 sDebugText_FlagsVars_VariableHex[] =         _("{STR_VAR_1}{CLEAR_TO 90}\n0x{STR_VAR_2}{CLEAR_TO 90}");
static const u8 sDebugText_FlagsVars_Variable[] =            _("Var: {STR_VAR_1}{CLEAR_TO 90}\nVal: {STR_VAR_3}{CLEAR_TO 90}\n{STR_VAR_2}");
static const u8 sDebugText_FlagsVars_VariableValueSet[] =    _("Var: {STR_VAR_1}{CLEAR_TO 90}\nVal: {STR_VAR_3}{CLEAR_TO 90}\n{STR_VAR_2}");
// Give Menu
static const u8 sDebugText_PokemonShiny[] =             _("Shiny:{CLEAR_TO 90}\n   {STR_VAR_2}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{CLEAR_TO 90}");
static const u8 sDebugText_IVs[] =                      _("IV {STR_VAR_1}:{CLEAR_TO 90}\n    {STR_VAR_3}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}");
static const u8 sDebugText_EVs[] =                      _("EV {STR_VAR_1}:{CLEAR_TO 90}\n    {STR_VAR_3}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}");
// Sound Menu
static const u8 sDebugText_Sound_SFX_ID[] =             _("SFX ID: {STR_VAR_3}   {START_BUTTON} Stop\n{STR_VAR_1}    \n{STR_VAR_2}");
static const u8 sDebugText_Sound_Music_ID[] =           _("Music ID: {STR_VAR_3}   {START_BUTTON} Stop\n{STR_VAR_1}    \n{STR_VAR_2}");

const u8 *const gText_DigitIndicator[] =
{
    COMPOUND_STRING("{LEFT_ARROW}+1{RIGHT_ARROW}        "),
    COMPOUND_STRING("{LEFT_ARROW}+10{RIGHT_ARROW}       "),
    COMPOUND_STRING("{LEFT_ARROW}+100{RIGHT_ARROW}      "),
    COMPOUND_STRING("{LEFT_ARROW}+1000{RIGHT_ARROW}     "),
    COMPOUND_STRING("{LEFT_ARROW}+10000{RIGHT_ARROW}    "),
    COMPOUND_STRING("{LEFT_ARROW}+100000{RIGHT_ARROW}   "),
    COMPOUND_STRING("{LEFT_ARROW}+1000000{RIGHT_ARROW}  "),
    COMPOUND_STRING("{LEFT_ARROW}+10000000{RIGHT_ARROW} "),
};

static const s32 sPowersOfTen[] =
{
             1,
            10,
           100,
          1000,
         10000,
        100000,
       1000000,
      10000000,
     100000000,
    1000000000,
};

// *******************************
// Menu Actions. Make sure that submenus are defined before the menus that call them.
static const struct DebugMenuOption sDebugMenu_Actions_TimeMenu_TimesOfDay[] =
{
    [TIME_MORNING] = { gTimeOfDayStringsTable[TIME_MORNING], DebugAction_TimeMenu_ChangeTimeOfDay },
    [TIME_DAY]     = { gTimeOfDayStringsTable[TIME_DAY],     DebugAction_TimeMenu_ChangeTimeOfDay },
    [TIME_EVENING] = { gTimeOfDayStringsTable[TIME_EVENING], DebugAction_TimeMenu_ChangeTimeOfDay },
    [TIME_NIGHT]   = { gTimeOfDayStringsTable[TIME_NIGHT],   DebugAction_TimeMenu_ChangeTimeOfDay },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_TimeMenu_Weekdays[] =
{
    [WEEKDAY_SUN] = { gDayNameStringsTable[WEEKDAY_SUN], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_MON] = { gDayNameStringsTable[WEEKDAY_MON], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_TUE] = { gDayNameStringsTable[WEEKDAY_TUE], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_WED] = { gDayNameStringsTable[WEEKDAY_WED], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_THU] = { gDayNameStringsTable[WEEKDAY_THU], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_FRI] = { gDayNameStringsTable[WEEKDAY_FRI], DebugAction_TimeMenu_ChangeWeekdays },
    [WEEKDAY_SAT] = { gDayNameStringsTable[WEEKDAY_SAT], DebugAction_TimeMenu_ChangeWeekdays },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_FollowerNPCMenu_Create[] =
{
    [DEBUG_FNPC_BRENDAN] = { gFollowerNPCStringsTable[DEBUG_FNPC_BRENDAN], DebugAction_CreateFollowerNPC },
    [DEBUG_FNPC_MAY] =     { gFollowerNPCStringsTable[DEBUG_FNPC_MAY],     DebugAction_CreateFollowerNPC },
    [DEBUG_FNPC_STEVEN] =  { gFollowerNPCStringsTable[DEBUG_FNPC_STEVEN],  DebugAction_CreateFollowerNPC },
    [DEBUG_FNPC_WALLY] =   { gFollowerNPCStringsTable[DEBUG_FNPC_WALLY],   DebugAction_CreateFollowerNPC },
    [DEBUG_FNPC_RED] =     { gFollowerNPCStringsTable[DEBUG_FNPC_RED],     DebugAction_CreateFollowerNPC },
    [DEBUG_FNPC_LEAF] =    { gFollowerNPCStringsTable[DEBUG_FNPC_LEAF],    DebugAction_CreateFollowerNPC },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_TimeMenu[] =
{
    { COMPOUND_STRING("Get time…"),         DebugAction_ExecuteScript, Debug_EventScript_TellTheTime },
    { COMPOUND_STRING("Get time of day…"),  DebugAction_ExecuteScript, Debug_EventScript_PrintTimeOfDay },
    { COMPOUND_STRING("Set time of day…"),  DebugAction_OpenSubMenuFakeRTC, sDebugMenu_Actions_TimeMenu_TimesOfDay },
    { COMPOUND_STRING("Set weekday…"),      DebugAction_OpenSubMenuFakeRTC, sDebugMenu_Actions_TimeMenu_Weekdays },
    { COMPOUND_STRING("Check wall clock…"), DebugAction_ExecuteScript, PlayersHouse_2F_EventScript_CheckWallClock },
    { COMPOUND_STRING("Set wall clock…"),   DebugAction_ExecuteScript, PlayersHouse_2F_EventScript_SetWallClock },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_BerryFunctions[] =
{
    { COMPOUND_STRING("Clear map trees"),      DebugAction_BerryFunctions_ClearAll },
    { COMPOUND_STRING("Ready map trees"),      DebugAction_BerryFunctions_Ready },
    { COMPOUND_STRING("Grow map trees"),       DebugAction_BerryFunctions_NextStage },
    { COMPOUND_STRING("Give map trees pests"), DebugAction_BerryFunctions_Pests },
    { COMPOUND_STRING("Give map trees weeds"), DebugAction_BerryFunctions_Weeds },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_FollowerNPCMenu[] =
{
    { COMPOUND_STRING("Create Follower"),  DebugAction_OpenSubMenuCreateFollowerNPC, sDebugMenu_Actions_FollowerNPCMenu_Create },
    { COMPOUND_STRING("Destroy Follower"), DebugAction_DestroyFollowerNPC },
    { NULL }
};

// Project Grounded: legendary-gevechten forceren (thema's en transities testen)
static const struct DebugMenuOption sDebugMenu_Actions_Legendary[] =
{
    { COMPOUND_STRING("Regirock"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Regirock },
    { COMPOUND_STRING("Regice"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Regice },
    { COMPOUND_STRING("Registeel"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Registeel },
    { COMPOUND_STRING("Regidrago"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Regidrago },
    { COMPOUND_STRING("Regieleki"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Regieleki },
    { COMPOUND_STRING("Regigigas"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Regigigas },
    { COMPOUND_STRING("Suicune"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Suicune },
    { COMPOUND_STRING("Raikou"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Raikou },
    { COMPOUND_STRING("Entei"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Entei },
    { COMPOUND_STRING("Groudon"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Groudon },
    { COMPOUND_STRING("Kyogre"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Kyogre },
    { COMPOUND_STRING("Rayquaza"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Rayquaza },
    { COMPOUND_STRING("Deoxys"), DebugAction_ExecuteScript, Debug_EventScript_Legend_DeoxysNormal },
    { COMPOUND_STRING("Mew"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Mew },
    { COMPOUND_STRING("Latias"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Latias },
    { COMPOUND_STRING("Latios"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Latios },
    { COMPOUND_STRING("Lugia"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Lugia },
    { COMPOUND_STRING("Ho-Oh"), DebugAction_ExecuteScript, Debug_EventScript_Legend_HoOh },
    { COMPOUND_STRING("Heatran"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Heatran },
    { COMPOUND_STRING("Genesect"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Genesect },
    { COMPOUND_STRING("Mewtwo"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Mewtwo },
    { COMPOUND_STRING("Jirachi"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Jirachi },
    { COMPOUND_STRING("Darkrai"), DebugAction_ExecuteScript, Debug_EventScript_Legend_Darkrai },
    { COMPOUND_STRING("Arceus"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ArceusNormal },
    { COMPOUND_STRING("Dialga"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Dialga },
    { COMPOUND_STRING("Palkia"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Palkia },
    { COMPOUND_STRING("Giratina"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_GiratinaAltered },
    { COMPOUND_STRING("Celebi"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Celebi },
    { COMPOUND_STRING("Uxie"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Uxie },
    { COMPOUND_STRING("Mesprit"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Mesprit },
    { COMPOUND_STRING("Azelf"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Azelf },
    { COMPOUND_STRING("Cresselia"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Cresselia },
    { COMPOUND_STRING("Meloetta"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_MeloettaAria },
    { COMPOUND_STRING("Zeraora"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Zeraora },
    { COMPOUND_STRING("Zygarde"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Zygarde50 },
    { COMPOUND_STRING("Necrozma"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Necrozma },
    { COMPOUND_STRING("Eternatus"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Eternatus },
    { COMPOUND_STRING("Calyrex"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Calyrex },
    { COMPOUND_STRING("Glastrier"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Glastrier },
    { COMPOUND_STRING("Spectrier"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Spectrier },
    { COMPOUND_STRING("Cobalion"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Cobalion },
    { COMPOUND_STRING("Terrakion"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Terrakion },
    { COMPOUND_STRING("Virizion"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Virizion },
    { COMPOUND_STRING("Keldeo"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_KeldeoOrdinary },
    { COMPOUND_STRING("Pecharunt"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Pecharunt },
    { COMPOUND_STRING("Xerneas"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Xerneas },
    { COMPOUND_STRING("Yveltal"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Yveltal },
    { COMPOUND_STRING("Zacian"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ZacianHero },
    { COMPOUND_STRING("Zamazenta"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ZamazentaHero },
    { COMPOUND_STRING("Articuno"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Articuno },
    { COMPOUND_STRING("Zapdos"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Zapdos },
    { COMPOUND_STRING("Moltres"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Moltres },
    { COMPOUND_STRING("Articuno (Galar)"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ArticunoGalar },
    { COMPOUND_STRING("Zapdos (Galar)"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ZapdosGalar },
    { COMPOUND_STRING("Moltres (Galar)"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_MoltresGalar },
    { COMPOUND_STRING("Victini"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Victini },
    { COMPOUND_STRING("Shaymin"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ShayminLand },
    { COMPOUND_STRING("Manaphy"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Manaphy },
    { COMPOUND_STRING("Volcanion"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Volcanion },
    { COMPOUND_STRING("Hoopa"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_HoopaConfined },
    { COMPOUND_STRING("Tornadus"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_TornadusIncarnate },
    { COMPOUND_STRING("Thundurus"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ThundurusIncarnate },
    { COMPOUND_STRING("Landorus"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_LandorusIncarnate },
    { COMPOUND_STRING("Zarude"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Zarude },
    { COMPOUND_STRING("Wo-Chien"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_WoChien },
    { COMPOUND_STRING("Chien-Pao"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ChienPao },
    { COMPOUND_STRING("Ting-Lu"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_TingLu },
    { COMPOUND_STRING("Chi-Yu"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_ChiYu },
    { COMPOUND_STRING("Ogerpon"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_OgerponTeal },
    { COMPOUND_STRING("Tapu Koko"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_TapuKoko },
    { COMPOUND_STRING("Nihilego"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Nihilego },
    { COMPOUND_STRING("Buzzwole"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Buzzwole },
    { COMPOUND_STRING("Pheromosa"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Pheromosa },
    { COMPOUND_STRING("Kartana"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Kartana },
    { COMPOUND_STRING("Koraidon"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Koraidon },
    { COMPOUND_STRING("Miraidon"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Miraidon },
    { COMPOUND_STRING("Terapagos"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_TerapagosNormal },
    { COMPOUND_STRING("Great Tusk"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_GreatTusk },
    { COMPOUND_STRING("Iron Valiant"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_IronValiant },
    { COMPOUND_STRING("Reshiram"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Reshiram },
    { COMPOUND_STRING("Zekrom"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Zekrom },
    { COMPOUND_STRING("Kyurem"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Kyurem },
    { COMPOUND_STRING("Marshadow"), DebugAction_ExecuteScript, Debug_EventScript_Legend_G_Marshadow },
    { NULL }
};

// Project Grounded: debugmenu Utilities > "Battle test…": één gevecht per eigen gevechtsthema en per eigen transitie.
// Wilde legendaries gaan via dezelfde special als het echte event (BattleSetup_StartLegendaryBattle/StartRegiBattle),
// wilde soorten met een eigen transitie via een gewoon gescript wild gevecht, trainers via hun echte trainer-id.
// Route-transities hangen van de kaart af: test die met "Wild battle (map)" op de route zelf.
enum
{
    BATTLE_TEST_LEGEND,  // BattleSetup_StartLegendaryBattle
    BATTLE_TEST_REGI,    // StartRegiBattle
    BATTLE_TEST_LATI,    // BattleSetup_StartLatiBattle (eigen Lati-intro)
    BATTLE_TEST_WILD,    // BattleSetup_StartScriptedWildBattle (transitie per soort)
    BATTLE_TEST_TRAINER, // trainergevecht (id2 = tweede trainer voor een dubbel, anders TRAINER_NONE)
};

struct BattleTest
{
    u8 kind;
    u8 level;
    u16 id;
    u16 id2;
};

#define BT_LEGEND(species, lvl) &(const struct BattleTest){ BATTLE_TEST_LEGEND, lvl, species, 0 }
#define BT_REGI(species)        &(const struct BattleTest){ BATTLE_TEST_REGI, 50, species, 0 }
#define BT_LATI(species)        &(const struct BattleTest){ BATTLE_TEST_LATI, 50, species, 0 }
#define BT_WILD(species)        &(const struct BattleTest){ BATTLE_TEST_WILD, 5, species, 0 }
#define BT_TRAINER(a, b)        &(const struct BattleTest){ BATTLE_TEST_TRAINER, 0, a, b }

static const struct DebugMenuOption sDebugMenu_Actions_BattleTest[] =
{
    // Trainers: eigen thema's en transities
    { COMPOUND_STRING("Wally 1 - Mauville"),     DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLY_MAUVILLE, TRAINER_NONE) },
    { COMPOUND_STRING("Wally 2 - Meteor Falls"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLY_METEOR_FALLS, TRAINER_NONE) },
    { COMPOUND_STRING("Wally 3 - Mt. Pyre"),     DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLY_MT_PYRE, TRAINER_NONE) },
    { COMPOUND_STRING("Wally 4 - Mossdeep"),     DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLY_MOSSDEEP, TRAINER_NONE) },
    { COMPOUND_STRING("Wally 5 - Victory Rd"),   DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLY_VR_1, TRAINER_NONE) },
    { COMPOUND_STRING("Birch (Macarena)"),       DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_BIRCH, TRAINER_NONE) },
    { COMPOUND_STRING("Prof. Oak"),              DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_PROF_OAK, TRAINER_NONE) },
    { COMPOUND_STRING("Brock (Kanto Gym)"),      DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_BROCK, TRAINER_NONE) },
    { COMPOUND_STRING("Colress"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_COLRESS_MAUVILLE, TRAINER_NONE) },
    { COMPOUND_STRING("Zinnia"),                 DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_ZINNIA, TRAINER_NONE) },
    { COMPOUND_STRING("N"),                      DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_N, TRAINER_NONE) },
    { COMPOUND_STRING("Ghetsis"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_GHETSIS, TRAINER_NONE) },
    { COMPOUND_STRING("Neo Plasma grunt"),       DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_PLASMA_GRUNT_M, TRAINER_NONE) },
    { COMPOUND_STRING("Rocket grunt"),           DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_ROCKET_GUARD, TRAINER_NONE) },
    { COMPOUND_STRING("Petrel (Rocket exec)"),   DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_PETREL, TRAINER_NONE) },
    { COMPOUND_STRING("Archie + Maxie"),         DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_ARCHIE_SOOTOPOLIS, TRAINER_MAXIE_SOOTOPOLIS) },
    { COMPOUND_STRING("Gabby & Ty"),             DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_GABBY_AND_TY_1, TRAINER_NONE) },
    { COMPOUND_STRING("Joey (Poochyena)"),       DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_JOEY, TRAINER_NONE) },
    { COMPOUND_STRING("Keccles (rival)"),        DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_KECCLES_1, TRAINER_NONE) },
    { COMPOUND_STRING("Mustard (mugshot)"),      DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MUSTARD, TRAINER_NONE) },
    { COMPOUND_STRING("Dave (Freed From Desire)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_DAVE, TRAINER_NONE) },
    { COMPOUND_STRING("Roxanne"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_ROXANNE_1, TRAINER_NONE) },
    { COMPOUND_STRING("Brawly"),                 DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_BRAWLY_1, TRAINER_NONE) },
    { COMPOUND_STRING("Wattson"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WATTSON_1, TRAINER_NONE) },
    { COMPOUND_STRING("Flannery"),               DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_FLANNERY_1, TRAINER_NONE) },
    { COMPOUND_STRING("Norman"),                 DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_NORMAN_1, TRAINER_NONE) },
    { COMPOUND_STRING("Winona"),                 DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WINONA_1, TRAINER_NONE) },
    { COMPOUND_STRING("Tate & Liza"),            DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_TATE_AND_LIZA_1, TRAINER_NONE) },
    { COMPOUND_STRING("Wallace"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_WALLACE_1, TRAINER_NONE) },
    { COMPOUND_STRING("Steven (champion)"),      DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_CHAMPION_STEVEN, TRAINER_NONE) },
    { COMPOUND_STRING("Mitch"),                  DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MITCH, TRAINER_NONE) },
    { COMPOUND_STRING("SickBlik (hotpot)"),      DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_SICKBLIK, TRAINER_NONE) },
    { COMPOUND_STRING("Mimi"),                   DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MIMI, TRAINER_NONE) },
    { COMPOUND_STRING("Burglar"),                DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_BURGLAR_1, TRAINER_NONE) },
    { COMPOUND_STRING("Shy Guy (Sunset Wilds)"),  DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_SHY_GUY_RED, TRAINER_NONE) },
    { COMPOUND_STRING("Shy Guy: green"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_SHY_GUY_GREEN, TRAINER_NONE) },
    { COMPOUND_STRING("Shy Guy: black"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_SHY_GUY_BLACK, TRAINER_NONE) },
    { COMPOUND_STRING("Shy Guy: Fly Guy"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_STADIUM_SHY_GUY_PINK, TRAINER_NONE) },
    { COMPOUND_STRING("Commander Boo"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_YI_COMMANDER_BOO, TRAINER_NONE) },
    { COMPOUND_STRING("Wario"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_YI_WARIO, TRAINER_NONE) },
    { COMPOUND_STRING("Agatha (Poke Tower)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_TOWER_AGATHA, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 1 Route 103"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_ROUTE_103_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 2 Rustboro"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_RUSTBORO_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 3 Route 110"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_ROUTE_110_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 4 Route 119"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_ROUTE_119_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 5 Lilycove"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_LILYCOVE_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival 6 Route 136"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MAY_ROUTE_136_MUDKIP, TRAINER_NONE) },
    { COMPOUND_STRING("Rival post-game"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_RIVAL_POSTGAME_TREECKO, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Sea (Swimmer)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_DECLAN, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Mountain (Hiker)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_SAWYER_1, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Nature (Bug Catcher)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_DAVIS, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Mystic (Hex Maniac)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_LEAH, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Chic (Beauty)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MELISSA, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Rock (Guitarist)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_KIRK, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Elite (Ace Trainer)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MARCEL, TRAINER_NONE) },
    { COMPOUND_STRING("Class: Kids (Youngster)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_CALVIN_1, TRAINER_NONE) },
    { COMPOUND_STRING("Class intro: Bug Catcher"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_DAVIS, TRAINER_NONE) },
    { COMPOUND_STRING("Class intro: Pokefan"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MIGUEL_1, TRAINER_NONE) },
    { COMPOUND_STRING("Class intro: Aroma Lady"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_DAISY, TRAINER_NONE) },
    { COMPOUND_STRING("Class intro: Parasol Lady"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_MADELINE_1, TRAINER_NONE) },
    { COMPOUND_STRING("Archie + Maxie (werkstraf)"), DebugAction_Util_BattleTest, BT_TRAINER(TRAINER_ARCHIE_SERVICE_1, TRAINER_MAXIE_SERVICE_1) },
    // Wilde legendaries: transitie + thema uit het echte event
    { COMPOUND_STRING("Zarude"),                 DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ZARUDE, 50) },
    { COMPOUND_STRING("Okidogi (Loyal 3)"),      DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_OKIDOGI, 65) },
    { COMPOUND_STRING("Suicune"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_SUICUNE, 50) },
    { COMPOUND_STRING("Raikou"),                 DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_RAIKOU, 50) },
    { COMPOUND_STRING("Entei"),                  DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ENTEI, 50) },
    { COMPOUND_STRING("Deoxys"),                 DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_DEOXYS_NORMAL, 50) },
    { COMPOUND_STRING("Mewtwo"),                 DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MEWTWO, 70) },
    { COMPOUND_STRING("Giratina"),               DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_GIRATINA_ALTERED, 70) },
    { COMPOUND_STRING("Darkrai"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_DARKRAI, 70) },
    { COMPOUND_STRING("Cresselia"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_CRESSELIA, 60) },
    { COMPOUND_STRING("Tapu Koko"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TAPU_KOKO, 70) },
    { COMPOUND_STRING("Tapu Lele"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TAPU_LELE, 70) },
    { COMPOUND_STRING("Tapu Bulu"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TAPU_BULU, 70) },
    { COMPOUND_STRING("Tapu Fini"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TAPU_FINI, 70) },
    { COMPOUND_STRING("Jirachi"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_JIRACHI, 70) },
    { COMPOUND_STRING("Victini"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_VICTINI, 70) },
    { COMPOUND_STRING("Shaymin"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_SHAYMIN_LAND, 70) },
    { COMPOUND_STRING("Heatran"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_HEATRAN, 70) },
    { COMPOUND_STRING("Genesect"),               DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_GENESECT, 70) },
    { COMPOUND_STRING("Mew"),                    DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MEW, 50) },
    { COMPOUND_STRING("Arceus"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ARCEUS_NORMAL, 80) },
    { COMPOUND_STRING("Dialga"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_DIALGA, 80) },
    { COMPOUND_STRING("Palkia"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_PALKIA, 80) },
    { COMPOUND_STRING("Celebi"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_CELEBI, 70) },
    { COMPOUND_STRING("Uxie"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_UXIE, 70) },
    { COMPOUND_STRING("Mesprit"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MESPRIT, 70) },
    { COMPOUND_STRING("Azelf"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_AZELF, 70) },
    { COMPOUND_STRING("Meloetta"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MELOETTA_ARIA, 70) },
    { COMPOUND_STRING("Zeraora"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ZERAORA, 70) },
    { COMPOUND_STRING("Zygarde"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ZYGARDE_50, 80) },
    { COMPOUND_STRING("Necrozma"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_NECROZMA, 80) },
    { COMPOUND_STRING("Eternatus"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ETERNATUS, 80) },
    { COMPOUND_STRING("Calyrex"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_CALYREX, 80) },
    { COMPOUND_STRING("Glastrier"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_GLASTRIER, 80) },
    { COMPOUND_STRING("Spectrier"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_SPECTRIER, 80) },
    { COMPOUND_STRING("Cobalion"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_COBALION, 70) },
    { COMPOUND_STRING("Keldeo"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_KELDEO_ORDINARY, 70) },
    { COMPOUND_STRING("Pecharunt"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_PECHARUNT, 70) },
    { COMPOUND_STRING("Xerneas"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_XERNEAS, 80) },
    { COMPOUND_STRING("Yveltal"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_YVELTAL, 80) },
    { COMPOUND_STRING("Zacian"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ZACIAN_HERO, 80) },
    { COMPOUND_STRING("Articuno (Galar)"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ARTICUNO_GALAR, 70) },
    { COMPOUND_STRING("Zapdos (Galar)"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_ZAPDOS_GALAR, 70) },
    { COMPOUND_STRING("Moltres (Galar)"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MOLTRES_GALAR, 70) },
    { COMPOUND_STRING("UB: Nihilego"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_NIHILEGO, 70) },
    { COMPOUND_STRING("Paradox: Great Tusk"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_GREAT_TUSK, 70) },
    { COMPOUND_STRING("Paradox: Iron Valiant"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_IRON_VALIANT, 70) },
    { COMPOUND_STRING("Koraidon"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_KORAIDON, 80) },
    { COMPOUND_STRING("Miraidon"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MIRAIDON, 80) },
    { COMPOUND_STRING("Terapagos"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TERAPAGOS_NORMAL, 80) },
    { COMPOUND_STRING("Wo-Chien (Ruin)"), DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_WO_CHIEN, 70) },
    { COMPOUND_STRING("Latias"), DebugAction_Util_BattleTest, BT_LATI(SPECIES_LATIAS) },
    { COMPOUND_STRING("Latios"), DebugAction_Util_BattleTest, BT_LATI(SPECIES_LATIOS) },
    { COMPOUND_STRING("Groudon"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_GROUDON, 70) },
    { COMPOUND_STRING("Kyogre"),                 DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_KYOGRE, 70) },
    { COMPOUND_STRING("Rayquaza"),               DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_RAYQUAZA, 70) },
    { COMPOUND_STRING("Lugia"),                  DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_LUGIA, 70) },
    { COMPOUND_STRING("Ho-Oh"),                  DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_HO_OH, 70) },
    { COMPOUND_STRING("Manaphy"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MANAPHY, 50) },
    { COMPOUND_STRING("Volcanion"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_VOLCANION, 70) },
    { COMPOUND_STRING("Hoopa"),                  DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_HOOPA_CONFINED, 70) },
    { COMPOUND_STRING("Hoopa Unbound"),          DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_HOOPA_UNBOUND, 70) },
    { COMPOUND_STRING("Tornadus"),               DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_TORNADUS_INCARNATE, 70) },
    { COMPOUND_STRING("Thundurus"),              DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_THUNDURUS_INCARNATE, 70) },
    { COMPOUND_STRING("Landorus"),               DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_LANDORUS_INCARNATE, 70) },
    { COMPOUND_STRING("Landorus-T"),             DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_LANDORUS_THERIAN, 70) },
    { COMPOUND_STRING("Munkidori (Loyal 3)"),    DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_MUNKIDORI, 65) },
    { COMPOUND_STRING("Fezandipiti (Loyal 3)"),  DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_FEZANDIPITI, 65) },
    { COMPOUND_STRING("Ogerpon"),                DebugAction_Util_BattleTest, BT_LEGEND(SPECIES_OGERPON_TEAL, 50) },
    { COMPOUND_STRING("Regirock"),               DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGIROCK) },
    { COMPOUND_STRING("Regice"),                 DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGICE) },
    { COMPOUND_STRING("Registeel"),              DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGISTEEL) },
    { COMPOUND_STRING("Regidrago"),              DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGIDRAGO) },
    { COMPOUND_STRING("Regieleki"),              DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGIELEKI) },
    { COMPOUND_STRING("Regigigas"),              DebugAction_Util_BattleTest, BT_REGI(SPECIES_REGIGIGAS) },
    // Wilde soorten met een eigen transitie (muziek = keuze bij WILD MUSIC in het optiemenu)
    { COMPOUND_STRING("Wild: Pikachu"),          DebugAction_Util_BattleTest, BT_WILD(SPECIES_PIKACHU) },
    { COMPOUND_STRING("Wild: Magikarp"),         DebugAction_Util_BattleTest, BT_WILD(SPECIES_MAGIKARP) },
    { COMPOUND_STRING("Wild: Psyduck"),          DebugAction_Util_BattleTest, BT_WILD(SPECIES_PSYDUCK) },
    { COMPOUND_STRING("Wild: Koffing"),          DebugAction_Util_BattleTest, BT_WILD(SPECIES_KOFFING) },
    { COMPOUND_STRING("Wild: Zangoose"),         DebugAction_Util_BattleTest, BT_WILD(SPECIES_ZANGOOSE) },
    { COMPOUND_STRING("Wild: Seviper"),          DebugAction_Util_BattleTest, BT_WILD(SPECIES_SEVIPER) },
    { NULL }
};

#undef BT_LEGEND
#undef BT_REGI
#undef BT_LATI
#undef BT_WILD
#undef BT_TRAINER

#include "data/debug_zone_warps.h" // Project Grounded: Utilities > "Zone warp…" (tools/grounded/debug_zone_warps.py)

static const struct DebugMenuOption sDebugMenu_Actions_Utilities[] =
{
    { COMPOUND_STRING("Zone warp…"),       DebugAction_OpenSubMenu, sDebugMenu_Actions_ZoneWarp },
    { COMPOUND_STRING("Warp to the Spire"), DebugAction_ExecuteScript, Debug_EventScript_SpireWarp },
    { COMPOUND_STRING("Warp to the Stadium"), DebugAction_ExecuteScript, Debug_EventScript_StadiumWarp },
    { COMPOUND_STRING("Fly to map…"),       DebugAction_Util_Fly },
    { COMPOUND_STRING("Warp to map warp…"), DebugAction_Util_Warp_Warp },
    { COMPOUND_STRING("Set weather…"),      DebugAction_Util_Weather },
    { COMPOUND_STRING("Font Test…"),        DebugAction_ExecuteScript, Debug_EventScript_FontTest },
    { COMPOUND_STRING("Time Functions…"),   DebugAction_OpenSubMenu, sDebugMenu_Actions_TimeMenu, },
    { COMPOUND_STRING("Watch credits…"),    DebugAction_Util_WatchCredits },
    { COMPOUND_STRING("Cheat start"),       DebugAction_Util_CheatStart },
    { COMPOUND_STRING("Berry Functions…"),  DebugAction_OpenSubMenu, sDebugMenu_Actions_BerryFunctions },
    { COMPOUND_STRING("EWRAM Counters…"),   DebugAction_ExecuteScript, Debug_EventScript_EWRAMCounters },
    { COMPOUND_STRING("Follower NPC…"),     DebugAction_OpenSubMenu, sDebugMenu_Actions_FollowerNPCMenu },
    { COMPOUND_STRING("Steven Multi"),      DebugAction_ExecuteScript, Debug_EventScript_Steven_Multi },
    { COMPOUND_STRING("Legendary battle…"), DebugAction_OpenSubMenu, sDebugMenu_Actions_Legendary },
    { COMPOUND_STRING("Battle test…"),      DebugAction_OpenSubMenu, sDebugMenu_Actions_BattleTest },
    { COMPOUND_STRING("Wild battle (map)"), DebugAction_ExecuteScript, Debug_EventScript_WildFromMap },
    { COMPOUND_STRING("Burglar: force"),    DebugAction_ExecuteScript, Debug_EventScript_BurglarForce },
    { COMPOUND_STRING("Force encounter…"),  DebugAction_Util_ForceEncounter },
    { COMPOUND_STRING("Force encounter: off"), DebugAction_ExecuteScript, Debug_EventScript_ForcedEncounterOff },
    { COMPOUND_STRING("The Spire"),         DebugAction_ExecuteScript, Debug_EventScript_SpirePrototype },
    { COMPOUND_STRING("Spire: reset run"),  DebugAction_ExecuteScript, Debug_EventScript_SpireResetRun },
    { COMPOUND_STRING("Stadium: singles"),  DebugAction_ExecuteScript, BattleStadium_EventScript_Singles },
    { COMPOUND_STRING("Stadium: doubles"),  DebugAction_ExecuteScript, BattleStadium_EventScript_Doubles },
    { COMPOUND_STRING("Stadium: unlock all"), DebugAction_ExecuteScript, Debug_EventScript_StadiumUnlockAll },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_PCBag_Fill[] =
{
    { COMPOUND_STRING("Fill PC Boxes Fast"),        DebugAction_PCBag_Fill_PCBoxes_Fast },
    { COMPOUND_STRING("Fill PC Boxes Slow (LAG!)"), DebugAction_PCBag_Fill_PCBoxes_Slow },
    { COMPOUND_STRING("Fill PC Items") ,            DebugAction_PCBag_Fill_PCItemStorage },
    { COMPOUND_STRING("Fill Pocket Items"),         DebugAction_PCBag_Fill_PocketItems },
    { COMPOUND_STRING("Fill Pocket Poké Balls"),    DebugAction_PCBag_Fill_PocketPokeBalls },
    { COMPOUND_STRING("Fill Pocket TMHM"),          DebugAction_PCBag_Fill_PocketTMHM },
    { COMPOUND_STRING("Fill Pocket Berries"),       DebugAction_PCBag_Fill_PocketBerries },
    { COMPOUND_STRING("Fill Pocket Key Items"),     DebugAction_PCBag_Fill_PocketKeyItems },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_PCBag[] =
{
    { COMPOUND_STRING("Access PC"),           DebugAction_ExecuteScript, EventScript_PC },
    { COMPOUND_STRING("Fill…"),               DebugAction_OpenSubMenu, sDebugMenu_Actions_PCBag_Fill },
    { COMPOUND_STRING("Clear Bag"),           DebugAction_PCBag_ClearBag },
    { COMPOUND_STRING("Clear Storage Boxes"), DebugAction_PCBag_ClearBoxes },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Party[] =
{
    { COMPOUND_STRING("Move Relearner"),     DebugAction_ExecuteScript, Common_EventScript_MoveRelearner },
    { COMPOUND_STRING("Hatch an Egg"),       DebugAction_ExecuteScript, Debug_HatchAnEgg },
    { COMPOUND_STRING("Heal party"),         DebugAction_Party_HealParty },
    { COMPOUND_STRING("Inflict Status1"),    DebugAction_ExecuteScript, Debug_EventScript_InflictStatus1 },
    { COMPOUND_STRING("Set Hidden Nature"),  DebugAction_ExecuteScript, Debug_EventScript_SetHiddenNature },
    { COMPOUND_STRING("Set Friendship"),     DebugAction_ExecuteScript, Debug_EventScript_SetFriendship },
    { COMPOUND_STRING("Set Ability"),        DebugAction_ExecuteScript, Debug_EventScript_SetAbility },
    { COMPOUND_STRING("Check EVs"),          DebugAction_ExecuteScript, Debug_EventScript_CheckEVs },
    { COMPOUND_STRING("Check IVs"),          DebugAction_ExecuteScript, Debug_EventScript_CheckIVs },
    { COMPOUND_STRING("Clear Party"),        DebugAction_Party_ClearParty },
    { COMPOUND_STRING("Set Party"),          DebugAction_Party_SetParty },
    { COMPOUND_STRING("Start Debug Battle"), DebugAction_Party_BattleSingle },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Give[] =
{
    { COMPOUND_STRING("Give item XYZ…"),    DebugAction_Give_Item },
    { COMPOUND_STRING("Pokémon (Basic)"),   DebugAction_Give_PokemonSimple },
    { COMPOUND_STRING("Pokémon (Complex)"), DebugAction_Give_PokemonComplex },
    { COMPOUND_STRING("Give Decoration…"),  DebugAction_Give_Decoration },
    { COMPOUND_STRING("Max Money"),         DebugAction_Give_MaxMoney },
    { COMPOUND_STRING("Max Coins"),         DebugAction_Give_MaxCoins },
    { COMPOUND_STRING("Max Battle Points"), DebugAction_Give_MaxBattlePoints },
    { COMPOUND_STRING("Daycare Egg"),       DebugAction_Give_DayCareEgg },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Player[] =
{
    { COMPOUND_STRING("Player name"),    DebugAction_Player_Name },
    { COMPOUND_STRING("Toggle gender"),  DebugAction_Player_Gender },
    { COMPOUND_STRING("New Trainer ID"), DebugAction_Player_Id },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Scripts[] =
{
    { COMPOUND_STRING("Script 1"), DebugAction_ExecuteScript, Debug_EventScript_Script_1 },
    { COMPOUND_STRING("Script 2"), DebugAction_ExecuteScript, Debug_EventScript_Script_2 },
    { COMPOUND_STRING("Script 3"), DebugAction_ExecuteScript, Debug_EventScript_Script_3 },
    { COMPOUND_STRING("Script 4"), DebugAction_ExecuteScript, Debug_EventScript_Script_4 },
    { COMPOUND_STRING("Script 5"), DebugAction_ExecuteScript, Debug_EventScript_Script_5 },
    { COMPOUND_STRING("Script 6"), DebugAction_ExecuteScript, Debug_EventScript_Script_6 },
    { COMPOUND_STRING("Script 7"), DebugAction_ExecuteScript, Debug_EventScript_Script_7 },
    { COMPOUND_STRING("Script 8"), DebugAction_ExecuteScript, Debug_EventScript_Script_8 },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Sound[] =
{
    { COMPOUND_STRING("SFX…"),   DebugAction_Sound_SE },
    { COMPOUND_STRING("Music…"), DebugAction_Sound_MUS },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_ROMInfo2[] =
{
    { COMPOUND_STRING("Save Block space"),  DebugAction_ExecuteScript, Debug_CheckSaveBlock },
    { COMPOUND_STRING("ROM space"),         DebugAction_ExecuteScript, Debug_CheckROMSpace },
    { COMPOUND_STRING("Expansion Version"), DebugAction_ExecuteScript, Debug_ShowExpansionVersion },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_Flags[] =
{
    [DEBUG_FLAGVAR_MENU_ITEM_FLAGS]                = { COMPOUND_STRING("Set Flag XYZ…"),                     DebugAction_FlagsVars_Flags },
    [DEBUG_FLAGVAR_MENU_ITEM_VARS]                 = { COMPOUND_STRING("Set Var XYZ…"),                      DebugAction_FlagsVars_Vars },
    [DEBUG_FLAGVAR_MENU_ITEM_DEXFLAGS_ALL]         = { COMPOUND_STRING("Pokédex Flags All"),                 DebugAction_FlagsVars_PokedexFlags_All },
    [DEBUG_FLAGVAR_MENU_ITEM_DEXFLAGS_RESET]       = { COMPOUND_STRING("Pokédex Flags Reset"),               DebugAction_FlagsVars_PokedexFlags_Reset },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKEDEX]       = { COMPOUND_STRING("Toggle {STR_VAR_1}Pokédex"),         DebugAction_ToggleFlag, DebugAction_FlagsVars_SwitchDex },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_NATDEX]        = { COMPOUND_STRING("Toggle {STR_VAR_1}National Dex"),    DebugAction_ToggleFlag, DebugAction_FlagsVars_SwitchNatDex },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKENAV]       = { COMPOUND_STRING("Toggle {STR_VAR_1}PokéNav"),         DebugAction_ToggleFlag, DebugAction_FlagsVars_SwitchPokeNav },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_MATCH_CALL]    = { COMPOUND_STRING("Toggle {STR_VAR_1}Match Call"),      DebugAction_ToggleFlag, DebugAction_FlagsVars_SwitchMatchCall },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_RUN_SHOES]     = { COMPOUND_STRING("Toggle {STR_VAR_1}Running Shoes"),   DebugAction_ToggleFlag, DebugAction_FlagsVars_RunningShoes },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_LOCATIONS]     = { COMPOUND_STRING("Toggle {STR_VAR_1}Fly Flags"),       DebugAction_ToggleFlag, DebugAction_FlagsVars_ToggleFlyFlags },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BADGES_ALL]    = { COMPOUND_STRING("Toggle {STR_VAR_1}All badges"),      DebugAction_ToggleFlag, DebugAction_FlagsVars_ToggleBadgeFlags },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_GAME_CLEAR]    = { COMPOUND_STRING("Toggle {STR_VAR_1}Game clear"),      DebugAction_ToggleFlag, DebugAction_FlagsVars_ToggleGameClear },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_FRONTIER_PASS] = { COMPOUND_STRING("Toggle {STR_VAR_1}Frontier Pass"),   DebugAction_ToggleFlag, DebugAction_FlagsVars_ToggleFrontierPass },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_COLLISION]     = { COMPOUND_STRING("Toggle {STR_VAR_1}Collision OFF"),   DebugAction_ToggleFlag, DebugAction_FlagsVars_CollisionOnOff },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_ENCOUNTER]     = { COMPOUND_STRING("Toggle {STR_VAR_1}Encounter OFF"),   DebugAction_ToggleFlag, DebugAction_FlagsVars_EncounterOnOff },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_TRAINER_SEE]   = { COMPOUND_STRING("Toggle {STR_VAR_1}Trainer See OFF"), DebugAction_ToggleFlag, DebugAction_FlagsVars_TrainerSeeOnOff },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_CATCHING]      = { COMPOUND_STRING("Toggle {STR_VAR_1}Catching OFF"),    DebugAction_ToggleFlag, DebugAction_FlagsVars_CatchingOnOff },
    [DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BAG_USE]       = { COMPOUND_STRING("Toggle {STR_VAR_1}Bag Use OFF"),     DebugAction_ToggleFlag, DebugAction_FlagsVars_BagUseOnOff },
    { NULL }
};

static const u8 *const sDebugMenu_Actions_BagUse_Options[] =
{
    COMPOUND_STRING("No Bag: {STR_VAR_1}Inactive"),
    COMPOUND_STRING("No Bag: {STR_VAR_1}VS Trainers"),
    COMPOUND_STRING("No Bag: {STR_VAR_1}Active"),
};

static const struct DebugMenuOption sDebugMenu_Actions_Main[] =
{
    { COMPOUND_STRING("Utilities…"),    DebugAction_OpenSubMenu, sDebugMenu_Actions_Utilities, },
    { COMPOUND_STRING("PC/Bag…"),       DebugAction_OpenSubMenu, sDebugMenu_Actions_PCBag, },
    { COMPOUND_STRING("Party…"),        DebugAction_OpenSubMenu, sDebugMenu_Actions_Party, },
    { COMPOUND_STRING("Give X…"),       DebugAction_OpenSubMenu, sDebugMenu_Actions_Give, },
    { COMPOUND_STRING("Player…"),       DebugAction_OpenSubMenu, sDebugMenu_Actions_Player, },
    { COMPOUND_STRING("Scripts…"),      DebugAction_OpenSubMenu, sDebugMenu_Actions_Scripts, },
    { COMPOUND_STRING("Flags & Vars…"), DebugAction_OpenSubMenuFlagsVars, sDebugMenu_Actions_Flags, },
    { COMPOUND_STRING("Sound…"),        DebugAction_OpenSubMenu, sDebugMenu_Actions_Sound, },
    { COMPOUND_STRING("ROM Info…"),     DebugAction_OpenSubMenu, sDebugMenu_Actions_ROMInfo2, },
    { COMPOUND_STRING("Cancel"),        DebugAction_Cancel, },
    { NULL }
};

// *******************************
// Windows
static const struct WindowTemplate sDebugMenuWindowTemplateMain =
{
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = DEBUG_MENU_WIDTH_MAIN,
    .height = 2 * DEBUG_MENU_HEIGHT_MAIN,
    .paletteNum = 15,
    .baseBlock = 1,
};

static const struct WindowTemplate sDebugMenuWindowTemplateExtra =
{
    .bg = 0,
    .tilemapLeft = 30 - DEBUG_MENU_WIDTH_EXTRA - 1,
    .tilemapTop = 1,
    .width = DEBUG_MENU_WIDTH_EXTRA,
    .height = 2 * DEBUG_MENU_HEIGHT_EXTRA,
    .paletteNum = 15,
    .baseBlock = 1,
};

static const struct WindowTemplate sDebugMenuWindowTemplateWeather =
{
    .bg = 0,
    .tilemapLeft = 30 - DEBUG_MENU_WIDTH_WEATHER - 1,
    .tilemapTop = 1,
    .width = DEBUG_MENU_WIDTH_WEATHER,
    .height = 2 * DEBUG_MENU_HEIGHT_WEATHER,
    .paletteNum = 15,
    .baseBlock = 1,
};

static const struct WindowTemplate sDebugMenuWindowTemplateSound =
{
    .bg = 0,
    .tilemapLeft = 30 - DEBUG_MENU_WIDTH_SOUND - 1,
    .tilemapTop = 1,
    .width = DEBUG_MENU_WIDTH_SOUND,
    .height = DEBUG_MENU_HEIGHT_SOUND,
    .paletteNum = 15,
    .baseBlock = 1,
};

static bool32 Debug_SaveCallbackMenu(struct DebugMenuOption *callbackItems);

// *******************************
// Functions universal
void Debug_ShowMainMenu(void)
{
    sDebugMenuListData = AllocZeroed(sizeof(*sDebugMenuListData));
    sDebugMenuListData->listId = 0;
    Debug_ShowMenu(DebugTask_HandleMenuInput_General, sDebugMenu_Actions_Main);
}

#define tMenuTaskId          data[0]
#define tWindowId            data[1]
#define tSubWindowId         data[2]
#define tInput               data[3]
#define tDigit               data[4]

static bool32 Debug_SaveCallbackMenu(struct DebugMenuOption *callbackItems)
{
    bool32 success = FALSE;
    for (u32 i = 0; i < DEBUG_MAX_SUB_MENU_LEVELS; i++)
    {
        if (sDebugMenuListData->subMenuItems[i] == NULL)
        {
            sDebugMenuListData->subMenuItems[i] = callbackItems;
            success = TRUE;
            break;
        }
    }
    return success;
}

static u32 Debug_RemoveCallbackMenu(void)
{
    u32 freeCallbackLevel = 0;
    for (u32 i = DEBUG_MAX_SUB_MENU_LEVELS; i > 0; i--)
    {
        if (sDebugMenuListData->subMenuItems[i - 1] != NULL)
        {
            sDebugMenuListData->subMenuItems[i - 1] = NULL;
            freeCallbackLevel = i - 1;
            break;
        }
    }
    return freeCallbackLevel;
}

static const struct DebugMenuOption *Debug_GetCurrentCallbackMenu(void)
{
    const struct DebugMenuOption *callbackItems = NULL;
    for (u32 i = DEBUG_MAX_SUB_MENU_LEVELS; i > 0; i--)
    {
        if (sDebugMenuListData->subMenuItems[i - 1] != NULL)
        {
            callbackItems = sDebugMenuListData->subMenuItems[i - 1];
            break;
        }
    }
    return callbackItems;
}

static bool32 IsSubMenuAction(const void *action)
{
    return action == DebugAction_OpenSubMenu
        || action == DebugAction_OpenSubMenuFlagsVars
        || action == DebugAction_OpenSubMenuFakeRTC
        || action == DebugAction_OpenSubMenuCreateFollowerNPC;
}

static void Debug_ShowMenu(DebugFunc HandleInput, const struct DebugMenuOption *items)
{
    struct ListMenuTemplate menuTemplate = {0};
    u8 windowId;
    u8 menuTaskId;
    u8 inputTaskId;

    if (items != NULL)
        Debug_SaveCallbackMenu((struct DebugMenuOption *)items);
    else
        items = Debug_GetCurrentCallbackMenu();

    // create window
    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateMain);
    DrawStdWindowFrame(windowId, FALSE);

    u32 totalItems = 0;

    if (sDebugMenuListData->listId == 1)
    {
        totalItems = Debug_GenerateListMenuNames();
    }
    else
    {
        for (u32 i = 0; items[i].text != NULL && i < DEBUG_MAX_MENU_ITEMS; i++)
        {
            sDebugMenuListData->listItems[i].id = i;
            StringExpandPlaceholders(gStringVar4, items[i].text);
            if (IsSubMenuAction(items[i].action))
                StringAppend(gStringVar4, sDebugText_Arrow);
            StringCopy(&sDebugMenuListData->itemNames[i][0], gStringVar4);
            sDebugMenuListData->listItems[i].name = &sDebugMenuListData->itemNames[i][0];
            totalItems++;
        }
    }

    // create list menu
    menuTemplate.items = sDebugMenuListData->listItems;
    menuTemplate.moveCursorFunc = ListMenuDefaultCursorMoveFunc;
    menuTemplate.totalItems = totalItems;
    menuTemplate.maxShowed = DEBUG_MENU_HEIGHT_MAIN;
    menuTemplate.windowId = windowId;
    menuTemplate.header_X = 0;
    menuTemplate.item_X = 8;
    menuTemplate.cursor_X = 0;
    menuTemplate.upText_Y = 1;
    menuTemplate.cursorPal = 2;
    menuTemplate.fillValue = 1;
    menuTemplate.cursorShadowPal = 3;
    menuTemplate.lettersSpacing = 1;
    menuTemplate.itemVerticalPadding = 0;
    menuTemplate.scrollMultiple = LIST_MULTIPLE_SCROLL_DPAD; // Project Grounded: links/rechts = een pagina terug/verder
    menuTemplate.fontId = DEBUG_MENU_FONT;
    menuTemplate.cursorKind = 0;
    menuTaskId = ListMenuInit(&menuTemplate, 0, 0);

    // create input handler task
    inputTaskId = CreateTask(HandleInput, 3);
    gTasks[inputTaskId].tMenuTaskId = menuTaskId;
    gTasks[inputTaskId].tWindowId = windowId;
    gTasks[inputTaskId].tSubWindowId = 0;

    Debug_RefreshListMenu(inputTaskId);

    // draw everything
    CopyWindowToVram(windowId, COPYWIN_FULL);
}

static void Debug_DestroyMenu(u8 taskId)
{
    DestroyListMenuTask(gTasks[taskId].tMenuTaskId, NULL, NULL);
    RemoveWindow(gTasks[taskId].tWindowId);
    DestroyTask(taskId);
}

static void Debug_DestroyMenu_Full(u8 taskId)
{
    if (gTasks[taskId].tSubWindowId != 0)
    {
        ClearStdWindowAndFrame(gTasks[taskId].tSubWindowId, FALSE);
        DebugAction_DestroyExtraWindow(taskId);
    }
    DestroyListMenuTask(gTasks[taskId].tMenuTaskId, NULL, NULL);
    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);
    DestroyTask(taskId);
    UnfreezeObjectEvents();
    Free(sDebugMenuListData);
}

static void Debug_DestroyMenu_Full_Script(u8 taskId, const u8 *script)
{
    Debug_DestroyMenu_Full(taskId);
    LockPlayerFieldControls();
    FreezeObjectEvents();
    ScriptContext_SetupScript(script);
}

static void Debug_HandleInput_Numeric(u8 taskId, s32 min, s32 max, u32 digits)
{
    if (JOY_NEW(DPAD_UP))
    {
        gTasks[taskId].tInput += sPowersOfTen[gTasks[taskId].tDigit];
        if (gTasks[taskId].tInput > max)
            gTasks[taskId].tInput = max;
    }
    if (JOY_NEW(DPAD_DOWN))
    {
        gTasks[taskId].tInput -= sPowersOfTen[gTasks[taskId].tDigit];
        if (gTasks[taskId].tInput < min)
            gTasks[taskId].tInput = min;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (gTasks[taskId].tDigit > 0)
            gTasks[taskId].tDigit -= 1;
    }
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (gTasks[taskId].tDigit < digits - 1)
            gTasks[taskId].tDigit += 1;
    }
}

static void DebugAction_Cancel(u8 taskId)
{
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_DestroyExtraWindow(u8 taskId)
{
    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    ClearStdWindowAndFrame(gTasks[taskId].tSubWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tSubWindowId);

    DestroyListMenuTask(gTasks[taskId].tMenuTaskId, NULL, NULL);
    DestroyTask(taskId);
    ScriptContext_Enable();
    UnfreezeObjectEvents();
}

static u8 DebugNativeStep_CreateDebugWindow(void)
{
    u8 windowId;

    LockPlayerFieldControls();
    FreezeObjectEvents();
    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);
    CopyWindowToVram(windowId, COPYWIN_FULL);

    return windowId;
}

static void DebugNativeStep_CloseDebugWindow(u8 taskId)
{
    ClearStdWindowAndFrame(gTasks[taskId].tSubWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tSubWindowId);
    DestroyTask(taskId);
    UnfreezeObjectEvents();
    UnlockPlayerFieldControls();
}

static const u16 sLocationFlags[] =
{
    FLAG_VISITED_LITTLEROOT_TOWN,
    FLAG_VISITED_OLDALE_TOWN,
    FLAG_VISITED_DEWFORD_TOWN,
    FLAG_VISITED_LAVARIDGE_TOWN,
    FLAG_VISITED_FALLARBOR_TOWN,
    FLAG_VISITED_VERDANTURF_TOWN,
    FLAG_VISITED_PACIFIDLOG_TOWN,
    FLAG_VISITED_PETALBURG_CITY,
    FLAG_VISITED_SLATEPORT_CITY,
    FLAG_VISITED_MAUVILLE_CITY,
    FLAG_VISITED_RUSTBORO_CITY,
    FLAG_VISITED_FORTREE_CITY,
    FLAG_VISITED_LILYCOVE_CITY,
    FLAG_VISITED_MOSSDEEP_CITY,
    FLAG_VISITED_SOOTOPOLIS_CITY,
    FLAG_VISITED_EVER_GRANDE_CITY,
    FLAG_VISITED_ASHFROST_TOWN, // Project Grounded
    FLAG_LANDMARK_POKEMON_LEAGUE,
    FLAG_LANDMARK_BATTLE_FRONTIER,
};

static u8 Debug_CheckToggleFlags(u8 id)
{
    bool32 result = FALSE;

    switch (id)
    {
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKEDEX:
            result = FlagGet(FLAG_SYS_POKEDEX_GET);
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_NATDEX:
            result = IsNationalPokedexEnabled();
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_POKENAV:
            result = FlagGet(FLAG_SYS_POKENAV_GET);
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_MATCH_CALL:
            result = FlagGet(FLAG_ADDED_MATCH_CALL_TO_POKENAV) && FlagGet(FLAG_HAS_MATCH_CALL);
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_RUN_SHOES:
            result = FlagGet(FLAG_SYS_B_DASH);
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_LOCATIONS:
            result = TRUE;
            for (u32 i = 0; i < ARRAY_COUNT(sLocationFlags); i++)
            {
                if (!FlagGet(sLocationFlags[i]))
                {
                    result = FALSE;
                    break;
                }
            }
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BADGES_ALL:
            result = TRUE;
            for (u32 i = 0; i < ARRAY_COUNT(gBadgeFlags); i++)
            {
                if (!FlagGet(gBadgeFlags[i]))
                {
                    result = FALSE;
                    break;
                }
            }
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_GAME_CLEAR:
            result = FlagGet(FLAG_SYS_GAME_CLEAR);
            break;
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_FRONTIER_PASS:
            result = FlagGet(FLAG_SYS_FRONTIER_PASS);
            break;
    #if OW_FLAG_NO_COLLISION != 0
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_COLLISION:
            result = FlagGet(OW_FLAG_NO_COLLISION);
            break;
    #endif
    #if OW_FLAG_NO_ENCOUNTER != 0
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_ENCOUNTER:
            result = FlagGet(OW_FLAG_NO_ENCOUNTER);
            break;
    #endif
    #if OW_FLAG_NO_TRAINER_SEE != 0
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_TRAINER_SEE:
            result = FlagGet(OW_FLAG_NO_TRAINER_SEE);
            break;
    #endif
    #if B_FLAG_NO_CATCHING != 0
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_CATCHING:
            result = FlagGet(B_FLAG_NO_CATCHING);
            break;
    #endif
        case DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BAG_USE:
            result = VarGet(B_VAR_NO_BAG_USE);
            break;
        default:
            result = 0xFF;
            break;
    }

    return result;
}

static u8 Debug_GenerateListMenuNames(void)
{
    const u8 sColor_Red[] = _("{COLOR RED}");
    const u8 sColor_Green[] = _("{COLOR GREEN}");
    u32 i, flagResult = 0;
    u8 const *name = NULL;

    u8 totalItems = 0;
    if (sDebugMenuListData->listId == 1)
        // Failsafe to prevent memory corruption
        totalItems = min(ARRAY_COUNT(sDebugMenu_Actions_Flags) - 1, DEBUG_MAX_MENU_ITEMS);

    // Copy item names for all entries but the last (which is Cancel)
    for (i = 0; i < totalItems; i++)
    {
        if (sDebugMenuListData->listId == 1)
        {
            flagResult = Debug_CheckToggleFlags(i);
            if (i == DEBUG_FLAGVAR_MENU_ITEM_TOGGLE_BAG_USE)
                name = sDebugMenu_Actions_BagUse_Options[flagResult];
            else
                name = sDebugMenu_Actions_Flags[i].text;
        }

        if (flagResult == 0xFF)
        {
            StringCopy(&sDebugMenuListData->itemNames[i][0], name);
        }
        else if (flagResult)
        {
            StringCopy(gStringVar1, sColor_Green);
            StringExpandPlaceholders(gStringVar4, name);
            StringCopy(&sDebugMenuListData->itemNames[i][0], gStringVar4);
        }
        else
        {
            StringCopy(gStringVar1, sColor_Red);
            StringExpandPlaceholders(gStringVar4, name);
            StringCopy(&sDebugMenuListData->itemNames[i][0], gStringVar4);
        }

        sDebugMenuListData->listItems[i].name = &sDebugMenuListData->itemNames[i][0];
        sDebugMenuListData->listItems[i].id = i;
    }
    return totalItems;
}

static void Debug_RefreshListMenu(u8 taskId)
{
    u8 totalItems = Debug_GenerateListMenuNames();

    // Set list menu data
    gMultiuseListMenuTemplate.items = sDebugMenuListData->listItems;
    gMultiuseListMenuTemplate.totalItems = totalItems;
    gMultiuseListMenuTemplate.maxShowed = DEBUG_MENU_HEIGHT_MAIN;
    gMultiuseListMenuTemplate.windowId = gTasks[taskId].tWindowId;
    gMultiuseListMenuTemplate.header_X = 0;
    gMultiuseListMenuTemplate.item_X = 8;
    gMultiuseListMenuTemplate.cursor_X = 0;
    gMultiuseListMenuTemplate.upText_Y = 1;
    gMultiuseListMenuTemplate.cursorPal = 2;
    gMultiuseListMenuTemplate.fillValue = 1;
    gMultiuseListMenuTemplate.cursorShadowPal = 3;
    gMultiuseListMenuTemplate.lettersSpacing = 1;
    gMultiuseListMenuTemplate.itemVerticalPadding = 0;
    gMultiuseListMenuTemplate.scrollMultiple = LIST_MULTIPLE_SCROLL_DPAD; // Project Grounded: links/rechts = een pagina terug/verder
    gMultiuseListMenuTemplate.fontId = 1;
    gMultiuseListMenuTemplate.cursorKind = 0;
}

static void DebugTask_HandleMenuInput_General(u8 taskId)
{
    const struct DebugMenuOption *options = Debug_GetCurrentCallbackMenu();
    u32 input = ListMenu_ProcessInput(gTasks[taskId].tMenuTaskId);
    struct DebugMenuOption option = options[input];

    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        if (option.action != NULL)
        {
            if (IsSubMenuAction(option.action))
            {
                ((DebugSubmenuFunc)option.action)(taskId, option.actionParams);
            }
            else if (option.action == DebugAction_ExecuteScript)
            {
                Debug_DestroyMenu_Full_Script(taskId, (const u8 *)option.actionParams);
            }
            else if (option.action == DebugAction_Util_BattleTest)
            {
                DebugAction_Util_BattleTest(taskId, (const struct BattleTest *)option.actionParams);
            }
            else if (option.action == DebugAction_Util_ZoneWarp)
            {
                DebugAction_Util_ZoneWarp(taskId, option.actionParams);
            }
            else if (option.action == DebugAction_ToggleFlag)
            {
                ((DebugFunc)option.actionParams)(taskId);
                DebugAction_ToggleFlag(taskId);
            }
            else
            {
                ((DebugFunc)option.action)(taskId);
            }
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        if (Debug_GetCurrentCallbackMenu() != NULL && Debug_RemoveCallbackMenu() != 0)
        {
            Debug_DestroyMenu(taskId);
            if (sDebugMenuListData->listId != 0)
                sDebugMenuListData->listId = 0;
            Debug_ShowMenu(DebugTask_HandleMenuInput_General, NULL);
        }
        else
        {
            Debug_DestroyMenu_Full(taskId);
            ScriptContext_Enable();
        }
    }
}

static void DebugAction_OpenSubMenuFlagsVars(u8 taskId, const struct DebugMenuOption *items)
{
    Debug_DestroyMenu(taskId);
    sDebugMenuListData->listId = 1;
    Debug_ShowMenu(DebugTask_HandleMenuInput_General, items);
}

static void DebugAction_OpenSubMenu(u8 taskId, const struct DebugMenuOption *items)
{
    Debug_DestroyMenu(taskId);
    sDebugMenuListData->listId = 0;
    Debug_ShowMenu(DebugTask_HandleMenuInput_General, items);
}

static void DebugAction_OpenSubMenuFakeRTC(u8 taskId, const struct DebugMenuOption *items)
{
    if (!OW_USE_FAKE_RTC)
    {
        Debug_DestroyMenu_Full_Script(taskId, Debug_EventScript_FakeRTCNotEnabled);
    }
    else
    {
        Debug_DestroyMenu(taskId);
        Debug_ShowMenu(DebugTask_HandleMenuInput_General, items);
    }
}

static void DebugAction_ExecuteScript(u8 taskId, const u8 *script)
{
    Debug_DestroyMenu_Full_Script(taskId, script);
}

static void DebugAction_ToggleFlag(u8 taskId)
{
    Debug_GenerateListMenuNames();
    RedrawListMenu(gTasks[taskId].tMenuTaskId);
}

static void DebugAction_OpenSubMenuCreateFollowerNPC(u8 taskId, const struct DebugMenuOption *items)
{
    if (FNPC_ENABLE_NPC_FOLLOWERS)
    {
        Debug_DestroyMenu(taskId);
        Debug_ShowMenu(DebugTask_HandleMenuInput_General, items);
    }
    else
    {
        Debug_DestroyMenu_Full_Script(taskId, Debug_Follower_NPC_Not_Enabled);
    }
}

// *******************************
// Actions Utilities

// Project Grounded: warp naar warp 0 van een kaart uit "Zone warp…" (zonder warps: het midden van de kaart)
static void DebugAction_Util_ZoneWarp(u8 taskId, const void *mapId)
{
    u16 map = (uintptr_t)mapId;
    SetWarpDestinationToMapWarp(map >> 8, map & 0xFF, 0);
    DoWarp();
    ResetInitialPlayerAvatarState();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_Util_Fly(u8 taskId)
{
    Debug_DestroyMenu_Full(taskId);
    SetMainCallback2(CB2_OpenFlyMap);
}

#define tMapGroup  data[5]
#define tMapNum    data[6]
#define tWarp      data[7]

#define LAST_MAP_GROUP (MAP_GROUPS_COUNT - 1)

static void DebugAction_Util_Warp_Warp(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, 3);
    ConvertIntToDecimalStringN(gStringVar2, LAST_MAP_GROUP, STR_CONV_MODE_LEADING_ZEROS, 3);
    StringExpandPlaceholders(gStringVar1, sDebugText_Util_WarpToMap_SelMax);
    StringCopy(gStringVar3, gText_DigitIndicator[0]);
    StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectMapGroup);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

    gTasks[taskId].func = DebugAction_Util_Warp_SelectMapGroup;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 0;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tMapGroup = 0;
    gTasks[taskId].tMapNum = 0;
    gTasks[taskId].tWarp = 0;
}

static void DebugAction_Util_Warp_SelectMapGroup(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, LAST_MAP_GROUP, 3);

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, 3);
        ConvertIntToDecimalStringN(gStringVar2, LAST_MAP_GROUP, STR_CONV_MODE_LEADING_ZEROS, 3);
        StringExpandPlaceholders(gStringVar1, sDebugText_Util_WarpToMap_SelMax);
        StringCopy(gStringVar3, gText_DigitIndicator[gTasks[taskId].tDigit]);
        StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectMapGroup);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        gTasks[taskId].tMapGroup = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, (MAP_GROUP_COUNT[gTasks[taskId].tMapGroup] - 1 >= 100) ? 3 : 2);
        ConvertIntToDecimalStringN(gStringVar2, MAP_GROUP_COUNT[gTasks[taskId].tMapGroup] - 1, STR_CONV_MODE_LEADING_ZEROS, (MAP_GROUP_COUNT[gTasks[taskId].tMapGroup] - 1 >= 100) ? 3 : 2);
        StringExpandPlaceholders(gStringVar1, sDebugText_Util_WarpToMap_SelMax);
        GetMapName(gStringVar2, Overworld_GetMapHeaderByGroupAndId(gTasks[taskId].tMapGroup, gTasks[taskId].tInput)->regionMapSectionId, 0);
        StringCopy(gStringVar3, gText_DigitIndicator[gTasks[taskId].tDigit]);
        StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectMap);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

        gTasks[taskId].func = DebugAction_Util_Warp_SelectMap;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Util_Warp_SelectMap(u8 taskId)
{
    u8 max_value = MAP_GROUP_COUNT[gTasks[taskId].tMapGroup]; //maps in the selected map group

    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, max_value - 1, 3);

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, (max_value >= 100) ? 3 : 2);
        ConvertIntToDecimalStringN(gStringVar2, MAP_GROUP_COUNT[gTasks[taskId].tMapGroup] - 1, STR_CONV_MODE_LEADING_ZEROS, (max_value >= 100) ? 3 : 2);
        StringExpandPlaceholders(gStringVar1, sDebugText_Util_WarpToMap_SelMax);
        GetMapName(gStringVar2, Overworld_GetMapHeaderByGroupAndId(gTasks[taskId].tMapGroup, gTasks[taskId].tInput)->regionMapSectionId, 0);
        StringCopy(gStringVar3, gText_DigitIndicator[gTasks[taskId].tDigit]);
        StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectMap);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        gTasks[taskId].tMapNum = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;

        StringCopy(gStringVar3, gText_DigitIndicator[gTasks[taskId].tDigit]);
        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, 3);
        StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectWarp);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
        gTasks[taskId].func = DebugAction_Util_Warp_SelectWarp;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Util_Warp_SelectWarp(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        if (JOY_NEW(DPAD_UP))
        {
            gTasks[taskId].tInput += sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput > 10)
                gTasks[taskId].tInput = 10;
        }
        if (JOY_NEW(DPAD_DOWN))
        {
            gTasks[taskId].tInput -= sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput < 0)
                gTasks[taskId].tInput = 0;
        }

        StringCopy(gStringVar3, gText_DigitIndicator[gTasks[taskId].tDigit]);
        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, 3);
        StringExpandPlaceholders(gStringVar4, sDebugText_Util_WarpToMap_SelectWarp);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        gTasks[taskId].tWarp = gTasks[taskId].tInput;
        //If there's no warp with the number available, warp to the center of the map.
        SetWarpDestinationToMapWarp(gTasks[taskId].tMapGroup, gTasks[taskId].tMapNum, gTasks[taskId].tWarp);
        DoWarp();
        ResetInitialPlayerAvatarState();
        DebugAction_DestroyExtraWindow(taskId);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

#undef tMapGroup
#undef tMapNum
#undef tWarp

void CheckSaveBlock1Size(struct ScriptContext *ctx)
{
    u32 currSb1Size = sizeof(struct SaveBlock1);
    u32 maxSb1Size = SECTOR_DATA_SIZE * (SECTOR_ID_SAVEBLOCK1_END - SECTOR_ID_SAVEBLOCK1_START + 1);
    ConvertIntToDecimalStringN(gStringVar1, currSb1Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar2, maxSb1Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar3, maxSb1Size - currSb1Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar4, 1, STR_CONV_MODE_LEFT_ALIGN, 6);
}

void CheckSaveBlock2Size(struct ScriptContext *ctx)
{
    u32 currSb2Size = (sizeof(struct SaveBlock2));
    u32 maxSb2Size = SECTOR_DATA_SIZE;
    ConvertIntToDecimalStringN(gStringVar1, currSb2Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar2, maxSb2Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar3, maxSb2Size - currSb2Size, STR_CONV_MODE_LEFT_ALIGN, 6);
}

void CheckSaveBlock3Size(struct ScriptContext *ctx)
{
    u32 currSb3Size = (sizeof(struct SaveBlock3));
    u32 maxSb3Size = SAVE_BLOCK_3_CHUNK_SIZE * NUM_SECTORS_PER_SLOT;
    ConvertIntToDecimalStringN(gStringVar1, currSb3Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar2, maxSb3Size, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar3, maxSb3Size - currSb3Size, STR_CONV_MODE_LEFT_ALIGN, 6);
}

void CheckPokemonStorageSize(struct ScriptContext *ctx)
{
    u32 currPkmnStorageSize = sizeof(struct PokemonStorage);
    u32 maxPkmnStorageSize = SECTOR_DATA_SIZE * (SECTOR_ID_PKMN_STORAGE_END - SECTOR_ID_PKMN_STORAGE_START + 1);
    ConvertIntToDecimalStringN(gStringVar1, currPkmnStorageSize, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar2, maxPkmnStorageSize, STR_CONV_MODE_LEFT_ALIGN, 6);
    ConvertIntToDecimalStringN(gStringVar3, maxPkmnStorageSize - currPkmnStorageSize, STR_CONV_MODE_LEFT_ALIGN, 6);
}

enum RoundMode
{
    ROUND_CEILING,
    ROUND_NEAREST,
    ROUND_FLOOR,
};

static u8 *ConvertQ22_10ToDecimalString(u8 *string, u32 q22_10, u32 decimalDigits, enum RoundMode roundMode)
{
    string = ConvertIntToDecimalStringN(string, q22_10 >> 10, STR_CONV_MODE_LEFT_ALIGN, 10);

    if (decimalDigits == 0)
        return string;

    *string++ = CHAR_PERIOD;

    q22_10 &= (1 << 10) - 1;
    while (decimalDigits-- > 1)
    {
        q22_10 *= 10;
        *string++ = CHAR_0 + (q22_10 >> 10);
        q22_10 &= (1 << 10) - 1;
    }

    q22_10 *= 10;
    switch (roundMode)
    {
    case ROUND_CEILING: q22_10 += (1 << 10) - 1; break;
    case ROUND_NEAREST: q22_10 += 1 << (10 - 1); break;
    case ROUND_FLOOR:                            break;
    }
    *string++ = CHAR_0 + (q22_10 >> 10);

    *string++ = EOS;

    return string;
}

void CheckROMSize(struct ScriptContext *ctx)
{
    extern u8 __rom_end[];
    u32 currROMSizeB = __rom_end - (const u8 *)ROM_START;
    u32 currROMSizeKB = (currROMSizeB + 1023) / 1024;
    u32 currROMFreeKB = ((const u8 *)ROM_END - __rom_end) / 1024;
    ConvertQ22_10ToDecimalString(gStringVar1, currROMSizeKB, 2, ROUND_CEILING);
    ConvertQ22_10ToDecimalString(gStringVar2, currROMFreeKB, 2, ROUND_FLOOR);
}

static void DebugAction_Util_Weather(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateWeather);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    //Display initial ID
    StringCopy(gStringVar2, gText_DigitIndicator[0]);
    ConvertIntToDecimalStringN(gStringVar3, 1, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringCopyPadded(gStringVar1, GetWeatherName(0), CHAR_SPACE, 30);
    StringExpandPlaceholders(gStringVar4, sDebugText_Util_Weather_ID);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

    gTasks[taskId].func = DebugAction_Util_Weather_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 0;
    gTasks[taskId].tDigit = 0;
}

static void DebugAction_Util_Weather_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, WEATHER_NONE, WEATHER_COUNT - 1, 3);

        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, 2);

        StringCopyPadded(gStringVar1, GetWeatherName(gTasks[taskId].tInput), CHAR_SPACE, 30);

        StringExpandPlaceholders(gStringVar4, sDebugText_Util_Weather_ID);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        if (gTasks[taskId].tInput <= 14 || gTasks[taskId].tInput >= 20)
        {
            gTasks[taskId].data[5] = gTasks[taskId].tInput;
            SetWeather(gTasks[taskId].data[5]);
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Util_WatchCredits(u8 taskId)
{
    Debug_DestroyMenu_Full(taskId);
    SetMainCallback2(CB2_StartCreditsSequence);
}

static void DebugAction_Player_Name(u8 taskId)
{
    DoNamingScreen(NAMING_SCREEN_PLAYER, gSaveBlock2Ptr->playerName, gSaveBlock2Ptr->playerGender, 0, 0, CB2_ReturnToFieldContinueScript);
}

static void DebugAction_Player_Gender(u8 taskId)
{
    if (gSaveBlock2Ptr->playerGender == MALE)
        gSaveBlock2Ptr->playerGender = FEMALE;
    else
        gSaveBlock2Ptr->playerGender = MALE;
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_Player_Id(u8 taskId)
{
    u32 trainerId = Random32();
    SetTrainerId(trainerId, gSaveBlock2Ptr->playerTrainerId);
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_Util_CheatStart(u8 taskId)
{
    if (!FlagGet(FLAG_SYS_CLOCK_SET))
        RtcInitLocalTimeOffset(0, 0);

    InitTimeBasedEvents();
    Debug_DestroyMenu_Full_Script(taskId, Debug_CheatStart);
}

void BufferExpansionVersion(struct ScriptContext *ctx)
{
    static const u8 sText_Released[] = _("\nRelease Build");
    static const u8 sText_Unreleased[] = _("\nDevelopment Build");
    u8 *string = gStringVar1;
    *string++ = CHAR_v;
    string = ConvertIntToDecimalStringN(string, EXPANSION_VERSION_MAJOR, STR_CONV_MODE_LEFT_ALIGN, 3);
    *string++ = CHAR_PERIOD;
    string = ConvertIntToDecimalStringN(string, EXPANSION_VERSION_MINOR, STR_CONV_MODE_LEFT_ALIGN, 3);
    *string++ = CHAR_PERIOD;
    string = ConvertIntToDecimalStringN(string, EXPANSION_VERSION_PATCH, STR_CONV_MODE_LEFT_ALIGN, 3);
    if (EXPANSION_TAGGED_RELEASE)
        string = StringCopy(string, sText_Released);
    else
        string = StringCopy(string, sText_Unreleased);
}

void DebugMenu_CalculateTime(struct ScriptContext *ctx)
{
    if (OW_USE_FAKE_RTC)
    {
        struct SiiRtcInfo *rtc = FakeRtc_GetCurrentTime();
        StringExpandPlaceholders(gStringVar1, gDayNameStringsTable[rtc->dayOfWeek]);
        ConvertIntToDecimalStringN(gStringVar2, rtc->hour, STR_CONV_MODE_LEFT_ALIGN, 3);
        ConvertIntToDecimalStringN(gStringVar3, rtc->minute, STR_CONV_MODE_LEADING_ZEROS, 2);
    }
    else
    {
        u32 day = ((gLocalTime.days - 1) + 6) % 7 ;
        RtcCalcLocalTime();
        StringExpandPlaceholders(gStringVar1, gDayNameStringsTable[day]);
        ConvertIntToDecimalStringN(gStringVar2, gLocalTime.hours, STR_CONV_MODE_LEFT_ALIGN, 3);
        ConvertIntToDecimalStringN(gStringVar3, gLocalTime.minutes, STR_CONV_MODE_LEADING_ZEROS, 2);
    }
}

void DebugMenu_CalculateTimeOfDay(struct ScriptContext *ctx)
{
    enum TimeOfDay timeOfDay = GetTimeOfDay();
    switch (timeOfDay)
    {
        case TIME_MORNING:
        case TIME_DAY:
        case TIME_EVENING:
        case TIME_NIGHT:
            StringExpandPlaceholders(gStringVar1, gTimeOfDayStringsTable[timeOfDay]);
            break;
        case TIMES_OF_DAY_COUNT:
            break;
    }
}

// *******************************
// Actions Flags and Vars
static void Debug_Display_FlagInfo(u32 flag, u32 digit, u8 windowId)
{
    ConvertIntToDecimalStringN(gStringVar1, flag, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_FLAGS);
    ConvertIntToHexStringN(gStringVar2, flag, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringExpandPlaceholders(gStringVar1, COMPOUND_STRING("{STR_VAR_1}{CLEAR_TO 90}\n0x{STR_VAR_2}{CLEAR_TO 90}"));
    if (FlagGet(flag))
        StringCopyPadded(gStringVar2, sDebugText_True, CHAR_SPACE, 15);
    else
        StringCopyPadded(gStringVar2, sDebugText_False, CHAR_SPACE, 15);
    StringCopy(gStringVar3, gText_DigitIndicator[digit]);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Flag: {STR_VAR_1}{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}\n{STR_VAR_3}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_FlagsVars_Flags(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial flag
    Debug_Display_FlagInfo(FLAG_TEMP_1, 0, windowId);

    gTasks[taskId].func = DebugAction_FlagsVars_FlagsSelect;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = FLAG_TEMP_1;
    gTasks[taskId].tDigit = 0;
}

static void DebugAction_FlagsVars_FlagsSelect(u8 taskId)
{
    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        FlagToggle(gTasks[taskId].tInput);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
        return;
    }

    Debug_HandleInput_Numeric(taskId, 1, FLAGS_COUNT - 1, DEBUG_NUMBER_DIGITS_FLAGS);

    if (JOY_NEW(DPAD_ANY) || JOY_NEW(A_BUTTON))
    {
        Debug_Display_FlagInfo(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }
}

#define tVarValue  data[5]

static void DebugAction_FlagsVars_Vars(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial var
    ConvertIntToDecimalStringN(gStringVar1, VARS_START, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
    ConvertIntToHexStringN(gStringVar2, VARS_START, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringExpandPlaceholders(gStringVar1, sDebugText_FlagsVars_VariableHex);
    ConvertIntToDecimalStringN(gStringVar3, 0, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    StringCopy(gStringVar2, gText_DigitIndicator[0]);
    StringExpandPlaceholders(gStringVar4, sDebugText_FlagsVars_Variable);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

    gTasks[taskId].func = DebugAction_FlagsVars_Select;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = VARS_START;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tVarValue = 0;
}

static void DebugAction_FlagsVars_Select(u8 taskId)
{
    Debug_HandleInput_Numeric(taskId, VARS_START, VARS_END, DEBUG_NUMBER_DIGITS_VARIABLES);

    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        ConvertIntToHexStringN(gStringVar2, gTasks[taskId].tInput, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringExpandPlaceholders(gStringVar1, sDebugText_FlagsVars_VariableHex);
        if (VarGetIfExist(gTasks[taskId].tInput) == 0xFFFF)
            gTasks[taskId].tVarValue = 0;
        else
            gTasks[taskId].tVarValue = VarGet(gTasks[taskId].tInput);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].tVarValue, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);

        //Combine str's to full window string
        StringExpandPlaceholders(gStringVar4, sDebugText_FlagsVars_Variable);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        gTasks[taskId].tDigit = 0;

        PlaySE(SE_RG_BALL_CLICK);

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        ConvertIntToHexStringN(gStringVar2, gTasks[taskId].tInput, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringExpandPlaceholders(gStringVar1, sDebugText_FlagsVars_VariableHex);
        if (VarGetIfExist(gTasks[taskId].tInput) == 0xFFFF)
            gTasks[taskId].tVarValue = 0;
        else
            gTasks[taskId].tVarValue = VarGet(gTasks[taskId].tInput);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].tVarValue, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);
        StringExpandPlaceholders(gStringVar4, sDebugText_FlagsVars_VariableValueSet);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

        gTasks[taskId].data[6] = gTasks[taskId].data[5]; //New value selector
        gTasks[taskId].func = DebugAction_FlagsVars_SetValue;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
        return;
    }
}

static void DebugAction_FlagsVars_SetValue(u8 taskId)
{
    if (JOY_NEW(DPAD_UP))
    {
        if (gTasks[taskId].data[6] + sPowersOfTen[gTasks[taskId].tDigit] <= 32000)
            gTasks[taskId].data[6] += sPowersOfTen[gTasks[taskId].tDigit];
        else
            gTasks[taskId].data[6] = 32000 - 1;

        if (gTasks[taskId].data[6] >= 32000)
            gTasks[taskId].data[6] = 32000 - 1;
    }
    if (JOY_NEW(DPAD_DOWN))
    {
        gTasks[taskId].data[6] -= sPowersOfTen[gTasks[taskId].tDigit];
        if (gTasks[taskId].data[6] < 0)
            gTasks[taskId].data[6] = 0;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        gTasks[taskId].tDigit -= 1;
        if (gTasks[taskId].tDigit < 0)
            gTasks[taskId].tDigit = 0;
    }
    if (JOY_NEW(DPAD_RIGHT))
    {
        gTasks[taskId].tDigit += 1;
        if (gTasks[taskId].tDigit > 4)
            gTasks[taskId].tDigit = 4;
    }

    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        VarSet(gTasks[taskId].tInput, gTasks[taskId].data[6]);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
        return;
    }

    if (JOY_NEW(DPAD_ANY) || JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);

        ConvertIntToDecimalStringN(gStringVar1, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        ConvertIntToHexStringN(gStringVar2, gTasks[taskId].tInput, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringExpandPlaceholders(gStringVar1, sDebugText_FlagsVars_VariableHex);
        StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].data[6], STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_VARIABLES);
        StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);
        StringExpandPlaceholders(gStringVar4, sDebugText_FlagsVars_VariableValueSet);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }
}

#undef tVarValue

static void DebugAction_FlagsVars_PokedexFlags_All(u8 taskId)
{
    u16 i;
    for (i = 0; i < NATIONAL_DEX_COUNT; i++)
    {
        GetSetPokedexFlag(i + 1, FLAG_SET_CAUGHT);
        GetSetPokedexFlag(i + 1, FLAG_SET_SEEN);
    }
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_FlagsVars_PokedexFlags_Reset(u8 taskId)
{
    int boxId, boxPosition, partyId;
    u16 species;

    // Reset Pokedex to emtpy
    memset(&gSaveBlock1Ptr->dexCaught, 0, sizeof(gSaveBlock1Ptr->dexCaught));
    memset(&gSaveBlock1Ptr->dexSeen, 0, sizeof(gSaveBlock1Ptr->dexSeen));

    // Add party Pokemon to Pokedex
    for (partyId = 0; partyId < PARTY_SIZE; partyId++)
    {
        if (GetMonData(&gPlayerParty[partyId], MON_DATA_SANITY_HAS_SPECIES))
        {
            species = GetMonData(&gPlayerParty[partyId], MON_DATA_SPECIES);
            GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_CAUGHT);
            GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_SEEN);
        }
    }

    // Add box Pokemon to Pokedex
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPosition = 0; boxPosition < IN_BOX_COUNT; boxPosition++)
        {
            if (GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_HAS_SPECIES))
            {
                species = GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SPECIES);
                GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_CAUGHT);
                GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_SEEN);
            }
        }
    }
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_FlagsVars_SwitchDex(u8 taskId)
{
    if (FlagGet(FLAG_SYS_POKEDEX_GET))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(FLAG_SYS_POKEDEX_GET);
}

static void DebugAction_FlagsVars_SwitchNatDex(u8 taskId)
{
    if (IsNationalPokedexEnabled())
    {
        DisableNationalPokedex();
        PlaySE(SE_PC_OFF);
    }
    else
    {
        EnableNationalPokedex();
        PlaySE(SE_PC_LOGIN);
    }
}

static void DebugAction_FlagsVars_SwitchPokeNav(u8 taskId)
{
    if (FlagGet(FLAG_SYS_POKENAV_GET))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(FLAG_SYS_POKENAV_GET);
}

static void DebugAction_FlagsVars_SwitchMatchCall(u8 taskId)
{
    if (FlagGet(FLAG_ADDED_MATCH_CALL_TO_POKENAV))
    {
        PlaySE(SE_PC_OFF);
        FlagClear(FLAG_ADDED_MATCH_CALL_TO_POKENAV);
        FlagClear(FLAG_HAS_MATCH_CALL);
    }
    else
    {
        PlaySE(SE_PC_LOGIN);
        FlagSet(FLAG_ADDED_MATCH_CALL_TO_POKENAV);
        FlagSet(FLAG_HAS_MATCH_CALL);
    }
}

static void DebugAction_FlagsVars_RunningShoes(u8 taskId)
{
    if (FlagGet(FLAG_SYS_B_DASH))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(FLAG_SYS_B_DASH);
}

static void DebugAction_FlagsVars_ToggleFlyFlags(u8 taskId)
{
    if (FlagGet(sLocationFlags[ARRAY_COUNT(sLocationFlags) - 1]))
    {
        PlaySE(SE_PC_OFF);
        for (u32 i = 0; i < ARRAY_COUNT(sLocationFlags); i++)
            FlagClear(sLocationFlags[i]);
    }
    else
    {
        PlaySE(SE_PC_LOGIN);
        for (u32 i = 0; i < ARRAY_COUNT(sLocationFlags); i++)
            FlagSet(sLocationFlags[i]);
    }
}

static void DebugAction_FlagsVars_ToggleBadgeFlags(u8 taskId)
{
    if (FlagGet(gBadgeFlags[ARRAY_COUNT(gBadgeFlags) - 1]))
    {
        PlaySE(SE_PC_OFF);
        for (u32 i = 0; i < ARRAY_COUNT(gBadgeFlags); i++)
            FlagClear(gBadgeFlags[i]);
    }
    else
    {
        PlaySE(SE_PC_LOGIN);
        for (u32 i = 0; i < ARRAY_COUNT(gBadgeFlags); i++)
            FlagSet(gBadgeFlags[i]);
    }
}

static void DebugAction_FlagsVars_ToggleGameClear(u8 taskId)
{
    // Sound effect
    if (FlagGet(FLAG_SYS_GAME_CLEAR))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(FLAG_SYS_GAME_CLEAR);
}

static void DebugAction_FlagsVars_ToggleFrontierPass(u8 taskId)
{
    // Sound effect
    if (FlagGet(FLAG_SYS_FRONTIER_PASS))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(FLAG_SYS_FRONTIER_PASS);
}

static void DebugAction_FlagsVars_CollisionOnOff(u8 taskId)
{
#if OW_FLAG_NO_COLLISION == 0
    Debug_DestroyMenu_Full_Script(taskId, Debug_FlagsNotSetOverworldConfigMessage);
#else
    if (FlagGet(OW_FLAG_NO_COLLISION))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(OW_FLAG_NO_COLLISION);
#endif
}

static void DebugAction_FlagsVars_EncounterOnOff(u8 taskId)
{
#if OW_FLAG_NO_ENCOUNTER == 0
    Debug_DestroyMenu_Full_Script(taskId, Debug_FlagsNotSetOverworldConfigMessage);
#else
    if (FlagGet(OW_FLAG_NO_ENCOUNTER))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(OW_FLAG_NO_ENCOUNTER);
#endif
}

static void DebugAction_FlagsVars_TrainerSeeOnOff(u8 taskId)
{
#if OW_FLAG_NO_TRAINER_SEE == 0
    Debug_DestroyMenu_Full_Script(taskId, Debug_FlagsNotSetOverworldConfigMessage);
#else
    if (FlagGet(OW_FLAG_NO_TRAINER_SEE))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(OW_FLAG_NO_TRAINER_SEE);
#endif
}

static void DebugAction_FlagsVars_BagUseOnOff(u8 taskId)
{
#if B_VAR_NO_BAG_USE < VARS_START || B_VAR_NO_BAG_USE > VARS_END
    Debug_DestroyMenu_Full_Script(taskId, Debug_VarsNotSetBattleConfigMessage);
#else
    PlaySE(SE_RG_BALL_CLICK);
    VarSet(B_VAR_NO_BAG_USE, (VarGet(B_VAR_NO_BAG_USE) + 1) % 3);
#endif
}

static void DebugAction_FlagsVars_CatchingOnOff(u8 taskId)
{
#if B_FLAG_NO_CATCHING == 0
    Debug_DestroyMenu_Full_Script(taskId, Debug_FlagsNotSetBattleConfigMessage);
#else
    if (FlagGet(B_FLAG_NO_CATCHING))
        PlaySE(SE_PC_OFF);
    else
        PlaySE(SE_PC_LOGIN);
    FlagToggle(B_FLAG_NO_CATCHING);
#endif
}

// *******************************
// Actions Give
#define ITEM_TAG 0xFDF3
#define tItemId    data[5]
#define tSpriteId  data[6]

static void Debug_Display_ItemInfo(u32 itemId, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    u8* end = CopyItemName(itemId, gStringVar1);
    u16 moveId = ItemIdToBattleMoveId(itemId);
    if (moveId != MOVE_NONE)
    {
        end = StringCopy(end, gText_Space);
        end = StringCopy(end, GetMoveName(moveId));
    }
    else if (CheckIfItemIsTMHMOrEvolutionStone(itemId) == 1)
    {
        end = StringCopy(end, COMPOUND_STRING(" None"));
    }

    WrapFontIdToFit(gStringVar1, end, DEBUG_MENU_FONT, WindowWidthPx(windowId));
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    ConvertIntToDecimalStringN(gStringVar3, itemId, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Item ID: {STR_VAR_3}\n{STR_VAR_1}{CLEAR_TO 90}\n\n{STR_VAR_2}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Item(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial item
    Debug_Display_ItemInfo(1, 0, windowId);

    gTasks[taskId].func = DebugAction_Give_Item_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 1;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tSpriteId = AddItemIconSprite(ITEM_TAG, ITEM_TAG, gTasks[taskId].tInput);
    gSprites[gTasks[taskId].tSpriteId].x2 = DEBUG_NUMBER_ICON_X+10;
    gSprites[gTasks[taskId].tSpriteId].y2 = DEBUG_NUMBER_ICON_Y+10;
    gSprites[gTasks[taskId].tSpriteId].oam.priority = 0;
}

static void DestroyItemIcon(u8 taskId)
{
    FreeSpriteTilesByTag(ITEM_TAG);
    FreeSpritePaletteByTag(ITEM_TAG);
    FreeSpriteOamMatrix(&gSprites[gTasks[taskId].tSpriteId]);
    DestroySprite(&gSprites[gTasks[taskId].tSpriteId]);
}

static void Debug_Display_ItemQuantity(u32 quantity, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar1, quantity, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEM_QUANTITY);
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Quantity:{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n\n{STR_VAR_2}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Item_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 1, ITEMS_COUNT - 1, DEBUG_NUMBER_DIGITS_ITEMS);
        Debug_Display_ItemInfo(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
        DestroyItemIcon(taskId);
        gTasks[taskId].tSpriteId = AddItemIconSprite(ITEM_TAG, ITEM_TAG, gTasks[taskId].tInput);
        gSprites[gTasks[taskId].tSpriteId].x2 = DEBUG_NUMBER_ICON_X+10;
        gSprites[gTasks[taskId].tSpriteId].y2 = DEBUG_NUMBER_ICON_Y+10;
        gSprites[gTasks[taskId].tSpriteId].oam.priority = 0;
    }

    if (JOY_NEW(A_BUTTON))
    {
        gTasks[taskId].tItemId = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 1;
        gTasks[taskId].tDigit = 0;
        Debug_Display_ItemQuantity(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
        gTasks[taskId].func = DebugAction_Give_Item_SelectQuantity;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        DestroyItemIcon(taskId);

        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Give_Item_SelectQuantity(u8 taskId)
{
    u32 itemId = gTasks[taskId].tItemId;

    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 1, MAX_BAG_ITEM_CAPACITY, MAX_ITEM_DIGITS);
        Debug_Display_ItemQuantity(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        DestroyItemIcon(taskId);

        PlaySE(MUS_LEVEL_UP);
        AddBagItem(itemId, gTasks[taskId].tInput);
        DebugAction_DestroyExtraWindow(taskId);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        DestroyItemIcon(taskId);

        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

#undef tItemId
#undef tSpriteId

//Pokemon
static void ResetMonDataStruct(struct DebugMonData *sDebugMonData)
{
    sDebugMonData->species          = 1;
    sDebugMonData->level            = MIN_LEVEL;
    sDebugMonData->isShiny          = FALSE;
    sDebugMonData->nature           = 0;
    sDebugMonData->abilityNum       = 0;
    sDebugMonData->teraType         = TYPE_NONE;
    sDebugMonData->dynamaxLevel     = 0;
    sDebugMonData->gmaxFactor       = FALSE;
    for (u32 i = 0; i < NUM_STATS; i++)
    {
        sDebugMonData->monIVs[i] = 0;
        sDebugMonData->monEVs[i] = 0;
    }
}

#define tIsComplex  data[5]
#define tSpriteId   data[6]
#define tIterator   data[7]

static void Debug_Display_SpeciesInfo(u32 species, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    u8 *end = StringCopy(gStringVar1, GetSpeciesName(species));
    WrapFontIdToFit(gStringVar1, end, DEBUG_MENU_FONT, WindowWidthPx(windowId));
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    ConvertIntToDecimalStringN(gStringVar3, species, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Species: {STR_VAR_3}\n{STR_VAR_1}{CLEAR_TO 90}\n\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_PokemonSimple(u8 taskId)
{
    u8 windowId;

    //Mon data struct
    sDebugMonData = AllocZeroed(sizeof(struct DebugMonData));
    ResetMonDataStruct(sDebugMonData);

    //Window initialization
    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial Pokémon
    Debug_Display_SpeciesInfo(sDebugMonData->species, 0, windowId);

    //Set task data
    gTasks[taskId].func = DebugAction_Give_Pokemon_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = sDebugMonData->species;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tIsComplex = FALSE;

    FreeMonIconPalettes();
    LoadMonIconPalettePersonality(gTasks[taskId].tInput, 0);
    gTasks[taskId].tSpriteId = CreateMonIcon(gTasks[taskId].tInput, SpriteCB_MonIcon, DEBUG_NUMBER_ICON_X, DEBUG_NUMBER_ICON_Y, 4, 0);
    gSprites[gTasks[taskId].tSpriteId].oam.priority = 0;
}

// Project Grounded: "Battle test…" (zie sDebugMenu_Actions_BattleTest). Tijdens het gevecht vecht een testteam
// (2x Arceus lv 100); party, geld, Pokédex-vlaggen en spelstatistieken worden vooraf bewaard en na afloop teruggezet.
// Er worden geen trainer- of eventflags gezet en verliezen geeft geen white-out. Een gevangen Pokémon verdwijnt weer met het testteam.
EWRAM_DATA bool8 gDebugBattleTest = FALSE;
static EWRAM_DATA const struct BattleTest *sBattleTestCurrent = NULL;
static EWRAM_DATA struct Pokemon sBattleTestParty[PARTY_SIZE] = {0};
static EWRAM_DATA u8 sBattleTestPartyCount = 0;
static EWRAM_DATA u32 sBattleTestMoney = 0;
static EWRAM_DATA u8 sBattleTestDexSeen[NUM_DEX_FLAG_BYTES] = {0};
static EWRAM_DATA u8 sBattleTestDexCaught[NUM_DEX_FLAG_BYTES] = {0};
static EWRAM_DATA u32 sBattleTestGameStats[NUM_GAME_STATS] = {0};
static EWRAM_DATA u16 sBattleTestDailyWilds = 0;

static void DebugAction_Util_BattleTest(u8 taskId, const struct BattleTest *test)
{
    sBattleTestCurrent = test;
    Debug_DestroyMenu_Full_Script(taskId, Debug_EventScript_BattleTest);
}

static void BattleTest_Restore(void)
{
    u32 i;

    memcpy(gPlayerParty, sBattleTestParty, sizeof(gPlayerParty));
    gPlayerPartyCount = sBattleTestPartyCount;
    SetMoney(&gSaveBlock1Ptr->money, sBattleTestMoney);
    memcpy(gSaveBlock1Ptr->dexSeen, sBattleTestDexSeen, NUM_DEX_FLAG_BYTES);
    memcpy(gSaveBlock1Ptr->dexCaught, sBattleTestDexCaught, NUM_DEX_FLAG_BYTES);
    for (i = 0; i < NUM_GAME_STATS; i++)
        SetGameStat(i, sBattleTestGameStats[i]);
    VarSet(VAR_DAILY_WILDS, sBattleTestDailyWilds);
    gDebugBattleTest = FALSE;
}

static void CB2_EndBattleTest(void)
{
    BattleTest_Restore();
    CpuFill16(0, (void *)(BG_PLTT), BG_PLTT_SIZE);
    ResetOamRange(0, 128);
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void BattleTest_CreateTestMon(struct Pokemon *mon)
{
    static const u16 moves[MAX_MON_MOVES] = { MOVE_DARK_PULSE, MOVE_PSYCHIC, MOVE_THUNDERBOLT, MOVE_ICE_BEAM };
    u32 i;

    CreateMon(mon, SPECIES_ARCEUS, 100, MAX_PER_STAT_IVS, FALSE, 0, OT_ID_PLAYER_ID, 0);
    for (i = 0; i < MAX_MON_MOVES; i++)
        SetMonMoveSlot(mon, moves[i], i);
}

void Debug_BattleTest_Start(void)
{
    const struct BattleTest *test = sBattleTestCurrent;
    u32 i;

    if (test == NULL)
        return;

    // bewaren
    memcpy(sBattleTestParty, gPlayerParty, sizeof(gPlayerParty));
    sBattleTestPartyCount = gPlayerPartyCount;
    sBattleTestMoney = GetMoney(&gSaveBlock1Ptr->money);
    memcpy(sBattleTestDexSeen, gSaveBlock1Ptr->dexSeen, NUM_DEX_FLAG_BYTES);
    memcpy(sBattleTestDexCaught, gSaveBlock1Ptr->dexCaught, NUM_DEX_FLAG_BYTES);
    for (i = 0; i < NUM_GAME_STATS; i++)
        sBattleTestGameStats[i] = GetGameStat(i);
    sBattleTestDailyWilds = VarGet(VAR_DAILY_WILDS);

    // testteam (twee, ook voor dubbelgevechten)
    ZeroPlayerPartyMons();
    BattleTest_CreateTestMon(&gPlayerParty[0]);
    BattleTest_CreateTestMon(&gPlayerParty[1]);
    gPlayerPartyCount = 2;
    gDebugBattleTest = TRUE;

    switch (test->kind)
    {
    case BATTLE_TEST_LEGEND:
        CreateScriptedWildMon(test->id, test->level, ITEM_NONE);
        BattleSetup_StartLegendaryBattle();
        break;
    case BATTLE_TEST_REGI:
        CreateScriptedWildMon(test->id, test->level, ITEM_NONE);
        StartRegiBattle();
        break;
    case BATTLE_TEST_LATI:
        CreateScriptedWildMon(test->id, test->level, ITEM_NONE);
        BattleSetup_StartLatiBattle();
        break;
    case BATTLE_TEST_WILD:
        CreateScriptedWildMon(test->id, test->level, ITEM_NONE);
        BattleSetup_StartScriptedWildBattle();
        break;
    case BATTLE_TEST_TRAINER:
    default:
        BattleSetup_StartBattleTestTrainer(test->id, test->id2, CB2_EndBattleTest);
        break;
    }
    gMain.savedCallback = CB2_EndBattleTest;
}

// Project Grounded: "Force encounter": kies een soort; alle wilde encounters (ook vissen, rock smash en
// "Wild battle (map)") worden die soort, op het level uit de tabel, tot "Force encounter: off".
// De eerstvolgende stap in het gras is meteen raak.
static void DebugAction_Util_ForceEncounter(u8 taskId)
{
    DebugAction_Give_PokemonSimple(taskId);
    gTasks[taskId].func = DebugAction_Util_ForceEncounter_SelectId;
}

static void DebugAction_Util_ForceEncounter_SelectId(u8 taskId)
{
    if (JOY_NEW(A_BUTTON))
    {
        gDebugForcedWildSpecies = gTasks[taskId].tInput;
        gDebugForceNextStep = TRUE;
        StringCopy(gStringVar1, GetSpeciesName(gDebugForcedWildSpecies));
        PlaySE(SE_SELECT);
        Free(sDebugMonData);
        FreeMonIconPalettes();
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        DebugAction_DestroyExtraWindow(taskId);
        LockPlayerFieldControls();
        FreezeObjectEvents();
        ScriptContext_SetupScript(Debug_EventScript_ForcedEncounterSet);
        return;
    }
    DebugAction_Give_Pokemon_SelectId(taskId);
    if (gTasks[taskId].func == DebugAction_Give_Pokemon_SelectId)
        gTasks[taskId].func = DebugAction_Util_ForceEncounter_SelectId;
}

static void DebugAction_Give_PokemonComplex(u8 taskId)
{
    u8 windowId;

    //Mon data struct
    sDebugMonData = AllocZeroed(sizeof(struct DebugMonData));
    ResetMonDataStruct(sDebugMonData);

    //Window initialization
    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial Pokémon
    Debug_Display_SpeciesInfo(sDebugMonData->species, 0, windowId);

    gTasks[taskId].func = DebugAction_Give_Pokemon_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 1;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tIsComplex = TRUE;

    FreeMonIconPalettes();
    LoadMonIconPalettePersonality(gTasks[taskId].tInput, 0);
    gTasks[taskId].tSpriteId = CreateMonIcon(gTasks[taskId].tInput, SpriteCB_MonIcon, DEBUG_NUMBER_ICON_X, DEBUG_NUMBER_ICON_Y, 4, 0);
    gSprites[gTasks[taskId].tSpriteId].oam.priority = 0;
    gTasks[taskId].tIterator = 0;
}

static void Debug_Display_Level(u32 level, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar1, level, STR_CONV_MODE_LEADING_ZEROS, 3);
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Level:{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 1, NUM_SPECIES - 1, DEBUG_NUMBER_DIGITS_ITEMS);
        Debug_Display_SpeciesInfo(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        FreeMonIconPalettes();
        LoadMonIconPalettePersonality(gTasks[taskId].tInput, 0);
        gTasks[taskId].tSpriteId = CreateMonIcon(gTasks[taskId].tInput, SpriteCB_MonIcon, DEBUG_NUMBER_ICON_X, DEBUG_NUMBER_ICON_Y, 4, 0);
        gSprites[gTasks[taskId].tSpriteId].oam.priority = 0;
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->species = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 1;
        gTasks[taskId].tDigit = 0;

        Debug_Display_Level(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);

        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectLevel;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        FreeMonIconPalettes();
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_TrueFalse(bool32 value, u8 windowId, const u8 *titleStr)
{
    static const u8 *txtStr;
    txtStr = value ? sDebugText_True : sDebugText_False;
    StringCopyPadded(gStringVar2, txtStr, CHAR_SPACE, 15);
    ConvertIntToDecimalStringN(gStringVar3, value, STR_CONV_MODE_LEADING_ZEROS, 0);
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    StringExpandPlaceholders(gStringVar4, titleStr);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectLevel(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 1, MAX_LEVEL, 3);
        Debug_Display_Level(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        FreeMonIconPalettes();
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        if (gTasks[taskId].tIsComplex == FALSE)
        {
            PlaySE(MUS_LEVEL_UP);
            ScriptGiveMon(sDebugMonData->species, gTasks[taskId].tInput, ITEM_NONE);
            // Set flag for user convenience
            FlagSet(FLAG_SYS_POKEMON_GET);
            Free(sDebugMonData);
            DebugAction_DestroyExtraWindow(taskId);
        }
        else
        {
            sDebugMonData->level = gTasks[taskId].tInput;
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;
            Debug_Display_TrueFalse(gTasks[taskId].tInput, gTasks[taskId].tSubWindowId, sDebugText_PokemonShiny);
            gTasks[taskId].func = DebugAction_Give_Pokemon_SelectShiny;
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        FreeMonIconPalettes();
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_Nature(u32 natureId, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar3, natureId, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    StringCopy(gStringVar1, gNaturesInfo[natureId].name);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Nature ID: {STR_VAR_3}{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectShiny(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        gTasks[taskId].tInput ^= JOY_NEW(DPAD_UP | DPAD_DOWN) > 0;
        Debug_Display_TrueFalse(gTasks[taskId].tInput, gTasks[taskId].tSubWindowId, sDebugText_PokemonShiny);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->isShiny = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;
        Debug_Display_Nature(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectNature;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_Ability(enum Ability abilityId, u32 digit, u8 windowId)//(u32 natureId, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar3, abilityId, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    u8 *end = StringCopy(gStringVar1, gAbilitiesInfo[abilityId].name);
    WrapFontIdToFit(gStringVar1, end, DEBUG_MENU_FONT, WindowWidthPx(windowId));
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Ability Num: {STR_VAR_3}{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectNature(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);

        if (JOY_NEW(DPAD_UP))
        {
            gTasks[taskId].tInput += sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput > NUM_NATURES - 1)
                gTasks[taskId].tInput = NUM_NATURES - 1;
        }
        if (JOY_NEW(DPAD_DOWN))
        {
            gTasks[taskId].tInput -= sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput < 0)
                gTasks[taskId].tInput = 0;
        }

        Debug_Display_Nature(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->nature = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;

        enum Ability abilityId = GetAbilityBySpecies(sDebugMonData->species, 0);
        Debug_Display_Ability(abilityId, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);

        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectAbility;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_TeraType(u32 typeId, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar3, typeId, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    StringCopy(gStringVar1, gTypesInfo[typeId].name);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Tera Type: {STR_VAR_3}{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectAbility(u8 taskId)
{
    u8 abilityCount = NUM_ABILITY_SLOTS - 1; //-1 for proper iteration
    u8 i = 0;

    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);

        if (JOY_NEW(DPAD_UP))
        {
            gTasks[taskId].tInput += sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput > abilityCount)
                gTasks[taskId].tInput = abilityCount;
        }
        if (JOY_NEW(DPAD_DOWN))
        {
            gTasks[taskId].tInput -= sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput < 0)
                gTasks[taskId].tInput = 0;
        }

        while (GetAbilityBySpecies(sDebugMonData->species, gTasks[taskId].tInput - i) == ABILITY_NONE && gTasks[taskId].tInput - i < NUM_ABILITY_SLOTS)
        {
            i++;
        }
        enum Ability abilityId = GetAbilityBySpecies(sDebugMonData->species, gTasks[taskId].tInput - i);
        Debug_Display_Ability(abilityId, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->abilityNum = gTasks[taskId].tInput - i;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;

        Debug_Display_TeraType(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);

        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectTeraType;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_DynamaxLevel(u32 level, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar1, level, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Dmax Lvl:{CLEAR_TO 90}\n{STR_VAR_1}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{STR_VAR_2}{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectTeraType(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);

        if (JOY_NEW(DPAD_UP))
        {
            gTasks[taskId].tInput += sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput > NUMBER_OF_MON_TYPES - 1)
                gTasks[taskId].tInput = NUMBER_OF_MON_TYPES - 1;
        }
        if (JOY_NEW(DPAD_DOWN))
        {
            gTasks[taskId].tInput -= sPowersOfTen[gTasks[taskId].tDigit];
            if (gTasks[taskId].tInput < 0)
                gTasks[taskId].tInput = 0;
        }

        Debug_Display_TeraType(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->teraType = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;

        Debug_Display_DynamaxLevel(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);

        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectDynamaxLevel;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_GigantamaxFactor(u32 input, u8 windowId)
{
    Debug_Display_TrueFalse(input, windowId, COMPOUND_STRING("Gmax Factor:{CLEAR_TO 90}\n   {STR_VAR_2}{CLEAR_TO 90}\n{CLEAR_TO 90}\n{CLEAR_TO 90}"));
}

static void DebugAction_Give_Pokemon_SelectDynamaxLevel(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, MAX_DYNAMAX_LEVEL, 2);
        Debug_Display_DynamaxLevel(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->dynamaxLevel = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;
        Debug_Display_GigantamaxFactor(gTasks[taskId].tInput, gTasks[taskId].tSubWindowId);
        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectGigantamaxFactor;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        FreeMonIconPalettes();
        FreeAndDestroyMonIconSprite(&gSprites[gTasks[taskId].tSpriteId]);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void Debug_Display_StatInfo(const u8* text, u32 stat, u32 value, u32 digit, u8 windowId, u32 maxValue)
{
    StringCopy(gStringVar1, gStatNamesTable[stat]);
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    ConvertIntToDecimalStringN(gStringVar3, value, STR_CONV_MODE_LEADING_ZEROS, CountDigits(maxValue));
    StringCopyPadded(gStringVar3, gStringVar3, CHAR_SPACE, 15);
    StringExpandPlaceholders(gStringVar4, text);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectGigantamaxFactor(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        gTasks[taskId].tInput ^= JOY_NEW(DPAD_UP | DPAD_DOWN) > 0;
        Debug_Display_GigantamaxFactor(gTasks[taskId].tInput, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        sDebugMonData->gmaxFactor = gTasks[taskId].tInput;
        gTasks[taskId].tInput = 0;
        gTasks[taskId].tDigit = 0;
        Debug_Display_StatInfo(sDebugText_IVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_IVS);
        gTasks[taskId].func = DebugAction_Give_Pokemon_SelectIVs;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Give_Pokemon_SelectIVs(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, MAX_PER_STAT_IVS, 3);
        Debug_Display_StatInfo(sDebugText_IVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_IVS);
    }

    //If A or B button
    if (JOY_NEW(A_BUTTON))
    {
        // Set IVs for stat
        sDebugMonData->monIVs[gTasks[taskId].tIterator] = gTasks[taskId].tInput;

        //Check if all IVs set
        if (gTasks[taskId].tIterator != NUM_STATS - 1)
        {
            gTasks[taskId].tIterator++;
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;

            Debug_Display_StatInfo(sDebugText_IVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_IVS);
            gTasks[taskId].func = DebugAction_Give_Pokemon_SelectIVs;
        }
        else
        {
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;
            gTasks[taskId].tIterator = 0;

            Debug_Display_StatInfo(sDebugText_EVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_EVS);
            gTasks[taskId].func = DebugAction_Give_Pokemon_SelectEVs;
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static u32 GetDebugPokemonTotalEV(void)
{
    u32 totalEVs = 0;
    for (u32 i = 0; i < NUM_STATS; i++)
        totalEVs += sDebugMonData->monEVs[i];
    return totalEVs;
}

static void Debug_Display_MoveInfo(u32 moveId, u32 iteration, u32 digit, u8 windowId)
{
    // Doesn't expand placeholdes so a 4th dynamic value can be shown.
    u8 *end = StringCopy(gStringVar1, GetMoveName(moveId));
    WrapFontIdToFit(gStringVar1, end, DEBUG_MENU_FONT, WindowWidthPx(windowId));
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    StringCopy(gStringVar4, COMPOUND_STRING("Move "));
    ConvertIntToDecimalStringN(gStringVar3, iteration, STR_CONV_MODE_LEADING_ZEROS, 1);
    StringAppend(gStringVar4, gStringVar3);
    StringAppend(gStringVar4, COMPOUND_STRING(": "));
    ConvertIntToDecimalStringN(gStringVar3, moveId, STR_CONV_MODE_LEADING_ZEROS, 3);
    StringAppend(gStringVar4, gStringVar3);
    StringAppend(gStringVar4, COMPOUND_STRING("{CLEAR_TO 90}\n"));
    StringAppend(gStringVar4, gStringVar1);
    StringAppend(gStringVar4, COMPOUND_STRING("{CLEAR_TO 90}\n{CLEAR_TO 90}\n"));
    StringAppend(gStringVar4, gText_DigitIndicator[digit]);
    StringAppend(gStringVar4, COMPOUND_STRING("{CLEAR_TO 90}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Pokemon_SelectEVs(u8 taskId)
{
    u16 totalEV = GetDebugPokemonTotalEV();

    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, MAX_PER_STAT_EVS, 4);
        Debug_Display_StatInfo(sDebugText_EVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_EVS);
    }

    //If A or B button
    if (JOY_NEW(A_BUTTON))
    {
        // Set EVs for stat
        sDebugMonData->monEVs[gTasks[taskId].tIterator] = gTasks[taskId].tInput;

        //Check if all EVs set
        if (gTasks[taskId].tIterator != NUM_STATS - 1)
        {
            gTasks[taskId].tIterator++;
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;
            Debug_Display_StatInfo(sDebugText_EVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_EVS);
            gTasks[taskId].func = DebugAction_Give_Pokemon_SelectEVs;
        }
        else
        {
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;
            gTasks[taskId].tIterator = 0;

            if (totalEV > MAX_TOTAL_EVS)
            {
                for (u32 i = 0; i < NUM_STATS; i++)
                {
                    sDebugMonData->monEVs[i] = 0;
                }

                PlaySE(SE_FAILURE);
                Debug_Display_StatInfo(sDebugText_EVs, gTasks[taskId].tIterator, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId, MAX_PER_STAT_EVS);
                gTasks[taskId].func = DebugAction_Give_Pokemon_SelectEVs;
            }
            else
            {
                Debug_Display_MoveInfo(gTasks[taskId].tInput, gTasks[taskId].tIterator, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
                gTasks[taskId].func = DebugAction_Give_Pokemon_Move;
            }
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Give_Pokemon_Move(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 0, MOVES_COUNT - 1, 4);

        Debug_Display_MoveInfo(gTasks[taskId].tInput, gTasks[taskId].tIterator, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
    }

    if (JOY_NEW(A_BUTTON))
    {
        // Set current value
        sDebugMonData->monMoves[gTasks[taskId].tIterator] = gTasks[taskId].tInput;

        // If MOVE_NONE selected, stop asking for additional moves
        if (gTasks[taskId].tInput == MOVE_NONE)
            gTasks[taskId].tIterator = MAX_MON_MOVES;

        //If NOT last move or selected MOVE_NONE ask for next move, else make mon
        if (gTasks[taskId].tIterator < MAX_MON_MOVES - 1)
        {
            gTasks[taskId].tIterator++;
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;

            Debug_Display_MoveInfo(gTasks[taskId].tInput, gTasks[taskId].tIterator, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
            gTasks[taskId].func = DebugAction_Give_Pokemon_Move;
        }
        else
        {
            gTasks[taskId].tInput = 0;
            gTasks[taskId].tDigit = 0;

            PlaySE(MUS_LEVEL_UP);
            gTasks[taskId].func = DebugAction_Give_Pokemon_ComplexCreateMon;
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Free(sDebugMonData);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

static void DebugAction_Give_Pokemon_ComplexCreateMon(u8 taskId) //https://github.com/ghoulslash/pokeemerald/tree/custom-givemon
{
    enum NationalDexOrder nationalDexNum;
    int sentToPc;
    struct Pokemon mon;
    u8 i;
    u16 moves[MAX_MON_MOVES];
    u8 IVs[NUM_STATS];
    u8 iv_val;
    u8 EVs[NUM_STATS];
    u8 ev_val;
    u16 species     = sDebugMonData->species;
    u8 level        = sDebugMonData->level;
    bool8 isShiny   = sDebugMonData->isShiny;
    u8 nature       = sDebugMonData->nature;
    u8 abilityNum   = sDebugMonData->abilityNum;
    u32 teraType    = sDebugMonData->teraType;
    u32 dmaxLevel   = sDebugMonData->dynamaxLevel;
    u32 gmaxFactor  = sDebugMonData->gmaxFactor;
    for (u32 i = 0; i < MAX_MON_MOVES; i++)
    {
        moves[i] = sDebugMonData->monMoves[i];
    }
    for (u32 i = 0; i < NUM_STATS; i++)
    {
        EVs[i] = sDebugMonData->monEVs[i];
        IVs[i] = sDebugMonData->monIVs[i];
    }

    //Nature
    if (nature == NUM_NATURES || nature == 0xFF)
        nature = Random() % NUM_NATURES;
    CreateMonWithNature(&mon, species, level, USE_RANDOM_IVS, nature);

    //Shininess
    SetMonData(&mon, MON_DATA_IS_SHINY, &isShiny);

    // Gigantamax factor
    SetMonData(&mon, MON_DATA_GIGANTAMAX_FACTOR, &gmaxFactor);

    // Dynamax Level
    SetMonData(&mon, MON_DATA_DYNAMAX_LEVEL, &dmaxLevel);

    // tera type
    if (teraType == TYPE_NONE || teraType == TYPE_MYSTERY || teraType >= NUMBER_OF_MON_TYPES)
        teraType = GetTeraTypeFromPersonality(&mon);
    SetMonData(&mon, MON_DATA_TERA_TYPE, &teraType);

    //IVs
    for (i = 0; i < NUM_STATS; i++)
    {
        iv_val = IVs[i];
        if (iv_val != USE_RANDOM_IVS && iv_val != 0xFF)
            SetMonData(&mon, MON_DATA_HP_IV + i, &iv_val);
    }

    //EVs
    for (i = 0; i < NUM_STATS; i++)
    {
        ev_val = EVs[i];
        if (ev_val)
            SetMonData(&mon, MON_DATA_HP_EV + i, &ev_val);
    }

    //Moves
    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        // Non-default moveset chosen. Reset moves before setting the chosen moves.
        if (moves[0] != MOVE_NONE)
            SetMonMoveSlot(&mon, MOVE_NONE, i);

        if (moves[i] == MOVE_NONE || moves[i] >= MOVES_COUNT)
            continue;

        SetMonMoveSlot(&mon, moves[i], i);
    }

    //Ability
    if (abilityNum == 0xFF || GetAbilityBySpecies(species, abilityNum) == ABILITY_NONE)
    {
        do {
            abilityNum = Random() % NUM_ABILITY_SLOTS;  // includes hidden abilities
        } while (GetAbilityBySpecies(species, abilityNum) == ABILITY_NONE);
    }

    SetMonData(&mon, MON_DATA_ABILITY_NUM, &abilityNum);

    //Update mon stats before giving it to the player
    CalculateMonStats(&mon);

    // give player the mon
    SetMonData(&mon, MON_DATA_OT_NAME, gSaveBlock2Ptr->playerName);
    SetMonData(&mon, MON_DATA_OT_GENDER, &gSaveBlock2Ptr->playerGender);
    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gPlayerParty[i], MON_DATA_SPECIES, NULL) == SPECIES_NONE)
            break;
    }

    if (i >= PARTY_SIZE)
    {
        sentToPc = CopyMonToPC(&mon);
    }
    else
    {
        sentToPc = MON_GIVEN_TO_PARTY;
        CopyMon(&gPlayerParty[i], &mon, sizeof(mon));
        gPlayerPartyCount = i + 1;
    }

    //Pokedex entry
    nationalDexNum = SpeciesToNationalPokedexNum(species);
    switch(sentToPc)
    {
    case MON_GIVEN_TO_PARTY:
    case MON_GIVEN_TO_PC:
        GetSetPokedexFlag(nationalDexNum, FLAG_SET_SEEN);
        GetSetPokedexFlag(nationalDexNum, FLAG_SET_CAUGHT);
        break;
    case MON_CANT_GIVE:
        break;
    }

    // Set flag for user convenience
    FlagSet(FLAG_SYS_POKEMON_GET);

    Free(sDebugMonData);
    DebugAction_DestroyExtraWindow(taskId); //return sentToPc;
}

#undef tIsComplex
#undef tSpriteId
#undef tIterator

//Decoration
#define tSpriteId  data[6]

static void Debug_Display_DecorationInfo(u32 itemId, u32 digit, u8 windowId)
{
    StringCopy(gStringVar2, gText_DigitIndicator[digit]);
    u8* end = StringCopy(gStringVar1, gDecorations[itemId].name);
    WrapFontIdToFit(gStringVar1, end, DEBUG_MENU_FONT, WindowWidthPx(windowId));
    StringCopyPadded(gStringVar1, gStringVar1, CHAR_SPACE, 15);
    ConvertIntToDecimalStringN(gStringVar3, itemId, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Decor ID: {STR_VAR_3}\n{STR_VAR_1}{CLEAR_TO 90}\n\n{STR_VAR_2}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugAction_Give_Decoration(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateExtra);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial decoration
    Debug_Display_DecorationInfo(1, 0, windowId);

    gTasks[taskId].func = DebugAction_Give_Decoration_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 1;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tSpriteId = AddDecorationIconObject(gTasks[taskId].tInput, DEBUG_NUMBER_ICON_X+8, DEBUG_NUMBER_ICON_Y+10, 0, ITEM_TAG, ITEM_TAG);
}

static void DestroyDecorationIcon(u8 taskId)
{
    FreeSpriteTilesByTag(ITEM_TAG);
    FreeSpritePaletteByTag(ITEM_TAG);
    FreeSpriteOamMatrix(&gSprites[gTasks[taskId].tSpriteId]);
    DestroySprite(&gSprites[gTasks[taskId].tSpriteId]);
}

static void DebugAction_Give_Decoration_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        PlaySE(SE_RG_BALL_CLICK);
        Debug_HandleInput_Numeric(taskId, 1, NUM_DECORATIONS, DEBUG_NUMBER_DIGITS_ITEMS);
        Debug_Display_DecorationInfo(gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
        DestroyDecorationIcon(taskId);
        gTasks[taskId].tSpriteId = AddDecorationIconObject(gTasks[taskId].tInput, DEBUG_NUMBER_ICON_X+8, DEBUG_NUMBER_ICON_Y+10, 0, ITEM_TAG, ITEM_TAG);
    }

    if (JOY_NEW(A_BUTTON))
    {
        DestroyItemIcon(taskId);

        PlaySE(MUS_LEVEL_UP);
        DecorationAdd(gTasks[taskId].tInput);
        DebugAction_DestroyExtraWindow(taskId);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        DestroyDecorationIcon(taskId);

        PlaySE(SE_RG_BALL_CLICK);
        DebugAction_DestroyExtraWindow(taskId);
    }
}

#undef tSpriteId

static void DebugAction_Give_MaxMoney(u8 taskId)
{
    SetMoney(&gSaveBlock1Ptr->money, MAX_MONEY);
}

static void DebugAction_Give_MaxCoins(u8 taskId)
{
    SetCoins(MAX_COINS);

    if (!CheckBagHasItem(ITEM_COIN_CASE, 1))
        AddBagItem(ITEM_COIN_CASE, 1);
}

static void DebugAction_Give_MaxBattlePoints(u8 taskId)
{
    gSaveBlock2Ptr->frontier.battlePoints = MAX_BATTLE_FRONTIER_POINTS;
}

static void DebugAction_Give_DayCareEgg(u8 taskId)
{
    s32 emptySlot = Daycare_FindEmptySpot(&gSaveBlock1Ptr->daycare);
    if (emptySlot == 0) // no daycare mons
        Debug_DestroyMenu_Full_Script(taskId, DebugScript_ZeroDaycareMons);
    else if (emptySlot == 1) // 1 daycare mon
        Debug_DestroyMenu_Full_Script(taskId, DebugScript_OneDaycareMons);
    else if (GetDaycareCompatibilityScore(&gSaveBlock1Ptr->daycare) == PARENTS_INCOMPATIBLE) // not compatible parents
        Debug_DestroyMenu_Full_Script(taskId, DebugScript_DaycareMonsNotCompatible);
    else // 2 pokemon which can have a pokemon baby together
        TriggerPendingDaycareEgg();
}

// *******************************
// Actions TimeMenu

static void DebugAction_TimeMenu_ChangeTimeOfDay(u8 taskId)
{
    u32 input = ListMenu_ProcessInput(gTasks[taskId].tMenuTaskId);

    DebugAction_DestroyExtraWindow(taskId);
    switch (input)
    {
        case TIME_MORNING:
            FakeRtc_ForwardTimeTo(MORNING_HOUR_BEGIN, 0, 0);
            break;
        case TIME_DAY:
            FakeRtc_ForwardTimeTo(DAY_HOUR_BEGIN, 0, 0);
            break;
        case TIME_EVENING:
            FakeRtc_ForwardTimeTo(EVENING_HOUR_BEGIN, 0, 0);
            break;
        case TIME_NIGHT:
            FakeRtc_ForwardTimeTo(NIGHT_HOUR_BEGIN, 0, 0);
            break;
    }
    Debug_DestroyMenu_Full(taskId);
    SetMainCallback2(CB2_LoadMap);
}

static void DebugAction_TimeMenu_ChangeWeekdays(u8 taskId)
{
    u32 input = ListMenu_ProcessInput(gTasks[taskId].tMenuTaskId);
    struct SiiRtcInfo *rtc = FakeRtc_GetCurrentTime();
    u32 daysToAdd = 0;

    DebugAction_DestroyExtraWindow(taskId);
    daysToAdd = ((input - rtc->dayOfWeek) + WEEKDAY_COUNT) % WEEKDAY_COUNT;
    FakeRtc_AdvanceTimeBy(daysToAdd, 0, 0, 0);
    Debug_DestroyMenu_Full(taskId);
    SetMainCallback2(CB2_LoadMap);
}

// *******************************
// Actions PCBag

static void DebugAction_PCBag_Fill_PCBoxes_Fast(u8 taskId) //Credit: Sierraffinity
{
    int boxId, boxPosition;
    u32 personality;
    struct BoxPokemon boxMon;
    u16 species = SPECIES_BULBASAUR;
    u8 speciesName[POKEMON_NAME_LENGTH + 1];

    personality = Random32();

    CreateBoxMon(&boxMon, species, 100, USE_RANDOM_IVS, FALSE, personality, OT_ID_PLAYER_ID, 0);

    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPosition = 0; boxPosition < IN_BOX_COUNT; boxPosition++, species++)
        {
            if (!GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_HAS_SPECIES))
            {
                StringCopy(speciesName, GetSpeciesName(species));
                SetBoxMonData(&boxMon, MON_DATA_NICKNAME, &speciesName);
                SetBoxMonData(&boxMon, MON_DATA_SPECIES, &species);
                GiveBoxMonInitialMoveset(&boxMon);
                gPokemonStoragePtr->boxes[boxId][boxPosition] = boxMon;
            }
        }
    }

    // Set flag for user convenience
    FlagSet(FLAG_SYS_POKEMON_GET);
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

static void DebugAction_PCBag_Fill_PCBoxes_Slow(u8 taskId)
{
    int boxId, boxPosition;
    struct BoxPokemon boxMon;
    u32 species = SPECIES_BULBASAUR;
    bool8 spaceAvailable = FALSE;

    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPosition = 0; boxPosition < IN_BOX_COUNT; boxPosition++)
        {
            if (!GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_HAS_SPECIES))
            {
                if (!spaceAvailable)
                    PlayBGM(MUS_RG_MYSTERY_GIFT);
                CreateBoxMon(&boxMon, species, 100, USE_RANDOM_IVS, FALSE, 0, OT_ID_PLAYER_ID, 0);
                gPokemonStoragePtr->boxes[boxId][boxPosition] = boxMon;
                species = (species < NUM_SPECIES - 1) ? species + 1 : 1;
                spaceAvailable = TRUE;
            }
        }
    }

    // Set flag for user convenience
    FlagSet(FLAG_SYS_POKEMON_GET);
    if (spaceAvailable)
        PlayBGM(GetCurrentMapMusic());

    Debug_DestroyMenu_Full_Script(taskId, Debug_BoxFilledMessage);
}

static void DebugAction_PCBag_Fill_PCItemStorage(u8 taskId)
{
    u16 itemId;

    for (itemId = 1; itemId < ITEMS_COUNT; itemId++)
    {
        if (!CheckPCHasItem(itemId, MAX_PC_ITEM_CAPACITY))
            AddPCItem(itemId, MAX_PC_ITEM_CAPACITY);
    }
}

static void DebugAction_PCBag_Fill_PocketItems(u8 taskId)
{
    u16 itemId;

    for (itemId = 1; itemId < ITEMS_COUNT; itemId++)
    {
        if (GetItemPocket(itemId) == POCKET_ITEMS && CheckBagHasSpace(itemId, MAX_BAG_ITEM_CAPACITY))
            AddBagItem(itemId, MAX_BAG_ITEM_CAPACITY);
    }
}

static void DebugAction_PCBag_Fill_PocketPokeBalls(u8 taskId)
{
    for (enum PokeBall ballId = BALL_STRANGE; ballId < POKEBALL_COUNT; ballId++)
    {
        if (CheckBagHasSpace(ballId, MAX_BAG_ITEM_CAPACITY))
            AddBagItem(gBallItemIds[ballId], MAX_BAG_ITEM_CAPACITY);
    }
}

static void DebugAction_PCBag_Fill_PocketTMHM(u8 taskId)
{
    u16 index, itemId;

    for (index = 0; index < NUM_ALL_MACHINES; index++)
    {
        itemId = GetTMHMItemId(index + 1);
        if (CheckBagHasSpace(itemId, 1) && ItemIdToBattleMoveId(itemId) != MOVE_NONE)
            AddBagItem(itemId, 1);
    }
}

static void DebugAction_PCBag_Fill_PocketBerries(u8 taskId)
{
    u16 itemId;

    for (itemId = FIRST_BERRY_INDEX; itemId < LAST_BERRY_INDEX; itemId++)
    {
        if (CheckBagHasSpace(itemId, MAX_BAG_ITEM_CAPACITY))
            AddBagItem(itemId, MAX_BAG_ITEM_CAPACITY);
    }
}

static void DebugAction_PCBag_Fill_PocketKeyItems(u8 taskId)
{
    u16 itemId;

    for (itemId = 1; itemId < ITEMS_COUNT; itemId++)
    {
        if (GetItemPocket(itemId) == POCKET_KEY_ITEMS && CheckBagHasSpace(itemId, 1))
            AddBagItem(itemId, 1);
    }
}

static void DebugAction_PCBag_ClearBag(u8 taskId)
{
    PlaySE(MUS_LEVEL_UP);
    ClearBag();
}

static void DebugAction_PCBag_ClearBoxes(u8 taskId)
{
    ResetPokemonStorageSystem();
    Debug_DestroyMenu_Full(taskId);
    ScriptContext_Enable();
}

// *******************************
// Actions Sound
static const u8 *const sBGMNames[END_MUS - START_MUS + 1];
static const u8 *const sSENames[END_SE + 1];

#define tCurrentSong  data[5]

static void DebugAction_Sound_SE(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateSound);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial sound effect
    StringCopy(gStringVar2, gText_DigitIndicator[0]);
    ConvertIntToDecimalStringN(gStringVar3, 1, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
    StringCopyPadded(gStringVar1, sSENames[0], CHAR_SPACE, 35);
    StringExpandPlaceholders(gStringVar4, sDebugText_Sound_SFX_ID);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

    StopMapMusic(); //Stop map music to better hear sounds

    gTasks[taskId].func = DebugAction_Sound_SE_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = 1;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tCurrentSong = gTasks[taskId].tInput;
}

static void DebugAction_Sound_SE_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        const u8 *seName;
        Debug_HandleInput_Numeric(taskId, 1, END_SE, DEBUG_NUMBER_DIGITS_ITEMS);

        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);
        seName = sSENames[gTasks[taskId].tInput - 1];
        if (seName == NULL)
            seName = sDebugText_Dashes;
        StringCopyPadded(gStringVar1, seName, CHAR_SPACE, 35);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
        StringExpandPlaceholders(gStringVar4, sDebugText_Sound_SFX_ID);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        m4aSongNumStop(gTasks[taskId].tCurrentSong);
        gTasks[taskId].tCurrentSong = gTasks[taskId].tInput;
        m4aSongNumStart(gTasks[taskId].tInput);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        m4aSongNumStop(gTasks[taskId].tCurrentSong);
        DebugAction_DestroyExtraWindow(taskId);
    }
    else if (JOY_NEW(START_BUTTON))
    {
        m4aSongNumStop(gTasks[taskId].tCurrentSong);
    }
}

static void DebugAction_Sound_MUS(u8 taskId)
{
    u8 windowId;

    ClearStdWindowAndFrame(gTasks[taskId].tWindowId, TRUE);
    RemoveWindow(gTasks[taskId].tWindowId);

    HideMapNamePopUpWindow();
    LoadMessageBoxAndBorderGfx();
    windowId = AddWindow(&sDebugMenuWindowTemplateSound);
    DrawStdWindowFrame(windowId, FALSE);

    CopyWindowToVram(windowId, COPYWIN_FULL);

    // Display initial song
    StringCopy(gStringVar2, gText_DigitIndicator[0]);
    ConvertIntToDecimalStringN(gStringVar3, START_MUS, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
    StringCopyPadded(gStringVar1, sBGMNames[0], CHAR_SPACE, 35);
    StringExpandPlaceholders(gStringVar4, sDebugText_Sound_Music_ID);
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);

    StopMapMusic(); //Stop map music to better hear new music

    gTasks[taskId].func = DebugAction_Sound_MUS_SelectId;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tInput = START_MUS;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tCurrentSong = gTasks[taskId].tInput;
}

static void DebugAction_Sound_MUS_SelectId(u8 taskId)
{
    if (JOY_NEW(DPAD_ANY))
    {
        const u8 *bgmName;
        Debug_HandleInput_Numeric(taskId, START_MUS, END_MUS, DEBUG_NUMBER_DIGITS_ITEMS);

        StringCopy(gStringVar2, gText_DigitIndicator[gTasks[taskId].tDigit]);
        bgmName = sBGMNames[gTasks[taskId].tInput - START_MUS];
        if (bgmName == NULL)
            bgmName = sDebugText_Dashes;
        StringCopyPadded(gStringVar1, bgmName, CHAR_SPACE, 35);
        ConvertIntToDecimalStringN(gStringVar3, gTasks[taskId].tInput, STR_CONV_MODE_LEADING_ZEROS, DEBUG_NUMBER_DIGITS_ITEMS);
        StringExpandPlaceholders(gStringVar4, sDebugText_Sound_Music_ID);
        AddTextPrinterParameterized(gTasks[taskId].tSubWindowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
    }

    if (JOY_NEW(A_BUTTON))
    {
        m4aSongNumStop(gTasks[taskId].tCurrentSong);
        gTasks[taskId].tCurrentSong = gTasks[taskId].tInput;
        m4aSongNumStart(gTasks[taskId].tInput);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        // m4aSongNumStop(gTasks[taskId].tCurrentSong);   //Uncomment if music should stop after leaving menu
        DebugAction_DestroyExtraWindow(taskId);
    }
    else if (JOY_NEW(START_BUTTON))
    {
        m4aSongNumStop(gTasks[taskId].tCurrentSong);
    }
}

static const u32 gDebugFollowerNPCGraphics[] =
{
    OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL,
    OBJ_EVENT_GFX_RIVAL_MAY_NORMAL,
    OBJ_EVENT_GFX_STEVEN,
    OBJ_EVENT_GFX_WALLY,
    OBJ_EVENT_GFX_RED,
    OBJ_EVENT_GFX_LEAF,
};

static void DebugAction_CreateFollowerNPC(u8 taskId)
{
    u32 input = ListMenu_ProcessInput(gTasks[taskId].tMenuTaskId);
    u32 gfx = gDebugFollowerNPCGraphics[input];

    Debug_DestroyMenu_Full(taskId);
    LockPlayerFieldControls();
    DestroyFollowerNPC();
    SetFollowerNPCData(FNPC_DATA_BATTLE_PARTNER, PARTNER_STEVEN);
    CreateFollowerNPC(gfx, FNPC_ALL, Debug_Follower_NPC_Event_Script);
    UnlockPlayerFieldControls();
}

static void DebugAction_DestroyFollowerNPC(u8 taskId)
{
    if (FNPC_ENABLE_NPC_FOLLOWERS)
    {
        Debug_DestroyMenu_Full(taskId);
        LockPlayerFieldControls();
        DestroyFollowerNPC();
        UnlockPlayerFieldControls();
    }
    else
    {
        Debug_DestroyMenu_Full_Script(taskId, Debug_Follower_NPC_Not_Enabled);
    }
}

#undef tCurrentSong


#define SOUND_LIST_BGM              \
    X(MUS_LITTLEROOT_TEST)          \
    X(MUS_GSC_ROUTE38)              \
    X(MUS_CAUGHT)                   \
    X(MUS_VICTORY_WILD)             \
    X(MUS_VICTORY_GYM_LEADER)       \
    X(MUS_VICTORY_LEAGUE)           \
    X(MUS_C_COMM_CENTER)            \
    X(MUS_GSC_PEWTER)               \
    X(MUS_C_VS_LEGEND_BEAST)        \
    X(MUS_ROUTE101)                 \
    X(MUS_ROUTE110)                 \
    X(MUS_ROUTE120)                 \
    X(MUS_PETALBURG)                \
    X(MUS_OLDALE)                   \
    X(MUS_GYM)                      \
    X(MUS_SURF)                     \
    X(MUS_PETALBURG_WOODS)          \
    X(MUS_LEVEL_UP)                 \
    X(MUS_HEAL)                     \
    X(MUS_OBTAIN_BADGE)             \
    X(MUS_OBTAIN_ITEM)              \
    X(MUS_EVOLVED)                  \
    X(MUS_OBTAIN_TMHM)              \
    X(MUS_LILYCOVE_MUSEUM)          \
    X(MUS_ROUTE122)                 \
    X(MUS_OCEANIC_MUSEUM)           \
    X(MUS_EVOLUTION_INTRO)          \
    X(MUS_EVOLUTION)                \
    X(MUS_MOVE_DELETED)             \
    X(MUS_ENCOUNTER_GIRL)           \
    X(MUS_ENCOUNTER_MALE)           \
    X(MUS_ABANDONED_SHIP)           \
    X(MUS_FORTREE)                  \
    X(MUS_BIRCH_LAB)                \
    X(MUS_B_TOWER_RS)               \
    X(MUS_ENCOUNTER_SWIMMER)        \
    X(MUS_CAVE_OF_ORIGIN)           \
    X(MUS_OBTAIN_BERRY)             \
    X(MUS_AWAKEN_LEGEND)            \
    X(MUS_SLOTS_JACKPOT)            \
    X(MUS_SLOTS_WIN)                \
    X(MUS_TOO_BAD)                  \
    X(MUS_ROULETTE)                 \
    X(MUS_LINK_CONTEST_P1)          \
    X(MUS_LINK_CONTEST_P2)          \
    X(MUS_LINK_CONTEST_P3)          \
    X(MUS_LINK_CONTEST_P4)          \
    X(MUS_ENCOUNTER_RICH)           \
    X(MUS_VERDANTURF)               \
    X(MUS_RUSTBORO)                 \
    X(MUS_POKE_CENTER)              \
    X(MUS_ROUTE104)                 \
    X(MUS_ROUTE119)                 \
    X(MUS_CYCLING)                  \
    X(MUS_POKE_MART)                \
    X(MUS_LITTLEROOT)               \
    X(MUS_MT_CHIMNEY)               \
    X(MUS_ENCOUNTER_FEMALE)         \
    X(MUS_LILYCOVE)                 \
    X(MUS_DESERT)                   \
    X(MUS_HELP)                     \
    X(MUS_UNDERWATER)               \
    X(MUS_VICTORY_TRAINER)          \
    X(MUS_TITLE)                    \
    X(MUS_INTRO)                    \
    X(MUS_ENCOUNTER_MAY)            \
    X(MUS_ENCOUNTER_INTENSE)        \
    X(MUS_ENCOUNTER_COOL)           \
    X(MUS_ROUTE113)                 \
    X(MUS_ENCOUNTER_AQUA)           \
    X(MUS_FOLLOW_ME)                \
    X(MUS_ENCOUNTER_BRENDAN)        \
    X(MUS_EVER_GRANDE)              \
    X(MUS_ENCOUNTER_SUSPICIOUS)     \
    X(MUS_VICTORY_AQUA_MAGMA)       \
    X(MUS_CABLE_CAR)                \
    X(MUS_GAME_CORNER)              \
    X(MUS_DEWFORD)                  \
    X(MUS_SAFARI_ZONE)              \
    X(MUS_VICTORY_ROAD)             \
    X(MUS_AQUA_MAGMA_HIDEOUT)       \
    X(MUS_SAILING)                  \
    X(MUS_MT_PYRE)                  \
    X(MUS_SLATEPORT)                \
    X(MUS_MT_PYRE_EXTERIOR)         \
    X(MUS_SCHOOL)                   \
    X(MUS_HALL_OF_FAME)             \
    X(MUS_FALLARBOR)                \
    X(MUS_SEALED_CHAMBER)           \
    X(MUS_CONTEST_WINNER)           \
    X(MUS_CONTEST)                  \
    X(MUS_ENCOUNTER_MAGMA)          \
    X(MUS_INTRO_BATTLE)             \
    X(MUS_ABNORMAL_WEATHER)         \
    X(MUS_WEATHER_GROUDON)          \
    X(MUS_SOOTOPOLIS)               \
    X(MUS_CONTEST_RESULTS)          \
    X(MUS_HALL_OF_FAME_ROOM)        \
    X(MUS_TRICK_HOUSE)              \
    X(MUS_ENCOUNTER_TWINS)          \
    X(MUS_ENCOUNTER_ELITE_FOUR)     \
    X(MUS_ENCOUNTER_HIKER)          \
    X(MUS_CONTEST_LOBBY)            \
    X(MUS_ENCOUNTER_INTERVIEWER)    \
    X(MUS_ENCOUNTER_CHAMPION)       \
    X(MUS_CREDITS)                  \
    X(MUS_END)                      \
    X(MUS_B_FRONTIER)               \
    X(MUS_B_ARENA)                  \
    X(MUS_OBTAIN_B_POINTS)          \
    X(MUS_REGISTER_MATCH_CALL)      \
    X(MUS_B_PYRAMID)                \
    X(MUS_B_PYRAMID_TOP)            \
    X(MUS_B_PALACE)                 \
    X(MUS_RAYQUAZA_APPEARS)         \
    X(MUS_B_TOWER)                  \
    X(MUS_OBTAIN_SYMBOL)            \
    X(MUS_B_DOME)                   \
    X(MUS_B_PIKE)                   \
    X(MUS_B_FACTORY)                \
    X(MUS_VS_RAYQUAZA)              \
    X(MUS_VS_FRONTIER_BRAIN)        \
    X(MUS_VS_MEW)                   \
    X(MUS_B_DOME_LOBBY)             \
    X(MUS_VS_WILD)                  \
    X(MUS_VS_AQUA_MAGMA)            \
    X(MUS_VS_TRAINER)               \
    X(MUS_VS_GYM_LEADER)            \
    X(MUS_VS_CHAMPION)              \
    X(MUS_VS_REGI)                  \
    X(MUS_VS_KYOGRE_GROUDON)        \
    X(MUS_VS_RIVAL)                 \
    X(MUS_VS_ELITE_FOUR)            \
    X(MUS_VS_AQUA_MAGMA_LEADER)     \
    X(MUS_RG_FOLLOW_ME)             \
    X(MUS_RG_GAME_CORNER)           \
    X(MUS_RG_ROCKET_HIDEOUT)        \
    X(MUS_RG_GYM)                   \
    X(MUS_RG_JIGGLYPUFF)            \
    X(MUS_RG_INTRO_FIGHT)           \
    X(MUS_RG_TITLE)                 \
    X(MUS_RG_CINNABAR)              \
    X(MUS_RG_LAVENDER)              \
    X(MUS_RG_HEAL)                  \
    X(MUS_RG_CYCLING)               \
    X(MUS_RG_ENCOUNTER_ROCKET)      \
    X(MUS_RG_ENCOUNTER_GIRL)        \
    X(MUS_RG_ENCOUNTER_BOY)         \
    X(MUS_RG_HALL_OF_FAME)          \
    X(MUS_RG_VIRIDIAN_FOREST)       \
    X(MUS_RG_MT_MOON)               \
    X(MUS_RG_POKE_MANSION)          \
    X(MUS_RG_CREDITS)               \
    X(MUS_RG_ROUTE1)                \
    X(MUS_RG_ROUTE24)               \
    X(MUS_RG_ROUTE3)                \
    X(MUS_RG_ROUTE11)               \
    X(MUS_RG_VICTORY_ROAD)          \
    X(MUS_RG_VS_GYM_LEADER)         \
    X(MUS_RG_VS_TRAINER)            \
    X(MUS_RG_VS_WILD)               \
    X(MUS_RG_VS_CHAMPION)           \
    X(MUS_RG_PALLET)                \
    X(MUS_RG_OAK_LAB)               \
    X(MUS_RG_OAK)                   \
    X(MUS_RG_POKE_CENTER)           \
    X(MUS_RG_SS_ANNE)               \
    X(MUS_RG_SURF)                  \
    X(MUS_RG_POKE_TOWER)            \
    X(MUS_RG_SILPH)                 \
    X(MUS_RG_FUCHSIA)               \
    X(MUS_RG_CELADON)               \
    X(MUS_RG_VICTORY_TRAINER)       \
    X(MUS_RG_VICTORY_WILD)          \
    X(MUS_RG_VICTORY_GYM_LEADER)    \
    X(MUS_RG_VERMILLION)            \
    X(MUS_RG_PEWTER)                \
    X(MUS_RG_ENCOUNTER_RIVAL)       \
    X(MUS_RG_RIVAL_EXIT)            \
    X(MUS_RG_DEX_RATING)            \
    X(MUS_RG_OBTAIN_KEY_ITEM)       \
    X(MUS_RG_CAUGHT_INTRO)          \
    X(MUS_RG_PHOTO)                 \
    X(MUS_RG_GAME_FREAK)            \
    X(MUS_RG_CAUGHT)                \
    X(MUS_RG_NEW_GAME_INSTRUCT)     \
    X(MUS_RG_NEW_GAME_INTRO)        \
    X(MUS_RG_NEW_GAME_EXIT)         \
    X(MUS_RG_POKE_JUMP)             \
    X(MUS_RG_UNION_ROOM)            \
    X(MUS_RG_NET_CENTER)            \
    X(MUS_RG_MYSTERY_GIFT)          \
    X(MUS_RG_BERRY_PICK)            \
    X(MUS_RG_SEVII_CAVE)            \
    X(MUS_RG_TEACHY_TV_SHOW)        \
    X(MUS_RG_SEVII_ROUTE)           \
    X(MUS_RG_SEVII_DUNGEON)         \
    X(MUS_RG_SEVII_123)             \
    X(MUS_RG_SEVII_45)              \
    X(MUS_RG_SEVII_67)              \
    X(MUS_RG_POKE_FLUTE)            \
    X(MUS_RG_VS_DEOXYS)             \
    X(MUS_RG_VS_MEWTWO)             \
    X(MUS_RG_VS_LEGEND)             \
    X(MUS_RG_ENCOUNTER_GYM_LEADER)  \
    X(MUS_RG_ENCOUNTER_DEOXYS)      \
    X(MUS_RG_TRAINER_TOWER)         \
    X(MUS_RG_SLOW_PALLET)           \
    X(MUS_RG_TEACHY_TV_MENU)

#define SOUND_LIST_SE               \
    X(SE_USE_ITEM)                  \
    X(SE_PC_LOGIN)                  \
    X(SE_PC_OFF)                    \
    X(SE_PC_ON)                     \
    X(SE_SELECT)                    \
    X(SE_WIN_OPEN)                  \
    X(SE_WALL_HIT)                  \
    X(SE_DOOR)                      \
    X(SE_EXIT)                      \
    X(SE_LEDGE)                     \
    X(SE_BIKE_BELL)                 \
    X(SE_NOT_EFFECTIVE)             \
    X(SE_EFFECTIVE)                 \
    X(SE_SUPER_EFFECTIVE)           \
    X(SE_BALL_OPEN)                 \
    X(SE_FAINT)                     \
    X(SE_FLEE)                      \
    X(SE_SLIDING_DOOR)              \
    X(SE_SHIP)                      \
    X(SE_BANG)                      \
    X(SE_PIN)                       \
    X(SE_BOO)                       \
    X(SE_BALL)                      \
    X(SE_CONTEST_PLACE)             \
    X(SE_A)                         \
    X(SE_I)                         \
    X(SE_U)                         \
    X(SE_E)                         \
    X(SE_O)                         \
    X(SE_N)                         \
    X(SE_SUCCESS)                   \
    X(SE_FAILURE)                   \
    X(SE_EXP)                       \
    X(SE_BIKE_HOP)                  \
    X(SE_SWITCH)                    \
    X(SE_CLICK)                     \
    X(SE_FU_ZAKU)                   \
    X(SE_CONTEST_CONDITION_LOSE)    \
    X(SE_LAVARIDGE_FALL_WARP)       \
    X(SE_ICE_STAIRS)                \
    X(SE_ICE_BREAK)                 \
    X(SE_ICE_CRACK)                 \
    X(SE_FALL)                      \
    X(SE_UNLOCK)                    \
    X(SE_WARP_IN)                   \
    X(SE_WARP_OUT)                  \
    X(SE_REPEL)                     \
    X(SE_ROTATING_GATE)             \
    X(SE_TRUCK_MOVE)                \
    X(SE_TRUCK_STOP)                \
    X(SE_TRUCK_UNLOAD)              \
    X(SE_TRUCK_DOOR)                \
    X(SE_BERRY_BLENDER)             \
    X(SE_CARD)                      \
    X(SE_SAVE)                      \
    X(SE_BALL_BOUNCE_1)             \
    X(SE_BALL_BOUNCE_2)             \
    X(SE_BALL_BOUNCE_3)             \
    X(SE_BALL_BOUNCE_4)             \
    X(SE_BALL_TRADE)                \
    X(SE_BALL_THROW)                \
    X(SE_NOTE_C)                    \
    X(SE_NOTE_D)                    \
    X(SE_NOTE_E)                    \
    X(SE_NOTE_F)                    \
    X(SE_NOTE_G)                    \
    X(SE_NOTE_A)                    \
    X(SE_NOTE_B)                    \
    X(SE_NOTE_C_HIGH)               \
    X(SE_PUDDLE)                    \
    X(SE_BRIDGE_WALK)               \
    X(SE_ITEMFINDER)                \
    X(SE_DING_DONG)                 \
    X(SE_BALLOON_RED)               \
    X(SE_BALLOON_BLUE)              \
    X(SE_BALLOON_YELLOW)            \
    X(SE_BREAKABLE_DOOR)            \
    X(SE_MUD_BALL)                  \
    X(SE_FIELD_POISON)              \
    X(SE_ESCALATOR)                 \
    X(SE_THUNDERSTORM)              \
    X(SE_THUNDERSTORM_STOP)         \
    X(SE_DOWNPOUR)                  \
    X(SE_DOWNPOUR_STOP)             \
    X(SE_RAIN)                      \
    X(SE_RAIN_STOP)                 \
    X(SE_THUNDER)                   \
    X(SE_THUNDER2)                  \
    X(SE_ELEVATOR)                  \
    X(SE_LOW_HEALTH)                \
    X(SE_EXP_MAX)                   \
    X(SE_ROULETTE_BALL)             \
    X(SE_ROULETTE_BALL2)            \
    X(SE_TAILLOW_WING_FLAP)         \
    X(SE_SHOP)                      \
    X(SE_CONTEST_HEART)             \
    X(SE_CONTEST_CURTAIN_RISE)      \
    X(SE_CONTEST_CURTAIN_FALL)      \
    X(SE_CONTEST_ICON_CHANGE)       \
    X(SE_CONTEST_ICON_CLEAR)        \
    X(SE_CONTEST_MONS_TURN)         \
    X(SE_SHINY)                     \
    X(SE_INTRO_BLAST)               \
    X(SE_MUGSHOT)                   \
    X(SE_APPLAUSE)                  \
    X(SE_VEND)                      \
    X(SE_ORB)                       \
    X(SE_DEX_SCROLL)                \
    X(SE_DEX_PAGE)                  \
    X(SE_POKENAV_ON)                \
    X(SE_POKENAV_OFF)               \
    X(SE_DEX_SEARCH)                \
    X(SE_EGG_HATCH)                 \
    X(SE_BALL_TRAY_ENTER)           \
    X(SE_BALL_TRAY_BALL)            \
    X(SE_BALL_TRAY_EXIT)            \
    X(SE_GLASS_FLUTE)               \
    X(SE_M_THUNDERBOLT)             \
    X(SE_M_THUNDERBOLT2)            \
    X(SE_M_HARDEN)                  \
    X(SE_M_NIGHTMARE)               \
    X(SE_M_VITAL_THROW)             \
    X(SE_M_VITAL_THROW2)            \
    X(SE_M_BUBBLE)                  \
    X(SE_M_BUBBLE2)                 \
    X(SE_M_BUBBLE3)                 \
    X(SE_M_RAIN_DANCE)              \
    X(SE_M_CUT)                     \
    X(SE_M_STRING_SHOT)             \
    X(SE_M_STRING_SHOT2)            \
    X(SE_M_ROCK_THROW)              \
    X(SE_M_GUST)                    \
    X(SE_M_GUST2)                   \
    X(SE_M_DOUBLE_SLAP)             \
    X(SE_M_DOUBLE_TEAM)             \
    X(SE_M_RAZOR_WIND)              \
    X(SE_M_ICY_WIND)                \
    X(SE_M_THUNDER_WAVE)            \
    X(SE_M_COMET_PUNCH)             \
    X(SE_M_MEGA_KICK)               \
    X(SE_M_MEGA_KICK2)              \
    X(SE_M_CRABHAMMER)              \
    X(SE_M_JUMP_KICK)               \
    X(SE_M_FLAME_WHEEL)             \
    X(SE_M_FLAME_WHEEL2)            \
    X(SE_M_FLAMETHROWER)            \
    X(SE_M_FIRE_PUNCH)              \
    X(SE_M_TOXIC)                   \
    X(SE_M_SACRED_FIRE)             \
    X(SE_M_SACRED_FIRE2)            \
    X(SE_M_EMBER)                   \
    X(SE_M_TAKE_DOWN)               \
    X(SE_M_BLIZZARD)                \
    X(SE_M_BLIZZARD2)               \
    X(SE_M_SCRATCH)                 \
    X(SE_M_VICEGRIP)                \
    X(SE_M_WING_ATTACK)             \
    X(SE_M_FLY)                     \
    X(SE_M_SAND_ATTACK)             \
    X(SE_M_RAZOR_WIND2)             \
    X(SE_M_BITE)                    \
    X(SE_M_HEADBUTT)                \
    X(SE_M_SURF)                    \
    X(SE_M_HYDRO_PUMP)              \
    X(SE_M_WHIRLPOOL)               \
    X(SE_M_HORN_ATTACK)             \
    X(SE_M_TAIL_WHIP)               \
    X(SE_M_MIST)                    \
    X(SE_M_POISON_POWDER)           \
    X(SE_M_BIND)                    \
    X(SE_M_DRAGON_RAGE)             \
    X(SE_M_SING)                    \
    X(SE_M_PERISH_SONG)             \
    X(SE_M_PAY_DAY)                 \
    X(SE_M_DIG)                     \
    X(SE_M_DIZZY_PUNCH)             \
    X(SE_M_SELF_DESTRUCT)           \
    X(SE_M_EXPLOSION)               \
    X(SE_M_ABSORB_2)                \
    X(SE_M_ABSORB)                  \
    X(SE_M_SCREECH)                 \
    X(SE_M_BUBBLE_BEAM)             \
    X(SE_M_BUBBLE_BEAM2)            \
    X(SE_M_SUPERSONIC)              \
    X(SE_M_BELLY_DRUM)              \
    X(SE_M_METRONOME)               \
    X(SE_M_BONEMERANG)              \
    X(SE_M_LICK)                    \
    X(SE_M_PSYBEAM)                 \
    X(SE_M_FAINT_ATTACK)            \
    X(SE_M_SWORDS_DANCE)            \
    X(SE_M_LEER)                    \
    X(SE_M_SWAGGER)                 \
    X(SE_M_SWAGGER2)                \
    X(SE_M_HEAL_BELL)               \
    X(SE_M_CONFUSE_RAY)             \
    X(SE_M_SNORE)                   \
    X(SE_M_BRICK_BREAK)             \
    X(SE_M_GIGA_DRAIN)              \
    X(SE_M_PSYBEAM2)                \
    X(SE_M_SOLAR_BEAM)              \
    X(SE_M_PETAL_DANCE)             \
    X(SE_M_TELEPORT)                \
    X(SE_M_MINIMIZE)                \
    X(SE_M_SKETCH)                  \
    X(SE_M_SWIFT)                   \
    X(SE_M_REFLECT)                 \
    X(SE_M_BARRIER)                 \
    X(SE_M_DETECT)                  \
    X(SE_M_LOCK_ON)                 \
    X(SE_M_MOONLIGHT)               \
    X(SE_M_CHARM)                   \
    X(SE_M_CHARGE)                  \
    X(SE_M_STRENGTH)                \
    X(SE_M_HYPER_BEAM)              \
    X(SE_M_WATERFALL)               \
    X(SE_M_REVERSAL)                \
    X(SE_M_ACID_ARMOR)              \
    X(SE_M_SANDSTORM)               \
    X(SE_M_TRI_ATTACK)              \
    X(SE_M_TRI_ATTACK2)             \
    X(SE_M_ENCORE)                  \
    X(SE_M_ENCORE2)                 \
    X(SE_M_BATON_PASS)              \
    X(SE_M_MILK_DRINK)              \
    X(SE_M_ATTRACT)                 \
    X(SE_M_ATTRACT2)                \
    X(SE_M_MORNING_SUN)             \
    X(SE_M_FLATTER)                 \
    X(SE_M_SAND_TOMB)               \
    X(SE_M_GRASSWHISTLE)            \
    X(SE_M_SPIT_UP)                 \
    X(SE_M_DIVE)                    \
    X(SE_M_EARTHQUAKE)              \
    X(SE_M_TWISTER)                 \
    X(SE_M_SWEET_SCENT)             \
    X(SE_M_YAWN)                    \
    X(SE_M_SKY_UPPERCUT)            \
    X(SE_M_STAT_INCREASE)           \
    X(SE_M_HEAT_WAVE)               \
    X(SE_M_UPROAR)                  \
    X(SE_M_HAIL)                    \
    X(SE_M_COSMIC_POWER)            \
    X(SE_M_TEETER_DANCE)            \
    X(SE_M_STAT_DECREASE)           \
    X(SE_M_HAZE)                    \
    X(SE_M_HYPER_BEAM2)             \
    X(SE_RG_DOOR)                   \
    X(SE_RG_CARD_FLIP)              \
    X(SE_RG_CARD_FLIPPING)          \
    X(SE_RG_CARD_OPEN)              \
    X(SE_RG_BAG_CURSOR)             \
    X(SE_RG_BAG_POCKET)             \
    X(SE_RG_BALL_CLICK)             \
    X(SE_RG_SHOP)                   \
    X(SE_RG_SS_ANNE_HORN)           \
    X(SE_RG_HELP_OPEN)              \
    X(SE_RG_HELP_CLOSE)             \
    X(SE_RG_HELP_ERROR)             \
    X(SE_RG_DEOXYS_MOVE)            \
    X(SE_RG_POKE_JUMP_SUCCESS)      \
    X(SE_RG_POKE_JUMP_FAILURE)      \
    X(SE_POKENAV_CALL)              \
    X(SE_POKENAV_HANG_UP)           \
    X(SE_ARENA_TIMEUP1)             \
    X(SE_ARENA_TIMEUP2)             \
    X(SE_PIKE_CURTAIN_CLOSE)        \
    X(SE_PIKE_CURTAIN_OPEN)         \
    X(SE_SUDOWOODO_SHAKE)

// Create BGM list
#define X(songId) static const u8 sBGMName_##songId[] = _(#songId);
SOUND_LIST_BGM
#undef X

#define X(songId) [songId - START_MUS] = sBGMName_##songId,
static const u8 *const sBGMNames[END_MUS - START_MUS + 1] =
{
SOUND_LIST_BGM
};
#undef X

// Create SE list
#define X(songId) static const u8 sSEName_##songId[] = _(#songId);
SOUND_LIST_SE
#undef X

#define X(songId) [songId - 1] = sSEName_##songId,
static const u8 *const sSENames[END_SE + 1] =
{
SOUND_LIST_SE
};
#undef X

// *******************************
// Actions BerryFunctions

static void DebugAction_BerryFunctions_ClearAll(u8 taskId)
{
    u8 i;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (gObjectEvents[i].movementType == MOVEMENT_TYPE_BERRY_TREE_GROWTH)
        {
            RemoveBerryTree(GetObjectEventBerryTreeId(i));
            SetBerryTreeJustPicked(gObjectEvents[i].localId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
        }
    }

    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_BerryFunctions_Ready(u8 taskId)
{
    u8 i;
    struct BerryTree *tree;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (gObjectEvents[i].movementType == MOVEMENT_TYPE_BERRY_TREE_GROWTH)
        {
            tree = &gSaveBlock1Ptr->berryTrees[GetObjectEventBerryTreeId(i)];
            if (tree->stage != BERRY_STAGE_NO_BERRY)
            {
                tree->stage = BERRY_STAGE_BERRIES - 1;
                BerryTreeGrow(tree);
            }
        }
    }

    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_BerryFunctions_NextStage(u8 taskId)
{
    u8 i;
    struct BerryTree *tree;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (gObjectEvents[i].movementType == MOVEMENT_TYPE_BERRY_TREE_GROWTH)
        {
            tree = &gSaveBlock1Ptr->berryTrees[GetObjectEventBerryTreeId(i)];
            BerryTreeGrow(tree);
        }
    }

    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_BerryFunctions_Pests(u8 taskId)
{
    u8 i;

    if (!OW_BERRY_PESTS)
    {
        Debug_DestroyMenu_Full_Script(taskId, Debug_BerryPestsDisabled);
        return;
    }

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (gObjectEvents[i].movementType == MOVEMENT_TYPE_BERRY_TREE_GROWTH)
        {
            if (gSaveBlock1Ptr->berryTrees[GetObjectEventBerryTreeId(i)].stage != BERRY_STAGE_PLANTED)
                gSaveBlock1Ptr->berryTrees[GetObjectEventBerryTreeId(i)].pests = TRUE;
        }
    }

    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_BerryFunctions_Weeds(u8 taskId)
{
    u8 i;

    if (!OW_BERRY_WEEDS)
    {
        Debug_DestroyMenu_Full_Script(taskId, Debug_BerryWeedsDisabled);
        return;
    }

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (gObjectEvents[i].movementType == MOVEMENT_TYPE_BERRY_TREE_GROWTH)
        {
            gSaveBlock1Ptr->berryTrees[GetObjectEventBerryTreeId(i)].weeds = TRUE;
        }
    }

    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

// *******************************
// Actions Party/Boxes

static void DebugAction_Party_HealParty(u8 taskId)
{
    PlaySE(SE_USE_ITEM);
    HealPlayerParty();
    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

void DebugNative_GetAbilityNames(void)
{
    u32 species = GetMonData(&gPlayerParty[gSpecialVar_0x8004], MON_DATA_SPECIES);
    StringCopy(gStringVar1, gAbilitiesInfo[GetAbilityBySpecies(species, 0)].name);
    StringCopy(gStringVar2, gAbilitiesInfo[GetAbilityBySpecies(species, 1)].name);
    StringCopy(gStringVar3, gAbilitiesInfo[GetAbilityBySpecies(species, 2)].name);
}

#define tPartyId               data[5]
#define tFriendship            data[6]

static void Debug_Display_FriendshipInfo(s32 oldFriendship, s32 newFriendship, u32 digit, u8 windowId)
{
    ConvertIntToDecimalStringN(gStringVar1, oldFriendship, STR_CONV_MODE_LEADING_ZEROS, 3);
    ConvertIntToDecimalStringN(gStringVar2, newFriendship, STR_CONV_MODE_LEADING_ZEROS, 3);
    StringCopy(gStringVar3, gText_DigitIndicator[digit]);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Friendship:\n{STR_VAR_1} {RIGHT_ARROW} {STR_VAR_2}\n\n{STR_VAR_3}"));
    AddTextPrinterParameterized(windowId, DEBUG_MENU_FONT, gStringVar4, 0, 0, 0, NULL);
}

static void DebugNativeStep_Party_SetFriendshipSelect(u8 taskId)
{
    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        gTasks[taskId].tFriendship = gTasks[taskId].tInput;
        SetMonData(&gPlayerParty[gTasks[taskId].tPartyId], MON_DATA_FRIENDSHIP, &gTasks[taskId].tInput);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_RG_BALL_CLICK);
        DebugNativeStep_CloseDebugWindow(taskId);
        return;
    }

    Debug_HandleInput_Numeric(taskId, 0, 255, 3);

    if (JOY_NEW(DPAD_ANY) || JOY_NEW(A_BUTTON))
        Debug_Display_FriendshipInfo(gTasks[taskId].tFriendship, gTasks[taskId].tInput, gTasks[taskId].tDigit, gTasks[taskId].tSubWindowId);
}

static void DebugNativeStep_Party_SetFriendshipMain(u8 taskId)
{
    u8 windowId = DebugNativeStep_CreateDebugWindow();
    u32 friendship = GetMonData(&gPlayerParty[gTasks[taskId].tPartyId], MON_DATA_FRIENDSHIP);

    // Display initial flag
    Debug_Display_FriendshipInfo(friendship, friendship, 0, windowId);

    gTasks[taskId].func = DebugNativeStep_Party_SetFriendshipSelect;
    gTasks[taskId].tSubWindowId = windowId;
    gTasks[taskId].tFriendship = friendship;
    gTasks[taskId].tInput = friendship;
    gTasks[taskId].tDigit = 0;
    gTasks[taskId].tPartyId = 0;
}

void DebugNative_Party_SetFriendship(void)
{
    if (gSpecialVar_0x8004 < PARTY_SIZE)
    {
        u32 taskId = CreateTask(DebugNativeStep_Party_SetFriendshipMain, 1);
        gTasks[taskId].tPartyId = gSpecialVar_0x8004;
    }
}

#undef tPartyId
#undef tFriendship

#undef tMenuTaskId
#undef tWindowId
#undef tSubWindowId
#undef tInput
#undef tDigit

static void DebugAction_Party_ClearParty(u8 taskId)
{
    ZeroPlayerPartyMons();
    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

enum DebugTrainerIds
{
    DEBUG_TRAINER_PLAYER,
    DEBUG_TRAINER_AI,
    DEBUG_TRAINERS_COUNT
};

const struct Trainer sDebugTrainers[DIFFICULTY_COUNT][DEBUG_TRAINERS_COUNT] =
{
#include "data/debug_trainers.h"
};

const struct Trainer* GetDebugAiTrainer(void)
{
    return &sDebugTrainers[DIFFICULTY_NORMAL][DEBUG_TRAINER_AI];
}

static void DebugAction_Party_SetParty(u8 taskId)
{
    ZeroPlayerPartyMons();
    CreateNPCTrainerPartyFromTrainer(gPlayerParty, &sDebugTrainers[DIFFICULTY_NORMAL][DEBUG_TRAINER_PLAYER], TRUE, BATTLE_TYPE_TRAINER);
    ScriptContext_Enable();
    Debug_DestroyMenu_Full(taskId);
}

static void DebugAction_Party_BattleSingle(u8 taskId)
{
    ZeroPlayerPartyMons();
    ZeroEnemyPartyMons();
    CreateNPCTrainerPartyFromTrainer(gPlayerParty, &sDebugTrainers[DIFFICULTY_NORMAL][DEBUG_TRAINER_PLAYER], TRUE, BATTLE_TYPE_TRAINER);
    CreateNPCTrainerPartyFromTrainer(gEnemyParty, GetDebugAiTrainer(), FALSE, BATTLE_TYPE_TRAINER);

    gBattleTypeFlags = BATTLE_TYPE_TRAINER;
    gDebugAIFlags = sDebugTrainers[DIFFICULTY_NORMAL][DEBUG_TRAINER_AI].aiFlags;
    gIsDebugBattle = TRUE;
    gBattleEnvironment = BattleSetup_GetEnvironmentId();
    CalculateEnemyPartyCount();
    BattleSetup_StartTrainerBattle_Debug();
    Debug_DestroyMenu_Full(taskId);
}

void CheckEWRAMCounters(struct ScriptContext *ctx)
{
    ConvertIntToDecimalStringN(gStringVar1, gFollowerSteps, STR_CONV_MODE_LEFT_ALIGN, 5);
    ConvertIntToDecimalStringN(gStringVar2, gChainFishingDexNavStreak, STR_CONV_MODE_LEFT_ALIGN, 5);
}
