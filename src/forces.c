// Project Grounded: Forces of Nature op routes (post-game). Tornadus, Thundurus en Landorus staan af en toe als
// object op een van hun kandidaatroutes, vluchten niet en brengen hun eigen weer mee (ook als de route normaal
// zonnig is). Bij elke binnenkomst van een kandidaatroute (lopend of via een warp) wordt opnieuw geloot; kom je
// alleen even uit een huis of grot op dezelfde route, dan blijft het zoals het was. Na vangen of verslaan zijn ze
// weg (FLAG_FORCES_*_DONE); vluchten of verliezen mag, dan komen ze later terug.
// Objecten: achteraan object_events van elke kandidaatroute (tools/grounded/maptools/forces_routes.py), met
// FLAG_FORCES_HIDE_* als objectflag. Scripts en hint-NPC's: data/scripts/forces.inc.
#include "global.h"
#include "forces.h"
#include "event_data.h"
#include "field_weather.h"
#include "overworld.h"
#include "random.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/vars.h"
#include "constants/weather.h"

#define FORCES_CHANCE 4 // 1 op 4 bij binnenkomst van een kandidaatroute (per Force)

enum
{
    FORCE_TORNADUS,
    FORCE_THUNDURUS,
    FORCE_LANDORUS,
    FORCE_COUNT,
};

struct Force
{
    u16 doneFlag;
    u16 hideFlag;
    u8 weather;
    u16 maps[4];      // MAP_* (groep << 8 | nummer); 0 = leeg
};

static const struct Force sForces[FORCE_COUNT] =
{
    [FORCE_TORNADUS]  = { FLAG_FORCES_TORNADUS_DONE,  FLAG_FORCES_HIDE_TORNADUS,  WEATHER_FOG_HORIZONTAL,
                          { MAP_ROUTE113, MAP_ROUTE118, MAP_ROUTE121 } },
    [FORCE_THUNDURUS] = { FLAG_FORCES_THUNDURUS_DONE, FLAG_FORCES_HIDE_THUNDURUS, WEATHER_RAIN_THUNDERSTORM,
                          { MAP_ROUTE119, MAP_ROUTE120, MAP_ROUTE123 } },
    [FORCE_LANDORUS]  = { FLAG_FORCES_LANDORUS_DONE,  FLAG_FORCES_HIDE_LANDORUS,  WEATHER_SANDSTORM,
                          { MAP_ROUTE112, MAP_ROUTE114, MAP_ROUTE117 } },
};

static EWRAM_DATA u16 sStateMap = 0;      // kaart waarvoor de laatste loting geldt
static EWRAM_DATA bool8 sStateHere = FALSE;
static EWRAM_DATA u8 sRouteWeather = 0;     // weer van de route zonder Force (voor na het gevecht)
static EWRAM_DATA u8 sForceNext = 0;      // debug: Force + 1 die bij de volgende kandidaatroute zeker verschijnt
EWRAM_DATA u8 gForcesStartingStatus = 0;  // gelezen in battle_main.c (beginveld van het gevecht)

static s32 FindForce(u16 map)
{
    for (u32 i = 0; i < FORCE_COUNT; i++)
    {
        for (u32 j = 0; j < ARRAY_COUNT(sForces[i].maps); j++)
        {
            if (sForces[i].maps[j] != 0 && sForces[i].maps[j] == map)
                return i;
        }
    }
    return -1;
}

// Aangeroepen bij elke kaartovergang (warp én lopend via een verbinding), na het ON_TRANSITION-script, zodat het
// weer van de Force het normale weer (ook de regencycli van Route 119/123) overschrijft.
void Forces_OnMapEnter(void)
{
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    u16 prev = (gLastUsedWarp.mapGroup << 8) | gLastUsedWarp.mapNum;
    s32 force = FindForce(map);
    bool32 here;

    if (force < 0)
    {
        if (IsMapTypeOutdoors(GetCurrentMapType()))
            sStateMap = 0; // andere buitenkaart: de Force is vertrokken
        return;
    }

    if (sStateMap == map && prev != map && !IsMapTypeOutdoors(GetLastUsedWarpMapType()))
    {
        here = sStateHere; // even een huis/grot in en weer uit: niets veranderd
    }
    else
    {
        here = FALSE;
        if (sForceNext == force + 1)
        {
            here = TRUE;
            sForceNext = 0;
        }
        else if (FlagGet(FLAG_SYS_GAME_CLEAR) && !FlagGet(sForces[force].doneFlag))
        {
            here = (Random() % FORCES_CHANCE) == 0;
        }
        if (FlagGet(sForces[force].doneFlag))
            here = FALSE;
        sStateMap = map;
        sStateHere = here;
    }

    if (here)
    {
        FlagClear(sForces[force].hideFlag);
        sRouteWeather = GetSavedWeather();
        SetSavedWeather(sForces[force].weather);
    }
    else
    {
        FlagSet(sForces[force].hideFlag);
    }
}

// Script: na het gevecht (gevangen of verslagen). De Force is weg, het weer van de route komt terug.
// Daarna doet het script doweather.
void Forces_Finish(void)
{
    sStateHere = FALSE;
    SetSavedWeather(sRouteWeather);
}

// Zolang een Force op deze kaart staat, veranderen weer-coördinaten (Route 113 as, Route 119/120/123) niets.
bool32 Forces_ActiveHere(void)
{
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    return sStateHere && sStateMap == map;
}

// Script: vlak voor het gevecht. Tornadus begint met Tailwind aan zijn kant (wind), de andere twee hebben genoeg
// aan hun weer (onweer = regen + Electric Terrain, zandstorm).
void Forces_PrepareBattle(void)
{
    if (gSpecialVar_0x8004 == FORCE_TORNADUS)
        gForcesStartingStatus = STARTING_STATUS_TAILWIND_OPPONENT;
    else
        gForcesStartingStatus = 0;
}

// Debug: VAR_0x8004 = Force (0 Tornadus, 1 Thundurus, 2 Landorus); bij de volgende kandidaatroute staat hij er zeker.
void Forces_DebugForceNext(void)
{
    sForceNext = gSpecialVar_0x8004 + 1;
}
