// Gegenereerd door tools/grounded/spire/relics.py; niet met de hand bewerken.
#ifndef GUARD_SPIRE_RELICS_H
#define GUARD_SPIRE_RELICS_H

// Relics = trainerspullen voor het hele team (vasthouditems zijn iets anders: één per Pokémon, zie de winkel).
enum SpireRelic
{
    SPIRE_RELIC_BERRY_POUCH, // common: Heal 10% more HP after every battle.
    SPIRE_RELIC_AMULET_COIN, // common: Earn 50% more money in every battle.
    SPIRE_RELIC_GUARD_SPEC, // common: DEFEND gives 30% more Block.
    SPIRE_RELIC_DIRE_HIT, // uncommon: Your Pokémon land critical hits more often.
    SPIRE_RELIC_MUSCLE_BAND, // uncommon: Your Pokémon deal 10% more damage.
    SPIRE_RELIC_WIDE_LENS, // uncommon: Your moves that hit both foes lose no power.
    SPIRE_RELIC_SOOTHE_BELL, // common: Resting at camp heals 30% more HP.
    SPIRE_RELIC_SACRED_ASH, // rare: Fainted Pokémon come back with 30% HP, not 1 HP.
    SPIRE_RELIC_X_SPEED, // common: Both your Pokémon start every battle with +1 Speed.
    SPIRE_RELIC_BLACK_FLUTE, // common: Foes start every battle with -1 Speed. It is that out of tune.
    SPIRE_RELIC_RING_TARGET, // common: Elites start with 20% less HP. They feel watched.
    SPIRE_RELIC_QUICK_BALL, // common: Foes in normal battles start with 15% less HP.
    SPIRE_RELIC_IRON_PLATE, // common: First turn: both your Pokémon start with Block, as if both DEFENDED.
    SPIRE_RELIC_ADRENALINE_ORB, // common: First turn of every battle: your moves deal 30% more.
    SPIRE_RELIC_LAVA_COOKIE, // common: Super-effective hits on your team deal 20% less. Crunchy armor.
    SPIRE_RELIC_HP_UP, // common: +8% max HP for both your Pokémon. Tastes like chalk.
    SPIRE_RELIC_PP_MAX, // common: When you get it: two random moves are upgraded (+).
    SPIRE_RELIC_ORAN_BERRY, // common: After a battle, a Pokémon below 50% HP heals 12% more.
    SPIRE_RELIC_LEPPA_BERRY, // common: After every battle, each move gets 3 PP back.
    SPIRE_RELIC_LUCK_INCENSE, // common: Gambles in events succeed 20% more often than the odds say.
    SPIRE_RELIC_X_DEFENSE, // uncommon: Both your Pokémon start every battle with +1 Defense.
    SPIRE_RELIC_X_SP_DEF, // uncommon: Both your Pokémon start every battle with +1 Sp. Def.
    SPIRE_RELIC_RUSTED_SHIELD, // uncommon: DEFEND on both Pokémon gives each 85% of the Block instead of 60%.
    SPIRE_RELIC_BERSERK_GENE, // uncommon: Below 50% HP, your Pokémon deal 25% more damage.
    SPIRE_RELIC_REAPER_CLOTH, // uncommon: Your moves deal 25% more to foes with a status condition.
    SPIRE_RELIC_POKE_FLUTE, // uncommon: Resting at camp also upgrades a random move. Snorlax hates it.
    SPIRE_RELIC_UP_GRADE, // uncommon: Upgrading at camp also upgrades a second, random move.
    SPIRE_RELIC_TM_CASE, // uncommon: Better move rewards: 25% rare and 45% uncommon (normally 10/30).
    SPIRE_RELIC_SWEET_HEART, // uncommon: Skip a move reward (B) and both Pokémon get +3% max HP instead.
    SPIRE_RELIC_FOCUS_BAND, // uncommon: A Pokémon fighting alone deals 30% more damage and takes 20% less.
    SPIRE_RELIC_HYPER_POTION, // uncommon: Before every boss battle, heal 30% HP.
    SPIRE_RELIC_SCANNER, // uncommon: Your super-effective hits deal 25% more damage.
    SPIRE_RELIC_X_ATTACK, // rare: Both your Pokémon start elite and boss battles with +1 Attack.
    SPIRE_RELIC_X_SP_ATK, // rare: Both your Pokémon start elite and boss battles with +1 Sp. Atk.
    SPIRE_RELIC_SHED_SHELL, // rare: Block no longer vanishes at the end of a turn: half of it stays.
    SPIRE_RELIC_RESIST_FEATHER, // rare: Once per battle, each Pokémon survives a knockout hit with 1 HP.
    SPIRE_RELIC_ACRO_BIKE, // rare: 3 times: hop to any room on the next floor, path or no path.
    SPIRE_RELIC_RAZOR_CLAW, // rare: Your critical hits deal 2x damage instead of 1.5x.
    SPIRE_RELIC_IRON_BALL, // rare: Every hit on your team does 2% of max HP less. Heavy, but worth it.
    SPIRE_RELIC_RAINBOW_PASS, // shop: Everything in the Poké Mart costs 30% less.
    SPIRE_RELIC_HEART_SCALE, // shop: The Move Relearner always costs 25¥. It is in love.
    SPIRE_RELIC_BIG_MALASADA, // shop: When you get it: +10% max HP and a full heal. Alolan cardio.
    SPIRE_RELIC_AWAKENING, // boss: Your Pokémon deal 20% more damage. No more resting at camp.
    SPIRE_RELIC_RELIC_CROWN, // boss: Start every battle with +1 Attack and +1 Sp. Atk. Battles pay no money.
    SPIRE_RELIC_ODD_KEYSTONE, // boss: Start every battle with +1 Defense and +1 Sp. Def. All intents read ???.
    SPIRE_RELIC_METEORITE, // boss: Your Pokémon deal 35% more damage, but also take 15% more.
    SPIRE_RELIC_DUBIOUS_DISC, // boss: Your team takes 20% less damage. Porygon2 refuses to upgrade moves.
    SPIRE_RELIC_MAX_MUSHROOMS, // boss: +25% max HP for both Pokémon. No more healing after battles.
    SPIRE_RELIC_STAR_PIECE, // boss: Elites give two relic rewards instead of one.
    SPIRE_RELIC_GRACIDEA, // boss: Every new act fully heals your team (normally 40%).
    SPIRE_RELIC_COUNT,
};

enum SpireRelicTier
{
    SPIRE_RELIC_TIER_COMMON,
    SPIRE_RELIC_TIER_UNCOMMON,
    SPIRE_RELIC_TIER_RARE,
    SPIRE_RELIC_TIER_SHOP,
    SPIRE_RELIC_TIER_BOSS,
    SPIRE_RELIC_TIER_COUNT,
};

#endif // GUARD_SPIRE_RELICS_H
