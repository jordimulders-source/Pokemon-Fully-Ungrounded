// Project Grounded: goedkope legendary-intro's (Jordi: "maak deze intro's goedkoop qua kbs"). Geen nieuwe graphics:
// alles is code (paletrekenwerk, scroll/vensters per beeldlijn, tiles die tijdens het spelen worden getekend) plus
// gevechtsanimatie-art en item-iconen die al in de ROM staan.
//   Swords of Justice + Keldeo  het scherm wordt door onzichtbare zwaarden in vieren gesneden, de stukken vliegen uiteen
//   Ultra Beasts                interdimensionale storing, dan een Ultra Wormhole
//   paradox-Pokémon             de wereld flikkert tussen verleden en toekomst, kiest er een en duikt erin
//   Eternatus                   rode hemel, Dynamax-energie, de grond scheurt open
//   Marshadow                   een schaduw kruipt het beeld in en neemt het over
//   Terapagos                   ronddraaiende Tera-kristallen in regenboogglans
//   Pecharunt                   paarse gifnevel, pecha-bessen, gifbellen en ketens
// Wordt onderaan src/battle_transition.c ingevoegd, na legend_intros.h (gebruikt GI_-, LI_- en Tapu_-hulpjes).
// Timing: alles telt op echte VBlanks vanaf de start van de transitie (= start van de muziek, Tapu_Elapsed), en de
// klappen vallen op de tel van het gevechtsthema (LC1_Beat).

#include "item_icon.h"
#include "constants/items.h"

#define LC1_MAX_TILES 760   // BG0: blok 2 + de onderste helft van blok 3 (de schermen staan vanaf 0xE000)
#define LC1_FX(bpm) (3600 * 256 / (bpm)) // frames per tel x 256
#define LC1_TEMPO_LEGENDARY LC1_FX(176)   // MUS_GROUNDED_VS_LEGENDARY
#define LC1_TEMPO_UB        LC1_FX(168)   // MUS_GROUNDED_VS_ULTRA_BEAST
#define LC1_TEMPO_AREA_ZERO LC1_FX(120)   // MUS_GROUNDED_VS_AREA_ZERO

enum { LCB_HOFS, LCB_VOFS, LCB_WIN0, LCB_WIN1, LCB_COLOR, LC1_NBUF };
#define LCF_HOFS  (1 << LCB_HOFS)   // BG1-3 HOFS per beeldlijn (de kaartlagen)
#define LCF_VOFS  (1 << LCB_VOFS)   // BG1-3 VOFS per beeldlijn
#define LCF_WIN0  (1 << LCB_WIN0)   // WIN0H per beeldlijn
#define LCF_WIN1  (1 << LCB_WIN1)   // WIN1H per beeldlijn
#define LCF_COLOR (1 << LCB_COLOR)  // één paletkleur per beeldlijn (verloop)

struct LegendCheap1
{
    u16 front[LC1_NBUF][DISPLAY_HEIGHT]; // wat de HBlank nu leest
    u16 back[LC1_NBUF][DISPLAY_HEIGHT];  // wat de taak schrijft (VBlank kopieert)
    u16 *bg0map, *bg0tiles;
    u8 *snap;                           // Swords: 8bpp-schermafdruk van de wereld (30x20 tiles)
    s32 start, last, beat0;
    u32 rng;
    u16 beatFx, nextTile, reserved;
    u16 lineFlags, colorIdx;
    u16 winin, winout, win0v, win1v, bldcnt, bldalpha, bldy;
    bool8 regs;                         // vensters/blend in de VBlank zetten
    u8 variant;
    u16 species;
    s16 v[16];                          // vrij per intro
    void (*vblank)(void);               // extra werk in de VBlank (na de rest)
};

static EWRAM_DATA struct LegendCheap1 *sLC1 = NULL;

struct LCIntro
{
    u16 beatFx;
    void (*init)(void);
    bool32 (*update)(s32 t);
    void (*finish)(void);
};

// ---------------------------------------------------------------------------------------------------------------------
// gedeelde hulpjes

static inline void LC1_ApplyLine(struct LegendCheap1 *lc, u32 y)
{
    u32 f = lc->lineFlags;
    if (f & LCF_HOFS)
    {
        u16 v = lc->front[LCB_HOFS][y];
        REG_BG1HOFS = v;
        REG_BG2HOFS = v;
        REG_BG3HOFS = v;
    }
    if (f & LCF_VOFS)
    {
        u16 v = lc->front[LCB_VOFS][y];
        REG_BG1VOFS = v;
        REG_BG2VOFS = v;
        REG_BG3VOFS = v;
    }
    if (f & LCF_WIN0)
        REG_WIN0H = lc->front[LCB_WIN0][y];
    if (f & LCF_WIN1)
        REG_WIN1H = lc->front[LCB_WIN1][y];
    if (f & LCF_COLOR)
        ((vu16 *)PLTT)[lc->colorIdx] = lc->front[LCB_COLOR][y];
}

static void HBlankCB_LC(void)
{
    u32 y = REG_VCOUNT + 1;
    if (y < DISPLAY_HEIGHT && sLC1 != NULL)
        LC1_ApplyLine(sLC1, y);
}

static void VBlankCB_LC(void)
{
    struct LegendCheap1 *lc = sLC1;
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
    if (lc == NULL)
        return;
    if (lc->lineFlags)
    {
        DmaCopy16(3, lc->back, lc->front, sizeof(lc->front));
        LC1_ApplyLine(lc, 0);
    }
    if (lc->regs)
    {
        REG_WININ = lc->winin;
        REG_WINOUT = lc->winout;
        REG_WIN0V = lc->win0v;
        REG_WIN1V = lc->win1v;
        REG_BLDCNT = lc->bldcnt;
        REG_BLDALPHA = lc->bldalpha;
        REG_BLDY = lc->bldy;
    }
    if (lc->vblank != NULL)
        lc->vblank();
}

// alleen de vensters die de intro zelf gebruikt aan
static void LC1_SetWindows(u16 bits)
{
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, bits);
}

static void LC1_StartLines(u16 flags)
{
    u32 y;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        sLC1->back[LCB_HOFS][y] = sLC1->front[LCB_HOFS][y] = sTransitionData->cameraX;
        sLC1->back[LCB_VOFS][y] = sLC1->front[LCB_VOFS][y] = sTransitionData->cameraY;
    }
    sLC1->lineFlags = flags;
    SetHBlankCallback(HBlankCB_LC);
    EnableInterrupts(INTR_FLAG_HBLANK);
    SetGpuRegBits(REG_OFFSET_DISPSTAT, DISPSTAT_HBLANK_INTR);
}

// vensters + blend aanzetten (de VBlank schrijft ze elke frame). De kaart heeft WIN0/WIN1 aan (alles zichtbaar,
// zonder blend): zonder eigen vensters LC1_ALL_VISIBLE meegeven
#define LC1_WININ_ALL (WININ_WIN0_ALL | WININ_WIN1_ALL)
static void LC1_UseRegs(u16 winin, u16 winout, u16 bldcnt)
{
    sLC1->regs = TRUE;
    sLC1->winin = winin;
    sLC1->winout = winout;
    sLC1->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);
    sLC1->win1v = WIN_RANGE(0, DISPLAY_HEIGHT);
    sLC1->bldcnt = bldcnt;
}

static u32 LC1_Rand(void)
{
    sLC1->rng = sLC1->rng * 1103515245 + 12345;
    return sLC1->rng >> 16;
}

// frame (relatief aan de start van de intro) van de n-de tel na de start
static s32 LC1_Beat(u32 n)
{
    return (s32)(((sLC1->beat0 + n) * sLC1->beatFx) >> 8) - sLC1->start;
}

// halve tellen: n2 = 2 * tel
static s32 LC1_Beat2(u32 n2)
{
    return (s32)(((sLC1->beat0 * 2 + n2) * sLC1->beatFx) >> 9) - sLC1->start;
}

#define LC1_AT(x) (sLC1->last < (x) && t >= (x))
#define LC1_WORLD_BG 0x1FFF   // de paletten van de kaart (BG 0-12)

static u32 LC1_WorldMask(u32 keep)
{
    return (LC1_WORLD_BG | 0xFFFF0000) & ~keep;
}

// kleur in het getoonde palet naar 'to' mengen (op de huidige faded kleuren, zodat effecten te stapelen zijn)
static void LC1_TintFaded(u32 mask, s32 k, u16 to)
{
    u32 i, j;
    if (k <= 0)
        return;
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        for (j = 0; j < 16; j++)
            gPlttBufferFaded[i * 16 + j] = Tapu_Blend(gPlttBufferFaded[i * 16 + j], to, k);
    }
}

static s32 LC1_Lum(u16 c)
{
    return ((c & 31) * 77 + ((c >> 5) & 31) * 150 + ((c >> 10) & 31) * 29) >> 8;
}

enum { LCP_SEPIA, LCP_FUTURE, LCP_INVERT, LCP_GRAY };

static u16 LC1_Filter(u16 c, u32 mode)
{
    s32 l = LC1_Lum(c);
    switch (mode)
    {
    case LCP_SEPIA:
        return RGB(min(31, l + 5), min(31, l + 2), max(0, l - 4));
    case LCP_FUTURE:
        return RGB(l / 4, min(31, l * 7 / 8 + 3), min(31, l + 6));
    case LCP_INVERT:
        return c ^ 0x7FFF;
    default:
        return RGB(l, l, l);
    }
}

// de wereld (unfaded) door een filter, sterkte k (0-16), in het getoonde palet
static void LC1_WorldFilter(u32 mode, s32 k, u32 keep)
{
    u32 i, j, mask = LC1_WorldMask(keep);
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        for (j = 0; j < 16; j++)
        {
            u16 c = gPlttBufferUnfaded[i * 16 + j];
            gPlttBufferFaded[i * 16 + j] = Tapu_Blend(c, LC1_Filter(c, mode), k);
        }
    }
}

// de wereld terug naar unfaded (de sprites in keep laat hij met rust)
static void LC1_WorldReset(u32 keep)
{
    u32 i, mask = LC1_WorldMask(keep) | GI_BG_PALS;
    for (i = 0; i < 32; i++)
        if ((mask >> i) & 1)
            CpuCopy16(&gPlttBufferUnfaded[i * 16], &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
}

// ---------------- BG0 als tekenvel: tiles worden pas aangemaakt waar getekend wordt (palet 15)
static void LC1_Bg0Init(void)
{
    GetBg0TilesDst(&sLC1->bg0map, &sLC1->bg0tiles);
    CpuFill16(0, sLC1->bg0map, BG_SCREEN_SIZE);
    CpuFill16(0, sLC1->bg0tiles, 32);
    sLC1->nextTile = 1;
    sLC1->reserved = 1;
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
}

// een vaste tile (patroon of effen kleur) die op meerdere plekken in de tilemap kan staan; vóór het tekenen aanmaken
static u32 LC1_NewTile(void)
{
    u32 n = sLC1->nextTile++;
    CpuFill16(0, &sLC1->bg0tiles[n * 16], 32);
    sLC1->reserved = sLC1->nextTile;
    return n;
}

static void LC1_SolidTile(u32 n, u32 c)
{
    CpuFill32(c * 0x11111111, &sLC1->bg0tiles[n * 16], 32);
}

static void LC1_TilePixel(u32 n, u32 x, u32 y, u32 c)
{
    u16 *p = &sLC1->bg0tiles[n * 16 + y * 2 + (x >> 2)];
    u32 sh = (x & 3) * 4;
    *p = (*p & ~(0xF << sh)) | (c << sh);
}

static void LC1_FillMap(u16 entry)
{
    u32 r;
    for (r = 0; r < 32; r++)
        CpuFill16(entry, &sLC1->bg0map[r * 32], 64);
}

// pixel zetten; een kleinere kleurindex wint (1 = kern, hogere = gloed)
static void LC1_Plot(s32 x, s32 y, u32 c)
{
    u16 *e, *p;
    u32 idx, sh, old;

    if ((u32)x >= DISPLAY_WIDTH || (u32)y >= DISPLAY_HEIGHT)
        return;
    e = &sLC1->bg0map[(y >> 3) * 32 + (x >> 3)];
    idx = *e & 0x3FF;
    if (idx == 0 || idx < sLC1->reserved)
    {
        u32 n;
        if (sLC1->nextTile >= LC1_MAX_TILES)
            return;
        n = sLC1->nextTile++;
        if (idx == 0)
            CpuFill16(0, &sLC1->bg0tiles[n * 16], 32);
        else
            CpuCopy16(&sLC1->bg0tiles[idx * 16], &sLC1->bg0tiles[n * 16], 32);
        idx = n;
        *e = idx | (15 << 12);
    }
    p = &sLC1->bg0tiles[idx * 16 + (y & 7) * 2 + ((x & 7) >> 2)];
    sh = (x & 3) * 4;
    old = (*p >> sh) & 0xF;
    if (old != 0 && old <= c)
        return;
    *p = (*p & ~(0xF << sh)) | (c << sh);
}

static void LC1_Stamp(s32 x, s32 y, s32 r, u32 c)
{
    s32 i, j;
    for (j = -r; j <= r; j++)
        for (i = -r; i <= r; i++)
            if (i * i + j * j <= r * r + r)
                LC1_Plot(x + i, y + j, c);
}

// lijn van (x0,y0) naar (x1,y1), alleen het stuk tussen from en to (0-256); drie lagen: gloed, rand, kern
static void LC1_Line(s32 x0, s32 y0, s32 x1, s32 y1, s32 from, s32 to, s32 r, u32 c)
{
    s32 dx = x1 - x0, dy = y1 - y0, n = max(abs(dx), abs(dy)), i, i0, i1;
    if (n == 0)
        return;
    i0 = n * from >> 8;
    i1 = n * to >> 8;
    for (i = i0; i <= i1; i++)
        LC1_Stamp(x0 + dx * i / n, y0 + dy * i / n, r, c);
}

static void LC1_Line3(s32 x0, s32 y0, s32 x1, s32 y1, s32 from, s32 to)
{
    LC1_Line(x0, y0, x1, y1, from, to, 2, 3);
    LC1_Line(x0, y0, x1, y1, from, to, 1, 2);
    LC1_Line(x0, y0, x1, y1, from, to, 0, 1);
}

// cirkel per beeldlijn (WIN-bereik) rond (cx, cy) met straal r
static void LC1_CircleWin(u16 *buf, s32 cx, s32 cy, s32 r)
{
    s32 y, dy, h;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        dy = y - cy;
        if (r <= 0 || dy * dy >= r * r)
        {
            buf[y] = 0;
            continue;
        }
        h = Sqrt(r * r - dy * dy);
        buf[y] = WIN_RANGE(max(0, cx - h), min(DISPLAY_WIDTH, cx + h));
    }
}

static void LC1_PlayCry(void)
{
    PlayCry_Normal(sLC1->species, 0);
}

// kort wit flitsen (k van 'from' naar 0 in len frames)
static void LC1_Flash(s32 t, s32 at, s32 len, s32 from, u32 mask, u16 color)
{
    if (t < at || t >= at + len)
        return;
    LC1_TintFaded(mask, from - (t - at) * from / len, color);
}

// naar wit in 5 frames; TRUE als het klaar is
static bool32 LC1_WhiteOut(s32 t, s32 end)
{
    s32 k;
    if (t < end - 5)
        return FALSE;
    k = min((t - (end - 5)) * 4, 16);
    LC1_TintFaded(PALETTES_ALL, k, RGB_WHITE);
    return t >= end;
}

// de runner: start, elke frame update(t) tot TRUE, dan bevroren naar zwart (zoals RouteTransition_Run)
#define tLcState data[0]
#define tLcDelay data[1]

static void LC1_Run(u8 taskId, const struct LCIntro *in)
{
    struct Task *task = &gTasks[taskId];
    s32 t;
    bool32 done;

    switch (task->tLcState)
    {
    case 0:
        sLC1 = AllocZeroed(sizeof(*sLC1));
        if (sLC1 == NULL)
        {
            FadeScreenBlack();
            DestroyTask(taskId);
            return;
        }
        InitTransitionData();
        ScanlineEffect_Clear();
        sLC1->start = Tapu_Elapsed();
        sLC1->last = -1;
        sLC1->beatFx = in->beatFx;
        sLC1->beat0 = ((sLC1->start + 8) * 256 + in->beatFx - 1) / in->beatFx; // eerste tel minstens 8 frames na de start
        sLC1->rng = 0x5EED1234;
        sLC1->species = GetMonData(&gEnemyParty[0], MON_DATA_SPECIES);
        LC1_Bg0Init();
        in->init();
        SetVBlankCallback(VBlankCB_LC);
        task->tLcState++;
        break;
    case 1:
        t = Tapu_Elapsed() - sLC1->start;
        gPaletteFade.bufferTransferDisabled = TRUE; // geen half bijgewerkt palet op het scherm als een update uitloopt
        done = in->update(t);
        gPaletteFade.bufferTransferDisabled = FALSE;
        if (done)
        {
            task->tLcDelay = 2;
            task->tLcState++;
        }
        sLC1->last = t;
        break;
    case 2:
        if (--task->tLcDelay == 0)
        {
            sLC1->lineFlags &= ~LCF_COLOR;
            CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            task->tLcState++;
        }
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            if (in->finish != NULL)
                in->finish();
            SetHBlankCallback(NULL);
            DisableInterrupts(INTR_FLAG_HBLANK);
            ClearGpuRegBits(REG_OFFSET_DISPSTAT, DISPSTAT_HBLANK_INTR);
            SetVBlankCallback(VBlankCB_BattleTransition);
            ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
            SetGpuReg(REG_OFFSET_BLDCNT, 0);
            SetGpuReg(REG_OFFSET_BLDY, 0);
            TRY_FREE_AND_SET_NULL(sLC1->snap);
            FREE_AND_SET_NULL(sLC1);
            DmaStop(0);
            FadeScreenBlack();
            DestroyTask(taskId);
        }
        break;
    }
}

#undef tLcState
#undef tLcDelay

// =====================================================================================================================
// Swords of Justice + Keldeo: de lucht staat stil, twee onzichtbare zwaardhalen (een X) laten witte snijlijnen achter,
// dan valt het beeld in vier stukken uiteen. Het beeld is een schermafdruk van de wereld (8bpp, de kaartlagen + de
// snijlijnen op BG0 samengevoegd, in stukjes tijdens de halen); elk stuk is een eigen BG (BG0-3) met een eigen scroll,
// randtiles krijgen per stuk een gemaskeerde kopie. Geen vensters of HBlank nodig.
#define SW_K1 179   // "\": helling 0,70 door het midden
#define SW_K2 159   // "/": helling 0,62
#define SW_SNAP_TILES (30 * 20)
#define SW_BLANK  SW_SNAP_TILES
#define SW_MAX_TILES 880   // 0xDC00: de schermen beginnen op 0xE000

static const u16 sSW_Pal[16] = {0, RGB(31, 31, 31), RGB(26, 31, 31), RGB(16, 23, 30)};
// richting per stuk (x16): boven, rechts, links, onder
static const s8 sSW_Dir[4][2] = {{-3, -16}, {16, -4}, {-16, 4}, {3, 16}};
static const u8 sSW_PieceBg[4] = {3, 2, 1, 0};

static s32 SW_Line1(s32 x) { return 80 + (((x - 120) * SW_K1) >> 8); }
static s32 SW_Line2(s32 x) { return 80 - (((x - 120) * SW_K2) >> 8); }
static u32 SW_Piece(s32 x, s32 y) { return ((y >= SW_Line1(x)) << 1) | (y >= SW_Line2(x)); }

// de kaartlagen (BG3 onder, BG1 boven) van beeldlijn y0 t/m y1-1 in de 8bpp-afdruk; index = palet * 16 + kleur.
// Per beeldlijn per laag 31 tilerijen (8 pixels in een u32); lege rijen worden overgeslagen.
static void LC1_SnapLines(s32 y0, s32 y1)
{
    u8 line[DISPLAY_WIDTH];
    u32 words[31];
    u8 pals[31];
    s32 y, bg, c, i;

    for (y = y0; y < y1; y++)
    {
        u8 *dst = &sLC1->snap[(y >> 3) * 30 * 64 + (y & 7) * 8];
        memset(line, 0, sizeof(line));
        for (bg = 3; bg >= 1; bg--)
        {
            u16 cnt = *(vu16 *)(REG_ADDR_BG0CNT + bg * 2);
            const u32 *chr = (const u32 *)(BG_VRAM + ((cnt >> 2) & 3) * 0x4000);
            const u16 *scr = (const u16 *)(BG_VRAM + ((cnt >> 8) & 0x1F) * 0x800);
            s32 sx0 = sTransitionData->cameraX & 0xFF, sy = (y + sTransitionData->cameraY) & 0xFF, fx = sx0 & 7;
            const u16 *row = &scr[(sy >> 3) * 32];
            u32 any = 0;

            if (!(REG_DISPCNT & (DISPCNT_BG0_ON << bg)))
                continue;
            for (c = 0; c < 31; c++)
            {
                u16 e = row[((sx0 >> 3) + c) & 31];
                u32 ty = (e & 0x800) ? 7 - (sy & 7) : (sy & 7);
                u32 w = chr[(e & 0x3FF) * 8 + ty];
                if (w != 0 && (e & 0x400))
                {
                    w = ((w >> 4) & 0x0F0F0F0F) | ((w & 0x0F0F0F0F) << 4);
                    w = (w >> 24) | ((w >> 8) & 0xFF00) | ((w << 8) & 0xFF0000) | (w << 24);
                }
                words[c] = w;
                pals[c] = (e >> 12) << 4;
                any |= w;
            }
            if (any == 0)
                continue;
            for (c = 0; c < 30; c++)
            {
                u32 a = words[c], b = words[c + 1];
                u8 *out = &line[c * 8];
                if ((a >> (fx * 4)) == 0 && (fx == 0 || (b << ((8 - fx) * 4)) == 0))
                    continue;
                for (i = 0; i < 8; i++)
                {
                    u32 s = i + fx, n;
                    if (s < 8)
                    {
                        n = (a >> (s * 4)) & 15;
                        if (n)
                            out[i] = pals[c] | n;
                    }
                    else
                    {
                        n = (b >> ((s - 8) * 4)) & 15;
                        if (n)
                            out[i] = pals[c + 1] | n;
                    }
                }
            }
        }
        for (c = 0; c < 30; c++)
            memcpy(&dst[c * 64], &line[c * 8], 8);
    }
}

// de getekende BG0-tiles (de snijlijnen, scroll 0) over de afdruk
static void LC1_SnapBg0(void)
{
    u32 r, c, py, px;
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            u16 e = sLC1->bg0map[r * 32 + c];
            const u32 *tp = (const u32 *)&sLC1->bg0tiles[(e & 0x3FF) * 16];
            u8 *dst = &sLC1->snap[(r * 30 + c) * 64];
            if ((e & 0x3FF) == 0)
                continue;
            for (py = 0; py < 8; py++)
            {
                u32 w = tp[py];
                for (px = 0; px < 8 && w; px++, w >>= 4)
                    if (w & 15)
                        dst[py * 8 + px] = 0xF0 | (w & 15);
            }
        }
    }
}

static void SW_Init(void)
{
    LoadPalette(sSW_Pal, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    sLC1->snap = Alloc(SW_SNAP_TILES * 64);
    sLC1->v[0] = 0; // afdruk: aantal beeldlijnen klaar
    sLC1->v[1] = 0; // gesplitst?
}

// de afdruk naar VRAM, per stuk een tilemap; randtiles krijgen per stuk een kopie met alleen hun eigen pixels
// na de splitsing: de tilemap per stuk (30x20) in het geheugen, en een tussenbuffer (21 rijen per BG) voor de VBlank
#define SW_PM(p)    (&((u16 *)sLC1->snap)[(p) * 600])
#define SW_STAGE(i) (&((u16 *)sLC1->snap)[4 * 600 + (i) * 21 * 32])

static void SW_VBlank(void)
{
    u32 i;
    for (i = 0; i < 4; i++)
    {
        DmaCopy16(3, SW_STAGE(i), BG_VRAM + ((sLC1->v[8 + i] >> 8) & 0x1F) * 0x800, 21 * 32 * 2);
        *(vu16 *)(REG_ADDR_BG0HOFS + i * 4) = sLC1->v[4 + i] & 7 ? (-(sLC1->v[4 + i] & 7)) & 0x1FF : 0;
        *(vu16 *)(REG_ADDR_BG0VOFS + i * 4) = sLC1->v[12 + i] & 7 ? (-(sLC1->v[12 + i] & 7)) & 0x1FF : 0;
    }
}

// stuk p verschoven over (mx, my) pixels in de tussenbuffer: grof per tile in de tilemap (geen omslaan rond de 256
// pixels van de BG), fijn met de scroll
static void SW_Place(u32 p, s32 mx, s32 my)
{
    u32 bg = sSW_PieceBg[p];
    u16 *dst = SW_STAGE(bg);
    const u16 *pm = SW_PM(p);
    s32 tx = mx >> 3, ty = my >> 3, r, c;

    CpuFill16(SW_BLANK, dst, 21 * 32 * 2);
    for (r = 0; r < 20; r++)
    {
        s32 dr = r + ty;
        if (dr < 0 || dr > 20)
            continue;
        for (c = 0; c < 30; c++)
        {
            s32 dc = c + tx;
            if (dc < 0 || dc > 30)
                continue;
            dst[dr * 32 + dc] = pm[r * 30 + c];
        }
    }
    sLC1->v[4 + bg] = mx;
    sLC1->v[12 + bg] = my;
}

// de afdruk naar VRAM (8bpp, tile 600 = leeg); randtiles krijgen per stuk een kopie met alleen hun eigen pixels
static void SW_Split(void)
{
    u32 i, n = SW_BLANK + 1, r, c, p;
    u8 *vram = (u8 *)BG_VRAM;
    u16 *pm;

    for (i = 0; i < 4; i++)
        sLC1->v[8 + i] = *(vu16 *)(REG_ADDR_BG0CNT + i * 2);
    CpuCopy32(sLC1->snap, vram, SW_SNAP_TILES * 64);
    CpuFill32(0, vram + SW_BLANK * 64, 64);
    // randtiles eerst (lezen nog uit de afdruk), dan de tilemaps in de (nu vrije) afdrukbuffer
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            s32 x0 = c * 8, y0 = r * 8;
            u32 idx = r * 30 + c, p0 = SW_Piece(x0, y0), mask;
            mask = (1 << p0) | (1 << SW_Piece(x0 + 7, y0)) | (1 << SW_Piece(x0, y0 + 7)) | (1 << SW_Piece(x0 + 7, y0 + 7));
            if (mask == (1u << p0))
                continue;
            for (p = 0; p < 4; p++)
            {
                u32 py, px;
                u16 *dst;
                const u8 *src = &sLC1->snap[idx * 64];
                if (!((mask >> p) & 1) || n >= SW_MAX_TILES)
                    continue;
                dst = (u16 *)(vram + n * 64);
                for (py = 0; py < 8; py++)
                {
                    for (px = 0; px < 8; px += 2)
                    {
                        u32 a = SW_Piece(x0 + px, y0 + py) == p ? src[py * 8 + px] : 0;
                        u32 b = SW_Piece(x0 + px + 1, y0 + py) == p ? src[py * 8 + px + 1] : 0;
                        *dst++ = a | (b << 8);
                    }
                }
                n++;
            }
        }
    }
    // zelfde volgorde nog eens, nu de tilemaps
    pm = (u16 *)sLC1->snap;
    CpuFill16(SW_BLANK, pm, 4 * 600 * 2);
    n = SW_BLANK + 1;
    for (r = 0; r < 20; r++)
    {
        for (c = 0; c < 30; c++)
        {
            s32 x0 = c * 8, y0 = r * 8;
            u32 idx = r * 30 + c, p0 = SW_Piece(x0, y0), mask;
            mask = (1 << p0) | (1 << SW_Piece(x0 + 7, y0)) | (1 << SW_Piece(x0, y0 + 7)) | (1 << SW_Piece(x0 + 7, y0 + 7));
            if (mask == (1u << p0))
            {
                SW_PM(p0)[idx] = idx;
                continue;
            }
            for (p = 0; p < 4; p++)
                if (((mask >> p) & 1) && n < SW_MAX_TILES)
                    SW_PM(p)[idx] = n++;
        }
    }
    for (p = 0; p < 4; p++)
        SW_Place(p, 0, 0);
    for (i = 0; i < 4; i++)
    {
        u16 *map = (u16 *)(BG_VRAM + ((sLC1->v[8 + i] >> 8) & 0x1F) * 0x800);
        CpuFill16(SW_BLANK, map, BG_SCREEN_SIZE);
        SetGpuReg(REG_OFFSET_BG0CNT + i * 2, BGCNT_PRIORITY(i) | BGCNT_CHARBASE(0) | BGCNT_256COLOR | (sLC1->v[8 + i] & 0x1F00) | BGCNT_TXT256x256);
    }
    sLC1->vblank = SW_VBlank;
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG_ALL_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    gPlttBufferUnfaded[0] = gPlttBufferFaded[0] = RGB_BLACK;
}

static bool32 SW_Update(s32 t)
{
    s32 s1 = LC1_Beat(1), s2 = LC1_Beat(2), hit = LC1_Beat(3), split = hit + 1, end = (sLC1->v[1] ? sLC1->v[3] : split) + 30, k, i;

    LC1_WorldReset(0);
    // de wereld houdt de adem in
    if (t < hit)
        LC1_TintFaded(LC1_WORLD_BG | 0xFFFF0000, min(t / 2, 5), RGB(0, 1, 3));

    // afdruk van de kaartlagen, een paar beeldlijnen per frame
    if (sLC1->snap != NULL && sLC1->v[0] < DISPLAY_HEIGHT && t < hit)
    {
        s32 y1 = min(sLC1->v[0] + 10, DISPLAY_HEIGHT);
        LC1_SnapLines(sLC1->v[0], y1);
        sLC1->v[0] = y1;
    }

    // de twee halen: de lijn schiet in 4 frames over het scherm
    for (i = 0; i < 2; i++)
    {
        s32 at = i ? s2 : s1, a = t - at, b = sLC1->last - at;
        if (a < 0 || b >= 4)
            continue;
        if (i == 0)
            LC1_Line3(-16, SW_Line1(-16), 256, SW_Line1(256), max(0, b + 1) * 64, min(a + 1, 4) * 64);
        else
            LC1_Line3(256, SW_Line2(256), -16, SW_Line2(-16), max(0, b + 1) * 64, min(a + 1, 4) * 64);
        if (LC1_AT(at))
            PlaySE(SE_M_CUT);
    }
    for (i = 0; i < 2; i++)
    {
        s32 at = i ? s2 : s1;
        LC1_Flash(t, at + 1, 6, 9, LC1_WorldMask(0), RGB_WHITE);
        if (t >= at && t < at + 4)
        {
            k = (t & 1) ? 2 : -2;
            SetGpuReg(REG_OFFSET_BG1HOFS, (sTransitionData->cameraX + k) & 0x1FF);
            SetGpuReg(REG_OFFSET_BG2HOFS, (sTransitionData->cameraX + k) & 0x1FF);
            SetGpuReg(REG_OFFSET_BG3HOFS, (sTransitionData->cameraX + k) & 0x1FF);
        }
        else if (t == at + 4 && !sLC1->v[1])
        {
            SetGpuReg(REG_OFFSET_BG1HOFS, sTransitionData->cameraX);
            SetGpuReg(REG_OFFSET_BG2HOFS, sTransitionData->cameraX);
            SetGpuReg(REG_OFFSET_BG3HOFS, sTransitionData->cameraX);
        }
    }
    // de snijlijnen gloeien na
    if (t >= s1 && t < hit)
        gPlttBufferFaded[BG_PLTT_ID(15) + 3] = Tapu_Blend(sSW_Pal[3], RGB(4, 10, 20), 8 + Sin((t * 16) & 0xFF, 6));

    // de klap: wit, dan in stukken
    if (t >= hit && !sLC1->v[1])
    {
        LC1_TintFaded(PALETTES_ALL, 16, RGB_WHITE);
        if (t >= split && sLC1->v[2]) // pas als het witte beeld al getoond wordt (geen scheur in het beeld)
        {
            if (sLC1->snap == NULL)
                return LC1_WhiteOut(t, t + 5);
            if (sLC1->v[0] < DISPLAY_HEIGHT)
                LC1_SnapLines(sLC1->v[0], DISPLAY_HEIGHT);
            LC1_SnapBg0(); // de snijlijnen erover
            SW_Split();
            sLC1->v[1] = 1;
            sLC1->v[3] = Tapu_Elapsed() - sLC1->start; // de stukken bewegen vanaf nu (de opbouw kost een paar frames)
            PlaySE(SE_M_SWORDS_DANCE);
        }
        if (LC1_AT(hit))
            PlaySE(SE_M_RAZOR_WIND);
        sLC1->v[2] = 1;
        return FALSE;
    }
    if (sLC1->v[1])
    {
        s32 u = t - sLC1->v[3], d = (u * u) / 8 + u, sh = (u < 8) ? ((u & 1) ? 3 : -3) : 0;
        for (i = 0; i < 4; i++)
            SW_Place(i, (d * sSW_Dir[i][0] >> 4) + sh, d * sSW_Dir[i][1] >> 4);
        LC1_TintFaded(PALETTES_ALL, max(0, 16 - u * 3), RGB_WHITE);
        if (u > 12)
            LC1_TintFaded(PALETTES_ALL, min((u - 12) / 2, 6), RGB_BLACK);
        gPlttBufferFaded[0] = RGB_BLACK; // de kieren
        if (u == 4)
            LC1_PlayCry();
    }
    return LC1_WhiteOut(t, end);
}

static void SW_Finish(void)
{
    TRY_FREE_AND_SET_NULL(sLC1->snap);
}

static const struct LCIntro sLC_Swords = {LC1_TEMPO_LEGENDARY, SW_Init, SW_Update, SW_Finish};

static void Task_LegendSwords(u8 taskId)
{
    LC1_Run(taskId, &sLC_Swords);
}

// =====================================================================================================================
// Ultra Beasts: interdimensionale storing (golvende beeldlijnen, om-en-om verschoven = een kleurscheiding, een
// verspringende strook, rood/cyaan flikkeren, de kleuren klappen op de tel om), dan gaat in het midden een Ultra Wormhole
// open: een spiraal die ronddraait (paletcyclus) in een groeiende cirkel met een lichtende rand. De spiraal wordt tijdens
// de storing berekend (BIOS ArcTan2/Sqrt, in blokjes van 2x2); hij is puntsymmetrisch, dus de onderste helft is de
// bovenste helft gespiegeld (300 tiles).
static const u16 sUB_Spiral[9] = {RGB(31, 31, 31), RGB(20, 28, 31), RGB(8, 20, 31), RGB(10, 4, 24), RGB(4, 0, 10),
                                  RGB(14, 0, 20), RGB(28, 8, 28), RGB(31, 22, 31), RGB(0, 0, 2)};

enum { LCPOL_SPIRAL, LCPOL_PAST, LCPOL_FUTURE };

// een beeldvullend poolpatroon (hoek + straal, BIOS ArcTan2/Sqrt, blokjes van 2x2) in 300 tiles vanaf 'first': de
// bovenste helft; het patroon is puntsymmetrisch, dus de onderste helft is dezelfde tiles 180 graden gedraaid
static void LC1_PolarMap(u32 first)
{
    u32 r, c;
    for (r = 0; r < 10; r++)
    {
        for (c = 0; c < 30; c++)
        {
            u16 e = (first + r * 30 + c) | (15 << 12);
            sLC1->bg0map[r * 32 + c] = e;
            sLC1->bg0map[(19 - r) * 32 + 29 - c] = e | 0xC00;
        }
    }
}

static void LC1_PolarTiles(u32 first, s16 *done, u32 n, u32 mode)
{
    while (n-- && *done < 300)
    {
        u32 i = (*done)++, r = i / 30, c = i % 30, bx, by;
        u32 rows[8] = {0};
        for (by = 0; by < 4; by++)
        {
            for (bx = 0; bx < 4; bx++)
            {
                s32 dx = (c * 8 + bx * 2) * 2 + 1 - 239, dy = (r * 8 + by * 2) * 2 + 1 - 159;
                u32 a = ArcTan2(dx, dy) >> 8, rr = Sqrt(dx * dx + dy * dy) >> 1, idx, depth;
                if (rr < 6)
                    idx = 9;
                else if (mode == LCPOL_SPIRAL)
                    idx = 1 + (((a * 2 + rr * 3) >> 5) & 7);
                else if (mode == LCPOL_PAST) // ringen die naar het midden dichter worden, licht gedraaid
                    idx = 1 + (((24000 / (rr + 8) + a * 2) >> 5) & 7);
                else // raster: ringen + 16 spaken, de lijnen licht (1-4), de vakken donker (5-8)
                {
                    depth = 12000 / (rr + 8);
                    idx = ((depth & 31) < 7 || (a & 15) < 2 ? 1 : 5) + ((depth >> 5) & 3);
                }
                idx |= idx << 4;
                rows[by * 2] |= idx << (bx * 8);
                rows[by * 2 + 1] |= idx << (bx * 8);
            }
        }
        CpuCopy32(rows, &sLC1->bg0tiles[(first + i) * 16], 32);
    }
}

static void UB_Init(void)
{
    LoadPalette(sUB_Spiral, BG_PLTT_ID(15) + 1, sizeof(sUB_Spiral));
    CpuFill32(0, &sLC1->bg0tiles[16], 300 * 32);
    LC1_PolarMap(1);
    sLC1->nextTile = sLC1->reserved = 301;
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG0_ON); // pas bij het wormgat
    LC1_StartLines(LCF_HOFS | LCF_VOFS);
    sLC1->v[0] = 0;
    sLC1->v[1] = -1;
}

static bool32 UB_Update(s32 t)
{
    s32 open = LC1_Beat(3), end = open + 34, y, amp, ch, u;
    u16 *h = sLC1->back[LCB_HOFS], *vv = sLC1->back[LCB_VOFS];
    bool32 inv = FALSE;

    LC1_PolarTiles(1, &sLC1->v[0], 9, LCPOL_SPIRAL);

    // storing per beeldlijn
    amp = min(t / 6, 7);
    ch = (t & 2) ? 1 + (t >= LC1_Beat(1)) + (t >= open) : 0;
    if (t / 5 != sLC1->v[1])
    {
        sLC1->v[1] = t / 5;
        sLC1->v[2] = LC1_Rand() % 140;
        sLC1->v[3] = 6 + LC1_Rand() % 18;
        sLC1->v[4] = (LC1_Rand() % 49) - 24;
    }
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 o = Sin((y * 5 + t * 9) & 0xFF, amp) + ((y & 1) ? ch : -ch);
        if (y >= sLC1->v[2] && y < sLC1->v[2] + sLC1->v[3] && t >= LC1_Beat(0))
            o += sLC1->v[4];
        h[y] = (sTransitionData->cameraX + o) & 0x1FF;
        vv[y] = (sTransitionData->cameraY + Sin((y * 3 - t * 5) & 0xFF, amp / 3)) & 0x1FF;
    }

    // kleuren: op de tel omgeklapt, verder rood/cyaan flikkeren
    for (u = 0; u < 3; u++)
        if ((t >= LC1_Beat(u) && t < LC1_Beat(u) + 3) || (t >= LC1_Beat2(u * 2 + 1) && t < LC1_Beat2(u * 2 + 1) + 1))
            inv = TRUE;
    if (inv)
        LC1_WorldFilter(LCP_INVERT, 16, 0);
    else
        LC1_WorldReset(0);
    LC1_TintFaded(LC1_WorldMask(0), 3 + (t >= open) * 2, (t & 1) ? RGB(31, 0, 24) : RGB(0, 24, 31));
    if (LC1_AT(LC1_Beat(0)))
        PlaySE(SE_M_PSYBEAM2);

    // het wormgat
    if (t >= open)
    {
        s32 R, rot, i;
        u = t - open;
        if (!sLC1->regs)
        {
            LC1_PolarTiles(1, &sLC1->v[0], 300, LCPOL_SPIRAL);
            LC1_UseRegs(WININ_WIN0_BG0 | WININ_WIN1_BG1 | WININ_WIN1_BG2 | WININ_WIN1_BG3 | WININ_WIN1_OBJ | WININ_WIN1_CLR,
                       WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ,
                       BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ);
            sLC1->bldy = 12;
            LC1_CircleWin(sLC1->back[LCB_WIN0], 120, 80, 0);
            LC1_CircleWin(sLC1->back[LCB_WIN1], 120, 80, 0);
            CpuCopy16(sLC1->back[LCB_WIN0], sLC1->front[LCB_WIN0], DISPLAY_HEIGHT * 2);
            CpuCopy16(sLC1->back[LCB_WIN1], sLC1->front[LCB_WIN1], DISPLAY_HEIGHT * 2);
            sLC1->lineFlags |= LCF_WIN0 | LCF_WIN1;
            LC1_SetWindows(DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
            SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG0_ON);
            PlaySE(SE_M_TELEPORT);
        }
        R = u * u / 12 + u * 2;
        LC1_CircleWin(sLC1->back[LCB_WIN0], 120, 80, R);
        LC1_CircleWin(sLC1->back[LCB_WIN1], 120, 80, R + 5 + u / 4);
        rot = (u * (4 + u / 6)) >> 2;
        for (i = 0; i < 8; i++)
            gPlttBufferFaded[BG_PLTT_ID(15) + 1 + i] = sUB_Spiral[(i + rot) & 7];
        gPlttBufferFaded[BG_PLTT_ID(15) + 9] = sUB_Spiral[8];
        if (u == 12)
            LC1_PlayCry();
    }
    return LC1_WhiteOut(t, end);
}

static const struct LCIntro sLC_UltraBeast = {LC1_TEMPO_UB, UB_Init, UB_Update, NULL};

static void Task_LegendUltraBeast(u8 taskId)
{
    LC1_Run(taskId, &sLC_UltraBeast);
}

// =====================================================================================================================
// Paradox-Pokémon: het heden flikkert tussen het verleden (sepia, korrel, krassen op de film, golvend als een oude
// projectie) en de toekomst (cyaan, scanlijnen, digitale blokken, verspringende stroken), op de tel van Battle! Area
// Zero: eerst in achtsten, dan zestienden, dan tweeëndertigsten. Dan kiest het beeld een tijdperk en duikt erin: het
// verleden sluit als een oude film (iris), de toekomst gaat uit als een crt-scherm.
enum { PX_PRESENT, PX_PAST, PX_FUTURE };
enum { PXT_GRAIN = 1, PXT_SCRATCH = 5, PXT_SCAN, PXT_BLOCK, PXT_TUNNEL = PXT_BLOCK + 3 };
// tijdtunnel: verleden amber/oer (ringen), toekomst cyaan/violet (raster: lijnen 1-4, vakken 5-8)
static const u16 sPX_TunnelPast[9] = {RGB(31, 30, 22), RGB(31, 24, 10), RGB(26, 15, 3), RGB(16, 8, 2), RGB(7, 3, 1),
                                      RGB(14, 7, 2), RGB(24, 14, 4), RGB(30, 22, 10), RGB(2, 1, 0)};
static const u16 sPX_TunnelFuture[9] = {RGB(24, 31, 31), RGB(8, 28, 31), RGB(20, 12, 31), RGB(31, 18, 31), RGB(1, 3, 9),
                                        RGB(4, 1, 10), RGB(0, 6, 12), RGB(6, 2, 14), RGB(0, 0, 3)};
static const u16 sPX_Pal[16] = {0, RGB(7, 4, 1), RGB(31, 28, 20), RGB(24, 20, 12), RGB(0, 6, 10), RGB(10, 31, 31),
                                RGB(26, 31, 31), RGB(6, 14, 31)};

static void PX_Init(void)
{
    u32 i, j;
    LoadPalette(sPX_Pal, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    for (i = 0; i < 4; i++) // korrel
    {
        u32 n = LC1_NewTile();
        for (j = 0; j < 3 + (i & 1); j++)
            LC1_TilePixel(n, LC1_Rand() & 7, LC1_Rand() & 7, 1 + (LC1_Rand() & 1));
    }
    i = LC1_NewTile(); // kras
    for (j = 0; j < 8; j++)
        if (j != 5)
            LC1_TilePixel(i, 3, j, 3);
    i = LC1_NewTile(); // scanlijnen
    for (j = 1; j < 8; j += 2)
        CpuFill16(0x4444, &sLC1->bg0tiles[i * 16 + j * 2], 4);
    for (j = 0; j < 3; j++) // blokken
    {
        i = LC1_NewTile();
        LC1_SolidTile(i, 5 + j);
    }
    LC1_UseRegs(LC1_WININ_ALL, WINOUT_WIN01_ALL, BLDCNT_EFFECT_BLEND | BLDCNT_TGT1_BG0 | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    LC1_StartLines(LCF_HOFS | LCF_VOFS);
    sLC1->v[0] = PX_PRESENT;
    // Koraidon en Miraidon (Jordi: "een past warp" / "een future warp"): de duik wordt een tijdtunnel
    sLC1->v[6] = (sLC1->species == SPECIES_KORAIDON || sLC1->species == SPECIES_MIRAIDON);
    sLC1->v[5] = 0;
    if (sLC1->v[6])
        CpuFill32(0, &sLC1->bg0tiles[PXT_TUNNEL * 16], 300 * 32);
}

static void PX_InitPast(void)
{
    PX_Init();
    sLC1->variant = PX_PAST;
}

static void PX_InitFuture(void)
{
    PX_Init();
    sLC1->variant = PX_FUTURE;
}

static void PX_DrawEra(u32 era, s32 t)
{
    u32 i;
    u16 *map = sLC1->bg0map;
    if (era == PX_PAST)
    {
        for (i = 0; i < 32 * 21; i++)
            map[i] = (PXT_GRAIN + (LC1_Rand() & 3)) | (LC1_Rand() & 0xC00) | (15 << 12);
        for (i = 0; i < 1 + (t & 1); i++)
        {
            u32 c = LC1_Rand() % 30, r;
            for (r = 0; r < 21; r++)
                map[r * 32 + c] = PXT_SCRATCH | (15 << 12);
        }
    }
    else if (era == PX_FUTURE)
    {
        for (i = 0; i < 32 * 21; i++)
            map[i] = PXT_SCAN | (15 << 12);
        for (i = 0; i < 14; i++)
        {
            u32 c = LC1_Rand() % 29, r = LC1_Rand() % 20, k = PXT_BLOCK + LC1_Rand() % 3;
            map[r * 32 + c] = k | (15 << 12);
            map[r * 32 + c + 1] = k | (15 << 12);
        }
    }
    else
    {
        CpuFill16(0, map, BG_SCREEN_SIZE);
    }
}

static bool32 PX_Warp(s32 t, s32 dive);

static bool32 PX_Update(s32 t)
{
    s32 p32 = ((t + sLC1->start) * 256 * 8) / sLC1->beatFx - sLC1->beat0 * 8;
    s32 dive = LC1_Beat(4), end = dive + 32, y, era, u;

    if (sLC1->v[6])
    {
        LC1_PolarTiles(PXT_TUNNEL, &sLC1->v[5], 9, sLC1->variant == PX_PAST ? LCPOL_PAST : LCPOL_FUTURE);
        if (t >= dive)
            return PX_Warp(t, dive);
    }
    u16 *h = sLC1->back[LCB_HOFS], *vv = sLC1->back[LCB_VOFS];

    if (p32 < 0)
        era = PX_PRESENT;
    else if (p32 < 16)
        era = ((p32 >> 2) & 1) ? PX_FUTURE : PX_PAST;
    else if (p32 < 24)
        era = ((p32 >> 1) & 1) ? PX_FUTURE : PX_PAST;
    else if (p32 < 28)
        era = (p32 & 1) ? PX_FUTURE : PX_PAST;
    else
        era = sLC1->variant;
    if (era != sLC1->v[0] || (era == PX_PAST && (t & 1)) || (era == PX_FUTURE && t % 3 == 0 && t < dive))
        PX_DrawEra(era, t);
    if (p32 >= 28 && !sLC1->v[1])
    {
        sLC1->v[1] = 1;
        LC1_PlayCry();
    }
    sLC1->v[0] = era;

    // kleuren en beeldlijnen
    u = t - dive;
    if (era == PX_PAST)
    {
        s32 a = 1 + (u > 0 ? u / 5 : 0);
        LC1_WorldFilter(LCP_SEPIA, 16, 0);
        LC1_TintFaded(LC1_WorldMask(0), (LC1_Rand() & 1) * 2, RGB(4, 2, 0)); // flakkerende projector
        sLC1->bldalpha = BLDALPHA_BLEND(9, 16);
        SetGpuReg(REG_OFFSET_BG0HOFS, LC1_Rand() & 7);
        SetGpuReg(REG_OFFSET_BG0VOFS, LC1_Rand() & 7);
        for (y = 0; y < DISPLAY_HEIGHT; y++)
        {
            h[y] = sTransitionData->cameraX;
            vv[y] = (sTransitionData->cameraY + Sin((y * 8 + t * 6) & 0xFF, a)) & 0x1FF;
        }
        gPlttBufferFaded[0] = RGB(3, 2, 1);
    }
    else if (era == PX_FUTURE)
    {
        LC1_WorldFilter(LCP_FUTURE, 16, 0);
        sLC1->bldalpha = BLDALPHA_BLEND(7, 16);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, (t & 1));
        for (y = 0; y < DISPLAY_HEIGHT; y++)
        {
            s32 band = y >> 3, o = 0;
            if (((band * 7 + t) % 11) < 2)
                o = ((s32)((band * 13 + t * 5) & 7) - 4) * 4;
            h[y] = (sTransitionData->cameraX + o) & 0x1FF;
            vv[y] = sTransitionData->cameraY;
        }
        gPlttBufferFaded[0] = RGB(0, 2, 4);
    }
    else
    {
        LC1_WorldReset(0);
    }

    // de duik
    if (u >= 0)
    {
        u16 *win = sLC1->back[LCB_WIN0];
        if (!(sLC1->lineFlags & LCF_WIN0))
        {
            sLC1->winin = WININ_WIN0_ALL;
            sLC1->winout = 0;
            for (y = 0; y < DISPLAY_HEIGHT; y++)
                sLC1->front[LCB_WIN0][y] = win[y] = WIN_RANGE(0, DISPLAY_WIDTH);
            sLC1->lineFlags |= LCF_WIN0;
            LC1_SetWindows(DISPCNT_WIN0_ON);
            PlaySE(sLC1->variant == PX_PAST ? SE_M_TELEPORT : SE_M_SKETCH);
        }
        if (sLC1->variant == PX_PAST)
        {
            // iris: een oude film sluit
            s32 R = max(0, 150 - u * u / 6 - u * 2);
            LC1_CircleWin(win, 120, 80, R);
            if (R == 0)
                LC1_TintFaded(PALETTES_ALL, 16, RGB_BLACK);
        }
        else
        {
            // crt uit: de beeldband wordt een lijn, de lijn een punt
            s32 hh = max(1, 80 - u * u / 3), w = u < 14 ? 120 : max(0, 120 - (u - 14) * 14);
            sLC1->win0v = WIN_RANGE(80 - hh, 80 + hh);
            for (y = 0; y < DISPLAY_HEIGHT; y++)
                win[y] = WIN_RANGE(120 - w, 120 + w);
            sLC1->bldcnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BG0;
            sLC1->bldy = min(u + 2, 16);
            gPlttBufferFaded[0] = RGB_BLACK;
        }
    }
    return LC1_WhiteOut(t, end);
}

// de tijdwarp: in het midden gaat een tunnel open (venster 0, met een lichtende rand in venster 1) die steeds sneller
// op je af komt (paletcyclus), de wereld eromheen trekt in het tijdperk weg, dan wit
static bool32 PX_Warp(s32 t, s32 dive)
{
    s32 u = t - dive, end = dive + 52, R, rot, i, y;
    const u16 *pal = sLC1->variant == PX_PAST ? sPX_TunnelPast : sPX_TunnelFuture;
    u16 *h = sLC1->back[LCB_HOFS], *vv = sLC1->back[LCB_VOFS];

    if (!(sLC1->lineFlags & LCF_WIN0))
    {
        LC1_PolarTiles(PXT_TUNNEL, &sLC1->v[5], 300, sLC1->variant == PX_PAST ? LCPOL_PAST : LCPOL_FUTURE);
        sLC1->winin = WININ_WIN0_BG0 | WININ_WIN1_BG1 | WININ_WIN1_BG2 | WININ_WIN1_BG3 | WININ_WIN1_OBJ | WININ_WIN1_CLR;
        sLC1->winout = WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ;
        sLC1->bldcnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ;
        sLC1->bldy = 12;
        LC1_CircleWin(sLC1->front[LCB_WIN0], 120, 80, 0);
        LC1_CircleWin(sLC1->front[LCB_WIN1], 120, 80, 0);
        CpuCopy16(sLC1->front[LCB_WIN0], sLC1->back[LCB_WIN0], DISPLAY_HEIGHT * 4);
        sLC1->lineFlags |= LCF_WIN0 | LCF_WIN1;
        LC1_SetWindows(DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
        PlaySE(sLC1->variant == PX_PAST ? SE_M_TELEPORT : SE_M_PSYBEAM2);
    }
    else if (!sLC1->v[7])
    {
        // een frame later: dan staan de vensters al (anders een frame lang de hele tunnel)
        sLC1->v[7] = 1;
        LC1_PolarMap(PXT_TUNNEL);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    }
    // de wereld blijft in het gekozen tijdperk en wordt naar de tunnel toe getrokken (golf + inzakken)
    LC1_WorldFilter(sLC1->variant == PX_PAST ? LCP_SEPIA : LCP_FUTURE, 16, 0);
    LC1_TintFaded(LC1_WorldMask(0), min(u / 3, 8), sLC1->variant == PX_PAST ? RGB(10, 5, 0) : RGB(2, 0, 10));
    gPlttBufferFaded[0] = pal[8];
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 pull = ((y - 80) * min(u, 30)) >> 4;
        h[y] = (sTransitionData->cameraX + Sin((y * 6 + t * 10) & 0xFF, 1 + u / 6)) & 0x1FF;
        vv[y] = (sTransitionData->cameraY + pull / 4) & 0x1FF;
    }
    R = u * u / 10 + u * 2;
    LC1_CircleWin(sLC1->back[LCB_WIN0], 120, 80, R);
    LC1_CircleWin(sLC1->back[LCB_WIN1], 120, 80, R + 4 + u / 5);
    // de tunnel: ringen komen op je af, steeds sneller
    rot = (u * (6 + u / 4)) >> 2;
    if (sLC1->variant == PX_PAST)
    {
        for (i = 0; i < 8; i++)
            gPlttBufferFaded[BG_PLTT_ID(15) + 1 + i] = pal[(i + 8 - (rot & 7)) & 7];
    }
    else
    {
        for (i = 0; i < 4; i++)
        {
            gPlttBufferFaded[BG_PLTT_ID(15) + 1 + i] = pal[(i + 4 - (rot & 3)) & 3];
            gPlttBufferFaded[BG_PLTT_ID(15) + 5 + i] = pal[4 + ((i + 4 - (rot & 3)) & 3)];
        }
    }
    gPlttBufferFaded[BG_PLTT_ID(15) + 9] = pal[8];
    // op de tel een lichtpuls door de tunnel
    for (i = 5; i < 8; i++)
        LC1_Flash(t, LC1_Beat(i), 6, 8, 1 << 15, sLC1->variant == PX_PAST ? RGB(31, 28, 16) : RGB(24, 31, 31));
    if (u == 20)
        PlaySE(sLC1->variant == PX_PAST ? SE_M_SACRED_FIRE : SE_M_HYPER_BEAM);
    return LC1_WhiteOut(t, end);
}

static const struct LCIntro sLC_ParadoxPast = {LC1_TEMPO_AREA_ZERO, PX_InitPast, PX_Update, NULL};
static const struct LCIntro sLC_ParadoxFuture = {LC1_TEMPO_AREA_ZERO, PX_InitFuture, PX_Update, NULL};

static void Task_LegendParadoxPast(u8 taskId)
{
    LC1_Run(taskId, &sLC_ParadoxPast);
}

static void Task_LegendParadoxFuture(u8 taskId)
{
    LC1_Run(taskId, &sLC_ParadoxFuture);
}

// =====================================================================================================================
// Eternatus: de hemel kleurt rood-paars (BG0 over het hele beeld, met per beeldlijn een verloop van paars naar
// Dynamax-rood dat op de tel oplicht), de grond dreunt steeds harder, rode energiezuilen schieten omhoog. Op de vierde
// tel scheurt de wereld open (een gloeiende zigzag) en de scheur gaat open als een oog vol rood licht terwijl de wereld
// eromheen wegzakt.
#define ET_CRACK_POINTS 11
// 4-6 de scheur (kern, rand, gloed), 13/14 de energiezuilen, 15 de hemel (per beeldlijn); een lagere index wint bij het tekenen
static const u16 sET_Pal[16] = {0, 0, 0, 0, RGB(31, 31, 28), RGB(31, 12, 14), RGB(22, 0, 8), 0, 0, 0, 0, 0, 0, RGB(31, 4, 10), RGB(31, 20, 24), RGB(20, 0, 12)};
static const s16 sET_Crack[ET_CRACK_POINTS][2] = {{-6, 72}, {24, 86}, {50, 66}, {76, 92}, {102, 74}, {124, 94},
                                                  {148, 70}, {174, 90}, {198, 70}, {222, 86}, {246, 76}};
static const u8 sET_BeamCol[6] = {2, 7, 12, 17, 22, 27};

static void ET_Init(void)
{
    u32 n, y;
    LoadPalette(sET_Pal, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    n = LC1_NewTile(); // 1: de hemel (kleur 15, per beeldlijn een andere kleur)
    LC1_SolidTile(n, 15);
    n = LC1_NewTile(); // 2: energiezuil
    for (y = 0; y < 8; y++)
        sLC1->bg0tiles[n * 16 + y * 2] = 0xEEDD, sLC1->bg0tiles[n * 16 + y * 2 + 1] = 0xDDEE;
    LC1_FillMap(1 | (15 << 12));
    LC1_UseRegs(LC1_WININ_ALL, WINOUT_WIN01_ALL, BLDCNT_EFFECT_BLEND | BLDCNT_TGT1_BG0 | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    sLC1->bldalpha = BLDALPHA_BLEND(0, 16);
    sLC1->colorIdx = BG_PLTT_ID(15) + 15;
    LC1_StartLines(LCF_HOFS | LCF_VOFS | LCF_COLOR);
}

static bool32 ET_Update(s32 t)
{
    s32 crack = LC1_Beat(4), open = crack + 8, end = open + 36, k, y, i, amp, jx, jy, pulse, sink = 0;
    u16 *h = sLC1->back[LCB_HOFS], *vv = sLC1->back[LCB_VOFS], *col = sLC1->back[LCB_COLOR];

    // de hemel kleurt in twee tellen
    k = min(t * 16 / max(1, LC1_Beat(2)), 16);
    LC1_WorldReset(0);
    LC1_TintFaded(LC1_WorldMask(0), k * 8 / 16 + (t >= open ? min((t - open) / 3, 3) : 0), RGB(8, 0, 5));
    if (t < open)
        sLC1->bldalpha = BLDALPHA_BLEND(k * 7 / 16, 16 - k / 4);

    // verloop per beeldlijn, licht op op de tel
    pulse = 0;
    for (i = 0; i < 8; i++)
    {
        s32 d = t - LC1_Beat(i);
        if (d >= 0 && d < 10)
            pulse = max(pulse, 10 - d);
    }
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        col[y] = Tapu_Blend(Tapu_Blend(RGB(14, 0, 20), RGB(31, 2, 4), y / 10), RGB(31, 18, 22), pulse);

    // dreunen
    amp = (t < LC1_Beat(1)) ? 0 : (t < crack ? 1 + (t >= LC1_Beat(3)) : 3);
    jx = amp ? (s32)(LC1_Rand() % (amp * 2 + 1)) - amp : 0;
    jy = amp ? (s32)(LC1_Rand() % (amp * 2 + 1)) - amp : 0;
    if (t >= open)
        sink = (t - open) * (t - open) / 14;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        h[y] = (sTransitionData->cameraX + jx + (t >= crack ? Sin((y * 9 + t * 13) & 0xFF, 2) : 0)) & 0x1FF;
        vv[y] = (sTransitionData->cameraY + jy - sink) & 0x1FF;
    }
    SetGpuReg(REG_OFFSET_BG0HOFS, jx & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, jy & 0x1FF);
    if (LC1_AT(LC1_Beat(1)))
        PlaySE(SE_M_EARTHQUAKE);

    // energiezuilen
    for (i = 0; i < 6; i++)
    {
        s32 st = LC1_Beat2(2 + i), hgt = (t - st) * 2 / 3, r;
        if (t < st || t >= open)
            continue;
        hgt = min(hgt, 20);
        for (r = 0; r < hgt; r++)
        {
            u16 *e = &sLC1->bg0map[(19 - r) * 32 + sET_BeamCol[i]];
            if ((e[0] & 0x3FF) < sLC1->reserved)
                e[0] = 2 | (15 << 12);
            if ((e[1] & 0x3FF) < sLC1->reserved)
                e[1] = 2 | (15 << 12);
        }
        if (LC1_AT(st) && !(i & 1))
            PlaySE(SE_M_CHARGE);
    }
    gPlttBufferFaded[BG_PLTT_ID(15) + 13] = (t & 2) ? RGB(31, 4, 10) : RGB(26, 0, 8);
    gPlttBufferFaded[BG_PLTT_ID(15) + 14] = (t & 2) ? RGB(31, 20, 24) : RGB(31, 28, 28);

    // de scheur
    if (t >= crack && sLC1->last < crack + 5)
    {
        s32 a = t - crack, b = sLC1->last - crack;
        for (i = 0; i < ET_CRACK_POINTS - 1; i++)
        {
            s32 from = max(0, b + 1) * 64, to = min(a + 1, 4) * 64;
            if (from > to)
                continue;
            LC1_Line(sET_Crack[i][0], sET_Crack[i][1], sET_Crack[i + 1][0], sET_Crack[i + 1][1], from, to, 3, 6);
            LC1_Line(sET_Crack[i][0], sET_Crack[i][1], sET_Crack[i + 1][0], sET_Crack[i + 1][1], from, to, 1, 5);
            LC1_Line(sET_Crack[i][0], sET_Crack[i][1], sET_Crack[i + 1][0], sET_Crack[i + 1][1], from, to, 0, 4);
        }
        if (LC1_AT(crack))
        {
            PlaySE(SE_THUNDER);
            LC1_PlayCry();
        }
    }
    LC1_Flash(t, crack, 8, 10, LC1_WorldMask(0), RGB(31, 6, 6));

    // de scheur gaat open: een oog van rood licht, de wereld zakt weg
    if (t >= open)
    {
        s32 u = t - open, H = u * u / 14 + u / 2, W = 150 + u * 2;
        u16 *win = sLC1->back[LCB_WIN0];
        if (!(sLC1->lineFlags & LCF_WIN0))
        {
            sLC1->winin = WININ_WIN0_BG0 | WININ_WIN0_CLR;
            sLC1->winout = WINOUT_WIN01_BG1 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ;
            sLC1->bldcnt = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG0 | BLDCNT_TGT1_BD;
            CpuFill16(0, sLC1->front[LCB_WIN0], DISPLAY_HEIGHT * 2);
            CpuFill16(0, win, DISPLAY_HEIGHT * 2);
            sLC1->lineFlags |= LCF_WIN0;
            LC1_SetWindows(DISPCNT_WIN0_ON);
            PlaySE(SE_M_HYPER_BEAM);
        }
        for (y = 0; y < DISPLAY_HEIGHT; y++)
        {
            s32 dy = abs(y - 82), half;
            if (dy >= H)
            {
                win[y] = 0;
                continue;
            }
            half = W * Sqrt(((H - dy) << 8) / H) >> 4;
            win[y] = WIN_RANGE(max(0, 120 - half), min(DISPLAY_WIDTH, 120 + half));
        }
        sLC1->bldy = min(4 + u / 3, 14);
    }
    return LC1_WhiteOut(t, end);
}

static const struct LCIntro sLC_Eternatus = {LC1_TEMPO_LEGENDARY, ET_Init, ET_Update, NULL};

static void Task_LegendEternatus(u8 taskId)
{
    LC1_Run(taskId, &sLC_Eternatus);
}

// =====================================================================================================================
// Marshadow: een schaduw kruipt van onderen en van de zijkanten het beeld in (per beeldlijn een verlicht stuk, venster
// 0, met een halfschaduw eromheen, venster 1 met 'donkerder maken'), met vingers die naar binnen grijpen. De wereld
// verliest haar kleur. Als alles zwart is, flakkert Marshadows groene vlam even op.
static bool32 MS_Update(s32 t)
{
    s32 engulf = LC1_Beat(5), end = engulf + 22, q, y, i;
    u16 *w0 = sLC1->back[LCB_WIN0], *w1 = sLC1->back[LCB_WIN1];

    q = min(t * 256 / max(1, engulf), 256);   // voortgang 0-256
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 base = 150 - (150 * q * q >> 16) - (q * 30 >> 8), rise = 210 * q >> 8, L, R;
        if (y > DISPLAY_HEIGHT - rise)
            base -= (y - (DISPLAY_HEIGHT - rise)) * 2;
        L = base + Sin((y * 6 + t * 5) & 0xFF, 7) + Sin((y * 15 - t * 8) & 0xFF, 3);
        R = base + Sin((y * 7 - t * 4 + 90) & 0xFF, 7) + Sin((y * 13 + t * 9) & 0xFF, 3);
        for (i = 0; i < 3; i++)
        {
            s32 yl = 30 + i * 50 + Sin((t * 2 + i * 80) & 0xFF, 18), yr = 50 + i * 45 + Sin((t * 3 + i * 60) & 0xFF, 16);
            s32 reach = (q * (40 + i * 10)) >> 8;
            if (abs(y - yl) < 10)
                L -= reach * (10 - abs(y - yl)) / 10;
            if (abs(y - yr) < 10)
                R -= reach * (10 - abs(y - yr)) / 10;
        }
        if (L + R <= 0)
            w0[y] = 0;
        else
            w0[y] = WIN_RANGE(max(0, min(DISPLAY_WIDTH, 120 - L)), max(0, min(DISPLAY_WIDTH, 120 + R)));
        if (L + R + 24 <= 0)
            w1[y] = 0;
        else
            w1[y] = WIN_RANGE(max(0, min(DISPLAY_WIDTH, 120 - L - 12)), max(0, min(DISPLAY_WIDTH, 120 + R + 12)));
    }

    // de wereld verliest haar kleur
    LC1_WorldFilter(LCP_GRAY, min(t / 3, 12), 0);
    LC1_TintFaded(LC1_WorldMask(0), q * 6 >> 8, RGB(3, 0, 6));
    gPlttBufferFaded[0] = RGB(1, 0, 2);
    if (LC1_AT(0))
        PlaySE(SE_M_FAINT_ATTACK);
    if (LC1_AT(LC1_Beat(2)))
        PlaySE(SE_M_NIGHTMARE);
    if (LC1_AT(engulf - 6))
        LC1_PlayCry();
    // de groene vlam
    if (t >= engulf + 4)
    {
        s32 u = t - (engulf + 4);
        gPlttBufferFaded[0] = Tapu_Blend(RGB(1, 0, 2), RGB(10, 31, 14), max(0, 12 - u * 2 + (u < 6 ? Sin(u * 40, 3) : 0)));
        if (u == 0)
            PlaySE(SE_M_SACRED_FIRE);
    }
    return t >= end;
}

static void MS_Init(void)
{
    LC1_UseRegs(WININ_WIN0_BG1 | WININ_WIN0_BG2 | WININ_WIN0_BG3 | WININ_WIN0_OBJ
             | WININ_WIN1_BG1 | WININ_WIN1_BG2 | WININ_WIN1_BG3 | WININ_WIN1_OBJ | WININ_WIN1_CLR, 0,
               BLDCNT_EFFECT_DARKEN | BLDCNT_TGT1_BG1 | BLDCNT_TGT1_BG2 | BLDCNT_TGT1_BG3 | BLDCNT_TGT1_OBJ);
    sLC1->bldy = 10;
    MS_Update(0);
    CpuCopy16(sLC1->back, sLC1->front, sizeof(sLC1->front));
    LC1_StartLines(LCF_WIN0 | LCF_WIN1);
    LC1_SetWindows(DISPCNT_WIN0_ON | DISPCNT_WIN1_ON);
}

static const struct LCIntro sLC_Marshadow = {LC1_TEMPO_LEGENDARY, MS_Init, MS_Update, NULL};

static void Task_LegendMarshadow(u8 taskId)
{
    LC1_Run(taskId, &sLC_Marshadow);
}

// =====================================================================================================================
// Terapagos: de wereld wordt donker, zes Tera-kristallen (gevechtsanimatie-art) draaien in een ellips om het midden en
// komen steeds dichterbij, elk draaiend om zijn as, met een buitenring van splinters die de andere kant op gaat. De
// kristallen krijgen een regenboogglans (paletcyclus) en flitsen op de tel. In het midden verschijnt het Tera-symbool,
// dan spat alles uiteen in het witte Stellar-licht.
#define TP_TAG_CRYSTAL 0x5B10
#define TP_TAG_SHARD   0x5B11
#define TP_TAG_SYMBOL  0x5B12
#define TP_CRYSTALS 6
#define TP_SHARDS   10
#define TP_SYMBOL   (TP_CRYSTALS + TP_SHARDS)

static u16 LC1_Rainbow(u32 h)
{
    u32 s = (h & 0xFF) * 6, f = (s & 0xFF) * 31 >> 8;
    switch (s >> 8)
    {
    case 0: return RGB(31, f, 0);
    case 1: return RGB(31 - f, 31, 0);
    case 2: return RGB(0, 31, f);
    case 3: return RGB(0, 31 - f, 31);
    case 4: return RGB(f, 0, 31);
    default: return RGB(31, 0, 31 - f);
    }
}

static void TP_Init(void)
{
    u32 i;
    LI_ResetSprites();
    for (i = 0; i < TP_CRYSTALS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_TeraCrystal, 0x800, gBattleAnimSpritePal_TeraCrystal, TP_TAG_CRYSTAL, &sGI_Oam64Affine, 120, 80, 2);
    for (i = 0; i < TP_SHARDS; i++)
        LI_Make(TP_CRYSTALS + i, gBattleAnimSpriteGfx_TeraShatter, 0x180, gBattleAnimSpritePal_TeraShatter, TP_TAG_SHARD, &sGI_Oam16, 120, 80, 3);
    LI_Make(TP_SYMBOL, gBattleAnimSpriteGfx_TeraSymbol, 0x200, gBattleAnimSpritePal_TeraSymbol, TP_TAG_SYMBOL, &sGI_Oam32Affine, 120, 80, 1);
}

static bool32 TP_Update(s32 t)
{
    s32 sym = LC1_Beat(3), burst = LC1_Beat(4), end = burst + 22, i, R, th, flash = 0;
    u32 keep = GI_SpritePalBit(TP_TAG_CRYSTAL) | GI_SpritePalBit(TP_TAG_SHARD) | GI_SpritePalBit(TP_TAG_SYMBOL);
    u8 pal;
    struct Sprite *s;

    LC1_WorldReset(keep);
    GI_ResetPals(keep);
    LC1_TintFaded(LC1_WorldMask(keep), min(t / 2, 12), RGB(1, 2, 7));

    // banen: dichterbij, steeds sneller; na de klap uit elkaar
    if (t < burst)
        R = 124 - 92 * t / max(1, burst);
    else
        R = 32 + (t - burst) * (t - burst) * 2 + (t - burst) * 4;
    th = t * 2 + t * t / 50;
    for (i = 0; i < 4; i++)
    {
        s32 d = t - LC1_Beat(i);
        if (d >= 0 && d < 8)
            flash = max(flash, 12 - d * 3 / 2);
    }
    for (i = 0; i < TP_CRYSTALS; i++)
    {
        s32 a = th + i * 256 / TP_CRYSTALS, scale = 112 + 48 * min(t, burst) / max(1, burst); // 256 = ware grootte
        s = LI_S(i);
        s->invisible = (t < 2);
        s->x = 120 + Cos(a & 0xFF, R);
        s->y = 80 + Sin(a & 0xFF, R * 5 / 8);
        LI_Affine(sLI_Spr[i], scale, (u16)((t * 600) * ((i & 1) ? 1 : -1) + i * 9000));
    }
    for (i = 0; i < TP_SHARDS; i++)
    {
        s32 a = -th * 3 / 2 + i * 256 / TP_SHARDS;
        s = LI_S(TP_CRYSTALS + i);
        s->invisible = (t < 6);
        s->x = 120 + Cos(a & 0xFF, R + 30);
        s->y = 80 + Sin(a & 0xFF, (R + 30) * 5 / 8);
        LI_Frame(TP_CRYSTALS + i, TP_TAG_SHARD, (t / 4 + i) % 3, 4);
    }
    // het symbool groeit in het midden
    s = LI_S(TP_SYMBOL);
    if (t >= sym)
    {
        s32 u = t - sym, scale = min(400, 16 + u * 22);
        s->invisible = FALSE;
        LI_Affine(sLI_Spr[TP_SYMBOL], scale, (u16)(u * 900));
        if (u == 0)
            PlaySE(SE_SHINY);
    }

    // regenboogglans (kristallen en splinters), witte flits op de tel
    pal = IndexOfSpritePaletteTag(TP_TAG_CRYSTAL);
    if (pal != 0xFF)
        for (i = 1; i < 16; i++)
            gPlttBufferFaded[OBJ_PLTT_ID(pal) + i] = Tapu_Blend(gPlttBufferUnfaded[OBJ_PLTT_ID(pal) + i], LC1_Rainbow(t * 5 + i * 17), 4);
    pal = IndexOfSpritePaletteTag(TP_TAG_SHARD);
    if (pal != 0xFF)
        for (i = 1; i < 16; i++)
            gPlttBufferFaded[OBJ_PLTT_ID(pal) + i] = Tapu_Blend(gPlttBufferUnfaded[OBJ_PLTT_ID(pal) + i], LC1_Rainbow(t * 7 + i * 30 + 128), 8);
    pal = IndexOfSpritePaletteTag(TP_TAG_SYMBOL);
    if (pal != 0xFF)
        for (i = 1; i < 16; i++)
            gPlttBufferFaded[OBJ_PLTT_ID(pal) + i] = Tapu_Blend(gPlttBufferUnfaded[OBJ_PLTT_ID(pal) + i], LC1_Rainbow(t * 9 + i * 12), 10);
    LC1_TintFaded(keep, flash, RGB_WHITE);
    if (LC1_AT(0))
        PlaySE(SE_M_REFLECT);

    // de klap: Stellar-wit
    LC1_Flash(t, burst, 10, 16, PALETTES_ALL, RGB_WHITE);
    if (LC1_AT(burst))
    {
        PlaySE(SE_M_DETECT);
        LC1_PlayCry();
    }
    if (LC1_WhiteOut(t, end))
    {
        for (i = 0; i <= TP_SYMBOL; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void TP_Finish(void)
{
    LI_DestroySprites();
    GI_FreeTag(TP_TAG_CRYSTAL);
    GI_FreeTag(TP_TAG_SHARD);
    GI_FreeTag(TP_TAG_SYMBOL);
}

static const struct LCIntro sLC_Terapagos = {LC1_TEMPO_AREA_ZERO, TP_Init, TP_Update, TP_Finish};

static void Task_LegendTerapagos(u8 taskId)
{
    LC1_Run(taskId, &sLC_Terapagos);
}

// =====================================================================================================================
// Pecharunt: een paarse gifnevel trekt op (de wereld kleurt paars-roze en trilt als hete lucht), gifbellen stijgen op en
// knappen, pecha-bessen (het item-icoon) tuimelen op de halve tel naar beneden en stuiteren als mochi, en op de vierde
// tel slaan twee paarse ketens (Malignant Chain) het beeld in. Dan wordt de nevel zo dik dat alles roze-wit wordt.
#define PC_TAG_BERRY  0x5B20
#define PC_TAG_BUBBLE 0x5B21
#define PC_TAG_CHAIN  0x5B22
#define PC_BERRIES 6
#define PC_BUBBLES 10
#define PC_CHAIN   (PC_BERRIES + PC_BUBBLES)
#define PC_FLOOR   (128 << 4)

static const struct OamData sPC_Oam64x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(64x32),
    .size = SPRITE_SIZE(64x32),
    .priority = 0,
};

static const u8 sPC_BerryX[PC_BERRIES] = {44, 150, 96, 196, 70, 124};

static void PC_Init(void)
{
    u32 i;
    u8 id;
    struct SpriteTemplate tmpl = {
        .tileTag = PC_TAG_BERRY,
        .paletteTag = PC_TAG_BERRY,
        .oam = &sGI_Oam32Affine,
        .anims = gDummySpriteAnimTable,
        .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable,
        .callback = SpriteCallbackDummy,
    };

    LI_ResetSprites();
    id = AddItemIconSprite(PC_TAG_BERRY, PC_TAG_BERRY, ITEM_PECHA_BERRY);
    if (id < MAX_SPRITES)
        DestroySprite(&gSprites[id]);
    for (i = 0; i < PC_BERRIES; i++)
    {
        id = CreateSprite(&tmpl, sPC_BerryX[i], -24, 1);
        sLI_Spr[i] = id;
        if (id < MAX_SPRITES)
        {
            gSprites[id].invisible = TRUE;
            gSprites[id].affineAnimPaused = TRUE;
            SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, 256, 256, 0);
        }
        sLI_Phys[i][0] = sPC_BerryX[i] << 4;
        sLI_Phys[i][1] = -24 << 4;
        sLI_Phys[i][2] = ((s32)(i & 1) * 2 - 1) * (4 + i);
        sLI_Phys[i][3] = 0;
    }
    for (i = 0; i < PC_BUBBLES; i++)
        LI_Make(PC_BERRIES + i, gBattleAnimSpriteGfx_PoisonBubble, 0x180, gBattleAnimSpritePal_PoisonBubble, PC_TAG_BUBBLE, &sGI_Oam16, 16 + i * 23, 176, 2);
    LI_Make(PC_CHAIN, gBattleAnimSpriteGfx_PurpleChain, 0x1000, gBattleAnimSpritePal_PurpleChain, PC_TAG_CHAIN, &sPC_Oam64x32, -40, 62, 0);
    LI_Make(PC_CHAIN + 1, gBattleAnimSpriteGfx_PurpleChain, 0x1000, gBattleAnimSpritePal_PurpleChain, PC_TAG_CHAIN, &sPC_Oam64x32, 280, 100, 0);
    if (sLI_Spr[PC_CHAIN + 1] < MAX_SPRITES)
        gSprites[sLI_Spr[PC_CHAIN + 1]].oam.matrixNum = ST_OAM_HFLIP;
    LC1_StartLines(LCF_HOFS);
}

static bool32 PC_Update(s32 t)
{
    s32 chains = LC1_Beat(4), thick = LC1_Beat(5), end = thick + 14, i, y, k;
    u32 keep = GI_SpritePalBit(PC_TAG_BERRY) | GI_SpritePalBit(PC_TAG_BUBBLE) | GI_SpritePalBit(PC_TAG_CHAIN);
    u16 *h = sLC1->back[LCB_HOFS];
    struct Sprite *s;

    // nevel
    LC1_WorldReset(keep);
    GI_ResetPals(keep);
    k = min(t / 3, 9);
    LC1_TintFaded(LC1_WorldMask(keep), k, RGB(22, 6, 20));
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        h[y] = (sTransitionData->cameraX + Sin((y * 4 + t * 3) & 0xFF, min(t / 25, 2))) & 0x1FF;
    if (LC1_AT(0))
        PlaySE(SE_M_TOXIC);

    // gifbellen: stijgen, knappen, opnieuw
    for (i = 0; i < PC_BUBBLES; i++)
    {
        s32 per = 46 + (i * 7) % 23, ph = (t + i * 13) % per, spd = 3 + (i % 3);
        s = LI_S(PC_BERRIES + i);
        s->invisible = (t < i * 3);
        s->x = 16 + i * 23 + Sin((t * 3 + i * 40) & 0xFF, 4);
        if (ph < per - 6)
        {
            s->y = 172 - ph * spd;
            LI_Frame(PC_BERRIES + i, PC_TAG_BUBBLE, 0, 4);
        }
        else
        {
            s->y = 172 - (per - 6) * spd;
            LI_Frame(PC_BERRIES + i, PC_TAG_BUBBLE, 2, 4);
            if (ph == per - 6 && (i & 3) == 0)
                PlaySE(SE_M_BUBBLE);
        }
    }

    // pecha-bessen: vallen op de halve tel, stuiteren als mochi
    for (i = 0; i < PC_BERRIES; i++)
    {
        s16 *p = sLI_Phys[i];
        s32 st = LC1_Beat2(i), sq = 256;
        s = LI_S(i);
        if (t < st)
            continue;
        s->invisible = FALSE;
        p[3] += 5;
        p[0] += p[2];
        p[1] += p[3];
        if (p[1] > PC_FLOOR && p[3] > 0)
        {
            sq = 256 + min(p[3] * 3, 140); // platgedrukt
            p[1] = PC_FLOOR;
            p[3] = -p[3] * 3 / 5;
            if (abs(p[3]) < 12)
                p[3] = 0;
            if (i < 3)
                PlaySE(SE_BALL_BOUNCE_1);
        }
        s->x = p[0] >> 4;
        s->y = p[1] >> 4;
        if (sLI_Spr[i] < MAX_SPRITES)
            SetOamMatrixRotationScaling(gSprites[sLI_Spr[i]].oam.matrixNum, 256 * 256 / sq, sq, (u16)(t * p[2] * 90));
    }

    // de ketens slaan in
    for (i = 0; i < 2; i++)
    {
        s32 u = t - chains - i * 3;
        s = LI_S(PC_CHAIN + i);
        if (u < 0)
            continue;
        s->invisible = FALSE;
        LI_Frame(PC_CHAIN + i, PC_TAG_CHAIN, min(u / 2, 3), 32);
        s->x = i ? max(196, 280 - u * 14) : min(44, -40 + u * 14);
        s->y = (i ? 100 : 62) + Sin((u * 16) & 0xFF, 3);
        if (u == 0)
            PlaySE(SE_M_BIND);
    }
    if (LC1_AT(LC1_Beat(3)))
        LC1_PlayCry();

    // de nevel wordt dik
    if (t >= thick)
        LC1_TintFaded(PALETTES_ALL, min((t - thick) * 2, 14), RGB(31, 16, 28));
    if (LC1_WhiteOut(t, end))
    {
        for (i = 0; i < PC_CHAIN + 2; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void PC_Finish(void)
{
    LI_DestroySprites();
    GI_FreeTag(PC_TAG_BERRY);
    GI_FreeTag(PC_TAG_BUBBLE);
    GI_FreeTag(PC_TAG_CHAIN);
}

static const struct LCIntro sLC_Pecharunt = {LC1_TEMPO_LEGENDARY, PC_Init, PC_Update, PC_Finish};

static void Task_LegendPecharunt(u8 taskId)
{
    LC1_Run(taskId, &sLC_Pecharunt);
}
