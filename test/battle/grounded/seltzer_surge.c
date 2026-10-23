#include "global.h"
#include "test/battle.h"

// Project Grounded: Seltzer Surge (TM51) - 80 power, 20% Speed -1, 10% confusion, raakt alleen beide tegenstanders (niet de partner, anders dan Surf).
SINGLE_BATTLE_TEST("Seltzer Surge lowers the target's Speed 20% of the time")
{
    PASSES_RANDOMLY(20, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_SELTZER_SURGE, MOVE_EFFECT_STAT_MINUS) == TRUE);
        ASSUME(GetMovePower(MOVE_SELTZER_SURGE) == 80);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SELTZER_SURGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SELTZER_SURGE, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, opponent);
        MESSAGE("The opposing Wobbuffet's Speed fell!");
    }
}

SINGLE_BATTLE_TEST("Seltzer Surge confuses the target 10% of the time")
{
    PASSES_RANDOMLY(10, 100, RNG_SECONDARY_EFFECT_2);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_SELTZER_SURGE, MOVE_EFFECT_CONFUSION) == TRUE);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SELTZER_SURGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SELTZER_SURGE, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}

DOUBLE_BATTLE_TEST("Seltzer Surge hits both opponents but not the user's partner")
{
    GIVEN {
        ASSUME(GetMoveTarget(MOVE_SELTZER_SURGE) == TARGET_BOTH);
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_SELTZER_SURGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SELTZER_SURGE, playerLeft);
        HP_BAR(opponentLeft);
        HP_BAR(opponentRight);
        NOT HP_BAR(playerRight);
    }
}
