// Project Grounded: lichte gevechtsintro's van vijf legendaries (Lugia, Ho-Oh, Volcanion, Hoopa, Forces of Nature).
// Wordt onderaan src/battle_transition.c ingevoegd, na de gymleider-intro's (src/data/gym_intros_a.h en _b.h): gebruikt
// dezelfde GI_-hulpjes, de route-transitie-runner en Tapu_Blend. Art: tools/grounded/legend_intros.py (BG0-beelden in de
// paletten 13-15); de rest zijn echte frontsprites en gevechtsanimatie-art die al in de ROM staan.

#include "item_icon.h"
#include "pokemon.h"
#include "constants/items.h"

#define LI_SPRITES 32
static EWRAM_DATA u8 sLI_Spr[LI_SPRITES] = {0};
static EWRAM_DATA s16 sLI_Phys[LI_SPRITES][4] = {0}; // x, y, vx, vy in 1/16 px

static void LI_ResetSprites(void)
{
    u32 i;
    for (i = 0; i < LI_SPRITES; i++)
        sLI_Spr[i] = MAX_SPRITES;
}

static struct Sprite *LI_S(u32 i)
{
    return GI_Sprite(sLI_Spr[i]);
}

// een onzichtbare sprite uit gevechtsanimatie-art (of eigen art) in slot i
static void LI_Make(u32 i, const u32 *gfx, u32 size, const u16 *pal, u16 tag, const struct OamData *oam, s16 x, s16 y, u8 subprio)
{
    u8 id = GI_CreateSprite(gfx, size, pal, tag, oam, x, y, subprio);
    sLI_Spr[i] = id;
    if (id < MAX_SPRITES)
        gSprites[id].invisible = TRUE;
}

static void LI_Frame(u32 i, u16 tag, u32 frame, u32 tilesPerFrame)
{
    if (sLI_Spr[i] < MAX_SPRITES)
        gSprites[sLI_Spr[i]].oam.tileNum = GetSpriteTileStartByTag(tag) + frame * tilesPerFrame;
}

static void LI_DestroySprites(void)
{
    u32 i;
    for (i = 0; i < LI_SPRITES; i++)
    {
        if (sLI_Spr[i] < MAX_SPRITES)
            GI_DestroySprite(sLI_Spr[i]);
        sLI_Spr[i] = MAX_SPRITES;
    }
}

// een frontsprite die kan schalen en draaien (affine, dubbele grootte)
static u8 LI_MonPicAffine(u16 species, s16 x, s16 y)
{
    u8 id = GI_MonPic(species, x, y);
    struct Sprite *s;
    if (id >= MAX_SPRITES)
        return id;
    s = &gSprites[id];
    s->oam.matrixNum = AllocOamMatrix();
    if (s->oam.matrixNum == 0xFF)
    {
        s->oam.matrixNum = 0;
        return id;
    }
    s->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    s->affineAnimPaused = TRUE;
    CalcCenterToCornerVec(s, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
    SetOamMatrixRotationScaling(s->oam.matrixNum, 256, 256, 0);
    return id;
}

static void LI_Affine(u8 id, s32 scale, u16 rot)
{
    if (id < MAX_SPRITES && gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, scale, scale, rot);
}

static void LI_DestroyMonPic(u8 id)
{
    if (id >= MAX_SPRITES)
        return;
    if (gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        FreeOamMatrix(gSprites[id].oam.matrixNum);
        gSprites[id].oam.affineMode = ST_OAM_AFFINE_OFF;
        gSprites[id].oam.matrixNum = 0;
    }
    FreeAndDestroyMonPicSprite(id);
}

// HBlank-DMA op BG0HOFS (golven, scheeftrekken); de buffer is gScanlineEffectRegBuffers[0]
static void LI_InitWave(void)
{
    InitTransitionData();
    ScanlineEffect_Clear();
    CpuFill16(0, gScanlineEffectRegBuffers[0], DISPLAY_HEIGHT * 2);
    CpuFill16(0, gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    sTransitionData->VBlank_DMA = TRUE;
    SetVBlankCallback(VBlankCB_PatternWeave);
}

static void LI_EndWave(void)
{
    SetVBlankCallback(VBlankCB_BattleTransition);
    DmaStop(0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
}

// trillen van BG0 met een vaste (willekeurige) verschuiving; geeft de verschuiving terug voor de sprites
static s32 LI_ShakeAmp(s32 amp)
{
    return amp > 0 ? (s32)(Random() % (amp * 2 + 1)) - amp : 0;
}

// =====================================================================================================================
// Lugia: we zinken. Het licht van boven dooft, bubbels stijgen, een zilveren veer dwarrelt rustig omlaag (de
// beschermer). Dan, in het donker, gaat een enorm oog open (een ooglid over Lugia's eigen kop uit de frontsprite), de
// oogvlek licht op, en er vormt zich een draaikolk (Aeroblast); het beeld kantelt de storm in: scheef, bliksem, wit.
static const u32 sLegLugia_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_lugia.4bpp.smol");
static const u32 sLegLugia_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_lugia_maps.bin.smol");
static const u16 sLegLugia_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_lugia.gbapal");

enum { LUG_MAP_SEA, LUG_MAP_HEAD, LUG_MAP_VORTEX };
#define LUG_TAG_FEATHER 0x5A60
#define LUG_TAG_BUBBLE  0x5A61
#define LUG_SEA         6
#define LUG_DARK        96    // het licht is helemaal weg
#define LUG_EYE         108   // het ooglid gaat open
#define LUG_EYE_LEN     20
#define LUG_GLOW        (LUG_EYE + 26)
#define LUG_VORTEX      152
#define LUG_STORM       178
#define LUG_END         214
#define LUG_BUBBLES     6
#define LUG_EYE_IDX     6     // BG 14: de donkerblauwe oogvlek
#define LUG_DEEP        RGB(0, 1, 4)

static const u16 sLugSilver[16] = {0, RGB(31, 31, 31), RGB(27, 28, 30), RGB(24, 25, 28), RGB(21, 22, 26), RGB(18, 19, 23),
                                   RGB(15, 16, 21), RGB(12, 13, 18)};
static const u8 sLugBubbleX[LUG_BUBBLES] = {28, 70, 106, 150, 184, 218};
static const u8 sLugBubbleSpeed[LUG_BUBBLES] = {20, 30, 16, 26, 18, 32}; // 1/16 px per frame
static const u8 sLugBubbleOfs[LUG_BUBBLES] = {0, 90, 40, 140, 60, 170};

static void RTLugia_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegLugia_Tiles, sLegLugia_Maps);
    LoadPalette(sLegLugia_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    LI_Make(0, gBattleAnimSpriteGfx_WhiteFeather, 32 * 64 / 2, sLugSilver, LUG_TAG_FEATHER, &sGI_Oam32, 120, -20, 0);
    for (i = 0; i < LUG_BUBBLES; i++)
        LI_Make(1 + i, gBattleAnimSpriteGfx_Bubble, 16 * 48 / 2, gBattleAnimSpritePal_RainDrops, LUG_TAG_BUBBLE, &sGI_Oam16, sLugBubbleX[i], 200, 1);
    task->tGiShown = 0xFF;
}

static bool8 RTLugia_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, depth, map, y, h;
    u32 keep = GI_SpritePalBit(LUG_TAG_FEATHER) | GI_SpritePalBit(LUG_TAG_BUBBLE);
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    u16 *win = gScanlineEffectRegBuffers[0];
    s16 *hofs = (s16 *)gScanlineEffectRegBuffers[0];
    struct Sprite *s;

    GI_ResetPals(keep);
    LoadPalette(sLegLugia_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    // zinken: de diepe banden worden eerst donker, de lichtbundels doven uit
    depth = max(0, min((t - LUG_SEA) * 16 / (LUG_DARK - LUG_SEA), 16));
    for (i = 1; i <= 6; i++)
        pal[i] = Tapu_Blend(pal[i], LUG_DEEP, max(0, min(depth + (i - 1) * 2 - 3, 16)));
    k = Sin((t * 6) & 0xFF, 2) + 2;
    pal[7] = Tapu_Blend(pal[7], pal[2], min(depth * 2 + k, 16));
    pal[8] = Tapu_Blend(pal[8], pal[3], min(depth * 2 + k, 16));
    // de kop komt uit het donker; de oogvlek gloeit
    if (t >= LUG_GLOW)
    {
        k = min((t - LUG_GLOW) * 2, 12) + (Sin(((t - LUG_GLOW) * 12) & 0xFF, 4));
        pal[16 + LUG_EYE_IDX] = Tapu_Blend(pal[16 + LUG_EYE_IDX], RGB(14, 30, 31), max(0, min(k, 16)));
    }
    // de draaikolk: fasen 1-8 draaien steeds sneller
    if (t >= LUG_VORTEX)
    {
        k = t - LUG_VORTEX;
        k = (k * (4 + k / 6)) >> 3;
        for (i = 0; i < 8; i++)
            pal[32 + 1 + i] = sLegLugia_Pal[32 + 1 + ((i + k) & 7)];
    }
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);
    if (t >= LUG_EYE && t < LUG_VORTEX)
        BlendPalettes(1 << 14, max(0, 12 - (t - LUG_EYE) / 2), RGB_BLACK);

    // welk beeld
    if (t < LUG_SEA)
        map = -1;
    else if (t < LUG_EYE)
        map = LUG_MAP_SEA;
    else if (t < LUG_VORTEX)
        map = LUG_MAP_HEAD;
    else
        map = LUG_MAP_VORTEX;
    if (map >= 0 && map != task->tGiShown)
    {
        if (task->tGiShown == 0xFF)
            GI_KillFieldWindows();
        if (map == LUG_MAP_HEAD)
        {
            // binnen het ooglid: BG0 op de (diepblauwe) achtergrondkleur met 'lichter maken': de oogspleet gloeit.
            // Daarbuiten de (zwart gemaakte) kaartlagen.
            GI_InitWindow();
            sTransitionData->WININ = WININ_WIN0_BG0 | WININ_WIN0_OBJ | WININ_WIN0_CLR;
            sTransitionData->WINOUT = WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3;
            sTransitionData->BLDCNT = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG0 | BLDCNT_TGT1_BD;
        }
        if (map == LUG_MAP_VORTEX)
        {
            GI_EndWindow();
            LI_InitWave();
        }
        GI_ShowMap(map);
        task->tGiShown = map;
    }

    // het ooglid: een ellips over de hele breedte die opengaat
    if (t >= LUG_EYE && t < LUG_VORTEX)
    {
        // een amandelvorm met spitse hoeken: halve breedte = W * wortel(1 - |dy| / h)
        h = 1 + min((t - LUG_EYE) * 100 / LUG_EYE_LEN, 100);
        for (y = 0; y < DISPLAY_HEIGHT; y++)
        {
            s32 dy = abs(y - 80), half;
            if (dy >= h)
            {
                win[y] = 0;
                continue;
            }
            half = 136 * Sqrt(((h - dy) << 8) / h) >> 4;
            win[y] = WIN_RANGE(max(0, 120 - half), min(DISPLAY_WIDTH, 120 + half));
        }
        // de spleet gloeit fel en dooft als het oog open is
        SetGpuReg(REG_OFFSET_BLDY, max(3, 16 - (t - LUG_EYE) * 13 / LUG_EYE_LEN));
    }

    // de draaikolk wervelt en kantelt de storm in
    if (t >= LUG_VORTEX)
    {
        s32 a = t - LUG_VORTEX, shear = (t >= LUG_STORM) ? (t - LUG_STORM) : 0;
        for (y = 0; y < DISPLAY_HEIGHT; y++)
            hofs[y] = Sin((y * 4 + a * 7) & 0xFF, 2 + a / 6) + (((y - 80) * shear) >> 3);
        SetGpuReg(REG_OFFSET_BG0VOFS, (t >= LUG_STORM ? LI_ShakeAmp(2 + shear / 10) : 0) & 0x1FF);
    }

    // de zilveren veer dwarrelt rustig omlaag
    s = LI_S(0);
    if (t >= LUG_SEA && t < LUG_EYE)
    {
        k = t - LUG_SEA;
        s->invisible = FALSE;
        s->x = 120 + Sin((k * 3) & 0xFF, 36);
        s->y = -16 + k * 112 / (LUG_EYE - LUG_SEA);
        LI_Frame(0, LUG_TAG_FEATHER, (((k * 3 + 64) & 0xFF) < 128) ? 0 : 1, 16);
        BlendPalettes(GI_SpritePalBit(LUG_TAG_FEATHER), max(depth / 3, (t - (LUG_EYE - 16))), RGB_BLACK);
    }
    else
    {
        s->invisible = TRUE;
    }
    // bubbels stijgen (in het donker steeds minder te zien)
    for (i = 0; i < LUG_BUBBLES; i++)
    {
        s = LI_S(1 + i);
        if (t < LUG_SEA || t >= LUG_EYE - 4)
        {
            s->invisible = TRUE;
            continue;
        }
        k = ((t * sLugBubbleSpeed[i]) >> 4) + sLugBubbleOfs[i];
        s->invisible = FALSE;
        s->y = 184 - (k % 200);
        s->x = sLugBubbleX[i] + Sin((t * 4 + i * 40) & 0xFF, 4);
        LI_Frame(1 + i, LUG_TAG_BUBBLE, (i & 1), 4);
    }
    BlendPalettes(GI_SpritePalBit(LUG_TAG_BUBBLE), min(depth * 3 / 4, 16), LUG_DEEP);

    // geluid
    if (t == LUG_SEA)
        PlaySE(SE_M_DIVE);
    if (t == LUG_SEA + 30 || t == LUG_SEA + 64)
        PlaySE(SE_M_BUBBLE);
    if (t == LUG_EYE + 6)
        PlayCry_Normal(SPECIES_LUGIA, 0);
    if (t == LUG_VORTEX)
        PlaySE(SE_M_WHIRLPOOL);
    if (t == LUG_STORM)
        PlaySE(SE_M_GUST);
    if (t == LUG_STORM + 8 || t == LUG_STORM + 22)
        PlaySE(SE_THUNDER);

    GI_FadeWorld(t, LUG_SEA, keep);
    if (t >= LUG_EYE && t < LUG_VORTEX)
        gPlttBufferFaded[0] = RGB(1, 2, 7);
    if (t >= LUG_SEA && t < LUG_SEA + 8)
        BlendPalettes(GI_BG_PALS, 16 - (t - LUG_SEA) * 2, RGB_BLACK);
    GI_Flash(t, LUG_VORTEX, 8, 16, keep, RGB_WHITE);
    GI_Flash(t, LUG_STORM + 8, 6, 14, keep, RGB_WHITE);
    GI_Flash(t, LUG_STORM + 22, 6, 14, keep, RGB_WHITE);
    if (GI_WhiteOut(t, LUG_END, keep))
    {
        for (i = 0; i < 1 + LUG_BUBBLES; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTLugia_Finish(struct Task *task)
{
    GI_EndWindow();
    LI_EndWave();
    LI_DestroySprites();
    GI_FreeTag(LUG_TAG_FEATHER);
    GI_FreeTag(LUG_TAG_BUBBLE);
    GI_Free();
}

static const struct RouteTransition sRT_LegendLugia =
{
    sPikachu_Tileset, 32, sLegLugia_Pal + 32, 1, 1, 0, RTLugia_Init, RTLugia_Update, RTLugia_Finish
};

static void Task_LegendLugia(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendLugia);
}

// =====================================================================================================================
// Ho-Oh: het silhouet van de Bell Tower bij schemering, gloeiende sintels (paletcyclus), de klok luidt. Een regenboog
// veegt over het scherm (kolom voor kolom), dan schiet een muur van vlammen op (Fire uit de gevechtsanimaties) en Ho-Oh
// stijgt eruit op als een feniks (eerst een gloeiend silhouet). Gouden veren waaieren uit als vleugels, alles glanst in
// regenboogkleuren, flits, gevecht.
static const u32 sLegHooh_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_hooh.4bpp.smol");
static const u32 sLegHooh_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_hooh_maps.bin.smol");
static const u16 sLegHooh_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_hooh.gbapal");

enum { HO_MAP_DUSK, HO_MAP_RAIN };
#define HO_TAG_FIRE     0x5A62
#define HO_TAG_FEATHER  0x5A63
#define HO_DUSK         6
#define HO_RAIN         30
#define HO_RAIN_LEN     22
#define HO_FIRE         66
#define HO_FIRE_LEN     30
#define HO_RISE         86
#define HO_RISE_LEN     36
#define HO_WINGS        126
#define HO_WINGS_LEN    16
#define HO_FLASH        158
#define HO_END          190
#define HO_FLAMES       16
#define HO_FEATHERS     10
#define HO_EMBER        11    // BG 13: drie fasen van de sintels
#define HO_X            120
#define HO_Y            62

static const u16 sHoGold[16] = {0, RGB(31, 30, 18), RGB(31, 27, 10), RGB(30, 23, 5), RGB(28, 19, 3), RGB(26, 15, 2),
                                RGB(22, 12, 2), RGB(18, 9, 1)};
static const u16 sHoRainbow[7] = {RGB(31, 6, 6), RGB(31, 17, 4), RGB(31, 28, 6), RGB(10, 26, 8), RGB(6, 20, 31),
                                  RGB(10, 10, 28), RGB(20, 8, 26)};
// eindpositie van de veren (t.o.v. Ho-Oh), linkervleugel; de rechter is gespiegeld
static const s8 sHoWing[HO_FEATHERS / 2][3] = {{-60, -2, 0}, {-74, -20, 16}, {-82, -38, 32}, {-84, -56, 48}, {-78, -72, 64}}; // x, y, hoek

static void RTHooh_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegHooh_Tiles, sLegHooh_Maps);
    LoadPalette(sLegHooh_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    for (i = 0; i < HO_FLAMES; i++)
        LI_Make(i, gBattleAnimSpriteGfx_Fire, 32 * 256 / 2, gBattleAnimSpritePal_Fire, HO_TAG_FIRE, &sGI_Oam32, 16 + (i & 7) * 30 + ((i >> 3) ? 15 : 0), 200, (i >> 3) ? 3 : 0);
    for (i = 0; i < HO_FEATHERS; i++)
        LI_Make(HO_FLAMES + i, gBattleAnimSpriteGfx_WhiteFeather, 32 * 64 / 2, sHoGold, HO_TAG_FEATHER, &sGI_Oam32Affine, HO_X, HO_Y, 2);
    task->tGiSprite0 = LI_MonPicAffine(SPECIES_HO_OH, HO_X, 220);
    GI_Sprite(task->tGiSprite0)->subpriority = 1;
    task->tGiShown = 0xFF;
}

static bool8 RTHooh_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, y;
    u32 keep, hoBit;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s, *hooh = GI_Sprite(task->tGiSprite0);

    hoBit = GI_SpritePalBit(SPECIES_HO_OH);
    keep = GI_SpritePalBit(HO_TAG_FIRE) | GI_SpritePalBit(HO_TAG_FEATHER) | hoBit;
    GI_ResetPals(keep);
    LoadPalette(sLegHooh_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    // de sintels fonkelen
    for (i = 0; i < 3; i++)
        pal[HO_EMBER + i] = sLegHooh_Pal[HO_EMBER + (i + t / 5) % 3];
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);
    // de lucht kleurt mee met de vlammen
    if (t >= HO_FIRE)
        BlendPalettes((1 << 13) | (1 << 14), min((t - HO_FIRE) / 3, 7), RGB(31, 10, 2));

    if (t == HO_DUSK)
    {
        GI_KillFieldWindows();
        GI_ShowMap(HO_MAP_DUSK);
    }
    // de regenboog veegt van links naar rechts over het scherm
    if (t >= HO_RAIN && t < HO_RAIN + HO_RAIN_LEN + 1)
    {
        s32 c0 = (t - HO_RAIN) * 30 / HO_RAIN_LEN, c1 = min((t - HO_RAIN + 1) * 30 / HO_RAIN_LEN, 30);
        if (c1 > c0)
            GI_PutRect(HO_MAP_RAIN, c0, 0, c1 - c0, 20, c0, 0);
    }

    // de muur van vlammen schiet op
    for (i = 0; i < HO_FLAMES; i++)
    {
        s = LI_S(i);
        if (t < HO_FIRE)
            continue;
        k = min(t - HO_FIRE - (i & 7) % 3 * 2, HO_FIRE_LEN);
        if (k < 0)
            continue;
        s->invisible = FALSE;
        y = (i >> 3) ? 104 : 128;
        s->y = y + (HO_FIRE_LEN - k) * (HO_FIRE_LEN - k) * 80 / (HO_FIRE_LEN * HO_FIRE_LEN) + Sin(((t + i * 23) * 8) & 0xFF, 2);
        LI_Frame(i, HO_TAG_FIRE, ((t >> 2) + i * 3) & 7, 16);
    }

    // Ho-Oh stijgt op uit de vlammen, eerst als gloeiend silhouet
    if (t >= HO_RISE)
    {
        k = min(t - HO_RISE, HO_RISE_LEN);
        hooh->invisible = FALSE;
        hooh->y = HO_Y + (HO_RISE_LEN - k) * (HO_RISE_LEN - k) * 160 / (HO_RISE_LEN * HO_RISE_LEN);
        LI_Affine(task->tGiSprite0, 384 + k * 64 / HO_RISE_LEN, 0);
        if (k < HO_RISE_LEN)
            BlendPalettes(hoBit, 16 - k * 16 / HO_RISE_LEN, RGB(31, 14, 2));
        else
            BlendPalettes(hoBit, 4 + Sin((t * 10) & 0xFF, 2), sHoRainbow[(t / 3) % 7]);
    }

    // gouden veren waaieren uit als vleugels en glanzen in regenboogkleuren
    for (i = 0; i < HO_FEATHERS; i++)
    {
        s32 j = i % (HO_FEATHERS / 2), side = (i < HO_FEATHERS / 2) ? 1 : -1, e;
        s = LI_S(HO_FLAMES + i);
        k = t - HO_WINGS - j * 2;
        if (k < 0)
            continue;
        s->invisible = FALSE;
        e = min(k, HO_WINGS_LEN);
        e = HO_WINGS_LEN * HO_WINGS_LEN - (HO_WINGS_LEN - e) * (HO_WINGS_LEN - e); // uitlopend
        s->x = HO_X + side * sHoWing[j][0] * e / (HO_WINGS_LEN * HO_WINGS_LEN);
        s->y = HO_Y + sHoWing[j][1] * e / (HO_WINGS_LEN * HO_WINGS_LEN) + Sin(((t + j * 9) * 10) & 0xFF, 2);
        LI_Frame(HO_FLAMES + i, HO_TAG_FEATHER, ((t >> 3) + j) & 1, 16);
        // de veerpunt wijst naar buiten (links in de art), de binnenste veren schuiner omhoog
        k = sHoWing[j][2] + Sin(((t + j * 11) * 6) & 0xFF, 4);
        LI_Affine(sLI_Spr[HO_FLAMES + i], 192 + e * 256 / (HO_WINGS_LEN * HO_WINGS_LEN), (u16)(-(side > 0 ? k : 180 - k) * 182));
    }
    if (t >= HO_WINGS)
        BlendPalettes(GI_SpritePalBit(HO_TAG_FEATHER), 3, sHoRainbow[(t / 4) % 7]);

    // geluid
    if (t == HO_DUSK || t == HO_DUSK + 24)
        PlaySE(SE_M_HEAL_BELL);
    if (t == HO_RAIN)
        PlaySE(SE_SHINY);
    if (t == HO_FIRE)
        PlaySE(SE_M_SACRED_FIRE);
    if (t == HO_RISE + 14)
        PlaySE(SE_M_FLAME_WHEEL);
    if (t == HO_RISE + 26)
        PlayCry_Normal(SPECIES_HO_OH, 0);
    if (t == HO_WINGS)
        PlaySE(SE_M_MORNING_SUN);
    if (t == HO_FLASH)
        PlaySE(SE_M_SACRED_FIRE2);

    GI_Shake((t >= HO_FIRE && t < HO_FIRE + 16) ? 1 : 0);
    GI_FadeWorld(t, HO_DUSK, keep);
    if (t >= HO_DUSK && t < HO_DUSK + 8)
        BlendPalettes(GI_BG_PALS, 16 - (t - HO_DUSK) * 2, RGB_BLACK);
    GI_Flash(t, HO_RAIN, 6, 8, keep, RGB_WHITE);
    GI_Flash(t, HO_FLASH, 12, 16, keep, RGB(31, 28, 16));
    if (GI_WhiteOut(t, HO_END, keep))
    {
        for (i = 0; i < HO_FLAMES + HO_FEATHERS; i++)
            LI_S(i)->invisible = TRUE;
        hooh->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTHooh_Finish(struct Task *task)
{
    GI_Shake(0);
    LI_DestroySprites();
    LI_DestroyMonPic(task->tGiSprite0);
    GI_FreeTag(HO_TAG_FIRE);
    GI_FreeTag(HO_TAG_FEATHER);
    GI_Free();
}

static const struct RouteTransition sRT_LegendHooh =
{
    sPikachu_Tileset, 32, sLegHooh_Pal + 32, 1, 1, 0, RTHooh_Init, RTHooh_Update, RTHooh_Finish
};

static void Task_LegendHooh(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendHooh);
}

// =====================================================================================================================
// Volcanion: een manometer op een geklonken plaat ("DO NOT TAP THE GLASS"). De naald kruipt tikkend van "fine" naar
// "NOPE", blijft daar trillend hangen, de klinknagels schieten er een voor een uit (de plaat trilt steeds harder), en
// dan blaast er van beide kanten stoom in beeld (zijn armkanonnen) tot alles wit is.
static const u32 sLegVolcanion_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion.4bpp.smol");
static const u32 sLegVolcanion_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_maps.bin.smol");
static const u16 sLegVolcanion_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion.gbapal");
static const u32 sLegVolcanion_NeedleGfx[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_needle.4bpp.smol");
static const u16 sLegVolcanion_NeedlePal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion_needle.gbapal");
static const u32 sLegVolcanion_RivetGfx[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_rivet.4bpp.smol");
static const u16 sLegVolcanion_RivetPal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion_rivet.gbapal");

enum { VOL_MAP_GAUGE, VOL_MAP_HOLES };
#define VOL_TAG_NEEDLE  0x5A64
#define VOL_TAG_RIVET   0x5A65
#define VOL_TAG_STEAM   0x5A66
#define VOL_SHOW        6
#define VOL_RED         96    // de naald staat in het rood
#define VOL_POP         100   // de eerste klinknagel
#define VOL_STEAM       138
#define VOL_END         178
#define VOL_RIVETS      6
#define VOL_STEAMS      10
#define VOL_CX          120
#define VOL_CY          76
#define VOL_ZONE_RED    9     // BG 14: de rode zone (knippert)

// klinknagels die eruit schieten (tile x, y van het 2x2-blok) en wanneer
static const u8 sVolRivet[VOL_RIVETS][3] = {{1, 1, 0}, {27, 17, 10}, {27, 1, 18}, {1, 17, 24}, {1, 9, 29}, {27, 9, 33}};
static const u8 sVolSteamY[VOL_STEAMS / 2] = {26, 54, 82, 110, 138};

static void RTVolcanion_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegVolcanion_Tiles, sLegVolcanion_Maps);
    LoadPalette(sLegVolcanion_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    LI_Make(0, sLegVolcanion_NeedleGfx, 64 * 64 / 2, sLegVolcanion_NeedlePal, VOL_TAG_NEEDLE, &sGI_Oam64Affine, VOL_CX, VOL_CY, 0);
    for (i = 0; i < VOL_RIVETS; i++)
        LI_Make(1 + i, sLegVolcanion_RivetGfx, 16 * 16 / 2, sLegVolcanion_RivetPal, VOL_TAG_RIVET, &sGI_Oam16, 0, 0, 0);
    for (i = 0; i < VOL_STEAMS; i++)
        LI_Make(1 + VOL_RIVETS + i, gBattleAnimSpriteGfx_MistCloud, 32 * 32 / 2, gBattleAnimSpritePal_MistCloud, VOL_TAG_STEAM, &sGI_Oam32Affine, 0, sVolSteamY[i % (VOL_STEAMS / 2)], 0);
    task->tGiShown = 0xFF;
}

static bool8 RTVolcanion_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, deg, dx = 0, dy = 0, amp;
    u32 keep = GI_SpritePalBit(VOL_TAG_NEEDLE) | GI_SpritePalBit(VOL_TAG_RIVET) | GI_SpritePalBit(VOL_TAG_STEAM);
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s, *needle = LI_S(0);

    GI_ResetPals(keep);
    LoadPalette(sLegVolcanion_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    if (t >= VOL_RED && ((t >> 2) & 1))
        pal[16 + VOL_ZONE_RED] = RGB(31, 20, 12);
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    if (t == VOL_SHOW)
    {
        GI_KillFieldWindows();
        GI_ShowMap(VOL_MAP_GAUGE);
    }

    // de plaat trilt steeds harder (BG en sprites samen)
    amp = (t >= VOL_POP) ? 1 + (t - VOL_POP) / 12 : (t >= VOL_RED - 20 ? 1 : 0);
    if (amp)
    {
        dx = LI_ShakeAmp(amp);
        dy = LI_ShakeAmp(amp);
    }
    SetGpuReg(REG_OFFSET_BG0HOFS, dx & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, dy & 0x1FF);

    // de naald: kruipt (steeds sneller) van -128 naar +118 graden en blijft daar trillend hangen
    if (t >= VOL_SHOW)
    {
        k = min(t - VOL_SHOW, VOL_RED - VOL_SHOW);
        deg = -128 + 246 * k * k / ((VOL_RED - VOL_SHOW) * (VOL_RED - VOL_SHOW));
        deg += (t >= VOL_RED) ? LI_ShakeAmp(4) : ((t >> 1) & 1);
        needle->invisible = FALSE;
        needle->x2 = -dx;
        needle->y2 = -dy;
        LI_Affine(sLI_Spr[0], 448, (u16)(-deg * 182));
        if (t < VOL_RED && (t - VOL_SHOW) % 12 == 0)
            PlaySE(SE_CLICK);
    }

    // klinknagels schieten eruit
    for (i = 0; i < VOL_RIVETS; i++)
    {
        s32 tx = sVolRivet[i][0], ty = sVolRivet[i][1];
        s = LI_S(1 + i);
        k = t - VOL_POP - sVolRivet[i][2];
        if (k < 0)
            continue;
        if (k == 0)
        {
            GI_PutRect(VOL_MAP_HOLES, tx, ty, 2, 2, tx, ty);
            sLI_Phys[i][0] = (tx * 8 + 8) << 4;
            sLI_Phys[i][1] = (ty * 8 + 8) << 4;
            sLI_Phys[i][2] = (tx < 15 ? -1 : 1) * (20 + (Random() & 15));
            sLI_Phys[i][3] = -64 - (Random() & 15);
            PlaySE(SE_M_COMET_PUNCH);
        }
        sLI_Phys[i][0] += sLI_Phys[i][2];
        sLI_Phys[i][1] += sLI_Phys[i][3];
        sLI_Phys[i][3] += 6;
        s->invisible = (sLI_Phys[i][1] >> 4) > 180;
        s->x = sLI_Phys[i][0] >> 4;
        s->y = sLI_Phys[i][1] >> 4;
        s->oam.matrixNum = ((k >> 1) & 1) ? ST_OAM_HFLIP : 0;
    }

    // stoom blaast van beide kanten naar binnen en wordt groter
    for (i = 0; i < VOL_STEAMS; i++)
    {
        s32 side = (i < VOL_STEAMS / 2) ? -1 : 1;
        s = LI_S(1 + VOL_RIVETS + i);
        k = t - VOL_STEAM - ((i * 3) % 5) * 2;
        if (k < 0)
            continue;
        s->invisible = FALSE;
        s->x = 120 + side * (150 - min(k * 6, 120)) + Sin(((t + i * 30) * 12) & 0xFF, 2);
        s->y = sVolSteamY[i % (VOL_STEAMS / 2)] + Sin(((t + i * 17) * 9) & 0xFF, 3);
        LI_Affine(sLI_Spr[1 + VOL_RIVETS + i], min(320 + k * 20, 512), 0);
    }

    // geluid
    if (t == VOL_RED)
        PlaySE(SE_M_SCREECH);
    if (t == VOL_STEAM - 8)
        PlayCry_Normal(SPECIES_VOLCANION, 0);
    if (t == VOL_STEAM)
        PlaySE(SE_M_MIST);
    if (t == VOL_STEAM + 14)
        PlaySE(SE_M_EXPLOSION);

    GI_FadeWorld(t, VOL_SHOW, keep);
    if (t >= VOL_SHOW && t < VOL_SHOW + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - VOL_SHOW) * 2, RGB_BLACK);
    if (t >= VOL_STEAM + 6 && t < VOL_END - 4)
    {
        k = (t - VOL_STEAM - 6) * 14 / (VOL_END - 4 - VOL_STEAM - 6);
        BlendPalettes(GI_BG_PALS | GI_SpritePalBit(VOL_TAG_NEEDLE) | GI_SpritePalBit(VOL_TAG_RIVET), k, RGB_WHITE);
    }
    if (GI_WhiteOut(t, VOL_END, keep))
    {
        for (i = 0; i < 1 + VOL_RIVETS + VOL_STEAMS; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTVolcanion_Finish(struct Task *task)
{
    LI_EndWave();
    LI_DestroySprites();
    GI_FreeTag(VOL_TAG_NEEDLE);
    GI_FreeTag(VOL_TAG_RIVET);
    GI_FreeTag(VOL_TAG_STEAM);
    GI_Free();
}

static const struct RouteTransition sRT_LegendVolcanion =
{
    sPikachu_Tileset, 32, sLegVolcanion_Pal + 32, 1, 1, 0, RTVolcanion_Init, RTVolcanion_Update, RTVolcanion_Finish
};

static void Task_LegendVolcanion(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendVolcanion);
}

// =====================================================================================================================
// Hoopa: midden in het beeld gaat een ringportaal open (venster 0 als groeiende cirkel), de woestijnnacht verschijnt.
// Er valt van alles uit (echte item-iconen), door de ring zwemt een Wailord voorbij (alleen binnen de ring te zien, hij
// past er niet door), een verdwaalde Magikarp floept eruit. Dan kijkt Hoopa zelf door de ring, zijn hand grijpt de camera
// (de hand uit Hoopa's gevechtsanimatie, x4) en trekt je de ring in: de wervel vult het beeld, wit, gevecht.
static const u32 sLegHoopa_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_hoopa.4bpp.smol");
static const u32 sLegHoopa_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_hoopa_maps.bin.smol");
static const u16 sLegHoopa_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_hoopa.gbapal");
static const u32 sLegHoopa_HandGfx[] = INCBIN_U32("graphics/battle_transitions/legend_hoopa_hand.4bpp.smol");
static const u16 sLegHoopa_HandPal[] = INCBIN_U16("graphics/battle_transitions/legend_hoopa_hand.gbapal");

enum { HP_MAP_PORTAL, HP_MAP_INSIDE };
#define HP_TAG_HAND     0x5A67
#define HP_TAG_ITEM     0x5A68 // t/m 0x5A6B (vier plekken)
#define HP_OPEN         6
#define HP_OPEN_LEN     14
#define HP_REVEAL       (HP_OPEN + HP_OPEN_LEN + 4)
#define HP_ITEMS        30
#define HP_ITEM_GAP     8
#define HP_NUM_ITEMS    7
#define HP_WAIL         100
#define HP_WAIL_LEN     40
#define HP_KARP         (HP_WAIL + HP_WAIL_LEN + 2)
#define HP_HOOPA        170
#define HP_HAND         186
#define HP_HAND_LEN     14
#define HP_GRAB         (HP_HAND + HP_HAND_LEN)
#define HP_INSIDE       (HP_GRAB + 4)
#define HP_END          (HP_INSIDE + 24)
#define HP_CX           120
#define HP_CY           68
#define HP_RING_IN      46
#define tHpSpecies      tRtA

static const u16 sHpItems[HP_NUM_ITEMS] = {ITEM_NUGGET, ITEM_POKE_BALL, ITEM_OLD_ROD, ITEM_RARE_CANDY, ITEM_SODA_POP,
                                           ITEM_MACH_BIKE, ITEM_BIG_PEARL};
static const s8 sHpItemVx[HP_NUM_ITEMS] = {-28, 22, -12, 34, -36, 14, -20};

static void HP_SetCircle(s32 r)
{
    if (r <= 0)
        CpuFill16(0, gScanlineEffectRegBuffers[0], DISPLAY_HEIGHT * 2);
    else
        SetCircularMask(gScanlineEffectRegBuffers[0], HP_CX, HP_CY, r);
}

static void HP_SetMon(struct Task *task, u16 species, s16 x, s16 y, bool32 affine)
{
    LI_DestroyMonPic(task->tGiSprite0);
    task->tGiSprite0 = affine ? LI_MonPicAffine(species, x, y) : GI_MonPic(species, x, y);
    GI_Sprite(task->tGiSprite0)->invisible = FALSE;
    GI_Sprite(task->tGiSprite0)->subpriority = 3; // de hand komt ervoor
}

// item-iconen: niet via DestroySpriteAndFreeResources (de template van AddItemIconSprite is al vrijgegeven), maar per tag
static void HP_FreeItem(u32 slot)
{
    if (sLI_Spr[1 + slot] < MAX_SPRITES)
        DestroySprite(&gSprites[sLI_Spr[1 + slot]]);
    sLI_Spr[1 + slot] = MAX_SPRITES;
    FreeSpriteTilesByTag(HP_TAG_ITEM + slot);
    FreeSpritePaletteByTag(HP_TAG_ITEM + slot);
}

static void HP_FreeItems(void)
{
    u32 i;
    for (i = 0; i < 4; i++)
        HP_FreeItem(i);
}

static void RTHoopa_Init(struct Task *task)
{
    u16 species = GetMonData(&gEnemyParty[0], MON_DATA_SPECIES);

    task->tHpSpecies = (species == SPECIES_HOOPA_UNBOUND) ? SPECIES_HOOPA_UNBOUND : SPECIES_HOOPA_CONFINED;
    GI_LoadGfx(sLegHoopa_Tiles, sLegHoopa_Maps);
    LoadPalette(sLegHoopa_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    LI_Make(0, sLegHoopa_HandGfx, 64 * 64 / 2, sLegHoopa_HandPal, HP_TAG_HAND, &sGI_Oam64Affine, HP_CX, HP_CY, 0);
    task->tGiSprite0 = MAX_SPRITES;
    task->tGiShown = 0xFF;
}

static bool8 RTHoopa_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, slot;
    u32 keep = GI_SpritePalBit(HP_TAG_HAND);
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0), *hand = LI_S(0);

    for (i = 0; i < 4; i++)
        keep |= GI_SpritePalBit(HP_TAG_ITEM + i);
    if (task->tGiSprite0 < MAX_SPRITES)
        keep |= 1 << (16 + gSprites[task->tGiSprite0].oam.paletteNum);
    GI_ResetPals(keep);
    LoadPalette(sLegHoopa_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    // de wervel draait (aan het eind steeds sneller)
    k = (t >= HP_GRAB) ? (t - HP_GRAB) * (t - HP_GRAB) / 8 + t / 2 : t / 3;
    for (i = 0; i < 8; i++)
        pal[16 + 1 + i] = sLegHoopa_Pal[16 + 1 + ((i + k) & 7)];
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    // het portaal gaat open, dan de woestijnnacht eromheen
    if (t == HP_OPEN)
    {
        GI_KillFieldWindows();
        GI_InitWindow();
        sTransitionData->WINOUT = WINOUT_WIN01_OBJ;
        HP_SetCircle(0);
        GI_ShowMap(HP_MAP_PORTAL);
        PlaySE(SE_M_TELEPORT);
    }
    if (t >= HP_OPEN && t <= HP_OPEN + HP_OPEN_LEN)
        HP_SetCircle((t - HP_OPEN) * (HP_RING_IN + 8) / HP_OPEN_LEN);
    if (t >= HP_REVEAL && t <= HP_REVEAL + 10)
        HP_SetCircle(HP_RING_IN + 8 + (t - HP_REVEAL) * 15);

    // spullen vallen eruit (vier plekken, om de beurt)
    for (i = 0; i < HP_NUM_ITEMS; i++)
    {
        k = t - HP_ITEMS - i * HP_ITEM_GAP;
        slot = i & 3;
        if (k == 0)
        {
            HP_FreeItem(slot);
            sLI_Spr[1 + slot] = AddItemIconSprite(HP_TAG_ITEM + slot, HP_TAG_ITEM + slot, sHpItems[i]);
            if (sLI_Spr[1 + slot] < MAX_SPRITES)
                gSprites[sLI_Spr[1 + slot]].oam.priority = 0;
            sLI_Phys[slot][0] = HP_CX << 4;
            sLI_Phys[slot][1] = HP_CY << 4;
            sLI_Phys[slot][2] = sHpItemVx[i];
            sLI_Phys[slot][3] = -56 - (i & 1) * 12;
            PlaySE((i & 1) ? SE_BALL_BOUNCE_1 : SE_BALL_BOUNCE_3);
        }
        if (k < 0 || k >= 4 * HP_ITEM_GAP || sLI_Spr[1 + slot] >= MAX_SPRITES)
            continue;
        s = &gSprites[sLI_Spr[1 + slot]];
        sLI_Phys[slot][0] += sLI_Phys[slot][2];
        sLI_Phys[slot][1] += sLI_Phys[slot][3];
        sLI_Phys[slot][3] += 7;
        s->x = sLI_Phys[slot][0] >> 4;
        s->y = sLI_Phys[slot][1] >> 4;
        if (s->y > 190)
            HP_FreeItem(slot);
    }

    // een Wailord zwemt achter de ring langs (alleen binnen de ring te zien)
    if (t == HP_WAIL)
    {
        HP_FreeItems();
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL;
        HP_SetCircle(HP_RING_IN);
        HP_SetMon(task, SPECIES_WAILORD, -70, HP_CY + 4, TRUE);
        mon = GI_Sprite(task->tGiSprite0);
        LI_Affine(task->tGiSprite0, 512, 0);
    }
    if (t >= HP_WAIL && t < HP_KARP)
    {
        mon->x = -70 + (t - HP_WAIL) * 380 / HP_WAIL_LEN;
        mon->y = HP_CY + 4 + Sin(((t - HP_WAIL) * 6) & 0xFF, 3);
        if (t == HP_WAIL + HP_WAIL_LEN / 2)
            PlayCry_Normal(SPECIES_WAILORD, 0);
    }
    // een verdwaalde Magikarp floept eruit
    if (t == HP_KARP)
    {
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ;
        HP_SetCircle(200);
        HP_SetMon(task, SPECIES_MAGIKARP, HP_CX, HP_CY, FALSE);
        mon = GI_Sprite(task->tGiSprite0);
        sLI_Phys[0][0] = HP_CX << 4;
        sLI_Phys[0][1] = HP_CY << 4;
        sLI_Phys[0][2] = 18;
        sLI_Phys[0][3] = -44;
        PlayCry_Normal(SPECIES_MAGIKARP, 0);
    }
    if (t > HP_KARP && t < HP_HOOPA)
    {
        sLI_Phys[0][0] += sLI_Phys[0][2];
        sLI_Phys[0][1] += sLI_Phys[0][3];
        sLI_Phys[0][3] += 8;
        mon->x = sLI_Phys[0][0] >> 4;
        mon->y = sLI_Phys[0][1] >> 4;
        mon->oam.matrixNum = ((t >> 2) & 1) ? ST_OAM_HFLIP : 0;
        mon->invisible = (mon->y > 200);
        if (t == HP_KARP + 6)
            PlaySE(SE_BALL_BOUNCE_2);
    }
    // Hoopa kijkt door de ring (weer alleen binnen de ring te zien)
    if (t == HP_HOOPA)
    {
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL;
        HP_SetCircle(HP_RING_IN);
        HP_SetMon(task, task->tHpSpecies, HP_CX, 150, FALSE);
        mon = GI_Sprite(task->tGiSprite0);
    }
    if (t >= HP_HOOPA && t < HP_INSIDE)
    {
        k = min(t - HP_HOOPA, 12);
        mon->y = HP_CY + 6 + (12 - k) * (12 - k) * 70 / 144;
        if (t == HP_HOOPA + 8)
            PlayCry_Normal(task->tHpSpecies, 0);
    }
    // de hand grijpt de camera en trekt je erin
    if (t == HP_HAND)
    {
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ;
        HP_SetCircle(200);
        hand->invisible = FALSE;
        PlaySE(SE_M_VITAL_THROW);
    }
    if (t >= HP_HAND)
    {
        if (t < HP_GRAB)
            k = 96 + (t - HP_HAND) * (t - HP_HAND) * 416 / (HP_HAND_LEN * HP_HAND_LEN);
        else if (t < HP_INSIDE)
            k = 512;
        else
            k = max(512 - (t - HP_INSIDE) * 40, 32);
        LI_Affine(sLI_Spr[0], k, (u16)(Sin((t * 9) & 0xFF, 6) * 160));
        hand->x = HP_CX + (t < HP_GRAB ? (t - HP_HAND) * 2 : 28) - 12;
        hand->y = HP_CY + 8;
        hand->invisible = (t >= HP_INSIDE + 12);
    }
    if (t == HP_GRAB)
        PlaySE(SE_M_VITAL_THROW2);
    if (t == HP_INSIDE)
    {
        mon->invisible = TRUE;
        GI_ShowMap(HP_MAP_INSIDE);
        PlaySE(SE_WARP_IN);
    }

    // sprites die deze frame zijn gemaakt ook meenemen (anders zijn ze een frame zwart)
    for (i = 0; i < 4; i++)
        keep |= GI_SpritePalBit(HP_TAG_ITEM + i);
    if (task->tGiSprite0 < MAX_SPRITES)
        keep |= 1 << (16 + gSprites[task->tGiSprite0].oam.paletteNum);
    GI_ResetPals(keep);
    GI_Shake((t >= HP_GRAB && t < HP_INSIDE + 2) ? 3 : 0);
    GI_FadeWorld(t, HP_OPEN, keep);
    GI_Flash(t, HP_OPEN + HP_OPEN_LEN, 6, 10, keep, RGB(31, 24, 31));
    GI_Flash(t, HP_INSIDE, 8, 16, keep, RGB_WHITE);
    if (GI_WhiteOut(t, HP_END, keep))
    {
        hand->invisible = mon->invisible = TRUE;
        GI_EndWindow();
        return TRUE;
    }
    return FALSE;
}

static void RTHoopa_Finish(struct Task *task)
{
    GI_Shake(0);
    GI_EndWindow();
    HP_FreeItems();
    LI_DestroySprites();
    LI_DestroyMonPic(task->tGiSprite0);
    task->tGiSprite0 = MAX_SPRITES;
    GI_FreeTag(HP_TAG_HAND);
    GI_Free();
}

static const struct RouteTransition sRT_LegendHoopa =
{
    sPikachu_Tileset, 32, sLegHoopa_Pal + 32, 1, 1, 0, RTHoopa_Init, RTHoopa_Update, RTHoopa_Finish
};

static void Task_LegendHoopa(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendHoopa);
}

// =====================================================================================================================
// Forces of Nature (Tornadus, Thundurus, Landorus, ook Therian): een weerbericht dat ontspoort. De echte Hoenn-kaart uit
// de PokéNav als weerkaart, een wolkenfront trekt van west naar oost ("Mild breeze from the west. Lovely."). Dan de
// UPDATE-balk, en per Pokémon gaat het anders mis:
// - Tornadus: het front blijkt een tornado (Tornado uit de gevechtsanimaties), de kaart golft en scheurt rij voor rij weg.
// - Thundurus: drie bliksems slaan in op de kaart (Lightning), brandplekken, Thundurus in de flits.
// - Landorus: de grond barst open vanuit het midden, zandstorm, en een "usage stats"-kaartje schuift in beeld
//   (LANDORUS-T: "OU usage: very yes").
static const u32 sLegForces_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_forces.4bpp.smol");
static const u32 sLegForces_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_forces_maps.bin.smol");
static const u16 sLegForces_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_forces.gbapal");

enum { FN_MAP_TV, FN_MAP_TV_T, FN_MAP_TV_TH, FN_MAP_TV_L, FN_MAP_CRACKED, FN_MAP_BURNT, FN_MAP_CARD_T, FN_MAP_CARD_I };
enum { FN_TORNADUS, FN_THUNDURUS, FN_LANDORUS };
#define FN_TAG_CLOUD    0x5A6C
#define FN_TAG_TORNADO  0x5A6D
#define FN_TAG_BOLT     0x5A6E
#define FN_TV           6
#define FN_DERAIL       96
#define FN_CLOUDS       5
#define FN_BOLTS        3
#define FN_ACCENT       6     // BG 14: de gele streep van de onderbalk (kleur per Pokémon)
#define FN_LIVE         5     // BG 14: LIVE (knippert na de UPDATE)
#define FN_SPR_TORNADO  FN_CLOUDS
#define FN_SPR_BOLT     (FN_CLOUDS + 1)
#define tFnKind         tRtA
#define tFnSpecies      tRtB
// Tornadus
#define FN_T_TWISTER    104
#define FN_T_WAVE       112
#define FN_T_TEAR       128
#define FN_T_FLY        148
#define FN_T_END        196
// Thundurus
#define FN_TH_STRIKE    106
#define FN_TH_GAP       20
#define FN_TH_MON       (FN_TH_STRIKE + 3 * FN_TH_GAP)
#define FN_TH_END       (FN_TH_MON + 32)
// Landorus
#define FN_L_CRACK      104
#define FN_L_CRACK_LEN  28
#define FN_L_SAND       128
#define FN_L_MON        142
#define FN_L_CARD       152
#define FN_L_CARD_LEN   10
#define FN_L_END        (FN_L_CARD + 52)

static const s8 sFnCloud[FN_CLOUDS][2] = {{0, 20}, {10, 40}, {14, 60}, {10, 80}, {0, 98}}; // onder y 130: niet over de onderbalk
static const u8 sFnStrike[3][2] = {{64, 70}, {160, 54}, {112, 104}}; // = FN_STRIKES in legend_intros.py
static const u8 sFnTearRows[15] = {9, 4, 13, 7, 2, 11, 15, 5, 10, 3, 14, 8, 16, 6, 12};
static const u16 sFnAccent[3] = {RGB(8, 28, 12), RGB(12, 18, 31), RGB(31, 18, 4)};
static const u16 sFnCloudTint[3] = {RGB(8, 26, 12), RGB(6, 4, 14), RGB(26, 20, 10)};

static u32 FN_End(struct Task *task)
{
    return task->tFnKind == FN_TORNADUS ? FN_T_END : task->tFnKind == FN_THUNDURUS ? FN_TH_END : FN_L_END;
}

static void RTForces_Init(struct Task *task)
{
    u32 i;
    u16 species = GetMonData(&gEnemyParty[0], MON_DATA_SPECIES);

    switch (species)
    {
    case SPECIES_THUNDURUS_INCARNATE:
    case SPECIES_THUNDURUS_THERIAN:
        task->tFnKind = FN_THUNDURUS;
        break;
    case SPECIES_LANDORUS_INCARNATE:
    case SPECIES_LANDORUS_THERIAN:
        task->tFnKind = FN_LANDORUS;
        break;
    case SPECIES_TORNADUS_INCARNATE:
    case SPECIES_TORNADUS_THERIAN:
        task->tFnKind = FN_TORNADUS;
        break;
    default:
        task->tFnKind = FN_TORNADUS;
        species = SPECIES_TORNADUS_INCARNATE;
        break;
    }
    task->tFnSpecies = species;
    GI_LoadGfx(sLegForces_Tiles, sLegForces_Maps);
    LoadPalette(sLegForces_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    for (i = 0; i < FN_CLOUDS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_MistCloud, 32 * 32 / 2, gBattleAnimSpritePal_MistCloud, FN_TAG_CLOUD, &sGI_Oam32Affine, -40, sFnCloud[i][1] + 16, 1);
    if (task->tFnKind == FN_TORNADUS)
        LI_Make(FN_SPR_TORNADO, gBattleAnimSpriteGfx_Tornado, 64 * 192 / 2, gBattleAnimSpritePal_Tornado, FN_TAG_TORNADO, &sGI_Oam64Affine, 0, 0, 0);
    if (task->tFnKind == FN_THUNDURUS)
        for (i = 0; i < FN_BOLTS; i++)
        {
            LI_Make(FN_SPR_BOLT + i, gBattleAnimSpriteGfx_Lightning, 32 * 160 / 2, gBattleAnimSpritePal_Lightning2, FN_TAG_BOLT, &sGI_Oam32Affine, 0, 0, 0);
            LI_Affine(sLI_Spr[FN_SPR_BOLT + i], 512, 0);
        }
    task->tGiSprite0 = MAX_SPRITES;
    task->tGiShown = 0xFF;
}

static void FN_ShowMon(struct Task *task, s16 x, s16 y)
{
    if (task->tGiSprite0 >= MAX_SPRITES)
        task->tGiSprite0 = GI_MonPic(task->tFnSpecies, x, y);
    GI_Sprite(task->tGiSprite0)->invisible = FALSE;
}

static bool8 RTForces_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, y, frontX, shake = 0, end = FN_End(task);
    u32 keep = GI_SpritePalBit(FN_TAG_CLOUD) | GI_SpritePalBit(FN_TAG_TORNADO) | GI_SpritePalBit(FN_TAG_BOLT);
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    s16 *hofs = (s16 *)gScanlineEffectRegBuffers[0];
    struct Sprite *s, *mon;

    if (task->tGiSprite0 < MAX_SPRITES)
        keep |= 1 << (16 + gSprites[task->tGiSprite0].oam.paletteNum);
    mon = GI_Sprite(task->tGiSprite0);
    GI_ResetPals(keep);
    LoadPalette(sLegForces_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    if (t >= FN_DERAIL)
    {
        pal[16 + FN_ACCENT] = sFnAccent[task->tFnKind];
        if ((t >> 3) & 1)
            pal[16 + FN_LIVE] = RGB(31, 26, 26);
    }
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    if (t == FN_TV)
    {
        GI_KillFieldWindows();
        GI_ShowMap(FN_MAP_TV);
        PlaySE(SE_PC_LOGIN);
    }
    if (t == FN_DERAIL)
    {
        GI_ShowRows(FN_MAP_TV_T + task->tFnKind, 17, 20);
        PlaySE(SE_DING_DONG);
    }

    // het wolkenfront trekt van west naar oost
    frontX = -30 + min(t, FN_DERAIL + 8) * 130 / (FN_DERAIL + 8);
    for (i = 0; i < FN_CLOUDS; i++)
    {
        s = LI_S(i);
        if (t < FN_TV)
            continue;
        s->invisible = FALSE;
        s->x = frontX - sFnCloud[i][0];
        s->y = sFnCloud[i][1] + 8 + Sin(((t + i * 20) * 4) & 0xFF, 2);
        k = 384;
        if (task->tFnKind == FN_TORNADUS && t >= FN_T_TWISTER)
        {
            // de wolken worden de tornado in gezogen
            s32 p = min(t - FN_T_TWISTER, 24);
            s->x += (frontX + 10 - s->x) * p / 24;
            s->y += (76 - s->y) * p / 24;
            k = 384 - p * 12;
            s->invisible = (p >= 24);
        }
        LI_Affine(sLI_Spr[i], k, 0);
    }
    if (t >= FN_DERAIL)
        BlendPalettes(GI_SpritePalBit(FN_TAG_CLOUD), min((t - FN_DERAIL) / 2, 10), sFnCloudTint[task->tFnKind]);

    switch (task->tFnKind)
    {
    case FN_TORNADUS:
        s = LI_S(FN_SPR_TORNADO);
        if (t >= FN_T_TWISTER)
        {
            k = t - FN_T_TWISTER;
            s->invisible = FALSE;
            s->x = 120 + min(k, 40) - 20 + Sin((t * 7) & 0xFF, 6);
            s->y = 76;
            LI_Frame(FN_SPR_TORNADO, FN_TAG_TORNADO, (t >> 2) % 3, 64);
            LI_Affine(sLI_Spr[FN_SPR_TORNADO], min(128 + k * 12, 512), 0);
            if (k == 0)
                PlaySE(SE_M_TWISTER);
            if (k == 30)
                PlaySE(SE_M_GUST);
        }
        if (t == FN_T_WAVE)
            LI_InitWave();
        if (t >= FN_T_WAVE)
        {
            s32 amp = min((t - FN_T_WAVE) / 2, 28);
            for (y = 0; y < DISPLAY_HEIGHT; y++)
                hofs[y] = Sin((y * 5 + t * 12) & 0xFF, amp) + ((y >= 16 && y < 136) ? Sin((y * 2 - t * 9) & 0xFF, amp / 2) : 0);
        }
        // rij voor rij scheurt de kaart weg
        if (t >= FN_T_TEAR && (t - FN_T_TEAR) % 3 == 0 && (t - FN_T_TEAR) / 3 < (s32)ARRAY_COUNT(sFnTearRows))
        {
            // een dichte, donkere tile (de achtergrond van de onderbalk, rechtsonder): BG0 blijft dicht, anders zie je
            // de (zwart gemaakte) kaart en de speler erdoor
            u16 *tilemap = RT_Tilemap();
            y = sFnTearRows[(t - FN_T_TEAR) / 3];
            CpuFill16(sGymIntro_Maps != NULL ? sGymIntro_Maps[19 * 30 + 29] : 0, &tilemap[y * 32], 32 * 2);
            PlaySE(SE_M_RAZOR_WIND);
        }
        if (t >= FN_T_FLY)
        {
            k = t - FN_T_FLY;
            FN_ShowMon(task, 300 - k * 9, 56 + Sin((k * 10) & 0xFF, 8));
            mon = GI_Sprite(task->tGiSprite0);
            mon->x = 300 - k * 9;
            mon->y = 56 + Sin((k * 10) & 0xFF, 8);
            if (k == 8)
                PlayCry_Normal(task->tFnSpecies, 0);
        }
        break;
    case FN_THUNDURUS:
        for (i = 0; i < 3; i++)
        {
            s32 st = FN_TH_STRIKE + i * FN_TH_GAP, sx = sFnStrike[i][0], sy = sFnStrike[i][1], j;
            k = t - st;
            if (k == 0)
            {
                GI_PutRect(FN_MAP_BURNT, (sx - 12) >> 3, (sy - 8) >> 3, 4, 3, (sx - 12) >> 3, (sy - 8) >> 3);
                PlaySE(SE_THUNDER);
            }
            if (k >= 0 && k < 12)
            {
                // de bliksem: drie stukken boven elkaar, van boven naar beneden aan
                for (j = 0; j < FN_BOLTS; j++)
                {
                    s = LI_S(FN_SPR_BOLT + j);
                    s->invisible = (k >= 10);
                    s->x = sx;
                    s->y = sy - 32 - (FN_BOLTS - 1 - j) * 64;
                    LI_Frame(FN_SPR_BOLT + j, FN_TAG_BOLT, (j == FN_BOLTS - 1) ? min(k / 2, 4) : ((k < 6) ? 2 : 3), 16);
                }
                shake = 3;
            }
            GI_Flash(t, st, 6, 14, keep, RGB_WHITE);
        }
        if (t >= FN_TH_MON)
        {
            k = t - FN_TH_MON;
            FN_ShowMon(task, 120, 70);
            mon = GI_Sprite(task->tGiSprite0);
            mon->x = 120 + ((k < 10) ? (s32)(Random() % 5) - 2 : 0);
            if (k == 0)
                PlaySE(SE_THUNDER2);
            if (k == 4)
                PlayCry_Normal(task->tFnSpecies, 0);
            if (k < 12)
                shake = 2;
        }
        GI_Flash(t, FN_TH_MON, 10, 16, keep, RGB(24, 26, 31));
        break;
    case FN_LANDORUS:
        if (t >= FN_L_CRACK - 4 && t < FN_L_CARD)
            shake = (t < FN_L_CRACK + FN_L_CRACK_LEN) ? 2 : 1;
        if (t == FN_L_CRACK)
            PlaySE(SE_M_EARTHQUAKE);
        // de barsten lopen vanuit het midden naar buiten (kolommen)
        if (t >= FN_L_CRACK && t <= FN_L_CRACK + FN_L_CRACK_LEN)
        {
            k = (t - FN_L_CRACK) * 16 / FN_L_CRACK_LEN;
            if (14 - k >= 0)
                GI_PutRect(FN_MAP_CRACKED, 14 - k, 2, 1, 15, 14 - k, 2);
            if (15 + k < 30)
                GI_PutRect(FN_MAP_CRACKED, 15 + k, 2, 1, 15, 15 + k, 2);
            if (k > 0)
            {
                GI_PutRect(FN_MAP_CRACKED, 15 - k, 2, 1, 15, 15 - k, 2);
                if (14 + k < 30)
                    GI_PutRect(FN_MAP_CRACKED, 14 + k, 2, 1, 15, 14 + k, 2);
            }
        }
        // zandstorm: alles kleurt zandkleurig, het beeld golft
        if (t >= FN_L_SAND)
        {
            BlendPalettes(1 << 13, min((t - FN_L_SAND) / 2, 9), RGB(26, 20, 10));
            if (t == FN_L_SAND)
            {
                LI_InitWave();
                PlaySE(SE_M_SANDSTORM);
            }
            k = (t < FN_L_CARD) ? min((t - FN_L_SAND) / 3, 4) : max(4 - (t - FN_L_CARD) / 2, 0);
            for (y = 0; y < DISPLAY_HEIGHT; y++)
                hofs[y] = (y >= 16 && y < 136) ? Sin((y * 9 + t * 21) & 0xFF, k) : 0;
        }
        if (t >= FN_L_MON)
        {
            k = min(t - FN_L_MON, 10);
            FN_ShowMon(task, 64, 92);
            mon = GI_Sprite(task->tGiSprite0);
            mon->y = 88 + (10 - k) * (10 - k);
            if (t == FN_L_MON + 6)
                PlayCry_Normal(task->tFnSpecies, 0);
        }
        // het kaartje schuift van rechts in beeld
        if (t >= FN_L_CARD && t <= FN_L_CARD + FN_L_CARD_LEN)
        {
            s32 dx = 30 - (t - FN_L_CARD) * 15 / FN_L_CARD_LEN;
            GI_PutRect(FN_MAP_CRACKED, 15, 6, 15, 8, 15, 6);
            GI_PutRect(task->tFnSpecies == SPECIES_LANDORUS_THERIAN ? FN_MAP_CARD_T : FN_MAP_CARD_I, 0, 0, 14, 8, dx, 6);
            if (t == FN_L_CARD)
                PlaySE(SE_RG_CARD_FLIPPING);
            if (t == FN_L_CARD + FN_L_CARD_LEN)
                PlaySE(SE_SUCCESS);
        }
        break;
    }

    if (task->tFnKind != FN_TORNADUS || t < FN_T_WAVE)
        GI_Shake(shake);
    else if (shake == 0)
        SetGpuReg(REG_OFFSET_BG0VOFS, LI_ShakeAmp(1 + (t - FN_T_WAVE) / 24) & 0x1FF);
    // een frontsprite die deze frame is gemaakt ook meenemen (anders is hij een frame zwart)
    if (task->tGiSprite0 < MAX_SPRITES && !(keep & (1 << (16 + gSprites[task->tGiSprite0].oam.paletteNum))))
    {
        keep |= 1 << (16 + gSprites[task->tGiSprite0].oam.paletteNum);
        GI_ResetPals(keep);
    }
    GI_FadeWorld(t, FN_TV, keep);
    if (t >= FN_TV && t < FN_TV + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - FN_TV) * 2, RGB_BLACK);
    if (GI_WhiteOut(t, end, keep))
    {
        for (i = 0; i < FN_CLOUDS + 1 + FN_BOLTS; i++)
            LI_S(i)->invisible = TRUE;
        mon->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTForces_Finish(struct Task *task)
{
    GI_Shake(0);
    LI_EndWave();
    LI_DestroySprites();
    GI_DestroyMonPic(task->tGiSprite0);
    task->tGiSprite0 = MAX_SPRITES;
    GI_FreeTag(FN_TAG_CLOUD);
    GI_FreeTag(FN_TAG_TORNADO);
    GI_FreeTag(FN_TAG_BOLT);
    GI_Free();
}

static const struct RouteTransition sRT_LegendForces =
{
    sPikachu_Tileset, 32, sLegForces_Pal + 32, 1, 1, 0, RTForces_Init, RTForces_Update, RTForces_Finish
};

static void Task_LegendForces(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendForces);
}
