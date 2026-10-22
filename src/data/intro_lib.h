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

// alleen rij r0 t/m r1-1 uit beeld n
static void GI_ShowRows(u32 n, u32 r0, u32 r1)
{
    u16 *tilemap = RT_Tilemap();
    const u16 *map;
    u32 r;

    if (sGymIntro_Maps == NULL)
        return;
    map = &sGymIntro_Maps[n * GI_MAP_SIZE];
    for (r = r0; r < r1; r++)
        CpuCopy16(&map[r * 30], &tilemap[r * 32], 30 * 2);
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

static u8 GI_TrainerPic(u16 pic, s16 x, s16 y)
{
    u8 id = CreateTrainerSprite(pic, x, y, 0, NULL);
    gSprites[id].oam.priority = 0;
    return id;
}

static u32 GI_TrainerPalBit(u16 pic)
{
    return GI_SpritePalBit(gTrainerSprites[pic].palette.tag);
}

static void GI_DestroyTrainerPic(u8 id)
{
    FreeSpriteOamMatrix(&gSprites[id]);
    DestroySpriteAndFreeResources(&gSprites[id]);
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

static const struct OamData sGI_Oam64 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

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

// spotlight/lichtbundel: venster 0 per beeldlijn (HBlank-DMA op WIN0H) met 'lichter maken' erin
static void GI_InitWindow(void)
{
    InitTransitionData();
    ScanlineEffect_Clear();
    CpuFill16(0, gScanlineEffectRegBuffers[0], DISPLAY_HEIGHT * 2);
    CpuFill16(0, gScanlineEffectRegBuffers[1], DISPLAY_HEIGHT * 2);
    sTransitionData->WININ = WININ_WIN0_ALL;
    sTransitionData->WINOUT = WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ;
    sTransitionData->WIN0V = DISPLAY_HEIGHT;
    sTransitionData->BLDCNT = 0;
    sTransitionData->VBlank_DMA = TRUE;
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
    SetVBlankCallback(VBlankCB_CircularMask);
}

static void GI_EndWindow(void)
{
    sTransitionData->BLDCNT = 0;
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON);
    SetVBlankCallback(VBlankCB_BattleTransition);
}

#include "trainer_pokemon_sprites.h"

// een Pokémon (zijn eigen frontsprite) als sprite; het palet krijgt de soort als tag
static u8 GI_MonPic(u16 species, s16 x, s16 y)
{
    u16 id = CreateMonPicSprite(species, FALSE, 0, TRUE, x, y, 0, species);
    if (id >= MAX_SPRITES)
        return MAX_SPRITES;
    gSprites[id].oam.priority = 0;
    gSprites[id].invisible = TRUE;
    return id;
}

static void GI_DestroyMonPic(u8 id)
{
    if (id < MAX_SPRITES)
        FreeAndDestroyMonPicSprite(id);
}

static struct Sprite *GI_Sprite(u8 id)
{
    static EWRAM_DATA struct Sprite sDummy = {0};
    return id < MAX_SPRITES ? &gSprites[id] : &sDummy;
}

// venster 0 als rechthoek (alleen daarbinnen BG en sprites, daarbuiten de zwarte achtergrond)
static void GI_SetRectWindow(s32 x0, s32 y0, s32 x1, s32 y1)
{
    u16 *win = gScanlineEffectRegBuffers[0];
    s32 y;
    for (y = 0; y < DISPLAY_HEIGHT; y++)
        win[y] = (y >= y0 && y < y1 && x1 > x0) ? WIN_RANGE(x0, x1) : 0;
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

static void GI_Flash(s32 t, s32 start, s32 len, s32 from, u32 keep, u16 color)
{
    s32 k;
    if (t < start || t >= start + len)
        return;
    k = from - (t - start) * from / len;
    BlendPalettes(GI_BG_PALS | keep, k, color);
}

static const struct OamData sGI_Oam8x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(8x32),
    .size = SPRITE_SIZE(8x32),
    .priority = 0,
};

static u16 GI_MixColor(u16 a, u16 b, s32 k, s32 n)
{
    s32 r = GET_R(a) + (GET_R(b) - GET_R(a)) * k / n;
    s32 g = GET_G(a) + (GET_G(b) - GET_G(a)) * k / n;
    s32 bl = GET_B(a) + (GET_B(b) - GET_B(a)) * k / n;
    return RGB(r, g, bl);
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

static const struct OamData sLI2_Oam16x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(16x32),
    .size = SPRITE_SIZE(16x32),
    .priority = 0,
};

static const struct OamData sLI2_Oam32x16 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 0,
};

static u32 LI2_MonBit(u8 id)
{
    return id < MAX_SPRITES ? 1 << (16 + gSprites[id].oam.paletteNum) : 0;
}

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

// de wereld in 8 frames naar zwart; vanaf 'start' is ons beeld er en blijft de rest zwart
static void LI2_FadeWorld(s32 t, s32 start, u32 bg, u32 keep)
{
    if (t < start)
        BlendPalettes(PALETTES_ALL & ~keep, min(t * 2, 16), RGB_BLACK);
    else
        LI2_FillField(bg, keep, RGB_BLACK);
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

// het beeld komt in 8 frames uit het zwart op
static void LI2_FadeIn(s32 t, s32 start, u32 bg)
{
    if (t >= start && t < start + 8)
        BlendPalettes(bg, 16 - (t - start) * 2, RGB_BLACK);
}

// HBlank-golf op BG0HOFS (hitte, splijten); waarde per beeldlijn. Vóór 'start' is de golf nog niet aan (de kaart kan
// de scanline-buffer nog gebruiken, bijv. het licht in een donkere grot): dan een eigen kladbuffer.
static EWRAM_DATA s16 sLI2_NoHofs[DISPLAY_HEIGHT] = {0};

static s16 *LI2_Hofs(s32 t, s32 start)
{
    return t > start ? (s16 *)gScanlineEffectRegBuffers[0] : sLI2_NoHofs;
}

