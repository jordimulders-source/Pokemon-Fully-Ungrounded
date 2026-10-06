// Project Grounded: de rondreizende handelaar op de drijvende markt (ten noorden van Route 133, ZEE_PLAN.md).
// Elke dag een ander assortiment van vijf zeldzame items: een mint, twee evolutie-items, een "schat"
// (Bottle Cap, Rare Candy, PP Up, ...) en een zeldzame bes. Afgeleid uit het RTC-dagnummer en de trainer-id,
// dus de hele dag hetzelfde. Geen Ability Capsule/Patch (verborgen abilities zijn niet verkrijgbaar) en geen TM's.
// VAR_0x8004 schuift de dag op (0 = vandaag; voor tests).
#include "global.h"
#include "event_data.h"
#include "rtc.h"
#include "shop.h"
#include "constants/items.h"

static EWRAM_DATA u16 sStock[6] = {0};

static const u16 sMints[] =
{
    ITEM_ADAMANT_MINT, ITEM_MODEST_MINT, ITEM_JOLLY_MINT, ITEM_TIMID_MINT, ITEM_BOLD_MINT, ITEM_CALM_MINT,
    ITEM_IMPISH_MINT, ITEM_CAREFUL_MINT, ITEM_BRAVE_MINT, ITEM_QUIET_MINT, ITEM_RELAXED_MINT, ITEM_SASSY_MINT,
    ITEM_NAUGHTY_MINT, ITEM_LONELY_MINT, ITEM_MILD_MINT, ITEM_RASH_MINT, ITEM_HASTY_MINT, ITEM_NAIVE_MINT,
    ITEM_LAX_MINT, ITEM_GENTLE_MINT, ITEM_SERIOUS_MINT,
};

// alleen items waarmee in deze game echt iets evolueert
static const u16 sEvoItems[] =
{
    ITEM_ELECTIRIZER, ITEM_MAGMARIZER, ITEM_PROTECTOR, ITEM_DUBIOUS_DISC, ITEM_REAPER_CLOTH, ITEM_RAZOR_CLAW,
    ITEM_RAZOR_FANG, ITEM_PRISM_SCALE, ITEM_OVAL_STONE, ITEM_SACHET, ITEM_WHIPPED_DREAM, ITEM_UPGRADE,
    ITEM_DRAGON_SCALE, ITEM_KINGS_ROCK, ITEM_METAL_COAT, ITEM_DEEP_SEA_TOOTH, ITEM_DEEP_SEA_SCALE,
    ITEM_SWEET_APPLE, ITEM_TART_APPLE, ITEM_CRACKED_POT, ITEM_BLACK_AUGURITE, ITEM_SHINY_STONE, ITEM_DUSK_STONE,
    ITEM_DAWN_STONE, ITEM_ICE_STONE,
};

static const u16 sTreasures[] =
{
    ITEM_BOTTLE_CAP, ITEM_BOTTLE_CAP, ITEM_BOTTLE_CAP, ITEM_GOLD_BOTTLE_CAP, ITEM_RARE_CANDY, ITEM_RARE_CANDY,
    ITEM_PP_UP, ITEM_PP_UP, ITEM_PP_MAX,
};

static const u16 sBerries[] =
{
    ITEM_LIECHI_BERRY, ITEM_GANLON_BERRY, ITEM_SALAC_BERRY, ITEM_PETAYA_BERRY, ITEM_APICOT_BERRY, ITEM_LANSAT_BERRY,
    ITEM_STARF_BERRY, ITEM_MICLE_BERRY, ITEM_CUSTAP_BERRY, ITEM_JABOCA_BERRY, ITEM_ROWAP_BERRY,
};

static u32 Mix(u32 h)
{
    h ^= h >> 15;
    h *= 2246822519u;
    h ^= h >> 13;
    h *= 3266489917u;
    h ^= h >> 16;
    return h;
}

void FloatingMarket_OpenShop(void)
{
    u32 h, a, b;
    u16 tid = gSaveBlock2Ptr->playerTrainerId[0] | (gSaveBlock2Ptr->playerTrainerId[1] << 8);

    RtcCalcLocalTime();
    h = Mix((u32)(gLocalTime.days + gSpecialVar_0x8004) * 2654435761u ^ (tid * 40503u) ^ 0x5EA3A7u);
    sStock[0] = sMints[h % ARRAY_COUNT(sMints)];
    h = Mix(h);
    a = h % ARRAY_COUNT(sEvoItems);
    h = Mix(h);
    b = (a + 1 + h % (ARRAY_COUNT(sEvoItems) - 1)) % ARRAY_COUNT(sEvoItems); // altijd een ander item dan a
    sStock[1] = sEvoItems[a];
    sStock[2] = sEvoItems[b];
    h = Mix(h);
    sStock[3] = sTreasures[h % ARRAY_COUNT(sTreasures)];
    h = Mix(h);
    sStock[4] = sBerries[h % ARRAY_COUNT(sBerries)];
    sStock[5] = ITEM_NONE;
    CreatePokemartMenu(sStock);
}
