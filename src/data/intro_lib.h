// Project Grounded: gedeelde hulpjes (GI_*) voor de lichte intro's (klasse-intro's en legendary-intro's). Wordt
// onderaan src/battle_transition.c ingevoegd en gebruikt de route-transitie-runner. Kwam uit de gymleider-intro's
// (gym_intros_a/b.h, verwijderd in Fully Ungrounded); art-hulpjes: tools/grounded/gym_intro_lib.py.

#include "graphics.h"

#define GI_BG_PALS    ((1 << 13) | (1 << 14) | (1 << 15))
#define GI_MAP_SIZE   (30 * 20)
#define tGiSprite0    data[5]
#define tGiSprite1    data[6]
#define tGiSprite2    data[7]
#define tGiSprite3    data[9]
#define tGiSprite4    data[10]
#define tGiShown      data[11]

static EWRAM_DATA u16 *sGymIntro_Maps = NULL;

// tiles (smol) naar BG0 vanaf tile 0, alle tilemaps (smol) naar een buffer
static void GI_LoadGfx(const u32 *tiles, const u32 *maps)
{
    u16 *tilemap, *tileset;
    void *buf;

    GetBg0TilesDst(&tilemap, &tileset);
    buf = Alloc(GetDecompressedDataSize(tiles));
    if (buf != NULL)
    {
        DecompressDataWithHeaderWram(tiles, buf);
        CpuCopy16(buf, tileset, GetDecompressedDataSize(tiles));
        Free(buf);
    }
    sGymIntro_Maps = Alloc(GetDecompressedDataSize(maps));
    if (sGymIntro_Maps != NULL)
        DecompressDataWithHeaderWram(maps, sGymIntro_Maps);
    CpuFill16(0, tilemap, BG_SCREEN_SIZE);
}

// vensters en scanline-effecten van de kaart uit (de donkere Dewford-gym toont sprites alleen in een cirkel rond de
// speler). Pas aanroepen als de wereld al zwart is, anders zie je even de hele donkere gym.
static void GI_KillFieldWindows(void)
{
    ScanlineEffect_Clear();
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
}

static void GI_Free(void)
{
    TRY_FREE_AND_SET_NULL(sGymIntro_Maps);
}

// een heel beeld; kolom 30/31 en rij 20/31 krijgen een kopie van de rand (voor het trillen)
static void GI_ShowMap(u32 n)
{
    u16 *tilemap = RT_Tilemap();
    const u16 *map;
    u32 r;

    if (sGymIntro_Maps == NULL)
        return;
    map = &sGymIntro_Maps[n * GI_MAP_SIZE];
    for (r = 0; r < 20; r++)
    {
        CpuCopy16(&map[r * 30], &tilemap[r * 32], 30 * 2);
        tilemap[r * 32 + 30] = map[r * 30 + 29];
        tilemap[r * 32 + 31] = map[r * 30];
    }
    CpuCopy16(&tilemap[19 * 32], &tilemap[20 * 32], 32 * 2);
    CpuCopy16(&tilemap[0], &tilemap[31 * 32], 32 * 2);
}

// een blok van w x h vakken uit beeld n (vanaf sx, sy) naar dx, dy op het scherm
static void GI_PutRect(u32 n, s32 sx, s32 sy, s32 w, s32 h, s32 dx, s32 dy)
{
    u16 *tilemap = RT_Tilemap();
    const u16 *map;
    s32 r, c;

    if (sGymIntro_Maps == NULL)
        return;
    map = &sGymIntro_Maps[n * GI_MAP_SIZE];
    for (r = 0; r < h; r++)
    {
        if (dy + r < 0 || dy + r >= 20)
            continue;
        for (c = 0; c < w; c++)
        {
            if (dx + c < 0 || dx + c >= 30)
                continue;
            tilemap[(dy + r) * 32 + dx + c] = map[(sy + r) * 30 + sx + c];
        }
    }
}

// alle paletten behalve die van BG0 (13-15) en 'keep' (OBJ-paletten van onze sprites) in het getoonde beeld op een kleur
static void GI_FillField(u32 keep, u16 color)
{
    u32 i;
    for (i = 0; i < 32; i++)
    {
        if (((GI_BG_PALS | keep) >> i) & 1)
            continue;
        CpuFill16(color, &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
    }
}

// de getoonde (faded) kleuren van onze sprites elke frame terug naar het origineel (na een flits of fade)
static void GI_ResetPals(u32 keep)
{
    u32 i;
    for (i = 16; i < 32; i++)
        if ((keep >> i) & 1)
            CpuCopy16(&gPlttBufferUnfaded[i * 16], &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
}

static u32 GI_SpritePalBit(u16 tag)
{
    u8 idx = IndexOfSpritePaletteTag(tag);
    return idx == 0xFF ? 0 : 1 << (16 + idx);
}

static void GI_Shake(s32 amp)
{
    if (amp <= 0)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        return;
    }
    SetGpuReg(REG_OFFSET_BG0HOFS, ((Random() % (amp * 2 + 1)) - amp) & 0x1FF);
    SetGpuReg(REG_OFFSET_BG0VOFS, ((Random() % (amp * 2 + 1)) - amp) & 0x1FF);
}

static const struct OamData sGI_Oam64Affine =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct OamData sGI_Oam16 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(16x16),
    .size = SPRITE_SIZE(16x16),
    .priority = 0,
};

static const struct OamData sGI_Oam32Affine =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(32x32),
    .size = SPRITE_SIZE(32x32),
    .priority = 0,
};

// een sprite uit een (gecomprimeerd) sheet; affine sprites krijgen een eigen matrix
static u8 GI_CreateSprite2(const u32 *gfx, u32 size, const u16 *pal, u16 tag, u16 palTag, const struct OamData *oam, s16 x, s16 y, u8 subprio)
{
    struct CompressedSpriteSheet sheet = {gfx, size, tag};
    struct SpritePalette spal = {pal, palTag};
    struct SpriteTemplate tmpl = {
        .tileTag = tag,
        .paletteTag = palTag,
        .oam = oam,
        .anims = gDummySpriteAnimTable,
        .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable,
        .callback = SpriteCallbackDummy,
    };
    u8 id;
    if (GetSpriteTileStartByTag(tag) == 0xFFFF)
        LoadCompressedSpriteSheet(&sheet);
    if (IndexOfSpritePaletteTag(palTag) == 0xFF)
        LoadSpritePalette(&spal);
    id = CreateSprite(&tmpl, x, y, subprio);
    if (oam->affineMode != ST_OAM_AFFINE_OFF)
    {
        // de matrix komt van CreateSprite (InitSpriteAffineAnim)
        gSprites[id].affineAnimPaused = TRUE;
        SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, 256, 256, 0);
    }
    return id;
}

// sprite met een eigen tile- en palettag (dezelfde waarde)
static u8 GI_CreateSprite(const u32 *gfx, u32 size, const u16 *pal, u16 tag, const struct OamData *oam, s16 x, s16 y, u8 subprio)
{
    return GI_CreateSprite2(gfx, size, pal, tag, tag, oam, x, y, subprio);
}

static void GI_DestroySprite(u8 id)
{
    if (gSprites[id].oam.affineMode != ST_OAM_AFFINE_OFF)
        FreeSpriteOamMatrix(&gSprites[id]);
    DestroySprite(&gSprites[id]);
}

static void GI_FreeTag(u16 tag)
{
    FreeSpriteTilesByTag(tag);
    FreeSpritePaletteByTag(tag);
}

#include "trainer_pokemon_sprites.h"

static struct Sprite *GI_Sprite(u8 id)
{
    static EWRAM_DATA struct Sprite sDummy = {0};
    return id < MAX_SPRITES ? &gSprites[id] : &sDummy;
}

// de wereld zwart (eerste frames uitfaden) en aan het eind wit; geeft TRUE op het laatste frame
static void GI_FadeWorld(s32 t, s32 start, u32 keep)
{
    if (t < start)
        BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, min(t * 2, 16), RGB_BLACK);
    else
        GI_FillField(keep, RGB_BLACK);
}

static bool32 GI_WhiteOut(s32 t, s32 end, u32 keep)
{
    s32 k;
    if (t < end - 4)
        return FALSE;
    k = min((t - (end - 4)) * 4 + 4, 16);
    BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
    GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
    return t >= end;
}

// ---------------- tijd en kleurmenging (uit de vroegere Tapu-intro's)
static u16 Tapu_Blend(u16 a, u16 b, s32 k)
{
    s32 ar = a & 31, ag = (a >> 5) & 31, ab = (a >> 10) & 31;
    s32 br = b & 31, bg = (b >> 5) & 31, bb = (b >> 10) & 31;
    if (k <= 0)
        return a;
    if (k >= 16)
        return b;
    ar += ((br - ar) * k) >> 4;
    ag += ((bg - ag) * k) >> 4;
    ab += ((bb - ab) * k) >> 4;
    return RGB(ar, ag, ab);
}

// frames sinds de start van de transitie (VBlanks), zie LaunchBattleTransitionTask
static s32 Tapu_Elapsed(void)
{
    u8 id = FindTaskIdByFunc(Task_BattleTransition);
    u32 start;
    if (id == TASK_NONE)
        return 0;
    start = (u16)gTasks[id].data[13] | ((u32)(u16)gTasks[id].data[14] << 16);
    return gMain.vblankCounter1 - start;
}

// 32x32-sprites (uit de vroegere gymleider-intro's)
static const struct OamData sGI_Oam32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(32x32),
    .size = SPRITE_SIZE(32x32),
    .priority = 0,
};

// ---------------- LI2-hulpjes (uit de vroegere legendary-intro's, tweede reeks)
#define LI2_PALS_MAP   (0x3F << 10)    // BG 10-15
#define LI2_PALS_DIM   (0x3F << 4)     // BG 4-9

// alle paletten behalve 'bg' (onze BG-paletten) en 'keep' (onze sprites) op een kleur
static void LI2_FillField(u32 bg, u32 keep, u16 color)
{
    u32 i;
    for (i = 0; i < 32; i++)
    {
        if (((bg | keep) >> i) & 1)
            continue;
        CpuFill16(color, &gPlttBufferFaded[i * 16], PLTT_SIZE_4BPP);
    }
}

static bool32 LI2_WhiteOut(s32 t, s32 end, u32 bg, u32 keep)
{
    s32 k;
    if (t < end - 4)
        return FALSE;
    k = min((t - (end - 4)) * 4 + 4, 16);
    BlendPalettes(bg | keep, k, RGB_WHITE);
    LI2_FillField(bg, keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
    return t >= end;
}

