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
#define SG_TAG_PAL      0x5A93   // t/m 0x5A93 + SG_NUM_PALS - 1

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
    if (sheet != SG_SHBIG)
        s->oam.matrixNum = flip ? ST_OAM_HFLIP : 0;
}

static u32 SG_PalBits(void)
{
    u32 i, bits = 0;
    for (i = 0; i < SG_NUM_PALS; i++)
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
    for (i = 0; i < SG_NUM_PALS; i++)
    {
        struct SpritePalette spal = {sShyGuyObj_Pal + i * 16, SG_TAG_PAL + i};
        if (IndexOfSpritePaletteTag(SG_TAG_PAL + i) == 0xFF)
            LoadSpritePalette(&spal);
    }
    for (i = 0; i < SG_COUNT; i++)
    {
        u32 sh = sheet[i];
        const struct OamData *oam = sh == SG_SH32 ? &sGI_Oam32 : (sh == SG_SH64 ? &sSG_Oam32x64 : &sSG_Oam64x32Affine);
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
    s32 e = Tapu_Elapsed(), i, k, beat, bob, stilt;
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
        s->x = sSG_Pos[i][0];
        s->y = sSG_Pos[i][1] + bob;
    }

    // de Stilt Guy: kijkt naar links (frame 7 gespiegeld), draait vanaf de blik langzaam via 'van voren' naar rechts
    stilt = e < SG_STARE ? 0 : min((e - SG_STARE) / 2, 14);
    SG_Frame(SG_STILT, SG_SH64, SG_F_STILT + sSG_StiltFrame[stilt < 7 ? 7 - stilt : stilt - 7], SG_PAL_STILT, stilt < 7);
    // de Fat Guy kijkt op het blad naar rechts: gespiegeld = naar links; hij draait zich op de blik om
    SG_Frame(SG_FAT, SG_SH64, SG_F_FAT + (idle ? (e / SG_EIGHTH) % 2 : 0), SG_PAL_FAT, e < SG_STARE + SG_EIGHTH / 2);
    // de Spear Guy danst op de tel, draait een achtste later dan de Fat Guy
    SG_Frame(SG_SPEAR, SG_SH64, SG_F_SPEAR + (idle ? ((e - SG_LAT) * 100 / 2769) & 1 : 0), SG_PAL_SPEAR, e >= SG_STARE + SG_EIGHTH);
    if (idle && beat < 6)
        LI_S(SG_SPEAR)->y -= 2;
    // de gewone: lopen op de plaats (droog); de rode springt op de draai op en kijkt de camera aan
    SG_Frame(SG_YELLOW, SG_SH32, SG_F_YELLOW + (idle ? 1 + (e / SG_EIGHTH) % 3 : 0), SG_PAL_YELLOW, FALSE);
    k = e - SG_TURN;
    SG_Frame(SG_RED, SG_SH32, SG_F_RED + (k >= 0 ? 4 : (idle ? 1 + (e / SG_EIGHTH + 1) % 3 : 0)), SG_PAL_RED, FALSE);
    if (k >= 0 && k < (s32)ARRAY_COUNT(sSG_Hop))
        LI_S(SG_RED)->y += sSG_Hop[k];
    // de struik: eerst alleen struik (ritselt op de tel), op de blik komt er een Shy Guy uit kijken
    k = e - (SG_STARE + SG_EIGHTH * 2);
    SG_Frame(SG_BUSH, SG_SH32, SG_F_BUSH + (k < 0 ? 0 : min(1 + k / 3, 3)), SG_PAL_BUSH, FALSE);
    if (idle && beat < 4)
        LI_S(SG_BUSH)->x += (e & 2) ? 1 : -1;
    // de Fly Guy: de propeller draait altijd door (anders valt hij), zweeft
    SG_Frame(SG_FLY, SG_SH32, SG_F_FLY + (e / 3) % 4, SG_PAL_FLY, FALSE);
    LI_S(SG_FLY)->y += Sin((e * 6) & 0xFF, 3);

    // '!' boven zijn hoofd (het Pokémon-uitroepteken: een trainer heeft je gezien. Hij is de trainer.)
    s = LI_S(SG_EXCL);
    SG_Frame(SG_EXCL, SG_SH32, SG_F_EXCL, SG_PAL_EXCL, FALSE);
    s->invisible = e < SG_TURN + 2 || e >= SG_END - 4;
    k = e - SG_TURN - 2;
    s->y = (close ? SG_BIG_Y - 36 : sSG_Pos[SG_EXCL][1] - 4) - (k >= 0 && k < 4 ? 4 - k : 0);
    if (close)
        s->x = SG_RED_X + 14;

    // close-up: de rode wordt de grote Shy Guy (2x), alles buiten de spot valt in het donker
    s = LI_S(SG_BIG);
    k = e - SG_CLOSE;
    s->invisible = !close;
    LI_S(SG_RED)->invisible = close || e < SG_SHOW;
    if (close)
    {
        SG_Frame(SG_BIG, SG_SHBIG, SG_F_BIG, SG_PAL_BIG, FALSE);
        LI_Affine(sLI_Spr[SG_BIG], 256 + min(k, 4) * 64, 0);
        s->x = SG_RED_X + ((e & 2) ? 1 : -1);
        s->y = SG_BIG_Y + (k < 4 ? (4 - k) * 7 : 0);
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
    for (i = 0; i < SG_NUM_PALS; i++)
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
