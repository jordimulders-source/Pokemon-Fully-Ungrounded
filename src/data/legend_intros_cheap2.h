// Project Grounded: goedkope legendary-intro's (Jordi: "maak deze intro's goedkoop qua kbs"). Calyrex/Glastrier/
// Spectrier, Celebi, het meren-trio, Meloetta, Latias/Latios, Zeraora, Cresselia, de Galar-vogels en Zygarde.
// Geen eigen art: alle BG0-beelden worden bij de start in C getekend (gradiënten met Bayer-dither, boomsilhouetten,
// ijs, slagen, de maan) en de rest is gevechtsanimatie-art en frontsprites die al in de ROM staan. Wordt onderaan
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
#define tLcMon2       data[15]               // tweede frontsprite (spiegelbeeld)

struct LCWork
{
    u16 map[32 * 20];
    u16 order[600];
    u8 top[256];
    u8 rowv[DISPLAY_HEIGHT];
    u8 cell[160];
    u8 frame[160];
    u16 tmp[16];
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
    task->tLcMon2 = MAX_SPRITES;
    task->tGiSprite0 = MAX_SPRITES;
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

static u8 LC_MonPic(u16 species, s16 x, s16 y, u8 prio)
{
    u8 id = GI_MonPic(species, x, y);
    if (id < MAX_SPRITES)
        gSprites[id].oam.priority = prio;
    return id;
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
    LI_DestroyMonPic(task->tGiSprite0);
    if (task->tLcMon2 < MAX_SPRITES)
        FreeAndDestroyMonPicSprite(task->tLcMon2);
    task->tGiSprite0 = task->tLcMon2 = MAX_SPRITES;
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
//   beschermer, stofwolkjes bij elke stap; het silhouet van de koning staat voor de zon met een lasso die rondzwiept;
//   op de klokslag gooit hij de lasso naar je toe en licht het bos groen op. De ruiters zetten de stappen van hun
//   paard (ijs of spookvuur).
// - Glastrier: de echte plek wordt koud blauw, elke stap bevriest (ijskristal) en de rijp groeit vanuit de afdrukken
//   over het hele beeld (BG0 telt op bij de wereld; 15 groeifasen in de paletkleuren).
// - Spectrier: de plek wordt zwartpaars, elke afdruk vat paars spookvuur en dooft weer; Spectrier flakkert half
//   doorzichtig op.
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
    {
        LI_Make(LCR_LASSO, gBattleAnimSpriteGfx_ThinRing, 0x800, gBattleAnimSpritePal_ThinRing, LCR_TAG_ROPE, &sGI_Oam64Affine, 120, 40, 1);
        task->tGiSprite0 = LC_MonPic(sp, 120, 84, 0);
    }
    else
    {
        task->tGiSprite0 = LC_MonPic(sp, 120, 74, 0);
    }

    if (v == LCR_GLASTRIER)
    {
        // de rijp telt op bij de wereld (zwart = niets)
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                                   | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 16));
        SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
        SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
    }
    else if (v == LCR_SPECTRIER)
    {
        if (task->tGiSprite0 < MAX_SPRITES)
            gSprites[task->tGiSprite0].oam.objMode = ST_OAM_OBJ_BLEND;
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_BD);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(10, 8));
    }
}

static bool8 RTCrown_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, age, beatK;
    u32 v = task->tLcVar, step = LCR_Step(v), keep, monBit;
    bool32 sunset = LCR_Sunset(v), done = FALSE;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCR_TAG_SHOE) | GI_SpritePalBit(LCR_TAG_FX) | GI_SpritePalBit(LCR_TAG_ROPE);
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

    // de legendary
    if (sunset)
    {
        struct Sprite *rope = LI_S(LCR_LASSO);
        u8 mat = rope->oam.matrixNum;
        k = t - LCR_MON_SHOW;
        mon->invisible = k < 0;
        if (k >= 0 && t < LC_HIT)
        {
            // silhouet voor de zon: komt uit de lucht op
            BlendPalettes(monBit, 16, Tapu_Blend(RGB(31, 24, 10), RGB(2, 1, 3), min(16, k * 2)));
            mon->y = 84 + max(0, 12 - k);
        }
        else if (k >= 0)
        {
            BlendPalettes(monBit, max(0, 16 - (t - LC_HIT) * 4), RGB_WHITE);
        }
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
    else
    {
        k = t - LC_BEAT(6);
        mon->invisible = k < 0;
        mon->y2 = Sin((t * 5) & 0xFF, 2);
        if (v == LCR_GLASTRIER && k >= 0)
            BlendPalettes(monBit, max(0, 16 - k), RGB_WHITE);
        else if (k >= 0)
        {
            BlendPalettes(monBit, max(0, 12 - k / 2), RGB(10, 0, 18));
            if (t < LC_HIT && (Random() & 7) == 0)
                mon->invisible = TRUE;
        }
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
// Celebi (Ilex Forest; Jordi: "mag een iconische Gold/Silver intro, met forest protection"): de echte plek valt
// terug in vier Game Boy Color-groentinten (alles, ook Celebi zelf). Het GS-flikkeren op de eerste drie tellen, dan
// wervelen de bladeren naar binnen, de tijd brokkelt (mozaïek) en in het midden zet zich een groene beschermkoepel uit
// waarin Celebi verschijnt. Daarna de GS-spiraal: zwarte vakjes draaien van buiten naar binnen dicht, tot de klokslag.
#define LCC_LEAVES     16
#define LCC_DOME       LCC_LEAVES
#define LCC_TAG_LEAF   0x5B23
#define LCC_TAG_DOME   0x5B24
#define LCC_FLICKER    LC_BEAT(3)   // tel 3 en 4
#define LCC_SWIRL      50
#define LCC_DOME_T     92
#define LCC_MON        LC_BEAT(5)
#define LCC_SPIRAL     128

static const u16 sLC_Gbc[4] = {RGB(3, 7, 4), RGB(9, 16, 8), RGB(19, 25, 10), RGB(28, 31, 21)};
static const u16 sLCC_Pal15[16] = {0, RGB(3, 7, 4)};

static u16 LC_GbcColor(u16 c)
{
    s32 l = (c & 31) * 5 + ((c >> 5) & 31) * 9 + ((c >> 10) & 31) * 2;
    return sLC_Gbc[l < 120 ? 0 : (l < 240 ? 1 : (l < 360 ? 2 : 3))];
}

static void LC_GbcPals(u32 mask)
{
    u32 i, j;
    for (i = 0; i < 32; i++)
    {
        if (!((mask >> i) & 1))
            continue;
        for (j = 0; j < 16; j++)
            gPlttBufferUnfaded[i * 16 + j] = LC_GbcColor(gPlttBufferUnfaded[i * 16 + j]);
        CpuCopy16(&gPlttBufferUnfaded[i * 16], &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
    }
}

// spiraal van buiten naar binnen (met de klok mee, linksboven beginnen)
static void LCC_MakeSpiral(void)
{
    s32 x0 = 0, y0 = 0, x1 = 29, y1 = 19, n = 0, x, y;
    while (x0 <= x1 && y0 <= y1)
    {
        for (x = x0; x <= x1; x++)
            sLC->order[n++] = y0 * 32 + x;
        for (y = y0 + 1; y <= y1; y++)
            sLC->order[n++] = y * 32 + x1;
        if (y0 < y1)
            for (x = x1 - 1; x >= x0; x--)
                sLC->order[n++] = y1 * 32 + x;
        if (x0 < x1)
            for (y = y1 - 1; y > y0; y--)
                sLC->order[n++] = y * 32 + x0;
        x0++, y0++, x1--, y1--;
    }
}

static void RTCelebi_Init(struct Task *task)
{
    u32 i, mine;
    LC_Begin(task, 0xCE1);
    if (sLC == NULL)
        return;
    LCC_MakeSpiral();
    // eerst de wereld (alle paletten die er nu zijn), dan onze sprites apart
    LC_GbcPals(PALETTES_ALL & ~(1 << 15));
    for (i = 0; i < LCC_LEAVES; i++)
        LI_Make(i, gBattleAnimSpriteGfx_Leaf, 0x480, gBattleAnimSpritePal_Leaf, LCC_TAG_LEAF, &sGI_Oam16, 120, 80, 2);
    LI_Make(LCC_DOME, gBattleAnimSpriteGfx_CircleOfLight, 0x800, gBattleAnimSpritePal_WhiteCircleOfLight, LCC_TAG_DOME, &sGI_Oam64Affine, 120, 76, 3);
    task->tGiSprite0 = LC_MonPic(SPECIES_CELEBI, 120, 74, 1);
    mine = GI_SpritePalBit(LCC_TAG_LEAF) | GI_SpritePalBit(LCC_TAG_DOME) | LI2_MonBit(task->tGiSprite0);
    LC_GbcPals(mine);
    for (i = 0; i <= LCC_DOME; i++)
        LI_S(i)->oam.priority = 1;   // onder de spiraal (BG0)
    LI_S(LCC_DOME)->oam.objMode = ST_OAM_OBJ_BLEND;
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(7, 12));
    SetGpuReg(REG_OFFSET_MOSAIC, 0);
    SetGpuRegBits(REG_OFFSET_BG1CNT, BGCNT_MOSAIC);
    SetGpuRegBits(REG_OFFSET_BG2CNT, BGCNT_MOSAIC);
    SetGpuRegBits(REG_OFFSET_BG3CNT, BGCNT_MOSAIC);
}

static bool8 RTCelebi_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), i, k, r, n;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0), *dome = LI_S(LCC_DOME);
    u16 *tilemap = RT_Tilemap();

    if (sLC == NULL)
        return TRUE;
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCC_TAG_LEAF) | GI_SpritePalBit(LCC_TAG_DOME);
    // alles (ook de wereld) terug naar de GBC-tinten; die staan al in 'unfaded'
    CpuCopy16(gPlttBufferUnfaded, gPlttBufferFaded, PLTT_SIZE);

    // GS-flikkeren op tel 1, 2 en 3: licht, donker, licht
    for (i = 0; i < 2; i++)
    {
        k = t - LCC_FLICKER - LC_BEAT(i);
        if (k >= 0 && k < 8)
            BlendPalettes(PALETTES_ALL & ~keep, 14 - k * 2, (i == 1) ? sLC_Gbc[0] : sLC_Gbc[3]);
    }

    // de tijd brokkelt
    k = (t > LC_BEAT(4)) ? min(4, (t - LC_BEAT(4)) / 9) : 0;
    SetGpuReg(REG_OFFSET_MOSAIC, k | (k << 4));

    // bladeren wervelen naar binnen
    for (i = 0; i < LCC_LEAVES; i++)
    {
        s = LI_S(i);
        k = t - LCC_SWIRL;
        r = 150 - k * 150 / (LCC_SPIRAL + 24 - LCC_SWIRL);
        s->invisible = k < 0 || r < 8;
        if (s->invisible)
            continue;
        s->x = 120 + Cos((i * 16 + k * 3 + k * k / 40) & 0xFF, r);
        s->y = 76 + Sin((i * 16 + k * 3 + k * k / 40) & 0xFF, r * 2 / 3);
        LI_Frame(i, LCC_TAG_LEAF, ((t >> 2) + i) % 9, 4);
    }

    // de beschermkoepel zet zich uit en pulseert op de tel
    k = t - LCC_DOME_T;
    dome->invisible = k < 0;
    if (k >= 0 && dome->oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        s32 sc = min(560, k * 14) + (6 - min(6, t % 20)) * 8;
        SetOamMatrixRotationScaling(dome->oam.matrixNum, sc, sc, 0);
    }

    // Celebi
    k = t - LCC_MON;
    mon->invisible = k < 0;
    mon->y2 = Sin((t * 6) & 0xFF, 3);
    if (k >= 0 && k < 16)
        BlendPalettes(monBit, 16 - k, sLC_Gbc[3]);
    if (LC_Cross(task, t, LCC_MON + 8))
        PlayCry_Normal(SPECIES_CELEBI, 0);
    if (LC_Cross(task, t, LCC_SWIRL))
        PlaySE(SE_M_RAZOR_WIND);

    // GS-spiraal
    k = t - LCC_SPIRAL;
    if (k >= 0)
    {
        n = min(600, (k + 1) * 600 / (LC_HIT - LCC_SPIRAL));
        for (i = 0; i < n; i++)
            tilemap[sLC->order[i]] = 1 | (15 << 12);
    }
    task->tLcLast = t;
    return t >= LC_HIT + 1;
}

static void RTCelebi_Finish(struct Task *task)
{
    SetGpuReg(REG_OFFSET_MOSAIC, 0);
    ClearGpuRegBits(REG_OFFSET_BG1CNT, BGCNT_MOSAIC);
    ClearGpuRegBits(REG_OFFSET_BG2CNT, BGCNT_MOSAIC);
    ClearGpuRegBits(REG_OFFSET_BG3CNT, BGCNT_MOSAIC);
    LC_FinishCommon(task);
    GI_FreeTag(LCC_TAG_LEAF);
    GI_FreeTag(LCC_TAG_DOME);
}

static const struct RouteTransition sRT_LegendCelebi =
{
    sLC_BlankTile, 32, sLCC_Pal15, 1, 1, 0, RTCelebi_Init, RTCelebi_Update, RTCelebi_Finish
};

static void Task_LegendCelebi(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendCelebi);
}

// =====================================================================================================================
// Uxie, Mesprit, Azelf (de Gen 4-meren; Jordi: "Feeling trio mag je een lake met daarna fadeout naar blauw, geel of
// roze afhankelijk van de pokemon"): een stil meer in de ochtendmist, de verre oever als bosrand, glinsteringen op het
// water. Op elke tel een kring in het water; de Pokémon rijst op boven het meer, met zijn spiegelbeeld (half doorzichtig,
// golvend) eronder. Dan kleurt alles naar zijn edelsteen: Uxie geel, Mesprit roze, Azelf blauw.
#define LCL_RINGS      4
#define LCL_TAG_RING   0x5B25
#define LCL_SURFACE    48
#define LCL_SKY_N      8
#define LCL_WATER_N    10
#define LCL_MON_T      LC_BEAT(3)
#define LCL_MON_Y      70
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
    u16 sp = LC_EnemySpecies();
    if (sp != SPECIES_UXIE && sp != SPECIES_MESPRIT)
        sp = SPECIES_AZELF;
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
    task->tGiSprite0 = LC_MonPic(sp, 120, LCL_MON_Y, 0);
    task->tLcMon2 = LC_MonPic(sp, 120, 2 * LCL_RIPPLE_Y - LCL_MON_Y - 4, 0);
    if (task->tLcMon2 < MAX_SPRITES)
    {
        struct Sprite *r = &gSprites[task->tLcMon2];
        r->vFlip = TRUE;
        r->oam.matrixNum |= ST_OAM_VFLIP;
        r->oam.objMode = ST_OAM_OBJ_BLEND;
        r->subpriority = 4;
    }
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(6, 10));
}

static bool8 RTLake_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0), *ref = GI_Sprite(task->tLcMon2);
    u16 cols[16];
    bool32 done;

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCL_TAG_RING);
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

    // de Pokémon rijst op met zijn spiegelbeeld
    k = t - LCL_MON_T;
    mon->invisible = ref->invisible = k < 0;
    if (k >= 0)
    {
        s32 rise = max(0, 24 - k) * max(0, 24 - k) / 24;
        mon->y2 = rise + Sin((t * 5) & 0xFF, 2);
        ref->y2 = -rise - Sin((t * 5) & 0xFF, 2);
        ref->x2 = Sin((t * 9) & 0xFF, 2);
        if (k < 24)
            BlendPalettes(monBit, 16 - k * 2 / 3, RGB(4, 9, 16));
    }
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
// Meloetta (Jordi: "mag je heel veel noten het beeld laten vullen"): de muzieknoten van Sing (gevechtsanimatie) als
// BG0-tiles. Op elke tel verdubbelt het aantal noten (1, 3, 7, 15, 31, 63, 127): op de klokslag staat het hele beeld
// vol. De noten dansen (golf per beeldlijn, hupje op de tel) en wisselen op elke tel van kleur; Meloetta zingt in
// het midden en er stijgen losse noten op.
#define LCM_CELLS      160   // 16 x 10 vakken van 16 x 16
#define LCM_TILE0      16
#define LCM_FLOATS     8
#define LCM_TAG_NOTE   0x5B26
#define LCM_MON_T      LC_BEAT(3)

// aantal noten na tel b (het eigen deel begint rond tel 2,4)
static const u8 sLCM_Count[9] = {0, 0, 0, 3, 8, 20, 44, 96, LCM_CELLS};

static void RTMeloetta_Init(struct Task *task)
{
    u32 i, j;
    u16 sp = LC_EnemySpecies(), *tilemap, *tileset;
    if (sp != SPECIES_MELOETTA_PIROUETTE)
        sp = SPECIES_MELOETTA_ARIA;
    LC_Begin(task, 0x3E10);
    if (sLC == NULL)
        return;
    GetBg0TilesDst(&tilemap, &tileset);
    DecompressDataWithHeaderVram(gBattleAnimSpriteGfx_MusicNotes2, tileset + LCM_TILE0 * 16);
    for (i = 0; i < LCM_CELLS; i++)
        sLC->cell[i] = i;
    for (i = LCM_CELLS - 1; i > 0; i--)
    {
        u8 tmp;
        j = LC_Rand() % (i + 1);
        tmp = sLC->cell[i];
        sLC->cell[i] = sLC->cell[j];
        sLC->cell[j] = tmp;
    }
    for (i = 0; i < LCM_CELLS; i++)
        sLC->frame[i] = LC_Rand() & 15;
    for (i = 0; i < LCM_FLOATS; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_MusicNotes2, 0x800, gBattleAnimSpritePal_MusicNotes2, LCM_TAG_NOTE, &sGI_Oam16, 120, 80, 1);
        LI_Frame(i, LCM_TAG_NOTE, (i * 5) & 15, 4);
    }
    task->tGiSprite0 = LC_MonPic(sp, 120, 80, 0);
    LI_InitWave();
    // de golf zet elke VBlank ook de vensters: alles laten zien (anders blijft alleen de achtergrondkleur over)
    sTransitionData->WININ = WININ_WIN0_ALL | WININ_WIN1_ALL;
    sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;
}

static void LCM_PutNote(u16 *tilemap, u32 cell, u32 frame)
{
    u32 cx = (cell & 15) * 2, cy = (cell >> 4) * 2, pal = 13 + (cell % 3);
    u32 base = LCM_TILE0 + frame * 4;
    tilemap[cy * 32 + cx] = base | (pal << 12);
    tilemap[cy * 32 + cx + 1] = (base + 1) | (pal << 12);
    tilemap[(cy + 1) * 32 + cx] = (base + 2) | (pal << 12);
    tilemap[(cy + 1) * 32 + cx + 1] = (base + 3) | (pal << 12);
}

static bool8 RTMeloetta_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, n, b, ph;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0);
    u16 *tilemap = RT_Tilemap();
    s16 *hofs = (s16 *)gScanlineEffectRegBuffers[0];

    if (sLC == NULL)
        return TRUE;
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCM_TAG_NOTE);
    r = LC_R(t);
    GI_ResetPals(keep);
    LC_DimWorld(r, keep, 12, RGB(5, 1, 9));

    // de kleuren draaien op elke tel door (rood/geel, groen/blauw, blauw/roze)
    b = t * 1000 / 20363;
    ph = t - LC_BEAT(b);
    for (i = 0; i < 3; i++)
        LC_SetBgPal(i, LC_Rotate(gBattleAnimSpritePal_MusicNotes2, (i + b) % 3));
    if (b >= 3 && ph < 6)
        BlendPalettes(GI_BG_PALS, 12 - ph * 2, RGB_WHITE);

    // noten: verdubbelen op elke tel
    n = sLCM_Count[min(b, 8)];
    for (i = 0; i < n; i++)
        LCM_PutNote(tilemap, sLC->cell[i], sLC->frame[sLC->cell[i]]);

    // dansen: golf per beeldlijn en een hupje op de tel
    for (i = 0; i < DISPLAY_HEIGHT; i++)
        hofs[i] = Sin((i * 3 + t * 5) & 0xFF, 3);
    SetGpuReg(REG_OFFSET_BG0VOFS, (ph < 4 && b >= 3) ? 2 : 0);

    // Meloetta zingt
    k = t - LCM_MON_T;
    mon->invisible = k < 0;
    mon->y2 = -abs(Sin((t * 256 / 41) & 0xFF, 4));
    if (k >= 0 && k < 12)
        BlendPalettes(monBit, 16 - k * 4 / 3, RGB_WHITE);
    if (LC_Cross(task, t, LCM_MON_T + 8))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    for (i = 0; i < LCM_FLOATS; i++)
    {
        s = LI_S(i);
        k = (t - LCM_MON_T - i * 7);
        s->invisible = k < 0;
        k %= 56;
        s->x = 120 + ((i & 1) ? 24 : -24) + Sin((k * 6 + i * 32) & 0xFF, 10);
        s->y = 72 - k * 3 / 2;
    }

    task->tLcLast = t;
    return LC_Out(t, LC_HIT + 1, 5, PALETTES_ALL, RGB_WHITE);
}

static void RTMeloetta_Finish(struct Task *task)
{
    LI_EndWave();
    LC_FinishCommon(task);
    GI_FreeTag(LCM_TAG_NOTE);
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

// BG0 telt op bij alles eronder (zwart = niets)
static void LC_Additive(u32 eva)
{
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3
                               | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(eva, 16));
    SetGpuReg(REG_OFFSET_WININ, GetGpuReg(REG_OFFSET_WININ) | WININ_WIN0_CLR | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, GetGpuReg(REG_OFFSET_WINOUT) | WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
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
// (drie gekartelde strepen) trekken op de tellen over het beeld, Zeraora flakkert op tussen de vonken, en dan komt de
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
    task->tGiSprite0 = LC_MonPic(SPECIES_ZERAORA, 120, 76, 0);
    if (task->tGiSprite0 < MAX_SPRITES)
        gSprites[task->tGiSprite0].subpriority = 5;
    LC_Additive(14);
}

static bool8 RTZeraora_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0), *paw;
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCZ_TAG_PAW) | GI_SpritePalBit(LCZ_TAG_SPARK);
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

    // Zeraora tussen de vonken
    k = t - LCZ_MON;
    mon->invisible = k < 0 || (t < LCZ_PAW && (Random() & 7) == 0);
    if (k >= 0 && k < 10)
        BlendPalettes(monBit, 16 - k * 3 / 2, RGB(31, 31, 12));
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
// Zygarde (alle vormen; Jordi: "een legends ZA groene Z zoals Zorro het beeld laten splijten"): drie snelle sneden op
// de achtsten, boven, schuin en onder: een groene Z over de plek. Zygarde verschijnt, de Z gloeit op, wordt een kier
// van licht en het beeld splijt (de kier gaat open, het beeld trilt), groen-wit.
#define LCY_CUT        LC_E8(8)
#define LCY_MON        LC_E8(11)
#define LCY_SPLIT      LC_BEAT(6)

static const struct LCStroke sLCY_Strokes[] =
{
    {36, 34, 206, 34, 2, 6, 14, 1, 2, 0, 0},
    {206, 34, 34, 128, 2, 6, 14, 3, 2, 0, 0},
    {34, 128, 206, 128, 2, 6, 14, 5, 2, 0, 0},
};

static void RTZygarde_Init(struct Task *task)
{
    u16 sp = LC_EnemySpecies();
    if (sp != SPECIES_ZYGARDE_10_AURA_BREAK && sp != SPECIES_ZYGARDE_COMPLETE)
        sp = SPECIES_ZYGARDE_50;
    LC_Begin(task, 0x2A6D);
    if (sLC == NULL)
        return;
    LC_StrokesInit(sLCY_Strokes, ARRAY_COUNT(sLCY_Strokes));
    task->tGiSprite0 = LC_MonPic(sp, 120, 80, 0);
    LC_Additive(14);
}

static bool8 RTZygarde_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *mon = GI_Sprite(task->tGiSprite0);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit;
    GI_ResetPals(keep);
    LC_GenStrokes(task);
    LC_DimWorld(r, keep, 13, RGB(0, 3, 1));

    cols[0] = 0;
    for (i = 0; i < 6; i++)
    {
        cols[1 + i] = LC_SlashColor(t, LCY_CUT + (i / 2) * LC_E8(1) + (i & 1), RGB(14, 31, 10), RGB(4, 24, 6), 20);
        cols[8 + i] = cols[1 + i] ? Tapu_Blend(0, RGB(2, 20, 4), 10) : 0;
    }
    cols[7] = 0;
    // de kier: de aura gaat open en wordt wit
    k = t - LCY_SPLIT;
    cols[15] = k < 0 ? 0 : Tapu_Blend(RGB(4, 20, 6), RGB(28, 31, 28), min(16, k));
    if (k >= 0)
        for (i = 1; i <= 6; i++)
            cols[i] = cols[i + 7] = Tapu_Blend(cols[i], RGB_WHITE, min(16, k));
    LC_SetBgPal(0, cols);

    k = t - LCY_MON;
    mon->invisible = k < 0;
    if (k >= 0 && k < 12)
        BlendPalettes(monBit, 16 - k * 4 / 3, RGB(6, 28, 8));
    if (t >= LCY_SPLIT)
        mon->x2 = LI_ShakeAmp(2);

    for (i = 0; i < 3; i++)
        if (LC_Cross(task, t, LCY_CUT + i * LC_E8(1)))
            PlaySE(SE_M_CUT);
    if (LC_Cross(task, t, LCY_MON + 6))
        PlayCry_Normal(LC_EnemySpecies(), 0);
    if (LC_Cross(task, t, LCY_SPLIT))
        PlaySE(SE_M_SOLAR_BEAM);
    GI_Shake(t >= LCY_SPLIT ? 1 + (t - LCY_SPLIT) / 12 : 0);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(24, 31, 22));
}

static void RTZygarde_Finish(struct Task *task)
{
    LC_FinishCommon(task);
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
// zacht dromerig (rood-wit of blauw-wit, Soul Dew), strepen eonlicht razen voorbij, de Pokémon schiet twee keer langs
// (als lichtflits, dan andersom) en zweeft dan in het midden; alles loopt over in een zachte kleurwas. Geen sync: de
// Southern Island-gevechten hebben hun eigen muziek.
#define LCE_TAG_NONE   0
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
    if (sp != SPECIES_LATIOS)
        sp = SPECIES_LATIAS;
    LC_Begin(task, 0xE0E0);
    if (sLC == NULL)
        return;
    task->tLcVar = sp;
    LC_StrokesInit(sLCE_Strokes, ARRAY_COUNT(sLCE_Strokes));
    task->tGiSprite0 = LI_MonPicAffine(sp, -60, 60);
    LC_Additive(12);
}

static bool8 RTEon_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *mon = GI_Sprite(task->tGiSprite0);
    u16 cols[16], eon = task->tLcVar == SPECIES_LATIOS ? RGB(8, 14, 31) : RGB(31, 10, 12);
    u16 soft = task->tLcVar == SPECIES_LATIOS ? RGB(24, 27, 31) : RGB(31, 24, 25);

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit;
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

    // langs, andersom, en blijven
    mon->invisible = TRUE;
    if (r >= LCE_FLY1 && r < LCE_FLY1 + 16)
    {
        k = r - LCE_FLY1;
        mon->invisible = FALSE;
        mon->x = -60 + k * 24;
        mon->y = 54;
        LI_Affine(task->tGiSprite0, 300, 0);
        BlendPalettes(monBit, 14, RGB_WHITE);
    }
    else if (r >= LCE_FLY2 && r < LCE_FLY2 + 16)
    {
        k = r - LCE_FLY2;
        mon->invisible = FALSE;
        mon->x = 300 - k * 24;
        mon->y = 108;
        if (mon->oam.affineMode != ST_OAM_AFFINE_OFF)
            SetOamMatrixRotationScaling(mon->oam.matrixNum, -420, 420, 0);
        BlendPalettes(monBit, 10, eon);
    }
    else if (r >= LCE_STAY)
    {
        k = min(r - LCE_STAY, 16);
        mon->invisible = FALSE;
        mon->x = 120 + (16 - k) * 6;
        mon->y = 76 - (16 - k) * 3 + Sin((r * 6) & 0xFF, 3);
        LI_Affine(task->tGiSprite0, 256 + (16 - k) * 24, 0);
        if (k < 16)
            BlendPalettes(monBit, 16 - k, RGB_WHITE);
    }
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
// Cresselia (Fullmoon Island; Jordi: "een maan"): het wordt nacht, de maan rijst op (BG0, optellend: kraters, een
// stralenkrans) en wast van sikkel naar vol, maanmist drijft laag over het beeld. Cresselia staat als silhouet voor de
// maan en licht op met de volle maan; op de klokslag een zachte lavendelwitte flits.
#define LCM2_MIST      8
#define LCM2_TAG_MIST  0x5B29
#define LCM2_X         120
#define LCM2_Y         62
#define LCM2_R         42
#define LCM2_MON       LC_BEAT(5)
#define LCM2_FULL      LC_BEAT(6)

static u32 LCM2_Pixel(s32 x, s32 y)
{
    s32 dx = x - LCM2_X, dy = y - LCM2_Y, d2 = dx * dx + dy * dy, band;
    u32 h;
    if (d2 >= (LCM2_R + 6) * (LCM2_R + 6))
        return 0;
    if (d2 >= LCM2_R * LCM2_R)
        return (((x + y) & 1) || d2 < (LCM2_R + 3) * (LCM2_R + 3)) ? 15 : 0;
    // banden langs de breedte van de rij: de terminator is gebogen (een sikkel)
    h = sLC->rowv[y] + 1;
    band = 1 + (dx + (s32)h) * 7 / (2 * (s32)h + 1);
    band = band < 1 ? 1 : (band > 7 ? 7 : band);
    if ((x - 104) * (x - 104) + (y - 48) * (y - 48) < 70 || (x - 134) * (x - 134) + (y - 76) * (y - 76) < 50
     || (x - 112) * (x - 112) + (y - 80) * (y - 80) < 26 || (x - 140) * (x - 140) + (y - 52) * (y - 52) < 20
     || (x - 96) * (x - 96) + (y - 70) * (y - 70) < 14)
        return 7 + band;   // krater: donkerder
    return band;
}

static u32 LCM2_Cell(s32 cx, s32 cy)
{
    s32 x = cx * 8 + 4 - LCM2_X, y = cy * 8 + 4 - LCM2_Y, r = LCM2_R + 12;
    return (x * x + y * y < r * r) ? (13 << 12) : LC_EMPTY;
}

static void RTCresselia_Init(struct Task *task)
{
    u32 i;
    LC_Begin(task, 0xC4E5);
    if (sLC == NULL)
        return;
    for (i = 0; i < DISPLAY_HEIGHT; i++)
    {
        s32 dy = i - LCM2_Y, w = 0;
        while ((w + 1) * (w + 1) + dy * dy < LCM2_R * LCM2_R)
            w++;
        sLC->rowv[i] = w;
    }
    sLC->matSet = AllocOamMatrix();
    if (sLC->matSet != 0xFF)
        SetOamMatrixRotationScaling(sLC->matSet, 640, 360, 0);
    for (i = 0; i < LCM2_MIST; i++)
    {
        LI_Make(i, gBattleAnimSpriteGfx_Smoke, 0x100, LC_Tint(gBattleAnimSpritePal_Smoke, RGB(6, 5, 14), RGB(22, 20, 30)),
                LCM2_TAG_MIST, &sGI_Oam16, 0, 0, 1);
        LI_S(i)->oam.objMode = ST_OAM_OBJ_BLEND;
        LI_Frame(i, LCM2_TAG_MIST, i & 1, 4);
        LC_UseMatrix(LI_S(i), sLC->matSet, SPRITE_SHAPE(16x16), SPRITE_SIZE(16x16));
    }
    task->tGiSprite0 = LC_MonPic(SPECIES_CRESSELIA, LCM2_X, LCM2_Y + 6, 0);
    LC_Additive(15);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(15, 16));
}

static bool8 RTCresselia_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k, term;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCM2_TAG_MIST);
    GI_ResetPals(keep);
    if (LC_Gen(task, t, LCM2_Pixel, LCM2_Cell) && r == 0)
        LC_ShowMap();
    LC_DimWorld(r, keep, 13, RGB(1, 2, 8));

    // de maan wast: banden rechts van de terminator zijn licht, links nog donker
    term = 8 - min(8, max(0, (t - LC_BEAT(3)) * 8 / (LCM2_FULL - LC_BEAT(3))));
    cols[0] = 0;
    for (i = 1; i <= 7; i++)
    {
        u16 c = (i >= term) ? RGB(26, 26, 20) : RGB(3, 3, 7);
        if (i == term)
            c = RGB(31, 31, 26); // de sikkelrand glanst
        cols[i] = c;
        cols[7 + i] = Tapu_Blend(c, 0, 5);
    }
    cols[15] = Tapu_Blend(RGB(10, 9, 18), RGB(18, 16, 28), (6 - min(6, t % 20)) * 2);
    LC_SetBgPal(0, cols);
    k = min(16, r * 16 / 44);
    BlendPalettes(GI_BG_PALS, 12 - min(12, k), RGB_BLACK);
    SetGpuReg(REG_OFFSET_BG0VOFS, (-(96 - k * 6)) & 0x1FF);   // de maan rijst op

    // maanmist laag over het beeld
    for (i = 0; i < LCM2_MIST; i++)
    {
        s = LI_S(i);
        s->invisible = FALSE;
        s->x = ((i * 40 + r * (1 + (i & 1))) % 320) - 40;
        s->y = 134 + (i % 3) * 10 + Sin((r * 4 + i * 40) & 0xFF, 3);
    }

    // Cresselia: silhouet voor de maan, licht op met de volle maan
    k = t - LCM2_MON;
    mon->invisible = k < 0;
    mon->y2 = Sin((t * 4) & 0xFF, 3);
    if (k >= 0)
    {
        if (t < LCM2_FULL)
            BlendPalettes(monBit, 16, RGB(2, 2, 6));
        else
            BlendPalettes(monBit, max(0, 16 - (t - LCM2_FULL)), RGB(2, 2, 6));
    }
    if (LC_Cross(task, t, LCM2_FULL))
        PlayCry_Normal(SPECIES_CRESSELIA, 0);
    if (LC_Cross(task, t, LC_BEAT(3)))
        PlaySE(SE_M_MOONLIGHT);
    task->tLcLast = t;
    return LC_Out(t, LC_HIT, 6, PALETTES_ALL, RGB(28, 25, 31));
}

static void RTCresselia_Finish(struct Task *task)
{
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    LC_FinishCommon(task);
    GI_FreeTag(LCM2_TAG_MIST);
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
// prisma (Necrozma zelf, als silhouet) dat al het licht en de kleur naar zich toe zuigt: de wereld wordt donker en
// prismastralen in alle kleuren van het spectrum schieten van de randen naar binnen en verdwijnen in het prisma, tot
// het beeld zwart is.
#define LCN_PRISM      LC_BEAT(3)
#define LCN_RAYS       LC_BEAT(4)
#define LCN_RAY_N      9

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
    task->tGiSprite0 = LI_MonPicAffine(sp, 120, 80);
    LC_Additive(16);
}

static bool8 RTNecrozma_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, j, k, edge;
    u32 keep, monBit;
    struct Sprite *mon = GI_Sprite(task->tGiSprite0);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
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
        LI_Affine(task->tGiSprite0, 160 + min(k, 60) * 2 + (6 - min(6, t % 20)) * 4, (u16)(k * 64));
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
// Galar-Zapdos (Route 111, rent rondjes; vechttype): stofstrepen razen voorbij, Galar-Zapdos sprint het beeld in (een
// hupje op elke achtste), en trapt: de klauw (de voet uit de Mega Kick-art) komt op je af, een inslag (de ster uit de
// klap-art) en scheuren vanuit het midden.
#define LCGZ_TAG_FOOT  0x5B2A
#define LCGZ_TAG_HIT   0x5B2B
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
    LC_Begin(task, 0x6A2D);
    if (sLC == NULL)
        return;
    LC_StrokesInit(sLCGZ_Strokes, ARRAY_COUNT(sLCGZ_Strokes));
    LI_Make(0, gBattleAnimSpriteGfx_HandsAndFeet, 0x800, LC_Tint(gBattleAnimSpritePal_HandsAndFeet, RGB(10, 4, 2), RGB(31, 24, 12)),
            LCGZ_TAG_FOOT, &sGI_Oam32Affine, 120, 80, 0);
    LI_Frame(0, LCGZ_TAG_FOOT, 2, 16);
    LI_Make(1, gBattleAnimSpriteGfx_Impact, 0x200, gBattleAnimSpritePal_Impact, LCGZ_TAG_HIT, &sGI_Oam32Affine, 120, 80, 1);
    task->tGiSprite0 = LI_MonPicAffine(SPECIES_ZAPDOS_GALAR, -40, 84);
    GI_Sprite(task->tGiSprite0)->subpriority = 5;
    LC_Additive(13);
}

static bool8 RTGalarZapdos_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *mon = GI_Sprite(task->tGiSprite0), *foot = LI_S(0), *hit = LI_S(1);
    u16 cols[16];

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCGZ_TAG_FOOT) | GI_SpritePalBit(LCGZ_TAG_HIT);
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

    // sprinten, met een hupje op elke achtste
    k = t - LCGZ_RUN;
    mon->invisible = k < 0;
    if (k >= 0)
    {
        s32 e = (t * 1000) % 10181;
        mon->x = min(120, -40 + k * 3);
        mon->y = 84 - (e < 5000 ? Sin(e * 128 / 5000, 6) : 0);
        LI_Affine(task->tGiSprite0, t < LCGZ_KICK ? 256 : 256 + min(t - LCGZ_KICK, 20) * 6, 0);
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
// en Galar-Moltres komt eruit op; op de klokslag slokt de aura het beeld op (Fiery Wrath).
#define LCGM_FLAMES    8
#define LCGM_AURA      LCGM_FLAMES   // drie ringen
#define LCGM_RINGS     3
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
    task->tGiSprite0 = LC_MonPic(SPECIES_MOLTRES_GALAR, 120, 74, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(10, 10));
}

static bool8 RTGalarMoltres_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), r, i, k;
    u32 keep, monBit;
    struct Sprite *s, *mon = GI_Sprite(task->tGiSprite0);

    if (sLC == NULL)
        return TRUE;
    r = LC_R(t);
    monBit = LI2_MonBit(task->tGiSprite0);
    keep = monBit | GI_SpritePalBit(LCGM_TAG_FIRE) | GI_SpritePalBit(LCGM_TAG_AURA);
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

    k = t - LCGM_MON;
    mon->invisible = k < 0;
    mon->y2 = Sin((t * 5) & 0xFF, 2);
    if (k >= 0)
        BlendPalettes(monBit, max(0, 16 - k / 2), RGB(2, 0, 4));
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
