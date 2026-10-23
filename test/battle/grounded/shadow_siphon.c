#include "global.h"
#include "test/battle.h"

// Project Grounded: Shadow Siphon - Dark-versie van Draining Kiss (50 BP, herstelt 75% van de schade).
SINGLE_BATTLE_TEST("Shadow Siphon restores 75% of the damage dealt")
{
    s16 damage, healed;
    GIVEN {
        ASSUME(GetMoveType(MOVE_SHADOW_SIPHON) == TYPE_DARK);
        ASSUME(MoveHasAdditionalEffect(MOVE_SHADOW_SIPHON, MOVE_EFFECT_ABSORB));
        PLAYER(SPECIES_WOBBUFFET) { HP(1); Moves(MOVE_SHADOW_SIPHON); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_SHADOW_SIPHON); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SHADOW_SIPHON, player);
        HP_BAR(opponent, captureDamage: &damage);
        HP_BAR(player, captureDamage: &healed);
    } THEN {
        EXPECT_MUL_EQ(damage, Q_4_12(-0.75), healed);
    }
}
