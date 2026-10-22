// Project Grounded: goedkope legendary-intro's (Jordi: "maak deze intro's goedkoop qua kbs"). Calyrex/Glastrier/
// Spectrier, Celebi, het meren-trio, Meloetta, Latias/Latios, Zeraora, Cresselia, de Galar-vogels en Zygarde.
// Geen eigen art: alle BG0-beelden worden bij de start in C getekend (gradiënten met Bayer-dither, boomsilhouetten,
// ijs, slagen, de sikkelmaan, het zeshoekraster) en de rest is gevechtsanimatie-art die al in de ROM staat. Geen
// Pokémon-sprites (Jordi: "ik vind het vaak beter wanneer je de sprites weglaat, lijkt minder budget"). Wordt onderaan
// src/battle_transition.c ingevoegd, na de andere legendary-intro's (gebruikt de GI_/LI_/LI2_-hulpjes, Tapu_Blend,
// Tapu_Elapsed en de route-transitie-runner).
// Op de muziek (MUS_GROUNDED_VS_LEGENDARY, 176 bpm, pauken in achtsten): t = echte VBlanks sinds de start van de
// transitie (= de start van de muziek). De buisklok op maat 3 (LC_HIT) is het hoogtepunt van elk intro.

#define LC_E8(e)      ((e) * 10181 / 1000)   // achtste noot e in frames (176 bpm bij 59,73 Hz)
#define LC_BEAT(b)    ((b) * 20363 / 1000)   // tel b
#define LC_HIT        163                    // maat 3, tel 1 (de buisklok)
#define LC_SHOW       0                      // r (frames sinds het eigen deel begint, na het grijze flitsen
                                             // van de transitie, rond t = 48): het eigen beeld verschijnt
#define LC_MAX_TILES  500
#define tLcLast       data[12]               // vorige t (eenmalige gebeurtenissen, ook bij overgeslagen frames)
#define tLcVar        data[13]               // variant (soort)
#define tLcGen        data[14]               // rijen van het beeld die al getekend zijn

struct LCWork
{
    u16 map[32 * 20];
    u16 order[600];
    u8 top[256];
    u8 rowv[DISPLAY_HEIGHT];
    u8 cell[160];
    u8 frame[160];
    u16 tmp[16];
    u8 shade[512];          // Celebi: GB-tint per kleur
    u32 hash[LC_MAX_TILES]; // LC_PaintRowsDedup
    u32 spr[32];            // Zygarde: een Cell (16x16)
    u8 hexloc[16 * 24];     // Zygarde: het zeshoekraster per blok
    u16 nextTile;
    u8 curPhase, curVar;
    u8 matLand, matSet;
    bool8 outFrozen;
    u32 seed;
    s32 t0;
};

static EWRAM_DATA struct LCWork *sLC = NULL;
static EWRAM_DATA u32 *sLCCanvas = NULL; // tiles 16 .. LC_MAX_TILES-1, eerst in EWRAM getekend

static const u32 sLC_BlankTile[8] = {0};
static const u16 sLC_Pal0[16] = {0};

typedef u32 (*LCPixel)(s32 x, s32 y);   // kleurindex 0-15
typedef u32 (*LCCell)(s32 cx, s32 cy);  // palet << 12, of LC_EMPTY

#define LC_EMPTY 0xFFFF
#define LC_PLAIN 0x0800   // cel hangt alleen van de rij af (gradiënt)

static u32 *LC_Tile(u32 n)
{
    u16 *tilemap, *tileset;
    GetBg0TilesDst(&tilemap, &tileset);
    return (u32 *)tileset + n * 8;
}

// tiles 1-15: één kleur (index = tilenummer)
static void LC_Begin(struct Task *task, u32 seed)
{
    u32 i;
    sLC = AllocZeroed(sizeof(*sLC));
    if (sLC == NULL)
        return;
    sLC->seed = seed;
    sLC->nextTile = 16;
    sLC->matLand = sLC->matSet = 0xFF;
    sLC->t0 = -1;
    for (i = 1; i < 16; i++)
        CpuFill32(i * 0x11111111, LC_Tile(i), 32);
    task->tLcLast = -1;
    task->tLcGen = 0;
    // de tijd-van-de-dag-update (elke minuut) zet de paletten van de wereld terug: tijdens het intro even niet
    if (gTimeUpdateCounter < 600)
        gTimeUpdateCounter = 600;
    LI_ResetSprites();
}

static void LC_EndWork(void)
{
    TRY_FREE_AND_SET_NULL(sLC);
}

// frames sinds de eerste update (het eigen deel); t blijft de muziektijd
static s32 LC_R(s32 t)
{
    if (sLC->t0 < 0)
        sLC->t0 = t;
    return t - sLC->t0;
}

static bool32 LC_Cross(struct Task *task, s32 t, s32 x)
{
    return task->tLcLast < x && t >= x;
}

// zoals LC_PaintRows, maar ontdubbelt over het hele beeld (hash per tile; voor herhalende patronen zoals een raster)
static void LC_PaintRowsDedup(LCPixel px, LCCell cell, u32 r0, u32 r1)
{
    u32 buf[8], cx, cy, x, y, any, h, c, n;
    for (cy = r0; cy < r1 && cy < 20; cy++)
    {
        for (cx = 0; cx < 32; cx++)
        {
            u16 *m = &sLC->map[cy * 32 + cx];
            c = cell(cx, cy);
            if (c == LC_EMPTY)
            {
                *m = 0;
                continue;
            }
            c &= ~LC_PLAIN;
            any = h = 0;
            for (y = 0; y < 8; y++)
            {
                u32 w = 0;
                for (x = 0; x < 8; x++)
                    w |= (px(cx * 8 + x, cy * 8 + y) & 15) << (x * 4);
                buf[y] = w;
                any |= w;
                h = h * 0x9E3779B1 + w;
            }
            if (any == 0)
            {
                *m = 0;
                continue;
            }
            for (n = 16; n < sLC->nextTile; n++)
                if (sLC->hash[n] == h && memcmp(buf, LC_Tile(n), sizeof(buf)) == 0)
                    break;
            if (n == sLC->nextTile)
            {
                if (n >= LC_MAX_TILES)
                {
                    *m = 0;
                    continue;
                }
                CpuCopy32(buf, LC_Tile(n), 32);
                sLC->hash[n] = h;
                sLC->nextTile++;
            }
            *m = n | c;
        }
    }
}

static bool32 LC_GenRowsDedup(struct Task *task, LCPixel px, LCCell cell, u32 rows)
{
    if (sLC == NULL || task->tLcGen >= 20)
        return TRUE;
    LC_PaintRowsDedup(px, cell, task->tLcGen, task->tLcGen + rows);
    task->tLcGen += rows;
    return task->tLcGen >= 20;
}

static void LC_ShowMap(void)
{
    if (sLC != NULL)
        CpuCopy16(sLC->map, RT_Tilemap(), 32 * 20 * 2);
}

static void LC_SetBgPal(u32 n, const u16 *cols)
{
    CpuCopy16(cols, &gPlttBufferUnfaded[BG_PLTT_ID(13 + n)], PLTT_SIZE_4BPP);
    CpuCopy16(cols, &gPlttBufferFaded[BG_PLTT_ID(13 + n)], PLTT_SIZE_4BPP);
}

static void LC_FreeMatrices(u32 n)
{
    u32 i;
    for (i = 0; i < n; i++)
    {
        struct Sprite *s = LI_S(i);
        if (sLI_Spr[i] < MAX_SPRITES && s->oam.affineMode != ST_OAM_AFFINE_OFF
         && (s->oam.matrixNum == sLC->matLand || s->oam.matrixNum == sLC->matSet))
        {
            s->oam.affineMode = ST_OAM_AFFINE_OFF;
            s->oam.matrixNum = 0;
        }
    }
    if (sLC->matLand != 0xFF)
        FreeOamMatrix(sLC->matLand);
    if (sLC->matSet != 0xFF)
        FreeOamMatrix(sLC->matSet);
    sLC->matLand = sLC->matSet = 0xFF;
}

static u16 LC_EnemySpecies(void)
{
    return GetMonData(&gEnemyParty[0], MON_DATA_SPECIES, NULL);
}

// de wereld (alles behalve BG 13-15 en 'keep') naar 'color'
static void LC_DimWorld(s32 t, u32 keep, s32 maxK, u16 color)
{
    BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, min(max(t, 0) * 2, maxK), color);
}

// BG0 telt op bij alles eronder (zwart = niets)
static void LC_Additive(u32 eva)
{
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                               | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(eva, 16));
    SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
}

// eindflits: vanaf 'start' in 'len' frames naar 'color' (mask), TRUE als het klaar is
static bool32 LC_Out(s32 t, s32 start, s32 len, u32 mask, u16 color)
{
    s32 k;
    if (t < start)
        return FALSE;
    if (!sLC->outFrozen)
    {
        // vanaf het getoonde beeld (gedimde wereld) blenden, niet vanaf de oorspronkelijke kleuren
        CpuCopy16(gPlttBufferFaded, gPlttBufferUnfaded, PLTT_SIZE);
        sLC->outFrozen = TRUE;
    }
    k = min(16, (t - start + 1) * 16 / len);
    BlendPalettes(mask, k, color);
    return t >= start + len;
}

static void LC_FinishCommon(struct Task *task)
{
    GI_Shake(0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    if (sLC != NULL)
        LC_FreeMatrices(LI_SPRITES);
    LI_DestroySprites();
    LC_EndWork();
    TRY_FREE_AND_SET_NULL(sLCCanvas);
}

// =====================================================================================================================
// ---------------- lijnen (slagen, scheuren, strepen) als BG0-beeld dat optelt bij de wereld
// Elke lijn: kern (index idx + stap) en gloed (index idx + stap + 7) langs de lijn in 'steps' stappen (zo kan een slag
// zich in een paar frames over het beeld trekken), optioneel gekarteld (bliksem) en met een aura (index 15).
struct LCStroke
{
    s16 x0, y0, x1, y1;
    u8 core, glow, aura;
    u8 idx, steps, jag;
    u8 pal; // 0-2 (BG-palet 13-15)
};

#define LC_MAX_STROKES 16
#define LC_STROKES_PER_FRAME 3

// =====================================================================================================================
// Zygarde (alle vormen; Jordi: "google hoe Zygarde behandeld wordt in de games, die Z is heel anders"): de Order-
// Pokémon bestaat uit Cores en Cells, in de games altijd groen-zwarte zeshoeken die oplichten (Power Construct: de
// Cells verzamelen zich; Core Enforcer in Legends Z-A: een hoofdletter Z op de grond). De plek wordt zwart en er
// verschijnt een zeshoekraster (BG0, optellend) dat op elke tel vanuit de Z een golf uitzendt. In het midden licht de
// Core op (de rode zeshoek), en op de achtsten vliegen groene Cells van alle kanten naar binnen; elke landing zet een
// stuk van de Z van zeshoeken aan, van linksboven tot rechtsonder. Op tel 7 is de Z af en gloeit wit, en het beeld
// breekt langs het raster: de naden worden wit van de Z naar buiten, alles trilt, en op de klokslag een groene flits.
// Geen Pokémon-sprite.
#define LCY_CELLS      16            // twee per stuk van de Z
#define LCY_TAG_CELL   0x5B2F
#define LCY_FLY        18            // vliegtijd van een Cell
#define LCY_E0         6             // eerste landing: achtste 6 (tel 3)
#define LCY_BREAK      LC_BEAT(7)
#define LCY_HX         18            // zeshoeken: i -1..16, j -1..14
#define LCY_HY         16
#define LCY_Z_LEN      455           // lengte van de Z (144 + 167 + 144)

static const u16 sLCY_CellPal[16] = {0, RGB(6, 28, 10), RGB(1, 10, 4), RGB(20, 31, 18)};

// de Z: boven (48,36)-(192,36), schuin naar (48,120), onder naar (192,120); afstand en positie langs de Z
static s32 LCY_ZDist(s32 x, s32 y, s32 *along)
{
    static const s16 sZ[4][2] = {{48, 36}, {192, 36}, {48, 120}, {192, 120}};
    s32 k, best = 0x7FFFFFFF, base = 0;
    for (k = 0; k < 3; k++)
    {
        s32 x0 = sZ[k][0], y0 = sZ[k][1], dx = sZ[k + 1][0] - x0, dy = sZ[k + 1][1] - y0;
        s32 len2 = dx * dx + dy * dy, len = (k == 1) ? 167 : 144, u, px, py, d2;
        u = ((x - x0) * dx + (y - y0) * dy) * 256 / len2;
        u = u < 0 ? 0 : (u > 256 ? 256 : u);
        px = x0 + dx * u / 256 - x;
        py = y0 + dy * u / 256 - y;
        d2 = px * px + py * py;
        if (d2 < best)
        {
            best = d2;
            *along = base + len * u / 256;
        }
        base += len;
    }
    return best;
}

// zeshoek (i, j): midden (16i + 8 (j oneven), 12j); sLC->order[(j+1)*18 + i+1] = vulkleur | ring << 8
static u32 LCY_Hex(s32 i, s32 j)
{
    if (i < -1 || i > 16 || j < -1 || j > 14)
        return 4 << 8;
    return sLC->order[(j + 1) * LCY_HX + i + 1];
}

// het raster herhaalt zich per 16 x 24 pixels: per pixel in dat blok staat de dichtstbijzijnde zeshoek (a), de
// tweede (b) en of het een naad is (sLC->hexloc, bij de start berekend: per pixel delen kan de GBA niet snel)
static const s8 sLCY_Cand[7][2] = {{0, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}, {0, 2}, {1, 2}};

static u32 LCY_Pixel(s32 x, s32 y)
{
    u32 v = sLC->hexloc[sLC->rowv[y] * 16 + (x & 15)], a = v & 7, b = (v >> 3) & 7;
    s32 bx = x >> 4, by = sLC->top[y] * 2;
    if (v & 0x40)
    {
        u32 ra = LCY_Hex(bx + sLCY_Cand[a][0], by + sLCY_Cand[a][1]) >> 8;
        u32 rb = LCY_Hex(bx + sLCY_Cand[b][0], by + sLCY_Cand[b][1]) >> 8;
        return 1 + min(ra, rb);           // naad: kleur 1-5 naar de ring
    }
    return LCY_Hex(bx + sLCY_Cand[a][0], by + sLCY_Cand[a][1]) & 0xFF;  // stuk van de Z (6-13), Core (14) of leeg (15)
}

static u32 LCY_Cell(s32 cx, s32 cy)
{
    return 13 << 12;
}

static void RTZygarde_Init(struct Task *task)
{
    s32 i, j, along, d2, best = 0x7FFFFFFF, core = 0, sx[8] = {0}, sy[8] = {0}, sn[8] = {0};
    u32 x, y;
    LC_Begin(task, 0x2A6D);
    if (sLC == NULL)
        return;
    for (j = -1; j <= 14; j++)
    {
        for (i = -1; i <= 16; i++)
        {
            s32 cx = 16 * i + ((j & 1) ? 8 : 0), cy = 12 * j, g, ring;
            u16 *h = &sLC->order[(j + 1) * LCY_HX + i + 1];
            d2 = LCY_ZDist(cx, cy, &along);
            if (d2 <= 7 * 7)
            {
                g = min(7, along * 8 / LCY_Z_LEN);
                *h = 6 + g;
                sx[g] += cx, sy[g] += cy, sn[g]++;
                d2 = (cx - 120) * (cx - 120) + (cy - 78) * (cy - 78);
                if (d2 < best)
                    best = d2, core = (j + 1) * LCY_HX + i + 1;
            }
            else
            {
                for (ring = 1; ring < 4 && d2 > (7 + ring * 16) * (7 + ring * 16); ring++)
                    ;
                *h = 15 | (ring << 8);
            }
        }
    }
    sLC->order[core] = 14;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        sLC->top[y] = y / 24;
        sLC->rowv[y] = y % 24;
    }
    for (y = 0; y < 24; y++)
    {
        for (x = 0; x < 16; x++)
        {
            s32 d[7], a = 0, b = 1, n;
            for (n = 0; n < 7; n++)
            {
                s32 dx = (s32)x - (16 * sLCY_Cand[n][0] + ((sLCY_Cand[n][1] & 1) ? 8 : 0)), dy = (s32)y - 12 * sLCY_Cand[n][1];
                d[n] = dx * dx + dy * dy;
            }
            if (d[1] < d[0])
                a = 1, b = 0;
            for (n = 2; n < 7; n++)
            {
                if (d[n] < d[a])
                    b = a, a = n;
                else if (d[n] < d[b])
                    b = n;
            }
            sLC->hexloc[y * 16 + x] = a | (b << 3) | ((d[b] - d[a] < 20) ? 0x40 : 0);
        }
    }
    for (i = 0; i < 8; i++)
    {
        sLC->cell[i] = sn[i] ? sx[i] / sn[i] : 120;
        sLC->frame[i] = sn[i] ? sy[i] / sn[i] : 80;
    }
    // een Cell: groene zeshoek met een donkere rand en een lichte kern
    CpuFill32(0, sLC->spr, sizeof(sLC->spr));
    for (y = 0; y < 16; y++)
    {
        for (x = 0; x < 16; x++)
        {
            s32 dx = abs((s32)x * 2 - 15), dy = abs((s32)y * 2 - 15), v = 0;
            if (dx <= 13 && dx / 2 + dy <= 15)
                v = (dx >= 11 || dx / 2 + dy >= 13) ? 2 : ((dx + dy <= 6) ? 3 : 1);
            sLC->spr[((y / 8) * 2 + x / 8) * 8 + (y & 7)] |= v << ((x & 7) * 4);
        }
    }
    {
        struct SpriteSheet sheet = {sLC->spr, sizeof(sLC->spr), LCY_TAG_CELL};
        LoadSpriteSheet(&sheet);
    }
    for (i = 0; i < LCY_CELLS; i++)
        LI_Make(i, (const u32 *)sLC->spr, sizeof(sLC->spr), sLCY_CellPal, LCY_TAG_CELL, &sGI_Oam16, 0, 0, 1);
    LC_Additive(14);
}

static bool8 RTZygarde_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, b, ph;
    u32 keep;
    struct Sprite *s;
    u16 cols[16], green = RGB(6, 28, 10);

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCY_TAG_CELL);
    GI_ResetPals(keep);
    if (task->tLcGen < 20)
    {
        LC_GenRowsDedup(task, LCY_Pixel, LCY_Cell, 4);
        if (task->tLcGen >= 20)
            LC_ShowMap();
    }
    LC_DimWorld(r, keep, 14, RGB(0, 2, 1));
    b = t * 1000 / 20363;
    ph = t - LC_BEAT(b);

    // het raster: ringen verschijnen vanuit de Z, op elke tel een golf naar buiten, bij het breken wit
    cols[0] = 0;
    for (k = 0; k < 5; k++)
    {
        s32 on = r - 10 - k * 3, w = ph - k * 2;
        u16 c = on < 0 ? 0 : Tapu_Blend(0, k ? RGB(1, 9, 3) : RGB(2, 13, 5), min(16, on * 3));
        if (t >= LC_BEAT(3) && on >= 0 && w >= 0 && w < 4)
            c = Tapu_Blend(c, green, 12 - w * 3);
        if (t >= LCY_BREAK + k * 3)
            c = Tapu_Blend(green, RGB(28, 31, 28), min(16, (t - LCY_BREAK - k * 3) * 4));
        cols[1 + k] = c;
    }
    // de Z: elk stuk licht op als zijn Cells landen
    for (k = 0; k < 8; k++)
    {
        s32 a = t - LC_E8(LCY_E0 + k);
        u16 c = a < 0 ? 0 : (a < 2 ? RGB_WHITE : green);
        if (a >= 2 && ph < 4)
            c = Tapu_Blend(c, RGB(22, 31, 20), 8 - ph * 2);
        if (t >= LCY_BREAK)
            c = Tapu_Blend(green, RGB(30, 31, 30), min(16, (t - LCY_BREAK) * 2));
        cols[6 + k] = c;
    }
    // de Core: klopt rood op de tel
    k = r - 6;
    cols[14] = k < 0 ? 0 : Tapu_Blend(RGB(14, 1, 3), RGB(31, 6, 8), (ph < 6) ? 16 - ph * 2 : 4);
    if (t >= LCY_BREAK)
        cols[14] = Tapu_Blend(cols[14], RGB_WHITE, min(16, (t - LCY_BREAK) * 2));
    // binnenkant van de zeshoeken: pas bij het breken
    k = t - LCY_BREAK - 10;
    cols[15] = k < 0 ? 0 : Tapu_Blend(0, RGB(6, 20, 8), min(16, k * 2));
    LC_SetBgPal(0, cols);

    // de Cells vliegen naar hun stuk van de Z
    for (i = 0; i < LCY_CELLS; i++)
    {
        s32 g = i / 2, land = LC_E8(LCY_E0 + g), a = (i * 89 + 40) & 0xFF, p;
        s = LI_S(i);
        k = t - (land - LCY_FLY);
        s->invisible = k < 0 || t >= land;
        if (s->invisible)
            continue;
        p = k * k * 256 / (LCY_FLY * LCY_FLY);
        s->x = 120 + Cos(a, 170) + ((sLC->cell[g] + ((i & 1) ? 8 : -8)) - 120 - Cos(a, 170)) * p / 256;
        s->y = 80 + Sin(a, 110) + (sLC->frame[g] - 80 - Sin(a, 110)) * p / 256;
    }

    for (k = 0; k < 8; k += 2)
        if (LC_Cross(task, t, LC_E8(LCY_E0 + k)))
            PlaySE(SE_M_LOCK_ON);
    if (LC_Cross(task, t, sLC->t0 + 6))
        PlaySE(SE_M_DETECT);
    if (LC_Cross(task, t, LCY_BREAK))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    if (LC_Cross(task, t, LCY_BREAK + 8))
        PlaySE(SE_M_BRICK_BREAK);
    GI_Shake(t >= LCY_BREAK + 8 ? 1 + (t - LCY_BREAK - 8) / 4 : 0);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(20, 31, 20));
}

static void RTZygarde_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCY_TAG_CELL);
}

static const struct RouteTransition sRT_LegendZygarde =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTZygarde_Init, RTZygarde_Update, RTZygarde_Finish
};

static void Task_LegendZygarde(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendZygarde);
}
