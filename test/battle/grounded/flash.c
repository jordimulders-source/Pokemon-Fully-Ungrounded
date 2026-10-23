#include "global.h"
#include "test/battle.h"

// Project Grounded: Flash is een statusmove die Accuracy, Attack en Sp. Atk van het doelwit verlaagt.
SINGLE_BATTLE_TEST("Flash lowers the target's Accuracy, Attack and Sp. Atk")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_FLASH) == EFFECT_STAT_CHANGE);
        ASSUME(GetMoveCategory(MOVE_FLASH) == DAMAGE_CATEGORY_STATUS);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_FLASH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FLASH, player);
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, opponent); // 1.17: alle stats in een keer
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ACC], DEFAULT_STAT_STAGE - 1);
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE - 1);
        EXPECT_EQ(opponent->statStages[STAT_SPATK], DEFAULT_STAT_STAGE - 1);
    }
}

SINGLE_BATTLE_TEST("Flash hits Ghost types because it is a status move")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GASTLY);
    } WHEN {
        TURN { MOVE(player, MOVE_FLASH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FLASH, player);
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ACC], DEFAULT_STAT_STAGE - 1);
    }
}
