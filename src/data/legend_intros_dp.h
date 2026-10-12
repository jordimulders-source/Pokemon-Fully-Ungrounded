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
// Dialga ("The clock in your room was never broken. It was waiting."): de wandklok uit de slaapkamer, op de tijd van
// de echte klok. Hij tikt, gaat dan steeds sneller lopen tot de wijzers een waas zijn, en staat op tel 6 ineens stil
// op twaalf uur. Blauwe kracht (Dialga's kleuren) omringt hem, de klok lost op en wordt een tijdtunnel; de wijzers
// worden erin gezogen. Battle! Dialga/Palkia: 180 bpm = 19,9 frames per tel.
static const u32 sDP_Spiral_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_dp_spiral.4bpp.smol");
static const u32 sDP_Spiral_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_dp_spiral_maps.bin.smol");

#define DIA_TAG_HAND    0x5AD0
#define DIA_TAG_FLAME   0x5AD1
#define DIA_TAG_HALO    0x5AD2
#define DIA_CLOCK_TILES 128
#define DIA_SHOW_AT     6
#define DIA_SHOW        DP_SHOW
#define DIA_RUSH        54    // tel 2,7: de wijzers gaan lopen
#define DIA_STOP        119   // tel 6: stilstand
#define DIA_FADE        139   // tel 7: de klok lost op
#define DIA_WARP        159   // tel 8: tijdtunnel
#define DIA_END         199   // tel 10
#define DIA_FLAMES      10
#define DIA_S_MIN       0
#define DIA_S_HOUR      1
#define DIA_S_HALO      2
#define DIA_S_FLAME     3
#define DIA_DARK        RGB(1, 2, 6)
#define DIA_CX          120
#define DIA_CY          80

// de klokkleuren naar Dialga: licht -> ijsblauw/wit, de rest -> staalblauw
static const u16 sDiaTint[16] = {
    RGB(1, 2, 6), RGB(24, 30, 31), RGB(19, 27, 31), RGB(17, 25, 31), RGB(15, 23, 30), RGB(8, 16, 31),
    RGB(4, 12, 31), RGB(4, 9, 30), RGB(2, 6, 26), RGB(1, 2, 6), RGB(19, 27, 31), RGB(5, 10, 19),
    RGB(8, 13, 24), RGB(3, 5, 12), RGB(29, 31, 31), RGB(0, 0, 0)
};
// Dialga's energie: vonken (index 1-9 van de Electricity-art) en de lichtkring (1-4)
static const u16 sDiaBolt[16] = {
    0, RGB_WHITE, RGB(24, 30, 31), RGB(17, 26, 31), 0, RGB(8, 18, 31), RGB(4, 12, 30), RGB(4, 9, 26), RGB(2, 6, 20),
    RGB(1, 4, 14), 0, 0, 0, 0, 0, 0
};
static const u16 sDiaEnergy[16] = {
    0, RGB(10, 20, 31), RGB(29, 31, 31), RGB(19, 27, 31), RGB(12, 20, 31), RGB(4, 9, 31), RGB(4, 14, 25),
    RGB(2, 6, 19), 0, 0, 0, 0, 0, 0, 0, 0
};
// tunnel: 14 fasen (index 1-14) en de kern (15)
static const u16 sDiaTunnel[14] = {
    RGB(1, 2, 6), RGB(2, 4, 10), RGB(4, 8, 16), RGB(8, 13, 22), RGB(12, 20, 28), RGB(19, 27, 31), RGB(29, 31, 31),
    RGB(19, 27, 31), RGB(8, 16, 31), RGB(4, 9, 24), RGB(2, 6, 16), RGB(1, 4, 11), RGB(1, 2, 8), RGB(1, 2, 6)
};
static const u16 sPalTunnel[14] = {
    RGB(4, 1, 6), RGB(8, 2, 11), RGB(13, 3, 16), RGB(20, 6, 22), RGB(26, 11, 26), RGB(30, 19, 29), RGB(31, 29, 31),
    RGB(30, 21, 28), RGB(27, 12, 24), RGB(20, 7, 21), RGB(13, 4, 16), RGB(8, 2, 11), RGB(5, 1, 8), RGB(4, 1, 6)
};

static u16 sDP_Pal[16];

// tunnelpalet in BG-palet 'pal': de fasen schuiven 'ph' op (draaien/zoomen), kern wit, 'bright' 0-16 naar wit
static void DP_TunnelPal(u32 pal, const u16 *cols, s32 ph, s32 bright)
{
    u32 i;
    sDP_Pal[0] = 0;
    for (i = 0; i < 14; i++)
        sDP_Pal[1 + i] = LI2_Mix(cols[(i + ph) % 14], RGB_WHITE, bright);
    sDP_Pal[15] = RGB_WHITE;
    DP_SetBgPal(pal, sDP_Pal);
}

// minuutwijzer-hoek (graden) op tijd t; de uurwijzer loopt 1/12 mee (en in de waas iets sneller)
static s32 DiaMinute(s32 t, s32 a0)
{
    s32 k;
    if (t < DIA_RUSH)
        return a0 + ((t - DIA_SHOW) / 8) * 6; // tikken
    k = t - DIA_RUSH;
    return a0 + ((DIA_RUSH - DIA_SHOW) / 8) * 6 + k * k * k / 400 + k * 2;
}

static void DiaHand(u32 slot, s32 deg, s32 scale)
{
    struct Sprite *s = LI_S(slot);
    s32 sn, cs;
    deg %= 360;
    if (deg < 0)
        deg += 360;
    sn = Sin2(deg) / 16;
    cs = Cos2(deg) / 16;
    DP_RotScale(s, deg, scale);
    s->x = DIA_CX + ((sn * 24 * scale) >> 16);
    s->y = DIA_CY - ((cs * 24 * scale) >> 16);
}

static void RTDialga_Init(struct Task *task)
{
    u32 i;

    DP_LoadTiles(gWallClock_Gfx, 0);
    DP_LoadTiles(sDP_Spiral_Tiles, DIA_CLOCK_TILES);
    sDP_Maps = DP_LoadMaps(gWallClockView_Tilemap);
    sDP_Maps2 = DP_LoadMaps(sDP_Spiral_Maps);
    CpuFill16(0, RT_Tilemap(), BG_SCREEN_SIZE);
    // de klok: alleen de wijzerplaat (kolom 7-22), de knopjes eromheen weg
    if (sDP_Maps != NULL)
        for (i = 0; i < 32 * 20; i++)
            if ((i % 32) < 7 || (i % 32) > 22 || ((i % 32) >= 21 && i / 32 >= 16))
                sDP_Maps[i] = sDP_Maps[7 * 32 + 1]; // een egaal vak van de achtergrond
    LI_ResetSprites();
    LI_Make(DIA_S_MIN, gWallClockHand_Gfx, 64 * 144 / 2, gWallClockMale_Pal, DIA_TAG_HAND, &sDP_Oam64Affine, DIA_CX, DIA_CY, 2);
    LI_Make(DIA_S_HOUR, gWallClockHand_Gfx, 64 * 144 / 2, gWallClockMale_Pal, DIA_TAG_HAND, &sDP_Oam64Affine, DIA_CX, DIA_CY, 1);
    LI_Frame(DIA_S_HOUR, DIA_TAG_HAND, 1, 64);
    LI_Make(DIA_S_HALO, gBattleAnimSpriteGfx_CircleOfLight, 64 * 64 / 2, sDiaEnergy, DIA_TAG_HALO, &sDP_Oam64AffineBlend, DIA_CX, DIA_CY, 3);
    for (i = 0; i < DIA_FLAMES; i++)
        LI_Make(DIA_S_FLAME + i, gBattleAnimSpriteGfx_Electricity, 32 * 128 / 2, sDiaBolt, DIA_TAG_FLAME, &sGI_Oam32, DIA_CX, DIA_CY, 0);
    // de echte tijd (zoals de klok in je kamer)
    RtcCalcLocalTime();
    sDP_Var[0] = gLocalTime.minutes * 6;
    sDP_Var[1] = (gLocalTime.hours % 12) * 30 + gLocalTime.minutes / 2;
    task->tDpLast = -1;
}

static bool8 RTDialga_Update(struct Task *task)
{
    s32 t = DP_Time(), last = task->tDpLast, i, k, m, h, sc, amp = 0;
    u32 keep, handBit, energyBit;
    u16 clock[16];
    struct Sprite *s;

    task->tDpLast = t;
    if (last < 0)
        DP_Begin(t, DIA_SHOW_AT);
    handBit = GI_SpritePalBit(DIA_TAG_HAND);
    energyBit = GI_SpritePalBit(DIA_TAG_FLAME) | GI_SpritePalBit(DIA_TAG_HALO);
    keep = handBit | energyBit;
    GI_ResetPals(keep);
    DP_FadeWorld(t, 1 << 13 | 1 << 14, keep);
    if (DP_AT(DIA_SHOW))
    {
        DP_HideWorld();
        DP_Put(sDP_Maps, 0, 32, 0, 13);
    }

    // klokpalet: de kamerklok (teal = donker), steeds blauwer, dan weg
    k = 0;
    if (t >= DIA_RUSH)
        k = min((t - DIA_RUSH) * 6 / (DIA_STOP - DIA_RUSH), 6);
    if (t >= DIA_STOP)
        k = min(6 + (t - DIA_STOP) / 2, 16);
    for (i = 0; i < 16; i++)
        clock[i] = (i == 9) ? DIA_DARK : LI2_Mix(gWallClockMale_Pal[i], sDiaTint[i], k);
    if (t >= DIA_FADE)
        for (i = 1; i < 16; i++)
            clock[i] = LI2_Mix(clock[i], DIA_DARK, min((t - DIA_FADE) * 16 / 16, 16));
    clock[0] = 0;
    if (t >= DIA_SHOW)
    {
        DP_SetBgPal(13, clock);
        if (t < DIA_SHOW + 8)
            BlendPalettes((1 << 13) | handBit, 16 - (t - DIA_SHOW) * 2, RGB_BLACK);
    }
    // tunnel
    if (t >= DIA_WARP)
    {
        k = t - DIA_WARP;
        DP_TunnelPal(14, sDiaTunnel, (k * (2 + k / 8)) / 2, DP_Pulse(t, DIA_WARP, 16, 10));
        if (DP_AT(DIA_WARP))
        {
            DP_Put(sDP_Maps2, 0, 30, DIA_CLOCK_TILES, 14);
            DP_StartDma(&REG_BG0HOFS, 1);
        }
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            gScanlineEffectRegBuffers[0][i] = Sin((i * 3 + k * 7) & 0xFF, min(k / 3, 8));
    }

    // wijzers
    m = DiaMinute(t, sDP_Var[0]);
    h = sDP_Var[1] + (m - sDP_Var[0]) / 12 + (t >= DIA_RUSH ? (t - DIA_RUSH) * (t - DIA_RUSH) / 40 : 0);
    sc = 256;
    if (t >= DIA_STOP)
        m = h = 0; // twaalf uur
    if (t >= DIA_FADE)
    {
        // de wijzers worden de tunnel in gezogen: draaien en krimpen
        k = t - DIA_FADE;
        m = -k * k;
        h = -k * k / 2;
        sc = max(256 - k * 7, 16);
    }
    for (i = 0; i < 2; i++)
    {
        s = LI_S(DIA_S_MIN + i);
        s->invisible = t < DIA_SHOW || sc <= 16;
        DiaHand(DIA_S_MIN + i, i ? h : m, sc);
    }
    // tikken: eerst gewoon, dan steeds sneller
    if (t >= DIA_SHOW && t < DIA_RUSH && (t - DIA_SHOW) % 8 == 0 && t != last)
        PlaySE(SE_CLICK);
    if (t >= DIA_RUSH && t < DIA_STOP - 4 && t != last && ((t - DIA_RUSH) % max(8 - (t - DIA_RUSH) / 12, 2)) == 0)
        PlaySE(SE_CLICK);
    if (DP_AT(DIA_STOP))
        PlaySE(SE_M_VICEGRIP);
    if (DP_AT(DIA_STOP + 6))
        PlaySE(SE_M_DETECT);
    if (DP_AT(DIA_FADE))
        PlayCry_Normal(SPECIES_DIALGA, 0);
    if (DP_AT(DIA_WARP))
        PlaySE(SE_M_TELEPORT);

    // blauwe kracht rond de klok: lichtkring (doorschijnend) en vlammen die rond de rand draaien
    s = LI_S(DIA_S_HALO);
    s->invisible = t < DIA_STOP + 2 || t >= DIA_WARP + 6;
    if (!s->invisible)
    {
        k = t - DIA_STOP;
        sc = 400 + Sin((k * 12) & 0xFF, 24) + (t >= DIA_FADE ? (t - DIA_FADE) * 6 : 0);
        LI_Affine(sLI_Spr[DIA_S_HALO], min(sc, 511), 0);
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BD);
        k = min(k / 2, 9);
        if (t >= DIA_FADE)
            k = max(9 - (t - DIA_FADE) / 2, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(k, 16));
    }
    // vonken springen over de rand (elke 3 frames een nieuwe plek), daarna fladderen ze weg
    for (i = 0; i < DIA_FLAMES; i++)
    {
        s32 ang, r;
        s = LI_S(DIA_S_FLAME + i);
        k = t - DIA_STOP - 2 - i * 2;
        s->invisible = k < 0 || t >= DIA_WARP + 8;
        if (s->invisible)
            continue;
        ang = i * 256 / DIA_FLAMES + DP_Hash(i, t / 3, 5) % 24 + t * 2;
        r = 58 + DP_Hash(i, t / 3, 9) % 10;
        if (t >= DIA_FADE)
            r += (t - DIA_FADE) * (t - DIA_FADE) / 6;
        s->x = DIA_CX + Cos(ang & 0xFF, r);
        s->y = DIA_CY + Sin(ang & 0xFF, r);
        LI_Frame(DIA_S_FLAME + i, DIA_TAG_FLAME, (t / 2 + i) & 3, 16);
    }
    energyBit = GI_SpritePalBit(DIA_TAG_FLAME);
    if (t >= DIA_STOP)
        BlendPalettes(energyBit | GI_SpritePalBit(DIA_TAG_HALO), DP_Pulse(t, DIA_STOP + 2, 12, 16), RGB_WHITE);

    // trillen: neemt toe met de snelheid, een klap bij de stilstand
    if (t >= DIA_RUSH && t < DIA_STOP)
        amp = (t - DIA_RUSH) / 30;
    amp = max(amp, DP_Pulse(t, DIA_STOP, 4, 10));
    if (t < DIA_WARP)
        GI_Shake(amp);
    else
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    // flits bij de stilstand en bij de tunnel
    GI_Flash(t, DIA_STOP, 6, 10, (1 << 13) | handBit, RGB_WHITE);
    if (LI2_WhiteOut(t, DIA_END, (1 << 13) | (1 << 14), keep))
        return TRUE;
    return FALSE;
}

static void RTDialga_Finish(struct Task *task)
{
    DP_Finish();
    GI_FreeTag(DIA_TAG_HAND);
    GI_FreeTag(DIA_TAG_FLAME);
    GI_FreeTag(DIA_TAG_HALO);
}

static const struct RouteTransition sRT_LegendDialga =
{
    sPikachu_Tileset, 32, sDP_Black16, 1, 1, 0, RTDialga_Init, RTDialga_Update, RTDialga_Finish
};

static void Task_LegendDialga(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendDialga);
}

// =====================================================================================================================
// Palkia ("Space is just distance that hasn't been folded yet."): op de maat Littleroot, Petalburg, Fortree, Mossdeep,
// Sootopolis (echte kaartuitsneden). Roze/paars kruipt van de randen naar binnen (venster 0 als rafelige ellips per
// beeldlijn, daarbuiten BG0 geblend met de roze achtergrondkleur), lichtbolletjes zweven langs de rand. Dan lopen de
// plekken door elkaar (per vak een andere stad, rijen verschoven), steeds wilder, tot het een brij is. Een paar frames
// heel helder Spear Pillar, dan de ruimtetunnel die in banen uiteenscheurt (Spacial Rend).
static const u32 sDP_Cities_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_dp_cities.4bpp.smol");
static const u32 sDP_Cities_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_dp_cities_maps.bin.smol");
static const u16 sDP_Cities_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_dp_cities.gbapal");

#define PAL_TAG_ORB     0x5AD4
#define PAL_SHOW_AT     8
#define PAL_SHOW        DP_SHOW
#define PAL_MIX         119   // tel 6
#define PAL_CHAOS       139   // tel 7
#define PAL_PILLAR      159   // tel 8
#define PAL_WARP        171
#define PAL_END         199   // tel 10
#define PAL_CITIES      5
#define PAL_MAP_PILLAR  5
#define PAL_BG          (0xFFF << 4)    // BG 4-15 (de steden)
#define PAL_TUNNEL_PAL  3
#define PAL_ORBS        10

static const u8 sPalCut[PAL_CITIES] = {0, 60, 80, 100, 110}; // de eerste meteen, dan tel 3, 4, 5 en 5,5
static const u8 sDP_Semi[33] = {
    255, 255, 255, 255, 254, 253, 251, 250, 248, 246, 243, 240, 237, 234, 230, 226, 222, 217, 212, 206, 200, 193,
    186, 178, 169, 160, 149, 137, 124, 108, 89, 63, 0
};
static const u16 sPalOrb[16] = {
    0, RGB(31, 20, 29), RGB(30, 16, 28), RGB(28, 12, 26), RGB(25, 9, 24), RGB(21, 7, 22), RGB(18, 5, 20),
    RGB(31, 25, 31), RGB(31, 31, 31), 0, 0, 0, 0, RGB(30, 16, 28), RGB(31, 25, 31), 0
};

// rafelige ellips (halve breedte rx, halve hoogte ry) als venster 0
static void PalWindow(s32 t, s32 rx)
{
    u16 *win = gScanlineEffectRegBuffers[0];
    s32 y, ry = rx * 2 / 3, dy, hw, x0, x1;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        dy = abs(y - 80);
        if (ry <= 0 || dy >= ry)
        {
            win[y] = 0;
            continue;
        }
        hw = rx * sDP_Semi[dy * 32 / ry] / 256 + Sin((y * 9 + t * 5) & 0xFF, 5) + Sin((y * 23 - t * 3) & 0xFF, 3);
        x0 = DP_Clamp(120 - hw, 0, 240);
        x1 = DP_Clamp(120 + hw, 0, 240);
        win[y] = x1 > x0 ? WIN_RANGE(x0, x1) : 0;
    }
}

// steden door elkaar: per vak een stad uit 'a'/'b' (kans p/256 op b) of, als chaos, uit alle vijf; rijen verschoven
static void PalMix(u32 a, u32 b, s32 p, bool32 chaos, u32 seed, s32 shift)
{
    u16 *tilemap = RT_Tilemap();
    s32 r, c, sc, city, rs;
    if (sDP_Maps == NULL)
        return;
    for (r = 0; r < 20; r++)
    {
        rs = shift ? (s32)(DP_Hash(r, seed, 7) % (shift * 2 + 1)) - shift : 0;
        for (c = 0; c < 32; c++)
        {
            sc = c + rs;
            sc = ((sc % 30) + 30) % 30;
            if (chaos)
                city = DP_Hash(c / 2, r / 2, seed) % PAL_CITIES;
            else
                city = ((s32)DP_Hash(c / 2 + r, r / 2, seed) < p) ? b : a;
            tilemap[r * 32 + c] = sDP_Maps[city * 600 + r * 30 + sc];
        }
    }
    CpuCopy16(&tilemap[19 * 32], &tilemap[20 * 32], 32 * 2);
    CpuCopy16(&tilemap[0], &tilemap[31 * 32], 32 * 2);
}

static void RTPalkia_Init(struct Task *task)
{
    u32 i;
    DP_LoadTiles(sDP_Cities_Tiles, 0);
    DP_LoadTiles(sDP_Spiral_Tiles, DP_CITIES_TILES);
    sDP_Maps = DP_LoadMaps(sDP_Cities_Maps);
    sDP_Maps2 = DP_LoadMaps(sDP_Spiral_Maps);
    CpuFill16(0, RT_Tilemap(), BG_SCREEN_SIZE);
    LI_ResetSprites();
    for (i = 0; i < PAL_ORBS; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_Orbs, 16 * 48 / 2, sPalOrb, PAL_TAG_ORB, &sDP_Oam8, 0, 0, 0);
        LI_Frame(i, PAL_TAG_ORB, (i * 2) % 7, 1);
    }
    task->tDpLast = -1;
}

static bool8 RTPalkia_Update(struct Task *task)
{
    s32 t = DP_Time(), last = task->tDpLast, i, k, rx = 0, ang, blend = 0;
    u32 keep = GI_SpritePalBit(PAL_TAG_ORB), bg = PAL_BG | (1 << PAL_TUNNEL_PAL);
    u16 pink;
    struct Sprite *s;

    task->tDpLast = t;
    if (last < 0)
        DP_Begin(t, PAL_SHOW_AT);
    GI_ResetPals(keep);
    DP_FadeWorld(t, bg, keep);
    if (t >= PAL_SHOW)
        LoadPalette(sDP_Cities_Pal, BG_PLTT_ID(4), 12 * PLTT_SIZE_4BPP);
    if (t >= PAL_SHOW && t < PAL_SHOW + 6)
        BlendPalettes(PAL_BG, 12 - (t - PAL_SHOW) * 2, RGB_BLACK);
    // achtergrondkleur: Palkia-roze, golvend
    pink = LI2_Mix(RGB(26, 8, 24), RGB(18, 6, 28), 8 + Sin((t * 6) & 0xFF, 8));
    gPlttBufferFaded[0] = gPlttBufferUnfaded[0] = (t >= PAL_SHOW && t < PAL_PILLAR) ? pink : RGB_BLACK;

    if (DP_AT(PAL_SHOW))
    {
        DP_HideWorld();
        DP_StartDma(&REG_WIN0H, 1);
        SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(0, DISPLAY_HEIGHT));
        SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_BG0 | WININ_WIN0_OBJ);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0 | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR);
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BD);
        PalWindow(t, 200);
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
    }
    // de steden op de maat
    for (i = 0; i < PAL_CITIES; i++)
    {
        if (DP_AT(i == 0 ? PAL_SHOW : sPalCut[i]))
        {
            DP_Put(sDP_Maps, i, 30, 0, -1);
            if (i > 0)
                PlaySE(SE_M_TELEPORT);
        }
    }
    // het roze kruipt naar binnen
    if (t >= PAL_SHOW && t < PAL_PILLAR)
    {
        if (t < PAL_MIX)
        {
            rx = 200 - (t - PAL_SHOW) * 120 / (PAL_MIX - PAL_SHOW);
            blend = 4 + (t - PAL_SHOW) * 6 / (PAL_MIX - PAL_SHOW);
        }
        else
        {
            rx = max(80 - (t - PAL_MIX) * 50 / (PAL_PILLAR - PAL_MIX), 30);
            blend = 9 + Sin((t * 16) & 0xFF, 2);
        }
        PalWindow(t, rx);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(16 - blend, blend));
        // flitsje bij elke wissel
        for (i = 1; i < PAL_CITIES; i++)
            if (t >= sPalCut[i] && t < sPalCut[i] + 4)
                BlendPalettes(PAL_BG, 8 - (t - sPalCut[i]) * 2, RGB(31, 24, 31));
        // lichtbolletjes langs de rand van de ellips
        for (i = 0; i < PAL_ORBS; i++)
        {
            s = LI_S(i);
            ang = i * 256 / PAL_ORBS + t * ((i & 1) ? 2 : -3);
            k = min(rx + 12 + Sin((t * 7 + i * 50) & 0xFF, 6), 150);
            s->x = 120 + Cos(ang & 0xFF, k);
            s->y = 80 + Sin(ang & 0xFF, k * 2 / 3);
            s->invisible = (t >= PAL_CHAOS && ((t >> 1) & 3) == (i & 3));
        }
    }
    // door elkaar
    if (t >= PAL_MIX && t < PAL_CHAOS)
    {
        k = t - PAL_MIX;
        i = (k / 6) % PAL_CITIES;
        PalMix(i, (i + 2) % PAL_CITIES, 48 + k * 7, FALSE, k / 3, k / 8);
    }
    else if (t >= PAL_CHAOS && t < PAL_PILLAR)
    {
        PalMix(0, 0, 0, TRUE, t, 3 + (t - PAL_CHAOS) / 6);
        GI_Shake(2 + (t - PAL_CHAOS) / 8);
    }
    // heel helder: Spear Pillar
    if (DP_AT(PAL_PILLAR))
    {
        DP_StopDma();
        ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        GI_Shake(0);
        DP_Put(sDP_Maps, PAL_MAP_PILLAR, 30, 0, -1);
        for (i = 0; i < PAL_ORBS; i++)
            LI_S(i)->invisible = TRUE;
        PlaySE(SE_M_DETECT);
    }
    if (t >= PAL_PILLAR && t < PAL_PILLAR + 4)
        BlendPalettes(PAL_BG, 10 - (t - PAL_PILLAR) * 3, RGB_WHITE);
    // ruimtetunnel die in banen scheurt
    if (t >= PAL_WARP)
    {
        k = t - PAL_WARP;
        DP_TunnelPal(PAL_TUNNEL_PAL, sPalTunnel, 1400 - (k * (2 + k / 8)) / 2, DP_Pulse(t, PAL_WARP, 16, 8));
        if (DP_AT(PAL_WARP))
        {
            DP_Put(sDP_Maps2, 0, 30, DP_CITIES_TILES, PAL_TUNNEL_PAL);
            DP_StartDma(&REG_BG0HOFS, 1);
            PlayCry_Normal(SPECIES_PALKIA, 0);
            PlaySE(SE_M_TELEPORT);
        }
        for (i = 0; i < DISPLAY_HEIGHT; i++)
            gScanlineEffectRegBuffers[0][i] = (((i / 12) & 1) ? 1 : -1) * min(k * k / 6, 60) + Sin((i * 4 + k * 9) & 0xFF, 3);
    }
    if (LI2_WhiteOut(t, PAL_END, bg, keep))
        return TRUE;
    return FALSE;
}

static void RTPalkia_Finish(struct Task *task)
{
    DP_Finish();
    GI_FreeTag(PAL_TAG_ORB);
}

static const struct RouteTransition sRT_LegendPalkia =
{
    sPikachu_Tileset, 32, sDP_Black16, 1, 1, 0, RTPalkia_Init, RTPalkia_Update, RTPalkia_Finish
};

static void Task_LegendPalkia(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendPalkia);
}

// =====================================================================================================================
// Arceus ("Somewhere, a very old Pokémon just found out you exist."): de wereld waar je staat trilt op de eerste twee
// stoten van het nummer, heilig licht kruipt van de randen naar binnen (BG0 additief over de wereld) en de wereld
// vervormt (BG1-3 per beeldlijn, HBlank-DMA op zes registers) tot alles wit-goud is. Op tel 8 verschijnt het teken
// (Jordi's plaatje, 128x128 als vier sprites) in een stralenkrans, op tel 9 slaat het nog eens in, en op tel 15 heel
// dominant: enorm, donkere stralen, flits, dan fade. Battle! Arceus: 150 bpm = 23,9 frames per tel.
static const u32 sDP_Arceus_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_dp_arceus.4bpp.smol");
static const u32 sDP_Arceus_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_dp_arceus_maps.bin.smol");
static const u32 sDP_ArcSym_Gfx[] = INCBIN_U32("graphics/battle_transitions/legend_dp_arceus_sym.4bpp.smol");
static const u16 sDP_ArcSym_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_dp_arceus_sym.gbapal");

enum { ARC_MAP_LIGHT, ARC_MAP_RAYS };
#define ARC_TAG_SYM     0x5AD5
#define ARC_TAG_HALO    0x5AD6
#define ARC_TAG_SPARK   0x5AD7
#define ARC_TAG_STAR    0x5AD8
#define ARC_HIT1        0     // tel 0
#define ARC_HIT2        24    // tel 1
#define ARC_WARP        34
#define ARC_WHITE       186   // alles wit-goud
#define ARC_SYM         191   // tel 8
#define ARC_HIT4        215   // tel 9
#define ARC_HIT4B       221   // tel 9,25
#define ARC_LAST        358   // tel 15
#define ARC_END         382   // tel 16
#define ARC_S_SYM       0     // vier slots
#define ARC_S_HALO      4
#define ARC_S_SPARK     5
#define ARC_SPARKS      8
#define ARC_S_STAR      (ARC_S_SPARK + ARC_SPARKS)
#define ARC_STARS       8
#define ARC_CX          120
#define ARC_CY          80
#define ARC_LIGHT       RGB(31, 30, 22)

static const u16 sArcEcho[] = {48, 72, 96, 239, 263, 287, 311}; // tel 2-4 en 10-13: de stoten galmen na
static const u16 sArcHalo[16] = {0, RGB(31, 29, 20), RGB(31, 27, 14), RGB(30, 23, 10), RGB(26, 18, 6)};
static const u16 sArcGold[16] = {
    0, RGB(31, 31, 26), RGB(31, 30, 20), RGB(31, 27, 12), RGB(31, 31, 31), RGB(29, 24, 9), RGB(31, 29, 16),
    RGB(30, 26, 12), RGB(31, 31, 28), RGB(31, 30, 22), RGB(28, 22, 8), 0, 0, 0, 0, 0
};
static const u8 sArcStarX[ARC_STARS] = {20, 50, 84, 112, 140, 170, 204, 228};
static const u8 sArcStarOfs[ARC_STARS] = {0, 90, 40, 140, 20, 110, 60, 160};

// alle trillingen op de stoten
static s32 ArcShake(s32 t)
{
    s32 i, a = DP_Pulse(t, ARC_HIT1, 4, 16);
    a = max(a, DP_Pulse(t, ARC_HIT2, 5, 18));
    for (i = 0; i < 3; i++)
        a = max(a, DP_Pulse(t, sArcEcho[i], 2, 10));
    if (t >= ARC_WARP && t < ARC_SYM)
        a = max(a, 1);
    a = max(a, DP_Pulse(t, ARC_SYM, 4, 14));
    a = max(a, DP_Pulse(t, ARC_HIT4, 4, 12));
    a = max(a, DP_Pulse(t, ARC_HIT4B, 3, 8));
    a = max(a, DP_Pulse(t, ARC_LAST, 7, 24));
    return a;
}

static void RTArceus_Init(struct Task *task)
{
    u32 i;
    s16 cx, cy;

    DP_LoadTiles(sDP_Arceus_Tiles, 0);
    sDP_Maps = DP_LoadMaps(sDP_Arceus_Maps);
    CpuFill16(0, RT_Tilemap(), BG_SCREEN_SIZE);
    LI_ResetSprites();
    LI2_BigMake(ARC_S_SYM, sDP_ArcSym_Gfx, sDP_ArcSym_Pal, ARC_TAG_SYM, 1);
    LI_Make(ARC_S_HALO, gBattleAnimSpriteGfx_CircleOfLight, 64 * 64 / 2, sArcHalo, ARC_TAG_HALO, &sDP_Oam64AffineBlend, ARC_CX, ARC_CY, 3);
    for (i = 0; i < ARC_SPARKS; i++)
        LI_Make(ARC_S_SPARK + i, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, sArcGold, ARC_TAG_SPARK, &sGI_Oam32, ARC_CX, ARC_CY, 0);
    for (i = 0; i < ARC_STARS; i++)
        LI_Make(ARC_S_STAR + i, gBattleAnimSpriteGfx_GoldStars, 16 * 24 / 2, gBattleAnimSpritePal_GoldStars, ARC_TAG_STAR, &sGI_Oam16, sArcStarX[i], -16, 2);
    // de wereld vervormen: BG1-3 HOFS/VOFS per beeldlijn
    GetCameraOffsetWithPan(&cx, &cy);
    sDP_Var[0] = cx;
    sDP_Var[1] = cy;
    DP_StartDma(&REG_BG1HOFS, 6);
    for (i = 0; i < DISPLAY_HEIGHT * 6; i++)
        gScanlineEffectRegBuffers[0][i] = gScanlineEffectRegBuffers[1][i] = (i & 1) ? cy : cx;
    // het licht telt op bij de wereld
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                               | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(16, 16));
    SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
    DP_Put(sDP_Maps, ARC_MAP_LIGHT, 30, 0, 13);
    task->tDpLast = -1;
}

static bool8 RTArceus_Update(struct Task *task)
{
    s32 t = DP_Time(), last = task->tDpLast, i, k, lvl, amp, sh, scale = 256, rot = 0, white;
    u32 keep, symBit;
    u16 *buf = gScanlineEffectRegBuffers[0];
    u16 pal[16];
    struct Sprite *s;
    bool32 sym = t >= ARC_SYM, dark = t >= ARC_LAST;

    task->tDpLast = t;
    symBit = GI_SpritePalBit(ARC_TAG_SYM);
    keep = symBit | GI_SpritePalBit(ARC_TAG_HALO) | GI_SpritePalBit(ARC_TAG_SPARK) | GI_SpritePalBit(ARC_TAG_STAR);
    GI_ResetPals(keep);
    amp = ArcShake(t);
    sh = LI_ShakeAmp(amp);

    if (!sym)
    {
        // heilig licht: de banden (index 1 = binnen, 15 = hoek) lichten op van buiten naar binnen; pulsen op de stoten
        lvl = 1 + t * 14 / ARC_WHITE + DP_Pulse(t, ARC_HIT1, 6, 20) + DP_Pulse(t, ARC_HIT2, 8, 20);
        for (i = 0; i < 3; i++)
            lvl += DP_Pulse(t, sArcEcho[i], 3, 12);
        pal[0] = 0;
        for (i = 1; i < 16; i++)
        {
            k = DP_Clamp((i + lvl - 15) * 4, 0, 16);
            pal[i] = LI2_Mix(RGB_BLACK, ARC_LIGHT, k);
        }
        DP_SetBgPal(13, pal);
        // de wereld zelf wordt lichter (wit-goud)
        white = DP_Clamp((t - 40) * 16 / (ARC_WHITE - 40), 0, 16);
        white = max(white, DP_Pulse(t, ARC_HIT2, 6, 10));
        BlendPalettes(PALETTES_ALL & ~(keep | (1 << 13) | (1 << 14) | (1 << 15)), white, RGB(31, 30, 24));
        // vervormen
        k = DP_Clamp((t - ARC_WARP) * 24 / (ARC_WHITE - ARC_WARP), 0, 24);
        for (i = 0; i < DISPLAY_HEIGHT; i++)
        {
            s32 hx = sDP_Var[0] + sh + Sin((i * 4 + t * 5) & 0xFF, k) + Sin((i * 11 - t * 3) & 0xFF, k / 3);
            s32 vy = sDP_Var[1] + sh / 2 + Sin((i * 3 - t * 4) & 0xFF, k / 2);
            buf[i * 6 + 0] = buf[i * 6 + 2] = buf[i * 6 + 4] = hx;
            buf[i * 6 + 1] = buf[i * 6 + 3] = buf[i * 6 + 5] = vy;
        }
        GI_Shake(amp / 2);
    }
    if (DP_AT(ARC_SYM))
    {
        // het teken: de wereld weg, stralenkrans
        DP_StopDma();
        DP_HideWorld();
        DP_Put(sDP_Maps, ARC_MAP_RAYS, 30, 0, 14);
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0);
        PlaySE(SE_M_MORNING_SUN);
    }
    if (sym)
    {
        // stralen: lichte banen die rond draaien; op tel 15 donker met gouden stralen
        u16 hi = dark ? RGB(31, 27, 12) : RGB_WHITE, mid = dark ? RGB(10, 7, 3) : RGB(31, 30, 23), lo = dark ? RGB(2, 2, 6) : RGB(31, 27, 17);
        k = t / 2;
        pal[0] = 0;
        for (i = 1; i < 16; i++)
        {
            s32 j = (i + k) % 5;
            pal[i] = j < 2 ? hi : (j == 2 ? mid : lo);
        }
        DP_SetBgPal(14, pal);
        LI2_FillField((1 << 14) | (1 << 13), keep, dark ? RGB(2, 2, 6) : RGB(31, 30, 24));
        GI_Shake(amp);
        // schaal: verschijnen (klein -> groot -> 1x), inslaan, en de laatste keer enorm
        k = t - ARC_SYM;
        if (k < 6)
            scale = 64 + k * 56;
        else if (k < 12)
            scale = 400 - (k - 6) * 24;
        scale += DP_Pulse(t, ARC_HIT4, 90, 10) + DP_Pulse(t, ARC_HIT4B, 40, 8);
        if (t >= ARC_LAST)
            scale = 480 - DP_Pulse(t, ARC_LAST, 160, 6);
        rot = Sin((t * 2) & 0xFF, 3);
        LI2_BigSet(ARC_S_SYM, ARC_CX + sh, ARC_CY + sh / 2 + Sin((t * 3) & 0xFF, 2), scale, rot, TRUE, 0);
        // halo achter het teken
        s = LI_S(ARC_S_HALO);
        s->invisible = FALSE;
        s->x = ARC_CX + sh;
        s->y = ARC_CY;
        LI_Affine(sLI_Spr[ARC_S_HALO], min(scale * 2 + Sin((t * 8) & 0xFF, 20), 511), 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(dark ? 12 : 8, 16));
        // het teken licht op bij elke stoot
        white = max(DP_Pulse(t, ARC_SYM, 16, 14), DP_Pulse(t, ARC_HIT4, 12, 10));
        white = max(white, DP_Pulse(t, ARC_HIT4B, 8, 6));
        white = max(white, DP_Pulse(t, ARC_LAST, 16, 10));
        for (i = 3; i < 7; i++)
            white = max(white, DP_Pulse(t, sArcEcho[i], 5, 8));
        BlendPalettes(symBit, white, RGB_WHITE);
        BlendPalettes(1 << 14, white / 2, RGB_WHITE);
    }
    // vonken: schieten weg bij het verschijnen en de laatste stoot, draaien ertussen rond het teken
    for (i = 0; i < ARC_SPARKS; i++)
    {
        s32 ang = i * 32 + t * 2, r;
        s = LI_S(ARC_S_SPARK + i);
        s->invisible = !sym;
        if (!sym)
            continue;
        k = t - (dark ? ARC_LAST : ARC_SYM);
        r = (k < 20) ? 20 + k * 3 : 80 + Sin((t * 4 + i * 32) & 0xFF, 6);
        if (dark)
            r = 30 + k * 7;
        s->x = ARC_CX + Cos(ang & 0xFF, r);
        s->y = ARC_CY + Sin(ang & 0xFF, r * 3 / 4);
        LI_Frame(ARC_S_SPARK + i, ARC_TAG_SPARK, (t / 3 + i) % 5, 16);
    }
    // gouden sterren dwarrelen omlaag
    for (i = 0; i < ARC_STARS; i++)
    {
        s = LI_S(ARC_S_STAR + i);
        k = t + sArcStarOfs[i];
        s->invisible = !sym;
        s->x = sArcStarX[i] + Sin((k * 4) & 0xFF, 8);
        s->y = ((k * 3 / 2) % 200) - 20;
    }
    // geluid
    if (DP_AT(ARC_HIT2))
        PlaySE(SE_M_SACRED_FIRE2);
    if (DP_AT(ARC_HIT4))
        PlaySE(SE_M_HYPER_BEAM);
    if (DP_AT(ARC_HIT4 + 8))
        PlayCry_Normal(SPECIES_ARCEUS, 0);
    if (DP_AT(ARC_LAST))
        PlaySE(SE_M_HYPER_BEAM2);
    // de fade: alles naar wit
    if (t >= ARC_LAST + 8)
    {
        k = DP_Clamp((t - ARC_LAST - 8) * 16 / (ARC_END - ARC_LAST - 8), 0, 16);
        BlendPalettes(keep | (1 << 14), k, RGB_WHITE);
        LI2_FillField(1 << 14, keep, LI2_Mix(RGB(2, 2, 6), RGB_WHITE, k));
    }
    if (t >= ARC_END)
    {
        for (i = 0; i <= ARC_S_STAR + ARC_STARS - 1; i++)
            LI_S(i)->invisible = TRUE;
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        LI2_FillField(0, 0, RGB_WHITE);
        return TRUE;
    }
    return FALSE;
}

static void RTArceus_Finish(struct Task *task)
{
    DP_Finish();
    GI_FreeTag(ARC_TAG_SYM);
    GI_FreeTag(ARC_TAG_HALO);
    GI_FreeTag(ARC_TAG_SPARK);
    GI_FreeTag(ARC_TAG_STAR);
}

static const struct RouteTransition sRT_LegendArceus =
{
    sPikachu_Tileset, 32, sDP_Black16, 1, 1, 0, RTArceus_Init, RTArceus_Update, RTArceus_Finish
};

static void Task_LegendArceus(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendArceus);
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
