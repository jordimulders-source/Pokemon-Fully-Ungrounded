// Project Grounded: gevechtsintro van de Shy Guys (Shy Squad op Yoshi's Island, de Stadium-Shy Guys, de Shy Guy in de
// woestijn), op de maat van Sunset Wilds (MUS_GROUNDED_VS_SUNSET_WILDS, 130 bpm: 27,7 frames per tel; de melodie valt
// in op tel 8). Jordi: "lekker droog diverse soorten shy guys uit Yoshi's Island die op een level staan, vervolgens
// draait er 1 om van oh shit het is mijn beurt om te vechten".
// Het begin van level 1-1. Zeven Shy Guys staan in een rij en kijken allemaal naar links (waar Yoshi vandaan komt):
// een Stilt Guy, een Fat Guy, een Spear Guy, de rode, een struik, een gele en een Fly Guy. Ze stappen droog op de maat
// mee. Tel 3: alles staat stil (de muziek niet). Tel 4: de rode draait zich om naar de camera, springt op, '!' (het
// Pokémon-uitroepteken). Tel 5: de rest draait zich langzaam naar hem toe (de Stilt Guy helemaal rond), de struik
// komt kijken. Tel 6: close-up, de rest valt in het donker, hij trilt. Tel 7: een hint-bord: "Wait. / It's my turn."
// Tel 8 (de melodie): wit, gevecht.
// Jordi: "kan je die net iets aanpassen voor de andere shy guys? Dat de juiste dan zegt wait it's my turn." Wie zich
// omdraait, het '!' krijgt en in de close-up staat, is de Shy Guy tegen wie je echt vecht (SG_GetVariant): een rode,
// groene, roze of zwarte (kleur van zijn trainerfoto; omgekleurde paletten van dezelfde frames), of de Fly Guy / Spear
// Guy (die ruilen dan van plek met de rode). De rij houdt zeven Shy Guys; de timing is voor alle varianten gelijk.
// Alles hangt aan de echte VBlanks sinds de start van de transitie (Tapu_Elapsed), niet aan taakframes.
// Wordt na src/data/wario_intro.h ingevoegd (GI_/LI_/LI2_-hulpjes). Art: tools/grounded/shyguy_intro.py (het level
// en het bord uit de ROM via tools/grounded/yi_shyguy_rip.py, de Shy Guys van het SMA3-spriteblad).
#include "shyguy_intro_gen.h"

static const u32 sShyGuyIntro_Tiles[] = INCBIN_U32("graphics/battle_transitions/shyguy_intro.4bpp.smol");
static const u32 sShyGuyIntro_Maps[] = INCBIN_U32("graphics/battle_transitions/shyguy_intro_maps.bin.smol");
static const u16 sShyGuyIntro_Pal[] = INCBIN_U16("graphics/battle_transitions/shyguy_intro.gbapal");
static const u32 sShyGuyS32_Gfx[] = INCBIN_U32("graphics/battle_transitions/shyguy_s32.4bpp.smol");
static const u32 sShyGuyS64_Gfx[] = INCBIN_U32("graphics/battle_transitions/shyguy_s64.4bpp.smol");
static const u32 sShyGuyBig_Gfx[] = INCBIN_U32("graphics/battle_transitions/shyguy_big.4bpp.smol");
static const u16 sShyGuyObj_Pal[] = INCBIN_U16("graphics/battle_transitions/shyguy_obj.gbapal");

enum { SG_MAP_LEVEL, SG_MAP_BOARD };
enum { SG_STILT, SG_FAT, SG_SPEAR, SG_RED, SG_BUSH, SG_YELLOW, SG_FLY, SG_EXCL, SG_BIG, SG_COUNT };
enum { SG_SH32, SG_SH64, SG_SHBIG };

#define SG_TAG_S32      0x5A90
#define SG_TAG_S64      0x5A91
#define SG_TAG_BIG      0x5A92
#define SG_TAG_PAL      0x5A93   // t/m 0x5A93 + SG_NUM_PALS
#define SG_PAL_CHOSEN   SG_NUM_PALS  // extra palet: de gekozen kleine figuur, omgekleurd (sSG_VarPal[variant][0])

#define SG_LAT          2        // gemeten: de eerste noot klinkt 2 VBlanks na de start van de transitietaak
#define SG_BEAT(k)      ((k) * 2769 / 100 + SG_LAT)
#define SG_SHOW         27       // na de flits van de transitie-intro (die telt al mee in de VBlanks)
#define SG_FREEZE       SG_BEAT(3)
#define SG_TURN         SG_BEAT(4)
#define SG_STARE        SG_BEAT(5)
#define SG_EIGHTH       14
#define SG_CLOSE        SG_BEAT(6)
#define SG_BOARD        SG_BEAT(7)
#define SG_END          SG_BEAT(8)
#define SG_GROUND       127      // voeten op de grond van 1-1
#define SG_RED_X        106
#define SG_BIG_Y        99
#define SG_SPOT_R       44
#define SG_FLY_HOVER_Y  (SG_GROUND - 16 - 10)   // de Fly Guy als gekozene: zweeft op de plek van de rode
#define SG_RED_X_FLY    168                     // de rode op de plek van de Fly Guy (op de grond)
#define tSgLast         data[2]  // laatst geziene VBlank-tijd (voor eenmalige gebeurtenissen bij vertraagde frames)

static const struct OamData sSG_Oam64x32Affine =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(64x32),
    .size = SPRITE_SIZE(64x32),
    .priority = 0,
};

// Stilt Guy: draaistand 0 (van voren) t/m 7 (opzij) -> een van de vijf frames in de sheet
static const u8 sSG_StiltFrame[8] = {0, 1, 1, 2, 2, 3, 3, 4};

static const struct OamData sSG_Oam32x64Affine =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(32x64),
    .size = SPRITE_SIZE(32x64),
    .priority = 0,
};

static const struct OamData sSG_Oam32x64 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(32x64),
    .size = SPRITE_SIZE(32x64),
    .priority = 0,
};

// x, y van het midden van de sprite; voor 32x64 staan de voeten op de onderrand van het vak
static const s16 sSG_Pos[SG_COUNT][2] =
{
    [SG_STILT]  = {20, SG_GROUND - 32},
    [SG_FAT]    = {50, SG_GROUND - 32},
    [SG_SPEAR]  = {78, SG_GROUND - 32},
    [SG_RED]    = {SG_RED_X, SG_GROUND - 16},
    [SG_BUSH]   = {136, SG_GROUND - 16},
    [SG_YELLOW] = {192, SG_GROUND - 16},
    [SG_FLY]    = {152, 64},
    [SG_EXCL]   = {SG_RED_X, SG_GROUND - 19 - 8},
    [SG_BIG]    = {SG_RED_X, SG_BIG_Y},
};
static const s8 sSG_Hop[] = {-2, -4, -5, -6, -6, -5, -4, -2, 0};

static EWRAM_DATA u8 sSG_Variant = 0;

// Wie is het? De Fly Guy en de Spear Guy op naam, de rest op de kleur van de trainerfoto (= die van de overworld-sprite).
static u32 SG_GetVariant(void)
{
    u16 t = TRAINER_BATTLE_PARAM.opponentA;
    if (t == TRAINER_YI_SHY_GUY_CAMP_A1)   // "FLY GUY"
        return SG_V_FLY;
    if (t == TRAINER_YI_SHY_GUY_CAMP_B1)                                        // "SPEAR GUY"
        return SG_V_SPEAR;
    switch (GetTrainerPicFromId(t))
    {
    case TRAINER_PIC_GUEST_SHY_GUY_GREEN:
        return SG_V_GREEN;
    case TRAINER_PIC_GUEST_SHY_GUY_PINK:
        return SG_V_PINK;
    case TRAINER_PIC_GUEST_SHY_GUY_BLACK:
        return SG_V_BLACK;
    default:
        return SG_V_RED;
    }
}

// de figuur die zich omdraait
static u32 SG_Chosen(void)
{
    return sSG_Variant == SG_V_FLY ? SG_FLY : (sSG_Variant == SG_V_SPEAR ? SG_SPEAR : SG_RED);
}

// '!' per variant: [0] in de rij, [1] in de close-up (x t.o.v. SG_RED_X, y absoluut)
static const s16 sSG_ExclPos[SG_NUM_VARIANTS][2][2] =
{
    [SG_V_RED]   = {{0, SG_GROUND - 19 - 12}, {14, SG_BIG_Y - 36}},
    [SG_V_GREEN] = {{0, SG_GROUND - 19 - 12}, {14, SG_BIG_Y - 36}},
    [SG_V_PINK]  = {{0, SG_GROUND - 19 - 12}, {14, SG_BIG_Y - 36}},
    [SG_V_BLACK] = {{0, SG_GROUND - 19 - 12}, {14, SG_BIG_Y - 36}},
    [SG_V_FLY]   = {{0, SG_FLY_HOVER_Y + 16 - SG_H_FLYTURN - 12}, {22, SG_BIG_Y - 34}},
    [SG_V_SPEAR] = {{-6, SG_GROUND - 22 - 12}, {-16, SG_BIG_Y - 30}},
};
// close-up: y-correctie zodat het midden van de figuur op SG_BIG_Y staat (kleine frames hebben de voeten onderaan)
static const s8 sSG_BigDy[SG_NUM_VARIANTS] =
{
    [SG_V_FLY]   = -(16 - SG_H_FLYTURN / 2) * 2,
    [SG_V_SPEAR] = -(32 - SG_H_SPEARTURN / 2) * 2,
};

// positie per variant: de gekozene staat op de plek van de rode, de rode op zijn plek (op de grond)
static void SG_Place(u32 i, s32 *x, s32 *y)
{
    u32 c = SG_Chosen();
    *x = sSG_Pos[i][0];
    *y = sSG_Pos[i][1];
    if (c == SG_RED)
        return;
    if (i == c)
    {
        *x = SG_RED_X;
        *y = c == SG_FLY ? SG_FLY_HOVER_Y : sSG_Pos[SG_SPEAR][1];
    }
    else if (i == SG_RED)
    {
        *x = c == SG_FLY ? SG_RED_X_FLY : sSG_Pos[SG_SPEAR][0];
    }
}

static bool32 SG_Hit(struct Task *task, s32 e, s32 at)
{
    return task->tSgLast < at && e >= at;
}

static void SG_Frame(u32 slot, u32 sheet, u32 frame, u32 pal, bool32 flip)
{
    static const u16 tags[] = {SG_TAG_S32, SG_TAG_S64, SG_TAG_BIG};
    static const u8 tilesPer[] = {16, 32, 32};
    struct Sprite *s = LI_S(slot);
    u8 p = IndexOfSpritePaletteTag(SG_TAG_PAL + pal);
    if (sLI_Spr[slot] >= MAX_SPRITES)
        return;
    s->oam.tileNum = GetSpriteTileStartByTag(tags[sheet]) + frame * tilesPer[sheet];
    if (p != 0xFF)
        s->oam.paletteNum = p;
    if (slot != SG_BIG)
        s->oam.matrixNum = flip ? ST_OAM_HFLIP : 0;
}

static u32 SG_PalBits(void)
{
    u32 i, bits = 0;
    for (i = 0; i <= SG_PAL_CHOSEN; i++)
        bits |= GI_SpritePalBit(SG_TAG_PAL + i);
    return bits;
}

static void RTShyGuy_Init(struct Task *task)
{
    u32 i;
    static const u8 sheet[SG_COUNT] = {SG_SH64, SG_SH64, SG_SH64, SG_SH32, SG_SH32, SG_SH32, SG_SH32, SG_SH32, SG_SHBIG};
    static const u16 tag[] = {SG_TAG_S32, SG_TAG_S64, SG_TAG_BIG};
    static const u32 *const gfx[] = {sShyGuyS32_Gfx, sShyGuyS64_Gfx, sShyGuyBig_Gfx};
    static const u32 size[] = {32 * 32 / 2 * SG_N_S32, 32 * 64 / 2 * SG_N_S64, 64 * 32 / 2 * SG_N_BIG};

    GI_LoadGfx(sShyGuyIntro_Tiles, sShyGuyIntro_Maps);
    LI_ResetSprites();
    sSG_Variant = SG_GetVariant();
    for (i = 0; i <= SG_PAL_CHOSEN; i++)
    {
        // het palet van de grote Shy Guy en het extra palet van de gekozene komen uit de variant
        const u16 *pal = i == SG_PAL_CHOSEN ? sSG_VarPal[sSG_Variant][0]
                       : (i == SG_PAL_BIG ? sSG_VarPal[sSG_Variant][1] : sShyGuyObj_Pal + i * 16);
        struct SpritePalette spal = {pal, SG_TAG_PAL + i};
        if (IndexOfSpritePaletteTag(SG_TAG_PAL + i) == 0xFF)
            LoadSpritePalette(&spal);
    }
    for (i = 0; i < SG_COUNT; i++)
    {
        u32 sh = sheet[i];
        const struct OamData *oam = sh == SG_SH32 ? &sGI_Oam32 : (sh == SG_SH64 ? &sSG_Oam32x64 : &sSG_Oam64x32Affine);
        // close-up van de Fly Guy / Spear Guy: zijn eigen kleine frame, 2x
        if (i == SG_BIG && sSG_Variant == SG_V_FLY)
            sh = SG_SH32, oam = &sGI_Oam32Affine;
        else if (i == SG_BIG && sSG_Variant == SG_V_SPEAR)
            sh = SG_SH64, oam = &sSG_Oam32x64Affine;
        u8 id = GI_CreateSprite2(gfx[sh], size[sh], sShyGuyObj_Pal, tag[sh], SG_TAG_PAL, oam,
                                 sSG_Pos[i][0], sSG_Pos[i][1], i == SG_BIG ? 0 : 2 + (i & 1));
        sLI_Spr[i] = id;
        if (id < MAX_SPRITES)
            gSprites[id].invisible = TRUE;
    }
    task->tSgLast = -1;
}

static bool8 RTShyGuy_Update(struct Task *task)
{
    s32 e = Tapu_Elapsed(), i, k, beat, bob, stilt, x, y;
    u32 c = SG_Chosen(), v = sSG_Variant;
    u32 keep = SG_PalBits(), bg = LI2_PALS_MAP;
    bool32 idle = e < SG_FREEZE, close = e >= SG_CLOSE;
    struct Sprite *s;

    GI_ResetPals(keep);
    if (e >= SG_SHOW)
        LoadPalette(sShyGuyIntro_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
    if (SG_Hit(task, e, SG_SHOW))
    {
        GI_KillFieldWindows();
        GI_ShowMap(SG_MAP_LEVEL);
    }

    // op de maat: elke tel even omhoog (alleen zolang ze nog meedoen)
    beat = (e - SG_LAT) * 100 % 2769 / 100;   // frames sinds de laatste tel (e >= SG_SHOW > SG_LAT)
    bob = (idle && beat < 4) ? -1 : 0;

    for (i = 0; i < SG_COUNT; i++)
    {
        s = LI_S(i);
        if (sLI_Spr[i] >= MAX_SPRITES)
            continue;
        s->invisible = e < SG_SHOW;
        SG_Place(i, &x, &y);
        s->x = x;
        s->y = y + bob;
    }

    // de Stilt Guy: kijkt naar links (frame 7 gespiegeld), draait vanaf de blik langzaam via 'van voren' naar rechts
    stilt = e < SG_STARE ? 0 : min((e - SG_STARE) / 2, 14);
    SG_Frame(SG_STILT, SG_SH64, SG_F_STILT + sSG_StiltFrame[stilt < 7 ? 7 - stilt : stilt - 7], SG_PAL_STILT, stilt < 7);
    // de Fat Guy kijkt op het blad naar rechts: gespiegeld = naar links; hij draait zich op de blik om
    SG_Frame(SG_FAT, SG_SH64, SG_F_FAT + (idle ? (e / SG_EIGHTH) % 2 : 0), SG_PAL_FAT, e < SG_STARE + SG_EIGHTH / 2);
    // de Spear Guy danst op de tel, draait een achtste later dan de Fat Guy (als gekozene: kijkt de camera aan)
    k = e - SG_TURN;
    if (c == SG_SPEAR && k >= 0)
        SG_Frame(SG_SPEAR, SG_SH64, SG_F_SPEARTURN, SG_PAL_SPEARTURN, FALSE);
    else
        SG_Frame(SG_SPEAR, SG_SH64, SG_F_SPEAR + (idle ? ((e - SG_LAT) * 100 / 2769) & 1 : 0),
                 c == SG_SPEAR ? SG_PAL_CHOSEN : SG_PAL_SPEAR, c != SG_SPEAR && e >= SG_STARE + SG_EIGHTH);
    if (idle && beat < 6)
        LI_S(SG_SPEAR)->y -= 2;
    // de gewone: lopen op de plaats (droog); de gekozene springt op de draai op en kijkt de camera aan
    SG_Frame(SG_YELLOW, SG_SH32, SG_F_YELLOW + (idle ? 1 + (e / SG_EIGHTH) % 3 : 0), SG_PAL_YELLOW, FALSE);
    if (c == SG_RED)
        SG_Frame(SG_RED, SG_SH32, SG_F_RED + (k >= 0 ? 4 : (idle ? 1 + (e / SG_EIGHTH + 1) % 3 : 0)), SG_PAL_CHOSEN, FALSE);
    else    // de rode op de plek van een ander: kijkt een achtste na de Fat Guy naar de gekozene
        SG_Frame(SG_RED, SG_SH32, SG_F_RED + (idle ? 1 + (e / SG_EIGHTH + 1) % 3 : 0), SG_PAL_RED,
                 (c == SG_SPEAR) == (e < SG_STARE + SG_EIGHTH));
    if (k >= 0 && k < (s32)ARRAY_COUNT(sSG_Hop))
        LI_S(c)->y += sSG_Hop[k];
    // de struik: eerst alleen struik (ritselt op de tel), op de blik komt er een Shy Guy uit kijken
    k = e - (SG_STARE + SG_EIGHTH * 2);
    SG_Frame(SG_BUSH, SG_SH32, SG_F_BUSH + (k < 0 ? 0 : min(1 + k / 3, 3)), SG_PAL_BUSH, FALSE);
    if (idle && beat < 4)
        LI_S(SG_BUSH)->x += (e & 2) ? 1 : -1;
    // de Fly Guy: de propeller draait altijd door (anders valt hij), zweeft (als gekozene: roze, van voren verschrikt)
    if (c == SG_FLY && e >= SG_TURN)
        SG_Frame(SG_FLY, SG_SH32, SG_F_FLYTURN + (e / 3) % 2, SG_PAL_FLYTURN, FALSE);
    else
        SG_Frame(SG_FLY, SG_SH32, SG_F_FLY + (e / 3) % 4, c == SG_FLY ? SG_PAL_CHOSEN : SG_PAL_FLY, FALSE);
    LI_S(SG_FLY)->y += Sin((e * 6) & 0xFF, 3);

    // '!' boven zijn hoofd (het Pokémon-uitroepteken: een trainer heeft je gezien. Hij is de trainer.)
    s = LI_S(SG_EXCL);
    SG_Frame(SG_EXCL, SG_SH32, SG_F_EXCL, SG_PAL_EXCL, FALSE);
    s->invisible = e < SG_TURN + 2 || e >= SG_END - 4;
    k = e - SG_TURN - 2;
    s->x = SG_RED_X + sSG_ExclPos[v][close][0];
    s->y = sSG_ExclPos[v][close][1] - (k >= 0 && k < 4 ? 4 - k : 0);

    // close-up: de rode wordt de grote Shy Guy (2x), alles buiten de spot valt in het donker
    s = LI_S(SG_BIG);
    k = e - SG_CLOSE;
    s->invisible = !close;
    LI_S(c)->invisible = close || e < SG_SHOW;
    if (close)
    {
        if (v == SG_V_FLY)
            SG_Frame(SG_BIG, SG_SH32, SG_F_FLYTURN + (e / 3) % 2, SG_PAL_FLYTURN, FALSE);
        else if (v == SG_V_SPEAR)
            SG_Frame(SG_BIG, SG_SH64, SG_F_SPEARTURN, SG_PAL_SPEARTURN, FALSE);
        else
            SG_Frame(SG_BIG, SG_SHBIG, SG_F_BIG, SG_PAL_BIG, FALSE);
        LI_Affine(sLI_Spr[SG_BIG], 256 + min(k, 4) * 64, 0);
        s->x = SG_RED_X + ((e & 2) ? 1 : -1);
        s->y = SG_BIG_Y + sSG_BigDy[v] + (k < 4 ? (4 - k) * 7 : 0);
    }
    if (SG_Hit(task, e, SG_CLOSE))
    {
        u16 *win;
        s32 y, d, h;
        GI_InitWindow();
        sTransitionData->WININ = WININ_WIN0_BG_ALL | WININ_WIN0_OBJ;
        sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR;
        sTransitionData->BLDCNT = BLDCNT_EFFECT_DARKEN | BLDCNT_TGT1_BG0 | BLDCNT_TGT1_OBJ | BLDCNT_TGT1_BD;
        SetGpuReg(REG_OFFSET_BLDY, 11);
        win = gScanlineEffectRegBuffers[0];
        for (y = 0; y < DISPLAY_HEIGHT; y++)
        {
            d = y - SG_BIG_Y;
            h = (d > -SG_SPOT_R && d < SG_SPOT_R) ? Sqrt(SG_SPOT_R * SG_SPOT_R - d * d) : 0;
            win[y] = h ? WIN_RANGE(SG_RED_X - h, SG_RED_X + h) : 0;
        }
        PlaySE(SE_M_DETECT);
    }
    if (SG_Hit(task, e, SG_BOARD))
    {
        u16 *win = gScanlineEffectRegBuffers[0];
        s32 y;
        // het bord (y 4-56) hoort bij het licht
        for (y = 4; y < 56; y++)
            win[y] = WIN_RANGE(40, 200);
        GI_ShowMap(SG_MAP_BOARD);
        PlaySE(SE_SELECT);
    }

    // geluid
    if (SG_Hit(task, e, SG_FREEZE))
        PlaySE(SE_LEDGE);       // een stap te veel, dan stilte
    if (SG_Hit(task, e, SG_TURN))
        PlaySE(SE_PIN);
    if (SG_Hit(task, e, SG_STARE) || SG_Hit(task, e, SG_STARE + SG_EIGHTH))
        PlaySE(SE_M_TAIL_WHIP);

    // wit op de melodie (venster en verduistering eerst uit, anders wordt de buitenkant grijs)
    if (SG_Hit(task, e, SG_END - 4))
        sTransitionData->BLDCNT = 0;

    task->tSgLast = e;
    LI2_FadeWorld(e, SG_SHOW, bg, keep);
    LI2_FadeIn(e, SG_SHOW, bg | keep);
    if (LI2_WhiteOut(e, SG_END, bg, keep))
    {
        for (i = 0; i < LI_SPRITES; i++)
            if (sLI_Spr[i] < MAX_SPRITES)
                LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTShyGuy_Finish(struct Task *task)
{
    u32 i;
    GI_EndWindow();
    LI_DestroySprites();
    FreeSpriteTilesByTag(SG_TAG_S32);
    FreeSpriteTilesByTag(SG_TAG_S64);
    FreeSpriteTilesByTag(SG_TAG_BIG);
    for (i = 0; i <= SG_PAL_CHOSEN; i++)
        FreeSpritePaletteByTag(SG_TAG_PAL + i);
    GI_Free();
}

static const struct RouteTransition sRT_ShyGuy =
{
    sPikachu_Tileset, 32, sShyGuyIntro_Pal + 5 * 16, 1, 1, 0, RTShyGuy_Init, RTShyGuy_Update, RTShyGuy_Finish
};

static void Task_ShyGuy(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_ShyGuy);
}
