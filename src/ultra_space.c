// Project Grounded: de Cosmog-lijn van Prof. Cozmo (zijn huis in Fallarbor).
// (Ultra Space zelf, met het portaal in Altering Cave, is in Fully Ungrounded verwijderd.)
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
#include "ultra_space.h"
#include "constants/flags.h"
#include "constants/species.h"

enum { ULTRA_SOLGALEO, ULTRA_LUNALA };

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
