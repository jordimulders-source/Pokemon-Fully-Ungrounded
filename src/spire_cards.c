// Project Grounded: The Spire - kaartenscherm (zie SPIRE_DESIGN.md en tools/grounded/spire/mockups.py).
// "Kies een van drie" na een gevecht (moves, relics) en bij een vertakte evolutie, plus een simpel
// berichtscherm (einde run, nieuwe act). Draft, rustplek, winkel en events hebben een eigen bestand.
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
};

enum
{
    STATE_CARDS,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_SLOT,
    STATE_MESSAGE,
    STATE_EXIT,
};

#define MAX_CARDS       3

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
    u16 value;      // move, soort of relic
};

struct SpireCards
{
    void (*onDone)(void);
    const u8 *title;
    const u8 *text;
    struct SpireCard cards[MAX_CARDS];
    u8 count;
    u8 mode;
    u8 state;
    u8 card;
    u8 mon;
    u8 slot;
    u8 afterMessage;        // 0 = klaar, 1 = terug naar de kaarten
    u16 teachMove;
    u8 handSpriteId;
    u8 iconSpriteIds[2];
    u8 cardSpriteIds[MAX_CARDS][3];
    u8 bob;
    u8 message[160];
    u8 list[SPIRE_RELIC_COUNT];     // relic-lijst (R op de kaart): alle relics die je hebt
    u8 listCount;
    u8 page;                        // drie per pagina
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
// relics: common grijs, uncommon blauw, rare goud, shop groen, boss rood
static const u8 sRelicTierBarColor[SPIRE_RELIC_TIER_COUNT] = {8, 4, 6, 9, 11};
static const u8 *const sRelicTierTextColor[SPIRE_RELIC_TIER_COUNT] = {sColor_Gray, sColor_Blue, sColor_Gold, sColor_Green, sColor_Red};
static const u8 sText_TierShop[] = _("SHOP RELIC");
static const u8 sText_TierBoss[] = _("BOSS RELIC");
static const u8 *const sRelicTierName[SPIRE_RELIC_TIER_COUNT] = {sText_Common, sText_Uncommon, sText_Rare, sText_TierShop, sText_TierBoss};
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


// --- helpers ----------------------------------------------------------------------------------
// Altijd met transparante achtergrond (het venster is al gevuld): anders wist elke regel de onderkant
// van de regel erboven.
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    u8 c[3] = {TEXT_COLOR_TRANSPARENT, color[1], color[2]};

    AddTextPrinterParameterized3(win, font, x, y, c, TEXT_SKIP_DRAW, str);
}

static void PrintCentered(u32 win, u32 font, u32 y, u32 width, const u8 *color, const u8 *str)
{
    s32 x;

    if (font == FONT_SMALL_NARROW && GetStringWidth(font, str, 0) > (s32)width - 2)
        font = FONT_SMALL_NARROWER; // lange namen (Heavy-Duty Boots)
    x = (width - GetStringWidth(font, str, 0)) / 2;
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

static bool32 CardTaken(u32 n, u32 kind, u32 value)
{
    u32 j;

    for (j = 0; j < n; j++)
        if (sCards->cards[j].kind == kind && sCards->cards[j].value == value)
            return TRUE;
    return FALSE;
}

static void AddMoveCard(u32 i)
{
    struct SpireCard *c = &sCards->cards[i];
    u32 tries = 0;

    c->kind = CARD_MOVE;
    do
    {
        u32 roll = Random() % 100;

        u32 type = TYPE_NONE;

        if (Spire_HasRelic(SPIRE_RELIC_TM_CASE)) // relic: betere beloningen (25% rare, 45% uncommon)
            c->rarity = roll < 25 ? 2 : roll < 70 ? 1 : 0;
        else
            c->rarity = roll < 10 ? 2 : roll < 40 ? 1 : 0;
        if (i < 2)
        {
            u16 species = GetMonData(&RUN.mons[i], MON_DATA_SPECIES);
            type = GetSpeciesType(species, (Random() & 1) ? 1 : 0);
        }
        c->value = Spire_RandomMoveOfType(c->rarity, type, i + tries);
    } while (CardTaken(i, CARD_MOVE, c->value) && ++tries < 20);
}

// Relic-lijst: de kaarten van de huidige pagina
static void FillRelicPage(void)
{
    u32 i, first = sCards->page * MAX_CARDS;

    memset(sCards->cards, 0, sizeof(sCards->cards));
    sCards->count = 0;
    for (i = 0; i < MAX_CARDS && first + i < sCards->listCount; i++)
    {
        sCards->cards[i].kind = CARD_RELIC;
        sCards->cards[i].value = sCards->list[first + i];
        sCards->count++;
    }
}

static void BuildCards(void)
{
    u32 i;

    memset(sCards->cards, 0, sizeof(sCards->cards));
    sCards->count = 3;
    switch (sCards->mode)
    {
    case SPIRE_CARDS_MOVES:
        // kaart 1 past bij je eerste Pokémon, kaart 2 bij je tweede, kaart 3 is willekeurig (zoals klassekaarten in Slay)
        for (i = 0; i < 3; i++)
            AddMoveCard(i);
        break;
    case SPIRE_CARDS_RELICS:
    {
        // elite: elke kaart common 50 / uncommon 33 / rare 17%; baas: boss-relics (gSpireRelicSource)
        u8 offered[MAX_CARDS];

        sCards->count = 0;
        for (i = 0; i < MAX_CARDS; i++)
        {
            u32 relic = Spire_RandomRelic(gSpireRelicSource, i * 3, offered, sCards->count);

            if (relic >= SPIRE_RELIC_COUNT)
                break;
            offered[sCards->count] = relic;
            sCards->cards[sCards->count].kind = CARD_RELIC;
            sCards->cards[sCards->count].value = relic;
            sCards->cards[sCards->count].rarity = 2;
            sCards->count++;
        }
        break;
    }
    case SPIRE_CARDS_RELIC_LIST:
        sCards->listCount = 0;
        for (i = 0; i < SPIRE_RELIC_COUNT; i++)
            if (Spire_HasRelic(i))
                sCards->list[sCards->listCount++] = i;
        sCards->page = 0;
        FillRelicPage();
        break;
    case SPIRE_CARDS_EVOLVE:
    {
        u16 targets[3];

        sCards->count = Spire_GetEvolutions(GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_SPECIES), targets);
        for (i = 0; i < sCards->count; i++)
        {
            sCards->cards[i].kind = CARD_MON;
            sCards->cards[i].value = targets[i];
        }
        break;
    }
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
    case SPIRE_CARDS_MESSAGE:
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sCards->title);
        break;
    case SPIRE_CARDS_RELIC_LIST:
        ConvertIntToDecimalStringN(gStringVar1, sCards->listCount, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("YOUR RELICS ({STR_VAR_1})"));
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Dark, gStringVar4);
        ConvertIntToDecimalStringN(gStringVar1, sCards->page + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        ConvertIntToDecimalStringN(gStringVar2, (sCards->listCount + MAX_CARDS - 1) / MAX_CARDS, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("page {STR_VAR_1}/{STR_VAR_2}"));
        PrintText(WIN_HEADER, FONT_NORMAL, 160, 1, sColor_Gray, gStringVar4);
        break;
    case SPIRE_CARDS_EVOLVE:
        GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_NICKNAME, gStringVar1);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} is evolving!"));
        PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, gStringVar4);
        PrintText(WIN_HEADER, FONT_NORMAL, 150, 1, sColor_Dark, COMPOUND_STRING("Into what?"));
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

static void DrawFooter(u32 win, const u8 *text, const u8 *color)
{
    PrintCentered(win, FONT_SMALL_NARROW, 37, 64, color, text);
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
        DrawFooter(win, sRarityName[c->rarity], sRarityTextColor[c->rarity]);
        break;
    }
    case CARD_MON:
        FillWindowPixelRect(win, PIXEL_FILL(14), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, GetSpeciesName(c->value));
        break;
    case CARD_RELIC:
    {
        u32 tier = gSpireRelics[c->value].tier;

        FillWindowPixelRect(win, PIXEL_FILL(sRelicTierBarColor[tier]), 0, 0, 64, 3);
        PrintCentered(win, FONT_SMALL_NARROW, 3, 64, sColor_Dark, gSpireRelics[c->value].name);
        DrawFooter(win, sRelicTierName[tier], sRelicTierTextColor[tier]);
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
    return sCards->mode != SPIRE_CARDS_MESSAGE && sCards->mode != SPIRE_CARDS_EVOLVE && sCards->mode != SPIRE_CARDS_RELIC_LIST
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

static const u8 *const sTierName[] = {COMPOUND_STRING("COMMON"), COMPOUND_STRING("COMMON"), COMPOUND_STRING("UNCOMMON"), COMPOUND_STRING("RARE")};

// Startmoves (als de soort ook een rental is) en verdere evoluties; voor het evolutiescherm.
static void DrawDraftLine(u16 species)
{
    const struct SpireRental *rental = Spire_FindRental(species);
    u16 targets[3];
    u8 *p = gStringVar4;
    u32 i;

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
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 24, sColor_Dark, gStringVar4);
        PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 170, 0, rental->tier >= 3 ? sColor_Gold : rental->tier == 2 ? sColor_Blue : sColor_Gray,
                  sTierName[rental->tier]);
    }
    p = gStringVar4;
    if (Spire_GetEvolutions(species, targets))
    {
        u16 mid = targets[0];

        p = StringCopy(p, COMPOUND_STRING("Act 2: "));
        p = StringCopy(p, GetSpeciesName(mid));
        if (Spire_GetEvolutions(species, targets) > 1)
            p = StringCopy(p, COMPOUND_STRING(" (or more)"));
        if (Spire_GetEvolutions(mid, targets))
        {
            p = StringCopy(p, COMPOUND_STRING("  Act 3: "));
            p = StringCopy(p, GetSpeciesName(targets[0]));
        }
    }
    else
    {
        p = StringCopy(p, COMPOUND_STRING("Does not evolve. Strong now, never stronger."));
    }
    PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 36, sColor_Purple, gStringVar4);
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
    DrawDraftLine(species);
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
        if (c->kind == CARD_MOVE)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, GetMoveDescription(c->value));
        else if (c->kind == CARD_RELIC)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gSpireRelics[c->value].desc);
        if (sCards->mode == SPIRE_CARDS_EVOLVE)
            DrawSpeciesStats(c->value);
        else if (sCards->mode == SPIRE_CARDS_RELIC_LIST)
            PrintText(WIN_BOTTOM, FONT_SMALL_NARROW, 2, 34, sColor_Gray, COMPOUND_STRING("{LEFT_ARROW}{RIGHT_ARROW}: browse     A/B: back to the map"));
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

    for (i = 0; i < sCards->count; i++)
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

static void CreateCardSprites(u32 card)
{
    struct SpireCard *c = &sCards->cards[card];
    u32 i = card;
    s16 left = 8 + i * 80;
    u8 id;

    sCards->cardSpriteIds[i][0] = sCards->cardSpriteIds[i][1] = sCards->cardSpriteIds[i][2] = SPRITE_NONE;
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
            sCards->cardSpriteIds[i][2] = CreateTypeSprite(GetSpeciesType(c->value, 1), left + 50, 40 + 38);
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
    }
}

static void DestroyCardSprites(u32 slot)
{
    u32 j;

    for (j = 0; j < 3; j++)
    {
        u8 id = sCards->cardSpriteIds[slot][j];

        if (id == SPRITE_NONE || id >= MAX_SPRITES)
            continue;
        DestroySprite(&gSprites[id]);
        sCards->cardSpriteIds[slot][j] = SPRITE_NONE;
    }
    // item-iconen hebben een eigen tag per plek: altijd vrijgeven, anders erft de volgende kaart het oude icoon
    FreeSpriteTilesByTag(TAG_ITEM + slot);
    FreeSpritePaletteByTag(TAG_ITEM + slot);
}

// Kaarten tekenen (lege plekken blijven leeg).
static void ShowCards(void)
{
    u32 i;

    for (i = 0; i < MAX_CARDS; i++)
    {
        DestroyCardSprites(i);
        if (i < sCards->count)
        {
            CreateCardSprites(i);
            DrawCard(i);
        }
        else
        {
            FillWindowPixelBuffer(WIN_CARD_0 + i, PIXEL_FILL(1));
            CopyWindowToVram(WIN_CARD_0 + i, COPYWIN_FULL);
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

    for (i = 0; i < MAX_CARDS; i++)
        sCards->cardSpriteIds[i][0] = sCards->cardSpriteIds[i][1] = sCards->cardSpriteIds[i][2] = SPRITE_NONE;
    ShowCards();
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = Spire_GetRunMon(i);

        sCards->iconSpriteIds[i] = SPRITE_NONE;
        if (sCards->mode != SPIRE_CARDS_MESSAGE && sCards->mode != SPIRE_CARDS_EVOLVE && sCards->mode != SPIRE_CARDS_RELIC_LIST
         && GetMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE)
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

// --- keuzes uitvoeren -------------------------------------------------------------------------
static void PickCard(void)
{
    struct SpireCard *c = &sCards->cards[sCards->card];

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
        ShowMessage(gStringVar4, FALSE);
        break;
    case CARD_MON:
        // alleen het evolutiescherm heeft soortkaarten
        GetMonData(&RUN.mons[gSpireEvolveMon], MON_DATA_NICKNAME, gStringVar1);
        Spire_EvolveTo(gSpireEvolveMon, c->value);
        StringCopy(gStringVar2, GetSpeciesName(c->value));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} evolved into {STR_VAR_2}!"));
        ShowMessage(gStringVar4, FALSE);
        break;
    }
}

// --- invoer -----------------------------------------------------------------------------------
// Relic-lijst: LEFT/RIGHT door alle relics (pagina's van drie), A/B terug naar de kaart.
static void TurnRelicPage(s32 delta)
{
    sCards->page += delta;
    FillRelicPage();
    sCards->card = (delta > 0) ? 0 : sCards->count - 1;
    ShowCards();
    DrawHeader();
    Redraw();
}

static void HandleRelicList(void)
{
    if (JOY_NEW(DPAD_LEFT) && (sCards->card > 0 || sCards->page > 0))
    {
        PlaySE(SE_SELECT);
        if (sCards->card > 0)
        {
            sCards->card--;
            Redraw();
        }
        else
        {
            TurnRelicPage(-1);
        }
    }
    else if (JOY_NEW(DPAD_RIGHT) && (sCards->card + 1 < sCards->count || (sCards->page + 1) * MAX_CARDS < sCards->listCount))
    {
        PlaySE(SE_SELECT);
        if (sCards->card + 1 < sCards->count)
        {
            sCards->card++;
            Redraw();
        }
        else
        {
            TurnRelicPage(1);
        }
    }
    else if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        Exit();
    }
}

static void HandleCards(void)
{
    if (sCards->mode == SPIRE_CARDS_RELIC_LIST)
    {
        HandleRelicList();
        return;
    }
    if (sCards->count == 0)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON))
            Exit();
        return;
    }
    if (JOY_NEW(DPAD_LEFT) && sCards->card > 0)
    {
        PlaySE(SE_SELECT);
        sCards->card--;
        Redraw();
    }
    else if (JOY_NEW(DPAD_RIGHT) && sCards->card + 1 < sCards->count)
    {
        PlaySE(SE_SELECT);
        sCards->card++;
        Redraw();
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PickCard();
    }
    else if (JOY_NEW(B_BUTTON) && sCards->mode == SPIRE_CARDS_MOVES && Spire_HasRelic(SPIRE_RELIC_SWEET_HEART))
    {
        // Sweet Heart (relic): een move overslaan geeft blijvend max HP (zoals Singing Bowl in Slay)
        PlaySE(SE_SELECT);
        Spire_ChangeMaxHp(3);
        ShowMessage(COMPOUND_STRING("You skip the moves. Sweet Heart:\nboth Pokémon get +3% max HP."), FALSE);
    }
    else if (JOY_NEW(B_BUTTON) && (sCards->mode == SPIRE_CARDS_MOVES || sCards->mode == SPIRE_CARDS_RELICS))
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
        u32 i;

        if (MonKnowsMove(mon, sCards->teachMove))
        {
            // kent hij al: blijf kiezen (de ander, of B)
            PlaySE(SE_FAILURE);
            return;
        }
        PlaySE(SE_SELECT);
        // lege plek? die staat al geselecteerd
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
                break;
        }
        sCards->slot = (i < MAX_MON_MOVES) ? i : 0;
        sCards->state = STATE_CHOOSE_SLOT;
        Redraw();
    }
    else if (JOY_NEW(B_BUTTON))
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
        Spire_ClearSlotUpgrade(mon, sCards->slot);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetMoveName(sCards->teachMove));
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
        ShowMessage(gStringVar4, FALSE);
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
