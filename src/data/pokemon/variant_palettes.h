// Gegenereerd door tools/grounded/variants/variants.py; niet met de hand bewerken.

#if (P_FAMILY_BULBASAUR)
static const u16 sVariants_Bulbasaur[] = INCBIN_U16("graphics/pokemon/bulbasaur/variants.gbapal");
#endif
#if (P_FAMILY_BULBASAUR)
static const u16 sVariants_Ivysaur[] = INCBIN_U16("graphics/pokemon/ivysaur/variants.gbapal");
#endif
#if (P_FAMILY_BULBASAUR)
static const u16 sVariants_Venusaur[] = INCBIN_U16("graphics/pokemon/venusaur/variants.gbapal");
#endif
#if (P_FAMILY_CHARMANDER)
static const u16 sVariants_Charmander[] = INCBIN_U16("graphics/pokemon/charmander/variants.gbapal");
#endif
#if (P_FAMILY_CHARMANDER)
static const u16 sVariants_Charmeleon[] = INCBIN_U16("graphics/pokemon/charmeleon/variants.gbapal");
#endif
#if (P_FAMILY_CHARMANDER)
static const u16 sVariants_Charizard[] = INCBIN_U16("graphics/pokemon/charizard/variants.gbapal");
#endif
#if (P_FAMILY_SQUIRTLE)
static const u16 sVariants_Squirtle[] = INCBIN_U16("graphics/pokemon/squirtle/variants.gbapal");
#endif
#if (P_FAMILY_SQUIRTLE)
static const u16 sVariants_Wartortle[] = INCBIN_U16("graphics/pokemon/wartortle/variants.gbapal");
#endif
#if (P_FAMILY_SQUIRTLE)
static const u16 sVariants_Blastoise[] = INCBIN_U16("graphics/pokemon/blastoise/variants.gbapal");
#endif

const struct VariantPalettes gVariantPalettes[] =
{
#if (P_FAMILY_BULBASAUR)
    {gMonPalette_Bulbasaur, sVariants_Bulbasaur},
#endif
#if (P_FAMILY_BULBASAUR)
    {gMonPalette_Ivysaur, sVariants_Ivysaur},
#endif
#if (P_FAMILY_BULBASAUR)
    {gMonPalette_Venusaur, sVariants_Venusaur},
#endif
#if (P_FAMILY_CHARMANDER)
    {gMonPalette_Charmander, sVariants_Charmander},
#endif
#if (P_FAMILY_CHARMANDER)
    {gMonPalette_Charmeleon, sVariants_Charmeleon},
#endif
#if (P_FAMILY_CHARMANDER)
    {gMonPalette_Charizard, sVariants_Charizard},
#endif
#if (P_FAMILY_SQUIRTLE)
    {gMonPalette_Squirtle, sVariants_Squirtle},
#endif
#if (P_FAMILY_SQUIRTLE)
    {gMonPalette_Wartortle, sVariants_Wartortle},
#endif
#if (P_FAMILY_SQUIRTLE)
    {gMonPalette_Blastoise, sVariants_Blastoise},
#endif
    {NULL, NULL},
};
