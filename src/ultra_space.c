// Project Grounded: Ultra Space (achterin Altering Cave) en de Cosmog-lijn van Prof. Cozmo (zijn huis in Fallarbor).
//
// Portaal: Ultra_PickPortal kiest een willekeurige Ultra Beast-locatie waarvan de UB nog niet gevangen is
// (FLAG_ULTRA_*; Poipole: gekregen van de aliens). Zijn alle tien de UB's gevangen, dan gaat het portaal naar Necrozma; is die ook gevangen, dan
// willekeurig naar één van alle elf plekken. De kaarten en het warpscript maakt tools/grounded/maptools/ultra_space.py.
//
// Cosmoem -> Solgaleo of Lunala (evolutieconditie IF_GROUNDED_SUN_MOON, zie Ultra_CosmoemTarget):
//  1. Staat precies één van Solgaleo/Lunala als gevangen in de Pokédex, dan wordt het de andere. Zo wordt de tweede
//     Cosmog van Cozmo (die je pas krijgt na het laten zien van de eerste Solgaleo/Lunala) altijd de andere vorm,
//     zonder dat die Pokémon zelf gemarkeerd hoeft te worden (Cosmog kan niet fokken en komt nergens anders voor).
//  2. Anders: Solrock eerder gevangen dan Lunatone -> Solgaleo, Lunatone eerst -> Lunala (FLAG_ULTRA_SOLROCK_FIRST /
//     FLAG_ULTRA_LUNATONE_FIRST, gezet bij de eerste Pokédex-vangst van een van beide, Ultra_OnNewDexCaught).
//     Saves van vóór deze regel: is maar één van beide gevangen, dan telt die als eerste.
//  3. Geen van beide gevangen (of beide zonder volgorde): 'willekeurig', maar vast per Pokémon (bit van de
//     personality), zodat de twee evolutie-entries nooit allebei of geen van beide waar zijn.
#include "global.h"
#include "event_data.h"
#include "pokedex.h"
#include "pokemon.h"
#include "random.h"
#include "ultra_space.h"
#include "constants/flags.h"
#include "constants/species.h"

enum { ULTRA_SOLGALEO, ULTRA_LUNALA };

static const u16 sUltraFlags[] = {
    FLAG_ULTRA_NIHILEGO, FLAG_ULTRA_BUZZWOLE, FLAG_ULTRA_PHEROMOSA, FLAG_ULTRA_XURKITREE, FLAG_ULTRA_CELESTEELA,
    FLAG_ULTRA_KARTANA, FLAG_ULTRA_GUZZLORD, FLAG_ULTRA_POIPOLE, FLAG_ULTRA_STAKATAKA, FLAG_ULTRA_BLACEPHALON,
    FLAG_ULTRA_NECROZMA, // altijd als laatste
};
#define NUM_ULTRA_SPOTS ARRAY_COUNT(sUltraFlags)
#define ULTRA_NECROZMA_SPOT (NUM_ULTRA_SPOTS - 1)

static bool32 DexCaught(u32 species)
{
    return GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_CAUGHT);
}

void Ultra_OnNewDexCaught(u32 nationalDexNum)
{
    if (FlagGet(FLAG_ULTRA_SOLROCK_FIRST) || FlagGet(FLAG_ULTRA_LUNATONE_FIRST))
        return;
    if (nationalDexNum == NATIONAL_DEX_SOLROCK && !DexCaught(SPECIES_LUNATONE))
        FlagSet(FLAG_ULTRA_SOLROCK_FIRST);
    else if (nationalDexNum == NATIONAL_DEX_LUNATONE && !DexCaught(SPECIES_SOLROCK))
        FlagSet(FLAG_ULTRA_LUNATONE_FIRST);
}

u32 Ultra_CosmoemTarget(struct Pokemon *mon)
{
    bool32 sol = DexCaught(SPECIES_SOLGALEO), luna = DexCaught(SPECIES_LUNALA);
    bool32 solrock = DexCaught(SPECIES_SOLROCK), lunatone = DexCaught(SPECIES_LUNATONE);

    if (sol != luna)                    // tweede Cosmog: de vorm die je nog niet hebt
        return sol ? ULTRA_LUNALA : ULTRA_SOLGALEO;
    if (FlagGet(FLAG_ULTRA_SOLROCK_FIRST))
        return ULTRA_SOLGALEO;
    if (FlagGet(FLAG_ULTRA_LUNATONE_FIRST))
        return ULTRA_LUNALA;
    if (solrock != lunatone)            // oude save: alleen één van beide gevangen
        return solrock ? ULTRA_SOLGALEO : ULTRA_LUNALA;
    return (GetMonData(mon, MON_DATA_PERSONALITY) >> 16) & 1;
}

// special: VAR_RESULT = plek waar het portaal heen gaat (0-9 Ultra Beasts, 10 Necrozma).
void Ultra_PickPortal(void)
{
    u8 open[NUM_ULTRA_SPOTS];
    u32 i, n = 0;

    for (i = 0; i < ULTRA_NECROZMA_SPOT; i++)
    {
        if (!FlagGet(sUltraFlags[i]))
            open[n++] = i;
    }
    if (n != 0)
        gSpecialVar_Result = open[Random() % n];
    else if (!FlagGet(sUltraFlags[ULTRA_NECROZMA_SPOT]))
        gSpecialVar_Result = ULTRA_NECROZMA_SPOT;
    else
        gSpecialVar_Result = Random() % NUM_ULTRA_SPOTS;
}

// special: VAR_RESULT = aantal Ultra Beasts (zonder Necrozma) dat nog open staat.
void Ultra_CountOpen(void)
{
    u32 i, n = 0;

    for (i = 0; i < NUM_ULTRA_SPOTS; i++)
    {
        if (!FlagGet(sUltraFlags[i]))
            n++;
    }
    gSpecialVar_Result = n;
}

// special (Cozmo): VAR_RESULT = 0 geen Solgaleo/Lunala in het team, 1 Solgaleo, 2 Lunala (de eerste in het team).
void Ultra_FindPartySunMoon(void)
{
    u32 i;

    gSpecialVar_Result = 0;
    for (i = 0; i < CalculatePlayerPartyCount(); i++)
    {
        u32 species = GetMonData(&gPlayerParty[i], MON_DATA_SPECIES);
        if (GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG))
            continue;
        if (species == SPECIES_SOLGALEO || species == SPECIES_LUNALA)
        {
            gSpecialVar_Result = (species == SPECIES_SOLGALEO) ? 1 : 2;
            return;
        }
    }
}
