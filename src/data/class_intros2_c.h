// Project Grounded: trainerklasse-intro's v2 (Jordi), deel c: Bug Catcher/Bug Maniac, Pokéfan, Aroma Lady, Parasol Lady.
// Wordt in src/data/class_intros.h ingevoegd (vóór sClassIntros); gebruikt de TI_*-runner daarvan.
//
//   Bug Catcher, Bug Maniac   een net zwiept twee keer en vangt bijen; een mug zoemt binnen; KLAP. "ehh… busted?"
//   Pokéfan                   plushies verschijnen één voor één, de fan staart met glinsterogen. "……"
//   Aroma Lady                een kruidentuin groeit op de tel, een zwerm bijen verknalt de oogst
//   Parasol Lady              regen, hagel, hittegolf, zandstorm: de parasol blokt alles. "Lovely weather."

#include "pokemon_icon.h"            // (staat niet bovenaan battle_transition.c)
#include "constants/pokemon_icon.h"

#define CIC_TAG_NET   0x7C31
#define CIC_TAG_MOSQ  0x7C32
#define CIC_TAG_ITEM1 0x7C33
#define CIC_TAG_ITEM2 0x7C34

static const u16 sCIc_TextPal[4] = {0, RGB(31, 31, 31), RGB(3, 3, 5), RGB(22, 2, 3)};

// zoom 256 = normaal, 512 = 2x (max. voor een dubbele affine-box)
static void CIc_Zoom(u8 id, s32 zoom, u16 rot)
{
    if (id < MAX_SPRITES && gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, max(16, zoom), max(16, zoom), rot);
}

// een gewone 32x32-sprite (item-icoon, mon-icoon) affine maken
static void CIc_Affine(u8 id)
{
    if (id >= MAX_SPRITES)
        return;
    gSprites[id].oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    gSprites[id].oam.matrixNum = AllocOamMatrix();
    gSprites[id].affineAnimPaused = TRUE;   // mon-iconen hebben eigen affine-animaties
    CalcCenterToCornerVec(&gSprites[id], SPRITE_SHAPE(32x32), SPRITE_SIZE(32x32), ST_OAM_AFFINE_DOUBLE);
    SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, 256, 256, 0);
}

// opploppen: 0 -> 1,25x -> 1x in 10 frames (zoom * base / 256)
static s32 CIc_Pop(s32 t, s32 at, s32 base)
{
    s32 d = t - at;
    if (d < 0)
        return 16;
    if (d < 6)
        return (60 + d * 52) * base / 256;
    if (d < 10)
        return (320 - (d - 6) * 16) * base / 256;
    return base;
}

static void CIc_SetFrame(u8 id, u16 tag, u32 ofs)
{
    if (id < MAX_SPRITES)
        gSprites[id].oam.tileNum = GetSpriteTileStartByTag(tag) + ofs;
}

static u8 CIc_Pic(s16 x, s16 y, bool32 affine)
{
    return TI_Trainer(GetTrainerPicFromId(sTI->trainer), x, y, affine);
}

// ---------------- Bug Catcher/Bug Maniac
#define BS_BEES 5
static const u16 sCIc_NetPal[4] = {0, RGB(28, 25, 16), RGB(17, 10, 4), RGB(7, 5, 3)};
static const u16 sCIc_MosqPal[4] = {0, RGB(4, 3, 3), RGB(26, 29, 31), RGB(26, 4, 4)};
// bijen: hoek (256-stappen) en straal op de boog van de zwaai (draaipunt 120,230)
static const u8 sCIc_BeeA[BS_BEES] = {100, 72, 46, 34, 60};
static const u8 sCIc_BeeR[BS_BEES] = {160, 160, 160, 112, 112};
// mug, 16x16, kop links: 5 rijen vleugels per frame + 9 rijen lijf
static const char sCIc_MosqWings[2][5][17] = {
    {".......2...22...", "......22..222...", "......22.222....", ".......2222.....", "........22......"},
    {"................", "................", ".......222222...", "......22222222..", "........2222...."},
};
static const char sCIc_MosqBody[9][17] = {
    "....1.1111......",
    "...111111111....",
    "111.111133311...",
    ".....1.1.11111.1",
    "....1..1..1.....",
    "...1...1...1....",
    "..1....1....1...",
    "..1.....1....1..",
    ".1......1.....1.",
};

static void CIBugSwat_Init(void)
{
    u8 *buf;
    s32 x, y, i, f;
    TI_SetPal(15, sCIc_TextPal, 4);
    for (i = 0; i < BS_BEES; i++)
        sTI->v[i] = TI_Anim(ANIM_TAG_ATTACK_ORDER, &gOamData_AffineOff_ObjNormal_16x16, -30, -30, 0);
    // het net: hoepel met gaas (midden 32,14, straal 12) en een steel naar beneden
    buf = AllocZeroed(64 * 64 / 2);
    if (buf != NULL)
    {
        for (y = 0; y < 64; y++)
            for (x = 0; x < 64; x++)
            {
                s32 dx = x - 32, dy = y - 14, d = dx * dx + dy * dy;
                if (d <= 13 * 13 && d >= 11 * 11)
                    TI_BufPixel(buf, 8, x, y, 2);
                else if (d < 11 * 11 && (((x + y) & 3) == 0 || ((x - y) & 3) == 0))
                    TI_BufPixel(buf, 8, x, y, 1);
                else if (y > 26 && y < 63 && x >= 31 && x <= 33)
                    TI_BufPixel(buf, 8, x, y, x == 33 ? 3 : 2);
            }
        sTI->v[5] = TI_BufSprite(buf, 64 * 64 / 2, CIC_TAG_NET, sCIc_NetPal, &gOamData_AffineDouble_ObjNormal_64x64, -80, -80);
        Free(buf);
    }
    // de mug (2 frames)
    buf = AllocZeroed(2 * 4 * 32);
    if (buf != NULL)
    {
        for (f = 0; f < 2; f++)
            for (y = 0; y < 14; y++)
                for (x = 0; x < 16; x++)
                {
                    char c = y < 5 ? sCIc_MosqWings[f][y][x] : sCIc_MosqBody[y - 5][x];
                    if (c != '.')
                        TI_BufPixel(buf + f * 4 * 32, 2, x, y + 1, c - '0');
                }
        sTI->v[6] = TI_BufSprite(buf, 2 * 4 * 32, CIC_TAG_MOSQ, sCIc_MosqPal, &gOamData_AffineDouble_ObjNormal_16x16, -30, -30);
        CIc_Zoom(sTI->v[6], 512, 0);
        Free(buf);
    }
    sTI->v[7] = TI_Anim(ANIM_TAG_HANDS_AND_FEET, &gOamData_AffineDouble_ObjNormal_32x32, -60, -60, 3 * 16);
    TI_Show(sTI->v[6], FALSE);
    TI_Show(sTI->v[7], FALSE);
    sTI->v[8] = 0;
    PlaySE(SE_M_STRING_SHOT);
}

static bool32 CIBugSwat_Update(s32 t)
{
    s32 b1 = TI_Beat(1), b2 = TI_Beat(2), b3 = TI_Beat(3), b4 = TI_Beat(4), end = TI_Beat(6) + 6;
    s32 a, r, i, hx, hy, mx, my, k;
    u8 net = sTI->v[5];

    // het net: eerst links buiten beeld, zwaai 1 naar rechts (grote boog), zwaai 2 terug (kleine boog), dan hangt het
    if (t < b2 - 8)
    {
        k = TI_Ramp(t, b1 - 10, b1 + 4);
        a = 120 - (k * 106 >> 8);
        r = 160;
    }
    else
    {
        k = TI_Ramp(t, b2 - 10, b2 + 4);
        a = 14 + (k * 66 >> 8);
        r = 112;
    }
    if (t >= b2 + 4)
        a += Sin((t * 4) & 0xFF, 3);
    hx = 120 + Cos(a & 0xFF, r);
    hy = 230 - Sin(a & 0xFF, r);
    TI_Pos(net, 120 + Cos(a & 0xFF, r - 18), 230 - Sin(a & 0xFF, r - 18));
    TI_Scale(net, 256, 256, ((a - 64) << 8) & 0xFFFF);
    if (TI_AT(b1 - 10) || TI_AT(b2 - 10))
        PlaySE(SE_M_CUT);

    // bijen: fladderen op de boog tot het net langskomt, daarna zitten ze in het net
    for (i = 0; i < BS_BEES; i++)
    {
        u8 bee = sTI->v[i];
        s32 bx, by;
        if (sTI->v[8] & (1 << i))
        {
            bx = hx + Sin((t * 9 + i * 50) & 0xFF, 5);
            by = hy + Cos((t * 7 + i * 80) & 0xFF, 4);
        }
        else
        {
            bx = 120 + Cos(sCIc_BeeA[i], sCIc_BeeR[i]) + Sin((t * 6 + i * 40) & 0xFF, 10);
            by = 230 - Sin(sCIc_BeeA[i], sCIc_BeeR[i]) + Sin((t * 11 + i * 70) & 0xFF, 6);
            // gevangen zodra de hoepel hun hoek op hun boog voorbij is (per frame gaat het net te hard voor een afstandstest)
            if (sCIc_BeeR[i] == r && (r == 160 ? (t >= b1 - 10 && a <= sCIc_BeeA[i]) : (t >= b2 - 10 && a >= sCIc_BeeA[i])))
            {
                sTI->v[8] |= 1 << i;
                PlaySE(SE_BALL_TRADE);
            }
        }
        TI_Pos(bee, bx, by);
        CIc_SetFrame(bee, ANIM_TAG_ATTACK_ORDER, ((t >> 1) & 1) * 8);
    }

    // de mug zoemt van rechts binnen en blijft hangen
    mx = 150 + Sin((t * 5) & 0xFF, 6);
    my = 52 + Sin((t * 13) & 0xFF, 5);
    if (t < b4 - 4)
    {
        k = TI_Ramp(t, b3, b4 - 4);
        mx += (256 - k) * 120 >> 8;
        my += Sin((k * 3) & 0xFF, 22 * (256 - k) >> 8);
    }
    TI_Pos(sTI->v[6], mx, my);
    CIc_SetFrame(sTI->v[6], CIC_TAG_MOSQ, (t & 1) * 4);
    TI_Show(sTI->v[6], t >= b3 && t < b4);
    if (TI_AT(b3) || TI_AT(b3 + 12))
        PlaySE(SE_M_SCREECH);

    // KLAP: de hand komt op je af, flits, schudden, een vlekje blijft over
    if (t >= b4 - 3 && t < b4 + 12)
    {
        TI_Show(sTI->v[7], TRUE);
        TI_Pos(sTI->v[7], 150, 56);
        CIc_Zoom(sTI->v[7], t < b4 ? 300 + (t - b4 + 3) * 70 : 512, 0);
    }
    else
    {
        TI_Show(sTI->v[7], FALSE);
    }
    if (TI_AT(b4))
    {
        PlaySE(SE_M_DOUBLE_SLAP);
        TI_Stamp(150, 56, 6, 2);
        TI_Stamp(152, 57, 3, 3);
        TI_Line(150, 56, 134, 46, 0, 256, 0, 2);
        TI_Line(150, 56, 166, 44, 0, 256, 0, 2);
        TI_Line(150, 56, 132, 66, 0, 256, 0, 2);
        TI_Line(150, 56, 168, 68, 0, 256, 0, 2);
        TI_Line(150, 56, 144, 74, 0, 256, 0, 2);
        TI_Stamp(163, 51, 1, 3);
        TI_Plot(138, 59, 3);
        TI_Plot(158, 66, 3);
    }
    TI_Shake(t >= b4 && t < b4 + 8 ? 4 - (t - b4) / 2 : 0);
    if (TI_AT(TI_Beat(5)))
        TI_TextBg(COMPOUND_STRING("ehh… busted?"), 13, 10, 12, 2, -1, 0, 0, 1, 2, FONT_NORMAL, 15);
    TI_Tint(TI_World(), TI_Ramp(t, 0, b2) * 4 >> 8, RGB(6, 14, 4));
    TI_Flash(t, b4, 6, 16, PALETTES_ALL & ~(1 << 15), RGB_WHITE);
    return t >= end;
}

static const struct TIntro sCI_BugSwat = {CIBugSwat_Init, CIBugSwat_Update};

// ---------------- Pokéfan: plushies verschijnen één voor één, de fan staart met glinsterende ogen. "……"
#define PF_HEARTS 4
// CreateMonIcon laat images naar een lokale variabele wijzen; dit maakt DestroySprite (TI_Free) veilig
static const struct SpriteFrameImage sCIc_IconImage = {NULL, 0x200};

static void CIFan_Init(void)
{
    u32 i;
    u16 pic = GetTrainerPicFromId(sTI->trainer);
    u8 id;
    TI_SetPal(15, sCIc_TextPal, 4);
    sTI->v[0] = TI_Anim(ANIM_TAG_MONSTER_DOLL, &gOamData_AffineDouble_ObjNormal_32x32, 46, 58, 0);
    sTI->v[1] = TI_Item(CIC_TAG_ITEM1, ITEM_POKE_DOLL, 94, 40);
    CIc_Affine(sTI->v[1]);
    sTI->v[2] = TI_Item(CIC_TAG_ITEM2, ITEM_FLUFFY_TAIL, 146, 40);
    CIc_Affine(sTI->v[2]);
    LoadMonIconPalette(SPECIES_WAILORD);
    id = CreateMonIcon(SPECIES_WAILORD, SpriteCallbackDummy, 194, 58, 1, 0);   // een knuffel beweegt niet
    if (id < MAX_SPRITES)
    {
        gSprites[id].images = &sCIc_IconImage;
        TI_AddTag(POKE_ICON_BASE_PAL_TAG + gSpeciesInfo[SPECIES_WAILORD].iconPalIndex);
        CIc_Affine(id);
        TI_Track(id, TIK_SPRITE);
    }
    sTI->v[3] = id;
    for (i = 0; i < 4; i++)
        TI_Show(sTI->v[i], FALSE);
    sTI->v[4] = TI_Anim(ANIM_TAG_EYE_SPARKLE, &gOamData_AffineDouble_ObjNormal_16x16, -20, -20, 0);
    sTI->v[5] = TI_Anim(ANIM_TAG_EYE_SPARKLE, &gOamData_AffineDouble_ObjNormal_16x16, -20, -20, 0);
    sTI->v[6] = TI_Anim(ANIM_TAG_EYE_SPARKLE, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
    for (i = 0; i < PF_HEARTS; i++)
    {
        sTI->v[8 + i] = TI_Anim(ANIM_TAG_RED_HEART, &gOamData_AffineOff_ObjNormal_16x16, -20, -20, 0);
        TI_Show(sTI->v[8 + i], FALSE);
    }
    sTI->v[7] = CIc_Pic(120, 124, FALSE);
    // ogen in de trainerfoto (64x64, linksboven = 88,92)
    if (pic == TRAINER_PIC_POKEFAN_M)
        sTI->v[12] = 88 + 36, sTI->v[13] = 92 + 24, sTI->v[14] = 7;
    else if (pic == TRAINER_PIC_POKEFAN_F)
        sTI->v[12] = 88 + 26, sTI->v[13] = 92 + 16, sTI->v[14] = 7;
    else
        sTI->v[12] = 88 + 28, sTI->v[13] = 92 + 18, sTI->v[14] = 8;
    TI_Show(sTI->v[4], FALSE);
    TI_Show(sTI->v[5], FALSE);
    TI_Show(sTI->v[6], FALSE);
}

static bool32 CIFan_Update(s32 t)
{
    s32 b4 = TI_Beat(4), end = TI_Beat(5) + 10, i, hop = 0, last = -1;
    static const s16 sTwinkle[4][2] = {{-14, -14}, {14, -16}, {16, 12}, {-16, 10}};
    for (i = 0; i < 4; i++)
    {
        s32 at = i == 0 ? TI_Beat2(1) : TI_Beat(i);
        u8 id = sTI->v[i];
        if (t >= at)
        {
            TI_Show(id, TRUE);
            CIc_Zoom(id, CIc_Pop(t, at, i == 3 ? 512 : 256), (Sin((t * 4 + i * 64) & 0xFF, 6) << 8) & 0xFFFF);
            last = i;
            if (t < at + 6)
                hop = -3;
        }
        if (TI_AT(at))
            PlaySE(i == 3 ? SE_M_ENCORE : SE_SHINY);
    }
    // een glinster bij de nieuwste plushie
    if (last >= 0)
    {
        u8 tw = sTI->v[6], id = sTI->v[last];
        s32 n = (t >> 2) & 3;
        TI_Show(tw, TRUE);
        TI_Pos(tw, gSprites[id].x + sTwinkle[n][0] * (last == 3 ? 2 : 1), gSprites[id].y + sTwinkle[n][1] * (last == 3 ? 2 : 1));
        CIc_SetFrame(tw, ANIM_TAG_EYE_SPARKLE, ((t >> 1) % 3) * 4);   // 3 frames
    }
    TI_Pos(sTI->v[7], 120, 124 + hop);
    // glinsterogen en hartjes
    if (t >= b4)
    {
        for (i = 0; i < 2; i++)
        {
            u8 e = sTI->v[4 + i];
            TI_Show(e, TRUE);
            TI_Pos(e, sTI->v[12] + (i ? sTI->v[14] : 0), sTI->v[13]);
            CIc_SetFrame(e, ANIM_TAG_EYE_SPARKLE, ((((t - b4) >> 2) + i) % 3) * 4);
            CIc_Zoom(e, 448, ((t * 6) << 8) & 0xFFFF);
        }
        TI_Show(sTI->v[6], FALSE);
    }
    if (TI_AT(b4))
    {
        PlaySE(SE_M_ATTRACT);
        for (i = 0; i < PF_HEARTS; i++)
            TI_Part(sTI->v[8 + i], sTI->v[12] + 4, sTI->v[13] - 8, (i * 2 - 3) * 10, -24, 1, 30);
        TI_TextBg(COMPOUND_STRING("……"), 18, 12, 6, 2, -1, 0, 0, 1, 2, FONT_NORMAL, 15);
    }
    TI_Tint(TI_World(), TI_Ramp(t, 0, TI_Beat(1)) * 10 >> 8, RGB(5, 2, 9));
    TI_Flash(t, b4, 6, 10, PALETTES_ALL & ~(1 << 15), RGB(31, 24, 28));
    return t >= end;
}

static const struct TIntro sCI_Fan = {CIFan_Init, CIFan_Update};

// ---------------- Aroma Lady: een kruidentuin groeit op de tel; een zwerm bijen verknalt de oogst
#define AR_PLANTS 6
#define AR_BEES   10
static const s16 sCIc_PlantPos[AR_PLANTS][2] = {{30, 120}, {68, 136}, {104, 144}, {140, 144}, {176, 136}, {212, 120}};

static void CIAroma_Init(void)
{
    u32 i;
    TI_SetPal(15, sCIc_TextPal, 4);
    sTI->v[20] = CIc_Pic(120, 78, FALSE);
    for (i = 0; i < AR_PLANTS; i++)
    {
        sTI->v[i] = TI_Anim(ANIM_TAG_SPROUT, &gOamData_AffineOff_ObjNormal_32x32, sCIc_PlantPos[i][0], sCIc_PlantPos[i][1], 0);
        sTI->v[6 + i] = TI_Anim(ANIM_TAG_FLOWER, &gOamData_AffineDouble_ObjNormal_16x16, -20, -20, 0);
        TI_Show(sTI->v[i], FALSE);
        TI_Show(sTI->v[6 + i], FALSE);
    }
    for (i = 0; i < AR_BEES; i++)
        sTI->extra[i] = TI_Anim(ANIM_TAG_ATTACK_ORDER, &gOamData_AffineOff_ObjNormal_16x16, -30, -30, 0);
    sTI->v[21] = 0;
    PlaySE(SE_M_SWEET_SCENT);
}

static bool32 CIAroma_Update(s32 t)
{
    s32 b3 = TI_Beat(3), b4 = TI_Beat(4), b5 = TI_Beat(5) + 6, end = TI_Beat(6) + 8, i, front = -999;
    // de zwerm: van links naar rechts over de tuin
    for (i = 0; i < AR_BEES; i++)
    {
        u8 bee = sTI->extra[i];
        s32 x = -24 + (t - b4) * 10 - (i % 5) * 14 - (i / 5) * 6, y = 118 + (i / 5) * 22 + Sin((t * 12 + i * 37) & 0xFF, 8);
        TI_Show(bee, t >= b4 && x < 260);
        TI_Pos(bee, x, y);
        CIc_SetFrame(bee, ANIM_TAG_ATTACK_ORDER, ((t >> 1) & 1) * 8);
        if (t >= b4 && x > front)
            front = x;
    }
    if (TI_AT(b4) || TI_AT(b4 + 14))
        PlaySE(SE_M_SCREECH);
    for (i = 0; i < AR_PLANTS; i++)
    {
        u8 sp = sTI->v[i], fl = sTI->v[6 + i];
        s32 at = TI_Beat2(i), x = sCIc_PlantPos[i][0], y = sCIc_PlantPos[i][1], f;
        bool32 eaten = (sTI->v[21] >> i) & 1;
        if (!eaten && front > x)
        {
            // opgevreten: de bloem valt, de plant zakt in
            sTI->v[21] |= 1 << i;
            eaten = TRUE;
            TI_Part(fl, x, y - 14, TI_RandRange(-8, 8), -10, 2, 20);
            PlaySE(SE_M_SCRATCH);
        }
        TI_Show(sp, t >= at);
        f = min(6, max(0, (t - at) * 7 / max(1, TI_Beat(1))));
        if (eaten)
            f = 1;
        CIc_SetFrame(sp, ANIM_TAG_SPROUT, f * 16);
        if (t >= b3 && !eaten)
        {
            TI_Show(fl, TRUE);
            TI_Pos(fl, x, y - 14);
            CIc_Zoom(fl, CIc_Pop(t, b3 + i, 256), 0);
        }
        if (TI_AT(at) && (i & 1) == 0)
            PlaySE(SE_M_GIGA_DRAIN);
    }
    if (TI_AT(b3))
        PlaySE(SE_SHINY);
    // de oogst wordt bruin; de wereld eerst groen en fris
    if (t >= b4)
    {
        s32 k = TI_Ramp(t, b4, b5 - 6) * 11 >> 8;
        TI_TintMore(TI_PalBit(sTI->v[0]) | TI_PalBit(sTI->v[6]), k, RGB(14, 9, 3));
    }
    TI_Tint(TI_World(), t < b4 ? TI_Ramp(t, 0, b3) * 5 >> 8 : 5 - (TI_Ramp(t, b4, b5) * 5 >> 8), RGB(10, 28, 8));
    // haar reactie: grauw, zakt een paar pixels
    if (t >= b5)
    {
        TI_TintMore(TI_PalBit(sTI->v[20]), TI_Ramp(t, b5, b5 + 8) * 7 >> 8, RGB(8, 10, 16));
        TI_Pos(sTI->v[20], 120 + (t < b5 + 8 ? ((t & 2) ? 2 : -2) : 0), 78 + min(3, (t - b5) / 3));
    }
    if (TI_AT(b5))
    {
        PlaySE(SE_FAINT);
        TI_TextBg(COMPOUND_STRING("…organic, they said."), 6, 1, 18, 2, -1, 0, 0, 1, 2, FONT_NORMAL, 15);
    }
    return t >= end;
}

static const struct TIntro sCI_Aroma = {CIAroma_Init, CIAroma_Update};

// ---------------- Parasol Lady: regen, hagel, hittegolf, zandstorm; de parasol blokt alles, zij leunt alleen wat mee
#define PS_PER 8
#define CIC_TAG_SUN 0x7C35
struct CIcWeather
{
    u16 tag, se;
    const struct OamData *oam;
    u8 ofs, from, speed;   // eerste tile, richting waar het vandaan komt (256-stappen, 0 = rechts, 64 = boven), frames tot de parasol
    s8 tilt;               // hoe ver ze de parasol erheen draait
    const u8 *label;
};

static const struct CIcWeather sCIc_Weather[4] = {
    {ANIM_TAG_RAIN_DROPS, SE_M_RAIN_DANCE, &gOamData_AffineOff_ObjNormal_16x32, 16, 84, 11, 0, COMPOUND_STRING("RAIN")},
    {ANIM_TAG_HAIL, SE_M_HAIL, &gOamData_AffineOff_ObjNormal_16x16, 0, 64, 13, -22, COMPOUND_STRING("HAIL")},
    {ANIM_TAG_SMALL_EMBER, SE_M_HEAT_WAVE, &gOamData_AffineOff_ObjNormal_32x32, 0, 100, 15, 10, COMPOUND_STRING("HEATWAVE")},
    {ANIM_TAG_FLYING_DIRT, SE_M_SANDSTORM, &gOamData_AffineOff_ObjNormal_32x32, 0, 128, 10, 26, COMPOUND_STRING("SANDSTORM")},
};
static const u16 sCIc_SunPal[4] = {0, RGB(31, 30, 12), RGB(31, 20, 2), RGB(31, 31, 26)};

// 32 deeltjes: v[0..23] en extra[8..15]
static u8 CIc_PSpr(u32 k)
{
    return k < 24 ? sTI->v[k] : sTI->extra[8 + k - 24];
}

static void CIParasol_Init(void)
{
    u32 w, i, x, y;
    u8 *buf;
    TI_SetPal(15, sCIc_TextPal, 4);
    for (w = 0; w < 4; w++)
        for (i = 0; i < PS_PER; i++)
        {
            u32 k = w * PS_PER + i;
            u8 id = TI_Anim(sCIc_Weather[w].tag, sCIc_Weather[w].oam, -40, -40, sCIc_Weather[w].ofs);
            if (k < 24)
                sTI->v[k] = id;
            else
                sTI->extra[8 + k - 24] = id;
            TI_Show(id, FALSE);
        }
    // de zon: een schijf met acht stralen (32x32, 2x)
    buf = AllocZeroed(16 * 32);
    sTI->extra[1] = MAX_SPRITES;
    if (buf != NULL)
    {
        for (y = 0; y < 32; y++)
            for (x = 0; x < 32; x++)
            {
                s32 dx = (s32)x - 16, dy = (s32)y - 16, d = dx * dx + dy * dy;
                if (d <= 49)
                    TI_BufPixel(buf, 4, x, y, d <= 16 ? 3 : 1);
                else if (d <= 225 && d > 81 && (dx == 0 || dy == 0 || dx == dy || dx == -dy))
                    TI_BufPixel(buf, 4, x, y, 2);
            }
        sTI->extra[1] = TI_BufSprite(buf, 16 * 32, CIC_TAG_SUN, sCIc_SunPal, &gOamData_AffineDouble_ObjNormal_32x32, 50, 56);
        Free(buf);
        TI_Show(sTI->extra[1], FALSE);
    }
    sTI->extra[0] = CIc_Pic(120, 96, TRUE);
    TI_Lines(TIF_WX);
}

static bool32 CIParasol_Update(s32 t)
{
    s32 end = TI_Beat(6), w, i, k, tilt = 0, prev = 0, px, py, c, s, y;
    u8 lady = sTI->extra[0];
    // kanteling: op de tel naar de volgende bui
    for (w = 0; w < 4; w++)
    {
        s32 at = TI_Beat(w);
        if (t >= at - 6)
        {
            k = TI_Ramp(t, at - 6, at);
            tilt = prev + ((sCIc_Weather[w].tilt - prev) * k >> 8);
        }
        prev = sCIc_Weather[w].tilt;
    }
    if (t >= TI_Beat(4) + 4)
        tilt = sCIc_Weather[3].tilt - (sCIc_Weather[3].tilt * TI_Ramp(t, TI_Beat(4) + 4, TI_Beat(5)) >> 8);
    CIc_Zoom(lady, 512, (tilt << 8) & 0xFFFF);
    // de parasol (in de foto rond 21,22 = 11 links en 10 boven het midden), 2x, meegedraaid
    c = Cos(tilt & 0xFF, 256);
    s = Sin(tilt & 0xFF, 256);
    px = 120 + ((-22 * c - 20 * s) >> 8);
    py = 96 + ((22 * s - 20 * c) >> 8);

    for (w = 0; w < 4; w++)
    {
        const struct CIcWeather *wd = &sCIc_Weather[w];
        s32 at = TI_Beat(w);
        if (TI_AT(at))
        {
            PlaySE(wd->se);
            TI_TextBg(wd->label, 1, 1, 10, 2, 0, 0, 0, 1, 2, FONT_NORMAL, 15);
        }
        for (i = 0; i < PS_PER; i++)
        {
            if (TI_AT(at + i * 2))
            {
                // bron: 110 px van de parasol in de windrichting, gespreid; doel: de parasol
                s32 spread = TI_RandRange(-60, 60), aim = TI_RandRange(-14, 14);
                s32 dx = Cos(wd->from, 256), dy = -Sin(wd->from, 256);
                s32 sx = px + (dx * 110 >> 8) + (-dy * spread >> 8), sy = py + (dy * 110 >> 8) + (dx * spread >> 8);
                s32 tx = px + (-dy * aim >> 8), ty = py + (dx * aim >> 8);
                u8 id = CIc_PSpr(w * PS_PER + i);
                TI_Part(id, sx, sy, (tx - sx) * 16 / wd->speed, (ty - sy) * 16 / wd->speed, 0, 40);
                CIc_SetFrame(id, wd->tag, wd->ofs);
            }
        }
    }
    // botsen tegen de parasol: terugkaatsen (regen spat uiteen)
    for (i = 0; i < TI_MAX_PART; i++)
    {
        struct TIPart *p = &sTI->part[i];
        s32 nx, ny, dot, d2;
        if (!p->on || p->ay != 0)
            continue;
        nx = (p->x >> 4) - px;
        ny = (p->y >> 4) - py;
        d2 = nx * nx + ny * ny;
        dot = p->vx * nx + p->vy * ny;
        if (d2 < 30 * 30 && dot < 0)
        {
            for (k = 0; k < PS_PER; k++)
                if (p->slot == CIc_PSpr(k))
                    break;
            if (k < PS_PER)
            {
                p->vx = p->vy = 0;   // spat uiteen; met snelheid 0 botst hij niet nog eens
                p->life = 8;
                CIc_SetFrame(p->slot, ANIM_TAG_RAIN_DROPS, 5 * 8);
                continue;
            }
            p->vx = (p->vx - 2 * dot * nx / max(1, d2)) / 2;
            p->vy = (p->vy - 2 * dot * ny / max(1, d2)) / 2;
            p->life = 14;
            p->ay = 1;   // markering: al gebotst (en een beetje zwaartekracht)
        }
    }
    // hittegolf: zon, oranje en trillend; zandstorm: geel-bruin
    k = t >= TI_Beat(2) - 4 && t < TI_Beat(3) + 4;
    TI_Show(sTI->extra[1], k);
    CIc_Zoom(sTI->extra[1], 400 + Sin((t * 16) & 0xFF, 40), (t * 300) & 0xFFFF);
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        sTI->back[TIB_WX][y] = sTI->camX + (k ? Sin((y * 8 + t * 10) & 0xFF, 2) : 0);
    if (k)
        TI_Tint(TI_World(), 7, RGB(31, 16, 4));
    else if (t >= TI_Beat(3) && t < TI_Beat(4) + 8)
        TI_Tint(TI_World(), 8, RGB(26, 20, 9));
    else
        TI_Tint(TI_World(), t >= TI_Beat(0) && t < TI_Beat(2) ? 6 : 0, RGB(6, 9, 16));
    if (TI_AT(TI_Beat(5)))
    {
        PlaySE(SE_M_HEAL_BELL);
        TI_TextBg(COMPOUND_STRING("Lovely weather."), 1, 1, 13, 2, 0, 0, 0, 1, 2, FONT_NORMAL, 15);
    }
    return t >= end;
}

static const struct TIntro sCI_Parasol = {CIParasol_Init, CIParasol_Update};
