// Project Grounded: BP-winkels en Hyper Training in de Battle Frontier (Exchange Service Corner).
// Doel (Jordi, 9 okt): binnen minuten elke Pokémon competitive maken. Gewone winkelmenu's (aantal kiezen) met
// prijzen in Battle Points (CreateBpMartMenu in shop.c). VAR_0x8004 kiest de winkel (BP_SHOP_* hieronder).
// Geen Ability Patch (verborgen abilities zijn niet verkrijgbaar) en geen Mega Stones/Z-kristallen/Tera.
#include "global.h"
#include "event_data.h"
#include "pokemon.h"
#include "shop.h"
#include "constants/items.h"

enum
{
    BP_SHOP_TRAINING,   // levelen en EV's: candies, vitamines, feathers, mochi, EV-bessen, Power-items
    BP_SHOP_TUNING,     // natuur en potentieel: mints, Bottle Caps, Ability Capsule, fokken
    BP_SHOP_HELD,       // competitieve held items
    BP_SHOP_TYPE,       // type-items: Memories (Silvally), gems, weerstandsbessen
    BP_SHOP_COUNT,
};

#define TRAINING_STOCK(X)                                                                                            \
    X(ITEM_EXP_CANDY_XS, 1) X(ITEM_EXP_CANDY_S, 1) X(ITEM_EXP_CANDY_M, 1) X(ITEM_EXP_CANDY_L, 2)                       \
    X(ITEM_EXP_CANDY_XL, 3) X(ITEM_RARE_CANDY, 1)                                                                     \
    X(ITEM_HP_UP, 1) X(ITEM_PROTEIN, 1) X(ITEM_IRON, 1) X(ITEM_CALCIUM, 1) X(ITEM_ZINC, 1) X(ITEM_CARBOS, 1)          \
    X(ITEM_HEALTH_FEATHER, 1) X(ITEM_MUSCLE_FEATHER, 1) X(ITEM_RESIST_FEATHER, 1) X(ITEM_GENIUS_FEATHER, 1)           \
    X(ITEM_CLEVER_FEATHER, 1) X(ITEM_SWIFT_FEATHER, 1)                                                                \
    X(ITEM_HEALTH_MOCHI, 1) X(ITEM_MUSCLE_MOCHI, 1) X(ITEM_RESIST_MOCHI, 1) X(ITEM_GENIUS_MOCHI, 1)                   \
    X(ITEM_CLEVER_MOCHI, 1) X(ITEM_SWIFT_MOCHI, 1) X(ITEM_FRESH_START_MOCHI, 1)                                       \
    X(ITEM_POMEG_BERRY, 1) X(ITEM_KELPSY_BERRY, 1) X(ITEM_QUALOT_BERRY, 1) X(ITEM_HONDEW_BERRY, 1)                    \
    X(ITEM_GREPA_BERRY, 1) X(ITEM_TAMATO_BERRY, 1)                                                                    \
    X(ITEM_POWER_WEIGHT, 4) X(ITEM_POWER_BRACER, 4) X(ITEM_POWER_BELT, 4) X(ITEM_POWER_LENS, 4)                       \
    X(ITEM_POWER_BAND, 4) X(ITEM_POWER_ANKLET, 4) X(ITEM_MACHO_BRACE, 4)                                              \
    X(ITEM_PP_UP, 2) X(ITEM_PP_MAX, 4)

#define TUNING_STOCK(X)                                                                                              \
    X(ITEM_ADAMANT_MINT, 2) X(ITEM_MODEST_MINT, 2) X(ITEM_JOLLY_MINT, 2) X(ITEM_TIMID_MINT, 2)                        \
    X(ITEM_BOLD_MINT, 2) X(ITEM_IMPISH_MINT, 2) X(ITEM_CALM_MINT, 2) X(ITEM_CAREFUL_MINT, 2)                          \
    X(ITEM_BRAVE_MINT, 2) X(ITEM_QUIET_MINT, 2) X(ITEM_RELAXED_MINT, 2) X(ITEM_SASSY_MINT, 2)                         \
    X(ITEM_LONELY_MINT, 2) X(ITEM_NAUGHTY_MINT, 2) X(ITEM_MILD_MINT, 2) X(ITEM_RASH_MINT, 2)                          \
    X(ITEM_HASTY_MINT, 2) X(ITEM_NAIVE_MINT, 2) X(ITEM_LAX_MINT, 2) X(ITEM_GENTLE_MINT, 2) X(ITEM_SERIOUS_MINT, 2)    \
    X(ITEM_BOTTLE_CAP, 2) X(ITEM_GOLD_BOTTLE_CAP, 8) X(ITEM_ABILITY_CAPSULE, 4)                                       \
    X(ITEM_DESTINY_KNOT, 4) X(ITEM_EVERSTONE, 1)

#define HELD_STOCK(X)                                                                                                \
    X(ITEM_CHOICE_BAND, 8) X(ITEM_CHOICE_SPECS, 8) X(ITEM_CHOICE_SCARF, 8) X(ITEM_LIFE_ORB, 8)                        \
    X(ITEM_LEFTOVERS, 8) X(ITEM_BLACK_SLUDGE, 6) X(ITEM_FOCUS_SASH, 6) X(ITEM_ASSAULT_VEST, 8)                        \
    X(ITEM_ROCKY_HELMET, 6) X(ITEM_HEAVY_DUTY_BOOTS, 6) X(ITEM_EVIOLITE, 8) X(ITEM_WEAKNESS_POLICY, 6)                \
    X(ITEM_BOOSTER_ENERGY, 6) X(ITEM_LOADED_DICE, 6) X(ITEM_COVERT_CLOAK, 6) X(ITEM_CLEAR_AMULET, 6)                  \
    X(ITEM_THROAT_SPRAY, 6) X(ITEM_BLUNDER_POLICY, 6) X(ITEM_PROTECTIVE_PADS, 6) X(ITEM_WISE_GLASSES, 4)              \
    X(ITEM_MUSCLE_BAND, 4) X(ITEM_EXPERT_BELT, 6) X(ITEM_AIR_BALLOON, 4) X(ITEM_LIGHT_CLAY, 4)                        \
    X(ITEM_LUM_BERRY, 2) X(ITEM_SITRUS_BERRY, 2) X(ITEM_FLAME_ORB, 4) X(ITEM_TOXIC_ORB, 4)                            \
    X(ITEM_WHITE_HERB, 3) X(ITEM_POWER_HERB, 3) X(ITEM_MENTAL_HERB, 3) X(ITEM_MIRROR_HERB, 3)                         \
    X(ITEM_RED_CARD, 4) X(ITEM_EJECT_BUTTON, 4) X(ITEM_EJECT_PACK, 4) X(ITEM_SAFETY_GOGGLES, 4)                       \
    X(ITEM_ABILITY_SHIELD, 4) X(ITEM_PUNCHING_GLOVE, 4) X(ITEM_UTILITY_UMBRELLA, 4) X(ITEM_SHED_SHELL, 4)             \
    X(ITEM_SCOPE_LENS, 4) X(ITEM_RAZOR_CLAW, 4) X(ITEM_WIDE_LENS, 4) X(ITEM_ZOOM_LENS, 4) X(ITEM_QUICK_CLAW, 4)       \
    X(ITEM_KINGS_ROCK, 4) X(ITEM_SHELL_BELL, 4) X(ITEM_BIG_ROOT, 4) X(ITEM_GRIP_CLAW, 4) X(ITEM_BINDING_BAND, 4)      \
    X(ITEM_METRONOME, 4) X(ITEM_ROOM_SERVICE, 4) X(ITEM_ADRENALINE_ORB, 4) X(ITEM_IRON_BALL, 2)                       \
    X(ITEM_LAGGING_TAIL, 2) X(ITEM_STICKY_BARB, 2) X(ITEM_TERRAIN_EXTENDER, 4)                                        \
    X(ITEM_DAMP_ROCK, 3) X(ITEM_HEAT_ROCK, 3) X(ITEM_SMOOTH_ROCK, 3) X(ITEM_ICY_ROCK, 3)                              \
    X(ITEM_ELECTRIC_SEED, 3) X(ITEM_GRASSY_SEED, 3) X(ITEM_MISTY_SEED, 3) X(ITEM_PSYCHIC_SEED, 3)                     \
    X(ITEM_FOCUS_BAND, 3) X(ITEM_BRIGHT_POWDER, 3) X(ITEM_LAX_INCENSE, 3) X(ITEM_BERSERK_GENE, 4)

#define TYPE_STOCK(X)                                                                                                \
    X(ITEM_FIGHTING_MEMORY, 4) X(ITEM_FLYING_MEMORY, 4) X(ITEM_POISON_MEMORY, 4) X(ITEM_GROUND_MEMORY, 4)             \
    X(ITEM_ROCK_MEMORY, 4) X(ITEM_BUG_MEMORY, 4) X(ITEM_GHOST_MEMORY, 4) X(ITEM_STEEL_MEMORY, 4)                      \
    X(ITEM_FIRE_MEMORY, 4) X(ITEM_WATER_MEMORY, 4) X(ITEM_GRASS_MEMORY, 4) X(ITEM_ELECTRIC_MEMORY, 4)                 \
    X(ITEM_PSYCHIC_MEMORY, 4) X(ITEM_ICE_MEMORY, 4) X(ITEM_DRAGON_MEMORY, 4) X(ITEM_DARK_MEMORY, 4)                   \
    X(ITEM_FAIRY_MEMORY, 4)                                                                                           \
    X(ITEM_NORMAL_GEM, 2) X(ITEM_FIRE_GEM, 2) X(ITEM_WATER_GEM, 2) X(ITEM_ELECTRIC_GEM, 2) X(ITEM_GRASS_GEM, 2)       \
    X(ITEM_ICE_GEM, 2) X(ITEM_FIGHTING_GEM, 2) X(ITEM_POISON_GEM, 2) X(ITEM_GROUND_GEM, 2) X(ITEM_FLYING_GEM, 2)      \
    X(ITEM_PSYCHIC_GEM, 2) X(ITEM_BUG_GEM, 2) X(ITEM_ROCK_GEM, 2) X(ITEM_GHOST_GEM, 2) X(ITEM_DRAGON_GEM, 2)          \
    X(ITEM_DARK_GEM, 2) X(ITEM_STEEL_GEM, 2) X(ITEM_FAIRY_GEM, 2)                                                     \
    X(ITEM_CHILAN_BERRY, 1) X(ITEM_OCCA_BERRY, 1) X(ITEM_PASSHO_BERRY, 1) X(ITEM_WACAN_BERRY, 1)                      \
    X(ITEM_RINDO_BERRY, 1) X(ITEM_YACHE_BERRY, 1) X(ITEM_CHOPLE_BERRY, 1) X(ITEM_KEBIA_BERRY, 1)                      \
    X(ITEM_SHUCA_BERRY, 1) X(ITEM_COBA_BERRY, 1) X(ITEM_PAYAPA_BERRY, 1) X(ITEM_TANGA_BERRY, 1)                       \
    X(ITEM_CHARTI_BERRY, 1) X(ITEM_KASIB_BERRY, 1) X(ITEM_HABAN_BERRY, 1) X(ITEM_COLBUR_BERRY, 1)                     \
    X(ITEM_BABIRI_BERRY, 1) X(ITEM_ROSELI_BERRY, 1) X(ITEM_KEE_BERRY, 1) X(ITEM_MARANGA_BERRY, 1)                     \
    X(ITEM_ENIGMA_BERRY, 1)

#define ITEM_ENTRY(item, price) item,
#define PRICE_ENTRY(item, price) price,

static const u16 sTrainingItems[] = { TRAINING_STOCK(ITEM_ENTRY) ITEM_NONE };
static const u16 sTrainingPrices[] = { TRAINING_STOCK(PRICE_ENTRY) 0 };
static const u16 sTuningItems[] = { TUNING_STOCK(ITEM_ENTRY) ITEM_NONE };
static const u16 sTuningPrices[] = { TUNING_STOCK(PRICE_ENTRY) 0 };
static const u16 sHeldItems[] = { HELD_STOCK(ITEM_ENTRY) ITEM_NONE };
static const u16 sHeldPrices[] = { HELD_STOCK(PRICE_ENTRY) 0 };
static const u16 sTypeItems[] = { TYPE_STOCK(ITEM_ENTRY) ITEM_NONE };
static const u16 sTypePrices[] = { TYPE_STOCK(PRICE_ENTRY) 0 };

static const u16 *const sShops[BP_SHOP_COUNT][2] =
{
    [BP_SHOP_TRAINING] = {sTrainingItems, sTrainingPrices},
    [BP_SHOP_TUNING]   = {sTuningItems, sTuningPrices},
    [BP_SHOP_HELD]     = {sHeldItems, sHeldPrices},
    [BP_SHOP_TYPE]     = {sTypeItems, sTypePrices},
};

void BpShop_Open(void)
{
    u32 shop = gSpecialVar_0x8004;

    if (shop >= BP_SHOP_COUNT)
        shop = BP_SHOP_TRAINING;
    CreateBpMartMenu(sShops[shop][0], sShops[shop][1]);
}

// Hyper Training. VAR_0x8004 = partyslot, VAR_0x8005 = stat (0 HP, 1 Atk, 2 Def, 3 Speed, 4 Sp. Atk, 5 Sp. Def, 6 = alle stats).
// VAR_RESULT: TRUE als er iets te trainen viel (en het is gedaan), FALSE als die stat(s) al op 31 staan.
// Het script controleert en neemt de Bottle Cap zelf (checkitem/removeitem) vóór het aanroepen met VAR_0x8006 = 1
// (zonder VAR_0x8006 alleen controleren).
void BpShop_HyperTrain(void)
{
    struct Pokemon *mon = &gPlayerParty[gSpecialVar_0x8004];
    u32 i, first = gSpecialVar_0x8005, last = gSpecialVar_0x8005;
    bool32 any = FALSE;
    u8 yes = TRUE;

    if (gSpecialVar_0x8005 >= NUM_STATS)
    {
        first = 0;
        last = NUM_STATS - 1;
    }
    for (i = first; i <= last; i++)
    {
        if (GetMonData(mon, MON_DATA_HP_IV + i) < MAX_PER_STAT_IVS && !GetMonData(mon, MON_DATA_HYPER_TRAINED_HP + i))
        {
            any = TRUE;
            if (gSpecialVar_0x8006)
                SetMonData(mon, MON_DATA_HYPER_TRAINED_HP + i, &yes);
        }
    }
    if (any && gSpecialVar_0x8006)
        CalculateMonStats(mon);
    gSpecialVar_Result = any;
}
