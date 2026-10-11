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

static const u8 sLC_Bayer[16] = {0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5};
static const u32 sLC_BlankTile[8] = {0};
static const u16 sLC_Pal0[16] = {0};

typedef u32 (*LCPixel)(s32 x, s32 y);   // kleurindex 0-15
typedef u32 (*LCCell)(s32 cx, s32 cy);  // palet << 12, of LC_EMPTY

#define LC_EMPTY 0xFFFF
#define LC_PLAIN 0x0800   // cel hangt alleen van de rij af (gradiënt)

static u32 LC_Rand(void)
{
    sLC->seed = sLC->seed * 1103515245 + 12345;
    return (sLC->seed >> 16) & 0x7FFF;
}

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

// gradiënt over 'rows' beeldlijnen: rowv[y] = positie * 16 (voor de Bayer-dither)
static void LC_RowGradient(u32 y0, u32 y1, u32 n)
{
    u32 y;
    for (y = y0; y < y1 && y < DISPLAY_HEIGHT; y++)
        sLC->rowv[y] = (y - y0) * (n - 1) * 16 / (y1 - y0);
}

static u32 LC_Grad(s32 x, s32 y, u32 n)
{
    u32 i = 1 + ((sLC->rowv[y] + sLC_Bayer[(y & 3) * 4 + (x & 3)]) >> 4);
    return i > n ? n : i;
}

// tekent rij r0 tot r1 (32 kolommen) in de tilemapbuffer; gelijke tiles naast elkaar worden gedeeld, en een LC_PLAIN-
// cel krijgt de tile van de eerste LC_PLAIN-cel in zijn rij (zonder te tekenen)
static void LC_PaintRows(LCPixel px, LCCell cell, u32 r0, u32 r1)
{
    u32 buf[8], prev[8];
    u32 cx, cy, x, y, any, prevTile, c, plain, plainTile;
    bool32 prevOk;

    for (cy = r0; cy < r1 && cy < 20; cy++)
    {
        prevOk = FALSE;
        prevTile = 0;
        plainTile = 0;
        for (cx = 0; cx < 32; cx++)
        {
            u16 *m = &sLC->map[cy * 32 + cx];
            c = cell(cx, cy);
            if (c == LC_EMPTY)
            {
                *m = 0;
                prevOk = FALSE;
                continue;
            }
            plain = c & LC_PLAIN;
            c &= ~LC_PLAIN;
            if (plain && plainTile)
            {
                *m = plainTile;
                continue;
            }
            any = 0;
            for (y = 0; y < 8; y++)
            {
                u32 w = 0;
                for (x = 0; x < 8; x++)
                    w |= (px(cx * 8 + x, cy * 8 + y) & 15) << (x * 4);
                buf[y] = w;
                any |= w;
            }
            if (any == 0)
            {
                *m = 0;
                continue;
            }
            if (prevOk && memcmp(buf, prev, sizeof(buf)) == 0)
            {
                *m = prevTile | c;
            }
            else if (sLC->nextTile >= LC_MAX_TILES)
            {
                *m = prevOk ? (prevTile | c) : 0;
            }
            else
            {
                CpuCopy32(buf, LC_Tile(sLC->nextTile), 32);
                memcpy(prev, buf, sizeof(buf));
                prevTile = sLC->nextTile++;
                prevOk = TRUE;
                *m = prevTile | c;
            }
            if (plain)
                plainTile = *m;
        }
    }
}

// het beeld tekenen, 'rows' rijen per aanroep; geeft TRUE als het klaar is
static bool32 LC_GenRows(struct Task *task, LCPixel px, LCCell cell, u32 rows)
{
    if (sLC == NULL || task->tLcGen >= 20)
        return TRUE;
    LC_PaintRows(px, cell, task->tLcGen, task->tLcGen + rows);
    task->tLcGen += rows;
    return task->tLcGen >= 20;
}

static bool32 LC_Gen(struct Task *task, s32 t, LCPixel px, LCCell cell)
{
    return LC_GenRows(task, px, cell, 20);
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

// een palet naar een kleurverloop van 'dark' (donker) tot 'light' (licht) op helderheid
static const u16 *LC_Tint(const u16 *src, u16 dark, u16 light)
{
    u32 i;
    sLC->tmp[0] = src[0];
    for (i = 1; i < 16; i++)
    {
        u16 c = src[i];
        s32 l = ((c & 31) * 2 + ((c >> 5) & 31) * 3 + ((c >> 10) & 31)) * 16 / (31 * 6);
        sLC->tmp[i] = Tapu_Blend(dark, light, l);
    }
    return sLC->tmp;
}

// kleuren in een palet ronddraaien: r -> g -> b
static const u16 *LC_Rotate(const u16 *src, u32 times)
{
    u32 i, k;
    for (i = 0; i < 16; i++)
    {
        u16 c = src[i];
        for (k = 0; k < times; k++)
            c = ((c & 31) << 5) | (((c >> 5) & 31) << 10) | ((c >> 10) & 31);
        sLC->tmp[i] = c;
    }
    return sLC->tmp;
}

static u16 LC_Mix3(u16 a, u16 b, u16 c, s32 k, s32 n)
{
    // k van 0 tot n: a -> b -> c
    if (k * 2 <= n)
        return Tapu_Blend(a, b, k * 32 / n);
    return Tapu_Blend(b, c, (k * 2 - n) * 16 / n);
}

// een sprite die met een gedeelde matrix schaalt en draait (affine, dubbele grootte)
static void LC_UseMatrix(struct Sprite *s, u8 mat, u8 shape, u8 size)
{
    if (mat == 0xFF || s == NULL)
        return;
    s->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    s->oam.matrixNum = mat;
    CalcCenterToCornerVec(s, shape, size, ST_OAM_AFFINE_DOUBLE);
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

// boomsilhouet (dennen): top[x] = bovenkant van het bos in kolom x
static void LC_Pines(u32 base, u32 lo, u32 hi, u32 spacing, u32 slope)
{
    s32 x, cx;
    for (x = 0; x < 256; x++)
        sLC->top[x] = base;
    for (cx = -8; cx < 264; cx += spacing / 2 + LC_Rand() % spacing)
    {
        s32 peak = lo + LC_Rand() % (hi - lo + 1);
        for (x = max(cx - 40, 0); x < min(cx + 40, 256); x++)
        {
            s32 d = abs(x - cx), v = peak + d * slope / 4 + ((d % 6) >= 4 ? 1 : 0);
            if (v < sLC->top[x])
                sLC->top[x] = v;
        }
    }
}

// =====================================================================================================================
// Calyrex, Glastrier, Spectrier (Crown Tundra-quest; Jordi: "Calyrex krijgt een soort forest protector horse riding
// cowboy theme. Glastrier zet ijsstappen, Spectrier ghost stappen."). Hoefafdrukken (het hoefijzer uit de Mega Punch-
// art) galopperen in achtsten over het beeld, op de pauken van het legendary-thema.
// - Calyrex (alle vormen): western bij zonsondergang. Een gedithered avondlucht, een halve zon achter het bos van de
//   beschermer, stofwolkjes bij elke stap; boven de zon zwiept een lasso rond, op de klokslag vliegt hij naar je toe
//   en licht het bos groen op. De ruiters zetten de stappen van hun paard (ijs of spookvuur).
// - Glastrier: de echte plek wordt koud blauw, elke stap bevriest (ijskristal) en de rijp groeit vanuit de afdrukken
//   over het hele beeld (BG0 telt op bij de wereld; 15 groeifasen in de paletkleuren).
// - Spectrier: de plek wordt zwartpaars, elke afdruk vat paars spookvuur en dooft weer.
enum { LCR_CALYREX, LCR_CALYREX_ICE, LCR_CALYREX_SHADOW, LCR_GLASTRIER, LCR_SPECTRIER };
#define LCR_PRINTS     11
#define LCR_E0         5     // eerste stap: achtste 5 (t 51), het eigen deel begint rond t 48
#define LCR_LASSO      (2 * LCR_PRINTS)
#define LCR_TAG_SHOE   0x5B20
#define LCR_TAG_FX     0x5B21
#define LCR_TAG_ROPE   0x5B22
#define LCR_HORIZON    112
#define LCR_SKY_N      11
#define LCR_MON_SHOW   102   // tel 5
#define LCR_END        (LC_HIT + 6)

static bool32 LCR_Sunset(u32 v)
{
    return v <= LCR_CALYREX_SHADOW;
}

static u32 LCR_Step(u32 v)
{
    if (v == LCR_CALYREX_ICE || v == LCR_GLASTRIER)
        return 1;
    if (v == LCR_CALYREX_SHADOW || v == LCR_SPECTRIER)
        return 2;
    return 0;
}

static void LCR_PrintPos(u32 e, bool32 sunset, s16 *x, s16 *y)
{
    *x = -6 + (e - LCR_E0 + 1) * 22;
    if (sunset)
        *y = 134 + ((e & 1) ? -7 : 7) + Sin((e * 20) & 0xFF, 3);
    else
        *y = 84 + ((e & 1) ? -8 : 8) + Sin((e * 18) & 0xFF, 22);
}

static u32 LCR_SunsetPixel(s32 x, s32 y)
{
    s32 dx, dy, d2;
    if (y >= LCR_HORIZON)
        return LC_Grad(x, y, 4);
    if (y >= sLC->top[x])
        return 15;
    dx = x - 120;
    dy = y - 102;
    d2 = dx * dx + dy * dy;
    if (d2 < 34 * 34)
        return d2 > 30 * 30 ? 12 : (d2 > 21 * 21 ? 13 : 14);
    return LC_Grad(x, y, LCR_SKY_N);
}

static u32 LCR_SunsetCell(s32 cx, s32 cy)
{
    s32 x;
    if (cy * 8 >= LCR_HORIZON)
        return (14 << 12) | LC_PLAIN;
    if (cx >= 9 && cx <= 20 && cy >= 8)
        return 13 << 12;   // de zon
    for (x = cx * 8; x < cx * 8 + 8; x++)
        if (sLC->top[x] <= cy * 8 + 7)
            return 13 << 12;
    return (13 << 12) | LC_PLAIN;
}

// rijp: per cel de fase (wanneer de dichtstbijzijnde stap er is + de afstand), vier ruispatronen per fase
static u32 LCR_FrostPhase(s32 cx, s32 cy)
{
    s32 e, best = LC_HIT - 24, px = cx * 8 + 4, py = cy * 8 + 4;
    for (e = LCR_E0; e < LCR_E0 + LCR_PRINTS; e++)
    {
        s16 x, y;
        s32 dx, dy, d, ft;
        LCR_PrintPos(e, FALSE, &x, &y);
        dx = abs(px - x);
        dy = abs(py - y);
        d = max(dx, dy) + min(dx, dy) / 2;
        ft = LC_E8(e) + d / 2;
        if (ft < best)
            best = ft;
    }
    return 1 + min(14, max(0, (best - 50) * 14 / (LC_HIT - 58)));
}

static s32 LCR_PhaseStart(u32 k)
{
    return 50 + (k - 1) * (LC_HIT - 58) / 14;
}

static void LCR_FrostGen(void)
{
    u32 k, v, x, y, n = 0;
    for (k = 1; k < 16; k++)
    {
        for (v = 0; v < 4; v++)
        {
            u32 buf[8];
            for (y = 0; y < 8; y++)
            {
                u32 w = 0;
                for (x = 0; x < 8; x++)
                {
                    u32 h = (x * 73 + y * 151 + v * 37 + k * 11 + ((x ^ y) & 3) * 29) * 2654435761u;
                    if ((h >> 24) < 150 || ((x + v) & 3) == (y & 3))
                        w |= k << (x * 4);
                }
                buf[y] = w;
            }
            CpuCopy32(buf, LC_Tile(16 + n++), 32);
        }
    }
}

static void RTCrown_Init(struct Task *task)
{
    u32 i, v, step;
    u16 sp = LC_EnemySpecies();
    bool32 sunset;
    const u16 *pal;

    switch (sp)
    {
    case SPECIES_CALYREX_ICE:    v = LCR_CALYREX_ICE; break;
    case SPECIES_CALYREX_SHADOW: v = LCR_CALYREX_SHADOW; break;
    case SPECIES_GLASTRIER:      v = LCR_GLASTRIER; break;
    case SPECIES_SPECTRIER:      v = LCR_SPECTRIER; break;
    default:                     v = LCR_CALYREX; sp = SPECIES_CALYREX; break;
    }
    LC_Begin(task, 0xCA1);
    task->tLcVar = v;
    if (sLC == NULL)
        return;
    sunset = LCR_Sunset(v);
    step = LCR_Step(v);

    if (sunset)
    {
        LC_Pines(100, 62, 92, 18, 9);
        LC_RowGradient(0, LCR_HORIZON, LCR_SKY_N);
        LC_RowGradient(LCR_HORIZON, DISPLAY_HEIGHT, 4);
    }
    else
    {
        u32 cx, cy;
        LCR_FrostGen();
        for (cy = 0; cy < 20; cy++)
            for (cx = 0; cx < 32; cx++)
                sLC->map[cy * 32 + cx] = (v == LCR_GLASTRIER)
                    ? ((16 + (LCR_FrostPhase(cx, cy) - 1) * 4 + ((cx * 7 + cy * 13) & 3)) | (13 << 12)) : 0;
        task->tLcGen = 20;
    }

    // hoefijzers: donker stof, ijs of spookvuur
    if (step == 1)
        pal = LC_Tint(gBattleAnimSpritePal_HorseshoeFist, RGB(4, 10, 20), RGB(31, 31, 31));
    else if (step == 2)
        pal = LC_Tint(gBattleAnimSpritePal_HorseshoeFist, RGB(8, 0, 14), RGB(30, 20, 31));
    else
        pal = LC_Tint(gBattleAnimSpritePal_HorseshoeFist, RGB(4, 2, 1), RGB(24, 17, 10));
    sLC->matLand = AllocOamMatrix();
    sLC->matSet = AllocOamMatrix();
    if (sLC->matLand != 0xFF)
        SetOamMatrixRotationScaling(sLC->matLand, 200, 200, 0xC000);
    if (sLC->matSet != 0xFF)
        SetOamMatrixRotationScaling(sLC->matSet, 160, 160, 0xC000);
    for (i = 0; i < LCR_PRINTS; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_HorseshoeFist, 0x800, pal, LCR_TAG_SHOE, &sGI_Oam32, 0, 0, 3);
        LI_Frame(i, LCR_TAG_SHOE, 1, 16);
        LC_UseMatrix(LI_S(i), sLC->matLand, SPRITE_SHAPE(32x32), SPRITE_SIZE(32x32));
    }
    for (i = 0; i < LCR_PRINTS; i++)
    {
        if (step == 1)
            LI_Make(LCR_PRINTS + i, gBattleAnimSpriteGfx_IceCrystals, 0x1C0, gBattleAnimSpritePal_IceCrystals, LCR_TAG_FX, &sGI_Oam16, 0, 0, 2);
        else if (step == 2)
            LI_Make(LCR_PRINTS + i, gBattleAnimSpriteGfx_PurpleFlame, 0x400, gBattleAnimSpritePal_PurpleFlame, LCR_TAG_FX, &sLI2_Oam16x32, 0, 0, 2);
        else
            LI_Make(LCR_PRINTS + i, gBattleAnimSpriteGfx_Smoke, 0x100,
                    LC_Tint(gBattleAnimSpritePal_Smoke, RGB(9, 6, 4), RGB(28, 21, 13)), LCR_TAG_FX, &sGI_Oam16, 0, 0, 2);
    }
    if (sunset)
        LI_Make(LCR_LASSO, gBattleAnimSpriteGfx_ThinRing, 0x800, gBattleAnimSpritePal_ThinRing, LCR_TAG_ROPE, &sGI_Oam64Affine, 120, 40, 1);

    if (v == LCR_GLASTRIER)
    {
        // de rijp telt op bij de wereld (zwart = niets)
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                                   | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 16));
        SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
        SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
    }
}

static bool8 RTCrown_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, age, beatK;
    u32 v = task->tLcVar, step = LCR_Step(v), keep;
    bool32 sunset = LCR_Sunset(v), done = FALSE;
    struct Sprite *s;
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCR_TAG_SHOE) | GI_SpritePalBit(LCR_TAG_FX) | GI_SpritePalBit(LCR_TAG_ROPE);
    GI_ResetPals(keep);
    beatK = 6 - min(6, t % 20);   // kort oplichten op elke tel

    if (sunset)
    {
        LC_Gen(task, t, LCR_SunsetPixel, LCR_SunsetCell);
        if (r == 0)
            LC_ShowMap();
        GI_FadeWorld(r, LC_SHOW, keep);
        // lucht: paars boven, rood, oranje, geel aan de horizon; zon; bos (wordt groen op de klokslag)
        cols[0] = 0;
        for (i = 0; i < LCR_SKY_N; i++)
            cols[1 + i] = LC_Mix3(RGB(4, 2, 11), RGB(25, 7, 12), RGB(31, 25, 10), i, LCR_SKY_N - 1);
        cols[12] = Tapu_Blend(RGB(31, 17, 5), RGB(31, 27, 14), beatK * 2);
        cols[13] = RGB(31, 26, 11);
        cols[14] = RGB(31, 31, 22);
        k = t - LC_HIT;
        cols[15] = (k >= 0) ? Tapu_Blend(RGB(8, 22, 6), RGB(3, 3, 4), min(16, k * 3)) : RGB(3, 2, 4);
        LC_SetBgPal(0, cols);
        cols[1] = RGB(9, 4, 4);
        cols[2] = RGB(7, 3, 3);
        cols[3] = RGB(5, 2, 3);
        cols[4] = RGB(3, 1, 2);
        LC_SetBgPal(1, cols);
        if (r < 8)
            BlendPalettes(GI_BG_PALS, 16 - r * 2, RGB_BLACK);
    }
    else if (v == LCR_GLASTRIER)
    {
        LC_DimWorld(r, keep, 9, RGB(3, 7, 16));
        if (r == 0)
            LC_ShowMap();
        cols[0] = 0;
        for (i = 1; i < 16; i++)
        {
            age = t - LCR_PhaseStart(i);
            cols[i] = age < 0 ? 0 : (age < 3 ? RGB(24, 28, 31) : ((i % 3) ? RGB(9, 14, 20) : RGB(13, 18, 24)));
        }
        LC_SetBgPal(0, cols);
    }
    else
    {
        LC_DimWorld(r, keep, 13, RGB(3, 0, 7));
    }

    // de stappen
    for (i = 0; i < LCR_PRINTS; i++)
    {
        s16 x, y;
        struct Sprite *fx = LI_S(LCR_PRINTS + i);
        s = LI_S(i);
        age = t - LC_E8(i + LCR_E0);
        LCR_PrintPos(i + LCR_E0, sunset, &x, &y);
        s->x = x;
        s->y = y;
        s->invisible = age < 0;
        fx->invisible = TRUE;
        if (age < 0)
            continue;
        if (age == 3 || (age > 3 && s->oam.matrixNum == sLC->matLand))
            LC_UseMatrix(s, sLC->matSet, SPRITE_SHAPE(32x32), SPRITE_SIZE(32x32));
        if (step == 0)
        {
            // stofwolkje dat opwaait en achterblijft
            fx->invisible = age >= 16;
            fx->x = x - 6 - age / 2;
            fx->y = y - 6 - age / 2;
            LI_Frame(LCR_PRINTS + i, LCR_TAG_FX, age >= 8, 4);
        }
        else if (step == 1)
        {
            // het ijs groeit uit de afdruk en glinstert
            fx->invisible = (age > 30 && ((t + i) & 7) == 0);
            fx->x = x + 2;
            fx->y = y - 4 - min(age, 4);
            LI_Frame(LCR_PRINTS + i, LCR_TAG_FX, 0, 4);
        }
        else
        {
            // spookvuur dat flakkert en weer dooft; ook de afdruk verdwijnt
            fx->invisible = age >= 44 || (age > 30 && (t & 1));
            fx->x = x;
            fx->y = y - 16 - age / 6;
            LI_Frame(LCR_PRINTS + i, LCR_TAG_FX, ((t >> 2) + i) & 3, 8);
            if (!sunset && (age >= 56 || (age > 44 && (t & 1))))
                s->invisible = TRUE;
        }
        if (LC_Cross(task, t, LC_E8(i + LCR_E0)) && step == 1 && (i & 3) == 1)
            PlaySE(SE_ICE_CRACK);
    }

    // de lasso van de koning (geen Pokémon-sprite: het touw en de stappen vertellen het)
    if (sunset)
    {
        struct Sprite *rope = LI_S(LCR_LASSO);
        u8 mat = rope->oam.matrixNum;
        // lasso: zwiept rond boven het hoofd, op de klokslag naar de camera
        k = t - (LCR_MON_SHOW - 20);
        rope->invisible = k < 0;
        if (k >= 0 && rope->oam.affineMode != ST_OAM_AFFINE_OFF)
        {
            s32 a = (t * 12) & 0xFF;
            if (t < LC_HIT)
            {
                rope->x = 120 + Cos(a, 10);
                rope->y = 40 + Sin(a, 3);
                SetOamMatrixRotationScaling(mat, 220 + Sin(a, 24), 64, (u16)Sin(a, 0x600));
                if (t < LCR_MON_SHOW)
                    BlendPalettes(GI_SpritePalBit(LCR_TAG_ROPE), 16, RGB(2, 1, 3));
            }
            else
            {
                k = t - LC_HIT;
                rope->x = 120;
                rope->y = 40 + k * 6;
                SetOamMatrixRotationScaling(mat, 256 + k * 160, 64 + k * 200, 0);
            }
        }
        if (LC_Cross(task, t, LCR_MON_SHOW - 20))
            PlaySE(SE_M_SWAGGER);
        if (LC_Cross(task, t, LC_HIT))
            PlaySE(SE_M_TAIL_WHIP);
    }
    if (LC_Cross(task, t, sunset ? LCR_MON_SHOW + 6 : LC_BEAT(6) + 6))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    if (LC_Cross(task, t, LC_HIT) && !sunset)
        PlaySE(v == LCR_GLASTRIER ? SE_ICE_BREAK : SE_M_NIGHTMARE);

    GI_Shake(t >= LC_HIT && t < LC_HIT + 6 ? 2 : 0);
    if (!sunset && t >= LC_HIT)
        done = LC_Out(t, LC_HIT, 6, PALETTES_ALL, v == LCR_GLASTRIER ? RGB(28, 31, 31) : RGB(16, 4, 26));
    else if (sunset)
        done = LC_Out(t, LC_HIT + 2, 5, PALETTES_ALL, RGB(31, 29, 20));
    task->tLcLast = t;
    return done;
}

static void RTCrown_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCR_TAG_SHOE);
    GI_FreeTag(LCR_TAG_FX);
    GI_FreeTag(LCR_TAG_ROPE);
}

static const struct RouteTransition sRT_LegendCrown =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTCrown_Init, RTCrown_Update, RTCrown_Finish
};

static void Task_LegendCrown(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendCrown);
}

// =====================================================================================================================
// Celebi (Ilex Forest; Jordi: "maak de celebi intro extreem nostalgisch"): even zit je weer achter een Game Boy Color.
// Het beeld wordt een GBC-scherm van 160x144 in een donkere rand met een brandend power-lampje (en het aan-geluidje),
// de plek valt terug in de vier groentinten en komt op zoals GSC een beeld opbouwt: vanuit wit, in tintstappen. Dan
// precies de wilde-gevechtsovergang van Gold/Silver/Crystal (pret/pokecrystal, engine/battle/battle_transition.asm):
// drie keer de BGP-flits (12 tintstappen: donkerder, zwart, terug, lichter, wit, terug) op de tellen 3, 4 en 5, met
// de gemaaide-grasblaadjes van het Celebi-schrijn (Crystal) die door het beeld dwarrelen, en dan de spin naar zwart
// (20 wiggen met de klok mee vanaf links, de echte wigtabellen) op tel 6 en 7. Op de klokslag de tijdreis: het zwart
// slaat om in Celebi-groen en wit. Geen Pokémon-sprite.
#define LCC_LEAVES     8
#define LCC_TAG_LEAF   0x5B23
#define LCC_FLASH      LC_BEAT(3)   // tel 3, 4 en 5
#define LCC_SPIN       LC_BEAT(6)   // 20 wiggen, 2 frames per wig
#define LCC_X0         5            // het GBC-scherm: 20 x 18 tiles vanaf tile (5, 1)
#define LCC_Y0         1
#define LCC_BLACK      3            // tile 3 = effen kleur 3 = de donkerste tint

static const u16 sLC_Gbc[4] = {RGB(3, 7, 4), RGB(9, 16, 8), RGB(19, 25, 10), RGB(28, 31, 21)};
// BGP-flits uit pokecrystal (.pals): elke stap verschuift de vier tinten (+ = donkerder)
static const s8 sLCC_FlashOff[12] = {1, 2, 3, 2, 1, 0, -1, -2, -3, -2, -1, 0};
// de wiggen van StartTrainerBattle_SpinToBlack: aantal tiles, verschuiving, aantal, ..., 0xFF
static const u8 sLCC_Wedge1[] = {2, 3, 5, 4, 9, 0xFF};
static const u8 sLCC_Wedge2[] = {1, 1, 2, 2, 4, 2, 4, 2, 3, 0xFF};
static const u8 sLCC_Wedge3[] = {2, 1, 3, 1, 4, 1, 4, 1, 4, 1, 3, 1, 2, 1, 1, 1, 1, 0xFF};
static const u8 sLCC_Wedge4[] = {4, 1, 4, 0, 3, 1, 3, 0, 2, 1, 2, 0, 1, 0xFF};
static const u8 sLCC_Wedge5[] = {4, 0, 3, 0, 3, 0, 2, 0, 2, 0, 1, 0, 1, 0, 1, 0xFF};
struct LCCSpin { u8 quad, x, y; const u8 *wedge; };  // quad: bit 0 rechts, bit 1 onder
static const struct LCCSpin sLCC_Spin[20] =
{
    {0, 1, 6, sLCC_Wedge1}, {0, 0, 3, sLCC_Wedge2}, {0, 1, 0, sLCC_Wedge3}, {0, 5, 0, sLCC_Wedge4}, {0, 9, 0, sLCC_Wedge5},
    {1, 10, 0, sLCC_Wedge5}, {1, 14, 0, sLCC_Wedge4}, {1, 18, 0, sLCC_Wedge3}, {1, 19, 3, sLCC_Wedge2}, {1, 18, 6, sLCC_Wedge1},
    {3, 18, 11, sLCC_Wedge1}, {3, 19, 14, sLCC_Wedge2}, {3, 18, 17, sLCC_Wedge3}, {3, 14, 17, sLCC_Wedge4}, {3, 10, 17, sLCC_Wedge5},
    {2, 9, 17, sLCC_Wedge5}, {2, 5, 17, sLCC_Wedge4}, {2, 1, 17, sLCC_Wedge3}, {2, 0, 14, sLCC_Wedge2}, {2, 1, 11, sLCC_Wedge1},
};

// GB-tint 0 (wit) .. 3 (zwart) op helderheid
static u8 LCC_Shade(u16 c)
{
    s32 l = (c & 31) * 5 + ((c >> 5) & 31) * 9 + ((c >> 10) & 31) * 2;
    return l < 120 ? 3 : (l < 240 ? 2 : (l < 360 ? 1 : 0));
}

// wig n in de volgorde zetten (sLC->order[gy * 20 + gx] = eerste wig die de tile zwart maakt)
static void LCC_Wedge(u32 n)
{
    const struct LCCSpin *sp = &sLCC_Spin[n];
    const u8 *d = sp->wedge;
    s32 x = sp->x, y = sp->y, dx = (sp->quad & 1) ? 1 : -1, dy = (sp->quad & 2) ? -1 : 1, c, xx;
    for (;;)
    {
        for (c = *d++, xx = x; c > 0; c--, xx += dx)
            if (xx >= 0 && xx < 20 && y >= 0 && y < 18 && sLC->order[y * 20 + xx] > n)
                sLC->order[y * 20 + xx] = n;
        y += dy;
        c = *d++;
        if (c == 0xFF)
            return;
        x -= dx * c;
    }
}

// de GBC-rand: donker, een lichtere binnenrand en het power-lampje links
static u32 LCC_BezelPixel(s32 x, s32 y)
{
    s32 dx = x - 18, dy = y - 44;
    if (dx * dx + dy * dy <= 3)
        return 2;
    if (dx * dx + dy * dy <= 10)
        return 5;
    if ((x == LCC_X0 * 8 - 1 || x == LCC_X0 * 8 + 160) && y >= LCC_Y0 * 8 - 1 && y <= LCC_Y0 * 8 + 144)
        return 4;
    if ((y == LCC_Y0 * 8 - 1 || y == LCC_Y0 * 8 + 144) && x >= LCC_X0 * 8 - 1 && x <= LCC_X0 * 8 + 160)
        return 4;
    return 1;
}

static u32 LCC_BezelCell(s32 cx, s32 cy)
{
    if (cx >= LCC_X0 && cx < LCC_X0 + 20 && cy >= LCC_Y0 && cy < LCC_Y0 + 18)
        return LC_EMPTY;
    return 13 << 12;
}

static void RTCelebi_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0xCE1);
    if (sLC == NULL)
        return;
    for (i = 0; i < 360; i++)
        sLC->order[i] = 0xFF;
    for (i = 0; i < 20; i++)
        LCC_Wedge(i);
    for (i = 0; i < LCC_LEAVES; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_Leaf, 0x480, gBattleAnimSpritePal_Leaf, LCC_TAG_LEAF, &sGI_Oam16, 0, 0, 2);
        LI_S(i)->oam.priority = 1;   // onder de rand en het zwart (BG0)
    }
    // elke kleur (wereld en blaadjes) krijgt zijn GB-tint
    for (i = 0; i < 512; i++)
        sLC->shade[i] = LCC_Shade(gPlttBufferUnfaded[i]);
    LC_PaintRows(LCC_BezelPixel, LCC_BezelCell, 0, 20);
    LC_ShowMap();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
}

static bool8 RTCelebi_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, off = 0, n;
    struct Sprite *s;
    u16 *tilemap = RT_Tilemap();
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);

    // het scherm gaat aan: vanuit wit in tintstappen (zoals GSC elk beeld laat opkomen)
    if (r < 12)
        off = -3 + r / 3;
    // de drie BGP-flitsen, elk een tel lang
    for (i = 0; i < 3; i++)
    {
        k = (t - LCC_FLASH - LC_BEAT(i)) * 12 / LC_BEAT(1);
        if (t >= LCC_FLASH + LC_BEAT(i) && k < 12)
            off = sLCC_FlashOff[k];
    }
    for (i = 0; i < 512; i++)
    {
        if (i >= 13 * 16 && i < 14 * 16)
            continue;
        k = sLC->shade[i] + off;
        gPlttBufferFaded[i] = sLC_Gbc[3 - (k < 0 ? 0 : (k > 3 ? 3 : k))];
    }

    // BG-palet 13: rand, lampje, het spin-zwart; op de klokslag de tijdreis (zwart -> Celebi-groen -> wit)
    CpuFill16(0, cols, sizeof(cols));
    cols[1] = RGB(5, 5, 7);
    cols[2] = r < 2 ? RGB(8, 2, 2) : RGB(31, 6, 4);
    cols[4] = RGB(11, 11, 14);
    cols[5] = r < 2 ? RGB(5, 5, 7) : RGB(15, 4, 5);
    k = t - LC_HIT;
    if (k < 0)
        cols[LCC_BLACK] = sLC_Gbc[0];
    else if (k < 3)
        cols[LCC_BLACK] = Tapu_Blend(sLC_Gbc[0], RGB(10, 30, 8), k * 6);
    else
        cols[LCC_BLACK] = Tapu_Blend(RGB(10, 30, 8), RGB(30, 31, 26), (k - 2) * 6);
    LC_SetBgPal(0, cols);

    // de blaadjes van het schrijn dwarrelen omlaag (tel 3 tot 6)
    for (i = 0; i < LCC_LEAVES; i++)
    {
        s = LI_S(i);
        k = t - LCC_FLASH - i * 5;
        s->invisible = k < 0 || t >= LCC_SPIN + 30;
        if (s->invisible)
            continue;
        s->x = LCC_X0 * 8 + 10 + ((i * 53) % 150) + Sin((k * 4 + i * 40) & 0xFF, 14) - k / 3;
        s->y = LCC_Y0 * 8 - 8 + ((k * 3 / 2 + i * 19) % 168);
        LI_Frame(i, LCC_TAG_LEAF, ((t >> 2) + i) % 9, 4);
    }

    // spin naar zwart: één wig per 2 frames
    k = t - LCC_SPIN;
    if (k >= 0)
    {
        n = min(20, k / 2 + 1);
        for (i = 0; i < 360; i++)
            if (sLC->order[i] < n)
                tilemap[(LCC_Y0 + i / 20) * 32 + LCC_X0 + i % 20] = LCC_BLACK | (13 << 12);
    }

    if (LC_Cross(task, t, sLC->t0))
        PlaySE(SE_PC_ON);
    if (LC_Cross(task, t, LCC_FLASH + LC_BEAT(2) + 8))
        PlayCry_Normal(SPECIES_CELEBI, 0);
    if (LC_Cross(task, t, LC_HIT))
        PlaySE(SE_M_TELEPORT);
    task->tLcLast = t;
    return t >= LC_HIT + 8;
}

static void RTCelebi_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCC_TAG_LEAF);
}

static const struct RouteTransition sRT_LegendCelebi =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTCelebi_Init, RTCelebi_Update, RTCelebi_Finish
};

static void Task_LegendCelebi(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendCelebi);
}

// =====================================================================================================================
// Uxie, Mesprit, Azelf (de Gen 4-meren; Jordi: "Feeling trio mag je een lake met daarna fadeout naar blauw, geel of
// roze afhankelijk van de pokemon"): een stil meer in de ochtendmist, de verre oever als bosrand, glinsteringen op het
// water. Op elke tel een kring in het water, die vanaf tel 3 de kleur van de edelsteen krijgt (iets onder het
// oppervlak); dan kleurt alles naar die edelsteen: Uxie geel, Mesprit roze, Azelf blauw.
#define LCL_RINGS      4
#define LCL_TAG_RING   0x5B25
#define LCL_SURFACE    48
#define LCL_SKY_N      8
#define LCL_WATER_N    10
#define LCL_MON_T      LC_BEAT(3)
#define LCL_RIPPLE_Y   106
#define LCL_TINT       LC_BEAT(6)

static u32 LCL_Pixel(s32 x, s32 y)
{
    if (y >= LCL_SURFACE)
    {
        u32 h;
        if (sLC->curVar && (y & 7) == 3)
        {
            h = (x >> 3) * 2654435761u + (y >> 3) * 40503u;
            if ((x & 7) >= ((h >> 12) & 3) && (x & 7) < ((h >> 12) & 3) + 3 + ((h >> 16) & 1))
                return 13 + ((h >> 20) % 3);
        }
        return LC_Grad(x, y, LCL_WATER_N);
    }
    if (y >= sLC->top[x])
        return 15;
    return LC_Grad(x, y, LCL_SKY_N);
}

static u32 LCL_Cell(s32 cx, s32 cy)
{
    u32 h;
    if (cy * 8 >= LCL_SURFACE)
    {
        h = (cx * 2654435761u + cy * 40503u) >> 8;
        sLC->curVar = (cy * 8 >= LCL_SURFACE + 8) && ((h & 0xFF) < 70);
        return sLC->curVar ? (14 << 12) : ((14 << 12) | LC_PLAIN);
    }
    sLC->curVar = 0;
    for (h = cx * 8; h < cx * 8 + 8; h++)
        if (sLC->top[h] <= cy * 8 + 7)
            return 13 << 12;
    return (13 << 12) | LC_PLAIN;
}

static u16 LCL_Color(void)
{
    switch (LC_EnemySpecies())
    {
    case SPECIES_UXIE:    return RGB(31, 27, 6);
    case SPECIES_MESPRIT: return RGB(31, 13, 22);
    default:              return RGB(7, 14, 31);
    }
}

static void RTLake_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0x1A6E);
    if (sLC == NULL)
        return;
    LC_Pines(LCL_SURFACE, 30, 42, 14, 6);
    LC_RowGradient(0, LCL_SURFACE, LCL_SKY_N);
    LC_RowGradient(LCL_SURFACE, DISPLAY_HEIGHT, LCL_WATER_N);
    for (i = 0; i < LCL_RINGS; i++)
        LI_Make(i, gBattleAnimSpriteGfx_ThinRing, 0x800, LC_Tint(gBattleAnimSpritePal_ThinRing, RGB(8, 14, 20), RGB(28, 31, 31)),
                LCL_TAG_RING, &sGI_Oam64Affine, 120, LCL_RIPPLE_Y, 3);
    for (i = 0; i < LCL_RINGS; i++)
        LI_S(i)->oam.objMode = ST_OAM_OBJ_BLEND;
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(6, 10));
}

static bool8 RTLake_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep;
    struct Sprite *s;
    u16 cols[16];
    bool32 done;

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCL_TAG_RING);
    GI_ResetPals(keep);
    LC_Gen(task, t, LCL_Pixel, LCL_Cell);
    if (r == 0)
        LC_ShowMap();
    GI_FadeWorld(r, LC_SHOW, keep);

    // ochtendmist boven, bosrand, water van licht (horizon) naar diep
    cols[0] = 0;
    for (i = 0; i < LCL_SKY_N; i++)
        cols[1 + i] = Tapu_Blend(RGB(12, 14, 21), RGB(27, 27, 28), i * 16 / (LCL_SKY_N - 1));
    cols[15] = RGB(5, 9, 11);
    LC_SetBgPal(0, cols);
    for (i = 0; i < LCL_WATER_N; i++)
        cols[1 + i] = Tapu_Blend(RGB(19, 23, 27), RGB(2, 5, 13), i * 16 / (LCL_WATER_N - 1));
    for (i = 0; i < 3; i++)
    {
        k = ((t >> 2) + i * 3) % 9;
        cols[13 + i] = k < 2 ? RGB(30, 31, 31) : (k < 4 ? RGB(18, 23, 28) : RGB(9, 14, 21));
    }
    LC_SetBgPal(1, cols);
    if (r < 8)
        BlendPalettes(GI_BG_PALS, 16 - r * 2, RGB_BLACK);

    // kringen: één per tel
    for (i = 0; i < LCL_RINGS; i++)
    {
        s32 b, born = -1;
        s = LI_S(i);
        for (b = 3 + i; b < 11; b += LCL_RINGS)
            if (t >= LC_BEAT(b))
                born = LC_BEAT(b);
        k = t - born;
        s->invisible = born < 0 || k >= 48;
        if (!s->invisible && s->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(s->oam.matrixNum, 48 + k * 9, (48 + k * 9) * 3 / 10, 0);
    }

    // iets onder het oppervlak: vanaf tel 3 kleuren de kringen naar de edelsteen
    k = t - LCL_MON_T;
    if (k >= 0)
        BlendPalettes(keep, min(11, k / 3), LCL_Color());
    if (LC_Cross(task, t, LCL_MON_T + 10))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    if (LC_Cross(task, t, LC_BEAT(3)))
        PlaySE(SE_M_BUBBLE);

    // alles kleurt naar de edelsteen
    done = FALSE;
    if (t >= LCL_TINT)
    {
        k = min(16, (t - LCL_TINT) * 16 / (LC_HIT - LCL_TINT));
        BlendPalettes(GI_BG_PALS | keep, k, LCL_Color());
        done = t >= LC_HIT + 2;
    }
    if (LC_Cross(task, t, LCL_TINT))
        PlaySE(SE_M_HEAL_BELL);
    task->tLcLast = t;
    return done;
}

static void RTLake_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCL_TAG_RING);
}

static const struct RouteTransition sRT_LegendLake =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTLake_Init, RTLake_Update, RTLake_Finish
};

static void Task_LegendLake(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendLake);
}

// =====================================================================================================================
// Meloetta (Jordi: "Meloetta is ook saai, emuleer daar wat muziek dances"): een optreden. Het podium wordt donker, een
// notenbalk licht op en twee spotlights zwaaien over het podium; onderin springt een equalizer op de achtsten. Acht
// noten (de Sing-art) dansen een choreografie op het legendary-thema: ze komen tapdansend op (links/rechts om en om
// op de achtsten), wiegen op de tellen (step-ball-change), doen op tel 5 een kickline (alles springt, het beeld veert
// mee), en op tel 6 de pirouette: de rij draait in een cirkel die steeds sneller rondtolt, elke noot tolt mee (de
// Pirouette-vorm), de spotlights zoeken het midden en op de klokslag een witte flits. Aria: groen, Pirouette: oranje.
// Geen Pokémon-sprite.
#define LCM_NOTES      8
#define LCM_SPOT       LCM_NOTES     // twee spotlights
#define LCM_TAG_NOTE   0x5B26
#define LCM_TAG_SPOT   0x5B2E
#define LCM_BAR_TILE   16            // tiles 16-19: equalizerstaafjes in kleur 1-4
#define LCM_STAFF_Y    60            // bovenste lijn; vijf lijnen, 6 px uit elkaar
#define LCM_TAP        LC_BEAT(3)
#define LCM_KICK       LC_BEAT(5)
#define LCM_SPIN       LC_BEAT(6)

static const u16 sLCM_SpotPal[16] = {0, RGB_WHITE};

static u32 LCM_StaffPixel(s32 x, s32 y)
{
    s32 d = y - LCM_STAFF_Y;
    return (d >= 0 && d <= 24 && d % 6 == 0) ? 1 : 0;
}

static u32 LCM_StaffCell(s32 cx, s32 cy)
{
    return (cy * 8 + 7 >= LCM_STAFF_Y && cy * 8 <= LCM_STAFF_Y + 24) ? ((13 << 12) | LC_PLAIN) : LC_EMPTY;
}

// waar noot i staat in de rij (op een lijn of tussen twee lijnen)
static void LCM_LinePos(u32 i, s32 *x, s32 *y)
{
    *x = 36 + i * 24;
    *y = LCM_STAFF_Y + 12 + ((i & 1) ? -9 : 3) - 8;
}

static void RTMeloetta_Init(struct Task *task)
{
    u32 i, k, y;
    u16 sp = LC_EnemySpecies();
    LC_Begin(task, 0x3E10);
    if (sLC == NULL)
        return;
    task->tLcVar = (sp == SPECIES_MELOETTA_PIROUETTE);
    // equalizerstaafjes: 6 px breed, 2 px tussenruimte
    for (k = 0; k < 4; k++)
    {
        u32 buf[8];
        for (y = 0; y < 8; y++)
            buf[y] = (y == 0) ? 0 : ((k + 1) * 0x01111110);
        CpuCopy32(buf, LC_Tile(LCM_BAR_TILE + k), 32);
    }
    sLC->nextTile = LCM_BAR_TILE + 4;
    LC_PaintRows(LCM_StaffPixel, LCM_StaffCell, 0, 20);
    sLC->matSet = AllocOamMatrix();
    for (i = 0; i < LCM_NOTES; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_MusicNotes2, 0x800, task->tLcVar ? gBattleAnimSpritePal_MusicNotes2
                : LC_Rotate(gBattleAnimSpritePal_MusicNotes2, 1), LCM_TAG_NOTE, &sGI_Oam16, 0, 0, 1);
        LI_Frame(i, LCM_TAG_NOTE, (i * 5) & 15, 4);
        LC_UseMatrix(LI_S(i), sLC->matSet, SPRITE_SHAPE(16x16), SPRITE_SIZE(16x16));
    }
    for (i = 0; i < 2; i++)
    {
        LI_Make(LCM_SPOT + i, gBattleAnimSpriteGfx_Spotlight, 0x800, sLCM_SpotPal, LCM_TAG_SPOT, &sGI_Oam64Affine, 0, 0, 4);
        LI_S(LCM_SPOT + i)->oam.objMode = ST_OAM_OBJ_BLEND;
        LI_S(LCM_SPOT + i)->oam.priority = 1;   // onder de notenbalk (BG0 telt er dan bij op)
    }
    LC_Additive(12);
}

static bool8 RTMeloetta_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, b, e, ph, eph, bump;
    u32 keep, noteBit, spotBit;
    bool32 piro = task->tLcVar;
    struct Sprite *s;
    u16 *tilemap = RT_Tilemap();
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    noteBit = GI_SpritePalBit(LCM_TAG_NOTE);
    spotBit = GI_SpritePalBit(LCM_TAG_SPOT);
    keep = noteBit | spotBit;
    GI_ResetPals(keep);
    LC_DimWorld(r, keep, 13, RGB(4, 1, 8));
    if (r == 0)
        LC_ShowMap();

    b = t * 1000 / 20363;          // tel
    ph = t - LC_BEAT(b);           // frames sinds de tel
    e = t * 1000 / 10181;          // achtste
    eph = t - LC_E8(e);
    bump = (t >= LCM_TAP && ph < 3) ? 2 - ph / 2 : 0;
    if (t >= LCM_KICK && t < LCM_SPIN && ph < 6)
        bump = 4 - ph / 2;

    // notenbalk (licht op op de tel) en equalizer
    CpuFill16(0, cols, sizeof(cols));
    k = min(16, r * 2);
    cols[1] = Tapu_Blend(0, Tapu_Blend(piro ? RGB(22, 12, 3) : RGB(6, 20, 10), RGB(31, 31, 24), (t >= LCM_TAP && ph < 4) ? 8 - ph * 2 : 0), k);
    LC_SetBgPal(0, cols);
    cols[1] = RGB(4, 18, 6);
    cols[2] = RGB(14, 22, 4);
    cols[3] = RGB(24, 22, 4);
    cols[4] = RGB(28, 8, 4);
    LC_SetBgPal(1, cols);
    for (i = 0; i < 30; i++)
    {
        u32 h = (i * 2654435761u + e * 40503u) >> 13, lvl;
        s32 tgt = (r < 6) ? 0 : 1 + (h % 3) + ((e & 1) == 0) + (i < 10 || (i > 20 && (e & 2)));
        lvl = max(0, min(4, tgt - eph / 4));
        for (k = 0; k < 4; k++)
            tilemap[(19 - k) * 32 + i] = (k < (s32)lvl) ? ((LCM_BAR_TILE + k) | (14 << 12)) : 0;
    }
    SetGpuReg(REG_OFFSET_BG0VOFS, (-bump) & 0x1FF);

    // spotlights: zwaaien om hun top, op de klokslag allebei naar het midden
    for (i = 0; i < 2; i++)
    {
        s32 ax = i ? 196 : 44, a;
        s = LI_S(LCM_SPOT + i);
        s->invisible = r < 4;
        a = Sin((t * 3 + i * 128) & 0xFF, 22) + (i ? 14 : -14);
        if (t >= LC_BEAT(7))
            a = a * max(0, LC_HIT - t) / (LC_HIT - LC_BEAT(7)) + (i ? 34 : -34) * min(16, t - LC_BEAT(7)) / 16;
        if (s->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(s->oam.matrixNum, 300, 500, (u16)(a << 8));
        s->x = ax - Sin(a & 0xFF, 60);
        s->y = -6 + Cos(a & 0xFF, 60);
    }
    cols[0] = piro ? RGB(12, 7, 3) : RGB(7, 10, 6);
    if (t >= LCM_TAP && ph < 4)
        cols[0] = Tapu_Blend(cols[0], RGB(24, 24, 20), 8 - ph * 2);
    k = IndexOfSpritePaletteTag(LCM_TAG_SPOT);
    if (k != 0xFF)
        gPlttBufferFaded[OBJ_PLTT_ID(k) + 1] = Tapu_Blend(0, cols[0], min(16, r * 2));

    // de dans
    // de noten zijn 1,5x zo groot; ze wiebelen op de tel en tollen bij de pirouette
    if (sLC->matSet != 0xFF)
    {
        s32 sc = 384 + (t >= LC_BEAT(7) ? (t - LC_BEAT(7)) * 8 : 0), rot = (t >= LCM_TAP && ph < 6) ? (6 - ph) * ((b & 1) ? 600 : -600) : 0;
        if (t >= LCM_SPIN)
            rot = (t - LCM_SPIN) * (t - LCM_SPIN) * 40;
        SetOamMatrixRotationScaling(sLC->matSet, sc, sc, (u16)rot);
    }
    for (i = 0; i < LCM_NOTES; i++)
    {
        s32 x, y, hop = 0, sway;
        s = LI_S(i);
        LCM_LinePos(i, &x, &y);
        s->invisible = r < 2;
        if (t < LCM_TAP)
        {
            // opkomen: tapdansend vanaf rechts, om en om op de achtsten
            k = LCM_TAP - t;
            x += k * 5;
            if ((u32)(e & 1) == (i & 1))
                hop = Sin(min(127, eph * 128 / 10), 8);
        }
        else if (t < LCM_KICK)
        {
            // tapdansen op de plek, de rij wiegt op de tellen (step-ball-change)
            sway = (b & 1) ? 8 : -8;
            x += -sway + 2 * sway * min(6, ph) / 6;
            if ((u32)(e & 1) == (i & 1))
                hop = Sin(min(127, eph * 128 / 10), 10);
        }
        else if (t < LCM_SPIN)
        {
            // kickline: alles springt op de tel, de buitenste noten het hoogst
            hop = Sin(min(127, ph * 128 / 20), 14 + abs((s32)i * 2 - 7));
        }
        else
        {
            // pirouette: van de rij naar een tollende cirkel
            s32 m = min(16, (t - LCM_SPIN) * 16 / 14), a, rad;
            k = t - LCM_SPIN;
            // rij -> cirkel zonder kruisen: even noten over de bovenkant, oneven over de onderkant
            a = ((i & 1) ? 112 - ((s32)i - 1) * 16 : 144 + (s32)i * 16) + k * 3 + k * k / 12;
            rad = 50 + (t >= LC_BEAT(7) ? (t - LC_BEAT(7)) * 3 : 0);
            x = x + ((120 + Cos(a & 0xFF, rad)) - x) * m / 16;
            y = y + ((70 + Sin(a & 0xFF, rad * 3 / 5)) - y) * m / 16;
            hop = (ph < 6) ? 3 - ph / 2 : 0;
        }
        s->x = x + 8;
        s->y = y + 8 - hop + bump;
        LI_Frame(i, LCM_TAG_NOTE, ((i * 5) + b) & 15, 4);
    }
    if (t >= LCM_TAP && ph < 4)
        BlendPalettes(noteBit, 10 - ph * 2, RGB_WHITE);

    if (LC_Cross(task, t, LCM_KICK))
        PlaySE(SE_M_ENCORE);
    if (LC_Cross(task, t, LCM_SPIN))
        PlaySE(SE_M_TEETER_DANCE);
    if (LC_Cross(task, t, LCM_SPIN + 10))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT + 1, 5, PALETTES_ALL, RGB_WHITE);
}

static void RTMeloetta_Finish(struct Task *task)
{
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    LC_FinishCommon(task);
    GI_FreeTag(LCM_TAG_NOTE);
    GI_FreeTag(LCM_TAG_SPOT);
}

static const struct RouteTransition sRT_LegendMeloetta =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTMeloetta_Init, RTMeloetta_Update, RTMeloetta_Finish
};

static void Task_LegendMeloetta(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendMeloetta);
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
static EWRAM_DATA const struct LCStroke *sLCStrokes = NULL;
static EWRAM_DATA u8 sLCStrokeN = 0;

static void LC_StrokesInit(const struct LCStroke *st, u32 n)
{
    sLCStrokes = st;
    sLCStrokeN = min(n, LC_MAX_STROKES);
    TRY_FREE_AND_SET_NULL(sLCCanvas);
    sLCCanvas = AllocZeroed((LC_MAX_TILES - 16) * 32);
}

// rang: kern > gloed > aura > leeg
static u32 LC_Rank(u32 v)
{
    if (v == 0)
        return 0;
    if (v == 15)
        return 1;
    return v >= 8 ? 2 : 3;
}

static void LC_Plot(s32 x, s32 y, u32 v, u32 pal)
{
    u32 cell, n, shift, *w;
    if (x < 0 || x >= 256 || y < 0 || y >= DISPLAY_HEIGHT)
        return;
    cell = (y >> 3) * 32 + (x >> 3);
    n = sLC->map[cell] & 0x3FF;
    if (n == 0)
    {
        if (sLC->nextTile >= LC_MAX_TILES)
            return;
        n = sLC->nextTile++;
        sLC->map[cell] = n | ((13 + pal) << 12);
    }
    w = &sLCCanvas[(n - 16) * 8 + (y & 7)];
    shift = (x & 7) * 4;
    if (LC_Rank(v) >= LC_Rank((*w >> shift) & 15))
        *w = (*w & ~(15 << shift)) | (v << shift);
}

// een lijn rasteren: langs de lijn per pixel, dwars van -breedte tot +breedte
static void LC_RasterStroke(const struct LCStroke *st)
{
    s32 dx = st->x1 - st->x0, dy = st->y1 - st->y0, len = 1, s, o, w = max(st->glow, st->aura);
    s32 ux, uy, nx, ny;
    while (len * len < dx * dx + dy * dy)
        len++;
    ux = dx * 256 / len;
    uy = dy * 256 / len;
    nx = -uy;
    ny = ux;
    for (s = 0; s <= len; s++)
    {
        s32 along = s * 255 / len, cx = st->x0 * 256 + ux * s, cy = st->y0 * 256 + uy * s, shift = 0;
        u32 step = st->idx + along * st->steps / 256;
        if (st->jag)
            shift = (abs(((along * st->jag) & 63) - 32) - 16) * 5 / 16;
        for (o = -w; o <= w; o++)
        {
            s32 d = abs(o), v;
            if (d < st->core)
                v = step;
            else if (d < st->glow)
                v = step + 7;
            else if (d < st->aura)
                v = 15;
            else
                continue;
            LC_Plot((cx + nx * (o + shift) + 128) >> 8, (cy + ny * (o + shift) + 128) >> 8, v, st->pal);
            // halve stap ernaast: geen gaatjes in schuine lijnen
            LC_Plot((cx + nx * (o + shift) + ux / 2 + 128) >> 8, (cy + ny * (o + shift) + uy / 2 + 128) >> 8, v, st->pal);
        }
    }
}

// een paar lijnen per frame; als ze allemaal getekend zijn naar VRAM en tonen. TRUE zodra het beeld er is.
static bool32 LC_GenStrokes(struct Task *task)
{
    u32 i;
    if (sLC == NULL || sLCCanvas == NULL)
        return TRUE;
    if (task->tLcGen > sLCStrokeN)
        return TRUE;
    for (i = 0; i < LC_STROKES_PER_FRAME && task->tLcGen < sLCStrokeN; i++)
        LC_RasterStroke(&sLCStrokes[task->tLcGen++]);
    if (task->tLcGen < sLCStrokeN)
        return FALSE;
    CpuCopy32(sLCCanvas, LC_Tile(16), (sLC->nextTile - 16) * 32);
    LC_ShowMap();
    TRY_FREE_AND_SET_NULL(sLCCanvas);
    task->tLcGen = sLCStrokeN + 1;
    return TRUE;
}

// kleur van een slag-index: zwart voor 'from', twee frames wit, dan 'hot' dat in 'fade' frames zakt naar 'cool'
static u16 LC_SlashColor(s32 t, s32 from, u16 hot, u16 cool, s32 fade)
{
    s32 k = t - from;
    if (k < 0)
        return 0;
    if (k < 2)
        return RGB_WHITE;
    return Tapu_Blend(hot, cool, min(16, (k - 2) * 16 / fade));
}

// =====================================================================================================================
// Zeraora (Jordi: "een soort electric paw strike"): Plasma Fists. De plek wordt donker, twee elektrische klauwhalen
// (drie gekartelde strepen) trekken op de tellen over het beeld, vonken knetteren rond het midden, en dan komt de
// klauw (de poot uit de Mega Punch-art) recht op de camera af: het beeld barst vanuit het midden.
#define LCZ_TAG_PAW    0x5B27
#define LCZ_TAG_SPARK  0x5B28
#define LCZ_SPARKS     4
#define LCZ_SLASH1     LC_BEAT(4)
#define LCZ_SLASH2     LC_BEAT(5)
#define LCZ_MON        92
#define LCZ_PAW        LC_BEAT(6)
#define LCZ_IMPACT     LC_BEAT(7)

static const struct LCStroke sLCZ_Strokes[] =
{
    // klauw 1 (linksboven naar rechtsonder), klauw 2 (andersom), scheuren vanuit het midden
    {40, 4, 150, 150, 2, 4, 0, 1, 2, 9, 0}, {66, -4, 176, 142, 2, 4, 0, 1, 2, 9, 0}, {92, -12, 202, 134, 2, 4, 0, 1, 2, 9, 0},
    {200, 4, 90, 150, 2, 4, 0, 3, 2, 9, 0}, {174, -4, 64, 142, 2, 4, 0, 3, 2, 9, 0}, {148, -12, 38, 134, 2, 4, 0, 3, 2, 9, 0},
    {120, 80, 0, 12, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 250, 30, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 20, 160, 1, 4, 0, 5, 2, 13, 0},
    {120, 80, 236, 158, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 130, 0, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 104, 160, 1, 4, 0, 5, 2, 13, 0},
};

static void RTZeraora_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0x2E4A);
    if (sLC == NULL)
        return;
    LC_StrokesInit(sLCZ_Strokes, ARRAY_COUNT(sLCZ_Strokes));
    LI_Make(0, gBattleAnimSpriteGfx_HandsAndFeet, 0x800, LC_Tint(gBattleAnimSpritePal_HandsAndFeet, RGB(4, 6, 16), RGB(31, 31, 14)),
            LCZ_TAG_PAW, &sGI_Oam32Affine, 120, 80, 0);
    LI_Frame(0, LCZ_TAG_PAW, 1, 16);
    for (i = 0; i < LCZ_SPARKS; i++)
        LI_Make(1 + i, gBattleAnimSpriteGfx_Electricity, 0x800, gBattleAnimSpritePal_ElectricOrbs, LCZ_TAG_SPARK, &sGI_Oam32, 0, 0, 1);
    LC_Additive(14);
}

static bool8 RTZeraora_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep;
    struct Sprite *s, *paw;
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCZ_TAG_PAW) | GI_SpritePalBit(LCZ_TAG_SPARK);
    GI_ResetPals(keep);
    LC_GenStrokes(task);
    LC_DimWorld(r, keep, 13, RGB(1, 1, 4));

    cols[0] = 0;
    for (i = 0; i < 2; i++)
    {
        cols[1 + i] = LC_SlashColor(t, LCZ_SLASH1 + i * 2, RGB(31, 30, 12), RGB(10, 12, 20), 24);
        cols[3 + i] = LC_SlashColor(t, LCZ_SLASH2 + i * 2, RGB(31, 30, 12), RGB(10, 12, 20), 24);
        cols[5 + i] = LC_SlashColor(t, LCZ_IMPACT + i, RGB(28, 31, 31), RGB(14, 20, 31), 30);
    }
    for (i = 1; i <= 6; i++)
        cols[i + 7] = cols[i] ? Tapu_Blend(cols[i], RGB(4, 10, 24), 10) : 0;
    cols[7] = cols[14] = cols[15] = 0;
    LC_SetBgPal(0, cols);

    // vonken knetteren rond het midden (waar de klauw vandaan komt)
    k = t - LCZ_MON;
    for (i = 0; i < LCZ_SPARKS; i++)
    {
        s = LI_S(1 + i);
        s->invisible = k < 0 || ((t + i) & 3) == 0;
        s->x = 120 + Cos((t * 9 + i * 64) & 0xFF, 40);
        s->y = 76 + Sin((t * 9 + i * 64) & 0xFF, 30);
        LI_Frame(1 + i, LCZ_TAG_SPARK, ((t >> 1) + i) & 3, 16);
    }

    // de klauw komt op de camera af
    paw = LI_S(0);
    k = t - LCZ_PAW;
    paw->invisible = k < 0 || t >= LCZ_IMPACT + 6;
    if (k >= 0 && paw->oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        s32 sc = 64 + k * k * 448 / ((LCZ_IMPACT - LCZ_PAW) * (LCZ_IMPACT - LCZ_PAW));
        SetOamMatrixRotationScaling(paw->oam.matrixNum, min(sc, 512), min(sc, 512), (u16)(Sin((t * 16) & 0xFF, 0x400)));
    }

    if (LC_Cross(task, t, LCZ_SLASH1) || LC_Cross(task, t, LCZ_SLASH2))
        PlaySE(SE_M_THUNDERBOLT2);
    if (LC_Cross(task, t, LCZ_MON + 4))
        PlayCry_Normal(SPECIES_ZERAORA, 0);
    if (LC_Cross(task, t, LCZ_PAW))
        PlaySE(SE_M_THUNDER_WAVE);
    if (LC_Cross(task, t, LCZ_IMPACT))
        PlaySE(SE_M_MEGA_KICK);
    GI_Shake(t >= LCZ_IMPACT && t < LCZ_IMPACT + 12 ? 3 : 0);
    if (t >= LCZ_IMPACT && t < LCZ_IMPACT + 4)
        BlendPalettes(PALETTES_ALL & ~GI_BG_PALS, 10, RGB(31, 31, 20));
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(31, 31, 24));
}

static void RTZeraora_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCZ_TAG_PAW);
    GI_FreeTag(LCZ_TAG_SPARK);
}

static const struct RouteTransition sRT_LegendZeraora =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTZeraora_Init, RTZeraora_Update, RTZeraora_Finish
};

static void Task_LegendZeraora(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendZeraora);
}

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

// =====================================================================================================================
// Latias/Latios (Southern Island; Jordi: "Latias/Latios kan je een eon achtig kleuren intro maken"): de plek kleurt
// zacht dromerig (rood-wit of blauw-wit), strepen eonlicht razen voorbij, een lichtbol schiet twee keer langs (wit,
// dan andersom in de eonkleur) en zweeft dan in het midden, met de Soul Dew (het item-icoon) erin; alles loopt over in
// een zachte kleurwas. Geen sync: de Southern Island-gevechten hebben hun eigen muziek.
#define LCE_TAG_ORB    0x5B33
#define LCE_TAG_DEW    0x5B34
#define LCE_FLY1       6
#define LCE_FLY2       30
#define LCE_STAY       56
#define LCE_WASH       100
#define LCE_END        110

static const struct LCStroke sLCE_Strokes[] =
{
    {0, 18, 120, 18, 1, 3, 0, 1, 1, 0, 0}, {140, 34, 250, 34, 1, 3, 0, 2, 1, 0, 0}, {20, 52, 200, 52, 1, 3, 0, 3, 1, 0, 0},
    {60, 70, 150, 70, 1, 3, 0, 4, 1, 0, 0}, {170, 88, 255, 88, 1, 3, 0, 1, 1, 0, 0}, {0, 104, 110, 104, 1, 3, 0, 2, 1, 0, 0},
    {130, 120, 240, 120, 1, 3, 0, 3, 1, 0, 0}, {30, 138, 160, 138, 1, 3, 0, 4, 1, 0, 0}, {180, 152, 255, 152, 1, 3, 0, 1, 1, 0, 0},
};

static void RTEon_Init(struct Task *task)
{
    u16 sp = LC_EnemySpecies();
    u8 id;
    if (sp != SPECIES_LATIOS)
        sp = SPECIES_LATIAS;
    LC_Begin(task, 0xE0E0);
    if (sLC == NULL)
        return;
    task->tLcVar = sp;
    LC_StrokesInit(sLCE_Strokes, ARRAY_COUNT(sLCE_Strokes));
    // de Pokémon als lichtbol die langs schiet; daarna zweeft de Soul Dew in het licht
    LI_Make(0, gBattleAnimSpriteGfx_CircleOfLight, 0x800, LC_Tint(gBattleAnimSpritePal_WhiteCircleOfLight,
            sp == SPECIES_LATIOS ? RGB(2, 5, 16) : RGB(16, 3, 5), sp == SPECIES_LATIOS ? RGB(20, 24, 31) : RGB(31, 20, 22)),
            LCE_TAG_ORB, &sGI_Oam64Affine, -60, 60, 2);
    LI_S(0)->oam.objMode = ST_OAM_OBJ_BLEND;
    id = AddItemIconSprite(LCE_TAG_DEW, LCE_TAG_DEW, ITEM_SOUL_DEW);
    sLI_Spr[1] = id;
    if (id < MAX_SPRITES)
    {
        gSprites[id].invisible = TRUE;
        gSprites[id].oam.priority = 0;
        gSprites[id].x = 120;
        gSprites[id].y = 76;
    }
    LC_Additive(12);
}

static bool8 RTEon_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, sc = 256;
    u32 keep;
    struct Sprite *orb = LI_S(0), *dew = LI_S(1);
    u16 cols[16], eon = task->tLcVar == SPECIES_LATIOS ? RGB(8, 14, 31) : RGB(31, 10, 12);
    u16 soft = task->tLcVar == SPECIES_LATIOS ? RGB(24, 27, 31) : RGB(31, 24, 25);

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCE_TAG_ORB) | GI_SpritePalBit(LCE_TAG_DEW);
    GI_ResetPals(keep);
    LC_GenStrokes(task);
    BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, min(r, 9), soft);

    // eonlicht: vier groepen strepen die om de beurt oplichten, het beeld raast naar links
    cols[0] = cols[7] = cols[15] = 0;
    for (i = 0; i < 4; i++)
    {
        k = ((r >> 1) + i * 3) % 8;
        cols[1 + i] = r < 4 ? 0 : (k < 2 ? RGB_WHITE : (k < 5 ? eon : Tapu_Blend(eon, 0, 8)));
        cols[8 + i] = Tapu_Blend(cols[1 + i], 0, 8);
    }
    cols[5] = cols[6] = cols[12] = cols[13] = cols[14] = 0;
    LC_SetBgPal(0, cols);
    SetGpuReg(REG_OFFSET_BG0HOFS, (r * 14) & 0x1FF);

    // langs (wit), andersom (eonkleur), en dan zweven in het midden met de Soul Dew erin
    orb->invisible = TRUE;
    dew->invisible = TRUE;
    if (r >= LCE_FLY1 && r < LCE_FLY1 + 16)
    {
        k = r - LCE_FLY1;
        orb->invisible = FALSE;
        orb->x = -60 + k * 24;
        orb->y = 54;
        sc = 110;
    }
    else if (r >= LCE_FLY2 && r < LCE_FLY2 + 16)
    {
        k = r - LCE_FLY2;
        orb->invisible = FALSE;
        orb->x = 300 - k * 24;
        orb->y = 108;
        sc = 130;
    }
    else if (r >= LCE_STAY)
    {
        k = min(r - LCE_STAY, 16);
        orb->invisible = FALSE;
        orb->x = dew->x = 120 + (16 - k) * 6;
        orb->y = dew->y = 76 - (16 - k) * 3 + Sin((r * 6) & 0xFF, 3);
        sc = 80 + k * 3 + Sin((r * 10) & 0xFF, 8);
        dew->invisible = k < 8;
    }
    if (orb->oam.affineMode != ST_OAM_AFFINE_OFF)
        SetOamMatrixRotationScaling(orb->oam.matrixNum, sc * 3 / 2, sc, 0);
    if (r == LCE_FLY1 || r == LCE_FLY2)
        PlaySE(SE_M_FLY);
    if (r == LCE_STAY + 8)
        PlayCry_Normal(task->tLcVar, 0);
    task->tLcLast = t;
    return LC_Out(r, LCE_WASH, LCE_END - LCE_WASH, PALETTES_ALL, soft);
}

static void RTEon_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCE_TAG_ORB);
    GI_FreeTag(LCE_TAG_DEW);
}

static const struct RouteTransition sRT_LegendEon =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTEon_Init, RTEon_Update, RTEon_Finish
};

static void Task_LegendEon(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendEon);
}

// =====================================================================================================================
// Cresselia (Fullmoon Island; Jordi: "die hele naam betekent crescent moon toch? wat doet de full moon daar?"): de
// Lunar-Pokémon, met halvemaanvormige ringen en de Lunar Wing. Het wordt nacht en de sterren gaan aan (BG0, optellend);
// op tel 3 gloeit een dunne sikkelmaan op (nooit vol: alleen de sikkel en zijn gloed). Op de tellen 4, 5 en 6 zwiepen
// telkens twee halvemaanbogen (de Psycho Cut-art) in een schuine baan om de sikkel, zoals Cresselia's ringen; roze en
// gele Lunar Dance-glinsters dwarrelen omlaag en droommist drijft laag over het beeld. Op tel 7 Moonblast: de bogen
// schieten de sikkel in, die wit-roze opvlamt, en op de klokslag een roze flits (geen ronde gloed: dat leek een volle
// maan).
// Geen Pokémon-sprite.
#define LCM2_MIST      6
#define LCM2_ARCS      6
#define LCM2_ARC0      LCM2_MIST
#define LCM2_GLINT0    (LCM2_ARC0 + LCM2_ARCS)
#define LCM2_GLINTS    6
#define LCM2_TAG_MIST  0x5B29
#define LCM2_TAG_ARC   0x5B30
#define LCM2_TAG_GLINT 0x5B31
#define LCM2_X         120           // de maan
#define LCM2_Y         52
#define LCM2_R         28
#define LCM2_IX        11            // de schijf die de sikkel uithapt
#define LCM2_IY        -7
#define LCM2_IR        26
#define LCM2_MOON      LC_BEAT(3)
#define LCM2_ARC_T     LC_BEAT(4)
#define LCM2_MOONBLAST LC_BEAT(7)

// de sikkel (kleur 1-3, kern het felst), zijn gloed (4-6, gedithered) en de sterren (8-10, drie fonkelgroepen)
static u32 LCM2_Pixel(s32 x, s32 y)
{
    s32 dx = x - LCM2_X, dy = y - LCM2_Y, d2 = dx * dx + dy * dy, ex = dx - LCM2_IX, ey = dy - LCM2_IY;
    u32 h;
    if (d2 < (LCM2_R + 12) * (LCM2_R + 12))
    {
        s32 d1 = Sqrt(d2 * 16), di = Sqrt((ex * ex + ey * ey) * 16), m, bay = sLC_Bayer[(y & 3) * 4 + (x & 3)];
        if (d1 < LCM2_R * 4 && di > LCM2_IR * 4)
        {
            m = min(LCM2_R * 4 - d1, di - LCM2_IR * 4);
            return m < 4 ? 1 : (m < 10 ? 2 : 3);
        }
        if (d1 < LCM2_R * 4 || di < LCM2_IR * 4 + 8)
            return 0;
        m = d1 - LCM2_R * 4;
        if (m < 10)
            return 4;
        if (m < 22 && bay < 10)
            return 5;
        if (m < 40 && bay < 4)
            return 6;
        return 0;
    }
    if (y > 118)
        return 0;
    h = (x * 2654435761u) ^ (y * 40503u * 2654435761u);
    h ^= h >> 15;
    if ((h & 0x1FF) < 2)
        return 8 + (h >> 20) % 3;
    return 0;
}

static u32 LCM2_Cell(s32 cx, s32 cy)
{
    return 13 << 12;
}

static void RTCresselia_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0xC4E5);
    if (sLC == NULL)
        return;
    sLC->matSet = AllocOamMatrix();
    if (sLC->matSet != 0xFF)
        SetOamMatrixRotationScaling(sLC->matSet, 640, 360, 0);
    for (i = 0; i < LCM2_MIST; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_Smoke, 0x100, LC_Tint(gBattleAnimSpritePal_Smoke, RGB(8, 4, 14), RGB(26, 18, 30)),
                LCM2_TAG_MIST, &sGI_Oam16, 0, 0, 1);
        LI_S(i)->oam.objMode = ST_OAM_OBJ_BLEND;
        LI_Frame(i, LCM2_TAG_MIST, i & 1, 4);
        LC_UseMatrix(LI_S(i), sLC->matSet, SPRITE_SHAPE(16x16), SPRITE_SIZE(16x16));
    }
    for (i = 0; i < LCM2_ARCS; i++)
    {
        LI_Make(LCM2_ARC0 + i, gBattleAnimSpriteGfx_PsychoCut, 0x200, LC_Tint(gBattleAnimSpritePal_PsychoCut, RGB(16, 6, 22), RGB(31, 27, 31)),
                LCM2_TAG_ARC, &sGI_Oam32Affine, 0, 0, 2);
        LI_S(LCM2_ARC0 + i)->oam.objMode = ST_OAM_OBJ_BLEND;
    }
    for (i = 0; i < LCM2_GLINTS; i++)
        LI_Make(LCM2_GLINT0 + i, gBattleAnimSpriteGfx_Sparkle4, 0xA00, LC_Tint(gBattleAnimSpritePal_Sparkle3, RGB(18, 6, 20), RGB(31, 30, 20)),
                LCM2_TAG_GLINT, &sGI_Oam32, 0, 0, 2);
    LC_Additive(15);
}

static bool8 RTCresselia_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, ph;
    u32 keep;
    struct Sprite *s;
    u16 cols[16], moon;

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCM2_TAG_MIST) | GI_SpritePalBit(LCM2_TAG_ARC) | GI_SpritePalBit(LCM2_TAG_GLINT);
    GI_ResetPals(keep);
    if (task->tLcGen < 20)
    {
        LC_GenRowsDedup(task, LCM2_Pixel, LCM2_Cell, 4);
        if (task->tLcGen >= 20)
            LC_ShowMap();
    }
    LC_DimWorld(r, keep, 13, RGB(1, 1, 7));
    ph = t - LC_BEAT(t * 1000 / 20363);

    // sterren fonkelen; de sikkel gloeit op en klopt zacht op de tel; Moonblast maakt hem wit-roze
    cols[0] = cols[7] = cols[11] = cols[12] = cols[13] = cols[14] = cols[15] = 0;
    for (i = 0; i < 3; i++)
    {
        k = ((r >> 3) + i * 2) % 6;
        cols[8 + i] = Tapu_Blend(0, k < 2 ? RGB(28, 28, 31) : (k < 4 ? RGB(14, 14, 22) : RGB(6, 6, 12)), min(16, r));
    }
    k = t - LCM2_MOON;
    moon = k < 0 ? 0 : Tapu_Blend(0, RGB(31, 29, 18), min(16, k + 2));
    if (k >= 0 && ph < 6)
        moon = Tapu_Blend(moon, RGB(31, 31, 28), 6 - ph);
    if (t >= LCM2_MOONBLAST)
        moon = Tapu_Blend(moon, RGB(31, 24, 30), min(16, (t - LCM2_MOONBLAST) * 2));
    cols[3] = moon;
    cols[2] = Tapu_Blend(0, moon, 12);
    cols[1] = Tapu_Blend(0, Tapu_Blend(moon, RGB(28, 20, 31), 6), 9);
    cols[4] = Tapu_Blend(0, Tapu_Blend(moon, RGB(24, 16, 31), 8), 7);
    cols[5] = Tapu_Blend(0, cols[4], 9);
    cols[6] = Tapu_Blend(0, cols[4], 5);
    LC_SetBgPal(0, cols);

    // droommist laag over het beeld
    for (i = 0; i < LCM2_MIST; i++)
    {
        s = LI_S(i);
        s->invisible = FALSE;
        s->x = ((i * 54 + r * (1 + (i & 1))) % 320) - 40;
        s->y = 138 + (i % 3) * 9 + Sin((r * 4 + i * 40) & 0xFF, 3);
    }

    // halvemaanbogen: per tel twee, in een schuine baan om de sikkel; bij Moonblast schieten ze de maan in
    for (i = 0; i < LCM2_ARCS; i++)
    {
        s32 born = LCM2_ARC_T + LC_BEAT(i / 2), a, rx, ry, x, y;
        s = LI_S(LCM2_ARC0 + i);
        k = t - born;
        s->invisible = k < 0;
        if (k < 0)
            continue;
        a = ((i & 1) ? 128 : 0) + k * 5 + i * 21;
        rx = 86 - i * 6;
        ry = 30 - i * 2;
        if (t >= LCM2_MOONBLAST)
        {
            s32 m = max(0, 16 - (t - LCM2_MOONBLAST));
            rx = rx * m / 16;
            ry = ry * m / 16;
            s->invisible = m == 0;
        }
        x = Cos(a & 0xFF, rx);
        y = Sin(a & 0xFF, ry);
        s->x = LCM2_X + x - y / 2;
        s->y = LCM2_Y + 4 + y + x / 5;
        if (s->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(s->oam.matrixNum, 400, 340, (u16)(((a + 64) & 0xFF) << 8));
    }

    // Lunar Dance: roze en gele glinsters dwarrelen omlaag
    for (i = 0; i < LCM2_GLINTS; i++)
    {
        s = LI_S(LCM2_GLINT0 + i);
        k = t - LCM2_ARC_T - i * 7;
        s->invisible = k < 0 || ((t + i) & 7) == 0;
        s->x = 20 + i * 40 + Sin((k * 3 + i * 50) & 0xFF, 10);
        s->y = -16 + (k * 2 + i * 23) % 150;
        LI_Frame(LCM2_GLINT0 + i, LCM2_TAG_GLINT, ((t >> 2) + i) % 5, 16);
    }

    if (LC_Cross(task, t, LCM2_MOON))
        PlaySE(SE_M_MOONLIGHT);
    for (i = 0; i < 3; i++)
        if (LC_Cross(task, t, LCM2_ARC_T + LC_BEAT(i)))
            PlaySE(SE_M_RAZOR_WIND);
    if (LC_Cross(task, t, LC_BEAT(6) + 10))
        PlayCry_Normal(SPECIES_CRESSELIA, 0);
    if (LC_Cross(task, t, LCM2_MOONBLAST))
        PlaySE(SE_M_MORNING_SUN);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(31, 24, 31));
}

static void RTCresselia_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCM2_TAG_MIST);
    GI_FreeTag(LCM2_TAG_ARC);
    GI_FreeTag(LCM2_TAG_GLINT);
}

static const struct RouteTransition sRT_LegendCresselia =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTCresselia_Init, RTCresselia_Update, RTCresselia_Finish
};

static void Task_LegendCresselia(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendCresselia);
}

// =====================================================================================================================
// Necrozma (alle vormen; Jordi: "light-devouring"): het beeld wordt fel wit, dan verschijnt in het midden een zwart
// prisma (een kristal uit de Tera-art, helemaal zwart) dat al het licht en de kleur naar zich toe zuigt: de wereld
// wordt donker en prismastralen in alle kleuren van het spectrum schieten van de randen naar binnen en verdwijnen
// in het prisma, tot het beeld zwart is.
#define LCN_PRISM      LC_BEAT(3)
#define LCN_RAYS       LC_BEAT(4)
#define LCN_RAY_N      9
#define LCN_TAG_PRISM  0x5B35

static const u16 sLCN_Spectrum[9] = {
    RGB(31, 6, 6), RGB(31, 18, 4), RGB(31, 30, 6), RGB(10, 31, 8), RGB(6, 30, 26), RGB(6, 16, 31), RGB(14, 8, 31), RGB(26, 8, 31), RGB(31, 10, 22),
};

// stralen van het midden naar de rand, kern = stap 1-5 (afstand), gloed 8-12; palet = kleurgroep
static const struct LCStroke sLCN_Strokes[LCN_RAY_N] =
{
    {120, 80, 120 + 150, 80 + 0, 2, 5, 0, 1, 5, 0, 0}, {120, 80, 120 + 115, 80 + 96, 2, 5, 0, 1, 5, 0, 1},
    {120, 80, 120 + 26, 80 + 148, 2, 5, 0, 1, 5, 0, 2}, {120, 80, 120 - 75, 80 + 130, 2, 5, 0, 1, 5, 0, 0},
    {120, 80, 120 - 141, 80 + 51, 2, 5, 0, 1, 5, 0, 1}, {120, 80, 120 - 141, 80 - 51, 2, 5, 0, 1, 5, 0, 2},
    {120, 80, 120 - 75, 80 - 130, 2, 5, 0, 1, 5, 0, 0}, {120, 80, 120 + 26, 80 - 148, 2, 5, 0, 1, 5, 0, 1},
    {120, 80, 120 + 115, 80 - 96, 2, 5, 0, 1, 5, 0, 2},
};

static void RTNecrozma_Init(struct Task *task)
{
    u16 sp = LC_EnemySpecies();
    if (sp != SPECIES_NECROZMA_DUSK_MANE && sp != SPECIES_NECROZMA_DAWN_WINGS && sp != SPECIES_NECROZMA_ULTRA)
        sp = SPECIES_NECROZMA;
    LC_Begin(task, 0x9E62);
    if (sLC == NULL)
        return;
    task->tLcVar = sp;
    LC_StrokesInit(sLCN_Strokes, LCN_RAY_N);
    // het zwarte prisma: een kristal (Tera-art) dat helemaal zwart is
    LI_Make(0, gBattleAnimSpriteGfx_TeraCrystal, 0x800, gBattleAnimSpritePal_TeraCrystal, LCN_TAG_PRISM, &sGI_Oam64Affine, 120, 80, 2);
    LC_Additive(16);
}

static bool8 RTNecrozma_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, j, k, edge;
    u32 keep, monBit;
    struct Sprite *mon = LI_S(0);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = GI_SpritePalBit(LCN_TAG_PRISM);
    keep = monBit;
    GI_ResetPals(keep);
    LC_GenStrokes(task);

    // eerst fel wit, dan zuigt het prisma het licht weg
    if (t < LCN_PRISM)
        BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, min(16, r * 3), RGB_WHITE);
    else
    {
        k = min(28, (t - LCN_PRISM) * 28 / (LC_HIT - 24 - LCN_PRISM));
        if (k < 8)
            BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, 16 - k * 2, RGB_WHITE);
        else
            BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, min(16, (k - 8) * 16 / 20), RGB_BLACK);
    }

    // stralen: de buitenste stappen doven eerst, de rest wordt feller naar het midden toe
    edge = 6 - (t - LCN_RAYS) * 6 / (LC_HIT - 4 - LCN_RAYS);   // stappen < edge zijn nog zichtbaar
    for (j = 0; j < 3; j++)
    {
        cols[0] = cols[6] = cols[7] = cols[13] = cols[14] = cols[15] = 0;
        for (i = 1; i <= 5; i++)
        {
            u16 c = sLCN_Spectrum[j * 3 + ((i + (t >> 2)) % 3)];
            bool32 on = t >= LCN_RAYS && i < edge;
            cols[i] = on ? Tapu_Blend(c, RGB_WHITE, (5 - i) * 2) : 0;
            cols[i + 7] = on ? Tapu_Blend(c, 0, 9) : 0;
        }
        LC_SetBgPal(j, cols);
    }

    // het zwarte prisma
    k = t - LCN_PRISM;
    mon->invisible = k < 0;
    if (k >= 0)
    {
        BlendPalettes(monBit, 16, RGB(1, 0, 2));
        if (mon->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(mon->oam.matrixNum, 160 + min(k, 60) * 2 + (6 - min(6, t % 20)) * 4,
                                        160 + min(k, 60) * 2 + (6 - min(6, t % 20)) * 4, (u16)(k * 64));
    }
    if (LC_Cross(task, t, LCN_PRISM))
        PlaySE(SE_M_COSMIC_POWER);
    if (LC_Cross(task, t, LCN_RAYS))
        PlaySE(SE_M_GIGA_DRAIN);
    if (LC_Cross(task, t, LCN_RAYS + 20))
        PlayCry_Normal(task->tLcVar, 0);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 4, PALETTES_ALL, RGB_BLACK);
}

static void RTNecrozma_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCN_TAG_PRISM);
}

static const struct RouteTransition sRT_LegendNecrozma =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTNecrozma_Init, RTNecrozma_Update, RTNecrozma_Finish
};

static void Task_LegendNecrozma(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendNecrozma);
}

// =====================================================================================================================
// Galar-Zapdos (Route 111, rent rondjes; vechttype): stofstrepen razen voorbij, op elke achtste een stofwolk van de
// sprint (links naar het midden), en dan de trap: de klauw (de voet uit de Mega Kick-art) komt op je af, een inslag
// (de ster uit de klap-art) en scheuren vanuit het midden.
#define LCGZ_TAG_FOOT  0x5B2A
#define LCGZ_TAG_HIT   0x5B2B
#define LCGZ_TAG_DUST  0x5B36
#define LCGZ_DUST      8
#define LCGZ_RUN       LC_BEAT(3)
#define LCGZ_KICK      LC_BEAT(6)
#define LCGZ_IMPACT    LC_BEAT(7)

static const struct LCStroke sLCGZ_Strokes[] =
{
    {0, 22, 140, 22, 1, 3, 0, 1, 1, 0, 0}, {120, 46, 255, 46, 1, 3, 0, 2, 1, 0, 0}, {10, 98, 170, 98, 1, 3, 0, 3, 1, 0, 0},
    {150, 124, 255, 124, 1, 3, 0, 1, 1, 0, 0}, {0, 146, 100, 146, 1, 3, 0, 2, 1, 0, 0},
    {120, 80, 0, 20, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 250, 40, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 30, 160, 1, 4, 0, 5, 2, 13, 0},
    {120, 80, 230, 160, 1, 4, 0, 5, 2, 13, 0}, {120, 80, 140, 0, 1, 4, 0, 5, 2, 13, 0},
};

static void RTGalarZapdos_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0x6A2D);
    if (sLC == NULL)
        return;
    LC_StrokesInit(sLCGZ_Strokes, ARRAY_COUNT(sLCGZ_Strokes));
    LI_Make(0, gBattleAnimSpriteGfx_HandsAndFeet, 0x800, LC_Tint(gBattleAnimSpritePal_HandsAndFeet, RGB(10, 4, 2), RGB(31, 24, 12)),
            LCGZ_TAG_FOOT, &sGI_Oam32Affine, 120, 80, 0);
    LI_Frame(0, LCGZ_TAG_FOOT, 2, 16);
    LI_Make(1, gBattleAnimSpriteGfx_Impact, 0x200, gBattleAnimSpritePal_Impact, LCGZ_TAG_HIT, &sGI_Oam32Affine, 120, 80, 1);
    for (i = 0; i < LCGZ_DUST; i++)
        LI_Make(2 + i, gBattleAnimSpriteGfx_Smoke, 0x100, LC_Tint(gBattleAnimSpritePal_Smoke, RGB(10, 5, 2), RGB(30, 22, 12)),
                LCGZ_TAG_DUST, &sGI_Oam16, 0, 0, 3);
    LC_Additive(13);
}

static bool8 RTGalarZapdos_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep;
    struct Sprite *s, *foot = LI_S(0), *hit = LI_S(1);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCGZ_TAG_DUST) | GI_SpritePalBit(LCGZ_TAG_FOOT) | GI_SpritePalBit(LCGZ_TAG_HIT);
    GI_ResetPals(keep);
    LC_GenStrokes(task);
    LC_DimWorld(r, keep, 12, RGB(5, 2, 1));

    cols[0] = cols[4] = cols[7] = cols[11] = cols[14] = cols[15] = 0;
    for (i = 0; i < 3; i++)
    {
        k = ((r >> 1) + i * 2) % 6;
        cols[1 + i] = (t < LCGZ_IMPACT) ? (k < 2 ? RGB(31, 26, 16) : RGB(16, 9, 4)) : 0;
        cols[8 + i] = Tapu_Blend(cols[1 + i], 0, 9);
    }
    for (i = 0; i < 2; i++)
    {
        cols[5 + i] = LC_SlashColor(t, LCGZ_IMPACT + i, RGB(31, 26, 12), RGB(20, 8, 2), 30);
        cols[12 + i] = Tapu_Blend(cols[5 + i], 0, 8);
    }
    LC_SetBgPal(0, cols);
    SetGpuReg(REG_OFFSET_BG0HOFS, (r * 12) & 0x1FF);

    // de sprint: op elke achtste een stofwolk, links naar het midden (om en om hoog en laag)
    for (i = 0; i < LCGZ_DUST; i++)
    {
        s = LI_S(2 + i);
        k = t - LC_E8(6 + i);
        s->invisible = k < 0 || k >= 20 || t >= LCGZ_IMPACT;
        s->x = 8 + i * 15 - k / 2;
        s->y = 116 + ((i & 1) ? 6 : -6) - k / 3;
        LI_Frame(2 + i, LCGZ_TAG_DUST, k >= 10, 4);
    }

    // de trap
    k = t - LCGZ_KICK;
    foot->invisible = k < 0 || t >= LCGZ_IMPACT + 4;
    if (k >= 0 && foot->oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        s32 sc = 64 + k * k * 448 / ((LCGZ_IMPACT - LCGZ_KICK) * (LCGZ_IMPACT - LCGZ_KICK));
        SetOamMatrixRotationScaling(foot->oam.matrixNum, min(sc, 512), min(sc, 512), 0x2000);
    }
    k = t - LCGZ_IMPACT;
    hit->invisible = k < 0 || k >= 10;
    if (k >= 0 && hit->oam.affineMode != ST_OAM_AFFINE_OFF)
        SetOamMatrixRotationScaling(hit->oam.matrixNum, min(512, 256 + k * 40), min(512, 256 + k * 40), (u16)(k * 0x600));

    if (LC_Cross(task, t, LCGZ_RUN))
        PlaySE(SE_M_DOUBLE_SLAP);
    if (LC_Cross(task, t, LCGZ_RUN + 16))
        PlayCry_Normal(SPECIES_ZAPDOS_GALAR, 0);
    if (LC_Cross(task, t, LCGZ_KICK))
        PlaySE(SE_M_JUMP_KICK);
    if (LC_Cross(task, t, LCGZ_IMPACT))
        PlaySE(SE_M_MEGA_KICK);
    GI_Shake(t >= LCGZ_IMPACT && t < LCGZ_IMPACT + 12 ? 3 : 0);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(31, 28, 20));
}

static void RTGalarZapdos_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCGZ_TAG_DUST);
    GI_FreeTag(LCGZ_TAG_FOOT);
    GI_FreeTag(LCGZ_TAG_HIT);
}

static const struct RouteTransition sRT_LegendGalarZapdos =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTGalarZapdos_Init, RTGalarZapdos_Update, RTGalarZapdos_Finish
};

static void Task_LegendGalarZapdos(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendGalarZapdos);
}

// =====================================================================================================================
// Galar-Moltres (Route 120, mist bij de tombe; duister type): de plek zakt weg in zwartpaars, zwarte vlammen (het vuur
// uit de gevechtsanimaties, paarszwart gekleurd) laaien op langs de onderrand, een duistere aura pulseert op de tel
// en daaruit laait één grote zwarte vlam op; op de klokslag slokt de aura het beeld op (Fiery Wrath).
#define LCGM_FLAMES    8
#define LCGM_AURA      LCGM_FLAMES   // drie ringen
#define LCGM_RINGS     3
#define LCGM_CORE      (LCGM_AURA + LCGM_RINGS)   // één grote zwarte vlam in het midden
#define LCGM_TAG_FIRE  0x5B2C
#define LCGM_TAG_AURA  0x5B2D
#define LCGM_MON       LC_BEAT(4)
#define LCGM_WRATH     LC_BEAT(7)

static void RTGalarMoltres_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0x6A30);
    if (sLC == NULL)
        return;
    for (i = 0; i < LCGM_FLAMES; i++)
        LI_Make(i, gBattleAnimSpriteGfx_Fire, 0x1000, LC_Tint(gBattleAnimSpritePal_Fire, RGB(0, 0, 0), RGB(13, 2, 17)),
                LCGM_TAG_FIRE, &sGI_Oam32, 0, 0, 1);
    for (i = 0; i < LCGM_RINGS; i++)
    {
        LI_Make(LCGM_AURA + i, gBattleAnimSpriteGfx_ThinRing, 0x800, LC_Tint(gBattleAnimSpritePal_ThinRing, RGB(4, 0, 8), RGB(22, 6, 28)),
                LCGM_TAG_AURA, &sGI_Oam64Affine, 120, 76, 4);
        LI_S(LCGM_AURA + i)->oam.objMode = ST_OAM_OBJ_BLEND;
    }
    LI_Make(LCGM_CORE, gBattleAnimSpriteGfx_Fire, 0x1000, gBattleAnimSpritePal_Fire, LCGM_TAG_FIRE, &sGI_Oam32Affine, 120, 70, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(10, 10));
}

static bool8 RTGalarMoltres_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep;
    struct Sprite *s;

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    keep = GI_SpritePalBit(LCGM_TAG_FIRE) | GI_SpritePalBit(LCGM_TAG_AURA);
    GI_ResetPals(keep);
    LC_DimWorld(r, keep, 13, RGB(2, 0, 4));

    // zwarte vlammen langs de onderrand, steeds hoger
    for (i = 0; i < LCGM_FLAMES; i++)
    {
        s = LI_S(i);
        k = r - i * 3;
        s->invisible = k < 0;
        s->x = 16 + i * 30;
        s->y = 160 - min(k, 20) - (t >= LCGM_WRATH ? (t - LCGM_WRATH) * 4 : 0) + Sin((t * 8 + i * 50) & 0xFF, 2);
        LI_Frame(i, LCGM_TAG_FIRE, ((t >> 2) + i) & 7, 16);
    }

    // de aura: op elke tel een duistere ring die uitdijt
    for (i = 0; i < LCGM_RINGS; i++)
    {
        s32 b, born = -1;
        s = LI_S(LCGM_AURA + i);
        for (b = 3 + i; b < 12; b += LCGM_RINGS)
            if (t >= LC_BEAT(b))
                born = LC_BEAT(b);
        k = t - born;
        s->invisible = born < 0 || k >= 40;
        if (!s->invisible && s->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(s->oam.matrixNum, min(512, 96 + k * 12), min(512, 96 + k * 12), 0);
    }

    // uit de aura laait één grote zwarte vlam op, die op de tel opflakkert
    s = LI_S(LCGM_CORE);
    k = t - LCGM_MON;
    s->invisible = k < 0;
    LI_Frame(LCGM_CORE, LCGM_TAG_FIRE, (t >> 2) & 7, 16);
    if (k >= 0 && s->oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        s32 sc = min(480, 96 + k * 8) + (6 - min(6, t % 20)) * 10 + (t >= LCGM_WRATH ? (t - LCGM_WRATH) * 12 : 0);
        SetOamMatrixRotationScaling(s->oam.matrixNum, sc, sc, 0);
        s->y = 70 - min(k, 40) / 4;
    }
    if (LC_Cross(task, t, LC_BEAT(3)))
        PlaySE(SE_M_NIGHTMARE);
    if (LC_Cross(task, t, LCGM_MON + 12))
        PlayCry_Normal(SPECIES_MOLTRES_GALAR, 0);
    if (LC_Cross(task, t, LCGM_WRATH))
        PlaySE(SE_M_FLAME_WHEEL2);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(8, 0, 12));
}

static void RTGalarMoltres_Finish(struct Task *task)
{
    LC_FinishCommon(task);
    GI_FreeTag(LCGM_TAG_FIRE);
    GI_FreeTag(LCGM_TAG_AURA);
}

static const struct RouteTransition sRT_LegendGalarMoltres =
{
    sLC_BlankTile, 32, sLC_Pal0, 1, 1, 0, RTGalarMoltres_Init, RTGalarMoltres_Update, RTGalarMoltres_Finish
};

static void Task_LegendGalarMoltres(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendGalarMoltres);
}
