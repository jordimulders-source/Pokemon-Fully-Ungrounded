// Project Grounded: lichte gevechtsintro's van vijf legendaries (Lugia, Ho-Oh, Volcanion, Hoopa, Forces of Nature).
// Wordt onderaan src/battle_transition.c ingevoegd, na de gymleider-intro's (src/data/gym_intros_a.h en _b.h): gebruikt
// dezelfde GI_-hulpjes, de route-transitie-runner en Tapu_Blend. Art: tools/grounded/legend_intros.py (BG0-beelden in de
// paletten 13-15); de rest zijn echte frontsprites en gevechtsanimatie-art die al in de ROM staan.

#include "item_icon.h"
#include "pokemon.h"
#include "constants/items.h"

#define LI_SPRITES 32
static EWRAM_DATA u8 sLI_Spr[LI_SPRITES] = {0};
static EWRAM_DATA s16 sLI_Phys[LI_SPRITES][4] = {0}; // x, y, vx, vy in 1/16 px

static void LI_ResetSprites(void)
{
    u32 i;
    for (i = 0; i < LI_SPRITES; i++)
        sLI_Spr[i] = MAX_SPRITES;
}

static struct Sprite *LI_S(u32 i)
{
    return GI_Sprite(sLI_Spr[i]);
}

// een onzichtbare sprite uit gevechtsanimatie-art (of eigen art) in slot i
static void LI_Make(u32 i, const u32 *gfx, u32 size, const u16 *pal, u16 tag, const struct OamData *oam, s16 x, s16 y, u8 subprio)
{
    u8 id = GI_CreateSprite(gfx, size, pal, tag, oam, x, y, subprio);
    sLI_Spr[i] = id;
    if (id < MAX_SPRITES)
        gSprites[id].invisible = TRUE;
}

static void LI_Frame(u32 i, u16 tag, u32 frame, u32 tilesPerFrame)
{
    if (sLI_Spr[i] < MAX_SPRITES)
        gSprites[sLI_Spr[i]].oam.tileNum = GetSpriteTileStartByTag(tag) + frame * tilesPerFrame;
}

static void LI_DestroySprites(void)
{
    u32 i;
    for (i = 0; i < LI_SPRITES; i++)
    {
        if (sLI_Spr[i] < MAX_SPRITES)
            GI_DestroySprite(sLI_Spr[i]);
        sLI_Spr[i] = MAX_SPRITES;
    }
}

// een frontsprite die kan schalen en draaien (affine, dubbele grootte)
static u8 LI_MonPicAffine(u16 species, s16 x, s16 y)
{
    u8 id = GI_MonPic(species, x, y);
    struct Sprite *s;
    if (id >= MAX_SPRITES)
        return id;
    s = &gSprites[id];
    s->oam.matrixNum = AllocOamMatrix();
    if (s->oam.matrixNum == 0xFF)
    {
        s->oam.matrixNum = 0;
        return id;
    }
    s->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
    s->affineAnimPaused = TRUE;
    CalcCenterToCornerVec(s, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
    SetOamMatrixRotationScaling(s->oam.matrixNum, 256, 256, 0);
    return id;
}

static void LI_Affine(u8 id, s32 scale, u16 rot)
{
    if (id < MAX_SPRITES && gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, scale, scale, rot);
}

static void LI_DestroyMonPic(u8 id)
{
    if (id >= MAX_SPRITES)
        return;
    if (gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
    {
        FreeOamMatrix(gSprites[id].oam.matrixNum);
        gSprites[id].oam.affineMode = ST_OAM_AFFINE_OFF;
        gSprites[id].oam.matrixNum = 0;
    }
    FreeAndDestroyMonPicSprite(id);
}

// HBlank-DMA op BG0HOFS (golven, scheeftrekken); de buffer is gScanlineEffectRegBuffers[0]
static void LI_InitWave(void)
{
    InitTransitionData();
    ScanlineEffect_Clear();
    CpuFill16(0, gScanlineEffectRegBuffers[0], DISPLAY_HEIGHT * 2);
    CpuFill16(0, gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    sTransitionData->VBlank_DMA = TRUE;
    SetVBlankCallback(VBlankCB_PatternWeave);
}

static void LI_EndWave(void)
{
    SetVBlankCallback(VBlankCB_BattleTransition);
    DmaStop(0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
}

// trillen van BG0 met een vaste (willekeurige) verschuiving; geeft de verschuiving terug voor de sprites
static s32 LI_ShakeAmp(s32 amp)
{
    return amp > 0 ? (s32)(Random() % (amp * 2 + 1)) - amp : 0;
}

// =====================================================================================================================
// Volcanion: een manometer op een geklonken plaat ("DO NOT TAP THE GLASS"). De naald kruipt tikkend van "fine" naar
// "NOPE", blijft daar trillend hangen, de klinknagels schieten er een voor een uit (de plaat trilt steeds harder), en
// dan blaast er van beide kanten stoom in beeld (zijn armkanonnen) tot alles wit is.
static const u32 sLegVolcanion_Tiles[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion.4bpp.smol");
static const u32 sLegVolcanion_Maps[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_maps.bin.smol");
static const u16 sLegVolcanion_Pal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion.gbapal");
static const u32 sLegVolcanion_NeedleGfx[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_needle.4bpp.smol");
static const u16 sLegVolcanion_NeedlePal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion_needle.gbapal");
static const u32 sLegVolcanion_RivetGfx[] = INCBIN_U32("graphics/battle_transitions/legend_volcanion_rivet.4bpp.smol");
static const u16 sLegVolcanion_RivetPal[] = INCBIN_U16("graphics/battle_transitions/legend_volcanion_rivet.gbapal");

enum { VOL_MAP_GAUGE, VOL_MAP_HOLES };
#define VOL_TAG_NEEDLE  0x5A64
#define VOL_TAG_RIVET   0x5A65
#define VOL_TAG_STEAM   0x5A66
#define VOL_SHOW        6
#define VOL_RED         96    // de naald staat in het rood
#define VOL_POP         100   // de eerste klinknagel
#define VOL_STEAM       138
#define VOL_END         178
#define VOL_RIVETS      6
#define VOL_STEAMS      10
#define VOL_CX          120
#define VOL_CY          76
#define VOL_ZONE_RED    9     // BG 14: de rode zone (knippert)

// klinknagels die eruit schieten (tile x, y van het 2x2-blok) en wanneer
static const u8 sVolRivet[VOL_RIVETS][3] = {{1, 1, 0}, {27, 17, 10}, {27, 1, 18}, {1, 17, 24}, {1, 9, 29}, {27, 9, 33}};
static const u8 sVolSteamY[VOL_STEAMS / 2] = {26, 54, 82, 110, 138};

static void RTVolcanion_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sLegVolcanion_Tiles, sLegVolcanion_Maps);
    LoadPalette(sLegVolcanion_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    LI_Make(0, sLegVolcanion_NeedleGfx, 64 * 64 / 2, sLegVolcanion_NeedlePal, VOL_TAG_NEEDLE, &sGI_Oam64Affine, VOL_CX, VOL_CY, 0);
    for (i = 0; i < VOL_RIVETS; i++)
        LI_Make(1 + i, sLegVolcanion_RivetGfx, 16 * 16 / 2, sLegVolcanion_RivetPal, VOL_TAG_RIVET, &sGI_Oam16, 0, 0, 0);
    for (i = 0; i < VOL_STEAMS; i++)
        LI_Make(1 + VOL_RIVETS + i, gBattleAnimSpriteGfx_MistCloud, 32 * 32 / 2, gBattleAnimSpritePal_MistCloud, VOL_TAG_STEAM, &sGI_Oam32Affine, 0, sVolSteamY[i % (VOL_STEAMS / 2)], 0);
    task->tGiShown = 0xFF;
}

static bool8 RTVolcanion_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, deg, dx = 0, dy = 0, amp;
    u32 keep = GI_SpritePalBit(VOL_TAG_NEEDLE) | GI_SpritePalBit(VOL_TAG_RIVET) | GI_SpritePalBit(VOL_TAG_STEAM);
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s, *needle = LI_S(0);

    GI_ResetPals(keep);
    LoadPalette(sLegVolcanion_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    if (t >= VOL_RED && ((t >> 2) & 1))
        pal[16 + VOL_ZONE_RED] = RGB(31, 20, 12);
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    if (t == VOL_SHOW)
    {
        GI_KillFieldWindows();
        GI_ShowMap(VOL_MAP_GAUGE);
    }

    // de plaat trilt steeds harder (BG en sprites samen)
    amp = (t >= VOL_POP) ? 1 + (t - VOL_POP) / 12 : (t >= VOL_RED - 20 ? 1 : 0);
    if (amp)
    {
        dx = LI_ShakeAmp(amp);
        dy = LI_ShakeAmp(amp);
    }
    SetGpuReg(REG_OFFSET_BG0HOFS, dx & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, dy & 0x1FF);

    // de naald: kruipt (steeds sneller) van -128 naar +118 graden en blijft daar trillend hangen
    if (t >= VOL_SHOW)
    {
        k = min(t - VOL_SHOW, VOL_RED - VOL_SHOW);
        deg = -128 + 246 * k * k / ((VOL_RED - VOL_SHOW) * (VOL_RED - VOL_SHOW));
        deg += (t >= VOL_RED) ? LI_ShakeAmp(4) : ((t >> 1) & 1);
        needle->invisible = FALSE;
        needle->x2 = -dx;
        needle->y2 = -dy;
        LI_Affine(sLI_Spr[0], 448, (u16)(-deg * 182));
        if (t < VOL_RED && (t - VOL_SHOW) % 12 == 0)
            PlaySE(SE_CLICK);
    }

    // klinknagels schieten eruit
    for (i = 0; i < VOL_RIVETS; i++)
    {
        s32 tx = sVolRivet[i][0], ty = sVolRivet[i][1];
        s = LI_S(1 + i);
        k = t - VOL_POP - sVolRivet[i][2];
        if (k < 0)
            continue;
        if (k == 0)
        {
            GI_PutRect(VOL_MAP_HOLES, tx, ty, 2, 2, tx, ty);
            sLI_Phys[i][0] = (tx * 8 + 8) << 4;
            sLI_Phys[i][1] = (ty * 8 + 8) << 4;
            sLI_Phys[i][2] = (tx < 15 ? -1 : 1) * (20 + (Random() & 15));
            sLI_Phys[i][3] = -64 - (Random() & 15);
            PlaySE(SE_M_COMET_PUNCH);
        }
        sLI_Phys[i][0] += sLI_Phys[i][2];
        sLI_Phys[i][1] += sLI_Phys[i][3];
        sLI_Phys[i][3] += 6;
        s->invisible = (sLI_Phys[i][1] >> 4) > 180;
        s->x = sLI_Phys[i][0] >> 4;
        s->y = sLI_Phys[i][1] >> 4;
        s->oam.matrixNum = ((k >> 1) & 1) ? ST_OAM_HFLIP : 0;
    }

    // stoom blaast van beide kanten naar binnen en wordt groter
    for (i = 0; i < VOL_STEAMS; i++)
    {
        s32 side = (i < VOL_STEAMS / 2) ? -1 : 1;
        s = LI_S(1 + VOL_RIVETS + i);
        k = t - VOL_STEAM - ((i * 3) % 5) * 2;
        if (k < 0)
            continue;
        s->invisible = FALSE;
        s->x = 120 + side * (150 - min(k * 6, 120)) + Sin(((t + i * 30) * 12) & 0xFF, 2);
        s->y = sVolSteamY[i % (VOL_STEAMS / 2)] + Sin(((t + i * 17) * 9) & 0xFF, 3);
        LI_Affine(sLI_Spr[1 + VOL_RIVETS + i], min(320 + k * 20, 512), 0);
    }

    // geluid
    if (t == VOL_RED)
        PlaySE(SE_M_SCREECH);
    if (t == VOL_STEAM - 8)
        PlayCry_Normal(SPECIES_VOLCANION, 0);
    if (t == VOL_STEAM)
        PlaySE(SE_M_MIST);
    if (t == VOL_STEAM + 14)
        PlaySE(SE_M_EXPLOSION);

    GI_FadeWorld(t, VOL_SHOW, keep);
    if (t >= VOL_SHOW && t < VOL_SHOW + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - VOL_SHOW) * 2, RGB_BLACK);
    if (t >= VOL_STEAM + 6 && t < VOL_END - 4)
    {
        k = (t - VOL_STEAM - 6) * 14 / (VOL_END - 4 - VOL_STEAM - 6);
        BlendPalettes(GI_BG_PALS | GI_SpritePalBit(VOL_TAG_NEEDLE) | GI_SpritePalBit(VOL_TAG_RIVET), k, RGB_WHITE);
    }
    if (GI_WhiteOut(t, VOL_END, keep))
    {
        for (i = 0; i < 1 + VOL_RIVETS + VOL_STEAMS; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTVolcanion_Finish(struct Task *task)
{
    LI_EndWave();
    LI_DestroySprites();
    GI_FreeTag(VOL_TAG_NEEDLE);
    GI_FreeTag(VOL_TAG_RIVET);
    GI_FreeTag(VOL_TAG_STEAM);
    GI_Free();
}

static const struct RouteTransition sRT_LegendVolcanion =
{
    sPikachu_Tileset, 32, sLegVolcanion_Pal + 32, 1, 1, 0, RTVolcanion_Init, RTVolcanion_Update, RTVolcanion_Finish
};

static void Task_LegendVolcanion(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_LegendVolcanion);
}
