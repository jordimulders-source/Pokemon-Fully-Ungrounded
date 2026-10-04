// Project Grounded: The Spire - winkel (Poké Mart, zie SPIRE_DESIGN.md).
// Zoals de Mart in de echte games: links een scrollende lijst met prijzen, rechts het icoon en de details,
// onderaan de beschrijving. Waren: 5 moves, 4 vasthouditems, 2 relics, Super Potion, Max Elixir en de
// Move Relearner (altijd; duurder per gebruik). Prijzen en onderbouwing: SPIRE_BALANS.md.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "item.h"
#include "item_icon.h"
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
#include "constants/characters.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/species.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#define RUN SPIRE_SAVE

enum
{
    WIN_HEADER,
    WIN_LIST,
    WIN_PREVIEW,
    WIN_DESC,
    WIN_COUNT,
};

enum
{
    WARE_MOVE,
    WARE_ITEM,
    WARE_RELIC,
    WARE_POTION,
    WARE_ELIXIR,
    WARE_RELEARN,
};

enum
{
    STATE_LIST,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_SLOT,
    STATE_RELEARN,
    STATE_MESSAGE,
    STATE_EXIT,
};

#define MAX_WARES     14
#define LIST_ROWS     6
#define ROW_HEIGHT    13
#define MAX_RELEARN   40
#define PAL_BRICKS    12
#define PAL_FRAME     14
#define PAL_TEXT      15
#define FRAME_TILE    0x200
#define TAG_ICON      0x5360
#define TAG_HAND      0x5361

struct Ware
{
    u8 kind;
    u8 rarity;
    u8 sold;
    u16 value;      // move, item of relic
    u16 price;
};

struct SpireShop
{
    void (*onDone)(void);
    struct Ware wares[MAX_WARES];
    u8 count;
    u8 cursor;
    u8 scroll;
    u8 state;
    u8 mon;
    u8 slot;
    u8 relearnCount;
    u8 relearnCursor;
    u8 relearnScroll;
    u16 teachMove;
    u16 relearnMoves[MAX_RELEARN];
    u8 iconSpriteId;
    u8 typeSpriteId;
    u8 keeperSpriteId;
    u8 monIconIds[2];
    u8 message[160];
};

static EWRAM_DATA struct SpireShop *sShop = NULL;

static const u32 sBrickTiles[2][8] =
{
    {0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x22222222},
    {0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x22222222},
};
static const u16 sBrickPal[16] = {RGB(4, 7, 12), RGB(4, 7, 12), RGB(7, 11, 18)};   // Mart-blauw

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
static const u8 sColor_Green[]  = {0, 9, 10};
static const u8 sColor_Red[]    = {0, 11, 12};
static const u8 sColor_Purple[] = {0, 14, 15};
static const u8 *const sRarityColor[] = {sColor_Dark, sColor_Blue, sColor_Gold};
static const u8 *const sRarityName[] = {COMPOUND_STRING("Common"), COMPOUND_STRING("Uncommon"), COMPOUND_STRING("Rare")};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER]  = {.bg = 0, .tilemapLeft = 1,  .tilemapTop = 1,  .width = 28, .height = 2,  .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_LIST]    = {.bg = 0, .tilemapLeft = 1,  .tilemapTop = 4,  .width = 17, .height = 10, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_PREVIEW] = {.bg = 0, .tilemapLeft = 20, .tilemapTop = 4,  .width = 9,  .height = 10, .paletteNum = PAL_TEXT, .baseBlock = 0x0E3},
    [WIN_DESC]    = {.bg = 0, .tilemapLeft = 1,  .tilemapTop = 16, .width = 28, .height = 3,  .paletteNum = PAL_TEXT, .baseBlock = 0x13D},
    DUMMY_WIN_TEMPLATE,
};

static void Task_SpireShop(u8 taskId);

// --- prijzen (zie SPIRE_BALANS.md) ------------------------------------------------------------
static const u16 sMovePrice[] = {45, 70, 120};
static const u16 sItemPrice[] = {50, 85, 140};
#define RELIC_PRICE   120
#define POTION_PRICE  35
#define ELIXIR_PRICE  40

static u16 RelearnPrice(void)
{
    return 50 + 25 * RUN.relearns;
}

// --- hulpjes ----------------------------------------------------------------------------------
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(win, font, x, y, color, TEXT_SKIP_DRAW, str);
}

static void PrintRight(u32 win, u32 font, u32 right, u32 y, const u8 *color, const u8 *str)
{
    PrintText(win, font, right - GetStringWidth(font, str, 0), y, color, str);
}

// Tekst over maximaal twee regels van 220 px verdelen (beschrijvingen uit de game zijn drie smalle regels).
static const u8 *Reflow(const u8 *src)
{
    u8 *dst = gStringVar4, *lineStart = gStringVar4, *lastSpace = NULL;
    bool32 broke = FALSE;

    while (*src != EOS && dst < gStringVar4 + 200)
    {
        u8 ch = (*src == CHAR_NEWLINE) ? CHAR_SPACE : *src;

        src++;
        *dst = ch;
        dst[1] = EOS;
        if (ch == CHAR_SPACE)
            lastSpace = dst;
        if (!broke && lastSpace != NULL && GetStringWidth(FONT_SMALL_NARROW, lineStart, 0) > 218)
        {
            *lastSpace = CHAR_NEWLINE;
            lineStart = lastSpace + 1;
            broke = TRUE;
        }
        dst++;
    }
    *dst = EOS;
    return gStringVar4;
}

static bool32 MonKnowsMove(struct Pokemon *mon, u32 move)
{
    u32 i;

    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == move)
            return TRUE;
    return FALSE;
}

static const u8 sName_Potion[] = _("Super Potion");
static const u8 sName_Elixir[] = _("Max Elixir");
static const u8 sName_Relearner[] = _("Move Relearner");
static const u8 sDesc_Potion[] = _("Both Pokémon heal 25% of their max HP. Right now, right here, on the counter.");
static const u8 sDesc_Elixir[] = _("Restores all PP of both Pokémon. PP carry over between battles in the Spire.");
static const u8 sDesc_Relearner[] = _("Remember any level-up move of the Pokémon's current species. You only pay if it learns one.");

static const u8 *WareName(const struct Ware *w)
{
    switch (w->kind)
    {
    case WARE_MOVE:    return GetMoveName(w->value);
    case WARE_ITEM:    return GetItemName(w->value);
    case WARE_RELIC:   return gSpireRelics[w->value].name;
    case WARE_POTION:  return sName_Potion;
    case WARE_ELIXIR:  return sName_Elixir;
    default:           return sName_Relearner;
    }
}

static const u8 *WareDesc(const struct Ware *w)
{
    switch (w->kind)
    {
    case WARE_MOVE:    return GetMoveDescription(w->value);
    case WARE_ITEM:    return Spire_GetItemDescription(w->value);
    case WARE_RELIC:   return gSpireRelics[w->value].desc;
    case WARE_POTION:  return sDesc_Potion;
    case WARE_ELIXIR:  return sDesc_Elixir;
    default:           return sDesc_Relearner;
    }
}

static u16 WarePrice(const struct Ware *w)
{
    return w->kind == WARE_RELEARN ? RelearnPrice() : w->price;
}

// --- waren --------------------------------------------------------------------------------------
static bool32 Taken(u32 n, u32 kind, u16 value)
{
    u32 i;

    for (i = 0; i < n; i++)
        if (sShop->wares[i].kind == kind && sShop->wares[i].value == value)
            return TRUE;
    return FALSE;
}

static void AddWare(u32 kind, u32 rarity, u16 value, u16 price)
{
    struct Ware *w = &sShop->wares[sShop->count++];

    w->kind = kind;
    w->rarity = rarity;
    w->value = value;
    w->price = price;
}

static void BuildWares(void)
{
    static const u8 sMoveRarity[] = {0, 0, 1, 1, 2};
    static const u8 sItemRarity[] = {0, 0, 1, 1};
    u32 i, tries;

    // moves: de eerste vier passen bij de types van je team (zoals klassekaarten), de laatste is vrij
    for (i = 0; i < ARRAY_COUNT(sMoveRarity); i++)
    {
        u16 move = MOVE_NONE;

        for (tries = 0; tries < 20; tries++)
        {
            u32 type = TYPE_NONE;

            if (i < 4)
                type = GetSpeciesType(GetMonData(&RUN.mons[i & 1], MON_DATA_SPECIES), (i >> 1) & 1);
            move = Spire_RandomMoveOfType(sMoveRarity[i], type, i * 5 + tries);
            if (!Taken(sShop->count, WARE_MOVE, move))
                break;
        }
        AddWare(WARE_MOVE, sMoveRarity[i], move, sMovePrice[sMoveRarity[i]]);
    }
    for (i = 0; i < ARRAY_COUNT(sItemRarity); i++)
    {
        u32 rarity = sItemRarity[i] + (i == 3 && Random() % 4 == 0);
        u16 item = ITEM_NONE;

        for (tries = 0; tries < 20; tries++)
        {
            item = Spire_RandomHeldItem(rarity, i * 7 + tries);
            if (!Taken(sShop->count, WARE_ITEM, item))
                break;
        }
        AddWare(WARE_ITEM, rarity, item, sItemPrice[rarity]);
    }
    for (i = 0; i < 2; i++)
    {
        u32 relic = SPIRE_RELIC_COUNT;

        for (tries = 0; tries < 20; tries++)
        {
            relic = Spire_RandomNewRelic(i * 3 + tries);
            if (relic >= SPIRE_RELIC_COUNT || !Taken(sShop->count, WARE_RELIC, relic))
                break;
        }
        if (relic < SPIRE_RELIC_COUNT && !Taken(sShop->count, WARE_RELIC, relic))
            AddWare(WARE_RELIC, 2, relic, RELIC_PRICE);
    }
    AddWare(WARE_POTION, 0, ITEM_SUPER_POTION, POTION_PRICE);
    AddWare(WARE_ELIXIR, 0, ITEM_MAX_ELIXIR, ELIXIR_PRICE);
    AddWare(WARE_RELEARN, 1, ITEM_HEART_SCALE, 0);
}

// --- tekenen ----------------------------------------------------------------------------------
static void DrawHeader(void)
{
    u8 buf[16];

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Blue, COMPOUND_STRING("POKé MART"));
    // positie in de lijst (de lijst scrolt)
    if (sShop->state == STATE_RELEARN)
    {
        ConvertIntToDecimalStringN(buf, sShop->relearnCursor + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringAppend(buf, COMPOUND_STRING("/"));
        ConvertIntToDecimalStringN(buf + StringLength(buf), sShop->relearnCount, STR_CONV_MODE_LEFT_ALIGN, 2);
    }
    else
    {
        ConvertIntToDecimalStringN(buf, sShop->cursor + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringAppend(buf, COMPOUND_STRING("/"));
        ConvertIntToDecimalStringN(buf + StringLength(buf), sShop->count, STR_CONV_MODE_LEFT_ALIGN, 2);
    }
    StringAppend(buf, COMPOUND_STRING(" {UP_ARROW}{DOWN_ARROW}"));
    PrintText(WIN_HEADER, FONT_SMALL_NARROW, 112, 3, sColor_Gray, buf);
    ConvertIntToDecimalStringN(buf, RUN.gold, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, COMPOUND_STRING("¥"));
    PrintRight(WIN_HEADER, FONT_NORMAL, 218, 1, sColor_Gold, buf);
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawList(void)
{
    u32 r;

    FillWindowPixelBuffer(WIN_LIST, PIXEL_FILL(1));
    if (sShop->state == STATE_RELEARN)
    {
        for (r = 0; r < LIST_ROWS && sShop->relearnScroll + r < sShop->relearnCount; r++)
        {
            u32 i = sShop->relearnScroll + r;

            if (i == sShop->relearnCursor)
                PrintText(WIN_LIST, FONT_SMALL_NARROW, 2, r * ROW_HEIGHT + 2, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_LIST, FONT_SMALL_NARROW, 10, r * ROW_HEIGHT + 2, sColor_Dark, GetMoveName(sShop->relearnMoves[i]));
        }
        CopyWindowToVram(WIN_LIST, COPYWIN_FULL);
        return;
    }
    for (r = 0; r < LIST_ROWS && sShop->scroll + r < sShop->count; r++)
    {
        u32 i = sShop->scroll + r;
        const struct Ware *w = &sShop->wares[i];
        const u8 *name = WareName(w);
        u32 font = GetStringWidth(FONT_SMALL_NARROW, name, 0) > 92 ? FONT_SMALL_NARROWER : FONT_SMALL_NARROW;
        u8 buf[12];

        if (i == sShop->cursor && sShop->state == STATE_LIST)
            PrintText(WIN_LIST, FONT_SMALL_NARROW, 2, r * ROW_HEIGHT + 2, sColor_Red, COMPOUND_STRING("▶"));
        PrintText(WIN_LIST, font, 10, r * ROW_HEIGHT + 2, w->sold ? sColor_Gray : sRarityColor[w->kind == WARE_MOVE || w->kind == WARE_ITEM ? w->rarity : 0], name);
        if (w->sold)
        {
            PrintRight(WIN_LIST, FONT_SMALL_NARROW, 134, r * ROW_HEIGHT + 2, sColor_Gray, COMPOUND_STRING("SOLD"));
        }
        else
        {
            ConvertIntToDecimalStringN(buf, WarePrice(w), STR_CONV_MODE_LEFT_ALIGN, 4);
            StringAppend(buf, COMPOUND_STRING("¥"));
            PrintRight(WIN_LIST, FONT_SMALL_NARROW, 134, r * ROW_HEIGHT + 2, RUN.gold >= WarePrice(w) ? sColor_Dark : sColor_Red, buf);
        }
    }
    CopyWindowToVram(WIN_LIST, COPYWIN_FULL);
}

static void FreeIcon(void)
{
    if (sShop->iconSpriteId != SPRITE_NONE)
    {
        DestroySprite(&gSprites[sShop->iconSpriteId]);
        sShop->iconSpriteId = SPRITE_NONE;
    }
    FreeSpriteTilesByTag(TAG_ICON);
    FreeSpritePaletteByTag(TAG_ICON);
}

static void ShowItemIcon(u16 item)
{
    u8 id;

    FreeIcon();
    id = AddItemIconSprite(TAG_ICON, TAG_ICON, item);
    if (id != MAX_SPRITES)
    {
        gSprites[id].x = 160 + 36;
        gSprites[id].y = 32 + 22;
        gSprites[id].oam.priority = 0;
        sShop->iconSpriteId = id;
    }
}

static void ShowMonIcons(bool32 show)
{
    u32 i;

    for (i = 0; i < 2; i++)
        gSprites[sShop->monIconIds[i]].invisible = !show;
}

// Rechts: icoon, soort en details van de ware onder de cursor; of de moves van de gekozen Pokémon.
static void DrawPreview(void)
{
    const struct Ware *w = &sShop->wares[sShop->cursor];
    u8 buf[24];

    FillWindowPixelBuffer(WIN_PREVIEW, PIXEL_FILL(1));
    gSprites[sShop->typeSpriteId].invisible = TRUE;
    ShowMonIcons(FALSE);

    if (sShop->state == STATE_CHOOSE_MON)
    {
        u32 i;

        FreeIcon();
        ShowMonIcons(TRUE);
        for (i = 0; i < 2; i++)
        {
            struct Pokemon *mon = Spire_GetRunMon(i);
            u16 held = GetMonData(mon, MON_DATA_HELD_ITEM);

            GetMonData(mon, MON_DATA_NICKNAME, buf);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 26, 4 + i * 38, sShop->mon == i ? sColor_Red : sColor_Dark, buf);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROWER, 26, 16 + i * 38, sColor_Gray, held != ITEM_NONE ? GetItemName(held) : COMPOUND_STRING("no item"));
            if (sShop->mon == i)
                PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 0, 8 + i * 38, sColor_Red, COMPOUND_STRING("▶"));
        }
    }
    else if (sShop->state == STATE_CHOOSE_SLOT)
    {
        struct Pokemon *mon = Spire_GetRunMon(sShop->mon);
        u32 i;

        FreeIcon();
        PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 2, 0, sColor_Blue, COMPOUND_STRING("Forget:"));
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            u32 m = GetMonData(mon, MON_DATA_MOVE1 + i);

            if (sShop->slot == i)
                PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 0, 13 + i * 13, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROWER, 8, 13 + i * 13, m ? sColor_Dark : sColor_Gray, m ? GetMoveName(m) : COMPOUND_STRING("-"));
        }
    }
    else if (sShop->state == STATE_RELEARN)
    {
        u16 move = sShop->relearnMoves[sShop->relearnCursor];

        FreeIcon();
        gSprites[sShop->typeSpriteId].invisible = FALSE;
        StartSpriteAnim(&gSprites[sShop->typeSpriteId], GetMoveType(move));
        gSprites[sShop->typeSpriteId].oam.paletteNum = gTypesInfo[GetMoveType(move)].palette;
        StringCopy(buf, COMPOUND_STRING("PWR "));
        if (GetMovePower(move) > 1)
            ConvertIntToDecimalStringN(buf + 4, GetMovePower(move), STR_CONV_MODE_LEFT_ALIGN, 3);
        else
            StringAppend(buf, COMPOUND_STRING("-"));
        PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 34, sColor_Dark, buf);
        StringCopy(buf, COMPOUND_STRING("PP "));
        ConvertIntToDecimalStringN(buf + 3, GetMovePP(move), STR_CONV_MODE_LEFT_ALIGN, 2);
        PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 45, sColor_Dark, buf);
    }
    else
    {
        switch (w->kind)
        {
        case WARE_MOVE:
        {
            u32 cat = GetMoveCategory(w->value);

            FreeIcon();
            gSprites[sShop->typeSpriteId].invisible = FALSE;
            StartSpriteAnim(&gSprites[sShop->typeSpriteId], GetMoveType(w->value));
            gSprites[sShop->typeSpriteId].oam.paletteNum = gTypesInfo[GetMoveType(w->value)].palette;
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 34, sColor_Dark,
                      cat == DAMAGE_CATEGORY_PHYSICAL ? COMPOUND_STRING("Physical") : cat == DAMAGE_CATEGORY_SPECIAL ? COMPOUND_STRING("Special") : COMPOUND_STRING("Status"));
            StringCopy(buf, COMPOUND_STRING("PWR "));
            if (GetMovePower(w->value) > 1)
                ConvertIntToDecimalStringN(buf + 4, GetMovePower(w->value), STR_CONV_MODE_LEFT_ALIGN, 3);
            else
                StringAppend(buf, COMPOUND_STRING("-"));
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 45, sColor_Dark, buf);
            StringCopy(buf, COMPOUND_STRING("PP "));
            ConvertIntToDecimalStringN(buf + 3, GetMovePP(w->value), STR_CONV_MODE_LEFT_ALIGN, 2);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 56, sColor_Dark, buf);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 68, sRarityColor[w->rarity], sRarityName[w->rarity]);
            break;
        }
        case WARE_ITEM:
            ShowItemIcon(w->value);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 40, sColor_Dark, COMPOUND_STRING("Held item"));
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 51, sColor_Gray, COMPOUND_STRING("one per mon"));
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 66, sRarityColor[w->rarity], sRarityName[w->rarity]);
            break;
        case WARE_RELIC:
            ShowItemIcon(gSpireRelics[w->value].item);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 40, sColor_Gold, COMPOUND_STRING("Relic"));
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 51, sColor_Gray, COMPOUND_STRING("whole team"));
            break;
        default:
            ShowItemIcon(w->value);
            PrintText(WIN_PREVIEW, FONT_SMALL_NARROW, 4, 40, sColor_Green, w->kind == WARE_RELEARN ? COMPOUND_STRING("Service") : COMPOUND_STRING("Used now"));
            break;
        }
    }
    CopyWindowToVram(WIN_PREVIEW, COPYWIN_FULL);
}

static void DrawDesc(void)
{
    FillWindowPixelBuffer(WIN_DESC, PIXEL_FILL(1));
    switch (sShop->state)
    {
    case STATE_LIST:
        PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Dark, Reflow(WareDesc(&sShop->wares[sShop->cursor])));
        break;
    case STATE_CHOOSE_MON:
        if (sShop->wares[sShop->cursor].kind == WARE_ITEM)
            PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Blue, COMPOUND_STRING("Who holds it? The old item stays behind.\nB: cancel, money back."));
        else if (sShop->wares[sShop->cursor].kind == WARE_RELEARN)
            PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Blue, COMPOUND_STRING("Who remembers a move?\nB: cancel."));
        else
            PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Blue, COMPOUND_STRING("Who learns it?\nB: cancel, money back."));
        break;
    case STATE_CHOOSE_SLOT:
        StringCopy(gStringVar1, GetMoveName(sShop->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Which move makes room for {STR_VAR_1}?\nB: back."));
        PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Blue, gStringVar4);
        break;
    case STATE_RELEARN:
        PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Dark, Reflow(GetMoveDescription(sShop->relearnMoves[sShop->relearnCursor])));
        break;
    case STATE_MESSAGE:
        PrintText(WIN_DESC, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sShop->message);
        break;
    }
    CopyWindowToVram(WIN_DESC, COPYWIN_FULL);
}

static void Redraw(void)
{
    DrawHeader();
    DrawList();
    DrawPreview();
    DrawDesc();
}

// --- scherm -------------------------------------------------------------------------------------
static void VBlankCB_SpireShop(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireShop(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

void Spire_OpenShop(void (*onDone)(void))
{
    u16 *tilemap;
    u32 i, x, y;

    sShop = AllocZeroed(sizeof(*sShop));
    sShop->onDone = onDone;
    sShop->iconSpriteId = SPRITE_NONE;
    BuildWares();

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
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sShop->monIconIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon, 160 + 14, 32 + 14 + i * 38,
                                             0, GetMonData(mon, MON_DATA_PERSONALITY));
        gSprites[sShop->monIconIds[i]].oam.priority = 0;
    }
    // de winkelhouder: Banette (afgedankte pop met een wrok; ruilt liever dan dat hij verkoopt)
    sShop->keeperSpriteId = CreateMonIconNoPersonality(SPECIES_BANETTE, SpriteCB_MonIcon, 8 + 92, 8 + 6, 0);
    LoadCompressedSpriteSheet(&gSpriteSheet_MoveTypes);
    LoadPalette(gMoveTypes_Pal, OBJ_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);
    sShop->typeSpriteId = CreateSprite(&gSpriteTemplate_MoveTypes, 160 + 36, 32 + 22, 0);
    gSprites[sShop->typeSpriteId].oam.priority = 0;

    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireShop);
    SetMainCallback2(CB2_SpireShop);
    CreateTask(Task_SpireShop, 0);
}

static void CloseShop(void)
{
    void (*onDone)(void) = sShop->onDone;

    FreeIcon();
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sShop);
    sShop = NULL;
    onDone();
}

static void ShowMessage(const u8 *text)
{
    StringExpandPlaceholders(sShop->message, text);
    sShop->state = STATE_MESSAGE;
    Redraw();
}

static void Refund(void)
{
    struct Ware *w = &sShop->wares[sShop->cursor];

    if (w->sold && w->kind != WARE_RELEARN)
    {
        RUN.gold += w->price;
        w->sold = FALSE;
    }
}

// --- kopen --------------------------------------------------------------------------------------
static void Buy(void)
{
    struct Ware *w = &sShop->wares[sShop->cursor];
    u16 price = WarePrice(w);

    if (w->sold || RUN.gold < price)
    {
        PlaySE(SE_FAILURE);
        if (!w->sold)
            ShowMessage(COMPOUND_STRING("Not enough money. The Mart is not a charity,\nunlike the Pokémon Center."));
        return;
    }
    PlaySE(SE_SHOP);
    switch (w->kind)
    {
    case WARE_MOVE:
        RUN.gold -= price;
        w->sold = TRUE;
        sShop->teachMove = w->value;
        sShop->mon = 0;
        sShop->state = STATE_CHOOSE_MON;
        break;
    case WARE_ITEM:
        RUN.gold -= price;
        w->sold = TRUE;
        sShop->mon = 0;
        sShop->state = STATE_CHOOSE_MON;
        break;
    case WARE_RELEARN:
        sShop->teachMove = MOVE_NONE;
        sShop->mon = 0;
        sShop->state = STATE_CHOOSE_MON;
        break;
    case WARE_RELIC:
        RUN.gold -= price;
        w->sold = TRUE;
        Spire_AddRelic(w->value);
        StringCopy(gStringVar1, gSpireRelics[w->value].name);
        ShowMessage(COMPOUND_STRING("You got the {STR_VAR_1}!\nIt works for your whole team."));
        return;
    case WARE_POTION:
        RUN.gold -= price;
        w->sold = TRUE;
        Spire_HealRun(25);
        ShowMessage(COMPOUND_STRING("Both Pokémon heal 25%.\nThe clerk pretends not to see the spraying."));
        return;
    case WARE_ELIXIR:
        RUN.gold -= price;
        w->sold = TRUE;
        Spire_RestorePP();
        ShowMessage(COMPOUND_STRING("All PP restored.\nIt tastes like batteries."));
        return;
    }
    Redraw();
}

static void BuildRelearnList(void)
{
    struct Pokemon *mon = Spire_GetRunMon(sShop->mon);
    const struct LevelUpMove *learnset = GetSpeciesLevelUpLearnset(GetMonData(mon, MON_DATA_SPECIES));
    u32 i, j;

    sShop->relearnCount = 0;
    sShop->relearnCursor = 0;
    sShop->relearnScroll = 0;
    for (i = 0; learnset[i].move != LEVEL_UP_MOVE_END && sShop->relearnCount < MAX_RELEARN; i++)
    {
        u16 move = learnset[i].move;
        bool32 dup = MonKnowsMove(mon, move) || Spire_IsMoveBanned(move);

        for (j = 0; j < sShop->relearnCount && !dup; j++)
            if (sShop->relearnMoves[j] == move)
                dup = TRUE;
        if (!dup)
            sShop->relearnMoves[sShop->relearnCount++] = move;
    }
}

static void StartChooseSlot(u16 move)
{
    struct Pokemon *mon = Spire_GetRunMon(sShop->mon);
    u32 i;

    sShop->teachMove = move;
    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
            break;
    sShop->slot = (i < MAX_MON_MOVES) ? i : 0;
    sShop->state = STATE_CHOOSE_SLOT;
    Redraw();
}

static void ChooseMon(void)
{
    struct Ware *w = &sShop->wares[sShop->cursor];
    struct Pokemon *mon = Spire_GetRunMon(sShop->mon);

    PlaySE(SE_SELECT);
    if (w->kind == WARE_ITEM)
    {
        u16 old = GetMonData(mon, MON_DATA_HELD_ITEM);

        SetMonData(mon, MON_DATA_HELD_ITEM, &w->value);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetItemName(w->value));
        if (old != ITEM_NONE)
        {
            StringCopy(gStringVar3, GetItemName(old));
            ShowMessage(COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}.\nThe {STR_VAR_3} stays behind on the counter."));
        }
        else
        {
            ShowMessage(COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}."));
        }
    }
    else if (w->kind == WARE_RELEARN)
    {
        BuildRelearnList();
        if (sShop->relearnCount == 0)
            ShowMessage(COMPOUND_STRING("The Relearner shrugs. There is nothing to\nremember. No fee."));
        else
        {
            sShop->state = STATE_RELEARN;
            Redraw();
        }
    }
    else if (MonKnowsMove(mon, sShop->teachMove))
    {
        PlaySE(SE_FAILURE);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        Refund();
        ShowMessage(COMPOUND_STRING("{STR_VAR_1} already knows it. Money back."));
    }
    else
    {
        StartChooseSlot(sShop->teachMove);
    }
}

static void Teach(void)
{
    struct Ware *w = &sShop->wares[sShop->cursor];
    struct Pokemon *mon = Spire_GetRunMon(sShop->mon);

    PlaySE(SE_RG_BALL_CLICK);
    SetMonMoveSlot(mon, sShop->teachMove, sShop->slot);
    Spire_ClearSlotUpgrade(mon, sShop->slot);
    if (w->kind == WARE_RELEARN)
    {
        RUN.gold -= min(RUN.gold, RelearnPrice());
        RUN.relearns++;
    }
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringCopy(gStringVar2, GetMoveName(sShop->teachMove));
    ShowMessage(COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
}

static void Task_SpireShop(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    switch (sShop->state)
    {
    case STATE_LIST:
    {
        u32 cur = sShop->cursor;

        if (JOY_REPEAT(DPAD_UP) && cur > 0)
            cur--;
        else if (JOY_REPEAT(DPAD_DOWN) && cur + 1 < sShop->count)
            cur++;
        else if (JOY_NEW(A_BUTTON))
            Buy();
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sShop->state = STATE_EXIT;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        if (cur != sShop->cursor)
        {
            PlaySE(SE_SELECT);
            sShop->cursor = cur;
            if (cur < sShop->scroll)
                sShop->scroll = cur;
            else if (cur >= sShop->scroll + LIST_ROWS)
                sShop->scroll = cur - LIST_ROWS + 1;
            Redraw();
        }
        break;
    }
    case STATE_CHOOSE_MON:
        if (JOY_NEW(DPAD_UP | DPAD_DOWN | DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sShop->mon ^= 1;
            Redraw();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            ChooseMon();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            Refund();
            sShop->state = STATE_LIST;
            Redraw();
        }
        break;
    case STATE_CHOOSE_SLOT:
        if (JOY_NEW(DPAD_UP) && sShop->slot > 0)
        {
            PlaySE(SE_SELECT);
            sShop->slot--;
            Redraw();
        }
        else if (JOY_NEW(DPAD_DOWN) && sShop->slot + 1 < MAX_MON_MOVES)
        {
            PlaySE(SE_SELECT);
            sShop->slot++;
            Redraw();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            Teach();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sShop->state = (sShop->wares[sShop->cursor].kind == WARE_RELEARN) ? STATE_RELEARN : STATE_CHOOSE_MON;
            Redraw();
        }
        break;
    case STATE_RELEARN:
    {
        u32 cur = sShop->relearnCursor;

        if (JOY_REPEAT(DPAD_UP) && cur > 0)
            cur--;
        else if (JOY_REPEAT(DPAD_DOWN) && cur + 1 < sShop->relearnCount)
            cur++;
        else if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            StartChooseSlot(sShop->relearnMoves[cur]);
            break;
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sShop->state = STATE_CHOOSE_MON;
            Redraw();
            break;
        }
        if (cur != sShop->relearnCursor)
        {
            PlaySE(SE_SELECT);
            sShop->relearnCursor = cur;
            if (cur < sShop->relearnScroll)
                sShop->relearnScroll = cur;
            else if (cur >= sShop->relearnScroll + LIST_ROWS)
                sShop->relearnScroll = cur - LIST_ROWS + 1;
            Redraw();
        }
        break;
    }
    case STATE_MESSAGE:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sShop->state = STATE_LIST;
            Redraw();
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseShop();
        break;
    }
}
