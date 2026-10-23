// Project Grounded: Enamorus en de liefdesdagen (post-game). Zodra Tornadus, Thundurus en Landorus alle drie
// afgehandeld zijn (FLAG_FORCES_*_DONE), is het op de meeste dagen in één van vier kleine stadjes "liefdesdag":
// hartjes boven de NPC's, een verliefd koppel, Prof. Birch met zijn drol (bekend van het strandresort) en Enamorus
// zelf, die je aanspreekt voor een gevecht. Welk stadje (of geen) volgt vast uit de dag van de klok, dus binnen een
// dag verandert het niet. Na het vangen van Enamorus blijven de liefdesdagen als sfeer bestaan, zonder Enamorus;
// versla je hem, dan vliegt hij weg en is hij er op een volgende liefdesdag weer.
// Objecten: achteraan object_events van elk stadje (tools/grounded/maptools/enamorus_towns.py), met
// FLAG_ENAMORUS_HIDE (Enamorus) en FLAG_LOVEDAY_HIDE (koppel, Birch, drol) als objectflag.
// Scripts: data/scripts/enamorus.inc.
#include "global.h"
#include "enamorus.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_effect.h"
#include "random.h"
#include "rtc.h"
#include "script.h"
#include "task.h"
#include "constants/field_effects.h"
#include "constants/flags.h"
#include "constants/maps.h"

#define LOVE_DAY_ROLL     6   // per dag: 0..3 = dat stadje, 4..5 = geen liefdesdag (2 op 3 dagen wel)
#define HEART_INTERVAL    40  // frames tussen twee hartjes

// Fully Ungrounded: dit waren Oldale, Dewford, Fallarbor en Lavaridge; Enamorus zit (nog) niet in de dex. Het
// mechaniek blijft slapend staan: MAP_UNDEFINED komt nooit voor; stadjes uit de nieuwe regio invullen.
static const u16 sLoveTowns[] =
{
    MAP_UNDEFINED,
    MAP_UNDEFINED,
    MAP_UNDEFINED,
    MAP_UNDEFINED,
};

static EWRAM_DATA u16 sLoveMap = 0;          // stadje waar het nu liefdesdag is en waar de speler staat (0 = geen)
static EWRAM_DATA u8 sDebugTown = 0;         // debug: stadje + 1 dat vandaag zeker liefdesdag heeft
static EWRAM_DATA u16 sDefeatedDay = 0;      // dag + 1 waarop Enamorus verslagen is (komt een volgende keer terug)

static u16 CurrentMap(void)
{
    return (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
}

static u16 Today(void)
{
    RtcCalcLocalTime();
    return (u16)(gLocalTime.days + 1);
}

bool32 Enamorus_LoveDaysUnlocked(void)
{
    return FlagGet(FLAG_FORCES_TORNADUS_DONE) && FlagGet(FLAG_FORCES_THUNDURUS_DONE) && FlagGet(FLAG_FORCES_LANDORUS_DONE);
}

// Stadje (index in sLoveTowns) met vandaag liefdesdag, of -1.
static s32 TodaysLoveTown(void)
{
    u32 h;

    if (sDebugTown != 0)
        return sDebugTown - 1;
    if (!Enamorus_LoveDaysUnlocked())
        return -1;
    h = (u32)Today() * 2654435761u;
    h ^= h >> 15;
    h *= 0x2C1B3C6Du;
    h ^= h >> 12;
    h %= LOVE_DAY_ROLL;
    return h < ARRAY_COUNT(sLoveTowns) ? (s32)h : -1;
}

// Aangeroepen bij elke kaartovergang (warp én lopend via een verbinding), na het ON_TRANSITION-script.
void Enamorus_OnMapEnter(void)
{
    u16 map = CurrentMap();
    s32 town = TodaysLoveTown();

    sLoveMap = 0;
    if (town >= 0 && sLoveTowns[town] == map)
    {
        sLoveMap = map;
        FlagClear(FLAG_LOVEDAY_HIDE);
        if (FlagGet(FLAG_ENAMORUS_DONE) || sDefeatedDay == Today())
            FlagSet(FLAG_ENAMORUS_HIDE);
        else
            FlagClear(FLAG_ENAMORUS_HIDE);
    }
    else
    {
        FlagSet(FLAG_LOVEDAY_HIDE);
        FlagSet(FLAG_ENAMORUS_HIDE);
    }
}

// Hartjes boven willekeurige mensen (en Pokémon) die in beeld staan, zolang de speler vrij rondloopt.
static void Task_LoveHearts(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    u8 candidates[OBJECT_EVENTS_COUNT];
    u32 count = 0;
    struct ObjectEvent *objEvent;

    if (sLoveMap == 0 || sLoveMap != CurrentMap())
    {
        DestroyTask(taskId);
        return;
    }
    if (ArePlayerFieldControlsLocked() || ++data[0] < HEART_INTERVAL)
        return;
    data[0] = Random() % 16; // niet in een strak ritme

    for (u32 i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        objEvent = &gObjectEvents[i];
        if (objEvent->active && !objEvent->isPlayer && !objEvent->invisible && !objEvent->offScreen
         && !objEvent->inanimate)
            candidates[count++] = i;
    }
    if (count == 0)
        return;
    objEvent = &gObjectEvents[candidates[Random() % count]];
    ObjectEventGetLocalIdAndMap(objEvent, &gFieldEffectArguments[0], &gFieldEffectArguments[1], &gFieldEffectArguments[2]);
    FieldEffectStart(FLDEFF_HEART_ICON);
}

// Aangeroepen na het ON_RESUME-script (na een warp, gevecht of menu, en lopend via een verbinding).
void Enamorus_StartHearts(void)
{
    if (sLoveMap != 0 && sLoveMap == CurrentMap() && !FuncIsActiveTask(Task_LoveHearts))
        CreateTask(Task_LoveHearts, 80);
}

// Script: na een gewonnen gevecht (niet gevangen) vliegt hij weg tot een volgende liefdesdag.
void Enamorus_Defeated(void)
{
    sDefeatedDay = Today();
}

// Debug: VAR_0x8004 = stadje (0 Oldale, 1 Dewford, 2 Fallarbor, 3 Lavaridge) dat vandaag zeker liefdesdag heeft.
void Enamorus_DebugForceTown(void)
{
    sDebugTown = gSpecialVar_0x8004 + 1;
}
