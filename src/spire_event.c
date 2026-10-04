// Project Grounded: The Spire - events (zie SPIRE_DESIGN.md).
// Bovenaan het verhaal, daaronder de opties met hun effecten (groen = winst, rood = kost, blauw = gok),
// onderaan het team. Events zijn data (tools/grounded/spire/events.py -> src/data/spire_events.h); dit
// bestand voert de effecten uit. Opties met een type-eis zijn alleen te kiezen met dat type in het team.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "bg.h"
#include "gpu_regs.h"
#include "item.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "move.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
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

struct SpireEventFx
{
    u8 fx;          // enum SpireFx
    s16 arg;
};

struct SpireEventOption
{
    const u8 *name;
    const u8 *summary;      // effectregel met kleurcodes
    u8 needType;            // TYPE_NONE = geen eis
    bool8 costsGold;
    u8 chance;              // kans op fx/result; anders fxFail/resultFail
    struct SpireEventFx fx[4];
    struct SpireEventFx fxFail[4];
    const u8 *result;
    const u8 *resultFail;
};

struct SpireEventData
{
    const u8 *title;
    const u8 *story;
    u16 species;            // icoon in de kop
    u8 acts;                // bit 0 = act 1
    u8 weight;              // kans om gekozen te worden (4 = normaal, 1 = zeldzaam)
    u8 count;
    struct SpireEventOption options[3];
};

#define SPIRE_EVENT_ICON_RECRUIT 0xFFFF   // icoon = de soort van {STR_VAR_3}
#define SPIRE_EVENT_ICON_PSEUDO  0xFFFE   // idem, en {STR_VAR_3} is een willekeurige pseudo-legendary

// Pseudo-legendaries (basisvorm; ze komen binnen op het stadium van de act + 1, zie RecruitPseudo)
static const u16 sPseudos[] =
{
    SPECIES_DRATINI, SPECIES_LARVITAR, SPECIES_BAGON, SPECIES_BELDUM, SPECIES_GIBLE,
    SPECIES_DEINO, SPECIES_GOOMY, SPECIES_JANGMO_O, SPECIES_DREEPY, SPECIES_FRIGIBAX,
};
#include "data/spire_events.h"

enum
{
    WIN_HEADER,
    WIN_STORY,
    WIN_OPTIONS,
    WIN_TEAM,
    WIN_COUNT,
};

enum
{
    STATE_OPTIONS,
    STATE_MESSAGE,
    STATE_CHOOSE_MON,
    STATE_CHOOSE_SLOT,
    STATE_EXIT,
};

// wat er na het bericht nog moet gebeuren
enum
{
    PEND_NONE,
    PEND_TEACH,
    PEND_ITEM,
    PEND_REPLACE,
    PEND_REMOVE,
    PEND_ELITE,
};

#define PAL_BRICKS    12
#define PAL_FRAME     14
#define PAL_TEXT      15
#define FRAME_TILE    0x200
#define ROW_HEIGHT    13
#define SUMMARY_X     78
#define MESSAGE_SIZE  320

struct SpireEventScreen
{
    void (*onDone)(void);
    const struct SpireEventData *ev;
    u8 cursor;
    u8 state;
    u8 pending;
    u8 mon;
    u8 slot;
    u16 pendingValue;   // move, item of soort
    u16 recruit;        // soort voor {STR_VAR_3}
    u16 recruitBase;    // pseudo: basisvorm (rental) en aantal evoluties daarna
    u8 recruitEvos;
    u8 iconSpriteId;
    u8 recruitName[POKEMON_NAME_LENGTH + 1];
    u8 message[MESSAGE_SIZE];
};

static EWRAM_DATA struct SpireEventScreen *sEv = NULL;
EWRAM_DATA u8 gSpireForcedEvent = 0;

static const u32 sBrickTiles[2][8] =
{
    {0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x11111112, 0x22222222},
    {0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x11111111, 0x22222222},
};
static const u16 sBrickPal[16] = {RGB(9, 5, 12), RGB(9, 5, 12), RGB(13, 8, 18)};   // event-paars

// Indexen volgen de kleurnamen uit charmap.txt, zodat {COLOR GREEN} enz. in de effectregels werken.
static const u16 sTextPal[16] =
{
    [0] = RGB(31, 31, 31), [1] = RGB(31, 31, 31),
    [2] = RGB(8, 8, 9),    [3] = RGB(26, 26, 27),   // DARK_GRAY / LIGHT_GRAY
    [4] = RGB(29, 8, 7),   [5] = RGB(31, 24, 23),   // RED / LIGHT_RED
    [6] = RGB(5, 19, 9),   [7] = RGB(22, 29, 23),   // GREEN / LIGHT_GREEN
    [8] = RGB(5, 15, 29),  [9] = RGB(23, 27, 31),   // BLUE / LIGHT_BLUE
    [10] = RGB(19, 19, 20),                          // grijs (niet te kiezen)
    [11] = RGB(25, 17, 1), [12] = RGB(31, 27, 17),  // goud
    [13] = RGB(15, 9, 22), [14] = RGB(26, 22, 30),  // paars
};
static const u8 sColor_Dark[]   = {0, 2, 3};
static const u8 sColor_Gray[]   = {0, 10, 3};
static const u8 sColor_Red[]    = {0, 4, 5};
static const u8 sColor_Green[]  = {0, 6, 7};
static const u8 sColor_Blue[]   = {0, 8, 9};
static const u8 sColor_Gold[]   = {0, 11, 12};
static const u8 sColor_Purple[] = {0, 13, 14};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_HEADER]  = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1,  .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    [WIN_STORY]   = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 4,  .width = 28, .height = 6, .paletteNum = PAL_TEXT, .baseBlock = 0x039},
    [WIN_OPTIONS] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 11, .width = 28, .height = 5, .paletteNum = PAL_TEXT, .baseBlock = 0x0E1},
    [WIN_TEAM]    = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 17, .width = 28, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 0x171},
    DUMMY_WIN_TEMPLATE,
};

static void Task_SpireEvent(u8 taskId);

// --- hulpjes ----------------------------------------------------------------------------------
static void PrintText(u32 win, u32 font, u32 x, u32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(win, font, x, y, color, TEXT_SKIP_DRAW, str);
}

static void PrintRight(u32 win, u32 font, u32 right, u32 y, const u8 *color, const u8 *str)
{
    PrintText(win, font, right - GetStringWidth(font, str, 0), y, color, str);
}

// Tekst met {STR_VAR_3} = de soort van dit event
static void Expand(u8 *dst, const u8 *src)
{
    StringCopy(gStringVar3, sEv->recruitName);
    StringExpandPlaceholders(dst, src);
}

// Regel achter het bericht plakken (met {STR_VAR_1}/{STR_VAR_2} al ingevuld door de aanroeper)
static void AppendLine(const u8 *fmt)
{
    u8 *end = sEv->message + StringLength(sEv->message);

    StringExpandPlaceholders(gStringVar4, fmt);
    if (end + StringLength(gStringVar4) + 2 >= sEv->message + MESSAGE_SIZE)
        return;
    if (end != sEv->message)
        *end++ = CHAR_NEWLINE;
    StringCopy(end, gStringVar4);
}

static bool32 MonKnowsMove(struct Pokemon *mon, u32 move)
{
    u32 i;

    for (i = 0; i < MAX_MON_MOVES; i++)
        if (GetMonData(mon, MON_DATA_MOVE1 + i) == move)
            return TRUE;
    return FALSE;
}

static bool32 TeamHasType(u32 type)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        u16 species = GetMonData(&RUN.mons[i], MON_DATA_SPECIES);

        if (GetSpeciesType(species, 0) == type || GetSpeciesType(species, 1) == type)
            return TRUE;
    }
    return FALSE;
}

static u32 GoldCost(const struct SpireEventOption *o)
{
    u32 i, cost = 0;

    for (i = 0; i < ARRAY_COUNT(o->fx); i++)
        if (o->fx[i].fx == SPIRE_FX_GOLD && o->fx[i].arg < 0)
            cost += -o->fx[i].arg;
    return cost;
}

static bool32 HasFx(const struct SpireEventOption *o, u32 fx)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(o->fx); i++)
        if (o->fx[i].fx == fx)
            return TRUE;
    return FALSE;
}

// Waarom een optie niet kan (NULL = kan wel)
static const u8 *sText_NeedRelic = COMPOUND_STRING("Needs a relic");
static const u8 *sText_NeedItem = COMPOUND_STRING("Needs a held item");
static const u8 *LockReason(const struct SpireEventOption *o)
{
    if (o->needType != TYPE_NONE && !TeamHasType(o->needType))
    {
        StringCopy(gStringVar1, gTypesInfo[o->needType].name);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Needs a {STR_VAR_1} type"));
        return gStringVar4;
    }
    if (HasFx(o, SPIRE_FX_LOSE_RELIC) && RUN.relics == 0)
        return sText_NeedRelic;
    if (HasFx(o, SPIRE_FX_LOSE_ITEMS) && GetMonData(&RUN.mons[0], MON_DATA_HELD_ITEM) == ITEM_NONE
                                      && GetMonData(&RUN.mons[1], MON_DATA_HELD_ITEM) == ITEM_NONE)
        return sText_NeedItem;
    return NULL;
}

static bool32 CanAfford(const struct SpireEventOption *o)
{
    return RUN.gold >= GoldCost(o);
}

// --- tekenen ----------------------------------------------------------------------------------
static void DrawHeader(void)
{
    u8 buf[16];

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    PrintText(WIN_HEADER, FONT_NORMAL, 4, 1, sColor_Purple, sEv->ev->title);
    ConvertIntToDecimalStringN(buf, RUN.gold, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(buf, COMPOUND_STRING("¥"));
    PrintRight(WIN_HEADER, FONT_NORMAL, 218, 1, sColor_Gold, buf);
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawStory(void)
{
    FillWindowPixelBuffer(WIN_STORY, PIXEL_FILL(1));
    switch (sEv->state)
    {
    case STATE_OPTIONS:
        Expand(gStringVar4, sEv->ev->story);
        PrintText(WIN_STORY, FONT_SMALL_NARROW, 2, 0, sColor_Dark, gStringVar4);
        break;
    case STATE_MESSAGE:
        PrintText(WIN_STORY, FONT_SMALL_NARROW, 2, 0, sColor_Dark, sEv->message);
        break;
    case STATE_CHOOSE_MON:
        switch (sEv->pending)
        {
        case PEND_TEACH:
            StringCopy(gStringVar1, GetMoveName(sEv->pendingValue));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Teach {STR_VAR_1} to whom?\nB: leave it."));
            break;
        case PEND_ITEM:
            StringCopy(gStringVar1, GetItemName(sEv->pendingValue));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Who holds the {STR_VAR_1}?\nThe old item stays behind. B: leave it."));
            break;
        case PEND_REPLACE:
            StringCopy(gStringVar1, GetSpeciesName(sEv->pendingValue));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} wants to join. Who makes room?\nThe newcomer arrives with full HP. B: say no."));
            break;
        default:
            StringCopy(gStringVar4, COMPOUND_STRING("Who lets go of a move?\nB: keep everything."));
            break;
        }
        PrintText(WIN_STORY, FONT_SMALL_NARROW, 2, 0, sColor_Blue, gStringVar4);
        break;
    case STATE_CHOOSE_SLOT:
        GetMonData(&RUN.mons[sEv->mon], MON_DATA_NICKNAME, gStringVar1);
        if (sEv->pending == PEND_TEACH)
        {
            StringCopy(gStringVar2, GetMoveName(sEv->pendingValue));
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Which move makes room for {STR_VAR_2}?\nB: back."));
        }
        else
        {
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Which move does {STR_VAR_1} forget?\nB: back."));
        }
        PrintText(WIN_STORY, FONT_SMALL_NARROW, 2, 0, sColor_Blue, gStringVar4);
        break;
    }
    CopyWindowToVram(WIN_STORY, COPYWIN_FULL);
}

static void DrawOptions(void)
{
    u32 i;

    FillWindowPixelBuffer(WIN_OPTIONS, PIXEL_FILL(1));
    switch (sEv->state)
    {
    case STATE_OPTIONS:
        for (i = 0; i < sEv->ev->count; i++)
        {
            const struct SpireEventOption *o = &sEv->ev->options[i];
            const u8 *lock = LockReason(o);
            u32 y = 1 + i * ROW_HEIGHT;

            if (i == sEv->cursor)
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 2, y, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 10, y,
                      (lock != NULL || !CanAfford(o)) ? sColor_Gray : (o->needType != TYPE_NONE) ? sColor_Blue : sColor_Dark, o->name);
            if (lock != NULL)
            {
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, SUMMARY_X, y, sColor_Gray, lock);
            }
            else
            {
                Expand(gStringVar4, o->summary);
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, SUMMARY_X, y, sColor_Dark, gStringVar4);
            }
        }
        break;
    case STATE_MESSAGE:
        PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 2, 1, sColor_Red, COMPOUND_STRING("▶"));
        PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 10, 1, sColor_Dark,
                  sEv->pending == PEND_ELITE ? COMPOUND_STRING("Fight!") : COMPOUND_STRING("Continue"));
        break;
    case STATE_CHOOSE_MON:
        for (i = 0; i < 2; i++)
        {
            struct Pokemon *mon = &RUN.mons[i];
            u32 y = 1 + i * ROW_HEIGHT;
            u16 held = GetMonData(mon, MON_DATA_HELD_ITEM);

            if (i == sEv->mon)
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 2, y, sColor_Red, COMPOUND_STRING("▶"));
            GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
            PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, 10, y, sColor_Dark, gStringVar1);
            if (sEv->pending == PEND_ITEM)
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, SUMMARY_X, y, sColor_Gray, held != ITEM_NONE ? GetItemName(held) : COMPOUND_STRING("no item"));
            else if (sEv->pending == PEND_TEACH && MonKnowsMove(mon, sEv->pendingValue))
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, SUMMARY_X, y, sColor_Gray, COMPOUND_STRING("already knows it"));
            else if (sEv->pending == PEND_REPLACE)
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, SUMMARY_X, y, sColor_Gray, GetSpeciesName(GetMonData(mon, MON_DATA_SPECIES)));
        }
        break;
    case STATE_CHOOSE_SLOT:
    {
        struct Pokemon *mon = &RUN.mons[sEv->mon];

        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            u32 m = GetMonData(mon, MON_DATA_MOVE1 + i), x = (i % 2) * 112, y = 1 + (i / 2) * ROW_HEIGHT;

            if (i == sEv->slot)
                PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, x + 2, y, sColor_Red, COMPOUND_STRING("▶"));
            PrintText(WIN_OPTIONS, FONT_SMALL_NARROW, x + 10, y, m ? sColor_Dark : sColor_Gray, m ? GetMoveName(m) : COMPOUND_STRING("-"));
        }
        break;
    }
    }
    CopyWindowToVram(WIN_OPTIONS, COPYWIN_FULL);
}

static void DrawTeam(void)
{
    u32 i;

    FillWindowPixelBuffer(WIN_TEAM, PIXEL_FILL(1));
    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 x = i * 112, hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);
        u32 pct = maxHp ? (hp * 100 + maxHp - 1) / maxHp : 0, fill = maxHp ? hp * 60 / maxHp : 0;
        u8 buf[8];

        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        PrintText(WIN_TEAM, FONT_SMALL_NARROW, x + 2, 0, sColor_Dark, gStringVar1);
        ConvertIntToDecimalStringN(buf, pct, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(buf, COMPOUND_STRING("%"));
        PrintRight(WIN_TEAM, FONT_SMALL_NARROW, x + 104, 0, pct > 50 ? sColor_Green : pct > 20 ? sColor_Gold : sColor_Red, buf);
        FillWindowPixelRect(WIN_TEAM, PIXEL_FILL(3), x + 2, 12, 60, 3);
        if (fill)
            FillWindowPixelRect(WIN_TEAM, PIXEL_FILL(pct > 50 ? 6 : pct > 20 ? 11 : 4), x + 2, 12, fill, 3);
    }
    CopyWindowToVram(WIN_TEAM, COPYWIN_FULL);
}

static void Redraw(void)
{
    DrawHeader();
    DrawStory();
    DrawOptions();
    DrawTeam();
}

// --- effecten ---------------------------------------------------------------------------------
static void LoseHp(struct Pokemon *mon, u32 percent)
{
    u32 hp = GetMonData(mon, MON_DATA_HP), loss = GetMonData(mon, MON_DATA_MAX_HP) * percent / 100;

    if (hp == 0)
        return;
    hp = (hp > loss) ? hp - loss : 1;
    SetMonData(mon, MON_DATA_HP, &hp);
}

// Blijvende max-HP-verandering in procentpunten van de gewone max HP (voor beide).
static void ChangeMaxHp(s32 delta)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP), newMax;

        RUN.hpBonus[i] = max(-60, min(60, RUN.hpBonus[i] + delta));
        CalculateMonStats(mon);
        Spire_ScaleMonHp(mon, Spire_PlayerHpPercent(i));
        newMax = GetMonData(mon, MON_DATA_MAX_HP);
        if (hp != 0)
            hp = (delta > 0) ? min(newMax, hp + (newMax - min(newMax, maxHp))) : max(1, min(hp, newMax));
        SetMonData(mon, MON_DATA_HP, &hp);
    }
}

static u32 CountMoves(struct Pokemon *mon)
{
    u32 slot, n = 0;

    for (slot = 0; slot < MAX_MON_MOVES; slot++)
        if (GetMonData(mon, MON_DATA_MOVE1 + slot) != MOVE_NONE)
            n++;
    return n;
}

// Een willekeurige move van een willekeurige Pokémon vergeten (laat er altijd één over).
static void ForgetRandomMove(void)
{
    u32 i = Random() & 1, slot, tries;
    struct Pokemon *mon;

    if (CountMoves(&RUN.mons[i]) <= 1)
        i ^= 1;
    mon = &RUN.mons[i];
    if (CountMoves(mon) <= 1)
        return;
    for (tries = 0; tries < 30; tries++)
    {
        slot = Random() % MAX_MON_MOVES;
        if (GetMonData(mon, MON_DATA_MOVE1 + slot) != MOVE_NONE)
            break;
    }
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringCopy(gStringVar2, GetMoveName(GetMonData(mon, MON_DATA_MOVE1 + slot)));
    SetMonMoveSlot(mon, MOVE_NONE, slot);
    Spire_ClearSlotUpgrade(mon, slot);
    AppendLine(COMPOUND_STRING("{STR_VAR_1} forgot {STR_VAR_2}."));
}

static void UpgradeRandomMoves(u32 count)
{
    u8 line[64];
    u8 *p = line;
    u32 k, tries;

    *p = EOS;
    for (k = 0; k < count; k++)
    {
        for (tries = 0; tries < 40; tries++)
        {
            u32 i = Random() & 1, slot = Random() % MAX_MON_MOVES;
            struct Pokemon *mon = &RUN.mons[i];

            if (GetMonData(mon, MON_DATA_MOVE1 + slot) == MOVE_NONE || Spire_IsSlotUpgraded(mon, slot))
                continue;
            Spire_UpgradeSlot(mon, slot);
            p = StringCopy(p, GetMoveName(GetMonData(mon, MON_DATA_MOVE1 + slot)));
            p = StringCopy(p, COMPOUND_STRING("+! "));
            break;
        }
    }
    AppendLine(line[0] != EOS ? line : COMPOUND_STRING("Nothing left to upgrade. Impressive."));
}

static void GiveRelic(void)
{
    u32 relic = Spire_RandomNewRelic(Random() % 8);

    if (relic < SPIRE_RELIC_COUNT)
    {
        Spire_AddRelic(relic);
        StringCopy(gStringVar1, gSpireRelics[relic].name);
        AppendLine(COMPOUND_STRING("You got the {STR_VAR_1}!"));
    }
    else
    {
        RUN.gold = min(9999, RUN.gold + 60);
        AppendLine(COMPOUND_STRING("You have every relic already. +60¥ instead."));
    }
}

static void LoseRelic(void)
{
    u32 i, n = 0, pick;

    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
        if (RUN.relics & (1u << i))
            n++;
    if (n == 0)
        return;
    pick = Random() % n;
    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
    {
        if ((RUN.relics & (1u << i)) && pick-- == 0)
        {
            RUN.relics &= ~(1u << i);
            StringCopy(gStringVar1, gSpireRelics[i].name);
            AppendLine(COMPOUND_STRING("The {STR_VAR_1} is gone."));
            return;
        }
    }
}

static void EvolveRandom(void)
{
    u32 i = Random() & 1, n;
    u16 targets[3];

    if (!Spire_CanEvolve(i))
        i ^= 1;
    n = Spire_GetEvolutions(GetMonData(&RUN.mons[i], MON_DATA_SPECIES), targets);
    if (n == 0)
    {
        RUN.gold = min(9999, RUN.gold + 60);
        AppendLine(COMPOUND_STRING("Nobody can evolve any further. +60¥ instead."));
        return;
    }
    GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, gStringVar1);
    Spire_EvolveTo(i, targets[Random() % n]);
    StringCopy(gStringVar2, GetSpeciesName(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)));
    AppendLine(COMPOUND_STRING("{STR_VAR_1} evolved into {STR_VAR_2}!"));
}

// Wonder Trade: een willekeurige Pokémon wordt een willekeurige rental, geëvolueerd tot de huidige act.
static void WonderTrade(void)
{
    u32 slot = Random() & 1, a, n;
    u16 targets[3];

    GetMonData(&RUN.mons[slot], MON_DATA_NICKNAME, gStringVar1);
    Spire_SetRental(slot, Spire_RandomRental(Random()));
    for (a = 1; a < RUN.act; a++)
    {
        n = Spire_GetEvolutions(GetMonData(&RUN.mons[slot], MON_DATA_SPECIES), targets);
        if (n)
            Spire_EvolveTo(slot, targets[Random() % n]);
    }
    StringCopy(gStringVar2, GetSpeciesName(GetMonData(&RUN.mons[slot], MON_DATA_SPECIES)));
    AppendLine(COMPOUND_STRING("{STR_VAR_1} went in. {STR_VAR_2} came out!"));
}

static void SpinWheel(void)
{
    switch (Random() % 6)
    {
    case 0:
        RUN.gold = min(9999, RUN.gold + 100);
        AppendLine(COMPOUND_STRING("Jackpot! +100¥. Spinda falls over."));
        break;
    case 1:
        AppendLine(COMPOUND_STRING("The wheel stops on 'relic'. Spinda is jealous."));
        GiveRelic();
        break;
    case 2:
        Spire_HealRun(100);
        Spire_RestorePP();
        AppendLine(COMPOUND_STRING("Full heal! Spinda is very proud of you."));
        break;
    case 3:
        LoseHp(&RUN.mons[0], 15);
        LoseHp(&RUN.mons[1], 15);
        AppendLine(COMPOUND_STRING("Spinda slaps everyone. -15% HP.\nIt was an accident. Probably."));
        break;
    case 4:
        AppendLine(COMPOUND_STRING("The wheel stops on 'upgrade'. Huh."));
        UpgradeRandomMoves(1);
        break;
    default:
        AppendLine(COMPOUND_STRING("The wheel stops on 'forget'. Sorry."));
        ForgetRandomMove();
        break;
    }
}

static void ApplyFx(const struct SpireEventFx *f)
{
    u32 i;

    switch (f->fx)
    {
    case SPIRE_FX_GOLD:
        if (f->arg > 0)
            RUN.gold = min(9999, RUN.gold + f->arg);
        else
            RUN.gold -= min(RUN.gold, (u32)-f->arg);
        break;
    case SPIRE_FX_GOLD_PCT:
        if (f->arg > 0)
            RUN.gold = min(9999, RUN.gold + RUN.gold * f->arg / 100);
        else
            RUN.gold -= RUN.gold * (-f->arg) / 100;
        break;
    case SPIRE_FX_HEAL:
        if (f->arg > 0)
        {
            Spire_HealRun(f->arg);
        }
        else
        {
            LoseHp(&RUN.mons[0], -f->arg);
            LoseHp(&RUN.mons[1], -f->arg);
        }
        break;
    case SPIRE_FX_HURT_ONE:
        LoseHp(&RUN.mons[Random() & 1], f->arg);
        break;
    case SPIRE_FX_MAXHP:
        ChangeMaxHp(f->arg);
        break;
    case SPIRE_FX_BP:
        RUN.bp += f->arg;
        break;
    case SPIRE_FX_RELIC:
        GiveRelic();
        break;
    case SPIRE_FX_LOSE_RELIC:
        LoseRelic();
        break;
    case SPIRE_FX_ITEM:
        sEv->pending = PEND_ITEM;
        sEv->pendingValue = Spire_RandomHeldItem(f->arg, Random());
        break;
    case SPIRE_FX_GIVE:
        sEv->pending = PEND_ITEM;
        sEv->pendingValue = f->arg;
        break;
    case SPIRE_FX_LOSE_ITEMS:
        for (i = 0; i < 2; i++)
        {
            u16 none = ITEM_NONE;
            SetMonData(&RUN.mons[i], MON_DATA_HELD_ITEM, &none);
        }
        break;
    case SPIRE_FX_TEACH:
        sEv->pending = PEND_TEACH;
        sEv->pendingValue = Spire_RandomMove(f->arg, Random());
        break;
    case SPIRE_FX_TEACH_TYPE:
        sEv->pending = PEND_TEACH;
        sEv->pendingValue = Spire_RandomMoveOfType(f->arg, GetSpeciesType(GetMonData(&RUN.mons[Random() & 1], MON_DATA_SPECIES), Random() & 1), Random());
        break;
    case SPIRE_FX_TEACH_MOVE:
        sEv->pending = PEND_TEACH;
        sEv->pendingValue = f->arg;
        break;
    case SPIRE_FX_UPGRADE:
        UpgradeRandomMoves(f->arg);
        break;
    case SPIRE_FX_FORGET:
        for (i = 0; i < (u32)f->arg; i++)
            ForgetRandomMove();
        break;
    case SPIRE_FX_REMOVE:
        sEv->pending = PEND_REMOVE;
        break;
    case SPIRE_FX_FULLHEAL:
        Spire_HealRun(100);
        Spire_RestorePP();
        break;
    case SPIRE_FX_PP:
        Spire_RestorePP();
        break;
    case SPIRE_FX_SLEEP:
    {
        u32 mask = 0;

        for (i = 0; i < 2; i++)
            if (Random() % 100 < (u32)f->arg)
                mask |= 1 << i;
        RUN.fungalMask |= mask;
        if (mask == 3)
        {
            AppendLine(COMPOUND_STRING("Both will start the next battle asleep."));
        }
        else if (mask)
        {
            GetMonData(&RUN.mons[mask == 2], MON_DATA_NICKNAME, gStringVar1);
            AppendLine(COMPOUND_STRING("{STR_VAR_1} will start the next battle asleep."));
        }
        break;
    }
    case SPIRE_FX_TOXIC:
        RUN.toxicFights = max(RUN.toxicFights, (u8)f->arg);
        break;
    case SPIRE_FX_ELITE:
        sEv->pending = PEND_ELITE;
        break;
    case SPIRE_FX_RECRUIT:
        sEv->pending = PEND_REPLACE;
        sEv->pendingValue = sEv->recruit;
        break;
    case SPIRE_FX_RECRUIT_SPECIES:
        sEv->pending = PEND_REPLACE;
        sEv->pendingValue = f->arg;
        break;
    case SPIRE_FX_DITTO:
        sEv->pending = PEND_REPLACE;
        sEv->pendingValue = SPECIES_DITTO;
        break;
    case SPIRE_FX_RECRUIT_PSEUDO:
        sEv->pending = PEND_REPLACE;
        sEv->pendingValue = sEv->recruit;
        break;
    case SPIRE_FX_WONDER:
        WonderTrade();
        break;
    case SPIRE_FX_EVOLVE:
        EvolveRandom();
        break;
    case SPIRE_FX_WHEEL:
        SpinWheel();
        break;
    }
}

static void PickOption(void)
{
    const struct SpireEventOption *o = &sEv->ev->options[sEv->cursor];
    const struct SpireEventFx *fx = o->fx;
    const u8 *text = o->result;
    u32 i;

    if (LockReason(o) != NULL || !CanAfford(o))
    {
        PlaySE(SE_FAILURE);
        return;
    }
    PlaySE(SE_SELECT);
    if (o->chance < 100 && Random() % 100 >= o->chance)
    {
        fx = o->fxFail;
        text = o->resultFail;
    }
    sEv->message[0] = EOS;
    if (text != NULL)
        Expand(sEv->message, text);
    sEv->pending = PEND_NONE;
    for (i = 0; i < ARRAY_COUNT(o->fx); i++)
        ApplyFx(&fx[i]);
    sEv->state = STATE_MESSAGE;
    Redraw();
}

// --- keuzes na het bericht ----------------------------------------------------------------------
static void ShowMessage(const u8 *text)
{
    StringExpandPlaceholders(sEv->message, text);
    sEv->pending = PEND_NONE;
    sEv->state = STATE_MESSAGE;
    Redraw();
}

static void FinishPending(void)
{
    struct Pokemon *mon = &RUN.mons[sEv->mon];

    switch (sEv->pending)
    {
    case PEND_ITEM:
    {
        u16 old = GetMonData(mon, MON_DATA_HELD_ITEM);

        SetMonData(mon, MON_DATA_HELD_ITEM, &sEv->pendingValue);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetItemName(sEv->pendingValue));
        if (old != ITEM_NONE)
        {
            StringCopy(gStringVar3, GetItemName(old));
            ShowMessage(COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}.\nThe {STR_VAR_3} stays behind."));
        }
        else
        {
            ShowMessage(COMPOUND_STRING("{STR_VAR_1} now holds the {STR_VAR_2}."));
        }
        break;
    }
    case PEND_REPLACE:
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        if (sEv->pendingValue == SPECIES_DITTO)
        {
            Spire_SetSpecialDitto(sEv->mon);
        }
        else if (sEv->recruitBase != SPECIES_NONE && sEv->pendingValue == sEv->recruit)
        {
            // pseudo: als rental (startmoves van de basisvorm), dan evolueren
            u32 k;
            u16 targets[3];

            Spire_SetRental(sEv->mon, sEv->recruitBase);
            for (k = 0; k < sEv->recruitEvos; k++)
                if (Spire_GetEvolutions(GetMonData(&RUN.mons[sEv->mon], MON_DATA_SPECIES), targets))
                    Spire_EvolveTo(sEv->mon, targets[0]);
        }
        else
        {
            Spire_SetRental(sEv->mon, sEv->pendingValue);
        }
        StringCopy(gStringVar2, GetSpeciesName(sEv->pendingValue));
        ShowMessage(COMPOUND_STRING("{STR_VAR_1} goes home.\n{STR_VAR_2} joins your team!"));
        break;
    }
}

static void StartPending(void)
{
    sEv->mon = 0;
    switch (sEv->pending)
    {
    case PEND_ELITE:
        sEv->onDone = Spire_StartEventFight;
        // fallthrough
    case PEND_NONE:
        sEv->state = STATE_EXIT;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        return;
    }
    sEv->state = STATE_CHOOSE_MON;
    Redraw();
}

static void ChooseMon(void)
{
    struct Pokemon *mon = &RUN.mons[sEv->mon];
    u32 i;

    switch (sEv->pending)
    {
    case PEND_TEACH:
        if (MonKnowsMove(mon, sEv->pendingValue))
        {
            PlaySE(SE_FAILURE);
            return;
        }
        PlaySE(SE_SELECT);
        for (i = 0; i < MAX_MON_MOVES; i++)
            if (GetMonData(mon, MON_DATA_MOVE1 + i) == MOVE_NONE)
                break;
        sEv->slot = (i < MAX_MON_MOVES) ? i : 0;
        sEv->state = STATE_CHOOSE_SLOT;
        Redraw();
        break;
    case PEND_REMOVE:
        if (CountMoves(mon) <= 1)
        {
            PlaySE(SE_FAILURE);
            return;
        }
        PlaySE(SE_SELECT);
        sEv->slot = 0;
        sEv->state = STATE_CHOOSE_SLOT;
        Redraw();
        break;
    default:
        PlaySE(SE_SELECT);
        FinishPending();
        break;
    }
}

static void ChooseSlot(void)
{
    struct Pokemon *mon = &RUN.mons[sEv->mon];
    u16 old = GetMonData(mon, MON_DATA_MOVE1 + sEv->slot);

    if (sEv->pending == PEND_REMOVE)
    {
        if (old == MOVE_NONE)
        {
            PlaySE(SE_FAILURE);
            return;
        }
        PlaySE(SE_SELECT);
        SetMonMoveSlot(mon, MOVE_NONE, sEv->slot);
        Spire_ClearSlotUpgrade(mon, sEv->slot);
        GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
        StringCopy(gStringVar2, GetMoveName(old));
        ShowMessage(COMPOUND_STRING("{STR_VAR_1} forgot {STR_VAR_2}.\nIt does not miss it."));
        return;
    }
    PlaySE(SE_RG_BALL_CLICK);
    SetMonMoveSlot(mon, sEv->pendingValue, sEv->slot);
    Spire_ClearSlotUpgrade(mon, sEv->slot);
    GetMonData(mon, MON_DATA_NICKNAME, gStringVar1);
    StringCopy(gStringVar2, GetMoveName(sEv->pendingValue));
    ShowMessage(COMPOUND_STRING("{STR_VAR_1} learned {STR_VAR_2}!"));
}

// --- scherm -------------------------------------------------------------------------------------
static bool32 EventSeen(u32 i)
{
    return (i < 32) ? (RUN.eventsSeen >> i) & 1 : (RUN.eventsSeen2 >> (i - 32)) & 1;
}

// Gewogen loting onder de events van deze act die deze run nog niet geweest zijn.
static u32 PickEvent(void)
{
    u32 i, total = 0, pick, round, act = 1u << (RUN.act - 1);

    if (gSpireForcedEvent != 0 && gSpireForcedEvent <= ARRAY_COUNT(sSpireEvents))
    {
        i = gSpireForcedEvent - 1;
        gSpireForcedEvent = 0;
        return i;
    }
    for (round = 0; round < 2 && total == 0; round++)
    {
        if (round == 1)
        {
            RUN.eventsSeen = 0;
            RUN.eventsSeen2 = 0;
        }
        for (i = 0; i < ARRAY_COUNT(sSpireEvents); i++)
            if ((sSpireEvents[i].acts & act) && !EventSeen(i))
                total += sSpireEvents[i].weight;
    }
    pick = Random() % (total ? total : 1);
    for (i = 0; i < ARRAY_COUNT(sSpireEvents); i++)
    {
        if (!(sSpireEvents[i].acts & act) || EventSeen(i))
            continue;
        if (pick < sSpireEvents[i].weight)
            break;
        pick -= sSpireEvents[i].weight;
    }
    if (i >= ARRAY_COUNT(sSpireEvents))
        i = 0;
    if (i < 32)
        RUN.eventsSeen |= 1u << i;
    else
        RUN.eventsSeen2 |= 1u << (i - 32);
    return i;
}

// Pseudo-legendary: willekeurige lijn, één stadium verder dan de act (act 1 = middelste vorm).
static void RollPseudo(void)
{
    u32 k;
    u16 species, targets[3];

    sEv->recruitBase = sPseudos[Random() % ARRAY_COUNT(sPseudos)];
    sEv->recruitEvos = min(2, RUN.act);
    species = sEv->recruitBase;
    for (k = 0; k < sEv->recruitEvos; k++)
        if (Spire_GetEvolutions(species, targets))
            species = targets[0];
    sEv->recruit = species;
}

static void VBlankCB_SpireEvent(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_SpireEvent(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

void Spire_OpenEvent(void (*onDone)(void))
{
    u16 *tilemap;
    u32 i, x, y;

    sEv = AllocZeroed(sizeof(*sEv));
    sEv->onDone = onDone;
    sEv->ev = &sSpireEvents[PickEvent()];
    if (sEv->ev->species == SPIRE_EVENT_ICON_PSEUDO)
        RollPseudo();
    else
        sEv->recruit = Spire_RandomEventRental(Random());
    StringCopy(sEv->recruitName, GetSpeciesName(sEv->recruit));
    sEv->iconSpriteId = SPRITE_NONE;

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

    // de Pokémon van het event, rechts naast de titel
    LoadMonIconPalettes();
    if (sEv->ev->species != SPECIES_NONE)
    {
        u16 species = (sEv->ev->species >= SPIRE_EVENT_ICON_PSEUDO) ? sEv->recruit : sEv->ev->species;

        sEv->iconSpriteId = CreateMonIconNoPersonality(species, SpriteCB_MonIcon,
                                                       8 + 4 + GetStringWidth(FONT_NORMAL, sEv->ev->title, 0) + 20, 8 + 6, 0);
        gSprites[sEv->iconSpriteId].oam.priority = 0;
    }

    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_SpireEvent);
    SetMainCallback2(CB2_SpireEvent);
    CreateTask(Task_SpireEvent, 0);
}

static void CloseEvent(void)
{
    void (*onDone)(void) = sEv->onDone;

    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sEv);
    sEv = NULL;
    onDone();
}

static void Task_SpireEvent(u8 taskId)
{
    if (gPaletteFade.active)
        return;

    switch (sEv->state)
    {
    case STATE_OPTIONS:
        if (JOY_NEW(DPAD_UP) && sEv->cursor > 0)
        {
            PlaySE(SE_SELECT);
            sEv->cursor--;
            DrawOptions();
        }
        else if (JOY_NEW(DPAD_DOWN) && sEv->cursor + 1 < sEv->ev->count)
        {
            PlaySE(SE_SELECT);
            sEv->cursor++;
            DrawOptions();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            PickOption();
        }
        break;
    case STATE_MESSAGE:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_SELECT);
            StartPending();
        }
        break;
    case STATE_CHOOSE_MON:
        if (JOY_NEW(DPAD_UP | DPAD_DOWN | DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sEv->mon ^= 1;
            DrawOptions();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            ChooseMon();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            ShowMessage(sEv->pending == PEND_REPLACE ? COMPOUND_STRING("You say no. It leaves, offended.")
                                                     : COMPOUND_STRING("You leave it behind. Someone else will be happy."));
        }
        break;
    case STATE_CHOOSE_SLOT:
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sEv->slot ^= 1;
            DrawOptions();
        }
        else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
        {
            PlaySE(SE_SELECT);
            sEv->slot ^= 2;
            DrawOptions();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            ChooseSlot();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sEv->state = STATE_CHOOSE_MON;
            Redraw();
        }
        break;
    case STATE_EXIT:
        DestroyTask(taskId);
        CloseEvent();
        break;
    }
}
