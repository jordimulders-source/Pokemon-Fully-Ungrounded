#include "global.h"
#include "test/battle.h"

// Project Grounded: Vintage Spill (TM53) - 60 power; confusion 50% bij de eerste treffer,
// 100% vanaf de tweede treffer op hetzelfde doelwit. De teller verdwijnt als het doelwit wisselt.
SINGLE_BATTLE_TEST("Vintage Spill confuses the target 50% of the time on the first hit")
{
    PASSES_RANDOMLY(50, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_VINTAGE_SPILL, MOVE_EFFECT_CONFUSION) == TRUE);
        ASSUME(GetMovePower(MOVE_VINTAGE_SPILL) == 60);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_VINTAGE_SPILL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_VINTAGE_SPILL, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}

SINGLE_BATTLE_TEST("Vintage Spill always confuses from the second hit on, even with other moves in between")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_VINTAGE_SPILL, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_VINTAGE_SPILL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_VINTAGE_SPILL, player);
        NOT ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, player);
        NOT ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_VINTAGE_SPILL, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}

SINGLE_BATTLE_TEST("Vintage Spill's confusion chance resets when the target switches out")
{
    PASSES_RANDOMLY(50, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { MOVE(player, MOVE_VINTAGE_SPILL, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
        TURN { SWITCH(opponent, 1); }
        TURN { SWITCH(opponent, 0); MOVE(player, MOVE_VINTAGE_SPILL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_VINTAGE_SPILL, player);
        NOT ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_VINTAGE_SPILL, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}
