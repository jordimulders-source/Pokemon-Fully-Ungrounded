// Project Grounded: de Burglar (SIMON). Bij het binnenlopen van een stad met een "inbrekershuis" is er een kleine
// kans dat hij vandaag langskomt. Loopt de speler daarna vlak voor dat huis, dan komt hij met zijn buit naar
// buiten, ziet de speler en vecht. Na zijn nederlaag haalt de bewoner de spullen terug en rent hij weg, en laat
// hij een Nugget vallen. Script: data/scripts/burglar.inc. De twee figuren worden zonder kaartobject gespawnd
// (lokale id's LOCALID_BURGLAR_THIEF/RESIDENT), dus de kaarten zelf zijn niet aangepast.
#include "global.h"
#include "burglar.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "random.h"
#include "rtc.h"
#include "script.h"
#include "script_movement.h"
#include "constants/event_object_movement.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/trainer_types.h"
#include "constants/vars.h"

extern const u8 Burglar_EventScript_Scene[];

struct BurglarHouse
{
    u16 map;          // MAP_* (groep << 8 | nummer)
    u8 doorX, doorY;  // deur van het huis (kaartcoördinaten)
    u16 residentGfx;  // bewoner (zelfde als binnen in het huis)
};

// Volgorde = VAR_0x8004 in burglar.inc (teksten per stad). Fully Ungrounded: de steden waren Hoenn-steden
// (zie het commentaar per regel); tot er steden in de nieuwe regio zijn staat er MAP_UNDEFINED en komt hij nergens.
static const struct BurglarHouse sHouses[] =
{
    { MAP_UNDEFINED,   19, 14, OBJ_EVENT_GFX_WOMAN_3 },    // 0 Mauville, House2: de tv
    { MAP_UNDEFINED,  21, 44, OBJ_EVENT_GFX_POKEFAN_M },  // 1 Slateport, House: een anker
    { MAP_UNDEFINED,   42,  6, OBJ_EVENT_GFX_KECLEON },    // 2 Lilycove, House1: een schilderij (de Kecleon komt naar buiten, Jordi)
    { MAP_UNDEFINED,   26, 46, OBJ_EVENT_GFX_OLD_MAN },    // 3 Rustboro, House3: een sok vol pensioen
    { MAP_UNDEFINED, 17, 15, OBJ_EVENT_GFX_WOMAN_5 },    // 4 Verdanturf, House: opa's urn
    { MAP_UNDEFINED,   6, 17, OBJ_EVENT_GFX_SCIENTIST_1 },// 5 Fallarbor, Cozmo's huis: een meteorietje (Cozmo zelf, Jordi)
    { MAP_UNDEFINED,  20, 24, OBJ_EVENT_GFX_POKEFAN_F },  // 6 Petalburg, House2: Normans servet
};

#define BURGLAR_TOWN_MAUVILLE 0
#define BURGLAR_CHANCE        12  // 1 op 12 bij het binnenlopen
#define BURGLAR_CHANCE_NIGHT  3   // Mauville 's nachts: 1 op 3
#define ZONE_X                4   // speler maximaal 4 tegels links/rechts van de deur
#define ZONE_Y                4   // en 1-4 rijen eronder
#define MAX_PATH              16

static EWRAM_DATA u8 sArmedHouse = 0;       // huis + 1 waar hij nu (dit kaartbezoek) klaarstaat; 0 = nergens
static EWRAM_DATA u8 sSceneHouse = 0;       // huis van de lopende scène
static EWRAM_DATA bool8 sForceNext = FALSE; // debug: volgende inbrekersstad gegarandeerd
static EWRAM_DATA u8 sMoveThief[MAX_PATH + 2] = {0};
static EWRAM_DATA u8 sMoveResident[MAX_PATH + 2] = {0};
static EWRAM_DATA u8 sMovePlayer[2] = {0};
static EWRAM_DATA s16 sThiefX = 0, sThiefY = 0; // eindpositie van de dief (kaartcoördinaten), voor na het gevecht
static EWRAM_DATA u8 sThiefDir = 0;

static const s8 sDirDX[] = { [DIR_SOUTH] = 0, [DIR_NORTH] = 0, [DIR_WEST] = -1, [DIR_EAST] = 1 };
static const s8 sDirDY[] = { [DIR_SOUTH] = 1, [DIR_NORTH] = -1, [DIR_WEST] = 0, [DIR_EAST] = 0 };

static s32 FindHouseForCurrentMap(void)
{
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    for (u32 i = 0; i < ARRAY_COUNT(sHouses); i++)
    {
        if (sHouses[i].map == map)
            return i;
    }
    return -1;
}

static u32 CountPartyMonsAtLeastLevel(u32 level)
{
    u32 i, n = 0;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gPlayerParty[i], MON_DATA_SPECIES) != SPECIES_NONE
         && !GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG)
         && GetMonData(&gPlayerParty[i], MON_DATA_LEVEL) >= level)
            n++;
    }
    return n;
}

static u32 CountBadges(void)
{
    u32 n = 0;
    for (u32 flag = FLAG_BADGE01_GET; flag <= FLAG_BADGE08_GET; flag++)
    {
        if (FlagGet(flag))
            n++;
    }
    return n;
}

// Eén team per badge (TRAINER_BURGLAR_1 = 1 badge … _8 = 8 badges) en een eigen team na de Hall of Fame (_9).
// Zonder badge komt hij niet (Burglar_OnMapEnter).
static u32 GetTier(void)
{
    u32 badges = CountBadges();
    if (FlagGet(FLAG_SYS_GAME_CLEAR))
        return 8;
    if (badges == 0)
        return 0;
    return badges > 8 ? 7 : badges - 1;
}

#define BURGLAR_GUARANTEE_EVERY 2  // na badge 2, 4 en 6 een gegarandeerd bezoek (max. 3)

static u32 GetGuaranteedVisits(void)
{
    u32 n = CountBadges() / BURGLAR_GUARANTEE_EVERY;
    return n > 3 ? 3 : n;
}

// Aangeroepen bij elke kaartovergang (warp én lopend via een verbinding), na het ON_TRANSITION-script.
void Burglar_OnMapEnter(void)
{
    s32 house = FindHouseForCurrentMap();
    u16 today;

    sArmedHouse = 0;
    if (house < 0)
        return;
    if (sForceNext)
    {
        sForceNext = FALSE;
        sArmedHouse = house + 1;
        return;
    }
    if (!FlagGet(FLAG_SYS_POKEMON_GET) || !FlagGet(FLAG_BADGE01_GET))
        return;
    // Jordi: nooit twee keer op rij in dezelfde stad (ook niet na een verloren gevecht)
    if (VarGet(VAR_BURGLAR_LAST_TOWN) == house + 1)
        return;
    // Post-game (Jordi): alleen als je minstens 3 Pokémon van lv 90+ bij je hebt, anders is het tijdverspilling
    if (FlagGet(FLAG_SYS_GAME_CLEAR) && CountPartyMonsAtLeastLevel(90) < 3)
        return;
    // Gegarandeerd: na badge 2, 4 en 6 komt hij bij het eerstvolgende bezoek aan een inbrekersstad, tot hij zo vaak
    // verslagen is (dus minstens 3 keer per playthrough, telkens met het team van dat moment). Ook als hij vandaag al
    // langskwam; verlies je van hem, dan komt hij terug.
    if (VarGet(VAR_BURGLAR_DEFEATS) < GetGuaranteedVisits())
    {
        sArmedHouse = house + 1;
        return;
    }
    RtcCalcLocalTime();
    today = (u16)(gLocalTime.days + 1); // 0 = nog nooit
    if (VarGet(VAR_BURGLAR_LAST_DAY) == today)
        return; // maximaal één inbraak per dag
    if (house == BURGLAR_TOWN_MAUVILLE && GetTimeOfDay() == TIME_NIGHT)
    {
        if (Random() % BURGLAR_CHANCE_NIGHT != 0)
            return;
    }
    else if (Random() % BURGLAR_CHANCE != 0)
    {
        return;
    }
    sArmedHouse = house + 1;
}

static bool32 CellFree(s16 x, s16 y, u32 dir)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    return GetCollisionAtCoords(player, x + MAP_OFFSET, y + MAP_OFFSET, dir) == COLLISION_NONE;
}

// Pad van (x,y) tot naast (tx,ty): eerst verticaal (naar de rij van het doel), dan horizontaal.
// Schrijft richtingen in dirs, geeft het aantal stappen terug (-1 als het pad geblokkeerd is).
static s32 BuildPath(s16 x, s16 y, s16 tx, s16 ty, u8 *dirs, bool32 check)
{
    s32 n = 0;
    s16 goalY = (x == tx) ? (ty > y ? ty - 1 : ty + 1) : ty;

    while (y != goalY && n < MAX_PATH)
    {
        u32 dir = (goalY > y) ? DIR_SOUTH : DIR_NORTH;
        y += sDirDY[dir];
        if (check && !CellFree(x, y, dir))
            return -1;
        dirs[n++] = dir;
    }
    if (x != tx)
    {
        s16 goalX = (tx > x) ? tx - 1 : tx + 1;
        while (x != goalX && n < MAX_PATH)
        {
            u32 dir = (goalX > x) ? DIR_EAST : DIR_WEST;
            x += sDirDX[dir];
            if (check && !CellFree(x, y, dir))
                return -1;
            dirs[n++] = dir;
        }
    }
    return n;
}

static u32 DirectionTowards(s16 x, s16 y, s16 tx, s16 ty)
{
    if (tx > x) return DIR_EAST;
    if (tx < x) return DIR_WEST;
    if (ty > y) return DIR_SOUTH;
    return DIR_NORTH;
}

static u32 OppositeDir(u32 dir)
{
    switch (dir)
    {
    case DIR_SOUTH: return DIR_NORTH;
    case DIR_NORTH: return DIR_SOUTH;
    case DIR_WEST:  return DIR_EAST;
    default:        return DIR_WEST;
    }
}

// Aangeroepen na elke stap (field_control_avatar.c). Start de scène als de speler vlak voor het huis loopt.
bool8 Burglar_TryTriggerOnStep(s16 px, s16 py)
{
    const struct BurglarHouse *h;
    s16 sx, sy, dx;
    u8 dirs[MAX_PATH];

    if (sArmedHouse == 0 || FindHouseForCurrentMap() != sArmedHouse - 1)
        return FALSE;
    if (gPlayerAvatar.flags & (PLAYER_AVATAR_FLAG_SURFING | PLAYER_AVATAR_FLAG_UNDERWATER))
        return FALSE;
    h = &sHouses[sArmedHouse - 1];
    px -= MAP_OFFSET;
    py -= MAP_OFFSET;
    sx = h->doorX;
    sy = h->doorY + 1;  // tegel vóór de deur
    dx = px - sx;
    if (dx < -ZONE_X || dx > ZONE_X || py < sy || py > sy + ZONE_Y - 1)
        return FALSE;
    if ((dx < 0 ? -dx : dx) + (py - sy) <= 1)
        return FALSE;  // te dichtbij: hij moet minstens één stap van de deur af kunnen
    if (!CellFree(sx, sy, DIR_SOUTH) || BuildPath(sx, sy, px, py, dirs, TRUE) < 0)
        return FALSE;

    sSceneHouse = sArmedHouse - 1;
    sArmedHouse = 0;
    VarSet(VAR_BURGLAR_LAST_TOWN, sSceneHouse + 1);
    ScriptContext_SetupScript(Burglar_EventScript_Scene);
    return TRUE;
}

static struct ObjectEvent *GetActor(u8 localId)
{
    u8 id = GetObjectEventIdByLocalIdAndMap(localId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    if (id >= OBJECT_EVENTS_COUNT)
        return NULL;
    return &gObjectEvents[id];
}

static void StartMovement(u8 localId, const u8 *script)
{
    ScriptMovement_StartObjectMovementScript(localId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, script);
}

// VAR_0x8004 = stad, 0x8005/0x8006 = deur, 0x8007 = sterkte (0-7 = badge 1-8, 8 = na de HoF), 0x8008 = aantal keer verslagen.
void Burglar_SetupVars(void)
{
    s32 house = sSceneHouse;
    gSpecialVar_0x8004 = house;
    gSpecialVar_0x8005 = sHouses[house].doorX;
    gSpecialVar_0x8006 = sHouses[house].doorY;
    gSpecialVar_0x8007 = GetTier();
    gSpecialVar_0x8008 = VarGet(VAR_BURGLAR_DEFEATS);
}

static void SpawnActor(u8 localId, u16 gfx, s16 x, s16 y, u32 dir)
{
    static const u8 sFaceTypes[] = { [DIR_SOUTH] = MOVEMENT_TYPE_FACE_DOWN, [DIR_NORTH] = MOVEMENT_TYPE_FACE_UP,
                                     [DIR_WEST] = MOVEMENT_TYPE_FACE_LEFT, [DIR_EAST] = MOVEMENT_TYPE_FACE_RIGHT };
    struct ObjectEventTemplate t = {0};

    if (GetActor(localId) != NULL)
        return;
    t.localId = localId;
    t.graphicsId = gfx;
    t.kind = OBJ_KIND_NORMAL;
    t.x = x;
    t.y = y;
    t.elevation = gObjectEvents[gPlayerAvatar.objectEventId].currentElevation;
    t.movementType = (dir >= DIR_SOUTH && dir <= DIR_EAST) ? sFaceTypes[dir] : MOVEMENT_TYPE_FACE_DOWN;
    t.trainerType = TRAINER_TYPE_NONE;
    SpawnSpecialObjectEvent(&t);
}

static void SpawnAtDoor(u8 localId, u16 gfx)
{
    SpawnActor(localId, gfx, sHouses[sSceneHouse].doorX, sHouses[sSceneHouse].doorY, DIR_SOUTH);
}

// Na het gevecht bestaan gespawnde objecten zonder kaartsjabloon niet meer: zet de dief terug.
void Burglar_RestoreThief(void)
{
    SpawnActor(LOCALID_BURGLAR_THIEF, OBJ_EVENT_GFX_BURGLAR, sThiefX, sThiefY, sThiefDir);
}

void Burglar_SpawnThief(void)
{
    SpawnAtDoor(LOCALID_BURGLAR_THIEF, OBJ_EVENT_GFX_BURGLAR);
}

void Burglar_SpawnResident(void)
{
    SpawnAtDoor(LOCALID_BURGLAR_RESIDENT, sHouses[sSceneHouse].residentGfx);
}

// Laat mover naar target lopen (tot ernaast); beiden kijken elkaar daarna aan.
static void Approach(u8 moverId, u8 *buf, u8 targetId, bool32 turnTarget)
{
    struct ObjectEvent *mover = GetActor(moverId);
    struct ObjectEvent *target = (targetId == LOCALID_PLAYER) ? &gObjectEvents[gPlayerAvatar.objectEventId] : GetActor(targetId);
    u8 dirs[MAX_PATH];
    s32 n, i;
    s16 x, y;

    if (mover == NULL || target == NULL)
        return;
    x = mover->currentCoords.x;
    y = mover->currentCoords.y;
    n = BuildPath(x, y, target->currentCoords.x, target->currentCoords.y, dirs, FALSE);
    for (i = 0; i < n; i++)
    {
        buf[i] = GetWalkNormalMovementAction(dirs[i]);
        x += sDirDX[dirs[i]];
        y += sDirDY[dirs[i]];
    }
    if (moverId == LOCALID_BURGLAR_THIEF)
    {
        sThiefX = x - MAP_OFFSET;
        sThiefY = y - MAP_OFFSET;
        sThiefDir = DirectionTowards(x, y, target->currentCoords.x, target->currentCoords.y);
    }
    buf[i++] = GetFaceDirectionMovementAction(DirectionTowards(x, y, target->currentCoords.x, target->currentCoords.y));
    buf[i] = MOVEMENT_ACTION_STEP_END;
    StartMovement(moverId, buf);
    if (turnTarget)
    {
        sMovePlayer[0] = GetFaceDirectionMovementAction(DirectionTowards(target->currentCoords.x, target->currentCoords.y, x, y));
        sMovePlayer[1] = MOVEMENT_ACTION_STEP_END;
        StartMovement(targetId, sMovePlayer);
    }
}

void Burglar_ThiefApproachPlayer(void)
{
    Approach(LOCALID_BURGLAR_THIEF, sMoveThief, LOCALID_PLAYER, TRUE);
}

void Burglar_ResidentApproachThief(void)
{
    Approach(LOCALID_BURGLAR_RESIDENT, sMoveResident, LOCALID_BURGLAR_THIEF, TRUE);
}

// Wegrennen: de richting met de meeste vrije tegels (max. 8), bij gelijkspel weg van de speler.
void Burglar_ThiefFlee(void)
{
    struct ObjectEvent *thief = GetActor(LOCALID_BURGLAR_THIEF);
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    u32 order[4], best = DIR_SOUTH, bestN = 0, i, n;

    if (thief == NULL)
        return;
    order[0] = OppositeDir(DirectionTowards(thief->currentCoords.x, thief->currentCoords.y, player->currentCoords.x, player->currentCoords.y));
    order[1] = DIR_SOUTH;
    order[2] = DIR_WEST;
    order[3] = DIR_EAST;
    for (i = 0; i < 4; i++)
    {
        s16 x = thief->currentCoords.x, y = thief->currentCoords.y;
        for (n = 0; n < 8; n++)
        {
            x += sDirDX[order[i]];
            y += sDirDY[order[i]];
            if (GetCollisionAtCoords(thief, x, y, order[i]) != COLLISION_NONE)
                break;
        }
        if (n > bestN)
        {
            bestN = n;
            best = order[i];
        }
    }
    for (i = 0; i < bestN; i++)
        sMoveThief[i] = GetWalkFasterMovementAction(best);
    sMoveThief[i] = MOVEMENT_ACTION_STEP_END;
    StartMovement(LOCALID_BURGLAR_THIEF, sMoveThief);
}

// Bewoner loopt terug: horizontaal naar de kolom van de deur, omhoog tot vóór de deur en kijkt naar boven.
void Burglar_ResidentGoHome(void)
{
    struct ObjectEvent *res = GetActor(LOCALID_BURGLAR_RESIDENT);
    const struct BurglarHouse *h = &sHouses[sSceneHouse];
    s16 x, y, gx = h->doorX + MAP_OFFSET, gy = h->doorY + 1 + MAP_OFFSET;
    u32 i = 0;

    if (res == NULL)
        return;
    x = res->currentCoords.x;
    y = res->currentCoords.y;
    while (x != gx && i < MAX_PATH)
    {
        sMoveResident[i++] = GetWalkNormalMovementAction(gx > x ? DIR_EAST : DIR_WEST);
        x += (gx > x) ? 1 : -1;
    }
    while (y != gy && i < MAX_PATH)
    {
        sMoveResident[i++] = GetWalkNormalMovementAction(gy > y ? DIR_SOUTH : DIR_NORTH);
        y += (gy > y) ? 1 : -1;
    }
    sMoveResident[i++] = GetFaceDirectionMovementAction(DIR_NORTH);
    sMoveResident[i] = MOVEMENT_ACTION_STEP_END;
    StartMovement(LOCALID_BURGLAR_RESIDENT, sMoveResident);
}

// VAR_0x8004: LOCALID_BURGLAR_THIEF of LOCALID_BURGLAR_RESIDENT.
void Burglar_RemoveActor(void)
{
    struct ObjectEvent *obj = GetActor(gSpecialVar_0x8004);
    if (obj != NULL)
        RemoveObjectEvent(obj);
}

void Burglar_Finish(void)
{
    u16 defeats = VarGet(VAR_BURGLAR_DEFEATS);
    if (defeats < 9999)
        VarSet(VAR_BURGLAR_DEFEATS, defeats + 1);
    RtcCalcLocalTime();
    VarSet(VAR_BURGLAR_LAST_DAY, (u16)(gLocalTime.days + 1));
    sSceneHouse = 0;
}

// Debug: de eerstvolgende inbrekersstad (of deze, als je er al bent) krijgt hem gegarandeerd.
void Burglar_DebugForce(void)
{
    s32 house = FindHouseForCurrentMap();
    if (house >= 0)
    {
        sArmedHouse = house + 1;
        gSpecialVar_Result = TRUE;
    }
    else
    {
        sForceNext = TRUE;
        gSpecialVar_Result = FALSE;
    }
}
