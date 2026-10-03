// Project Grounded: The Spire - kaartenscherm (zie SPIRE_DESIGN.md en tools/grounded/spire/mockups.py).
// Eén scherm voor alles met "kies een van drie": moves na een gevecht, relics, de draft van rentals,
// de rustplek, de winkel en events. Plus een simpel berichtscherm (einde run, nieuwe act).
// Stijl: torenstenen op de achtergrond, kaarten in kaders, rode rand om de gekozen kaart, de PC-hand.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
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
#include "strings.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

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
    CARD_NONE,
    CARD_MOVE,
    CARD_MON,
    CARD_RELIC,
    CARD_OPTION,
};

// opties (rust, winkel, events)
enum
{
    OPT_REST,
    OPT_EVOLVE_0,
    OPT_EVOLVE_1,
    OPT_POTION,
    OPT_EV_SAMPLE,
    OPT_EV_STEAL,
    OPT_EV_LEAVE,
    OPT_EV_READ,
    OPT_EV_GRAMMAR,
    OPT_EV_OPEN,
    OPT_EV_POKE,
    OPT_EV_ACCEPT,
    OPT_EV_RUDE,
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
#define BRICK_TILE    0x000
#define PAL_BRICKS    12
#define PAL_FRAME_SEL 13
#define PAL_FRAME     14
#define PAL_TEXT      15
#define TAG_HAND      0x5301
#define TAG_ITEM      0x5310

struct SpireCard
{
    u8 kind;
    u8 rarity;      // 0 common, 1 uncommon, 2 rare
    u8 sold:1;
    u16 value;      // move, soort, relic of optie
    u16 price;      // winkel; 0 = gratis
};

struct SpireCards
{
    void (*onDone)(void);
    const u8 *title;
    const u8 *text;
    struct SpireCard cards[3];
    u8 count;
    u8 mode;
    u8 state;
    u8 card;
    u8 mon;
    u8 slot;
    u8 afterMessage;        // 0 = klaar, 1 = terug naar de kaarten
    u8 event;
    u16 teachMove;
    u8 handSpriteId;
    u8 iconSpriteIds[2];
    u8 cardSpriteIds[3][2];
    u8 bob;
    u8 message[160];
};

static EWRAM_DATA struct SpireCards *sCards = NULL;

// --- graphics ---------------------------------------------------------------------------------
static const u16 sHandCursor_Pal[] = INCBIN_U16("graphics/pokemon_storage/hand_cursor.gbapal");
static const u8 sHandCursor_Gfx[] = INCBIN_U8("graphics/pokemon_storage/hand_cursor.4bpp");

// stenen: twee tegels, 16x8 per steen, verspringend per rij (index 1 = steen, 2 = voeg)
static const u32 sBrickTiles[2][8] =
{
    {0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x22222222},
    {0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x22222222},
};
static const u16 sBrickPal[16] = {RGB(5, 4, 9), RGB(5, 4, 9), RGB(8, 7, 14)};

// tekstpalet: 1 wit, 2 donker, 3 schaduw, 4/5 blauw, 6/7 goud, 8 grijs, 9/10 groen, 11/12 rood, 13 balk
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

static const u8 sRarityBarColor[] = {8, 4, 6};
static const u8 *const sRarityTextColor[] = {sColor_Gray, sColor_Blue, sColor_Gold};
static const u8 sText_Common[] = _("COMMON");
static const u8 sText_Uncommon[] = _("UNCOMMON");
static const u8 sText_Rare[] = _("RARE");
static const u8 *const sRarityName[] = {sText_Common, sText_Uncommon, sText_Rare};
static const u8 sText_Phys[] = _("Phys.");
static const u8 sText_Spec[] = _("Spec.");
static const u8 sText_Status[] = _("Stat.");

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_CARD_0] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_CARD_1] = {.bg = 0, .tilemapLeft = 11, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x069},
    [WIN_CARD_2] = {.bg = 0, .tilemapLeft = 21, .tilemapTop = 5, .width = 8, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x099},
    [WIN_BOTTOM] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 13, .width = 28, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x0C9},
    DUMMY_WIN_TEMPLATE,
};

static const struct OamData sOam_Hand = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};
static const struct SpriteSheet sSpriteSheet_Hand = {sHandCursor_Gfx, 0x200, TAG_HAND};
static const struct SpritePalette sSpritePal_Hand = {sHandCursor_Pal, TAG_HAND};
static void SpriteCB_Hand(struct Sprite *sprite);
static const struct SpriteTemplate sSpriteTemplate_Hand =
{
    .tileTag = TAG_HAND, .paletteTag = TAG_HAND, .oam = &sOam_Hand, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCB_Hand,
};

static void CB2_SpireCards(void);
static void Task_SpireCards(u8 taskId);
static void Redraw(void);

// --- events (placeholders; Jordi herschrijft) --------------------------------------------------
struct SpireEvent
{
    const u8 *title;
    const u8 *story;
    u8 options[3];
};

static const struct SpireEvent sEvents[] =
{
    {COMPOUND_STRING("FREE SAMPLES"), COMPOUND_STRING("A Kecleon runs a free sample stand.\nIt is suspiciously free."),
     {OPT_EV_SAMPLE, OPT_EV_STEAL, OPT_EV_LEAVE}},
    {COMPOUND_STRING("WRITING ON THE WALL"), COMPOUND_STRING("An Unown spells out a word on the wall.\nIt is an insult. About you."),
     {OPT_EV_READ, OPT_EV_GRAMMAR, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A CHEST"), COMPOUND_STRING("A treasure chest. It is breathing.\nIt is a Ditto. It is doing its best."),
     {OPT_EV_OPEN, OPT_EV_POKE, OPT_EV_LEAVE}},
    {COMPOUND_STRING("A HELPFUL HIKER"), COMPOUND_STRING("A Hiker offers to carry your team\nup a floor. He insists. Loudly."),
     {OPT_EV_ACCEPT, OPT_EV_RUDE, OPT_EV_LEAVE}},
};

struct SpireOption
{
    const u8 *name;
    const u8 *line1;
    const u8 *line2;
    const u8 *desc;
    u16 iconSpecies;
};

static const struct SpireOption sOptions[] =
{
    [OPT_REST]       = {COMPOUND_STRING("Rest"), COMPOUND_STRING("Heal HP"), COMPOUND_STRING("and all PP"), COMPOUND_STRING("Chansey patches your team up.\nNo questions. No insurance."), SPECIES_CHANSEY},
    [OPT_EVOLVE_0]   = {COMPOUND_STRING("Evolve"), COMPOUND_STRING("your first"), COMPOUND_STRING("Pokémon"), COMPOUND_STRING("Evolve now. Stronger, bigger,\nslightly more opinionated."), SPECIES_NONE},
    [OPT_EVOLVE_1]   = {COMPOUND_STRING("Evolve"), COMPOUND_STRING("your second"), COMPOUND_STRING("Pokémon"), COMPOUND_STRING("Evolve now. Stronger, bigger,\nslightly more opinionated."), SPECIES_NONE},
    [OPT_POTION]     = {COMPOUND_STRING("Potion"), COMPOUND_STRING("Heal both"), COMPOUND_STRING("for 30%"), COMPOUND_STRING("A Potion for the whole team.\nShaken, not stirred."), SPECIES_NONE},
    [OPT_EV_SAMPLE]  = {COMPOUND_STRING("Taste it"), COMPOUND_STRING("Heal 30%"), COMPOUND_STRING("...or not"), COMPOUND_STRING("Probably food. Probably."), SPECIES_NONE},
    [OPT_EV_STEAL]   = {COMPOUND_STRING("Steal it"), COMPOUND_STRING("+40 ¥"), COMPOUND_STRING("-15% HP"), COMPOUND_STRING("Kecleon can turn invisible.\nAnd it hits hard."), SPECIES_NONE},
    [OPT_EV_LEAVE]   = {COMPOUND_STRING("Leave"), COMPOUND_STRING("Nothing"), COMPOUND_STRING("happens"), COMPOUND_STRING("The safest choice.\nThe tower judges you for it."), SPECIES_NONE},
    [OPT_EV_READ]    = {COMPOUND_STRING("Read it"), COMPOUND_STRING("Learn a"), COMPOUND_STRING("rare move"), COMPOUND_STRING("Say the word out loud.\nSomething answers."), SPECIES_NONE},
    [OPT_EV_GRAMMAR] = {COMPOUND_STRING("Correct it"), COMPOUND_STRING("+30 ¥"), COMPOUND_STRING(""), COMPOUND_STRING("Fix the spelling. The Unown\npays you to go away."), SPECIES_NONE},
    [OPT_EV_OPEN]    = {COMPOUND_STRING("Open it"), COMPOUND_STRING("Get a relic"), COMPOUND_STRING("-20% HP"), COMPOUND_STRING("It bites. Then it gives you\nsomething to make up for it."), SPECIES_NONE},
    [OPT_EV_POKE]    = {COMPOUND_STRING("Poke it"), COMPOUND_STRING("+25 ¥"), COMPOUND_STRING(""), COMPOUND_STRING("It drops some coins and\npretends nothing happened."), SPECIES_NONE},
    [OPT_EV_ACCEPT]  = {COMPOUND_STRING("Accept"), COMPOUND_STRING("Heal 25%"), COMPOUND_STRING(""), COMPOUND_STRING("Being carried is undignified.\nAlso very relaxing."), SPECIES_NONE},
    [OPT_EV_RUDE]    = {COMPOUND_STRING("Refuse"), COMPOUND_STRING("+2 BP"), COMPOUND_STRING(""), COMPOUND_STRING("He respects your rudeness.\nHikers are like that."), SPECIES_NONE},
};

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

static bool32 IsSecondDraft(void)
{
    return GetMonData(&RUN.mons[0], MON_DATA_SPECIES) != SPECIES_NONE;
}

static bool32 CardTaken(u32 n, u32 kind, u32 value)
{
    u32 j;

    for (j = 0; j < n; j++)
        if (sCards->cards[j].kind == kind && sCards->cards[j].value == value)
            return TRUE;
    return FALSE;
}

static void AddMoveCard(u32 i, s32 forceRarity)
{
    struct SpireCard *c = &sCards->cards[i];
    u32 tries = 0;

    c->kind = CARD_MOVE;
    do
    {
        u32 roll = Random() % 100;

        if (forceRarity >= 0)
            c->rarity = forceRarity;
        else
            c->rarity = roll < 10 ? 2 : roll < 40 ? 1 : 0;
        c->value = Spire_RandomMove(c->rarity, i + tries);
    } while (CardTaken(i, CARD_MOVE, c->value) && ++tries < 20);
}

static void BuildCards(void)
{
    u32 i;

    memset(sCards->cards, 0, sizeof(sCards->cards));
    sCards->count = 3;
    switch (sCards->mode)
    {
    case SPIRE_CARDS_MOVES:
        for (i = 0; i < 3; i++)
            AddMoveCard(i, -1);
        break;
    case SPIRE_CARDS_RELICS:
        sCards->count = 0;
        for (i = 0; i < 3; i++)
        {
            u32 relic, tries = 0;

            do
                relic = Spire_RandomNewRelic(i * 3 + tries);
            while (relic < SPIRE_RELIC_COUNT && CardTaken(sCards->count, CARD_RELIC, relic) && ++tries < 20);
            if (relic >= SPIRE_RELIC_COUNT || CardTaken(sCards->count, CARD_RELIC, relic))
                break;
            sCards->cards[sCards->count].kind = CARD_RELIC;
            sCards->cards[sCards->count].value = relic;
            sCards->cards[sCards->count].rarity = 2;
            sCards->count++;
        }
        break;
    case SPIRE_CARDS_DRAFT:
        for (i = 0; i < 3; i++)
        {
            u32 tries = 0;
            u16 species;

            do
                species = Spire_RandomRental(i + tries * 3);
            while ((CardTaken(i, CARD_MON, species) || (IsSecondDraft() && GetMonData(&RUN.mons[0], MON_DATA_SPECIES) == species))
                && ++tries < 30);
            sCards->cards[i].kind = CARD_MON;
            sCards->cards[i].value = species;
        }
        break;
    case SPIRE_CARDS_REST:
        sCards->count = 1;
        sCards->cards[0].kind = CARD_OPTION;
        sCards->cards[0].value = OPT_REST;
        for (i = 0; i < 2; i++)
        {
            if (Spire_CanEvolve(i))
            {
                sCards->cards[sCards->count].kind = CARD_OPTION;
                sCards->cards[sCards->count].value = OPT_EVOLVE_0 + i;
                sCards->count++;
            }
        }
        break;
    case SPIRE_CARDS_SHOP:
        AddMoveCard(0, 1 + (Random() % 3 == 0));
        sCards->cards[0].price = sCards->cards[0].rarity == 2 ? 70 : 40;
        sCards->cards[1].kind = CARD_RELIC;
        sCards->cards[1].value = Spire_RandomNewRelic(0);
        sCards->cards[1].rarity = 2;
        sCards->cards[1].price = 100;
        if (sCards->cards[1].value >= SPIRE_RELIC_COUNT)
        {
            AddMoveCard(1, 2);
            sCards->cards[1].price = 70;
        }
        sCards->cards[2].kind = CARD_OPTION;
        sCards->cards[2].value = OPT_POTION;
        sCards->cards[2].price = 30;
        break;
    case SPIRE_CARDS_EVENT:
        sCards->event = Random() % ARRAY_COUNT(sEvents);
        for (i = 0; i < 3; i++)
        {
            sCards->cards[i].kind = CARD_OPTION;
            sCards->cards[i].value = sEvents[sCards->event].options[i];
        }
        break;
    default:
        sCards->count = 0;
        break;
    }
}

// --- tekenen ----------------------------------------------------------------------------------
static void DrawHeader(void)
{
    u8 buf[32];
    u32 x;

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    switch (sCards->mode)
    {
    case SPIRE_CARDS_MOVES:
    case SPIRE_CARDS_RELICS:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Dark, sCards->mode == SPIRE_CARDS_MOVES ? COMPOUND_STRING("VICTORY!") : COMPOUND_STRING("TREASURE!"));
        x = 96;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.bp, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING(" BP"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Blue, buf);
        x += GetStringWidth(FONT_NORMAL, buf, 0) + 8;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.gold, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Gold, buf);
        x += GetStringWidth(FONT_NORMAL, buf, 0) + 8;
        buf[0] = CHAR_PLUS;
        ConvertIntToDecimalStringN(buf + 1, gSpireResult.healPercent, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("% HP"));
        PrintText(WIN_HEADER, FONT_NORMAL, x, 1, sColor_Green, buf);
        break;
    case SPIRE_CARDS_DRAFT:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, COMPOUND_STRING("THE SPIRE"));
        PrintText(WIN_HEADER, FONT_NORMAL, 84, 1, sColor_Dark,
                  IsSecondDraft() ? COMPOUND_STRING("Pick your 2nd Pokémon") : COMPOUND_STRING("Pick your 1st Pokémon"));
        break;
    case SPIRE_CARDS_REST:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Red, COMPOUND_STRING("POKéMON CENTER"));
        PrintText(WIN_HEADER, FONT_NORMAL, 130, 1, sColor_Dark, COMPOUND_STRING("Take a breather."));
        break;
    case SPIRE_CARDS_SHOP:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Blue, COMPOUND_STRING("POKé MART"));
        ConvertIntToDecimalStringN(buf, RUN.gold, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintText(WIN_HEADER, FONT_NORMAL, 214 - GetStringWidth(FONT_NORMAL, buf, 0), 1, sColor_Gold, buf);
        break;
    case SPIRE_CARDS_EVENT:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sEvents[sCards->event].title);
        break;
    case SPIRE_CARDS_MESSAGE:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sCards->title);
        break;
    }
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

// Alleen de rand (tilemap), zonder de inhoud van het venster te wissen.
static void DrawFrameOnly(u32 win, u32 pal)
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

static void DrawCardFrame(u32 i)
{
    DrawFrameOnly(WIN_CARD_0 + i, (i == sCards->card && sCards->state == STATE_CARDS) ? PAL_FRAME_SEL : PAL_FRAME);
}

static void DrawFooter(u32 win, struct SpireCard *c, const u8 *fallback, const u8 *color)
{
    u8 buf[12];

    if (c->sold)
    {
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, sColor_Red, COMPOUND_STRING("SOLD"));
    }
    else if (c->price)
    {
        ConvertIntToDecimalStringN(buf, c->price, STR_CONV_MODE_LEFT_ALIGN, 4);
        StringAppend(buf, COMPOUND_STRING("¥"));
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, RUN.gold >= c->price ? sColor_Gold : sColor_Red, buf);
    }
    else if (fallback != NULL)
    {
        PrintCentered(win, FONT_SMALL_NARROW, 37, 64, color, fallback);
    }
}

static void DrawCard(u32 i)
{
    u32 win = WIN_CARD_0 + i;
    struct SpireCard *c = &sCards->cards[i];
    u8 buf[16];

    DrawCardFrame(i);
    PutWindowTilemap(win);
    FillWindowPixelBuffer(win, PIXEL_FILL(1));
    switch (c->kind)
    {
    case CARD_MOVE:
    {
        const u8 *cat;

        FillWindowPixelRect(win, PIXEL_FILL(sRarityBarColor[c->rarity]), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetMoveName(c->value));
        switch (GetMoveCategory(c->value))
        {
        case DAMAGE_CATEGORY_PHYSICAL: cat = sText_Phys; break;
        case DAMAGE_CATEGORY_SPECIAL:  cat = sText_Spec; break;
        default:                       cat = sText_Status; break;
        }
        PrintText(win, FONT_SMALL_NARROW, 40, 15, sColor_Dark, cat);
        if (GetMovePower(c->value) > 1)
        {
            StringCopy(buf, COMPOUND_STRING("PWR "));
            ConvertIntToDecimalStringN(buf + 4, GetMovePower(c->value), STR_CONV_MODE_LEFT_ALIGN, 3);
        }
        else
        {
            StringCopy(buf, COMPOUND_STRING("PWR -"));
        }
        PrintText(win, FONT_SMALL_NARROW, 2, 26, sColor_Dark, buf);
        StringCopy(buf, COMPOUND_STRING("PP "));
        ConvertIntToDecimalStringN(buf + 3, GetMovePP(c->value), STR_CONV_MODE_LEFT_ALIGN, 2);
        PrintText(win, FONT_SMALL_NARROW, 40, 26, sColor_Dark, buf);
        DrawFooter(win, c, sRarityName[c->rarity], sRarityTextColor[c->rarity]);
        break;
    }
    case CARD_MON:
        FillWindowPixelRect(win, PIXEL_FILL(14), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetSpeciesName(c->value));
        break;
    case CARD_RELIC:
        FillWindowPixelRect(win, PIXEL_FILL(6), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, gSpireRelics[c->value].name);
        DrawFooter(win, c, COMPOUND_STRING("RELIC"), sColor_Gold);
        break;
    case CARD_OPTION:
    {
        const struct SpireOption *o = &sOptions[c->value];

        FillWindowPixelRect(win, PIXEL_FILL(11), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, o->name);
        if (c->value == OPT_EVOLVE_0 || c->value == OPT_EVOLVE_1)
        {
            PrintCentered(win, FONT_SMALL_NARROW, 37, 64, sColor_Purple,
                          GetSpeciesName(GetMonData(&RUN.mons[c->value - OPT_EVOLVE_0], MON_DATA_SPECIES)));
        }
        else if (o->iconSpecies == SPECIES_NONE)
        {
            PrintCentered(win, FONT_SMALL_NARROW, 16, 64, sColor_Dark, o->line1);
            PrintCentered(win, FONT_SMALL_NARROW, 26, 64, sColor_Dark, o->line2);
        }
        DrawFooter(win, c, NULL, sColor_Dark);
        break;
    }
    }
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

static bool32 ShowTeam(void)
{
    return sCards->mode != SPIRE_CARDS_DRAFT && sCards->mode != SPIRE_CARDS_MESSAGE
        && sCards->state != STATE_CHOOSE_SLOT && sCards->state != STATE_MESSAGE;
}

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
        if (sCards->state == STATE_CHOOSE_MON && sCards->mon == i)
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

static void DrawSpeciesStats(u16 species)
{
    u8 buf[64];
    u8 *p = buf;

    p = StringCopy(p, COMPOUND_STRING("HP "));
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
    p = ConvertIntToDecimalStringN(p, gSpeciesInfo[species].baseSpeed, STR_CONV_MODE_LEFT_ALIGN, 3);
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetSpeciesName(species));
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 12, sColor_Gray, buf);
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 28, sColor_Dark, COMPOUND_STRING("It evolves after act 1. Pick wisely, or don't."));
}

static void SetSpritesVisible(void)
{
    u32 i;
    bool32 team = ShowTeam();

    for (i = 0; i < 2; i++)
        if (sCards->iconSpriteIds[i] != SPRITE_NONE)
            gSprites[sCards->iconSpriteIds[i]].invisible = !team;
}

static void DrawBottom(void)
{
    struct SpireCard *c = &sCards->cards[sCards->card];
    u32 move = (c->kind == CARD_MOVE) ? c->value : MOVE_NONE;

    FillWindowPixelBuffer(WIN_BOTTOM, PIXEL_FILL(1));
    switch (sCards->state)
    {
    case STATE_CARDS:
        if (sCards->count == 0)
        {
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, COMPOUND_STRING("Nothing left to take. Press A."));
            break;
        }
        if (sCards->mode == SPIRE_CARDS_EVENT)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sEvents[sCards->event].story);
        else if (c->kind == CARD_MOVE)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetMoveDescription(c->value));
        else if (c->kind == CARD_RELIC)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gSpireRelics[c->value].desc);
        else if (c->kind == CARD_OPTION)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sOptions[c->value].desc);
        if (sCards->mode == SPIRE_CARDS_DRAFT)
            DrawSpeciesStats(c->value);
        else
            DrawTeamRow(22, move);
        break;
    case STATE_CHOOSE_MON:
        StringCopy(gStringVar1, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Teach {STR_VAR_1} to whom?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        DrawTeamRow(22, sCards->teachMove);
        break;
    case STATE_CHOOSE_SLOT:
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);
        u32 i;

        StringCopy(gStringVar1, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Forget which move for {STR_VAR_1}?"));
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            u32 m = GetMonData(mon, MON_DATA_MOVE1 + i);

            if (sCards->slot == i)
                PrintText(WIN_BOTTOM, FONT_NORMAL, 26 + (i % 2) * 100, 14 + (i / 2) * 14, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 36 + (i % 2) * 100, 16 + (i / 2) * 14, sColor_Dark,
                      m ? GetMoveName(m) : COMPOUND_STRING("-"));
        }
        break;
    }
    case STATE_MESSAGE:
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sCards->message);
        break;
    }
    CopyWindowToVram(WIN_BOTTOM, COPYWIN_FULL);
    SetSpritesVisible();
}

static void PlaceHand(void)
{
    struct Sprite *hand = &gSprites[sCards->handSpriteId];

    if (sCards->state == STATE_CARDS && sCards->count > 0)
    {
        hand->x = 8 + sCards->card * 80 + 52;
        hand->y = 34;
        hand->invisible = FALSE;
    }
    else
    {
        hand->invisible = TRUE;
    }
}

static void SpriteCB_Hand(struct Sprite *sprite)
{
    sCards->bob++;
    sprite->y2 = (sCards->bob & 0x10) ? 2 : 0;
}

static void Redraw(void)
{
    u32 i;

    for (i = 0; i < 3; i++)
        if (i < sCards->count)
            DrawCardFrame(i);
    ScheduleBgCopyTilemapToVram(0);
    DrawBottom();
    PlaceHand();
}

// --- sprites op de kaarten --------------------------------------------------------------------
static u8 CreateTypeSprite(enum Type type, s16 x, s16 y)
{
    u8 id = CreateSprite(&gSpriteTemplate_MoveTypes, x, y, 0);

    StartSpriteAnim(&gSprites[id], type);
    gSprites[id].oam.paletteNum = gTypesInfo[type].palette;
    gSprites[id].oam.priority = 0;
    return id;
}

static void CreateCardSprites(u32 i)
{
    struct SpireCard *c = &sCards->cards[i];
    s16 left = 8 + i * 80;
    u8 id;

    sCards->cardSpriteIds[i][0] = sCards->cardSpriteIds[i][1] = SPRITE_NONE;
    switch (c->kind)
    {
    case CARD_MOVE:
        sCards->cardSpriteIds[i][0] = CreateTypeSprite(GetMoveType(c->value), left + 18, 40 + 16 + 4);
        break;
    case CARD_MON:
        id = CreateMonIconNoPersonality(c->value, SpriteCB_MonIcon, left + 18, 40 + 30, 0);
        gSprites[id].oam.priority = 0;
        sCards->cardSpriteIds[i][0] = id;
        sCards->cardSpriteIds[i][1] = CreateTypeSprite(GetSpeciesType(c->value, 0), left + 50, 40 + 22);
        if (GetSpeciesType(c->value, 1) != GetSpeciesType(c->value, 0))
            CreateTypeSprite(GetSpeciesType(c->value, 1), left + 50, 40 + 38);
        break;
    case CARD_RELIC:
        id = AddItemIconSprite(TAG_ITEM + i, TAG_ITEM + i, gSpireRelics[c->value].item);
        if (id != MAX_SPRITES)
        {
            gSprites[id].x = left + 32;
            gSprites[id].y = 40 + 26;
            gSprites[id].oam.priority = 0;
            sCards->cardSpriteIds[i][0] = id;
        }
        break;
    case CARD_OPTION:
    {
        u16 species = sOptions[c->value].iconSpecies;

        if (c->value == OPT_EVOLVE_0 || c->value == OPT_EVOLVE_1)
        {
            const struct Evolution *evo = GetSpeciesEvolutions(GetMonData(&RUN.mons[c->value - OPT_EVOLVE_0], MON_DATA_SPECIES));
            species = evo[0].targetSpecies;
        }
        if (species != SPECIES_NONE)
        {
            id = CreateMonIconNoPersonality(species, SpriteCB_MonIcon, left + 32, 40 + 26, 0);
            gSprites[id].oam.priority = 0;
            sCards->cardSpriteIds[i][0] = id;
        }
        break;
    }
    }
}

// --- scherm openen en sluiten -----------------------------------------------------------------
static void VBlankCB_SpireCards(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireCards(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void LoadBricks(void)
{
    u16 *tilemap = AllocZeroed(BG_SCREEN_SIZE);
    u32 x, y;

    LoadBgTiles(1, sBrickTiles, sizeof(sBrickTiles), BRICK_TILE);
    LoadPalette(sBrickPal, BG_PLTT_ID(PAL_BRICKS), PLTT_SIZE_4BPP);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = (((x + (y & 1)) & 1) + BRICK_TILE) | (PAL_BRICKS << 12);
    SetBgTilemapBuffer(1, tilemap);
    ScheduleBgCopyTilemapToVram(1);
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

    LoadBricks();
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadWindowGfx(WIN_HEADER, 0, FRAME_TILE, BG_PLTT_ID(PAL_FRAME));
    // rode variant van het kader voor de gekozen kaart (randkleuren 2-6)
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME)], &gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL)], PLTT_SIZE_4BPP);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 2] = RGB(18, 3, 3);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 3] = RGB(29, 8, 6);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 4] = RGB(24, 5, 5);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 5] = RGB(31, 13, 10);
    gPlttBufferUnfaded[BG_PLTT_ID(PAL_FRAME_SEL) + 6] = RGB(31, 19, 16);
    gPlttBufferUnfaded[0] = RGB(5, 4, 9);

    DrawFrameOnly(WIN_HEADER, PAL_FRAME);
    DrawFrameOnly(WIN_BOTTOM, PAL_FRAME);
    PutWindowTilemap(WIN_HEADER);
    PutWindowTilemap(WIN_BOTTOM);

    LoadMonIconPalettes();
    LoadSpriteSheet(&sSpriteSheet_Hand);
    LoadSpritePalette(&sSpritePal_Hand);
    LoadCompressedSpriteSheet(&gSpriteSheet_MoveTypes);
    LoadPalette(gMoveTypes_Pal, OBJ_PLTT_ID(13), 3 * PLTT_SIZE_4BPP);

    for (i = 0; i < sCards->count; i++)
    {
        CreateCardSprites(i);
        DrawCard(i);
    }
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sCards->iconSpriteIds[i] = SPRITE_NONE;
        if (sCards->mode != SPIRE_CARDS_DRAFT && sCards->mode != SPIRE_CARDS_MESSAGE && GetMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE)
        {
            sCards->iconSpriteIds[i] = CreateMonIcon(GetMonData(mon, MON_DATA_SPECIES), SpriteCB_MonIcon,
                                                     8 + 24 + i * 104, 104 + 22 + 10, 0, GetMonData(mon, MON_DATA_PERSONALITY));
            gSprites[sCards->iconSpriteIds[i]].oam.priority = 0;
        }
    }
    sCards->handSpriteId = CreateSprite(&sSpriteTemplate_Hand, 0, 0, 0);

    DrawHeader();
    if (sCards->mode == SPIRE_CARDS_MESSAGE)
    {
        sCards->state = STATE_MESSAGE;
        StringCopy(sCards->message, sCards->text);
        sCards->afterMessage = 0;
    }
    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireCards);
    SetMainCallback2(CB2_SpireCards);
    CreateTask(Task_SpireCards, 0);
}

static void OpenCards(u32 mode, const u8 *title, const u8 *text, void (*onDone)(void))
{
    sCards = AllocZeroed(sizeof(*sCards));
    sCards->mode = mode;
    sCards->onDone = onDone;
    sCards->title = title;
    sCards->text = text;
    BuildCards();
    SetupScreen();
}

void Spire_OpenCards(u32 mode, void (*onDone)(void))
{
    OpenCards(mode, NULL, NULL, onDone);
}

void Spire_OpenMessage(const u8 *title, const u8 *text, void (*onDone)(void))
{
    OpenCards(SPIRE_CARDS_MESSAGE, title, text, onDone);
}

static void CloseScreen(void)
{
    void (*onDone)(void) = sCards->onDone;

    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sCards);
    sCards = NULL;
    onDone();
}

static void Exit(void)
{
    sCards->state = STATE_EXIT;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
}

static void ShowMessage(const u8 *text, bool32 backToCards)
{
    StringCopy(sCards->message, text);
    sCards->state = STATE_MESSAGE;
    sCards->afterMessage = backToCards;
    Redraw();
}

static void StartTeach(u16 move)
{
    sCards->teachMove = move;
    sCards->mon = 0;
    sCards->state = STATE_CHOOSE_MON;
    Redraw();
}

static void LoseHp(u32 percent)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), loss = GetMonData(mon, MON_DATA_MAX_HP) * percent / 100;

        hp = (hp > loss) ? hp - loss : 1;
        SetMonData(mon, MON_DATA_HP, &hp);
    }
}

static void AddGold(u32 gold)
{
    RUN.gold = min(9999, RUN.gold + gold);
}

// --- keuzes uitvoeren -------------------------------------------------------------------------
static void PickOption(u32 opt)
{
    switch (opt)
    {
    case OPT_REST:
        Spire_HealRun(Spire_HasRelic(SPIRE_RELIC_SOOTHE_BELL) ? 80 : SPIRE_REST_HEAL);
        Spire_RestorePP();
        ShowMessage(COMPOUND_STRING("Your team rests. HP and PP restored."), FALSE);
        break;
    case OPT_EVOLVE_0:
    case OPT_EVOLVE_1:
    {
        u32 i = opt - OPT_EVOLVE_0;

        GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, gStringVar1);
        Spire_Evolve(i);
        StringCopy(gStringVar2, GetSpeciesName(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} evolved into {STR_VAR_2}!"));
        ShowMessage(gStringVar4, FALSE);
        break;
    }
    case OPT_POTION:
        Spire_HealRun(30);
        ShowMessage(COMPOUND_STRING("Both Pokémon feel better."), TRUE);
        break;
    case OPT_EV_SAMPLE:
        if (Random() % 2)
        {
            Spire_HealRun(30);
            ShowMessage(COMPOUND_STRING("Delicious! Your team heals 30%."), FALSE);
        }
        else
        {
            LoseHp(10);
            ShowMessage(COMPOUND_STRING("It was a sock. Your team loses 10% HP."), FALSE);
        }
        break;
    case OPT_EV_STEAL:
        AddGold(40);
        LoseHp(15);
        ShowMessage(COMPOUND_STRING("You grab 40¥. Kecleon grabs you back."), FALSE);
        break;
    case OPT_EV_READ:
        StartTeach(Spire_RandomMove(2, Random()));
        break;
    case OPT_EV_GRAMMAR:
        AddGold(30);
        ShowMessage(COMPOUND_STRING("The Unown pays you 30¥ to leave."), FALSE);
        break;
    case OPT_EV_OPEN:
    {
        u32 relic = Spire_RandomNewRelic(0);

        LoseHp(20);
        if (relic < SPIRE_RELIC_COUNT)
        {
            Spire_AddRelic(relic);
            StringCopy(gStringVar1, gSpireRelics[relic].name);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Ouch! But you got {STR_VAR_1}!"));
            ShowMessage(gStringVar4, FALSE);
        }
        else
        {
            ShowMessage(COMPOUND_STRING("Ouch. It was empty. Ditto shrugs."), FALSE);
        }
        break;
    }
    case OPT_EV_POKE:
        AddGold(25);
        ShowMessage(COMPOUND_STRING("Ditto drops 25¥ and looks away."), FALSE);
        break;
    case OPT_EV_ACCEPT:
        Spire_HealRun(25);
        ShowMessage(COMPOUND_STRING("You are carried. It is humiliating.\nYour team heals 25%."), FALSE);
        break;
    case OPT_EV_RUDE:
        RUN.bp += 2;
        ShowMessage(COMPOUND_STRING("The Hiker nods with respect. +2 BP."), FALSE);
        break;
    default:
        ShowMessage(COMPOUND_STRING("You walk on. Nothing happens.\nThe tower sighs."), FALSE);
        break;
    }
}

static void PickCard(void)
{
    struct SpireCard *c = &sCards->cards[sCards->card];

    if (c->sold)
    {
        PlaySE(SE_FAILURE);
        return;
    }
    if (c->price)
    {
        if (RUN.gold < c->price)
        {
            PlaySE(SE_FAILURE);
            ShowMessage(COMPOUND_STRING("Not enough money. The Mart is not\na charity, unlike the Pokémon Center."), TRUE);
            return;
        }
        RUN.gold -= c->price;
        c->sold = TRUE;
        DrawHeader();
        DrawCard(sCards->card);
    }
    PlaySE(SE_SELECT);
    switch (c->kind)
    {
    case CARD_MOVE:
        StartTeach(c->value);
        break;
    case CARD_RELIC:
        Spire_AddRelic(c->value);
        StringCopy(gStringVar1, gSpireRelics[c->value].name);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("You got the {STR_VAR_1}!"));
        ShowMessage(gStringVar4, sCards->mode == SPIRE_CARDS_SHOP);
        break;
    case CARD_MON:
    {
        u32 slot = IsSecondDraft() ? 1 : 0;

        Spire_SetRental(slot, c->value);
        StringCopy(gStringVar1, GetSpeciesName(c->value));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} joins you!"));
        ShowMessage(gStringVar4, FALSE);
        break;
    }
    case CARD_OPTION:
        PickOption(c->value);
        break;
    }
}

// --- invoer -----------------------------------------------------------------------------------
static void HandleCards(void)
{
    if (sCards->count == 0)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON))
            Exit();
        return;
    }
    if (JOY_NEW(DPAD_LEFT) && sCards->card > 0)
    {
        PlaySE(SE_SELECT);
        DrawCardFrame(sCards->card);
        sCards->card--;
        Redraw();
    }
    else if (JOY_NEW(DPAD_RIGHT) && sCards->card + 1 < sCards->count)
    {
        PlaySE(SE_SELECT);
        DrawCardFrame(sCards->card);
        sCards->card++;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PickCard();
    }
    else if (JOY_NEW(B_BUTTON) && (sCards->mode == SPIRE_CARDS_MOVES || sCards->mode == SPIRE_CARDS_RELICS || sCards->mode == SPIRE_CARDS_SHOP))
    {
        PlaySE(SE_SELECT);
        Exit();
    }
}

static void HandleChooseMon(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sCards->mon ^= 1;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);

        PlaySE(SE_SELECT);
        if (MonKnowsMove(mon, sCards->teachMove))
        {
            GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} already knows it!"));
            ShowMessage(gStringVar4, TRUE);
        }
        else
        {
            u32 i;

            // lege plek? dan meteen leren
            for (i = 0; i < MAX_MON_MOVES; i++)
            {
                if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
                    break;
            }
            sCards->slot = (i < MAX_MON_MOVES) ? i : 0;
            sCards->state = STATE_CHOOSE_SLOT;
            Redraw();
        }
    }
    else if (JOY_NEW(B_BUTTON) && sCards->mode != SPIRE_CARDS_EVENT)
    {
        PlaySE(SE_SELECT);
        sCards->state = STATE_CARDS;
        Redraw();
    }
}

static void HandleChooseSlot(void)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        sCards->slot ^= 1;
        Redraw();
    }
    else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
    {
        PlaySE(SE_SELECT);
        sCards->slot ^= 2;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        struct Pokemon *mon = Spire_GetRunMon(sCards->mon);

        PlaySE(SE_RG_BALL_CLICK);
        SetMonMoveSlot(mon, sCards->teachMove, sCards->slot);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
        ShowMessage(gStringVar4, sCards->mode == SPIRE_CARDS_SHOP);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sCards->state = STATE_CHOOSE_MON;
        Redraw();
    }
}

static void Task_SpireCards(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    switch (sCards->state)
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
            if (sCards->afterMessage)
            {
                sCards->state = STATE_CARDS;
                Redraw();
            }
            else
            {
                Exit();
            }
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseScreen();
        break;
    }
}
