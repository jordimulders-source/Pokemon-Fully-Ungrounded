#include "global.h"
#include "battle_main.h"
#include "mon_variants.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "constants/characters.h"

// Kansen in promille, cumulatief: 75% normaal, dan 10 / 6 / 4 / 3 / 1,5 / 0,5%.
// Debug/emulatortests: 1..7 forceert variant 0..6 voor elke Pokémon.
EWRAM_DATA u8 gDebugForcedVariant = 0;

static const u16 sVariantThresholds[NUM_MON_VARIANTS] = {750, 850, 910, 950, 980, 995, 1000};

// Alleen de bovenste 16 bits: geslacht (laag byte) en nature-correcties (een paar
// eenheden) laten de variant zo met rust.
static u32 VariantFromPersonality(u32 personality)
{
    u32 h = personality >> 16;
    u32 roll, i;

    h *= 0x045D9F3B;
    h ^= h >> 16;
    h *= 0x045D9F3B;
    h ^= h >> 16;
    roll = h % 1000;
    for (i = 0; i < NUM_MON_VARIANTS - 1; i++)
    {
        if (roll < sVariantThresholds[i])
            break;
    }
    return i;
}

u32 GetVariantFromPersonality(u32 personality)
{
    if (gDebugForcedVariant != 0)
        return gDebugForcedVariant - 1;
    return VariantFromPersonality(personality);
}

const u16 *GetVariantPalette(const u16 *normalPalette, u32 variant)
{
    static const struct VariantPalettes *sLast = NULL;
    u32 i;

    if (variant == MON_VARIANT_NORMAL || variant >= NUM_MON_VARIANTS || normalPalette == NULL)
        return NULL;

    if (sLast == NULL || sLast->normal != normalPalette)
    {
        sLast = NULL;
        for (i = 0; gVariantPalettes[i].normal != NULL; i++)
        {
            if (gVariantPalettes[i].normal == normalPalette)
            {
                sLast = &gVariantPalettes[i];
                break;
            }
        }
        if (sLast == NULL)
            return NULL;
    }
    return &sLast->variants[(variant - 1) * 16];
}

// Zoekt de dichtstbijzijnde bovenste helft die de gevraagde variant geeft, en
// zet daarna de nature terug (dat verschuift de personality maar een paar eenheden).
u32 SetPersonalityVariant(u32 personality, u32 variant, u32 nature)
{
    u32 i, p;

    if (variant >= NUM_MON_VARIANTS)
        return personality;
    for (i = 0; i < 0x10000; i++)
    {
        p = (((personality >> 16) + i) << 16) | (personality & 0xFFFF);
        ModifyPersonalityForNature(&p, nature);
        if (VariantFromPersonality(p) == variant)
            return p;
    }
    return personality;
}

u32 ApplyTrainerMonVariant(u32 personality, u32 trainerVariant, u32 nature)
{
    if (trainerVariant != 0)
        return SetPersonalityVariant(personality, trainerVariant - 1, nature);
    if (!TRAINER_MON_VARIANTS_RANDOM)
        return SetPersonalityVariant(personality, MON_VARIANT_NORMAL, nature);
    return personality;
}

const struct VariantPalettes *GetVariantEntry(const u16 *normalPalette)
{
    u32 i;

    if (normalPalette == NULL)
        return NULL;
    for (i = 0; gVariantPalettes[i].normal != NULL; i++)
    {
        if (gVariantPalettes[i].normal == normalPalette)
            return &gVariantPalettes[i];
    }
    return NULL;
}

// variant 1..6; de namen staan achter elkaar, gescheiden door EOS
const u8 *GetVariantName(const struct VariantPalettes *entry, u32 variant)
{
    const u8 *str;

    if (entry == NULL || variant == MON_VARIANT_NORMAL || variant >= NUM_MON_VARIANTS)
        return NULL;
    str = entry->names;
    while (--variant != 0)
    {
        while (*str != EOS)
            str++;
        str++;
    }
    return str;
}

void VariantDex_Record(u16 species, u32 personality, bool32 isShiny, bool32 caught)
{
    u8 bit;

    if (species == SPECIES_NONE || species >= NUM_SPECIES)
        return;
    bit = isShiny ? VARIANT_DEX_SHINY : GetVariantFromPersonality(personality);
    gSaveBlock1Ptr->variantDexSeen[species] |= 1 << bit;
    if (caught)
        gSaveBlock1Ptr->variantDexCaught[species] |= 1 << bit;
}

void VariantDex_RecordBoxMon(struct BoxPokemon *boxMon, bool32 caught)
{
    u16 species;

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return;
    species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    VariantDex_Record(species, GetBoxMonData(boxMon, MON_DATA_PERSONALITY), GetBoxMonData(boxMon, MON_DATA_IS_SHINY), caught);
}

// Alles wat de speler nu heeft telt als gezien en gevangen (geschenken, eieren,
// evoluties, ruilen en oude saves); draait bij het openen van de Pokédex.
void VariantDex_SweepOwned(void)
{
    u32 i, j;

    for (i = 0; i < gPlayerPartyCount; i++)
        VariantDex_RecordBoxMon(&gPlayerParty[i].box, TRUE);
    for (i = 0; i < TOTAL_BOXES_COUNT; i++)
    {
        for (j = 0; j < IN_BOX_COUNT; j++)
            VariantDex_RecordBoxMon(GetBoxedMonPtr(i, j), TRUE);
    }
}
