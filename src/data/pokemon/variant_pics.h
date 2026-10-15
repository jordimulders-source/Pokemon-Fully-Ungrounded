// Poké Ball-patronen voor Voltorb en Electrode (tools/grounded/variants/ball_patterns.py).
// Variant 1..6 = Great, Ultra, Quick, Safari, Dusk, Master.

static const u32 sVariantFrontPic_VoltorbGreat[] = INCBIN_U32("graphics/pokemon/voltorb/ball_great/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbGreat[] = INCBIN_U32("graphics/pokemon/voltorb/ball_great/back.4bpp.smol");
static const u32 sVariantFrontPic_VoltorbUltra[] = INCBIN_U32("graphics/pokemon/voltorb/ball_ultra/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbUltra[] = INCBIN_U32("graphics/pokemon/voltorb/ball_ultra/back.4bpp.smol");
static const u32 sVariantFrontPic_VoltorbQuick[] = INCBIN_U32("graphics/pokemon/voltorb/ball_quick/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbQuick[] = INCBIN_U32("graphics/pokemon/voltorb/ball_quick/back.4bpp.smol");
static const u32 sVariantFrontPic_VoltorbSafari[] = INCBIN_U32("graphics/pokemon/voltorb/ball_safari/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbSafari[] = INCBIN_U32("graphics/pokemon/voltorb/ball_safari/back.4bpp.smol");
static const u32 sVariantFrontPic_VoltorbDusk[] = INCBIN_U32("graphics/pokemon/voltorb/ball_dusk/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbDusk[] = INCBIN_U32("graphics/pokemon/voltorb/ball_dusk/back.4bpp.smol");
static const u32 sVariantFrontPic_VoltorbMaster[] = INCBIN_U32("graphics/pokemon/voltorb/ball_master/anim_front.4bpp.smol");
static const u32 sVariantBackPic_VoltorbMaster[] = INCBIN_U32("graphics/pokemon/voltorb/ball_master/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeGreat[] = INCBIN_U32("graphics/pokemon/electrode/ball_great/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeGreat[] = INCBIN_U32("graphics/pokemon/electrode/ball_great/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeUltra[] = INCBIN_U32("graphics/pokemon/electrode/ball_ultra/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeUltra[] = INCBIN_U32("graphics/pokemon/electrode/ball_ultra/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeQuick[] = INCBIN_U32("graphics/pokemon/electrode/ball_quick/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeQuick[] = INCBIN_U32("graphics/pokemon/electrode/ball_quick/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeSafari[] = INCBIN_U32("graphics/pokemon/electrode/ball_safari/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeSafari[] = INCBIN_U32("graphics/pokemon/electrode/ball_safari/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeDusk[] = INCBIN_U32("graphics/pokemon/electrode/ball_dusk/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeDusk[] = INCBIN_U32("graphics/pokemon/electrode/ball_dusk/back.4bpp.smol");
static const u32 sVariantFrontPic_ElectrodeMaster[] = INCBIN_U32("graphics/pokemon/electrode/ball_master/anim_front.4bpp.smol");
static const u32 sVariantBackPic_ElectrodeMaster[] = INCBIN_U32("graphics/pokemon/electrode/ball_master/back.4bpp.smol");

static const struct VariantMonPic sVariantMonPics[] =
{
    {SPECIES_VOLTORB, 1, sVariantFrontPic_VoltorbGreat, sVariantBackPic_VoltorbGreat},
    {SPECIES_VOLTORB, 2, sVariantFrontPic_VoltorbUltra, sVariantBackPic_VoltorbUltra},
    {SPECIES_VOLTORB, 3, sVariantFrontPic_VoltorbQuick, sVariantBackPic_VoltorbQuick},
    {SPECIES_VOLTORB, 4, sVariantFrontPic_VoltorbSafari, sVariantBackPic_VoltorbSafari},
    {SPECIES_VOLTORB, 5, sVariantFrontPic_VoltorbDusk, sVariantBackPic_VoltorbDusk},
    {SPECIES_VOLTORB, 6, sVariantFrontPic_VoltorbMaster, sVariantBackPic_VoltorbMaster},
    {SPECIES_ELECTRODE, 1, sVariantFrontPic_ElectrodeGreat, sVariantBackPic_ElectrodeGreat},
    {SPECIES_ELECTRODE, 2, sVariantFrontPic_ElectrodeUltra, sVariantBackPic_ElectrodeUltra},
    {SPECIES_ELECTRODE, 3, sVariantFrontPic_ElectrodeQuick, sVariantBackPic_ElectrodeQuick},
    {SPECIES_ELECTRODE, 4, sVariantFrontPic_ElectrodeSafari, sVariantBackPic_ElectrodeSafari},
    {SPECIES_ELECTRODE, 5, sVariantFrontPic_ElectrodeDusk, sVariantBackPic_ElectrodeDusk},
    {SPECIES_ELECTRODE, 6, sVariantFrontPic_ElectrodeMaster, sVariantBackPic_ElectrodeMaster},
};
