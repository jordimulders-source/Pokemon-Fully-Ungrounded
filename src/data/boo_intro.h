// Project Grounded: gevechtsintro van de Boos (Commander Boo in het spookhuis op Yoshi's Island, en Boo als gast in het
// Battle Stadium). Jordi: "bij Boo mag je een haunted house pakken uit de game waar Boo's hun ogen bedekken, Kamek langs
// komt vliegen met zijn magische spreuk en van 1 Boo een Commander maakt waardoor die tegen je gaat battlen".
// Het spookhuis uit Yoshi's Island, vijf Boos met de handen voor de ogen (je kijkt naar ze). Er gluurt er één, heel even.
// Kamek raast op zijn bezem door het beeld en vuurt in het voorbijgaan zijn spreuk (cirkel, driehoek, vierkant) op de
// middelste Boo af, zonder af te remmen of om te kijken. De Boo zwelt op (nog steeds met de handen voor de ogen), de
// anderen gluren. Poef: hij draait zich om en is Commander Boo (zijn eigen trainerfoto), met de tong uit. De anderen
// slaan de handen weer voor de ogen. Eén tel later gluren ze toch weer. Wit, gevecht.
// Op de beat van MUS_GROUNDED_VS_BROKEN_PIER (132 bpm = 27,27 frames per tel): de spreuk raakt op de eerste tel van maat
// 2, Commander Boo staat er op tel 3 van maat 2, het gevecht begint op de eerste tel van maat 3. Geteld in VBlanks vanaf
// de start van de transitie (Tapu_Elapsed), zie de tijden hieronder.
// Wordt na src/data/wario_intro.h ingevoegd (GI_/LI_/LI2_-hulpjes). Art: tools/grounded/boo_intro.py (het spookhuis in
// BG-palet 10-13); de Boos, Kamek en zijn spreuk komen uit de ROM van SMA3 (tools/grounded/sma3_boo_rip.py).
static const u32 sBooIntro_Tiles[] = INCBIN_U32("graphics/battle_transitions/boo_intro.4bpp.smol");
static const u32 sBooIntro_Maps[] = INCBIN_U32("graphics/battle_transitions/boo_intro_maps.bin.smol");
static const u16 sBooIntro_Pal[] = INCBIN_U16("graphics/battle_transitions/boo_intro.gbapal");
static const u32 sBooYi_Gfx[] = INCBIN_U32("graphics/battle_transitions/boo_yi.4bpp.smol");
static const u16 sBooYi_Pal[] = INCBIN_U16("graphics/battle_transitions/boo_yi.gbapal");
static const u32 sBooKamek_Gfx[] = INCBIN_U32("graphics/battle_transitions/boo_kamek.4bpp.smol");
static const u16 sBooKamek_Pal[] = INCBIN_U16("graphics/battle_transitions/boo_kamek.gbapal");
static const u32 sBooMagic_Gfx[] = INCBIN_U32("graphics/battle_transitions/boo_magic.4bpp.smol");
static const u16 sBooMagic_Pal[] = INCBIN_U16("graphics/battle_transitions/boo_magic.gbapal");

#define BOO_PALS_BG     (0xF << 10)     // BG 10-13: het spookhuis
#define BOO_TAG_YI      0x5B40
#define BOO_TAG_KAMEK   0x5B41
#define BOO_TAG_MAGIC   0x5B42
#define BOO_TAG_SPARK   0x5B43
// standen in boo_yi (16 tiles per stand)
enum { BOO_F_SHY, BOO_F_LOOK, BOO_F_LOOK2, BOO_F_MOUTH };
// slots in sLI_Spr
#define BOO_N           5
#define BOO_TARGET      2               // de middelste Boo wordt Commander Boo
#define BOO_S_KAMEK     5
#define BOO_S_MAGIC     6               // t/m 11
#define BOO_MAGIC_N     6
#define BOO_S_SPARK     12              // t/m 17
#define BOO_SPARK_N     6
// tijden (VBlanks vanaf de start van de transitie). Gemeten in een emulatoropname (beeld + geluid samen): de tellen van
// de muziek vallen op t = 8 + k * 27,27 (de eerste tel 9 VBlanks na de start; de flits vooraf duurt al ±20)
#define BOO_SHOW        8               // in taakframes: de flits vooraf duurt al ±20 VBlanks, dus het spookhuis staat er rond tel 2
#define BOO_PEEK        49              // tel 2,5 (op de 'en'): één Boo gluurt
#define BOO_KAMEK       63              // tel 3: Kamek
#define BOO_CAST        90              // tel 4: de spreuk
#define BOO_HIT         117             // maat 2, tel 1: raak
#define BOO_POOF        144             // tel 2: poef, hij draait zich om
#define BOO_REVEAL      172             // tel 3: Commander Boo
#define BOO_PEEK2       199             // tel 4: de anderen gluren toch weer
#define BOO_END         226             // maat 3, tel 1: het gevecht
#define BOO_CMD_X       120
#define BOO_CMD_Y       76

static const struct OamData sBoo_Oam8 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(8x8),
    .size = SPRITE_SIZE(8x8),
    .priority = 0,
};

static const struct OamData sBoo_Oam64x32Affine =
{
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .shape = SPRITE_SHAPE(64x32),
    .size = SPRITE_SIZE(64x32),
    .priority = 0,
};

static const s16 sBooPos[BOO_N][2] = {{38, 86}, {80, 72}, {120, 92}, {160, 72}, {202, 86}};

static EWRAM_DATA u8 sBooCmd = 0;               // Commander Boo (de trainerfoto; gezet in RTBoo_Init)
static EWRAM_DATA s16 sBooLast = 0;             // vorige t (gebeurtenissen vallen niet weg bij een vertraagd frame)

// heeft de klok tijdstip x net gepasseerd?
static bool32 BooAt(s32 last, s32 t, s32 x)
{
    return last < x && t >= x;
}

// Kamek: binnen vanaf rechts op tel 3, met een vaste vaart naar links (hij remt niet af)
static s32 BooKamekX(s32 t)
{
    return 300 - (t - BOO_KAMEK) * 4;
}

static s32 BooKamekY(s32 t)
{
    return 30 + Sin((t * 6) & 0xFF, 3);
}

static void BooMatrix(u8 id, s32 xs, s32 ys)
{
    if (id >= MAX_SPRITES || gSprites[id].oam.affineMode == ST_OAM_AFFINE_OFF)
        return;
    if (xs > -16 && xs < 16)
        xs = xs < 0 ? -16 : 16;   // niet door nul delen (ConvertScaleParam)
    SetOamMatrixRotationScaling(gSprites[id].oam.matrixNum, xs, ys, 0);
}

static void BooBurst(s32 k)
{
    u32 i;
    for (i = 0; i < BOO_SPARK_N; i++)
    {
        struct Sprite *s = LI_S(BOO_S_SPARK + i);
        s32 r = 10 + k * 3, a = (i * 256 / BOO_SPARK_N + k * 2) & 0xFF;
        s->invisible = k < 0 || k >= 16;
        s->x = BOO_CMD_X + Cos(a, r);
        s->y = BOO_CMD_Y + 8 + Sin(a, r);
        if (!s->invisible)
            LI_Frame(BOO_S_SPARK + i, BOO_TAG_SPARK, min(k >> 2, 4), 16);
    }
}

static void RTBoo_Init(struct Task *task)
{
    u32 i;
    struct Sprite *s;

    GI_LoadGfx(sBooIntro_Tiles, sBooIntro_Maps);
    LI_ResetSprites();
    for (i = 0; i < BOO_N; i++)
        LI_Make(i, sBooYi_Gfx, 4 * 32 * 32 / 2, sBooYi_Pal, BOO_TAG_YI, i == BOO_TARGET ? &sGI_Oam32Affine : &sGI_Oam32,
                sBooPos[i][0], sBooPos[i][1], 3);
    LI_Make(BOO_S_KAMEK, sBooKamek_Gfx, 64 * 32 / 2, sBooKamek_Pal, BOO_TAG_KAMEK, &sBoo_Oam64x32Affine, 300, 30, 2);
    LI_Affine(sLI_Spr[BOO_S_KAMEK], 512, 0);
    for (i = 0; i < BOO_MAGIC_N; i++)
        LI_Make(BOO_S_MAGIC + i, sBooMagic_Gfx, 12 * 8 * 8 / 2, sBooMagic_Pal, BOO_TAG_MAGIC, &sBoo_Oam8, 0, 0, 0);
    for (i = 0; i < BOO_SPARK_N; i++)
        LI_Make(BOO_S_SPARK + i, gBattleAnimSpriteGfx_Sparkle4, 32 * 160 / 2, gBattleAnimSpritePal_Sparkle3, BOO_TAG_SPARK, &sGI_Oam32, 0, 0, 0);

    // Commander Boo: zijn eigen trainerfoto (staat al in de ROM), affine zodat hij kan groeien en zich omdraaien
    sBooCmd = GI_TrainerPic(TRAINER_PIC_GUEST_BOO, BOO_CMD_X, BOO_CMD_Y);
    if (sBooCmd < MAX_SPRITES)
    {
        s = &gSprites[sBooCmd];
        s->invisible = TRUE;
        s->subpriority = 0;
        s->oam.matrixNum = AllocOamMatrix();
        if (s->oam.matrixNum == 0xFF)
        {
            s->oam.matrixNum = 0;
        }
        else
        {
            s->oam.affineMode = ST_OAM_AFFINE_DOUBLE;
            s->affineAnimPaused = TRUE;
            CalcCenterToCornerVec(s, SPRITE_SHAPE(64x64), SPRITE_SIZE(64x64), ST_OAM_AFFINE_DOUBLE);
            BooMatrix(sBooCmd, 256, 256);
        }
    }
    sBooLast = -1;
}

static bool8 RTBoo_Update(struct Task *task)
{
    s32 t = Tapu_Elapsed(), u = task->tRtTimer, last = sBooLast, i, k, shake = 0;
    u32 keep;
    struct Sprite *s;
    bool32 show = u >= BOO_SHOW;

    sBooLast = t;
    keep = GI_SpritePalBit(BOO_TAG_YI) | GI_SpritePalBit(BOO_TAG_KAMEK) | GI_SpritePalBit(BOO_TAG_MAGIC)
         | GI_SpritePalBit(BOO_TAG_SPARK) | GI_TrainerPalBit(TRAINER_PIC_GUEST_BOO);
    GI_ResetPals(keep);
    if (show)
        LoadPalette(sBooIntro_Pal, BG_PLTT_ID(10), 4 * PLTT_SIZE_4BPP);
    if (u == BOO_SHOW)
    {
        GI_KillFieldWindows();
        GI_ShowMap(0);
    }

    // ---- de Boos: zweven, handen voor de ogen
    for (i = 0; i < BOO_N; i++)
    {
        u32 f = BOO_F_SHY;
        s = LI_S(i);
        s->invisible = !show || (i == BOO_TARGET && t >= BOO_POOF);
        s->x = sBooPos[i][0];
        s->y = sBooPos[i][1] + Sin((t * 4 + i * 50) & 0xFF, 3);
        if (i == 4 && t >= BOO_PEEK && t < BOO_PEEK + 12)
            f = BOO_F_LOOK;                                  // eentje gluurt even, ziet jou kijken, en schaamt zich weer
        if (i != BOO_TARGET && t >= BOO_HIT + 8 && t < BOO_REVEAL)
            f = (i & 1) ? BOO_F_LOOK2 : BOO_F_LOOK;          // de anderen gluren naar het opzwellen
        if (i != BOO_TARGET && t >= BOO_PEEK2)
            f = (i & 1) ? BOO_F_LOOK : BOO_F_LOOK2;          // en toch weer
        LI_Frame(i, BOO_TAG_YI, f, 16);
    }

    // ---- Kamek raast door het beeld
    s = LI_S(BOO_S_KAMEK);
    s->x = BooKamekX(t);
    s->y = BooKamekY(t);
    s->invisible = t < BOO_KAMEK || s->x < -70;
    if (BooAt(last, t, BOO_KAMEK))
        PlaySE(SE_M_FLY);
    if (BooAt(last, t, BOO_CAST))
        PlaySE(SE_M_TRI_ATTACK);

    // ---- de spreuk: zes vormen uit zijn toverstaf, die allemaal tegelijk op de beat inslaan
    for (i = 0; i < BOO_MAGIC_N; i++)
    {
        s32 t0 = BOO_CAST + i * 3, x0 = BooKamekX(t0) - 40, y0 = BooKamekY(t0) + 10, n = BOO_HIT - t0;
        s32 tx = sBooPos[BOO_TARGET][0], ty = sBooPos[BOO_TARGET][1];
        s = LI_S(BOO_S_MAGIC + i);
        k = t - t0;
        s->invisible = k < 0 || t >= BOO_HIT;
        if (s->invisible)
            continue;
        s->x = x0 + (tx - x0) * k / n;
        s->y = y0 + (ty - y0) * k / n + Sin((k * 20 + i * 40) & 0xFF, 5);
        LI_Frame(BOO_S_MAGIC + i, BOO_TAG_MAGIC, (i % 3) * 4 + (((t >> 1) + i) & 3), 1);
    }

    // ---- raak: flits, sterretjes, de Boo zwelt op (handen nog voor de ogen)
    if (BooAt(last, t, BOO_HIT))
        PlaySE(SE_M_TRI_ATTACK2);
    if (BooAt(last, t, BOO_HIT + 4))
        PlaySE(SE_M_STAT_INCREASE);
    if (t >= BOO_HIT && t < BOO_HIT + 6)
    {
        BlendPalettes(BOO_PALS_BG | keep, 12 - (t - BOO_HIT) * 2, RGB_WHITE);
        shake = 2;
    }
    if (t >= BOO_HIT && t < BOO_POOF)
    {
        s32 g = (t - BOO_HIT) * 256 / (BOO_POOF - BOO_HIT), w = Sin(((t - BOO_HIT) * 20) & 0xFF, 20);
        s = LI_S(BOO_TARGET);
        s->y = sBooPos[BOO_TARGET][1] - g * 12 / 256;
        BooMatrix(sLI_Spr[BOO_TARGET], 256 + g + w, 256 + g - w);
    }
    if (t < BOO_POOF)
        BooBurst(t - BOO_HIT);
    else
        BooBurst(t - BOO_POOF);

    // ---- poef: hij draait zich om, groeit, en is Commander Boo
    if (BooAt(last, t, BOO_POOF))
        PlaySE(SE_M_TELEPORT);
    if (BooAt(last, t, BOO_REVEAL))
        PlaySE(SE_M_NIGHTMARE);
    if (sBooCmd < MAX_SPRITES)
    {
        s32 sc, xs;
        s = &gSprites[sBooCmd];
        s->invisible = t < BOO_POOF;
        s->x = BOO_CMD_X;
        s->y = BOO_CMD_Y + Sin((t * 4) & 0xFF, 2);
        if (t < BOO_REVEAL)
        {
            k = (t - BOO_POOF) * 128 / (BOO_REVEAL - BOO_POOF);       // een halve slag: van rug naar gezicht
            sc = 256 + (t - BOO_POOF) * 160 / (BOO_REVEAL - BOO_POOF);
            xs = -Cos(max(k, 0) & 0xFF, sc);
        }
        else
        {
            k = t - BOO_REVEAL;
            sc = 432 + max(0, 8 - k) * 8;                            // BOE: een sprong naar voren, dan staat hij
            if (t >= BOO_PEEK2)
                sc += max(0, 6 - (t - BOO_PEEK2)) * 3;               // de tong
            xs = sc;
        }
        BooMatrix(sBooCmd, xs, sc);
    }
    if (t >= BOO_REVEAL && t < BOO_REVEAL + 12)
        shake = 4 - (t - BOO_REVEAL) / 3;
    if (t >= BOO_REVEAL && t < BOO_REVEAL + 4)
        BlendPalettes(BOO_PALS_BG, 8 - (t - BOO_REVEAL) * 2, RGB_BLACK);   // het licht flakkert

    GI_Shake(shake);
    LI2_FadeIn(u, BOO_SHOW, BOO_PALS_BG | keep);
    LI2_FadeWorld(u, BOO_SHOW, BOO_PALS_BG, keep);
    if (!show)
    {
        for (i = 0; i < LI_SPRITES; i++)
            LI_S(i)->invisible = TRUE;
    }
    if (LI2_WhiteOut(t, BOO_END, BOO_PALS_BG, keep))
    {
        for (i = 0; i < LI_SPRITES; i++)
            LI_S(i)->invisible = TRUE;
        if (sBooCmd < MAX_SPRITES)
            gSprites[sBooCmd].invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTBoo_Finish(struct Task *task)
{
    GI_Shake(0);
    LI_DestroySprites();
    if (sBooCmd < MAX_SPRITES)
        GI_DestroyTrainerPic(sBooCmd);
    sBooCmd = MAX_SPRITES;
    GI_FreeTag(BOO_TAG_YI);
    GI_FreeTag(BOO_TAG_KAMEK);
    GI_FreeTag(BOO_TAG_MAGIC);
    GI_FreeTag(BOO_TAG_SPARK);
    GI_Free();
}

static const struct RouteTransition sRT_Boo =
{
    sPikachu_Tileset, 32, sBooIntro_Pal + 3 * 16, 1, 1, 0, RTBoo_Init, RTBoo_Update, RTBoo_Finish
};

static void Task_Boo(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_Boo);
}
