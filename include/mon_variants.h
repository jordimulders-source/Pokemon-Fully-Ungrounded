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
};

// Gegenereerd (src/data/pokemon/variant_palettes.h), eindigt op {NULL, NULL}.
extern const struct VariantPalettes gVariantPalettes[];

u32 GetVariantFromPersonality(u32 personality);
const u16 *GetVariantPalette(const u16 *normalPalette, u32 variant);
u32 SetPersonalityVariant(u32 personality, u32 variant, u32 nature);
u32 ApplyTrainerMonVariant(u32 personality, u32 trainerVariant, u32 nature);
const u32 *GetVariantMonPic(u16 species, u32 personality, bool32 isFrontPic);

#endif // GUARD_MON_VARIANTS_H
