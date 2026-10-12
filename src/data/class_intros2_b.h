// Project Grounded: trainerklasse-intro's v2 (Jordi), deel b: Hiker, Psychic, Bird Keeper, Battle Girl.
// Opgenomen in src/battle_transition.c direct na src/data/class_intros.h; gebruikt de runner en de TI_*-helpers daarvan.
//
//   Hiker        springt als een superheld (cape, speedlines) van rots naar rots omhoog; dan wolkige randen, het beeld
//                golft: het was een droomwolk. De echte Hiker zit in de hoek te lachen: HO HO HO.
//   Psychic      Poké Ball, Potion, lepel en Old Rod zweven wiebelig omhoog (paars glimmetje), de Psychic perst
//                (trillende lijntjes), en dan valt alles tegelijk: plof.
//   Bird Keeper  dramatische lancering van een Wingull, het beeld volgt hem één tel door de lucht... en hij landt
//                meteen naast een Oran Berry en pikt. “…wtf.”
//   Battle Girl  in flying-kick-pose door een muur, een rots, een bunker, de maan en de zon. HAIYAAAH.

#include "pokemon_icon.h"
#include "graphics.h"

#pragma GCC push_options
#pragma GCC optimize("Os")   // klein houden (Jordi: licht qua KB's); snelheid is hier ruim genoeg

#define C2B_TAG_STREAK 0x7EB0
#define C2B_TAG_TEXT   0x7EB1   // t/m 0x7EB3
#define C2B_TAG_ITEM   0x7EB4   // t/m 0x7EB7
#define C2B_TAG_GULL   0x7EB8
#define C2B_TAG_OBST   0x7EB9
#define C2B_TAG_CHUNK  0x7EBA
#define C2B_TAG_CAPE   0x7EBB

static const u16 sC2B_StreakPal[3] = {0, RGB(31, 31, 31), RGB(22, 24, 31)};
static const u16 sC2B_TextPal[3] = {0, RGB(31, 31, 31), RGB(6, 4, 10)};

// een witte streep (32x16, lijn in het midden, loopt taps af): speedlines
static u8 C2B_Streak(void)
{
    u8 buf[4 * 2 * 32], id;
    s32 x;
    memset(buf, 0, sizeof(buf));
    for (x = 0; x < 32; x++)
    {
        TI_BufPixel(buf, 4, x, 7, x < 6 ? 2 : 1);
        if (x > 12)
            TI_BufPixel(buf, 4, x, 8, x < 20 ? 2 : 1);
    }
    id = TI_BufSprite(buf, sizeof(buf), C2B_TAG_STREAK, sC2B_StreakPal, &gOamData_AffineDouble_ObjNormal_32x16, 0, -40);
    TI_Show(id, FALSE);
    return id;
}

static u8 C2B_Text(const u8 *str, u32 n, u32 w, u32 h, s16 x, s16 y)
{
    const struct OamData *oam = (w == 4) ? &gOamData_AffineDouble_ObjNormal_32x16 : &gOamData_AffineDouble_ObjNormal_64x32;
    u8 id = TI_TextSprite(str, w, h, w == 4 ? 1 : 9, C2B_TAG_TEXT + n, sC2B_TextPal, oam, x, y);
    TI_Show(id, FALSE);
    return id;
}

// item-icoon (32x32, niet affien) affien maken, zodat het groter kan en kan draaien
static void C2B_Affine(u8 id)
{
    struct Sprite *sp;
    u8 m;
    if (id >= MAX_SPRITES)
        return;
    m = AllocOamMatrix();
    if (m == 0xFF)
        return;
    sp = &gSprites[id];
    sp->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    sp->oam.matrixNum = m;
    CalcCenterToCornerVec(sp, SPRITE_SHAPE(32x32), SPRITE_SIZE(32x32), ST_OAM_AFFINE_DOUBLE);
    SetOamMatrixRotationScaling(m, 256, 256, 0);
}

// ---------------------------------------------------------------------------------------------------------------------
// Hiker: de superheld-droom
//   v[0] droom-Hiker, v[1] cape, v[2..5] speedlines, v[6] echte Hiker, v[7..9] HO, v[10] voortgang wolkrand,
//   v[11] schudden
static const u16 sC2B_HikerPal[16] =
{
    0, RGB(12, 9, 8), RGB(21, 17, 12), RGB(14, 12, 12), RGB(23, 19, 15), RGB(16, 15, 16), RGB(24, 22, 21),
    RGB(18, 18, 21), RGB(26, 25, 27), RGB(31, 31, 31), RGB(22, 20, 29), RGB(6, 5, 5),
    RGB(9, 14, 27), RGB(13, 19, 29), RGB(19, 24, 31), RGB(16, 18, 26),
};
static const u16 sC2B_HoPal[3] = {0, RGB(31, 23, 4), RGB(9, 3, 2)};
static const u16 sC2B_CapePal[4] = {0, RGB(28, 4, 5), RGB(18, 2, 4), RGB(31, 25, 6)};
// rotspieken (in pixels): x0, x1, bovenkant; van dichtbij (onder) naar ver (boven)
static const u8 sC2B_Ledges[4][3] = {{184, 232, 144}, {112, 160, 112}, {32, 80, 80}, {128, 184, 48}};
static const s16 sC2B_HikerPos[4][2] = {{208, 124}, {136, 92}, {56, 60}, {156, 28}};

static void CIHiker2_Init(void)
{
    u8 cape[4 * 4 * 32];
    s32 i, x, y, d;
    u32 sky[5];
    TI_SetPal(15, sC2B_HikerPal, ARRAY_COUNT(sC2B_HikerPal));
    // lucht in banden (met een dither-rij ertussen), dan een nevelige bergketen, dan de rotspieken
    for (i = 0; i < 5; i++)
    {
        sky[i] = TI_NewTile();
        for (y = 0; y < 8; y++)
            for (x = 0; x < 8; x++)
                TI_TilePixel(sky[i], x, y, (i & 1) ? (((x + y) & 1) ? 12 + i / 2 : 13 + i / 2) : 12 + i / 2);
    }
    for (y = 0; y < 20; y++)
        for (x = 0; x < 30; x++)
            TI_Put(x, y, sky[y < 6 ? 0 : y == 6 ? 1 : y < 12 ? 2 : y == 12 ? 3 : 4] | (15 << 12));
    {
        u32 haze = TI_NewTile();
        TI_SolidTile(haze, 15);
        for (i = 0; i < 30; i++)
        {
            s32 hmax = 0, row;
            for (x = i * 8; x < i * 8 + 8; x++)
                hmax = max(hmax, 92 + Sin((x * 3) & 0xFF, 16) + Sin((x * 9 + 40) & 0xFF, 5));
            row = (hmax + 7) / 8;
            for (y = row; y < 20; y++)
                TI_Put(i, y, haze | (15 << 12));
            for (x = i * 8; x < i * 8 + 8; x++)
                for (y = 92 + Sin((x * 3) & 0xFF, 16) + Sin((x * 9 + 40) & 0xFF, 5); y < row * 8; y++)
                    TI_Plot(x, y, 15);
        }
    }
    for (d = 3; d >= 0; d--)
    {
        s32 body = 1 + d * 2, edge = 2 + d * 2, x0 = sC2B_Ledges[d][0], x1 = sC2B_Ledges[d][1], top = sC2B_Ledges[d][2];
        for (y = top - 4; y < DISPLAY_HEIGHT; y++)
        {
            s32 w = (y - top) / 4 + ((y * 7 + d) % 3), xa = x0 - max(0, w), xb = x1 + max(0, w);
            if (y < top)   // grillige top
            {
                for (x = x0; x < x1; x++)
                    if (Sin((x * 23 + d * 50) & 0xFF, 3) + 3 > top - y)
                        TI_Plot(x, y, edge);
                continue;
            }
            for (x = xa; x < xb; x++)
                TI_Plot(x, y, (y < top + 3 || x < xa + 2) ? edge : (x >= xb - 2) ? 11 : body);
        }
        // een paar barsten
        TI_Line(x0 + 10, top + 14, x0 + 18, top + 30, 0, 256, 0, 11);
        TI_Line(x1 - 12, top + 26, x1 - 20, top + 44, 0, 256, 0, 11);
    }
    // randen buiten beeld (het schudden schuift BG0 een paar pixels): kopie van de buren
    for (y = 0; y < 20; y++)
    {
        sTI->bg0map[y * 32 + 30] = sTI->bg0map[y * 32 + 29];
        sTI->bg0map[y * 32 + 31] = sTI->bg0map[y * 32 + 0];
    }
    for (x = 0; x < 32; x++)
    {
        sTI->bg0map[20 * 32 + x] = sTI->bg0map[19 * 32 + x];
        sTI->bg0map[31 * 32 + x] = sTI->bg0map[0 * 32 + x];
    }
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0 | WINOUT_WIN01_CLR);
    sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
    sTI->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);

    // cape: driehoek naar rechts (wappert achter de Hiker aan)
    memset(cape, 0, sizeof(cape));
    for (y = 4; y < 30; y++)
        for (x = 2; x < 30; x++)
        {
            s32 half = (x * 13) >> 5;   // breder naar achter
            if (abs(y - 14 - (x >> 3)) <= half)
                TI_BufPixel(cape, 4, x, y, ((x + y * 2) % 11) < 2 ? 2 : (x < 4 ? 3 : 1));
        }
    sTI->v[1] = TI_BufSprite(cape, sizeof(cape), C2B_TAG_CAPE, sC2B_CapePal, &gOamData_AffineDouble_ObjNormal_32x32, 0, -60);
    gSprites[sTI->v[1]].subpriority = 20;
    sTI->v[0] = TI_Trainer(GetTrainerPicFromId(sTI->trainer), sC2B_HikerPos[0][0], sC2B_HikerPos[0][1], TRUE);
    TI_Scale(sTI->v[0], 341, 341, 0);
    for (i = 0; i < 4; i++)
        sTI->v[2 + i] = C2B_Streak();
    sTI->v[6] = TI_Trainer(GetTrainerPicFromId(sTI->trainer), 40, 200, TRUE);
    TI_Show(sTI->v[6], FALSE);
    for (i = 0; i < 3; i++)
    {
        sTI->v[7 + i] = TI_TextSprite(COMPOUND_STRING("HO"), 8, 4, 9, C2B_TAG_TEXT + i, sC2B_HoPal, &gOamData_AffineDouble_ObjNormal_64x32, 96 + i * 44, 112 - i * 30);
        TI_Show(sTI->v[7 + i], FALSE);
    }
    PlaySE(SE_M_DOUBLE_TEAM);
}

// gevulde wolk-cirkel op BG0: schaduwrand + wit
static void C2B_Puff(s32 x, s32 y, s32 r)
{
    TI_Stamp(x, y, r + 2, 10);
    TI_Stamp(x - 1, y - 1, r, 9);
}

static bool32 CIHiker2_Update(s32 t)
{
    s32 b4 = TI_Beat(4), b5 = TI_Beat(5), end = TI_Beat(7) + 4, i, y, r, n, cx, cy;
    u8 h = sTI->v[0], cape = sTI->v[1];
    s32 dir = -1;

    // sprongen: landt op richel n precies op tel n (1..3); de hele tel is één boog
    n = 0;
    for (i = 1; i <= 3; i++)
        if (t >= TI_Beat(i - 1))
            n = i;
    if (n == 0)
    {
        cx = sC2B_HikerPos[0][0];
        cy = sC2B_HikerPos[0][1] + (t > 2 ? 2 : 0);   // door de knieën
    }
    else if (t >= TI_Beat(3))
    {
        cx = sC2B_HikerPos[3][0];
        cy = sC2B_HikerPos[3][1] + (t < TI_Beat(3) + 4 ? 3 : 0);
        dir = 1;
    }
    else
    {
        s32 a = TI_Beat(n - 1), bb = TI_Beat(n), k = TI_Ramp(t, a, bb);
        s32 x0 = sC2B_HikerPos[n - 1][0], y0 = sC2B_HikerPos[n - 1][1], x1 = sC2B_HikerPos[n][0], y1 = sC2B_HikerPos[n][1];
        cx = x0 + ((x1 - x0) * k >> 8);
        cy = y0 + ((y1 - y0) * k >> 8) - Sin(k >> 1, 34);
        dir = x1 < x0 ? -1 : 1;
        // speedlines achter hem aan
        for (i = 0; i < 4; i++)
        {
            u8 s = sTI->v[2 + i];
            s32 back = 10 + i * 9, ang;
            TI_Show(s, k > 10 && k < 236);
            TI_Pos(s, cx - dir * back + (i & 1 ? 6 : -6), cy + 10 + back / 2 - i * 4);
            ang = dir < 0 ? 0xE000 : 0x2000;   // schuin, met de sprong mee
            TI_Scale(s, dir < 0 ? -256 : 256, 256, ang);
        }
    }
    if (t >= TI_Beat(3))
        for (i = 0; i < 4; i++)
            TI_Show(sTI->v[2 + i], FALSE);
    for (i = 1; i <= 3; i++)
    {
        if (TI_AT(TI_Beat(i - 1)) && i > 1)
            PlaySE(SE_LEDGE);
        if (TI_AT(TI_Beat(i)))
        {
            PlaySE(i == 3 ? SE_M_MEGA_KICK : SE_M_ROCK_THROW);
            sTI->v[11] = i == 3 ? 5 : 3;
        }
    }
    if (TI_AT(TI_Beat(0)))
        PlaySE(SE_LEDGE);
    TI_Pos(h, cx, cy);
    // heldenpose: iets groter, schuin vooruit; in de lucht gestrekt
    if (t >= TI_Beat(3))
        TI_Scale(h, 300, 300, 0);
    else
        TI_Scale(h, 341 * (dir < 0 ? 1 : -1), 330, (dir < 0 ? 0x0600 : 0xFA00));
    // cape aan de schouders, wappert
    TI_Pos(cape, cx - dir * 18, cy - 2);
    TI_Scale(cape, dir < 0 ? 256 : -256, 256 - Sin((t * 20) & 0xFF, 50), (Sin((t * 14) & 0xFF, 10) << 8) & 0xFFFF);

    if (sTI->v[11] > 0)
        sTI->v[11]--;
    TI_Shake(sTI->v[11]);
    TI_Flash(t, TI_Beat(3), 8, 12, PALETTES_ALL, RGB(31, 31, 24));

    // de droomwolk: wolkranden groeien naar binnen, het beeld golft en wordt bleek
    if (t >= b4)
    {
        static const s16 sEdge[][3] = {
            {0, 0, 24}, {120, -4, 18}, {240, 0, 24}, {0, 160, 24}, {240, 160, 24}, {60, -6, 16}, {180, -6, 16},
            {-6, 80, 18}, {246, 80, 18}, {-4, 40, 14}, {244, 40, 14}, {-4, 120, 14}, {244, 120, 14}, {30, -4, 12},
            {90, -6, 14}, {150, -6, 14}, {210, -4, 12}, {60, 164, 16}, {120, 166, 18}, {180, 164, 16}, {30, 162, 12},
            {90, 164, 12}, {150, 164, 12}, {210, 162, 12},
        };
        if (TI_AT(b4))
            PlaySE(SE_M_HEAL_BELL);
        for (i = 0; i < 3 && sTI->v[10] < (s32)ARRAY_COUNT(sEdge); i++, sTI->v[10]++)
        {
            const s16 *e = sEdge[sTI->v[10]];
            C2B_Puff(e[0], e[1], e[2]);
        }
        // wazig: de droom (BG0 behalve de wolk, en de droom-Hiker met cape) verbleekt en golft zacht
        r = TI_Ramp(t, b4, b5) * 9 >> 8;
        for (i = 1; i < 16; i++)
            if (i != 9 && i != 10)
                gPlttBufferFaded[15 * 16 + i] = Tapu_Blend(sTI->base[15 * 16 + i], RGB(29, 27, 31), r);
        // de droom-Hiker wordt doorschijnend (de echte deelt zijn palet, dus niet via de kleuren)
        if (TI_AT(b4))
        {
            gSprites[h].oam.objMode = ST_OAM_OBJ_BLEND;
            gSprites[cape].oam.objMode = ST_OAM_OBJ_BLEND;
            TI_Blend(BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG0, 16, 0);
        }
        sTI->bldalpha = BLDALPHA_BLEND(16 - (r >> 1) - (r >> 2), (r >> 1) + (r >> 2));
    }
    // de echte Hiker in de hoek, met denkwolkjes; lacht HO HO HO
    if (t >= b5)
    {
        s32 dt = t - b5, j;
        if (TI_AT(b5))
        {
            PlaySE(SE_M_SWAGGER);
            C2B_Puff(80, 102, 3);
            C2B_Puff(92, 90, 5);
            C2B_Puff(108, 76, 7);
        }
        TI_Show(sTI->v[6], TRUE);
        y = 124 - abs(Sin((dt * 16) & 0xFF, 5));
        TI_Pos(sTI->v[6], 42, dt < 6 ? 200 - dt * 13 : y);
        TI_Scale(sTI->v[6], 256 + Sin((dt * 32) & 0xFF, 12), 256 - Sin((dt * 32) & 0xFF, 12), (Sin((dt * 16) & 0xFF, 6) << 8) & 0xFFFF);
        for (j = 0; j < 3; j++)
        {
            s32 at = TI_Beat2(10 + j) - b5, k;
            if (dt < at)
                continue;
            k = TI_Ramp(dt, at, at + 5);
            TI_Show(sTI->v[7 + j], TRUE);
            TI_Scale(sTI->v[7 + j], 384 - k, 384 - k, (Sin(((dt - at) * 20) & 0xFF, 8) << 8) & 0xFFFF);
            gSprites[sTI->v[7 + j]].y2 = -abs(Sin(((dt - at) * 16) & 0xFF, 3));
        }
    }
    else
    {
        TI_Show(sTI->v[6], FALSE);
    }
    return t >= end;
}

static const struct TIntro sCI_Hiker = {CIHiker2_Init, CIHiker2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Psychic: gewone spullen zweven amateuristisch omhoog en vallen dan allemaal tegelijk
//   v[0] Psychic, v[1..4] items, v[5] "...plof", v[6] schudden
static const u16 sC2B_PsyItems[4] = {ITEM_POKE_BALL, ITEM_POTION, ITEM_TWISTED_SPOON, ITEM_OLD_ROD};
static const s16 sC2B_PsyX[4] = {50, 92, 150, 194};
static const s8 sC2B_PsyLift[4] = {80, 94, 72, 86};
static const u16 sC2B_PsyPal[3] = {0, RGB(27, 18, 31), RGB(31, 31, 31)};
#define PSY_GROUND 136

static void CIPsychic2_Init(void)
{
    u32 i;
    TI_SetPal(15, sC2B_PsyPal, ARRAY_COUNT(sC2B_PsyPal));
    sTI->v[0] = TI_Trainer(GetTrainerPicFromId(sTI->trainer), 120, 84, TRUE);
    for (i = 0; i < 4; i++)
    {
        sTI->v[1 + i] = TI_Item(C2B_TAG_ITEM + i, sC2B_PsyItems[i], sC2B_PsyX[i], PSY_GROUND);
        C2B_Affine(sTI->v[1 + i]);
    }
    sTI->v[5] = C2B_Text(COMPOUND_STRING("…plop."), 0, 8, 4, 120, 30);
    PlaySE(SE_M_PSYBEAM);
}

static bool32 CIPsychic2_Update(s32 t)
{
    s32 b1 = TI_Beat(1), drop = TI_Beat(4), end = TI_Beat(6), i, k;
    u8 psy = sTI->v[0];
    // concentratie: trillende lijntjes rond het hoofd
    if (TI_AT(b1))
    {
        PlaySE(SE_M_TELEPORT);
        for (i = 0; i < 12; i++)
        {
            s32 a = (i * 21 + 136) & 0xFF;
            TI_Line(120 + Cos(a, 30), 56 + Sin(a, 27), 120 + Cos(a, 40), 56 + Sin(a, 36), 0, 256, 1, (i & 1) + 1);
        }
    }
    if (t >= b1 && t < drop)
    {
        sTI->bg0x = TI_RandRange(-1, 1);
        sTI->bg0y = TI_RandRange(-1, 1);
        gSprites[psy].x2 = TI_RandRange(-1, 1) * (1 + (t >= TI_Beat(3)));
        TI_Scale(psy, 256 + Sin((t * 40) & 0xFF, 4), 256 - (TI_Ramp(t, b1, drop) * 10 >> 8), 0);
    }
    for (i = 0; i < 4; i++)
    {
        u8 it = sTI->v[1 + i];
        s32 lift, wob;
        if (t >= drop)
            break;
        // amateur-levitatie: met horten en stoten, de Old Rod zakt steeds terug
        lift = TI_Ramp(t, b1 + i * 5, TI_Beat(3) + i * 3) * sC2B_PsyLift[i] >> 8;
        if (((t + i * 7) & 15) < 3)
            lift -= 3;
        if (i == 3)
            lift = lift * (192 + Sin((t * 6) & 0xFF, 64)) >> 8;
        wob = Sin((t * (9 + i * 2) + i * 60) & 0xFF, 3 + (t >= TI_Beat(3)) * 2);
        TI_Pos(it, sC2B_PsyX[i] + wob, PSY_GROUND - lift + (Cos((t * 11 + i * 40) & 0xFF, 2)));
        TI_Scale(it, 171, 171, (Sin((t * (7 + i) + i * 50) & 0xFF, 10) << 8) & 0xFFFF);
        // paars glimmetje
        if (t >= b1)
            TI_TintMore(TI_PalBit(it), 5 + Sin((t * 12 + i * 64) & 0xFF, 4), RGB(24, 8, 31));
    }
    if (t >= b1 && t < drop)
        TI_Tint(TI_World(), TI_Ramp(t, 0, drop) * 8 >> 8, RGB(12, 4, 18));
    // en... plof
    if (TI_AT(drop))
    {
        PlaySE(SE_FALL);
        TI_FillMap(0);
        sTI->bg0x = sTI->bg0y = 0;
        gSprites[psy].x2 = 0;
        for (i = 0; i < 4; i++)
        {
            u8 it = sTI->v[1 + i];
            TI_Part(it, gSprites[it].x, gSprites[it].y, 0, 0, 5, 0);
            TI_Scale(it, 171, 171, 0);
        }
    }
    if (t >= drop)
    {
        for (i = 0; i < 4; i++)
        {
            struct TIPart *p;
            u32 j;
            for (j = 0; j < TI_MAX_PART; j++)
            {
                p = &sTI->part[j];
                if (p->on && p->slot == sTI->v[1 + i] && p->y > PSY_GROUND * 16)
                {
                    p->y = PSY_GROUND * 16;
                    if (p->vy > 30)
                    {
                        p->vy = -p->vy / 4;
                        if (i == 0)
                        {
                            PlaySE(SE_M_STRENGTH);
                            sTI->v[6] = 4;
                        }
                    }
                    else
                    {
                        p->vy = 0;
                        p->ay = 0;
                    }
                }
            }
        }
        k = TI_Ramp(t, drop, drop + 6);
        TI_Scale(psy, 256, 236 + (k * 20 >> 8), 0);
        TI_Tint(TI_World(), 8 - (k * 8 >> 8), RGB(12, 4, 18));
    }
    if (sTI->v[6] > 0)
    {
        sTI->v[6]--;
        TI_WorldMove(0, sTI->v[6] & 1 ? 2 : -1);
    }
    else
    {
        TI_WorldMove(0, 0);
    }
    if (t >= TI_Beat(5))
    {
        TI_Show(sTI->v[5], TRUE);
        TI_Scale(sTI->v[5], 192, 192, 0);
    }
    return t >= end;
}

static const struct TIntro sCI_Psychic = {CIPsychic2_Init, CIPsychic2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Bird Keeper: de Wingull gaat de wijde wereld in... en landt meteen bij het voer
//   v[0] Bird Keeper, v[1] Wingull, v[2] Oran Berry, v[3] "!", v[4] "...wtf.", v[5..8] speedlines
#define BK_X 180
#define BK_Y 92

static void CIBird2_Init(void)
{
    u32 i, n;
    const u16 *pal = gMonIconPalettes[gSpeciesInfo[SPECIES_WINGULL].iconPalIndex];
    TI_SetPal(15, sC2B_StreakPal, 3);
    TI_SetCol(15, 3, RGB(27, 29, 31));
    // lucht-shot op BG0 (verborgen tot de lancering): wolken en windstrepen
    for (n = 0; n < 7; n++)
    {
        s32 x = 34 + n * 30, y = 22 + ((n * 53) % 110), w = 14 + (n * 7) % 12;
        for (i = 0; i < 3; i++)
            TI_Stamp(x + (s32)i * w / 2 - w / 2, y - (i == 1) * 4, 7 + (i == 1) * 3, 3);
        TI_Line(max(4, x - 40), y + 14, x - 4, y + 14, 0, 256, 0, 1);
    }
    TI_Windows(DISPCNT_WIN0_ON, WININ_WIN0_ALL, TI_NO_BG0 | WINOUT_WIN01_CLR);
    sTI->win0h = WIN_RANGE(0, 0);
    sTI->win0v = WIN_RANGE(0, DISPLAY_HEIGHT);
    sTI->v[0] = TI_Trainer(GetTrainerPicFromId(sTI->trainer), BK_X, BK_Y, TRUE);
    sTI->v[2] = TI_Item(C2B_TAG_ITEM, ITEM_ORAN_BERRY, 46, 136);
    sTI->v[1] = TI_BufSprite(GetMonIconPtr(SPECIES_WINGULL, 0), 1024, C2B_TAG_GULL, pal, &gOamData_AffineDouble_ObjNormal_32x32, BK_X - 34, BK_Y - 22);
    sTI->v[3] = TI_Bang(BK_X - 4, BK_Y - 46);
    sTI->v[4] = C2B_Text(COMPOUND_STRING("…wtf."), 0, 8, 4, 104, 44);
    for (i = 0; i < 4; i++)
        sTI->v[5 + i] = C2B_Streak();
    PlaySE(SE_TAILLOW_WING_FLAP);
}

static bool32 CIBird2_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), land = b2 + 8, b4 = TI_Beat(4), b5 = TI_Beat(5), end = TI_Beat(6) + 6, i, k;
    u8 bk = sTI->v[0], gull = sTI->v[1], berry = sTI->v[2];
    u32 frame = 0;
    if (t < b1)
    {
        // aanloop: de Bird Keeper buigt naar achter, de Wingull klappert op zijn hand
        k = TI_Ramp(t, 0, b1);
        TI_Scale(bk, 256, 256, ((-k * 12) & 0xFFFF));
        TI_Pos(gull, BK_X - 34 + (k * 8 >> 8), BK_Y - 22 + (k * 6 >> 8));
        TI_Scale(gull, 171, 171, 0);
        frame = (t >> 2) & 1;
        TI_Tint(TI_World(), k * 5 >> 8, RGB(4, 4, 10));
    }
    else if (t < b2)
    {
        // lancering en één tel heldhaftig door de lucht
        s32 dt = t - b1;
        if (TI_AT(b1))
        {
            PlaySE(SE_M_FLY);
            sTI->win0h = WIN_RANGE(0, DISPLAY_WIDTH);
        }
        TI_Show(bk, FALSE);
        TI_Show(berry, FALSE);
        k = TI_Ramp(dt, 0, 6);
        TI_Pos(gull, (BK_X - 34) - ((BK_X - 34 - 112) * k >> 8), (BK_Y - 22) - ((BK_Y - 22 - 70) * k >> 8) + Sin((t * 10) & 0xFF, 4));
        TI_Scale(gull, 171 - (k * 43 >> 8), 171 - (k * 43 >> 8), (Sin((t * 6) & 0xFF, 6) << 8) & 0xFFFF);
        frame = (t >> 1) & 1;
        sTI->bg0x += 9;
        TI_Tint(TI_World(), 15, RGB(13, 21, 31));
        for (i = 0; i < 4; i++)
        {
            u8 s = sTI->v[5 + i];
            TI_Show(s, TRUE);
            TI_Scale(s, 256, 256, 0);
            TI_Pos(s, ((dt * 14 + i * 67) % 300) - 30 + 0, 30 + i * 30 + (i & 1) * 6);
        }
        TI_Flash(t, b1, 6, 16, PALETTES_ALL, RGB_WHITE);
    }
    else
    {
        // terug op aarde: hij was nooit weg
        if (TI_AT(b2))
        {
            sTI->win0h = WIN_RANGE(0, 0);
            for (i = 0; i < 4; i++)
                TI_Show(sTI->v[5 + i], FALSE);
            TI_Show(bk, TRUE);
            TI_Show(berry, TRUE);
            TI_Scale(bk, 256, 256, 0x0600);
            PlaySE(SE_M_WING_ATTACK);
        }
        k = TI_Ramp(t, b2, land);
        if (t < land)
        {
            TI_Pos(gull, 72, -16 + (k * k * 134 >> 16));
            TI_Scale(gull, 171, 171, 0);
            frame = (t >> 1) & 1;
        }
        else
        {
            // pikken op de halve tellen
            s32 p = 0;
            if (TI_AT(land))
                PlaySE(SE_LEDGE);
            for (i = 5; i <= 8; i++)
            {
                s32 at = TI_Beat2(i);
                if (t >= at && t < at + 5)
                    p = 1;
                if (TI_AT(at))
                    PlaySE(SE_RG_BAG_CURSOR);
            }
            TI_Pos(gull, 72 - p * 3, 118 + p * 5);
            TI_Scale(gull, 171, 171, p ? 0x1400 : 0);
            frame = 0;
            if (t >= TI_Beat2(8) + 3)
                TI_Show(berry, FALSE);   // op
        }
        TI_Tint(TI_World(), 0, 0);
        // de Bird Keeper: "!" en dan "...wtf."
        if (TI_AT(b4))
        {
            PlaySE(SE_PIN);
            TI_Show(sTI->v[3], TRUE);
            TI_Scale(sTI->v[3], 160, 160, 0);
        }
        if (t >= b4)
            TI_Scale(bk, 256, 256 + (t < b4 + 4 ? -12 : 0), 0);
        if (TI_AT(b5))
        {
            TI_Show(sTI->v[3], FALSE);
            TI_Show(sTI->v[4], TRUE);
            TI_Scale(sTI->v[4], 171, 171, 0);
            PlaySE(SE_FAINT);
        }
        if (t >= b5)
            TI_Scale(bk, 256, 270, 0);   // zakt een beetje in
    }
    gSprites[gull].oam.tileNum = GetSpriteTileStartByTag(C2B_TAG_GULL) + frame * 16;
    return t >= end;
}

static const struct TIntro sCI_Bird = {CIBird2_Init, CIBird2_Update};

// ---------------------------------------------------------------------------------------------------------------------
// Battle Girl: flying kick door muur, rots, bunker, maan en zon. HAIYAAAH.
//   v[0] Battle Girl, v[1] obstakel, v[2..11] brokken, v[12..17] speedlines, v[18] HAIYAAAH, v[19] schudden
static const u16 sC2B_ObstPal[15] =
{
    0, RGB(3, 3, 4), RGB(22, 8, 5), RGB(26, 23, 19), RGB(15, 14, 13), RGB(23, 22, 20), RGB(11, 13, 8), RGB(17, 19, 11),
    RGB(29, 29, 22), RGB(21, 21, 16), RGB(31, 27, 6), RGB(31, 15, 3), RGB(5, 3, 2), RGB(31, 31, 31), RGB(1, 1, 1),
};
static const u16 sC2B_HaiPal[3] = {0, RGB(31, 29, 8), RGB(24, 3, 3)};
static const u8 sC2B_ChunkCols[5][2] = {{2, 3}, {4, 5}, {6, 7}, {8, 9}, {10, 11}};
static const u8 sC2B_ImpactX[5] = {126, 124, 120, 122, 112};
#define BG_IMPACT_Y 84

// obstakel n tekenen in een 64x64-buffer (crack: met barsten)
static void C2B_DrawObstacle(u8 *buf, u32 n, bool32 crack)
{
    s32 x, y;
    memset(buf, 0, 64 * 64 / 2);
    for (y = 0; y < 64; y++)
        for (x = 0; x < 64; x++)
        {
            s32 dx = x - 32, dy = y - 32, d2 = dx * dx + dy * dy, c = 0;
            switch (n)
            {
            case 0: // bakstenen muur
                if (x >= 10 && x < 54 && y >= 2 && y < 62)
                {
                    c = 2;
                    if ((y - 2) % 8 == 7 || ((x - 10 + (((y - 2) / 8) & 1) * 8) % 16) == 15)
                        c = 3;
                    if (x == 10 || x == 53 || y == 2 || y == 61)
                        c = 1;
                }
                break;
            case 1: // rotsblok
            {
                s32 r = 24 + Sin((x * 3 + y * 5) & 0xFF, 2) + (dy > 0 ? 3 : -2);
                if (d2 < r * r)
                    c = (d2 > (r - 2) * (r - 2)) ? 1 : (dx + dy < -14 ? 5 : 4);
                break;
            }
            case 2: // bunker: koepel met schietgleuf
                if (y >= 18 && y < 58 && abs(dx) < 30 - (y < 30 ? (30 - y) : 0))
                {
                    c = y < 24 ? 7 : 6;
                    if (y >= 34 && y < 39 && abs(dx) < 15)
                        c = 14;
                    if (y == 57 || abs(dx) == 29 - (y < 30 ? (30 - y) : 0))
                        c = 1;
                }
                break;
            case 3: // maan
                if (d2 < 27 * 27)
                {
                    c = (dx > 8 && d2 > 18 * 18) ? 9 : 8;
                    if ((dx + 8) * (dx + 8) + (dy + 6) * (dy + 6) < 30 || (dx - 6) * (dx - 6) + (dy - 9) * (dy - 9) < 42
                     || (dx + 2) * (dx + 2) + (dy - 14) * (dy - 14) < 12 || (dx - 10) * (dx - 10) + (dy + 12) * (dy + 12) < 16)
                        c = 9;
                }
                break;
            case 4: // zon met stralen
                if (d2 < 20 * 20)
                    c = d2 < 12 * 12 ? 13 : 10;
                else if (d2 < 24 * 24)
                    c = 11;
                else if (d2 < 31 * 31 && (((dx + 64) / 3 + (dy + 64) / 3) % 4 == 0 || abs(dx) < 2 || abs(dy) < 2 || abs(abs(dx) - abs(dy)) < 2))
                    c = 11;
                break;
            }
            if (c)
                TI_BufPixel(buf, 8, x, y, c);
        }
    if (crack)
    {
        u32 b, j, r = 0xBEEF + n * 91;
        for (b = 0; b < 5; b++)
        {
            s32 px = 32, py = 32, ang = b * 51 + (r & 31);
            for (j = 0; j < 6; j++)
            {
                s32 i2, nx, ny;
                r = r * 1103515245 + 12345;
                ang = (ang + ((s32)((r >> 16) & 47) - 24)) & 0xFF;
                nx = px + Cos(ang, 5);
                ny = py + Sin(ang, 5);
                for (i2 = 0; i2 <= 5; i2++)
                {
                    s32 qx = px + (nx - px) * i2 / 5, qy = py + (ny - py) * i2 / 5;
                    if ((u32)qx < 64 && (u32)qy < 64)
                        TI_BufPixel(buf, 8, qx, qy, 12);
                }
                px = nx;
                py = ny;
            }
        }
    }
}

static void C2B_LoadObstacle(u32 n, bool32 crack)
{
    u8 *buf = Alloc(64 * 64 / 2);
    u16 tile = GetSpriteTileStartByTag(C2B_TAG_OBST);
    if (buf == NULL)
        return;
    C2B_DrawObstacle(buf, n, crack);
    if (tile != 0xFFFF)
        CpuCopy16(buf, (void *)(OBJ_VRAM0 + tile * TILE_SIZE_4BPP), 64 * 64 / 2);
    else
        sTI->v[1] = TI_BufSprite(buf, 64 * 64 / 2, C2B_TAG_OBST, sC2B_ObstPal, &gOamData_AffineDouble_ObjNormal_64x64, -80, BG_IMPACT_Y);
    Free(buf);
}

static void CIBGirl_Init(void)
{
    u8 chunks[5 * 32];
    u32 i, k, x, y;
    C2B_LoadObstacle(0, FALSE);
    // brokken: 5 frames (een per obstakel), elk een onregelmatig stuk in de kleuren van dat obstakel
    memset(chunks, 0, sizeof(chunks));
    for (k = 0; k < 5; k++)
        for (y = 0; y < 8; y++)
            for (x = 0; x < 8; x++)
            {
                s32 dx = (s32)x * 2 - 7, dy = (s32)y * 2 - 7;
                if (abs(dx) + abs(dy) * 3 / 2 < 10 + (s32)((x * 7 + y * 3) % 3))
                    TI_BufPixel(&chunks[k * 32], 1, x, y, (dx + dy < -2) ? sC2B_ChunkCols[k][1] : sC2B_ChunkCols[k][0]);
            }
    for (i = 0; i < 10; i++)
    {
        sTI->v[2 + i] = TI_BufSprite(chunks, sizeof(chunks), C2B_TAG_CHUNK, sC2B_ObstPal, &gOamData_AffineOff_ObjNormal_8x8, 0, -20);
        TI_Show(sTI->v[2 + i], FALSE);
    }
    for (i = 0; i < 6; i++)
        sTI->v[12 + i] = C2B_Streak();
    sTI->v[0] = TI_Trainer(GetTrainerPicFromId(sTI->trainer), 172, 82, TRUE);
    sTI->v[18] = TI_TextSprite(COMPOUND_STRING("HAIYAAAH"), 8, 4, 9, C2B_TAG_TEXT, sC2B_HaiPal, &gOamData_AffineDouble_ObjNormal_64x32, 112, 134);
    TI_Show(sTI->v[18], FALSE);
    PlaySE(SE_M_JUMP_KICK);
}

static bool32 CIBGirl_Update(s32 t)
{
    static const u16 sSE[5] = {SE_M_BRICK_BREAK, SE_M_ROCK_THROW, SE_M_EXPLOSION, SE_M_MEGA_KICK, SE_M_SELF_DESTRUCT};
    s32 b6 = TI_Beat(6), end = TI_Beat(7) + 6, i, n = -1, k;
    u8 girl = sTI->v[0], ob = sTI->v[1];
    // de Battle Girl: schuin in de trap, deint mee
    TI_Pos(girl, 172 + Sin((t * 8) & 0xFF, 2), 82 + Sin((t * 11) & 0xFF, 3));
    TI_Scale(girl, 240, 272, 0x1C00);
    // speedlines naar rechts (zij vliegt naar links)
    for (i = 0; i < 6; i++)
    {
        u8 s = sTI->v[12 + i];
        TI_Show(s, t < b6);
        TI_Scale(s, -256, 256, 0);
        TI_Pos(s, ((t * 11 + i * 53) % 290) - 30, 16 + i * 24 + (i & 1) * 9);
    }
    // obstakels: elk komt van links aan en wordt precies op tel n+1 geraakt
    for (i = 0; i < 5; i++)
    {
        s32 at = TI_Beat(i + 1);
        if (t >= at - 16 && t < at + 1)
            n = i;
        if (TI_AT(at - 16))
        {
            C2B_LoadObstacle(i, FALSE);
            TI_Show(ob, TRUE);
        }
        if (TI_AT(at))
        {
            u32 j;
            PlaySE(sSE[i]);
            sTI->v[19] = i >= 3 ? 7 : 4;
            if (i >= 3)
                C2B_LoadObstacle(i, TRUE);   // maan en zon barsten eerst
            for (j = 0; j < 10; j++)
            {
                u8 c = sTI->v[2 + j];
                TI_Part(c, sC2B_ImpactX[i] + TI_RandRange(-10, 18), BG_IMPACT_Y + TI_RandRange(-20, 20),
                        -TI_RandRange(16, 56), -TI_RandRange(0, 44), 3, 34);
                gSprites[c].oam.tileNum = GetSpriteTileStartByTag(C2B_TAG_CHUNK) + i;
            }
        }
        if (t == at + (i >= 3 ? 6 : 1) || (sTI->last < at + (i >= 3 ? 6 : 1) && t >= at + (i >= 3 ? 6 : 1) && t < at + 8))
            TI_Show(ob, FALSE);
    }
    if (n >= 0)
    {
        s32 at = TI_Beat(n + 1);
        k = TI_Ramp(t, at - 16, at);
        TI_Pos(ob, -40 + ((sC2B_ImpactX[n] + 40) * k >> 8), BG_IMPACT_Y + (n == 3 ? -10 : n == 4 ? -14 : 0));
        if (n == 4)
            TI_Scale(ob, 192, 192, (t * 64) & 0xFFFF);
        else if (n == 3)
            TI_Scale(ob, 240, 240, 0);
        else
            TI_Scale(ob, 256, 256, 0);
        if (t >= at)   // na de klap even stilstaan op het raakpunt
            TI_Pos(ob, sC2B_ImpactX[n] + TI_RandRange(-2, 2), gSprites[ob].y);
    }
    // lucht: na de bunker de ruimte in (nacht voor de maan, gloed voor de zon)
    k = TI_Ramp(t, TI_Beat(3) + 2, TI_Beat(4) - 8) * 13 >> 8;
    if (t < TI_Beat(5) - 10)
        TI_Tint(TI_World(), k, RGB(2, 2, 8));
    else
        TI_Tint(TI_World(), 13 - (TI_Ramp(t, TI_Beat(5) - 10, TI_Beat(5)) * 4 >> 8), Tapu_Blend(RGB(2, 2, 8), RGB(31, 20, 6), TI_Ramp(t, TI_Beat(5) - 10, TI_Beat(5)) >> 4));
    for (i = 1; i <= 5; i++)
        TI_Flash(t, TI_Beat(i), i == 5 ? 14 : 6, i == 5 ? 16 : 10, PALETTES_ALL, RGB_WHITE);
    // HAIYAAAH
    if (TI_AT(b6))
    {
        PlaySE(SE_M_SKY_UPPERCUT);
        TI_Show(sTI->v[18], TRUE);
        sTI->v[19] = 6;
    }
    if (t >= b6)
    {
        k = TI_Ramp(t, b6, b6 + 5);
        TI_Scale(sTI->v[18], 384 - k, 384 - k, 0);
        if (t >= b6 + 2)
            TI_Tint(TI_World(), 6, RGB(31, 24, 8));
    }
    if (sTI->v[19] > 0)
        sTI->v[19]--;
    TI_Shake(sTI->v[19]);
    return t >= end;
}

static const struct TIntro sCI_BGirl = {CIBGirl_Init, CIBGirl_Update};

#pragma GCC pop_options
