// Project Grounded: de Azure Flute (Arceus, na Spear Pillar).
// Gebruiken vanuit de tas speelt data/scripts/azure_flute.inc af; dat vraagt hier een hint op over de volgende
// legendary die nog niet gevangen is. De lijst staat in src/data/azure_flute_hints.h en wordt gemaakt door
// tools/grounded/azure_flute.py (opnieuw draaien als er legendaries bijkomen).
// Een soort telt als afgehandeld als hij gevangen is (Pokédex) of als zijn ontmoeting voorgoed op is (goneFlag).
#include "global.h"
#include "event_data.h"
#include "pokedex.h"
#include "pokemon.h"
#include "string_util.h"
#include "constants/flags.h"
#include "constants/species.h"

struct AzureFluteHint
{
    u16 species;
    u16 goneFlag; // 0 = geen; anders: ontmoeting voorgoed op (verslagen zonder terugkeer, gift ontvangen)
    const u8 *text;
};

#include "data/azure_flute_hints.h"

// Welke hint de fluit de vorige keer gaf; volgende keer de volgende open soort (niet bewaard, hoeft ook niet).
static EWRAM_DATA u8 sAzureFluteCursor = 0;

static bool32 IsHintResolved(u32 i)
{
    const struct AzureFluteHint *h = &sAzureFluteHints[i];
    if (GetSetPokedexFlag(SpeciesToNationalPokedexNum(h->species), FLAG_GET_CAUGHT))
        return TRUE;
    if (h->goneFlag != 0 && FlagGet(h->goneFlag))
        return TRUE;
    return FALSE;
}

static u32 CountOpenHints(void)
{
    u32 i, n = 0;
    for (i = 0; i < ARRAY_COUNT(sAzureFluteHints); i++)
    {
        if (!IsHintResolved(i))
            n++;
    }
    return n;
}

static const u8 sText_OneLeft[] = _("The AZURE FLUTE hums a single note.\nOne legend is still unaccounted for.\p");
static const u8 sText_SomeLeft[] = _("The AZURE FLUTE hums.\n{STR_VAR_1} legends are still unaccounted for.\p");

// special: VAR_RESULT = aantal open soorten; bij > 0 staat de hint (met teller) in gStringVar4.
void AzureFlute_GetHint(void)
{
    u32 n = CountOpenHints();
    u32 i, k, count = ARRAY_COUNT(sAzureFluteHints);

    gSpecialVar_Result = n;
    if (n == 0)
        return;
    if (sAzureFluteCursor >= count)
        sAzureFluteCursor = 0;
    for (k = 0; k < count; k++)
    {
        i = (sAzureFluteCursor + k) % count;
        if (!IsHintResolved(i))
            break;
    }
    sAzureFluteCursor = (i + 1) % count;
    ConvertIntToDecimalStringN(gStringVar1, n, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringExpandPlaceholders(gStringVar4, n == 1 ? sText_OneLeft : sText_SomeLeft);
    StringAppend(gStringVar4, sAzureFluteHints[i].text);
}

// special (debug/emulatortests): markeer alle soorten uit de lijst als gevangen.
void AzureFlute_DebugCatchAll(void)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sAzureFluteHints); i++)
    {
        u32 dex = SpeciesToNationalPokedexNum(sAzureFluteHints[i].species);
        GetSetPokedexFlag(dex, FLAG_SET_SEEN);
        GetSetPokedexFlag(dex, FLAG_SET_CAUGHT);
    }
}
