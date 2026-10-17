#ifndef GUARD_MON_VARIANTS_H
#define GUARD_MON_VARIANTS_H

// Kleurvarianten ("skins"): elke Pokémon krijgt uit zijn personality een variant.
// 0 = normaal, 1..6 = steeds zeldzamer en opvallender. Shiny staat hier los van.
#define MON_VARIANT_NORMAL 0
#define NUM_MON_VARIANTS   7

// Trainer-Pokémon zonder 'Variant:' in trainers.party: TRUE = variant uit de
// personality (zoals wild), FALSE = altijd normaal (ook Frontier-teams).
#define TRAINER_MON_VARIANTS_RANDOM FALSE // Jordi 15 okt: trainers eerst altijd normaal

struct VariantPalettes
{
    const u16 *normal;
    const u16 *variants; // (NUM_MON_VARIANTS - 1) * 16 kleuren
    const u8 *names;     // 6 Engelse namen, gescheiden door EOS
};

// Gegenereerd (src/data/pokemon/variant_palettes.h), eindigt op {NULL, NULL, NULL}.
extern const struct VariantPalettes gVariantPalettes[];

u32 GetVariantFromPersonality(u32 personality);
const u16 *GetVariantPalette(const u16 *normalPalette, u32 variant);
u32 SetPersonalityVariant(u32 personality, u32 variant, u32 nature);
u32 ApplyTrainerMonVariant(u32 personality, u32 trainerVariant, u32 nature);
const struct VariantPalettes *GetVariantEntry(const u16 *normalPalette);
const u8 *GetVariantName(const struct VariantPalettes *entry, u32 variant);

// Pokédex-kleurenpagina: per soort welke kleuren gezien/gevangen zijn.
#define VARIANT_DEX_SHINY 7
struct BoxPokemon;
void VariantDex_Record(u16 species, u32 personality, bool32 isShiny, bool32 caught);
void VariantDex_RecordBoxMon(struct BoxPokemon *boxMon, bool32 caught);
void VariantDex_SweepOwned(void);

#endif // GUARD_MON_VARIANTS_H
