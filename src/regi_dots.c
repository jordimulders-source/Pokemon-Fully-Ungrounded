// Project Grounded: de Regi-stippenpuzzel (vervangt de braille-puzzels).
// In de voorkamer van elke Regi-grot liggen stippen in het oogpatroon van die Regi. Bekijk je de muur,
// dan lichten de stippen een voor een op in de juiste volgorde; loop ze in dezelfde volgorde af.
// Een verkeerde stip laat alles doven. Als alle stippen branden, gaat de ingang naar de Regi open.
#include "global.h"
#include "event_data.h"
#include "field_camera.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/vars.h"

#define METATILE_REGI_DOT_OFF 0x3A8
#define METATILE_REGI_DOT_ON  0x3A9
#define MAX_REGI_DOTS 9

struct RegiDots
{
    u16 map;
    u16 flag; // puzzel opgelost
    u8 count;
    u8 x[MAX_REGI_DOTS]; // in de volgorde waarin ze moeten oplichten
    u8 y[MAX_REGI_DOTS];
};

static const struct RegiDots sRegiDots[] =
{
    // Regirock: een H
    {MAP_DESERT_RUINS, FLAG_SYS_REGIROCK_PUZZLE_COMPLETED, 7,
        {6, 6, 6, 8, 10, 10, 10}, {22, 24, 26, 24, 22, 24, 26}},
    // Regice: een zeshoek met een stip in het midden
    {MAP_ISLAND_CAVE, FLAG_SYS_BRAILLE_REGICE_COMPLETED, 7,
        {7, 9, 10, 9, 7, 6, 8}, {22, 22, 24, 26, 26, 24, 24}},
    // Registeel: een kruis (twee schuine streken)
    {MAP_ANCIENT_TOMB, FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED, 9,
        {6, 7, 8, 9, 10, 10, 9, 7, 6}, {22, 23, 24, 25, 26, 22, 23, 25, 26}},
    // Regieleki: een boog met een stip in het midden
    {MAP_REGIELEKI_CAVE, FLAG_SYS_REGIELEKI_PUZZLE_COMPLETED, 7,
        {5, 6, 5, 8, 11, 10, 11}, {22, 24, 25, 24, 25, 24, 22}},
    // Regidrago: een vork
    {MAP_REGIDRAGO_CAVE, FLAG_SYS_REGIDRAGO_PUZZLE_COMPLETED, 7,
        {6, 10, 8, 7, 9, 8, 8}, {22, 22, 23, 24, 24, 25, 27}},
};

// de dichte ingang (7-9, 19-20) zoals hij in de layout staat, met botsing
static const u16 sOpenEntrance[2][3] = {{0x62A, 0x62B, 0x62C}, {0x632, 0x233, 0x634}};

static const struct RegiDots *GetRegiDots(void)
{
    u32 i;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    for (i = 0; i < ARRAY_COUNT(sRegiDots); i++)
        if (sRegiDots[i].map == map)
            return &sRegiDots[i];
    return NULL;
}

static void SetDot(const struct RegiDots *dots, u32 i, bool32 lit)
{
    MapGridSetMetatileIdAt(dots->x[i] + MAP_OFFSET, dots->y[i] + MAP_OFFSET, lit ? METATILE_REGI_DOT_ON : METATILE_REGI_DOT_OFF);
}

static void SetAllDots(const struct RegiDots *dots, bool32 lit)
{
    u32 i;
    for (i = 0; i < dots->count; i++)
        SetDot(dots, i, lit);
}

// ON_LOAD: opgelost = alle stippen branden
void RegiDots_OnLoad(void)
{
    const struct RegiDots *dots = GetRegiDots();
    if (dots != NULL && FlagGet(dots->flag))
        SetAllDots(dots, TRUE);
}

// coord-trigger op een stip. VAR_RESULT: 0 = niets, 1 = goed, 2 = fout (alles gedoofd), 3 = opgelost
void RegiDots_Step(void)
{
    const struct RegiDots *dots = GetRegiDots();
    s16 x, y;
    u32 i, progress;

    gSpecialVar_Result = 0;
    if (dots == NULL || FlagGet(dots->flag))
        return;
    PlayerGetDestCoords(&x, &y);
    x -= MAP_OFFSET;
    y -= MAP_OFFSET;
    for (i = 0; i < dots->count; i++)
        if (dots->x[i] == x && dots->y[i] == y)
            break;
    if (i == dots->count)
        return;

    progress = VarGet(VAR_TEMP_1);
    if (i < progress)
        return; // brandt al
    if (i == progress)
    {
        SetDot(dots, i, TRUE);
        progress++;
        gSpecialVar_Result = 1;
        if (progress == dots->count)
        {
            FlagSet(dots->flag);
            gSpecialVar_Result = 3;
        }
    }
    else
    {
        SetAllDots(dots, FALSE);
        progress = 0;
        gSpecialVar_Result = 2;
        if (i == 0)
        {
            // opnieuw beginnen telt meteen als eerste stip
            SetDot(dots, 0, TRUE);
            progress = 1;
        }
    }
    VarSet(VAR_TEMP_1, progress);
    DrawWholeMapView();
}

// de muur: VAR_0x8004 = welke stap van de reeks. Steekt alleen die stip aan (de rest uit).
// VAR_RESULT = FALSE als de reeks klaar is (dan staat alles weer uit).
void RegiDots_ShowStep(void)
{
    const struct RegiDots *dots = GetRegiDots();
    gSpecialVar_Result = FALSE;
    if (dots == NULL)
        return;
    SetAllDots(dots, FALSE);
    if (gSpecialVar_0x8004 < dots->count)
    {
        SetDot(dots, gSpecialVar_0x8004, TRUE);
        gSpecialVar_Result = TRUE;
    }
    VarSet(VAR_TEMP_1, 0);
    DrawWholeMapView();
}

// na het voorspelen: alles uit, behalve als de puzzel al is opgelost
void RegiDots_Reset(void)
{
    const struct RegiDots *dots = GetRegiDots();
    if (dots == NULL)
        return;
    SetAllDots(dots, FlagGet(dots->flag));
    VarSet(VAR_TEMP_1, 0);
    DrawWholeMapView();
}

void RegiDots_OpenEntrance(void)
{
    u32 r, c;
    for (r = 0; r < 2; r++)
        for (c = 0; c < 3; c++)
            MapGridSetMetatileIdAt(7 + c + MAP_OFFSET, 19 + r + MAP_OFFSET, sOpenEntrance[r][c]);
    DrawWholeMapView();
}
