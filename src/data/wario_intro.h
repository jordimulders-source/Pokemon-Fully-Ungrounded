// Project Grounded: gevechtsintro van Wario (Yoshi's Island-fort, en als gast in het Battle Stadium), v2 in WarioWare-
// stijl. Jordi: "maak het heel goofy en Wario Ware achtig", "kijk in Wario Ware naar de filmpjes die er al in zitten",
// "Wario moet echt als een soort gekke superheld/alleskunner uit de intro komen".
// Een razendsnelle reeks microgames, elk met een opdracht in grote letters en onderin de WarioWare-timer (een bom met
// een brandende lont): EAT! (Wario op de bank uit de openingsfilm eet een knoflookbol in drie happen), INVENT! (Wario
// aan zijn bureau met dollartekens in de ogen en het Game-idee in een denkwolk), FLY! (Wario die door de lucht vliegt,
// uit het verhaalfilmpje), FLEX! (de dubbele biceps). De lont is op: BOEM. WIN!: de grote close-up-grijns ("Think you
// can beat my games?"), sterren, en dan de W als superheldenembleem die het beeld overneemt.
// Wordt na src/data/legend_intros2.h ingevoegd (GI_/LI_/LI2_-hulpjes). Art: tools/grounded/wario_intro.py; de WarioWare-
// art is schoon uit VRAM/OAM gerenderd (tools/grounded/warioware_rip.py). BG-set A (kaarten, close-up) in palet 10-15,
// BG-set B (het embleem) in palet 13-15, pas geladen als het embleem komt.
static const u32 sWarioIntro_Tiles[] = INCBIN_U32("graphics/battle_transitions/wario_intro.4bpp.smol");
static const u32 sWarioIntro_Maps[] = INCBIN_U32("graphics/battle_transitions/wario_intro_maps.bin.smol");
static const u16 sWarioIntro_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_intro.gbapal");
static const u32 sWarioCrest_Tiles[] = INCBIN_U32("graphics/battle_transitions/wario_crest.4bpp.smol");
static const u32 sWarioCrest_Maps[] = INCBIN_U32("graphics/battle_transitions/wario_crest_maps.bin.smol");
static const u16 sWarioCrest_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_crest.gbapal");
static const u32 sWarioCouch_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_couch.4bpp.smol");
static const u16 sWarioCouch_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_couch.gbapal");
static const u32 sWarioCash_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_cash.4bpp.smol");
static const u16 sWarioCash_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_cash.gbapal");
static const u32 sWarioFly_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_fly.4bpp.smol");
static const u16 sWarioFly_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_fly.gbapal");
static const u32 sWarioFlex_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_flex.4bpp.smol");
static const u16 sWarioFlex_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_flex.gbapal");
static const u32 sWarioGarlic_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_garlic.4bpp.smol");
static const u16 sWarioGarlic_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_garlic.gbapal");
static const u32 sWarioSpark_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_spark.4bpp.smol");
static const u16 sWarioSpark_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_spark.gbapal");
static const u32 sWarioBoom_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_boom.4bpp.smol");
static const u16 sWarioBoom_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_boom.gbapal");

enum { WAR_MAP_EAT, WAR_MAP_INVENT, WAR_MAP_FLY, WAR_MAP_FLEX, WAR_MAP_BAR, WAR_MAP_FACE };
enum { WAR_MAP_CREST, WAR_MAP_CREST_BIG, WAR_MAP_CREST_HUGE };
#define WAR_TAG_BIG     0x5A80   // tiles van het grote object van deze kaart
#define WAR_TAG_BIGPAL  0x5A81   // t/m 0x5A84: de vier kwadrantpaletten
#define WAR_TAG_GARLIC  0x5A85
#define WAR_TAG_SPARK   0x5A86
#define WAR_TAG_BOOM    0x5A87
#define WAR_TAG_STAR    0x5A88
#define WAR_SHOW        8
#define WAR_CARD        (WAR_SHOW + 1)   // vier kaarten van WAR_CARD_LEN frames
#define WAR_CARD_LEN    26
#define WAR_BOOM        (WAR_CARD + 4 * WAR_CARD_LEN - 4)
#define WAR_FACE        (WAR_CARD + 4 * WAR_CARD_LEN)
#define WAR_CREST       (WAR_FACE + 22)
#define WAR_END         (WAR_CREST + 16)
#define WAR_STARS       6
// slots in sLI_Spr: 0-3 groot object, 4-7 tweede frame (vliegen), 8 knoflook, 9 vonk, 10 boem, 11-16 sterren
#define WAR_S_GARLIC    8
#define WAR_S_SPARK     9
#define WAR_S_BOOM      10
#define WAR_S_STAR      11

static const u16 sWarBurst[8] = {RGB(31, 28, 6), RGB(30, 24, 3), RGB(16, 6, 22), RGB(12, 3, 18),
                                 RGB(31, 28, 6), RGB(30, 24, 3), RGB(16, 6, 22), RGB(12, 3, 18)};
static const s8 sWarStar[WAR_STARS][2] = {{-70, -40}, {64, -50}, {-84, 20}, {80, 14}, {-40, 52}, {48, 48}};

static void WarBigFree(void)
{
    u32 i;
    for (i = 0; i < 8; i++)
    {
        if (sLI_Spr[i] < MAX_SPRITES)
            GI_DestroySprite(sLI_Spr[i]);
        sLI_Spr[i] = MAX_SPRITES;
    }
    FreeSpriteTilesByTag(WAR_TAG_BIG);
    for (i = 0; i < 4; i++)
        FreeSpritePaletteByTag(WAR_TAG_BIGPAL + i);
}

// een groot object (128 x 128, vier 64x64-sprites met elk een eigen palet), 'frames' standen in de sheet; voor elke
// stand vier slots (stand 0: 0-3, stand 1: 4-7)
static void WarBigMake(const u32 *gfx, const u16 *pal, u32 frames)
{
    u32 f, q;
    WarBigFree();
    for (f = 0; f < frames; f++)
    {
        for (q = 0; q < 4; q++)
        {
            u8 id = GI_CreateSprite2(gfx, frames * LI2_BIG_SIZE, pal + q * 16, WAR_TAG_BIG, WAR_TAG_BIGPAL + q, &sGI_Oam64Affine, 120, 80, 1);
            sLI_Spr[f * 4 + q] = id;
            if (id < MAX_SPRITES)
                gSprites[id].invisible = TRUE;
            LI_Frame(f * 4 + q, WAR_TAG_BIG, f * 4 + q, 64);
        }
    }
}

static u32 WarBigPalBits(void)
{
    u32 q, bits = 0;
    for (q = 0; q < 4; q++)
        bits |= GI_SpritePalBit(WAR_TAG_BIGPAL + q);
    return bits;
}

static void RTWario_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sWarioIntro_Tiles, sWarioIntro_Maps);
    LI_ResetSprites();
    LI_Make(WAR_S_GARLIC, sWarioGarlic_Gfx, 32 * 128 / 2, sWarioGarlic_Pal, WAR_TAG_GARLIC, &sGI_Oam32, 0, 0, 0);
    LI_Make(WAR_S_SPARK, sWarioSpark_Gfx, 16 * 16 / 2, sWarioSpark_Pal, WAR_TAG_SPARK, &sGI_Oam16, 0, 151, 0);
    LI_Make(WAR_S_BOOM, sWarioBoom_Gfx, 64 * 64 / 2, sWarioBoom_Pal, WAR_TAG_BOOM, &sGI_Oam64Affine, 20, 146, 0);
    for (i = 0; i < WAR_STARS; i++)
        LI_Make(WAR_S_STAR + i, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, gBattleAnimSpritePal_Sparkle3, WAR_TAG_STAR, &sGI_Oam32, 0, 0, 0);
    WarBigMake(sWarioCouch_Gfx, sWarioCouch_Pal, 1);
}

static bool8 RTWario_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, card = -1, c0 = 0, shake = 0, scale = 256, bx = 140, by = 78, frame = 0, pose = 0;
    bool32 bigShow = FALSE;
    u32 bg, keep;
    u16 *u = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *s;

    if (t >= WAR_CARD && t < WAR_FACE)
    {
        card = (t - WAR_CARD) / WAR_CARD_LEN;
        c0 = WAR_CARD + card * WAR_CARD_LEN;
    }
    bg = t >= WAR_CREST ? GI_BG_PALS : LI2_PALS_MAP;
    keep = WarBigPalBits() | GI_SpritePalBit(WAR_TAG_GARLIC) | GI_SpritePalBit(WAR_TAG_SPARK)
         | GI_SpritePalBit(WAR_TAG_BOOM) | GI_SpritePalBit(WAR_TAG_STAR);
    GI_ResetPals(keep);
    if (t >= WAR_SHOW && t < WAR_CREST)
        LoadPalette(sWarioIntro_Pal, BG_PLTT_ID(10), 6 * PLTT_SIZE_4BPP);
    if (t >= WAR_CREST)
    {
        // het embleem: de stralenkrans draait (index 1-8 in palet 13-15)
        LoadPalette(sWarioCrest_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
        for (i = 0; i < 8; i++)
            u[1 + i] = u[16 + 1 + i] = u[32 + 1 + i] = sWarBurst[(i + (t >> 1)) & 7];
        CpuCopy16(u, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);
    }
    if (t == WAR_SHOW)
        GI_KillFieldWindows();

    // ---- de kaarten
    if (card >= 0 && t == c0 + 1) // een frame na de sprites (die gaan pas in de VBlank over): geen oude Wario op de nieuwe kaart
        GI_ShowMap(WAR_MAP_EAT + card);
    if (card >= 0 && t == c0)
    {
        PlaySE(SE_BALL_OPEN);
        if (card == 1)
            WarBigMake(sWarioCash_Gfx, sWarioCash_Pal, 1);
        else if (card == 2)
            WarBigMake(sWarioFly_Gfx, sWarioFly_Pal, 2);
        else if (card == 3)
            WarBigMake(sWarioFlex_Gfx, sWarioFlex_Pal, 1);
    }
    if (card >= 0)
    {
        k = t - c0;
        // de lont brandt op: de vonk loopt naar de bom, de lont rechts ervan verdwijnt
        {
            s32 sx = 232 - k * 196 / (WAR_CARD_LEN - 2);
            s = LI_S(WAR_S_SPARK);
            s->invisible = sx < 34;
            s->x = sx;
            s->y = 151 + ((t >> 1) & 1);
            if (sx >= 34)
                GI_PutRect(WAR_MAP_BAR, (sx + 4) / 8, 18, 30 - (sx + 4) / 8, 2, (sx + 4) / 8, 18);
        }
        // eerst staat de opdracht alleen in beeld (zoals in WarioWare), dan begint het spelletje
        bigShow = k >= 5;
        k -= 5;
        if (card == 0)
        {
            // EAT!: hap, hap, hap
            s = LI_S(WAR_S_GARLIC);
            frame = k < 4 ? 0 : (k < 9 ? 1 : (k < 14 ? 2 : 3));
            s->invisible = k < 0 || k >= 18;
            s->x = 118;
            s->y = 80;
            LI_Frame(WAR_S_GARLIC, WAR_TAG_GARLIC, frame, 16);
            if (k == 4 || k == 9 || k == 14)
                PlaySE(SE_M_BITE);
            if ((k >= 4 && k < 7) || (k >= 9 && k < 12) || (k >= 14 && k < 17))
                by += 2;
            if (k == 18)
                PlaySE(SE_M_SWAGGER2); // doorgeslikt
        }
        else if (card == 1)
        {
            // INVENT!: het idee stempelt erin, dollartekens
            LI_S(WAR_S_GARLIC)->invisible = TRUE;
            bx = 128;
            by = 76;
            scale = k < 0 ? 256 : (k < 4 ? 384 - k * 32 : 256 + ((k >> 1) & 1) * 6);
            if (k == 2)
                PlaySE(SE_SHOP);
        }
        else if (card == 2)
        {
            // FLY!: schuin door de lucht, twee standen om de beurt
            bx = -40 + k * 330 / (WAR_CARD_LEN - 5);
            by = 136 - k * 120 / (WAR_CARD_LEN - 5);
            pose = (t >> 2) & 1;
            if (k == 0)
                PlaySE(SE_M_FLY);
        }
        else
        {
            // FLEX!: stempelt erin, dan pompen
            bx = 120;
            by = 80;
            scale = k < 0 ? 256 : (k < 4 ? 448 - k * 48 : 256 + ((k / 4) & 1) * 16);
            if (k >= 0 && k < 3)
                shake = 3;
            if (k == 0)
                PlaySE(SE_M_SWAGGER);
            if (k == 12)
                PlaySE(SE_M_HARDEN);
        }
        if (k >= -4 && k < -1)
            BlendPalettes(bg | keep, 10 - (k + 4) * 3, RGB_WHITE); // de flits tussen de microgames
    }
    // het grote object (bij FLY! twee standen: de andere vier slots onzichtbaar)
    for (i = 0; i < 2; i++)
        if (sLI_Spr[i * 4] < MAX_SPRITES)
            LI2_BigSet(i * 4, bx, by, scale, 0, bigShow && pose == i, 0);

    // ---- de lont is op: BOEM
    s = LI_S(WAR_S_BOOM);
    k = t - WAR_BOOM;
    s->invisible = k < 0 || k >= 10;
    if (!s->invisible)
    {
        LI_Affine(sLI_Spr[WAR_S_BOOM], 256 + k * 40, 0);
        shake = 4;
        if (k == 0)
            PlaySE(SE_M_EXPLOSION);
    }

    // ---- WIN!: de close-up, sterren
    if (t == WAR_FACE)
    {
        WarBigFree();
        GI_ShowMap(WAR_MAP_FACE);
        PlaySE(SE_M_SWAGGER2);
    }
    if (t >= WAR_FACE && t < WAR_CREST)
    {
        k = t - WAR_FACE;
        if (k < 4)
            BlendPalettes(bg | keep, 12 - k * 3, RGB_WHITE);
        shake = (k & 4) ? 1 : 0; // hij schudt van het lachen
        for (i = 0; i < WAR_STARS; i++)
        {
            s32 j = k - i * 2;
            s = LI_S(WAR_S_STAR + i);
            s->invisible = j < 0 || j >= 12 || t >= WAR_CREST - 1;
            s->x = 120 + sWarStar[i][0];
            s->y = 70 + sWarStar[i][1];
            if (!s->invisible)
                LI_Frame(WAR_S_STAR + i, WAR_TAG_STAR, min(j >> 1, 4), 16);
            if (j == 0 && (i & 1) == 0)
                PlaySE(SE_SHINY);
        }
    }

    // ---- het embleem neemt het beeld over
    if (t == WAR_CREST)
    {
        for (i = 0; i < WAR_STARS; i++)
            LI_S(WAR_S_STAR + i)->invisible = TRUE;
        GI_Free();
        GI_LoadGfx(sWarioCrest_Tiles, sWarioCrest_Maps);
        GI_ShowMap(WAR_MAP_CREST);
        PlaySE(SE_M_STRENGTH);
    }
    if (t == WAR_CREST + 4)
        GI_ShowMap(WAR_MAP_CREST_BIG);
    if (t == WAR_CREST + 8)
    {
        GI_ShowMap(WAR_MAP_CREST_HUGE);
        PlaySE(SE_M_MEGA_KICK2);
    }
    if (t >= WAR_CREST && t < WAR_CREST + 12)
        shake = 4 - (t - WAR_CREST) / 3;
    // wissel van tileset achter een wit frame (tiles gaan meteen naar VRAM, paletten pas in de VBlank)
    if (t == WAR_CREST - 1)
        BlendPalettes(PALETTES_ALL, 16, RGB_WHITE);
    if (t >= WAR_CREST && t < WAR_CREST + 4)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - WAR_CREST) * 4, RGB_WHITE);

    GI_Shake(shake);
    LI2_FadeIn(t, WAR_SHOW, LI2_PALS_MAP | keep);
    LI2_FadeWorld(t, WAR_SHOW, bg, keep);
    if (LI2_WhiteOut(t, WAR_END, bg, keep))
    {
        for (i = 0; i < LI_SPRITES; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTWario_Finish(struct Task *task)
{
    GI_Shake(0);
    WarBigFree();
    LI_DestroySprites();
    GI_FreeTag(WAR_TAG_GARLIC);
    GI_FreeTag(WAR_TAG_SPARK);
    GI_FreeTag(WAR_TAG_BOOM);
    GI_FreeTag(WAR_TAG_STAR);
    GI_Free();
}

static const struct RouteTransition sRT_Wario =
{
    sPikachu_Tileset, 32, sWarioIntro_Pal + 5 * 16, 1, 1, 0, RTWario_Init, RTWario_Update, RTWario_Finish
};

static void Task_Wario(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Wario);
}
