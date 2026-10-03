// Project Grounded: The Spire - beloningsscherm na een gewonnen gevecht (zie SPIRE_DESIGN.md).
// Drie movekaarten (common/uncommon/rare); kies er één, kies wie hem leert en welke move hij vergeet.
// B slaat de beloning over. Daarna terug naar het opgegeven callback.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "graphics.h"
#include "menu_helpers.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
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
#include "strings.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/moves.h"
#include "constants/rgb.h"
#include "constants/songs.h"

enum
{
    WIN_HEADER,
    WIN_CARD_0,
    WIN_CARD_1,
    WIN_CARD_2,
    WIN_BOTTOM,
    WIN_COUNT,
};

enum
{
    RARITY_COMMON,
    RARITY_UNCOMMON,
    RARITY_RARE,
};

enum
{
    STATE_CARDS,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_SLOT,
    STATE_MESSAGE,
    STATE_EXIT,
};

#define FRAME_TILE    0x200
#define FRAME_PAL     14
#define TEXT_PAL      15
#define TAG_HAND      0x5301

struct SpireReward
{
    MainCallback callback;
    u16 moves[3];
    u8 rarity[3];
    u8 state;
    u8 card;
    u8 mon;
    u8 slot;
    u8 bpGained;
    u8 handSpriteId;
    u8 typeSpriteIds[3];
    u8 iconSpriteIds[2];
    u8 bob;
};

static EWRAM_DATA struct SpireReward *sReward = NULL;

// --- movepools per zeldzaamheid (prototype; later per act en per rental) ---------------------
static const u16 sCommonMoves[] =
{
    MOVE_HEADBUTT, MOVE_BITE, MOVE_WATER_PULSE, MOVE_MAGICAL_LEAF, MOVE_SHOCK_WAVE, MOVE_ICY_WIND,
    MOVE_ROCK_TOMB, MOVE_AERIAL_ACE, MOVE_MUD_SHOT, MOVE_FLAME_WHEEL, MOVE_PSYBEAM, MOVE_SHADOW_CLAW,
    MOVE_DRAGON_BREATH, MOVE_BRICK_BREAK, MOVE_POISON_JAB, MOVE_BUG_BITE, MOVE_DRAINING_KISS, MOVE_SNARL,
    MOVE_PROTECT,
};
static const u16 sUncommonMoves[] =
{
    MOVE_FLAMETHROWER, MOVE_SURF, MOVE_THUNDERBOLT, MOVE_ICE_BEAM, MOVE_ENERGY_BALL, MOVE_EARTH_POWER,
    MOVE_PSYCHIC, MOVE_SHADOW_BALL, MOVE_DRAGON_PULSE, MOVE_DARK_PULSE, MOVE_FLASH_CANNON, MOVE_X_SCISSOR,
    MOVE_ROCK_SLIDE, MOVE_CRUNCH, MOVE_SLUDGE_BOMB, MOVE_AURA_SPHERE, MOVE_FREEZE_DRY, MOVE_TAILWIND,
    MOVE_HELPING_HAND, MOVE_CALM_MIND, MOVE_SWORDS_DANCE, MOVE_WIDE_GUARD,
};
static const u16 sRareMoves[] =
{
    MOVE_FIRE_BLAST, MOVE_HYDRO_PUMP, MOVE_THUNDER, MOVE_BLIZZARD, MOVE_CLOSE_COMBAT, MOVE_EARTHQUAKE,
    MOVE_OUTRAGE, MOVE_MOONBLAST, MOVE_DRACO_METEOR, MOVE_HEAT_WAVE, MOVE_LEAF_STORM, MOVE_DRAGON_DANCE,
    MOVE_QUIVER_DANCE, MOVE_FOLLOW_ME, MOVE_FAKE_OUT,
};

// --- graphics ---------------------------------------------------------------------------------
static const u16 sHandCursor_Pal[] = INCBIN_U16("graphics/pokemon_storage/hand_cursor.gbapal");
static const u8 sHandCursor_Gfx[] = INCBIN_U8("graphics/pokemon_storage/hand_cursor.4bpp");

// tekstpalet: 1 wit, 2 donker, 3 schaduw, 4/5 blauw, 6/7 goud, 8 grijs, 9/10 groen, 11/12 rood, 13 donkere balk
static const u16 sTextPal[16] =
{
    RGB(31, 31, 31), RGB(31, 31, 31), RGB(8, 8, 9), RGB(26, 26, 27),
    RGB(5, 15, 29), RGB(23, 27, 31), RGB(25, 17, 1), RGB(31, 27, 17),
    RGB(19, 19, 20), RGB(9, 25, 14), RGB(23, 30, 24), RGB(29, 8, 7),
    RGB(31, 24, 23), RGB(10, 10, 11), RGB(31, 31, 31), RGB(31, 31, 31),
};

static const u8 sColor_Dark[]  = {1, 2, 3};
static const u8 sColor_Blue[]  = {1, 4, 5};
static const u8 sColor_Gold[]  = {1, 6, 7};
static const u8 sColor_Gray[]  = {1, 8, 3};
static const u8 sColor_Green[] = {1, 9, 10};
static const u8 sColor_Red[]   = {1, 11, 12};

static const u8 sRarityBarColor[] = {8, 4, 6};
static const u8 *const sRarityTextColor[] = {sColor_Gray, sColor_Blue, sColor_Gold};
static const u8 *const sRarityName[] =
{
    COMPOUND_STRING("COMMON"), COMPOUND_STRING("UNCOMMON"), COMPOUND_STRING("RARE"),
};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 2, .paletteNum = TEXT_PAL, .baseBlock = 0x001},
    [WIN_CARD_0] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = TEXT_PAL, .baseBlock = 0x039},
    [WIN_CARD_1] = {.bg = 0, .tilemapLeft = 11, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = TEXT_PAL, .baseBlock = 0x069},
    [WIN_CARD_2] = {.bg = 0, .tilemapLeft = 21, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = TEXT_PAL, .baseBlock = 0x099},
    [WIN_BOTTOM] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 13, .width = 28, .height = 6, .paletteNum = TEXT_PAL, .baseBlock = 0x0C9},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam_Hand =
{
    .shape = SPRITE_SHAPE(32x32),
    .size = SPRITE_SIZE(32x32),
    .priority = 0,
};
static const struct SpriteSheet sSpriteSheet_Hand = {sHandCursor_Gfx, 0x200, TAG_HAND};
static const struct SpritePalette sSpritePal_Hand = {sHandCursor_Pal, TAG_HAND};
static void SpriteCB_Hand(struct Sprite *sprite);
static const struct SpriteTemplate sSpriteTemplate_Hand =
{
    .tileTag = TAG_HAND,
    .paletteTag = TAG_HAND,
    .oam = &sOam_Hand,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_Hand,
};

static void CB2_SpireReward(void);
static void Task_SpireReward(u8 taskId);

// --- helpers ----------------------------------------------------------------------------------
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(win, font, x, y, color, TEXT_SKIP_DRAW, str);
}

static void PrintCentered(u32 win, u32 font, u32 y, u32 width, const u8 *color, const u8 *str)
{
    s32 x = (width - GetStringWidth(font, str, 0)) / 2;
    PrintText(win, font, x < 0 ? 0 : x, y, color, str);
}

static bool32 MonKnowsMove(struct Pokemon *mon, u32 move)
{
    u32 i;

    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == move)
            return TRUE;
    return FALSE;
}

static bool32 IsStab(struct Pokemon *mon, u32 move)
{
    u32 species = GetMonData(mon, MON_DATA_SPECIES);
    enum Type type = GetMoveType(move);

    return !IsBattleMoveStatus(move) && (GetSpeciesType(species, 0) == type || GetSpeciesType(species, 1) == type);
}

static void RollMoves(void)
{
    u32 i, j;

    for (i = 0; i < 3; i++)
    {
        u32 roll, move;
        bool32 dup;

        do
        {
            roll = Random() % 100;
            if (roll < 10)
            {
                sReward->rarity[i] = RARITY_RARE;
                move = sRareMoves[Random() % ARRAY_COUNT(sRareMoves)];
            }
            else if (roll < 40)
            {
                sReward->rarity[i] = RARITY_UNCOMMON;
                move = sUncommonMoves[Random() % ARRAY_COUNT(sUncommonMoves)];
            }
            else
            {
                sReward->rarity[i] = RARITY_COMMON;
                move = sCommonMoves[Random() % ARRAY_COUNT(sCommonMoves)];
            }
            dup = FALSE;
            for (j = 0; j < i; j++)
                if (sReward->moves[j] == move)
                    dup = TRUE;
        } while (dup);
        sReward->moves[i] = move;
    }
}

// --- tekenen ----------------------------------------------------------------------------------
static const u8 sText_Phys[] = _("Phys.");
static const u8 sText_Spec[] = _("Spec.");
static const u8 sText_Status[] = _("Stat.");

static void DrawHeader(void)
{
    u8 buf[24];

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Dark, COMPOUND_STRING("VICTORY!"));
    buf[0] = CHAR_PLUS;
    ConvertIntToDecimalStringN(buf + 1, sReward->bpGained, STR_CONV_MODE_LEFT_ALIGN, 2);
    StringAppend(buf, COMPOUND_STRING(" BP"));
    PrintText(WIN_HEADER, FONT_NORMAL, 120, 1, sColor_Blue, buf);
    PrintText(WIN_HEADER, FONT_NORMAL, 160, 1, sColor_Green, COMPOUND_STRING("+20% HP"));
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawCard(u32 i)
{
    u32 win = WIN_CARD_0 + i;
    u32 move = sReward->moves[i];
    u8 buf[16];
    const u8 *cat;

    FillWindowPixelBuffer(win, PIXEL_FILL(1));
    FillWindowPixelRect(win, PIXEL_FILL(sRarityBarColor[sReward->rarity[i]]), 0, 0, 64, 3);
    PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetMoveName(move));
    switch (GetMoveCategory(move))
    {
    case DAMAGE_CATEGORY_PHYSICAL: cat = sText_Phys; break;
    case DAMAGE_CATEGORY_SPECIAL:  cat = sText_Spec; break;
    default:                       cat = sText_Status; break;
    }
    PrintText(win, FONT_SMALL_NARROW, 40, 15, sColor_Dark, cat);
    if (GetMovePower(move) > 1)
    {
        StringCopy(buf, COMPOUND_STRING("PWR "));
        ConvertIntToDecimalStringN(buf + 4, GetMovePower(move), STR_CONV_MODE_LEFT_ALIGN, 3);
    }
    else
    {
        StringCopy(buf, COMPOUND_STRING("PWR -"));
    }
    PrintText(win, FONT_SMALL_NARROW, 2, 26, sColor_Dark, buf);
    StringCopy(buf, COMPOUND_STRING("PP "));
    ConvertIntToDecimalStringN(buf + 3, GetMovePP(move), STR_CONV_MODE_LEFT_ALIGN, 2);
    PrintText(win, FONT_SMALL_NARROW, 38, 26, sColor_Dark, buf);
    PrintCentered(win, FONT_SMALL_NARROW, 37, 64, sRarityTextColor[sReward->rarity[i]], sRarityName[sReward->rarity[i]]);
    CopyWindowToVram(win, COPYWIN_FULL);
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

// Onderste vak, regel met beide Pokémon (naam, HP-balk, %, STAB); icoontjes zijn sprites.
static void DrawTeamRow(u32 y, u32 move)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);
        u8 nick[POKEMON_NAME_LENGTH + 1];
        u8 buf[8];
        u32 x = 40 + i * 104;
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);

        GetMonData(mon, MON_DATA_NICKNAME, nick);
        if (sReward->state == STATE_CHOOSE_MON && sReward->mon == i)
            PrintText(WIN_BOTTOM, FONT_NORMAL, x - 38, y + 4, sColor_Red, COMPOUND_STRING("▶"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x, y, sColor_Dark, nick);
        if (move != MOVE_NONE && IsStab(mon, move))
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x + 46, y, sColor_Red, COMPOUND_STRING("STAB"));
        DrawHpBar(WIN_BOTTOM, x, y + 13, mon);
        ConvertIntToDecimalStringN(buf, maxHp ? (hp * 100 + maxHp - 1) / maxHp : 0, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("%"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, x + 44, y + 9, sColor_Dark, buf);
    }
}

static void SetIconsVisible(bool32 visible)
{
    u32 i;

    for (i = 0; i < 2; i++)
        gSprites[sReward->iconSpriteIds[i]].invisible = !visible;
}

static void DrawBottom(void)
{
    u32 move = sReward->moves[sReward->card];

    FillWindowPixelBuffer(WIN_BOTTOM, PIXEL_FILL(1));
    switch (sReward->state)
    {
    case STATE_CARDS:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetMoveDescription(move));
        DrawTeamRow(22, move);
        SetIconsVisible(TRUE);
        break;
    case STATE_CHOOSE_MON:
        StringCopy(gStringVar1, GetMoveName(move));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Teach {STR_VAR_1} to whom?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        DrawTeamRow(22, move);
        SetIconsVisible(TRUE);
        break;
    case STATE_CHOOSE_SLOT:
    {
        struct Pokemon *mon = Spire_GetRunMon(sReward->mon);
        u32 i;

        StringCopy(gStringVar1, GetMoveName(move));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Forget which move for {STR_VAR_1}?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            u32 m = GetMonData(mon, MON_DATA_MOVE1 + i);
            if (sReward->slot == i)
                PrintText(WIN_BOTTOM, FONT_NORMAL, 26 + (i % 2) * 100, 14 + (i / 2) * 14, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 36 + (i % 2) * 100, 16 + (i / 2) * 14, sColor_Dark,
                      m ? GetMoveName(m) : COMPOUND_STRING("-"));
        }
        SetIconsVisible(FALSE);
        break;
    }
    case STATE_MESSAGE:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        SetIconsVisible(FALSE);
        break;
    }
    CopyWindowToVram(WIN_BOTTOM, COPYWIN_FULL);
}

static void PlaceHand(void)
{
    struct Sprite *hand = &gSprites[sReward->handSpriteId];

    switch (sReward->state)
    {
    case STATE_CARDS:
        hand->x = 8 + sReward->card * 80 + 52;
        hand->y = 34;
        break;

    default:
        hand->invisible = TRUE;
        return;
    }
    hand->invisible = FALSE;
}

static void SpriteCB_Hand(struct Sprite *sprite)
{
    sReward->bob++;
    sprite->y2 = (sReward->bob & 0x10) ? 2 : 0;
}

static void Redraw(void)
{
    DrawBottom();
    PlaceHand();
}

// --- scherm openen en sluiten -----------------------------------------------------------------
static void VBlankCB_SpireReward(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireReward(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void SetupScreen(void)
{
    u32 i;

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

    // achtergrond: donker torenpaars (backdrop)
    LoadPalette(sTextPal, BG_PLTT_ID(TEXT_PAL), PLTT_SIZE_4BPP);
    gPlttBufferUnfaded[0] = RGB(6, 4, 11);
    LoadUserWindowBorderGfx(WIN_HEADER, FRAME_TILE, BG_PLTT_ID(FRAME_PAL));
    for (i = 0; i < WIN_COUNT; i++)
        DrawStdFrameWithCustomTileAndPalette(i, FALSE, FRAME_TILE, FRAME_PAL);

    // sprites: Pokémon-icoontjes, type-icoontjes en de hand uit de pc
    LoadMonIconPalettes();
    LoadSpriteSheet(&sSpriteSheet_Hand);
    LoadSpritePalette(&sSpritePal_Hand);
    LoadCompressedSpriteSheet(&gSpriteSheet_MoveTypes);
    LoadPalette(gMoveTypes_Pal, OBJ_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    for (i = 0; i < 3; i++)
    {
        enum Type type = GetMoveType(sReward->moves[i]);
        u8 id = CreateSprite(&gSpriteTemplate_MoveTypes, 8 + i * 80 + 18, 40 + 16 + 4, 0);

        StartSpriteAnim(&gSprites[id], type);
        gSprites[id].oam.paletteNum = gTypesInfo[type].palette;
        gSprites[id].oam.priority = 0;
        sReward->typeSpriteIds[i] = id;
    }
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sReward->iconSpriteIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon,
                                                  8 + 24 + i * 104, 104 + 22 + 10, 0, GetMonData(mon, MON_DATA_PERSONALITY));
        gSprites[sReward->iconSpriteIds[i]].oam.priority = 0;
    }
    sReward->handSpriteId = CreateSprite(&sSpriteTemplate_Hand, 0, 0, 0);

    DrawHeader();
    for (i = 0; i < 3; i++)
        DrawCard(i);
    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireReward);
    SetMainCallback2(CB2_SpireReward);
    CreateTask(Task_SpireReward, 0);
}

void Spire_OpenReward(MainCallback callback, u32 bpGained)
{
    sReward = AllocZeroed(sizeof(*sReward));
    sReward->callback = callback;
    sReward->bpGained = bpGained;
    RollMoves();
    SetupScreen();
}

static void CloseScreen(void)
{
    MainCallback callback = sReward->callback;

    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(sReward);
    sReward = NULL;
    SetMainCallback2(callback);
}

// --- invoer -----------------------------------------------------------------------------------
static void HandleCards(void)
{
    if (JOY_NEW(DPAD_LEFT) && sReward->card > 0)
    {
        PlaySE(SE_SELECT);
        sReward->card--;
        Redraw();
    }
    else if (JOY_NEW(DPAD_RIGHT) && sReward->card < 2)
    {
        PlaySE(SE_SELECT);
        sReward->card++;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        sReward->state = STATE_CHOOSE_MON;
        Redraw();
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sReward->state = STATE_EXIT;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}

static void HandleChooseMon(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sReward->mon ^= 1;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sReward->mon);

        PlaySE(SE_SELECT);
        if (MonKnowsMove(mon, sReward->moves[sReward->card]))
        {
            GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} already knows it!"));
            sReward->state = STATE_MESSAGE;
            sReward->slot = 0xFF; // terug naar de kaarten na A
        }
        else
        {
            sReward->state = STATE_CHOOSE_SLOT;
            sReward->slot = 0;
        }
        Redraw();
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sReward->state = STATE_CARDS;
        Redraw();
    }
}

static void HandleChooseSlot(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sReward->slot ^= 1;
        Redraw();
    }
    else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
    {
        PlaySE(SE_SELECT);
        sReward->slot ^= 2;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sReward->mon);
        u32 move = sReward->moves[sReward->card];

        PlaySE(SE_RG_BALL_CLICK);
        SetMonMoveSlot(mon, move, sReward->slot);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetMoveName(move));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
        sReward->state = STATE_MESSAGE;
        sReward->slot = 0;
        Redraw();
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sReward->state = STATE_CHOOSE_MON;
        Redraw();
    }
}

static void Task_SpireReward(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    switch (sReward->state)
    {
    case STATE_CARDS:
        HandleCards();
        break;
    case STATE_CHOOSE_MON:
        HandleChooseMon();
        break;
    case STATE_CHOOSE_SLOT:
        HandleChooseSlot();
        break;
    case STATE_MESSAGE:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_SELECT);
            if (sReward->slot == 0xFF)
            {
                sReward->state = STATE_CARDS;
                Redraw();
            }
            else
            {
                sReward->state = STATE_EXIT;
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            }
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseScreen();
        break;
    }
}
