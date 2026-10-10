// Project Grounded: lichte gevechtsintro's, tweede reeks (Articuno, Zapdos, Moltres, Zacian/Zamazenta, Xerneas/Yveltal).
// Wordt onderaan src/battle_transition.c ingevoegd, na src/data/legend_intros.h (gebruikt de GI_/LI_-hulpjes en de
// route-transitie-runner). Art: tools/grounded/legend_intros2.py. De achtergronden zijn de echte kaarten waar de
// legendary staat; daarvoor gebruiken deze intro's de BG-paletten 10-15 (en 4-9 voor het uitgedoofde Glimwood): de
// wereld is dan al zwart en ligt helemaal onder het (ondoorzichtige) BG0-beeld. Die paletten worden pas geladen als het
// beeld verschijnt, zodat de wereld tijdens het uitfaden zijn eigen kleuren houdt.

#include "legend_intros2_gen.h"

#define LI2_PALS_MAP   (0x3F << 10)    // BG 10-15
#define LI2_PALS_DIM   (0x3F << 4)     // BG 4-9

static const struct OamData sLI2_Oam16x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(16x32),
    .size = SPRITE_SIZE(16x32),
    .priority = 0,
};

static const struct OamData sLI2_Oam32x16 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 0,
};

static u32 LI2_MonBit(u8 id)
{
    return id < MAX_SPRITES ? 1 << (16 + gSprites[id].oam.paletteNum) : 0;
}

// alle paletten behalve 'bg' (onze BG-paletten) en 'keep' (onze sprites) op een kleur
static void LI2_FillField(u32 bg, u32 keep, u16 color)
{
    u32 i;
    for (i = 0; i < 32; i++)
    {
        if (((bg | keep) >> i) & 1)
            continue;
        CpuFill16(color, &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
    }
}

// de wereld in 8 frames naar zwart; vanaf 'start' is ons beeld er en blijft de rest zwart
static void LI2_FadeWorld(s32 t, s32 start, u32 bg, u32 keep)
{
    if (t < start)
        BlendPalettes(PALETTES_ALL & ~keep, min(t * 2, 16), RGB_BLACK);
    else
        LI2_FillField(bg, keep, RGB_BLACK);
}

static bool32 LI2_WhiteOut(s32 t, s32 end, u32 bg, u32 keep)
{
    s32 k;
    if (t < end - 4)
        return FALSE;
    k = min((t - (end - 4)) * 4 + 4, 16);
    BlendPalettes(bg | keep, k, RGB_WHITE);
    LI2_FillField(bg, keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
    return t >= end;
}

// het beeld komt in 8 frames uit het zwart op
static void LI2_FadeIn(s32 t, s32 start, u32 bg)
{
    if (t >= start && t < start + 8)
        BlendPalettes(bg, 16 - (t - start) * 2, RGB_BLACK);
}

// HBlank-golf op BG0HOFS (hitte, splijten); waarde per beeldlijn. Vóór 'start' is de golf nog niet aan (de kaart kan
// de scanline-buffer nog gebruiken, bijv. het licht in een donkere grot): dan een eigen kladbuffer.
static EWRAM_DATA s16 sLI2_NoHofs[DISPLAY_HEIGHT] = {0};

static s16 *LI2_Hofs(s32 t, s32 start)
{
    return t > start ? (s16 *)gScanlineEffectRegBuffers[0] : sLI2_NoHofs;
}

// =====================================================================================================================
// Articuno (Shoal Cave, Frozen Depths: "It has been sitting here so long the ice thinks it's furniture."): er groeien
// ijsvarens over het beeld, van de randen naar binnen, over de echte grot heen (BG0 additief over de wereld geblend; de
// varens zijn één beeld waarvan de 15 kleuren de groeifasen zijn). In het nog heldere midden verschijnt Articuno (achter
// het ijs), sneeuwvlokken dwarrelen, en dan vriest ook het midden dicht: Articuno zit ín het ijs. Het ijs barst vanuit
// het midden en spat in brokken uiteen.
static const u32 sLegArticuno_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_articuno.4bpp.smol");
static const u32 sLegArticuno_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_articuno_maps.bin.smol");
static const u16 sLegArticuno_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_articuno.gbapal");

enum { ART_MAP_FROST, ART_MAP_CRACK };
#define ART_TAG_SNOW    0x5A70
#define ART_TAG_CHUNK   0x5A71
#define ART_GROW        2     // fase 1 groeit; fase i op ART_GROW + (i - 1) * ART_STEP (t/m 13)
#define ART_STEP        5
#define ART_MON         34    // Articuno in het midden
#define ART_CRY         46
#define ART_FREEZE      74    // fase 14 (rand van het midden), fase 15 zes frames later
#define ART_CRACK       92
#define ART_SHATTER     104
#define ART_END         124
#define ART_SNOWS       10
#define ART_CHUNKS      10
#define ART_X           120
#define ART_Y           78

static const u16 sArtIce[3] = {RGB(13, 19, 27), RGB(9, 14, 23), RGB(17, 23, 29)};
static const u8 sArtSnowX[ART_SNOWS] = {14, 40, 66, 92, 118, 144, 170, 196, 222, 30};
static const u8 sArtSnowOfs[ART_SNOWS] = {0, 70, 30, 110, 50, 140, 20, 90, 60, 120};

static s32 ArtPhaseStart(u32 i)
{
    if (i <= 13)
        return ART_GROW + (i - 1) * ART_STEP;
    return i == 14 ? ART_FREEZE : ART_FREEZE + 6;
}

static void RTArticuno_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegArticuno_Tiles, sLegArticuno_Maps);
    LoadPalette(sLegArticuno_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    CpuFill16(0, &gPlttBufferUnfaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);
    CpuFill16(0, &gPlttBufferFaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);
    LI_ResetSprites();
    for (i = 0; i < ART_SNOWS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_Snowflakes, 16 * 224 / 2, gBattleAnimSpritePal_Snowflakes, ART_TAG_SNOW, &sLI2_Oam16x32, sArtSnowX[i], -32, 0);
    for (i = 0; i < ART_CHUNKS; i++)
        LI_Make(ART_SNOWS + i, gBattleAnimSpriteGfx_IceChunk, 32 * 160 / 2, gBattleAnimSpritePal_IceChunk, ART_TAG_CHUNK, &sGI_Oam32, ART_X, ART_Y, 0);
    task->tGiSprite0 = GI_MonPic(SPECIES_ARTICUNO, ART_X, ART_Y);
    if (task->tGiSprite0 < MAX_SPRITES)
        gSprites[task->tGiSprite0].oam.priority = 1; // achter het ijs (BG0)
    // het ijs telt op bij wat eronder ligt (zwart = niets): de grot blijft zichtbaar tot hij dichtvriest
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                               | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(11, 16));
    // de grot heeft vensters aan (verlichting); daarbinnen moet het blenden ook mogen
    SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
}

static bool8 RTArticuno_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, age;
    u32 keep, artBit;
    u16 *u = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s, *art = GI_Sprite(task->tGiSprite0);

    artBit = LI2_MonBit(task->tGiSprite0);
    keep = artBit | GI_SpritePalBit(ART_TAG_SNOW) | GI_SpritePalBit(ART_TAG_CHUNK);
    GI_ResetPals(keep);
    LoadPalette(sLegArticuno_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    // groeifasen: nog niet = zwart (telt niets op), net gegroeid = wit, daarna ijsblauw
    u[0] = 0;
    for (i = 1; i < 16; i++)
    {
        age = t - ArtPhaseStart(i);
        u[i] = age < 0 ? 0 : (age < 3 ? RGB_WHITE : sArtIce[i % 3]);
    }
    CpuCopy16(u, &gPlttBufferFaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);

    if (t == 0)
        GI_ShowMap(ART_MAP_FROST);
    if (t == ART_CRACK)
    {
        GI_ShowMap(ART_MAP_CRACK);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(14, 16));
    }

    // Articuno verschijnt uit het wit in het nog heldere midden, zwevend
    if (t >= ART_MON)
    {
        k = t - ART_MON;
        art->invisible = FALSE;
        art->y2 = Sin((t * 6) & 0xFF, 3);
        if (k < 12)
            BlendPalettes(artBit, 16 - k * 4 / 3, RGB_WHITE);
    }

    // sneeuwvlokken dwarrelen omlaag
    for (i = 0; i < ART_SNOWS; i++)
    {
        s = LI_S(i);
        k = t + sArtSnowOfs[i];
        s->invisible = (t < 4 || t >= ART_SHATTER);
        s->x = sArtSnowX[i] + Sin((k * 5) & 0xFF, 6);
        s->y = ((k * 3 / 2) & 0xFF) - 40;
        LI_Frame(i, ART_TAG_SNOW, i % 7, 8);
    }

    // het ijs spat uiteen
    for (i = 0; i < ART_CHUNKS; i++)
    {
        s = LI_S(ART_SNOWS + i);
        k = t - ART_SHATTER;
        if (k < 0)
            continue;
        if (k == 0)
        {
            u32 ang = i * 256 / ART_CHUNKS + (Random() & 15);
            sLI_Phys[ART_SNOWS + i][0] = ART_X << 4;
            sLI_Phys[ART_SNOWS + i][1] = ART_Y << 4;
            sLI_Phys[ART_SNOWS + i][2] = Cos(ang & 0xFF, 56 + (Random() & 15));
            sLI_Phys[ART_SNOWS + i][3] = Sin(ang & 0xFF, 48 + (Random() & 15)) - 16;
            LI_Frame(ART_SNOWS + i, ART_TAG_CHUNK, i % 3, 16);
        }
        sLI_Phys[ART_SNOWS + i][0] += sLI_Phys[ART_SNOWS + i][2];
        sLI_Phys[ART_SNOWS + i][1] += sLI_Phys[ART_SNOWS + i][3];
        sLI_Phys[ART_SNOWS + i][3] += 4;
        s->x = sLI_Phys[ART_SNOWS + i][0] >> 4;
        s->y = sLI_Phys[ART_SNOWS + i][1] >> 4;
        s->invisible = FALSE;
    }

    // geluid
    if (t == 2 || t == 26 || t == 50)
        PlaySE(SE_ICE_CRACK);
    if (t == 12)
        PlaySE(SE_M_HAIL);
    if (t == ART_CRY)
        PlayCry_Normal(SPECIES_ARTICUNO, 0);
    if (t == ART_FREEZE)
        PlaySE(SE_M_BLIZZARD);
    if (t == ART_CRACK || t == ART_CRACK + 6)
        PlaySE(SE_ICE_CRACK);
    if (t == ART_SHATTER)
        PlaySE(SE_ICE_BREAK);

    GI_Shake((t >= ART_CRACK && t < ART_SHATTER + 8) ? (t >= ART_SHATTER ? 3 : 1) : 0);
    GI_Flash(t, ART_SHATTER, 8, 12, keep, RGB_WHITE);
    if (GI_WhiteOut(t, ART_END, keep))
    {
        for (i = 0; i < ART_SNOWS + ART_CHUNKS; i++)
            LI_S(i)->invisible = TRUE;
        art->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTArticuno_Finish(struct Task *task)
{
    GI_Shake(0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    LI_DestroySprites();
    GI_DestroyMonPic(task->tGiSprite0);
    GI_FreeTag(ART_TAG_SNOW);
    GI_FreeTag(ART_TAG_CHUNK);
    GI_Free();
}

static const struct RouteTransition sRT_LegendArticuno =
{
    sPikachu_Tileset, 32, sLegArticuno_Pal + 32, 1, 1, 0, RTArticuno_Init, RTArticuno_Update, RTArticuno_Finish
};

static void Task_LegendArticuno(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendArticuno);
}

// =====================================================================================================================
// Zapdos (Route 119, de richel boven het Weather Institute: "It's not a forecast. It's a tenant."): het instituut 's
// nachts in de regen. Bij elke bliksem licht alles op en staat Zapdos er als zwart silhouet, steeds dichterbij: eerst
// klein op de klif, dan boven de koepels, dan vlak voor je, in kleur en vol vonken, met onderin de weersvoorspelling.
// Drie bliksems slaan tegelijk in, wit.
static const u32 sLegZapdos_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_zapdos.4bpp.smol");
static const u32 sLegZapdos_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_zapdos_maps.bin.smol");
static const u16 sLegZapdos_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_zapdos.gbapal");

enum { ZAP_MAP_INSTITUTE, ZAP_MAP_CAPTION };
#define ZAP_TAG_RAIN    0x5A72
#define ZAP_TAG_BOLT    0x5A73
#define ZAP_TAG_SPARK   0x5A74
#define ZAP_SHOW        8
#define ZAP_F1          26
#define ZAP_F2          52
#define ZAP_F3          78
#define ZAP_STRIKE      108
#define ZAP_END         126
#define ZAP_RAINS       12
#define ZAP_BOLTS       15    // drie kolommen van vijf
#define ZAP_SPARKS      4
#define ZAP_NIGHT       RGB(1, 1, 5)

static const u8 sZapRainX[ZAP_RAINS] = {0, 150, 60, 210, 30, 180, 90, 240, 120, 15, 165, 75};
static const u8 sZapRainY[ZAP_RAINS] = {0, 40, 80, 120, 160, 200, 240, 20, 60, 100, 140, 180};
// bliksemkolom per inslag: x en de eerste kolom
static const u8 sZapBoltX[3] = {200, 40, 120};

static void ZapBolt(u32 col, s32 x, bool32 show)
{
    u32 j;
    for (j = 0; j < 5; j++)
    {
        struct Sprite *s = LI_S(ZAP_RAINS + col * 5 + j);
        s->invisible = !show;
        s->x = x + ((j & 1) ? 3 : 0);
        s->y = 16 + j * 32;
    }
}

static void RTZapdos_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegZapdos_Tiles, sLegZapdos_Maps);
    LI_ResetSprites();
    for (i = 0; i < ZAP_RAINS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_RainDrops, 16 * 224 / 2, gBattleAnimSpritePal_RainDrops, ZAP_TAG_RAIN, &sLI2_Oam16x32, 0, -40, 1);
    for (i = 0; i < ZAP_BOLTS; i++)
    {
        LI_Make(ZAP_RAINS + i, gBattleAnimSpriteGfx_Lightning, 32 * 160 / 2, gBattleAnimSpritePal_Lightning2, ZAP_TAG_BOLT, &sGI_Oam32, 0, 0, 0);
        LI_Frame(ZAP_RAINS + i, ZAP_TAG_BOLT, i % 5, 16);
    }
    for (i = 0; i < ZAP_SPARKS; i++)
        LI_Make(ZAP_RAINS + ZAP_BOLTS + i, gBattleAnimSpriteGfx_Electricity, 32 * 128 / 2, gBattleAnimSpritePal_ElectricOrbs, ZAP_TAG_SPARK, &sGI_Oam32, 0, 0, 0);
    task->tGiSprite0 = LI_MonPicAffine(SPECIES_ZAPDOS, 120, 70);
    GI_Sprite(task->tGiSprite0)->subpriority = 2;
}

static bool8 RTZapdos_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, lvl = 12, white = 0, dx = 0;
    u32 keep, zapBit;
    struct Sprite *s, *zap = GI_Sprite(task->tGiSprite0);
    static const u8 sFlashes[4] = {ZAP_F1, ZAP_F2, ZAP_F3, ZAP_STRIKE};

    zapBit = LI2_MonBit(task->tGiSprite0);
    keep = zapBit | GI_SpritePalBit(ZAP_TAG_RAIN) | GI_SpritePalBit(ZAP_TAG_BOLT) | GI_SpritePalBit(ZAP_TAG_SPARK);
    GI_ResetPals(keep);
    if (t >= ZAP_SHOW)
        LoadPalette(sLegZapdos_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
    if (t == ZAP_SHOW)
        GI_KillFieldWindows();
    if (t == ZAP_SHOW + 1) // een frame na de paletten (die gaan pas in de VBlank over)
        GI_ShowMap(ZAP_MAP_INSTITUTE);

    // nacht; bij een bliksem eerst wit, dan de echte kleuren die weer donker worden
    for (i = 0; i < 4; i++)
    {
        k = t - sFlashes[i];
        if (k >= 0 && k < 2)
            white = 9;
        else if (k >= 2 && k < 13)
            lvl = min(lvl, k - 2);
    }
    if (t >= ZAP_F3 + 13)
        lvl = min(lvl, 6 + (Random() & 1) * 2); // Zapdos licht het instituut zelf op
    if (t >= ZAP_SHOW)
    {
        if (white)
            BlendPalettes(LI2_PALS_MAP, white, RGB_WHITE);
        else
            BlendPalettes(LI2_PALS_MAP, max(lvl, 16 - (t - ZAP_SHOW)), ZAP_NIGHT); // komt uit het zwart op
    }
    if (t == ZAP_F3)
        GI_ShowRows(ZAP_MAP_CAPTION, 18, 20);

    // regen, schuin
    for (i = 0; i < ZAP_RAINS; i++)
    {
        s = LI_S(i);
        s->invisible = t < ZAP_SHOW;
        s->x = ((sZapRainX[i] - t * 3) & 0xFF) - 8;
        s->y = ((sZapRainY[i] + t * 9) & 0xFF) - 40;
    }

    // bliksems
    ZapBolt(0, sZapBoltX[0], t >= ZAP_F1 && t < ZAP_F1 + 5);
    ZapBolt(1, sZapBoltX[1], t >= ZAP_F2 && t < ZAP_F2 + 5);
    ZapBolt(2, sZapBoltX[2], t >= ZAP_F3 && t < ZAP_F3 + 4);
    if (t >= ZAP_STRIKE && t < ZAP_STRIKE + 10)
    {
        ZapBolt(0, 56, TRUE);
        ZapBolt(1, 184, TRUE);
        ZapBolt(2, 120, TRUE);
    }

    // Zapdos: alleen te zien als het bliksemt, als silhouet; daarna vlak voor je, in kleur
    zap->invisible = TRUE;
    if (t >= ZAP_F1 && t < ZAP_F1 + 9)
    {
        zap->invisible = FALSE;
        zap->x = 52;
        zap->y = 30;
        LI_Affine(task->tGiSprite0, 120, 0);
        BlendPalettes(zapBit, 16, RGB_BLACK);
    }
    else if (t >= ZAP_F2 && t < ZAP_F2 + 11)
    {
        zap->invisible = FALSE;
        zap->x = 172;
        zap->y = 46;
        LI_Affine(task->tGiSprite0, 232, 0);
        BlendPalettes(zapBit, 16, RGB_BLACK);
    }
    else if (t >= ZAP_F3)
    {
        k = min(t - ZAP_F3, 20);
        zap->invisible = FALSE;
        zap->x = 120;
        zap->y = 70;
        LI_Affine(task->tGiSprite0, 320 + k * 8, 0);
        if (t < ZAP_F3 + 3)
            BlendPalettes(zapBit, 16, RGB_BLACK);
        else if (t < ZAP_F3 + 7)
            BlendPalettes(zapBit, 10, RGB_WHITE);
    }

    // vonken rond Zapdos
    for (i = 0; i < ZAP_SPARKS; i++)
    {
        s = LI_S(ZAP_RAINS + ZAP_BOLTS + i);
        s->invisible = t < ZAP_F3 + 4 || ((t + i) & 3) == 0;
        s->x = 120 + Cos((t * 7 + i * 64) & 0xFF, 50);
        s->y = 66 + Sin((t * 7 + i * 64) & 0xFF, 38);
        LI_Frame(ZAP_RAINS + ZAP_BOLTS + i, ZAP_TAG_SPARK, ((t >> 1) + i) & 3, 16);
    }

    // geluid
    if (t == ZAP_F1 + 3)
        PlaySE(SE_THUNDER);
    if (t == ZAP_F2 + 2)
        PlaySE(SE_THUNDER2);
    if (t == ZAP_F3)
        PlaySE(SE_M_THUNDER_WAVE);
    if (t == ZAP_F3 + 4)
        PlayCry_Normal(SPECIES_ZAPDOS, 0);
    if (t == ZAP_STRIKE)
        PlaySE(SE_M_THUNDERBOLT);

    if (t >= ZAP_STRIKE && t < ZAP_STRIKE + 12)
        dx = LI_ShakeAmp(3);
    GI_Shake(t >= ZAP_STRIKE && t < ZAP_STRIKE + 12 ? 3 : 0);
    zap->x2 = dx;
    LI2_FadeWorld(t, ZAP_SHOW, LI2_PALS_MAP, keep);
    if (LI2_WhiteOut(t, ZAP_END, LI2_PALS_MAP, keep))
    {
        for (i = 0; i < ZAP_RAINS + ZAP_BOLTS + ZAP_SPARKS; i++)
            LI_S(i)->invisible = TRUE;
        zap->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTZapdos_Finish(struct Task *task)
{
    GI_Shake(0);
    LI_DestroySprites();
    LI_DestroyMonPic(task->tGiSprite0);
    GI_FreeTag(ZAP_TAG_RAIN);
    GI_FreeTag(ZAP_TAG_BOLT);
    GI_FreeTag(ZAP_TAG_SPARK);
    GI_Free();
}

static const struct RouteTransition sRT_LegendZapdos =
{
    sPikachu_Tileset, 32, sLegZapdos_Pal + 5 * 16, 1, 1, SE_RAIN, RTZapdos_Init, RTZapdos_Update, RTZapdos_Finish
};

static void Task_LegendZapdos(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendZapdos);
}

// =====================================================================================================================
// Moltres (de kraterrand van Mt. Chimney: "The lava is warming its feet on MOLTRES."): het lavameer op de top van
// bovenaf, de lucht trilt van de hitte (golf per beeldlijn), sintels stijgen op. Moltres staat met zijn voeten in de
// lava, schreeuwt en stijgt op, naar de camera toe (van bovenaf = groter), in een ring van vlammen. Sky Attack: hij
// gloeit wit op, de krater kleurt mee, en hij duikt recht op je af.
static const u32 sLegMoltres_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_moltres.4bpp.smol");
static const u32 sLegMoltres_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_moltres_maps.bin.smol");
static const u16 sLegMoltres_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_moltres.gbapal");

#define MOL_TAG_EMBER   0x5A75
#define MOL_TAG_FIRE    0x5A76
#define MOL_SHOW        8
#define MOL_CRY         26
#define MOL_RISE        32
#define MOL_RISE_LEN    26
#define MOL_CHARGE      (MOL_RISE + MOL_RISE_LEN)
#define MOL_DIVE        84
#define MOL_DIVE_LEN    14
#define MOL_END         110
#define MOL_EMBERS      8
#define MOL_FLAMES      6
#define MOL_X           120
#define MOL_Y           88

static const u8 sMolEmberX[MOL_EMBERS] = {24, 62, 98, 136, 172, 210, 44, 190};
static const u8 sMolEmberOfs[MOL_EMBERS] = {0, 50, 100, 20, 70, 120, 35, 85};

static void RTMoltres_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegMoltres_Tiles, sLegMoltres_Maps);
    LI_ResetSprites();
    for (i = 0; i < MOL_EMBERS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_SmallEmber, 32 * 160 / 2, gBattleAnimSpritePal_SmallEmber, MOL_TAG_EMBER, &sGI_Oam32, sMolEmberX[i], 200, 1);
    for (i = 0; i < MOL_FLAMES; i++)
        LI_Make(MOL_EMBERS + i, gBattleAnimSpriteGfx_Fire, 32 * 256 / 2, gBattleAnimSpritePal_Fire, MOL_TAG_FIRE, &sGI_Oam32, MOL_X, MOL_Y, 0);
    task->tGiSprite0 = LI_MonPicAffine(SPECIES_MOLTRES, MOL_X, MOL_Y);
    GI_Sprite(task->tGiSprite0)->subpriority = 2;
}

static bool8 RTMoltres_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, e, amp, dx = 0, scale, y;
    u32 keep, molBit;
    s16 *hofs = LI2_Hofs(t, MOL_SHOW);
    struct Sprite *s, *mol = GI_Sprite(task->tGiSprite0);

    molBit = LI2_MonBit(task->tGiSprite0);
    keep = molBit | GI_SpritePalBit(MOL_TAG_EMBER) | GI_SpritePalBit(MOL_TAG_FIRE);
    GI_ResetPals(keep);
    if (t >= MOL_SHOW)
    {
        LoadPalette(sLegMoltres_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
        // de lava golft (heller en donkerder per kleur, verschoven)
        for (i = 0; i < MOL_LAVA_COUNT; i++)
        {
            // zelfde kleur = zelfde fase (anders golft de lava per tile)
            k = gPlttBufferUnfaded[sMolLava[i]];
            BlendPalette(sMolLava[i], 1, 5 + Sin((t * 6 + ((k >> 5) & 31) * 24) & 0xFF, 5), RGB(31, 29, 10));
            gPlttBufferUnfaded[sMolLava[i]] = gPlttBufferFaded[sMolLava[i]];
        }
    }
    if (t == MOL_SHOW)
    {
        GI_KillFieldWindows();
        LI_InitWave(); // pas nu: de wereld is zwart (de golf zet ook vensters en blenden)
    }
    if (t == MOL_SHOW + 1) // een frame na de paletten (die gaan pas in de VBlank over)
        GI_ShowMap(0);

    // de lucht trilt van de hitte
    amp = t < MOL_RISE ? 1 : (t < MOL_CHARGE ? 2 : 3);
    if (t >= MOL_DIVE)
        dx = LI_ShakeAmp(3);
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        hofs[i] = (Sin((i * 6 + t * 5) & 0xFF, amp) + dx) & 0x1FF;
    SetGpuReg(REG_OFFSET_BG0VOFS, (t >= MOL_DIVE ? LI_ShakeAmp(2) : 0) & 0x1FF);

    // Moltres: voeten in de lava, dan omhoog (groter), gloeien, duiken
    scale = 150;
    y = MOL_Y;
    if (t >= MOL_RISE)
    {
        k = min(t - MOL_RISE, MOL_RISE_LEN);
        e = MOL_RISE_LEN * MOL_RISE_LEN - (MOL_RISE_LEN - k) * (MOL_RISE_LEN - k);
        scale = 150 + 150 * e / (MOL_RISE_LEN * MOL_RISE_LEN);
        y = MOL_Y - 20 * e / (MOL_RISE_LEN * MOL_RISE_LEN);
    }
    if (t >= MOL_DIVE)
    {
        k = min(t - MOL_DIVE, MOL_DIVE_LEN);
        scale = 300 + 212 * k * k / (MOL_DIVE_LEN * MOL_DIVE_LEN);
        y = MOL_Y - 20 + 12 * k / MOL_DIVE_LEN;
    }
    if (t >= MOL_SHOW)
    {
        mol->invisible = FALSE;
        mol->y = y + (t < MOL_RISE ? Sin((t * 8) & 0xFF, 2) : 0);
        mol->x2 = dx;
        LI_Affine(task->tGiSprite0, scale, 0);
    }
    if (t >= MOL_CHARGE && t < MOL_DIVE)
        BlendPalettes(molBit, 6 + Sin(((t - MOL_CHARGE) * 20) & 0xFF, 6), RGB(31, 31, 24));
    if (t >= MOL_DIVE)
        BlendPalettes(molBit, min(12, (t - MOL_DIVE) * 2), RGB(31, 31, 24));
    // de krater kleurt mee
    if (t >= MOL_CHARGE && t >= MOL_SHOW + 8)
        BlendPalettes(LI2_PALS_MAP, min((t - MOL_CHARGE) / 3, 9), RGB(31, 18, 4));
    LI2_FadeIn(t, MOL_SHOW, LI2_PALS_MAP | keep);

    // sintels stijgen op uit de lava
    for (i = 0; i < MOL_EMBERS; i++)
    {
        s = LI_S(i);
        k = t + sMolEmberOfs[i];
        s->invisible = t < MOL_SHOW;
        s->x = sMolEmberX[i] + Sin((k * 6) & 0xFF, 5) + dx;
        s->y = 150 - ((k * 3 / 2) & 0x7F);
        LI_Frame(i, MOL_TAG_EMBER, (k >> 2) % 5, 16);
    }

    // een ring van vlammen rond Moltres, die meegroeit
    for (i = 0; i < MOL_FLAMES; i++)
    {
        s = LI_S(MOL_EMBERS + i);
        k = t - MOL_RISE - i;
        if (k < 0)
            continue;
        e = min(40 + k * 2, t >= MOL_DIVE ? 130 : 70);
        s->invisible = FALSE;
        s->x = MOL_X + Cos((i * 43 + t * 3) & 0xFF, e) + dx;
        s->y = y + Sin((i * 43 + t * 3) & 0xFF, e * 3 / 4);
        LI_Frame(MOL_EMBERS + i, MOL_TAG_FIRE, ((t >> 2) + i * 3) & 7, 16);
    }

    // geluid
    if (t == MOL_SHOW + 2)
        PlaySE(SE_M_HEAT_WAVE);
    if (t == MOL_CRY)
        PlayCry_Normal(SPECIES_MOLTRES, 0);
    if (t == MOL_RISE + 4)
        PlaySE(SE_M_FLAME_WHEEL);
    if (t == MOL_CHARGE)
        PlaySE(SE_M_DETECT);
    if (t == MOL_DIVE)
        PlaySE(SE_M_SKY_UPPERCUT);
    if (t == MOL_DIVE + 8)
        PlaySE(SE_M_SACRED_FIRE2);

    LI2_FadeWorld(t, MOL_SHOW, LI2_PALS_MAP, keep);
    if (LI2_WhiteOut(t, MOL_END, LI2_PALS_MAP, keep))
    {
        for (i = 0; i < MOL_EMBERS + MOL_FLAMES; i++)
            LI_S(i)->invisible = TRUE;
        mol->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTMoltres_Finish(struct Task *task)
{
    LI_EndWave();
    LI_DestroySprites();
    LI_DestroyMonPic(task->tGiSprite0);
    GI_FreeTag(MOL_TAG_EMBER);
    GI_FreeTag(MOL_TAG_FIRE);
    GI_Free();
}

static const struct RouteTransition sRT_LegendMoltres =
{
    sPikachu_Tileset, 32, sLegMoltres_Pal + 5 * 16, 1, 1, 0, RTMoltres_Init, RTMoltres_Update, RTMoltres_Finish
};

static void Task_LegendMoltres(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendMoltres);
}

// =====================================================================================================================
// ---------------- grote objecten (128 x 128) uit vier 64x64-sprites die samen schalen en draaien: zwaard, schild, Y, X
#define LI2_BIG_SIZE    (128 * 128 / 2)

static void LI2_BigMake(u32 b, const u32 *gfx, const u16 *pal, u16 tag, u8 subprio)
{
    u32 q;
    for (q = 0; q < 4; q++)
    {
        LI_Make(b + q, gfx, LI2_BIG_SIZE, pal, tag, &sGI_Oam64Affine, 120, 80, subprio);
        LI_Frame(b + q, tag, q, 64);
    }
}

// midden (cx, cy), schaal (256 = 1x), draaiing (0-255, tegen de klok in), prioriteit (1 = achter BG0)
static void LI2_BigSet(u32 b, s32 cx, s32 cy, s32 scale, s32 rot, bool32 show, u8 prio)
{
    u32 q;
    s32 c = Cos(rot & 0xFF, 256), sn = Sin(rot & 0xFF, 256);
    for (q = 0; q < 4; q++)
    {
        struct Sprite *s = LI_S(b + q);
        s32 ox = (q & 1) ? 32 : -32, oy = (q & 2) ? 32 : -32;
        s32 rx = (ox * c + oy * sn) >> 8, ry = (-ox * sn + oy * c) >> 8;
        s->x = cx + rx * scale / 256;
        s->y = cy + ry * scale / 256;
        s->invisible = !show || s->y < -64 || s->y > DISPLAY_HEIGHT + 64; // anders loopt OAM-y rond
        s->oam.priority = prio;
        LI_Affine(sLI_Spr[b + q], scale, (u16)((rot & 0xFF) << 8));
    }
}

static u16 LI2_Mix(u16 a, u16 b, s32 k)
{
    s32 r = a & 31, g = (a >> 5) & 31, bl = (a >> 10) & 31;
    r += (((b & 31) - r) * k) >> 4;
    g += ((((b >> 5) & 31) - g) * k) >> 4;
    bl += ((((b >> 10) & 31) - bl) * k) >> 4;
    return RGB(r, g, bl);
}

// het spritepalet van 'tag' per index tussen a en b (k[i] 0-16), in de unfaded buffer (GI_ResetPals zet het door)
static void LI2_MixPal(u16 tag, const u16 *a, const u16 *b, const u8 *k)
{
    u8 slot = IndexOfSpritePaletteTag(tag);
    u32 i;
    u16 *u;
    if (slot == 0xFF)
        return;
    u = &gPlttBufferUnfaded[OBJ_PLTT_ID(slot)];
    for (i = 1; i < 16; i++)
        u[i] = LI2_Mix(a[i], b[i], k[i]);
}

static u16 *LI2_ObjPal(u16 tag)
{
    u8 slot = IndexOfSpritePaletteTag(tag);
    return slot == 0xFF ? NULL : &gPlttBufferUnfaded[OBJ_PLTT_ID(slot)];
}

// =====================================================================================================================
// Zacian en Zamazenta (de open plek achterin het Mega Forest, in de schaduw; bloemblaadjes dwarrelen). Geen wolf in
// beeld: midden op de open plek zweeft het Rusted Sword / Rusted Shield (het item-icoon x4 met Scale2x, vier sprites).
// De roest valt er in schilfers af en het wordt roestvrij (kleur per index gemengd: grijs/roest -> zilverblauw met een
// gouden gevest, of rood met goud zoals de Crowned-vorm), een glinster schiet erover en de wolf huilt (buiten beeld).
// - Zacian: het zwaard draait horizontaal en slicet het beeld: een witte snee (venster 0 als band, de achtergrondkleur
//   wit) volgt het zwaard, dan splijt het beeld open (golf per beeldlijn).
// - Zamazenta: de open plek wordt zwart, het schild beukt drie keer tegen het scherm: het beeld schudt en de barsten in
//   het "glas" (BG0 vóór het schild) groeien per klap, bij de derde breekt het.
static const u32 sLegWolves_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_wolves.4bpp.smol");
static const u32 sLegWolves_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_wolves_maps.bin.smol");
static const u16 sLegWolves_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_wolves.gbapal");
static const u32 sLegSword_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_sword.4bpp.smol");
static const u16 sLegSword_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_sword.gbapal");
static const u16 sLegSword_CleanPal[] = INCBIN_U16("graphics/battle_transitions/legend_sword_clean.gbapal");
static const u32 sLegShield_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_shield.4bpp.smol");
static const u16 sLegShield_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_shield.gbapal");
static const u16 sLegShield_CleanPal[] = INCBIN_U16("graphics/battle_transitions/legend_shield_clean.gbapal");
static const u32 sLegRustFlakes_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_rust_flakes.4bpp.smol");
static const u16 sLegRustFlakes_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_rust_flakes.gbapal");

#define tWolfZam        data[12]
enum { WOLF_MAP_CLEARING, WOLF_MAP_CRACK1, WOLF_MAP_CRACK2, WOLF_MAP_CRACK3 };
#define WOLF_TAG_PETAL  0x5A77
#define WOLF_TAG_ITEM   0x5A78
#define WOLF_TAG_FLAKE  0x5A79
#define WOLF_TAG_GLINT  0x5A7B
#define WOLF_SHOW       8
#define WOLF_PETALS     8
#define WOLF_FLAKES     8
#define WOLF_ITEM       WOLF_PETALS                    // vier slots
#define WOLF_FLAKE0     (WOLF_ITEM + 4)
#define WOLF_GLINT      (WOLF_FLAKE0 + WOLF_FLAKES)
#define WOLF_X          120
#define WOLF_Y          76
#define WOLF_SHADE      RGB(2, 4, 7)
#define WOLF_RUST       20    // de roest valt eraf (±24 frames)
#define WOLF_GLEAM      46
#define WOLF_CRY        52
// Zacian
#define ZAC_SWING       56    // het zwaard draait horizontaal
#define ZAC_SWING_LEN   6
#define ZAC_CUT         64    // en slicet van rechts naar links
#define ZAC_CUT_LEN     6
#define ZAC_SPLIT       72
#define ZAC_SPLIT_LEN   16
#define ZAC_END         (ZAC_SPLIT + ZAC_SPLIT_LEN + 12)
// Zamazenta
#define ZAM_FOCUS       56    // de open plek wordt zwart
#define ZAM_DARK        64
#define ZAM_HIT_LEN     6     // aanloop per klap
#define ZAM_END         108

static const u8 sWolfPetalX[WOLF_PETALS] = {10, 50, 90, 130, 170, 210, 30, 190};
static const u8 sWolfPetalOfs[WOLF_PETALS] = {0, 60, 120, 30, 90, 150, 200, 75};
static const s8 sWolfFlake[WOLF_FLAKES][2] = {{-30, 22}, {18, -10}, {-6, 30}, {28, -28}, {-22, 4}, {8, 14}, {34, -4}, {-12, -20}};
// per kleurindex: wanneer hij roestvrij wordt (de roest eerst, dan het metaal)
static const u8 sWolfStagger[16] = {0, 10, 12, 14, 16, 6, 0, 2, 4, 6, 8, 10, 12, 14, 2, 4};
static const u8 sZamHit[3] = {70, 84, 98};

static void RTWolves_Init(struct Task *task)
{
    u32 i, zam = task->tWolfZam;

    GI_LoadGfx(sLegWolves_Tiles, sLegWolves_Maps);
    LI_ResetSprites();
    for (i = 0; i < WOLF_PETALS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_Petal, 16 * 112 / 2, gBattleAnimSpritePal_Petal, WOLF_TAG_PETAL, &sGI_Oam16, sWolfPetalX[i], -20, 0);
    LI2_BigMake(WOLF_ITEM, zam ? sLegShield_Gfx : sLegSword_Gfx, zam ? sLegShield_Pal : sLegSword_Pal, WOLF_TAG_ITEM, 2);
    for (i = 0; i < WOLF_FLAKES; i++)
        LI_Make(WOLF_FLAKE0 + i, sLegRustFlakes_Gfx, 16 * 64 / 2, sLegRustFlakes_Pal, WOLF_TAG_FLAKE, &sGI_Oam16, 0, 0, 1);
    LI_Make(WOLF_GLINT, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, gBattleAnimSpritePal_Sparkle3, WOLF_TAG_GLINT, &sGI_Oam32, 0, 0, 0);
    task->tGiSprite1 = zam ? SPECIES_ZAMAZENTA_HERO : SPECIES_ZACIAN_HERO;
}

static bool8 RTWolves_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, dx = 0, dy = 0, end, gap = -1, cutY = WOLF_Y, cutX = 0, split = 0;
    s32 ix = WOLF_X, iy = WOLF_Y, scale = 256, rot = 0, prio = 0;
    bool32 show = t >= WOLF_SHOW, done;
    u32 keep, zam = task->tWolfZam;
    u8 kk[16];
    s16 *hofs = LI2_Hofs(t, WOLF_SHOW);
    struct Sprite *s;

    end = zam ? ZAM_END : ZAC_END;
    keep = GI_SpritePalBit(WOLF_TAG_PETAL) | GI_SpritePalBit(WOLF_TAG_ITEM) | GI_SpritePalBit(WOLF_TAG_FLAKE) | GI_SpritePalBit(WOLF_TAG_GLINT);

    // roest -> roestvrij, per kleurindex
    for (i = 0; i < 16; i++)
        kk[i] = min(max((t - WOLF_RUST - sWolfStagger[i]) * 2, 0), 16);
    LI2_MixPal(WOLF_TAG_ITEM, zam ? sLegShield_Pal : sLegSword_Pal, zam ? sLegShield_CleanPal : sLegSword_CleanPal, kk);
    GI_ResetPals(keep);
    if (t >= WOLF_SHOW)
    {
        LoadPalette(sLegWolves_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
        if (!zam || t < ZAM_DARK)
            BlendPalettes(LI2_PALS_MAP & ~(1 << 15), 5, WOLF_SHADE); // de schaduw van het bos
    }
    if (t == WOLF_SHOW)
    {
        GI_KillFieldWindows();
        LI_InitWave();
        // venster 0: binnen niets (de achtergrondkleur, wit, is de snee; ook geen sprites, anders zie je de speler
        // van de kaart als zwart silhouet), buiten alles
        sTransitionData->WININ = 0;
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ;
        sTransitionData->WIN0V = 0;
    }
    if (t == WOLF_SHOW + 1) // een frame na de paletten (die gaan pas in de VBlank over)
        GI_ShowMap(WOLF_MAP_CLEARING);

    // het voorwerp zweeft
    iy = WOLF_Y + Sin((t * 4) & 0xFF, 2);
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        hofs[i] = 0;

    if (!zam)
    {
        // Zacian: draaien tot de kling naar links wijst, dan van rechts naar links door het beeld
        if (t >= ZAC_SWING)
        {
            k = min(t - ZAC_SWING, ZAC_SWING_LEN);
            rot = -(k * 32 / ZAC_SWING_LEN);
        }
        if (t >= ZAC_CUT)
        {
            k = min(t - ZAC_CUT, ZAC_CUT_LEN);
            ix = WOLF_X - k * k * 240 / (ZAC_CUT_LEN * ZAC_CUT_LEN);
            iy = WOLF_Y;
            show = ix > -70;
            gap = 2;
            cutX = max(ix - 40, 0);
            if (t == ZAC_CUT)
                PlaySE(SE_M_CUT);
        }
        if (t >= ZAC_SPLIT)
        {
            k = min(t - ZAC_SPLIT, ZAC_SPLIT_LEN);
            split = k * k * 90 / (ZAC_SPLIT_LEN * ZAC_SPLIT_LEN);
            gap = 2 + k * k * 40 / (ZAC_SPLIT_LEN * ZAC_SPLIT_LEN);
            cutX = 0;
            for (i = 0; i < DISPLAY_HEIGHT; i++)
                hofs[i] = i < cutY ? split : -split;
        }
        if (t == ZAC_SWING)
            PlaySE(SE_M_SWORDS_DANCE);
        if (t == ZAC_SPLIT)
            PlaySE(SE_M_RAZOR_WIND);
    }
    else
    {
        // Zamazenta: zwart, dan drie klappen tegen het scherm
        if (t >= ZAM_FOCUS && t < ZAM_DARK)
            BlendPalettes(LI2_PALS_MAP, (t - ZAM_FOCUS) * 2 + 2, RGB_BLACK);
        if (t == ZAM_DARK)
            CpuFill16(0, RT_Tilemap(), BG_SCREEN_SIZE);
        if (t >= ZAM_DARK)
        {
            prio = 1; // achter het "glas"
            scale = 288;
            // de kaart (BG1-3) ligt nu bloot: zijn paletten 10-14 zwart houden, alleen de barsten (15) blijven
            BlendPalettes(LI2_PALS_MAP & ~(1 << 15), 16, RGB_BLACK);
        }
        for (i = 0; i < 3; i++)
        {
            k = t - sZamHit[i];
            if (k >= -ZAM_HIT_LEN && k < 0)
                scale = 288 + (k + ZAM_HIT_LEN) * 132 / ZAM_HIT_LEN;          // aanloop naar het scherm
            else if (k >= 0 && k < 8)
            {
                scale = 420 - k * 16;                                         // terugveren
                dx = LI_ShakeAmp(4 - k / 2);
                dy = LI_ShakeAmp(3 - k / 3);
            }
            if (k == 0)
            {
                GI_ShowMap(WOLF_MAP_CRACK1 + i);
                PlaySE(i == 2 ? SE_ICE_BREAK : SE_M_MEGA_KICK2);
            }
            if (i == 2 && k >= 0)
                scale = 420;
            if (k >= 0 && k < 5)
                BlendPalettes((1 << 15) | keep, (i == 2 ? 14 : 8) * (5 - k) / 5, RGB_WHITE); // flits (niet op 13/14: kaart)
        }
        if (t == ZAM_FOCUS)
            PlaySE(SE_M_HARDEN);
    }

    // het voorwerp (vier sprites)
    LI2_BigSet(WOLF_ITEM, ix + dx, iy + dy, scale, rot, show, prio);
    // de roest valt eraf
    for (i = 0; i < WOLF_FLAKES; i++)
    {
        s = LI_S(WOLF_FLAKE0 + i);
        k = t - WOLF_RUST - 1 - i * 3;
        s->invisible = k < 0 || k >= 28;
        if (s->invisible)
            continue;
        s->x = WOLF_X + sWolfFlake[i][0] + ((i & 1) ? k / 3 : -k / 3);
        s->y = WOLF_Y + sWolfFlake[i][1] + (k * k) / 12;
        LI_Frame(WOLF_FLAKE0 + i, WOLF_TAG_FLAKE, (i + (k >> 2)) & 3, 4);
    }
    // een glinster schiet over het voorwerp
    s = LI_S(WOLF_GLINT);
    k = t - WOLF_GLEAM;
    s->invisible = k < 0 || k >= 10;
    if (!s->invisible)
    {
        s->x = WOLF_X + 30 - k * 6;
        s->y = WOLF_Y - 30 + k * 6;
        LI_Frame(WOLF_GLINT, WOLF_TAG_GLINT, min(k >> 1, 4), 16);
    }
    if (t == WOLF_RUST)
        PlaySE(SE_M_DETECT);
    if (t == WOLF_GLEAM)
        PlaySE(SE_SHINY);
    if (t == WOLF_CRY)
        PlayCry_Normal(task->tGiSprite1, 0);

    // BG: snee, splijten en trillen
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        hofs[i] = (hofs[i] + dx) & 0x1FF;
    SetGpuReg(REG_OFFSET_BG0VOFS, dy & 0x1FF);
    if (gap >= 0 && t > WOLF_SHOW)
    {
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
        SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(cutX, 240));
        sTransitionData->WIN0V = WIN_RANGE(max(cutY - gap, 0), min(cutY + gap, DISPLAY_HEIGHT));
    }
    else if (t > WOLF_SHOW)
    {
        sTransitionData->WIN0V = 0;
    }

    // bloemblaadjes (niet meer als het donker is)
    for (i = 0; i < WOLF_PETALS; i++)
    {
        s = LI_S(i);
        k = t + sWolfPetalOfs[i];
        s->invisible = t < WOLF_SHOW || (zam && t >= ZAM_DARK);
        s->x = sWolfPetalX[i] + Sin((k * 4) & 0xFF, 12) - (k & 0x3F);
        s->y = ((k & 0xFF) * 3 >> 2) - 20;
        LI_Frame(i, WOLF_TAG_PETAL, (k >> 3) % 7, 4);
    }

    LI2_FadeIn(t, WOLF_SHOW, LI2_PALS_MAP | keep);
    LI2_FadeWorld(t, WOLF_SHOW, LI2_PALS_MAP, keep);
    done = LI2_WhiteOut(t, end, LI2_PALS_MAP, keep);
    if (gap >= 0)
        gPlttBufferFaded[0] = RGB_WHITE; // de snee
    if (done)
    {
        for (i = 0; i <= WOLF_GLINT; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTWolves_Finish(struct Task *task)
{
    sTransitionData->WIN0V = 0;
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
    LI_EndWave();
    LI_DestroySprites();
    GI_FreeTag(WOLF_TAG_PETAL);
    GI_FreeTag(WOLF_TAG_ITEM);
    GI_FreeTag(WOLF_TAG_FLAKE);
    GI_FreeTag(WOLF_TAG_GLINT);
    GI_Free();
}

static const struct RouteTransition sRT_LegendWolves =
{
    sPikachu_Tileset, 32, sLegWolves_Pal + 5 * 16, 1, 1, 0, RTWolves_Init, RTWolves_Update, RTWolves_Finish
};

// per wolf een eigen taakfunctie (Transition_WaitForMain zoekt op de taakfunctie)
static void Task_LegendZacian(u8 taskId)
{
    if (gTasks[taskId].tState == 0)
        gTasks[taskId].tWolfZam = FALSE;
    RouteTransition_Run(taskId, &sRT_LegendWolves);
}

static void Task_LegendZamazenta(u8 taskId)
{
    if (gTasks[taskId].tState == 0)
        gTasks[taskId].tWolfZam = TRUE;
    RouteTransition_Run(taskId, &sRT_LegendWolves);
}

// =====================================================================================================================
// Xerneas en Yveltal (Glimwood Tangle: leven en dood). De echte heksenkring, in kleur (palet 10-15) of uitgedoofd zoals
// toen de Impidimp-bende het licht doofde (dezelfde tiles met palet 4-9). Per vak kiest C de toestand op afstand van de
// kring, zodat het licht als een ring uitdijt (Xerneas) of van buiten naar binnen wegtrekt (Yveltal). Geen Pokémon in
// beeld, maar hun letter (vier sprites, 128 x 128):
// - Xerneas: Ballonlea, grauw. Een grote X van gewei hangt grauw in de kring en flikkert ("a lamp on its last bulb");
//   de lichtjes gaan een voor een aan (geel, paars, rood, blauw), het gewei kleurt blauw, de kleur stroomt vanuit de
//   kring over het bos (leven geven), de lichtjes gaan rond als in de Active Mode, glinsters stijgen op, Geomancy:
//   regenboog, wit.
// - Yveltal: de Tangle in volle gloed. Een zwarte Y (gespreide vleugels en staart) daalt in de kring en zijn rode
//   strepen gloeien op; de kleur trekt van buiten naar binnen weg en rode veren worden naar de Y toe gezogen (het leven
//   gaat naar Yveltal), Oblivion Wing kleurt alles rood en het beeld gaat op zwart.
static const u32 sLegXerneas_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_xerneas.4bpp.smol");
static const u32 sLegXerneas_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_xerneas_maps.bin.smol");
static const u16 sLegXerneas_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_xerneas.gbapal");
static const u16 sLegXerneas_DimPal[] = INCBIN_U16("graphics/battle_transitions/legend_xerneas_dying.gbapal");
static const u32 sLegYveltal_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_yveltal.4bpp.smol");
static const u32 sLegYveltal_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_yveltal_maps.bin.smol");
static const u16 sLegYveltal_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_yveltal.gbapal");
static const u16 sLegYveltal_DimPal[] = INCBIN_U16("graphics/battle_transitions/legend_yveltal_dying.gbapal");
static const u32 sLegXSym_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_xsym.4bpp.smol");
static const u16 sLegXSym_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_xsym.gbapal");
static const u16 sLegXSym_DimPal[] = INCBIN_U16("graphics/battle_transitions/legend_xsym_dim.gbapal");
static const u32 sLegYSym_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_ysym.4bpp.smol");
static const u16 sLegYSym_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_ysym.gbapal");
static const u16 sLegYSym_DarkPal[] = INCBIN_U16("graphics/battle_transitions/legend_ysym_dark.gbapal");

#define GLIM_TAG_FX     0x5A7A
#define GLIM_TAG_SYM    0x5A7C
#define GLIM_SHOW       8
#define GLIM_FX         8
#define GLIM_SYM        GLIM_FX        // vier slots
#define GLIM_CX         120
#define GLIM_CY         84
#define GLIM_SYM_Y      72
// Xerneas
#define XER_CRY         26
#define XER_LIGHT       28    // de vier lichtjes, om de 4 frames
#define XER_SPREAD      46
#define XER_SPREAD_LEN  32
#define XER_GEO         (XER_SPREAD + XER_SPREAD_LEN)
#define XER_END         (XER_GEO + 20)
#define XER_ORB         7     // indexen 7-10: de lichtjes
// Yveltal
#define YVE_SWEEP       12
#define YVE_SWEEP_LEN   24
#define YVE_CRY         (YVE_SWEEP + YVE_SWEEP_LEN)
#define YVE_DRAIN       (YVE_CRY + 2)
#define YVE_DRAIN_LEN   34
#define YVE_OBLIVION    (YVE_DRAIN + YVE_DRAIN_LEN + 2)
#define YVE_END         (YVE_OBLIVION + 24)

static const u8 sGlimFxX[GLIM_FX] = {40, 200, 80, 160, 20, 220, 60, 180};
static const u8 sGlimFxOfs[GLIM_FX] = {0, 16, 32, 48, 64, 80, 96, 112};
// rode veren (de White Feather uit de gevechtsanimaties met een eigen palet), en waar ze vandaan komen
static const u16 sYveRed[16] = {0, RGB(28, 4, 6), RGB(24, 3, 5), RGB(20, 2, 4), RGB(16, 2, 3), RGB(12, 1, 2),
                                RGB(8, 1, 2), RGB(5, 1, 2)};
static const s16 sYveFeatherFrom[GLIM_FX][2] = {{-10, 20}, {250, 30}, {-10, 120}, {250, 130}, {60, -16}, {180, -16},
                                                {40, 176}, {200, 176}};

// elk vak in kleur als het (met wat ruis) binnen straal r van de kring ligt, anders uitgedoofd
static void LI2_GlimTiles(s32 r)
{
    u16 *tilemap = RT_Tilemap();
    s32 row, col, dx, dy, rr;
    u16 v;

    if (sGymIntro_Maps == NULL)
        return;
    for (row = 0; row < 20; row++)
    {
        for (col = 0; col < 30; col++)
        {
            v = sGymIntro_Maps[row * 30 + col];
            dx = col * 8 + 4 - GLIM_CX;
            dy = row * 8 + 4 - GLIM_CY;
            rr = r + ((col * 5 + row * 11) & 15) - 8;
            if (v != 0 && (rr <= 0 || dx * dx + dy * dy >= rr * rr))
                v -= 6 << 12;
            tilemap[row * 32 + col] = v;
        }
    }
}

static bool32 IsYveltalIntro(struct Task *task)
{
    return task->tWolfZam;
}

static void RTGlim_Init(struct Task *task)
{
    u32 i, yve = IsYveltalIntro(task);
    u16 species = yve ? SPECIES_YVELTAL : GetMonData(&gEnemyParty[0], MON_DATA_SPECIES);

    if (!yve && species != SPECIES_XERNEAS && species != SPECIES_XERNEAS_ACTIVE)
        species = SPECIES_XERNEAS;
    GI_LoadGfx(yve ? sLegYveltal_Tiles : sLegXerneas_Tiles, yve ? sLegYveltal_Maps : sLegXerneas_Maps);
    LI_ResetSprites();
    for (i = 0; i < GLIM_FX; i++)
    {
        if (yve)
            LI_Make(i, gBattleAnimSpriteGfx_WhiteFeather, 32 * 64 / 2, sYveRed, GLIM_TAG_FX, &sGI_Oam32, sYveFeatherFrom[i][0], sYveFeatherFrom[i][1], 1);
        else
            LI_Make(i, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, gBattleAnimSpritePal_Sparkle3, GLIM_TAG_FX, &sGI_Oam32, sGlimFxX[i], 200, 0);
    }
    LI2_BigMake(GLIM_SYM, yve ? sLegYSym_Gfx : sLegXSym_Gfx, yve ? sLegYSym_DarkPal : sLegXSym_DimPal, GLIM_TAG_SYM, 2);
    task->tGiSprite1 = species;
}

static bool8 RTGlim_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, e, r, scale = 256, sy = GLIM_SYM_Y;
    u32 yve = IsYveltalIntro(task), keep, symBit, bg = LI2_PALS_MAP | LI2_PALS_DIM;
    u8 kk[16];
    u16 *sp;
    struct Sprite *s;

    symBit = GI_SpritePalBit(GLIM_TAG_SYM);
    keep = symBit | GI_SpritePalBit(GLIM_TAG_FX);
    if (t >= GLIM_SHOW)
    {
        LoadPalette(yve ? sLegYveltal_Pal : sLegXerneas_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
        LoadPalette(yve ? sLegYveltal_DimPal : sLegXerneas_DimPal, BG_PLTT_ID(4), 6 * PLTT_SIZE_4BPP);
    }
    if (t == GLIM_SHOW)
        GI_KillFieldWindows();

    if (!yve)
    {
        // de X: grauw en flikkerend, dan de lichtjes een voor een, dan het gewei
        for (i = 0; i < 16; i++)
            kk[i] = (t >= XER_SPREAD) ? min((t - XER_SPREAD) * 2, 16) : ((Random() & 3) ? 0 : 5);
        for (i = 0; i < 4; i++)
            if (t >= XER_LIGHT + i * 4)
                kk[XER_ORB + i] = 16;
        LI2_MixPal(GLIM_TAG_SYM, sLegXSym_DimPal, sLegXSym_Pal, kk);
        sp = LI2_ObjPal(GLIM_TAG_SYM);
        if (sp != NULL)
        {
            for (i = 0; i < 4; i++)
            {
                k = t - XER_LIGHT - i * 4;
                if (k >= 0 && k < 2)
                    sp[XER_ORB + i] = RGB_WHITE;                                    // gaat aan
                else if (t >= XER_SPREAD + 8)
                    sp[XER_ORB + i] = sLegXSym_Pal[XER_ORB + ((i + t / 5) & 3)];   // Active Mode: de kleuren gaan rond
            }
        }
        GI_ResetPals(keep);
        // de kleur stroomt vanuit de kring naar buiten
        r = t < XER_SPREAD ? 0 : (t - XER_SPREAD) * 8;
        if (t > GLIM_SHOW && t <= XER_SPREAD + XER_SPREAD_LEN)
            LI2_GlimTiles(r);
        if (t >= XER_GEO)
        {
            k = min(t - XER_GEO, 16);
            scale = 256 + k * 3 + Sin((t * 12) & 0xFF, 6);
            BlendPalettes(LI2_PALS_MAP | GI_SpritePalBit(GLIM_TAG_FX), 3, sHoRainbow[(t / 3) % 7]);
        }
        LI2_BigSet(GLIM_SYM, GLIM_CX, sy + Sin((t * 3) & 0xFF, 2), scale, 0, t >= GLIM_SHOW, 0);
        // glinsters stijgen op
        for (i = 0; i < GLIM_FX; i++)
        {
            s = LI_S(i);
            k = t - XER_SPREAD + sGlimFxOfs[i] / 3;
            s->invisible = t < XER_SPREAD;
            if (s->invisible)
                continue;
            s->x = sGlimFxX[i] + Sin((k * 5) & 0xFF, 6);
            s->y = 150 - ((k * 2) & 0x7F);
            LI_Frame(i, GLIM_TAG_FX, (k >> 2) % 5, 16);
        }
        if (t >= XER_SPREAD)
            BlendPalettes(GI_SpritePalBit(GLIM_TAG_FX), 5, sHoRainbow[(t / 4 + 3) % 7]); // regenboogglinsters
        if (t == XER_CRY)
            PlayCry_Normal(task->tGiSprite1, 0);
        for (i = 0; i < 4; i++)
            if (t == XER_LIGHT + i * 4)
                PlaySE(SE_M_DETECT);
        if (t == XER_SPREAD)
            PlaySE(SE_M_MOONLIGHT);
        if (t == XER_GEO)
            PlaySE(SE_M_MORNING_SUN);
    }
    else
    {
        // de Y: daalt als zwart silhouet in de kring, dan gloeien de rode strepen op
        for (i = 0; i < 16; i++)
            kk[i] = t < YVE_CRY + 2 ? 0 : min((t - YVE_CRY - 2) * 2, 16);
        LI2_MixPal(GLIM_TAG_SYM, sLegYSym_DarkPal, sLegYSym_Pal, kk);
        GI_ResetPals(keep);
        if (t >= YVE_SWEEP)
        {
            k = min(t - YVE_SWEEP, YVE_SWEEP_LEN);
            e = YVE_SWEEP_LEN * YVE_SWEEP_LEN - (YVE_SWEEP_LEN - k) * (YVE_SWEEP_LEN - k);
            sy = -30 + (GLIM_SYM_Y + 30) * e / (YVE_SWEEP_LEN * YVE_SWEEP_LEN);
            scale = 400 - 144 * e / (YVE_SWEEP_LEN * YVE_SWEEP_LEN);
            if (t < YVE_CRY)
                BlendPalettes(symBit, 16, RGB_BLACK);
            else if (t >= YVE_OBLIVION)
                BlendPalettes(symBit, 6 + Sin(((t - YVE_OBLIVION) * 24) & 0xFF, 5), RGB(31, 2, 4));
        }
        LI2_BigSet(GLIM_SYM, GLIM_CX, sy, scale, 0, t >= YVE_SWEEP, 0);
        // de kleur trekt van buiten naar binnen weg
        r = t < YVE_DRAIN ? 400 : 260 - (t - YVE_DRAIN) * 8;
        if (t > GLIM_SHOW && t <= YVE_DRAIN + YVE_DRAIN_LEN)
            LI2_GlimTiles(r);
        if (t >= YVE_OBLIVION)
            BlendPalettes(bg, min((t - YVE_OBLIVION) * 2 / 3, 12), RGB(16, 0, 2));
        // rode veren worden naar de Y toe gezogen
        for (i = 0; i < GLIM_FX; i++)
        {
            s = LI_S(i);
            k = t - YVE_DRAIN - i * 3;
            s->invisible = k < 0 || k >= 20;
            if (s->invisible)
                continue;
            e = k * k;
            s->x = sYveFeatherFrom[i][0] + (GLIM_CX - sYveFeatherFrom[i][0]) * e / 400;
            s->y = sYveFeatherFrom[i][1] + (GLIM_SYM_Y - sYveFeatherFrom[i][1]) * e / 400;
            LI_Frame(i, GLIM_TAG_FX, (k >> 2) & 1, 16);
        }
        if (t == YVE_SWEEP)
            PlaySE(SE_M_FLY);
        if (t == YVE_CRY)
            PlayCry_Normal(SPECIES_YVELTAL, 0);
        if (t == YVE_DRAIN)
            PlaySE(SE_M_GIGA_DRAIN);
        if (t == YVE_OBLIVION)
            PlaySE(SE_M_HYPER_BEAM);
    }

    LI2_FadeIn(t, GLIM_SHOW, bg | keep);
    LI2_FadeWorld(t, GLIM_SHOW, bg, keep);
    if (!yve)
    {
        if (LI2_WhiteOut(t, XER_END, bg, keep))
        {
            for (i = 0; i < GLIM_FX + 4; i++)
                LI_S(i)->invisible = TRUE;
            return TRUE;
        }
    }
    else
    {
        // Yveltal eindigt in het zwart
        if (t >= YVE_END - 10)
        {
            k = min((t - (YVE_END - 10)) * 2 + 2, 16);
            BlendPalettes(bg | keep, k, RGB_BLACK);
        }
        if (t >= YVE_END)
        {
            for (i = 0; i < GLIM_FX + 4; i++)
                LI_S(i)->invisible = TRUE;
            return TRUE;
        }
    }
    return FALSE;
}

static void RTGlim_Finish(struct Task *task)
{
    LI_DestroySprites();
    GI_FreeTag(GLIM_TAG_FX);
    GI_FreeTag(GLIM_TAG_SYM);
    GI_Free();
}

static const struct RouteTransition sRT_LegendXerneas =
{
    sPikachu_Tileset, 32, sLegXerneas_Pal + 5 * 16, 1, 1, 0, RTGlim_Init, RTGlim_Update, RTGlim_Finish
};

static const struct RouteTransition sRT_LegendYveltal =
{
    sPikachu_Tileset, 32, sLegYveltal_Pal + 5 * 16, 1, 1, 0, RTGlim_Init, RTGlim_Update, RTGlim_Finish
};

static void Task_LegendXerneas(u8 taskId)
{
    if (gTasks[taskId].tState == 0)
        gTasks[taskId].tWolfZam = FALSE;
    RouteTransition_Run(taskId, &sRT_LegendXerneas);
}

static void Task_LegendYveltal(u8 taskId)
{
    if (gTasks[taskId].tState == 0)
        gTasks[taskId].tWolfZam = TRUE;
    RouteTransition_Run(taskId, &sRT_LegendYveltal);
}
#undef tWolfZam
