// Project Grounded: The Spire - draft (zie SPIRE_DESIGN.md).
// Tien rentals in een raster; je kiest er twee. Onderaan: types, base stats, startmoves, zeldzaamheid en
// de evoluties per act van de Pokémon onder de cursor.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "move.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "pokemon_summary_screen.h"
#include "random.h"
#include "scanline_effect.h"
#include "sound.h"
#include "spire.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

#define DRAFT_COUNT 10
#define COLUMNS     5

enum
{
    WIN_HEADER,
    WIN_GRID,
    WIN_INFO,
    WIN_COUNT,
};

#define PAL_BRICKS  12
#define PAL_FRAME   14
#define PAL_TEXT    15
#define FRAME_TILE  0x200
#define TAG_CURSOR  0x5350

struct SpireDraft
{
    void (*onDone)(void);
    u16 species[DRAFT_COUNT];
    u8 iconSpriteIds[DRAFT_COUNT];
    u8 typeSpriteIds[2];
    u8 cursorSpriteId;
    u8 cursor;
    u8 picks[2];
    u8 pickCount;
    u8 done;
    u16 timer;
};

static EWRAM_DATA struct SpireDraft *sDraft = NULL;

static const u32 sCursorGfx[] = INCBIN_U32("graphics/grounded/spire/cursor.4bpp");
static const u16 sCursorPal[] = INCBIN_U16("graphics/grounded/spire/cursor.gbapal");

static const u32 sBrickTiles[2][8] =
{
    {0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x22222222},
    {0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x22222222},
};
static const u16 sBrickPal[16] = {RGB(5, 4, 9), RGB(5, 4, 9), RGB(8, 7, 14)};

static const u16 sTextPal[16] =
{
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(8, 8, 9), RGB(26, 26, 27),
    RGB(5, 15, 29), RGB(23, 27, 31), RGB(25, 17, 1), RGB(31, 27, 17),
    RGB(19, 19, 20), RGB(5, 19, 9), RGB(22, 29, 23), RGB(29, 8, 7),
    RGB(31, 24, 23), RGB(10, 10, 11), RGB(15, 9, 22), RGB(26, 22, 30),
};
static const u8 sColor_Dark[]   = {0, 2, 3};
static const u8 sColor_Blue[]   = {0, 4, 5};
static const u8 sColor_Gold[]   = {0, 6, 7};
static const u8 sColor_Gray[]   = {0, 8, 3};
static const u8 sColor_Red[]    = {0, 11, 12};
static const u8 sColor_Purple[] = {0, 14, 15};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_GRID]   = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 4, .width = 28, .height = 8, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_INFO]   = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 13, .width = 28, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x119},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam32 = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};
static const struct SpriteSheet sSpriteSheet_Cursor = {sCursorGfx, 0x200, TAG_CURSOR};
static const struct SpritePalette sSpritePal_Cursor = {sCursorPal, TAG_CURSOR};
static const struct SpriteTemplate sSpriteTemplate_Cursor =
{
    .tileTag = TAG_CURSOR, .paletteTag = TAG_CURSOR, .oam = &sOam32, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static const u8 *const sTierName[] = {COMPOUND_STRING("COMMON"), COMPOUND_STRING("COMMON"), COMPOUND_STRING("UNCOMMON"), COMPOUND_STRING("RARE")};

static void Task_SpireDraft(u8 taskId);

static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(win, font, x, y, color, TEXT_SKIP_DRAW, str);
}

static s32 PickIndex(u32 i)
{
    u32 k;

    for (k = 0; k < sDraft->pickCount; k++)
        if (sDraft->picks[k] == i)
            return k;
    return -1;
}

// cel i: middelpunt van het icoon op het scherm
static void CellPos(u32 i, s16 *x, s16 *y)
{
    *x = 8 + 22 + (i % COLUMNS) * 45;
    *y = 32 + 11 + (i / COLUMNS) * 30;
}

static void DrawHeader(void)
{
    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, COMPOUND_STRING("THE SPIRE"));
    if (sDraft->pickCount == 2)
        PrintText(WIN_HEADER, FONT_NORMAL, 84, 1, sColor_Red, COMPOUND_STRING("A: begin   B: change"));
    else
        PrintText(WIN_HEADER, FONT_NORMAL, 84, 1, sColor_Dark,
                  sDraft->pickCount == 0 ? COMPOUND_STRING("Pick 2 of these 10") : COMPOUND_STRING("Pick one more"));
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawGrid(void)
{
    u32 i;

    FillWindowPixelBuffer(WIN_GRID, PIXEL_FILL(1));
    for (i = 0; i < DRAFT_COUNT; i++)
    {
        const u8 *name = GetSpeciesName(sDraft->species[i]);
        s32 pick = PickIndex(i);
        u32 font = GetStringWidth(FONT_SMALL_NARROW, name, 0) > 44 ? FONT_SMALL_NARROWER : FONT_SMALL_NARROW;
        s32 x = (i % COLUMNS) * 45 + (44 - GetStringWidth(font, name, 0)) / 2;
        u32 y = (i / COLUMNS) * 30 + 20;

        if (pick >= 0)
        {
            // gekozen: goudkleurige naam en het nummer
            FillWindowPixelRect(WIN_GRID, PIXEL_FILL(7), (i % COLUMNS) * 45 + 1, (i / COLUMNS) * 30 + 1, 42, 29);
            PrintText(WIN_GRID, FONT_SMALL_NARROW, (i % COLUMNS) * 45 + 3, (i / COLUMNS) * 30 + 1, sColor_Red,
                      pick == 0 ? COMPOUND_STRING("1") : COMPOUND_STRING("2"));
        }
        PrintText(WIN_GRID, font, x < 0 ? 0 : x, y, pick >= 0 ? sColor_Gold : sColor_Dark, name);
    }
    CopyWindowToVram(WIN_GRID, COPYWIN_FULL);
}

static void DrawInfo(void)
{
    u16 species = sDraft->species[sDraft->cursor];
    const struct SpireRental *rental = Spire_FindRental(species);
    u16 targets[3];
    u8 *p;
    u32 i;

    FillWindowPixelBuffer(WIN_INFO, PIXEL_FILL(1));
    PrintText(WIN_INFO, FONT_NORMAL, 2, 0, sColor_Dark, GetSpeciesName(species));
    if (rental)
        PrintText(WIN_INFO, FONT_SMALL_NARROW, 176, 2, rental->tier >= 3 ? sColor_Gold : rental->tier == 2 ? sColor_Blue : sColor_Gray,
                  sTierName[rental->tier]);

    p = StringCopy(gStringVar4, COMPOUND_STRING("HP "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseHP, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Atk "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseAttack, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Def "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseDefense, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  SpA "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpAttack, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  SpD "));
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpDefense, STR_CONV_MODE_LEFT_ALIGN, 3);
    p = StringCopy(p, COMPOUND_STRING("  Spe "));
    ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpeed, STR_CONV_MODE_LEFT_ALIGN, 3);
    PrintText(WIN_INFO, FONT_SMALL_NARROW, 2, 15, sColor_Gray, gStringVar4);

    p = gStringVar4;
    if (rental)
    {
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            if (rental->moves[i] == MOVE_NONE)
                continue;
            if (p != gStringVar4)
                p = StringCopy(p, COMPOUND_STRING(", "));
            p = StringCopy(p, GetMoveName(rental->moves[i]));
        }
    }
    PrintText(WIN_INFO, FONT_SMALL_NARROW, 2, 25, sColor_Dark, gStringVar4);

    p = gStringVar4;
    if (Spire_GetEvolutions(species, targets))
    {
        u16 mid = targets[0];
        bool32 branch = Spire_GetEvolutions(species, targets) > 1;

        p = StringCopy(p, COMPOUND_STRING("Act 2: "));
        p = StringCopy(p, GetSpeciesName(mid));
        if (branch)
            p = StringCopy(p, COMPOUND_STRING(" or more"));
        if (Spire_GetEvolutions(mid, targets))
        {
            p = StringCopy(p, COMPOUND_STRING("   Act 3: "));
            p = StringCopy(p, GetSpeciesName(targets[0]));
        }
    }
    else
    {
        p = StringCopy(p, COMPOUND_STRING("Does not evolve. Strong now, never stronger."));
    }
    PrintText(WIN_INFO, FONT_SMALL_NARROW, 2, 35, sColor_Purple, gStringVar4);
    CopyWindowToVram(WIN_INFO, COPYWIN_FULL);

    // types als sprites naast de naam
    for (i = 0; i < 2; i++)
    {
        struct Sprite *t = &gSprites[sDraft->typeSpriteIds[i]];
        enum Type type = GetSpeciesType(species, i);

        t->invisible = (i == 1 && type == GetSpeciesType(species, 0));
        StartSpriteAnim(t, type);
        t->oam.paletteNum = gTypesInfo[type].palette;
        t->x = 8 + 2 + GetStringWidth(FONT_NORMAL, GetSpeciesName(species), 0) + 22 + i * 34;
    }
}

static void PlaceCursor(void)
{
    s16 x, y;

    CellPos(sDraft->cursor, &x, &y);
    gSprites[sDraft->cursorSpriteId].x = x;
    gSprites[sDraft->cursorSpriteId].y = y - 2;
    gSprites[sDraft->cursorSpriteId].invisible = ((sDraft->timer & 0x1F) >= 0x1A);
}

// ---------------------------------------------------------------------------------------------

static void VBlankCB_SpireDraft(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireDraft(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

// Tien verschillende rentals, elk met de zeldzaamheid van de draft (C 35, B 35, A 22, S 8%).
static void RollDraft(void)
{
    u32 i, j, tries;

    for (i = 0; i < DRAFT_COUNT; i++)
    {
        for (tries = 0; tries < 40; tries++)
        {
            u16 species = Spire_RandomRental(i * 7 + tries * 3);
            bool32 dup = FALSE;

            for (j = 0; j < i; j++)
                if (sDraft->species[j] == species)
                    dup = TRUE;
            sDraft->species[i] = species;
            if (!dup)
                break;
        }
    }
}

void Spire_OpenDraft(void (*onDone)(void))
{
    u16 *tilemap;
    u32 i, x, y;

    sDraft = AllocZeroed(sizeof(*sDraft));
    sDraft->onDone = onDone;
    RollDraft();

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

    // torenstenen (zoals de kaartenschermen)
    tilemap = AllocZeroed(BG_SCREEN_SIZE);
    LoadBgTiles(1, sBrickTiles, sizeof(sBrickTiles), 0);
    LoadPalette(sBrickPal, BG_PLTT_ID(PAL_BRICKS), PLTT_SIZE_4BPP);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = ((x + (y & 1)) & 1) | (PAL_BRICKS << 12);
    SetBgTilemapBuffer(1, tilemap);
    ScheduleBgCopyTilemapToVram(1);

    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadWindowGfx(WIN_HEADER, 0, FRAME_TILE, BG_PLTT_ID(PAL_FRAME));
    for (i = 0; i < WIN_COUNT; i++)
    {
        DrawStdFrameWithCustomTileAndPalette(i, FALSE, FRAME_TILE, PAL_FRAME);
        PutWindowTilemap(i);
    }

    LoadMonIconPalettes();
    for (i = 0; i < DRAFT_COUNT; i++)
    {
        s16 cx, cy;

        CellPos(i, &cx, &cy);
        sDraft->iconSpriteIds[i] = CreateMonIconNoPersonality(sDraft->species[i], SpriteCB_MonIcon, cx,
                                                              cy + Spire_IconYAdjust(sDraft->species[i], 0), 1);
    }
    LoadCompressedSpriteSheet(&gSpriteSheet_MoveTypes);
    LoadPalette(gMoveTypes_Pal, OBJ_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    for (i = 0; i < 2; i++)
    {
        sDraft->typeSpriteIds[i] = CreateSprite(&gSpriteTemplate_MoveTypes, 0, 104 + 8, 0);
        gSprites[sDraft->typeSpriteIds[i]].oam.priority = 0;
    }
    LoadSpriteSheet(&sSpriteSheet_Cursor);
    LoadSpritePalette(&sSpritePal_Cursor);
    sDraft->cursorSpriteId = CreateSprite(&sSpriteTemplate_Cursor, 0, 0, 0);

    DrawHeader();
    DrawGrid();
    DrawInfo();
    PlaceCursor();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireDraft);
    SetMainCallback2(CB2_SpireDraft);
    CreateTask(Task_SpireDraft, 0);
}

static void CloseDraft(void)
{
    void (*onDone)(void) = sDraft->onDone;

    Spire_SetRental(0, sDraft->species[sDraft->picks[0]]);
    Spire_SetRental(1, sDraft->species[sDraft->picks[1]]);
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sDraft);
    sDraft = NULL;
    onDone();
}

static void Task_SpireDraft(u8 taskId)
{
    u32 cur = sDraft->cursor;

    sDraft->timer++;
    PlaceCursor();
    if (gPaletteFade.active)
        return;
    if (sDraft->done)
    {
        DestroyTask(taskId);
        CloseDraft();
        return;
    }

    if (JOY_NEW(DPAD_LEFT) && cur % COLUMNS > 0)
        cur--;
    else if (JOY_NEW(DPAD_RIGHT) && cur % COLUMNS < COLUMNS - 1)
        cur++;
    else if (JOY_NEW(DPAD_UP) && cur >= COLUMNS)
        cur -= COLUMNS;
    else if (JOY_NEW(DPAD_DOWN) && cur + COLUMNS < DRAFT_COUNT)
        cur += COLUMNS;
    else if (JOY_NEW(A_BUTTON))
    {
        s32 pick = PickIndex(cur);

        if (sDraft->pickCount == 2)
        {
            PlaySE(SE_SELECT);
            sDraft->done = TRUE;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            return;
        }
        if (pick < 0)
        {
            PlayCry_Normal(sDraft->species[cur], 0);
            sDraft->picks[sDraft->pickCount++] = cur;
        }
        else
        {
            PlaySE(SE_FAILURE);
        }
        DrawHeader();
        DrawGrid();
    }
    else if (JOY_NEW(B_BUTTON) && sDraft->pickCount > 0)
    {
        PlaySE(SE_SELECT);
        sDraft->pickCount--;
        DrawHeader();
        DrawGrid();
    }
    if (cur != sDraft->cursor)
    {
        PlaySE(SE_SELECT);
        sDraft->cursor = cur;
        DrawInfo();
    }
}
