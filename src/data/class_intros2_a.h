// Project Grounded: trainerklasse-intro's v2, set a (Jordi): Fisherman, Guitarist, Ninja Boy, Collector.
// Ingevoegd in src/data/class_intros.h vlak voor de dispatch-tabel; gebruikt de TI_*-runner daar.
// Alles is code: vormen op BG0 (CI2A_Fill/CI2A_HLine), kleine sprites uit een buffer, gevechtsanimatie-art, mon-iconen
// (Magikarp, de kaarten) en trainerfoto's die al in de ROM staan.
//
//   Fisherman    lijn uit; een laars, een visgraat, Magikarp (drie keer "wah wah"); de hengel buigt dubbel, is weg, en
//                iets enorms met één gloeiend oog komt uit de diepte
//   Guitarist    een rock-game-fretboard in perspectief; gekleurde noten schuiven op de tel naar de slaglijn (E5, A5,
//                D5, G5), dan een power chord over alle vijf de snaren
//   Ninja Boy    drie handtekens (RAM! SNAKE! TIGER!) met speedlines, schaduwklonen (1, 3, 7), een blauwe wervelbol
//                in een bladerwervel terwijl de wereld meedraait, poef: BELIEVE IT.
//   Collector    kaarten (met mon-icoon, holo) leggen zich op een rij, LOSERS., de bril glimt (shiny), en achter hem
//                rijst een gigantische Wailord-knuffel op (MINT)

#include "pokemon_icon.h"

#define CI2A_TAG_SHEET 0x7A41
#define CI2A_TAG_TXT1  0x7A42
#define CI2A_TAG_TXT2  0x7A43
#define CI2A_TAG_TXT3  0x7A44
#define CI2A_TAG_TXT4  0x7A45

// ---------------------------------------------------------------------------------------------------------------------
// gedeelde hulpjes

// een rij [x0, x1) op BG0 in kleur c (palet 15), per tegel in één schrijfactie
static void CI2A_HLine(s32 y, s32 x0, s32 x1, u32 c)
{
    s32 tx;
    if ((u32)y >= DISPLAY_HEIGHT)
        return;
    x0 = max(x0, 0);
    x1 = min(x1, DISPLAY_WIDTH);
    for (tx = x0 >> 3; tx * 8 < x1; tx++)
    {
        s32 a = max(x0, tx * 8) - tx * 8, b = min(x1, tx * 8 + 8) - tx * 8;
        u32 mask = (b >= 8 ? 0xFFFFFFFF : (1u << (b * 4)) - 1) & ~((1u << (a * 4)) - 1), idx, *row;
        TI_Plot(tx * 8 + a, y, c);   // zorgt voor een eigen tegel
        idx = sTI->bg0map[(y >> 3) * 32 + tx] & 0x3FF;
        if (idx < sTI->reserved)
            continue;
        row = (u32 *)&sTI->bg0tiles[idx * 16 + (y & 7) * 2];
        *row = (*row & ~mask) | ((c * 0x11111111) & mask);
    }
}

static u32 CI2A_Solid(u32 c)
{
    u32 n = TI_NewTile();
    TI_SolidTile(n, c);
    return n;
}

// een vorm vullen: pixelrij y0+i loopt van xa[i] tot xb[i]; tegels die er helemaal in vallen krijgen de effen tegel
static void CI2A_Fill(const s16 *xa, const s16 *xb, s32 y0, s32 n, u32 c, u32 solid)
{
    s32 i, ty, tx;
    for (ty = max(0, (y0 + 7) >> 3); ty < 20 && ty * 8 + 8 <= y0 + n; ty++)
    {
        s32 lo = -999, hi = 999, k;
        for (k = 0; k < 8; k++)
        {
            lo = max(lo, xa[ty * 8 + k - y0]);
            hi = min(hi, xb[ty * 8 + k - y0]);
        }
        for (tx = max(0, (lo + 7) >> 3); tx < 30 && tx * 8 + 8 <= hi; tx++)
            TI_Put(tx, ty, solid | (15 << 12));
    }
    for (i = 0; i < n; i++)
    {
        s32 y = y0 + i, x = max(0, xa[i]), e = min(DISPLAY_WIDTH, xb[i]);
        if ((u32)y >= DISPLAY_HEIGHT)
            continue;
        while (x < e)
        {
            s32 nx = min(e, (x | 7) + 1);
            if ((sTI->bg0map[(y >> 3) * 32 + (x >> 3)] & 0x3FF) != solid)
                CI2A_HLine(y, x, nx, c);
            x = nx;
        }
    }
}

// spannen van een ellips voor de rijen y0..y0+n-1
static void CI2A_Ellipse(s16 *xa, s16 *xb, s32 y0, s32 n, s32 cx, s32 cy, s32 rx, s32 ry)
{
    s32 i;
    for (i = 0; i < n; i++)
    {
        s32 dy = y0 + i - cy, w;
        xa[i] = xb[i] = 0;
        if (dy * dy > ry * ry)
            continue;
        w = rx * Sqrt(ry * ry - dy * dy) / ry;
        xa[i] = cx - w;
        xb[i] = cx + w + 1;
    }
}

static void CI2A_FillEllipse(s32 cx, s32 cy, s32 rx, s32 ry, u32 c, u32 solid)
{
    s16 xa[DISPLAY_HEIGHT], xb[DISPLAY_HEIGHT];
    CI2A_Ellipse(xa, xb, 0, DISPLAY_HEIGHT, cx, cy, rx, ry);
    CI2A_Fill(xa, xb, 0, DISPLAY_HEIGHT, c, solid);
}

static void CI2A_Ring(s32 cx, s32 cy, s32 rx, s32 ry, s32 r, u32 c)
{
    s32 a;
    for (a = 0; a < 256; a += 2)
        TI_Stamp(cx + Cos(a, rx), cy + Sin(a, ry), r, c);
}

// kleine sprite-art als tekens ('.' = leeg, '1'-'7' = kleur), 16 breed
static void CI2A_Art(u8 *buf, u32 frame, u32 row0, const char *art, u32 rows)
{
    u32 x, y;
    for (y = 0; y < rows; y++)
        for (x = 0; x < 16; x++)
            if (art[y * 16 + x] != '.')
                TI_BufPixel(buf, 2, x, frame * 16 + row0 + y, art[y * 16 + x] - '0');
}

static void CI2A_BufRect(u8 *buf, u32 wTiles, s32 x0, s32 y0, s32 x1, s32 y1, u32 c)
{
    s32 x, y;
    for (y = y0; y < y1; y++)
        for (x = x0; x < x1; x++)
            TI_BufPixel(buf, wTiles, x, y, c);
}

// mon-icoon (Magikarp, kaarten): TI_Free ruimt die niet goed op (eigen tegels), dus zelf weggooien met CI2A_FreeIcon
static u8 CI2A_Icon(u16 species, s16 x, s16 y)
{
    u8 id;
    LoadMonIconPalette(species);
    id = CreateMonIcon(species, SpriteCallbackDummy, x, y, 0, 0);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    TI_Show(id, FALSE);
    return TI_Track(id, TIK_MON);
}

static void CI2A_FreeIcon(u8 id)
{
    if (id < MAX_SPRITES && gSprites[id].inUse)
    {
        FreeSpritePaletteByTag(GetSpritePaletteTagByPaletteNum(gSprites[id].oam.paletteNum));
        FreeAndDestroyMonIconSprite(&gSprites[id]);
    }
}

// BG0 komt van onderen omhoog (venster 0 laat BG0 alleen onder de bovenrand zien)
static void CI2A_Rise(s32 off)
{
    sTI->bg0y = -off;
    sTI->win0h = off >= DISPLAY_HEIGHT ? 0 : WIN_RANGE(0, DISPLAY_WIDTH);
    sTI->win0v = WIN_RANGE(max(0, min(off, DISPLAY_HEIGHT - 1)), DISPLAY_HEIGHT);
}

static const u16 sCI2A_TextPal[4] = {0, RGB(31, 31, 31), RGB(20, 2, 2), 0};

// ---------------------------------------------------------------------------------------------------------------------
// Fisherman: kansloze vissersactie

// 1 lijn, 2 hengel, 3 rood, 4 silhouet, 5 oog, 6 tekst, 7 tekstschaduw, 8 tanden
static const u16 sCI2A_FishPal[9] = {0, RGB(30, 30, 28), RGB(27, 19, 9), RGB(31, 6, 4), RGB(1, 2, 5), RGB(31, 29, 6), RGB(31, 31, 31), RGB(3, 3, 5), RGB(26, 26, 22)};
// 1 donker, 2 bruin, 3 lichtbruin, 4 bot, 5 rood, 6 wit
static const u16 sCI2A_JunkPal[7] = {0, RGB(4, 3, 2), RGB(14, 8, 3), RGB(22, 14, 7), RGB(29, 29, 25), RGB(31, 5, 4), RGB(31, 31, 31)};

static const char sCI2A_Boot[] =
    "....111111......"
    "....123321......"
    "....122321......"
    "....122221......"
    "....122221......"
    "....122221......"
    "...1222221......"
    "...12222221111.."
    "..122222222231.."
    "..12222202222231"
    "..12222222222221"
    "..11111111111111"
    "...1.1...1.1....";
static const char sCI2A_Bone[] =
    "4.....4.4.4....."
    "44....4.4.4..44."
    ".44...4.4.4.4444"
    "..4444444444414."
    ".44...4.4.4.4444"
    "44....4.4.4..44."
    "4.....4.4.4.....";
static const char sCI2A_Bobber[] =
    "......1111......"
    ".....155551....."
    ".....155551....."
    ".....166661....."
    "......1661......"
    ".......11.......";

static const u8 *const sCI2A_Catch[4] = {
    COMPOUND_STRING("1. a boot"),
    COMPOUND_STRING("2. a fishbone"),
    COMPOUND_STRING("3. Magikarp (again)"),
    COMPOUND_STRING("4. oh no."),
};

#define FI_BOBBER  0
#define FI_JUNK    1   // 1-3: laars, visgraat, Magikarp
#define FI_BANG    4
#define FI_BUBBLE  5
#define FI_ROD     6   // getekende buiging (-1 = niets)
#define FI_LBX     7   // getekende lijn: dobber x, y, doorhang
#define FI_LBY     8
#define FI_LSAG    9
#define FI_DEEP    10  // 1 = de hengel is weg, het silhouet staat op BG0

// de hengel: kwadratische kromme van onder links naar de top; bend 0-256 = recht tot dubbelgebogen
static void CI2A_RodTip(s32 bend, s32 *x, s32 *y)
{
    *x = 46 + (72 * bend >> 8);
    *y = 100 + (40 * bend >> 8);
}

static void CI2A_DrawRod(s32 bend, u32 c)
{
    s32 i, tx, ty, cx = 20 + (6 * bend >> 8), cy = 136 - (110 * bend >> 8);
    CI2A_RodTip(bend, &tx, &ty);
    for (i = 0; i <= 64; i++)
    {
        s32 u = i * 4, w = 256 - u;
        s32 x = (w * w * -6 + 2 * u * w * cx + u * u * tx) >> 16;
        s32 y = (w * w * 172 + 2 * u * w * cy + u * u * ty) >> 16;
        TI_Stamp(x, y, i < 54 ? 1 : 0, c);
    }
}

static void CI2A_DrawLine(s32 bend, s32 bx, s32 by, s32 sag, u32 c)
{
    s32 i, tx, ty;
    CI2A_RodTip(bend, &tx, &ty);
    for (i = 0; i <= 64; i++)
        TI_Plot(tx + (bx - tx) * i / 64, ty + (by - ty) * i / 64 + Sin(i * 2, sag), c);
}

static void CI2A_FishSet(s32 bend, s32 bx, s32 by, s32 sag)
{
    s32 *v = sTI->v;
    if (v[FI_DEEP] || (bend == v[FI_ROD] && bx == v[FI_LBX] && by == v[FI_LBY] && sag == v[FI_LSAG]))
        return;
    if (v[FI_ROD] >= 0)
    {
        CI2A_DrawLine(v[FI_ROD], v[FI_LBX], v[FI_LBY], v[FI_LSAG], 0);
        if (bend != v[FI_ROD])
            CI2A_DrawRod(v[FI_ROD], 0);
    }
    if (bend != v[FI_ROD])
        CI2A_DrawRod(bend, 2);
    CI2A_DrawLine(bend, bx, by, sag, 1);
    v[FI_ROD] = bend;
    v[FI_LBX] = bx;
    v[FI_LBY] = by;
    v[FI_LSAG] = sag;
}

// het ding uit de diepte: lijf, gevorkte staart, rugvin, één gloeiend oog, tanden
static void CI2A_DrawDeep(void)
{
    s16 xa[DISPLAY_HEIGHT], xb[DISPLAY_HEIGHT];
    u32 solid = CI2A_Solid(4), y, i;
    CI2A_FillEllipse(118, 112, 104, 52, 4, solid);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 d = abs((s32)y - 112);
        xa[y] = xb[y] = 0;
        if (y >= 60)   // staart: een V die naar rechts openklapt
        {
            xa[y] = 206 - d / 3;
            xb[y] = 214 + d;
        }
        if (y >= 36 && y < 70 && xb[y] == 0)   // rugvin
        {
            xa[y] = 112 - (y - 36) / 2;
            xb[y] = 120 + (y - 36);
        }
    }
    CI2A_Fill(xa, xb, 0, DISPLAY_HEIGHT, 4, solid);
    CI2A_FillEllipse(60, 96, 11, 7, 5, 0);
    CI2A_FillEllipse(61, 96, 2, 6, 4, 0);
    for (i = 0; i < 9; i++)   // tanden: driehoekjes langs de bek
    {
        TI_Line(14 + i * 9, 120, 18 + i * 9, 130, 0, 256, 0, 6);
        TI_Line(18 + i * 9, 130, 22 + i * 9, 120, 0, 256, 0, 6);
    }
}

static void CIFish2_Init(void)
{
    u8 *buf = AllocZeroed(3 * 4 * 32);
    u32 i;
    TI_SetPal(15, sCI2A_FishPal, ARRAY_COUNT(sCI2A_FishPal));
    if (buf != NULL)
    {
        CI2A_Art(buf, 0, 1, sCI2A_Boot, sizeof(sCI2A_Boot) / 16);
        CI2A_Art(buf, 1, 4, sCI2A_Bone, sizeof(sCI2A_Bone) / 16);
        CI2A_Art(buf, 2, 5, sCI2A_Bobber, sizeof(sCI2A_Bobber) / 16);
        sTI->v[FI_BOBBER] = TI_BufSprite(buf, 3 * 4 * 32, CI2A_TAG_SHEET, sCI2A_JunkPal, &gOamData_AffineOff_ObjNormal_16x16, -20, -20);
        for (i = 0; i < 2; i++)
        {
            sTI->v[FI_JUNK + i] = TI_BufSprite(buf, 3 * 4 * 32, CI2A_TAG_SHEET, sCI2A_JunkPal, &gOamData_AffineDouble_ObjNormal_16x16, -20, -20);
            gSprites[sTI->v[FI_JUNK + i]].oam.tileNum += i * 4;
            TI_Show(sTI->v[FI_JUNK + i], FALSE);
        }
        gSprites[sTI->v[FI_BOBBER]].oam.tileNum += 8;
        Free(buf);
    }
    sTI->v[FI_JUNK + 2] = CI2A_Icon(SPECIES_MAGIKARP, -40, -40);
    sTI->v[FI_BANG] = TI_Bang(152, 64);
    sTI->v[FI_BUBBLE] = TI_Anim(ANIM_TAG_SMALL_BUBBLES, &gOamData_AffineOff_ObjNormal_16x16, 0, 200, 0);
    TI_Show(sTI->v[FI_BUBBLE], FALSE);
    sTI->v[FI_ROD] = -1;
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0);
    CI2A_Rise(0);
    PlaySE(SE_M_FLY);
}

static bool32 CIFish2_Update(s32 t)
{
    s32 *v = sTI->v;
    s32 h2 = TI_Beat2(2), h9 = TI_Beat2(9), h10 = TI_Beat2(11), h12 = TI_Beat2(13), end = TI_Beat2(14) + 4;
    s32 k, bx = 152, by = 100, sag = 7, bend = 0, shake = 0;

    if (t < h2)
    {
        // uitgooien: de dobber vliegt in een boog, de lijn strak erachteraan
        s32 r = TI_Ramp(t, 0, h2);
        bx = 46 + (106 * r >> 8);
        by = 100 - Sin(r >> 1, 56);
        sag = 0;
    }
    if (TI_AT(h2))
    {
        PlaySE(SE_M_BUBBLE);
        TI_Part(v[FI_BUBBLE], 152, 96, 0, -10, 1, 16);
    }
    if (t >= h2)
        by += Sin((t * 12) & 0xFF, 2);
    // drie vangsten, telkens op de halve tel: dobber duikt, iets vliegt eruit, en valt
    for (k = 0; k < 3; k++)
    {
        s32 hc = TI_Beat2(3 + 2 * k);
        u8 id = v[FI_JUNK + k];
        if (t >= hc - 6 && t < hc)
        {
            by = 104;
            sag = 0;
        }
        if (TI_AT(hc))
        {
            struct TIPart *p = TI_Part(id, 152, 96, -24, -96, 7, 0);
            (void)p;
            PlaySE(SE_BALL_BOUNCE_1);
            TI_TextBg(sCI2A_Catch[k], 1, 1 + 2 * k, 14, 2, 0, 0, 0, 6, 7, FONT_NORMAL, 15);
        }
        if (TI_AT(hc + 10))
            PlaySE(SE_FAILURE);
        if (t >= hc && id < MAX_SPRITES)
        {
            if (k < 2)
                TI_Scale(id, 256, 256, (t - hc) * (k ? -2400 : 1800));
            else if (((t - hc) & 3) == 0)
                gSprites[id].oam.matrixNum ^= ST_OAM_HFLIP;   // Magikarp spartelt
        }
    }
    // de grote beet: "!", de hengel buigt dubbel, het beeld schudt
    if (TI_AT(h9))
    {
        PlaySE(SE_PIN);
        TI_Show(v[FI_BANG], TRUE);
        TI_Scale(v[FI_BANG], 128, 128, 0);
        TI_TextBg(sCI2A_Catch[3], 1, 7, 14, 2, 0, 0, 0, 6, 7, FONT_NORMAL, 15);
    }
    if (t >= h9)
    {
        TI_Show(v[FI_BOBBER], FALSE);
        bend = TI_Ramp(t, h9, h9 + 8) & ~127;   // in twee stappen: elke nieuwe stand kost een hertekening
        bx = 154;
        by = 112;
        sag = 0;
        shake = t < h12 ? 2 + (t - h9) / 6 : 0;
    }
    if (!v[FI_DEEP])
        CI2A_FishSet(bend, bx, by, sag);
    TI_Pos(v[FI_BOBBER], bx, by - 4);
    // de hengel is weg; iets enorms komt omhoog
    if (TI_AT(h10))
    {
        PlaySE(SE_M_STRENGTH);
        TI_Show(v[FI_BANG], FALSE);
        TI_FillMap(0);
        sTI->nextTile = sTI->reserved = 1;
        v[FI_DEEP] = 1;
        CI2A_Rise(DISPLAY_HEIGHT);   // tekenen duurt langer dan een beeld: eerst verbergen
        CI2A_DrawDeep();
    }
    TI_Shake(min(shake, 6));
    if (TI_AT(h10))
        for (k = 0; k < 3; k++)
            TI_Show(v[FI_JUNK + k], FALSE);
    if (t >= h10)
    {
        s32 r = TI_Ramp(t, h10, h12);
        CI2A_Rise(160 - (r * (512 - r) * 160 >> 16));
        TI_Tint(TI_World(), r * 13 >> 8, RGB(1, 3, 8));
    }
    else
    {
        sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
        sTI->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);
    }
    // het oog gaat aan
    if (TI_AT(h12))
        PlaySE(SE_M_LEER);
    if (t >= h12)
        gPlttBufferFaded[15 * 16 + 5] = ((t - h12) & 4) ? RGB(31, 31, 31) : RGB(31, 29, 6);
    TI_Flash(t, h12, 8, 10, PALETTES_ALL, RGB(31, 31, 31));
    if (t >= end)
        CI2A_FreeIcon(v[FI_JUNK + 2]);
    return t >= end;
}

static const struct TIntro sCI_Fish2 = {CIFish2_Init, CIFish2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Guitarist: rock-game-fretboard met akkoorden op de tel

// 1-5 snaarkleuren, 6 wit, 7 snaargrijs, 8-13 banden (fretten), 14 donker
static const u16 sCI2A_GtPal[15] = {
    0, RGB(4, 28, 6), RGB(31, 4, 4), RGB(31, 28, 2), RGB(6, 12, 31), RGB(31, 16, 2), RGB(31, 31, 31), RGB(13, 12, 18),
    RGB(3, 2, 6), RGB(3, 2, 6), RGB(3, 2, 6), RGB(3, 2, 6), RGB(3, 2, 6), RGB(3, 2, 6), RGB(2, 1, 3),
};

#define GT_STRIKE 132
#define GT_CHORDS 5
#define GT_SPARKS 6
#define GT_NOTES  13   // 2+2+2+2+5
static const u16 sCI2A_StageCols[4] = {RGB(31, 4, 22), RGB(4, 24, 31), RGB(31, 26, 4), RGB(10, 31, 8)};
static const u8 sCI2A_ChordHalf[GT_CHORDS] = {2, 4, 6, 7, 8};
static const u8 sCI2A_ChordLanes[GT_CHORDS] = {0x03, 0x06, 0x0C, 0x18, 0x1F};
static const u8 *const sCI2A_ChordName[GT_CHORDS] = {
    COMPOUND_STRING("E5"), COMPOUND_STRING("A5"), COMPOUND_STRING("D5"), COMPOUND_STRING("G5"), COMPOUND_STRING("POWER\nCHORD"),
};

static s32 CI2A_GtHalf(s32 y)
{
    return 26 + y * 74 / 160;
}

// x van het midden van snaar 'lane' op hoogte y
static s32 CI2A_GtLaneX(s32 lane, s32 y)
{
    s32 hw = CI2A_GtHalf(y);
    return 120 - hw + (2 * hw * (2 * lane + 1)) / 10;
}

static void CIGuitar2_Init(void)
{
    u8 *buf = AllocZeroed(5 * 4 * 32);
    s32 y, k, x;
    TI_SetPal(15, sCI2A_GtPal, ARRAY_COUNT(sCI2A_GtPal));
    // de baan: per rij een band (diepte 24 banden tot de slaglijn, de fret is één van de zes kleuren)
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 hw = CI2A_GtHalf(y), p = Sqrt((y << 16) / GT_STRIKE);
        CI2A_HLine(y, 120 - hw, 120 + hw, 8 + ((p * 3 / 32) % 6));
        for (k = 0; k <= 5; k++)
        {
            x = 120 - hw + 2 * hw * k / 5;
            TI_Plot(x, y, k == 0 || k == 5 ? 6 : 7);
            if (k == 0 || k == 5)
                TI_Plot(x + (k ? -1 : 1), y, 6);
        }
    }
    CI2A_HLine(GT_STRIKE - 1, 120 - CI2A_GtHalf(GT_STRIKE), 120 + CI2A_GtHalf(GT_STRIKE), 6);
    for (k = 0; k < 5; k++)
        CI2A_Ring(CI2A_GtLaneX(k, GT_STRIKE), GT_STRIKE, 9, 5, 1, k + 1);
    // noten: vijf gekleurde gems (16x16, ellips met rand en glimlicht)
    if (buf != NULL)
    {
        for (k = 0; k < 5; k++)
            for (y = 0; y < 16; y++)
                for (x = 0; x < 16; x++)
                {
                    s32 dx = 2 * x - 15, dy = 2 * y - 15, e = dx * dx * 81 + dy * dy * 196;
                    if (e > 196 * 81)
                        continue;
                    TI_BufPixel(buf, 2, x, k * 16 + y, e > 196 * 81 * 6 / 10 ? 14 : (dy < -4 && dx < 0 && dx > -9) ? 6 : k + 1);
                }
        for (k = 0; k < GT_NOTES; k++)
        {
            sTI->v[k] = TI_BufSprite(buf, 5 * 4 * 32, CI2A_TAG_SHEET, sCI2A_GtPal, &gOamData_AffineDouble_ObjNormal_16x16, -30, -30);
            TI_Show(sTI->v[k], FALSE);
        }
        Free(buf);
    }
    for (k = 0; k < GT_SPARKS; k++)
    {
        sTI->extra[k] = TI_Anim(ANIM_TAG_MUSIC_NOTES, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, (k % 6) * 4);
        TI_Show(sTI->extra[k], FALSE);
    }
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0);
    sTI->win0h = 0;
    PlaySE(SE_M_ENCORE);
}

static bool32 CIGuitar2_Update(s32 t)
{
    s32 half = TI_Beat2(1) - TI_Beat2(0), beat = TI_Beat(1) - TI_Beat(0), end = TI_Beat2(11);
    s32 c, l, n = 0, since = 99, last = -1, rev, ph, sp = 0;
    // de baan rolt van boven het beeld in
    rev = TI_Ramp(t, 0, max(1, half)) * DISPLAY_HEIGHT >> 8;
    sTI->win0h = rev > 0 ? WIN_RANGE(0, DISPLAY_WIDTH) : 0;
    sTI->win0v = WIN_RANGE(0, max(1, rev));
    // de fretten schuiven op het tempo van de noten (24 banden per tel)
    ph = t * 24 / max(1, beat);
    gPlttBufferFaded[15 * 16 + 8 + (ph % 6)] = RGB(12, 10, 20);
    for (c = 0; c < GT_CHORDS; c++)
    {
        s32 hit = TI_Beat2(sCI2A_ChordHalf[c]);
        if (t >= hit)
        {
            since = t - hit;
            last = c;
        }
        for (l = 0; l < 5; l++)
        {
            u8 id;
            s32 p, y;
            if (!(sCI2A_ChordLanes[c] & (1 << l)))
                continue;
            id = sTI->v[n++];
            if (id >= MAX_SPRITES)
                continue;
            if (t < hit - beat || t >= hit)
            {
                TI_Show(id, FALSE);
                continue;
            }
            p = TI_Ramp(t, hit - beat, hit);
            y = GT_STRIKE * p * p >> 16;
            TI_Show(id, TRUE);
            gSprites[id].oam.tileNum = GetSpriteTileStartByTag(CI2A_TAG_SHEET) + l * 4;
            TI_Pos(id, CI2A_GtLaneX(l, y), y);
            TI_Scale(id, 65536 / (154 + p), 65536 / (154 + p), 0);
        }
        if (TI_AT(hit))
        {
            PlaySE(c == GT_CHORDS - 1 ? SE_M_HYPER_BEAM : SE_M_BELLY_DRUM);
            TI_TextBg(sCI2A_ChordName[c], 0, 6, 7, 4, -1, 0, 0, 6, 14, FONT_NORMAL, 15);
            for (l = 0; l < 5; l++)
                if (sCI2A_ChordLanes[c] & (1 << l))
                    TI_Part(sTI->extra[(sp++ + c * 2) % GT_SPARKS], CI2A_GtLaneX(l, GT_STRIKE), GT_STRIKE - 8, (l - 2) * 8, -TI_RandRange(40, 56), 2, 30);
        }
    }
    // geraakte snaren lichten op
    if (last >= 0 && since < 8)
        for (l = 0; l < 5; l++)
            if (sCI2A_ChordLanes[last] & (1 << l))
                gPlttBufferFaded[15 * 16 + 1 + l] = RGB(31, 31, 31);
    // podium: donker, met een kleurpuls op elke slag
    TI_Tint(TI_World(), 9, RGB(1, 0, 3));
    if (last >= 0)
        TI_TintMore(TI_World(), since < 8 ? 8 - since : 0, sCI2A_StageCols[last & 3]);
    TI_WorldMove(last == GT_CHORDS - 1 && since < 16 ? Sin((since * 80) & 0xFF, 16 - since) : 0, 0);
    TI_Flash(t, TI_Beat2(8), 12, 16, PALETTES_ALL, RGB(31, 31, 31));
    return t >= end;
}

static const struct TIntro sCI_Guitar2 = {CIGuitar2_Init, CIGuitar2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Ninja Boy: handtekens, schaduwklonen, een wervelbol in een bladerwervel, poef

#define NB_TEXT   0   // 0-2: RAM! SNAKE! TIGER!
#define NB_CLONE  3   // 3-9: zeven ninja's
#define NB_ORB    10
#define NB_END    11
#define NB_LEAF   12  // 12-21
#define NB_LEAVES 10
#define NB_CLONES 7
static const s16 sCI2A_ClonePos[NB_CLONES][2] = {{120, 104}, {60, 108}, {180, 108}, {30, 74}, {90, 70}, {150, 70}, {210, 74}};
static const u8 sCI2A_CloneHalf[NB_CLONES] = {3, 4, 4, 5, 5, 5, 5};
static const u8 *const sCI2A_Seal[3] = {COMPOUND_STRING("RAM!"), COMPOUND_STRING("SNAKE!"), COMPOUND_STRING("TIGER!")};

static void CINinja2_Init(void)
{
    u32 i, pic = GetTrainerPicFromId(sTI->trainer);
    TI_SetCol(15, 1, RGB(31, 31, 31));
    TI_SetCol(15, 2, RGB(20, 20, 24));
    // speedlines naar het midden (getekend, zichtbaar via de blend)
    for (i = 0; i < 44; i++)
    {
        s32 a = (i * 256 / 44 + TI_RandRange(-2, 2)) & 0xFF, r0 = TI_RandRange(44, 80);
        TI_Line(120 + Cos(a, r0 * 3 / 2), 80 + Sin(a, r0), 120 + Cos(a, 200), 80 + Sin(a, 140), 0, 256, 0, (i & 1) + 1);
        if ((i & 3) == 0)
            TI_Line(121 + Cos(a, r0 * 3 / 2), 80 + Sin(a, r0), 121 + Cos(a, 200), 80 + Sin(a, 140), 0, 256, 0, 1);
    }
    TI_Blend(BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3, 0, 16);
    for (i = 0; i < 3; i++)
    {
        sTI->v[NB_TEXT + i] = TI_TextSprite(sCI2A_Seal[i], 8, 4, 8, CI2A_TAG_TXT1 + i, sCI2A_TextPal, &gOamData_AffineDouble_ObjNormal_64x32, 120, 72);
        TI_Show(sTI->v[NB_TEXT + i], FALSE);
    }
    // de ninja zelf + zes klonen op dezelfde tegels
    sTI->v[NB_CLONE] = TI_Trainer(pic, -64, -64, FALSE);
    for (i = 1; i < NB_CLONES; i++)
    {
        struct SpriteTemplate tmpl = {
            .tileTag = gTrainerSprites[pic].frontPic.tag, .paletteTag = gTrainerSprites[pic].palette.tag,
            .oam = &gOamData_AffineOff_ObjNormal_64x64, .anims = gDummySpriteAnimTable, .images = NULL,
            .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
        };
        u8 id = CreateSprite(&tmpl, -64, -64, i < 3 ? 2 : 4);
        sTI->v[NB_CLONE + i] = id < MAX_SPRITES ? TI_Track(id, TIK_SPRITE) : MAX_SPRITES;
    }
    for (i = 0; i < NB_CLONES; i++)
    {
        TI_Show(sTI->v[NB_CLONE + i], FALSE);
        sTI->extra[i] = TI_Anim(ANIM_TAG_GRAY_SMOKE, &gOamData_AffineDouble_ObjNormal_32x32, -40, -40, 0);
        TI_Show(sTI->extra[i], FALSE);
    }
    // de wervelbol: de Hypnosis-spiraal in blauw
    sTI->v[NB_ORB] = TI_Anim(ANIM_TAG_SPIRAL, &gOamData_AffineDouble_ObjNormal_64x64, 120, 100, 0);
    if (sTI->v[NB_ORB] < MAX_SPRITES)
    {
        u32 p = 16 + gSprites[sTI->v[NB_ORB]].oam.paletteNum;
        gSprites[sTI->v[NB_ORB]].subpriority = 0;
        TI_Show(sTI->v[NB_ORB], FALSE);
        for (i = 1; i < 16; i++)
            TI_SetCol(p, i, Tapu_Blend(RGB(2, 6, 22), RGB(24, 31, 31), TI_Lum(gPlttBufferFaded[p * 16 + i]) * 16 / 31));
    }
    for (i = 0; i < NB_LEAVES; i++)
    {
        sTI->v[NB_LEAF + i] = TI_Anim(ANIM_TAG_LEAF, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
        TI_Show(sTI->v[NB_LEAF + i], FALSE);
    }
    sTI->v[NB_END] = TI_TextSprite(COMPOUND_STRING("BELIEVE IT."), 8, 4, 8, CI2A_TAG_TXT4, sCI2A_TextPal, &gOamData_AffineDouble_ObjNormal_64x32, 120, 128);
    TI_Show(sTI->v[NB_END], FALSE);
    TI_Lines(TIF_WX);
}

// rookwolkje: 5 frames, groeit
static void CI2A_Puff(u8 id, s32 t, s32 t0, s32 x, s32 y)
{
    s32 dt = t - t0;
    if (id >= MAX_SPRITES)
        return;
    if (dt < 0 || dt >= 18)
    {
        if (dt >= 18)
            TI_Show(id, FALSE);
        return;
    }
    TI_Show(id, TRUE);
    TI_Pos(id, x, y);
    gSprites[id].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_GRAY_SMOKE) + min(4, dt / 4) * 16;
    TI_Scale(id, 256 - min(128, dt * 12), 256 - min(128, dt * 12), 0);
}

static bool32 CINinja2_Update(s32 t)
{
    s32 h6 = TI_Beat2(6), h10 = TI_Beat2(10), end = TI_Beat2(12) + 4, i, y, eva = 0, shake = 0, twist = 0;
    // handtekens op de halve tel
    for (i = 0; i < 3; i++)
    {
        s32 at = TI_Beat2(i), dt = t - at;
        u8 id = sTI->v[NB_TEXT + i];
        if (TI_AT(at))
            PlaySE(SE_M_DETECT);
        if (dt >= 0 && t < TI_Beat2(i + 1))
        {
            TI_Show(id, TRUE);
            TI_Scale(id, 128 + (dt < 3 ? (3 - dt) * 12 : 0), 128 + (dt < 3 ? (3 - dt) * 12 : 0), (u16)(Sin((dt * 40) & 0xFF, 6) << 8));
            eva = max(0, 16 - dt * 2);
            shake = max(0, 3 - dt / 3);
        }
        else
        {
            TI_Show(id, FALSE);
        }
    }
    // schaduwklonen: 1, 3, 7, elk met een rookwolkje
    for (i = 0; i < NB_CLONES; i++)
    {
        s32 at = TI_Beat2(sCI2A_CloneHalf[i]);
        u8 id = sTI->v[NB_CLONE + i];
        if (TI_AT(at) && (i == 0 || i == 1 || i == 3))
            PlaySE(SE_M_DOUBLE_TEAM);
        if (t >= at + 2 && t < h10 + 4 && id < MAX_SPRITES)
        {
            TI_Show(id, TRUE);
            TI_Pos(id, sCI2A_ClonePos[i][0], sCI2A_ClonePos[i][1] + (t >= h6 ? Sin((t * 8 + i * 37) & 0xFF, 2) : 0));
        }
        else
        {
            TI_Show(id, FALSE);
        }
        if (t < h10)
            CI2A_Puff(sTI->extra[i], t, at, sCI2A_ClonePos[i][0], sCI2A_ClonePos[i][1] + 8);
        else   // de grote poef aan het eind
            CI2A_Puff(sTI->extra[i], t, h10 + (i & 1), sCI2A_ClonePos[i][0], sCI2A_ClonePos[i][1]);
    }
    // de wervelbol + bladerwervel, de wereld draait mee
    if (TI_AT(h6))
        PlaySE(SE_M_RAZOR_WIND);
    if (TI_AT(TI_Beat2(8)))
        PlaySE(SE_M_GUST);
    if (t >= h6 && t < h10 + 2)
    {
        s32 r = TI_Ramp(t, h6, TI_Beat2(9)), sc = 65536 / (64 + r * 448 / 256);
        u8 orb = sTI->v[NB_ORB];
        TI_Show(orb, TRUE);
        TI_Scale(orb, sc, sc, (u16)(t * 0x1600));
        gSprites[orb].x2 = Sin((t * 40) & 0xFF, 1);
        twist = r * 10 >> 8;
        for (i = 0; i < NB_LEAVES; i++)
        {
            s32 a = (i * 26 + t * (6 + (i & 1))) & 0xFF, rad = 100 - (TI_Ramp(t, h6, h10) * 56 >> 8) + (i & 3) * 6;
            u8 id = sTI->v[NB_LEAF + i];
            TI_Show(id, TRUE);
            TI_Pos(id, 120 + Cos(a, rad * 3 / 2), 96 + Sin(a, rad * 2 / 3));
            gSprites[id].oam.tileNum = GetSpriteTileStartByTag(ANIM_TAG_LEAF) + (((t >> 2) + i) & 7) * 4;
        }
    }
    else
    {
        TI_Show(sTI->v[NB_ORB], FALSE);
        for (i = 0; i < NB_LEAVES; i++)
            TI_Show(sTI->v[NB_LEAF + i], FALSE);
    }
    if (TI_AT(h10))
        PlaySE(SE_M_EXPLOSION);
    if (t >= h10 + 8)
    {
        TI_Show(sTI->v[NB_END], TRUE);
        TI_Scale(sTI->v[NB_END], 128, 128, 0);
    }
    if (t >= TI_Beat2(3) && t < h10)
        eva = max(eva, twist);
    sTI->bldalpha = BLDALPHA_BLEND(eva, 16);
    TI_Shake(shake + (t >= h6 && t < h10 ? 1 : 0));
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        sTI->back[TIB_WX][y] = sTI->camX + sTI->wx + (twist ? Sin((y * 3 + t * 9) & 0xFF, twist * (80 - abs(y - 80)) / 80) : 0);
    TI_Tint(TI_World(), t >= h10 ? 8 - min(8, (t - h10) / 2) : TI_Ramp(t, 0, h6) * 8 >> 8, RGB(2, 2, 6));
    TI_Flash(t, h10, 10, 16, PALETTES_ALL, RGB(31, 31, 31));
    return t >= end;
}

static const struct TIntro sCI_Ninja2 = {CINinja2_Init, CINinja2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Collector: kaarten, LOSERS., de bril glimt, en een gigantische Wailord-knuffel

#define CO_CARDS  5
#define CO_CARD   0   // 0-4
#define CO_ICON   5   // 5-9
#define CO_LOSERS 10
#define CO_PIC    11
#define CO_SPARK  12  // 12-13
// 1 rand, 2 geel, 3 wit, 4 holo, 5 grijs, 6 rood
static const u16 sCI2A_CardPal[7] = {0, RGB(4, 4, 6), RGB(31, 26, 6), RGB(31, 31, 30), RGB(18, 26, 31), RGB(18, 18, 20), RGB(31, 6, 4)};
// 1 rand, 2 lijf, 3 buik, 4 wit, 5 roze, 6 naad
static const u16 sCI2A_WailordPal[7] = {0, RGB(3, 5, 12), RGB(9, 16, 28), RGB(29, 27, 20), RGB(31, 31, 31), RGB(31, 15, 17), RGB(5, 9, 19)};
static const u16 sCI2A_CardMons[CO_CARDS] = {SPECIES_PIKACHU, SPECIES_CHARIZARD, SPECIES_MEW, SPECIES_GENGAR, SPECIES_EEVEE};
static const u16 sCI2A_Holo[6] = {RGB(31, 18, 22), RGB(31, 28, 14), RGB(18, 31, 18), RGB(14, 28, 31), RGB(20, 18, 31), RGB(31, 18, 31)};

static void CI2A_DrawWailord(void)
{
    s16 xa[DISPLAY_HEIGHT], xb[DISPLAY_HEIGHT], ba[DISPLAY_HEIGHT], bb[DISPLAY_HEIGHT];
    s32 y, x;
    CI2A_Ellipse(xa, xb, 0, DISPLAY_HEIGHT, 124, 94, 128, 66);
    CI2A_Fill(xa, xb, 0, DISPLAY_HEIGHT, 2, CI2A_Solid(2));
    // buik: onderste deel, binnen het lijf
    CI2A_Ellipse(ba, bb, 0, DISPLAY_HEIGHT, 112, 156, 124, 46);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        ba[y] = max(ba[y], xa[y]);
        bb[y] = min(bb[y], xb[y]);
        if (bb[y] < ba[y])
            ba[y] = bb[y] = 0;
    }
    CI2A_Fill(ba, bb, 0, DISPLAY_HEIGHT, 3, CI2A_Solid(3));
    // naad (stiksels) langs de buik
    for (x = 4; x < 236; x += 7)
        for (y = 30; y < DISPLAY_HEIGHT; y++)
            if (x >= ba[y] && x < bb[y])
            {
                TI_Line(x, y + 2, x + 3, y + 2, 0, 256, 0, 6);
                break;
            }
    CI2A_Ring(124, 94, 128, 66, 1, 1);
    // blaasgat-bultjes, oog met glimlicht, bek, blosje
    CI2A_FillEllipse(150, 30, 7, 5, 2, 0);
    CI2A_FillEllipse(166, 32, 6, 4, 2, 0);
    CI2A_FillEllipse(34, 76, 9, 10, 1, 0);
    CI2A_FillEllipse(31, 72, 3, 3, 4, 0);
    CI2A_FillEllipse(30, 96, 7, 3, 5, 0);
    TI_Line(0, 108, 40, 112, 0, 256, 0, 1);
    TI_Line(40, 112, 62, 108, 0, 256, 0, 1);
    // het label: MINT
    TI_TextBg(COMPOUND_STRING("MINT"), 24, 16, 5, 2, -1, 0, 4, 1, 4, FONT_NORMAL, 15);
    TI_Line(206, 128, 200, 112, 0, 256, 0, 1);
}

static void CICollect_Init(void)
{
    u8 *buf = AllocZeroed(4 * 4 * 32);
    u32 i;
    TI_SetPal(15, sCI2A_WailordPal, ARRAY_COUNT(sCI2A_WailordPal));
    CI2A_DrawWailord();
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0);
    CI2A_Rise(DISPLAY_HEIGHT);
    // de kaart: gele rand, naamstrook met HP-stip, holovak, twee tekstregels
    if (buf != NULL)
    {
        CI2A_BufRect(buf, 4, 4, 0, 28, 32, 1);
        CI2A_BufRect(buf, 4, 5, 1, 27, 31, 2);
        CI2A_BufRect(buf, 4, 7, 3, 25, 6, 3);
        CI2A_BufRect(buf, 4, 22, 4, 24, 5, 6);
        CI2A_BufRect(buf, 4, 7, 7, 25, 19, 4);
        CI2A_BufRect(buf, 4, 7, 20, 25, 29, 3);
        CI2A_BufRect(buf, 4, 8, 22, 21, 23, 5);
        CI2A_BufRect(buf, 4, 8, 25, 18, 26, 5);
        for (i = 0; i < CO_CARDS; i++)
        {
            sTI->v[CO_CARD + i] = TI_BufSprite(buf, 4 * 4 * 32, CI2A_TAG_SHEET, sCI2A_CardPal, &gOamData_AffineOff_ObjNormal_32x32, -40, -40);
            if (sTI->v[CO_CARD + i] < MAX_SPRITES)
                gSprites[sTI->v[CO_CARD + i]].subpriority = 3;
        }
        Free(buf);
    }
    for (i = 0; i < CO_CARDS; i++)
    {
        sTI->v[CO_ICON + i] = CI2A_Icon(sCI2A_CardMons[i], -40, -40);
        if (sTI->v[CO_ICON + i] < MAX_SPRITES)
            gSprites[sTI->v[CO_ICON + i]].subpriority = 2;
    }
    sTI->v[CO_LOSERS] = TI_TextSprite(COMPOUND_STRING("LOSERS."), 8, 4, 8, CI2A_TAG_TXT1, sCI2A_TextPal, &gOamData_AffineDouble_ObjNormal_64x32, 120, 126);
    TI_Show(sTI->v[CO_LOSERS], FALSE);
    sTI->v[CO_PIC] = TI_Trainer(TRAINER_PIC_COLLECTOR, 120, 200, TRUE);
    TI_Show(sTI->v[CO_PIC], FALSE);
    TI_Scale(sTI->v[CO_PIC], 128, 128, 0);
    for (i = 0; i < 2; i++)
    {
        sTI->v[CO_SPARK + i] = TI_Anim(ANIM_TAG_SPARKLE_4, &gOamData_AffineDouble_ObjNormal_32x32, -40, -40, 16);
        TI_Show(sTI->v[CO_SPARK + i], FALSE);
    }
    PlaySE(SE_RG_CARD_FLIPPING);
}

static bool32 CICollect_Update(s32 t)
{
    s32 h5 = TI_Beat2(5), h6 = TI_Beat2(6), h7 = TI_Beat2(7), h8 = TI_Beat2(8), h10 = TI_Beat2(10), end = TI_Beat2(11) + 6;
    s32 i, r, holo;
    // kaarten schuiven één voor één op hun plek, op de halve tel; vanaf de 3e tel vallen ze weg
    for (i = 0; i < CO_CARDS; i++)
    {
        s32 at = TI_Beat2(i), sx = 40 + i * 40, x;
        u8 card = sTI->v[CO_CARD + i], icon = sTI->v[CO_ICON + i];
        if (TI_AT(at))
            PlaySE(SE_RG_CARD_FLIP);
        if (TI_AT(h6))
        {
            s32 vx = TI_RandRange(-24, 24), vy = -TI_RandRange(30, 50);
            TI_Part(card, sx, 52, vx, vy, 8, 30);
            TI_Part(icon, sx, 48, vx, vy, 8, 30);
        }
        if (t >= h6 || t < at - 10)
            continue;
        r = 256 - TI_Ramp(t, at - 10, at);
        x = sx + ((270 - sx) * r * r >> 16);
        TI_Show(card, TRUE);
        TI_Show(icon, TRUE);
        TI_Pos(card, x, 52 + Sin((t * 6 + i * 50) & 0xFF, 2));
        TI_Pos(icon, x, 48 + Sin((t * 6 + i * 50) & 0xFF, 2));
    }
    // holo: het kaartvak loopt door de regenboog
    if (sTI->v[CO_CARD] < MAX_SPRITES)
    {
        holo = 16 + gSprites[sTI->v[CO_CARD]].oam.paletteNum;
        gPlttBufferFaded[holo * 16 + 4] = sCI2A_Holo[(t >> 2) % 6];
    }
    // LOSERS.
    if (TI_AT(h5))
        PlaySE(SE_M_SWAGGER);
    if (t >= h5 && t < h8)
    {
        TI_Show(sTI->v[CO_LOSERS], TRUE);
        r = max(128, 320 - (t - h5) * 48);
        TI_Scale(sTI->v[CO_LOSERS], r, r, 0);
    }
    else
    {
        TI_Show(sTI->v[CO_LOSERS], FALSE);
    }
    // de verzamelaar komt omhoog, de bril glimt
    if (t >= h6)
    {
        TI_Show(sTI->v[CO_PIC], TRUE);
        TI_Pos(sTI->v[CO_PIC], 120, 104 + (96 * (256 - TI_Ramp(t, h6, h6 + 8)) >> 8));
    }
    if (TI_AT(h7))
        PlaySE(SE_SHINY);
    for (i = 0; i < 2; i++)
    {
        s32 dt = t - h7 - i * 3;
        u8 id = sTI->v[CO_SPARK + i];
        if (t >= h10)
            dt = t - h10 - i * 4;   // nog een glinster op de knuffel
        if (dt >= 0 && dt < 14)
        {
            s32 sc = 256 * 6 / (1 + min(dt, 13 - dt) * 2);
            TI_Show(id, TRUE);
            if (t >= h10)
                TI_Pos(id, i ? 40 : 26, i ? 82 : 68);
            else
                TI_Pos(id, i ? 128 : 116, 64);
            TI_Scale(id, max(128, sc), max(128, sc), (u16)(dt * 0x900));
        }
        else
        {
            TI_Show(id, FALSE);
        }
    }
    TI_Flash(t, h7, 6, 10, TI_PalBit(sTI->v[CO_PIC]), RGB(31, 31, 31));
    // en dan: de knuffel
    if (TI_AT(h8))
        PlaySE(SE_M_STRENGTH);
    if (TI_AT(h10))
        PlaySE(SE_BALL_BOUNCE_1);
    if (t >= h8)
    {
        r = TI_Ramp(t, h8, h10);
        CI2A_Rise(t < h10 ? 160 - (r * (512 - r) * 160 >> 16) : -Sin(min(128, (t - h10) * 16), 6));
    }
    TI_Tint(TI_World(), TI_Ramp(t, 0, h5) * 9 >> 8, RGB(1, 1, 3));
    if (t >= end)
        for (i = 0; i < CO_CARDS; i++)
            CI2A_FreeIcon(sTI->v[CO_ICON + i]);
    return t >= end;
}

static const struct TIntro sCI_Collect = {CICollect_Init, CICollect_Update};
