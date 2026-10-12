// Project Grounded: gymleider-intro's (deel A: Roxanne, Brawly, Wattson, Flannery). Wordt onderaan
// src/battle_transition.c ingevoegd (gebruikt de route-transitie-runner en zijn hulpjes). Vervangen de mugshot: de intro
// stelt de leider zelf voor (met haar/zijn eigen trainerfoto), en mugshot + intro samen duurt te lang (zoals bij Steven).
// Zuinig: een paar stilstaande BG0-beelden (tools/grounded/<naam>_transition.py, gedeelde hulpjes in gym_intro_lib.py),
// de beweging met sprites (trainerfoto's en gevechtsanimatie-art die al in de ROM staan), paletcycli, tilemap-blokken,
// vensters en trillen.

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

// ---------------- Roxanne ("Yo! Put your lighters up!"): de gym gaat op zwart. In het donker "PUT YOUR / LIGHTERS UP!",
// de zaal steekt in drie golven de aanstekers op (en wiegt), dan klikt de spotlight aan op Roxanne (venster 0 met
// 'lichter maken', de lichtkegel en de lichtvlek op het podium per beeldlijn). Twee rotsblokken zakken als versterkers
// omlaag (dreun), de powerchord flitst, het publiek gaat los, onderin een disclaimer. tools/grounded/roxanne_transition.py
static const u32 sGymRoxanne_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_roxanne.4bpp.smol");
static const u32 sGymRoxanne_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_roxanne_maps.bin.smol");
static const u16 sGymRoxanne_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_roxanne.gbapal");
static const u32 sGymRoxanne_AmpGfx[] = INCBIN_U32("graphics/battle_transitions/gym_roxanne_amp.4bpp.smol");
static const u16 sGymRoxanne_AmpPal[] = INCBIN_U16("graphics/battle_transitions/gym_roxanne_amp.gbapal");

enum { ROX_MAP_A, ROX_MAP_B, ROX_MAP_W1, ROX_MAP_W2A, ROX_MAP_W2B, ROX_MAP_DA, ROX_MAP_DB };
#define ROX_TAG_AMP   0x5A30
#define ROX_DARK      16    // zaal (zwart) in beeld
#define ROX_WORD1     20
#define ROX_WORD2     40
#define ROX_LIGHT1    52    // aanstekers, drie golven
#define ROX_SPOT      92
#define ROX_AMP       116
#define ROX_AMP_LEN   28
#define ROX_LAND      (ROX_AMP + ROX_AMP_LEN)
#define ROX_CHORD     (ROX_LAND + 6)
#define ROX_DISC      (ROX_CHORD + 10)
#define ROX_END       (ROX_LAND + 44)

// vlamkleuren per groep: {kern, buitenkant} in twee standen (flakkeren)
static const u16 sRoxFlame[2][3][2] =
{
    {{RGB(31, 31, 21), RGB(31, 18, 5)}, {RGB(31, 29, 17), RGB(29, 14, 4)}, {RGB(31, 31, 25), RGB(31, 21, 8)}},
    {{RGB(31, 27, 12), RGB(27, 12, 3)}, {RGB(31, 31, 22), RGB(31, 18, 6)}, {RGB(31, 26, 10), RGB(26, 10, 2)}},
};
// zakken van de versterkers: y per frame (uitlopen + een klein veertje bij het neerkomen)
static const s8 sRoxAmpBounce[] = {0, -3, -4, -3, -1, 0};

static void RTRoxanne_Init(struct Task *task)
{
    s32 y, half, d;
    u16 *win;

    GI_LoadGfx(sGymRoxanne_Tiles, sGymRoxanne_Maps);
    LoadPalette(sGymRoxanne_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_ROXANNE, 120, 74);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_CreateSprite(sGymRoxanne_AmpGfx, 64 * 64 / 2, sGymRoxanne_AmpPal, ROX_TAG_AMP, &sGI_Oam64, 52, -40, 1);
    task->tGiSprite2 = GI_CreateSprite(sGymRoxanne_AmpGfx, 64 * 64 / 2, sGymRoxanne_AmpPal, ROX_TAG_AMP, &sGI_Oam64, 188, -40, 1);
    gSprites[task->tGiSprite2].oam.matrixNum = ST_OAM_HFLIP;
    task->tGiShown = 0xFF;

    // lichtkegel (vanaf de lamp op y 18 naar het podium op y 96) en de lichtvlek op het podium (ellips rond y 106)
    GI_InitWindow();
    win = gScanlineEffectRegBuffers[0];
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        half = 0;
        if (y >= 18 && y < 96)
            half = 4 + (y - 18) * 40 / 78;
        d = y - 106;
        if (d > -17 && d < 17)
            half = max(half, 46 * Sqrt(289 - d * d) / 17);
        win[y] = half ? WIN_RANGE(120 - half, 120 + half) : 0;
    }
    SetGpuReg(REG_OFFSET_BLDY, 6);
}

static bool8 RTRoxanne_Update(struct Task *task)
{
    s32 t = task->tRtTimer, g, k, y, map, frenzy;
    u32 keep;
    struct Sprite *rox = &gSprites[task->tGiSprite0];
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];

    // BG-paletten opnieuw (de runner zet palet 15 elke frame), vlammen per groep aan/uit en flakkerend
    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_ROXANNE) | GI_SpritePalBit(ROX_TAG_AMP);
    GI_ResetPals(keep);
    LoadPalette(sGymRoxanne_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    frenzy = (t >= ROX_LAND);
    for (g = 0; g < 3; g++)
    {
        k = frenzy ? ((t >> 1) + g) & 1 : ((t >> 2) + g * 3 + (t >> 4)) & 1;
        if (t >= ROX_LIGHT1 + g * 10)
        {
            pal[4 + g * 2] = sRoxFlame[k][g][0];
            pal[5 + g * 2] = sRoxFlame[k][g][1];
        }
        else
        {
            pal[4 + g * 2] = 0;
            pal[5 + g * 2] = 0;
        }
    }
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    // welk beeld: tekst in het donker, daarna (vanaf de spot) zonder tekst; het publiek wiegt
    k = (t >> (frenzy ? 3 : 4)) & 1;
    if (t < ROX_DARK)
        map = -1;
    else if (t < ROX_WORD1)
        map = ROX_MAP_A;
    else if (t < ROX_WORD2)
        map = ROX_MAP_W1;
    else if (t < ROX_SPOT)
        map = (t < ROX_LIGHT1) ? ROX_MAP_W2A : (k ? ROX_MAP_W2B : ROX_MAP_W2A);
    else if (t < ROX_DISC)
        map = k ? ROX_MAP_B : ROX_MAP_A;
    else
        map = k ? ROX_MAP_DB : ROX_MAP_DA;
    if (map >= 0 && map != task->tGiShown)
    {
        GI_ShowMap(map);
        task->tGiShown = map;
    }

    // spotlight: aan, even uit, weer aan (oude lamp); Roxanne komt uit het donker
    if (t == ROX_SPOT || t == ROX_SPOT + 5)
        sTransitionData->BLDCNT = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG_ALL | BLDCNT_TGT1_BD;
    if (t == ROX_SPOT + 2)
        sTransitionData->BLDCNT = 0;
    if (t == ROX_SPOT)
    {
        rox->invisible = FALSE;
        PlaySE(SE_SWITCH);
    }
    if (t >= ROX_SPOT && t <= ROX_SPOT + 8)
        BlendPalettes(GI_TrainerPalBit(TRAINER_PIC_LEADER_ROXANNE), (t == ROX_SPOT + 2 || t == ROX_SPOT + 3) ? 14 : 8 - (t - ROX_SPOT), RGB_BLACK);

    // de versterkers zakken (uitlopend) en veren na bij het neerkomen
    if (t >= ROX_AMP)
    {
        k = min(t - ROX_AMP, ROX_AMP_LEN);
        y = 78 - (ROX_AMP_LEN - k) * (ROX_AMP_LEN - k) * 118 / (ROX_AMP_LEN * ROX_AMP_LEN);
        if (t >= ROX_LAND && t - ROX_LAND < (s32)ARRAY_COUNT(sRoxAmpBounce))
            y += sRoxAmpBounce[t - ROX_LAND];
        gSprites[task->tGiSprite1].y = y;
        gSprites[task->tGiSprite2].y = y;
    }

    // geluid
    if (t == 0)
        PlaySE(SE_PC_OFF);
    if (t == ROX_WORD1)
        PlaySE(SE_M_SWAGGER);
    if (t == ROX_WORD2)
        PlaySE(SE_APPLAUSE);
    if (t == ROX_LIGHT1)
        PlaySE(SE_M_EMBER);
    if (t == ROX_AMP)
        PlaySE(SE_M_BIND);
    if (t == ROX_LAND)
        PlaySE(SE_M_STRENGTH);
    if (t == ROX_CHORD)
        PlaySE(SE_M_EXPLOSION);
    if (t == ROX_CHORD + 8)
        PlaySE(SE_APPLAUSE);

    // trillen bij het neerkomen en de powerchord
    if (t >= ROX_LAND && t < ROX_LAND + 8)
        k = 3;
    else if (t >= ROX_CHORD && t < ROX_CHORD + 14)
        k = 2;
    else
        k = 0;
    GI_Shake(k);
    rox->x2 = gSprites[task->tGiSprite1].x2 = gSprites[task->tGiSprite2].x2 = k ? (s16)(Random() % (k * 2 + 1)) - k : 0;

    // de wereld zwart (in de eerste frames uitfaden), flitsen wit
    if (t < ROX_DARK)
        BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, t, RGB_BLACK);
    else
        GI_FillField(keep, RGB_BLACK);
    if (t >= ROX_CHORD && t < ROX_CHORD + 10)
    {
        k = 12 - (t - ROX_CHORD) * 12 / 10;
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        sTransitionData->BLDCNT = (t & 1) ? 0 : (BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG_ALL | BLDCNT_TGT1_BD);
    }
    if (t == ROX_CHORD + 10)
        sTransitionData->BLDCNT = BLDCNT_EFFECT_LIGHTEN | BLDCNT_TGT1_BG_ALL | BLDCNT_TGT1_BD;
    if (t >= ROX_END - 4)
    {
        k = min((t - (ROX_END - 4)) * 4 + 4, 16);
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        if (t >= ROX_END)
        {
            // de sprites weg: de fade naar zwart wisselt BG en sprites af, anders zie je even silhouetten
            rox->invisible = gSprites[task->tGiSprite1].invisible = gSprites[task->tGiSprite2].invisible = TRUE;
            GI_EndWindow();
            return TRUE;
        }
    }
    return FALSE;
}

static void RTRoxanne_Finish(struct Task *task)
{
    GI_EndWindow();
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroySprite(task->tGiSprite1);
    GI_DestroySprite(task->tGiSprite2);
    GI_FreeTag(ROX_TAG_AMP);
    GI_Free();
}

static const struct RouteTransition sRT_GymRoxanne =
{
    sPikachu_Tileset, 32, sGymRoxanne_Pal + 32, 1, 1, 0, RTRoxanne_Init, RTRoxanne_Update, RTRoxanne_Finish
};

static void Task_GymRoxanne(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymRoxanne);
}

// ---------------- Brawly (UFC: "Let me see if you're worth the contract!"): de walkout door de spelerstunnel (lichtringen
// razen op je af via een paletcyclus, het beeld deint mee met de passen, LIVE in de hoek), wit de arena in, Brawly in de
// octagon met cameraflitsen in het publiek, de omroeperbalk "BRAWLY - DOUBLE CHAMP" schuift in beeld. Dan close-up van
// het kooigaas: zijn vuist komt van achter het gaas (sprite achter BG0) op de camera af, het gaas bolt en de klap flitst.
// tools/grounded/brawly_transition.py
static const u32 sGymBrawly_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_brawly.4bpp.smol");
static const u32 sGymBrawly_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_brawly_maps.bin.smol");
static const u16 sGymBrawly_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_brawly.gbapal");
static const u32 sGymBrawly_FlashGfx[] = INCBIN_U32("graphics/battle_transitions/gym_brawly_flash.4bpp.smol");
static const u16 sGymBrawly_FlashPal[] = INCBIN_U16("graphics/battle_transitions/gym_brawly_flash.gbapal");
static const u32 sGymBrawly_FistGfx[] = INCBIN_U32("graphics/battle_transitions/gym_brawly_fist.4bpp.smol");
static const u16 sGymBrawly_FistPal[] = INCBIN_U16("graphics/battle_transitions/gym_brawly_fist.gbapal");

enum { BRAWLY_MAP_TUNNEL, BRAWLY_MAP_OCTAGON, BRAWLY_MAP_ATLAS, BRAWLY_MAP_MESH, BRAWLY_MAP_DENT };
#define BRAWLY_TAG_FIST   0x5A31
#define BRAWLY_TAG_IMPACT 0x5A32
#define BRAWLY_TAG_FLASH  0x5A38
#define BRAWLY_TUNNEL     6
#define BRAWLY_WHITE      52    // het licht aan het eind van de tunnel
#define BRAWLY_ARENA      62
#define BRAWLY_BANNER     78
#define BRAWLY_WINDUP     132
#define BRAWLY_CLOSE      140   // close-up van het gaas
#define BRAWLY_HIT        148
#define BRAWLY_END        (BRAWLY_HIT + 28)

static const s8 sBrawlyBob[16] = {0, 1, 2, 2, 3, 2, 2, 1, 0, -1, -1, -2, -2, -2, -1, -1};
// cameraflitsen: plekken (in vakken) in het publiek en het gaas
static const u8 sBrawlyFlashPos[][2] = {
    {3, 1}, {22, 3}, {11, 0}, {27, 5}, {6, 4}, {17, 1}, {1, 6}, {24, 0}, {14, 3}, {8, 1}, {20, 6}, {26, 2}, {4, 2}, {12, 5}, {18, 4}, {9, 6},
};

static void RTBrawly_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sGymBrawly_Tiles, sGymBrawly_Maps);
    LoadPalette(sGymBrawly_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_BRAWLY, 120, 76);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_CreateSprite(sGymBrawly_FistGfx, 64 * 64 / 2, sGymBrawly_FistPal, BRAWLY_TAG_FIST, &sGI_Oam64Affine, 120, 84, 1);
    gSprites[task->tGiSprite1].oam.priority = 1; // achter het gaas (BG0)
    gSprites[task->tGiSprite1].invisible = TRUE;
    task->tGiSprite2 = GI_CreateSprite(gBattleAnimSpriteGfx_PunchImpact, 32 * 32 / 2, gBattleAnimSpritePal_PunchImpact, BRAWLY_TAG_IMPACT, &sGI_Oam32Affine, 120, 80, 0);
    gSprites[task->tGiSprite2].invisible = TRUE;
    for (i = 0; i < 3; i++)
    {
        task->data[12 + i] = GI_CreateSprite(sGymBrawly_FlashGfx, 16 * 32 / 2, sGymBrawly_FlashPal, BRAWLY_TAG_FLASH, &sGI_Oam16, 0, 0, 0);
        gSprites[task->data[12 + i]].invisible = TRUE;
    }
    task->tGiShown = 0xFF;
}

static bool8 RTBrawly_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, x, sc;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *brawly = &gSprites[task->tGiSprite0];
    struct Sprite *fist = &gSprites[task->tGiSprite1];
    struct Sprite *impact = &gSprites[task->tGiSprite2];

    LoadPalette(sGymBrawly_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_BRAWLY) | GI_SpritePalBit(BRAWLY_TAG_FIST) | GI_SpritePalBit(BRAWLY_TAG_IMPACT)
         | GI_SpritePalBit(BRAWLY_TAG_FLASH);
    GI_ResetPals(keep);

    if (t < BRAWLY_ARENA)
    {
        // tunnel: de felle ring schuift elke 3 frames een stap naar voren (index 4-7), het beeld deint met de passen
        k = (t / 3) & 3;
        for (i = 0; i < 4; i++)
            pal[4 + i] = sGymBrawly_Pal[4 + ((i + k) & 3)];
        CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);
        if (t == BRAWLY_TUNNEL)
        {
            GI_KillFieldWindows();
            GI_ShowMap(BRAWLY_MAP_TUNNEL);
            PlaySE(SE_APPLAUSE);
        }
        SetGpuReg(REG_OFFSET_BG0VOFS, sBrawlyBob[t & 15] & 0x1FF);
        if (t < BRAWLY_TUNNEL)
            BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, t * 3, RGB_BLACK);
        else
            GI_FillField(keep, RGB_BLACK);
        if (t >= BRAWLY_WHITE)
        {
            k = min((t - BRAWLY_WHITE) * 2, 16);
            BlendPalettes(GI_BG_PALS, k, RGB_WHITE);
            GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        }
        return FALSE;
    }

    if (t < BRAWLY_CLOSE)
    {
        // de octagon
        if (t == BRAWLY_ARENA)
        {
            SetGpuReg(REG_OFFSET_BG0VOFS, 0);
            GI_ShowMap(BRAWLY_MAP_OCTAGON);
            brawly->invisible = FALSE;
            PlaySE(SE_M_ENCORE);
        }
        // cameraflitsen (drie sprites): elk 2 frames aan, 5 uit, steeds op een andere plek; af en toe flitst het hele beeld
        for (i = 0; i < 3; i++)
        {
            struct Sprite *fl = &gSprites[task->data[12 + i]];
            k = t - BRAWLY_ARENA - 6 - i * 3;
            if (k < 0)
                continue;
            if (k % 7 == 0)
            {
                x = (k / 7 * 3 + i * 5) % ARRAY_COUNT(sBrawlyFlashPos);
                fl->x = sBrawlyFlashPos[x][0] * 8 + 8;
                fl->y = sBrawlyFlashPos[x][1] * 8 + 8;
                fl->oam.tileNum = GetSpriteTileStartByTag(BRAWLY_TAG_FLASH) + ((k / 7 + i) & 1) * 4;
            }
            fl->invisible = (k % 7) >= 2;
        }
        if (t >= BRAWLY_ARENA + 6 && (t % 17) == 0)
            PlaySE(SE_CLICK);
        // de omroeperbalk schuift van links in beeld
        if (t >= BRAWLY_BANNER)
        {
            x = min((t - BRAWLY_BANNER) * 5, 30) - 30;
            GI_ShowRows(BRAWLY_MAP_OCTAGON, 14, 19);
            GI_PutRect(BRAWLY_MAP_ATLAS, 0, 0, 30, 5, x, 14);
            if (t == BRAWLY_BANNER)
                PlaySE(SE_M_RAZOR_WIND);
        }
        // Brawly veert in zijn stance, haalt aan het eind uit
        brawly->y2 = ((t >> 3) & 1) ? -1 : 0;
        brawly->x2 = 0;
        if (t >= BRAWLY_WINDUP)
        {
            brawly->x2 = min(t - BRAWLY_WINDUP, 4);
            if (t == BRAWLY_WINDUP)
                PlaySE(SE_M_COMET_PUNCH);
        }
        GI_FillField(keep, RGB_BLACK);
        if (t < BRAWLY_ARENA + 8)
        {
            k = 16 - (t - BRAWLY_ARENA) * 2;
            BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        }
        if (t >= BRAWLY_ARENA + 6 && (t % 23) == 0)
            BlendPalettes(GI_BG_PALS | keep, 6, RGB_WHITE);
        return FALSE;
    }

    // close-up: de vuist komt van achter het gaas op je af, klap, het gaas bolt
    if (t == BRAWLY_CLOSE)
    {
        GI_ShowMap(BRAWLY_MAP_MESH);
        brawly->invisible = TRUE;
        for (i = 0; i < 3; i++)
            gSprites[task->data[12 + i]].invisible = TRUE;
        fist->invisible = FALSE;
    }
    if (t < BRAWLY_HIT)
    {
        k = t - BRAWLY_CLOSE;
        sc = 64 + k * k * 448 / 49;
        SetOamMatrixRotationScaling(fist->oam.matrixNum, sc, sc, (u16)(0x10000 - 0x0400 + k * 0x80));
    }
    if (t == BRAWLY_HIT)
    {
        GI_ShowMap(BRAWLY_MAP_DENT);
        SetOamMatrixRotationScaling(fist->oam.matrixNum, 512, 512, 0);
        impact->invisible = FALSE;
        SetOamMatrixRotationScaling(impact->oam.matrixNum, 512, 512, 0);
        PlaySE(SE_M_MEGA_KICK);
    }
    if (t >= BRAWLY_HIT)
    {
        k = t - BRAWLY_HIT;
        if (k == 6)
            impact->invisible = TRUE;
        GI_Shake(k < 10 ? 4 - k / 3 : 0);
        fist->x2 = impact->x2 = (k < 10) ? (s16)(Random() % 7) - 3 : 0;
    }
    GI_FillField(keep, RGB_BLACK);
    if (t >= BRAWLY_HIT && t < BRAWLY_HIT + 5)
    {
        k = 12 - (t - BRAWLY_HIT) * 3;
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
    }
    if (t >= BRAWLY_END - 4)
    {
        k = min((t - (BRAWLY_END - 4)) * 4 + 4, 16);
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        if (t >= BRAWLY_END)
            brawly->invisible = fist->invisible = impact->invisible = TRUE;
        return t >= BRAWLY_END;
    }
    return FALSE;
}

static void RTBrawly_Finish(struct Task *task)
{
    u32 i;

    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroySprite(task->tGiSprite1);
    GI_DestroySprite(task->tGiSprite2);
    GI_FreeTag(BRAWLY_TAG_FIST);
    GI_FreeTag(BRAWLY_TAG_IMPACT);
    for (i = 0; i < 3; i++)
        GI_DestroySprite(task->data[12 + i]);
    GI_FreeTag(BRAWLY_TAG_FLASH);
    GI_Free();
}

static const struct RouteTransition sRT_GymBrawly =
{
    sPikachu_Tileset, 32, sGymBrawly_Pal + 32, 1, 1, 0, RTBrawly_Init, RTBrawly_Update, RTBrawly_Finish
};

static void Task_GymBrawly(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymBrawly);
}

// ---------------- Wattson: alles is een scam. Harde cut naar de serverfarm (ledjes knipperen, de 'rigged door' van de
// Mauville-gym knettert), een spervuur van pop-ups, de WATTCOIN-koers schiet naar de maan en crasht (-99%, RUGPULLED),
// nog meer pop-ups, een SCAM-stempel slaat erop, Wattson komt lachend omhoog: "Wahahahah!", dan hapert het beeld.
// tools/grounded/wattson_transition.py
static const u32 sGymWattson_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_wattson.4bpp.smol");
static const u32 sGymWattson_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_wattson_maps.bin.smol");
static const u16 sGymWattson_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_wattson.gbapal");
static const u32 sGymWattson_ScamGfx[] = INCBIN_U32("graphics/battle_transitions/gym_wattson_scam.4bpp.smol");
static const u16 sGymWattson_ScamPal[] = INCBIN_U16("graphics/battle_transitions/gym_wattson_scam.gbapal");

enum { WATT_MAP_SERVERS, WATT_MAP_ATLAS0, WATT_MAP_ATLAS1, WATT_MAP_CHART0, WATT_MAP_CHART1, WATT_MAP_CHART2 };
enum { WATT_POP_WINNER, WATT_POP_COIN, WATT_POP_MAGNE, WATT_POP_DOOR, WATT_POP_VIRUS, WATT_POP_LIKE, WATT_POP_CODE, WATT_POP_HODL };
#define WATT_TAG_SCAM   0x5A33
#define WATT_CHART      62
#define WATT_DRAW       66
#define WATT_DRAW_LEN   40
#define WATT_CRASH      (WATT_DRAW + WATT_DRAW_LEN)
#define WATT_SPAM       (WATT_CRASH + 8)
#define WATT_STAMP      144
#define WATT_RISE       152
#define WATT_LAUGH      160
#define WATT_GLITCH     194
#define WATT_END        (WATT_GLITCH + 12)

// pop-ups in atlas 0: kolom, rij, breedte, hoogte
static const u8 sWattPopup[][4] = {
    [WATT_POP_WINNER] = {0, 0, 15, 6},
    [WATT_POP_COIN] = {15, 0, 13, 7},
    [WATT_POP_MAGNE] = {0, 6, 15, 5},
    [WATT_POP_DOOR] = {15, 7, 14, 5},
    [WATT_POP_VIRUS] = {0, 11, 15, 5},
    [WATT_POP_LIKE] = {15, 12, 13, 4},
    [WATT_POP_CODE] = {0, 16, 13, 4},
    [WATT_POP_HODL] = {15, 16, 8, 4},
};
// wanneer welke pop-up waar verschijnt (frame, pop-up, kolom, rij)
static const u8 sWattSpam[][4] = {
    {10, WATT_POP_WINNER, 1, 1},
    {17, WATT_POP_COIN, 16, 2},
    {24, WATT_POP_MAGNE, 3, 8},
    {31, WATT_POP_DOOR, 15, 9},
    {38, WATT_POP_VIRUS, 6, 4},
    {45, WATT_POP_LIKE, 17, 14},
    {52, WATT_POP_CODE, 1, 14},
    {WATT_SPAM + 0, WATT_POP_HODL, 21, 1},
    {WATT_SPAM + 3, WATT_POP_COIN, 0, 0},
    {WATT_SPAM + 6, WATT_POP_WINNER, 14, 6},
    {WATT_SPAM + 9, WATT_POP_HODL, 2, 10},
    {WATT_SPAM + 12, WATT_POP_VIRUS, 13, 13},
    {WATT_SPAM + 15, WATT_POP_LIKE, 4, 3},
    {WATT_SPAM + 18, WATT_POP_DOOR, 1, 13},
    {WATT_SPAM + 21, WATT_POP_HODL, 22, 9},
    {WATT_SPAM + 24, WATT_POP_MAGNE, 9, 7},
    {WATT_SPAM + 27, WATT_POP_CODE, 16, 1},
};

static void RTWattson_Init(struct Task *task)
{
    GI_LoadGfx(sGymWattson_Tiles, sGymWattson_Maps);
    LoadPalette(sGymWattson_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_WATTSON, 196, 200);
    task->tGiSprite1 = GI_CreateSprite(sGymWattson_ScamGfx, 64 * 32 / 2, sGymWattson_ScamPal, WATT_TAG_SCAM, &sGI_Oam64Affine, 112, 64, 0);
    gSprites[task->tGiSprite1].oam.shape = SPRITE_SHAPE(64x32);
    gSprites[task->tGiSprite1].oam.size = SPRITE_SIZE(64x32);
    CalcCenterToCornerVec(&gSprites[task->tGiSprite1], SPRITE_SHAPE(64x32), SPRITE_SIZE(64x32), ST_OAM_AFFINE_DOUBLE);
    gSprites[task->tGiSprite1].invisible = TRUE;
    PlaySE(SE_PC_LOGIN);
}

static bool8 RTWattson_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, c, reveal;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *watt = &gSprites[task->tGiSprite0];
    struct Sprite *scam = &gSprites[task->tGiSprite1];

    // ledjes (BG 13 index 6-8) knipperen elk in hun eigen ritme, de barrière (BG 15 index 1) knettert
    LoadPalette(sGymWattson_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    for (i = 0; i < 3; i++)
        if (((t + i * 5) / (3 + i)) & 1)
            pal[6 + i] = RGB(4, 4, 8);
    k = (t >> 1) % 3;
    pal[32 + 1] = (k == 0) ? RGB(31, 31, 31) : (k == 1) ? RGB(0, 31, 31) : RGB(6, 14, 20);
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);
    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_WATTSON) | GI_SpritePalBit(WATT_TAG_SCAM);
    GI_ResetPals(keep);
    // harde cut: de wereld gaat in frame 0 op zwart, de serverfarm komt een frame later (als de paletten er staan)
    if (t == 1)
    {
        GI_KillFieldWindows();
        GI_ShowMap(WATT_MAP_SERVERS);
    }

    // pop-ups
    for (i = 0; i < (s32)ARRAY_COUNT(sWattSpam); i++)
    {
        if (sWattSpam[i][0] != t)
            continue;
        k = sWattSpam[i][1];
        GI_PutRect(WATT_MAP_ATLAS0, sWattPopup[k][0], sWattPopup[k][1], sWattPopup[k][2], sWattPopup[k][3], sWattSpam[i][2], sWattSpam[i][3]);
        PlaySE(k == WATT_POP_COIN ? SE_SHOP : SE_SELECT);
    }

    // de koersgrafiek: venster, dan kolom voor kolom de lijn (omhoog), de crash, dan de labels
    if (t == WATT_CHART)
    {
        GI_PutRect(WATT_MAP_CHART0, 3, 2, 24, 11, 3, 2);
        PlaySE(SE_PC_ON);
    }
    if (t >= WATT_DRAW && t <= WATT_CRASH)
    {
        reveal = 3 + (t - WATT_DRAW) * 24 / WATT_DRAW_LEN;
        for (c = 3; c < reveal && c < 27; c++)
            GI_PutRect(WATT_MAP_CHART1, c, 3, 1, 10, c, 3);
        if (t == WATT_DRAW)
            PlaySE(SE_M_STAT_INCREASE);
        if (t == WATT_CRASH - 6)
            PlaySE(SE_M_STAT_DECREASE);
    }
    if (t == WATT_CRASH)
    {
        GI_PutRect(WATT_MAP_CHART2, 3, 2, 24, 11, 3, 2);
        PlaySE(SE_FAILURE);
    }

    // SCAM-stempel: groot en scheef erop, dan vast
    if (t >= WATT_STAMP)
    {
        k = min(t - WATT_STAMP, 5);
        scam->invisible = FALSE;
        SetOamMatrixRotationScaling(scam->oam.matrixNum, 512 - k * 48, 512 - k * 48, 0x0A00);
        if (t == WATT_STAMP + 5)
            PlaySE(SE_BANG);
    }

    // Wattson komt lachend omhoog, met de tekstballon
    if (t >= WATT_RISE)
    {
        k = min(t - WATT_RISE, 8);
        watt->y = 200 - k * 10;
        watt->y2 = (t >= WATT_LAUGH && ((t >> 2) & 1)) ? -2 : 0;
        if (t == WATT_LAUGH)
        {
            GI_PutRect(WATT_MAP_ATLAS1, 12, 12, 12, 3, 12, 12);
            PlaySE(SE_SHOP);
        }
    }

    // trillen: crash, stempel, haperend beeld aan het eind
    if ((t >= WATT_CRASH && t < WATT_CRASH + 8) || (t >= WATT_STAMP + 5 && t < WATT_STAMP + 11))
        GI_Shake(2);
    else if (t >= WATT_GLITCH)
    {
        SetGpuReg(REG_OFFSET_BG0HOFS, (Random() % 48) - 24);
        SetGpuReg(REG_OFFSET_BG0VOFS, (Random() % 9) - 4);
        if (t == WATT_GLITCH)
            PlaySE(SE_PC_OFF);
    }
    else
        GI_Shake(0);

    GI_FillField(keep, RGB_BLACK);
    if (t >= WATT_CRASH && t < WATT_CRASH + 8)
        BlendPalettes(GI_BG_PALS, 8 - (t - WATT_CRASH), RGB(31, 0, 0));
    if (t >= WATT_GLITCH && (t & 1))
        BlendPalettes(GI_BG_PALS | keep, 6, RGB(0, 31, 31));
    if (t >= WATT_END - 4)
    {
        k = min((t - (WATT_END - 4)) * 4 + 4, 16);
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        if (t >= WATT_END)
            watt->invisible = scam->invisible = TRUE;
        return t >= WATT_END;
    }
    return FALSE;
}

static void RTWattson_Finish(struct Task *task)
{
    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroySprite(task->tGiSprite1);
    GI_FreeTag(WATT_TAG_SCAM);
    GI_Free();
}

static const struct RouteTransition sRT_GymWattson =
{
    sPikachu_Tileset, 32, sGymWattson_Pal + 32, 1, 1, 0, RTWattson_Init, RTWattson_Update, RTWattson_Finish
};

static void Task_GymWattson(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymWattson);
}

// ---------------- Flannery: een camping in de schemering (rood tentje met de Poké Ball van de Red Tent, kampvuur, bordje
// "NO WIFI. JUST ANALOG HEAT."), op de achtergrond Mt. Chimney. De grond rommelt, de vulkaan ontploft (Fire Plume op de
// krater, lavabommen, de lucht kleurt rood), Flannery: "Totally planned!", en een stuk vulkanisch gesteente vliegt recht
// op de camera af: de lens barst. tools/grounded/flannery_transition.py
static const u32 sGymFlannery_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_flannery.4bpp.smol");
static const u32 sGymFlannery_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_flannery_maps.bin.smol");
static const u16 sGymFlannery_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_flannery.gbapal");
static const u16 sGymFlannery_RockPal[] = INCBIN_U16("graphics/battle_transitions/gym_flannery_rock.gbapal");

enum { FLAN_MAP_CAMP, FLAN_MAP_CRACK, FLAN_MAP_BUBBLE };
#define FLAN_TAG_FIRE    0x5A34
#define FLAN_TAG_PLUME   0x5A35
#define FLAN_TAG_BOMB    0x5A36
#define FLAN_TAG_ROCK    0x5A37
#define FLAN_CAMP        8
#define FLAN_RUMBLE      48
#define FLAN_ERUPT       86
#define FLAN_BUBBLE      104
#define FLAN_ROCK        118
#define FLAN_ROCK_LEN    24
#define FLAN_HIT         (FLAN_ROCK + FLAN_ROCK_LEN)
#define FLAN_END         (FLAN_HIT + 30)
#define FLAN_BOMBS       4
#define FLAN_CRATER_X    176
#define FLAN_CRATER_Y    36

// lavabommen: startframe, vx en vy (1/16 px per frame), grootte (frame in Warm Rock)
static const s16 sFlanBomb[FLAN_BOMBS][4] = {
    {FLAN_ERUPT + 4, -40, -88, 1},
    {FLAN_ERUPT + 8, 30, -100, 2},
    {FLAN_ERUPT + 12, -72, -72, 2},
    {FLAN_ERUPT + 16, 56, -84, 3},
};

static const struct OamData sGI_Oam32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(32x32),
    .size = SPRITE_SIZE(32x32),
    .priority = 0,
};

static void RTFlannery_Init(struct Task *task)
{
    u32 i;
    u8 id;

    GI_LoadGfx(sGymFlannery_Tiles, sGymFlannery_Maps);
    LoadPalette(sGymFlannery_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_FLANNERY, 208, 110);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_CreateSprite(gBattleAnimSpriteGfx_Fire, 32 * 256 / 2, gBattleAnimSpritePal_Fire, FLAN_TAG_FIRE, &sGI_Oam32, 168, 132, 1);
    gSprites[task->tGiSprite1].invisible = TRUE;
    // de pluim deelt het palet van het kampvuur (zuinig met OBJ-paletten: drukke kaarten zoals het Stadium)
    task->tGiSprite2 = GI_CreateSprite2(gBattleAnimSpriteGfx_FirePlume, 32 * 160 / 2, gBattleAnimSpritePal_Fire, FLAN_TAG_PLUME, FLAN_TAG_FIRE, &sGI_Oam32Affine, FLAN_CRATER_X, FLAN_CRATER_Y - 20, 2);
    gSprites[task->tGiSprite2].invisible = TRUE;
    SetOamMatrixRotationScaling(gSprites[task->tGiSprite2].oam.matrixNum, 512, 512, 0);
    task->tGiSprite3 = GI_CreateSprite(gBattleAnimSpriteGfx_BigRock, 64 * 64 / 2, sGymFlannery_RockPal, FLAN_TAG_ROCK, &sGI_Oam64Affine, FLAN_CRATER_X, FLAN_CRATER_Y, 0);
    gSprites[task->tGiSprite3].invisible = TRUE;
    // lavabommen: vier sprites, hun id's in data[12-15]
    for (i = 0; i < FLAN_BOMBS; i++)
    {
        id = GI_CreateSprite(gBattleAnimSpriteGfx_WarmRock, 32 * 168 / 2, gBattleAnimSpritePal_WarmRock, FLAN_TAG_BOMB, &sGI_Oam32, FLAN_CRATER_X, FLAN_CRATER_Y, 2);
        gSprites[id].invisible = TRUE;
        gSprites[id].oam.tileNum += sFlanBomb[i][3] * 16;
        task->data[12 + i] = id;
    }
    BlendPalettes(GI_BG_PALS, 16, RGB_BLACK);
}

static bool8 RTFlannery_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, dt, sc;
    u32 keep;
    struct Sprite *flan = &gSprites[task->tGiSprite0];
    struct Sprite *fire = &gSprites[task->tGiSprite1];
    struct Sprite *plume = &gSprites[task->tGiSprite2];
    struct Sprite *rock = &gSprites[task->tGiSprite3];
    struct Sprite *bomb;

    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_FLANNERY) | GI_SpritePalBit(FLAN_TAG_FIRE) | GI_SpritePalBit(FLAN_TAG_BOMB) | GI_SpritePalBit(FLAN_TAG_ROCK);
    GI_ResetPals(keep);
    LoadPalette(sGymFlannery_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    if (t < FLAN_CAMP)
    {
        BlendPalettes(PALETTES_ALL & ~GI_BG_PALS & ~keep, t * 2, RGB_BLACK);
        BlendPalettes(GI_BG_PALS, 16, RGB_BLACK);
        return FALSE;
    }
    if (t == FLAN_CAMP)
    {
        GI_KillFieldWindows();
        GI_ShowMap(FLAN_MAP_CAMP);
        flan->invisible = FALSE;
        fire->invisible = FALSE;
        PlaySE(SE_M_EMBER);
    }

    // kampvuur (8 frames Fire), lavagloed op de krater
    fire->oam.tileNum = GetSpriteTileStartByTag(FLAN_TAG_FIRE) + ((t >> 2) & 7) * 16;
    if ((t >> 3) & 1)
        gPlttBufferUnfaded[BG_PLTT_ID(13) + 8] = RGB(31, 20, 6);
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(13)], &gPlttBufferFaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);

    // de grond rommelt, dan de uitbarsting
    if (t == FLAN_RUMBLE)
        PlaySE(SE_M_EARTHQUAKE);
    if (t >= FLAN_ERUPT)
    {
        dt = t - FLAN_ERUPT;
        if (t == FLAN_ERUPT)
        {
            plume->invisible = FALSE;
            PlaySE(SE_M_EXPLOSION);
        }
        k = dt / 4;
        if (k > 4)
            k = 2 + (k & 1);
        plume->oam.tileNum = GetSpriteTileStartByTag(FLAN_TAG_PLUME) + k * 16;
        // de lucht kleurt rood (BG 13 index 1-5 en de lucht in BG 14 = index 1-3), de krater gloeit fel
        k = min(dt / 2, 8);
        BlendPalette(BG_PLTT_ID(13) + 1, 5, k, RGB(31, 6, 0));
        BlendPalette(BG_PLTT_ID(14) + 1, 3, k, RGB(31, 6, 0));
        gPlttBufferFaded[BG_PLTT_ID(13) + 8] = RGB(31, 24, 8);
        gPlttBufferFaded[BG_PLTT_ID(13) + 9] = RGB(31, 31, 20);
        // lavabommen in een boog
        for (i = 0; i < FLAN_BOMBS; i++)
        {
            bomb = &gSprites[task->data[12 + i]];
            k = t - sFlanBomb[i][0];
            if (k < 0)
                continue;
            bomb->invisible = FALSE;
            bomb->x = FLAN_CRATER_X + sFlanBomb[i][1] * k / 16;
            bomb->y = FLAN_CRATER_Y + (sFlanBomb[i][2] * k + 6 * k * k) / 16;
            if (bomb->y > 176)
                bomb->invisible = TRUE;
        }
    }

    // "Totally planned!"
    if (t == FLAN_BUBBLE)
        GI_PutRect(FLAN_MAP_BUBBLE, 13, 7, 13, 3, 13, 7);
    if (t >= FLAN_BUBBLE && t < FLAN_ROCK)
        flan->y2 = ((t >> 2) & 1) ? -1 : 0;

    // de steen komt op de camera af (groeit, draait), dan barst de lens
    if (t >= FLAN_ROCK)
    {
        k = min(t - FLAN_ROCK, FLAN_ROCK_LEN);
        rock->invisible = FALSE;
        sc = 40 + k * k * 472 / (FLAN_ROCK_LEN * FLAN_ROCK_LEN);
        rock->x = FLAN_CRATER_X + (120 - FLAN_CRATER_X) * k / FLAN_ROCK_LEN;
        rock->y = FLAN_CRATER_Y + (80 - FLAN_CRATER_Y) * k / FLAN_ROCK_LEN;
        SetOamMatrixRotationScaling(rock->oam.matrixNum, sc, sc, (u16)(k * 0x500));
        if (t == FLAN_ROCK)
            PlaySE(SE_FALL);
    }
    if (t == FLAN_HIT)
    {
        GI_ShowMap(FLAN_MAP_CRACK);
        PlaySE(SE_ICE_BREAK);
    }

    // trillen
    if (t >= FLAN_RUMBLE && t < FLAN_ERUPT)
        GI_Shake(1);
    else if (t >= FLAN_ERUPT && t < FLAN_ERUPT + 12)
        GI_Shake(3);
    else if (t >= FLAN_HIT && t < FLAN_HIT + 12)
        GI_Shake(4 - (t - FLAN_HIT) / 4);
    else
        GI_Shake(0);
    k = (t >= FLAN_HIT && t < FLAN_HIT + 12) ? (s16)(Random() % 5) - 2 : 0;
    rock->x2 = flan->x2 = k;

    GI_FillField(keep, RGB_BLACK);
    if (t < FLAN_CAMP + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - FLAN_CAMP) * 2, RGB_BLACK);
    if (t >= FLAN_ERUPT && t < FLAN_ERUPT + 6)
        BlendPalettes(GI_BG_PALS | keep, 10 - (t - FLAN_ERUPT) * 2, RGB(31, 28, 16));
    if (t >= FLAN_HIT && t < FLAN_HIT + 8)
    {
        k = 14 - (t - FLAN_HIT) * 2;
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
    }
    if (t >= FLAN_END - 4)
    {
        k = min((t - (FLAN_END - 4)) * 4 + 4, 16);
        BlendPalettes(GI_BG_PALS | keep, k, RGB_WHITE);
        GI_FillField(keep, RGB(k * 31 / 16, k * 31 / 16, k * 31 / 16));
        if (t >= FLAN_END)
        {
            flan->invisible = fire->invisible = plume->invisible = rock->invisible = TRUE;
            for (i = 0; i < FLAN_BOMBS; i++)
                gSprites[task->data[12 + i]].invisible = TRUE;
        }
        return t >= FLAN_END;
    }
    return FALSE;
}

static void RTFlannery_Finish(struct Task *task)
{
    u32 i;
    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroySprite(task->tGiSprite1);
    GI_DestroySprite(task->tGiSprite2);
    GI_DestroySprite(task->tGiSprite3);
    for (i = 0; i < FLAN_BOMBS; i++)
        GI_DestroySprite(task->data[12 + i]);
    GI_FreeTag(FLAN_TAG_FIRE);
    GI_FreeTag(FLAN_TAG_PLUME);
    GI_FreeTag(FLAN_TAG_BOMB);
    GI_FreeTag(FLAN_TAG_ROCK);
    GI_Free();
}

static const struct RouteTransition sRT_GymFlannery =
{
    sPikachu_Tileset, 32, sGymFlannery_Pal + 32, 1, 1, 0, RTFlannery_Init, RTFlannery_Update, RTFlannery_Finish
};

static void Task_GymFlannery(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymFlannery);
}
