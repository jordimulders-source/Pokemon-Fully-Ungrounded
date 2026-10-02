#include "global.h"
#include "test/battle.h"

// Project Grounded: Lager Lagoon (TM52) - bier-Surf: 65 power, 50% confusion, raakt iedereen naast de gebruiker (ook de partner).
SINGLE_BATTLE_TEST("Lager Lagoon confuses the target 50% of the time")
{
    PASSES_RANDOMLY(50, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_LAGER_LAGOON, MOVE_EFFECT_CONFUSION) == TRUE);
        ASSUME(GetMovePower(MOVE_LAGER_LAGOON) == 65);
        ASSUME(GetMoveType(MOVE_LAGER_LAGOON) == TYPE_WATER);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_LAGER_LAGOON); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LAGER_LAGOON, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}

DOUBLE_BATTLE_TEST("Lager Lagoon hits both opponents and the user's partner")
{
    GIVEN {
        ASSUME(GetMoveTarget(MOVE_LAGER_LAGOON) == MOVE_TARGET_FOES_AND_ALLY);
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_LAGER_LAGOON); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LAGER_LAGOON, playerLeft);
        HP_BAR(opponentLeft);
        HP_BAR(playerRight);
        HP_BAR(opponentRight);
    }
}
