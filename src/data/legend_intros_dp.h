// Project Grounded: gevechtsintro's van Dialga, Palkia, Arceus en Mew. Wordt onderaan src/battle_transition.c
// ingevoegd, na src/data/legend_intros2.h (gebruikt de GI_/LI_/LI2_-hulpjes, de route-transitie-runner en
// Tapu_Elapsed). Art: tools/grounded/legend_intros_dp.py. Alle vier lopen op de maat van hun muziek: de tijd is het
// aantal VBlanks sinds de muziek startte (CreateBattleStartTask start hem een frame vóór de transitie), zodat
// vertraagde frames de sync niet breken.
// - Dialga: de wandklok uit je slaapkamer (de echte, gWallClock_*), de wijzers gaan steeds sneller, staan op de tel
//   ineens stil, blauwe kracht omringt de klok, hij lost op, tijdtunnel.
// - Palkia: Littleroot, Petalburg, Fortree, Mossdeep, Sootopolis op de maat, roze kruipt van de randen naar binnen,
//   de plekken lopen door elkaar tot er geen touw meer aan vast te knopen is, even helder Spear Pillar, ruimtetunnel.
// - Arceus: de wereld trilt in heilig licht, vervormt, het teken verschijnt en slaat nog twee keer in op de stoten
//   in de intro van het nummer; de laatste keer enorm, dan fade.
// - Mew: Guyana bij zonsopgang (tepui met waterval, regenwoud, rivier, nevel) in parallax, een roze glinstering
//   schiet door het woud, en vlak voor het gevecht zwiept Mews staart door beeld.

#include "legend_intros_dp_gen.h"
#include "rtc.h"

extern const u32 gWallClockHand_Gfx[];

#define DP_TIME_OFS     1     // muziekstart -> transitiestart
#define tDpLast         data[12]

static EWRAM_DATA u16 *sDP_Maps = NULL;
static EWRAM_DATA u16 *sDP_Maps2 = NULL;
static EWRAM_DATA vu16 *sDP_DmaReg = NULL;
static EWRAM_DATA u8 sDP_DmaCount = 0;
static EWRAM_DATA s16 sDP_Var[8] = {0};

static const u16 sDP_Black16[16] = {0};

static const struct OamData sDP_Oam64Affine =
{
    .affineMode = ST_OAM_AFFINE_NORMAL,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct OamData sDP_Oam8 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(8x8),
    .size = SPRITE_SIZE(8x8),
    .priority = 0,
};

static const struct OamData sDP_Oam32x16Blend =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_BLEND,
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 0,
};

static const struct OamData sDP_Oam64AffineBlend =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .objMode = ST_OAM_OBJ_BLEND,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static u32 DP_Hash(u32 a, u32 b, u32 c)
{
    return ((a * 73 + b * 151 + c * 233 + 17) * 2654435761u) >> 24;
}

// tijd in VBlanks sinds de muziek startte
static s32 DP_Time(void)
{
    return Tapu_Elapsed() + DP_TIME_OFS;
}

// TRUE op het eerste frame op of na x (ook als er frames vertraagd waren)
#define DP_AT(x) (last < (x) && t >= (x))

// de eerste update: de wereld vervaagt vanaf hier (de standaardflits ervoor duurt een tel), het beeld komt op
// 'nominal' of zes frames na de start
static void DP_Begin(s32 t, s32 nominal)
{
    sDP_Var[6] = t;
    sDP_Var[7] = max(nominal, t + 6);
}

#define DP_SHOW (sDP_Var[7])

static void DP_FadeWorld(s32 t, u32 bg, u32 keep)
{
    s32 t0 = sDP_Var[6], show = sDP_Var[7];
    if (t < show)
        BlendPalettes(PALETTES_ALL & ~keep, min((t - t0 + 1) * 16 / (show - t0), 16), RGB_BLACK);
    else
        LI2_FillField(bg, keep, RGB_BLACK);
}

static u16 *DP_LoadMaps(const u32 *src)
{
    u16 *p = Alloc(GetDecompressedDataSize(src));
    if (p != NULL)
        DecompressDataWithHeaderWram(src, p);
    return p;
}

static void DP_LoadTiles(const u32 *src, u32 firstTile)
{
    u16 *tilemap, *tileset;
    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(src, tileset + firstTile * 16);
}

static void DP_FreeMaps(void)
{
    TRY_FREE_AND_SET_NULL(sDP_Maps);
    TRY_FREE_AND_SET_NULL(sDP_Maps2);
}

// beeld n (breedte w vakken, 20 rijen) op BG0; tile + ofs, palet vervangen als pal >= 0. Kolom 30/31 en rij 20/31
// krijgen een kopie van de rand (voor het trillen)
static void DP_Put(const u16 *maps, u32 n, u32 w, u32 ofs, s32 pal)
{
    u16 *tilemap = RT_Tilemap();
    const u16 *map;
    u32 r, c, v;

    if (maps == NULL)
        return;
    map = &maps[n * w * 20];
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 32; c++)
        {
            v = map[r * w + (c < w ? c : (c == 30 ? w - 1 : 0))];
            if (v != 0)
            {
                v += ofs;
                if (pal >= 0)
                    v = (v & 0x0FFF) | (pal << 12);
            }
            tilemap[r * 32 + c] = v;
        }
    }
    CpuCopy16(&tilemap[19 * 32], &tilemap[20 * 32], 32 * 2);
    CpuCopy16(&tilemap[0], &tilemap[31 * 32], 32 * 2);
}

// ---------------- HBlank-DMA: per beeldlijn 'count' halfwoorden naar opeenvolgende registers vanaf 'reg'.
// gScanlineEffectRegBuffers[0] vullen; de VBlank kopieert naar [1], zet lijn 0 meteen en de DMA doet de rest.
static void VBlankCB_DP(void)
{
    u32 i, n = sDP_DmaCount;
    DmaStop(0);
    VBlankCB_BattleTransition();
    if (sDP_DmaReg != NULL)
    {
        DmaCopy16(3, gScanlineEffectRegBuffers[0], gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2 * n);
        for (i = 0; i < n; i++)
            sDP_DmaReg[i] = gScanlineEffectRegBuffers[1][i];
        if (n == 1)
            DmaSet(0, &gScanlineEffectRegBuffers[1][1], sDP_DmaReg, B_TRANS_DMA_FLAGS);
        else
            DmaSet(0, &gScanlineEffectRegBuffers[1][n], sDP_DmaReg,
                   n | ((DMA_SRC_INC | DMA_DEST_RELOAD | DMA_REPEAT | DMA_16BIT | DMA_START_HBLANK | DMA_ENABLE) << 16));
    }
}

static void DP_StartDma(vu16 *reg, u32 count)
{
    if (sDP_DmaReg == NULL)
    {
        ScanlineEffect_Clear();
        CpuFill16(0, gScanlineEffectRegBuffers[0], DISPLAY_HEIGHT * 2 * count);
        CpuFill16(0, gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2 * count);
    }
    sDP_DmaCount = count;
    sDP_DmaReg = reg;
    SetVBlankCallback(VBlankCB_DP);
}

static void DP_StopDma(void)
{
    sDP_DmaReg = NULL;
    DmaStop(0);
}

static void DP_EndDma(void)
{
    DP_StopDma();
    SetVBlankCallback(VBlankCB_BattleTransition);
}

static void DP_HideWorld(void)
{
    GI_KillFieldWindows();
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG1_ON | DISPCNT_BG2_ON | DISPCNT_BG3_ON);
}

static void DP_ShowWorld(void)
{
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG1_ON | DISPCNT_BG2_ON | DISPCNT_BG3_ON);
}

static void DP_Finish(void)
{
    DP_EndDma();
    GI_Shake(0);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    LI_DestroySprites();
    DP_FreeMaps();
    DP_ShowWorld();
}

static void DP_SetBgPal(u32 pal, const u16 *cols)
{
    CpuCopy16(cols, &gPlttBufferUnfaded[BG_PLTT_ID(pal)], PLTT_SIZE_4BPP);
    CpuCopy16(cols, &gPlttBufferFaded[BG_PLTT_ID(pal)], PLTT_SIZE_4BPP);
}

static s32 DP_Clamp(s32 v, s32 lo, s32 hi)
{
    return v < lo ? lo : (v > hi ? hi : v);
}

// een puls die op 'at' begint met 'amp' en in 'len' frames uitdooft
static s32 DP_Pulse(s32 t, s32 at, s32 amp, s32 len)
{
    if (t < at || t >= at + len)
        return 0;
    return amp - (t - at) * amp / len;
}

// affine sprite (NORMAL, 64x64) draaien (graden, met de klok mee) en schalen (256 = 1x)
static void DP_RotScale(struct Sprite *s, s32 deg, s32 scale)
{
    s32 sn, cs, inv;
    deg %= 360;
    if (deg < 0)
        deg += 360;
    sn = Sin2(deg) / 16;
    cs = Cos2(deg) / 16;
    inv = 65536 / max(scale, 16);
    SetOamMatrix(s->oam.matrixNum, cs * inv >> 8, sn * inv >> 8, -sn * inv >> 8, cs * inv >> 8);
}

// =====================================================================================================================
// Mew ("Discovered in Guyana. Officially. Unofficially, it discovered us."): Guyana bij zonsopgang. Een tepui met een
// waterval in de nevel, regenwoud, een rivier; de lagen schuiven elk met hun eigen snelheid (BG0HOFS per beeldlijn).
// Nevelslierten drijven langs (doorschijnende sprites). Een roze glinstering schiet door het woud (Mew, zoals hij in
// de verhalen altijd net uit beeld is), twinkelt op tel 4, en vlak voor het gevecht zwiept Mews echte staart (uit zijn
// frontsprite) door beeld. Battle! Mew: 128 bpm = 28 frames per tel.
static const u32 sDP_Mew_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_dp_mew.4bpp.smol");
static const u32 sDP_Mew_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_dp_mew_maps.bin.smol");
static const u16 sDP_Mew_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_dp_mew.gbapal");
static const u32 sDP_MewTail_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_dp_mew_tail.4bpp.smol");
static const u16 sDP_MewTail_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_dp_mew_tail.gbapal");

#define MEW_TAG_MIST    0x5AD9
#define MEW_TAG_GLINT   0x5ADA
#define MEW_TAG_TAIL    0x5ADB
#define MEW_SHOW_AT     8
#define MEW_SHOW        DP_SHOW
#define MEW_GLINT       40
#define MEW_TWINKLE     112   // tel 4
#define MEW_GLINT_END   150
#define MEW_TAIL        176
#define MEW_TAIL_LEN    34
#define MEW_END         224   // tel 8
#define MEW_NPALS       (16 - DP_MEW_PAL0)
#define MEW_BG          (((1 << MEW_NPALS) - 1) << DP_MEW_PAL0)
#define MEW_S_TAIL      0
#define MEW_S_GLINT     1
#define MEW_S_MIST      2
#define MEW_MISTS       6

static const u16 sMewGlint[16] = {
    0, RGB(31, 22, 29), RGB(31, 19, 27), RGB(31, 25, 30), RGB(30, 17, 26), 0, RGB(31, 28, 31), RGB(31, 24, 30),
    RGB(31, 31, 31), RGB(31, 26, 30), RGB(31, 31, 31), 0, 0, 0, 0, 0
};
static const u16 sMewMist[16] = {0, 0, 0, 0, 0, 0, 0, 0, RGB(28, 29, 28)};
static const u8 sMewMistY[MEW_MISTS] = {74, 84, 96, 112, 70, 102};
static const u8 sMewMistOfs[MEW_MISTS] = {0, 70, 150, 30, 200, 110};
// parallax: 1/16 px per frame per laag (lucht + tepui's, ver woud, rivier, dichtbij)
static const u8 sMewSpeed[4] = {3, 7, 11, 19};

static void RTMew_Init(struct Task *task)
{
    u32 i;
    DP_LoadTiles(sDP_Mew_Tiles, 0);
    sDP_Maps = DP_LoadMaps(sDP_Mew_Maps);
    CpuFill16(0, RT_Tilemap(), BG_SCREEN_SIZE);
    LI_ResetSprites();
    LI_Make(MEW_S_TAIL, sDP_MewTail_Gfx, 64 * 64 / 2, sDP_MewTail_Pal, MEW_TAG_TAIL, &sGI_Oam64Affine, 0, 0, 0);
    LI_Make(MEW_S_GLINT, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, sMewGlint, MEW_TAG_GLINT, &sGI_Oam32, 0, 0, 1);
    for (i = 0; i < MEW_MISTS; i++)
    {
        LI_Make(MEW_S_MIST + i, gBattleAnimSpriteGfx_MistCloud, 32 * 32 / 2, sMewMist, MEW_TAG_MIST, &sDP_Oam32x16Blend, 0, sMewMistY[i], 2);
        LI_Frame(MEW_S_MIST + i, MEW_TAG_MIST, i & 1, 8);
    }
    task->tDpLast = -1;
}

static bool8 RTMew_Update(struct Task *task)
{
    s32 t = DP_Time(), last = task->tDpLast, i, k, y, band, x, scale, rot, px, py;
    u32 keep = GI_SpritePalBit(MEW_TAG_MIST) | GI_SpritePalBit(MEW_TAG_GLINT) | GI_SpritePalBit(MEW_TAG_TAIL);
    u16 *buf = gScanlineEffectRegBuffers[0];
    struct Sprite *s;

    task->tDpLast = t;
    if (last < 0)
        DP_Begin(t, MEW_SHOW_AT);
    GI_ResetPals(keep);
    DP_FadeWorld(t, MEW_BG, keep);
    if (t >= MEW_SHOW)
    {
        u16 *u = &gPlttBufferUnfaded[BG_PLTT_ID(DP_MEW_PAL0)];
        u16 fall[3];
        LoadPalette(sDP_Mew_Pal, BG_PLTT_ID(DP_MEW_PAL0), MEW_NPALS * PLTT_SIZE_4BPP);
        // de waterval: index 1-3 van elk palet gaan rond
        for (i = 0; i < 3; i++)
            fall[i] = u[1 + (i + t / 4) % 3];
        for (k = 0; k < MEW_NPALS; k++)
            for (i = 0; i < 3; i++)
                u[k * 16 + 1 + i] = gPlttBufferFaded[BG_PLTT_ID(DP_MEW_PAL0) + k * 16 + 1 + i] = fall[i];
        if (t < MEW_SHOW + 10)
            BlendPalettes(MEW_BG | GI_SpritePalBit(MEW_TAG_MIST), 16 - (t - MEW_SHOW) * 16 / 10, RGB_BLACK);
    }
    if (DP_AT(MEW_SHOW))
    {
        DP_HideWorld();
        DP_Put(sDP_Maps, 0, 32, 0, -1);
        DP_StartDma(&REG_BG0HOFS, 1);
        // nevel doorschijnend over het beeld
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(6, 12));
    }
    // parallax
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        band = y < DP_MEW_BAND1 ? 0 : (y < DP_MEW_BAND2 ? 1 : (y < DP_MEW_BAND3 ? 2 : 3));
        buf[y] = (t * sMewSpeed[band]) >> 4;
    }
    // nevel
    for (i = 0; i < MEW_MISTS; i++)
    {
        s = LI_S(MEW_S_MIST + i);
        s->invisible = t < MEW_SHOW;
        x = (sMewMistOfs[i] + t * (2 + (i & 1)) / 4) % 300;
        s->x = 270 - x;
        s->y = sMewMistY[i] + Sin((t * 2 + i * 40) & 0xFF, 2);
    }
    // de glinstering: een roze lichtje schiet in bogen door het woud, twinkelt op tel 4 en verdwijnt
    s = LI_S(MEW_S_GLINT);
    s->invisible = t < MEW_GLINT || t >= MEW_GLINT_END;
    if (!s->invisible)
    {
        s32 stop = MEW_TWINKLE - MEW_GLINT, sx = 250 - stop * 3, sy = 100 + Sin((stop * 7) & 0xFF, 22);
        k = t - MEW_GLINT;
        if (k <= stop)
        {
            s->x = 250 - k * 3;
            s->y = 100 + Sin((k * 7) & 0xFF, 22);
        }
        else
        {
            k = max(k - stop - 14, 0); // twinkelen, dan weg naar linksboven
            s->x = sx - k * 5;
            s->y = sy - k * 3;
        }
        LI_Frame(MEW_S_GLINT, MEW_TAG_GLINT, (t >= MEW_TWINKLE && t < MEW_TWINKLE + 14) ? (t / 2) % 5 : (t / 4) % 2, 16);
    }
    if (DP_AT(MEW_TWINKLE))
        PlaySE(SE_SHINY);
    // de staart: zwiept van rechtsonder naar linksboven door beeld (draaipunt = de staartbasis)
    s = LI_S(MEW_S_TAIL);
    k = t - MEW_TAIL;
    s->invisible = k < 0 || k >= MEW_TAIL_LEN;
    if (!s->invisible)
    {
        s32 c, sn, bx, by;
        px = 250 - k * 9;
        py = 175 - k * 7 + (k * k) / 7;
        rot = (-24 + k * 5) & 0xFF;          // tegen de klok in (0-255)
        scale = 512;
        c = Cos(rot, 256);
        sn = Sin(rot, 256);
        bx = (DP_MEW_TAIL_BX * c + DP_MEW_TAIL_BY * sn) >> 8;
        by = (-DP_MEW_TAIL_BX * sn + DP_MEW_TAIL_BY * c) >> 8;
        s->x = px - bx * scale / 256;
        s->y = py - by * scale / 256;
        LI_Affine(sLI_Spr[MEW_S_TAIL], scale, (u16)(rot << 8));
    }
    if (DP_AT(MEW_TAIL + 4))
        PlaySE(SE_M_TAIL_WHIP);
    if (DP_AT(MEW_TAIL + 14))
        PlayCry_Normal(SPECIES_MEW, 0);
    if (LI2_WhiteOut(t, MEW_END, MEW_BG, keep))
    {
        for (i = 0; i < MEW_S_MIST + MEW_MISTS; i++)
            LI_S(i)->invisible = TRUE;
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        return TRUE;
    }
    return FALSE;
}

static void RTMew_Finish(struct Task *task)
{
    DP_Finish();
    GI_FreeTag(MEW_TAG_MIST);
    GI_FreeTag(MEW_TAG_GLINT);
    GI_FreeTag(MEW_TAG_TAIL);
}

static const struct RouteTransition sRT_LegendMew =
{
    sPikachu_Tileset, 32, sDP_Black16, 1, 1, 0, RTMew_Init, RTMew_Update, RTMew_Finish
};

static void Task_LegendMew(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendMew);
}

#undef tDpLast
#undef DP_AT
