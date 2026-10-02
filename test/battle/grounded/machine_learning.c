#include "global.h"
#include "test/battle.h"

// Project Grounded: Machine Learning - Electric status. Opeenvolgende beurten: 1, 2, 3 en daarna alle 5 stats +1
// (hoogste basisstats eerst). 20% kans op hallucinatie: dan een willekeurige move.
ASSUMPTIONS
{
    ASSUME(GetMoveEffect(MOVE_MACHINE_LEARNING) == EFFECT_MACHINE_LEARNING);
}

SINGLE_BATTLE_TEST("Machine Learning raises 1, 2, 3 and then all stats on consecutive turns")
{
    GIVEN {
        PLAYER(SPECIES_PORYGON) { Moves(MOVE_MACHINE_LEARNING); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
    } SCENE {
        MESSAGE("Porygon finished\ntraining epoch 1!");
        MESSAGE("Porygon finished\ntraining epoch 4!");
    } THEN {
        // 1 + 2 + 3 + 5 = 11 boosts over vijf stats: de hoogste basisstats het vaakst
        EXPECT_EQ(player->statStages[STAT_ATK] + player->statStages[STAT_DEF] + player->statStages[STAT_SPATK]
                + player->statStages[STAT_SPDEF] + player->statStages[STAT_SPEED] - 5 * DEFAULT_STAT_STAGE, 11);
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
    }
}

SINGLE_BATTLE_TEST("Machine Learning starts over after using another move")
{
    GIVEN {
        PLAYER(SPECIES_PORYGON) { Moves(MOVE_MACHINE_LEARNING, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, FALSE)); }
    } SCENE {
        MESSAGE("Porygon finished\ntraining epoch 1!");
        MESSAGE("Porygon finished\ntraining epoch 1!");
    }
}

SINGLE_BATTLE_TEST("Machine Learning can hallucinate into a random move")
{
    GIVEN {
        PLAYER(SPECIES_PORYGON) { Moves(MOVE_MACHINE_LEARNING); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_MACHINE_LEARNING, WITH_RNG(RNG_MACHINE_LEARNING, TRUE)); }
    } SCENE {
        MESSAGE("Porygon used Machine Learning!");
        MESSAGE("Porygon hallucinated!\nIt confidently did something else!");
        NOT MESSAGE("Porygon finished\ntraining epoch 1!");
    }
}
