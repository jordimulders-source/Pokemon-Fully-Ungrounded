#include "global.h"
#include "grounded_forms.h"
#include "pokemon.h"
#include "random.h"
#include "rtc.h"
#include "constants/species.h"

// Project Grounded: Vivillon-patronen zijn willekeurig (alle 20, ook Fancy en Poké Ball),
// Deerling/Sawsbuck volgen het seizoen van de echte datum zoals in Gen 5.

#define PATTERNS(mon) {                                                                  \
    SPECIES_##mon##_ICY_SNOW, SPECIES_##mon##_POLAR, SPECIES_##mon##_TUNDRA,              \
    SPECIES_##mon##_CONTINENTAL, SPECIES_##mon##_GARDEN, SPECIES_##mon##_ELEGANT,         \
    SPECIES_##mon##_MEADOW, SPECIES_##mon##_MODERN, SPECIES_##mon##_MARINE,               \
    SPECIES_##mon##_ARCHIPELAGO, SPECIES_##mon##_HIGH_PLAINS, SPECIES_##mon##_SANDSTORM,  \
    SPECIES_##mon##_RIVER, SPECIES_##mon##_MONSOON, SPECIES_##mon##_SAVANNA,              \
    SPECIES_##mon##_SUN, SPECIES_##mon##_OCEAN, SPECIES_##mon##_JUNGLE,                   \
    SPECIES_##mon##_FANCY, SPECIES_##mon##_POKEBALL }

static const u16 sScatterbugForms[] = PATTERNS(SCATTERBUG);
static const u16 sSpewpaForms[] = PATTERNS(SPEWPA);
static const u16 sVivillonForms[] = PATTERNS(VIVILLON);

enum { SEASON_SPRING, SEASON_SUMMER, SEASON_AUTUMN, SEASON_WINTER };

static const u16 sDeerlingForms[] = {
    [SEASON_SPRING] = SPECIES_DEERLING_SPRING,
    [SEASON_SUMMER] = SPECIES_DEERLING_SUMMER,
    [SEASON_AUTUMN] = SPECIES_DEERLING_AUTUMN,
    [SEASON_WINTER] = SPECIES_DEERLING_WINTER,
};
static const u16 sSawsbuckForms[] = {
    [SEASON_SPRING] = SPECIES_SAWSBUCK_SPRING,
    [SEASON_SUMMER] = SPECIES_SAWSBUCK_SUMMER,
    [SEASON_AUTUMN] = SPECIES_SAWSBUCK_AUTUMN,
    [SEASON_WINTER] = SPECIES_SAWSBUCK_WINTER,
};

static u32 GetSeason(void)
{
    switch (GetMonth())
    {
    case MONTH_MAR: case MONTH_APR: case MONTH_MAY:
        return SEASON_SPRING;
    case MONTH_JUN: case MONTH_JUL: case MONTH_AUG:
        return SEASON_SUMMER;
    case MONTH_SEP: case MONTH_OCT: case MONTH_NOV:
        return SEASON_AUTUMN;
    case MONTH_DEC: case MONTH_JAN: case MONTH_FEB:
        return SEASON_WINTER;
    default: // geen (werkende) klok
        return SEASON_SPRING;
    }
}

u32 GetRandomPatternForm(u32 species)
{
    switch (GET_BASE_SPECIES_ID(species))
    {
    case SPECIES_SCATTERBUG:
        return sScatterbugForms[Random() % ARRAY_COUNT(sScatterbugForms)];
    case SPECIES_SPEWPA:
        return sSpewpaForms[Random() % ARRAY_COUNT(sSpewpaForms)];
    case SPECIES_VIVILLON:
        return sVivillonForms[Random() % ARRAY_COUNT(sVivillonForms)];
    }
    return species;
}

u32 GetSeasonalForm(u32 species)
{
    switch (GET_BASE_SPECIES_ID(species))
    {
    case SPECIES_DEERLING:
        return sDeerlingForms[GetSeason()];
    case SPECIES_SAWSBUCK:
        return sSawsbuckForms[GetSeason()];
    }
    return species;
}

u32 GetWildEncounterForm(u32 species)
{
    return GetSeasonalForm(GetRandomPatternForm(species));
}

void SeasonalFormUpdateParty(void)
{
    u32 i;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon = &gPlayerParty[i];
        u32 species = GetMonData(mon, MON_DATA_SPECIES);
        u32 base = GET_BASE_SPECIES_ID(species);
        u32 target;

        if ((base != SPECIES_DEERLING && base != SPECIES_SAWSBUCK) || GetMonData(mon, MON_DATA_IS_EGG))
            continue;
        target = GetSeasonalForm(species);
        if (target != species)
        {
            SetMonData(mon, MON_DATA_SPECIES, &target);
            CalculateMonStats(mon);
        }
    }
}
