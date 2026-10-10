// Project Grounded: gevechtsintro van Wario (Yoshi's Island-fort, en als gast in het Battle Stadium). Jordi: "een stuk
// knoflook dat opgegeten wordt en een grote geel-paars omlijnde W die in beeld komt, daarna Wario in diverse poses, met
// de W die terugkomt en het beeld overneemt." Wordt na src/data/legend_intros2.h ingevoegd (gebruikt de GI_/LI_/LI2_-
// hulpjes). Art: tools/grounded/wario_intro.py; Wario zelf zijn de echte GBA-poses (Scale3x) als groot object.
//
// Een draaiende stralenkrans in geel en paars (paletcyclus). Een knoflookbol: HAP, HAP, HAP (het beeld schokt bij
// elke hap) en hij is op. Dan dreunt de W in beeld (ground pound: flits en trillen). Wario zelf in drie poses
// (grijns, dubbele biceps, opzij), elke pose stempelt erin. Dan komt de W terug en wordt in drie stappen zo groot dat
// hij het beeld overneemt: geel, wit, gevecht.
static const u32 sWarioIntro_Tiles[] = INCBIN_U32("graphics/battle_transitions/wario_intro.4bpp.smol");
static const u32 sWarioIntro_Maps[] = INCBIN_U32("graphics/battle_transitions/wario_intro_maps.bin.smol");
static const u16 sWarioIntro_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_intro.gbapal");
static const u32 sWarioPoses_Gfx[] = INCBIN_U32("graphics/battle_transitions/wario_poses.4bpp.smol");
static const u16 sWarioPoses_Pal[] = INCBIN_U16("graphics/battle_transitions/wario_poses.gbapal");

enum { WAR_MAP_BURST, WAR_MAP_GARLIC0, WAR_MAP_GARLIC1, WAR_MAP_GARLIC2, WAR_MAP_GARLIC3, WAR_MAP_W, WAR_MAP_W_BIG, WAR_MAP_W_HUGE };
#define WAR_TAG_POSE    0x5A80
#define WAR_SHOW        8
#define WAR_BITE        22    // drie happen, om de 10 frames
#define WAR_BITE_GAP    10
#define WAR_GONE        (WAR_BITE + 3 * WAR_BITE_GAP)   // op
#define WAR_W           54    // de W dreunt in beeld
#define WAR_POSE        66    // drie poses, om de 15 frames
#define WAR_POSE_GAP    15
#define WAR_RETURN      (WAR_POSE + 3 * WAR_POSE_GAP)   // de W komt terug en neemt het beeld over
#define WAR_END         (WAR_RETURN + 16)
#define WAR_Y           84

static const u16 sWarBurst[8] = {RGB(31, 28, 6), RGB(30, 24, 3), RGB(16, 6, 22), RGB(12, 3, 18),
                                 RGB(31, 28, 6), RGB(30, 24, 3), RGB(16, 6, 22), RGB(12, 3, 18)};
static const s16 sWarPoseX[3] = {120, 112, 128};

static void RTWario_Init(struct Task *task)
{
    u32 q;

    GI_LoadGfx(sWarioIntro_Tiles, sWarioIntro_Maps);
    LoadPalette(sWarioIntro_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    LI_ResetSprites();
    for (q = 0; q < 4; q++)
    {
        LI_Make(q, sWarioPoses_Gfx, 3 * LI2_BIG_SIZE, sWarioPoses_Pal, WAR_TAG_POSE, &sGI_Oam64Affine, 120, WAR_Y, 0);
        LI_Frame(q, WAR_TAG_POSE, q, 64);
    }
}

static bool8 RTWario_Update(struct Task *task)
{
    s32 t = task->tRtTimer, i, k, pose = -1, scale = 256, shake = 0, x = 120;
    u32 keep = GI_SpritePalBit(WAR_TAG_POSE);
    u16 *u = &gPlttBufferUnfaded[BG_PLTT_ID(13)];

    GI_ResetPals(keep);
    LoadPalette(sWarioIntro_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    // de stralenkrans draait (index 1-8 in alle drie de paletten)
    for (i = 0; i < 8; i++)
    {
        u16 c = sWarBurst[(i + (t >> 1)) & 7];
        u[1 + i] = u[16 + 1 + i] = u[32 + 1 + i] = c;
    }
    CpuCopy16(u, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    if (t == WAR_SHOW)
    {
        GI_KillFieldWindows();
        GI_ShowMap(WAR_MAP_GARLIC0);
    }
    // hap, hap, hap
    for (i = 0; i < 3; i++)
    {
        k = t - WAR_BITE - i * WAR_BITE_GAP;
        if (k == 0)
        {
            GI_ShowMap(WAR_MAP_GARLIC1 + i);
            PlaySE(SE_M_BITE);
        }
        if (k >= 0 && k < 4)
            shake = 3 - k / 2;
    }
    if (t == WAR_GONE)
    {
        GI_ShowMap(WAR_MAP_BURST);
        PlaySE(SE_M_SWAGGER); // ...en doorgeslikt
    }
    // de W dreunt in beeld
    if (t == WAR_W)
    {
        GI_ShowMap(WAR_MAP_W);
        PlaySE(SE_M_STRENGTH);
    }
    if (t >= WAR_W && t < WAR_W + 8)
        shake = 5 - (t - WAR_W) / 2;
    GI_Flash(t, WAR_W, 6, 12, keep, RGB_WHITE);

    // Wario in drie poses, elke pose stempelt erin
    if (t >= WAR_POSE && t < WAR_RETURN)
    {
        pose = (t - WAR_POSE) / WAR_POSE_GAP;
        k = (t - WAR_POSE) % WAR_POSE_GAP;
        if (t == WAR_POSE)
            GI_ShowMap(WAR_MAP_BURST);
        scale = k < 4 ? 448 - k * 48 : 256 + (k < 7 ? (7 - k) * 6 : 0);
        x = sWarPoseX[pose];
        if (k < 3)
            shake = 3;
        if (k == 0)
            PlaySE(pose == 1 ? SE_M_SWAGGER : SE_M_MEGA_KICK2);
        GI_Flash(t, WAR_POSE + pose * WAR_POSE_GAP, 4, 8, 0, RGB_WHITE);
    }
    for (i = 0; i < 4; i++)
    {
        if (pose >= 0)
            LI_Frame(i, WAR_TAG_POSE, pose * 4 + i, 64);
    }
    LI2_BigSet(0, x + (shake ? LI_ShakeAmp(shake) : 0), WAR_Y, scale, 0, pose >= 0, 0);

    // de W komt terug en neemt het beeld over
    if (t == WAR_RETURN)
    {
        GI_ShowMap(WAR_MAP_W);
        PlaySE(SE_M_STRENGTH);
    }
    if (t == WAR_RETURN + 3)
        GI_ShowMap(WAR_MAP_W_BIG);
    if (t == WAR_RETURN + 6)
    {
        GI_ShowMap(WAR_MAP_W_HUGE);
        PlaySE(SE_M_MEGA_KICK2);
    }
    if (t >= WAR_RETURN && t < WAR_RETURN + 10)
        shake = 4;

    GI_Shake(shake);
    GI_FadeWorld(t, WAR_SHOW, keep);
    if (t >= WAR_SHOW && t < WAR_SHOW + 4)
        BlendPalettes(GI_BG_PALS, 16 - (t - WAR_SHOW) * 4, RGB_BLACK);
    if (GI_WhiteOut(t, WAR_END, keep))
    {
        for (i = 0; i < 4; i++)
            LI_S(i)->invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTWario_Finish(struct Task *task)
{
    GI_Shake(0);
    LI_DestroySprites();
    GI_FreeTag(WAR_TAG_POSE);
    GI_Free();
}

static const struct RouteTransition sRT_Wario =
{
    sPikachu_Tileset, 32, sWarioIntro_Pal + 32, 1, 1, 0, RTWario_Init, RTWario_Update, RTWario_Finish
};

static void Task_Wario(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Wario);
}
