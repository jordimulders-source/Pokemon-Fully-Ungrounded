// Gegenereerd door tools/grounded/debug_zone_warps.py, niet met de hand bewerken.

static const struct DebugMenuOption sDebugMenu_ZoneWarp_FullyUngrounded_0[] =
{
    { COMPOUND_STRING("StartTown"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_START_TOWN },
    { COMPOUND_STRING("StartTown_PC_1F"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_START_TOWN_POKEMON_CENTER_1F },
    { COMPOUND_STRING("StartTown_PC_2F"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_START_TOWN_POKEMON_CENTER_2F },
    { COMPOUND_STRING("StartTown_Mart"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_START_TOWN_MART },
    { COMPOUND_STRING("Stock_House1"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_HOUSE1 },
    { COMPOUND_STRING("Stock_House2"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_HOUSE2 },
    { COMPOUND_STRING("Stock_HouseWithBed"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_HOUSE_WITH_BED },
    { COMPOUND_STRING("Stock_SmallHouse"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_SMALL_HOUSE },
    { COMPOUND_STRING("Stock_TwoStory_1F"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_TWO_STORY_1F },
    { COMPOUND_STRING("Stock_TwoStory_2F"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_TWO_STORY_2F },
    { COMPOUND_STRING("Stock_Lab"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_STOCK_LAB },
    { COMPOUND_STRING("TestMap"), DebugAction_Util_ZoneWarp, (const void *)(uintptr_t)MAP_TEST_MAP },
    { NULL }
};

static const struct DebugMenuOption sDebugMenu_Actions_ZoneWarp[] =
{
    { COMPOUND_STRING("Fully Ungrounded…"), DebugAction_OpenSubMenu, sDebugMenu_ZoneWarp_FullyUngrounded_0 },
    { NULL }
};
