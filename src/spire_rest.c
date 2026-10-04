// Project Grounded: The Spire - rustplek (Snorlax-kamp, zie SPIRE_DESIGN.md).
// Een geïmproviseerd Pokémon Center: Snorlax slaapt in het midden, links Chansey (helen), rechts Porygon2 (een move
// upgraden). De achtergrond is de gevechtsachtergrond van het biome, in schemertinten.
// Upgrade ("+"): een aanval doet 30% meer schade, een statusmove verandert een stat één stap meer en mist niet;
// de move krijgt ook maximale PP. Opgeslagen als PP Up 3 op die slot (SPIRE_UPGRADED).
#include "global.h"
#include "battle.h"
#include "battle_bg.h"
#include "battle_environment.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "move.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "scanline_effect.h"
#include "sound.h"
#include "spire.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/characters.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

enum
{
    WIN_HEADER,
    WIN_LEFT,
    WIN_RIGHT,
    WIN_BOTTOM,
    WIN_COUNT,
};

enum
{
    STATE_MAIN,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_MOVE,
    STATE_MESSAGE,
    STATE_EXIT,
};

enum
{
    CHOICE_REST,
    CHOICE_UPGRADE,
};

#define PAL_FRAME_SEL 13
#define PAL_FRAME     14
#define PAL_TEXT      15
#define FRAME_TILE    0x200
#define TAG_HAND      0x5341

struct SpireRest
{
    void (*onDone)(void);
    u8 state;
    u8 choice;
    u8 mon;
    u8 slot;
    u8 done;
    u8 picSpriteIds[3];     // Chansey, Snorlax, Porygon2
    u8 iconSpriteIds[2];
    u8 handSpriteId;
    u16 timer;
    u8 message[128];
};

static EWRAM_DATA struct SpireRest *sRest = NULL;

static const u16 sHandCursor_Pal[] = INCBIN_U16("graphics/pokemon_storage/hand_cursor.gbapal");
static const u8 sHandCursor_Gfx[] = INCBIN_U8("graphics/pokemon_storage/hand_cursor.4bpp");

static const u16 sTextPal[16] =
{
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(8, 8, 9), RGB(26, 26, 27),
    RGB(5, 15, 29), RGB(23, 27, 31), RGB(25, 17, 1), RGB(31, 27, 17),
    RGB(19, 19, 20), RGB(5, 19, 9), RGB(22, 29, 23), RGB(29, 8, 7),
    RGB(31, 24, 23), RGB(10, 10, 11), RGB(15, 9, 22), RGB(26, 22, 30),
};
static const u8 sColor_Dark[]   = {1, 2, 3};
static const u8 sColor_Blue[]   = {1, 4, 5};
static const u8 sColor_Gold[]   = {1, 6, 7};
static const u8 sColor_Gray[]   = {1, 8, 3};
static const u8 sColor_Green[]  = {1, 9, 10};
static const u8 sColor_Red[]    = {1, 11, 12};
static const u8 sColor_Purple[] = {1, 14, 15};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 0},
    {.bg = 3, .charBaseIndex = 2, .mapBaseIndex = 26, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_LEFT]   = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 12, .width = 13, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_RIGHT]  = {.bg = 0, .tilemapLeft = 16, .tilemapTop = 12, .width = 13, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x053},
    [WIN_BOTTOM] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 16, .width = 28, .height = 3, .paletteNum = PAL_TEXT, .baseBlock = 0x06D},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam_Hand = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};
static const struct SpriteSheet sSpriteSheet_Hand = {sHandCursor_Gfx, 0x200, TAG_HAND};
static const struct SpritePalette sSpritePal_Hand = {sHandCursor_Pal, TAG_HAND};
static const struct SpriteTemplate sSpriteTemplate_Hand =
{
    .tileTag = TAG_HAND, .paletteTag = TAG_HAND, .oam = &sOam_Hand, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void Task_SpireRest(u8 taskId);

// ---------------------------------------------------------------------------------------------
// Upgrades (ook gebruikt in gevechten, zie spire.c)

bool32 Spire_IsSlotUpgraded(struct Pokemon *mon, u32 slot)
{
    return ((GetMonData(mon, MON_DATA_PP_BONUSES) >> (slot * 2)) & 3) == 3;
}

void Spire_UpgradeSlot(struct Pokemon *mon, u32 slot)
{
    u32 bonuses = GetMonData(mon, MON_DATA_PP_BONUSES) | (3 << (slot * 2));
    u32 pp;

    SetMonData(mon, MON_DATA_PP_BONUSES, &bonuses);
    pp = CalculatePPWithBonus(GetMonData(mon, MON_DATA_MOVE1 + slot), bonuses, slot);
    SetMonData(mon, MON_DATA_PP1 + slot, &pp);
}

void Spire_ClearSlotUpgrade(struct Pokemon *mon, u32 slot)
{
    u32 bonuses = GetMonData(mon, MON_DATA_PP_BONUSES) & ~(3 << (slot * 2));

    SetMonData(mon, MON_DATA_PP_BONUSES, &bonuses);
}

// Lege move-slots dichtschuiven (met PP en upgrade), zodat de cursor in gevecht nooit op een leeg slot staat
void Spire_CompactMoves(struct Pokemon *mon)
{
    u16 moves[MAX_MON_MOVES];
    u8 pp[MAX_MON_MOVES];
    u32 i, n = 0, bonuses = GetMonData(mon, MON_DATA_PP_BONUSES), newBonuses = 0;

    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        u16 move = GetMonData(mon, MON_DATA_MOVE1 + i);

        if (move == MOVE_NONE)
            continue;
        moves[n] = move;
        pp[n] = GetMonData(mon, MON_DATA_PP1 + i);
        newBonuses |= ((bonuses >> (i * 2)) & 3) << (n * 2);
        n++;
    }
    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        u16 move = (i < n) ? moves[i] : MOVE_NONE;
        u8 p = (i < n) ? pp[i] : 0;

        SetMonData(mon, MON_DATA_MOVE1 + i, &move);
        SetMonData(mon, MON_DATA_PP1 + i, &p);
    }
    SetMonData(mon, MON_DATA_PP_BONUSES, &newBonuses);
}

// ---------------------------------------------------------------------------------------------
// Achtergrond: gevechtsachtergrond van het biome (ook in de Spire-gevechten zelf)

static const u8 sBiomeEnvironment[SPIRE_BIOME_COUNT] =
{
    [SPIRE_BIOME_GROVE] = BATTLE_ENVIRONMENT_LONG_GRASS,
    [SPIRE_BIOME_DOCKS] = BATTLE_ENVIRONMENT_POND,
    [SPIRE_BIOME_HIVE]  = BATTLE_ENVIRONMENT_SAND,
    [SPIRE_BIOME_FROST] = BATTLE_ENVIRONMENT_GLACIA,
    [SPIRE_BIOME_COURT] = BATTLE_ENVIRONMENT_FRONTIER,
    [SPIRE_BIOME_ABYSS] = BATTLE_ENVIRONMENT_SIDNEY,
};

u32 Spire_GetBiomeEnvironment(void)
{
    return RUN.biome < SPIRE_BIOME_COUNT ? sBiomeEnvironment[RUN.biome] : BATTLE_ENVIRONMENT_PLAIN;
}

// Laadt de achtergrond op BG3 (tiles in charbase 2, tilemap in screenbase 26, paletten 2-4) en kleurt hem:
// tint = doelkleur, amount = 0-16 (hoeveel naar de tint toe), bijv. schemer = donkerpaars.
void Spire_LoadBiomeBackground(u16 tint, u32 amount)
{
    u32 env = Spire_GetBiomeEnvironment();
    u32 i;

    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[env].background.tileset, (void *)(BG_CHAR_ADDR(2)));
    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[env].background.tilemap, (void *)(BG_SCREEN_ADDR(26)));
    LoadPalette(gBattleEnvironmentInfo[env].background.palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
    for (i = BG_PLTT_ID(2); i < BG_PLTT_ID(5); i++)
    {
        u16 c = gPlttBufferUnfaded[i];
        s32 r = GET_R(c), g = GET_G(c), b = GET_B(c);

        r += (GET_R(tint) - r) * (s32)amount / 16;
        g += (GET_G(tint) - g) * (s32)amount / 16;
        b += (GET_B(tint) - b) * (s32)amount / 16;
        gPlttBufferUnfaded[i] = RGB(r, g, b);
    }
}

// ---------------------------------------------------------------------------------------------
// Tekenen

// Altijd met transparante achtergrond (het venster is al gevuld): anders wist elke regel de onderkant
// van de regel erboven.
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    u8 c[3] = {TEXT_COLOR_TRANSPARENT, color[1], color[2]};

    AddTextPrinterParameterized3(win, font, x, y, c, TEXT_SKIP_DRAW, str);
}

static void DrawFrame(u32 win, u32 pal)
{
    u32 l = GetWindowAttribute(win, WINDOW_TILEMAP_LEFT), t = GetWindowAttribute(win, WINDOW_TILEMAP_TOP);
    u32 w = GetWindowAttribute(win, WINDOW_WIDTH), h = GetWindowAttribute(win, WINDOW_HEIGHT);

    FillBgTilemapBufferRect(0, FRAME_TILE + 0, l - 1, t - 1, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 1, l, t - 1, w, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 2, l + w, t - 1, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 3, l - 1, t, 1, h, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 5, l + w, t, 1, h, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 6, l - 1, t + h, 1, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 7, l, t + h, w, 1, pal);
    FillBgTilemapBufferRect(0, FRAME_TILE + 8, l + w, t + h, 1, 1, pal);
}

static u32 RestPercent(void)
{
    return Spire_HasRelic(SPIRE_RELIC_SOOTHE_BELL) ? SPIRE_REST_HEAL + 30 : SPIRE_REST_HEAL;
}

static void DrawHeader(void)
{
    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Red, COMPOUND_STRING("SNORLAX CAMP"));
    PrintText(WIN_HEADER, FONT_NORMAL, 100, 1, sColor_Dark, COMPOUND_STRING("Shh. Snorlax is asleep."));
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawHpBar(u32 win, u32 x, u32 y, struct Pokemon *mon)
{
    u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);
    u32 w = maxHp ? 40 * hp / maxHp : 0;
    u32 col = (hp * 2 > maxHp) ? 9 : (hp * 5 > maxHp) ? 6 : 11;

    FillWindowPixelRect(win, PIXEL_FILL(13), x, y, 42, 4);
    if (w)
        FillWindowPixelRect(win, PIXEL_FILL(col), x + 1, y + 1, w, 2);
}

// Linker/rechter venster: de twee keuzes, of je twee Pokémon (welke move?), of de moves van één Pokémon.
static void DrawOptions(void)
{
    u32 i;
    u8 buf[24];

    for (i = 0; i < 2; i++)
    {
        u32 win = WIN_LEFT + i;
        bool32 sel;

        FillWindowPixelBuffer(win, PIXEL_FILL(1));
        if (sRest->state == STATE_CHOOSE_MON || (sRest->state == STATE_MAIN && FALSE))
        {
            struct Pokemon *mon = Spire_GetRunMon(i);
            u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);

            sel = (sRest->mon == i);
            GetMonData(mon, MON_DATA_NICKNAME, buf);
            PrintText(win, FONT_SMALL_NARROW, 26, 0, sel ? sColor_Red : sColor_Dark, buf);
            DrawHpBar(win, 26, 11, mon);
            ConvertIntToDecimalStringN(buf, maxHp ? (hp * 100 + maxHp - 1) / maxHp : 0, STR_CONV_MODE_LEFT_ALIGN, 3);
            StringAppend(buf, COMPOUND_STRING("%"));
            PrintText(win, FONT_SMALL_NARROW, 72, 6, sColor_Dark, buf);
        }
        else if (sRest->state == STATE_CHOOSE_MOVE)
        {
            struct Pokemon *mon = Spire_GetRunMon(sRest->mon);
            u32 k;

            sel = (sRest->slot % 2 == i);
            for (k = 0; k < 2; k++)
            {
                u32 slot = k * 2 + i;
                u32 m = GetMonData(mon, MON_DATA_MOVE1 + slot);
                u8 *p;

                if (m == MOVE_NONE)
                {
                    PrintText(win, FONT_SMALL_NARROW, 10, k * 8, sColor_Gray, COMPOUND_STRING("-"));
                    continue;
                }
                p = StringCopy(gStringVar4, GetMoveName(m));
                if (Spire_IsSlotUpgraded(mon, slot))
                    StringCopy(p, COMPOUND_STRING("+"));
                if (sRest->slot == slot)
                    PrintText(win, FONT_SMALL_NARROW, 2, k * 8, sColor_Red, COMPOUND_STRING("▶"));
                PrintText(win, FONT_SMALL_NARROW, 10, k * 8, Spire_IsSlotUpgraded(mon, slot) ? sColor_Gold : sColor_Dark, gStringVar4);
            }
        }
        else if (i == CHOICE_REST)
        {
            sel = (sRest->choice == CHOICE_REST);
            buf[0] = CHAR_PLUS;
            ConvertIntToDecimalStringN(buf + 1, RestPercent(), STR_CONV_MODE_LEFT_ALIGN, 3);
            StringAppend(buf, COMPOUND_STRING("% HP, PP"));
            PrintText(win, FONT_NORMAL, 4, 0, sColor_Green, COMPOUND_STRING("REST"));
            PrintText(win, FONT_SMALL_NARROW, 38, 3, sColor_Dark, buf);
        }
        else
        {
            sel = (sRest->choice == CHOICE_UPGRADE);
            PrintText(win, FONT_NORMAL, 4, 0, sColor_Blue, COMPOUND_STRING("UPGRADE"));
            PrintText(win, FONT_SMALL_NARROW, 60, 3, sColor_Dark, COMPOUND_STRING("a move +"));
        }
        CopyWindowToVram(win, COPYWIN_FULL);
        DrawFrame(win, (sel && sRest->state != STATE_MESSAGE) ? PAL_FRAME_SEL : PAL_FRAME);
    }
    ScheduleBgCopyTilemapToVram(0);
}

static void DrawBottom(void)
{
    u32 i;

    FillWindowPixelBuffer(WIN_BOTTOM, PIXEL_FILL(1));
    switch (sRest->state)
    {
    case STATE_MAIN:
        if (sRest->choice == CHOICE_REST)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark,
                      COMPOUND_STRING("Chansey patches you up. Status cured too.\nNo questions. No insurance."));
        else
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark,
                      COMPOUND_STRING("Attack: +30% power. Status move: one extra\nstat stage and it never misses. Max PP."));
        break;
    case STATE_CHOOSE_MON:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Blue, COMPOUND_STRING("Whose move does Porygon2 rewrite?"));
        break;
    case STATE_CHOOSE_MOVE:
        GetMonData(Spire_GetRunMon(sRest->mon), MON_DATA_NICKNAME, gStringVar1);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Which move of {STR_VAR_1}? (B: back)"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Blue, gStringVar4);
        break;
    case STATE_MESSAGE:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sRest->message);
        break;
    }
    CopyWindowToVram(WIN_BOTTOM, COPYWIN_FULL);
    for (i = 0; i < 2; i++)
        if (sRest->iconSpriteIds[i] != SPRITE_NONE)
            gSprites[sRest->iconSpriteIds[i]].invisible = (sRest->state != STATE_CHOOSE_MON);
}

static void Redraw(void)
{
    DrawOptions();
    DrawBottom();
}

// ---------------------------------------------------------------------------------------------
// Sprites

static void UpdateSprites(void)
{
    struct Sprite *hand = &gSprites[sRest->handSpriteId];
    u32 i;

    sRest->timer++;
    // Snorlax ademt
    gSprites[sRest->picSpriteIds[1]].y2 = ((sRest->timer >> 5) & 1) ? 1 : 0;
    // de gekozen helper staat in het licht, de andere in de schaduw
    for (i = 0; i < 2; i++)
    {
        u32 id = sRest->picSpriteIds[i == 0 ? 0 : 2];
        bool32 lit = (sRest->choice == i) || sRest->state == STATE_MESSAGE;

        gSprites[id].oam.objMode = lit ? ST_OAM_OBJ_NORMAL : ST_OAM_OBJ_BLEND;
        gSprites[id].y2 = (lit && ((sRest->timer >> 4) & 1)) ? -1 : 0;
    }
    if (sRest->state == STATE_MAIN)
    {
        hand->x = sRest->choice == CHOICE_REST ? 70 : 206;
        hand->y = 42 + (((sRest->timer >> 4) & 1) ? 2 : 0);
        hand->invisible = FALSE;
    }
    else
    {
        hand->invisible = TRUE;
    }
}

static void CreateSprites(void)
{
    u32 i;

    sRest->picSpriteIds[0] = CreateMonPicSprite(SPECIES_CHANSEY, FALSE, 0, TRUE, 52, 62, 0, SPECIES_CHANSEY); // palettetag = soort
    sRest->picSpriteIds[1] = CreateMonPicSprite(SPECIES_SNORLAX, FALSE, 0, TRUE, 120, 58, 0, SPECIES_SNORLAX);
    sRest->picSpriteIds[2] = CreateMonPicSprite(SPECIES_PORYGON2, FALSE, 0, TRUE, 188, 62, 0, SPECIES_PORYGON2);
    for (i = 0; i < 3; i++)
        gSprites[sRest->picSpriteIds[i]].oam.priority = 1;
    // Snorlax slaapt achter de helpers
    gSprites[sRest->picSpriteIds[1]].oam.priority = 2;

    LoadMonIconPalettes();
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sRest->iconSpriteIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon,
                                                8 + 20 + i * 120, 96 + 8, 0, GetMonData(mon, MON_DATA_PERSONALITY));
        gSprites[sRest->iconSpriteIds[i]].oam.priority = 0;
    }
    LoadSpriteSheet(&sSpriteSheet_Hand);
    LoadSpritePalette(&sSpritePal_Hand);
    sRest->handSpriteId = CreateSprite(&sSpriteTemplate_Hand, 0, 0, 0);
}

// ---------------------------------------------------------------------------------------------
// Scherm

static void VBlankCB_SpireRest(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireRest(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

void Spire_OpenRest(void (*onDone)(void))
{
    sRest = AllocZeroed(sizeof(*sRest));
    sRest->onDone = onDone;

    SetVBlankCallback(NULL);
    ScanlineEffect_Stop();
    ResetPaletteFade();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetTasks();
    ResetVramOamAndBgCntRegs();
    ResetAllBgsCoordinates();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    SetBgTilemapBuffer(0, AllocZeroed(BG_SCREEN_SIZE));
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();

    // schemer: de achtergrond trekt naar een warm donkerpaars, alsof er een kampvuur brandt
    Spire_LoadBiomeBackground(RGB(9, 4, 10), 7);
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadWindowGfx(WIN_HEADER, 0, FRAME_TILE, BG_PLTT_ID(PAL_FRAME));
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME)], &gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL)], PLTT_SIZE_4BPP);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 2] = RGB(18, 3, 3);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 3] = RGB(29, 8, 6);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 4] = RGB(24, 5, 5);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 5] = RGB(31, 13, 10);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 6] = RGB(31, 19, 16);

    DrawFrame(WIN_HEADER, PAL_FRAME);
    DrawFrame(WIN_BOTTOM, PAL_FRAME);
    // de helpers staan voor de balie (de vensters), Snorlax erachter
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_LEFT);
    PutWindowTilemap(WIN_RIGHT);
    PutWindowTilemap(WIN_BOTTOM);
    CreateSprites();
    DrawHeader();
    Redraw();
    UpdateSprites();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG3_ON);
    // helpers in de schaduw: half doorzichtig over de achtergrond
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG3 | BLDCNT_EFFECT_BLEND);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(9, 7));
    ShowBg(0);
    ShowBg(3);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireRest);
    SetMainCallback2(CB2_SpireRest);
    CreateTask(Task_SpireRest, 0);
}

static void CloseRest(void)
{
    void (*onDone)(void) = sRest->onDone;
    u32 i;

    for (i = 0; i < 3; i++)
        FreeAndDestroyMonPicSprite(sRest->picSpriteIds[i]);
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    Free(sRest);
    sRest = NULL;
    onDone();
}

static void ShowMessage(const u8 *text)
{
    StringExpandPlaceholders(sRest->message, text);
    sRest->state = STATE_MESSAGE;
    Redraw();
}

static void DoRest(void)
{
    Spire_HealRun(RestPercent());
    Spire_RestorePP();
    PlayFanfare(MUS_HEAL);
    ShowMessage(COMPOUND_STRING("Chansey tucks your team in next to Snorlax.\nHP and PP restored. Nobody snores. Much."));
}

static void DoUpgrade(void)
{
    struct Pokemon *mon = Spire_GetRunMon(sRest->mon);
    u32 move = GetMonData(mon, MON_DATA_MOVE1 + sRest->slot);

    Spire_UpgradeSlot(mon, sRest->slot);
    PlaySE(SE_EXP_MAX);
    StringCopy(gStringVar1, GetMoveName(move));
    ShowMessage(COMPOUND_STRING("Porygon2 rewrites the code of {STR_VAR_1}.\nIt is now {STR_VAR_1}+. Do not ask how."));
}

static void Task_SpireRest(u8 taskId)
{
    UpdateSprites();
    if (gPaletteFade.active)
        return;

    switch (sRest->state)
    {
    case STATE_MAIN:
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sRest->choice ^= 1;
            Redraw();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            if (sRest->choice == CHOICE_REST)
            {
                DoRest();
            }
            else
            {
                sRest->mon = 0;
                sRest->state = STATE_CHOOSE_MON;
                Redraw();
            }
        }
        break;
    case STATE_CHOOSE_MON:
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sRest->mon ^= 1;
            Redraw();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            sRest->slot = 0;
            sRest->state = STATE_CHOOSE_MOVE;
            Redraw();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sRest->state = STATE_MAIN;
            Redraw();
        }
        break;
    case STATE_CHOOSE_MOVE:
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sRest->slot ^= 1;
            Redraw();
        }
        else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
        {
            PlaySE(SE_SELECT);
            sRest->slot ^= 2;
            Redraw();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            struct Pokemon *mon = Spire_GetRunMon(sRest->mon);

            if (GetMonData(mon, MON_DATA_MOVE1 + sRest->slot) == MOVE_NONE || Spire_IsSlotUpgraded(mon, sRest->slot))
                PlaySE(SE_FAILURE);
            else
                DoUpgrade();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sRest->state = STATE_CHOOSE_MON;
            Redraw();
        }
        break;
    case STATE_MESSAGE:
        if (JOY_NEW(A_BUTTON | B_BUTTON) && IsFanfareTaskInactive())
        {
            PlaySE(SE_SELECT);
            sRest->state = STATE_EXIT;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseRest();
        break;
    }
}
