// Project Grounded: Pokemarts met een assortiment dat meegroeit met de badges (zoals Gen 4+).
// Elke gewone Mart roept `badgemart <lijst>` aan: eerst het basisassortiment hieronder (afhankelijk van
// het aantal badges), daarna de stadsspecialiteiten uit <lijst> (X-items, mail, speciale ballen, ...).
#include "global.h"
#include "event_data.h"
#include "script.h"
#include "shop.h"
#include "constants/items.h"
#include "constants/flags.h"

struct BadgeMartItem
{
    u16 item;
    u8 badges;
};

static const struct BadgeMartItem sBadgeMartCore[] =
{
    {ITEM_POKE_BALL,     0},
    {ITEM_GREAT_BALL,    2},
    {ITEM_ULTRA_BALL,    5},
    {ITEM_POTION,        0},
    {ITEM_SUPER_POTION,  1},
    {ITEM_HYPER_POTION,  5},
    {ITEM_MAX_POTION,    7},
    {ITEM_FULL_RESTORE,  8},
    {ITEM_REVIVE,        3},
    {ITEM_ANTIDOTE,      0},
    {ITEM_PARALYZE_HEAL, 0},
    {ITEM_AWAKENING,     0},
    {ITEM_BURN_HEAL,     0},
    {ITEM_ICE_HEAL,      0},
    {ITEM_FULL_HEAL,     5},
    {ITEM_ESCAPE_ROPE,   0},
    {ITEM_REPEL,         0},
    {ITEM_SUPER_REPEL,   3},
    {ITEM_MAX_REPEL,     6},
};

#define BADGE_MART_MAX 64

static EWRAM_DATA u16 sBadgeMartItems[BADGE_MART_MAX] = {0};

static u32 CountBadges(void)
{
    u32 i, count = 0;
    for (i = FLAG_BADGE01_GET; i <= FLAG_BADGE08_GET; i++)
    {
        if (FlagGet(i))
            count++;
    }
    return count;
}

static bool32 InBadgeMart(u32 n, u16 item)
{
    u32 i;
    for (i = 0; i < n; i++)
    {
        if (sBadgeMartItems[i] == item)
            return TRUE;
    }
    return FALSE;
}

static void BuildBadgeMart(const u16 *extras)
{
    u32 i, n = 0, badges = CountBadges();

    for (i = 0; i < ARRAY_COUNT(sBadgeMartCore); i++)
    {
        if (badges >= sBadgeMartCore[i].badges)
            sBadgeMartItems[n++] = sBadgeMartCore[i].item;
    }
    for (i = 0; extras != NULL && extras[i] != ITEM_NONE && n < BADGE_MART_MAX - 1; i++)
    {
        if (!InBadgeMart(n, extras[i]))
            sBadgeMartItems[n++] = extras[i];
    }
    sBadgeMartItems[n] = ITEM_NONE;
}

// callnative uit de macro badgemart; het woord na de aanroep is de lijst met stadsspecialiteiten.
void ScrNative_BadgeMart(struct ScriptContext *ctx)
{
    const u16 *extras = (const u16 *)ScriptReadWord(ctx);

    BuildBadgeMart(extras);
    CreatePokemartMenu(sBadgeMartItems);
}
