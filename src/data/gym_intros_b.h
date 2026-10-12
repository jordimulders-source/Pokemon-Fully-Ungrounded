// Project Grounded: gymleider-intro's (deel B: Norman, Winona, Tate & Liza, Wallace). Wordt onderaan
// src/battle_transition.c ingevoegd, na deel A (src/data/gym_intros_a.h): gebruikt dezelfde GI_-hulpjes en de
// route-transitie-runner. Art via tools/grounded/<naam>_transition.py (gedeelde hulpjes in gym_intro_lib.py).

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

// ---------------- Norman (Netflix: "Hm... a new season of BLACK MIRROR... Ok, I'm sick of you, face my SLAKING!"):
// het startscherm van NORMFLIX ("Continue watching for DAD"), dan "Are you still watching?": de cursor gaat even naar
// "Go outside" en springt vanzelf terug, Continue. Pauze, en het beeld krimpt terug in de tv (venster 0) van de
// woonkamer, waar Slaking op de bank hangt (Zzz). "OK, I'M SICK OF YOU." / "FACE MY SLAKING!": Slaking schrikt wakker.
// tools/grounded/norman_transition.py
static const u32 sGymNorman_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_norman.4bpp.smol");
static const u32 sGymNorman_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_norman_maps.bin.smol");
static const u16 sGymNorman_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_norman.gbapal");

enum { NOR_MAP_HOME, NOR_MAP_STILL, NOR_MAP_PAUSE, NOR_MAP_ROOM, NOR_MAP_ROOM1, NOR_MAP_ROOM2 };
#define NOR_TAG_Z       0x5A40
// leestijd (Jordi: te snel om de tekst te lezen): ±1 s per 3-4 woorden, minimaal ±1,5 s per tekst
#define NOR_HOME        8
#define NOR_STILL       (NOR_HOME + 54)     // startscherm (was 42)
#define NOR_HOVER       (NOR_STILL + 66)    // "Are you still watching BLACK MIRROR?" (was 16)
#define NOR_BACK        (NOR_HOVER + 30)    // cursor op "Go outside (not recommended)" (was 10)
#define NOR_PRESS       (NOR_BACK + 18)     // (was 14)
#define NOR_PAUSE       (NOR_PRESS + 6)
#define NOR_SHRINK      (NOR_PAUSE + 6)
#define NOR_SHRINK_LEN  14
#define NOR_ROOM        (NOR_SHRINK + NOR_SHRINK_LEN)
#define NOR_SUB1        (NOR_ROOM + 20)     // (was 12)
#define NOR_SUB2        (NOR_SUB1 + 72)     // "OK, I'M SICK OF YOU." (was 18)
#define NOR_END         (NOR_SUB2 + 72)     // "FACE MY SLAKING!" (was 32)
#define NOR_HL          6     // BG 13: rand van de geselecteerde titel
#define NOR_BTN_A       5     // BG 15: Continue watching
#define NOR_BTN_B       6     // BG 15: Go outside
#define NOR_WALL_LIT    2     // BG 14: tv-licht op de muur
#define NOR_SCREEN      9     // BG 14: het tv-scherm
#define NOR_SLAKING_X   180
#define NOR_SLAKING_Y   100

static const s8 sNorHop[] = {-4, -8, -10, -10, -8, -5, -2, 0, -2, -3, -2, 0};

static void RTNorman_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sGymNorman_Tiles, sGymNorman_Maps);
    LoadPalette(sGymNorman_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_NORMAN, 108, 112);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_MonPic(SPECIES_SLAKING, NOR_SLAKING_X, NOR_SLAKING_Y);
    for (i = 0; i < 2; i++)
    {
        task->data[12 + i] = GI_CreateSprite(gBattleAnimSpriteGfx_SnoreZ, 32 * 32 / 2, gBattleAnimSpritePal_SnoreZ, NOR_TAG_Z, &sGI_Oam32, 0, 0, 0);
        gSprites[task->data[12 + i]].invisible = TRUE;
    }
    task->tGiShown = 0xFF;
}

static bool8 RTNorman_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, map, p;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *norman = &gSprites[task->tGiSprite0];
    struct Sprite *slaking = GI_Sprite(task->tGiSprite1);
    struct Sprite *z;

    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_NORMAN) | GI_SpritePalBit(SPECIES_SLAKING) | GI_SpritePalBit(NOR_TAG_Z);
    GI_ResetPals(keep);
    LoadPalette(sGymNorman_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    // paletten: de geselecteerde titel pulseert, de knoppen, het tv-licht flakkert
    pal[NOR_HL] = ((t >> 3) & 1) ? RGB(20, 20, 20) : RGB(31, 31, 31);
    k = (t >= NOR_HOVER && t < NOR_BACK);
    pal[32 + NOR_BTN_A] = k ? RGB(8, 8, 8) : RGB(27, 2, 3);
    pal[32 + NOR_BTN_B] = k ? RGB(27, 2, 3) : RGB(8, 8, 8);
    if (t >= NOR_PRESS && t < NOR_PRESS + 4)
        pal[32 + NOR_BTN_A] = RGB(31, 24, 24);
    k = Random() % 3;
    if (((t >> 2) & 1) && k)
    {
        pal[16 + NOR_WALL_LIT] = RGB(9, 10, 16);
        pal[16 + NOR_SCREEN] = RGB(7, 9, 17);
    }
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);
    // achter de vraag (en de pauzeknop) dimt het startscherm
    if (t >= NOR_STILL && t < NOR_ROOM)
        BlendPalette(BG_PLTT_ID(13), 16, 9, RGB_BLACK);

    // welk beeld
    if (t < NOR_HOME)
        map = -1;
    else if (t < NOR_STILL)
        map = NOR_MAP_HOME;
    else if (t < NOR_PAUSE)
        map = NOR_MAP_STILL;
    else if (t < NOR_ROOM)
        map = NOR_MAP_PAUSE;
    else if (t < NOR_SUB1)
        map = NOR_MAP_ROOM;
    else if (t < NOR_SUB2)
        map = NOR_MAP_ROOM1;
    else
        map = NOR_MAP_ROOM2;
    if (map >= 0 && map != task->tGiShown)
    {
        if (task->tGiShown == 0xFF)
            GI_KillFieldWindows();
        GI_ShowMap(map);
        task->tGiShown = map;
    }

    // het beeld krimpt terug in de tv (venster 0; daarbuiten zwart)
    if (t == NOR_SHRINK)
    {
        GI_InitWindow();
        sTransitionData->WINOUT = 0;
        GI_SetRectWindow(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT);
        PlaySE(SE_PC_OFF);
    }
    if (t > NOR_SHRINK && t < NOR_ROOM)
    {
        p = t - NOR_SHRINK;
        p = p * p * 256 / (NOR_SHRINK_LEN * NOR_SHRINK_LEN);
        GI_SetRectWindow(24 * p / 256, 48 * p / 256, DISPLAY_WIDTH - (DISPLAY_WIDTH - 96) * p / 256, DISPLAY_HEIGHT - (DISPLAY_HEIGHT - 96) * p / 256);
    }
    if (t == NOR_ROOM)
    {
        GI_EndWindow();
        norman->invisible = FALSE;
        slaking->invisible = FALSE;
        PlaySE(SE_M_SNORE);
    }

    // Zzz boven Slaking, tot hij wakker schrikt
    for (i = 0; i < 2; i++)
    {
        z = &gSprites[task->data[12 + i]];
        k = t - NOR_ROOM - i * 14;
        z->invisible = (k < 0 || t >= NOR_SUB2);
        if (k < 0)
            continue;
        k %= 28;
        z->x = NOR_SLAKING_X + 22 + k / 2 + ((k >> 2) & 1);
        z->y = NOR_SLAKING_Y - 24 - k * 2 / 3;
    }

    // "FACE MY SLAKING!": Slaking springt op, kreet, dreun
    if (t == NOR_SUB1)
        PlaySE(SE_M_SWAGGER);
    if (t == NOR_SUB2)
    {
        PlayCry_Normal(SPECIES_SLAKING, 0);
        PlaySE(SE_M_STRENGTH);
    }
    slaking->y2 = 0;
    if (t >= NOR_SUB2 && t - NOR_SUB2 < (s32)ARRAY_COUNT(sNorHop))
        slaking->y2 = sNorHop[t - NOR_SUB2];
    norman->x2 = 0;
    if (t >= NOR_SUB1 && t < NOR_SUB2)
        norman->x2 = min((t - NOR_SUB1) / 2, 3);
    k = (t >= NOR_SUB2 && t < NOR_SUB2 + 10) ? 2 : 0;
    GI_Shake(k);

    GI_FadeWorld(t, NOR_HOME, keep);
    if (t >= NOR_HOME && t < NOR_HOME + 8)
        BlendPalettes(GI_BG_PALS, 16 - (t - NOR_HOME) * 2, RGB_BLACK);
    GI_Flash(t, NOR_PAUSE, 4, 8, 0, RGB_WHITE);
    GI_Flash(t, NOR_SUB2, 6, 10, keep, RGB_WHITE);
    if (GI_WhiteOut(t, NOR_END, keep))
    {
        norman->invisible = slaking->invisible = TRUE;
        for (i = 0; i < 2; i++)
            gSprites[task->data[12 + i]].invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTNorman_Finish(struct Task *task)
{
    u32 i;

    GI_Shake(0);
    GI_EndWindow();
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroyMonPic(task->tGiSprite1);
    for (i = 0; i < 2; i++)
        GI_DestroySprite(task->data[12 + i]);
    GI_FreeTag(NOR_TAG_Z);
    GI_Free();
}

static const struct RouteTransition sRT_GymNorman =
{
    sPikachu_Tileset, 32, sGymNorman_Pal + 32, 1, 1, 0, RTNorman_Init, RTNorman_Update, RTNorman_Finish
};

static void Task_GymNorman(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymNorman);
}

// ---------------- Winona (budgetvliegmaatschappij, jetlag, "I just want to retreat to my tree house"): het vertrekbord
// van WINAIR, WN001 naar FORTREE staat op DELAYED; de flappen ratelen om naar BOARDING (ding-dong). Dan de gate: door het
// raam vliegt haar 'vliegtuig' over (Altaria), "Elegant. Soaring. Delayed.", en haar koffertje springt open: veren alle
// kanten op, "BAGGAGE FEE!" / "No miles earned." tools/grounded/winona_transition.py
static const u32 sGymWinona_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_winona.4bpp.smol");
static const u32 sGymWinona_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_winona_maps.bin.smol");
static const u16 sGymWinona_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_winona.gbapal");
static const u32 sGymWinona_CaseGfx[] = INCBIN_U32("graphics/battle_transitions/gym_winona_case.4bpp.smol");
static const u16 sGymWinona_CasePal[] = INCBIN_U16("graphics/battle_transitions/gym_winona_case.gbapal");

enum { WIN_MAP_DELAYED, WIN_MAP_FLAP1, WIN_MAP_FLAP2, WIN_MAP_BOARDING, WIN_MAP_GATE, WIN_MAP_GATE1, WIN_MAP_GATE2 };
#define WIN_TAG_CASE     0x5A41
#define WIN_TAG_FEATHER  0x5A42
// leestijd: vooral het einde (de grap) langer in beeld
#define WIN_BOARD        8
#define WIN_FLIP         (WIN_BOARD + 48)   // het bord met DELAYED (was 32)
#define WIN_CHIME        (WIN_FLIP + 16)
#define WIN_GATE         (WIN_FLIP + 44)    // (was 38)
#define WIN_SUB1         (WIN_GATE + 8)
#define WIN_FLY          (WIN_GATE + 4)
#define WIN_FLY_LEN      84
#define WIN_POP          (WIN_SUB1 + 84)    // "Elegant. Soaring. Delayed." (was 46)
#define WIN_END          (WIN_POP + 120)    // "BAGGAGE FEE!" / "No miles earned." (was 42)
#define WIN_STATUS       7      // BG 13: de statusflap van WN001
#define WIN_FEATHERS     4
#define WIN_CASE_X       130
#define WIN_CASE_Y       128

// de flappen: welk beeld op welk frame (vanaf WIN_FLIP)
static const u8 sWinFlaps[] = {WIN_MAP_FLAP1, WIN_MAP_FLAP2, WIN_MAP_FLAP1, WIN_MAP_FLAP2, WIN_MAP_BOARDING};
// veren: vx, vy (1/16 px per frame)
static const s8 sWinFeather[WIN_FEATHERS][2] = {{-34, -60}, {26, -72}, {-12, -84}, {44, -48}};

static void RTWinona_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sGymWinona_Tiles, sGymWinona_Maps);
    LoadPalette(sGymWinona_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_WINONA, 92, 108);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_MonPic(SPECIES_ALTARIA, 280, 60);
    task->tGiSprite2 = GI_CreateSprite(sGymWinona_CaseGfx, 32 * 64 / 2, sGymWinona_CasePal, WIN_TAG_CASE, &sGI_Oam32, WIN_CASE_X, WIN_CASE_Y, 1);
    gSprites[task->tGiSprite2].invisible = TRUE;
    for (i = 0; i < WIN_FEATHERS; i++)
    {
        task->data[12 + i] = GI_CreateSprite(gBattleAnimSpriteGfx_WhiteFeather, 32 * 64 / 2, gBattleAnimSpritePal_WhiteFeather, WIN_TAG_FEATHER, &sGI_Oam32, WIN_CASE_X, WIN_CASE_Y, 0);
        gSprites[task->data[12 + i]].invisible = TRUE;
    }
    task->tGiShown = 0xFF;
}

static bool8 RTWinona_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, map;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    struct Sprite *winona = &gSprites[task->tGiSprite0];
    struct Sprite *altaria = GI_Sprite(task->tGiSprite1);
    struct Sprite *suitcase = &gSprites[task->tGiSprite2];
    struct Sprite *fe;

    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_WINONA) | GI_SpritePalBit(SPECIES_ALTARIA) | GI_SpritePalBit(WIN_TAG_CASE)
         | GI_SpritePalBit(WIN_TAG_FEATHER);
    GI_ResetPals(keep);
    LoadPalette(sGymWinona_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    // de statusflap knippert: rood (DELAYED), dan groen (BOARDING)
    if (t < WIN_FLIP)
        pal[WIN_STATUS] = ((t >> 3) & 1) ? RGB(16, 4, 3) : RGB(29, 8, 6);
    else if (t >= WIN_FLIP + 16)
        pal[WIN_STATUS] = ((t >> 2) & 1) ? RGB(8, 22, 8) : RGB(14, 31, 12);
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], PLTT_SIZE_4BPP);

    // welk beeld
    if (t < WIN_BOARD)
        map = -1;
    else if (t < WIN_FLIP)
        map = WIN_MAP_DELAYED;
    else if (t < WIN_GATE)
        map = sWinFlaps[min((t - WIN_FLIP) / 4, (s32)ARRAY_COUNT(sWinFlaps) - 1)];
    else if (t < WIN_SUB1)
        map = WIN_MAP_GATE;
    else if (t < WIN_POP)
        map = WIN_MAP_GATE1;
    else
        map = WIN_MAP_GATE2;
    if (map >= 0 && map != task->tGiShown)
    {
        if (task->tGiShown == 0xFF)
            GI_KillFieldWindows();
        // het bord: alleen de statusflap van WN001 verandert
        if (map <= WIN_MAP_BOARDING && task->tGiShown <= WIN_MAP_BOARDING)
        {
            GI_PutRect(map, 18, 5, 12, 3, 18, 5);
            PlaySE(SE_CLICK);
        }
        else
        {
            GI_ShowMap(map);
        }
        task->tGiShown = map;
    }
    if (t == WIN_CHIME)
        PlaySE(SE_DING_DONG);

    // de gate: Winona en haar koffertje, Altaria vliegt voorbij
    if (t == WIN_GATE)
    {
        winona->invisible = FALSE;
        suitcase->invisible = FALSE;
        altaria->invisible = FALSE;
        PlaySE(SE_M_FLY);
    }
    if (t >= WIN_FLY)
    {
        k = min(t - WIN_FLY, WIN_FLY_LEN);
        altaria->x = 280 - k * 320 / WIN_FLY_LEN;
        altaria->y = 58 + (Sin((t * 8) & 0xFF, 5));
        if (t == WIN_FLY + 30)
            PlayCry_Normal(SPECIES_ALTARIA, 0);
        if (t >= WIN_FLY && ((t - WIN_FLY) % 24) == 0 && t < WIN_FLY + 72)
            PlaySE(SE_TAILLOW_WING_FLAP);
    }
    // Winona zucht (zakt een pixel), het koffertje wiebelt en springt open
    winona->y2 = (t >= WIN_SUB1 && t < WIN_POP && ((t >> 4) & 1)) ? 1 : 0;
    suitcase->x2 = (t >= WIN_POP - 12 && t < WIN_POP) ? (((t >> 1) & 1) ? 1 : -1) : 0;
    if (t == WIN_POP)
    {
        suitcase->oam.tileNum = GetSpriteTileStartByTag(WIN_TAG_CASE) + 16;
        PlaySE(SE_BALL_OPEN);
    }
    if (t == WIN_POP + 4)
        PlaySE(SE_M_SWAGGER);
    for (i = 0; i < WIN_FEATHERS; i++)
    {
        fe = &gSprites[task->data[12 + i]];
        k = t - WIN_POP - i;
        if (k < 0)
            continue;
        fe->invisible = FALSE;
        // eerst omhoog, dan dwarrelen ze heen en weer naar beneden
        fe->x = WIN_CASE_X + sWinFeather[i][0] * min(k, 20) / 16 + (k > 20 ? Sin(((k - 20) * 6 + i * 64) & 0xFF, 8) : 0);
        fe->y = WIN_CASE_Y - 8 + (sWinFeather[i][1] * min(k, 20) + 2 * min(k, 20) * min(k, 20)) / 16 + (k > 20 ? (k - 20) / 3 : 0);
        fe->oam.tileNum = GetSpriteTileStartByTag(WIN_TAG_FEATHER) + (((k >> 3) + i) & 1) * 16;
    }
    GI_Shake((t >= WIN_POP && t < WIN_POP + 8) ? 2 : 0);

    GI_FadeWorld(t, WIN_BOARD, keep);
    if (t >= WIN_BOARD && t < WIN_BOARD + 8)
        BlendPalettes(GI_BG_PALS, 16 - (t - WIN_BOARD) * 2, RGB_BLACK);
    GI_Flash(t, WIN_GATE, 6, 12, keep, RGB_WHITE);
    GI_Flash(t, WIN_POP, 6, 8, keep, RGB_WHITE);
    if (GI_WhiteOut(t, WIN_END, keep))
    {
        winona->invisible = altaria->invisible = suitcase->invisible = TRUE;
        for (i = 0; i < WIN_FEATHERS; i++)
            gSprites[task->data[12 + i]].invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTWinona_Finish(struct Task *task)
{
    u32 i;

    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroyMonPic(task->tGiSprite1);
    GI_DestroySprite(task->tGiSprite2);
    for (i = 0; i < WIN_FEATHERS; i++)
        GI_DestroySprite(task->data[12 + i]);
    GI_FreeTag(WIN_TAG_CASE);
    GI_FreeTag(WIN_TAG_FEATHER);
    GI_Free();
}

static const struct RouteTransition sRT_GymWinona =
{
    sPikachu_Tileset, 32, sGymWinona_Pal + 32, 1, 1, 0, RTWinona_Init, RTWinona_Update, RTWinona_Finish
};

static void Task_GymWinona(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymWinona);
}

// ---------------- Tate & Liza ("Twin Flame energy", tarot, "your aura screaming in lowercase"; Jordi: tarotkaarten,
// ouijaborden en vage spirituele shit tot een psychic overload). Een ouijabord bij paarse kaarsvlammen: de planchette
// spelt R-I-P en schiet naar GOOD BYE. Drie tarotkaarten draaien om (THE TWINS, THE MOON, DEATH (yours)): "TATE: The
// cards have spoken..." / "LIZA: ...and they hate you." Dan de overload: psychische ringen razen naar buiten
// (paletcyclus), ogen gaan open, lepels buigen en cirkelen om de tweeling, "TWIN FLAME ENERGY: PEAK PERFORMANCE", en dan
// alleen nog "aaaaaaaaaaaaah" (your aura, screaming in lowercase). tools/grounded/tateliza_transition.py
static const u32 sGymTateLiza_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_tateliza.4bpp.smol");
static const u32 sGymTateLiza_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_tateliza_maps.bin.smol");
static const u16 sGymTateLiza_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_tateliza.gbapal");
static const u32 sGymTateLiza_PlanchetteGfx[] = INCBIN_U32("graphics/battle_transitions/gym_tateliza_planchette.4bpp.smol");
static const u16 sGymTateLiza_PlanchettePal[] = INCBIN_U16("graphics/battle_transitions/gym_tateliza_planchette.gbapal");

enum {
    TL_MAP_OUIJA0, TL_MAP_OUIJA1, TL_MAP_OUIJA2, TL_MAP_OUIJA3,
    TL_MAP_BACK, TL_MAP_HALF_B, TL_MAP_EDGE, TL_MAP_HALF_F, TL_MAP_FRONT, TL_MAP_SUB1, TL_MAP_SUB2,
    TL_MAP_RINGS, TL_MAP_RINGS1, TL_MAP_RINGS2,
};
enum { TL_SPR_PLANCHETTE, TL_SPR_FLAME0, TL_SPR_FLAME1, TL_SPR_EYE0, TL_SPR_SPOON0 = TL_SPR_EYE0 + 4, TL_SPR_COUNT = TL_SPR_SPOON0 + 4 };
#define TL_TAG_PLANCHETTE 0x5A43
#define TL_TAG_FLAME      0x5A44
#define TL_TAG_EYE        0x5A45
#define TL_TAG_SPOON      0x5A46
// leestijd: vooral het einde (de grap) langer in beeld
#define TL_OUIJA          8
#define TL_TAROT          84
#define TL_FLIP           (TL_TAROT + 20)   // "TATE: The cards have spoken..." eerst even alleen (was 8)
#define TL_FLIP_GAP       16                // tijd per kaart (was 12)
#define TL_SUB2           (TL_FLIP + 2 * TL_FLIP_GAP + 12)
#define TL_OVER           (TL_SUB2 + 96)    // "LIZA: ...and they hate you." (was 10)
#define TL_SCREAM         (TL_OVER + 84)    // "TWIN FLAME ENERGY: PEAK PERFORMANCE" (was 30)
#define TL_END            (TL_SCREAM + 66)  // "aaaaaaaaaaaaah" (was 26)
#define TL_CX             120
#define TL_CY             88

static EWRAM_DATA u8 sTL_Sprites[TL_SPR_COUNT] = {0};

// de planchette: begin, duur, doel (gat bovenin op de letter: sprite-midden = letter + (0, 5))
static const s16 sTLMoves[][4] = {
    {14, 12, 95, 57 + 5},     // R
    {32, 10, 150, 32 + 5},    // I
    {48, 10, 70, 61 + 5},     // P
    {64, 8, 120, 112 + 5},    // GOOD BYE
};
static const u8 sTLCardCols[] = {4, 12, 20};
static const s16 sTLEyePos[4][2] = {{36, 48}, {204, 48}, {52, 128}, {188, 128}};

static const struct OamData sGI_Oam16x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .shape = SPRITE_SHAPE(16x32),
    .size = SPRITE_SIZE(16x32),
    .priority = 0,
};

static void RTTateLiza_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sGymTateLiza_Tiles, sGymTateLiza_Maps);
    LoadPalette(sGymTateLiza_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_LEADER_TATE_AND_LIZA, TL_CX, TL_CY + 4);
    gSprites[task->tGiSprite0].invisible = TRUE;
    sTL_Sprites[TL_SPR_PLANCHETTE] = GI_CreateSprite(sGymTateLiza_PlanchetteGfx, 32 * 32 / 2, sGymTateLiza_PlanchettePal, TL_TAG_PLANCHETTE, &sGI_Oam32, 120, 100, 0);
    sTL_Sprites[TL_SPR_FLAME0] = GI_CreateSprite(gBattleAnimSpriteGfx_PurpleFlame, 16 * 128 / 2, gBattleAnimSpritePal_PurpleFlame, TL_TAG_FLAME, &sGI_Oam16x32, 24, 112, 1);
    sTL_Sprites[TL_SPR_FLAME1] = GI_CreateSprite(gBattleAnimSpriteGfx_PurpleFlame, 16 * 128 / 2, gBattleAnimSpritePal_PurpleFlame, TL_TAG_FLAME, &sGI_Oam16x32, 215, 112, 1);
    for (i = 0; i < 4; i++)
    {
        sTL_Sprites[TL_SPR_EYE0 + i] = GI_CreateSprite(gBattleAnimSpriteGfx_OpeningEye, 32 * 128 / 2, gBattleAnimSpritePal_OpeningEye, TL_TAG_EYE, &sGI_Oam32, sTLEyePos[i][0], sTLEyePos[i][1], 1);
        sTL_Sprites[TL_SPR_SPOON0 + i] = GI_CreateSprite(gBattleAnimSpriteGfx_BentSpoon, 16 * 192 / 2, gBattleAnimSpritePal_BentSpoon, TL_TAG_SPOON, &sGI_Oam16x32, TL_CX, TL_CY, 0);
    }
    for (i = 0; i < TL_SPR_COUNT; i++)
        gSprites[sTL_Sprites[i]].invisible = TRUE;
    task->tGiShown = 0xFF;
}

static bool8 RTTateLiza_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, x, y, map, phase;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(14)];
    struct Sprite *twins = &gSprites[task->tGiSprite0];
    struct Sprite *pl = &gSprites[sTL_Sprites[TL_SPR_PLANCHETTE]];
    struct Sprite *s;

    keep = GI_TrainerPalBit(TRAINER_PIC_LEADER_TATE_AND_LIZA) | GI_SpritePalBit(TL_TAG_PLANCHETTE) | GI_SpritePalBit(TL_TAG_FLAME)
         | GI_SpritePalBit(TL_TAG_EYE) | GI_SpritePalBit(TL_TAG_SPOON);
    GI_ResetPals(keep);
    LoadPalette(sGymTateLiza_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    // de ringen lopen naar buiten (BG 14 index 1-8), bij de schreeuw elke frame
    phase = (t >= TL_SCREAM) ? t * 2 : t / 3;
    for (i = 0; i < 8; i++)
        pal[1 + i] = sGymTateLiza_Pal[16 + 1 + ((i - phase) & 7)];
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(14)], PLTT_SIZE_4BPP);

    // welk beeld (het ouijabord: de letters komen erbij als de planchette erop staat)
    if (t < TL_OUIJA)
        map = -1;
    else if (t < TL_TAROT)
    {
        map = TL_MAP_OUIJA0;
        for (i = 0; i < 3; i++)
            if (t >= sTLMoves[i][0] + sTLMoves[i][1])
                map = TL_MAP_OUIJA1 + i;
    }
    else if (t < TL_OVER)
        map = TL_MAP_BACK;
    else if (t < TL_SCREAM)
        map = TL_MAP_RINGS;
    else
        map = TL_MAP_RINGS2;
    if (map >= 0 && map != task->tGiShown)
    {
        if (task->tGiShown == 0xFF)
            GI_KillFieldWindows();
        if (map >= TL_MAP_OUIJA1 && map <= TL_MAP_OUIJA3)
        {
            GI_PutRect(map, 20, 15, 8, 3, 20, 15);
            PlaySE(SE_PIN);
        }
        else
        {
            GI_ShowMap(map);
        }
        task->tGiShown = map;
    }

    // het ouijabord: kaarsvlammen en de planchette
    if (t == TL_OUIJA)
    {
        pl->invisible = FALSE;
        gSprites[sTL_Sprites[TL_SPR_FLAME0]].invisible = FALSE;
        gSprites[sTL_Sprites[TL_SPR_FLAME1]].invisible = FALSE;
        PlaySE(SE_M_CONFUSE_RAY);
    }
    if (t < TL_TAROT)
    {
        for (i = 0; i < 2; i++)
            gSprites[sTL_Sprites[TL_SPR_FLAME0 + i]].oam.tileNum = GetSpriteTileStartByTag(TL_TAG_FLAME) + (((t >> 2) + i * 2) & 3) * 8;
        x = 120;
        y = 100;
        for (i = 0; i < (s32)ARRAY_COUNT(sTLMoves); i++)
        {
            if (t < sTLMoves[i][0])
                break;
            k = min(t - sTLMoves[i][0], sTLMoves[i][1]);
            // glijden met uitlopen: k * (2n - k) / n^2
            x = x + (sTLMoves[i][2] - x) * k * (2 * sTLMoves[i][1] - k) / (sTLMoves[i][1] * sTLMoves[i][1]);
            y = y + (sTLMoves[i][3] - y) * k * (2 * sTLMoves[i][1] - k) / (sTLMoves[i][1] * sTLMoves[i][1]);
        }
        pl->x = x;
        pl->y = y;
        // het bord trilt een beetje als de geest erin zit
        pl->x2 = (t & 2) ? 1 : 0;
        if (t == sTLMoves[3][0])
            PlaySE(SE_M_LEER);
    }
    if (t == TL_TAROT)
    {
        pl->invisible = TRUE;
        gSprites[sTL_Sprites[TL_SPR_FLAME0]].invisible = TRUE;
        gSprites[sTL_Sprites[TL_SPR_FLAME1]].invisible = TRUE;
    }

    // tarot: de kaarten draaien een voor een om (achterkant, half, zijkant, half, voorkant)
    if (t >= TL_TAROT && t < TL_OVER)
    {
        if (t == TL_TAROT + 4)
            GI_PutRect(TL_MAP_SUB1, 0, 0, 30, 3, 0, 0);
        for (i = 0; i < 3; i++)
        {
            k = t - (TL_FLIP + i * TL_FLIP_GAP);
            if (k < 0 || k > 6 || (k & 1))
                continue;
            GI_PutRect(TL_MAP_HALF_B + k / 2, sTLCardCols[i], 4, 7, 12, sTLCardCols[i], 4);
            if (k == 0)
                PlaySE(SE_RG_CARD_FLIP);
        }
        if (t == TL_SUB2)
        {
            GI_PutRect(TL_MAP_SUB2, 0, 0, 30, 3, 0, 0);
            PlaySE(SE_M_NIGHTMARE);
        }
    }

    // de overload
    if (t == TL_OVER)
    {
        twins->invisible = FALSE;
        PlaySE(SE_M_PSYBEAM);
    }
    if (t == TL_OVER + 4)
        GI_ShowRows(TL_MAP_RINGS1, 0, 3);
    if (t >= TL_OVER)
    {
        for (i = 0; i < 4; i++)
        {
            // ogen gaan open
            s = &gSprites[sTL_Sprites[TL_SPR_EYE0 + i]];
            k = t - (TL_OVER + 6 + i * 5);
            if (k >= 0)
            {
                s->invisible = FALSE;
                s->oam.tileNum = GetSpriteTileStartByTag(TL_TAG_EYE) + min(k / 2, 3) * 16;
                if (k == 0)
                    PlaySE(SE_M_LEER);
            }
            // lepels buigen en cirkelen, steeds sneller
            s = &gSprites[sTL_Sprites[TL_SPR_SPOON0 + i]];
            k = t - TL_OVER;
            s->invisible = FALSE;
            phase = (k * k / 24 + k * 2 + i * 64) & 0xFF;
            s->x = TL_CX + Cos(phase, 60);
            s->y = TL_CY + Sin(phase, 36);
            s->oam.tileNum = GetSpriteTileStartByTag(TL_TAG_SPOON) + min(k / 5, 5) * 8;
        }
        if (t == TL_OVER + 16)
            PlaySE(SE_M_PSYBEAM2);
        if (t == TL_SCREAM)
            PlaySE(SE_M_SCREECH);
        k = (t >= TL_SCREAM + 24) ? 1 : (t >= TL_SCREAM) ? 3 : ((t >= TL_OVER + 20) ? 1 : 0);
        GI_Shake(k);
        twins->x2 = k ? (s16)(Random() % (k * 2 + 1)) - k : 0;
        twins->y2 = k ? (s16)(Random() % (k * 2 + 1)) - k : 0;
    }

    GI_FadeWorld(t, TL_OUIJA, keep);
    if (t >= TL_OUIJA && t < TL_OUIJA + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - TL_OUIJA) * 2, RGB_BLACK);
    GI_Flash(t, TL_TAROT, 4, 10, keep, RGB_WHITE);
    GI_Flash(t, TL_OVER, 6, 12, keep, RGB(31, 20, 31));
    // stroboscoop bij de schreeuw
    // (alleen het begin: daarna blijft het beeld rustig genoeg om de schreeuw te lezen)
    if (t >= TL_SCREAM && t < TL_SCREAM + 24 && ((t >> 1) & 1))
        BlendPalettes(GI_BG_PALS | keep, 9, (t & 4) ? RGB_WHITE : RGB(31, 8, 28));
    if (GI_WhiteOut(t, TL_END, keep))
    {
        twins->invisible = TRUE;
        for (i = 0; i < TL_SPR_COUNT; i++)
            gSprites[sTL_Sprites[i]].invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTTateLiza_Finish(struct Task *task)
{
    u32 i;

    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    for (i = 0; i < TL_SPR_COUNT; i++)
        GI_DestroySprite(sTL_Sprites[i]);
    GI_FreeTag(TL_TAG_PLANCHETTE);
    GI_FreeTag(TL_TAG_FLAME);
    GI_FreeTag(TL_TAG_EYE);
    GI_FreeTag(TL_TAG_SPOON);
    GI_Free();
}

static const struct RouteTransition sRT_GymTateLiza =
{
    sPikachu_Tileset, 32, sGymTateLiza_Pal + 32, 1, 1, 0, RTTateLiza_Init, RTTateLiza_Update, RTTateLiza_Finish
};

static void Task_GymTateLiza(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymTateLiza);
}

// ---------------- Wallace (sommelier van de Crater Pub: "Your spirit has a certain... bouquet.", "a performance of
// liquid illusions", "Santé!"). Een zwevende fles (illusie) schenkt een groot wijnglas vol, laag voor laag (paletten);
// Wallace walst mee. De wijn kleurt Hoenn-blauw ("Notes of brine, regret and KYOGRE."), het glas springt, en een golf
// slaat van rechts over de pub (kolommen + Splash op het front). "SANTÉ!" tools/grounded/wallace_transition.py
static const u32 sGymWallace_Tiles[] = INCBIN_U32("graphics/battle_transitions/gym_wallace.4bpp.smol");
static const u32 sGymWallace_Maps[] = INCBIN_U32("graphics/battle_transitions/gym_wallace_maps.bin.smol");
static const u16 sGymWallace_Pal[] = INCBIN_U16("graphics/battle_transitions/gym_wallace.gbapal");
static const u32 sGymWallace_StreamGfx[] = INCBIN_U32("graphics/battle_transitions/gym_wallace_stream.4bpp.smol");
static const u16 sGymWallace_StreamPal[] = INCBIN_U16("graphics/battle_transitions/gym_wallace_stream.gbapal");

enum { WAL_MAP_PUB, WAL_MAP_PUB1, WAL_MAP_PUB2, WAL_MAP_PUB3, WAL_MAP_BROKEN, WAL_MAP_WAVE, WAL_MAP_SANTE };
#define WAL_TAG_STREAM   0x5A47
#define WAL_TAG_SPLASH   0x5A48
// ±25% langzamer dan de eerste versie (Jordi: "echt net iets te snel")
#define WAL_PUB          8
#define WAL_POUR         18
#define WAL_SUB1         33
#define WAL_SUB2         75
#define WAL_SWIRL        85
#define WAL_BLUE         115
#define WAL_BLUE_LEN     20
#define WAL_BREAK        145
#define WAL_WAVE         155
#define WAL_WAVE_LEN     19    // het golffront loopt in zoveel frames over het scherm
#define WAL_SANTE        (WAL_WAVE + 28)
#define WAL_END          (WAL_SANTE + 44)
#define WAL_BANDS        8
#define WAL_WATER        7     // BG 15 index 7-10: water

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

static void RTWallace_Init(struct Task *task)
{
    u32 i;

    GI_LoadGfx(sGymWallace_Tiles, sGymWallace_Maps);
    LoadPalette(sGymWallace_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    task->tGiSprite0 = GI_TrainerPic(TRAINER_PIC_CHAMPION_WALLACE, 64, 100);
    gSprites[task->tGiSprite0].invisible = TRUE;
    task->tGiSprite1 = GI_CreateSprite(sGymWallace_StreamGfx, 8 * 32 / 2, sGymWallace_StreamPal, WAL_TAG_STREAM, &sGI_Oam8x32, 176, 58, 1);
    task->tGiSprite2 = GI_CreateSprite(sGymWallace_StreamGfx, 8 * 32 / 2, sGymWallace_StreamPal, WAL_TAG_STREAM, &sGI_Oam8x32, 176, 90, 1);
    gSprites[task->tGiSprite1].invisible = gSprites[task->tGiSprite2].invisible = TRUE;
    for (i = 0; i < 3; i++)
    {
        task->data[12 + i] = GI_CreateSprite(gBattleAnimSpriteGfx_Splash, 64 * 64 / 2, gBattleAnimSpritePal_Splash, WAL_TAG_SPLASH, &sGI_Oam64, 260, 44 + i * 44, 0);
        gSprites[task->data[12 + i]].invisible = TRUE;
    }
    task->tGiShown = 0xFF;
}

static bool8 RTWallace_Update(struct Task *task)
{
    s32 t = task->tRtTimer, k, i, filled, front;
    u32 keep;
    u16 *pal = &gPlttBufferUnfaded[BG_PLTT_ID(13)];
    u16 wine;
    struct Sprite *wallace = &gSprites[task->tGiSprite0];
    struct Sprite *s;

    keep = GI_TrainerPalBit(TRAINER_PIC_CHAMPION_WALLACE) | GI_SpritePalBit(WAL_TAG_STREAM) | GI_SpritePalBit(WAL_TAG_SPLASH);
    GI_ResetPals(keep);
    LoadPalette(sGymWallace_Pal, BG_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    // de wijn: laag voor laag vol, de bovenste laag glinstert bij het walsen, dan kleurt alles Hoenn-blauw
    filled = (t < WAL_POUR + 4) ? 0 : min((t - WAL_POUR - 4) * 2 / 15 + 1, WAL_BANDS);
    k = (t < WAL_BLUE) ? 0 : min(t - WAL_BLUE, WAL_BLUE_LEN);
    wine = GI_MixColor(RGB(15, 2, 5), RGB(4, 11, 25), k, WAL_BLUE_LEN);
    for (i = 0; i < WAL_BANDS; i++)
    {
        u16 c = (i < filled) ? wine : RGB(8, 4, 3);
        if (i == filled - 1 && t >= WAL_SWIRL && ((t >> 2) & 1))
            c = GI_MixColor(wine, RGB_WHITE, 1, 5);
        pal[16 + 1 + i] = c;
    }
    // het water van de golf loopt rond
    for (i = 0; i < 4; i++)
        pal[32 + WAL_WATER + i] = sGymWallace_Pal[32 + WAL_WATER + ((i + (t >> 2)) & 3)];
    CpuCopy16(pal, &gPlttBufferFaded[BG_PLTT_ID(13)], 3 * PLTT_SIZE_4BPP);

    if (t == WAL_PUB)
    {
        GI_KillFieldWindows();
        GI_ShowMap(WAL_MAP_PUB);
        wallace->invisible = FALSE;
        task->tGiShown = WAL_MAP_PUB;
    }
    if (t == WAL_SUB1)
        GI_ShowRows(WAL_MAP_PUB1, 0, 3);
    if (t == WAL_SUB2)
        GI_ShowRows(WAL_MAP_PUB2, 0, 3);
    if (t == WAL_BLUE + 4)
        GI_ShowRows(WAL_MAP_PUB3, 0, 3);

    // schenken
    if (t == WAL_POUR)
    {
        gSprites[task->tGiSprite1].invisible = gSprites[task->tGiSprite2].invisible = FALSE;
        PlaySE(SE_M_BUBBLE);
    }
    if (t >= WAL_POUR && t < WAL_SWIRL && ((t - WAL_POUR) % 16) == 8)
        PlaySE(SE_M_BUBBLE2);
    if (t == WAL_SWIRL)
    {
        gSprites[task->tGiSprite1].invisible = gSprites[task->tGiSprite2].invisible = TRUE;
        PlaySE(SE_M_WHIRLPOOL);
    }
    // Wallace walst mee (en blijft walsen, ook in de golf)
    wallace->x2 = (t >= WAL_SWIRL) ? Sin((t * 6) & 0xFF, 2) : 0;
    if (t == WAL_BLUE)
        PlaySE(SE_M_RAIN_DANCE);

    // het glas springt
    if (t == WAL_BREAK)
    {
        GI_ShowMap(WAL_MAP_BROKEN);
        GI_ShowRows(WAL_MAP_PUB3, 0, 3);
        PlaySE(SE_ICE_BREAK);
    }
    // de golf slaat van rechts over de pub: kolommen van het waterbeeld, Splash op het front
    if (t >= WAL_WAVE)
    {
        front = 30 - min((t - WAL_WAVE) * 30 / WAL_WAVE_LEN, 30);
        // na SANTÉ uit het SANTÉ-beeld (de tekst loopt door tot in rij 3)
        if (front < 30)
            GI_PutRect(t >= WAL_SANTE ? WAL_MAP_SANTE : WAL_MAP_WAVE, front, 3, 30 - front, 15, front, 3);
        for (i = 0; i < 3; i++)
        {
            s = &gSprites[task->data[12 + i]];
            s->invisible = (front <= 0 && t > WAL_WAVE + WAL_WAVE_LEN + 3) || t >= WAL_SANTE;
            s->x = front * 8 + 8 + ((i & 1) ? 6 : 0);
            s->y = 44 + i * 40 + ((t >> 1) & 1);
        }
        if (t == WAL_WAVE)
            PlaySE(SE_M_SURF);
    }
    if (t == WAL_SANTE)
    {
        GI_ShowRows(WAL_MAP_SANTE, 0, 4);
        PlaySE(SE_GLASS_FLUTE);
    }
    if (t >= WAL_BREAK && t < WAL_BREAK + 6)
        GI_Shake(3);
    else if (t >= WAL_WAVE && t < WAL_WAVE + WAL_WAVE_LEN + 3)
        GI_Shake(2);
    else
        GI_Shake(0);

    GI_FadeWorld(t, WAL_PUB, keep);
    if (t >= WAL_PUB && t < WAL_PUB + 8)
        BlendPalettes(GI_BG_PALS | keep, 16 - (t - WAL_PUB) * 2, RGB_BLACK);
    GI_Flash(t, WAL_BREAK, 6, 12, keep, RGB_WHITE);
    if (GI_WhiteOut(t, WAL_END, keep))
    {
        wallace->invisible = gSprites[task->tGiSprite1].invisible = gSprites[task->tGiSprite2].invisible = TRUE;
        for (i = 0; i < 3; i++)
            gSprites[task->data[12 + i]].invisible = TRUE;
        return TRUE;
    }
    return FALSE;
}

static void RTWallace_Finish(struct Task *task)
{
    u32 i;

    GI_Shake(0);
    GI_DestroyTrainerPic(task->tGiSprite0);
    GI_DestroySprite(task->tGiSprite1);
    GI_DestroySprite(task->tGiSprite2);
    for (i = 0; i < 3; i++)
        GI_DestroySprite(task->data[12 + i]);
    GI_FreeTag(WAL_TAG_STREAM);
    GI_FreeTag(WAL_TAG_SPLASH);
    GI_Free();
}

static const struct RouteTransition sRT_GymWallace =
{
    sPikachu_Tileset, 32, sGymWallace_Pal + 32, 1, 1, 0, RTWallace_Init, RTWallace_Update, RTWallace_Finish
};

static void Task_GymWallace(u8 taskId)
{
    RouteTransition_Run(taskId, &sRT_GymWallace);
}
